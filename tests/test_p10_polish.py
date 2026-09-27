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
    QLabel,
    QListWidget,
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
        """P14: 강조는 railOptionsBtn / railHistoryBtn 에만 붙는다(기획서 v5.0)."""
        controller = _make_controller()
        opt = controller.find(QPushButton, "railOptionsBtn")
        hist = controller.find(QPushButton, "railHistoryBtn")
        home = controller.find(QPushButton, "railHomeBtn")
        controller._rail_page_toggle("history")
        self.assertIn("0078D4", hist.styleSheet())
        self.assertNotIn("0078D4", opt.styleSheet())
        self.assertNotIn("0078D4", home.styleSheet())
        controller._rail_page_toggle("options")
        self.assertIn("0078D4", opt.styleSheet())
        self.assertNotIn("0078D4", hist.styleSheet())
        self.assertNotIn("0078D4", home.styleSheet())


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


class P10ExecFixTests(unittest.TestCase):
    """실행 화면修正: 레일 텍스트 표시, 미리보기 크기, 이력 메타 단축."""

    def test_rail_buttons_have_visible_text(self):
        controller = _make_controller()
        for name, expected in (("railHomeBtn", "홈"),
                               ("railHistoryBtn", "이력"),
                               ("railHelpBtn", "?"),
                               ("railSettingsBtn", "설정")):
            with self.subTest(button=name):
                button = controller.find(QPushButton, name)
                self.assertIsNotNone(button)
                self.assertEqual(button.text(), expected)

    def test_preview_removed_card_replaces_it(self):
        # P11: 미리보기 라벨 삭제됨 — 채팅 카드+모달이 대체
        controller = _make_controller()
        from PySide6.QtWidgets import QLabel
        self.assertIsNone(controller.find(QLabel, "previewLabel"))

    def test_history_meta_uses_short_model(self):
        import tempfile
        from app.sections.session import SessionManager
        controller = _make_controller()
        tmp = tempfile.TemporaryDirectory()
        controller.session_manager = SessionManager(
            Path(tmp.name) / ".sessions")
        controller._tmpdir = tmp
        session = controller.session_manager.new_session(
            model="juggernautXL_ragnarok.safetensors")
        session["title"] = "테스트"
        controller.session_manager.save_session(session)
        controller._refresh_history_list()
        history_list = controller.find(QListWidget, "historyList")
        self.assertIsNotNone(history_list)
        row_text = history_list.item(0).text()
        self.assertNotIn("juggernautXL_ragnarok.safetensors", row_text)


if __name__ == "__main__":
    unittest.main()
