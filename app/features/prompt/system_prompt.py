"""Feature 계층: 프롬프트 도메인 로직 (순수 Python, UI 프레임워크 금지)."""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional

# ZANIME 스타일 값 (app/constants.py 와 동일한 값)
ZANIME_STYLES = ("webtoon", "japanime", "basic")


def select_system_prompt(
    *,
    comfy_model_name: str,
    is_flux: bool,
    is_zimage: bool,
    is_ernie: bool,
    is_zanime: bool,
    zanime_style: str = "",
    use_korean: bool = True,
    ext_prompts: Optional[Dict[str, Any]] = None,
    log: Optional[Callable[[str], None]] = None,
) -> str:
    """ComfyUI 모델 계열에 맞는 시스템 프롬프트 지시문을 고른다.

    - zanime + 스타일 지정 : 스타일 전용 지시문
    - ERNIE                 : ERNIE 전용 지시문
    - Flux / ZImage / Zanime: 문장형(Flux) 지시문
    - 그 외 (SDXL 계열 등)  : 태그형(쉼표 구분) 지시문
    """
    ext = ext_prompts or {}
    emit = log or (lambda _msg: None)
    suffix = "kr" if use_korean else "en"
    fallback = ext.get(f"system_prompt_flux_{suffix}") or ext.get("system_prompt_sdxl_kr") or ""

    style = (zanime_style or "").strip().lower()
    if is_zanime and style in ZANIME_STYLES:
        keys = {
            "webtoon": f"system_prompt_zanime_webtoon_{suffix}",
            "japanime": f"system_prompt_zanime_anime_{suffix}",
            "basic": f"system_prompt_zanime_basic_{suffix}",
        }
        system_prompt = ext.get(keys[style]) or ""
        if not system_prompt:
            emit(f"[ZANIME 스타일] '{style}' 전용 지시문이 없어 기본 문장형 지시문으로 대체합니다.")
            return fallback
        emit(f"[ZANIME 스타일] '{style}' 스타일 프롬프트 지시문을 사용합니다.")
        return system_prompt

    if is_ernie:
        emit(f"[AI 자동 분석] '{comfy_model_name}' 모델 감지: 'ERNIE 전용' 프롬프트 지시문을 사용합니다.")
        return (ext.get(f"system_prompt_ernie_{suffix}") or fallback)

    if is_flux or is_zimage or is_zanime:
        emit(f"[AI 자동 분석] '{comfy_model_name}' 모델 감지: '문장형' 프롬프트 지시문을 사용합니다.")
        return (ext.get(f"system_prompt_flux_{suffix}") or "")

    emit(f"[AI 자동 분석] '{comfy_model_name}' 모델 감지: '태그형(쉼표 구분)' 프롬프트 지시문을 사용합니다.")
    return (ext.get(f"system_prompt_sdxl_{suffix}") or "")
