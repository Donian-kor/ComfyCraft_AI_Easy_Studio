"""테마 전환의 '사용자 동작' 부분.

토큰 계산(색값, 재색칠)은 tokens.py 가 한다. 여기는 그 위에
'설정에 저장한다'는 것과 '저장된 값을 읽는다'만 맡는다.
AppState 가 이 두 함수를 불러 쓴다.
"""

from __future__ import annotations

from typing import Any

from app.ui.flet.theme.tokens import set_theme_mode, theme_mode


def load_theme_mode(config_manager: Any) -> str:
    """설정 파일에 저장된 테마를 읽어 화면에 적용한다. 적용된 모드를 돌려준다.

    컨트롤을 그리기 전에 불러와야 첫 화면부터 그 테마로 칠해진다.
    설정 파일이 없거나 깨졌으면 다크로 시작한다.
    """
    try:
        mode = config_manager.get().ui.theme.mode
    except Exception:
        mode = "dark"
    return set_theme_mode(mode)


def save_theme_mode(services: Any, mode: str) -> bool:
    """선택한 테마를 설정 파일에 남긴다. 성공 여부를 돌려준다.

    저장은 부가 기능이므로 실패해도 앱은 계속 돌아가야 한다.
    (테마 전환 자체는 이미 화면에 반영된 상태)
    """
    try:
        config = services.config
        config.ui.theme.mode = mode
        return bool(services.config_manager.save(config))
    except Exception:
        return False


def current_theme_mode() -> str:
    """지금 적용된 모드 이름. (테마가 없으면 다크)"""
    return theme_mode()
