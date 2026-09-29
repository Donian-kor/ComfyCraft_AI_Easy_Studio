"""Flet App Shell (Phase 4).

    App
    ├─ TopBar
    ├─ NavigationRail
    ├─ MainContent
    └─ StatusBar

셸은 레이아웃과 탐색만 책임진다. 업무 로직은 pages/ 아래로 내려간다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional

import flet as ft

from app.ui.flet.theme.tokens import TOKENS, status_color


@dataclass(frozen=True)
class NavItem:
    """내비게이션 항목 1개."""

    route: str
    label: str
    icon: str           # 선택되지 않았을 때
    selected_icon: str  # 선택되었을 때


NAV_ITEMS: List[NavItem] = [
    NavItem("/", "홈", ft.Icons.HOME_OUTLINED, ft.Icons.HOME),
    NavItem("/generate", "생성", ft.Icons.IMAGE_OUTLINED, ft.Icons.IMAGE),
    NavItem("/models", "모델", ft.Icons.LAYERS_OUTLINED, ft.Icons.LAYERS),
    NavItem("/chat", "대화", ft.Icons.CHAT_BUBBLE_OUTLINE, ft.Icons.CHAT_BUBBLE),
    NavItem("/history", "기록", ft.Icons.HISTORY, ft.Icons.HISTORY),
    NavItem("/settings", "설정", ft.Icons.SETTINGS_OUTLINED, ft.Icons.SETTINGS),
    NavItem("/help", "도움말", ft.Icons.HELP_OUTLINE, ft.Icons.HELP),
]


def route_index(route: str) -> int:
    """라우트 문자열을 NavigationRail 인덱스로 바꾼다."""
    for i, item in enumerate(NAV_ITEMS):
        if item.route == route:
            return i
    return 0


def index_route(index: Optional[int]) -> str:
    """NavigationRail 인덱스를 라우트로 되돌린다."""
    if index is None or index < 0 or index >= len(NAV_ITEMS):
        return NAV_ITEMS[0].route
    return NAV_ITEMS[index].route


class AppShell:
    """TopBar + NavigationRail + 본문 + 상태바를 묶는 컨테이너.

    컨트롤 트리만 만든다. 상태 변경은 update_* 메서드로 국소적으로 한다
    (전체 rebuild 는 진행 표시가 깜빡이게 만든다).
    """

    def __init__(self, on_navigate: Callable[[str], None]) -> None:
        self._on_navigate = on_navigate
        self._content_area = ft.Container(expand=True)
        self._status_text = ft.Text("", size=TOKENS.size_caption,
                                    color=TOKENS.on_surface_variant)
        self._job_bar = ft.ProgressBar(value=0, visible=False, height=4)
        self._job_label = ft.Text("", size=TOKENS.size_caption, color=TOKENS.primary)
        self._status_dot = ft.Container(
            width=8, height=8, border_radius=ft.BorderRadius(4, 4, 4, 4),
            bgcolor=TOKENS.on_surface_variant,
        )
        self._title = ft.Text("ComfyCraft", size=TOKENS.size_title,
                              weight=ft.FontWeight.W_600)
        self._rail = self._build_rail()
        self._comfy_indicator = self._build_service_indicator("ComfyUI")
        self._lm_indicator = self._build_service_indicator("LM Studio")

    # --- 구성 -------------------------------------------------------------
    def _build_rail(self) -> ft.NavigationRail:
        return ft.NavigationRail(
            bgcolor=TOKENS.surface,
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=88,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(item.icon),
                    selected_icon=ft.Icon(item.selected_icon),
                    label=item.label,
                    padding=ft.Padding.symmetric(vertical=TOKENS.space_xs),
                )
                for item in NAV_ITEMS
            ],
            on_change=self._handle_rail_change,
        )

    def _build_service_indicator(self, name: str) -> ft.Container:
        """연결 상태 표시등. dot 은 나중에 색만 바꾸므로 data 로 들고 있다."""
        dot = ft.Container(
            width=8, height=8,
            border_radius=ft.BorderRadius(4, 4, 4, 4),
            bgcolor=TOKENS.on_surface_variant,
        )
        return ft.Container(
            content=ft.Row(
                controls=[
                    dot,
                    ft.Text(name, size=TOKENS.size_caption,
                            color=TOKENS.on_surface_variant),
                ],
                spacing=TOKENS.space_sm,
                tight=True,
            ),
            tooltip=name,
            data=dot,
        )

    def _handle_rail_change(self, event: ft.Event) -> None:
        index = getattr(event.control, "selected_index", 0)
        self._on_navigate(index_route(index))

    def _build_topbar(self) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                controls=[
                    self._title,
                    ft.Text("AI Easy Studio", size=TOKENS.size_caption,
                            color=TOKENS.on_surface_variant),
                    ft.Container(expand=True),
                    self._comfy_indicator,
                    ft.Container(width=TOKENS.space_md),
                    self._lm_indicator,
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=TOKENS.space_xl,
                                         vertical=TOKENS.space_md),
            bgcolor=TOKENS.surface,
        )

    def _build_statusbar(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    self._job_bar,
                    ft.Row(
                        controls=[
                            self._status_dot,
                            self._status_text,
                            ft.Container(expand=True),
                            self._job_label,
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                spacing=TOKENS.space_xs,
                tight=True,
            ),
            padding=ft.Padding.symmetric(horizontal=TOKENS.space_xl,
                                         vertical=TOKENS.space_sm),
            bgcolor=TOKENS.surface,
        )

    def build(self) -> ft.Row:
        """전체 셸 컨트롤 트리를 만든다."""
        return ft.Row(
            controls=[
                self._rail,
                ft.VerticalDivider(width=1, color=TOKENS.outline),
                ft.Column(
                    controls=[
                        self._build_topbar(),
                        self._build_hairline(),
                        self._content_area,
                        self._build_statusbar(),
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

    @staticmethod
    def _build_hairline() -> ft.Container:
        """1px 구분선. VerticalDivider 는 높이 지정이 안 되므로 Container 를 쓴다."""
        return ft.Container(height=1, bgcolor=TOKENS.outline)

    # --- 상태 갱신 --------------------------------------------------------
    # 컨트롤.update() 는 화면에 붙어 있어야 동작한다. 앱 시작 직후나
    # 헤드리스 테스트에서는 아직 붙지 않았으므로, 값만 설정하고 조용히 넘긴다.

    @staticmethod
    def _safe_update(*controls: ft.Control) -> None:
        for control in controls:
            try:
                control.update()
            except RuntimeError:
                # 아직 page 에 붙지 않은 상태 — 값만 바꾼 채 다음 렌더를 기다린다.
                pass

    def set_content(self, control: ft.Control) -> None:
        self._content_area.content = control
        self._safe_update(self._content_area)

    def sync_route(self, route: str) -> None:
        """라우트에 맞춰 레일 선택 표시를 맞춘다."""
        self._rail.selected_index = route_index(route)
        self._safe_update(self._rail)

    def set_service_status(self, service: str, ok: Optional[bool]) -> None:
        """ComfyUI / LM Studio 연결 표시등을 갱신한다."""
        target = self._comfy_indicator if service == "comfy" else self._lm_indicator
        dot = target.data
        dot.bgcolor = (TOKENS.on_surface_variant if ok is None
                       else status_color("connected" if ok else "disconnected"))
        self._safe_update(target)

    def set_status(self, message: str, kind: str = "idle") -> None:
        """하단 상태줄을 갱신한다."""
        self._status_text.value = message
        self._status_dot.bgcolor = status_color(kind)
        self._safe_update(self._status_text, self._status_dot)

    def set_job_progress(self, progress: Optional[int], label: str = "") -> None:
        """생성 진행률을 표시한다. None 이면 숨긴다.

        화면을 옮겨도 Job 이 살아 있으므로, 이 표시도 페이지와 무관하다.
        """
        if progress is None:
            self._job_bar.visible = False
            self._job_label.value = ""
        else:
            self._job_bar.visible = True
            self._job_bar.value = max(0, min(progress, 100)) / 100.0
            self._job_label.value = label
        self._safe_update(self._job_bar, self._job_label)
