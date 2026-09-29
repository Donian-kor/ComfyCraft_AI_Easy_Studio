"""Feature 계층 — 워크플로우 조립/검증 (순수 Python).

기존 app/sections/generation.py 의 build_workflow / _validate_workflow 를
Controller 참조 없이 옮긴 것이다. 외부와의 상호작용은 전부 콜백 주입으로 받는다.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from app.features.generation.facedetailer import inject_facedetailer
from app.models.generation import FaceDetailerSettings, GenerationRequest

LogFn = Callable[[str], None]
NodeExistsFn = Callable[[str], bool]
GetClipsFn = Callable[[], List[str]]
GetVaesFn = Callable[[], List[str]]


def validate_workflow(workflow: Dict[str, Any], node_exists: Optional[NodeExistsFn] = None) -> None:
    """워크플로우가 ComfyUI 에 큐잉 가능한 형태인지 확인한다.

    문제가 있으면 RuntimeError 를 던진다.
    """
    if not isinstance(workflow, dict) or not workflow:
        raise RuntimeError("생성 워크플로우가 비어 있습니다.")

    issues: List[str] = []
    missing_nodes: List[str] = []

    for node_id, node in workflow.items():
        if not isinstance(node, dict):
            continue
        class_type = node.get("class_type")
        inputs = node.get("inputs")
        if not isinstance(inputs, dict):
            continue

        if class_type == "KSampler":
            for field_name in ("model", "positive", "negative", "latent_image"):
                if isinstance(inputs.get(field_name), dict):
                    issues.append(
                        f"노드 {node_id}의 {field_name} 값이 dict 형태라 ComfyUI 연결이 아닙니다."
                    )

        # 각 노드 타입이 ComfyUI 서버에 존재하는지 확인
        if class_type and node_exists is not None and not node_exists(class_type):
            missing_nodes.append(f"{class_type} (노드 ID: {node_id})")

    if missing_nodes:
        issues.append(
            f"ComfyUI에 없는 노드 타입: {', '.join(missing_nodes)}. "
            "해당 커스텀 노드가 설치되어 있는지 확인하세요."
        )

    if issues:
        raise RuntimeError("ComfyUI 워크플로우 검증 실패: " + "; ".join(issues))


def build_workflow(
    request: GenerationRequest,
    profile: Any,
    *,
    manager: Any,
    filename_prefix: str,
    log: Optional[LogFn] = None,
    node_exists: Optional[NodeExistsFn] = None,
    get_clips: Optional[GetClipsFn] = None,
    get_vaes: Optional[GetVaesFn] = None,
    find_sam_model: Optional[Callable[[], Optional[str]]] = None,
) -> Dict[str, Any]:
    """모델 프로필에 맞는 ComfyUI 워크플로우를 조립한다.

    기준점(base)은 3종류다 (workflows/base/):
      checkpoint_loadersimple  : MODEL+CLIP+VAE 내장 (단일 파일)
      unet_clploadergguf       : Unet + CLIP 1개 + VAE
      unet_dualclploadergguf   : Unet + CLIP 2개 + VAE + FluxGuidance
    프로필의 resolved_base() 값이 base/<파일명>.json 과 1:1 대응한다.

    FaceDetailer 는 어떤 기준점에서도 공통으로 마지막에 1번 주입된다.
    """
    emit = log or (lambda _msg: None)
    exists = node_exists or (lambda _name: True)
    clips_of = get_clips or (lambda: [])
    vaes_of = get_vaes or (lambda: [])

    model_name = request.comfy_model
    prompt = request.prompt
    negative = request.negative_prompt
    seed = request.seed
    prefix = filename_prefix

    base_wf: Optional[Dict[str, Any]] = None

    # 1) 프로필에 커스텀 워크플로우가 지정돼 있으면 그 파일을 우선 사용한다.
    #    (설정창 "모델 추가"로 자동 생성한 워크플로우)
    custom_file = str(getattr(profile, "workflow_file", "") or "").strip()
    if custom_file:
        try:
            base_wf = manager.render_custom_workflow(
                workflow_file=custom_file,
                model_name=model_name,
                positive_prompt=prompt,
                negative_prompt=negative,
                width=request.width,
                height=request.height,
                seed=seed,
                steps=request.steps,
                cfg=request.cfg,
                sampler_name=request.sampler,
                scheduler=request.scheduler,
                denoise=request.denoise,
                filename_prefix=prefix,
            )
            emit(f"커스텀 워크플로우 사용: {custom_file}")
        except (OSError, ValueError) as exc:
            # 커스텀 워크플로우가 깨져 있으면 기본 경로로 폴백한다(생성 중단 금지).
            emit(f"[⚠️] 커스텀 워크플로우를 쓸 수 없어 기본 경로로 대체합니다: {exc}")
            base_wf = None

    base_name = str(getattr(profile, "resolved_base", lambda: "")() or
                    getattr(profile, "workflow_type", "") or "")

    # 기준점 자리표시자 확정값 — 수동 등록에서 고른 값을 그대로 사용한다.
    profile_clip_type = str(getattr(profile, "clip_type", "") or "stable_diffusion")
    profile_guidance = getattr(profile, "guidance", None)
    if profile_guidance is None:
        profile_guidance = 3.5
    try:
        profile_guidance = float(profile_guidance)
    except (TypeError, ValueError):
        profile_guidance = 3.5

    # 기준점 2: Unet + 단일 CLIP (ZImage 등)
    if base_wf is None and base_name == "unet_clploadergguf":
        required = ["UnetLoaderGGUF", "CLIPLoaderGGUF", "VAELoader", "KSampler"]
        missing = [n for n in required if not exists(n)]
        if missing:
            raise RuntimeError(
                f"Unet+CLIP 기준점 노드 누락: {', '.join(missing)}. "
                "ComfyUI 서버에 해당 커스텀 노드를 설치해주세요."
            )
        clips = clips_of()
        if not clips:
            raise RuntimeError("ComfyUI CLIP 모델을 찾을 수 없습니다.")
        base_wf = manager.render_zimage_workflow(
            model_name=model_name,
            positive_prompt=prompt,
            negative_prompt=negative,
            width=request.width,
            height=request.height,
            seed=seed,
            steps=request.steps,
            cfg=request.cfg,
            clip_name=profile.select_clip(clips),
            vae_name=profile.select_vae(vaes_of()),
            sampler_name=request.sampler,
            scheduler=request.scheduler,
            denoise=request.denoise,
            filename_prefix=prefix,
        )

    # 기준점 3: Unet + Dual CLIP (Flux 등)
    if base_wf is None and base_name == "unet_dualclploadergguf":
        required = ["UnetLoaderGGUF", "DualCLIPLoaderGGUF", "FluxGuidance", "VAELoader"]
        missing = [n for n in required if not exists(n)]
        if missing:
            raise RuntimeError(
                f"Unet+DualCLIP 기준점 노드 누락: {', '.join(missing)}. "
                "ComfyUI 서버에 해당 커스텀 노드를 설치해주세요."
            )
        clips = clips_of()
        if len(clips) < 2:
            raise RuntimeError(
                "Flux 모델은 2개의 CLIP 모델이 필요합니다. "
                "ComfyUI에 Flux용 CLIP 2개를 로드해 주세요."
            )
        clip1, clip2 = profile.select_clip_pair(clips)
        base_wf = manager.render_flux_gguf_workflow(
            model_name=model_name,
            positive_prompt=prompt,
            negative_prompt=negative,
            width=request.width,
            height=request.height,
            seed=seed,
            steps=request.steps,
            guidance=max(1.0, profile_guidance),
            clip_name1=clip1,
            clip_name2=clip2,
            clip_type=profile_clip_type,
            vae_name=profile.select_vae(vaes_of()),
            sampler_name=request.sampler,
            scheduler=request.scheduler,
            denoise=request.denoise,
            filename_prefix=prefix,
        )

    # 기준점 1: Checkpoint (단일 파일) — 위에서 처리되지 않은 나머지 전부
    if base_wf is None:
        base_wf = manager.render_checkpoint_workflow(
            model_name=model_name,
            positive_prompt=prompt,
            negative_prompt=negative,
            width=request.width,
            height=request.height,
            seed=seed,
            steps=request.steps,
            cfg=request.cfg,
            sampler_name=request.sampler,
            scheduler=request.scheduler,
            denoise=request.denoise,
            filename_prefix=prefix,
        )

    # FaceDetailer 주입
    if request.facedetailer.enabled:
        base_wf = inject_facedetailer(
            base_wf,
            seed,
            request.facedetailer,
            log=emit,
            node_exists=node_exists,
            find_sam_model=find_sam_model,
        )

    return base_wf

