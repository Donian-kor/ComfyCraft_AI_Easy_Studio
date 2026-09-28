# -*- coding: utf-8 -*-
"""대화 데이터 모델.

세션 메시지가 채팅 화면의 유일한 진실이다. 위젯은 상태를 갖지 않는다.
카드 전환은 메시지의 kind/metadata 변경으로 표현되고, 화면은 언제든
render() 로 이 데이터로부터 다시 그릴 수 있다.

레거시 호환: 예전 세션 파일은 {"kind": "ai"|"user"|"system", "text": ...}
형식이었다. from_dict() 가 이를 role="ai", kind="text" 로 변환한다.
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

# --- kind 상수 -----------------------------------------------------------
KIND_TEXT = "text"
KIND_GENERATION = "generation"
KIND_IMAGE = "image"

# generation 카드의 진행 단계 (metadata["phase"])
PHASE_PROMPT = "prompt"            # 프롬프트 확인 카드
PHASE_GENERATING = "generating"    # 생성 중 카드
PHASE_FAILED = "failed"

_ROLE_KINDS = {"ai", "user", "system"}


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _new_id() -> str:
    return uuid.uuid4().hex[:12]


@dataclass
class ChatMessageData:
    """대화 메시지 1개. 위젯 상태가 아니라 데이터만 들고 있다."""

    id: str = field(default_factory=_new_id)
    role: str = "ai"
    kind: str = KIND_TEXT
    text: str = ""
    created_at: str = field(default_factory=_now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    # -- 생성 흐름 편의 성-API --------------------------------------------
    @property
    def phase(self) -> str:
        return str(self.metadata.get("phase", PHASE_PROMPT))

    @phase.setter
    def phase(self, value: str) -> None:
        self.metadata["phase"] = value

    def is_prompt_phase(self) -> bool:
        return self.kind == KIND_GENERATION and self.phase == PHASE_PROMPT

    def is_generating_phase(self) -> bool:
        return self.kind == KIND_GENERATION and self.phase == PHASE_GENERATING

    def become_image(self, image_path: str, meta: str = "", prompt: str = "",
                     snapshot: Optional[Dict[str, Any]] = None) -> None:
        """생성 중 카드가 이미지 카드로 바뀐다 (kind 자체가 교체).

        새 메시지를 만들지 않고 이 메시지를 전환하므로 화면 위치가 유지된다.
        """
        self.kind = KIND_IMAGE
        self.metadata = {
            "image_path": image_path,
            "meta": meta,
            "prompt": prompt,
            "snapshot": dict(snapshot or {}),
        }

    # -- 직렬화 ------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "id": self.id,
            "role": self.role,
            "kind": self.kind,
            "text": self.text,
            "created_at": self.created_at,
            "metadata": dict(self.metadata),
        }
        # 이미지 카드의 필드는 읽기 편하도록 최상위에도 함께 노출한다.
        # (구버전 코드·외부 도구가 record["image_path"] 로 읽는 경우 대응)
        if self.kind == KIND_IMAGE:
            payload["image_path"] = self.metadata.get("image_path", "")
            payload["meta"] = self.metadata.get("meta", "")
            payload["prompt"] = self.metadata.get("prompt", "")
            payload["snapshot"] = dict(self.metadata.get("snapshot", {}))
        return payload

    @classmethod
    def from_dict(cls, raw: Any) -> Optional["ChatMessageData"]:
        if not isinstance(raw, dict):
            return None
        kind = str(raw.get("kind", KIND_TEXT) or KIND_TEXT)
        role = str(raw.get("role", "ai") or "ai")
        # 레거시: kind 에 role 값이 들어있던 형식
        if kind in _ROLE_KINDS:
            role = kind
            kind = KIND_TEXT
        metadata = raw.get("metadata")
        if not isinstance(metadata, dict):
            metadata = {}
        if kind == KIND_IMAGE and not metadata:
            # 레거시 이미지 레코드는 필드가 최상위에 흩어져 있다.
            metadata = {
                "image_path": str(raw.get("image_path", "") or ""),
                "meta": str(raw.get("meta", "") or ""),
                "prompt": str(raw.get("prompt", "") or ""),
                "snapshot": dict(raw.get("snapshot") or {}),
            }
        return cls(
            id=str(raw.get("id") or _new_id()),
            role=role,
            kind=kind,
            text=str(raw.get("text", "") or ""),
            created_at=str(raw.get("created_at") or raw.get("timestamp")
                           or _now()),
            metadata=metadata,
        )


def messages_from_raw(raw_list: Any) -> List[ChatMessageData]:
    """레거시/신규 혼합 세션의 messages 를 dataclass 리스트로 변환."""
    if not isinstance(raw_list, list):
        return []
    out: List[ChatMessageData] = []
    for raw in raw_list:
        message = ChatMessageData.from_dict(raw)
        if message is not None:
            out.append(message)
    return out


def messages_to_raw(messages: List[ChatMessageData]) -> List[Dict[str, Any]]:
    return [m.to_dict() for m in messages]


@dataclass
class GenerationState:
    """현재 실행 중인 생성 1건의 컨텍스트 (세션과 무관한 런타임 상태).

    카드 위젯 참조를 갖지 않는다. 세션 전환 시 이 객체만 버리면 되고,
    화면은 세션 데이터로 다시 그려진다.
    """

    message_id: str = ""
    original_prompt: str = ""
    enhanced_prompt: str = ""
    started_monotonic: float = field(default_factory=time.monotonic)
