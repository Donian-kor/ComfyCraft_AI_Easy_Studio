# -*- coding: utf-8 -*-
"""P7: 미리보기 모달 — 탐색·줌·회전·포커스 복원 검증 (offscreen)."""
from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel

import main as main_module
from app.gui.chat_widgets import ClickableLabel, ImageCard
from app.gui.image_preview import ImagePreviewModal
from app.gui.ui_loader import load_ui

BASE_DIR = Path(__file__).resolve().parent.parent
UI_FILE = BASE_DIR / "assets" / "ui" / "main.ui"


def _make_image(path: Path, size: int = 64) -> str:
    QPixmap(size, size).save(str(path))
    return str(path)


def _make_controller():
    app = QApplication.instance() or QApplication([])
    window = load_ui(UI_FILE)
    controller = main_module.MainController(window)
    return controller


class P7ModalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
        cls.tmp = tempfile.TemporaryDirectory()
        cls.paths = [
            _make_image(Path(cls.tmp.name) / f"img{i}.png", 64 + i * 8)
            for i in range(3)
        ]

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_open_and_navigate(self):
        modal = ImagePreviewModal(parent=None)
        modal.open_with(self.paths, 1, modal=False)
        self.assertEqual(modal.position_label.text(), "2 / 3")
        modal.show_next()
        self.assertEqual(modal.position_label.text(), "3 / 3")
        modal.show_next()
        self.assertEqual(modal.position_label.text(), "1 / 3")
        modal.show_prev()
        self.assertEqual(modal.position_label.text(), "3 / 3")
        modal.close()

    def test_single_image_disables_navigation(self):
        modal = ImagePreviewModal(parent=None)
        modal.open_with(self.paths[:1], 0, modal=False)
        self.assertFalse(modal.prev_button.isEnabled())
        self.assertFalse(modal.next_button.isEnabled())
        modal.close()

    def test_zoom_bounds(self):
        modal = ImagePreviewModal(parent=None)
        modal.open_with(self.paths[:1], 0, modal=False)
        for _ in range(20):
            modal.zoom_in()
        self.assertEqual(modal._zoom, modal.MAX_ZOOM)
        for _ in range(40):
            modal.zoom_out()
        self.assertEqual(modal._zoom, modal.MIN_ZOOM)
        modal.close()

    def test_rotate_cycles(self):
        modal = ImagePreviewModal(parent=None)
        modal.open_with(self.paths[:1], 0, modal=False)
        for _ in range(4):
            modal.rotate()
        self.assertEqual(modal._rotation, 0)
        modal.close()

    def test_empty_paths_do_nothing(self):
        modal = ImagePreviewModal(parent=None)
        modal.open_with([], 0, modal=False)
        self.assertFalse(modal.isVisible())
        modal.close()

    def test_save_callback(self):
        saved = []
        modal = ImagePreviewModal(
            parent=None, on_save=lambda p: saved.append(p))
        modal.open_with(self.paths[:1], 0, modal=False)
        modal.save_button.click()
        self.assertEqual(saved, [self.paths[0]])
        modal.close()

    def test_focus_restored_on_close(self):
        anchor = QLabel("anchor")
        anchor.show()
        calls = []
        orig_focus = anchor.setFocus
        anchor.setFocus = lambda *a, **k: (calls.append(True),
                                           orig_focus(*a, **k))
        modal = ImagePreviewModal(parent=None)
        modal.open_with(self.paths[:1], 0,
                        return_focus_widget=anchor, modal=False)
        modal.close()
        self.app.processEvents()
        # 닫힐 때 트리거 위젯으로 포커스 복원을 시도해야 함
        self.assertTrue(calls)
        anchor.close()

    def test_card_image_click_opens(self):
        fired = []
        label = ClickableLabel()
        label.clicked.connect(lambda: fired.append(True))
        from PySide6.QtTest import QTest
        from PySide6.QtCore import Qt
        QTest.mouseClick(label, Qt.MouseButton.LeftButton)
        self.assertEqual(fired, [True])

    def test_controller_opens_preview(self):
        controller = _make_controller()
        opened = []
        import app.main_controller as mc_module
        orig_modal = mc_module.ImagePreviewModal

        class FakeModal:
            def __init__(self, *args, **kwargs):
                pass

            def open_with(self, paths, index,
                          return_focus_widget=None):
                opened.append((list(paths), index))

        mc_module.ImagePreviewModal = FakeModal
        try:
            controller._chat_log = [
                {"kind": "image", "image_path": self.paths[0]},
                {"kind": "image", "image_path": self.paths[1]},
            ]
            controller._open_preview(self.paths[1])
            self.assertEqual(len(opened), 1)
            self.assertEqual(opened[0][0], self.paths[:2])
            self.assertEqual(opened[0][1], 1)
        finally:
            mc_module.ImagePreviewModal = orig_modal


if __name__ == "__main__":
    unittest.main()
