# -*- coding: utf-8 -*-
"""UI/UX 4단계 검증 — 최소 크기, 포커스 링, 도움말 테마, 에러 배너."""
from __future__ import annotations

import os
import unittest
import xml.dom.minidom
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

BASE_DIR = Path(__file__).resolve().parent.parent
THEME_DIR = BASE_DIR / "assets" / "ui" / "themes"


class UiUxStepTests(unittest.TestCase):
    def test_step1_minimum_window_size(self) -> None:
        """1단계: 창 최소 높이가 700이어야 화면이 깨지지 않는다."""
        ui_text = (BASE_DIR / "assets" / "ui" / "main.ui").read_text(encoding="utf-8")
        self.assertIn("<height>700</height>", ui_text)
        self.assertNotIn("<height>160</height>", ui_text)

    def test_step2_focus_ring_in_all_themes(self) -> None:
        """2단계: 9개 테마 전부 키보드 포커스 링 규칙을 가져야 한다."""
        qss_files = sorted(THEME_DIR.glob("*.qss"))
        self.assertEqual(len(qss_files), 9, f"테마는 9개여야 함: {len(qss_files)}")
        for path in qss_files:
            with self.subTest(theme=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertIn("QPushButton:focus", text)
                self.assertIn("QCheckBox:focus", text)

    def test_step3_help_dialog_has_no_hardcoded_colors(self) -> None:
        """3단계: 도움말 .ui에 하드코딩 색상/죽은 data-theme 분기가 없어야 한다."""
        ui_text = (BASE_DIR / "assets" / "ui" / "help_dialog_v2.ui").read_text(
            encoding="utf-8"
        )
        for color in ("#1a1a1a", "#ffffff", "#fafafa", "#e0e0e0"):
            self.assertNotIn(color, ui_text, f"하드코딩 색상 잔존: {color}")
        self.assertNotIn("data-theme", ui_text)
        self.assertIn("palette(", ui_text)
        # XML이 깨지지 않았는지도 확인
        xml.dom.minidom.parse(str(BASE_DIR / "assets" / "ui" / "help_dialog_v2.ui"))

    def test_step3_help_dialog_loads(self) -> None:
        """3단계: 도움말 다이얼로그가 실제로 로드되어야 한다."""
        from PySide6.QtWidgets import QApplication

        from app.gui.ui_loader import load_dialog_ui

        app = QApplication.instance() or QApplication([])
        dlg = load_dialog_ui(BASE_DIR / "assets" / "ui" / "help_dialog_v2.ui")
        self.assertEqual(dlg.objectName(), "HelpDialog")

    def test_step4_error_banner_ui_and_style(self) -> None:
        """4단계: 에러 배너 위젯 + 9개 테마 스타일이 있어야 한다."""
        main_ui = (BASE_DIR / "assets" / "ui" / "main.ui").read_text(encoding="utf-8")
        self.assertIn('name="errorBannerLabel"', main_ui)
        xml.dom.minidom.parse(str(BASE_DIR / "assets" / "ui" / "main.ui"))
        for path in sorted(THEME_DIR.glob("*.qss")):
            with self.subTest(theme=path.name):
                self.assertIn(
                    "errorBannerLabel", path.read_text(encoding="utf-8")
                )

    def test_step4_error_banner_logic(self) -> None:
        """4단계: 에러 배너 표시/숨기기/에러핸들러가 main.py에 있어야 한다."""
        source = (BASE_DIR / "main.py").read_text(encoding="utf-8")
        for name in (
            "def show_error_banner",
            "def clear_error_banner",
            "def _reveal_log_on_error",
            "def _on_generation_error",
            "def _on_error_banner_clicked",
        ):
            self.assertIn(name, source, f"main.py에 없음: {name}")


if __name__ == "__main__":
    unittest.main()
