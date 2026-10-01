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


def _probe_endpoint(url: str, endpoint: str, timeout: tuple[float, float] = (0.2, 0.3), max_retries: int = 1) -> bool:
    """프로브 엔드포인트 체크 (응답이 오면 연결된 것으로 본다)

    회귀 근거: 예전에는 HEAD 로 확인했다. ComfyUI 의 /system_stats 는
    HEAD 를 처리하지 않아 405(Method Not Allowed) 를 돌려주고, 그걸
    '연결 실패'로 오판했다(GET 재시도는 타임아웃/연결 거부일 때만
    돌아갔고, 405 응답일 때는 시도조차 하지 않았다). 서버가 켜져 있어도
    표시등이 빨강으로 나오는 원인.

    원본 Qt 도 get_system_stats()(GET) 로 판정했다. 여기서도 GET 으로
    확인하고, 상태 코드가 400 미만이면 연결된 것으로 본다.
    """
    normalized = _normalize_url(url)
    if not normalized:
        return False
    try:
        response = requests.get(f"{normalized}{endpoint}", timeout=timeout)
        return response.status_code < 400
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

    # 연결에 실패한 것이지 'URL 이 없다' 것이 아닐 수 있다.
    # 호출부가 resolve_live_url() 결과를 보고 'URL 이 비었다' 고 말하면
    # 사용자는 설정 화면을 아무리 찾아도 원인을 알 수 없다.
    if normalized:
        raise ConnectionProbeError(normalized, endpoint)
    return ""


class ConnectionProbeError(RuntimeError):
    """주소에는 응답이 있었지만 연결 판정을 통과하지 못했을 때.

    호출부는 이 예외를 받아 '연결 안 됨' 으로 표시한다. 주소가 비어
    있는 경우('')와 구분되게 하려고 따로 뺀다.
    """

    def __init__(self, url: str, endpoint: str) -> None:
        super().__init__(f"{url}{endpoint} 에서 응답을 받지 못했습니다")
        self.url = url
        self.endpoint = endpoint


def check_connection_status(service: str, url: str, candidates: Optional[Iterable[str]] = None) -> ConnectionStatus:
    """원격 서비스 연결을 실제로 응답해 확인한다."""
    label = "LM Studio" if "lm" in (service or "").lower() else "ComfyUI"
    try:
        resolved_url = resolve_live_url(service, url, candidates)
    except ConnectionProbeError:
        # 주소는 있는데 응답이 없었다. 'URL 이 없다' 고 말하면 오도이다.
        return ConnectionStatus(service=service, url=url, ok=False,
                                message=f"{label} 연결 안 됨 (응답 없음)")
    status = ConnectionStatus(service=service, url=resolved_url, ok=False,
                              message="미확인")
    if not resolved_url:
        status.message = "서버 주소가 비어 있습니다."
        return status

    endpoint = "/v1/models" if "lm" in (service or "").lower() else "/system_stats"
    status.ok = _probe_endpoint(resolved_url, endpoint)
    status.message = (f"{label} 연결됨" if status.ok
                      else f"{label} 연결 안 됨")
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
    excluded_tokens = ("vae", "clip", "text_encoder", "text_encoders",
                       "tokenizer", "embeddings", "encoder", "t5", "umt5",
                       "clip-vit", "sigclip", "-vit-",
                       "llama", "mistral", "gemma",
                       "upscaler", "controlnet", "control_", "lora")
    # qwen은 예외: Qwen-Image 같은 이미지 모델과
    # Qwen-VL/Instruct 같은 언어 모델을 함께 가리키므로 별도 판별한다.
    qwen_llm_tokens = ("vl", "instruct", "chat", "llm")
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
            if "qwen" in lower_name and any(
                    token in lower_name for token in qwen_llm_tokens):
                continue
            if name and name not in seen:
                seen.add(name)
                names.append(name)

    return names


def check_connection_silent(service: str, url: str, timeout: float = 0.3) -> bool:
    """조용하게 연결 확인 (자동 초기화용) - 매우 빠른 응답.

    재시도 0회: 이 함수의 존재 이유가 "즉시"라서다. 기본 재시도+백오프가
    붙으면 서버가 꺼져 있을 때 4초를 붙잡아 자동 초기화 전체가 느려진다.
    """
    try:
        from app.core.api_client import LMStudioApiClient, ComfyUIApiClient
        client = (LMStudioApiClient(url, max_retries=0) if service == "lm"
                  else ComfyUIApiClient(url, max_retries=0))
        response = client.get_models(timeout=timeout) if service == "lm" else client.get_system_stats(timeout=timeout)
        return bool(response is not None and getattr(response, "status_code", 500) < 400)
    except Exception:
        return False
