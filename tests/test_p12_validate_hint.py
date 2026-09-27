# -*- coding: utf-8 -*-
"""P12: profileValidateLabel 초기 안내 문구(.ui 기본값) + 3상태 표시 검증.

초기 안내 문구는 Python이 아니라 settings_dialog.ui에 정의되어야 한다
(단일 진실 원천). 여기서는 .ui에 값이 실제로 들어있는지 확인한다.
"""
from __future__ import annotations

import os
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QLabel

from app.gui.dialogs import settings_dialog as sd
from app.gui.ui_loader import load_dialog_ui
from app.paths import SETTINGS_DIALOG_FILE

BASE_DIR = Path(__file__).resolve().parent.parent
THEMES_DIR = BASE_DIR / "assets" / "ui" / "themes"
UI_FILE = Path(SETTINGS_DIALOG_FILE)


class _FakeRegistry:
    """model_registry.profiles만 있으면 _setup_model_tab이 동작한다."""

    profiles: list = []


class _FakeController:
    """_setup_model_tab이 쓰는 최소 인터페이스만 제공."""

    def __init__(self):
        self.logged: list[str] = []
        self.model_registry = _FakeRegistry()

    def append_log(self, message: str) -> None:
        self.logged.append(message)


class P12ValidateHintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.dlg = load_dialog_ui(Path(SETTINGS_DIALOG_FILE))
        self.controller = _FakeController()
        sd._setup_model_tab(self.dlg, self.controller)
        self.label = self.dlg.findChild(QLabel, "profileValidateLabel")

    def test_label_exists(self):
        self.assertIsNotNone(self.label)

    def test_initial_hint_defined_in_ui_file(self):
        """초기 문구는 .ui에 있어야 한다 (Python 하드코딩 금지)."""
        xml = UI_FILE.read_text(encoding="utf-8")
        self.assertIn('name="profileValidateLabel"', xml)
        start = xml.find('name="profileValidateLabel"')
        block = xml[start:start + 600]
        text_at = block.find("<string>")
        self.assertNotEqual(text_at, -1, ".ui에 기본 text가 없음")
        end = block.find("</string>", text_at)
        self.assertNotEqual(block[text_at + len("<string>"):end].strip(), "",
                            ".ui의 초기 text가 비어 있음")
        self.assertNotIn("PROFILE_INITIAL_HINT",
                         (BASE_DIR / "app" / "gui" / "dialogs" /
                          "settings_dialog.py").read_text(encoding="utf-8"),
                         "초기 문구가 Python에 하드코딩되어 있음")

    def test_initial_hint_not_blank(self):
        """다이얼로그를 열자마자 빈 라벨로 보이지 않아야 한다."""
        self.assertTrue(self.label.text().strip(), "초기 문구가 비어 있음")
        self.assertFalse(self.label.text().startswith(("✓", "✗")),
                         "초기 안내에는 결과 기호가 붙으면 안 됨")

    def test_initial_state_is_info(self):
        self.assertEqual(self.label.property("state"), "info")

    def test_initial_hint_not_logged(self):
        """초기 안내는 사용자 조작이 아니므로 로그에 쌓이지 않는다."""
        self.assertEqual(self.controller.logged, [])

    def test_ok_prefix_and_state(self):
        sd.apply_profile_status(self.label, "저장되었습니다", True)
        self.assertEqual(self.label.text(), "✓ 저장되었습니다")
        self.assertEqual(self.label.property("state"), "ok")

    def test_error_prefix_and_state(self):
        sd.apply_profile_status(self.label, "프로필명을 입력하세요.", False)
        self.assertEqual(self.label.text(), "✗ 프로필명을 입력하세요.")
        self.assertEqual(self.label.property("state"), "error")

    def test_info_path_has_no_prefix(self):
        sd.apply_profile_status(self.label, "안내 문구입니다.", None)
        self.assertEqual(self.label.text(), "안내 문구입니다.")
        self.assertEqual(self.label.property("state"), "info")

    def test_apply_profile_status_accepts_none_label(self):
        self.assertIsNone(sd.apply_profile_status(None, "x", True))

    def test_wordwrap_enabled(self):
        self.assertTrue(self.label.wordWrap())

    def test_qss_rules_present_in_both_themes(self):
        for theme in ("fluent_dark.qss", "fluent_light.qss"):
            with self.subTest(theme=theme):
                qss = (THEMES_DIR / theme).read_text(encoding="utf-8")
                self.assertIn("QLabel#profileValidateLabel {", qss)
                self.assertIn('QLabel#profileValidateLabel[state="ok"]', qss)
                self.assertIn('QLabel#profileValidateLabel[state="error"]', qss)


if __name__ == "__main__":
    unittest.main()