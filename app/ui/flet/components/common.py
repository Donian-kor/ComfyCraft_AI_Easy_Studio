"""재사용 가능한 UI 컴포넌트.

business 로직을 담지 않는다. 입력/출력은 모두 콜백과 속성으로 받는다.
"""

from __future__ import annotations

from typing import Callable, List, Optional

import flet as ft

from app.ui.flet.theme.tokens import TOKENS, radius, status_color


def section_card(title: str, content: ft.Control, *, expand: bool = True,
                 trailing: Optional[ft.Control] = None) -> ft.Container:
    """제목 + 본문으로 이루어진 Material 카드."""
    header = ft.Row(
        controls=[
            ft.Text(title, size=TOKENS.size_caption, weight=ft.FontWeight.W_600,
                    color=TOKENS.on_surface_variant),
            ft.Container(expand=True),
        ] + ([trailing] if trailing is not None else []),
        tight=True,
    )
    return ft.Container(
        content=ft.Column(
            controls=[header, content],
            spacing=TOKENS.space_sm,
            tight=True,
        ),
        bgcolor=TOKENS.surface,
        border_radius=radius(TOKENS.radius_lg),
        padding=ft.Padding.all(TOKENS.space_lg),
        expand=expand,
    )


def collapsible(title: str, content: ft.Control, *, expanded: bool = False,
                subtitle: str = "", on_toggle: Optional[Callable[[bool], None]] = None
                ) -> ft.Column:
    """접기/펼치기 패널 (Phase 6: 정보 밀도 조절).

    기능 삭제가 아니라 '기본 화면에 다 보여주지 않는 것' 이 목적이다.
    """
    chevron = ft.Icon(
        icon=ft.Icons.KEYBOARD_ARROW_DOWN if expanded else ft.Icons.KEYBOARD_ARROW_RIGHT,
        size=TOKENS.size_body,
        color=TOKENS.on_surface_variant,
    )

    def handle_toggle(_event: ft.Event) -> None:
        is_open = not panel.visible
        panel.visible = is_open
        chevron.icon = (ft.Icons.KEYBOARD_ARROW_DOWN if is_open
                        else ft.Icons.KEYBOARD_ARROW_RIGHT)
        safe_update(chevron, panel)
        if on_toggle is not None:
            on_toggle(is_open)

    header = ft.Container(
        content=ft.Row(
            controls=[
                chevron,
                ft.Text(title, size=TOKENS.size_body, weight=ft.FontWeight.W_500),
                ft.Container(expand=True),
                ft.Text(subtitle, size=TOKENS.size_caption,
                        color=TOKENS.on_surface_variant) if subtitle
                else ft.Container(),
            ],
            spacing=TOKENS.space_sm,
            tight=True,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding.symmetric(vertical=TOKENS.space_sm),
        on_click=handle_toggle,
        border_radius=radius(TOKENS.radius_sm),
    )

    panel = ft.Container(
        content=content,
        visible=expanded,
        padding=ft.Padding.only(left=TOKENS.space_lg, bottom=TOKENS.space_sm),
    )

    return ft.Column(controls=[header, panel], spacing=0, tight=True)


def labeled_field(label: str, control: ft.Control) -> ft.Column:
    """라벨 + 컨트롤 묶음."""
    return ft.Column(
        controls=[
            ft.Text(label, size=TOKENS.size_caption, color=TOKENS.on_surface_variant),
            control,
        ],
        spacing=TOKENS.space_xs,
        tight=True,
    )


def status_pill(message: str, kind: str = "idle") -> ft.Container:
    """상태를 색깔 + 텍스트로 보여주는 작은 배지."""
    color = status_color(kind)
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(width=6, height=6,
                             border_radius=ft.BorderRadius(3, 3, 3, 3),
                             bgcolor=color),
                ft.Text(message, size=TOKENS.size_caption, color=color),
            ],
            spacing=TOKENS.space_sm,
            tight=True,
        ),
        bgcolor=ft.Colors.with_opacity(0.12, color),
        border_radius=radius(TOKENS.radius_pill),
        padding=ft.Padding.symmetric(horizontal=TOKENS.space_md,
                                     vertical=TOKENS.space_xs),
    )


def empty_state(icon: str, title: str, hint: str) -> ft.Container:
    """아무것도 없을 때 보여줄 안내."""
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(icon, size=44, color=TOKENS.outline),
                ft.Text(title, size=TOKENS.size_body, color=TOKENS.on_surface_variant),
                ft.Text(hint, size=TOKENS.size_caption,
                        color=TOKENS.outline, text_align=ft.TextAlign.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=TOKENS.space_sm,
        ),
        expand=True,
        alignment=ft.Alignment(0.5, 0.5),
    )


def option_row(label: str, control: ft.Control, width: int = 190) -> ft.Row:
    """좌측 라벨 + 우측 컨트롤 한 줄 (고급 옵션용)."""
    return ft.Row(
        controls=[
            ft.Text(label, size=TOKENS.size_caption, color=TOKENS.on_surface_variant),
            ft.Container(expand=True),
            ft.Container(content=control, width=width),
        ],
        spacing=TOKENS.space_sm,
        tight=True,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def safe_update(*controls: Optional[ft.Control]) -> None:
    """컨트롤을 갱신하되, 아직 page 에 붙지 않았으면 조용히 넘어간다.

    헤드리스 테스트와 앱 시작 직후(첫 렌더 전) 모두에서 상태를
    설정할 수 있어야 하므로 UI 계층 전부 이 함수를 쓴다.

    회귀 근거: 예전에는 update() 의 RuntimeError 를 그냥 삼켰다. 그래서
    백그라운드 스레드(모델 목록 조회)에서 갱신하면 *조용히 실패*했고,
    '모델을 바꿔도 아무 반응이 없다'는 증상이 났다. 이제 UI 스레드가
    아니면 갱신을 UI 스레드로 넘긴다.
    """
    from app.ui.flet.ui_loop import is_ui_thread, run_on_ui

    for control in controls:
        if control is None:
            continue
        if is_ui_thread():
            try:
                control.update()
            except RuntimeError:
                # 아직 page 에 붙지 않았다(헤드리스 테스트/초기 렌더 전)
                pass
            continue
        run_on_ui(lambda c=control: c.update())


def padded_column(controls: List[ft.Control], padding: int, *,
                  spacing: int = 0, expand: bool = True,
                  scroll: ft.ScrollMode = ft.ScrollMode.AUTO) -> ft.Container:
    """안쪽 여백이 있는 세로 목록.

    Flet 의 Column 은 padding 을 받지 않으므로, 여백이 필요하면
    반드시 Container 로 감싸야 한다.
    """
    return ft.Container(
        content=ft.Column(controls=controls, spacing=spacing, scroll=scroll),
        padding=ft.Padding.all(padding),
        expand=expand,
    )
