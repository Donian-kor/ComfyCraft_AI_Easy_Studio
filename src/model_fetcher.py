"""
Model Fetcher for ComfyUI + LMStudio Integration GUI
LM Studio 및 ComfyUI 모델 목록 조회 로직을 통합 관리하는 클래스
"""

import threading
import time
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List, Optional, Tuple

import requests

# src 패키지 내부에서 모듈을 참조하기 위해 현재 디렉토리 추가
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config_manager import ConfigManager, get_config_manager


@dataclass
class CacheEntry:
    """캐시 엔트리"""
    timestamp: float
    data: Any


class ModelFetcher:
    """모델 목록 조회 및 캐싱을 담당하는 클래스"""
    
    def __init__(self, config_manager: Optional[ConfigManager] = None):
        self.config_manager = config_manager or get_config_manager()
        self.config = self.config_manager.get()
        self._cache: Dict[str, CacheEntry] = {}
        self._cache_lock = Lock()
        self._cache_ttl = self.config.cache.model_cache_ttl_seconds
    
    @staticmethod
    def _normalize_url_for_cache(url: str) -> str:
        """캐시 키용 URL 정규화 (실제 요청과 동일하게)
        
        LM Studio의 경우 127.0.0.1을 localhost로 변환하여
        캐시 키가 실제 요청 URL과 일치하도록 함.
        """
        normalized = (url or "").rstrip("/")
        # LM Studio 요청 시 127.0.0.1 -> localhost 변환과 동일하게 처리
        return normalized.replace("127.0.0.1", "localhost")
    
    def _get_cache_key(self, prefix: str, url: str) -> str:
        """캐시 키 생성 (정규화된 URL 사용)"""
        normalized_url = self._normalize_url_for_cache(url)
        return f"{prefix}:{normalized_url}"
    
    def _get_cached(self, cache_key: str) -> Optional[Any]:
        """캐시에서 데이터 조회 (TTL 확인)"""
        with self._cache_lock:
            entry = self._cache.get(cache_key)
            if entry and (time.monotonic() - entry.timestamp) < self._cache_ttl:
                return entry.data
            if entry:
                del self._cache[cache_key]
            return None
    
    def _set_cache(self, cache_key: str, data: Any) -> None:
        """캐시에 데이터 저장"""
        with self._cache_lock:
            self._cache[cache_key] = CacheEntry(timestamp=time.monotonic(), data=data)
    
    def invalidate_cache(self, prefix: str, url: str) -> None:
        """특정 URL의 캐시 무효화"""
        cache_key = self._get_cache_key(prefix, url)
        with self._cache_lock:
            self._cache.pop(cache_key, None)
    
    def invalidate_all(self) -> None:
        """전체 캐시 무효화"""
        with self._cache_lock:
            self._cache.clear()
    
    # ==================== LM Studio 모델 조회 ====================
    
    def get_lmstudio_models(self, url: Optional[str] = None) -> List[str]:
        """LM Studio에서 로드된 모델 목록 조회 (캐시 지원)"""
        url = url or self.config.lmstudio.url
        cache_key = self._get_cache_key("lm", url)
        
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
        
        models = self._fetch_lmstudio_models(url)
        self._set_cache(cache_key, models)
        return models
    
    def _fetch_lmstudio_models(self, url: str) -> List[str]:
        """LM Studio API에서 모델 목록 직접 조회 (초고속)"""
        try:
            # 극단적으로 짧은 타임아웃
            response = requests.get(
                url.rstrip('/') + "/v1/models",
                timeout=(0.2, 0.3)
            )
            response.raise_for_status()
            data = response.json().get("data", [])
            models = [item.get("id") for item in data if item.get("id")]
            return models
        except Exception:
            return []
    
    def get_preferred_lmstudio_models(self, selected_model: str = "", url: Optional[str] = None) -> List[str]:
        """선택된 모델을 우선순위로 둔 모델 목록 반환"""
        available = self.get_lmstudio_models(url)
        preferred = []
        seen = set()
        
        # 사용자가 선택한 모델이 있으면 최우선
        if selected_model and selected_model not in ("없음", "로드된 모델 없음", ""):
            preferred.append(selected_model)
            seen.add(selected_model)
        
        # 나머지 사용 가능한 모델 추가
        for model in available:
            if model and model not in seen:
                preferred.append(model)
                seen.add(model)
        
        return preferred if preferred else ["로드된 모델 없음"]
    
    # ==================== ComfyUI 모델 조회 ====================
    
    def get_comfyui_models(self, url: Optional[str] = None) -> List[str]:
        """ComfyUI에서 사용 가능한 모델 목록 조회 (캐시 지원)"""
        url = url or self.config.comfyui.url
        cache_key = self._get_cache_key("comfy", url)
        
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
        
        models = self._fetch_comfyui_models(url)
        self._set_cache(cache_key, models)
        return models
    
    @staticmethod
    def _is_clip_model_name(name: str) -> bool:
        if not isinstance(name, str):
            return False
        lowered = name.lower()
        return (
            name.startswith("clip/")
            or name.startswith("text_encoders/")
            or any(keyword in lowered for keyword in ("gemma", "qwen", "llama", "clip"))
        )

    @staticmethod
    def _unique_names(values: List[str]) -> List[str]:
        seen = set()
        result = []
        for value in values:
            if value and value not in seen:
                seen.add(value)
                result.append(value)
        return result

    @staticmethod
    def _looks_like_model_name(value: str) -> bool:
        if not isinstance(value, str):
            return False
        cleaned = value.strip()
        if not cleaned:
            return False
        lower = cleaned.lower()
        if lower in {"pixel_space", "none", "default"}:
            return False
        return (
            any(lower.endswith(ext) for ext in (".safetensors", ".ckpt", ".pt", ".bin", ".gguf", ".sft"))
            or "/" in cleaned
            or "\\" in cleaned
        )

    @classmethod
    def _flatten_model_candidates(cls, value: Any) -> List[str]:
        flattened: List[str] = []
        if isinstance(value, str):
            flattened.append(value)
        elif isinstance(value, (list, tuple)):
            for item in value:
                flattened.extend(cls._flatten_model_candidates(item))
        elif isinstance(value, dict):
            for child in value.values():
                flattened.extend(cls._flatten_model_candidates(child))
        return flattened

    def _collect_model_names_from_object_info(self, node_data: Dict[str, Any], key_names: Tuple[str, ...]) -> List[str]:
        result = []
        for key_name in key_names:
            values = node_data.get(key_name, [])
            for candidate in self._flatten_model_candidates(values):
                if not self._looks_like_model_name(candidate):
                    continue
                if self._is_clip_model_name(candidate):
                    continue
                if candidate not in result:
                    result.append(candidate)
        return result

    def _fetch_comfyui_models(self, url: str) -> List[str]:
        """ComfyUI에서 모델 목록 조회 (초고속 API 조회 + 필요시 로컬 스캔, 재시도 로직 포함)"""
        models = []
        base_url = url.rstrip('/')

        is_online = False
        
        # 초고속 온라인 상태 확인
        try:
            r = requests.get(f"{base_url}/system_stats", timeout=(0.15, 0.25))
            if r.status_code == 200:
                is_online = True
        except Exception:
            return []

        if not is_online:
            return []

        for node_name in ("CheckpointLoaderSimple", "UnetLoaderGGUF", "UNETLoader"):
            try:
                resp = requests.get(f"{base_url}/object_info/{node_name}", timeout=(0.2, 0.3))
                if resp.status_code == 200:
                    node_data = resp.json().get(node_name, {}).get("input", {}).get("required", {})
                    models.extend(self._collect_model_names_from_object_info(node_data, ("ckpt_name", "unet_name")))
                    if models:  # 모델을 찾으면 바로 반환
                        return models
            except Exception:
                pass

        if not models:
            try:
                response = requests.get(f"{base_url}/object_info", timeout=(0.3, 0.5))
                if response.status_code == 200:
                    obj = response.json()
                    for node_name in ("CheckpointLoaderSimple", "UnetLoaderGGUF", "UNETLoader"):
                        if node_name in obj:
                            node_data = obj[node_name].get("input", {}).get("required", {})
                            models.extend(self._collect_model_names_from_object_info(node_data, ("ckpt_name", "unet_name")))
            except Exception:
                pass

        if not models:
            supported_exts = {'.safetensors', '.ckpt', '.pt', '.bin', '.gguf', '.sft'}
            excluded_tokens = ("vae", "clip", "text_encoder", "text_encoders", "tokenizer", "embeddings")
            for base in self.config_manager.get_model_base_paths():
                for subfolder in ("checkpoints", "diffusion_models", "unet"):
                    dir_path = base / subfolder
                    if dir_path.exists():
                        for p in dir_path.glob("**/*.*"):
                            if not p.is_file() or p.suffix.lower() not in supported_exts:
                                continue
                            lower_name = p.name.lower()
                            if any(token in lower_name for token in excluded_tokens):
                                continue
                            if not self._is_clip_model_name(p.name) and p.name not in models:
                                models.append(p.name)

        models = self._unique_names(models)
        return models if models else ["없음"]
    
    def get_comfyui_vaes(self, url: Optional[str] = None) -> List[str]:
        """ComfyUI에서 사용 가능한 VAE 목록 조회"""
        url = url or self.config.comfyui.url
        cache_key = self._get_cache_key("vae", url)
        
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
        
        vaes = self._fetch_comfyui_vaes(url)
        self._set_cache(cache_key, vaes)
        return vaes
    
    def _fetch_comfyui_vaes(self, url: str) -> List[str]:
        """VAE 목록 조회 (경량 API + 필요시 로컬 스캔)"""
        vaes = []
        base_url = url.rstrip('/')

        try:
            response = requests.get(f"{base_url}/object_info/VAELoader", timeout=(0.5, 1.0))
            if response.status_code == 200:
                info = response.json().get("VAELoader", {}).get("input", {}).get("required", {}).get("vae_name", [])
                if info and isinstance(info[0], list):
                    vaes = [v for v in info[0] if v != "pixel_space"]
        except Exception:
            pass

        if not vaes:
            for base in self.config_manager.get_model_base_paths():
                vae_dir = base / "vae"
                if vae_dir.exists():
                    for f in vae_dir.glob("**/*.*"):
                        if f.is_file() and f.suffix.lower() in ('.safetensors', '.pt', '.ckpt', '.bin'):
                            if f.name not in vaes:
                                vaes.append(f.name)

        return self._unique_names(vaes)
    
    def get_comfyui_clips(self, url: Optional[str] = None) -> List[str]:
        """ComfyUI에서 사용 가능한 CLIP/텍스트 인코더 목록 조회"""
        url = url or self.config.comfyui.url
        cache_key = self._get_cache_key("clip", url)
        
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
        
        clips = self._fetch_comfyui_clips(url)
        self._set_cache(cache_key, clips)
        return clips
    
    def _fetch_comfyui_clips(self, url: str) -> List[str]:
        """CLIP 목록 조회 (경량 API + 필요시 로컬 스캔)"""
        clips = []
        base_url = url.rstrip('/')

        for node_name in ("CLIPLoader", "CLIPLoaderGGUF", "DualCLIPLoader", "DualCLIPLoaderGGUF"):
            try:
                response = requests.get(f"{base_url}/object_info/{node_name}", timeout=(0.5, 1.0))
                if response.status_code == 200:
                    required = response.json().get(node_name, {}).get("input", {}).get("required", {})
                    for key in ("clip_name", "clip_name1", "clip_name2"):
                        values = required.get(key, [])
                        if not values:
                            continue
                        for candidate in self._flatten_model_candidates(values):
                            if not self._looks_like_model_name(candidate):
                                continue
                            if candidate not in clips:
                                clips.append(candidate)
            except Exception:
                pass

        if not clips:
            for base in self.config_manager.get_model_base_paths():
                for folder in ("text_encoders", "clip"):
                    dir_path = base / folder
                    if dir_path.exists():
                        for f in dir_path.glob("**/*.*"):
                            if f.is_file() and f.suffix.lower() in ('.safetensors', '.pt', '.ckpt', '.bin', '.gguf'):
                                if f.name not in clips:
                                    clips.append(f.name)

        clips = self._unique_names(clips)

        def _rank(name: str) -> int:
            n = name.lower()
            if "clip_g" in n or "clip_l" in n or "flux" in n:
                return 0
            if "qwen3" in n or "qwen" in n:
                return 1
            if "gemma" in n:
                return 2
            if "t5" in n or "clip" in n or "sdxl" in n:
                return 3
            return 5

        clips.sort(key=_rank)
        return clips
    
    def get_clip_types(self, url: Optional[str] = None) -> List[str]:
        """ComfyUI에서 지원하는 CLIP type 목록 조회"""
        url = url or self.config.comfyui.url
        cache_key = self._get_cache_key("clip_types", url)
        
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
        
        types = self._fetch_clip_types(url)
        self._set_cache(cache_key, types)
        return types
    
    def _fetch_clip_types(self, url: str) -> List[str]:
        """CLIP 타입 목록 조회"""
        try:
            response = requests.get(
                url.rstrip('/') + "/object_info",
                timeout=(0.5, 1.5)
            )
            if response.status_code == 200:
                obj = response.json()
                types_info = obj.get("CLIPLoader", {}).get("input", {}).get("required", {}).get("type", [[]])
                if types_info and isinstance(types_info[0], list):
                    return types_info[0]
        except Exception:
            pass
        return ["stable_diffusion"]
    
    def has_comfy_node(self, node_type: str, url: Optional[str] = None) -> bool:
        """ComfyUI 서버에 특정 노드 타입이 존재하는지 확인"""
        url = url or self.config.comfyui.url
        cache_key = self._get_cache_key(f"node:{node_type}", url)
        
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
        
        result = self._check_comfy_node(node_type, url)
        self._set_cache(cache_key, result)
        return result
    
    def _check_comfy_node(self, node_type: str, url: str) -> bool:
        """노드 존재 여부 직접 확인"""
        try:
            response = requests.get(
                f"{url.rstrip('/')}/object_info/{node_type}",
                timeout=(0.5, 1.0)
            )
            if response.status_code == 200:
                return node_type in response.json()
        except Exception:
            pass
        return False
    
    def check_server_status(self, lm_url: Optional[str] = None, comfy_url: Optional[str] = None) -> Tuple[bool, bool]:
        """LM Studio와 ComfyUI 서버 상태 병렬 확인"""
        target_lm = lm_url or self.config.lmstudio.url
        target_comfy = comfy_url or self.config.comfyui.url
        
        lm_ok = False
        comfy_ok = False
        
        def _check_lm():
            nonlocal lm_ok
            try:
                r = requests.get(target_lm.rstrip('/') + "/v1/models", timeout=(0.4, 0.8))
                lm_ok = (r.status_code == 200)
            except Exception:
                lm_ok = False
                
        def _check_comfy():
            nonlocal comfy_ok
            try:
                r = requests.get(target_comfy.rstrip('/') + "/system_stats", timeout=(0.4, 0.8))
                comfy_ok = (r.status_code == 200)
            except Exception:
                comfy_ok = False
                
        t1 = threading.Thread(target=_check_lm)
        t2 = threading.Thread(target=_check_comfy)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        
        return lm_ok, comfy_ok


# 전역 인스턴스
_model_fetcher: Optional[ModelFetcher] = None


def get_model_fetcher(config_manager: Optional[ConfigManager] = None) -> ModelFetcher:
    """ModelFetcher 싱글톤 인스턴스 반환"""
    global _model_fetcher
    if _model_fetcher is None:
        _model_fetcher = ModelFetcher(config_manager)
    return _model_fetcher


def reset_model_fetcher():
    """ModelFetcher 인스턴스 리셋 (테스트용)"""
    global _model_fetcher
    _model_fetcher = None