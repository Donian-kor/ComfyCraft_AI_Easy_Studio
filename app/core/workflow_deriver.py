# -*- coding: utf-8 -*-
"""워크플로우 파생 생성기.

workflows/base/<base>.json (불변 기준점) + workflows/default_profiles.json (최적값)
→ workflows/models/<profile>.json (모델별 파생 워크플로우)

설계 원칙:
- base 파일은 절대 수정하지 않는다 (읽기 전용).
- 파생 파일에는 런타임 치환용 __PLACEHOLDER__ (모델명/프롬프트/해상도 등)를
  그대로 남기고, 모델마다 고정되는 값(인코더 종류, CLIP 타입, guidance)만
  지금 확정한다.
- 그래서 같은 base 를 쓰는 모델이 늘어나도 base 는 그대로다.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# 모델마다 고정되는 값 → base 안의 자리표시자
#   __TEXT_CLASS__  : 텍스트 인코더 노드 이름 (CLIPTextEncode / TextEncodeZImageOmni)
#   __TEXT_FIELD__  : 프롬프트 입력 필드명 (text / prompt)
#   __CLIP_TYPE__   : CLIPLoader 의 type (stable_diffusion / flux ...)
#   __GUIDANCE__    : FluxGuidance.guidance (숫자)
_FIXED_KEYS = ("__TEXT_CLASS__", "__TEXT_FIELD__", "__CLIP_TYPE__", "__GUIDANCE__")

# 런타임까지 남겨 둘 자리표시자 (생성 시점 값)
_RUNTIME_TOKENS = (
    "__MODEL_NAME__", "__POSITIVE_PROMPT__", "__NEGATIVE_PROMPT__",
    "__WIDTH__", "__HEIGHT__", "__SEED__", "__STEPS__", "__CFG__",
    "__SAMPLER_NAME__", "__SCHEDULER__", "__DENOISE__", "__FILENAME_PREFIX__",
    "__CLIP_NAME__", "__CLIP_NAME1__", "__CLIP_NAME2__", "__VAE_NAME__",
)


def base_dir(project_root: Optional[Path] = None) -> Path:
    root = Path(project_root) if project_root else Path(__file__).resolve().parent.parent.parent
    return root / "workflows" / "base"


def models_dir(project_root: Optional[Path] = None) -> Path:
    root = Path(project_root) if project_root else Path(__file__).resolve().parent.parent.parent
    return root / "workflows" / "models"


def load_base(base_name: str, project_root: Optional[Path] = None) -> Dict[str, Any]:
    """기준점 워크플로우를 읽는다 (없으면 예외)."""
    path = base_dir(project_root) / f"{base_name}.json"
    if not path.is_file():
        raise FileNotFoundError(f"기준점 워크플로우가 없습니다: {path.name}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not data:
        raise ValueError(f"기준점 워크플로우 형식이 올바르지 않습니다: {path.name}")
    return data


def _replace(obj: Any, mapping: Dict[str, Any]) -> Any:
    """dict 값/키와 리스트 원소까지 재귀 치환한다."""
    if isinstance(obj, str):
        return mapping.get(obj, obj)
    if isinstance(obj, dict):
        return {
            (mapping.get(k, k) if isinstance(k, str) else k): _replace(v, mapping)
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [_replace(item, mapping) for item in obj]
    return obj


def build_derived(profile: Dict[str, Any], project_root: Optional[Path] = None) -> Dict[str, Any]:
    """프로필 1개로 파생 워크플로우를 만든다 (런타임 플레이스홀더는 유지)."""
    base_name = str(profile.get("base", "") or "").strip()
    if not base_name:
        raise ValueError("프로필에 base 가 없습니다.")
    template = load_base(base_name, project_root)

    mapping = {
        "__TEXT_CLASS__": str(profile.get("text_class") or "CLIPTextEncode"),
        "__TEXT_FIELD__": str(profile.get("text_field") or "text"),
        "__CLIP_TYPE__": str(profile.get("clip_type") or "stable_diffusion"),
        "__GUIDANCE__": profile.get("guidance", 3.5),
    }
    return _replace(template, mapping)


def write_derived(name: str, profile: Dict[str, Any],
                  project_root: Optional[Path] = None) -> Path:
    """파생 워크플로우를 파일로 저장한다."""
    out_dir = models_dir(project_root)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{name}.json"
    data = build_derived(profile, project_root)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_profiles(project_root: Optional[Path] = None) -> Dict[str, Any]:
    root = Path(project_root) if project_root else Path(__file__).resolve().parent.parent.parent
    path = root / "workflows" / "default_profiles.json"
    return json.loads(path.read_text(encoding="utf-8"))


def build_all(project_root: Optional[Path] = None) -> list:
    """default_profiles.json 의 모든 모델에 대해 파생 워크플로우를 만든다."""
    profiles = load_profiles(project_root)
    created = []
    for name, profile in profiles.items():
        if not isinstance(profile, dict):
            continue
        created.append(write_derived(name, profile, project_root).name)
    logger.info("파생 워크플로우 %d개 생성: %s", len(created), created)
    return created


def assert_base_untouched(snapshot: Dict[str, str],
                          project_root: Optional[Path] = None) -> None:
    """기준점 파일이 생성 과정에서 변경되지 않았는지 확인한다."""
    for base_name, before in snapshot.items():
        path = base_dir(project_root) / f"{base_name}.json"
        after = path.read_text(encoding="utf-8")
        if before != after:
            raise RuntimeError(f"기준점 파일이 변경되었습니다: {path.name}")


def snapshot_bases(project_root: Optional[Path] = None) -> Dict[str, str]:
    """기준점 파일들의 현재 내용을 스냅샷한다 (불변 검증용)."""
    out: Dict[str, str] = {}
    for path in sorted(base_dir(project_root).glob("*.json")):
        out[path.stem] = path.read_text(encoding="utf-8")
    return out


if __name__ == "__main__":  # 수동 재생성: python -m app.core.workflow_deriver
    logging.basicConfig(level=logging.INFO)
    print("\n".join(build_all()))
