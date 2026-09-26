"""Tests for MainController — unittest 기반 (pytest 미설치)."""
from __future__ import annotations

import os
import unittest

# 헤드리스/CI 환경에서 Qt GUI 초기화 방지
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QPlainTextEdit
from PySide6.QtCore import Qt

# MainController import는 setup()이 즉시 실행되므로 주의
# 실제 위젯 Mocking은 불가능하므로 _find_or_raise만 검증
from main import MainController


class MainControllerTests(unittest.TestCase):
    def test_error_handling_find_or_raise(self) -> None:
        """_find_or_raise가 존재하지 않는 위젯에서 RuntimeError를 던지는지."""
        # 최소한의 컨트롤러 생성 (설정 파일 읽기만 수행)
        # 실제 UI 초기화는 offscreen으로 진행
        app = QApplication.instance() or QApplication([])
        controller = MainController.__new__(MainController)
        controller.config = {}
        # _find_or_raise는 self.window.findChild를 사용하므로 window 속성 필요
        from PySide6.QtWidgets import QWidget
        controller.window = QWidget()
        # 존재하지 않는 위젯 이름으로 호출 → RuntimeError 기대
        with self.assertRaises(RuntimeError):
            controller._find_or_raise(QPlainTextEdit, "존재하지않는위젯이름")

    def test_generation_snapshot_normalizes_values(self) -> None:
        """Snapshot normalization preserves supplied generation settings."""
        # 실제 위젯 트리 없이는 완전한 테스트 불가 → 구조 검증만
        # L1676-1695 기준 필수 키 목록 확인
        # 메서드 존재 확인 (코드 구조 검증)
        self.assertTrue(hasattr(MainController, "capture_snapshot"))
        # 키 목록이 코드에 존재함을 문서화 (실제 실행은 offscreen 필요)
        from app.sections.generation import build_generation_snapshot

        settings = build_generation_snapshot(
            {
                "width": 768,
                "height": 1024,
                "steps": 28,
                "cfg": 5.5,
                "seed": 123,
                "sampler": "dpmpp_2m",
                "scheduler": "karras",
                "denoise": 0.75,
            }
        )
        self.assertEqual(
            (
                settings.width,
                settings.height,
                settings.steps,
                settings.cfg,
                settings.seed,
                settings.sampler,
                settings.scheduler,
                settings.denoise,
            ),
            (768, 1024, 28, 5.5, 123, "dpmpp_2m", "karras", 0.75),
        )


if __name__ == "__main__":
    unittest.main()
