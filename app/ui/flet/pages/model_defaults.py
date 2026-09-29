"""모델 프로필을 생성 옵션 값으로 옮기는 로직.

options.py 가 600줄 제한에 걸리지 않도록, '프로필 → 슬라이더/드롭다운 값'
변환을 여기 뺀다. 이 모듈은 ModelProfile 을 알고 Flet 컨트롤은 모른다.
(Flet 를 import 하면 UI 계층 규칙을 어기므로 값만 다루고,
 실제로 값을 넣는 코드는 OptionsPanel.apply_model_defaults() 가 맡는다)
"""

from __future__ import annotations

from typing import Dict, Optional

from app.features.prompt.prompts import SCHEDULER_NAMES, SAMPLER_NAMES

# 프로필의 내부 값(euler) → 화면 표기(Euler)
_SAMPLER_LABELS: Dict[str, str] = {v: k for k, v in SAMPLER_NAMES.items()}


def resolve_steps(profile) -> Optional[int]:
    """프로필의 권장 Steps (없으면 None)."""
    value = int(getattr(profile, "default_steps", 0) or 0)
    return value or None


def resolve_cfg(profile) -> Optional[float]:
    """프로필의 권장 CFG (없으면 None)."""
    value = float(getattr(profile, "default_cfg", 0) or 0)
    return value or None


def resolve_sampler(profile) -> str:
    """프로필의 샘플러 내부 값을 화면 표기로 바꾼다.

    프로필은 'euler'(내부값), 드롭다운은 'Euler'(표기)를 쓴다.
    표에 없는 값이면 내부값을 그대로 준다(드롭다운에서 걸러낼 수 있다).
    """
    sampler = str(getattr(profile, "sampler_name", "") or "")
    return _SAMPLER_LABELS.get(sampler, sampler)


def resolve_scheduler(profile) -> str:
    """프로필의 스케줄러. 모르는 값이면 'normal'."""
    scheduler = str(getattr(profile, "scheduler", "") or "")
    return scheduler if scheduler in SCHEDULER_NAMES else "normal"


def format_notice(profile, cfg: float, steps: int) -> str:
    """원본 Qt 의 '✓ ... 최적 설정 적용됨' 배지 문구."""
    name = str(getattr(profile, "name", "") or "").upper()
    return f"✓ {name} 최적 설정 적용됨 (CFG {cfg} / {steps}스텝)"
