"""Feature 계층 — FaceDetailer(안면 보정) 워크플로우 주입 (순수 Python).

기존 app/sections/generation.py 의 GenerationWorker._inject_facedetailer 를
Controller 참조 없이 옮긴 것이다. ComfyUI API 접근은 콜백으로 주입받는다.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Tuple

from app.models.generation import FaceDetailerSettings

# 공식 FaceDetailer sam_detection_hint 9종. 구버전 UI 값이 남아 있어도
# 여기 없으면 center-1 로 되돌린다.
VALID_SAM_DETECTION_HINTS = (
    "center-1", "horizontal-2", "vertical-2", "rect-4",
    "diamond-4", "mask-area", "mask-points", "mask-point-bbox", "none",
)

LogFn = Callable[[str], None]
NodeExistsFn = Callable[[str], bool]
FindSamModelFn = Callable[[], Optional[str]]


def find_workflow_anchors(workflow: Dict[str, Any]) -> Tuple[Optional[str], Optional[str], List[str]]:
    """FaceDetailer 결합에 필요한 기준 노드 ID 를 찾는다.

    Returns: (ksampler_id, vae_decode_id, [save_image_id, ...])
    """
    ksampler_id: Optional[str] = None
    vae_decode_id: Optional[str] = None
    save_ids: List[str] = []
    for node_id, node in workflow.items():
        if not isinstance(node, dict):
            continue
        class_type = node.get("class_type", "")
        if class_type == "KSampler":
            ksampler_id = node_id
        elif class_type == "VAEDecode":
            vae_decode_id = node_id
        elif class_type == "SaveImage":
            save_ids.append(node_id)
    return ksampler_id, vae_decode_id, save_ids


def _clip_of(workflow: Dict[str, Any], node_id: Any) -> Optional[Any]:
    try:
        return workflow.get(str(node_id), {}).get("inputs", {}).get("clip")
    except Exception:
        return None


def _resolve_clip_source(workflow: Dict[str, Any], positive_source: Any,
                         ksampler_id: str) -> Any:
    """CLIPTextEncode / FluxGuidance 체인을 따라 CLIP 원본 링크를 역추적한다."""
    clip_source = None

    if positive_source and isinstance(positive_source, list) and positive_source:
        pos_inputs = workflow.get(str(positive_source[0]), {}).get("inputs", {})
        clip_source = pos_inputs.get("clip")
        # FluxGuidance 등은 clip 대신 conditioning 링크를 가짐 → 한 단계 더 추적
        if not clip_source and isinstance(pos_inputs.get("conditioning"), list):
            try:
                clip_source = _clip_of(workflow, pos_inputs["conditioning"][0])
            except Exception:
                pass

    if not clip_source:
        # 어떤 인코더 노드든 clip 링크를 빌려온다(모든 워크플로우 종류 호환)
        for node in workflow.values():
            if not isinstance(node, dict):
                continue
            if node.get("class_type") in ("CLIPTextEncode", "TextEncodeZImageOmni"):
                cand = node.get("inputs", {}).get("clip")
                if isinstance(cand, list) and cand:
                    clip_source = cand
                    break

    if not clip_source:
        # 못 찾으면 로더 노드에서 정석 출력 인덱스로 백업 매핑
        # (CheckpointLoaderSimple clip=출력1, CLIP 계열 clip=출력0)
        for node_id, node in workflow.items():
            if not isinstance(node, dict):
                continue
            ctype = node.get("class_type", "")
            if ctype == "CheckpointLoaderSimple":
                return [node_id, 1]
            if ctype in ("CLIPLoader", "CLIPLoaderGGUF", "DualCLIPLoaderGGUF"):
                return [node_id, 0]
        clip_source = [ksampler_id, 1]


def inject_facedetailer(
    workflow: Dict[str, Any],
    seed: int,
    settings: FaceDetailerSettings,
    *,
    log: Optional[LogFn] = None,
    node_exists: Optional[NodeExistsFn] = None,
    find_sam_model: Optional[FindSamModelFn] = None,
) -> Dict[str, Any]:
    """기본 워크플로우에 FaceDetailer 노드를 주입한다 (ComfyUI Impact Pack 필요).

    노드가 없거나 조립이 실패하면 원본 워크플로우를 그대로 돌려준다 —
    안면 보정 실패가 이미지 생성 전체 실패로 번지지 않게 하기 위함이다.
    """
    emit = log or (lambda _msg: None)

    if node_exists is not None:
        if not node_exists("FaceDetailer"):
            emit("[⚠️ 알림] ComfyUI 서버에 'Impact Pack(FaceDetailer)'이 설치되어 있지 않습니다. "
                 "기본 생성으로 진행합니다.")
            return workflow
        if not node_exists("UltralyticsDetectorProvider"):
            emit("[⚠️ 알림] ComfyUI 서버에 'UltralyticsDetectorProvider(Impact Pack)'가 없습니다. "
                 "기본 생성으로 진행합니다.")
            return workflow

    try:
        ksampler_id, vae_decode_id, save_ids = find_workflow_anchors(workflow)
        if not ksampler_id or not vae_decode_id:
            emit("[⚠️ 경고] KSampler 또는 VAE Decode 노드를 찾을 수 없습니다. "
                 "FaceDetailer 주입을 건너뜁니다.")
            return workflow

        # KSampler 입력 링크에서 원본 model / positive 소스를 역추적
        ksampler_inputs = workflow[ksampler_id].get("inputs", {})
        model_source = ksampler_inputs.get("model")
        positive_source = ksampler_inputs.get("positive")
        vae_source = workflow[vae_decode_id].get("inputs", {}).get("vae")

        # 역추적 실패 대비 안전 장치
        if not model_source:
            model_source = [ksampler_id, 0]
        if not vae_source:
            vae_source = [ksampler_id, 2]

        clip_source = _resolve_clip_source(workflow, positive_source, ksampler_id)

        # 안면 인식 디텍터 노드 추가
        next_id = max(int(k) for k in workflow.keys() if str(k).lstrip("-").isdigit()) + 1
        detector_id = str(next_id)
        workflow[detector_id] = {
            "inputs": {"model_name": "bbox/face_yolov8m.pt"},
            "class_type": "UltralyticsDetectorProvider",
        }

        # SAMLoader 노드 추가 (SAM 모델이 서버에 있으면 세그멘테이션 활성화)
        sam_loader_id: Optional[str] = None
        sam_model_name = find_sam_model() if find_sam_model is not None else None
        if sam_model_name:
            sam_loader_id = str(next_id + 1)
            workflow[sam_loader_id] = {
                "inputs": {"model_name": sam_model_name, "device_mode": "AUTO"},
                "class_type": "SAMLoader",
            }
            emit(f"[AI 안면 보정] SAM 모델 연결 완료: {sam_model_name} "
                 "(SAM 세그멘테이션 기반 정밀 마스크 활성화)")

        hint = str(settings.sam_detection_hint or "center-1")
        if hint not in VALID_SAM_DETECTION_HINTS:
            hint = "center-1"

        emit(f"[AI 안면 정밀 보정] 파이프라인 가동 ── "
             f"Steps: {settings.steps}, CFG: {settings.cfg}, Denoise: {settings.denoise}, "
             f"BBoxThresh: {settings.bbox_threshold}, SAMHint: {hint}")
        if not sam_loader_id:
            emit("[FaceDetailer] SAM 모델 미연결 상태에서는 YOLO BBox 기준으로 동작합니다 "
                 "(SAM 세부 옵션은 부분 적용).")

        fd_id = str(next_id + (2 if sam_loader_id else 1))
        negative_source = ksampler_inputs.get("negative")
        workflow[fd_id] = {
            "inputs": {
                "image": [vae_decode_id, 0],
                "model": model_source,
                "clip": clip_source,
                "vae": vae_source,
                "guide_size": settings.guide_size,
                "guide_size_for": True,
                "max_size": settings.max_size,
                "seed": seed,
                "steps": settings.steps,
                "cfg": settings.cfg,
                # 안면 질감 묘사 전용 고성능 샘플러 고정
                "sampler_name": "dpmpp_2m_sde",
                "scheduler": "karras",
                "denoise": settings.denoise,
                "feather": settings.feather,
                "noise_mask": True,
                "force_inpaint": True,
                "bbox_detector": [detector_id, 0],
                "sam_model_opt": [sam_loader_id, 0] if sam_loader_id else None,
                "positive": ([positive_source[0], 0]
                             if positive_source and isinstance(positive_source, list)
                             else clip_source),
                "negative": ([negative_source[0], 0]
                             if negative_source and isinstance(negative_source, list)
                             else clip_source),
                "bbox_threshold": settings.bbox_threshold,
                "bbox_dilation": settings.bbox_dilation,
                "bbox_crop_factor": settings.bbox_crop_factor,
                "sam_detection_hint": hint,
                "sam_dilation": settings.sam_dilation,
                "sam_threshold": settings.sam_threshold,
                "sam_bbox_expansion": settings.sam_bbox_expansion,
                "sam_mask_hint_threshold": settings.sam_mask_hint_threshold,
                "sam_mask_hint_use_negative": settings.sam_mask_hint_use_negative,
                "wildcard": "",
                "cycle": settings.cycle,
                "drop_size": settings.drop_size,
            },
            "class_type": "FaceDetailer",
        }

        # 최종 저장 노드를 FaceDetailer 출력으로 우회시킨다
        for save_id in save_ids:
            node = workflow.get(save_id)
            if node and node.get("class_type") == "SaveImage":
                node["inputs"]["images"] = [fd_id, 0]
                emit(f"[AI 안면 보정] 저장 노드({save_id}번) 파이프라인 우회 연동 완료.")

        emit("[AI 안면 보정] FaceDetailer 워크플로우 조립 및 주입이 완료되었습니다.")
        return workflow

    except Exception as exc:
        emit(f"[⚠️ 시스템 에러] FaceDetailer 구조 조립 중 오류 발생: {exc}. "
             "안전을 위해 무보정 원본 생성으로 우회합니다.")
        return workflow

    return clip_source
