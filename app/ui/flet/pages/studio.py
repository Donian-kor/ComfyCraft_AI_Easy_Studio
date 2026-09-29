"""홈 = 원본의 챗봇 작업 화면 (StudioPage).

원본 main.ui 구조를 그대로 따른다. 단, 좌측 레일(railFrame)은
셸(AppShell)이 전역으로 하나만 둔다 — 여기서 또 만들면 화면에
사이드바가 두 개로 중복된다.

    셸의 레일  │  옵션 패널  │  챗봇 대화
                │             │  ┌──────────────┐
                │  모델       │  │ 카드 흐름     │
                │  LM 모델    │  │ 프롬프트→생성 │
                │  해상도     │  │ →이미지       │
                │  Seed       │  └──────────────┘
                │  Steps/CFG  │  ┌──────────────┐
                │  FaceDetail │  │ 입력창 + 전송 │  ← 이게 핵심
                └─────────────┘  └──────────────┘
"""

from __future__ import annotations

from typing import Callable, List, Optional

import flet as ft

from app.ui.flet.components.common import safe_update
from app.ui.flet.pages.chat import ChatPanel
from app.ui.flet.pages.options import OptionsPanel
from app.ui.flet.theme.tokens import TOKENS, radius


class StudioPage:
    """챗봇 작업 화면: 좌측 옵션 + 우측 대화 + 하단 입력."""

    def __init__(self, *, on_send: Optional[Callable[[str], None]] = None,
                 on_stop: Optional[Callable[[], None]] = None) -> None:
        self._on_send = on_send
        self._on_stop = on_stop
        self.options = OptionsPanel()
        self.chat = ChatPanel()

        self._prompt = ft.TextField(
            multiline=True, min_lines=1, max_lines=5,
            hint_text="그릴 장면을 설명해 주세요",
            border_radius=radius(TOKENS.radius_lg),
            bgcolor=TOKENS.surface_variant,
            on_submit=self._handle_submit,
        )
        self._send_button = ft.FilledButton(
            "전송", icon=ft.Icons.ARROW_UPWARD, on_click=self._handle_send)
        self._stop_button = ft.OutlinedButton(
            "중단", icon=ft.Icons.STOP_CIRCLE_OUTLINED, on_click=self._handle_stop,
            visible=False)
        self._hint = ft.Text(
            "Enter 로 전송 · Shift+Enter 로 줄바꿈",
            size=TOKENS.size_caption, color=TOKENS.outline)

    # --- 이벤트 ---------------------------------------------------------
    def _handle_send(self, _event: ft.Event) -> None:
        text = (self._prompt.value or "").strip()
        if not text:
            return
        self._prompt.value = ""
        safe_update(self._prompt)
        if self._on_send is not None:
            self._on_send(text)

    def _handle_submit(self, _event: ft.Event) -> None:
        self._handle_send(_event)

    def _handle_stop(self, _event: ft.Event) -> None:
        if self._on_stop is not None:
            self._on_stop()

    # --- 레이아웃 --------------------------------------------------------
    def _build_input_frame(self) -> ft.Control:
        return ft.Container(
            content=ft.Row(
                controls=[self._prompt, self._stop_button, self._send_button],
                spacing=TOKENS.space_sm,
                vertical_alignment=ft.CrossAxisAlignment.END,
            ),
            padding=ft.Padding.all(TOKENS.space_lg),
            bgcolor=TOKENS.surface,
        )

    def build(self) -> ft.Control:
        """옵션 패널 + 챗봇(대화/입력) 2분할.

        좌측 레일은 셸이 전역으로 하나만 둔다. 여기서 다시 만들면
        사이드바가 중복되므로 넣지 않는다.
        """
        return ft.Row(
            controls=[
                self.options.build(),
                ft.VerticalDivider(width=1, color=TOKENS.outline),
                ft.Column(
                    controls=[
                        ft.Container(content=self.chat.build(), expand=True),
                        self._build_input_frame(),
                    ],
                    expand=True,
                    spacing=0,
                    tight=True,
                ),
            ],
            expand=True,
            spacing=0,
            tight=True,
        )

    # --- 상태 ------------------------------------------------------------
    def set_busy(self, running: bool) -> None:
        """생성 중이면 전송을 막고 중단 버튼을 보여준다."""
        self._send_button.disabled = running
        self._stop_button.visible = running
        safe_update(self._send_button, self._stop_button)

    def set_hint(self, text: str) -> None:
        self._hint.value = text
        safe_update(self._hint)

    def focus_prompt(self) -> None:
        try:
            self._prompt.focus()
        except Exception:
            pass
