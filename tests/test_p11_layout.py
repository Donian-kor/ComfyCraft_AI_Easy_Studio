# -*- coding: utf-8 -*-
"""P11: 목업 레이아웃 일치 — 3층 구조, 치수, 삭제 위젯, 로그 탭 검증."""
from __future__ import annotations

import os
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QWidget,
)

import main as main_module
from app.gui.ui_loader import load_dialog_ui
from app.gui.ui_loader import load_ui
from app.paths import SETTINGS_DIALOG_FILE

BASE_DIR = Path(__file__).resolve().parent.parent
UI_FILE = BASE_DIR / "assets" / "ui" / "main.ui"

REMOVED_WIDGETS = [
    "viewerCard", "generateButton", "logGroupBox", "logTextEdit",
    "saveImageButton", "resetButton", "copyImageButton", "toggleLogButton",
    "previewLabel", "progressBar", "progressStatusLabel",
    "progressPercentLabel", "elapsedLabel",
    "step1Card", "step2Card",
    "modelSelectLabel", "chatCounterLabel", "badgeLabel", "headerDivider",
    "helpButton", "settingsButton",
    "positivePromptCounterLabel", "negativePromptCounterLabel",
    "enhancePromptCounterLabel", "copyPromptButton",
    "modelProfileNoticeLabel",
]


def _make_controller():
    app = QApplication.instance() or QApplication([])
    window = load_ui(UI_FILE)
    controller = main_module.MainController(window)
    return controller


class P11StructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_three_layer_structure(self):
        window = load_ui(UI_FILE)
        for name in ("headerFrame", "studioContainer", "chatFrame",
                     "inputFrame", "railFrame", "leftScrollArea",
                     "optionsLayout", "inputRowLayout"):
            with self.subTest(widget=name):
                found_widget = window.findChild(QWidget, name)
                from PySide6.QtWidgets import QLayout
                found_layout = window.findChild(QLayout, name)
                self.assertTrue(found_widget is not None
                                or found_layout is not None, name)
        # 에러는 별도 배너 위젯 없이 채팅 메시지로 표시한다
        self.assertIsNone(window.findChild(QLabel, "errorBannerLabel"))

    def test_removed_widgets_absent(self):
        window = load_ui(UI_FILE)
        for name in REMOVED_WIDGETS:
            with self.subTest(widget=name):
                self.assertIsNone(window.findChild(QWidget, name))

    def test_dimensions(self):
        window = load_ui(UI_FILE)
        header = window.findChild(QFrame, "headerFrame")
        self.assertEqual(header.maximumHeight(), 60)
        panel = window.findChild(QWidget, "leftScrollArea")
        self.assertEqual(panel.maximumWidth(), 340)
        self.assertFalse(panel.isVisibleTo(window))
        chat_input = window.findChild(QPlainTextEdit, "chatInputEdit")
        self.assertEqual(chat_input.maximumHeight(), 34)
        send = window.findChild(QPushButton, "sendBtn")
        self.assertEqual(send.maximumWidth(), 34)
        self.assertEqual(send.maximumHeight(), 34)
        new_chat = window.findChild(QPushButton, "newChatBtn")
        self.assertGreaterEqual(new_chat.minimumWidth(), 120)
        input_frame = window.findChild(QFrame, "inputFrame")
        self.assertEqual(input_frame.maximumHeight(), 58)

    def test_hidden_holders_kept(self):
        window = load_ui(UI_FILE)
        for name in ("positivePromptEdit", "enhancePromptEdit"):
            with self.subTest(widget=name):
                edit = window.findChild(QPlainTextEdit, name)
                self.assertIsNotNone(edit)
                self.assertFalse(edit.isVisibleTo(window))


class P11BehaviorTests(unittest.TestCase):
    def test_generation_finished_without_progress_widgets(self):
        controller = _make_controller()
        controller.generation_finished(True)  # 예외 없어야 함
        controller.generation_finished(False)

    def test_append_log_without_main_widgets(self):
        controller = _make_controller()
        controller.append_log("테스트 로그")
        self.assertIn("테스트 로그", controller.get_log_lines()[-1])
        controller.clear_logs()
        self.assertTrue(any("초기화" in line
                            for line in controller.get_log_lines()))

    def test_log_tab_widgets_present(self):
        dlg = load_dialog_ui(SETTINGS_DIALOG_FILE)
        tabs = dlg.findChild(QTabWidget, "settingsTabWidget")
        titles = [tabs.tabText(i) for i in range(tabs.count())]
        self.assertIn("로그", titles)
        self.assertIsNotNone(dlg.findChild(QTextEdit, "logTabEdit"))
        for name in ("logClearBtn", "logSaveBtn", "logCopyBtn"):
            with self.subTest(widget=name):
                self.assertIsNotNone(dlg.findChild(QPushButton, name))

    def test_panel_pages_are_exclusive(self):
        # P11 수정: ◷ 선택 시 옵션 위젯(중첩 행 포함)이 숨고 이력만 보여야 한다
        controller = _make_controller()
        controller._rail_page_toggle("history")
        from PySide6.QtWidgets import QSlider
        steps = controller.find(QSlider, "stepsSlider")
        self.assertFalse(steps.isVisibleTo(controller.window))
        options_visible = [
            w.objectName() for w in controller._options_widgets()
            if w.isVisibleTo(controller.window)]
        self.assertEqual(options_visible, [])
        history = controller.find(QWidget, "historyPage")
        self.assertTrue(history.isVisibleTo(controller.window))
        controller._rail_page_toggle("options")
        history = controller.find(QWidget, "historyPage")
        self.assertFalse(history.isVisibleTo(controller.window))
        self.assertTrue(steps.isVisibleTo(controller.window))

    def test_header_badges_left_of_theme(self):
        # 연결 배지 2개는 테마 드롭다운 바로 좌측에 있어야 한다
        window = load_ui(UI_FILE)
        header = window.findChild(QWidget, "headerFrame")
        order = []
        layout = header.layout()
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget is not None:
                order.append(widget.objectName())
            else:
                spacer = item.spacerItem()
                order.append("spacer" if spacer is not None else "layout")
        badges_idx = [order.index("comfyStatusBtn"),
                      order.index("lmStatusBtn")]
        theme_idx = order.index("themeComboBox")
        spacer_idx = order.index("spacer")
        self.assertLess(spacer_idx, min(badges_idx))
        self.assertEqual(max(badges_idx) + 1, theme_idx)


if __name__ == "__main__":
    unittest.main()
