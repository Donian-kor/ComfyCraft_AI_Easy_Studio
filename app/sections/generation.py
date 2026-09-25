"""Generation settings, worker, and runtime snapshot management."""

from __future__ import annotations
import json
import random
import time
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from PySide6.QtCore import QObject, QThread, Signal

from app.core.api_client import ComfyUIApiClient, ComfyUIWebSocketClient
from app.core.model_registry import get_model_registry
from app.core.workflow_manager import get_workflow_manager
from app.sections.prompt import (
    SAMPLER_NAMES,
    SCHEDULER_NAMES,
    enhance_prompt_sync,
    load_external_prompts,
)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class GenerationSettings:
    width: int = 1024
    height: int = 1024
    steps: int = 20
    cfg: float = 7.0
    seed: int = -1
    sampler: str = "euler"
    scheduler: str = "normal"
    denoise: float = 1.0


def build_generation_snapshot(raw: dict) -> GenerationSettings:
    """Normalize UI input values into a generation settings object."""
    return GenerationSettings(
        width=int(raw.get("width", 1024)),
        height=int(raw.get("height", 1024)),
        steps=int(raw.get("steps", 20)),
        cfg=float(raw.get("cfg", 7.0)),
        seed=int(raw.get("seed", -1)),
        sampler=str(raw.get("sampler", "euler")),
        scheduler=str(raw.get("scheduler", "normal")),
        denoise=float(raw.get("denoise", 1.0)),
    )


# ---------------------------------------------------------------------------
# Worker signals
# ---------------------------------------------------------------------------

class WorkerSignals(QObject):
    progress = Signal(int)
    status = Signal(str)
    log = Signal(str)
    image = Signal(str)
    error = Signal(str)
    finished = Signal(bool)
    enhanced_prompt = Signal(str)


# ---------------------------------------------------------------------------
# Generation worker
# ---------------------------------------------------------------------------

class GenerationWorker:
    """이미지 생성 워커 - ComfyUI 워크플로우 실행 및 결과 다운로드 담당"""

    def __init__(self, controller, snapshot: Dict[str, Any]):
        self.controller = controller
        self.config = controller.config
        self.snapshot = snapshot
        self.signals = WorkerSignals()
        self.stop_requested = False
        self._last_model_name = None
        self.comfy_api: Optional[ComfyUIApiClient] = None
        self.comfy_ws: Optional[ComfyUIWebSocketClient] = None

    def stop(self):
        self.stop_requested = True
        try:
            if self.comfy_api:
                self.comfy_api.interrupt(timeout=2)
                self.comfy_api.clear_queue(timeout=2)
        except Exception:
            pass
        try:
            if self.comfy_ws:
                self.comfy_ws.close()
        except Exception:
            pass

    def run(self):
        try:
            success = self.generate()
        except Exception as exc:
            self.signals.error.emit(str(exc))
            success = False
        finally:
            # 🌟 생성 종료 시(성공/실패/중단 모두) ComfyUI 큐 정리 및 웹소켓 종료
            try:
                if self.comfy_api:
                    self.comfy_api.clear_queue(timeout=2)
                    self.emit_log("ComfyUI 큐 정리 완료")
            except Exception as e:
                self.emit_log(f"[⚠️ 경고] 큐 정리 실패: {e}")
            try:
                if self.comfy_ws:
                    self.comfy_ws.close()
            except Exception:
                pass
            self.signals.finished.emit(success)

    def generate(self) -> bool:
        snapshot = self.snapshot
        self.signals.status.emit("ComfyUI 연결 확인 중...")
        self.comfy_api = ComfyUIApiClient(snapshot["comfy_url"])
        response = self.comfy_api.get_system_stats(timeout=3)
        response.raise_for_status()

        model_name = snapshot["comfy_model"]
        if not model_name or model_name in ("없음", "로드된 모델 없음"):
            raise RuntimeError("ComfyUI 모델을 선택해주세요.")

        profile = self.controller.model_registry.detect(model_name)
        seed = snapshot["seed"] if snapshot["seed"] >= 0 else random.randint(1, 2**31 - 1)
        
        # 1️⃣ UI 스냅샷으로부터 원본 프롬프트 가져오기
        prompt = snapshot["prompt"]

        # 2️⃣ enhancePromptEdit에 이미 텍스트가 있는지 확인 (스냅샷에서 가져옴)
        pre_existing_ui_text = snapshot.get("enhance_prompt", "").strip()

        # ★ 스타일 변경 감지: 스냅샷에 저장된 스타일과 현재 스타일이 다르면
        #    이전 스타일의 프롬프트를 무시하고 다시 향상합니다.
        saved_style = snapshot.get("zanime_style", "").strip().lower()
        current_style = (self.config.prompts.zanime_style or "").strip().lower()
        style_changed = (saved_style != "" and saved_style != current_style)

        # 3️⃣ LM Studio 프롬프트 향상 단계
        # enhancePromptEdit에 텍스트가 있고 스타일이 동일하면 향상을 건너뜀
        if pre_existing_ui_text and not style_changed:
            self.emit_log("enhancePromptEdit에 이미 텍스트가 있어 프롬프트 향상을 건너뜁니다.")
            prompt = pre_existing_ui_text
        elif self.controller.is_lm_connected():
            if style_changed:
                self.emit_log(f"[ZANIME 스타일 변경] '{saved_style}' → '{current_style}' : 프롬프트 향상을 새로 수행합니다.")
            else:
                self.emit_log("LM Studio를 통해 프롬프트 향상 중...")
            enhanced = self.enhance_prompt(prompt)
            if enhanced:
                prompt = enhanced
                self.emit_log("LM Studio 프롬프트 강화 완료.")

                # 🚀 main.py에 연결된 이벤트를 통해 GUI 창(enhancePromptEdit)에 텍스트 주입
                self.signals.enhanced_prompt.emit(prompt)

                # GUI에 텍스트가 반영될 수 있도록 잠시 대기
                time.sleep(0.2)
            else:
                self.emit_log("LM Studio 응답이 올바르지 않아 원본 프롬프트를 사용합니다.")
        else:
            self.emit_log("LM Studio 미연결로 프롬프트 강화 생략 (원본 사용)")

        # 4️⃣ 🎯 [핵심 수정] ComfyUI로 전송할 최종 텍스트는
        # 반드시 화면의 'enhancePromptEdit' 창에 입력된 최신 본문을 직접 가져옵니다.
        final_positive_prompt = prompt
        if hasattr(self.controller, "ui") and hasattr(self.controller.ui, "enhancePromptEdit"):
            ui_text = self.controller.ui.enhancePromptEdit.toPlainText().strip()
            if ui_text:
                final_positive_prompt = ui_text
                self.emit_log("enhancePromptEdit 창의 최종 편집본을 ComfyUI 워크플로우에 적용합니다.")

        negative = snapshot["negative"] or self.controller.config.prompts.negative_default
        
        # 4️⃣ 최종 확정된 프롬프트로 워크플로우 조립
        workflow = self.build_workflow(profile, model_name, final_positive_prompt, negative, seed)
        self._validate_workflow(workflow)

        if self.stop_requested:
            return False

        # 🌟 [중요] 새 생성 시작 전 ComfyUI 큐/실행 상태 강제 정리 (재실행 400 에러 방지)
        # 🌟 [개선] 모델이 변경된 경우에만 free_memory 호출 (같은 모델이면 메모리 유지)
        try:
            self.comfy_api.interrupt(timeout=2)
            self.comfy_api.clear_queue(timeout=2)
            if self._last_model_name is None or self._last_model_name != model_name:
                self.comfy_api.free_memory(timeout=3)
                self._last_model_name = model_name
                self.emit_log("사전 큐 정리 완료 (interrupt + clear_queue + free_memory)")
            else:
                self.emit_log(f"동일 모델({model_name}) 유지 — free_memory 건너뜀")
        except Exception as e:
            self.emit_log(f"[⚠️ 경고] 사전 큐 정리 중 오류 (무시하고 진행): {e}")

        # 🌟 정리 후 잠시 대기하여 ComfyUI가 내부 상태를 정리할 시간 확보
        time.sleep(0.5)

        # (이후 ComfyUI 큐 등록 및 웹소켓 통신 코드는 기존과 동일)
        workflow_json_str = json.dumps(workflow, indent=2, ensure_ascii=False)
        self.emit_log(f"[DEBUG] 워크플로우 JSON (전체):\n{workflow_json_str}")

        self.signals.status.emit("워크플로우 큐 등록 중...")
        try:
            response = self.comfy_api.prompt(workflow, timeout=self.controller.config.comfyui.timeout_seconds)
            response.raise_for_status()
        except Exception as e:
            error_detail = ""
            try:
                if hasattr(response, 'text') and response.text:
                    error_detail = f" / 응답: {response.text[:1000]}"
                if hasattr(response, 'status_code'):
                    error_detail = f" / 상태코드: {response.status_code}{error_detail}"
            except:
                pass
            self.emit_log(f"[ERROR] ComfyUI 프롬프트 등록 실패: {str(e)}{error_detail}")
            # 🌟 실패 시 워크플로우 JSON도 함께 로그로 남김 (디버깅용)
            self.emit_log(f"[DEBUG] 실패한 워크플로우:\n{workflow_json_str}")
            raise

        prompt_id = response.json().get("prompt_id")
        if not prompt_id:
            raise RuntimeError("ComfyUI에서 prompt_id를 받지 못했습니다.")
        self.emit_log(f"워크플로우 큐 등록 완료: {prompt_id}")

# 아래와 같이 깔끔하게 감싸서 실행하도록 변경합니다.
        try:
            self.comfy_ws = ComfyUIWebSocketClient(
                snapshot["comfy_url"],
                on_progress=lambda value: self.signals.progress.emit(int(value)),
                on_status=lambda value: self.signals.log.emit(str(value)),
            )
            # [Source 3번 파일 - 기존 위치]
            self.comfy_ws.set_prompt_id(prompt_id)
            # 👇 [👍 추가] 웹소켓 내부 상태나 수신 이벤트를 내 프로그램 로그창으로 직접 바이패스합니다.
            self.comfy_ws.on_status = lambda status_dict: self.emit_log(f"[소켓 상태] {status_dict}")
            
            self.comfy_ws.start()

            # 🌟 WebSocket URL 디버그 로그
            self.emit_log(f"[WebSocket] 연결 시도: {self.comfy_ws.ws_url}")
            
            self.emit_log("ComfyUI WebSocket 연결 프로세스 시작")
            
            # 👇 [👍 수정 및 교체] 웹소켓이 '진짜' 연결될 때까지 최대 2초간 안전하게 대기합니다.
            connected_wait = 0
            while not getattr(self.comfy_ws, "_connected", False) and connected_wait < 20:
                time.sleep(0.1)
                connected_wait += 1
                
            if getattr(self.comfy_ws, "_connected", False):
                self.emit_log("ComfyUI WebSocket 연결 완벽 성공!")
            else:
                self.emit_log("[⚠️ 경고] WebSocket 연결 수립 지연 - HTTP 폴링으로 진행률 추적을 대체합니다.")
            
        except Exception as exc:
            self.emit_log(f"WebSocket 초기화 실패: {exc}")
            self.comfy_ws = None


        self.signals.status.emit("이미지 생성 중...")

        interval = max(self.controller.config.comfyui.poll_interval_seconds, 0.2)
        max_wait = self.controller.config.comfyui.max_wait_seconds
        attempts = int(max_wait / interval)
        
        # 모델 로딩 단계 추적용
        model_loading_logged = False
        last_progress = 0
        
        for attempt in range(attempts):
            if self.stop_requested:
                return False
            
            history = self.comfy_api.history(prompt_id, timeout=5)
            if history.status_code == 200:
                item = history.json().get(prompt_id)
                if item:
                    comfy_error = self._extract_comfyui_error(item)
                    if comfy_error:
                        raise RuntimeError(f"ComfyUI 작업 실패: {comfy_error}")
                    result_path = self.download_first_image(item)
                    if result_path:
                        self.signals.progress.emit(100)
                        self.signals.image.emit(str(result_path))
                        self.emit_log(f"이미지 다운로드 완료: {result_path}")
                        # 🌟 생성 완료 후 ComfyUI 큐 정리 (재실행 시 400 에러 방지)
                        try:
                            self.comfy_api.clear_queue(timeout=2)
                            self.emit_log("ComfyUI 큐 정리 완료")
                        except Exception as e:
                            self.emit_log(f"[⚠️ 경고] 큐 정리 실패: {e}")
                        return True
            
            # 🌟 WebSocket에서 실제 진행률이 오면 last_progress 업데이트됨
            # (ComfyUIWebSocketClient에서 on_progress 콜백으로 progress 시그널 발생 시 자동 반영)
            current_progress = getattr(self.comfy_ws, "_last_progress", 0) if self.comfy_ws else 0
            if current_progress > last_progress:
                last_progress = current_progress
                model_loading_logged = False  # 실제 진행 시작되면 로깅 리셋
            
            # 🌟 모델 로딩 단계(진행률 0% 유지 시) 시각적 피드백 + 로그
            if last_progress == 0 and not model_loading_logged:
                elapsed = attempt * interval
                if elapsed >= 30:  # 30초 후부터 로그 출력
                    self.emit_log(f"[모델 로딩 중] 대용량 모델 초기화 대기... ({elapsed:.0f}초 경과, 최대 {max_wait}초 대기)")
                    model_loading_logged = True
            
            time.sleep(interval)

        raise RuntimeError(f"이미지 생성 시간이 초과되었습니다. (최대 {max_wait}초 대기)")

    @staticmethod
    def _extract_comfyui_error(item: Dict[str, Any]) -> Optional[str]:
        if not isinstance(item, dict):
            return None

        direct_error = item.get("error")
        if direct_error:
            return str(direct_error)

        status = item.get("status", {})
        if isinstance(status, dict):
            error = status.get("error")
            if error:
                return str(error)
            messages = status.get("messages")
            if isinstance(messages, list):
                for msg in messages:
                    if isinstance(msg, dict):
                        candidate = msg.get("error") or msg.get("message")
                        if candidate:
                            return str(candidate)
                    elif isinstance(msg, str) and msg:
                        return msg

        for node_output in item.get("outputs", {}).values():
            if not isinstance(node_output, dict):
                continue
            status = node_output.get("status", {})
            if isinstance(status, dict):
                error = status.get("error")
                if error:
                    return str(error)
                messages = status.get("messages")
                if isinstance(messages, list):
                    for msg in messages:
                        if isinstance(msg, dict):
                            candidate = msg.get("error") or msg.get("message")
                            if candidate:
                                return str(candidate)
                        elif isinstance(msg, str) and msg:
                            return msg

        return None

    def _require_comfy_api(self) -> ComfyUIApiClient:
        """comfy_api가 None이 아님을 보장하고 반환합니다."""
        if self.comfy_api is None:
            raise RuntimeError("ComfyUI API 클라이언트가 초기화되지 않았습니다.")
        return self.comfy_api

    def _comfyui_node_exists(self, node_name: str, base_url: str) -> bool:
        try:
            api = self._require_comfy_api()
            response = api.get_object_info(
                node_name,
                timeout=(0.5, 1.0)
            )
            if response.status_code != 200:
                return False
            payload = response.json()
            return isinstance(payload, dict) and node_name in payload
        except Exception:
            return False

    def _find_sam_model_name(self, comfy_url: str, preferred: str = "sam_vit_b_01ec64.pth") -> Optional[str]:
        """SAMLoader가 사용할 SAM 모델 파일명을 서버에서 조회합니다.

        - 서버에 SAMLoader 노드가 없으면 None 반환 (SAM 미연결 상태로 동작)
        - 사용자가 설치한 sam_vit_b_01ec64.pth가 우선이고, 없으면 서버에 존재하는 첫 SAM 파일을 사용
        """
        try:
            api = self._require_comfy_api()
            response = api.get_object_info(
                "SAMLoader",
                timeout=(0.5, 1.0),
            )
            if response.status_code != 200:
                return None
            payload = response.json().get("SAMLoader", {})
            required = (
                payload.get("input", {}).get("required", {})
                if isinstance(payload, dict)
                else {}
            )
            model_name_spec = required.get("model_name")
            if not (isinstance(model_name_spec, list) and model_name_spec and isinstance(model_name_spec[0], list)):
                return None
            candidates = [str(name) for name in model_name_spec[0] if name]
            if not candidates:
                return None
            if preferred in candidates:
                return preferred
            return candidates[0]
        except Exception:
            return None

    def _validate_workflow(self, workflow: Dict[str, Any]):
        if not isinstance(workflow, dict) or not workflow:
            raise RuntimeError("생성 워크플로우가 비어 있습니다.")

        issues = []
        missing_nodes = []
        comfy_url = self.snapshot.get("comfy_url", "")
        
        for node_id, node in workflow.items():
            if not isinstance(node, dict):
                continue
            class_type = node.get("class_type")
            inputs = node.get("inputs")
            if not isinstance(inputs, dict):
                continue

            if class_type == "KSampler":
                for field_name in ("model", "positive", "negative", "latent_image"):
                    value = inputs.get(field_name)
                    if isinstance(value, dict):
                        issues.append(f"노드 {node_id}의 {field_name} 값이 dict 형태라 ComfyUI 연결이 아닙니다.")

            # 🌟 각 노드 타입이 ComfyUI에 존재하는지 확인
            if class_type and comfy_url:
                if not self._comfyui_node_exists(class_type, comfy_url):
                    missing_nodes.append(f"{class_type} (노드 ID: {node_id})")

        if missing_nodes:
            issues.append(f"ComfyUI에 없는 노드 타입: {', '.join(missing_nodes)}. 해당 커스텀 노드가 설치되어 있는지 확인하세요.")

        if issues:
            raise RuntimeError("ComfyUI 워크플로우 검증 실패: " + "; ".join(issues))

    def build_workflow(self, profile, model_name, prompt, negative, seed):
        s = self.snapshot
        manager = self.controller.workflow_manager
        prefix = self.controller.build_filename_prefix()
        comfy_url = s["comfy_url"]

        # 모델 종류별로 기본 워크플로우만 먼저 만든 뒤,
        # 마지막에 FaceDetailer를 공통으로 1번 주입한다.
        # (Checkpoint뿐 아니라 Flux/GGUF/ZImage에서도 얼굴 보정이 동작하도록)
        base_wf = None

        # ZImage/Turbo 모델 처리
        if manager.is_zimage_model(model_name) or profile.workflow_type == "zimage":
            required_nodes = ["UnetLoaderGGUF", "CLIPLoaderGGUF", "VAELoader", "KSampler", "TextEncodeZImageOmni"]
            missing = [name for name in required_nodes if not self._comfyui_node_exists(name, comfy_url)]
            if missing:
                if manager.is_gguf_model(model_name):
                    raise RuntimeError(
                        f"ZImage 전용 노드 누락: {', '.join(missing)}. "
                        f"ComfyUI 서버에 해당 커스텀 노드를 설치해주세요."
                    )
                self.emit_log(f"ZImage 전용 노드 누락: {', '.join(missing)}. 기본 checkpoint 경로로 대체합니다.")
                base_wf = manager.render_checkpoint_workflow(
                    model_name=model_name,
                    positive_prompt=prompt,
                    negative_prompt=negative,
                    width=s["width"],
                    height=s["height"],
                    seed=seed,
                    steps=s["steps"],
                    cfg=s["cfg"],
                    filename_prefix=prefix
                )
            else:
                clips = self.controller.model_fetcher.get_comfyui_clips(comfy_url)
                vaes = self.controller.model_fetcher.get_comfyui_vaes(comfy_url)
                if not clips:
                    raise RuntimeError("ComfyUI CLIP 모델을 찾을 수 없습니다.")
                base_wf = manager.render_zimage_workflow(
                    model_name=model_name,
                    positive_prompt=prompt,
                    negative_prompt=negative,
                    width=s["width"],
                    height=s["height"],
                    seed=seed,
                    steps=s["steps"],
                    cfg=s["cfg"],
                    clip_name=profile.select_clip(clips),
                    vae_name=profile.select_vae(vaes),
                    sampler_name=s["sampler"],
                    scheduler=s["scheduler"],
                    denoise=s["denoise"],
                    filename_prefix=prefix
                )

        # Flux 모델 처리
        if base_wf is None and (profile.workflow_type == "flux_gguf" or manager.is_flux_model(model_name) or profile.family == "flux"):
            required_nodes = ["UnetLoaderGGUF", "DualCLIPLoaderGGUF", "FluxGuidance", "VAELoader"]
            missing = [name for name in required_nodes if not self._comfyui_node_exists(name, comfy_url)]
            if missing:
                if manager.is_gguf_model(model_name):
                    raise RuntimeError(
                        f"Flux 전용 노드 누락: {', '.join(missing)}. "
                        f"ComfyUI 서버에 해당 커스텀 노드를 설치해주세요."
                    )
                self.emit_log(f"Flux 전용 노드 누락: {', '.join(missing)}. 기본 checkpoint 경로로 대체합니다.")
                base_wf = manager.render_checkpoint_workflow(
                    model_name=model_name,
                    positive_prompt=prompt,
                    negative_prompt=negative,
                    width=s["width"],
                    height=s["height"],
                    seed=seed,
                    steps=s["steps"],
                    cfg=s["cfg"],
                    filename_prefix=prefix
                )
            else:
                clips = self.controller.model_fetcher.get_comfyui_clips(comfy_url)
                vaes = self.controller.model_fetcher.get_comfyui_vaes(comfy_url)
                if len(clips) < 2:
                    raise RuntimeError("Flux 모델은 2개의 CLIP 모델이 필요합니다. ComfyUI에 Flux용 CLIP 2개를 로드해 주세요.")
                clip1, clip2 = profile.select_clip_pair(clips)
                base_wf = manager.render_flux_gguf_workflow(
                    model_name=model_name,
                    positive_prompt=prompt,
                    negative_prompt=negative,
                    width=s["width"],
                    height=s["height"],
                    seed=seed,
                    steps=s["steps"],
                    guidance=max(1.0, s["cfg"]),
                    clip_name1=clip1,
                    clip_name2=clip2,
                    clip_type="flux",
                    vae_name=profile.select_vae(vaes),
                    sampler_name=s["sampler"],
                    scheduler=s["scheduler"],
                    denoise=s["denoise"],
                    filename_prefix=prefix
                )

        # GGUF/UNET 모델 처리
        if base_wf is None and manager.is_gguf_model(model_name):
            clips = self.controller.model_fetcher.get_comfyui_clips(comfy_url)
            vaes = self.controller.model_fetcher.get_comfyui_vaes(comfy_url)
            if not clips:
                raise RuntimeError("ComfyUI CLIP 모델을 찾을 수 없습니다.")
            base_wf = manager.render_gguf_workflow(
                model_name=model_name,
                positive_prompt=prompt,
                negative_prompt=negative,
                width=s["width"],
                height=s["height"],
                seed=seed,
                steps=s["steps"],
                cfg=s["cfg"],
                unet_class="UnetLoaderGGUF",
                weight_dtype="default",
                clip_class="CLIPLoaderGGUF" if clips[0].lower().endswith(".gguf") else "CLIPLoader",
                clip_name=clips[0],
                clip_type="stable_diffusion",
                vae_name=profile.select_vae(vaes),
                sampler_name=s["sampler"],
                scheduler=s["scheduler"],
                denoise=s["denoise"],
                filename_prefix=prefix
            )

        # Checkpoint 모델 처리 (위에서 처리되지 않은 나머지 전부)
        if base_wf is None:
            base_wf = manager.render_checkpoint_workflow(
                model_name=model_name,
                positive_prompt=prompt,
                negative_prompt=negative,
                width=s["width"],
                height=s["height"],
                seed=seed,
                steps=s["steps"],
                cfg=s["cfg"],
                sampler_name=s["sampler"],
                scheduler=s["scheduler"],
                denoise=s["denoise"],
                filename_prefix=prefix
            )
        
        # FaceDetailer 주입 (스냅샷에서 활성화 여부 확인)
        if s.get("facedetailer_enabled", False):
            base_wf = self._inject_facedetailer(base_wf, comfy_url, seed, s, prefix)
        
        return base_wf

    def _inject_facedetailer(self, workflow: Dict[str, Any], comfy_url: str, seed: int, s: Dict[str, Any], prefix: str) -> Dict[str, Any]:
        """
        기본 워크플로우에 FaceDetailer 노드를 주입하여 얼굴 보정 기능을 추가합니다.
        ComfyUI Impact Pack의 FaceDetailer 노드가 필요합니다.
        UI에서 설정한 파라미터를 사용합니다.
        """
        if not self._comfyui_node_exists("FaceDetailer", comfy_url):
            self.emit_log("[⚠️ 알림] ComfyUI 서버에 'Impact Pack(FaceDetailer)'이 설치되어 있지 않습니다. 기본 생성으로 진행합니다.")
            return workflow
        if not self._comfyui_node_exists("UltralyticsDetectorProvider", comfy_url):
            self.emit_log("[⚠️ 알림] ComfyUI 서버에 'UltralyticsDetectorProvider(Impact Pack)'가 없습니다. 기본 생성으로 진행합니다.")
            return workflow
        
        try:
            ksampler_node_id = None
            vae_decode_node_id = None
            save_image_node_ids = []
            
            for node_id, node in workflow.items():
                class_type = node.get("class_type", "")
                if class_type == "KSampler":
                    ksampler_node_id = node_id
                elif class_type == "VAEDecode":
                    vae_decode_node_id = node_id
                elif class_type == "SaveImage":
                    save_image_node_ids.append(node_id)
            
            if not ksampler_node_id or not vae_decode_node_id:
                self.emit_log("[⚠️ 경고] KSampler 또는 VAE Decode 노드를 찾을 수 없습니다. FaceDetailer 주입을 건너뜁니다.")
                return workflow
            
            # 🌟 [안정성 패치] KSampler 노드의 인풋 링크에서 오리지널 모델, CLIP 원본 소스를 역추적합니다.
            ksampler_inputs = workflow[ksampler_node_id].get("inputs", {})
            model_source = ksampler_inputs.get("model")       # 예: ["2", 0]
            positive_source = ksampler_inputs.get("positive") # CLIP 정보 파악용
            
            # VAE 소스는 VAE Decode 노드의 인풋 링크에서 역추적합니다.
            vae_decode_inputs = workflow[vae_decode_node_id].get("inputs", {})
            vae_source = vae_decode_inputs.get("vae")         # 예: ["4", 2]

            # 만약 KSampler 링크 역추적이 실패할 경우를 대비한 안전 장치 백업본 지정
            if not model_source: model_source = [ksampler_node_id, 0]
            if not vae_source: vae_source = [ksampler_node_id, 2]

            # 긍정 프롬프트(Conditioning) 링크에서 오리지널 CLIP 노드를 역추적 시도
            # (Checkpoint/CLIPTextEncode뿐 아니라 FluxGuidance -> CLIPTextEncode 체인도 따라감)
            clip_source = None
            def _clip_of(node_id):
                try:
                    n = workflow.get(str(node_id), {})
                    return n.get("inputs", {}).get("clip")
                except Exception:
                    return None
            if positive_source and isinstance(positive_source, list) and len(positive_source) > 0:
                pos_node_id = str(positive_source[0])
                pos_node = workflow.get(pos_node_id, {})
                pos_inputs = pos_node.get("inputs", {})
                clip_source = pos_inputs.get("clip")
                # FluxGuidance 등은 clip 대신 conditioning 링크를 가짐 -> 한 단계 더 추적
                if not clip_source and isinstance(pos_inputs.get("conditioning"), list):
                    try:
                        cond_src_id = str(pos_inputs["conditioning"][0])
                        clip_source = _clip_of(cond_src_id)
                    except Exception:
                        pass

            if not clip_source:
                # 어떤 인코더 노드든 clip 링크를 빌려옴 (모든 워크플로우 종류 호환)
                for node_id, node in workflow.items():
                    if node.get("class_type") in ("CLIPTextEncode", "TextEncodeZImageOmni"):
                        cand = node.get("inputs", {}).get("clip")
                        if isinstance(cand, list) and len(cand) > 0:
                            clip_source = cand
                            break
            if not clip_source:
                # 못 찾으면 로더 노드에서 정석 출력 인덱스로 백업 매핑
                # (CheckpointLoaderSimple clip=출력1, CLIP 계열 clip=출력0)
                for node_id, node in workflow.items():
                    ctype = node.get("class_type", "")
                    if ctype == "CheckpointLoaderSimple":
                        clip_source = [node_id, 1]
                        break
                    if ctype in ("CLIPLoader", "CLIPLoaderGGUF", "DualCLIPLoaderGGUF"):
                        clip_source = [node_id, 0]
                        break
                if not clip_source:
                    clip_source = [ksampler_node_id, 1]

            # 안면 인식 디텍터 노드 추가
            detector_node_id = str(max(int(k) for k in workflow.keys()) + 1)
            workflow[detector_node_id] = {
                "inputs": {
                    "model_name": "bbox/face_yolov8m.pt"
                },
                "class_type": "UltralyticsDetectorProvider"
            }

            # SAMLoader 노드 추가 (SAM 모델이 서버에 있으면 SAM 세그멘테이션 활성화)
            sam_loader_node_id = None
            sam_model_name = self._find_sam_model_name(comfy_url)
            if sam_model_name:
                sam_loader_node_id = str(int(detector_node_id) + 1)
                workflow[sam_loader_node_id] = {
                    "inputs": {
                        "model_name": sam_model_name,
                        "device_mode": "AUTO",
                    },
                    "class_type": "SAMLoader"
                }
                self.emit_log(
                    f"[AI 안면 보정] SAM 모델 연결 완료: {sam_model_name} "
                    "(SAM 세그멘테이션 기반 정밀 마스크 활성화)"
                )

            # UI 가변 값 취합 (스냅샷에서 가져오기, 기본값 제공)
            facedetailer_denoise = s.get("facedetailer_denoise", 0.4)
            facedetailer_steps = s.get("facedetailer_steps", 20)
            facedetailer_cfg = s.get("facedetailer_cfg", 4.0)
            facedetailer_guide_size = s.get("facedetailer_guide_size", 256)
            facedetailer_max_size = s.get("facedetailer_max_size", 512)
            facedetailer_feather = s.get("facedetailer_feather", 5)
            # 새로운 FaceDetailer 파라미터들
            facedetailer_bbox_threshold = s.get("facedetailer_bbox_threshold", 0.5)
            facedetailer_bbox_dilation = s.get("facedetailer_bbox_dilation", 10)
            facedetailer_bbox_crop_factor = s.get("facedetailer_bbox_crop_factor", 1.5)
            facedetailer_sam_detection_hint = s.get("facedetailer_sam_detection_hint", "center-1")
            # 구버전 UI 값(center-2/center-3/center-4/all)이 히스토리에 남아 있어도
            # 공식 FaceDetailer 옵션 9종이 아니면 기본값 center-1로 되돌림
            if facedetailer_sam_detection_hint not in (
                "center-1", "horizontal-2", "vertical-2", "rect-4",
                "diamond-4", "mask-area", "mask-points", "mask-point-bbox", "none",
            ):
                facedetailer_sam_detection_hint = "center-1"
            facedetailer_sam_dilation = s.get("facedetailer_sam_dilation", 0)
            facedetailer_sam_threshold = s.get("facedetailer_sam_threshold", 0.93)
            facedetailer_sam_bbox_expansion = s.get("facedetailer_sam_bbox_expansion", 0)
            facedetailer_sam_mask_hint_threshold = s.get("facedetailer_sam_mask_hint_threshold", 0.7)
            facedetailer_sam_mask_hint_use_negative = s.get("facedetailer_sam_mask_hint_use_negative", "False")
            facedetailer_cycle = s.get("facedetailer_cycle", 1)
            facedetailer_drop_size = s.get("facedetailer_drop_size", 10)
            
            self.emit_log(
                f"[AI 안면 정밀 보정] 파이프라인 가동 ── "
                f"Steps: {facedetailer_steps}, CFG: {facedetailer_cfg}, Denoise: {facedetailer_denoise}, "
                f"BBoxThresh: {facedetailer_bbox_threshold}, SAMHint: {facedetailer_sam_detection_hint}"
            )
            # SAM 모델이 없는 경우에만 안내 (SAMLoader 연결 시 해당 로그 생략)
            if not sam_loader_node_id:
                self.emit_log("[FaceDetailer] SAM 모델 미연결 상태에서는 YOLO BBox 기준으로 동작합니다 (SAM 세부 옵션은 부분 적용).")

            # FaceDetailer 핵심 노드 조립 및 결합
            # 🌟 ComfyUI Impact Pack FaceDetailer 노드는 많은 필수 입력이 필요합니다.
            # 에러 메시지에 나온 모든 필수 입력값을 기본값과 함께 제공합니다.
            facedetailer_node_id = str(int(detector_node_id) + (2 if sam_loader_node_id else 1))
            workflow[facedetailer_node_id] = {
                "inputs": {
                    "image": [vae_decode_node_id, 0],      # 원본 완성 이미지 소스 연결
                    "model": model_source,                 # 🌟 안전하게 역추적된 모델 오리지널 링크 연결!
                    "clip": clip_source,                   # 🌟 안전하게 역추적된 CLIP 오리지널 링크 연결!
                    "vae": vae_source,                     # 🌟 안전하게 역추적된 VAE 오리지널 링크 연결!
                    "guide_size": facedetailer_guide_size,
                    "guide_size_for": True,
                    "max_size": facedetailer_max_size,
                    "seed": seed,
                    "steps": facedetailer_steps,
                    "cfg": facedetailer_cfg,
                     # 안면 질감 묘사 전용 고성능 고화질 샘플러 고정
                    "sampler_name": "dpmpp_2m_sde",        
                    "scheduler": "karras",
                    "denoise": facedetailer_denoise,
                    "feather": facedetailer_feather,
                    "noise_mask": True,
                    "force_inpaint": True,
                    "bbox_detector": [detector_node_id, 0],
                    "sam_model_opt": [sam_loader_node_id, 0] if sam_loader_node_id else None,
                    # 🌟 아래는 ComfyUI Impact Pack FaceDetailer 필수 입력값들 (UI 설정값 사용)
                    "positive": [positive_source[0], 0] if positive_source and isinstance(positive_source, list) else clip_source,
                    "negative": [negative_source[0], 0] if (negative_source := ksampler_inputs.get("negative")) and isinstance(negative_source, list) else clip_source,
                    "bbox_threshold": facedetailer_bbox_threshold,
                    "bbox_dilation": facedetailer_bbox_dilation,
                    "bbox_crop_factor": facedetailer_bbox_crop_factor,
                    "sam_detection_hint": facedetailer_sam_detection_hint,
                    "sam_dilation": facedetailer_sam_dilation,
                    "sam_threshold": facedetailer_sam_threshold,
                    "sam_bbox_expansion": facedetailer_sam_bbox_expansion,
                    "sam_mask_hint_threshold": facedetailer_sam_mask_hint_threshold,
                    "sam_mask_hint_use_negative": facedetailer_sam_mask_hint_use_negative,
                    "wildcard": "",
                    "cycle": facedetailer_cycle,
                    "drop_size": facedetailer_drop_size,
                },
                "class_type": "FaceDetailer"
            }
            
            # 최종 저장 노드 우회 연동
            for save_node_id in save_image_node_ids:
                node = workflow.get(save_node_id)
                if node and node.get("class_type") == "SaveImage":
                    node["inputs"]["images"] = [facedetailer_node_id, 0]
                    self.emit_log(f"[AI 안면 보정] 저장 노드({save_node_id}번) 파이프라인 우회 연동 완료.")
            
            self.emit_log("[AI 안면 보정] FaceDetailer 워크플로우 조립 및 주입 프로세스가 성공적으로 완료되었습니다.")
            return workflow
            
        except Exception as e:
            self.emit_log(f"[⚠️ 시스템 에러] FaceDetailer 구조 조립 중 오류 발생: {e}. 안전을 위해 무보정 원본 생성으로 우회합니다.")
            return workflow


# 3번째 파일 () 내부의 enhance_prompt 함수 교체 코드

    # 3번째 파일 내부의 enhance_prompt 함수 최종 교체안

    def enhance_prompt(self, prompt: str) -> Optional[str]:
        s = self.snapshot
        model = s["lm_model"]
        comfy_model_name = s.get("comfy_model") # 🌟 현재 선택된 ComfyUI 모델 이름

        if not model or model == "로드된 모델 없음":
            self.emit_log("LM Studio 모델이 없어 원본 프롬프트를 사용합니다.")
            return None

        # 원본 소스 코드에 내장된 자동 아키텍처 판별 메커니즘 작동
        profile = self.controller.model_registry.detect(comfy_model_name)
        manager = self.controller.workflow_manager

        ext_prompts = load_external_prompts()
        use_korean = self.controller.config.prompts.use_korean_prompt

        # 🌟 [개선안] 기존 소스 코드의 워크플로우 분기법과 100% 동일하게 오차 없이 판별
        is_flux = bool(profile.workflow_type == "flux_gguf" or manager.is_flux_model(comfy_model_name) or profile.family == "flux")
        is_zimage = bool(manager.is_zimage_model(comfy_model_name) or profile.workflow_type == "zimage")
        is_ernie = bool(profile.family == "ernie")
        lowered_model_name = (comfy_model_name or "").lower()
        is_zanime = bool(
            "z-anime" in lowered_model_name
            or "zanime" in lowered_model_name
            or "z_anime_base" in lowered_model_name
            or "anime_aio" in lowered_model_name
            or profile.family == "zanime"
            or profile.name == "zanime_aio"
        )

        # zanime 모델일 때만: 저장된 스타일 설정을 따라 별도 시스템 프롬프트 사용
        # - webtoon: 한국 웹툰 스타일 (국가/인종은 랜덤으로 유지, 랜덤 반영)
        # - japanime: 일본 애니 스타일 (국가/인종은 랜덤으로 유지, 랜덤 반영)
        # - basic: 애니 기본 방향
        zanime_style = (self.config.prompts.zanime_style or "").strip().lower()
        if is_zanime and zanime_style in ("webtoon", "japanime", "basic"):
            style_suffix = "kr" if use_korean else "en"
            if zanime_style == "webtoon":
                system_prompt = (
                    ext_prompts.get(f"system_prompt_zanime_webtoon_{style_suffix}") or ""
                )
            elif zanime_style == "japanime":
                system_prompt = (
                    ext_prompts.get(f"system_prompt_zanime_anime_{style_suffix}") or ""
                )
            else:
                system_prompt = (
                    ext_prompts.get(f"system_prompt_zanime_basic_{style_suffix}") or ""
                )
            if not system_prompt:
                self.emit_log(
                    f"[ZANIME 스타일] '{zanime_style}' 전용 지시문이 없어 기본 문장형 지시문으로 대체합니다."
                )
                system_prompt = ext_prompts.get("system_prompt_flux_kr" if use_korean else "system_prompt_flux_en") or ""
            else:
                self.emit_log(
                    f"[ZANIME 스타일] '{zanime_style}' 스타일 프롬프트 지시문을 사용합니다."
                )
        elif is_ernie:
            self.emit_log(
                f"[AI 자동 분석] '{comfy_model_name}' 모델 감지: 'ERNIE 전용' 프롬프트 지시문을 사용합니다."
            )
            system_prompt = ext_prompts.get(
                "system_prompt_ernie_kr" if use_korean else "system_prompt_ernie_en"
            ) or ext_prompts.get("system_prompt_flux_kr" if use_korean else "system_prompt_flux_en") or ""
        elif is_flux or is_zimage or is_zanime:
            self.emit_log(f"[AI 자동 분석] '{comfy_model_name}' 모델 감지: '문장형' 프롬프트 지시문을 사용합니다.")
            system_prompt = ext_prompts.get("system_prompt_flux_kr" if use_korean else "system_prompt_flux_en") or ""
        
       # 2. 저거넛, 리얼비스를 포함한 나머지 모든 SDXL 계열일 때 ➡️ '태그형' 프롬프트 분기
        else:
            self.emit_log(f"[AI 자동 분석] '{comfy_model_name}' 모델 감지: '태그형(쉼표 구분)' 프롬프트 지시문을 사용합니다.")
            system_prompt = ext_prompts.get("system_prompt_sdxl_kr" if use_korean else "system_prompt_sdxl_en") or ""

        # 만약 json 매핑 문제로 해당 키가 안 읽히면 백업용 기본값 지정
        if not system_prompt:
            system_prompt = ext_prompts.get("system_prompt_sdxl_kr" if use_korean else "system_prompt_sdxl_en") or ""

        return enhance_prompt_sync(
            lm_url=s["lm_url"],
            model=model,
            prompt=prompt,
            system_prompt=system_prompt,
            timeout=self.controller.config.lmstudio.timeout_seconds
        )



    def download_first_image(self, history_item: Dict[str, Any]) -> Optional[Path]:
        api = self._require_comfy_api()
        for output in history_item.get("outputs", {}).values():
            images = output.get("images", [])
            if not images:
                continue
            image = images[0]
            response = api.view({
                "filename": image.get("filename", "output.png"),
                "subfolder": image.get("subfolder", ""),
                "type": image.get("type", "output"),
            }, timeout=30)
            response.raise_for_status()
            destination = self.controller.output_dir / Path(image.get("filename", "output.png")).name
            destination.write_bytes(response.content)
            return destination
        return None

    def emit_log(self, message: str):
        self.signals.log.emit(message)
