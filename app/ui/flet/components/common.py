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


def framed_section(title: str, content: ft.Control, *, subtitle: str = "",
                  accent: Optional[str] = None, trailing: Optional[ft.Control] = None,
                  width: Optional[int] = None) -> ft.Container:
    """제목 + 테두리 프레임 + 본문. '어디까지가 어느 옵션인가'를 구분한다.

    기존 _section() 은 제목 텍스트만 두고 배경/테두리가 없었다. 그래서
    스크롤이 길어지면 어디부터가 어느 그룹인지 알 수 없었다.

    구분 단서 세 가지를 겹쳐 쓴다.
      1) 테두리  : 프레임 경계가 곧 그룹 경계
      2) 배경    : surface_variant (본문과 아주 살짝 다른 톤)
      3) 색 점   : 왼쪽 위 accent 점으로 제목을 눈으로 잡아준다

    accent 를 주면 제목 옆에 그 색의 점을 놓는다. 안 주면 기본색을 쓴다.
    """
    dot_color = accent or TOKENS.primary
    header = ft.Row(
        controls=[
            ft.Container(
                width=6, height=6, bgcolor=dot_color,
                border_radius=ft.BorderRadius(3, 3, 3, 3)),
            ft.Text(title, size=TOKENS.size_caption, weight=ft.FontWeight.W_600,
                    color=TOKENS.on_surface),
            ft.Container(expand=True),
        ] + ([trailing] if trailing is not None else [
            ft.Text(subtitle, size=TOKENS.size_caption,
                    color=TOKENS.on_surface_variant)] if subtitle else []),
        spacing=TOKENS.space_sm, tight=True,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    return ft.Container(
        content=ft.Column(
            controls=[header, content],
            spacing=TOKENS.space_md, tight=True),
        bgcolor=TOKENS.surface_variant,
        border=ft.Border.all(1, TOKENS.outline),
        border_radius=radius(TOKENS.radius_md),
        padding=ft.Padding.all(TOKENS.space_md),
        width=width,
    )


def overlayed_counter(field: ft.Control, counter: ft.Control,
                      badge: Optional[ft.Control] = None) -> ft.Stack:
    """텍스트 필드 안에 우측 위로 카운터(와 초과 배지)를 겹친다.

    Flet 의 `TextField.counter` 는 입력칸 *밖* 아래에 그린다. 그래서
    직접 쓰면 카운터가 입력줄 아래에 떨어져 보인다. Stack 으로 덮어
    '입력칸 안쪽 우측 위' 로 옮긴다.

    회귀 근거(두 번 삽질함):
      1) 자식에 `Container.alignment` 를 주면 그 자식은 *positioned* 로
         취급돼 `Stack.alignment` 가 통째로 무시되고 좌상단에 그려진다.
         → `top` / `right` 를 명시한다.
      2) `StackFit.LOOSE` 로 두면 오버레이 크기가 Stack 기준이 되어
         입력칸이 줄 수에 따라 커져도 카운터가 어긋난다.
         → `PASS_THROUGH` 로 입력칸 크기를 그대로 따라간다.
    """
    row_controls = ([badge] if badge is not None else []) + [counter]
    return ft.Stack(
        controls=[
            field,
            ft.Container(
                content=ft.Row(
                    controls=row_controls,
                    spacing=TOKENS.space_xs, tight=True,
                    alignment=ft.MainAxisAlignment.END),
                # 라벨(Field 의 floating label)이 위쪽에 뜨므로 그만큼
                # 내려야 글자와 겹치지 않는다. content_padding.top 과
                # 같은 값을 쓴다(24).
                top=TOKENS.space_xl,
                right=TOKENS.space_md,
                ignore_interactions=True),
        ],
        clip_behavior=ft.ClipBehavior.NONE,
        fit=ft.StackFit.PASS_THROUGH,
    )


def framed_box(content: ft.Control) -> ft.Container:
    """제목 없는 본문만 테두리 프레임으로 감싼다.

    collapsible(有自己的 헤더) 처럼 제목이 이미 있는 묶음을 감쌀 때 쓴다.
    제목을 또 만들면 두 개가 생기므로, 이쪽은 본문만 받는다.
    """
    return ft.Container(
        content=content,
        bgcolor=TOKENS.surface_variant,
        border=ft.Border.all(1, TOKENS.outline),
        border_radius=radius(TOKENS.radius_md),
        padding=ft.Padding.all(TOKENS.space_md),
    )


def collapsible(title: str, content: ft.Control, *, expanded: bool = False,
                subtitle: str = "", on_toggle: Optional[Callable[[bool], None]] = None
                ) -> ft.Column:
    """접기/펼치기 패널 (Phase 6: 정보 밀도 조절).

    기능 삭제가 아니라 '기본 화면에 다 보여주지 않는 것' 이 목적이다.

    반환값은 반드시 ft.Column 이다. (제목 헤더 + 본문 2개짜리)
    이 구조를 밖에서 가정하는 코드가 많으므로, 프레임으로 감싸거나
    헤더에 요소를 끼워 넣지 않는다. 감싸려면 호출처에서 framed_box() 를 쓴다.
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


def option_row(label: str, control: ft.Control, width: int = 190,
               label_width: int = 0) -> ft.Row:
    """좌측 라벨 + 우측 컨트롤 한 줄 (기본 옵션용).

    label_width 를 주면 라벨을 그 폭으로 고정한다. 그러면 라벨 길이가
    달라도(Steps / Sampler / Scheduler) 컨트롤이 매 줄 같은 자리에서
    시작해 세로 정렬이 맞는다. 안 주면 원래처럼 길이만큼 차지한다.
    """
    # 회귀 근거: 라벨(고정폭) + '미리' 공백 컨테이너(1px) + 컨트롤 로
    # 만들면 Row 의 spacing 이 *자식 사이마다* 들어가서 간격이 두 번
    # 반영된다. 1px 공백은 1px 밖에 안 되는데 spacing 이 8px 씩 두 번이라
    # 합계가 프레임을 9px 넘겨, 드롭다운 화살표가 잘렸다.
    # → 라벨을 고정폭으로 잡았으면 별도 공백 컨트롤을 넣지 않는다.
    #    (간격은 Row.spacing 이 한 번만 넣는다)
    if label_width:
        label_control: ft.Control = ft.Container(
            content=ft.Text(label, size=TOKENS.size_caption,
                            color=TOKENS.on_surface_variant, no_wrap=True),
            width=label_width)
        return ft.Row(
            controls=[
                label_control,
                ft.Container(content=control, width=width),
            ],
            spacing=TOKENS.space_sm,
            tight=True,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    return ft.Row(
        controls=[
            ft.Text(label, size=TOKENS.size_caption,
                    color=TOKENS.on_surface_variant),
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
