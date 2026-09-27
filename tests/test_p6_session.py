# -*- coding: utf-8 -*-
"""P6: 세션·이력 — 매니저 CRUD, 저장 트리거, 전환·잠금, 수정 요청 검증."""
from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QListWidget, QPlainTextEdit

import main as main_module
from app.gui.chat_widgets import ChatMessage, ImageCard
from app.gui.ui_loader import load_ui
from app.sections.session import SessionManager

BASE_DIR = Path(__file__).resolve().parent.parent
UI_FILE = BASE_DIR / "assets" / "ui" / "main.ui"


def _make_controller():
    app = QApplication.instance() or QApplication([])
    window = load_ui(UI_FILE)
    controller = main_module.MainController(window)
    return controller


class P6ManagerTests(unittest.TestCase):
    def test_crud_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = SessionManager(Path(tmp) / ".sessions")
            session = manager.new_session(model="flux.safetensors")
            session["title"] = "고양이 그리기"
            session["messages"] = [
                {"kind": "user", "text": "고양이", "timestamp": "t"}]
            self.assertTrue(manager.save_session(session))
            entries = manager.list_sessions()
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]["title"], "고양이 그리기")
            loaded = manager.load_session(session["session_id"])
            self.assertEqual(loaded["messages"][0]["text"], "고양이")
            self.assertTrue(
                manager.rename_session(session["session_id"], "강아지"))
            self.assertEqual(
                manager.load_session(session["session_id"])["title"], "강아지")
            self.assertTrue(manager.delete_session(session["session_id"]))
            self.assertEqual(manager.list_sessions(), [])

    def test_list_order_and_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = SessionManager(Path(tmp) / ".sessions")
            for title in ("a", "b", "c"):
                session = manager.new_session()
                session["title"] = title
                manager.save_session(session)
            entries = manager.list_sessions()
            self.assertEqual([e["title"] for e in entries], ["c", "b", "a"])
            self.assertEqual(len(manager.list_sessions(limit=2)), 2)


class P6SessionFlowTests(unittest.TestCase):
    def _make_isolated(self):
        controller = _make_controller()
        tmp = tempfile.TemporaryDirectory()
        controller.session_manager = SessionManager(
            Path(tmp.name) / ".sessions")
        controller._tmpdir = tmp  # 테스트 종료 후 정리 방지용 참조 유지
        # 생성 시 실제 디렉토리에서 복원됐을 수 있는 상태를 초기화
        controller._current_session = None
        controller._chat_log = []
        controller._clear_chat_widgets()
        return controller

    def test_send_creates_session_file(self):
        controller = self._make_isolated()
        calls = []
        orig_start = controller.start_generation
        controller.start_generation = lambda: calls.append(True)
        try:
            edit = controller.find(QPlainTextEdit, "chatInputEdit")
            edit.setPlainText("고양이 그려줘")
            controller._send_chat_text()
            self.assertEqual(calls, [True])
            session = controller._current_session
            self.assertIsNotNone(session)
            self.assertTrue(session["title"].startswith("고양이"))
            loaded = controller.session_manager.load_session(
                session["session_id"])
            self.assertTrue(any(
                m.get("kind") == "user" for m in loaded["messages"]))
        finally:
            controller.start_generation = orig_start

    def test_switch_renders_messages(self):
        controller = self._make_isolated()
        manager = controller.session_manager
        session = manager.new_session()
        session["title"] = "복원 테스트"
        session["messages"] = [
            {"kind": "user", "text": "hello",
             "timestamp": "2026-01-01T00:00:00"},
            {"kind": "ai", "text": "world",
             "timestamp": "2026-01-01T00:00:01"},
        ]
        manager.save_session(session)
        self.assertTrue(controller._switch_session(session["session_id"]))
        bubbles = controller.window.findChildren(ChatMessage)
        texts = [b.bubble.text() for b in bubbles]
        self.assertIn("hello", texts)
        self.assertIn("world", texts)

    def test_new_chat_blocked_while_generating(self):
        controller = self._make_isolated()
        controller._ensure_session()
        before = controller._current_session["session_id"]

        class FakeWorker:
            def stop(self):
                pass

        controller.worker = FakeWorker()
        try:
            controller._on_new_chat_clicked()
            controller._switch_session("nope")
            self.assertEqual(
                controller._current_session["session_id"], before)
        finally:
            controller.worker = None

    def test_reuse_restores_full_snapshot(self):
        controller = self._make_isolated()
        snapshot = {
            "prompt": "a cat", "negative": "blurry",
            "comfy_model": "flux1-dev-Q4_0.gguf",
            "width": 1152, "height": 896, "steps": 28, "cfg": 5.0,
            "seed": 777, "sampler": "euler", "scheduler": "normal",
            "denoise": 1.0, "enhance_prompt": "a cat, detailed",
        }
        controller._on_reuse_request(snapshot)
        positive = controller.find(QPlainTextEdit, "positivePromptEdit")
        self.assertEqual(positive.toPlainText().strip(), "a cat")
        from PySide6.QtWidgets import QSpinBox
        seed = controller.find(QSpinBox, "seedSpinBox")
        self.assertEqual(seed.value(), 777)
        self.assertEqual(controller.get_steps_value(), 28)
        edit = controller.find(QPlainTextEdit, "chatInputEdit")
        self.assertIn("a cat", edit.toPlainText())

    def test_history_list_refresh(self):
        controller = self._make_isolated()
        manager = controller.session_manager
        for title in ("세션1", "세션2"):
            session = manager.new_session()
            session["title"] = title
            manager.save_session(session)
        controller._refresh_history_list()
        history_list = controller.find(QListWidget, "historyList")
        self.assertIsNotNone(history_list)
        self.assertEqual(history_list.count(), 2)

    def test_recent_menu_populated(self):
        controller = self._make_isolated()
        manager = controller.session_manager
        session = manager.new_session()
        session["title"] = "최근항목"
        manager.save_session(session)
        controller._rebuild_recent_menu()
        menu = controller._recent_menu
        texts = [a.text() for a in menu.actions() if not a.isSeparator()]
        self.assertIn("최근항목", texts)


if __name__ == "__main__":
    unittest.main()
