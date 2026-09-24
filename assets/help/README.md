# ComfyCraft AI Easy Studio (v0.3.0-dev)

**버전**: v0.3.0-dev (커밋 기준: `0648039`, 2026-09-19 기준)

LM Studio의 똑똑한 프롬프트 작성 능력과 ComfyUI의 강력한 이미지 생성 기술을 하나로 합친 **통합 이미지 생성 프로그램**입니다. 파이썬이나 복잡한 노드 연결을 몰라도 누구나 쉽게 고품질 이미지를 생성할 수 있습니다.

---

## 📌 0. 업데이트 내역

이번 v0.3 버전에서 새롭게 추가되거나 개선된 핵심 기능들입니다.

- **강력한 얼굴 보정 (FaceDetailer)**: 체크박스 하나로 얼굴 영역만 자동 인식해 픽셀 단위로 선명하게 다듬어 줍니다.
- **실시간 기록 복원 (히스토리)**: 방금 만든 이미지 4장이 우측 썸네일로 자동 저장됩니다. 클릭 한 번이면 당시 사용했던 프롬프트, 시드, 얼굴 보정 설정까지 똑같이 복원됩니다.
- **초보자 맞춤 자동화**: 복잡한 노드 연결 없이 사용할 모델(Flux, ZImage 등)만 고르면 최적의 세팅이 자동으로 적용됩니다.
- **시드 고정 및 고급 설정**: 동일한 얼굴이나 구도를 유지하고 싶을 때 '시드 고정' 기능을 제공하며, 전문가용 샘플러와 스텝 수 조절 패널이 깔끔하게 숨겨져 있습니다.
- **클립보드 연동**: 생성된 영문 프롬프트나 완성된 이미지를 버튼 하나로 복사해 다른 곳에 바로 붙여넣을 수 있습니다.

### v0.3.0-dev (커밋 `0648039`, 2026-09-19)

> Git 태그가 존재하지 않아 커밋 해시를 기준으로 버전을 기록합니다.
>
> - **생성 파이프라인 안정성 강화**: 이미지 생성 파이프라인의 신뢰성 및 안정성을 향상시켰습니다.
> - **환경 설정 업데이트**: 설정 파일 및 환경 구성을 최신 상태로 정리했습니다.

---

## ⚙️ 1. 프로그램 사용 및 설치법

### 시스템 권장 사양

|     구분      | CPU           | RAM        | GPU (그래픽)  | 여유 용량         |
| :-----------: | :------------ | :--------- | :------------ | :---------------- |
| **최소 사양** | Intel i5 이상 | 8 GB       | GTX 1060 이상 | 50 GB 이상        |
| **권장 사양** | Intel i7 이상 | 16 GB      | RTX 3070 이상 | 100 GB 이상       |
|  **고성능**   | Intel i9 이상 | 32 GB 이상 | RTX 4090 이상 | 500 GB 이상 (SSD) |

> **얼굴 보정(FaceDetailer) 사용 시 참고**: 얼굴 보정 기능을 위해선 ComfyUI에 `Impact Pack`, `SAM 모델`, `YOLO 모델`을 별도로 설치해야 하며, 이는 GPU 메모리(VRAM) 사용량을 추가로 약 1~2GB 정도 더 요구할 수 있습니다. VRAM이 부족한 경우 최소 사양의 1단계 이상 여유 있는 사양을 권장합니다.

### 프로그램 다운로드 및 설치 (권장 방식)

명령 프롬프트(CMD)나 PowerShell을 열고 아래 명령어를 순서대로 입력하세요.

```bash
# 1. 프로그램 폴더 다운로드 및 이동
git clone <repository-url>
cd comfyui_Lmstudio_gui

# 2. 파이썬 가상 환경 만들기 및 켜기 (패키지 꼬임 방지)
python -m venv .venv
.venv\Scripts\Activate.ps1     # Windows PowerShell 기준 (실행 정책 문제 시: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force)

# 3. 필요한 파이썬 패키지 설치 (requirements.txt에 명시된 패키지: requests, websocket-client, PySide6, markdown)
pip install -r requirements.txt
```

### 프로그램 실행 및 기본 사용 흐름

가상 환경이 켜진 상태에서 아래 명령어로 프로그램을 실행합니다.

```bash
python main.py
```

1. **연결 확인**: 앱 상단의 `LM Studio 연결 확인`, `ComfyUI 연결 확인` 버튼을 눌러 두 서버가 잘 연결되었는지 파란불을 확인합니다.
2. **모델 선택**: 사용할 프롬프트 언어 모델과 그림용 ComfyUI 모델을 고릅니다.
3. **프롬프트 입력**: "예쁜 고양이" 처럼 간단히 적고 `✨ 프롬프트 향상` 버튼을 누르면 AI가 상세하게 영어로 번역/확장해 줍니다.
4. **생성하기**: 초록색 `생성 시작` 버튼을 눌러 이미지를 완성합니다!

---

## 🎨 2. ComfyUI 필수 설치 노드 및 페이스 디테일러 설치 방법

본 프로그램과 완벽하게 연동되려면 ComfyUI가 기본 웹 서버 모드(포트 8188)로 켜져 있어야 하며, 특히 **얼굴 보정(FaceDetailer)** 기능을 쓰기 위해서는 ComfyUI 웹 화면(Manager)에서 아래 3가지를 반드시 설치해야 합니다.

1. **Impact Pack (보정 필수 뼈대)**
   - ComfyUI Manager -> `Install Custom Nodes` 이동
   - 검색창에 `Impact Pack` 검색 후 `ComfyUI-Impact-Pack` (작성자: ltdrdata) 설치
   - 설치 후 ComfyUI 서버를 완전히 껐다가 다시 켜주세요.
   - ComfyUI Manager -> `Install Custom Nodes` 이동
   - 검색창에 `Impact Pack` 검색 후 `ComfyUI-Impact-Pack` (작성자: ltdrdata) 설치
   - 설치 후 ComfyUI 서버를 완전히 껐다가 다시 켜주세요.
2. **SAM 모델 (정밀 마스크용)**
   - ComfyUI Manager -> `Install Models` 이동
   - 검색창에 `sam_vit_b` 검색 후 `sam_vit_b_01ec64.pth` 찾아서 설치
   - 정상 설치 시 `ComfyUI/models/sams` 폴더에 파일이 저장됩니다.
   - ComfyUI Manager -> `Install Models` 이동
   - 검색창에 `sam_vit_b` 검색 후 `sam_vit_b_01ec64.pth` 찾아서 설치
   - 정상 설치 시 `ComfyUI/models/sams` 폴더에 파일이 저장됩니다.
3. **YOLO 모델 (안면 감지용)**
   - ComfyUI Manager -> `Install Models` 이동
   - 검색창에 `face_yolov8m` 검색 후 `bbox/face_yolov8m.pt` 모델 설치
   - ComfyUI Manager -> `Install Models` 이동
   - 검색창에 `face_yolov8m` 검색 후 `bbox/face_yolov8m.pt` 모델 설치

---

## 💬 3. LM Studio 설치 및 사용 방법

프롬프트를 똑똑하게 확장해주는 역할을 합니다.

1. **다운로드 및 설치**: [LM Studio 공식 홈페이지](https://lmstudio.ai/)에서 다운로드 후 설치합니다.
2. **모델 로드**: 프로그램 좌측 돋보기 메뉴에서 사용할 언어 모델(예: qwen 등)을 검색해 다운로드한 뒤, 상단 탭에서 모델을 불러옵니다(Load).
3. **로컬 서버 켜기**:
   - 좌측 메뉴 중 **↔ (Local Server)** 모양 아이콘 클릭
   - 포트가 `1234`로 설정되어 있는지 확인
   - 초록색 `Start Server` 버튼을 눌러 서버를 켭니다.

---

## 🛠️ 4. 자주 묻는 질문 및 에러 해결법

### 1) 설치 및 실행 에러

- **"Python/pip를 찾을 수 없음"**
  - 파이썬(3.10 이상)이 윈도우에 깔려 있는지, 설치 시 'Add to PATH' 옵션을 체크했는지 확인하세요.
- **"PySide6 설치 실패"**
  - 파이썬 버전이 너무 낮으면 설치되지 않습니다. 3.10 이상으로 업데이트해 주세요.

### 2) 연결 및 작동 에러

- **"연결 실패" 팝업이 뜰 때**
  - LM Studio(포트 1234)와 ComfyUI(포트 8188) 창이 실제로 켜져 있는지 확인하세요. 방화벽이 차단하고 있을 수도 있습니다.
- **"로드된 모델 없음" 이라고 뜰 때**
  - LM Studio 프로그램 내부에서 상단의 언어 모델이 제대로 불러와져 있는지 다시 한번 확인하세요.
- **멈춘 것처럼 보임 (이미지 생성 시간 초과)**
  - 컴퓨터 그래픽카드(VRAM) 사양 부족일 수 있습니다. 이미지 해상도(Width/Height)와 보정 Steps를 낮춰서 다시 시도해 보세요.

### 3) 프로그램 삭제 및 초기화 방법

- **설정 리셋하기 (화면이 꼬였을 때)**
  - 프로그램 안의 `workflows` 폴더로 들어가서 `app_config.json` 과 `prompt.json` 파일을 지우고 앱을 다시 켜세요. 새것으로 완전 초기화됩니다.
- **앱 완전 삭제**
  - 프로그램 폴더 안의 `.venv` 폴더를 통째로 지우시면 무겁게 깔려있던 파이썬 패키지들이 깔끔하게 모두 지워집니다.
