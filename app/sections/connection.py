"""Connection-related logic for LM Studio and ComfyUI.

This module is part of the rebuild layout and keeps the connection state
responsibilities isolated from the main UI entry point.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import requests


@dataclass
class ConnectionStatus:
    service: str
    url: str
    ok: bool = False
    message: str = "미확인"


def _normalize_url(url: str) -> str:
    value = (url or "").strip()
    if not value:
        return ""
    return value.rstrip("/")


def _coerce_path_string(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, os.PathLike):
        value = os.fspath(value)
    if isinstance(value, str):
        return value.strip().replace("\\", "/").rstrip("/")
    return str(value).strip().replace("\\", "/").rstrip("/")


def _probe_endpoint(url: str, endpoint: str, timeout: tuple[float, float] = (0.1, 0.15), max_retries: int = 1) -> bool:
    """프로브 엔드포인트 체크 (초고속 응답 확인)"""
    normalized = _normalize_url(url)
    if not normalized:
        return False
    
    try:
        # HEAD 요청으로 초고속 확인 (응답 헤더만 받음)
        response = requests.head(f"{normalized}{endpoint}", timeout=(0.1, 0.1), allow_redirects=False)
        return response.status_code < 400
    except (requests.Timeout, requests.ConnectionError):
        try:
            # HEAD 실패 시 GET으로 재시도 (매우 짧은 타임아웃)
            response = requests.get(f"{normalized}{endpoint}", timeout=(0.1, 0.1))
            return response.status_code < 400
        except Exception:
            return False
    except Exception:
        return False


def resolve_live_url(service: str, preferred_url: Optional[str] = None, candidates: Optional[Iterable[str]] = None) -> str:
    """Return the live URL for the requested service.
    
    Only checks the provided URL (from UI input). Does not fall back to other candidates.
    """
    service_name = (service or "").lower()
    endpoint = "/v1/models" if "lm" in service_name else "/system_stats"

    # 사용자가 입력한 URL만 확인
    normalized = _normalize_url(preferred_url)
    if normalized and _probe_endpoint(normalized, endpoint):
        return normalized

    # URL이 없거나 연결 실패 시 빈 문자열 반환
    return ""


def check_connection_status(service: str, url: str, candidates: Optional[Iterable[str]] = None) -> ConnectionStatus:
    """Validate a remote service connection using a live server probe."""
    resolved_url = resolve_live_url(service, url, candidates)
    status = ConnectionStatus(service=service, url=resolved_url, ok=False, message="未確認")
    if not resolved_url:
        status.message = "URL이 비어 있습니다."
        return status

    endpoint = "/v1/models" if "lm" in (service or "").lower() else "/system_stats"
    status.ok = _probe_endpoint(resolved_url, endpoint)
    status.message = f"{service} 연결됨" if status.ok else f"{service} 연결 안 됨"
    return status


def get_default_comfyui_model_roots() -> list[str]:
    """Return the common local ComfyUI model directory roots used by the original GUI."""
    env_candidates = [
        os.environ.get("COMFYUI_MODEL_PATH"),
        os.environ.get("COMFYUI_PATH"),
    ]

    local_candidates = [
        r"C:/ComfyUI/models",
        r"C:/ComfyUI_windows_portable/ComfyUI/models",
        r"D:/ComfyUI/models",
        r"E:/ComfyUI/models",
        str(Path.home() / "AppData" / "Local" / "Comfy-Desktop" / "ComfyUI-Shared" / "models"),
        str(Path.home() / "AppData" / "Local" / "Comfy-Desktop" / "ComfyUI-Installs" / "ComfyUI" / "ComfyUI" / "models"),
    ]

    ordered = []
    seen = set()
    for candidate in [*env_candidates, *local_candidates]:
        normalized = _normalize_url(candidate) if isinstance(candidate, str) else ""
        if not normalized:
            continue
        normalized = normalized.replace("\\", "/").rstrip("/")
        if normalized and normalized not in seen:
            seen.add(normalized)
            ordered.append(normalized)
    return ordered


def resolve_model_directory(preferred_path: Optional[str] = None, extra_candidates: Optional[Iterable[str]] = None) -> str:
    """Resolve the first existing ComfyUI model root containing typical subdirectories."""
    subdirs = ("checkpoints", "diffusion_models", "unet", "vae", "clip", "text_encoders", "loras")
    ordered = []
    seen = set()

    for value in [preferred_path, *list(extra_candidates or [])]:
        candidate = _coerce_path_string(value)
        if candidate and candidate not in seen:
            seen.add(candidate)
            ordered.append(candidate)

    for candidate in get_default_comfyui_model_roots():
        if candidate not in seen:
            seen.add(candidate)
            ordered.append(candidate)

    for candidate in ordered:
        candidate_path = Path(candidate).expanduser()
        if candidate_path.exists() and any((candidate_path / subdir).is_dir() for subdir in subdirs):
            return str(candidate_path)

    for candidate in ordered:
        candidate_path = Path(candidate).expanduser()
        if candidate_path.exists():
            return str(candidate_path)

    return ""


def scan_comfyui_model_names(model_root: Optional[str] = None, extra_candidates: Optional[Iterable[str]] = None) -> list[str]:
    """Scan a ComfyUI model root for the model names the GUI expects to show."""
    root = resolve_model_directory(model_root, extra_candidates)
    if not root:
        return []

    root_path = Path(root).expanduser()
    if not root_path.exists():
        return []

    valid_suffixes = {".safetensors", ".ckpt", ".pt", ".bin", ".gguf", ".sft"}
    allowed_subdirs = ("checkpoints", "diffusion_models", "unet")
    excluded_tokens = ("vae", "clip", "text_encoder", "text_encoders", "tokenizer", "embeddings")
    names: list[str] = []
    seen: set[str] = set()

    for subdir in allowed_subdirs:
        folder = root_path / subdir
        if not folder.exists():
            continue
        for file_path in folder.rglob("*"):
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() not in valid_suffixes:
                continue
            name = file_path.name
            lower_name = name.lower()
            if any(token in lower_name for token in excluded_tokens):
                continue
            if name and name not in seen:
                seen.add(name)
                names.append(name)

    return names


def check_connection_silent(service: str, url: str, timeout: float = 0.3) -> bool:
    """조용하게 연결 확인 (자동 초기화용) - 매우 빠른 응답"""
    try:
        from app.core.api_client import LMStudioApiClient, ComfyUIApiClient
        client = LMStudioApiClient(url) if service == "lm" else ComfyUIApiClient(url)
        response = client.get_models(timeout=timeout) if service == "lm" else client.get_system_stats(timeout=timeout)
        return bool(response is not None and getattr(response, "status_code", 500) < 400)
    except Exception:
        return False
