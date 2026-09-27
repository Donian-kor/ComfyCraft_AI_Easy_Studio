"""경로 상수 — Phase 4에서 순환 참조 방지를 위해 분리.

main_controller와 dialogs 양쪽에서 참조하는 경로 상수를 중립 모듈에 둔다.
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SETTINGS_DIALOG_FILE = BASE_DIR / "assets" / "ui" / "settings_dialog.ui"
HELP_DIALOG_FILE = BASE_DIR / "assets" / "ui" / "help_dialog_v2.ui"
