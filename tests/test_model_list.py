# -*- coding: utf-8 -*-
"""모델 목록 정리 + 채팅 오류 메시지 검증."""
from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QPushButton

import main as main_module
from app.gui.chat_widgets import ChatMessage
from app.gui.ui_loader import load_ui
from app.sections.connection import scan_comfyui_model_names

BASE_DIR = Path(__file__).resolve().parent.parent
UI_FILE = BASE_DIR / "assets" / "ui" / "main.ui"


def _make_controller():
    app = QApplication.instance() or QApplication([])
    window = load_ui(UI_FILE)
    controller = main_module.MainController(window)
    return controller


class ModelScanTests(unittest.TestCase):
    def _make_tree(self, root: Path, files: list) -> None:
        (root / "checkpoints").mkdir(parents=True, exist_ok=True)
        (root / "diffusion_models").mkdir(parents=True, exist_ok=True)
        for name in files:
            (root / "checkpoints" / name).write_bytes(b"fake")

    def test_legit_models_included(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._make_tree(root, [
                "juggernautXL_ragnarok.safetensors",
                "flux1-dev-Q4_0.gguf",
                "qwen_image_fp8.safetensors",
            ])
            names = scan_comfyui_model_names(str(root))
            self.assertIn("juggernautXL_ragnarok.safetensors", names)
            self.assertIn("flux1-dev-Q4_0.gguf", names)
            # Qwen-Image는 이미지 모델이므로 포함
            self.assertIn("qwen_image_fp8.safetensors", names)

    def test_non_models_excluded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._make_tree(root, [
                "t5xxl_fp16.safetensors",
                "umt5_xxl_fp8.safetensors",
                "qwen_2.5_vl_7b_fp8.gguf",
                "llama-3-8b-Q4.gguf",
                "clip_l.safetensors",
                "my-vae-model.safetensors",
                "controlnet-canny.safetensors",
                "upscaler-esrgan.safetensors",
                "some-lora.safetensors",
                "real-model.safetensors",
            ])
            names = scan_comfyui_model_names(str(root))
            self.assertIn("real-model.safetensors", names)
            for bad in ("t5xxl_fp16.safetensors",
                        "umt5_xxl_fp8.safetensors",
                        "qwen_2.5_vl_7b_fp8.gguf",
                        "llama-3-8b-Q4.gguf",
                        "clip_l.safetensors",
                        "my-vae-model.safetensors",
                        "controlnet-canny.safetensors",
                        "upscaler-esrgan.safetensors",
                        "some-lora.safetensors"):
                with self.subTest(model=bad):
                    self.assertNotIn(bad, names)


class ChatErrorTests(unittest.TestCase):
    def test_error_message_with_buttons(self):
        controller = _make_controller()
        controller.show_error_banner("연결 실패")
        messages = controller.window.findChildren(ChatMessage)
        ai_texts = [m.bubble.text() for m in messages if m.role == "ai"]
        self.assertTrue(any("연결 실패" in t for t in ai_texts))
        for name in ("chatErrRetryBtn", "chatErrEditBtn", "chatErrLogBtn"):
            with self.subTest(button=name):
                self.assertIsNotNone(
                    controller.window.findChild(QPushButton, name))

    def test_empty_error_does_nothing(self):
        controller = _make_controller()
        before = len(controller.window.findChildren(ChatMessage))
        controller.show_error_banner("")
        controller.clear_error_banner()
        after = len(controller.window.findChildren(ChatMessage))
        self.assertEqual(before, after)

    def test_retry_without_history_is_safe(self):
        controller = _make_controller()
        controller._retry_last_request()  # 기록 없음 → 안내만, 예외 없음
        controller._reuse_last_snapshot()  # 스냅샷 없음 → 안내만, 예외 없음


if __name__ == "__main__":
    unittest.main()
