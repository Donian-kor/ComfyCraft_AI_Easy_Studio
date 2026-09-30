"""클립보드 복사 도우미 (Flet 1.x Service API).

회귀 근거: Flet 1.0 에서 클립보드 API 가 바뀌어 **두 곳 모두 조용히 실패**했다.
    page.set_clipboard(text)      ← 1.0 에 없다 (설정 로그 탭의 '복사')
    ft.Clipboard.set_data(text)   ← 1.0 에 없다 (이미지 카드의 '경로 복사')
두 경로 다 예외를 삼키고 있어서 화면에는 "복사했습니다"라고만 보였다.

지금은 ft.Clipboard 서비스의 비동기 set() 을 UI 루프에서 실행한다.
Service 는 생성 시점의 페이지에 자동 등록되므로 앱 시작 시 안에서 만든다.
"""

from __future__ import annotations

from typing import Optional

import flet as ft

from app.ui.flet.ui_loop import run_on_ui

_service: Optional[ft.Clipboard] = None


def set_clipboard_service(service: Optional[ft.Clipboard]) -> None:
    """복사에 쓸 Clipboard 서비스를 등록한다 (테스트에서 교체할 수 있다)."""
    global _service
    _service = service


def attach_clipboard() -> Optional[ft.Clipboard]:
    """Clipboard 서비스를 만들어 등록한다.

    Service 는 **생성 시점의 페이지**에 자동 등록되므로 반드시
    main(page) 안에서 부른다. 페이지 컨텍스트가 없으면 등록되지 않아
    복사가 동작하지 않는다(false 를 주는 이유).
    """
    try:
        service = ft.Clipboard()
    except Exception:
        return None
    set_clipboard_service(service)
    return service


def copy_text(text: str) -> bool:
    """텍스트를 클립보드에 넣는다. 준비 전이거나 빈 값이면 False."""
    service = _service
    if service is None or not text:
        return False
    # set() 은 코루틴이다. run_on_ui 가 UI 스레드에서 실행한다
    # (등록된 루프가 없으면 조용히 넘어간다 — 테스트/초기화 안전).
    run_on_ui(lambda: service.set(text))
    return True
