"""Execution flow, progress tracking, and loading animation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QProgressBar, QLabel


@dataclass
class ExecutionStatus:
    running: bool = False
    progress: int = 0
    status_text: str = "대기 중"


def create_execution_status() -> ExecutionStatus:
    return ExecutionStatus()


def update_execution_status(status: ExecutionStatus, progress: int, text: str) -> None:
    status.progress = max(0, min(progress, 100))
    status.status_text = text
    status.running = progress < 100


def format_elapsed(seconds: int) -> str:
    """경과 시간을 한국어로 포매팅 (예: '1분 0초', '1분 5초')"""
    minutes, secs = divmod(seconds, 60)
    hours, mins = divmod(minutes, 60)
    if hours:
        return f"{hours}시간 {mins}분 {secs}초"
    elif mins:
        return f"{mins}분 {secs}초"
    else:
        return f"{secs}초"


class LoadingAnimation:
    """로딩바 애니메이션 관리 클래스"""

    def __init__(self, progress_bar: QProgressBar, status_label: QLabel):
        self.progress_bar = progress_bar
        self.status_label = status_label
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_animation)
        self.animation_value = 0
        self.animation_direction = 1
        self.is_animating = False

    def start(self, status_text: str):
        self.is_animating = True
        self.animation_value = 0
        self.animation_direction = 1
        self.status_label.setText(status_text)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.timer.start(50)

    def stop(self):
        self.is_animating = False
        self.timer.stop()
        self.progress_bar.setValue(100)

    def _update_animation(self):
        if not self.is_animating:
            return

        self.animation_value += 2 * self.animation_direction

        if self.animation_value >= 100:
            self.animation_value = 100
            self.animation_direction = -1
        elif self.animation_value <= 0:
            self.animation_value = 0
            self.animation_direction = 1

        self.progress_bar.setValue(self.animation_value)

    def set_real_progress(self, value: int):
        """실제 진행률이 들어오면 애니메이션 정지"""
        if value > 0:
            self.stop()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(max(0, min(100, value)))


class ElapsedTimer:
    """경과 시간 측정 및 표시 클래스"""

    def __init__(self, elapsed_label: QLabel):
        self.elapsed_label = elapsed_label
        self.timer = QTimer()
        self.timer.timeout.connect(self._update)
        self.start_time: Optional[float] = None

    def start(self):
        import time
        self.start_time = time.monotonic()
        self.timer.start(1000)

    def stop(self):
        self.timer.stop()

    def _update(self):
        if self.start_time is not None:
            import time
            elapsed = int(time.monotonic() - self.start_time)
            self.elapsed_label.setText(format_elapsed(elapsed))
