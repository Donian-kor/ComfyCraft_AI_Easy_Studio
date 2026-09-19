# 설치 및 필수 노드

본 프로그램과 완벽하게 연동되려면 **ComfyUI**가 기본 웹 서버 모드(포트 8188)로 켜져 있어야 하며, 특히 **얼굴 보정(FaceDetailer)** 기능을 쓰기 위해서는 ComfyUI 웹 화면(Manager)에서 아래 3가지를 반드시 설치해야 합니다.

## 시스템 권장 사양

| 구분 | CPU | RAM | GPU (그래픽) | 여유 용량 |
|------|-----|-----|--------------|-----------|
| **최소 사양** | Intel i5 이상 | 8 GB | GTX 1060 이상 (6GB VRAM) | 50 GB 이상 |
| **권장 사양** | Intel i7 이상 | 16 GB | RTX 3070 이상 (8GB VRAM) | 100 GB 이상 |
| **고성능** | Intel i9 이상 | 32 GB 이상 | RTX 4090 (24GB VRAM) | 500 GB 이상 (SSD) |

> **참고**: GGUF 양자화 모델(Q4_K_S) 사용 시 VRAM 6~8GBでも 쾌적하게 동작합니다.

---

## 프로그램 설치 및 실행

### 1. 저장소 복제
```bash
git clone <repository-url>
cd comfyui_Lmstudio_gui
```

### 2. 파이썬 가상환경 생성 및 활성화
```bash
# 가상환경 생성 (패키지 꼬임 방지)
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat

# Linux/Mac
source .venv/bin/activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 프로그램 실행
```bash
python main.py
```

---

## ComfyUI 필수 설치 노드 (FaceDetailer용)

ComfyUI Manager(웹 UI 좌측 메뉴)에서 설치하세요.

### 1. Impact Pack (필수 뼈대)
```
ComfyUI Manager → Install Custom Nodes
검색: "Impact Pack"
설치: ComfyUI-Impact-Pack (작성자: ltdrdata)
⚠️ 설치 후 ComfyUI 서버를 **완전히 껐다가 다시 켜세요** (재시작 필수)
```

### 2. SAM 모델 (정밀 마스크용)
```
ComfyUI Manager → Install Models
검색: "sam_vit_b"
설치: sam_vit_b_01ec64.pth
→ 저장 위치: ComfyUI/models/sams/sam_vit_b_01ec64.pth
```

### 3. YOLO 모델 (안면 감지용)
```
ComfyUI Manager → Install Models
검색: "face_yolov8m"
설치: bbox/face_yolov8m.pt
→ 저장 위치: ComfyUI/models/ultralytics/bbox/face_yolov8m.pt
```

### 설치 확인
ComfyUI 웹 UI에서 워크플로우 로드 시 `FaceDetailer` 관련 노드들이 에러 없이 보여야 합니다.

---

## LM Studio 설치 및 설정

프롬프트를 똑똑하게 확장해주는 언어 모델 서버입니다.

### 1. 다운로드 및 설치
- [LM Studio 공식 홈페이지](https://lmstudio.ai/)에서 OS에 맞는 버전 다운로드 후 설치

### 2. 모델 로드
1. 좌측 돋보기 메뉴(🔍) 클릭
2. 검색창에 사용할 언어 모델 검색 (추천: `qwen2.5-7b-instruct`, `llama-3.1-8b-instruct`, `gemma-2-9b-it`)
3. 모델 다운로드 (양자화: Q4_K_M 또는 Q5_K_M 권장)
4. 상단 탭에서 모델 선택 → `Load` 클릭 (GPU 레이어 수 조정 가능)

### 3. 로컬 서버 켜기
```
1. 좌측 메뉴 중 ↔ (Local Server) 아이콘 클릭
2. 포트가 1234로 설정되어 있는지 확인
3. 초록색 Start Server 버튼 눌러 서버 시작
4. "Server started at http://localhost:1234" 메시지 확인
```

### 4. 프로그램에서 연동 확인
- 프로그램 헤더 `LM Studio 연결 확인` 버튼 클릭
- 초록불(🟢 준비 완료) 뜨면 연동 성공

---

## ComfyUI 설치 및 실행

이미지 생성 백엔드 서버입니다.

### 1. 설치 (이미 있는 경우 건너뛰기)
```bash
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
pip install -r requirements.txt
```

### 2. 모델 다운로드
ComfyUI `models/checkpoints/` 폴더에 `.safetensors` 또는 `.gguf` 모델 파일 배치
- 추천: [HuggingFace ComfyUI 모델](https://huggingface.co/models?library=comfyui)

### 3. 서버 실행
```bash
# 기본 실행 (로컬만)
python main.py

# 외부 접속 허용 (필수: 이 프로그램이 연결하려면)
python main.py --listen --port 8188

# GPU 메모리 최적화 옵션 (선택)
python main.py --listen --port 8188 --force-fp16
```

### 4. 프로그램에서 연동 확인
- 프로그램 헤더 `ComfyUI 연결 확인` 버튼 클릭
- 모델 폴더 경로 설정 (`⚙️ 설정` → `모델 폴더` 입력)
- 초록불(🟢 준비 완료) + 모델 목록 로드되면 성공

---

## 필수 모델 다운로드 링크

### FaceDetailer용 (필수)
| 모델 | 용도 | 다운로드 |
|------|------|----------|
| `sam_vit_b_01ec64.pth` | SAM 세그멘테이션 | ComfyUI Manager에서 설치 권장 |
| `face_yolov8m.pt` | YOLO 안면 감지 | ComfyUI Manager에서 설치 권장 |

### 추천 생성 모델 (예시)
| 모델 | 패밀리 | 용도 | 비고 |
|------|--------|------|------|
| `flux1-dev-Q4_K_S.gguf` | FLUX | 실사/일반 고품질 | GGUF 양자화, VRAM 절약 |
| `zimage_turbo-Q4_K_S.gguf` | ZImage | 고속 생성 | Turbo 버전, 8~12스텝 |
| `z_anime_base.safetensors` | Z-ANIME | 웹툰/애니 | 스타일 선택 필수 |
| `animagineXL_v31.safetensors` | SDXL | 애니메이션 | 부정 프롬프트 필요 |
| `juggernaut_xl_v10.safetensors` | SDXL | 실사/범용 | 고품질 실사 |

---

## 폴더 구조 요약

```
프로젝트 루트/
├── main.py                    # 메인 엔트리
├── requirements.txt           # 파이썬 의존성
├── assets/
│   ├── help/                  # 도움말 콘텐츠
│   │   ├── md/                # 마크다운 소스
│   │   └── html/              # 빌드된 HTML (자동 생성)
│   ├── ui/                    # Qt Designer .ui 파일
│   ├── icons/                 # SVG 아이콘 리소스
│   └── themes/                # QSS 테마 파일
├── workflows/                 # ComfyUI 워크플로우 JSON
│   └── app_config.json        # 설정 파일 (자동 생성)
├── output/                    # 생성된 이미지 저장 (자동 생성)
└── .venv/                     # 가상환경 (gitignore)
```

---

## 문제 해결

### ComfyUI 연결 실패
- ComfyUI가 `--listen --port 8188`로 실행 중인지 확인
- 방화벽에서 8188 포트 허용
- `http://localhost:8188` 브라우저 접속 테스트

### LM Studio 연결 실패
- Local Server가 시작됨(초록불)인지 확인
- 포트 1234 충돌 없는지 확인 (다른 앱 사용 중이면 설정에서 변경)
- 방화벽에서 1234 포트 허용

### "로드된 모델 없음"
- ComfyUI 웹 UI에서 모델이 실제로 로드되어 있는지 확인
- 모델 폴더 경로가 정확한지 설정에서 확인 (`checkpoints` 또는 `unet` 폴더 존재)
- 프로그램 재시작 후 모델 새로고침

### FaceDetailer 작동 안 함
- Impact Pack 설치 후 ComfyUI **완전 재시작**했는지 확인
- SAM/YOLO 모델이 올바른 경로에 있는지 확인
- ComfyUI 콘솔 로그에 에러 메시지 확인

### VRAM 부족 (Out of Memory)
- GGUF 양자화 모델 사용 (Q4_K_S)
- 해상도 낮추기 (512×512 시작)
- Steps 줄이기 (15~20)
- FaceDetailer 끄기
- ComfyUI 실행 시 `--force-fp16` 옵션 추가

---

## 프로그램 삭제 및 초기화

### 설정 리셋 (화면이 꼬였을 때)
```
프로젝트 폴더/workflows/ 폴더에서 다음 파일 삭제 후 재실행:
- app_config.json
- prompt.json
```

### 완전 삭제
```
프로젝트 폴더/.venv/ 폴더 통째로 삭제
→ 파이썬 패키지 모두 깔끔하게 제거됨
```

---

## 다음 단계

- [시작하기](01_getting_started.html) - 빠른 시작 가이드
- [LM Studio 연동](09_lmstudio.html) - 언어 모델 서버 상세
- [자주 묻는 질문](10_faq.html) - 트러블슈팅 모음