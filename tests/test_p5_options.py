# -*- coding: utf-8 -*-
"""P5: 옵션 다듬기 — 향상 박스 숨김, 되돌리기, FD 기본값 검증 (offscreen)."""
from __future__ import annotations

import os
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFrame,
    QPlainTextEdit,
    QPushButton,
    QSlider,
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


class P5OptionsTests(unittest.TestCase):
    def test_enhance_card_hidden_but_box_kept(self):
        # P11: 향상 카드 컨테이너 삭제됨 — 박스는 히든 홀더로 유지
        controller = _make_controller()
        self.assertIsNone(controller.find(QFrame, "enhancePromptCard"))
        box = controller.find(QPlainTextEdit, "enhancePromptEdit")
        self.assertIsNotNone(box)

    def test_facedetailer_default_off(self):
        controller = _make_controller()
        check = controller.find(QCheckBox, "facedetailerCheckBox")
        self.assertIsNotNone(check)
        self.assertFalse(check.isChecked())

    def test_reset_button_exists_and_resets(self):
        controller = _make_controller()
        button = controller.find(QPushButton, "resetOptionsButton")
        self.assertIsNotNone(button)
        controller.set_models([], ["flux1-dev-Q4_0.gguf"])
        combo = controller.find(object, "comfyModelCombo")
        combo.setCurrentIndex(0)
        # 값 변경 후 되돌리기
        steps = controller.find(QSlider, "stepsSlider")
        steps.setValue(steps.minimum())
        controller._reset_options_to_defaults()
        from app.core.model_registry import get_model_registry
        profile = get_model_registry().detect("flux1-dev-Q4_0.gguf")
        self.assertEqual(
            controller.get_steps_value(), profile.default_steps)
        # FaceDetailer도 초기화됨
        check = controller.find(QCheckBox, "facedetailerCheckBox")
        self.assertFalse(check.isChecked())

    def test_reset_without_model_is_safe(self):
        controller = _make_controller()
        controller._reset_options_to_defaults()  # 모델 없음 → 안내만, 예외 없음


if __name__ == "__main__":
    unittest.main()
