"""Application 계층: 내부 이미지 생성 전송 계층 (Diffusers 기반).

ComfyTransport 를 대체하여 로컬에서 직접 이미지를 생성한다.
"""

from __future__ import annotations

import os
import time
import torch
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple

from diffusers import (
    StableDiffusionXLPipeline,
    StableDiffusionPipeline,
    DiffusionPipeline,
    DPMSolverMultistepScheduler,
    EulerAncestralDiscreteScheduler,
    EulerDiscreteScheduler,
    DDIMScheduler,
)
from transformers import CLIPTextModel, CLIPTokenizer
from safetensors.torch import load_file

from app.models.generation import GenerationRequest, GenerationResult, GenerationProgress
from app.core.model_registry import ModelRegistry
from app.core.model_profiles.base import ModelProfile

ProgressFn = Callable[[GenerationProgress], None]
LogFn = Callable[[str], None]


class InternalTransport:
    """내부 이미지 생성을 담당하는 전송 계층."""

    def __init__(self, output_dir: Path, *, log: Optional[LogFn] = None):
        self._output_dir = output_dir
        self._log = log or (lambda _m: None)
        self._device = "cuda" if torch.cuda.is_available() else "cpu"
        self._torch_dtype = torch.float16 if self._device == "cuda" else torch.float32
        self._loaded_models: Dict[str, Any] = {}  # 캐시된 모델들
        self._log(f"내부 생성 엔진 초기화 완료 (device: {self._device}, dtype: {self._torch_dtype})")

    def _log_msg(self, message: str) -> None:
        """로그 메시지 출력"""
        self._log(message)

    def prepare_queue(self, model_name: str, last_model: Optional[str]) -> Optional[str]:
        """모델 로딩 준비 (캐시 관리)"""
        # 내부 엔진에서는 모델 캐시를 관리하지만,
        # ComfyUI와 동일한 인터페이스를 유지하기 위해 모델명만 반환
        self._log_msg(f"모델 준비 요청: {model_name}")
        return model_name

    def clear_queue(self) -> None:
        """캐시 정리"""
        self._log_msg("내부 엔진 캐시 정리")
        # 실제로는 메모리 관리가 필요할 수 있음
        # torch.cuda.empty_cache() 등

    def interrupt(self) -> None:
        """생성 중단 (현재는 지원하지 않음)"""
        self._log_msg["내부 엔진에서는 인터럽트를 지원하지 않습니다."]

    def node_exists(self, node_name: str) -> bool:
        """내부 엔진에서는 특정 노드 개념이 없으므로 항상 True 반환"""
        # 내부 엔진에서는 ComfyUI 노드 개념이 없으므로
        # 모든 노드가 존재한다고 간주
        return True

    def find_sam_model_name(self, preferred: str = "sam_vit_b_01ec64.pth") -> Optional[str]:
        """SAM 모델 찾기 (내부 엔진에서는 지원하지 않음)"""
        self._log_msg["내부 엔진에서는 SAM 모델을 지원하지 않습니다."]
        return None

    def download_first_image(self, history_item: Dict[str, Any]) -> Optional[Path]:
        """이미지 다운로드 (내부 엔진에서는 불필요)"""
        # 내부 엔진에서는 이미지가 바로 생성되므로 이 메서드는 사용되지 않음
        return None

    def wait_for_result(self, prompt_id: str, *, interval: float, max_wait: int,
                        should_stop: Callable[[], bool],
                        on_progress: Optional[ProgressFn] = None) -> Optional[Path]:
        """결과 기다리기 (내부 엔진에서는 직접 생성)"""
        # 내부 엔진에서는 prompt_id 개념이 없으므로
        # 실제 생성 로직을 여기서 구현해야 함
        # 하지만 이 메서드는 ComfyTransport 인터페이스를 유지하기 위해 존재
        # 실제 생성은 generate_image 메서드에서 처리
        self._log_msg["내부 엔진에서는 wait_for_result를 직접 호출하지 않습니다."]
        return None

    def generate_image(self, request: GenerationRequest, 
                      on_progress: Optional[ProgressFn] = None,
                      log: Optional[LogFn] = None) -> GenerationResult:
        """내부 엔진을 사용하여 이미지 생성"""
        start_time = time.time()
        log_fn = log or self._log
        
        try:
            # 진행 상태 초기화
            self._progress_update(on_progress, log_fn, "generating", 0, "모델 로딩 중...")
            
            # 모델 로드 또는 캐시에서 가져오기
            pipeline = self._load_pipeline(request.comfy_model)
            
            # 프롬프트 처리 (LMStudio 향상 건너뛰고 원본 사용)
            prompt = request.prompt
            negative_prompt = request.negative_prompt
            
            # 시드 처리
            seed = request.seed if request.seed >= 0 else torch.randint(0, 2**32 - 1, (1,)).item()
            
            # 진행 상태 업데이트
            self._progress_update(on_progress, log_fn, "generating", 10, "이미지 생성 시작...")
            
            # 이미지 생성
            generator = torch.Generator(device=self._device).manual_seed(seed)
            
            # Stable Diffusion XL 또는 일반 Stable Diffusion 파이프라인 선택
            if "sdxl" in request.comfy_model.lower() or "sd-xl" in request.comfy_model.lower():
                result = pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    width=request.width,
                    height=request.height,
                    num_inference_steps=request.steps,
                    guidance_scale=request.cfg,
                    generator=generator,
                    output_type="pil",
                )
            else:
                result = pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    width=request.width,
                    height=request.height,
                    num_inference_steps=request.steps,
                    guidance_scale=request.cfg,
                    generator=generator,
                    output_type="pil",
                )
            
            image = result.images[0]
            
            # 진행 상태 업데이트
            self._progress_update(on_progress, log_fn, "generating", 90, "이미지 저장 중...")
            
            # 이미지 저장
            output_dir = self._output_dir
            output_dir.mkdir(parents=True, exist_ok=True)
            
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{request.filename_prefix or 'ComfyUI'}_{timestamp}.png"
            image_path = output_dir / filename
            
            image.save(image_path)
            
            # 완료 상태
            self._progress_update(on_progress, log_fn, "done", 100, "생성 완료")
            
            elapsed_time = time.time() - start_time
            
            return GenerationResult(
                status="done",
                image_path=str(image_path),
                prompt=prompt,
                meta=f"{request.width}x{request.height}",
                elapsed=elapsed_time,
                model=request.comfy_model,
                width=request.width,
                height=request.height,
                seed=seed,
                enhanced_prompt=prompt,
                snapshot=request.to_dict(),
                logs=[f"내부 생성 완료: {elapsed_time:.2f}초"],
            )
            
        except Exception as exc:
            self._log_msg(f"[ERROR] 내부 생성 실패: {exc}")
            import traceback
            self._log_msg(traceback.format_exc())
            
            return GenerationResult(
                status="failed",
                prompt=request.prompt,
                model=request.comfy_model,
                width=request.width,
                height=request.height,
                seed=request.seed if request.seed >= 0 else 0,
                snapshot=request.to_dict(),
                logs=[f"내부 생성 오류: {str(exc)}"],
                error=str(exc),
                elapsed=time.time() - start_time,
            )

    def _load_pipeline(self, model_name: str) -> Any:
        """모델 로드 또는 캐시에서 가져오기"""
        if model_name in self._loaded_models:
            self._log_msg(f"캐시에서 모델 로드: {model_name}")
            return self._loaded_models[model_name]
        
        self._log_msg(f"새 모델 로드 시작: {model_name}")
        
        # 모델 파일 경로 찾기
        model_path = self._find_model_path(model_name)
        if not model_path:
            raise FileNotFoundError(f"모델을 찾을 수 없습니다: {model_name}")
        
        # 모델 유형에 따라 적절한 파이프라인 선택
        if self._is_flux_model(model_name):
            pipeline = self._load_flux_pipeline(model_path, model_name)
        elif self._is_sdxl_model(model_name):
            pipeline = self._load_sdxl_pipeline(model_path, model_name)
        elif self._is_zimage_model(model_name):
            pipeline = self._load_zimage_pipeline(model_path, model_name)
        else:
            # 기본 Stable Diffusion 파이프라인
            pipeline = self._load_standard_pipeline(model_path, model_name)
        
        # 모델을 캐시에 저장
        self._loaded_models[model_name] = pipeline
        self._log_msg(f"모델 로드 완료 및 캐시 저장: {model_name}")
        
        return pipeline

    def _find_model_path(self, model_name: str) -> Optional[Path]:
        """모델 파일 경로 찾기"""
        # 설정에서 모델 경로 목록 가져오기
        from app.core.config_manager import get_config_manager
        config_manager = get_config_manager()
        base_paths = config_manager.get_model_base_paths()
        
        # 각 경로에서 모델 파일 찾기
        for base_path in base_paths:
            if not base_path.exists():
                continue
                
            # 정확한 파일명 찾기
            model_path = base_path / model_name
            if model_path.exists():
                return model_path
            
            # 확장자별로 찾기
            for ext in [".safetensors", ".ckpt", ".pt", ".bin", ".gguf"]:
                model_path = base_path / f"{model_name}{ext}"
                if model_path.exists():
                    return model_path
        
        return None

    def _is_flux_model(self, model_name: str) -> bool:
        """Flux 모델인지 확인"""
        lower_name = model_name.lower()
        return "flux" in lower_name

    def _is_sdxl_model(self, model_name: str) -> bool:
        """SDXL 모델인지 확인"""
        lower_name = model_name.lower()
        return "sdxl" in lower_name or "sd-xl" in lower_name

    def _is_zimage_model(self, model_name: str) -> bool:
        """ZImage 모델인지 확인"""
        lower_name = model_name.lower()
        return "zimage" in lower_name or "z_image" in lower_name

    def _load_flux_pipeline(self, model_path: Path, model_name: str) -> Any:
        """Flux 파이프라인 로드"""
        self._log_msg(f"Flux 파이프라인 로드 중: {model_path}")
        # Flux 모델은 현재 diffusers에서 완전히 지원되지 않을 수 있음
        # 대안으로 Stable Diffusion XL 사용하거나 커스텀 구현 필요
        try:
            # Flux 모델을 위한 시도 (향후 구현 예정)
            pipeline = DiffusionPipeline.from_pretrained(
                str(model_path),
                torch_dtype=self._torch_dtype,
                variant="fp16" if self._device == "cuda" else None,
            )
            pipeline.to(self._device)
            return pipeline
        except Exception as e:
            self._log_msg(f"[WARNING] Flux 모델 로드 실패, SDXL로 대체: {e}")
            return self._load_sdxl_pipeline(model_path, model_name)

    def _load_sdxl_pipeline(self, model_path: Path, model_name: str) -> Any:
        """SDXL 파이프라인 로드"""
        self._log_msg(f"SDXL 파이프라인 로드 중: {model_path}")
        try:
            pipeline = StableDiffusionXLPipeline.from_pretrained(
                str(model_path),
                torch_dtype=self._torch_dtype,
                variant="fp16" if self._device == "cuda" else None,
            )
            pipeline.to(self._device)
            
            # 스케줄러 옵션 설정 (요청에 따라)
            pipeline.scheduler = EulerDiscreteScheduler.from_config(pipeline.scheduler.config)
            
            return pipeline
        except Exception as e:
            self._log_msg(f"[ERROR] SDXL 파이프라인 로드 실패: {e}")
            raise

    def _load_zimage_pipeline(self, model_path: Path, model_name: str) -> Any:
        """ZImage 파이프라인 로드"""
        self._log_msg(f"ZImage 파이프라인 로드 중: {model_path}")
        # ZImage 모델도 현재 표준 라이브러리에서 지원되지 않을 수 있음
        # 대안으로 일반 Stable Diffusion 사용
        try:
            pipeline = StableDiffusionPipeline.from_pretrained(
                str(model_path),
                torch_dtype=self._torch_dtype,
                safety_checker=None,  # 안전 검사기 비활성화 (선택사항)
            )
            pipeline.to(self._device)
            
            # ZImage에 적합한 스케줄러 설정
            pipeline.scheduler = DPMSolverMultistepScheduler.from_config(pipeline.scheduler.config)
            
            return pipeline
        except Exception as e:
            self._log_msg(f"[ERROR] ZImage 파이프라인 로드 실패: {e}")
            raise

    def _load_standard_pipeline(self, model_path: Path, model_name: str) -> Any:
        """일반 Stable Diffusion 파이프라인 로드"""
        self._log_msg(f"Standard 파이프라인 로드 중: {model_path}")
        try:
            pipeline = StableDiffusionPipeline.from_pretrained(
                str(model_path),
                torch_dtype=self._torch_dtype,
                safety_checker=None,
            )
            pipeline.to(self._device)
            
            # 기본 스케줄러 설정
            pipeline.scheduler = EulerAncestralDiscreteScheduler.from_config(pipeline.scheduler.config)
            
            return pipeline
        except Exception as e:
            self._log_msg(f"[ERROR] Standard 파이프라인 로드 실패: {e}")
            raise

    def _progress_update(self, on_progress: Optional[ProgressFn], 
                        log_fn: LogFn,
                        status: str,
                        progress: int,
                        message: str) -> None:
        """진행 상태 업데이트"""
        if on_progress is not None:
            on_progress(GenerationProgress(
                status=status,
                progress=max(0, min(int(progress), 100)),
                message=message,
                log="",
                preview="",
                enhanced_prompt="",
                elapsed_seconds=0.0,
            ))
        log_fn(f"[{status}] {message} ({progress}%)")