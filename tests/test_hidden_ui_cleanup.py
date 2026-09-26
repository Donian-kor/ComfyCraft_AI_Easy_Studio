# -*- coding: utf-8 -*-
"""hiddenSettingsContainer 제거 회귀 방지 — 죽은 위젯 참조가 코드에 남지 않았는지 검증."""
from __future__ import annotations

import os
import unittest
from pathlib import Path

# 헤드리스/CI 환경에서 Qt GUI 초기화 방지
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.gui.ui_loader import load_ui

BASE_DIR = Path(__file__).resolve().parent.parent
UI_FILE = BASE_DIR / "assets" / "ui" / "main.ui"

# 제거 대상 위젯 (그룹A/B/C — 수정계획안.md §1 기준)
REMOVED_WIDGETS = [
    "hiddenSettingsContainer",
    "lmUrlEdit",
    "comfyUrlEdit",
    "comfyModelPathEdit",
    "lmStatusLabel",
    "comfyStatusLabel",
    "modelPathStatusLabel",
    "lmCheckButton",
    "comfyCheckButton",
    "browseModelFolderButton",
    "loadConfigButton",
    "saveConfigButton",
    "restoreDefaultsButton",
    "exitButton",
    "helpBrowser",
]


def _load_window() -> QWidget:
    """main.ui를 offscreen으로 로드한다 (앱당 1회 QApplication)."""
    app = QApplication.instance() or QApplication([])
    return load_ui(UI_FILE)


class HiddenUiRemovalTests(unittest.TestCase):
    """죽은 UI 제거가 완전했는지, 그리고 살아있는 위젯이 손상되지 않았는지 검증."""

    def test_removed_widgets_absent_from_ui(self) -> None:
        """main.ui에 죽은 위젯이 남아있지 않아야 한다."""
        window = _load_window()
        for name in REMOVED_WIDGETS:
            with self.subTest(widget=name):
                self.assertIsNone(
                    window.findChild(QWidget, name),
                    f"{name} 이(가) 여전히 main.ui 위젯 트리에 존재합니다",
                )

    def test_removed_widget_names_absent_from_ui_xml(self) -> None:
        """main.ui XML에 죽은 위젯명이 name 속성으로 남아있지 않아야 한다."""
        xml = UI_FILE.read_text(encoding="utf-8")
        for name in REMOVED_WIDGETS:
            with self.subTest(widget=name):
                self.assertNotIn(f'name="{name}"', xml)

    def test_settings_layout_absent(self) -> None:
        """settingsLayout(테마 폴백 대상)이 제거되어야 한다."""
        window = _load_window()
        self.assertIsNone(window.findChild(QVBoxLayout, "settingsLayout"))

    def test_surviving_widgets_still_present(self) -> None:
        """정리 과정에서 살아있는 위젯이 실수로 삭제되지 않았는지 확인."""
        window = _load_window()
        self.assertIsNotNone(window.findChild(QWidget, "themeComboBox"))
        self.assertIsNotNone(window.findChild(QPushButton, "helpButton"))
        self.assertIsNotNone(window.findChild(QPushButton, "settingsButton"))
        self.assertIsNotNone(window.findChild(QLabel, "positivePromptEdit")
                             or window.findChild(QWidget, "positivePromptEdit"))

    def test_main_py_has_no_dead_widget_lookup(self) -> None:
        """main.py에 죽은 위젯 문자열 참조가 (주석 제외) 남아있지 않아야 한다."""
        source = (BASE_DIR / "main.py").read_text(encoding="utf-8")
        live_code = "\n".join(
            line for line in source.splitlines() if not line.lstrip().startswith("#")
        )
        for name in REMOVED_WIDGETS:
            with self.subTest(widget=name):
                self.assertNotIn(
                    f'"{name}"',
                    live_code,
                    f"main.py에 죽은 위젯 참조가 남아있습니다: {name}",
                )

    def test_load_config_does_not_crash(self) -> None:
        """load_config()가 죽은 위젯 접근으로 AttributeError를 내면 안 된다.

        회귀 버그: main.py:1389의 comfyModelPathEdit.setText()가
        위젯 제거 후 NoneType 크래시를 유발했다.
        """
        import main as main_module
        from PySide6.QtWidgets import QMessageBox

        # 모달 대화상자가 테스트를 멈추지 않도록 무효화
        original_msg = main_module.show_message_box
        original_exec = QMessageBox.exec
        main_module.show_message_box = lambda *a, **k: None
        QMessageBox.exec = lambda self, *a, **k: QMessageBox.StandardButton.Ok
        try:
            window = _load_window()
            controller = main_module.MainController(window)
            controller.load_config()  # 크래시하던 지점
        finally:
            main_module.show_message_box = original_msg
            QMessageBox.exec = original_exec


if __name__ == "__main__":
    unittest.main()
