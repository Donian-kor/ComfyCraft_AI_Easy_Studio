"""Flet 앱 실행 진입점 (Phase 4).

    python main.py

Flet 만 이 파일에서 시작된다. Application/Feature/Core 는 이 모듈을
import 하지 않는다.
"""

from __future__ import annotations

import flet as ft

from app.logging_config import setup_logging
from app.paths import BASE_DIR
from app.ui.flet import window_state
from app.ui.flet.app_state import AppState, set_ui_loop
from app.ui.flet.clipboard import attach_clipboard
from app.ui.flet.shell import AppShell
from app.ui.flet.theme.switcher import load_theme_mode
from app.ui.flet.theme.tokens import build_theme, flet_theme_mode

WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 900


def _saved_theme_mode() -> str:
    """저장된 테마를 읽어 적용한다. 실패하면 다크.

    컨트롤을 그리기 전에 불러와야 첫 화면부터 그 테마로 칠해진다.
    """
    from app.core.config_manager import get_config_manager

    return load_theme_mode(get_config_manager())


def main(page: ft.Page) -> None:
    """Flet 이 호출하는 앱 초기화 함수."""
    setup_logging()
    # 생성 Job 은 백그라운드 스레드에서 도므로, UI 갱신을 이 루프로 넘긴다.
    # (page.run_task 도 내부적으로 같은 루프를 쓴다)
    set_ui_loop(page.loop)
    # 클립보드 서비스는 페이지 컨텍스트 안에서 만들어야 등록된다.
    attach_clipboard()
    page.title = "ComfyCraft AI Easy Studio"
    # 저장해 둔 테마를 먼저 적용한다. 컨트롤을 그리기 전에 토큰을
    # 정해야 첫 화면부터 그 테마로 칠해진다.
    saved_mode = _saved_theme_mode()
    page.theme_mode = flet_theme_mode()
    page.theme = build_theme()
    page.bgcolor = None

    state = AppState()
    # 창 위치/크기 복원. 컨트롤을 만들기 전에 적용해야 첫 프레임부터
    # 사용자가 잡아 둔 크기로 뜬다.
    window_state.apply(page, state.services.config_manager)

    state.shell = AppShell(on_navigate=state.navigate,
                           on_new_chat=state.new_chat,
                           on_toggle_theme=state.toggle_theme,
                           on_open_help=lambda: state.navigate("/help"))
    state.shell.attach_page(page)
    # FaceDetailer 가이드 버튼 → 셸 다이얼로그. pages 는 셸을 모르고
    # 셸만 pages 를 아는 방향으로 배선한다(단방향 의존).
    state.studio.options.set_guide_handler(state.shell)

    page.add(state.shell.build())
    # 순서가 중요하다: 환영 인사를 *먼저* 넣고 화면을 그려야 한다.
    # (navigate() 가 page.build() 로 이미 만든 트리를 나중에 갱신하려 하면
    #  컨트롤이 아직 page 에 붙지 않아 safe_update 가 RuntimeError 를 삼키고
    #  인사가 화면에 반영되지 않는다. 그래서 start() 를 navigate() 보다 먼저.)
    state.start()
    state.navigate("/")

    page.on_disconnect = state.jobs.cancel_active
    page.on_route_change = _make_route_handler(state)
    page.on_keyboard_event = _make_keyboard_handler(state)
    # 창 위치/크기를 '끝날 때' 저장한다. resize/move 는 초당 수십 번
    # 불리므로 저장하지 않고, CLOSE 일 때만 한 번 저장한다.
    #
    # prevent_close=True 가 반드시 먼저다. 이 값이 False(기본값)면 OS 의
    # 닫기 신호가 on_event 로 올라오지 않아 저장이 영영 실행되지 않는다.
    page.window.prevent_close = True
    # 실제 창 크기를 추적한다. page.window.width 는 리사이즈를 반영하지
    # 않으므로, on_resize 로 받아야 사용자가 만든 크기가 저장된다.
    tracker = window_state.SizeTracker()
    page.on_resize = tracker.observe
    page.window.on_event = _make_window_close_handler(page, state, tracker)


def _make_route_handler(state: AppState):
    """라우트 변경(주소창 등)을 내부 탐색에 연결한다."""
    def handler(event: ft.Event) -> None:
        route = getattr(event, "route", "") or "/"
        if route:
            state.navigate(str(route))
    return handler


def _make_keyboard_handler(state: AppState):
    """전역 단축키 (원본 main_controller.eventFilter 대응).

    - ESC       → 생성 중단 (생성 중일 때만)
    - Ctrl+N    → 새 대화 시작 (생성 중이면 new_chat 이 거부한다)

    TextField 입력에는 손대지 않는다. 관찰만 하므로 한글 타이핑에 영향이 없고,
    전송 Enter 는 입력칸의 on_submit 이 그대로 맡는다.
    """
    def handler(event: ft.KeyboardEvent) -> None:
        key = str(getattr(event, "key", "") or "").upper()
        ctrl = bool(getattr(event, "ctrl", False))
        alt = bool(getattr(event, "alt", False))
        meta = bool(getattr(event, "meta", False))

        if key in ("ESC", "ESCAPE") and not (ctrl or alt or meta):
            # 생성 중일 때만 중단 버튼과 같은 동작. 평상시 ESC 는 아무 일도 없다.
            if state.jobs.is_busy:
                state.stop_generation()
        elif key == "N" and ctrl and not (alt or meta):
            state.new_chat()
    return handler


def _make_window_close_handler(page: ft.Page, state: AppState,
                               tracker: "window_state.SizeTracker"):
    """창이 닫힐 때 위치/크기를 저장하고, 실제로 창을 닫는다.

    왜 prevent_close 가 필요한가:
      Flet 의 Window.prevent_close 기본값은 False 다. False 면 OS 의
      닫기 신호를 on_event 로 *올려주지 않는다.* 그래서 CLOSE 를 기다리는
      방식으로는 저장이 영영 일어나지 않았다(조용히 실패).

      prevent_close=True 로 두면 닫기 신호가 on_event 로 올라오고,
      그때 저장한 뒤 직접 창을 닫아야 한다.

    run_task 는 coroutine function 만 받는다:
      예전 코드는 run_task(lambda: save(...)) 였는데 lambda 는
      coroutine 이 아니라 TypeError 였다. 여기서는 저장 자체가 동기라
      코루틴으로 감쌀 필요가 없다.
    """
    def handler(event) -> None:
        kind = getattr(getattr(event, "type", None), "value", None) \
            or getattr(event, "type", None)
        if str(kind or "") != "close":
            return
        # 저장부터 (끝나기 전에 확실히 끝내야 한다)
        window_state.save(page, state.services, tracker)
        # 그다음 실제로 닫는다. prevent_close 를 다시 내리지 않으면
        # 이 호출이 또 CLOSE 를 올려 무한 반복이 된다.
        #
        # 회귀 근거: Window.destroy() 는 coroutine 이다. 그냥 호출하면
        # 'coroutine was never awaited' 경고만 남고 실행이 안 된다.
        async def _finish_close() -> None:
            page.window.prevent_close = False
            await page.window.destroy()
        page.run_task(_finish_close)
    return handler


def run() -> None:
    """애플리케이션을 실행한다."""
    ft.run(main, assets_dir=str(BASE_DIR / "assets"))


if __name__ == "__main__":
    run()
