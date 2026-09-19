# LM Studio 연동

LM Studio는 로컬에서 LLM(대규모 언어 모델)을 실행하고, OpenAI 호환 API 서버로 제공해주는 프로그램입니다. 이 프로그램에서는 **한국어 아이디어를 영문 프롬프트로 확장**하는 용도로 사용합니다.

## 왜 LM Studio인가?

| 장점 | 설명 |
|------|------|
| **완전 로컬** | 데이터 외부 전송 없음, 프라이버시 보장 |
| **무료** | 라이선스 비용 없음, 모델만 다운로드하면 사용 가능 |
| **다양한 모델** | HuggingFace 수천 개 모델 지원 (GGUF 양자화) |
| **OpenAI 호환** | 표준 API로 쉬운 연동 |
| **GPU 가속** | Metal(CUDA/ROCm) 지원으로 빠른 추론 |

---

## 설치 및 기본 설정

### 1. 다운로드
- [lmstudio.ai](https://lmstudio.ai/) → OS 선택 → 다운로드 → 설치

### 2. 모델 선택 가이드

| 용도 | 추천 모델 | 양자화 | VRAM 필요 |
|------|-----------|--------|-----------|
| **균형 (추천)** | `qwen2.5-7b-instruct` | Q4_K_M | ~6 GB |
| **고품질** | `llama-3.1-8b-instruct` | Q4_K_M | ~6 GB |
| **한국어 강함** | `eeve-korean-instruct-10.8b` | Q4_K_M | ~8 GB |
| **경량/빠름** | `gemma-2-2b-it` | Q4_K_M | ~3 GB |
| **최고 품질** | `qwen2.5-14b-instruct` | Q4_K_M | ~10 GB |

**양자화 선택 팁**:
- `Q4_K_M`: 품질/속도/용량 최적 균형 (기본 추천)
- `Q5_K_M`: 조금 더 품질, 조금 더 용량
- `Q8_0`: 고품질, 큰 용량
- `Q2_K`: 최대 압축, 품질 저하 감수

### 3. 모델 로드 설정
```
모델 선택 → 우측 설정 패널:
- GPU Layers: -1 (전체 GPU) 또는 VRAM에 맞게 조정 (예: 35)
- Context Length: 4096 이상 (프롬프트 길이에 따라)
- Flash Attention: ON (지원 시)
```

---

## 로컬 서버 실행

### 서버 시작 단계
```
1. 좌측 사이드바 ↔ (Local Server) 아이콘 클릭
2. 포트: 1234 (기본값, 변경 가능)
3. 모델: 드롭다운에서 로드된 모델 선택
4. ▶ Start Server 클릭
5. 상태: "Server started at http://localhost:1234" 확인
```

### 서버 설정 옵션
| 설정 | 추천값 | 설명 |
|------|--------|------|
| **Port** | 1234 | 다른 앱과 충돌 시 변경 (프로그램 설정에서도 동일하게 변경) |
| **Host** | localhost | 외부 접속 필요 시 `0.0.0.0` (보안 주의) |
| **CORS** | ON | 웹에서 호출 시 필요, 로컬 프로그램이면 OFF 해도 됨 |
| **API Key** | 비워둠 | 인증 불필요 |

---

## 프로그램에서 연동 설정

### 1. 서버 주소 입력
- 메인 화면 `LM Studio 서버 주소` 입력란: `http://localhost:1234`
- 또는 `⚙️ 설정` 대화상자에서 동일하게 설정

### 2. 연결 확인
- `LM Studio 연결 확인` 버튼 클릭
- 🟢 준비 완료 뜨면 성공
- 🔴 미연결 시: 서버 시작 여부, 포트, 방화벽 확인

### 3. 모델 선택
- `언어 모델 (LM Studio AI)` 드롭다운에서 사용 모델 선택
- 목록 안 뜨면: LM Studio에서 모델 Load 후 서버 재시작 → 프로그램에서 새로고침

---

## 프롬프트 확장 프롬프트 (시스템 프롬프트)

프로그램은 내부적으로 다음 같은 시스템 프롬프트를 사용해 한국어를 영문으로 확장합니다:

```
You are an expert prompt engineer for Stable Diffusion/FLUX image generation.
Convert the user's Korean idea into a detailed, high-quality English prompt.
Include: subject, style, lighting, composition, quality tags, technical details.
Output ONLY the English prompt, no explanations.
```

**사용자 커스터마이징**: `workflows/prompt.json` 파일에서 시스템 프롬프트 수정 가능

---

## 추천 모델별 특성

### Qwen 2.5 시리즈 (추천 1순위)
- **한국어 이해도 최상급** (한국어 벤치마크 1위)
- 지시 따르기 능력 우수
- 7B/14B/32B 크기 선택 가능

### Llama 3.1 시리즈
- 영어 프롬프트 품질 매우 높음
- 한국어 입력도 잘 이해하지만 Qwen보다 약간 떨어짐
- 커뮤니티 지원 활발

### Gemma 2 시리즈
- 구글 개발, 경량화 우수
- 2B/9B/27B, 작은 모델도 성능 좋음
- 한국어 지원 양호

### 한국어 특화 모델 (EEVE, KoAlpaca 등)
- 한국어 이해 특화
- 영문 프롬프트 생성 품질은 범용 모델보다 낮을 수 있음
- 한국어 아이디어 입력 시 유리

---

## 성능 최적화

### GPU 레이어 수 조절
```
VRAM 8GB  이하: GPU Layers 20~30
VRAM 10~12GB: GPU Layers 35~40 (전체 -1 추천)
VRAM 16GB 이상: GPU Layers -1 (전체)
```
- CPU 오프로드 시 속도 저하, VRAM 절약
- `gguf` 모델 로드 시 자동으로 레이어 분할

### 컨텍스트 길이
- 기본 4096 토큰 충분 (프롬프트 확장용)
- 긴 대화/복잡한 지시 필요 시 8192로 증가

### 병렬 요청
- 이 프로그램은 단일 요청 순차 처리
- 동시 생성 시 LM Studio 큐잉 처리

---

## 문제 해결

| 증상 | 원인 | 해결 |
|------|------|------|
| 서버 시작 안 됨 | 포트 1234 충돌 | 다른 프로세스 종료 또는 포트 변경 |
| 모델 목록 안 뜸 | 모델 미로드 / 서버 미시작 | 모델 Load → Server Start 순서 확인 |
| 연결 실패 (프로그램) | 방화벽 / 주소 오타 | `http://localhost:1234` 정확 입력, 방화벽 허용 |
| 프롬프트 품질 낮음 | 모델 크기 작음 / 양자화 과도 | 7B 이상, Q4_K_M 이상 모델 사용 |
| 응답 느림 | GPU 레이어 부족 / CPU 오프로드 | GPU Layers 늘리기, 더 작은 모델 사용 |
| 메모리 부족 | 모델이 VRAM 초과 | 더 작은 모델, 더 높은 양자화(Q4→Q3) |

---

## 고급: 커스텀 프롬프트 템플릿

`workflows/prompt.json` 파일 구조:
```json
{
  "system_prompt": "You are an expert prompt engineer...",
  "user_template": "{korean_idea}\n\nConvert to English prompt:",
  "negative_template": "ugly, deformed, blurry, low quality..."
}
```

수정 후 프로그램 재시작 시 적용됨.

---

## 다음 단계

- [시작하기](01_getting_started.html) - 전체 워크플로우
- [프롬프트 작성](04_prompt_writing.html) - 효과적인 프롬프트 기법
- [모델 설정](03_model_settings.html) - 생성 모델과 연동
- [자주 묻는 질문](10_faq.html) - 트러블슈팅