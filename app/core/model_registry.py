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
        """프로필 JSON을 읽어 등록한다 (P13: 단일 파일 + 스키마 검증).

        이전에는 json/·workflows/·model_profiles_json/ 폴더의 *.json을 전부 훑었는데,
        그 결과 설정 파일(app_config.json)의 최상위 키(ui, cache, workflow 등)와
        배열 인덱스(1, 2, 3 …)가 모델 프로필로 잘못 등록되었다.
        4cut 방식대로 "프로필 파일"만 읽고, 스키마를 통과한 항목만 받는다.
        """
        base_dir: Path = Path(__file__).resolve().parent.parent.parent
        # (폴더, 파일명) 목록 — 워크플로우/설정 JSON은 절대 포함하지 않는다.
        sources: List[Tuple[Path, str]] = [
            (base_dir / "workflows", "default_profiles.json"),
            (base_dir / "json", "default_profiles.json"),
            (base_dir / "model_profiles_json", "default_profiles.json"),
        ]
        # 사용자가 설정창에서 직접 저장한 수동 프로필은 전부 등록 대상이다.
        manual_dir: Path = base_dir / "model_profiles_json"
        if manual_dir.exists():
            sources.extend(
                (manual_dir, path.name)
                for path in sorted(manual_dir.glob("*.json"))
                if path.name != "default_profiles.json"
            )

        for folder, file_name in sources:
            file_path = folder / file_name
            if not file_path.is_file():
                continue
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
            except (OSError, ValueError):
                continue
            for profile in self._profiles_from_payload(payload):
                self.register(profile)

    def _profiles_from_payload(self, payload) -> List[ModelProfile]:
        """JSON 페이로드에서 프로필 스키마를 만족하는 항목만 뽑는다.

        스키마: dict 안에 각 값이 dict이며 "patterns" 또는 "workflow_type"을 갖고,
        최소 1개 이상의 패턴이 있어야 한다. 설정 파일의 임의 키는 걸러진다.
        """
        result: List[ModelProfile] = []
        if not isinstance(payload, dict):
            return result
        for profile_name, profile_data in payload.items():
            if not isinstance(profile_data, dict):
                continue
            if not self._looks_like_profile(profile_data):
                continue
            result.append(ModelProfile(
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
                workflow_file=str(profile_data.get("workflow_file", "") or ""),
            ))
        return result

    @staticmethod
    def _looks_like_profile(data: dict) -> bool:
        """프로필 스키마인지 판별한다 (설정/워크플로우 JSON 오인 방지)."""
        patterns = data.get("patterns")
        has_patterns = isinstance(patterns, (list, tuple)) and len(patterns) > 0
        if not has_patterns:
            return False
        return "workflow_type" in data or "default_steps" in data

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

    def is_zanime(self, model_name: str) -> bool:
        """zanime 계열 모델인지 판별한다. (중복 방지를 위한 통합 로직)"""
        profile = self.detect(model_name)
        lowered = (model_name or "").lower()
        return bool(
            "z-anime" in lowered
            or "zanime" in lowered
            or "z_anime_base" in lowered
            or "anime_aio" in lowered
            or profile.family == "zanime"
            or profile.name == "zanime_aio"
        )

    def is_flux(self, model_name: str) -> bool:
        """Flux 계열 모델인지 판별한다."""
        from app.core.workflow_manager import get_workflow_manager
        profile = self.detect(model_name)
        return bool(
            profile.workflow_type == "flux_gguf"
            or get_workflow_manager().is_flux_model(model_name)
            or profile.family == "flux"
        )

    def is_zimage(self, model_name: str) -> bool:
        """ZImage 계열 모델인지 판별한다."""
        from app.core.workflow_manager import get_workflow_manager
        profile = self.detect(model_name)
        return bool(
            get_workflow_manager().is_zimage_model(model_name)
            or profile.workflow_type == "zimage"
        )

    def is_ernie(self, model_name: str) -> bool:
        """ERNIE 계열 모델인지 판별한다."""
        profile = self.detect(model_name)
        return bool(profile.family == "ernie")

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
