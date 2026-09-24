# 시작하기

**ComfyCraft AI Easy Studio**에 오신 것을 환영합니다! 이 프로그램은 **LM Studio**의 똑똑한 프롬프트 작성 능력과 **ComfyUI**의 강력한 이미지 생성 기술을 하나로 합친 통합 이미지 생성 프로그램입니다. 파이썬이나 복잡한 노드 연결을 몰라도 누구나 쉽게 고품질 이미지를 생성할 수 있습니다.

---

## 주요 특징

| 기능 | 설명 |
|------|------|
| **AI 프롬프트 마법사** | 한국어 아이디어를 입력하면 AI가 상세한 영문 프롬프트로 자동 확장 |
| **자동 최적 설정** | 모델만 선택하면 Steps, CFG, Sampler, VAE, CLIP 등 최적값 자동 적용 |
| **강력한 얼굴 보정** | FaceDetailer로 얼굴 영역만 자동 인식해 픽셀 단위 보정 |
| **히스토리 관리** | 최근 생성 이미지 4장 썸네일로 저장, 클릭 한 번으로 설정 완전 복원 |
| **클립보드 연동** | 프롬프트/이미지 원클릭 복사 |

---

## 1단계: 필수 프로그램 설치

### LM Studio (프롬프트 확장용)
1. [lmstudio.ai](https://lmstudio.ai/)에서 OS에 맞는 버전 다운로드 후 설치
2. 좌측 돋보기(🔍) 클릭 → 모델 검색 (추천: `qwen2.5-7b-instruct`, `llama-3.1-8b-instruct`, `gemma-2-9b-it`)
3. 모델 다운로드 (양자화: **Q4_K_M** 또는 **Q5_K_M** 권장)
4. 상단 탭에서 모델 선택 → `Load` 클릭 (GPU 레이어 수 조정 가능)

### ComfyUI (이미지 생성 백엔드)
```bash
# 이미 설치된 경우 건너뛰기
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
pip install -r requirements.txt
```

### FaceDetailer 필수 노드 (ComfyUI Manager에서 설치)
ComfyUI 웹 UI 좌측 메뉴 **Manager**에서 다음 3가지 설치:
1. **Impact Pack** (필수 뼈대): `ComfyUI-Impact-Pack` 검색 → 설치 → **ComfyUI 완전 재시작 필수**
2. **SAM 모델** (정밀 마스크): `sam_vit_b` 검색 → `sam_vit_b_01ec64.pth` 설치
3. **YOLO 모델** (안면 감지): `face_yolov8m` 검색 → `bbox/face_yolov8m.pt` 설치

---

## 2단계: 서버 실행

### LM Studio 로컬 서버
```
1. 좌측 메뉴 ↔ (Local Server) 아이콘 클릭
2. 포트 1234 확인
3. 초록색 Start Server 버튼 클릭
4. "Server started at http://localhost:1234" 메시지 확인
```

### ComfyUI 서버 (외부 접속 허용 필수)
```bash
# 기본 실행 (로컬만)
python main.py

# 외부 접속 허용 (이 프로그램이 연결하려면 필수)
python main.py --listen --port 8188

# GPU 메모리 최적화 (선택)
python main.py --listen --port 8188 --force-fp16
```

> **확인**: 브라우저에서 `http://localhost:8188` 접속되면 성공

---

## 3단계: 이 프로그램 설치 및 실행

```bash
# 1. 저장소 복제
git clone <repository-url>
cd comfyui_Lmstudio_gui

# 2. 파이썬 가상환경 생성 및 활성화
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat

# Linux/Mac
source .venv/bin/activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 프로그램 실행
python main.py
```

---

## 4단계: 첫 이미지 생성 (5분 완성)

### ① 서버 연결 확인
프로그램 헤더에서 두 버튼 클릭:
- `LM Studio 연결 확인` → 🟢 준비 완료
- `ComfyUI 연결 확인` → 🟢 준비 완료 + 모델 목록 로드

### ② 모델 폴더 경로 설정 (ComfyUI 모델 인식용)
`⚙️ 설정` 버튼 클릭 → `모델 폴더` 입력란에 ComfyUI `models` 폴더 경로 입력
- 예: `C:\ComfyUI\models` 또는 `~/ComfyUI/models`
- `checkpoints` 또는 `unet` / `diffusion_models` 폴더가 있어야 인식됨

### ③ 모델 선택
- **언어 모델 (LM Studio AI)**: 프롬프트 확장용 (큰 모델일수록 더 상세한 프롬프트)
- **생성 모델 (ComfyUI AI 엔진)**: 이미지 생성용 (자동으로 최적 설정 적용)

### ④ 한국어 아이디어 입력
```
입력 예시:
"비 오는 날 네온사인 빛나는 사이버펑크 도시, 창가에 앉은 은발 안드로이드 소녀, 
영화 같은 조명, 8k 해상도, 마스터피스"
```
> **팁**: 구체적 명사 + 형용사 + 스타일/분위기 키워드 조합이 가장 좋습니다.

### ⑤ AI 프롬프트 마법사 실행
`✨ AI 프롬프트 마법사로 영문 확장 생성` 버튼 클릭 → 하단 에디터에 영문 프롬프트 생성됨

### ⑥ 생성 시작!
초록색 `▶ 생성 시작` 버튼 클릭 → 진행바, 경과시간, 퍼센트 실시간 표시

---

## 화면 구성

```
┌─────────────────────────────────────────────────────────────┐
│ 헤더: 앱 제목 | 서버 상태(🟢/🔴) | 테마 | ❓ 도움말 | ⚙️ 설정  │
├──────────────┬──────────────────────────────────────────────┤
│  좌측 사이드바  │  메인 작업 영역 (3단계 워크플로우)             │
│  🏠 홈         │  1️⃣ 한국어 아이디어 → AI 프롬프트 변환        │
│  🎨 ComfyUI    │  2️⃣ 핵심 생성 옵션 (모델, 비율, 고급설정)      │
│  💬 LM Studio  │  3️⃣ 생성 실행 및 결과 확인                    │
│  ⚙️ 설정       │                                              │
└──────────────┴──────────────────────────────────────────────┘
```

- **사이드바**: 마우스 올리면 자동 확장, 떼면 자동 축소
- **홈 화면**: 카드 버튼으로 각 탭 바로 이동 가능

---

## 시스템 권장 사양

| 구분 | CPU | RAM | GPU (VRAM) | 여유 용량 |
|------|-----|-----|------------|-----------|
| **최소** | Intel i5+ | 8 GB | GTX 1060 (6GB) | 50 GB+ |
| **권장** | Intel i7+ | 16 GB | RTX 3070 (8GB) | 100 GB+ |
| **고성능** | Intel i9+ | 32 GB+ | RTX 4090 (24GB) | 500 GB+ (SSD) |

> **참고**: GGUF 양자화 모델(Q4_K_S) 사용 시 VRAM 6~8GB로도 쾌적하게 동작합니다.

---

## 다음 단계

- [기본 워크플로우](02_basic_usage.html) - 3단계 전체 플로우 상세
- [모델 설정](03_model_settings.html) - 모델 프로파일, 다운로드, 폴더 설정
- [프롬프트 작성 가이드](04_prompt_writing.html) - 효과적인 프롬프트 작성법
- [생성 옵션 상세](05_generation_options.html) - Steps, CFG, Sampler 등 파라미터
- [FaceDetailer 얼굴 보정](06_facedetailer.html) - 얼굴 보정 옵션 및 활용
- [히스토리 & 단축키](07_history_shortcuts.html) - 썸네일 활용법, 단축키 모음
- [문제해결 (FAQ)](08_faq.html) - 설치/연결/생성 오류 해결