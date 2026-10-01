# LM Studio → QwenImage21PromptEnhancerT8 직접 임베딩 프로젝트

## 목표
LM Studio 기반 프롬프트 강화 dependency를 **Qwen 로컬 프롬프트 강화 서비스**로 완전 대체하여
- LM Studio 서버 연결 제거
- ComfyUI 커스텀 노드 설치 의무 제거
- QwenImage21PromptEnhancerT8 논리를 **파이썬 서비스 계층에 직접 임베드**

## 범위
- 작업 범위: **모든 모델** (FLUX, SDXL, ERNIE, ZANIME, RealVisXL, JuggernautXL, ZImage, Qwen)
- 구현 방식: **파이썬 서비스 임베딩 + 점진적 마이그레이션**
- 영향 범위: `app/services/` (신규), `app/application/generation_service.py`, `app/features/prompt/prompts.py`
- 워크플로우 템플릿: Base 템플릿 **변경 불필요** (ComfyUI 노드 삽입 불필요)

## 아키텍처 변경

### 현재 흐름 (LM Studio 의존)
```
User prompts → GenerationService → enhance_prompt_sync() → LM Studio API → Enhanced prompts
→ WorkflowManager.render() → workflow with __POSITIVE_PROMPT__ → ComfyUI → Images
```

### 새 흐름 (Qwen 직접 임베딩)
```
User prompts → GenerationService → QwenImage21PromptEnhancer.enhance() → Enhanced prompts
→ WorkflowManager.render() → workflow with __POSITIVE_PROMPT__ → ComfyUI → Images
```

**핵심 차이**: 프롬프트 강화가 **ComfyUI 노드**에서 이루어지지 않고 **파이썬 서비스**에서 이루어짐

## 세부 구현 계획 (점진적 마이그레이션)

### 0단계: Qwen 프롬프트 강화 서비스 작성 (`app/services/prompt_enhancement.py`)
**새로운 파일 생성**

- `qwen_image21.py`의 핵심 프롬프트 강화 로직 임베드 (203줄):
  - `_build_messages()` - 강화용 메시지 구성 (Qwen Skill 포함)
  - `_extract_json()` - JSON 응답 파싱 (`{"rewritten_prompt": "...", "wh_ratio": "..."}`)
  - `_validate_output()` - 강화된 프롬프트 및 종횡비 검증
  - `_clean_secret()` - API 키 및 민감 데이터 마스킹
  - `_load_skill()` - 공식 SKILL.md 로드 및 SHA256 검증
  - `_build_messages()` - 8단계 프롬프트 강화 스키마 적용

- `local_qwen_provider.py`의 지역 GGUF 로직 임베드 (108줄):
  - `LocalQwenProvider.complete()` - llama.cpp 추론 호출
  - `settings_from_values()` - 런타임 설정 관리
  - `apply_local_language_lock()` - 언어 잠금 적용

- `local_qwen_runtime.py`의 LLama GGUF 관리자 임베드 (39줄): Runtime 설정만

- ComfyUI 의존성 완전 제거 (`from comfy_api.latest import io`, `io.ComfyNode`)
- 표준 Python 파일 I/O 및 표준 라이브러리만 사용
- `select_system_prompt()` 활용 (`app/features/prompt/system_prompt.py`의 모델 family별 프롬프트 선택)

### 1단계: 생성 서비스 업데이트 (`app/application/generation_service.py`)
**수정 파일**

- `_resolve_prompt()` 메서드:
  - LM Studio `enhance_prompt_sync()` 호출 제거
  - `QwenImage21PromptEnhancer.enhance()` 호출 추가
  - 모델 family 탐지 (`system_prompt.select_system_prompt()`) 활용
  - 원본 프롬프트 유지, 서비스 계층에서 강화 수행

### 2단계: 프롬프트 유틸리티 정리 (`app/features/prompt/prompts.py`)
**수정 파일**

- LM Studio enhancement 함수 삭제:
  - `enhance_prompt_sync()` - 완전 삭제 (Qwen 서비스에서 대체)
  - `_build_chat_payload()` - LM Studio API 전용, 삭제
  - `_request_native_chat()` - LM Studio native API 전용, 삭제
  - `_normalize_lm_url()` - LM Studio URL 정리, 삭제
  - `_strip_reasoning_prefix()` - reasoning 제거, 보관 (LM Studio 전용)
  - `_clean_model_text()` - LM Studio 응답 처리, 보관 (LM Studio 전용)
  - `_extract_text_from_message()` - LM Studio 응답 처리, 보관 (LM Studio 전용)
  - `_parse_chat_response()` - LM Studio 응답 처리, 보관 (LM Studio 전용)
  - `_extract_final_from_reasoning()` - LM Studio 응답 처리, 보관 (LM Studio 전용)

**유지할 함수**:
  - `normalize_prompt()` - 유틸리티, 필요 시 사용
  - `prompt_character_count()` - 유틸리티
  - `enforce_prompt_character_limit()` - 유틸리티
  - `build_negative_prompt()` - 유틸리티
  - `model_supports_negative()` - 모델 판별
  - `resolve_negative_prompt()` - 네거티브 프롬프트 결정
  - `load_external_prompts()` - 외부 프롬프트 파일 로드
  - `SAMPLER_NAMES`, `SCHEDULER_NAMES`, `sampler_label_to_value()`, `sampler_value_to_label()`

### 3단계: 워크플로우 템플릿 검증 (변경 불필요)
**복사본 미수정**

- `workflows/base/*.json` - 변경 없음 (ComfyUI 노드 삽입 불필요)
- `workflows/models/*.json` (8개) - 변경 없음
- `workflows/ERNIE-AIO-Upscale.json` - 변경 없음
- `workflow_deriver.py` - 변경 없음 (`_RUNTIME_TOKENS` 유지)
- `workflow_manager.py` - `render_*_workflow()` 메서드는 `__POSITIVE_PROMPT__` 플레이스홀더 유지, 변경 불필요

### 4단계: 사용자 정의 워크플로우 처리
**선택적 변경**

#### 4.1 `ERNIE-AIO-Upscale.json`
- **변경 불필요**: 프롬프트 강화가 파이썬 서비스 레이어에서 수행
- `CLIPTextEncode` 노드의 `text` 입력은 `__POSITIVE_PROMPT__` 플레이스홀더 또는 빈 문자열 사용

#### 4.2 `Qwen_Image.json` / `Qwen_Image_api.json`
- **변경 불필요**: Qwen 노드는 로컬 프롬프트 강화용 (이미지 생성용 Qwen 노드)
- 기존 `__POSITIVE_PROMPT__` 플레이스홀더 유지

## 구현 순서

### 1단계: Qwen 프롬프트 강화 서비스 작성
**파일**: `app/services/prompt_enhancement.py` (예상 350줄)

```python
# 주요 구성 요소:
# 1. QwenImage2.1 Skill 임베드 (192줄)
# 2. LocalQwenProvider 임베드 (108줄)  
# 3. 프롬프트 강화 클래스 (50줄)

class QwenImage21PromptEnhancer:
    def __init__(self, model_path: str = "qwen_pe_t2i_heretic-Q4_K_M.gguf"):
        self.provider = LocalQwenProvider(settings)
        self.skill = self._load_skill()  # Qwen Skill 8단계 임베드
    
    def enhance(self, prompt: str, model_family: str, options: dict) -> str:
        system_prompt = select_system_prompt(model_family)
        messages = self._build_enhancement_messages(prompt, system_prompt)
        response = self.provider.complete(messages, **options)
        enhanced = self._extract_json(response)
        return enhanced.get("rewritten_prompt", prompt)
```

### 2단계: 생성 서비스에 통합
**수정**: `app/application/generation_service.py`

```python
# _resolve_prompt() 메서드 수정:
def _resolve_prompt(self, model_name, user_prompt, negative_prompt):
    # LM Studio enhancement 제거
    # Qwen enhancement 추가:
    enhancer = QwenImage21PromptEnhancer()
    enhanced_prompt = enhancer.enhance(prompt, model_family, options)
    return enhanced_prompt, negative_prompt
```

### 3단계: 프롬프트 유틸리티 정리
**수정**: `app/features/prompt/prompts.py`

- LM Studio enhancement 함수 제거 (13개 함수)
- 시스템 프롬프트 (`select_system_prompt()`)는 Qwen 서비스에서 활용

### 4단계: 단위 테스트
```bash
pytest tests/ -q
# Qwen 프롬프트 강화 서비스 동작 확인
```

### 5단계: 통합 테스트 (선택)
```bash
# 1개 모델로 프롬프트 강화 + 이미지 생성 테스트
```

## 파일 변경 목록

### 생성 파일
- `app/services/prompt_enhancement.py` - Qwen 프롬프트 강화 서비스 (약 350줄)

### 수정 파일
- `app/application/generation_service.py` - LM Studio → Qwen enhancement 교체
- `app/features/prompt/prompts.py` - LM Studio 함수 삭제

### 변경 불필요 (복사본)
- `workflows/base/checkpoint_loadersimple.json`
- `workflows/base/unet_clploadergguf.json`
- `workflows/base/unet_dualclploadergguf.json`
- `workflows/models/*.json` (8개 파일)
- `workflows/ERNIE-AIO-Upscale.json`
- `app/core/workflow_manager.py`

## LM Studio vs Qwen: 장점 비교

| 항목 | LM Studio | Qwen 임베딩 |
|------|-----------|-------------|
| **설치 의무** | LM Studio 서버 설치 필요 | 로컬 GGUF 모델만 있으면 됨 |
| **Dependency** | 외부 API 의존 | ComfyUI 커스텀 노드 의존 |
| **워크플로우 복잡도** | Python + ComfyUI 노드 2단계 | Python 서비스 1단계 |
| **디버깅 용이성** | 어려움 (두 시스템 분리) | 쉬움 (통합 로깅) |
| **프롬프트 강화 품질** | 모델별 시스템 프롬프트 | Qwen Skill 기반 (8단계 프롬프트 강화) |

## 검증을 위한 사양

### 프롬프트 강화 작동 확인
1. **사용자가 프롬프트 입력** → `GenerationService._resolve_prompt()` 호출
2. **QwenImage21PromptEnhancer.enhance()**가 로컬로 프롬프트 강화 (약 0.5초)
3. **강화된 프롬프트**가 `__POSITIVE_PROMPT__` 플레이스홀더로 워크플로우에 삽입
4. **ComfyUI**가 강화된 프롬프트로 이미지 생성 정상 작동

### 백업 및 복구
- 변경 전 `git add -A && git commit -m "chore: work before LM Studio replacement"`
- LM Studio 로직은 `prompts.py`에서 완전 삭제 (복구 불필요)

### 호환성 유지
- 워크플로우 템플릿 변경 없음 (ComfyUI 노드 삽입 불필요)
- 모델 카드/설정 UI 변경 최소화
- 기존 `system_prompt.py` 유지 (모델별 프롬프트 선택)

## 위험성 및 완화책

### 위험성 1: Qwen 로컬 모델 로드 실패
- **완화책**: LM Studio fallback을 유지 (옵션 플래그)
- `USE_QWEN_ENHANCEMENT` 설정 추가, 기본값 `True`

### 위험성 2: 프롬프트 강화 품질 저하
- **완화책**: Qwen_Image_api.json 참조 워크플로우와 비교 테스트
- 모델별 프롬프트 강화 품질 검증

### 위험성 3: ComfyUI 커스텀 노드 의존성 문제
- **완화책**: 워크플로우 템플릿 변경 불필요

## 프로젝트 일정

| 단계 | 기간 | 담당자 |
|------|------|--------|
| Qwen 프롬프트 강화 서비스 작성 | 2일 | 개발자 |
| 생성 서비스 통합 | 1일 | 개발자 |
| 프롬프트 유틸리티 정리 | 0.5일 | 개발자 |
| 단위 테스트 | 1일 | QA |
| 통합 테스트 | 1일 | QA |
| 사용자 정의 워크플로우 처리 | 0.5일 | 개발자 |

**총 예정 기간**: 5일

## 완료 기준

### 기능
- LM Studio API 호출 완전 제거 (`enhance_prompt_sync()` 호출 없음)
- QwenImage21PromptEnhancer가 모든 모델 워크플로우에 프롬프트 강화
- 모든 모델에서 프롬프트 강화 정상 작동
- 워크플로우 템플릿 변경 없음

### 성능
- 프롬프트 강화 시간: LM Studio 대비 10% 이내 (양쪽 모두 로컬)
- CPU 사용량: 기존과 동일 수준
- 메모리 사용량: 기존과 동일 수준

### 품질
- 프롬프트 강화 품질: 기존 LM Studio 대체 가능 (Qwen Skill 기반)
- 모델 동작: 모든 모델 정상 작동
- 오류율: 0.1% 이내

## 시작 준비사항

### 0. 필요 파일 확인
- `C:\Users\donian\AppData\Local\Comfy-Desktop\ComfyUI-Installs\donian\ComfyUI\custom_nodes\minimax-h3-seedance-music3-prompt-enhancer-t8\official_skills\qwen-image-2.1\SKILL.md`
- `C:\Users\donian\AppData\Local\Comfy-Desktop\ComfyUI-Installs\donian\ComfyUI\custom_nodes\minimax-h3-seedance-music3-prompt-enhancer-t8\local_qwen_provider.py`

### 1. Qwen 모델 확인
- `qwen_pe_t2i_heretic-Q4_K_M.gguf` 모델이 프로젝트에 존재하는지 확인
- ComfyUI models 디렉토리: `ComfyUI/models/LLM/`

---

**프로젝트 리더** : 0단계(Qwen 프롬프트 강화 서비스 작성)부터 시작하겠습니다. 진행하시겠습니까?
- **네**: 즉시 `app/services/prompt_enhancement.py` 작성 시작
- **아니요**: 추가 질문이나 계획 수정 필요