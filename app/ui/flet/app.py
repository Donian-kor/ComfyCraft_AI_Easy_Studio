"""Flet 앱 실행 진입점 (Phase 4).

    python main.py

Flet 만 이 파일에서 시작된다. Application/Feature/Core 는 이 모듈을
import 하지 않는다.
"""

from __future__ import annotations

import flet as ft

from app.logging_config import setup_logging
from app.paths import BASE_DIR
from app.ui.flet.app_state import AppState
from app.ui.flet.shell import AppShell
from app.ui.flet.theme.tokens import build_theme

WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 900


def main(page: ft.Page) -> None:
    """Flet 이 호출하는 앱 초기화 함수."""
    setup_logging()
    page.title = "ComfyCraft AI Easy Studio"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = build_theme()
    page.bgcolor = None
    page.window.width = WINDOW_WIDTH
    page.window.height = WINDOW_HEIGHT
    page.window.min_width = 960
    page.window.min_height = 640

    state = AppState()
    state.shell = AppShell(on_navigate=state.navigate)
    state.shell.attach_page(page)

    page.add(state.shell.build())
    state.navigate("/")
    state.shell.set_status("무엇을 그려드릴까요?", "idle")

    page.on_disconnect = state.jobs.cancel_active
    page.on_route_change = _make_route_handler(state)


def _make_route_handler(state: AppState):
    """라우트 변경(주소창 등)을 내부 탐색에 연결한다."""
    def handler(event: ft.Event) -> None:
        route = getattr(event, "route", "") or "/"
        if route:
            state.navigate(str(route))
    return handler


def run() -> None:
    """애플리케이션을 실행한다."""
    ft.run(main, assets_dir=str(BASE_DIR / "assets"))


if __name__ == "__main__":
    run()
