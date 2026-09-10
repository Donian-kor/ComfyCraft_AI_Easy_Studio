"""Result preview and output management."""

from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog, QLabel, QMessageBox


@dataclass
class ResultInfo:
    path: str
    filename: str


def build_result_info(path: str) -> ResultInfo:
    file_path = Path(path)
    return ResultInfo(path=str(file_path), filename=file_path.name)


def ensure_output_directory(path: str) -> Path:
    output_dir = Path(path)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def show_image(preview_label: QLabel, path: str) -> bool:
    """이미지를 미리보기 라벨에 표시합니다."""
    pixmap = QPixmap(path)
    if not pixmap.isNull():
        preview_label.setPixmap(
            pixmap.scaled(
                preview_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )
        preview_label.setText("")
        return True
    return False


def save_image_as(window, current_image_path: Optional[str], output_dir: Path) -> Optional[str]:
    """이미지를 다른 이름으로 저장합니다."""
    if not current_image_path:
        return None
    source = Path(current_image_path)
    target, _ = QFileDialog.getSaveFileName(
        window, "이미지 저장", source.name, "Images (*.png *.jpg *.jpeg *.webp)"
    )
    if target:
        shutil.copy2(source, target)
        return target
    return None


def open_output_folder(output_dir: Path) -> bool:
    """출력 폴더를 엽니다."""
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        if sys.platform == "win32":
            subprocess.Popen(["explorer", str(output_dir)])
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(output_dir)])
        else:
            subprocess.Popen(["xdg-open", str(output_dir)])
        return True
    except OSError:
        return False


def build_filename_prefix(config_output, output_dir: Path) -> str:
    """파일명 접두사를 생성합니다."""
    from datetime import datetime
    prefix = config_output.filename_prefix or "ComfyUI"
    now = datetime.now()
    replacements = {
        "%date%": now.strftime("%Y%m%d"),
        "%time%": now.strftime("%H%M%S"),
        "%datetime%": now.strftime("%Y%m%d_%H%M%S"),
        "%counter%": f"{len(list(output_dir.glob('*.png'))) + 1:04d}"
    }
    for token, value in replacements.items():
        prefix = prefix.replace(token, value)
    return prefix


def show_message_box(parent, icon: QMessageBox.Icon, title: str, text: str,
                     buttons: QMessageBox.StandardButton = QMessageBox.StandardButton.Ok) -> QMessageBox.StandardButton:
    """현재 테마 스타일에 맞는 메시지 박스 표시"""
    msg_box = QMessageBox(parent)
    msg_box.setIcon(icon)
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setStandardButtons(buttons)
    msg_box.setStyleSheet("QMessageBox QLabel { min-width: 280px; }")
    return msg_box.exec()
