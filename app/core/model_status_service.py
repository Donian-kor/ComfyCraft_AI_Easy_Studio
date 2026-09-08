"""Service layer for model presence and selection."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ModelStatus:
    lm_models: List[str] = field(default_factory=list)
    comfy_models: List[str] = field(default_factory=list)


class ModelStatusService:
    """GUI에서 사용하는 모델 상태 조회 및 선택 로직을 분리한다."""

    def __init__(self, model_fetcher):
        self.model_fetcher = model_fetcher

    @staticmethod
    def _normalize_models(models: Optional[List[str]], fallback: str) -> List[str]:
        if models:
            return list(models)
        return [fallback]

    def fetch(self, url_lm: str, url_comfy: str) -> ModelStatus:
        lm_models = self._normalize_models(self.model_fetcher.get_lmstudio_models(url_lm), "로드된 모델 없음")
        comfy_models = self._normalize_models(self.model_fetcher.get_comfyui_models(url_comfy), "로드된 모델 없음")
        return ModelStatus(lm_models=lm_models, comfy_models=comfy_models)

    @staticmethod
    def choose_model(current_value: str, options: List[str]) -> str:
        if not options:
            return ""
        if current_value in options:
            return current_value
        return options[0]
