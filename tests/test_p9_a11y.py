# -*- coding: utf-8 -*-
"""P9: 오류·접근성 — 템플릿, 금지어, 안내, 접근성 이름 검증."""
from __future__ import annotations

import os
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QLabel,
    QPlainTextEdit,
    QPushButton,
)

import main as main_module
from app.gui.ui_loader import load_ui

BASE_DIR = Path(__file__).resolve().parent.parent
UI_FILE = BASE_DIR / "assets" / "ui" / "main.ui"


def _make_controller():
    app = QApplication.instance() or QApplication([])
    window = load_ui(UI_FILE)
    controller = main_module.MainController(window)
    return controller


class P9TemplateTests(unittest.TestCase):
    def test_templates_complete(self):
        from app.main_controller import TEMPLATES
        for key in ("welcome", "done", "edited", "generating",
                    "model_changed", "options_reset", "failed", "lm_off",
                    "blocked", "busy", "style_pick"):
            with self.subTest(template=key):
                self.assertIn(key, TEMPLATES)
                self.assertTrue(TEMPLATES[key])


class P9ValidationTests(unittest.TestCase):
    def test_blocked_word_rejected(self):
        controller = _make_controller()
        ok, hit = controller._validate_chat_text("nsfw 이미지 그려줘")
        self.assertFalse(ok)
        self.assertTrue(hit)

    def test_normal_text_passes(self):
        controller = _make_controller()
        ok, hit = controller._validate_chat_text("귀여운 고양이 그려줘")
        self.assertTrue(ok)
        self.assertEqual(hit, "")

    def test_blocked_send_shows_inline_error(self):
        controller = _make_controller()
        calls = []
        orig_start = controller.start_generation
        controller.start_generation = lambda: calls.append(True)
        try:
            edit = controller.find(QPlainTextEdit, "chatInputEdit")
            edit.setPlainText("nsfw 그려줘")
            controller._send_chat_text()
            self.assertEqual(calls, [])
            error = controller.find(QLabel, "chatInputErrorLabel")
            self.assertTrue(error.isVisibleTo(controller.window))
        finally:
            controller.start_generation = orig_start

    def test_lm_off_notice_added(self):
        controller = _make_controller()
        calls = []
        orig_start = controller.start_generation
        controller.start_generation = lambda: calls.append(True)
        try:
            # 서버 없음 → LM 미연결 상태
            self.assertFalse(controller.is_lm_connected())
            edit = controller.find(QPlainTextEdit, "chatInputEdit")
            edit.setPlainText("고양이 그려줘")
            controller._send_chat_text()
            self.assertEqual(calls, [True])
            from app.gui.chat_widgets import ChatMessage
            ai_texts = [m.bubble.text()
                        for m in controller.window.findChildren(ChatMessage)
                        if m.role == "ai"]
            self.assertTrue(any("원문" in t for t in ai_texts))
        finally:
            controller.start_generation = orig_start


class P9AccessibilityTests(unittest.TestCase):
    def test_accessible_names_set(self):
        controller = _make_controller()
        send = controller.find(QPushButton, "sendBtn")
        self.assertEqual(send.accessibleName(), "이미지 생성하기")
        picker = controller.find(QComboBox, "comfyModelCombo")
        self.assertEqual(picker.accessibleName(), "이미지 생성 모델 선택")
        edit = controller.find(QPlainTextEdit, "chatInputEdit")
        self.assertEqual(edit.accessibleName(), "이미지 설명 입력")
        live = controller.find(QLabel, "chatLiveLabel")
        self.assertIsNotNone(live)

    def test_reduced_motion_disables_pulse(self):
        controller = _make_controller()
        os.environ["COMFYCRAFT_REDUCE_MOTION"] = "1"
        try:
            self.assertTrue(controller._reduced_motion())
            bubble = controller._show_status_bubble()
            self.assertFalse(bubble._pulse_timer.isActive())
            controller._hide_status_bubble()
        finally:
            os.environ.pop("COMFYCRAFT_REDUCE_MOTION", None)

    def test_greeting_only_when_empty(self):
        import tempfile
        from app.sections.session import SessionManager
        controller = _make_controller()
        tmp = tempfile.TemporaryDirectory()
        controller.session_manager = SessionManager(
            Path(tmp.name) / ".sessions")
        controller._tmpdir = tmp
        controller._chat_log = []
        controller._clear_chat_widgets()
        controller._maybe_greet()
        from app.gui.chat_widgets import ChatMessage
        ai_texts = [m.bubble.text()
                    for m in controller.window.findChildren(ChatMessage)
                    if m.role == "ai"]
        self.assertTrue(any("안녕하세요" in t for t in ai_texts))
        # 두 번째 호출은 중복 추가 안 됨 (로그 존재)
        before = len(controller.window.findChildren(ChatMessage))
        controller._maybe_greet()
        after = len(controller.window.findChildren(ChatMessage))
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
