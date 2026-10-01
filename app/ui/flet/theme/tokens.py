"""Material 3 테마 토큰 (Phase 11).

QSS 의 대체물. 색상 값을 여러 UI 에 직접 하드코딩하지 않도록
여기 한 곳에서 관리하고, 컴포넌트는 토큰 이름을 받아 쓴다.

다크(DARK)/라이트(LIGHT) 두 벌을 두고 `set_theme_mode()` 로 전환한다.
컴포넌트가 `TOKENS.surface` 처럼 값을 읽어 컨트롤을 만들기 때문에
전환할 때는 두 가지를 같이 해야 한다.

1. 앞으로 만들 컨트롤 → 활성 테마를 가리키는 프록시(TOKENS) 가 처리
2. 이미 만들어진 컨트롤 → `recolor_tree()` 로 색을 갈아 끼운다

앱을 통째로 다시 그리면 사용자가 폼에 쳐 둔 값이 지워지므로,
색만 바꾸는 2번 방식을 기본으로 쓴다.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from typing import Dict, Optional

import flet as ft


@dataclass(frozen=True)
class ThemeTokens:
    """Material 3 계열 색상/간격/모서리 토큰."""

    # 색상
    primary: str = "#7C6CFF"
    on_primary: str = "#FFFFFF"
    primary_container: str = "#2A2450"
    on_primary_container: str = "#D9D2FF"

    secondary: str = "#64D8CB"
    on_secondary: str = "#00382F"
    secondary_container: str = "#1E4A44"
    on_secondary_container: str = "#B8F2EA"

    background: str = "#0F1117"
    surface: str = "#161923"
    surface_variant: str = "#1E2230"
    surface_container: str = "#1A1E29"

    on_surface: str = "#E6E8F0"
    on_surface_variant: str = "#9AA0B4"

    outline: str = "#2E3345"
    outline_variant: str = "#3A4056"

    success: str = "#4ADE80"
    warning: str = "#FBBF24"
    error: str = "#F87171"
    info: str = "#60A5FA"

    # 간격 (px)
    space_xs: int = 4
    space_sm: int = 8
    space_md: int = 12
    space_lg: int = 16
    space_xl: int = 24
    space_xxl: int = 32

    # 모서리 (px)
    radius_sm: int = 8
    radius_md: int = 12
    radius_lg: int = 16
    radius_pill: int = 999

    # 폰트
    font_family: str = "Malgun Gothic"
    font_mono: str = "Consolas"

    size_caption: int = 11
    size_body: int = 13
    size_title: int = 16
    size_headline: int = 22


# 다크 테마(기본값). 라이트는 위쪽 LIGHT 참조.
DARK = ThemeTokens()


# --- 라이트 테마 ---------------------------------------------------------
# 다크와 같은 항목 순서/이름을 그대로 갖는다(프록시가 이름으로 찾으므로).
LIGHT = ThemeTokens(
    primary="#5B4BD6",
    on_primary="#FFFFFF",
    primary_container="#E4DEFF",
    on_primary_container="#1A1046",
    secondary="#0E7C6F",
    on_secondary="#FFFFFF",
    secondary_container="#C9F2EA",
    on_secondary_container="#00201B",
    background="#F6F5FB",
    surface="#FFFFFF",
    surface_variant="#EDEBF5",
    surface_container="#F2F0F9",
    on_surface="#1B1B22",
    on_surface_variant="#5A5A6B",
    outline="#C9C6D8",
    outline_variant="#DFDCEA",
    success="#1B8A4B",
    warning="#B26A00",
    error="#C53434",
    info="#2563C9",
)


class _TokenProxy:
    """활성 테마(TOKENS)를 대신 세워 주는 객체.

    컴포넌트는 `TOKENS.surface` 처럼 이름을 읽는다. 그 이름이 계속
    살아 있으면서 값만 현재 테마를 따라가게 하려면, 실제 토큰 대신
    이 프록시를 건네야 한다. (`TOKENS` 를 통째로 바꾸면 이미
    import 해 둔 모듈에는 전파되지 않는다)
    """

    __slots__ = ("active",)

    def __init__(self, tokens: ThemeTokens) -> None:
        object.__setattr__(self, "active", tokens)

    def use(self, tokens: ThemeTokens) -> None:
        object.__setattr__(self, "active", tokens)

    def __getattr__(self, name: str):
        # __slots__ 때문에 active 는 __getattr__ 로 오지 않는다.
        return getattr(object.__getattribute__(self, "active"), name)

    def __repr__(self) -> str:  # 디버그용
        return f"<TOKENS {object.__getattribute__(self, 'active')!r}>"


TOKENS = _TokenProxy(DARK)

# 상태 → 토큰 이름. 값(색)이 아니라 이름을 담는다.
# 그래야 테마를 바꿀 때 상태 표를 다시 만들 필요가 없다.
_STATUS_TOKEN_NAMES: Dict[str, str] = {
    "idle": "on_surface_variant",
    "ok": "success",
    "connected": "success",
    "disconnected": "error",
    "pending": "warning",
    "running": "info",
    "generating": "info",
    "error": "error",
    "failed": "error",
    "cancelled": "warning",
    "done": "success",
}

# 상태 → 색상 매핑. 모든 상태 표시가 이 표를 거친다.
# 값은 매번 활성 토큰에서 계산한다(테마 전환에 자동으로 따라간다).
def _build_status_colors() -> Dict[str, str]:
    return {status: getattr(TOKENS, attr)
            for status, attr in _STATUS_TOKEN_NAMES.items()}


STATUS_COLORS: Dict[str, str] = _build_status_colors()

# 현재 테마 모드. "dark" / "light"
_mode: str = "dark"


def theme_mode() -> str:
    """현재 테마 모드 이름 ("dark" / "light")."""
    return _mode


def set_theme_mode(mode: str) -> str:
    """테마를 다크/라이트로 바꾼다. 바뀐 모드 이름을 돌려준다.

    알 수 없는 이름은 "dark" 로 본다(설정 파일이 손상된 경우 대비).
    """
    global _mode
    _mode = "light" if str(mode or "").strip().lower() == "light" else "dark"
    TOKENS.use(LIGHT if _mode == "light" else DARK)
    return _mode


def toggle_theme_mode() -> str:
    """다크 ↔ 라이트를 뒤집는다. 바뀐 모드 이름을 돌려준다."""
    return set_theme_mode("light" if _mode == "dark" else "dark")


def flet_theme_mode() -> ft.ThemeMode:
    """Flet Page.theme_mode 에 넣을 값."""
    return ft.ThemeMode.LIGHT if _mode == "light" else ft.ThemeMode.DARK


# --- 이미 만든 컨트롤의 색 갈아 끼우기 ----------------------------------
# 컨트롤은 dataclass 이고 값은 _values 딕셔너리에 들어 있다.
# getattr/setattr 로 바꾸면 Flet 이 변경을 감지해 다시 그린다.
_COLOR_FIELDS = (
    "color", "bgcolor", "outline_color", "divider_color",
    "track_color", "thumb_color", "accent_color",
)


def recolor_tree(control, mapping: Dict[str, str]) -> int:
    """컨트롤 트리를 훑어 예전 색 → 새 색으로 바꾼다. 바꾼 개수를 돌려준다.

    mapping 은 {예전색: 새색} 이다. 토큰에 없는 색(사용자가 고른 색 등)은
    건드리지 않는다. 컴포넌트가 토큰을 안 쓰는 곳도 안전하다.
    """
    if not mapping or control is None:
        return 0
    changed = 0
    for field in _COLOR_FIELDS:
        current = getattr(control, field, None)
        if isinstance(current, str) and current in mapping:
            try:
                setattr(control, field, mapping[current])
                changed += 1
            except (AttributeError, TypeError):
                pass
    changed += _recolor_border(control, mapping)
    for child in _iter_children(control):
        changed += recolor_tree(child, mapping)
    return changed


def _recolor_border(control, mapping: Dict[str, str]) -> int:
    """Container 의 테두리 색도 테마를 따라간다.

    회귀 근거: 섹션 카드의 테두리(TOKENS.outline)를 쓰기 시작하면서,
    테마를 바꾸면 *배경과 글자색만* 바뀌고 테두리는 다크용 값(#2E3345)에
    남았다. 라이트 배경에 다크 테두리가 떠서 프레임이 깨져 보였다.
    테두리는 Border.top/right/bottom/left 로 쪼개져 있어 따로 봐야 한다.
    """
    border = getattr(control, "border", None)
    if border is None:
        return 0
    changed = 0
    for side_name in ("top", "right", "bottom", "left"):
        side = getattr(border, side_name, None)
        color = getattr(side, "color", None)
        if isinstance(color, str) and color in mapping:
            try:
                side.color = mapping[color]
                changed += 1
            except (AttributeError, TypeError):
                pass
    return changed


def _iter_children(control):
    """컨트롤의 자식 컨트롤을 순서대로 내놓는다(트리 모양 무관).

    Flet 컨트롤은 dataclass 이고 자식들은 필드값으로 들어 있다
    (Row/Column 의 controls, Container 의 content, Dialog 의 actions 등).
    그래서 필드 값을 훑어 컨트롤 인스턴스만 뽑는다.
    """
    for field in dataclasses.fields(control):
        value = getattr(control, field.name, None)
        if isinstance(value, ft.Control):
            yield value
        elif isinstance(value, (list, tuple)):
            for item in value:
                if isinstance(item, ft.Control):
                    yield item


def color_mapping(old: ThemeTokens, new: ThemeTokens) -> Dict[str, str]:
    """토큰 세트 두 개에서 {이전색: 새색} 대응표를 만든다.

    같은 값이면 넣지 않는다(문자열 키라 같은 색은 축약된다).
    """
    mapping: Dict[str, str] = {}
    for field in dataclasses.fields(ThemeTokens):
        before = getattr(old, field.name)
        after = getattr(new, field.name)
        if isinstance(before, str) and isinstance(after, str) and before != after:
            mapping[before] = after
    return mapping


def status_color(status: str) -> str:
    """상태 문자열을 색상으로 바꾼다 (미등록 상태는 중립색)."""
    key = str(status or "idle").lower()
    table = _build_status_colors()
    return table.get(key, TOKENS.on_surface_variant)




def radius(value: int) -> ft.BorderRadius:
    return ft.BorderRadius(value, value, value, value)


def only_left(value: int) -> ft.BorderRadius:
    return ft.BorderRadius(top_left=value, top_right=value,
                           bottom_left=value, bottom_right=value)


def build_theme() -> ft.Theme:
    """Material 3 테마를 현재 활성 토큰으로 만든다."""
    t = TOKENS
    scheme = ft.ColorScheme(
        primary=t.primary,
        on_primary=t.on_primary,
        primary_container=t.primary_container,
        on_primary_container=t.on_primary_container,
        secondary=t.secondary,
        on_secondary=t.on_secondary,
        secondary_container=t.secondary_container,
        on_secondary_container=t.on_secondary_container,
        surface=t.surface,
        on_surface=t.on_surface,
        surface_container=t.surface_container,
        surface_container_high=t.surface_variant,
        on_surface_variant=t.on_surface_variant,
        outline=t.outline,
        outline_variant=t.outline_variant,
        error=t.error,
    )
    return ft.Theme(
        color_scheme=scheme,
        color_scheme_seed=t.primary,
        font_family=t.font_family,
        scaffold_bgcolor=t.background,
        canvas_color=t.background,
        card_theme=ft.CardTheme(
            color=t.surface,
            elevation=0,
            margin=0,
            shape=ft.RoundedRectangleBorder(radius=t.radius_lg),
        ),
        divider_color=t.outline_variant,
        divider_theme=ft.DividerTheme(color=t.outline_variant, thickness=1, space=1),
        scrollbar_theme=ft.ScrollbarTheme(
            thumb_color=t.outline,
            radius=t.radius_pill,
            thickness=6,
        ),
        appbar_theme=ft.AppBarTheme(
            bgcolor=t.surface,
            color=t.on_surface,
            elevation=0,
            elevation_on_scroll=0,
            toolbar_height=64,
        ),
        navigation_rail_theme=ft.NavigationRailTheme(
            bgcolor=t.surface,
            indicator_color=t.primary_container,
            use_indicator=True,
            selected_label_text_style=ft.TextStyle(color=t.primary, size=t.size_body),
            unselected_label_text_style=ft.TextStyle(
                color=t.on_surface_variant, size=t.size_body),
        ),
        progress_indicator_theme=ft.ProgressIndicatorTheme(
            color=t.primary,
            linear_min_height=6,
            linear_track_color=t.outline,
            border_radius=t.radius_pill,
        ),
        filled_button_theme=ft.FilledButtonTheme(
            style=ft.ButtonStyle(
                bgcolor=t.primary,
                color=t.on_primary,
                shape=ft.RoundedRectangleBorder(radius=t.radius_md),
                padding=ft.Padding.symmetric(horizontal=t.space_xl, vertical=t.space_md),
            )
        ),
        outlined_button_theme=ft.OutlinedButtonTheme(
            style=ft.ButtonStyle(
                color=t.on_surface,
                side=ft.BorderSide(1, t.outline),
                shape=ft.RoundedRectangleBorder(radius=t.radius_md),
            )
        ),
        text_button_theme=ft.TextButtonTheme(
            style=ft.ButtonStyle(color=t.primary)
        ),
        icon_button_theme=ft.IconButtonTheme(
            style=ft.ButtonStyle(color=t.on_surface_variant)
        ),
    )


def apply_theme(page, mode: str, root=None) -> int:
    """페이지를 지정한 테마로 바꾼다. 새로 칠한 컨트롤 수를 돌려준다.

    순서:
      1) 활성 토큰을 바꾼다 (앞으로 만들 컨트롤용)
      2) page.theme / page.theme_mode 를 다시 설정한다
      3) 이미 만들어진 트리의 색을 갈아 끼운다 (root 가 없으면 page 전체)

    root 를 주면 그 서브트리만 칠한다. page 전체를 훑으면 대화 카드처럼
    스크롤로 밖에 나간 컨트롤까지 만지므로, 화면 루트만 넘기는 편이 낫다.

    회귀 근거: 처음에는 update() 를 부르는 걸 빼먹었다. 속성은 제대로
    바뀌는데 Flet 은 '이제 화면에 반영하라'는 신호를 받아야 클라이언트로
    보내므로, 상태줄 메시지만 바뀌고 화면 색은 그대로인 상태가 됐다.
    """
    normalized = "light" if str(mode or "").strip().lower() == "light" else "dark"
    old = DARK if normalized == "light" else LIGHT
    new = LIGHT if normalized == "light" else DARK
    changed = recolor_tree(root if root is not None else page,
                           color_mapping(old, new))
    set_theme_mode(normalized)
    if page is not None:
        page.theme_mode = flet_theme_mode()
        page.theme = build_theme()
        _push_update(page)
    return changed


def _push_update(page) -> None:
    """페이지 변경분을 클라이언트에 보낸다. 못 보내도 앱은 계속 돈다."""
    try:
        page.update()
    except Exception:
        # 아직 page 에 붙지 않았거나(헤드리스 테스트) 이미 닫힌 세션.
        # 다음 갱신 때 자연히 반영되므로 삼킨다.
        pass
