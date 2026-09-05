"""
Workflow Manager for ComfyUI + LMStudio Integration GUI
워크플로우 템플릿 로드, 렌더링, 검증을 담당하는 클래스
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

# src 패키지 내부에서 모듈을 참조하기 위해 현재 디렉토리 추가
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config_manager import get_config_manager, ConfigManager, AppConfig


@dataclass
class WorkflowTemplate:
    """워크플로우 템플릿 메타데이터"""
    name: str
    path: Path
    raw_template: Dict[str, Any]
    placeholders: List[str]


class WorkflowManager:
    """워크플로우 템플릿 관리 클래스"""
    
    def __init__(self, config_manager: Optional[ConfigManager] = None):
        self.config_manager = config_manager or get_config_manager()
        self.config: AppConfig = self.config_manager.get()
        self._templates: Dict[str, WorkflowTemplate] = {}
        self._load_templates()
    
    def _load_templates(self) -> None:
        """설정된 템플릿 파일들 로드"""
        base_dir = Path(__file__).resolve().parent.parent

        # 체크포인트 템플릿
        checkpoint_path = base_dir / self.config.workflow.checkpoint_template
        if checkpoint_path.exists():
            self._templates["checkpoint"] = self._load_template("checkpoint", checkpoint_path)

        # GGUF/UNET 템플릿
        gguf_path = base_dir / self.config.workflow.gguf_template
        if gguf_path.exists():
            self._templates["gguf"] = self._load_template("gguf", gguf_path)

        # Flux GGUF 템플릿
        flux_gguf_path = base_dir / self.config.workflow.flux_gguf_template
        if flux_gguf_path.exists():
            self._templates["flux_gguf"] = self._load_template("flux_gguf", flux_gguf_path)

        # ZImage 템플릿
        zimage_path = base_dir / self.config.workflow.zimage_template
        if zimage_path.exists():
            self._templates["zimage"] = self._load_template("zimage", zimage_path)
    
    def _load_template(self, name: str, path: Path) -> WorkflowTemplate:
        """템플릿 파일 로드 및 플레이스홀더 추출"""
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        
        # 플레이스홀더 추출 (__UPPER_CASE__ 패턴)
        placeholders = self._extract_placeholders(raw)
        
        return WorkflowTemplate(
            name=name,
            path=path,
            raw_template=raw,
            placeholders=placeholders
        )
    
    def _extract_placeholders(self, obj: Any, prefix: str = "") -> List[str]:
        """JSON 객체에서 __PLACEHOLDER__ 패턴 추출"""
        placeholders = []
        
        if isinstance(obj, dict):
            for value in obj.values():
                placeholders.extend(self._extract_placeholders(value, prefix))
        elif isinstance(obj, list):
            for item in obj:
                placeholders.extend(self._extract_placeholders(item, prefix))
        elif isinstance(obj, str) and obj.startswith("__") and obj.endswith("__"):
            placeholders.append(obj)
        
        return list(dict.fromkeys(placeholders))  # 중복 제거, 순서 유지
    
    def get_template(self, template_type: str) -> Optional[WorkflowTemplate]:
        """템플릿 조회"""
        return self._templates.get(template_type)
    
    def render_checkpoint_workflow(
        self,
        model_name: str,
        positive_prompt: str,
        negative_prompt: str,
        width: int,
        height: int,
        seed: int,
        steps: int,
        cfg: float,
        sampler_name: Optional[str] = None,
        scheduler: Optional[str] = None,
        denoise: Optional[float] = None,
        filename_prefix: Optional[str] = None
    ) -> Dict[str, Any]:
        """체크포인트 워크플로우 렌더링"""
        template = self.get_template("checkpoint")
        if not template:
            raise ValueError("Checkpoint workflow template not found")
        
        prefix = filename_prefix or self.config.output.filename_prefix
        
        replacements = {
            "__MODEL_NAME__": model_name,
            "__POSITIVE_PROMPT__": positive_prompt,
            "__NEGATIVE_PROMPT__": negative_prompt,
            "__WIDTH__": width,
            "__HEIGHT__": height,
            "__SEED__": seed,
            "__STEPS__": steps,
            "__CFG__": cfg,
            "__SAMPLER_NAME__": sampler_name or self.config.workflow.sampler_name,
            "__SCHEDULER__": scheduler or self.config.workflow.scheduler,
            "__DENOISE__": self.config.workflow.denoise if denoise is None else denoise,
            "__FILENAME_PREFIX__": prefix,
        }
        
        return self._render_template(template.raw_template, replacements)
    
    def render_gguf_workflow(
        self,
        model_name: str,
        positive_prompt: str,
        negative_prompt: str,
        width: int,
        height: int,
        seed: int,
        steps: int,
        cfg: float,
        unet_class: str,
        weight_dtype: str,
        clip_class: str,
        clip_name: str,
        clip_type: str,
        vae_name: str,
        sampler_name: Optional[str] = None,
        scheduler: Optional[str] = None,
        denoise: Optional[float] = None,
        filename_prefix: Optional[str] = None
    ) -> Dict[str, Any]:
        """GGUF/UNET 워크플로우 렌더링"""
        template = self.get_template("gguf")
        if not template:
            raise ValueError("GGUF workflow template not found")
        
        prefix = filename_prefix or self.config.output.filename_prefix
        
        replacements = {
            "__MODEL_NAME__": model_name,
            "__POSITIVE_PROMPT__": positive_prompt,
            "__NEGATIVE_PROMPT__": negative_prompt,
            "__WIDTH__": width,
            "__HEIGHT__": height,
            "__SEED__": seed,
            "__STEPS__": steps,
            "__CFG__": cfg,
            "__SAMPLER_NAME__": sampler_name or self.config.workflow.sampler_name,
            "__SCHEDULER__": scheduler or self.config.workflow.scheduler,
            "__DENOISE__": self.config.workflow.denoise if denoise is None else denoise,
            "__UNET_CLASS__": unet_class,
            "__WEIGHT_DTYPE__": weight_dtype,
            "__CLIP_CLASS__": clip_class,
            "__CLIP_NAME__": clip_name,
            "__CLIP_TYPE__": clip_type,
            "__VAE_NAME__": vae_name,
            "__FILENAME_PREFIX__": prefix,
        }
        
        return self._render_template(template.raw_template, replacements)
    
    def render_flux_gguf_workflow(
        self,
        model_name: str,
        positive_prompt: str,
        negative_prompt: str,
        width: int,
        height: int,
        seed: int,
        steps: int,
        guidance: float,
        clip_name1: str,
        clip_name2: str,
        clip_type: str,
        vae_name: str,
        sampler_name: Optional[str] = None,
        scheduler: Optional[str] = None,
        denoise: Optional[float] = None,
        filename_prefix: Optional[str] = None
    ) -> Dict[str, Any]:
        """Flux GGUF 워크플로우 렌더링 (DualCLIPLoaderGGUF + FluxGuidance)"""
        template = self.get_template("flux_gguf")
        if not template:
            raise ValueError("Flux GGUF workflow template not found")

        prefix = filename_prefix or self.config.output.filename_prefix

        replacements = {
            "__MODEL_NAME__": model_name,
            "__POSITIVE_PROMPT__": positive_prompt,
            "__NEGATIVE_PROMPT__": negative_prompt,
            "__WIDTH__": width,
            "__HEIGHT__": height,
            "__SEED__": seed,
            "__STEPS__": steps,
            "__GUIDANCE__": guidance,
            "__SAMPLER_NAME__": sampler_name or self.config.workflow.sampler_name,
            "__SCHEDULER__": scheduler or self.config.workflow.scheduler,
            "__DENOISE__": self.config.workflow.denoise if denoise is None else denoise,
            "__CLIP_NAME1__": clip_name1,
            "__CLIP_NAME2__": clip_name2,
            "__CLIP_TYPE__": clip_type,
            "__VAE_NAME__": vae_name,
            "__FILENAME_PREFIX__": prefix,
        }

        return self._render_template(template.raw_template, replacements)

    def render_zimage_workflow(
        self,
        model_name: str,
        positive_prompt: str,
        negative_prompt: str,
        width: int,
        height: int,
        seed: int,
        steps: int,
        cfg: float,
        clip_name: str,
        vae_name: str,
        sampler_name: Optional[str] = None,
        scheduler: Optional[str] = None,
        denoise: Optional[float] = None,
        filename_prefix: Optional[str] = None
    ) -> Dict[str, Any]:
        """ZImage 전용 워크플로우 렌더링"""
        template = self.get_template("zimage")
        if not template:
            raise ValueError("ZImage workflow template not found")

        prefix = filename_prefix or self.config.output.filename_prefix

        replacements = {
            "__MODEL_NAME__": model_name,
            "__POSITIVE_PROMPT__": positive_prompt,
            "__NEGATIVE_PROMPT__": negative_prompt,
            "__WIDTH__": width,
            "__HEIGHT__": height,
            "__SEED__": seed,
            "__STEPS__": steps,
            "__CFG__": cfg,
            "__SAMPLER_NAME__": sampler_name or self.config.workflow.sampler_name,
            "__SCHEDULER__": scheduler or self.config.workflow.scheduler,
            "__DENOISE__": self.config.workflow.denoise if denoise is None else denoise,
            "__CLIP_NAME__": clip_name,
            "__VAE_NAME__": vae_name,
            "__FILENAME_PREFIX__": prefix,
        }

        return self._render_template(template.raw_template, replacements)

    def _render_template(self, template: Dict[str, Any], replacements: Dict[str, Any]) -> Dict[str, Any]:
        """템플릿에 값 치환하여 최종 워크플로우 생성"""
        def replace_value(value: Any) -> Any:
            if isinstance(value, str):
                return replacements.get(value, value)
            elif isinstance(value, dict):
                return {k: replace_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [replace_value(item) for item in value]
            return value
        
        return replace_value(template)
    
    def is_gguf_model(self, model_name: str) -> bool:
        """모델명이 GGUF/UNET 모델인지 판별"""
        if not model_name:
            return False
        name_lower = model_name.lower()
        return name_lower.endswith(".gguf") or "unet" in name_lower
    
    def is_flux_model(self, model_name: str) -> bool:
        """모델명이 Flux 계열인지 판별"""
        if not model_name:
            return False
        return "flux" in model_name.lower()

    def is_zimage_model(self, model_name: str) -> bool:
        """모델명이 ZImage/Turbo 계열인지 판별"""
        if not model_name:
            return False
        lowered = model_name.lower()
        return "zimage" in lowered or "turbo" in lowered

    def get_model_preset(self, model_name: str):
        """설정에서 모델 프리셋 조회"""
        return self.config_manager.get().model_presets.get(model_name)
    
    def get_available_templates(self) -> List[str]:
        """사용 가능한 템플릿 타입 목록"""
        return list(self._templates.keys())


# 전역 인스턴스
_workflow_manager: Optional[WorkflowManager] = None


def get_workflow_manager(config_manager: Optional[ConfigManager] = None) -> WorkflowManager:
    """WorkflowManager 싱글톤 인스턴스 반환"""
    global _workflow_manager

    if config_manager is not None:
        if _workflow_manager is None or _workflow_manager.config_manager is not config_manager:
            _workflow_manager = WorkflowManager(config_manager)
        return _workflow_manager

    if _workflow_manager is None:
        _workflow_manager = WorkflowManager(config_manager)
    return _workflow_manager


def reset_workflow_manager():
    """WorkflowManager 인스턴스 리셋 (테스트용)"""
    global _workflow_manager
    _workflow_manager = None