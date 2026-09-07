# -*- coding: utf-8 -*-
"""assets/ui/style.qss(기본 다크 테마)를 바탕으로 5개 색상 시안 테마 파일을 생성.

실행:  .venv/Scripts/python.exe tools/generate_themes.py
출력:  assets/ui/themes/ 폴더에 테마 QSS 6종
       (fluent_dark = style.qss 사본 + 시안 5종)

새 테마를 추가하려면 THEME_MAPPINGS 에 항목을 추가하고 다시 실행하면 됩니다.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_QSS = BASE_DIR / "assets" / "ui" / "style.qss"
OUTPUT_DIR = BASE_DIR / "assets" / "ui" / "themes"

# ---------------------------------------------------------------------------
# 색상 치환표.  키 = style.qss에 있는 현재 값, 값 = 시안에서 바뀔 색상.
# (대소문자는 무시하고 치환하며, 치환 충돌을 막기 위해 placeholder 2단계로 처리)
# ---------------------------------------------------------------------------
THEME_MAPPINGS: dict[str, dict[str, str]] = {
    # A. 미드나잇 네이비 — 짙은 남색 + 하늘색 액센트
    "midnight_navy": {
        "#181818": "#0b101c",   # 창/사이드바 배경
        "#212121": "#111a2c",   # 기본 표면
        "#2c2c2c": "#1b2740",   # 카드
        "#333333": "#22314f",   # 입력칸
        "#3a3a3a": "#2a3c60",   # 호버/스핀버튼
        "#2b2b2b": "#16203a",   # 버튼 눌림
        "#2a2a2a": "#131c30",   # 비활성 버튼
        "#262626": "#192339",   # 비활성 입력칸
        "#2a4a73": "#2b538c",   # 히어로 카드 그라데이션 끝
        "#f5f5f5": "#eaf0fb",   # 기본 글자
        "#e0e0e0": "#c9d5ee",   # 보조 글자(제목 등)
        "#b8b8b8": "#9fb0cf",   # 라벨/상태 글자
        "#6c6c70": "#5d6b8c",   # 비활성 글자
        "#757575": "#6b7a99",   # 카운터 글자
        "#0078d4": "#4cc2ff",   # 액센트
        "#2096f3": "#7ad3ff",   # 액센트 호버/그라데이션
        "#005fb8": "#2ba3e0",   # 액센트 눌림
        "#c42b1c": "#e05263",   # 위험 버튼
        "#d13438": "#f26d7d",
        "#a62a22": "#c24454",
    },
    # B. 에메랄드 포레스트 — 짙은 초록 + 민트 액센트
    "emerald_forest": {
        "#181818": "#0b1210",
        "#212121": "#122019",
        "#2c2c2c": "#1b2f26",
        "#333333": "#223a30",
        "#3a3a3a": "#2a463a",
        "#2b2b2b": "#16261f",
        "#2a2a2a": "#14231d",
        "#262626": "#1a2d25",
        "#2a4a73": "#1f5240",
        "#f5f5f5": "#eaf5ef",
        "#e0e0e0": "#c4ded2",
        "#b8b8b8": "#a3bfb2",
        "#6c6c70": "#5f7d70",
        "#757575": "#6b8578",
        "#0078d4": "#34d399",
        "#2096f3": "#5ce0ac",
        "#005fb8": "#1fa87a",
        "#c42b1c": "#e05263",
        "#d13438": "#f26d7d",
        "#a62a22": "#c24454",
    },
    # C. 퍼플 네뷸라 — 짙은 보라 + 라벤더 액센트
    "purple_nebula": {
        "#181818": "#100d1a",
        "#212121": "#1a1428",
        "#2c2c2c": "#271e3d",
        "#333333": "#2f2549",
        "#3a3a3a": "#392d57",
        "#2b2b2b": "#1f1833",
        "#2a2a2a": "#1c1630",
        "#262626": "#241c3a",
        "#2a4a73": "#4a3680",
        "#f5f5f5": "#f0eaf8",
        "#e0e0e0": "#d4c8ea",
        "#b8b8b8": "#b3a6cc",
        "#6c6c70": "#6f6390",
        "#757575": "#7a6d96",
        "#0078d4": "#a78bfa",
        "#2096f3": "#c4b5fd",
        "#005fb8": "#8b6cf0",
        "#c42b1c": "#e05263",
        "#d13438": "#f26d7d",
        "#a62a22": "#c24454",
    },
    # D. 웜 코코아 — 짙은 갈색 + 골드 액센트
    "warm_cocoa": {
        "#181818": "#16110d",
        "#212121": "#221a14",
        "#2c2c2c": "#2e241b",
        "#333333": "#382b21",
        "#3a3a3a": "#43342a",
        "#2b2b2b": "#261c14",
        "#2a2a2a": "#241b13",
        "#262626": "#2d221a",
        "#2a4a73": "#6b4a23",
        "#f5f5f5": "#f5efe8",
        "#e0e0e0": "#ddcdba",
        "#b8b8b8": "#c4b5a5",
        "#6c6c70": "#776a5b",
        "#757575": "#8a7a68",
        "#0078d4": "#f0a13e",
        "#2096f3": "#ffc46b",
        "#005fb8": "#d0862a",
        "#c42b1c": "#d9534f",
        "#d13438": "#e56b66",
        "#a62a22": "#b84340",
    },
    # E. 플루언트 라이트 — 밝은 회백색 + 파랑 액센트
    "fluent_light": {
        "#181818": "#ebebeb",
        "#212121": "#f5f5f5",
        "#2c2c2c": "#ffffff",
        "#333333": "#ffffff",
        "#3a3a3a": "#e2e2e2",
        "#2b2b2b": "#d5d5d5",
        "#2a2a2a": "#e8e8e8",
        "#262626": "#f0f0f0",
        "#2a4a73": "#cfe3f5",
        "#f5f5f5": "#1a1a1a",
        "#e0e0e0": "#3d3d3d",
        "#b8b8b8": "#5c5c5c",
        "#6c6c70": "#9a9a9a",
        "#757575": "#8a8a8a",
        "#0078d4": "#0078d4",   # 라이트에서도 파란 액센트 유지
        "#2096f3": "#2096f3",
        "#005fb8": "#005fb8",
        "#c42b1c": "#c42b1c",
        "#d13438": "#d13438",
        "#a62a22": "#a62a22",
    },
}

# 밝은 테마: 흰색 반투명(호버 하이라이트 등)은 어두운 반투명으로 뒤집어야 보임
LIGHT_THEMES = {"fluent_light"}

# 라이트 테마에서 "밝은 배경 위 흰 글자"를 어두운 글자로 바꾸는 규칙.
# 선택자별로 정밀하게 지정하며, 아래에 없는 곳(파란/빨간 배경 위 흰 글자,
# selection-color 등)은 흰색 그대로 유지됩니다.
LIGHT_TEXT_DARKEN = [
    r"(QMainWindow\s*\{[^}]*?(?<!selection-)(?<!background-)color:\s*)#ffffff",
    r"(QFrame#sidebar_frame QPushButton:hover\s*\{[^}]*?(?<!selection-)(?<!background-)color:\s*)#ffffff",
    r"(QFrame#sidebar_frame QPushButton:pressed\s*\{[^}]*?(?<!selection-)(?<!background-)color:\s*)#ffffff",
    r"(QLabel#appTitle\s*\{[^}]*?(?<!selection-)(?<!background-)color:\s*)#ffffff",
    r"(QTabBar::tab:hover\s*\{[^}]*?(?<!selection-)(?<!background-)color:\s*)#ffffff",
    r"(QTabBar::tab:selected\s*\{[^}]*?(?<!selection-)(?<!background-)color:\s*)#ffffff",
    r"(QLabel#lmTitleLabel,\s*QLabel#comfyTitleLabel\s*\{[^}]*?(?<!selection-)(?<!background-)color:\s*)#ffffff",
    r"(QGroupBox\s*\{[^}]*?(?<!selection-)(?<!background-)color:\s*)#ffffff",
    r"(QLabel#heroTitle\s*\{[^}]*?(?<!selection-)(?<!background-)color:\s*)#ffffff",
    r"(QLabel#lmCardTitle,\s*QLabel#comfyCardTitle\s*\{[^}]*?(?<!selection-)(?<!background-)color:\s*)#ffffff",
    r"(QLineEdit,[^{}]*?\{[^}]*?(?<!selection-)(?<!background-)color:\s*)#ffffff",
    r"(QComboBox QAbstractItemView\s*\{[^}]*?(?<!selection-)(?<!background-)color:\s*)#ffffff",
    r"(QPushButton\s*\{[^}]*?(?<!selection-)(?<!background-)color:\s*)#ffffff",
    r"(QPushButton#preset_[^{]*\{[^}]*?background-color:\s*#[0-9a-fA-F]+;[^}]*?(?<!selection-)(?<!background-)color:\s*)#ffffff",
    r"(QProgressBar\s*\{[^}]*?(?<!selection-)(?<!background-)color:\s*)#ffffff",
    r"(QToolTip\s*\{[^}]*?(?<!selection-)(?<!background-)color:\s*)#ffffff",
    r"(QMessageBox QLabel\s*\{[^}]*?(?<!selection-)(?<!background-)color:\s*)#ffffff",
]

def swap_colors(qss: str, mapping: dict[str, str]) -> str:
    """매핑 표대로 색상을 치환한다. (placeholder 2단계로 연쇄 치환 방지)"""
    tokens: dict[str, str] = {}
    for i, (old, new) in enumerate(mapping.items()):
        placeholder = f"@@THEME_TOKEN_{i}@@"
        tokens[placeholder] = new
        qss = re.sub(re.escape(old), placeholder, qss, flags=re.IGNORECASE)
    for placeholder, new in tokens.items():
        qss = qss.replace(placeholder, new)
    return qss


def flip_white_overlays_for_light(qss: str) -> str:
    """라이트 테마용: 흰색 반투명 오버레이를 검정 반투명으로 뒤집는다."""
    return re.sub(
        r"rgba\(255,\s*255,\s*255,\s*([0-9.]+)\)",
        r"rgba(0, 0, 0, \1)",
        qss,
    )


def darken_white_text_for_light(qss: str) -> str:
    """라이트 테마: 밝은 배경 위 흰 글자를 어둡게 바꾼다.

    LIGHT_TEXT_DARKEN 에 없는 곳(파란/빨간 배경 위 흰 글자,
    selection-color)은 흰색 그대로 유지됩니다.
    """
    for pattern in LIGHT_TEXT_DARKEN:
        qss = re.sub(pattern, r"\g<1>#1a1a1a", qss, flags=re.IGNORECASE)
    return qss


def validate(qss: str, name: str) -> list[str]:
    """생성된 QSS의 간단한 무결성 검사. 문제 문자열 리스트 반환."""
    problems: list[str] = []
    if qss.count("{") != qss.count("}"):
        problems.append(f"{name}: 괄호 불일치 {{={qss.count('{')} }}={qss.count('}')}")
    if "@@THEME_TOKEN_" in qss:
        problems.append(f"{name}: 치환되지 않은 토큰 남음")
    return problems


def main() -> int:
    if not SOURCE_QSS.exists():
        print(f"[오류] 원본 QSS를 찾을 수 없습니다: {SOURCE_QSS}")
        return 1

    source = SOURCE_QSS.read_text(encoding="utf-8")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    outputs: dict[str, str] = {"fluent_dark": source}  # 기본 테마 = style.qss 사본
    for theme_key, mapping in THEME_MAPPINGS.items():
        themed = swap_colors(source, mapping)
        if theme_key in LIGHT_THEMES:
            themed = flip_white_overlays_for_light(themed)
            themed = darken_white_text_for_light(themed)
        outputs[theme_key] = themed

    problems: list[str] = []
    for theme_key, qss in outputs.items():
        out_path = OUTPUT_DIR / f"{theme_key}.qss"
        out_path.write_text(qss, encoding="utf-8")
        problems.extend(validate(qss, theme_key))
        print(f"[생성] {out_path.name}  ({len(qss):,}자)")

    if problems:
        print("[검증 실패]")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"[완료] 테마 {len(outputs)}종이 {OUTPUT_DIR} 에 저장되었습니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())