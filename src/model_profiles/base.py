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
            "clip1": self.default_clip1,
            "clip2": self.default_clip2,
            "vae": self.default_vae,
            "default_steps": self.default_steps,
            "default_cfg": self.default_cfg,
            "sampler_name": self.sampler_name,
            "scheduler": self.scheduler,
        }
