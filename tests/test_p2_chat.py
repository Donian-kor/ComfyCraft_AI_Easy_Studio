# -*- coding: utf-8 -*-
"""P2: 채팅 송수신 — 위젯, 카운터, 전송 규칙 검증 (offscreen)."""
from __future__ import annotations

import os
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QPlainTextEdit, QPushButton, QWidget

import main as main_module
from app.gui.chat_widgets import ChatMessage, ImageCard
from app.gui.ui_loader import load_ui

BASE_DIR = Path(__file__).resolve().parent.parent
UI_FILE = BASE_DIR / "assets" / "ui" / "main.ui"


def _make_controller():
    # refresh_models는 패치하지 않는다: 클래스 패치가 인터프리터 종료 시
    # C++ 삭제 충돌을 유발함. 서버가 없으면 연결 실패로 즉시 끝나 안전하다.
    # 세션 관리자는 임시 디렉토리로 격리한다 (실제 outputs 오염 방지).
    import tempfile
    from app.sections.session import SessionManager
    app = QApplication.instance() or QApplication([])
    window = load_ui(UI_FILE)
    controller = main_module.MainController(window)
    tmp = tempfile.TemporaryDirectory()
    controller.session_manager = SessionManager(Path(tmp.name) / ".sessions")
    controller._tmpdir = tmp
    # 생성 시 실제 디렉토리에서 복원됐을 수 있는 상태를 초기화
    controller._current_session = None
    controller._chat_log = []
    controller._clear_chat_widgets()
    return controller


class P2ChatWidgetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_chat_message_roles(self):
        for role in ("user", "ai", "system"):
            msg = ChatMessage(role, "hello")
            self.assertEqual(msg.role, role)
            self.assertEqual(msg.bubble.text(), "hello")
            # P4/P6용 액션 행 존재
            self.assertIsNotNone(msg.action_row)

    def test_image_card_missing_file(self):
        card = ImageCard("no-such-file.png", "meta", "prompt")
        self.assertIn("불러올 수 없습니다", card.image_label.text())
        self.assertEqual(card.meta_label.text(), "meta")

    def test_image_card_prompt_fold(self):
        card = ImageCard("no-such-file.png", "meta", "prompt-text")
        self.assertFalse(card.prompt_label.isVisibleTo(card))
        card.prompt_toggle.setChecked(True)
        self.assertTrue(card.prompt_label.isVisibleTo(card))


class P2ChatFlowTests(unittest.TestCase):
    def test_empty_input_disables_send(self):
        controller = _make_controller()
        edit = controller.find(QPlainTextEdit, "chatInputEdit")
        button = controller.find(QPushButton, "sendBtn")
        edit.setPlainText("")
        self.assertFalse(button.isEnabled())

    def test_counter_updates(self):
        # P11: 카운터 라벨 삭제됨 — 5000자 강제 + 초과 시 인라인 경고
        controller = _make_controller()
        edit = controller.find(QPlainTextEdit, "chatInputEdit")
        edit.setPlainText("고양이")
        from PySide6.QtWidgets import QLabel
        self.assertIsNone(controller.find(QLabel, "chatCounterLabel"))
        edit.setPlainText("x" * 5001)
        self.assertEqual(len(edit.toPlainText()), 5000)
        error = controller.find(QLabel, "chatInputErrorLabel")
        self.assertTrue(error.isVisibleTo(controller.window))

    def test_send_syncs_prompt_and_clears_enhance(self):
        controller = _make_controller()
        calls = []
        orig_start = controller.start_generation
        controller.start_generation = lambda: calls.append(True)
        try:
            edit = controller.find(QPlainTextEdit, "chatInputEdit")
            edit.setPlainText("슈퍼맨 그려줘")
            controller._on_send_btn_clicked()
            self.assertEqual(calls, [True])
            positive = controller.find(QPlainTextEdit, "positivePromptEdit")
            self.assertEqual(positive.toPlainText().strip(), "슈퍼맨 그려줘")
            enhanced = controller.find(QPlainTextEdit, "enhancePromptEdit")
            self.assertEqual(enhanced.toPlainText().strip(), "")
            # 사용자 메시지 버블 추가됨
            bubbles = controller.window.findChildren(ChatMessage)
            self.assertTrue(any(b.role == "user" for b in bubbles))
        finally:
            controller.start_generation = orig_start

    def test_empty_enter_is_ignored(self):
        controller = _make_controller()
        calls = []
        orig_start = controller.start_generation
        controller.start_generation = lambda: calls.append(True)
        try:
            edit = controller.find(QPlainTextEdit, "chatInputEdit")
            edit.setPlainText("   ")
            controller._on_chat_enter_pressed()
            self.assertEqual(calls, [])
        finally:
            controller.start_generation = orig_start

    def test_stop_button_calls_stop(self):
        controller = _make_controller()
        stopped = []

        class FakeWorker:
            def stop(self):
                stopped.append(True)

        controller.worker = FakeWorker()
        try:
            controller._on_send_btn_clicked()
            self.assertEqual(stopped, [True])
        finally:
            controller.worker = None

    def test_image_card_appended_on_show_image(self):
        controller = _make_controller()
        from PySide6.QtGui import QPixmap
        img_path = Path(os.environ.get("TEMP", "/tmp")) / "p2_test_img.png"
        QPixmap(32, 32).save(str(img_path))
        try:
            controller._pending_chat = {"text": "고양이"}
            controller.show_image(str(img_path), add_history=False)
            cards = controller.window.findChildren(ImageCard)
            self.assertEqual(len(cards), 1)
        finally:
            try:
                img_path.unlink()
            except OSError:
                pass


if __name__ == "__main__":
    unittest.main()
