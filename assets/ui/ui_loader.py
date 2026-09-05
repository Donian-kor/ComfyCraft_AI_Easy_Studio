from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader


def load_ui(path: Path):
    loader = QUiLoader()
    file = QFile(str(path))
    if not file.open(QIODevice.ReadOnly):
        raise RuntimeError(f"UI 파일을 열 수 없습니다: {path}")
    try:
        obj = loader.load(file)
    finally:
        file.close()
    if obj is None:
        raise RuntimeError(f"Qt가 UI 파일을 읽지 못했습니다: {path}")
    return obj
