"""모델 프로필 -> 사람이 읽는 표시명/특징 (원본 app/gui/chat_widgets.py 이식).

원본 Qt 의 PROFILE_SHORT / FAMILY_SHORT / PROFILE_FEATURE /
FAMILY_FEATURE 표와 describe_model() 을 그대로 옮긴다.

'프로필 -> 옵션 값' 변환(model_defaults.py)과 역할이 다르다. 여기는
'사람에게 보여줄 이름'만 만든다.

표 구조는 그대로 두는 이유가 있다. 키가 "ModelRegistry.detect() 가 돌려주는
profile.name" 이고, workflows/default_profiles.json 이 있으면 이름이
JSON 키(flux1-krea-dev 등)다. 내장 폴백 이름(flux_gguf 등)만 적어두면
조회가 실패해 family 로 폴백하고 같은 family 계열이 전부 같은 이름으로
뭉개진다(FLUX 2종이 구분 안 되던 문제). 그래서 JSON 이름을 먼저,
내장 이름을 뒤에 두는 순서가 의미를 가진다.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Set, Tuple

# 키는 'ModelRegistry.detect() 가 돌려주는 profile.name' 이다.
# 표시명은 목록에만 쓰고, 내부 로직은 항상 정확한 파일명을 쓴다.
PROFILE_SHORT = {
    # -- workflows/default_profiles.json (실사용 경로, 이름 우선) --
    "flux1-krea-dev": "FLUX Krea",
    "flux1-schnell": "FLUX Schnell",
    "z_image_turbo": "ZImage",
    "z-anime-base-aio": "Z-Anime",
    "realvisxl_v5": "RealVisXL",
    "juggernautxl_ragnarok": "JuggernautXL",
    "ernie-aio-base": "ERNIE Base",
    "ernie-aio-turbo": "ERNIE Turbo",
    # -- 내장 프로필 (default_profiles.json 이 없을 때의 폴백) --
    "flux_gguf": "FLUX",
    "zimage_turbo": "ZImage",
    "zanime_aio": "Z-Anime",
}
FAMILY_SHORT = {
    "flux": "FLUX",
    "zimage": "ZImage",
    "zanime": "Z-Anime",
    "ernie": "ERNIE",
    "realvisxl": "RealVisXL",
    "juggernautxl": "JuggernautXL",
}
PROFILE_FEATURE = {
    # -- workflows/default_profiles.json --
    "flux1-krea-dev": "사실적·고품질",
    "flux1-schnell": "초고속·4스텝",
    "z_image_turbo": "빠른 생성",
    "z-anime-base-aio": "애니·웹툰",
    "realvisxl_v5": "사실적·고품질",
    "juggernautxl_ragnarok": "사실적·고품질",
    "ernie-aio-base": "정밀·네거티브 강함",
    "ernie-aio-turbo": "초고속·8스텝",
    # -- 내장 프로필 --
    "flux_gguf": "사실적·고품질",
    "zimage_turbo": "빠른 생성",
    "zanime_aio": "애니·웹툰",
}
FAMILY_FEATURE = {
    "flux": "사실적·고품질",
    "zimage": "빠른 생성",
    "zanime": "애니·웹툰",
    "ernie": "포스터·타이포",
    "realvisxl": "사실적·고품질",
    "juggernautxl": "사실적·고품질",
}


def describe_model(profile, filename: str,
                   used_shorts: Optional[Set[str]] = None) -> Tuple[str, str, str]:
    """프로필+파일명 -> (짧은 표시명, 특징, 툴팁).

    같은 표시명이 이미 쓰였으면 파일 이름 앞부분을 덧붙여 구분한다.
    """
    used_shorts = used_shorts if used_shorts is not None else set()
    stem = Path(filename).stem if filename else ""
    name = getattr(profile, "name", "") or ""
    family = getattr(profile, "family", "") or ""
    short = PROFILE_SHORT.get(name) or FAMILY_SHORT.get(family) or stem
    feature = (PROFILE_FEATURE.get(name) or FAMILY_FEATURE.get(family)
               or "범용 체크포인트")
    if short in used_shorts and stem:
        short = f"{short} ({stem[:14]})"
    used_shorts.add(short)
    tooltip = f"{filename} — {feature}" if filename else feature
    return short, feature, tooltip
