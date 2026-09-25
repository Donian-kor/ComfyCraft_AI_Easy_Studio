"""Prompt building, validation, and LM Studio enhancement helpers."""

from __future__ import annotations

import json
import traceback
import re
from pathlib import Path
from typing import Any, Optional, cast

import requests
from PySide6.QtCore import QThread, Signal


# ---------------------------------------------------------------------------
# Pure helpers (no Qt dependency)
# ---------------------------------------------------------------------------

def normalize_prompt(text: str) -> str:
    """Trim extra whitespace and normalize prompt input."""
    return (text or "").strip()


def prompt_character_count(text: str) -> int:
    return len(normalize_prompt(text))


def build_negative_prompt(default_text: str) -> str:
    return normalize_prompt(default_text) or "low quality, blurry, bad anatomy"


# ---------------------------------------------------------------------------
# External prompts.json loader
# ---------------------------------------------------------------------------

_PROMPTS_FILE_CANDIDATES = (
    Path(__file__).resolve().parent.parent.parent / "workflows" / "prompt.json",
)

_FALLBACK_PROMPTS: dict[str, str] = {
  "system_prompt_flux_en": "You are a master AI Image Prompt Engineer specialized in the ComfyUI workflow and FLUX (specifically Krea Dev) model architecture. Your task is to transform the user's brief input into a highly detailed English prompt that maximizes FLUX's natural language understanding capabilities.\n\nFollow this strict output structure:\nWrite a cohesive, cinematic, and descriptive paragraph of English text. Do not use any brackets, section headers like [SUBJECT] or [ENVIRONMENT] in the actual prompt text. Instead, naturally embed the subject, environment, lighting, and style into a flowing narrative. Use descriptive adjectives (e.g., 'intensely detailed', 'soft golden light') instead of weighted tags (e.g., (epic:1.3)) to emphasize elements.\nWrite a comma-separated list of undesired elements.\n\nMandatory Rules:\n1. **ABSOLUTELY FORBIDDEN:** Never add prefixes like 'masterpiece, best quality, ultra-detailed, 8k, sharp focus' (FLUX ignores these and they add noise). Never add '--ar', '--neg', or any other WebUI/Midjourney syntax. Never add brackets like [SUBJECT]: to the final prompt output.\n2. Use Natural Language Emphasis: Instead of weighting syntax, use words like 'extremely', 'highly detailed', 'very prominent' to guide the model's focus.\n3. If the user's input is vague or too brief, DO NOT ask clarifying questions. Intelligently infer missing details using cinematic tropes, artistic best practices, and logical context.\n4. If the user asks for a portrait, automatically include 'deformed iris, asymmetrical eyes, crooked nose, bad teeth' in the [NEGATIVE PROMPT] list.\n5. When the input is in Korean, perfectly interpret the cultural nuance, emotional subtext, and idiomatic expressions before translating them into the final English prompt. Output only English in the PROMPT block.\n\nOutput ONLY the final prompt without Markdown formatting, code blocks, or intro/outro commentary.",
  
  "system_prompt_flux_kr": "당신은 ComfyUI 워크플로우와 FLUX(특히 Krea Dev) 모델에 특화된 최고 수준의 AI 이미지 프롬프트 엔지니어입니다. 사용자의 짧은 입력을 FLUX의 자연어 이해 능력을 극대화하는 상세한 영어 프롬프트로 변환해야 합니다.\n\n반드시 아래 구조를 따라 작성하세요:\n주제, 배경, 조명, 스타일을 자연스럽게 녹여낸 시네마틱하고 서술적인 영어 문단을 작성하세요. 실제 프롬프트 텍스트에는 [SUBJECT], [ENVIRONMENT] 같은 섹션 헤더나 괄호를 절대 넣지 마세요. 대신 'intensely detailed', 'soft golden light' 같은 형용사를 사용해 강조하세요.\n원치 않는 요소들을 쉼표로 구분하여 나열하세요.\n\n필수 실행 규칙:\n1. **절대 금지:** 'masterpiece, best quality, ultra-detailed, 8k, sharp focus' 같은 접두사를 넣지 마세요 (FLUX는 무시하며 오히려 노이즈만 추가합니다). '--ar', '--neg' 또는 기타 WebUI/Midjourney 문법도 절대 출력하지 마세요. 최종 프롬프트에 [SUBJECT]: 같은 대괄호를 넣지 마세요.\n2. 자연어 강조: (epic:1.3) 같은 가중치 문법 대신 'extremely', 'highly detailed', 'very prominent' 같은 단어를 사용해 모델의 집중력을 유도하세요.\n3. 입력이 모호하거나 너무 짧을 경우, 질문하지 말고 영화적 클리셰와 예술적 감각으로 디테일을 추론하여 채우세요.\n4. 인물(초상화) 주제일 경우, [NEGATIVE PROMPT]에 'deformed iris, asymmetrical eyes, crooked nose, bad teeth'를 자동으로 포함하세요.\n5. 한국어 입력 시, 문화적 뉘앙스와 감정적 함축 의미를 완벽하게 해석하여 최종 영어 프롬프트로 번역하세요. 프롬프트는 반드시 영어로만 출력합니다.\n\n최종 출력물은 코드블록이나 부가 설명 없이 정해진 구조 그대로만 제공하세요.",

  "system_prompt_sdxl_en": "You are a master AI Image Prompt Engineer specialized in Juggernaut XL Ragnarok and RealVisXL models. Your task is to transform the user's brief input into a high-quality, comma-separated tag-style English prompt.\n\nFollow this strict output structure:\nWrite a highly detailed list of English tags separated by commas. Start with the core subject (e.g., 'photo of a young Korean woman'), followed by appearance, clothing, environment/background, lighting, and camera/cinematic style tags.\nDO NOT write long sentences, paragraphs, or narrative verbs like 'is walking' or 'is sitting'. Use clear nouns, descriptive adjectives, and short cinematic phrases.\n\nKey Model Requirements to Inject:\n1. For Juggernaut XL: Emphasize rich environmental textures (e.g., 'lush green mossy ground, intricate details on tree barks, detailed fabric texture') and atmospheric elements.\n2. For RealVisXL: Emphasize realistic camera settings, physical lighting, and raw photo quality (e.g., 'shot on 35mm lens, f/2.0, dslr portrait, dappled sunlight filtering through the canopy, volumetric lighting, realistic shadows, raw photo').\n\nMandatory Rules:\n1. ABSOLUTELY FORBIDDEN: Never add prefixes like 'masterpiece, best quality, ultra-detailed'. Never add markdown code blocks, backticks, intros, or outros.\n2. Output ONLY the final list of tags separated by commas, in plain English without any surrounding text."
,
  "system_prompt_sdxl_kr": "당신은 Juggernaut XL Ragnarok 및 RealVisXL 모델에 특화된 최고 수준의 AI 이미지 프롬프트 엔지니어입니다. 당신의 임무는 사용자의 짧은 한국어 또는 영어 입력을 쉼표(,)로 구분된 고품질 영어 태그 형태의 프롬프트로 변환하는 것입니다.\n\n반드시 아래의 출력 구조를 엄격히 따르세요:\n문장이나 줄글이 아닌, 핵심 단어(태그)들을 쉼표로 연결한 영어 리스트 형태로 작성하세요. 시작은 항상 핵심 주제(예: 'photo of a young Korean woman')로 하고, 이어서 외모 묘사, 의상, 배경/환경, 조명, 카메라/시네마틱 스타일 태그 순서로 단어들을 배치하세요.\n'is walking', 'is sitting'과 같은 긴 문장, 문단, 또는 서술형 동사는 절대 쓰지 마세요. 명사, 명사 구절, 형용사 위주의 짧은 시네마틱 태그만 사용해야 합니다.\n\n각 모델별 필수 주입 요구사항:\n1. Juggernaut XL 기준: 풍성한 환경적 질감(예: 'lush green mossy ground, intricate details on tree barks, detailed fabric texture')과 대기 표현을 강조하세요.\n2. RealVisXL 기준: 실제 카메라 설정, 물리적 조명 및 원본 사진 품질(예: 'shot on 35mm lens, f/2.0, dslr portrait, dappled sunlight filtering through the canopy, volumetric lighting, realistic shadows, raw photo')을 강조하세요.\n\n필수 실행 규칙:\n1. 절대 금지: 'masterpiece, best quality, ultra-detailed'와 같은 무의미한 접두사를 넣지 마세요. 마크다운 코드 블록(```), 백틱, 시작 인사나 끝맺음말(설명 등)을 절대 출력하지 마세요.\n2. 최종 출력물은 주변의 부가 설명 없이 오직 쉼표로 구분된 영문 태그 리스트만 일반 텍스트로 제공하세요."
  ,
  "system_prompt_ernie_en": "You are a master AI image prompt engineer specialized in ERNIE-AIO-Base and ERNIE-AIO-Turbo checkpoints for ComfyUI. Transform the user's brief input into one effective natural-language English image prompt. Preserve explicit details, infer missing visual details without asking questions, and describe the subject, setting, composition, lighting, colors, atmosphere, and style when relevant. For posters, advertisements, covers, infographics, logos, or UI layouts, describe layout, visual hierarchy, spacing, alignment, balance, and focal points. Preserve exact wording and describe placement and legibility when readable text is requested; otherwise do not add text, logos, watermarks, or UI elements. Do not use weighted syntax, Midjourney commands, repetitive quality spam, or a negative-prompt section. Output only the final prompt.",

  "system_prompt_ernie_kr": "당신은 ComfyUI의 ERNIE-AIO-Base 및 ERNIE-AIO-Turbo 체크포인트용 AI 이미지 프롬프트 엔지니어입니다. 사용자의 입력을 자연어 영어 이미지 프롬프트 하나로 변환하고 명시된 디테일을 보존하세요. 필요한 경우 주제, 환경, 구도, 조명, 색감, 분위기, 스타일을 구체적으로 묘사하세요. 포스터, 광고물, 표지, 인포그래픽, 로고 또는 UI 레이아웃이면 배치, 시각적 계층, 여백, 정렬, 균형, 시선 지점을 설명하세요. 텍스트를 요청하면 정확한 문구와 위치 및 가독성을 유지하고, 요청하지 않았다면 글자, 로고, 워터마크, UI를 추가하지 마세요. 가중치 문법, Midjourney 문법, 반복적인 품질 표현, 네거티브 프롬프트는 사용하지 말고 최종 프롬프트만 출력하세요."
}



def load_external_prompts() -> dict[str, Any]:
    # 1. 내 컴퓨터 안에 "prompts.json" 파일이 실제로 존재하는지 뒤져봅니다.
    for file_path in _PROMPTS_FILE_CANDIDATES:
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    # 2. 파일이 있다면, 그 파일 안의 내용으로 통째로 교체합니다!
                    return cast(dict[str, Any], json.load(f))
            except Exception:
                # 파일 읽다가 에러가 나면 1단계의 백업본을 씁니다.
                return dict(_FALLBACK_PROMPTS)
                
    # 3. 만약 prompts.json 파일이 어디에도 없다면 1단계의 백업본을 리턴합니다.
    return dict(_FALLBACK_PROMPTS)

# ---------------------------------------------------------------------------
# Sampler / scheduler constants (single source of truth)
# ---------------------------------------------------------------------------

SAMPLER_NAMES = {
    "DPM++ SDE·부드러움": "dpmpp_2m_sde",
    "DPM++ 2M·균형": "dpmpp_2m",
    "Euler·선명함": "euler",
    "Euler Ancestral·다양함": "euler_ancestral",
    "LCM·초고속": "lcm",
    "DDIM·안정적": "ddim",
}

SCHEDULER_NAMES = [
    "normal",
    "karras",
    "exponential",
    "sgm_uniform",
    "simple",
    "ddim_uniform",
    "beta",
    "linear_quadratic",
    "kl_optimal",
]


def sampler_label_to_value(label: str) -> str:
    return SAMPLER_NAMES.get(label, "euler")


def sampler_value_to_label(value: str) -> str:
    for label, mapped in SAMPLER_NAMES.items():
        if mapped == value:
            return label
    return value


# ---------------------------------------------------------------------------
# LM Studio prompt enhancement (shared between worker + sync call)
# ---------------------------------------------------------------------------

def _build_chat_payload(model: str, system_prompt: str, user_prompt: str) -> dict[str, Any]:
    """Build a non-streaming prompt-enhancement request.

    The enhancement task needs the final prompt, not the model's chain-of-thought.
    LM Studio supports several reasoning controls depending on backend/model;
    extra fields are harmless for OpenAI-compatible servers that ignore them.
    """
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "temperature": 0.2,
        # Give the model enough room for the final prompt without encouraging
        # a long chain-of-thought.
        "max_tokens": 2000,
        "reasoning": False,
        "enable_thinking": False,
        "chat_template_kwargs": {"enable_thinking": False},
    }


def _normalize_lm_url(url: str) -> str:
    normalized = (url or "").rstrip("/")
    return normalized.replace("127.0.0.1", "localhost")


def _strip_reasoning_prefix(text: str) -> str:
    """Remove explicit reasoning/thinking sections and keep a final answer when present."""
    if not text:
        return ""

    text = text.replace("\ufeff", "").strip()

    # XML-style reasoning block.
    lower = text.lower()
    for start_tag in ("<think>", "<thinking>", "<reasoning>"):
        start_pos = lower.find(start_tag)
        if start_pos >= 0:
            for end_tag in ("</think>", "</thinking>", "</reasoning>"):
                end_pos = lower.find(end_tag, start_pos + len(start_tag))
                if end_pos >= 0:
                    tail = text[end_pos + len(end_tag):].strip()
                    if tail:
                        text = tail
                    else:
                        return ""
                    break
            else:
                # Unclosed reasoning: do not treat it as a final prompt.
                return ""

    # Textual final-answer markers. Only use the part after them.
    markers = (
        "final answer:",
        "final response:",
        "final prompt:",
        "final output:",
        "output:",
        "answer:",
    )
    lower = text.lower()
    positions = [(lower.rfind(marker), marker) for marker in markers if lower.rfind(marker) >= 0]
    if positions:
        pos, marker = max(positions, key=lambda x: x[0])
        tail = text[pos + len(marker):].strip()
        if tail:
            text = tail

    # Strip markdown fences and a leading "Prompt:" wrapper.
    text = re.sub(r"^\s*```(?:text|plaintext|markdown)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```\s*$", "", text).strip()
    text = re.sub(r"^\s*prompt\s*:\s*", "", text, flags=re.I)

    # Remove obvious reasoning headings if they somehow remain at the beginning.
    text = re.sub(
        r"^\s*(?:here['’]?s\s+a\s+thinking\s+process|thinking\s+process|analysis|chain\s+of\s+thought)\s*:?\s*",
        "",
        text,
        flags=re.I,
    ).strip()

    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        text = text[1:-1].strip()

    return text


def _clean_model_text(value: object) -> str:
    """Convert supported LM Studio/OpenAI text fields into clean final text."""
    if value is None:
        return ""

    if isinstance(value, str):
        return _strip_reasoning_prefix(value)

    if isinstance(value, list):
        items = cast(list[Any], value)
        parts: list[str] = []
        for item in items:
            if isinstance(item, str):
                cleaned = _strip_reasoning_prefix(item)
                if cleaned:
                    parts.append(cleaned)
            elif isinstance(item, dict):
                item_fields = cast(dict[str, Any], item)
                # Prefer actual text output fields over reasoning fields.
                for key in ("text", "content", "output_text", "value"):
                    candidate = item_fields.get(key)
                    if isinstance(candidate, str) and candidate.strip():
                        cleaned = _strip_reasoning_prefix(candidate)
                        if cleaned:
                            parts.append(cleaned)
                            break
        return "\n".join(parts).strip()

    if isinstance(value, dict):
        fields = cast(dict[str, Any], value)
        for key in ("text", "content", "output_text", "value"):
            candidate = fields.get(key)
            if isinstance(candidate, (str, list)):
                cleaned = _clean_model_text(cast(str | list[Any], candidate))
                if cleaned:
                    return cleaned
        return ""

    return ""


def _extract_text_from_message(message: object) -> str:
    """Extract ONLY final-answer fields from a message.

    reasoning_content/reasoning are deliberately excluded here. They are
    internal thinking and must never be shown as the enhanced image prompt.
    """
    if isinstance(message, (str, list)):
        return _clean_model_text(cast(str | list[Any], message))

    if not isinstance(message, dict):
        return ""

    message_fields = cast(dict[str, Any], message)
    for key in ("content", "text", "output_text", "final", "answer", "response"):
        cleaned = _clean_model_text(message_fields.get(key))
        if cleaned:
            return cleaned

    return ""


def _extract_final_from_reasoning(reasoning: object) -> str:
    """Best-effort extraction when a model puts its final answer in reasoning_content."""
    if not isinstance(reasoning, str) or not reasoning.strip():
        return ""

    text = reasoning.strip()
    lower = text.lower()

    # Explicit final-answer marker is the safest fallback.
    markers = (
        "final answer:",
        "final response:",
        "final prompt:",
        "final output:",
    )
    positions = [(lower.rfind(marker), marker) for marker in markers if lower.rfind(marker) >= 0]
    if positions:
        pos, marker = max(positions, key=lambda x: x[0])
        return _strip_reasoning_prefix(text[pos + len(marker):])

    # If the model has an obvious "Drafting the Prompt" section, extract the
    # final attempt only when it looks like a prompt rather than prose.
    for marker in ("final prompt", "final output", "final version"):
        pos = lower.rfind(marker)
        if pos >= 0:
            tail = text[pos:].split(":", 1)
            if len(tail) == 2:
                candidate = _strip_reasoning_prefix(tail[1])
                if candidate:
                    return candidate

    # Never return raw reasoning: that is worse than reporting no valid prompt.
    return ""


def _parse_chat_response(response_json: dict[str, Any]) -> str:
    """Parse final answer from common LM Studio/OpenAI response shapes."""
    choices = response_json.get("choices")
    if isinstance(choices, list):
        for choice in cast(list[Any], choices):
            if not isinstance(choice, dict):
                continue
            choice_fields = cast(dict[str, Any], choice)

            # Final response first.
            final_text = _extract_text_from_message(choice_fields.get("message"))
            if final_text:
                return final_text

            # Some servers put the final text directly on the choice.
            for key in ("text", "output_text", "content", "answer", "response", "final"):
                final_text = _clean_model_text(choice_fields.get(key))
                if final_text:
                    return final_text

            # Last-resort reasoning extraction, ONLY with an explicit final marker.
            message = choice_fields.get("message")
            if isinstance(message, dict):
                message_fields = cast(dict[str, Any], message)
                final_text = _extract_final_from_reasoning(
                    message_fields.get("reasoning_content") or message_fields.get("reasoning")
                )
                if final_text:
                    return final_text

    # Responses / REST styles.
    for key in ("output_text", "text", "content", "response", "answer", "final"):
        final_text = _clean_model_text(response_json.get(key))
        if final_text:
            return final_text

    output = response_json.get("output")
    if isinstance(output, list):
        collected: list[str] = []
        for item in cast(list[Any], output):
            if not isinstance(item, dict):
                continue
            item_fields = cast(dict[str, Any], item)
            item_type = str(item_fields.get("type", "")).lower()
            if "reason" in item_type:
                continue
            candidate = _extract_text_from_message(item_fields)
            if candidate:
                collected.append(candidate)
        if collected:
            return "\n".join(collected).strip()

    return ""

def _request_native_chat(
    base_url: str,
    model: str,
    prompt: str,
    system_prompt: str,
    timeout: int,
) -> str:
    """Use LM Studio's native /api/v1/chat endpoint with reasoning disabled."""
    url = f"{base_url}/api/v1/chat"
    payload: dict[str, Any] = {
        "model": model,
        "input": prompt,
        "system_prompt": system_prompt,
        "stream": False,
        "temperature": 0.2,
        "max_output_tokens": 2000,
        "reasoning": "off",
    }
    response = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=timeout,
    )
    response.raise_for_status()
    return _parse_chat_response(response.json())


def enhance_prompt_sync(
    lm_url: str,
    model: str,
    prompt: str,
    system_prompt: str,
    timeout: int = 15,
) -> Optional[str]:
    """Enhance a prompt using LM Studio, preferring reasoning-off execution."""
    if not model or model == "로드된 모델 없음":
        return None

    base_url = _normalize_lm_url(lm_url)

    # 1) Native LM Studio REST API. Best for controlling reasoning behavior.
    try:
        enhanced = _request_native_chat(
            base_url, model, prompt, system_prompt, timeout
        )
        if enhanced:
            return enhanced
    except Exception:
        pass

    # 2) OpenAI-compatible endpoint.
    url = f"{base_url}/v1/chat/completions"
    payload = _build_chat_payload(model, system_prompt, prompt)
    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=timeout,
        )
        response.raise_for_status()
        return _parse_chat_response(response.json()) or None
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Qt-based async worker (used by the standalone enhance button)
# ---------------------------------------------------------------------------

class PromptEnhanceWorker(QThread):
    """LM Studio 프롬프트 향상 전용 워커"""
    finished_signal = Signal(str)
    error_signal = Signal(str)
    debug_signal = Signal(str)

    def __init__(self, lm_url: str, model_name: str, prompt: str, system_prompt: str, timeout: int = 20):
        super().__init__()
        self.lm_url = lm_url
        self.model_name = model_name
        self.prompt = prompt
        self.system_prompt = system_prompt
        self.timeout = timeout

    def run(self):
        try:
            self.debug_signal.emit(f"[Worker] 시작: {self.lm_url}, 모델: {self.model_name}")
            base_url = _normalize_lm_url(self.lm_url)

            # 1) Native LM Studio REST API: reasoning off.
            native_url = f"{base_url}/api/v1/chat"
            native_payload: dict[str, Any] = {
                "model": self.model_name,
                "input": self.prompt,
                "system_prompt": self.system_prompt,
                "stream": False,
                "temperature": 0.2,
                "max_output_tokens": 2000,
                "reasoning": "off",
            }

            self.debug_signal.emit(f"[Worker] 요청 전송: {native_url}")
            try:
                response = requests.post(
                    native_url,
                    json=native_payload,
                    headers={"Content-Type": "application/json"},
                    timeout=self.timeout,
                )
                self.debug_signal.emit(f"[Worker] 응답 수신: {response.status_code}")

                if response.ok:
                    response_json = cast(dict[str, Any], response.json())
                    enhanced = _parse_chat_response(response_json)
                    if enhanced:
                        self.debug_signal.emit(f"[Worker] 성공(Native): {enhanced[:80]}...")
                        self.finished_signal.emit(enhanced)
                        return
            except Exception as native_exc:
                self.debug_signal.emit(f"[Worker] Native API 실패 → 호환 API 재시도: {native_exc}")

            # 2) OpenAI-compatible fallback.
            url = f"{base_url}/v1/chat/completions"
            payload = _build_chat_payload(self.model_name, self.system_prompt, self.prompt)

            self.debug_signal.emit(f"[Worker] 요청 전송: {url}")
            response = requests.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=self.timeout,
            )
            self.debug_signal.emit(f"[Worker] 응답 수신: {response.status_code}")

            if not response.ok:
                body_preview = response.text[:2200].replace("\n", " ")
                self.debug_signal.emit(f"[Worker] HTTP 오류 본문: {body_preview}")
                response.raise_for_status()

            response_json = response.json()
            enhanced = _parse_chat_response(response_json)

            if enhanced:
                self.debug_signal.emit(f"[Worker] 성공(OpenAI): {enhanced[:80]}...")
                self.finished_signal.emit(enhanced)
                return

            # Diagnostic only; never treat reasoning_content itself as the final prompt.
            try:
                raw_preview = json.dumps(response_json, ensure_ascii=False)[:1800]
            except Exception:
                raw_preview = str(response_json)[:1800]
            self.debug_signal.emit(
                f"[Worker] 최종 프롬프트 없음. 응답 구조: {raw_preview}"
            )
            self.error_signal.emit(
                "LM Studio가 최종 프롬프트를 반환하지 않았습니다. "
                "모델의 추론이 출력 제한에 걸렸거나 최종 답변을 생성하지 못했습니다."
            )

        except requests.Timeout:
            self.error_signal.emit("LM Studio 요청 시간 초과 (Timeout)")
        except requests.ConnectionError as exc:
            self.error_signal.emit(f"LM Studio 서버 연결 실패: {exc}")
        except Exception as exc:
            self.debug_signal.emit(f"[Worker] 예외 발생: {traceback.format_exc()}")
            self.error_signal.emit(f"프롬프트 향상 실패: {exc}")

