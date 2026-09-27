"""로깅 설정 — main.py에서 분리됨 (Phase 1)."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class QPlainTextEditLogger(logging.Handler):
    """QPlainTextEdit에 로그를 출력하는 핸들러."""

    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)
        if self.widget is not None:
            self.widget.appendPlainText(msg)


def setup_logging(base_dir: Path) -> None:
    """파일 로깅을 설정합니다.

    로그 포맷, 파일 위치(app.log), 회전 정책(2MB/백업 3개)은
    기존 main.py의 동작과 동일하게 유지한다.
    """
    # 로그 파일 (프로젝트 루트 옆 app.log) — 2MB 초과 시 회전하며 최대 3개 백업 유지
    file_handler = RotatingFileHandler(
        base_dir / "app.log", maxBytes=2_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    # root logger에 부착 → app.* 모듈 로거(예: generation.py의 debug)도 파일로 기록됨
    # (main 로거에 붙이면 propagate 경로와 이중 기록이 생기므로 root에만 붙인다)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
