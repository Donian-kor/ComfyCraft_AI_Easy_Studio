from __future__ import annotations

import importlib
from io import TextIOWrapper
import json
import pkgutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple

from app.core.config_manager import get_config_manager
from app.core.model_profiles.base import ModelProfile


@dataclass
class ModelRegistry:
    profiles: List[ModelProfile] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._register_builtin_profiles()
        self._register_json_profiles()

    def _register_builtin_profiles(self) -> None:
        for module_info in pkgutil.iter_modules(importlib.import_module("app.core.model_profiles").__path__):
            if module_info.name.startswith("_"):
                continue
            module: ModuleType = importlib.import_module(f"app.core.model_profiles.{module_info.name}")
            for value in vars(module).values():
                if isinstance(value, type) and issubclass(value, ModelProfile) and value is not ModelProfile:
                    profile: ModelProfile = value()
                    self.register(profile)

    def _register_json_profiles(self) -> None:
        base_dir: Path = Path(__file__).resolve().parent.parent.parent
        folders: List[Path] = [
            base_dir / "json",
            base_dir / "workflows",
            base_dir / "model_profiles_json",
        ]

        for folder in folders:
            if not folder.exists():
                continue

            for file_path in sorted(folder.glob("*.json")):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        payload = json.load(f)
                    if isinstance(payload, dict):
                        for profile_name, profile_data in payload.items():
                            if not isinstance(profile_data, dict):
                                continue
                            profile = ModelProfile(
                                name=profile_data.get("name", profile_name),
                                family=profile_data.get("family", profile_name),
                                aliases=tuple(profile_data.get("aliases", [])),
                                patterns=tuple(profile_data.get("patterns", [])),
                                workflow_type=profile_data.get("workflow_type", "checkpoint"),
                                default_clip1=profile_data.get("default_clip1", ""),
                                default_clip2=profile_data.get("default_clip2", ""),
                                default_vae=profile_data.get("default_vae", ""),
                                default_steps=int(profile_data.get("default_steps", 29)),
                                default_cfg=float(profile_data.get("default_cfg", 1.0)),
                                sampler_name=profile_data.get("sampler_name", "euler"),
                                scheduler=profile_data.get("scheduler", "normal"),
                                priority=int(profile_data.get("priority", 100)),
                            )
                            self.register(profile)
                    elif isinstance(payload, list):
                        for item in payload:
                            if not isinstance(item, dict):
                                continue
                            profile = ModelProfile(
                                name=item.get("name", "custom"),
                                family=item.get("family", item.get("name", "custom")),
                                aliases=tuple(item.get("aliases", [])),
                                patterns=tuple(item.get("patterns", [])),
                                workflow_type=item.get("workflow_type", "checkpoint"),
                                default_clip1=item.get("default_clip1", ""),
                                default_clip2=item.get("default_clip2", ""),
                                default_vae=item.get("default_vae", ""),
                                default_steps=int(item.get("default_steps", 29)),
                                default_cfg=float(item.get("default_cfg", 1.0)),
                                sampler_name=item.get("sampler_name", "euler"),
                                scheduler=item.get("scheduler", "normal"),
                                priority=int(item.get("priority", 100)),
                            )
                            self.register(profile)
                except Exception:
                    continue

    def register(self, profile: ModelProfile) -> None:
        if profile not in self.profiles:
            self.profiles.append(profile)
        self.profiles.sort(key=lambda p: p.priority)

    def detect(self, model_name: str) -> ModelProfile:
        if not model_name:
            return self._build_fallback_profile("generic")

        candidates: List[ModelProfile] = [p for p in self.profiles if p.matches(model_name)]
        if candidates:
            return sorted(candidates, key=lambda p: p.priority)[0]

        return self._build_fallback_profile(model_name)

    def _build_fallback_profile(self, model_name: str) -> ModelProfile:
        lowered: str = (model_name or "").lower()

        if "flux" in lowered:
            profile = ModelProfile(
                name="inferred_flux",
                family="flux",
                aliases=("flux",),
                patterns=("flux",),
                workflow_type="flux_gguf",
                default_clip1="clip_l.safetensors",
                default_clip2="t5-v1_1-xxl-encoder-Q4_K_M.gguf",
                default_vae="diffusion_pytorch_model.safetensors",
                default_steps=29,
                default_cfg=1.0,
                sampler_name="euler",
                scheduler="simple",
                priority=50,
            )
            if "dev" in lowered or "krea" in lowered:
                profile.default_steps = 29
                profile.default_cfg = 1
            else:
                profile.default_steps = 4
                profile.default_cfg = 1.0
            return profile

        if "zimage" in lowered or "z_image" in lowered:
            return ModelProfile(
                name="inferred_zimage",
                family="zimage",
                aliases=("zimage", "z_image"),
                patterns=("zimage", "z_image"),
                workflow_type="zimage",
                default_vae="diffusion_pytorch_model.safetensors",
                default_steps=8,
                default_cfg=1,
                sampler_name="dpmpp_2m",
                scheduler="karras",
                priority=60,
            )

        return ModelProfile(
            name="generic",
            family="generic",
            aliases=(),
            patterns=(),
            workflow_type="checkpoint",
            default_vae="ae.safetensors",
            default_steps=29,
            default_cfg=1.0,
            sampler_name="euler",
            scheduler="normal",
            priority=999,
        )

    def infer_from_directory(self, model_names: Iterable[str]) -> List[Tuple[str, ModelProfile]]:
        results: List[Tuple[str, ModelProfile]] = []
        for name in model_names:
            profile: ModelProfile = self.detect(name)
            results.append((name, profile))
        return results

    def discover_from_model_dirs(self, roots: Optional[Iterable[str]] = None) -> List[Tuple[str, ModelProfile]]:
        """ComfyUI 모델 폴더를 스캔해 파일명 기반으로 프로필을 자동 인식"""
        if roots is None:
            try:
                roots = [str(p) for p in get_config_manager().get_model_base_paths()]
            except Exception:
                roots = []

        discovered: List[Tuple[str, ModelProfile]] = []
        seen = set()
        supported_exts: set[str] = {".safetensors", ".ckpt", ".pt", ".bin", ".gguf", ".sft"}

        for root in roots:
            root_path: Path = Path(root).expanduser()
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file():
                    continue
                if path.suffix.lower() not in supported_exts:
                    continue
                name: str = path.name
                if name in seen:
                    continue
                seen.add(name)
                discovered.append((name, self.detect(name)))

        return discovered


_registry: Optional[ModelRegistry] = None


def get_model_registry() -> ModelRegistry:
    global _registry
    if _registry is None:
        _registry = ModelRegistry()
    return _registry
