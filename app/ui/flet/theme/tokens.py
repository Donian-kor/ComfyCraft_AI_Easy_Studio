"""Material 3 테마 토큰 (Phase 11).

QSS 의 대체물. 색상 값을 여러 UI 에 직접 하드코딩하지 않도록
여기 한 곳에서 관리하고, 컴포넌트는 토큰 이름을 받아 쓴다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

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


TOKENS = ThemeTokens()

# 상태 → 색상 매핑. 모든 상태 표시가 이 표를 거친다.
STATUS_COLORS: Dict[str, str] = {
    "idle": TOKENS.on_surface_variant,
    "ok": TOKENS.success,
    "connected": TOKENS.success,
    "disconnected": TOKENS.error,
    "pending": TOKENS.warning,
    "running": TOKENS.info,
    "generating": TOKENS.info,
    "error": TOKENS.error,
    "failed": TOKENS.error,
    "cancelled": TOKENS.warning,
    "done": TOKENS.success,
}


def status_color(status: str) -> str:
    """상태 문자열을 색상으로 바꾼다 (미등록 상태는 중립색)."""
    return STATUS_COLORS.get(str(status or "idle").lower(), TOKENS.on_surface_variant)


def radius(value: int) -> ft.BorderRadius:
    return ft.BorderRadius(value, value, value, value)


def only_left(value: int) -> ft.BorderRadius:
    return ft.BorderRadius(top_left=value, top_right=value,
                           bottom_left=value, bottom_right=value)


def build_theme() -> ft.Theme:
    """Material 3 다크 테마를 만든다."""
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
