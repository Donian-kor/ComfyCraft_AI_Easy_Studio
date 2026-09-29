"""Feature 계층: 생성 결과 파일 관리 (순수 Python, UI 프레임워크 금지).

기존 app/sections/result.py 에서 Qt 위젯 연동만 뺀 부분을 옮긴 것이다.
(미리보기 라벨 조작, 파일 다이얼로그, 메시지 박스는 UI 계층 관심사이므로 제외)
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class ResultInfo:
    """생성 결과 파일 정보."""

    path: str
    filename: str


def build_result_info(path: str) -> ResultInfo:
    file_path = Path(path)
    return ResultInfo(path=str(file_path), filename=file_path.name)


def ensure_output_directory(path: str) -> Path:
    output_dir = Path(path)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def open_output_folder(output_dir: Path) -> bool:
    """출력 폴더를 운영체제 파일 관리자로 연다."""
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
    """%date%/%time%/%counter% 같은 토큰을 채운 파일명 접두사를 만든다."""
    prefix = getattr(config_output, "filename_prefix", "") or "ComfyUI"
    now = datetime.now()
    replacements = {
        "%date%": now.strftime("%Y%m%d"),
        "%time%": now.strftime("%H%M%S"),
        "%datetime%": now.strftime("%Y%m%d_%H%M%S"),
        "%counter%": f"{len(list(Path(output_dir).glob('*.png'))) + 1:04d}",
    }
    for token, value in replacements.items():
        prefix = prefix.replace(token, value)
    return prefix


def copy_image(source_path: str, target_path: str) -> Optional[str]:
    """이미지를 다른 이름으로 복사한다. 실패하면 None."""
    try:
        source = Path(source_path)
        if not source.exists():
            return None
        shutil.copy2(source, target_path)
        return target_path
    except OSError:
        return None
