"""홈 = 원본의 챗봇 작업 화면 (StudioPage).

원본 main.ui 구조를 그대로 따른다.

    railFrame  │  옵션 패널  │  챗봇 대화
               │             │  ┌──────────────┐
    홈         │  모델       │  │ 카드 흐름     │
    옵션       │  LM 모델    │  │ 프롬프트→생성 │
    이력       │  해상도     │  │ →이미지       │
    ?          │  Seed       │  └──────────────┘
    설정       │  Steps/CFG  │  ┌──────────────┐
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

# 원본 좌측 레일 순서와 같다
RAIL_ITEMS = [
    ("홈", ft.Icons.HOME_OUTLINED, ft.Icons.HOME),
    ("옵션", ft.Icons.TUNE_OUTLINED, ft.Icons.TUNE),
    ("이력", ft.Icons.HISTORY, ft.Icons.HISTORY),
    ("도움말", ft.Icons.HELP_OUTLINE, ft.Icons.HELP),
    ("설정", ft.Icons.SETTINGS_OUTLINED, ft.Icons.SETTINGS),
]


class StudioPage:
    """챗봇 작업 화면: 좌측 옵션 + 우측 대화 + 하단 입력."""

    def __init__(self, *, on_send: Optional[Callable[[str], None]] = None,
                 on_stop: Optional[Callable[[], None]] = None,
                 on_rail: Optional[Callable[[str], None]] = None) -> None:
        self._on_send = on_send
        self._on_stop = on_stop
        self._on_rail = on_rail
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
        self._rail = self._build_rail()

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
    def _build_rail(self) -> ft.NavigationRail:
        return ft.NavigationRail(
            bgcolor=TOKENS.surface,
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=80,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(icon),
                    selected_icon=ft.Icon(selected),
                    label=label,
                )
                for label, icon, selected in RAIL_ITEMS
            ],
            on_change=self._handle_rail_change,
        )

    def _handle_rail_change(self, event: ft.Event) -> None:
        index = getattr(event.control, "selected_index", 0)
        if self._on_rail is None or not (0 <= index < len(RAIL_ITEMS)):
            return
        label = RAIL_ITEMS[index][0]
        # '홈'은 현재 화면이므로 다시 그리지 않는다
        if label != "홈" and self._on_rail is not None:
            self._on_rail(label)

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
        """레일 + 옵션 + 챗봇(대화/입력) 3분할."""
        return ft.Row(
            controls=[
                self._rail,
                ft.VerticalDivider(width=1, color=TOKENS.outline),
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
