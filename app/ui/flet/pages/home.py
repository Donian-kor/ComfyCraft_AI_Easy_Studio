"""홈 화면: 연결 상태 요약 + 주요 화면으로의 바로가기."""

from __future__ import annotations

from typing import Callable, Optional

import flet as ft

from app.ui.flet.components.common import padded_column, section_card, status_pill
from app.ui.flet.theme.tokens import TOKENS, radius


class HomePage:
    """앱 첫 화면: 연결 상태 요약 + 주요 화면으로의 바로가기."""

    def __init__(self, *, on_navigate: Optional[Callable[[str], None]] = None) -> None:
        self._on_navigate = on_navigate
        self._comfy_pill = status_pill("ComfyUI 확인 중", "idle")
        self._lm_pill = status_pill("LM Studio 확인 중", "idle")

    def set_connection(self, service: str, ok: Optional[bool],
                       detail: str = "") -> None:
        pill = self._comfy_pill if service == "comfy" else self._lm_pill
        name = "ComfyUI" if service == "comfy" else "LM Studio"
        if ok is None:
            pill.content.controls[1].value = f"{name} 미확인"
        elif ok:
            pill.content.controls[1].value = f"{name} 연결됨"
        else:
            pill.content.controls[1].value = detail or f"{name} 연결 안 됨"

    def _quick_link(self, icon: str, label: str, route: str) -> ft.Control:
        """바로가기 타일. 클릭하면 해당 라우트로 이동한다."""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(icon, size=22, color=TOKENS.primary),
                    ft.Text(label, size=TOKENS.size_caption),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=TOKENS.space_xs,
                tight=True),
            bgcolor=TOKENS.surface_variant,
            border_radius=radius(TOKENS.radius_md),
            padding=ft.Padding.all(TOKENS.space_lg),
            on_click=(lambda _e, r=route: self._on_navigate(r))
                     if self._on_navigate else None,
        )

    def build(self) -> ft.Control:
        links = ft.Row(
            controls=[
                self._quick_link(ft.Icons.IMAGE, "이미지 만들기", "/generate"),
                self._quick_link(ft.Icons.LAYERS, "모델 관리", "/models"),
                self._quick_link(ft.Icons.HISTORY, "생성 기록", "/history"),
                self._quick_link(ft.Icons.HELP, "도움말", "/help"),
            ],
            spacing=TOKENS.space_md, tight=True)

        return padded_column(
            controls=[
                section_card("연결 상태", ft.Row(
                    controls=[self._comfy_pill, self._lm_pill],
                    spacing=TOKENS.space_md, tight=True)),
                section_card("바로가기", links),
                section_card("안내", ft.Text(
                    "왼쪽 메뉴에서 각 화면으로 이동할 수 있습니다. "
                    "이미지를 만드는 중에도 다른 화면을 다닐 수 있습니다.",
                    size=TOKENS.size_caption, color=TOKENS.on_surface_variant)),
            ],
            padding=TOKENS.space_xl,
            spacing=TOKENS.space_lg,
        )
