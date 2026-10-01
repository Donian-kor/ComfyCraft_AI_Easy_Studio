"""모델 프로필을 생성 옵션 값으로 옮기는 로직.

options.py 가 600줄 제한에 걸리지 않도록, '프로필 → 슬라이더/드롭다운 값'
변환을 여기 뺀다. 이 모듈은 ModelProfile 을 알고 Flet 컨트롤은 모른다.
(Flet 를 import 하면 UI 계층 규칙을 어기므로 값만 다루고,
 실제로 값을 넣는 코드는 OptionsPanel.apply_model_defaults() 가 맡는다)
"""

from __future__ import annotations

from typing import Optional

from app.features.prompt.prompts import SCHEDULER_NAMES, SAMPLER_NAMES

# Flet Dropdown 의 value 는 반드시 옵션의 'key' 여야 화면에 표시된다.
# Sampler 드롭다운은 key=value(내부값 euler) / text=label(표시명)로 만들어져
# 있으므로, 여기서도 라벨이 아닌 내부값을 돌려줘야 한다.
# 라벨("Euler·선명함")을 주면 어떤 key 와도 매칭되지 않아 박스가 빈칸이 되고,
# to_request() 가 그 라벨을 sampler 이름으로 그대로 실어 보내게 된다.
_SAMPLER_VALUES = set(SAMPLER_NAMES.values())

# 네거티브 프롬프트 지원 판정은 app/features/prompt/prompts.py 가 소유한다.
# GenerationService(application 계층)도 같은 판정이 필요하기 때문이다.
# 여기서 로컬 사본을 두면 두 벌이 갈라져 판정이 어긋난다.
# 여기서는 UI 표시용으로 재노출만 한다.
from app.features.prompt.prompts import (  # noqa: E402
    model_supports_negative,
    resolve_negative_prompt,
)


def resolve_steps(profile) -> Optional[int]:
    """프로필의 권장 Steps (없으면 None)."""
    value = int(getattr(profile, "default_steps", 0) or 0)
    return value or None


def resolve_cfg(profile) -> Optional[float]:
    """프로필의 권장 CFG (없으면 None)."""
    value = float(getattr(profile, "default_cfg", 0) or 0)
    return value or None


def resolve_sampler(profile) -> str:
    """프로필의 샘플러 내부 값(euler 등)을 그대로 돌려준다.

    드롭다운의 key 와 같은 '내부값'을 줘야 박스에 정상 표시된다.
    목록에 없는 값이면 기본값 'euler' 로 떨어뜨린다(빈칸 방지).
    """
    sampler = str(getattr(profile, "sampler_name", "") or "")
    return sampler if sampler in _SAMPLER_VALUES else "euler"


def resolve_scheduler(profile) -> str:
    """프로필의 스케줄러. 모르는 값이면 'normal'."""
    scheduler = str(getattr(profile, "scheduler", "") or "")
    return scheduler if scheduler in SCHEDULER_NAMES else "normal"


def format_notice(profile, cfg: float, steps: int) -> str:
    """원본 Qt 의 '✓ ... 최적 설정 적용됨' 배지 문구."""
    name = str(getattr(profile, "name", "") or "").upper()
    return f"✓ {name} 최적 설정 적용됨 (CFG {cfg} / {steps}스텝)"
