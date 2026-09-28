from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Sequence, Tuple


@dataclass
class ModelProfile:
    name: str
    family: str
    aliases: Sequence[str] = field(default_factory=tuple)
    patterns: Sequence[str] = field(default_factory=tuple)
    workflow_type: str = "checkpoint"
    default_clip1: str = ""
    default_clip2: str = ""
    default_vae: str = ""
    default_steps: int = 10
    default_cfg: float = 1
    sampler_name: str = "euler"
    scheduler: str = "normal"
    priority: int = 100
    # P13: 자동 생성된 커스텀 워크플로우 파일 경로(비어 있으면 workflow_type 기본 템플릿 사용)
    workflow_file: str = ""
    # 기준점(base) 이름 — workflows/base/<base>.json 과 1:1 대응.
    # 빈 값이면 workflow_type 으로 폴백한다.
    base: str = ""
    # 기준점 워크플로우의 자리표시자를 확정하는 값 (workflow_deriver 와 동일 키).
    # 수동 등록 다이얼로그에서 고른 값이 여기까지 실려와야 파생에 반영된다.
    clip_type: str = "stable_diffusion"
    text_class: str = "CLIPTextEncode"
    text_field: str = "text"
    guidance: float = 3.5

    def deriver_fields(self) -> dict:
        """workflow_deriver.build_derived() 가 쓰는 자리표시자 값."""
        return {
            "base": self.resolved_base(),
            "clip_type": self.clip_type,
            "text_class": self.text_class,
            "text_field": self.text_field,
            "guidance": self.guidance,
        }

    def matches(self, model_name: str) -> bool:
        if not model_name:
            return False
        lowered = model_name.lower()
        for token in self.aliases + tuple(self.patterns):
            if token and token.lower() in lowered:
                return True
        return False

    def select_clip(self, available_clips: Iterable[str]) -> str:
        """단일 CLIP 선택 (ZImage 등에서 사용)"""
        clips = list(available_clips)
        if not clips:
            return self.default_clip1 or ""
        if self.default_clip1 and self.default_clip1 in clips:
            return self.default_clip1
        return clips[0]

    def select_clip_pair(self, available_clips: Iterable[str]) -> Tuple[str, str]:
        clips = list(available_clips)
        if not clips:
            return "", ""
        default1 = self.default_clip1
        default2 = self.default_clip2

        if default1 and default1 in clips:
            clip1 = default1
        else:
            clip1 = clips[0]

        if default2 and default2 in clips:
            clip2 = default2
        elif len(clips) > 1:
            clip2 = clips[1]
        else:
            clip2 = clips[0]

        return clip1, clip2

    def select_vae(self, available_vaes: Iterable[str]) -> str:
        vaes = list(available_vaes)
        if self.default_vae and self.default_vae in vaes:
            return self.default_vae
        if vaes:
            return vaes[0]
        return self.default_vae or "ae.safetensors"

    def as_preset(self) -> dict:
        return {
            "type": self.workflow_type,
            "base": self.base or self.workflow_type,
            "clip1": self.default_clip1,
            "clip2": self.default_clip2,
            "vae": self.default_vae,
            "default_steps": self.default_steps,
            "default_cfg": self.default_cfg,
            "sampler_name": self.sampler_name,
            "scheduler": self.scheduler,
        }

    def resolved_base(self) -> str:
        """기준점 이름. base 가 비어 있으면 workflow_type 으로 폴백한다."""
        return (self.base or self.workflow_type or "checkpoint").strip()
