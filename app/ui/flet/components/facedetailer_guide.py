"""FaceDetailer(안면 보정) 초보자 가이드 다이얼로그 (P3-3).

원본 Qt 의 app/gui/dialogs/facedetailer_guide_dialog.py(show_facedetailer_guide)
를 Flet 로 이식한다. 내용은 도움말 화면이 이미 쓰는
assets/help/md/06_facedetailer.md 를 그대로 읽는다(문서가 한 벌뿐이어야
'어느 쪽이 최신인지' 알 수 있다).
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

import flet as ft

from app.paths import BASE_DIR
from app.ui.flet.theme.tokens import TOKENS

# 도움말 화면('안면 보정' 항목)이 쓰는 파일과 같은 문서.
GUIDE_PATH = Path(BASE_DIR) / "assets" / "help" / "md" / "06_facedetailer.md"


def show_facedetailer_guide(
    page: Optional[ft.Page],
    *,
    on_open_help: Optional[Callable[[], None]] = None,
) -> None:
    """안면 보정 가이드 다이얼로그를 연다.

    page 가 None 이면(헤드리스 테스트 등) 아무 것도 하지 않는다.
    """
    if page is None:
        return

    try:
        text = GUIDE_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        text = f"가이드 파일을 읽을 수 없습니다: {exc}"

    def open_help(_e: ft.Event) -> None:
        try:
            page.pop_dialog()
        except Exception:
            pass
        if on_open_help is not None:
            on_open_help()

    dialog = ft.AlertDialog(
        title=ft.Text("안면 보정 가이드", size=TOKENS.size_body),
        content=ft.Container(
            content=ft.Markdown(text, selectable=True),
            width=820, height=560),
        actions=[
            ft.TextButton("도움말에서 보기", on_click=open_help),
            ft.TextButton("닫기", on_click=lambda _e: page.pop_dialog()),
        ],
    )
    try:
        page.show_dialog(dialog)
    except Exception:
        # 헤드리스 환경에서는 열지 못해도 흐름을 막지 않는다
        pass
