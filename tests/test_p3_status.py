# -*- coding: utf-8 -*-
"""P3: 생성 중 상태 버블 — 위젯 단위 + 컨트롤러 연동 검증 (offscreen)."""
from __future__ import annotations

import os
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

import main as main_module
from app.gui.chat_widgets import GenerationStatusBubble
from app.gui.ui_loader import load_ui

BASE_DIR = Path(__file__).resolve().parent.parent
UI_FILE = BASE_DIR / "assets" / "ui" / "main.ui"


def _make_controller():
    app = QApplication.instance() or QApplication([])
    window = load_ui(UI_FILE)
    controller = main_module.MainController(window)
    return controller


class P3StatusBubbleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_bubble_progress_and_status(self):
        bubble = GenerationStatusBubble(parent=None)
        bubble.set_status("프롬프트 분석 중...")
        self.assertEqual(bubble.status_label.text(), "프롬프트 분석 중...")
        bubble.set_progress(45)
        self.assertEqual(bubble.bar.value(), 45)
        bubble.set_progress(999)
        self.assertEqual(bubble.bar.value(), 100)
        bubble.deleteLater()

    def test_bubble_pulse_starts_and_stops(self):
        bubble = GenerationStatusBubble(parent=None)
        self.assertFalse(bubble._pulse_timer.isActive())
        bubble.start()
        self.assertTrue(bubble._pulse_timer.isActive())
        bubble.stop()
        self.assertFalse(bubble._pulse_timer.isActive())
        bubble.deleteLater()

    def test_bubble_pulse_can_be_disabled(self):
        bubble = GenerationStatusBubble(parent=None)
        bubble.pulse_enabled = False
        bubble.start()
        self.assertFalse(bubble._pulse_timer.isActive())
        bubble.deleteLater()

    def test_cancel_button_calls_callback(self):
        calls = []
        bubble = GenerationStatusBubble(
            on_cancel=lambda: calls.append(True), parent=None)
        bubble.cancel_button.click()
        self.assertEqual(calls, [True])
        bubble.deleteLater()


class P3ControllerStatusTests(unittest.TestCase):
    def test_show_and_hide_bubble(self):
        controller = _make_controller()
        self.assertIsNone(controller._status_bubble)
        bubble = controller._show_status_bubble()
        self.assertIsNotNone(bubble)
        self.assertIs(controller._status_bubble, bubble)
        controller._hide_status_bubble()
        self.assertIsNone(controller._status_bubble)

    def test_hide_without_bubble_is_safe(self):
        controller = _make_controller()
        controller._hide_status_bubble()  # 예외 없어야 함
        controller.generation_finished(True)  # 버블 없이 완료 처리
        from PySide6.QtWidgets import QPushButton
        send = controller.find(QPushButton, "sendBtn")
        self.assertEqual(send.text(), "➤")

    def test_cancel_routes_to_stop(self):
        controller = _make_controller()
        stopped = []

        class FakeWorker:
            def stop(self):
                stopped.append(True)

        controller.worker = FakeWorker()
        try:
            bubble = controller._show_status_bubble()
            bubble.cancel_button.click()
            self.assertEqual(stopped, [True])
        finally:
            controller.worker = None


if __name__ == "__main__":
    unittest.main()
