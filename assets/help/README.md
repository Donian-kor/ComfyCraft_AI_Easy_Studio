# ComfyCraft AI Easy Studio (v4.4 통합기획 기준)

**버전**: v4.4 (통합기획서 v4.4 반영, 커밋 기준: `49d23df`, 2026-09-29 기준)

## 📊 프로젝트 통계 (2026-09-29 기준)

| 항목 | 내용 |
|---|---|
| Python 파일 | **57개** (`.kilo/worktrees/` 사본 제외, `__init__.py` 및 `tests/` 포함) |
| 총 라인 | **18,326줄** |
| 테스트 | **6개 파일** (conftest.py 포함) / 70 passed (8.62s) ✅ |
| 커밋 상태 | clean, `main` 브랜치 |
| 런타임 의존성 | `requests`, `websocket-client`, `PySide6`, `markdown` |
| 린터 도구 | **미설치** (ruff / flake8 / pylint / mypy 전부 없음) |

> **재검증 결과**: PowerShell의 `Get-Content | Measure-Object -Line`가 CRLF 줄 끝 표시가 있는 파일의 라인 수를 부정확하게 셌습니다. Python 기준으로 재측정한 모든 라인 수는 아래 표와 별도의 **정확한 값**으로 교체되었습니다. PowerShell 원본 값은 ~~취소선~~으로 표시했습니다.

LM Studio의 프롬프트 확장 능력과 ComfyUI의 이미지 생성 기술을 하나로 합친 **통합 이미지 생성 프로그램**입니다. 단일 이미지 생성뿐만 아니라 **4컷 만화 자동 생성(스토리→컷별 생성→대사 합성→2x2 합성)**을 지원합니다.

---

## 📌 0. 주요 기능 요약 (v4.4 기준)

- **단일 이미지 생성**: 프롬프트 입력 → LM Studio 확장 → ComfyUI 생성 → 채팅 말풍선 표시
- **4컷 만화 생성 (신규)**: 아이디어 입력 → 4컷 스토리 자동 구성 → 컷별 이미지 순차 생성 → YOLO 말풍선 감지 + Stage2 대사 합성 → 2x2 합성본 완성
- **컷 재생성**: 완성된 4컷 중 원하는 컷만 재생성 → 합성 자동 재수행
- **세션 관리**: 채팅·이미지·만화 데이터 통합 저장·복원 (`session.json` 단일 파일)
- **실시간 진행 표시**: 생성 카드(프롬프트→진행중→완료) 모핑 전환, 정지 버튼으로 즉시 중단 가능
- **설정 패널 (420px)**: 생성 옵션·모델 상세·해상도·샘플링·네거티브·FaceDetailer 15개 슬라이더 3열 1행 배치

### v4.4 변경점 (통합기획서 반영)
- **B안 확정**: YOLO 말풍선 감지(`bubble_detector.py`) + 2단계 Stage2 워크플로우를 **필수**로 격상. PIL 고정위치 폴백은 실패 안전망으로 유지.
- **테스트 전략 변경**: 기존 `tests/` 6개 파일(70 passed)은 `.gitignore`에 가려 git 추적에서 제외된 상태. 각 페이즈(A1~A6)마다 전용 신규 테스트 작성 필요.
- **페이즈 구성**: A1(프롬프트 덮어쓰기 수정) → A2(스토리/모델 이식) → A3(합성/YOLO/Stage2 이식 + 선행 5항목) → A4(컷 루프/컨트롤러 접합 3개) → A5(세션 comic 블록/컷 보기/재생성) → A6(UI 배선/수동 확인)

---

## ⚙️ 1. 프로그램 사용 및 설치법

### 시스템 권장 사양

|     구분      | CPU           | RAM        | GPU (그래픽)  | 여유 용량         |
| :-----------: | :------------ | :--------- | :------------ | :---------------- |
| **최소 사양** | Intel i5 이상 | 16 GB      | RTX 3060 12GB | 100 GB 이상       |
| **권장 사양** | Intel i7 이상 | 32 GB      | RTX 4070 16GB | 200 GB 이상 (SSD) |
|  **고성능**   | Intel i9 이상 | 64 GB 이상 | RTX 4090 24GB | 500 GB 이상 (SSD) |

> **4컷 만화·YOLO·Stage2 사용 시 참고**: 
> - 만화 생성은 컷당 ComfyUI 왕복 2회(이미지 생성 + 대사 합성) → 4컷 = 총 8회 실행. 시간·VRAM·취소 지점 2배 증가.
> - YOLO(`ultralytics`) + 모델 파일 `comic-speech-bubble-detector.pt` 별도 필요.
> - Stage2 워크플로우 JSON(`4cut_default_stage2.json` 계열) ComfyUI 측에 별도 필요.
> - VRAM 12GB 미만에서는 512×512 이하 해상도 권장.

### 프로그램 다운로드 및 설치 (권장 방식)

```bash
# 1. 프로그램 폴더 다운로드 및 이동
git clone <repository-url>
cd ComfyCraft_AI_Easy_Studio

# 2. 파이썬 가상 환경 만들기 및 켜기 (패키지 꼬임 방지)
python -m venv .venv
.venv\Scripts\Activate.ps1     # Windows PowerShell 기준

# 3. 필요한 파이썬 패키지 설치
# requirements.txt: requests, websocket-client, PySide6, markdown, Pillow>=10.0,<13, ultralytics
pip install -r requirements.txt

# 4. (B안) YOLO 말풍선 감지 모델 별도 배치
# models/ultralytics/comic-speech-bubble-detector.pt 위치에 모델 파일 위치
# config/paths.json 또는 환경변수 COMFY_BUBBLE_MODEL_PATH로 경로 지정
```

### 프로그램 실행 및 기본 사용 흐름

가상 환경이 켜진 상태에서:

```bash
python main.py
```

1. **연결 확인**: 상단 배지 `LM Studio 연결됨` / `ComfyUI 연결됨` 파란불 확인
2. **모드 선택**: 입력줄 좌측 피커에서 `단일 이미지` ↔ `만화 4컷` 토글
3. **모델 선택**: 옵션 패널(사이드바 `옵션` 버튼)에서 생성 모델(Flux/ZImage/애니/ERNIE) 및 상세 설정
4. **프롬프트/아이디어 입력**:
   - 단일: "예쁜 고양이" → `✨ 프롬프트 향상` → `➤ 생성 시작`
   - 만화: "강아지가 비 오는 골목에서 고양이를 구하는 4컷 만화 만들어줘" → `➤ 생성 시작` (자동: 스토리 구성 → 4컷 순차 생성 → 대사 합성 → 2x2 합성)
5. **결과 확인**: 채팅 말풍선에 이미지 카드 표시. 만화는 `컷 보기` 토글로 4컷 개별 확인 가능
6. **재생성/저장/복사**: 컷별 `[↻ 다시 만들기]`, 합성본 `[저장]`/`[복사]`, `[전체 다시 만들기]`

---

## 🎨 2. ComfyUI 필수 설치 노드 및 워크플로우

본 프로그램과 연동되려면 ComfyUI가 기본 웹 서버 모드(포트 8188)로 켜져 있어야 합니다.

### 공통 필수 노드
- **ComfyUI-Impact-Pack** (ltdrdata) — FaceDetailer 등 고급 노드 뼈대
- **ComfyUI-Inspire-Pack** (ltdrdata) — 마스크·이미지 유틸리티

### 단일 이미지 생성용 (기존)
- 기본 워크플로우 3베이스: `checkpoint` / `unet_clip` / `unet_dual_clip` + 파생 5종(자동 파생)

### 4컷 만화 생성용 (B안 필수 추가)
1. **YOLO 말풍선 감지 모델**
   - `models/ultralytics/comic-speech-bubble-detector.pt` 배치
   - 경로: `config/paths.json` → `"bubble_model_path"` 또는 환경변수 `COMFY_BUBBLE_MODEL_PATH`

2. **Stage2 대사 합성 워크플로우**
   - `workflows/4cut_default_stage2.json` (또는 베이스명 `_stage2.json` 규칙) ComfyUI `workflows/` 폴더에 배치
   - 노드 구성: `ImageScale` → `DrawText`(말풍선) → `ImageComposite` → `SaveImage`
   - 프로그램은 `GenerationWorker` 내부에서 `prepare_stage2` → `queue_prompt` → `wait_for_image` 순서로 실행

3. **기본 폰트** (Windows 기본 `malgun.ttf` 사용, 없으면 Noto Sans CJK 폴백)

---

## 💬 3. LM Studio 설치 및 사용 방법

프롬프트를 똑똑하게 확장해주는 역할을 합니다 (단일/만화 공통).

1. **다운로드 및 설치**: [LM Studio 공식 홈페이지](https://lmstudio.ai/)에서 다운로드 후 설치
2. **모델 로드**: 좌측 돋보기 메뉴에서 언어 모델(예: `qwen2.5-7b-instruct`, `gemma-2-9b-it` 등) 검색·다운로드 후 상단 탭에서 Load
3. **로컬 서버 켜기**:
   - 좌측 메뉴 **↔ (Local Server)** 아이콘 클릭
   - 포트 `1234` 확인 (프로그램 기본값)
   - 초록색 `Start Server` 버튼 클릭
4. **만화용 시스템 프롬프트**: 프로그램 내부에 4컷 JSON 스키마 강제 프롬프트 내장 (`story_service.py` 참조). 별도 설정 불필요.

---

## 🛠️ 4. 자주 묻는 질문 및 에러 해결법

### 1) 설치 및 실행 에러

| 증상 | 원인/해결 |
|---|---|
| **"Python/pip를 찾을 수 없음"** | Python 3.10+ 설치 시 `Add to PATH` 체크 필요 |
| **"PySide6 설치 실패"** | Python 3.10+ 필수. `pip install --upgrade pip` 후 재시도 |
| **"Pillow/ultralytics 설치 실패"** | `pip install --upgrade pip setuptools wheel` 후 `pip install -r requirements.txt` |
| **YOLO 모델 파일 없음 경고** | `config/paths.json`에 `"bubble_model_path"` 지정 또는 `COMFY_BUBBLE_MODEL_PATH` 환경변수 설정 |

### 2) 연결 및 작동 에러

| 증상 | 원인/해결 |
|---|---|
| **"연결 실패" 팝업** | LM Studio(1234)·ComfyUI(8188) 둘 다 실행 중인지, 방화벽 허용 확인 |
| **"로드된 모델 없음"** | LM Studio 상단에서 모델 Load 완료했는지 확인 |
| **만화 생성 중 멈춤/타임아웃** | VRAM 부족 → 해상도 512×512 이하, Steps 20 이하로 낮춤. 취소 버튼(■)로 즉시 중단 가능 |
| **대사 합성 실패(`failed`)** | Stage2 워크플로우 JSON 누락 → `workflows/4cut_default_stage2.json` 확인. 자동으로 PIL 폴백(`fallback`)으로 대체됨 |
| **정지 버튼이 안 먹힘 (만화 중)** | v4.4 D1 수정 필요: 컨트롤러 `stop_generation()`에 `_comic_runner.cancel()` 분기 추가 확인 |

### 3) 프로그램 삭제 및 초기화 방법

- **설정 리셋** (화면이 꼬였을 때): `workflows/app_config.json`, `workflows/app_config.json.bak` 삭제 후 재시작
- **앱 완전 삭제**: `.venv` 폴더 통째 삭제 → Python 패키지 모두 제거
- **세션 데이터만 삭제**: `.sessions/` 폴더 삭제 (이미지 파일은 `outputs/`에 별도 보존됨)

---

## 📚 5. 개발자 참고 (통합기획서 v4.4 연계)

| 문서 | 위치 | 용도 |
|---|---|---|
| **통합기획서 v4.4** | `통합기획서.html` | 전체 페이즈·게이트·금지·리스크·스키마·목업 정의 |
| **UI/UX 기획 v5.1** | `uiux디자인기획.html` | 3층 레이아웃·사이드바 5버튼·420px 패널·옵션 3열 규칙 |
| **전수분석서** | `두프로젝트_코드_기능_UI_전수분석서.html` | 원자료(코드·UI·테스트 교차 분석) — 참고용, 계획 판단은 통합기획서 우선 |
| **4cut 원본** | `C:\Users\donian\Desktop\python\4cut_LocalComic_Studio` | 이식 대상 5모듈 + Stage2/YOLO 3모듈 + 테스트 9종 |

### 페이즈별 게이트 요약 (v4.4)

| 페이즈 | 핵심 작업 | 게이트 (신규 테스트 필수) |
|---|---|---|
| **A1** | `generation.py:191-195` `prompt_override` 분기 1줄 | 단일 이미지 수동 확인 + 프롬프트 오버라이드 테스트 1건 통과 |
| **A2** | `app/comic/models.py`, `story.py` 이식 (import만 변경) | `master_seed` 동일성·캐릭터/스타일 고정 테스트 통과 + `import app.comic.story` |
| **A3** | 합성·YOLO·Stage2 이식 + **선행 ①~⑤ 완료 필수** | `make_2x2`/`wrap_text`/대사상태전이 테스트 3종 통과 + `composited`/`fallback` 수동 확인 |
| **A4** | `ComicRunner` + `ComicSignals` + 컨트롤러 3개 수정 | 컷 1→4 순차·시드 동일·정지버튼 실제 중단·취소 시 완료컷 보존·단일 이미지 회귀 |
| **A5** | `session["comic"]` 저장·복원 + `ImageCard` 컷보기/재생성 | comic 왕복 + `test_chat_models` 확장 통과 + 재생성 시 타 컷 해시 불변 |
| **A6** | `main.ui` 만화 토글 버튼 + 전송 분기 | ON: 4컷→합성→컷보기→재생성 / OFF: 단일 정상 / 정지즉시중단 / 세션 복원 |

---

> **주의**: 이 README는 통합기획서 v4.4 기준으로 작성되었습니다. 실제 구현 진행 중 세부 사항(파일 경로, 설정 키, 워크플로우 노드명 등)은 통합기획서와 코드를 기준으로 정합성을 맞춰 주세요. **테스트 파일은 `.gitignore`으로 인해 버전 관리 대상이 아니므로, 중요한 변경 전후에 반드시 테스트를 실행하여 검증하세요.**