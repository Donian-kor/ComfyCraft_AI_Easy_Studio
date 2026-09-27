# -*- coding: utf-8 -*-
"""P4: 모델 피커 — 표시명/파일명 분리, 최적값, ZAnime 흐름 검증 (offscreen)."""
from __future__ import annotations

import os
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QComboBox

import main as main_module
from app.gui.chat_widgets import ChatMessage, describe_model
from app.gui.ui_loader import load_ui

BASE_DIR = Path(__file__).resolve().parent.parent
UI_FILE = BASE_DIR / "assets" / "ui" / "main.ui"

FILENAMES = [
    "flux1-dev-Q4_0.gguf",
    "ERNIE-AIO-Base-fp8.safetensors",
    "ERNIE-AIO-Turbo-fp8.safetensors",
    "z-anime_aio_v1.safetensors",
]


def _make_controller():
    app = QApplication.instance() or QApplication([])
    window = load_ui(UI_FILE)
    controller = main_module.MainController(window)
    return controller


class P4DescribeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_short_labels_and_features(self):
        from app.core.model_registry import get_model_registry
        registry = get_model_registry()
        used = set()
        shorts = {}
        for filename in FILENAMES:
            short, feature, tooltip = describe_model(
                registry.detect(filename), filename, used)
            shorts[filename] = short
            self.assertTrue(short)
            self.assertTrue(feature)
            self.assertIn(filename, tooltip)
        # ERNIE Base/Turbo 구분
        self.assertNotEqual(
            shorts["ERNIE-AIO-Base-fp8.safetensors"],
            shorts["ERNIE-AIO-Turbo-fp8.safetensors"])
        self.assertIn("Base", shorts["ERNIE-AIO-Base-fp8.safetensors"])
        self.assertIn("Turbo", shorts["ERNIE-AIO-Turbo-fp8.safetensors"])


class P4ComboDataTests(unittest.TestCase):
    def test_display_and_data_separation(self):
        controller = _make_controller()
        controller.set_models([], FILENAMES)
        combo = controller.find(QComboBox, "comfyModelCombo")
        self.assertEqual(combo.count(), len(FILENAMES))
        for i, filename in enumerate(FILENAMES):
            # 표시 텍스트에 정확한 파일명이 그대로 있으면 안 됨
            self.assertNotEqual(combo.itemText(i), filename)
            # itemData에는 정확한 파일명
            self.assertEqual(str(combo.itemData(i)), filename)

    def test_helper_returns_exact_filename(self):
        controller = _make_controller()
        controller.set_models([], FILENAMES)
        combo = controller.find(QComboBox, "comfyModelCombo")
        combo.setCurrentIndex(1)
        self.assertEqual(
            controller._comfy_model_file(), FILENAMES[1])

    def test_snapshot_uses_exact_filename(self):
        controller = _make_controller()
        controller.set_models([], FILENAMES)
        combo = controller.find(QComboBox, "comfyModelCombo")
        combo.setCurrentIndex(2)
        snapshot = controller.capture_snapshot()
        self.assertEqual(snapshot["comfy_model"], FILENAMES[2])

    def test_model_change_applies_defaults_and_system_message(self):
        controller = _make_controller()
        controller.set_models([], FILENAMES)
        combo = controller.find(QComboBox, "comfyModelCombo")
        before = len(controller.window.findChildren(ChatMessage))
        combo.setCurrentIndex(1)  # 인덱스 변경 보장용 경유
        combo.setCurrentIndex(0)  # FLUX
        # 시스템 메시지 추가됨
        messages = controller.window.findChildren(ChatMessage)
        self.assertGreater(len(messages), before)
        system_texts = [m.bubble.text() for m in messages
                        if m.role == "system"]
        self.assertTrue(any("최적 설정" in text for text in system_texts))
        # Steps가 FLUX 최적값과 일치 (ZImage 기본 10이 아님)
        from app.core.model_registry import get_model_registry
        profile = get_model_registry().detect(FILENAMES[0])
        self.assertEqual(
            controller.get_steps_value(), profile.default_steps)

    def test_restore_by_exact_filename(self):
        controller = _make_controller()
        controller.set_models([], FILENAMES)
        self.assertTrue(
            controller._set_comfy_model_file(FILENAMES[3]))
        self.assertEqual(
            controller._comfy_model_file(), FILENAMES[3])
        self.assertFalse(controller._set_comfy_model_file("없음.safetensors"))


class P4ZanimeFlowTests(unittest.TestCase):
    def test_send_requests_style_when_missing(self):
        controller = _make_controller()
        controller.set_models([], ["z-anime_aio_v99.safetensors"])
        combo = controller.find(QComboBox, "comfyModelCombo")
        combo.setCurrentIndex(0)
        controller.config.prompts.zanime_style = ""
        calls = []
        orig_start = controller.start_generation
        controller.start_generation = lambda: calls.append(True)
        try:
            from PySide6.QtWidgets import QPlainTextEdit
            edit = controller.find(QPlainTextEdit, "chatInputEdit")
            edit.setPlainText("애니 고양이")
            controller._send_chat_text()
            # 생성 시작 안 됨 + 스타일 요청 메시지 표시
            self.assertEqual(calls, [])
            messages = controller.window.findChildren(ChatMessage)
            ai_texts = [m.bubble.text() for m in messages if m.role == "ai"]
            self.assertTrue(any("스타일" in t for t in ai_texts))
            # 스타일 버튼 3개 존재
            style_buttons = [
                b for b in controller.window.findChildren(object)
                if (b.objectName() or "").startswith("chatZanime_")]
            self.assertEqual(len(style_buttons), 3)
            # 웹툰 선택 → 저장 + 대기 메시지 자동 생성
            controller._on_zanime_style_picked("webtoon")
            self.assertEqual(controller.current_zanime_style(), "webtoon")
            self.assertEqual(calls, [True])
        finally:
            controller.start_generation = orig_start
            controller.config.prompts.zanime_style = ""


if __name__ == "__main__":
    unittest.main()
