# -*- coding: utf-8 -*-
"""P14: 사이드바 5버튼 + 홈/옵션 역할 분리 (기획서 v5.0 목업 1-A·5·5-A·5-B)."""
from __future__ import annotations

import os
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QSpacerItem

from app.gui.ui_loader import load_ui

BASE_DIR = Path(__file__).resolve().parent.parent
UI_FILE = BASE_DIR / "assets" / "ui" / "main.ui"

RAIL_BUTTONS = [
    ("railHomeBtn", "홈"),
    ("railOptionsBtn", "옵션"),
    ("railHistoryBtn", "이력"),
    ("railHelpBtn", "?"),
    ("railSettingsBtn", "설정"),
]


class RailStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
        cls.window = load_ui(UI_FILE)

    def test_five_buttons_exist(self):
        for name, text in RAIL_BUTTONS:
            with self.subTest(button=name):
                button = self.window.findChild(QPushButton, name)
                self.assertIsNotNone(button, f"{name} 없음")
                self.assertEqual(button.text(), text)

    def test_button_size_55(self):
        for name, _ in RAIL_BUTTONS:
            with self.subTest(button=name):
                button = self.window.findChild(QPushButton, name)
                self.assertEqual(button.width(), 55)
                self.assertEqual(button.height(), 55)

    def test_rail_width_76(self):
        rail = self.window.findChild(QWidget, "railFrame")
        self.assertEqual(rail.minimumWidth(), 76)
        self.assertEqual(rail.maximumWidth(), 76)

    def test_rail_order_top3_bottom2(self):
        """상단 3(홈/옵션/이력) / spacer / 하단 2(?/설정)."""
        rail = self.window.findChild(QWidget, "railFrame")
        layout = rail.layout()
        kinds = []
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget is not None:
                kinds.append(("btn", widget.objectName()))
            elif item.spacerItem() is not None:
                kinds.append(("spacer", "railSpacer"))
        self.assertEqual(
            kinds,
            [
                ("btn", "railHomeBtn"),
                ("btn", "railOptionsBtn"),
                ("btn", "railHistoryBtn"),
                ("spacer", "railSpacer"),
                ("btn", "railHelpBtn"),
                ("btn", "railSettingsBtn"),
            ],
        )

    def test_spacer_exists_once(self):
        rail = self.window.findChild(QWidget, "railFrame")
        layout = rail.layout()
        spacers = [layout.itemAt(i).spacerItem() for i in range(layout.count())
                   if layout.itemAt(i).spacerItem() is not None]
        self.assertEqual(len(spacers), 1)

    def test_home_tooltip_is_not_options(self):
        """홈의 툴팁이 '생성 옵션'이면 이름-기능 불일치(기획서 v5.0가 고친 문제)."""
        home = self.window.findChild(QPushButton, "railHomeBtn")
        tooltip = home.toolTip()
        self.assertNotIn("생성 옵션", tooltip)
        self.assertIn("메인", tooltip)

    def test_options_tooltip_mentions_options(self):
        opt = self.window.findChild(QPushButton, "railOptionsBtn")
        self.assertIn("옵션", opt.toolTip())


class RailSelectionMappingTests(unittest.TestCase):
    """강조 대상은 옵션/이력뿐 (홈·?·설정은 강조 없음)."""

    def test_mapping_excludes_home(self):
        import main as main_module
        source = (BASE_DIR / "app" / "main_controller.py").read_text(encoding="utf-8")
        start = source.find("def _update_rail_selection")
        block = source[start:start + 700]
        self.assertIn('"options": "railOptionsBtn"', block)
        self.assertIn('"history": "railHistoryBtn"', block)
        self.assertNotIn('"railHomeBtn"', block)

    def test_home_handler_exists(self):
        source = (BASE_DIR / "app" / "main_controller.py").read_text(encoding="utf-8")
        self.assertIn("def _rail_home_clicked", source)

    def test_home_connected_to_new_handler(self):
        source = (BASE_DIR / "app" / "main_controller.py").read_text(encoding="utf-8")
        self.assertIn("home.clicked.connect(self._rail_home_clicked)", source)
        # P1 초기 연결에서 홈은 제외되어야 한다 (이중 실행 방지)
        self.assertIn('for name in ("railOptionsBtn", "railHistoryBtn"):', source)


if __name__ == "__main__":
    unittest.main()
