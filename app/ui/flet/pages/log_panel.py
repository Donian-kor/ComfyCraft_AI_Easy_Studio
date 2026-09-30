"""로그 창 (원본 settings_dialog.ui 의 tabLog: logTabEdit/Clear/Save/Copy).

원본은 Qt 의 QPlainTextEdit 에 로그 핸들러로 실시간을 흘려 넣었다.
Flet 에는 그 핸들러가 없으므로, 화면을 열 때 app.log 를 읽어 보여준다.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import List, Optional

import flet as ft

from app.paths import BASE_DIR
from app.ui.flet.components.common import section_card
from app.ui.flet.theme.tokens import TOKENS

LOG_PATH = BASE_DIR / "app.log"

# 화면에 함께 띄울 줄 수 (전부 띄우면 창이 무겁다)
MAX_LOG_LINES = 800


class LogPanel:
    """app.log 를 읽어 보여주는 창. 지우기/저장/복사를 제공한다."""

    def __init__(self, path: Optional[Path] = None) -> None:
        self._path = Path(path or LOG_PATH)
        self._text = ft.TextField(
            value="", multiline=True, min_lines=20, max_lines=28,
            read_only=True, expand=True,
            text_size=TOKENS.size_caption,
            border=ft.InputBorder.NONE,
            bgcolor=TOKENS.surface)
        self._status = ft.Text("", size=TOKENS.size_caption,
                               color=TOKENS.on_surface_variant)
        self._follow = ft.Switch(label="자동 갱신", value=True)
        self._last_size = -1

    # --- 읽기 -------------------------------------------------------------
    def _read_lines(self) -> List[str]:
        if not self._path.is_file():
            return []
        try:
            with open(self._path, "r", encoding="utf-8", errors="replace") as handle:
                lines = handle.readlines()
        except OSError:
            return []
        return lines[-MAX_LOG_LINES:]

    def refresh(self) -> None:
        """파일이 바뀌었으면 화면 텍스트를 갱신한다."""
        try:
            size = self._path.stat().st_size if self._path.is_file() else 0
        except OSError:
            size = 0
        if size == self._last_size:
            return
        self._last_size = size
        lines = self._read_lines()
        self._text.value = "".join(lines) if lines else "(아직 로그가 없습니다)"
        try:
            self._text.update()
        except RuntimeError:
            pass      # 아직 page 에 붙지 않은 상태

    def _handle_timer(self, _event: ft.Event) -> None:
        if self._follow.value:
            self.refresh()
        # 타이머는 한 번만 등록하고 계속 돌린다.
        if not self._timer_running:
            self._timer_running = True
            self._restart_timer()

    def _restart_timer(self) -> None:
        page = getattr(self._text, "page", None)
        if page is None:
            self._timer_running = False
            return
        try:
            import asyncio

            async def loop() -> None:
                while True:
                    await asyncio.sleep(POLL_SECONDS)
                    if not self._follow.value:
                        continue
                    try:
                        self.refresh()
                    except Exception:
                        pass

            asyncio.ensure_future(loop())
        except Exception:
            self._timer_running = False

    # --- 동작 -------------------------------------------------------------
    def clear(self, _event: Optional[ft.Event] = None) -> None:
        """화면 내용만 지운다 (원본 logClearBtn 과 같은 안전 동작)."""
        self._text.value = ""
        try:
            self._text.update()
        except RuntimeError:
            pass
        self._set_status("화면만 지웠습니다. (파일은 그대로입니다)")

    def save_as(self, _event: Optional[ft.Event] = None) -> None:
        """현재 로그를 다른 이름으로 저장한다."""
        stamp = time.strftime("%Y%m%d_%H%M%S")
        target = self._path.parent / f"app_log_{stamp}.txt"
        try:
            target.write_text(self._text.value or "", encoding="utf-8")
        except OSError as exc:
            self._set_status(f"저장 실패: {exc}")
            return
        self._set_status(f"저장했습니다: {target.name}")

    def copy(self, _event: Optional[ft.Event] = None) -> None:
        """클립보드에 복사한다.

        회귀 근거: 예전에는 page.set_clipboard() 를 썼는데 Flet 1.0 에 그
        메서드가 없어 예외로 빠졌다(버튼이 '복사 실패'로만 끝났다).
        지금은 앱 시작 시 등록한 Clipboard 서비스를 쓴다.
        """
        from app.ui.flet.clipboard import copy_text

        if not copy_text(self._text.value or ""):
            self._set_status("클립보드를 사용할 수 없습니다.")
            return
        self._set_status("클립보드에 복사했습니다.")

    def _set_status(self, message: str) -> None:
        self._status.value = message
        try:
            self._status.update()
        except RuntimeError:
            pass

    # --- 화면 -------------------------------------------------------------
    def build(self) -> ft.Control:
        self.refresh()
        return section_card(
            "로그",
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.OutlinedButton("지우기", icon=ft.Icons.CLEAR_ALL,
                                              on_click=self.clear),
                            ft.OutlinedButton("다른 이름으로 저장",
                                              icon=ft.Icons.SAVE_ALT,
                                              on_click=self.save_as),
                            ft.OutlinedButton("복사", icon=ft.Icons.COPY_ALL,
                                              on_click=self.copy),
                            self._follow,
                            ft.Container(expand=True),
                            ft.Text(str(self._path), size=TOKENS.size_caption,
                                    color=TOKENS.outline),
                        ],
                        spacing=TOKENS.space_md, tight=True),
                    self._text,
                    self._status,
                ],
                spacing=TOKENS.space_sm, tight=True),
            expand=True)
