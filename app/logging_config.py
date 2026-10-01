"""로깅 설정 — main.py에서 분리됨 (Phase 1).

Qt 위젯에 로그를 흘리던 QPlainTextEditLogger 는 Flet 전환으로 제거했다.
현재는 파일 로깅만 담당한다.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(base_dir: Path | None = None) -> None:
    """파일 로깅을 설정합니다.

    로그 포맷, 파일 위치(app.log), 회전 정책(2MB/백업 3개)은
    기존 동작과 동일하게 유지한다.
    """
    if base_dir is None:
        from app.paths import BASE_DIR

        base_dir = BASE_DIR
    base_dir = Path(base_dir)

    # 로그 파일 (프로젝트 루트 옆 app.log) — 2MB 초과 시 회전하며 최대 3개 백업 유지
    file_handler = RotatingFileHandler(
        base_dir / "app.log", maxBytes=2_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

    # root logger에 부착 → app.* 모듈 로거의 debug 기록도 파일로 남는다
    # (main 로거에만 붙이면 propagate 경로와 이중 기록이 생기므로 root 에만 붙인다)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    # 앱 재시작 시 핸들러가 누적되지 않도록 기존 파일 핸들러를 걷어낸다
    for handler in list(root_logger.handlers):
        if isinstance(handler, RotatingFileHandler):
            root_logger.removeHandler(handler)
            handler.close()
    root_logger.addHandler(file_handler)
