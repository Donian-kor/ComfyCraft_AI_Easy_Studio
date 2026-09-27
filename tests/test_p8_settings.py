# -*- coding: utf-8 -*-
"""P8: 설정 다이얼로그 — 탭 구조, 수동 프로필 검증·저장·삭제 검증."""
from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QLineEdit,
    QListWidget,
    QPushButton,
    QTabWidget,
)

from app.core.model_registry import ModelRegistry
from app.gui.dialogs.settings_dialog import (
    profile_data_to_registry,
    save_manual_profile,
    validate_manual_profile,
)
from app.gui.ui_loader import load_dialog_ui
from app.paths import SETTINGS_DIALOG_FILE

BASE_DIR = Path(__file__).resolve().parent.parent

GOOD = {
    "name": "my-test-model",
    "patterns": "mytest, my_test",
    "workflow_type": "checkpoint",
    "steps": 25,
    "cfg": 6.5,
    "sampler": "euler",
    "scheduler": "normal",
    "clip1": "",
    "clip2": "",
    "vae": "",
}


class P8ValidateTests(unittest.TestCase):
    def test_valid_passes(self):
        self.assertEqual(validate_manual_profile(dict(GOOD)), [])

    def test_empty_name_blocked(self):
        data = dict(GOOD, name="  ")
        self.assertTrue(validate_manual_profile(data))

    def test_bad_name_blocked(self):
        data = dict(GOOD, name="한글 이름!")
        self.assertTrue(validate_manual_profile(data))

    def test_empty_patterns_blocked(self):
        data = dict(GOOD, patterns=" , ")
        self.assertTrue(validate_manual_profile(data))

    def test_bad_workflow_blocked(self):
        data = dict(GOOD, workflow_type="custom_json")
        errors = validate_manual_profile(data)
        self.assertTrue(errors)

    def test_out_of_range_blocked(self):
        self.assertTrue(validate_manual_profile(dict(GOOD, steps=0)))
        self.assertTrue(validate_manual_profile(dict(GOOD, steps=201)))
        self.assertTrue(validate_manual_profile(dict(GOOD, cfg=0.0)))
        self.assertTrue(validate_manual_profile(dict(GOOD, cfg=99.0)))

    def test_save_blocked_on_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            ok, message = save_manual_profile(
                dict(GOOD, name=""), Path(tmp))
            self.assertFalse(ok)
            self.assertTrue(message)
            self.assertEqual(list(Path(tmp).glob("*.json")), [])

    def test_save_and_detect(self):
        with tempfile.TemporaryDirectory() as tmp:
            ok, message = save_manual_profile(dict(GOOD), Path(tmp))
            self.assertTrue(ok, message)
            files = list(Path(tmp).glob("*.json"))
            self.assertEqual(len(files), 1)
            payload = profile_data_to_registry(dict(GOOD))
            profile_data = payload["my-test-model"]
            from app.core.model_profiles.base import ModelProfile
            registry = ModelRegistry()
            registry.register(ModelProfile(
                name=profile_data["name"],
                family=profile_data["family"],
                aliases=tuple(profile_data["aliases"]),
                patterns=tuple(profile_data["patterns"]),
                workflow_type=profile_data["workflow_type"],
                default_clip1=profile_data["default_clip1"],
                default_clip2=profile_data["default_clip2"],
                default_vae=profile_data["default_vae"],
                default_steps=profile_data["default_steps"],
                default_cfg=profile_data["default_cfg"],
                sampler_name=profile_data["sampler_name"],
                scheduler=profile_data["scheduler"],
                priority=profile_data["priority"],
            ))
            detected = registry.detect("something_mytest_v1.safetensors")
            self.assertEqual(detected.name, "my-test-model")
            self.assertEqual(detected.default_steps, 25)


class P8DialogStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_tabs_and_model_widgets_present(self):
        dlg = load_dialog_ui(SETTINGS_DIALOG_FILE)
        tabs = dlg.findChild(QTabWidget, "settingsTabWidget")
        self.assertIsNotNone(tabs)
        titles = [tabs.tabText(i) for i in range(tabs.count())]
        self.assertIn("AI 서버", titles)
        self.assertTrue(any(t.startswith("이미지 모델") for t in titles))
        for name, widget_type in (
            ("profileAutoList", QListWidget),
            ("profileNameEdit", QLineEdit),
            ("profilePatternsEdit", QLineEdit),
            ("profileWorkflowCombo", QComboBox),
            ("profileFileCombo", QComboBox),
            ("profileDeleteBtn", QPushButton),
            ("profileSaveBtn", QPushButton),
        ):
            with self.subTest(widget=name):
                self.assertIsNotNone(dlg.findChild(widget_type, name))

    def test_existing_controls_preserved(self):
        dlg = load_dialog_ui(SETTINGS_DIALOG_FILE)
        for name, widget_type in (
            ("dlgComfyUrlEdit", QLineEdit),
            ("dlgModelPathEdit", QLineEdit),
            ("dlgLmUrlEdit", QLineEdit),
            ("dlgComfyCheckBtn", QPushButton),
            ("dlgLmCheckBtn", QPushButton),
            ("dlgBrowseBtn", QPushButton),
            ("dlgLoadConfigBtn", QPushButton),
            ("dlgResetDefaultsBtn", QPushButton),
            ("dlgSaveCloseBtn", QPushButton),
        ):
            with self.subTest(widget=name):
                self.assertIsNotNone(dlg.findChild(widget_type, name))


if __name__ == "__main__":
    unittest.main()
