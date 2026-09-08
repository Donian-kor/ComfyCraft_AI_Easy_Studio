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
    "midnight_navy": "🌙  미드나잇 네이비",
    "emerald_forest": "🌲  에메랄드 포레스트",
    "purple_nebula": "🔮  퍼플 네뷸라",
    "warm_cocoa": "🍫  웜 코코아",
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
    return key