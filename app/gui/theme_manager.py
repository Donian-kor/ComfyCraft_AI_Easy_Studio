# -*- coding: utf-8 -*-
"""UI 테마 목록/적용/선택 저장을 담당하는 모듈.

테마 파일은 assets/ui/themes/{키}.qss 에 위치하며,
선택한 테마는 workflows/ui_theme.json 에 저장되어 다음 실행 때도 유지됩니다.
"""
from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtWidgets import QApplication

GUI_DIR = Path(__file__).resolve().parent                     # app/gui
PROJECT_ROOT = GUI_DIR.parent.parent                          # 프로젝트 루트
ASSETS_UI_DIR = PROJECT_ROOT / "assets" / "ui"                # UI 디자인 리소스 위치
THEME_DIR = ASSETS_UI_DIR / "themes"                          # assets/ui/themes
LEGACY_QSS = ASSETS_UI_DIR / "style.qss"                      # 이전 방식(단일 style.qss) 폴백용
SETTING_PATH = PROJECT_ROOT / "workflows" / "ui_theme.json"

DEFAULT_THEME = "fluent_dark"

# 콤보박스에 표시되는 순서대로 정의
AVAILABLE_THEMES: dict[str, str] = {
    "fluent_dark": "🎨  플루언트 다크 (기본)",
    "midnight_navy": "🌙  미드나잇 네이비 (미드톤)",
    "emerald_forest": "🌲  에메랄드 포레스트 (미드톤)",
    "purple_nebula": "🔮  퍼플 네뷸라 (미드톤)",
    "warm_cocoa": "🍫  웜 코코아 (미드톤)",
    "slate_amber": "🧱  슬레이트 앰버 (미드톤)",
    "midnight_coral": "🪸  미드나잇 코랄 (미드톤)",
    "plum_sage": "🌸  플럼 세이지 (미드톤 라이트)",
    "fluent_light": "☀️  플루언트 라이트",
}


def available_themes() -> dict[str, str]:
    """{테마 키: 표시 이름} 사전 반환"""
    return dict(AVAILABLE_THEMES)


def load_theme_choice(setting_path: Path = SETTING_PATH) -> str:
    """저장된 테마 키를 읽는다. 없거나 잘못됐으면 기본 테마 반환."""
    try:
        if setting_path.exists():
            data = json.loads(setting_path.read_text(encoding="utf-8"))
            key = str(data.get("theme", "")).strip()
            if key in AVAILABLE_THEMES:
                return key
            if key:
                print(f"[테마] 알 수 없는 테마 키라 기본값 사용: {key!r}")
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[테마] 설정을 읽을 수 없어 기본값 사용: {exc}")
    return DEFAULT_THEME


def save_theme_choice(key: str, setting_path: Path = SETTING_PATH) -> bool:
    """테마 선택을 JSON 파일로 저장한다. 성공 여부 반환."""
    if key not in AVAILABLE_THEMES:
        print(f"[테마] 저장할 수 없는 테마 키: {key!r}")
        return False
    try:
        setting_path.parent.mkdir(parents=True, exist_ok=True)
        setting_path.write_text(
            json.dumps({"theme": key}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return True
    except OSError as exc:
        print(f"[테마] 설정 저장 실패: {exc}")
        return False


def theme_qss(key: str) -> str:
    """테마 키에 해당하는 QSS 문자열. 못 찾으면 기본 → 레거시 → 빈 문자열 순으로 폴백."""
    if key in AVAILABLE_THEMES:
        qss_path = THEME_DIR / f"{key}.qss"
        if qss_path.exists():
            return qss_path.read_text(encoding="utf-8")
        print(f"[테마] 파일을 찾을 수 없어 기본 테마로 대체: {qss_path}")
        key = DEFAULT_THEME

    qss_path = THEME_DIR / f"{key}.qss"
    if qss_path.exists():
        return qss_path.read_text(encoding="utf-8")

    if LEGACY_QSS.exists():  # 테마 폴더가 통째로 없을 때의 최후 폴백
        print(f"[테마] 테마 폴더가 없어 기존 style.qss 사용: {LEGACY_QSS}")
        return LEGACY_QSS.read_text(encoding="utf-8")

    print("[테마] 어떤 QSS 파일도 찾을 수 없습니다. 스타일 없이 실행합니다.")
    return ""


def apply_theme(app: QApplication, key: str) -> str:
    """애플리케이션에 테마를 적용하고, 실제로 적용된 테마 키를 반환한다."""
    if key not in AVAILABLE_THEMES:
        print(f"[테마] 알 수 없는 테마 키라 기본값으로 대체: {key!r}")
        key = DEFAULT_THEME
    qss = theme_qss(key)
    if qss:
        app.setStyleSheet(qss)
    else:
        app.setStyleSheet("")  # 테마 파일이 전혀 없으면 스타일 해제
    # 상태 속성(property)이 새 테마에 맞게 즉시 반영되도록 이벤트 처리
    app.processEvents()
    # SplitTextButton 테마 색상 업데이트
    _update_split_text_button_theme(key)
    # PlayStopButton 테마 색상 업데이트
    _update_play_stop_button_theme(key)
    # Z-ANIME 스타일 버튼 테마 색상 업데이트
    _update_zanime_style_button_theme(key)
    return key


def _update_split_text_button_theme(key: str) -> None:
    """SplitTextButton의 테마 색상을 업데이트한다."""
    try:
        from app.gui.split_text_button import SplitTextButton
        colors = _SPLIT_TEXT_BUTTON_COLORS.get(key, _SPLIT_TEXT_BUTTON_COLORS[DEFAULT_THEME])
        SplitTextButton.updateThemeColors(key, colors)
    except Exception:
        pass


def _update_play_stop_button_theme(key: str) -> None:
    """PlayStopButton의 테마 색상을 업데이트한다."""
    try:
        from app.gui.play_stop_button import PlayStopButton
        colors = _PLAY_STOP_BUTTON_COLORS.get(key, _PLAY_STOP_BUTTON_COLORS[DEFAULT_THEME])
        PlayStopButton.updateThemeColors(key, colors)
    except Exception:
        pass


def _update_zanime_style_button_theme(key: str) -> None:
    """Z-ANIME 스타일 버튼의 테마 색상을 업데이트한다."""
    try:
        from app.gui.zanime_style_button import ZAnimeStyleButton
        colors = _ZANIME_STYLE_BUTTON_COLORS.get(key, _ZANIME_STYLE_BUTTON_COLORS[DEFAULT_THEME])
        ZAnimeStyleButton.update_theme_colors(key, colors)
    except Exception:
        pass


# SplitTextButton용 테마 색상 테이블
_SPLIT_TEXT_BUTTON_COLORS: dict[str, dict[str, dict[str, str]]] = {
    "fluent_dark": {
        "accent": {"bg": "#0078D4", "text": "#ffffff"},
        "success": {"bg": "#4edea3", "text": "#ffffff"},
        "error": {"bg": "#ffb4ab", "text": "#ffffff"},
        "warning": {"bg": "#fbbf24", "text": "#1a1a1a"},
        "pending": {"bg": "#b8c0cc", "text": "#1a1a1a"},
    },
    "midnight_navy": {
        "accent": {"bg": "#4cc2ff", "text": "#ffffff"},
        "success": {"bg": "#7ed9f5", "text": "#ffffff"},
        "error": {"bg": "#ffb4ab", "text": "#ffffff"},
        "warning": {"bg": "#ffc97a", "text": "#1a1a1a"},
        "pending": {"bg": "#d5ddf0", "text": "#1a1a1a"},
    },
    "emerald_forest": {
        "accent": {"bg": "#34d399", "text": "#ffffff"},
        "success": {"bg": "#7ce0af", "text": "#ffffff"},
        "error": {"bg": "#ffb4ab", "text": "#ffffff"},
        "warning": {"bg": "#ffd98a", "text": "#1a1a1a"},
        "pending": {"bg": "#d9e8e0", "text": "#1a1a1a"},
    },
    "purple_nebula": {
        "accent": {"bg": "#a78bfa", "text": "#ffffff"},
        "success": {"bg": "#c4b5fd", "text": "#ffffff"},
        "error": {"bg": "#ffb4ab", "text": "#ffffff"},
        "warning": {"bg": "#ffd9b8", "text": "#1a1a1a"},
        "pending": {"bg": "#d9d1ec", "text": "#1a1a1a"},
    },
    "warm_cocoa": {
        "accent": {"bg": "#f0a13e", "text": "#ffffff"},
        "success": {"bg": "#ffc57a", "text": "#ffffff"},
        "error": {"bg": "#ffb4ab", "text": "#ffffff"},
        "warning": {"bg": "#ffe5b8", "text": "#1a1a1a"},
        "pending": {"bg": "#ddd2c4", "text": "#1a1a1a"},
    },
    "slate_amber": {
        "accent": {"bg": "#e8a33d", "text": "#ffffff"},
        "success": {"bg": "#f4d99a", "text": "#ffffff"},
        "error": {"bg": "#ffb4ab", "text": "#ffffff"},
        "warning": {"bg": "#ffe5b8", "text": "#1a1a1a"},
        "pending": {"bg": "#c3c8d4", "text": "#1a1a1a"},
    },
    "midnight_coral": {
        "accent": {"bg": "#e8637a", "text": "#ffffff"},
        "success": {"bg": "#ffa8b8", "text": "#ffffff"},
        "error": {"bg": "#ff8a92", "text": "#ffffff"},
        "warning": {"bg": "#ffd5c0", "text": "#1a1a1a"},
        "pending": {"bg": "#c6bedd", "text": "#1a1a1a"},
    },
    "plum_sage": {
        "accent": {"bg": "#7a3b69", "text": "#ffffff"},
        "success": {"bg": "#b8a0c4", "text": "#1a1a1a"},
        "error": {"bg": "#e8a8ac", "text": "#1a1a1a"},
        "warning": {"bg": "#e6c8d4", "text": "#1a1a1a"},
        "pending": {"bg": "#4e4657", "text": "#ffffff"},
    },
    "fluent_light": {
        "accent": {"bg": "#0078d4", "text": "#ffffff"},
        "success": {"bg": "#4edea3", "text": "#ffffff"},
        "error": {"bg": "#ffb4ab", "text": "#1a1a1a"},
        "warning": {"bg": "#fbbf24", "text": "#1a1a1a"},
        "pending": {"bg": "#5c5c5c", "text": "#ffffff"},
    },
}


# PlayStopButton용 테마 색상 테이블 (play: 시작 버튼 색상, stop: 정지 버튼 색상)
_PLAY_STOP_BUTTON_COLORS: dict[str, dict[str, dict[str, str]]] = {
    "fluent_dark": {
        "play": {"bg": "#0078D4"},
        "stop": {"bg": "#C42B1C"},
    },
    "midnight_navy": {
        "play": {"bg": "#4cc2ff"},
        "stop": {"bg": "#E05263"},
    },
    "emerald_forest": {
        "play": {"bg": "#34d399"},
        "stop": {"bg": "#E05263"},
    },
    "purple_nebula": {
        "play": {"bg": "#a78bfa"},
        "stop": {"bg": "#E05263"},
    },
    "warm_cocoa": {
        "play": {"bg": "#f0a13e"},
        "stop": {"bg": "#d9534f"},
    },
    "slate_amber": {
        "play": {"bg": "#e8a33d"},
        "stop": {"bg": "#C42B1C"},
    },
    "midnight_coral": {
        "play": {"bg": "#e8637a"},
        "stop": {"bg": "#C42B1C"},
    },
    "plum_sage": {
        "play": {"bg": "#7a3b69"},
        "stop": {"bg": "#c42b1c"},
    },
    "fluent_light": {
        "play": {"bg": "#0078d4"},
        "stop": {"bg": "#c42b1c"},
    },
}


# Z-ANIME 스타일 버튼용 테마 색상 테이블
# selected_*: 선택된 버튼(눌린 상태), unselected_*: 선택되지 않은 버튼
_ZANIME_STYLE_BUTTON_COLORS: dict[str, dict[str, str]] = {
    "fluent_dark": {
        "selected_bg": "#0078D4",
        "selected_border": "#4cc2ff",
        "selected_text": "#ffffff",
        "unselected_bg": "#3a3a3a",
        "unselected_border": "#5a5a5a",
        "unselected_text": "#f0f0f0",
    },
    "midnight_navy": {
        "selected_bg": "#4cc2ff",
        "selected_border": "#a6e3ff",
        "selected_text": "#0b1b2b",
        "unselected_bg": "#2b3a4d",
        "unselected_border": "#46586e",
        "unselected_text": "#eaf2fb",
    },
    "emerald_forest": {
        "selected_bg": "#34d399",
        "selected_border": "#a7f3d0",
        "selected_text": "#0d2b1f",
        "unselected_bg": "#2c4437",
        "unselected_border": "#476b56",
        "unselected_text": "#eaf7f0",
    },
    "purple_nebula": {
        "selected_bg": "#a78bfa",
        "selected_border": "#ddd6fe",
        "selected_text": "#241a3d",
        "unselected_bg": "#3a3350",
        "unselected_border": "#574d75",
        "unselected_text": "#f1ecff",
    },
    "warm_cocoa": {
        "selected_bg": "#f0a13e",
        "selected_border": "#ffd9a8",
        "selected_text": "#3a2408",
        "unselected_bg": "#4a3a2c",
        "unselected_border": "#6b5745",
        "unselected_text": "#f7efe6",
    },
    "slate_amber": {
        "selected_bg": "#e8a33d",
        "selected_border": "#ffdc9e",
        "selected_text": "#38260a",
        "unselected_bg": "#3f4652",
        "unselected_border": "#5b6472",
        "unselected_text": "#eef1f6",
    },
    "midnight_coral": {
        "selected_bg": "#e8637a",
        "selected_border": "#ffb3c0",
        "selected_text": "#ffffff",
        "unselected_bg": "#463043",
        "unselected_border": "#66485f",
        "unselected_text": "#f9eef4",
    },
    "plum_sage": {
        "selected_bg": "#7a3b69",
        "selected_border": "#b58aa8",
        "selected_text": "#ffffff",
        "unselected_bg": "#e6dfe4",
        "unselected_border": "#b9a9b6",
        "unselected_text": "#33232f",
    },
    "fluent_light": {
        "selected_bg": "#0078d4",
        "selected_border": "#005a9e",
        "selected_text": "#ffffff",
        "unselected_bg": "#e2e2e2",
        "unselected_border": "#b8b8b8",
        "unselected_text": "#1a1a1a",
    },
}


def zanime_style_button_colors(key: str) -> dict[str, str]:
    """Z-ANIME 스타일 버튼에 쓸 테마 색상 사전을 반환한다."""
    colors = _ZANIME_STYLE_BUTTON_COLORS.get(key)
    if colors is None:
        colors = _ZANIME_STYLE_BUTTON_COLORS.get(DEFAULT_THEME)
    return dict(colors or {})