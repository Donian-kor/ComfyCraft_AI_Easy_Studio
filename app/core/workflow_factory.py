"""ComfyUI 이미지 모델용 워크플로우 자동 생성·검증 도우미 (P13).

4cut_LocalComic_Studio의 studio/services/workflow_factory.py를 이식한 모듈.
목적은 "새 모델을 추가하면 그 모델에 맞는 워크플로우 JSON을 자동으로 만들어 준다"다.

- 모델 파일명만 고르면 기본 템플릿을 복사해 체크포인트명만 주입한다 (LLM 불필요).
- 만들어진 워크플로우는 필수 노드/체크포인트 참조를 검사해 사용 가능 여부를 알려준다.
- 검증에 실패하면 저장을 막고, 이유를 사용자에게 보여준다.
- AI(LM Studio) 생성은 위 방식이 통하지 않을 때 쓰는 폴백 경로다(실험적).
"""
from __future__ import annotations

import json
import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

# 기본 템플릿: 워크플로우 종류(wf_type/base) → base/ 하위 파일명
TEMPLATE_FILES = {
    "checkpoint": "base/checkpoint_loadersimple.json",
    "checkpoint_loadersimple": "base/checkpoint_loadersimple.json",
    "gguf": "base/unet_clploadergguf.json",
    "unet_clploadergguf": "base/unet_clploadergguf.json",
    "flux_gguf": "base/unet_dualclploadergguf.json",
    "unet_dualclploadergguf": "base/unet_dualclploadergguf.json",
    "zimage": "base/unet_clploadergguf.json",
}
DEFAULT_TEMPLATE_NAME = "base/checkpoint_loadersimple.json"

# 4cut과 동일한 상수 (워크플로우 골격이 같으므로 그대로 쓸 수 있다)
DEFAULT_MODEL_PLACEHOLDER = "YOUR_MODEL.safetensors"
CHECKPOINT_NODE_TYPE = "CheckpointLoaderSimple"
CHECKPOINT_INPUT_NAME = "ckpt_name"
# ComfyCraft 템플릿은 __MODEL_NAME__ 같은 플레이스홀더를 쓴다.
# 4cut 템플릿은 값이 확정돼 있다. 둘 다 "미지정"으로 취급한다.
PLACEHOLDER_VALUES = (DEFAULT_MODEL_PLACEHOLDER, "__MODEL_NAME__", "__CHECKPOINT__")

# 필수 노드 — 워크플로우 종류별로 필요한 노드가 다르므로 분류한다.
# gguf 템플릿은 class_type 자체가 __UNET_CLASS__ / __CLIP_CLASS__ 플레이스홀더라
# 로더·인코더 노드를 이름으로 검사할 수 없다. 템플릿 실측 기준이다.
COMMON_REQUIRED_NODE_TYPES = ("KSampler", "SaveImage", "VAEDecode")
REQUIRED_BY_WF_TYPE = {
    "checkpoint": ("CheckpointLoaderSimple", "CLIPTextEncode"),
    "checkpoint_loadersimple": ("CheckpointLoaderSimple", "CLIPTextEncode"),
    "gguf": ("KSampler", "SaveImage", "VAEDecode"),
    "unet_clploadergguf": ("UnetLoaderGGUF", "CLIPLoaderGGUF", "SaveImage", "VAEDecode"),
    "flux_gguf": ("UnetLoaderGGUF", "DualCLIPLoaderGGUF", "CLIPTextEncode"),
    "unet_dualclploadergguf": ("UnetLoaderGGUF", "DualCLIPLoaderGGUF", "CLIPTextEncode"),
    "zimage": ("UnetLoaderGGUF", "CLIPLoaderGGUF", "TextEncodeZImageOmni"),
}
# 모델 파일명이 주입되는 입력 필드 (로더마다 이름이 다르다)
MODEL_INPUT_NAMES = ("ckpt_name", "unet_name", "model_name", "name")

SYSTEM_PROMPT = (
    "당신은 ComfyUI API 워크플로우(노드 ID → {class_type, inputs} 사전)를 작성하는 도우미입니다. "
    "반드시 JSON 객체 하나만 반환하고, 노드 ID는 문자열, 각 노드는 class_type과 inputs를 가진 객체여야 합니다. "
    "존재하지 않는 노드 이름을 새로 만들지 말고, 참조 워크플로우에 있는 노드 구성만 사용하세요."
)


def slugify(value) -> str:
    """프로필 id·파일명으로 쓸 수 있는 안전한 문자열을 만든다."""
    cleaned = re.sub(r"[^0-9a-zA-Z가-힣]+", "_", str(value or "").strip()).strip("_").lower()
    return cleaned or "custom_model"


def workflow_stem(model_file, model_id="") -> str:
    """자동 생성 워크플로우 파일명의 뿌리를 만든다(모델 파일명 우선)."""
    stem = Path(str(model_file or "")).stem.strip()
    return slugify(stem or model_id)


def load_workflow(path) -> dict:
    """워크플로우 JSON을 읽는다. 없거나 형식이 틀리면 예외를 올린다."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"워크플로우 파일이 없습니다: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"워크플로우 JSON 형식이 올바르지 않습니다: {e}") from e
    if not isinstance(data, dict):
        raise ValueError("워크플로우 JSON 최상위가 객체(노드 사전)가 아닙니다.")
    return data


def _is_model_loader(node: dict) -> bool:
    """모델 파일을 담는 로더 노드인지 판별한다.

    ComfyCraft의 gguf_unet.json은 class_type 자체가 __UNET_CLASS__ /
    __CLIP_CLASS__ 플레이스홀더라 이름만으로는 판별할 수 없다.
    이런 경우엔 모델 파일명 필드(ckpt_name/unet_name/...)를 담고 있는지로 본다.
    """
    class_type = str(node.get("class_type", ""))
    if "Loader" in class_type:
        return True
    inputs = node.get("inputs")
    if not isinstance(inputs, dict):
        return False
    return any(field in inputs for field in MODEL_INPUT_NAMES)


def _set_checkpoint(data: dict, model_file: str) -> bool:
    """로더 노드의 모델 파일명 필드에 값을 주입한다. 하나라도 바꾸면 True.

    ComfyCraft 템플릿은 __MODEL_NAME__ 플레이스홀더를 쓰고,
    4cut 템플릿은 값이 확정돼 있어 같은 방식으로 덮어쓴다.
    """
    changed = False
    for node in data.values():
        if not isinstance(node, dict) or not _is_model_loader(node):
            continue
        inputs = node.setdefault("inputs", {})
        for field in MODEL_INPUT_NAMES:
            if field in inputs:
                inputs[field] = model_file
                changed = True
                break
    return changed


def _first_node(data: dict, class_type: str):
    for value in data.values():
        if isinstance(value, dict) and value.get("class_type") == class_type:
            return value
    return None


def _has_node_ref(node: dict, input_name: str, data: dict) -> bool:
    """KSampler의 positive/negative 연결이 실제 노드를 가리키는지 확인."""
    value = node.get("inputs", {}).get(input_name)
    if not (isinstance(value, list) and value):
        return False
    return str(value[0]) in data


def validate_workflow_data(data: dict, model_file: str = "",
                           wf_type: str = "checkpoint") -> list:
    """워크플로우 dict를 검사해 오류 목록을 반환한다 (비어 있으면 통과)."""
    errors: list = []
    if not isinstance(data, dict):
        return ["워크플로우 최상위가 객체(노드 사전)가 아닙니다."]

    for node_type in REQUIRED_BY_WF_TYPE.get(wf_type, REQUIRED_BY_WF_TYPE["checkpoint"]):
        if _first_node(data, node_type) is None:
            errors.append(f"필수 노드({node_type})가 없습니다.")

    # 모델 파일명 주입 여부 — 로더 중 하나 이상에 실제 값이 들어 있어야 한다.
    assigned = []
    for node in data.values():
        if not isinstance(node, dict) or not _is_model_loader(node):
            continue
        inputs = node.get("inputs", {})
        for field in MODEL_INPUT_NAMES:
            if field in inputs:
                assigned.append(str(inputs[field]))
                break
    if not assigned:
        errors.append("체크포인트(모델 파일)가 워크플로우에 지정되지 않았습니다.")
    else:
        unresolved = [v for v in assigned if not v or v in PLACEHOLDER_VALUES]
        if unresolved:
            errors.append("체크포인트(모델 파일)가 워크플로우에 지정되지 않았습니다.")
        elif model_file and not any(
                Path(v).name.lower() == Path(str(model_file)).name.lower()
                for v in assigned):
            errors.append(
                f"워크플로우 체크포인트({assigned[0]})가 선택한 모델({model_file})과 다릅니다.")

    sampler = _first_node(data, "KSampler")
    if sampler is not None and not _has_node_ref(sampler, "positive", data):
        errors.append("KSampler의 positive 프롬프트 연결을 찾을 수 없습니다.")
    return errors


def validate_workflow(path, model_file: str = "", wf_type: str = "checkpoint") -> list:
    """워크플로우 파일을 읽어 검사한다."""
    try:
        data = load_workflow(path)
    except (OSError, ValueError) as exc:
        return [str(exc)]
    return validate_workflow_data(data, model_file, wf_type)


def template_path(workflows_dir, wf_type: str = "checkpoint") -> Path:
    """워크플로우 종류에 해당하는 기본 템플릿 경로."""
    return Path(workflows_dir) / TEMPLATE_FILES.get(wf_type, DEFAULT_TEMPLATE_NAME)


def build_from_template(model_file, model_id, workflows_dir,
                        wf_type: str = "checkpoint") -> Path:
    """기본 템플릿을 복사해 모델 파일명만 새 모델로 바꾼 워크플로우를 만든다.

    원본 템플릿은 절대 수정하지 않는다(복사본을 새 파일로 저장).
    남은 __PLACEHOLDER__는 그대로 두며, 생성 시점에 WorkflowManager가 채운다.
    """
    model_file = str(model_file or "").strip()
    if not model_file:
        raise ValueError("모델 파일명이 비어 있습니다.")
    src = template_path(workflows_dir, wf_type)
    data = load_workflow(src)
    if not _set_checkpoint(data, model_file):
        raise ValueError(
            f"템플릿({src.name})에 모델 로더 노드가 없어 자동 생성할 수 없습니다.")
    target = Path(workflows_dir) / f"{workflow_stem(model_file, model_id)}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return target


def build_llm_prompt(model_file, base_template=None, previous_errors=None) -> str:
    """LM Studio에 보낼 워크플로우 생성 프롬프트를 만든다."""
    lines = [
        f"이미지 생성 모델 파일: {model_file}",
        "아래 참조 워크플로우와 같은 노드 구성/연결을 유지하면서, 이 모델로 이미지를 생성하는 "
        "ComfyUI API 워크플로우 JSON을 만들어 주세요.",
        f"- {CHECKPOINT_NODE_TYPE}의 inputs.{CHECKPOINT_INPUT_NAME} 값은 정확히 '{model_file}' 로 지정합니다.",
        "- 긍정/부정 CLIPTextEncode 2개, KSampler(seed/steps/cfg/sampler_name/scheduler), "
        "EmptyLatentImage(width/height), VAEDecode, SaveImage를 포함합니다.",
        "참조 워크플로우 JSON:",
        json.dumps(base_template, ensure_ascii=False, indent=2)
        if base_template
        else "(참조 없음 — 표준 ComfyUI 이미지 생성 구성을 사용하세요.)",
    ]
    if previous_errors:
        lines.append("이전 시도의 문제점(반드시 고칠 것):")
        lines.extend(f"- {error}" for error in previous_errors)
    return "\n".join(lines)


def generate_with_llm(lm_client, model_file, workflows_dir, model_id,
                      wf_type: str = "checkpoint", retries: int = 3,
                      output_suffix: str = "_ai") -> Path:
    """LM Studio에 워크플로우 생성을 요청하고, 검증을 통과한 결과만 파일로 저장한다.

    lm_client는 chat_json(system_prompt, user_prompt) → dict 를 제공하는 객체.
    템플릿을 그대로 돌려주는(체크포인트 미지정) 응답은 채택하지 않는다.
    실패하면 RuntimeError를 던지고 기존 워크플로우는 그대로 둔다.
    """
    model_file = str(model_file or "").strip()
    if not model_file:
        raise ValueError("모델 파일명이 비어 있습니다.")
    try:
        base_template = load_workflow(template_path(workflows_dir, wf_type))
    except (OSError, ValueError):
        base_template = None

    errors: list = []
    for attempt in range(1, max(1, int(retries)) + 1):
        data = lm_client.chat_json(
            SYSTEM_PROMPT,
            build_llm_prompt(model_file, base_template, errors or None),
        )
        errors = validate_workflow_data(data, model_file, wf_type)
        if not errors:
            target = (Path(workflows_dir)
                      / f"{workflow_stem(model_file, model_id)}{output_suffix}.json")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                              encoding="utf-8")
            return target
        logger.warning("AI 워크플로우 %s차 시도 실패: %s", attempt, errors)
    raise RuntimeError("AI가 만든 워크플로우가 검증을 통과하지 못했습니다 — "
                       + " / ".join(errors))


def check_model_file(client, model_file, timeout: int = 5):
    """ComfyUI가 해당 체크포인트를 갖고 있는지 확인한다. (상태, 안내문) 반환.

    상태는 "ok"(있음) / "missing"(없음) / "unknown"(확인 불가) 중 하나다.
    """
    model_file = str(model_file or "").strip()
    if not model_file:
        return "unknown", "모델 파일이 지정되지 않았습니다."
    try:
        names = client.list_checkpoints(timeout=timeout)
    except Exception as e:  # noqa: BLE001 — 연결 불가도 '확인 불가'로 안내
        return "unknown", f"ComfyUI 확인 불가: {e}"
    if not names:
        return "unknown", "ComfyUI가 체크포인트 목록을 반환하지 않았습니다."
    target = Path(model_file).name.lower()
    if any(Path(str(name)).name.lower() == target for name in names):
        return "ok", f"ComfyUI에 {model_file} 있음"
    return "missing", f"ComfyUI에 {model_file} 없음 — checkpoints 폴더에 파일을 넣어 주세요."

