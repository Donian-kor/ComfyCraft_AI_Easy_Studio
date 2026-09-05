"""Generation settings, worker, and runtime snapshot management."""

from __future__ import annotations
import json
import random
import sys
import time
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QApplication  # 🚀 여기를 QtWidgets로 올바르게 지정합니다!

# Add project root to path for imports
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src import (
    ComfyUIApiClient,
    ComfyUIWebSocketClient,
    get_workflow_manager,
    get_model_registry,
)

# Import from 03_Prompt using importlib to handle numeric folder name
import importlib.util
_prompt_path = _PROJECT_ROOT / "03_Prompt" / "prompt.py"
_prompt_spec = importlib.util.spec_from_file_location("section_03_Prompt_prompt", _prompt_path)
_prompt_mod = importlib.util.module_from_spec(_prompt_spec)
assert _prompt_spec and _prompt_spec.loader
sys.modules["section_03_Prompt_prompt"] = _prompt_mod
_prompt_spec.loader.exec_module(_prompt_mod)

SAMPLER_NAMES = _prompt_mod.SAMPLER_NAMES
SCHEDULER_NAMES = _prompt_mod.SCHEDULER_NAMES
enhance_prompt_sync = _prompt_mod.enhance_prompt_sync
load_external_prompts = _prompt_mod.load_external_prompts


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
        self.snapshot = snapshot
        self.signals = WorkerSignals()
        self.stop_requested = False
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

        # 3️⃣ LM Studio 프롬프트 향상 단계
        # enhancePromptEdit에 텍스트가 이미 있으면 향상을 건너뛰고, 비어있을 때만 수행
        if pre_existing_ui_text:
            self.emit_log("enhancePromptEdit에 이미 텍스트가 있어 프롬프트 향상을 건너뜁니다.")
            prompt = pre_existing_ui_text
        elif self.controller.is_lm_connected():
            self.emit_log("LM Studio를 통해 프롬프트 향상 중...")
            enhanced = self.enhance_prompt(prompt)
            if enhanced:
                prompt = enhanced
                self.emit_log("LM Studio 프롬프트 강화 완료.")

                # 🚀 main.py에 연결된 이벤트를 통해 GUI 창(enhancePromptEdit)에 텍스트 주입
                self.signals.enhanced_prompt.emit(prompt)

                # QEventLoop가 GUI를 새로고침하고 텍스트를 완전히 반영할 수 있도록 안전하게 대기
                for _ in range(5):
                    time.sleep(0.05)
                    QApplication.processEvents()
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

        # (이후 ComfyUI 큐 등록 및 웹소켓 통신 코드는 기존과 동일)
        workflow_json_str = json.dumps(workflow, indent=2, ensure_ascii=False)
        self.emit_log(f"[DEBUG] 워크플로우 JSON:\n{workflow_json_str[:500]}...")

        self.signals.status.emit("워크플로우 큐 등록 중...")
        try:
            response = self.comfy_api.prompt(workflow, timeout=self.controller.config.comfyui.timeout_seconds)
            response.raise_for_status()
        except Exception as e:
            error_detail = ""
            try:
                if hasattr(response, 'text'):
                    error_detail = f" / {response.text[:200]}"
            except:
                pass
            self.emit_log(f"[ERROR] ComfyUI 응답 실패: {str(e)}{error_detail}")
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

            self.emit_log("ComfyUI WebSocket 연결 프로세스 시작")
            
            # 👇 [👍 수정 및 교체] 웹소켓이 '진짜' 연결될 때까지 최대 2초간 안전하게 대기합니다.
            connected_wait = 0
            while not getattr(self.comfy_ws, "_connected", False) and connected_wait < 20:
                time.sleep(0.1)
                connected_wait += 1
                QApplication.processEvents()
                
            if getattr(self.comfy_ws, "_connected", False):
                self.emit_log("ComfyUI WebSocket 연결 완벽 성공!")
            else:
                self.emit_log("[⚠️ 경고] WebSocket 연결 수립 지연 - HTTP 폴링으로 진행률 추적을 대체합니다.")
            
        except Exception as exc:
            self.emit_log(f"WebSocket 초기화 실패: {exc}")
            self.comfy_ws = None


        self.signals.status.emit("이미지 생성 중...")

        interval = max(self.controller.config.comfyui.poll_interval_seconds, 0.2)
        attempts = int(self.controller.config.comfyui.max_wait_seconds / interval)
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
                        return True
           
            # 👍 아래와 같이 주석 처리하여 가짜 게이지 상승을 막습니다.
            # if not getattr(self.comfy_ws, "_connected", False):
            #     self.signals.progress.emit(min(95, 10 + attempt * 3))
            time.sleep(interval)

        raise RuntimeError("이미지 생성 시간이 초과되었습니다.")

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

    def _comfyui_node_exists(self, node_name: str, base_url: str) -> bool:
        try:
            response = self.comfy_api.session.get(
                f"{base_url.rstrip('/')}/object_info/{node_name}",
                timeout=(0.5, 1.0)
            )
            if response.status_code != 200:
                return False
            payload = response.json()
            return isinstance(payload, dict) and node_name in payload
        except Exception:
            return False

    def _validate_workflow(self, workflow: Dict[str, Any]):
        if not isinstance(workflow, dict) or not workflow:
            raise RuntimeError("생성 워크플로우가 비어 있습니다.")

        issues = []
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

        if issues:
            raise RuntimeError("ComfyUI 워크플로우 검증 실패: " + "; ".join(issues))

    def build_workflow(self, profile, model_name, prompt, negative, seed):
        s = self.snapshot
        manager = self.controller.workflow_manager
        prefix = self.controller.build_filename_prefix()
        comfy_url = s["comfy_url"]

        # ZImage/Turbo 모델 처리
        if manager.is_zimage_model(model_name) or profile.workflow_type == "zimage":
            required_nodes = ["UnetLoaderGGUF", "CLIPLoaderGGUF", "VAELoader", "KSampler", "TextEncodeZImageOmni"]
            missing = [name for name in required_nodes if not self._comfyui_node_exists(name, comfy_url)]
            if missing:
                self.emit_log(f"ZImage 전용 노드 누락: {', '.join(missing)}. 기본 checkpoint 경로로 대체합니다.")
                return manager.render_checkpoint_workflow(
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

            clips = self.controller.model_fetcher.get_comfyui_clips(comfy_url)
            vaes = self.controller.model_fetcher.get_comfyui_vaes(comfy_url)
            if not clips:
                raise RuntimeError("ComfyUI CLIP 모델을 찾을 수 없습니다.")
            return manager.render_zimage_workflow(
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
        if profile.workflow_type == "flux_gguf" or manager.is_flux_model(model_name) or profile.family == "flux":
            required_nodes = ["UnetLoaderGGUF", "DualCLIPLoaderGGUF", "FluxGuidance", "VAELoader"]
            missing = [name for name in required_nodes if not self._comfyui_node_exists(name, comfy_url)]
            if missing:
                self.emit_log(f"Flux 전용 노드 누락: {', '.join(missing)}. 기본 checkpoint 경로로 대체합니다.")
                return manager.render_checkpoint_workflow(
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

            clips = self.controller.model_fetcher.get_comfyui_clips(comfy_url)
            vaes = self.controller.model_fetcher.get_comfyui_vaes(comfy_url)
            if len(clips) < 2:
                raise RuntimeError("Flux 모델은 2개의 CLIP 모델이 필요합니다. ComfyUI에 Flux용 CLIP 2개를 로드해 주세요.")
            clip1, clip2 = profile.select_clip_pair(clips)
            return manager.render_flux_gguf_workflow(
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
        if manager.is_gguf_model(model_name):
            clips = self.controller.model_fetcher.get_comfyui_clips(comfy_url)
            vaes = self.controller.model_fetcher.get_comfyui_vaes(comfy_url)
            if not clips:
                raise RuntimeError("ComfyUI CLIP 모델을 찾을 수 없습니다.")
            return manager.render_gguf_workflow(
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

        # Checkpoint 모델 처리
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
            clip_source = None
            if positive_source and isinstance(positive_source, list) and len(positive_source) > 0:
                pos_node_id = str(positive_source[0])
                pos_node = workflow.get(pos_node_id, {})
                clip_source = pos_node.get("inputs", {}).get("clip")
            
            if not clip_source:
                # 못 찾으면 기본 템플릿의 정석 배치 번호 백업 매핑
                for node_id, node in workflow.items():
                    if node.get("class_type") in ("CLIPLoader", "CheckpointLoaderSimple"):
                        clip_source = [node_id, 1]
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
            
            # UI 가변 값 취합
            facedetailer_denoise = s.get("facedetailer_denoise", 0.4)
            facedetailer_steps = s.get("facedetailer_steps", 20)
            facedetailer_cfg = s.get("facedetailer_cfg", 4.0)
            facedetailer_guide_size = s.get("facedetailer_guide_size", 256)
            facedetailer_max_size = s.get("facedetailer_max_size", 512)
            facedetailer_feather = s.get("facedetailer_feather", 5)
            
            self.emit_log(
                f"[AI 안면 정밀 보정] 파이프라인 가동 ── "
                f"Steps: {facedetailer_steps}, CFG: {facedetailer_cfg}, Denoise: {facedetailer_denoise}"
            )
            
            # FaceDetailer 핵심 노드 조립 및 결합
            facedetailer_node_id = str(int(detector_node_id) + 1)
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
                    "sampler_name": "dpmpp_2m_sde",        # 안면 질감 묘사 전용 고성능 고화질 샘플러 고정
                    "scheduler": "karras",
                    "denoise": facedetailer_denoise,
                    "feather": facedetailer_feather,
                    "noise_mask": True,
                    "force_inpaint": True,
                    "bbox_detector": [detector_node_id, 0],
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

        # 1. 모델이 FLUX이거나 ZImage 계열일 때 ➡️ '문장형' 프롬프트 분기
        if is_flux or is_zimage:
            self.emit_log(f"[AI 자동 분석] '{comfy_model_name}' 모델 감지: '문장형' 프롬프트 지시문을 사용합니다.")
            system_prompt = ext_prompts.get("system_prompt_flux_kr" if use_korean else "system_prompt_flux_en")
        
       # 2. 저거넛, 리얼비스를 포함한 나머지 모든 SDXL 계열일 때 ➡️ '태그형' 프롬프트 분기
        else:
            self.emit_log(f"[AI 자동 분석] '{comfy_model_name}' 모델 감지: '태그형(쉼표 구분)' 프롬프트 지시문을 사용합니다.")
            system_prompt = ext_prompts.get("system_prompt_sdxl_kr" if use_korean else "system_prompt_sdxl_en")

        # 만약 json 매핑 문제로 해당 키가 안 읽히면 백업용 기본값 지정
        if not system_prompt:
            system_prompt = ext_prompts.get("system_prompt_sdxl_kr" if use_korean else "system_prompt_sdxl_en")

        return enhance_prompt_sync(
            lm_url=s["lm_url"],
            model=model,
            prompt=prompt,
            system_prompt=system_prompt,
            timeout=self.controller.config.lmstudio.timeout_seconds
        )



    def download_first_image(self, history_item: Dict[str, Any]) -> Optional[Path]:
        for output in history_item.get("outputs", {}).values():
            images = output.get("images", [])
            if not images:
                continue
            image = images[0]
            response = self.comfy_api.view({
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
