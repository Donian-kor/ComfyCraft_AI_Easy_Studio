"""이미지 생성 요청/결과/진행 상태 데이터 모델.

Phase 2: 기존 GenerationWorker(Qt Signal)에서 UI 의존을 끊어낸 순수 dataclass.
이 모듈은 flet 도 PySide6 도 import 하지 않는다.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

# --- 진행 상태 -------------------------------------------------------------
STATUS_IDLE = "idle"
STATUS_CONNECTING = "connecting"
STATUS_ENHANCING = "enhancing"
STATUS_SUBMITTING = "submitting"
STATUS_GENERATING = "generating"
STATUS_DONE = "done"
STATUS_FAILED = "failed"
STATUS_CANCELLED = "cancelled"


@dataclass
class FaceDetailerSettings:
    """FaceDetailer(안면 보정) 옵션. UI 에서 접어 표시하되 값은 그대로 보존한다."""

    enabled: bool = False
    denoise: float = 0.40
    steps: int = 20
    cfg: float = 4.0
    guide_size: int = 256
    max_size: int = 768
    feather: int = 5
    bbox_threshold: float = 0.50
    bbox_dilation: int = 10
    bbox_crop_factor: float = 1.50
    sam_detection_hint: str = "bbox"
    sam_dilation: int = 0
    sam_threshold: float = 0.93
    sam_bbox_expansion: int = 0
    sam_mask_hint_threshold: float = 0.70
    sam_mask_hint_use_negative: bool = False
    cycle: int = 1
    drop_size: int = 10

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items()}

    def to_legacy_dict(self) -> Dict[str, Any]:
        """레거시 스냅샷 키(facedetailer_ 접두사)로 펼친다."""
        return {f"facedetailer_{k}": v for k, v in self.__dict__.items()}

    @classmethod
    def from_dict(cls, raw: Optional[Dict[str, Any]]) -> "FaceDetailerSettings":
        """새 중첩 dict 와 레거시 평면 dict(facedetailer_ 접두사) 모두 받는다."""
        raw = raw or {}
        base = cls()
        known = set(base.to_dict())
        picked: Dict[str, Any] = {}

        for key, value in raw.items():
            name = key[len("facedetailer_"):] if key.startswith("facedetailer_") else key
            if name in known:
                picked[name] = value

        # 레거시는 "True"/"False" 문자열로 ComboBox 텍스트를 넘겨왔다.
        for flag in ("sam_mask_hint_use_negative",):
            if isinstance(picked.get(flag), str):
                picked[flag] = picked[flag].strip().lower() == "true"
        if isinstance(picked.get("sam_detection_hint"), str):
            picked["sam_detection_hint"] = picked["sam_detection_hint"].strip()

        return cls(**picked)


@dataclass
class GenerationRequest:
    """생성 1건에 필요한 모든 입력. UI 상태의 스냅샷 그 자체."""

    prompt: str = ""
    negative_prompt: str = ""
    enhanced_prompt: str = ""

    comfy_url: str = "http://127.0.0.1:8188"
    comfy_model: str = ""

    lm_url: str = "http://127.0.0.1:1234"
    lm_model: str = ""

    width: int = 1024
    height: int = 1024
    steps: int = 20
    cfg: float = 7.0
    seed: int = -1
    sampler: str = "euler"
    scheduler: str = "normal"
    denoise: float = 1.0

    zanime_style: str = ""
    filename_prefix: str = ""
    poll_interval_seconds: float = 1.0
    max_wait_seconds: int = 600

    facedetailer: FaceDetailerSettings = field(default_factory=FaceDetailerSettings)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "prompt": self.prompt,
            "negative_prompt": self.negative_prompt,
            "enhanced_prompt": self.enhanced_prompt,
            "comfy_url": self.comfy_url,
            "comfy_model": self.comfy_model,
            "lm_url": self.lm_url,
            "lm_model": self.lm_model,
            "width": self.width,
            "height": self.height,
            "steps": self.steps,
            "cfg": self.cfg,
            "seed": self.seed,
            "sampler": self.sampler,
            "scheduler": self.scheduler,
            "denoise": self.denoise,
            "zanime_style": self.zanime_style,
            "filename_prefix": self.filename_prefix,
            "poll_interval_seconds": self.poll_interval_seconds,
            "max_wait_seconds": self.max_wait_seconds,
            "facedetailer": self.facedetailer.to_dict(),
        }

    @classmethod
    def from_dict(cls, raw: Optional[Dict[str, Any]]) -> "GenerationRequest":
        """레거시 GenerationWorker 스냅샷(평면 dict)도 그대로 받는다.

        레거시 키 매핑:
          negative      -> negative_prompt
          enhance_prompt-> enhanced_prompt
          facedetailer_*-> facedetailer.<name>
        """
        raw = dict(raw or {})
        alias = {
            "negative": "negative_prompt",
            "enhance_prompt": "enhanced_prompt",
        }
        for old, new in alias.items():
            if old in raw and new not in raw:
                raw[new] = raw.pop(old)
            raw.pop(old, None)

        # 중첩 dict("facedetailer": {...}) 와 레거시 평면 키(facedetailer_*)를
        # 둘 다 읽는다. 중첩 dict 를 무시하면 '이 설정으로' 되돌리기가
        # FaceDetailer 값을 전부 초기화해 버린다.
        if isinstance(raw.get("facedetailer"), dict):
            facedetailer = FaceDetailerSettings.from_dict(raw.pop("facedetailer"))
        else:
            facedetailer = FaceDetailerSettings.from_dict(raw)
            for key in list(raw):
                if key.startswith("facedetailer_"):
                    raw.pop(key)

        base = cls()
        fields = {k: v for k, v in raw.items() if k in base.to_dict()}
        fields["facedetailer"] = facedetailer
        return cls(**fields)


@dataclass
class GenerationProgress:
    """생성 진행 이벤트. UI 는 이것만 보고 화면을 갱신한다."""

    status: str = STATUS_IDLE
    progress: int = 0
    message: str = ""
    log: str = ""
    preview: str = ""
    enhanced_prompt: str = ""
    elapsed_seconds: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "progress": self.progress,
            "message": self.message,
            "log": self.log,
            "preview": self.preview,
            "enhanced_prompt": self.enhanced_prompt,
            "elapsed_seconds": self.elapsed_seconds,
        }


@dataclass
class GenerationResult:
    """생성 최종 결과."""

    status: str = STATUS_FAILED
    image_path: str = ""
    prompt: str = ""
    meta: str = ""
    elapsed: float = 0.0
    model: str = ""
    width: int = 0
    height: int = 0
    seed: int = 0
    enhanced_prompt: str = ""
    snapshot: Dict[str, Any] = field(default_factory=dict)
    logs: list = field(default_factory=list)
    error: str = ""

    @property
    def ok(self) -> bool:
        return self.status == STATUS_DONE and bool(self.image_path)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "image_path": self.image_path,
            "prompt": self.prompt,
            "meta": self.meta,
            "elapsed": self.elapsed,
            "model": self.model,
            "width": self.width,
            "height": self.height,
            "seed": self.seed,
            "enhanced_prompt": self.enhanced_prompt,
            "snapshot": dict(self.snapshot),
            "logs": list(self.logs),
            "error": self.error,
        }


class StopToken:
    """생성 중단 요청을 담는 스레드 안전 플래그."""

    def __init__(self) -> None:
        self._event = threading.Event()

    def request_stop(self) -> None:
        self._event.set()

    def is_set(self) -> bool:
        return self._event.is_set()

    def reset(self) -> None:
        self._event.clear()


def new_monotonic() -> float:
    return time.monotonic()

    def from_dict(cls, raw: Optional[Dict[str, Any]]) -> "GenerationRequest":
        """레거시 GenerationWorker 스냅샷(평면 dict)도 그대로 받는다."""
        raw = dict(raw or {})
        if "facedetailer" in raw:
            facedetailer = FaceDetailerSettings.from_dict(raw.pop("facedetailer"))
        else:
            # 레거시는 facedetailer 옵션이 스냅샷 최상위에 펼쳐져 있었다.
            facedetailer = FaceDetailerSettings()
            known = set(facedetailer.to_dict())
            for key in list(raw):
                if key in known:
                    setattr(facedetailer, key, raw.pop(key))

        base = cls()
        fields = {k: v for k, v in raw.items() if k in base.to_dict()}
        fields["facedetailer"] = facedetailer
        return cls(**fields)

        raw = raw or {}
        base = cls()
        return cls(**{k: v for k, v in raw.items() if k in base.to_dict()})
