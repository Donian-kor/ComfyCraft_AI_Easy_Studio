"""Feature 계층: 실행 진행 상태 (순수 Python, UI 프레임워크 금지).

기존 app/sections/execution.py 의 Qt 위젯 애니메이션 부분을 제외하고
상태 데이터와 포매팅만 남긴다. (LoadingAnimation/ElapsedTimer 는 UI 계층 관심사)
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class ExecutionStatus:
    """생성 실행 상태."""

    running: bool = False
    progress: int = 0
    status_text: str = "대기 중"


def create_execution_status() -> ExecutionStatus:
    return ExecutionStatus()


def update_execution_status(status: ExecutionStatus, progress: int, text: str) -> None:
    status.progress = max(0, min(progress, 100))
    status.status_text = text
    status.running = progress < 100


def format_elapsed(seconds: float) -> str:
    """경과 시간을 한국어로 포매팅 (예: '1분 5초')."""
    total = int(max(0.0, float(seconds or 0.0)))
    minutes, secs = divmod(total, 60)
    hours, mins = divmod(minutes, 60)
    if hours:
        return f"{hours}시간 {mins}분 {secs}초"
    if mins:
        return f"{mins}분 {secs}초"
    return f"{secs}초"


class ElapsedCounter:
    """경과 시간 측정 (Qt 타이머 없이). UI 가 초마다 읽어간다."""

    def __init__(self) -> None:
        self._start_time: Optional[float] = None

    def start(self) -> None:
        self._start_time = time.monotonic()

    def stop(self) -> None:
        self._start_time = None

    @property
    def elapsed_seconds(self) -> float:
        if self._start_time is None:
            return 0.0
        return time.monotonic() - self._start_time

    def text(self) -> str:
        return format_elapsed(self.elapsed_seconds)
