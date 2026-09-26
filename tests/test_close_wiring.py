"""스레드 풀 종료 및 창 close 이벤트 배선 검증 — [7번] 스레드 관리 개선 회귀 방지."""
from __future__ import annotations

import inspect
import os
import time
import unittest
from concurrent.futures import ThreadPoolExecutor

# 헤드리스/CI 환경에서 Qt GUI 초기화 방지
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QCoreApplication, QEvent, QTimer
from PySide6.QtWidgets import QApplication, QWidget

from main import MainController


def _make_partial_controller(window: QWidget) -> MainController:
    """__init__(setup()) 없이 close() 동작에 필요한 속성만 구성한 컨트롤러."""
    controller = MainController.__new__(MainController)
    controller.window = window
    controller._closing = False
    controller._close_allowed = False
    controller.worker = None
    controller._io_pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="TIo")
    controller._gen_pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="TGen")
    controller.close_timer = QTimer(window)
    controller.close_timer.setSingleShot(True)
    controller.close_timer.timeout.connect(controller._finalize_window_close)
    return controller


def _wait_until(cond, timeout: float = 3.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline and not cond():
        QCoreApplication.processEvents()
        time.sleep(0.02)


class ThreadCloseWiringTests(unittest.TestCase):
    def test_init_installs_window_event_filter(self) -> None:
        """__init__이 window에 close 이벤트 필터를 설치하고 풀을 생성해야 한다."""
        src = inspect.getsource(MainController.__init__)
        self.assertIn("installEventFilter(self)", src)
        self.assertIn("_io_pool", src)
        self.assertIn("_gen_pool", src)

    def test_close_shuts_down_thread_pools(self) -> None:
        """close()는 즉시 스레드 풀을 shutdown해야 한다 (대기 중 작업 취소 포함)."""
        app = QApplication.instance() or QApplication([])
        window = QWidget()
        controller = _make_partial_controller(window)
        controller.close()
        # shutdown된 풀은 새 작업을 예약할 수 없음
        with self.assertRaises(RuntimeError):
            controller._io_pool.submit(lambda: None)
        with self.assertRaises(RuntimeError):
            controller._gen_pool.submit(lambda: None)
        # close() 진입 시 재진입 가드가 설정되어야 함
        self.assertTrue(controller._closing)
        app.processEvents()

    def test_close_event_consumed_until_finalize(self) -> None:
        """정리 완료 전의 창 close(X) 이벤트는 소비되어 창이 유지되어야 한다."""
        app = QApplication.instance() or QApplication([])
        window = QWidget()
        window.show()
        controller = _make_partial_controller(window)
        app.processEvents()
        self.assertTrue(window.isVisible())

        close_event = QEvent(QEvent.Type.Close)

        # 1차 close 이벤트 → 소비(True) + 정리 시작, 창은 그대로 유지
        self.assertTrue(controller.eventFilter(window, close_event))
        app.processEvents()
        self.assertTrue(window.isVisible())
        # 풀은 이미 shutdown됨
        with self.assertRaises(RuntimeError):
            controller._io_pool.submit(lambda: None)

        # 2차 X 클릭(정리 중) → 중복 close() 호출 없이 계속 소비
        self.assertTrue(controller.eventFilter(window, close_event))

        # close_timer(100ms) 만료 → _finalize_window_close → 실제 종료
        _wait_until(lambda: not window.isVisible())
        self.assertFalse(window.isVisible())

        # 종료 허용 후에는 close 이벤트가 통과(False)
        self.assertFalse(controller.eventFilter(window, close_event))

    def test_close_event_consumed_when_cleanup_started_elsewhere(self) -> None:
        """종료 버튼으로 정리가 시작된 뒤의 X 클릭도 안전하게 소비되어야 한다."""
        app = QApplication.instance() or QApplication([])
        window = QWidget()
        window.show()
        controller = _make_partial_controller(window)
        controller.close()  # exitButton 경로
        app.processEvents()
        self.assertTrue(controller._closing)
        self.assertTrue(window.isVisible())
        self.assertTrue(controller.eventFilter(window, QEvent(QEvent.Type.Close)))
        # timer 만료 후 실제 종료
        _wait_until(lambda: not window.isVisible())
        self.assertFalse(window.isVisible())


if __name__ == "__main__":
    unittest.main()