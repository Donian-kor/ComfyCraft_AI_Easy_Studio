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

# 완료 발화 — 이미지 카드 위 말풍선이 말하는 한 마디. 여기 한 곳에서만 정의하고
# 컨트롤러의 TEMPLATES["done"] 이 이 값을 그대로 쓴다(같은 말이 두 갈래로
# 갈라지지 않도록).
SAY_DONE = "다 그렸어요! 어때요?"

# 레거시 완료 발화 판별 표식. 예전 버전은 완료 문장을 카드 아래 별도 text
# 메시지로 저장했다. 그 문구는 항상 이 두 말 중 하나로 끝나는 형태였으므로,
# 다른 AI 안내(모델 변경/옵션 초기화/수정 재요청)와 혼동하지 않는다.
_LEGACY_DONE_MARKERS = ("완성했어요", "그렸어요")


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

    # -- AI 발화(카드 위 말풍선) ------------------------------------------
    @property
    def say(self) -> str:
        """카드 위에 AI 가 말하는 문구 (없으면 빈 문자열).

        카드는 '무엇을 하고 있는가'(연결 확인/샘플링/중단 중)를 보여주고,
        이 문구는 '지금 내가 뭘 하는지'를 사람 말투로 말한다. 둘은 별개다.
        """
        return str(self.metadata.get("say", "") or "")

    @say.setter
    def say(self, value: str) -> None:
        text = str(value or "")
        if text:
            self.metadata["say"] = text
        else:
            self.metadata.pop("say", None)

    def has_say(self) -> bool:
        return bool(self.say)

    def become_image(self, image_path: str, meta: str = "", prompt: str = "",
                     snapshot: Optional[Dict[str, Any]] = None,
                     say: str = "") -> None:
        """생성 중 카드가 이미지 카드로 바뀐다 (kind 자체가 교체).

        새 메시지를 만들지 않고 이 메시지를 전환하므로 화면 위치가 유지된다.

        say 를 주면 진행 중이던 AI 발화 문구를 이어받는다. 생성이 끝났다고
        발화가 사라지면 카드 위 말풍선이 빈자리로 남으므로, 완료 문구로
        교체해 "빈 말풍선 + 아래 새 말풍선" 이 중복으로 뜨는 것을 막는다.
        주지 않으면(레거시 경로) 발화 없이 카드만 남는다.
        """
        self.kind = KIND_IMAGE
        # metadata 를 통째로 교체하므로 이전 진행 발화(say)는 자연히 제거된다.
        self.metadata = {
            "image_path": image_path,
            "meta": meta,
            "prompt": prompt,
            "snapshot": dict(snapshot or {}),
        }
        if str(say or "").strip():
            self.metadata["say"] = str(say)

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


def _looks_like_legacy_done(message: "ChatMessageData") -> bool:
    """레거시 완료 발화(= 카드 아래에 따로 붙던 AI 한마디)인지 판별한다."""
    if message.kind != KIND_TEXT or message.role != "ai":
        return False
    text = message.text.strip()
    return any(text.endswith(marker) or marker in text
               for marker in _LEGACY_DONE_MARKERS)


def _absorb_legacy_done(messages: List["ChatMessageData"]) -> List["ChatMessageData"]:
    """레거시 세션의 '완료 발화 text 메시지'를 이미지 카드 말풍선으로 옮긴다.

    예전 버전은 진행 중이던 AI 발화를 이미지 카드로 넘기면서 지우고, 완료
    문장을 카드 아래 별도 text 메시지로 만들었다. 그래서 저장된 세션에는
    (say 없는 이미지 카드) + (그 아래 완료 문구) 가 붙어 있었다. 지금은
    진행 발화가 그대로 물려받아 말풍선에서 제자리 교체되므로, 과거 기록도
    같은 모양으로 되돌려야 한다 — 아니면 예전 세션만 말풍선이 없고,
    중복 발화까지 보인다.
    """
    out: List["ChatMessageData"] = []
    index = 0
    total = len(messages)
    while index < total:
        message = messages[index]
        # 이미지 카드가 말풍선을 갖고 있으면 이미 최신 형식이다.
        if message.kind == KIND_IMAGE and not message.say:
            follow = index + 1
            if (follow < total
                    and _looks_like_legacy_done(messages[follow])):
                # 진행 중이던 발화와 같은 톤으로 통일한다. 모델명·소요시간은
                # 카드 메타 줄에 이미 있으므로 되풀이하지 않는다.
                message.metadata["say"] = SAY_DONE
                index = follow + 1     # 흡수한 완료 발화는 건너뛴다
                out.append(message)
                continue
        out.append(message)
        index += 1
    return out


def messages_from_raw(raw_list: Any) -> List[ChatMessageData]:
    """레거시/신규 혼합 세션의 messages 를 dataclass 리스트로 변환.

    로드 시점에 레거시 완료 발화 마이그레이션까지 적용하므로, 예전 세션도
    신규 세션과 같은 화면(카드 위 말풍선 1개, 중복 없음)이 된다.
    """
    if not isinstance(raw_list, list):
        return []
    out: List[ChatMessageData] = []
    for raw in raw_list:
        message = ChatMessageData.from_dict(raw)
        if message is not None:
            out.append(message)
    return _absorb_legacy_done(out)


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
