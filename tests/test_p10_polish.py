# -*- coding: utf-8 -*-
"""P10: 테마 2종 정리, 레일 선택 강조, 렌더 성능 스모크 검증."""
from __future__ import annotations

import os
import time
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QPushButton,
)

import main as main_module
from app.gui.chat_widgets import ChatMessage
from app.gui.ui_loader import load_ui
from app.gui.theme_manager import VISIBLE_THEMES

BASE_DIR = Path(__file__).resolve().parent.parent
UI_FILE = BASE_DIR / "assets" / "ui" / "main.ui"


def _make_controller():
    app = QApplication.instance() or QApplication([])
    window = load_ui(UI_FILE)
    controller = main_module.MainController(window)
    return controller


class P10ThemeTests(unittest.TestCase):
    def test_visible_themes_are_two(self):
        self.assertEqual(list(VISIBLE_THEMES),
                         ["fluent_dark", "fluent_light"])

    def test_combo_shows_only_two_themes(self):
        controller = _make_controller()
        combo = controller.find(QComboBox, "themeComboBox")
        self.assertEqual(combo.count(), 2)
        keys = [combo.itemData(i) for i in range(combo.count())]
        self.assertEqual(keys, ["fluent_dark", "fluent_light"])

    def test_chat_qss_present_in_visible_themes(self):
        for theme in ("fluent_dark", "fluent_light"):
            path = (BASE_DIR / "assets" / "ui" / "themes" / f"{theme}.qss")
            text = path.read_text(encoding="utf-8")
            for selector in ("#chatUserBubble", "#chatAiBubble",
                             "#chatSystemText", "#imageCard"):
                with self.subTest(theme=theme, selector=selector):
                    self.assertIn(selector, text)


class P10RailSelectionTests(unittest.TestCase):
    def test_selection_highlight_follows_page(self):
        controller = _make_controller()
        home = controller.find(QPushButton, "railHomeBtn")
        hist = controller.find(QPushButton, "railHistoryBtn")
        controller._rail_page_toggle("history")
        self.assertIn("0078D4", hist.styleSheet())
        self.assertNotIn("0078D4", home.styleSheet())
        controller._rail_page_toggle("options")
        self.assertIn("0078D4", home.styleSheet())
        self.assertNotIn("0078D4", hist.styleSheet())


class P10PerfSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_200_messages_render_in_time(self):
        started = time.monotonic()
        for i in range(200):
            ChatMessage("user" if i % 2 else "ai", f"메시지 {i}").deleteLater()
        elapsed = time.monotonic() - started
        self.assertLess(elapsed, 20.0, f"200개 렌더 {elapsed:.1f}초 초과")


if __name__ == "__main__":
    unittest.main()
