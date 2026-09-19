# 자주 묻는 질문 (FAQ)

## 설치 및 실행

### Q: "Python을 찾을 수 없습니다" / "pip 명령이 없습니다"
**A**: 파이썬이 설치되지 않았거나 PATH에 등록되지 않았습니다.
1. [python.org](https://python.org/)에서 Python 3.10+ 다운로드 설치
2. 설치 시 **"Add Python to PATH" 체크 필수**
3. 터미널 재시작 후 `python --version` 확인

### Q: "PySide6 설치 실패" / "Microsoft Visual C++ 필요"
**A**: 파이썬 버전이 낮거나 빌드 도구 부족.
- Python 3.10 이상 사용
- Windows: `Visual Studio Build Tools` 설치 또는 `pip install --upgrade pip setuptools wheel` 후 재시도

### Q: 가상환경 활성화 안 됨 (PowerShell 스크립트 오류)
**A**: PowerShell 실행 정책 제한.
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# 또는
.venv\Scripts\Activate.ps1 대신 .venv\Scripts\activate.bat 사용 (CMD)
```

---

## 연결 및 서버

### Q: "연결 실패" 팝업이 뜹니다
**A**: 다음 체크리스트 순서대로 확인:
1. **LM Studio**: Local Server 탭에서 초록불(시작됨) 인가?
2. **ComfyUI**: 터미널에서 `python main.py --listen --port 8188` 실행 중인가?
3. **포트**: 1234(LM), 8188(ComfyUI) 다른 프로그램에서 안 쓰는가?
4. **방화벽**: Windows 방화벽에서 Python/터미널 허용인가?
5. **주소**: 프로그램 설정에서 `http://localhost:1234`, `http://localhost:8188` 정확히 입력했는가?

### Q: "로드된 모델 없음" 이라고 뜹니다
**A**: 
- LM Studio: 모델이 Load 되어 있고 서버가 시작됐는지 확인
- ComfyUI: 웹 UI(http://localhost:8188)에서 모델이 로드되어 있는지 확인
- 프로그램에서 `모델 폴더 경로`가 정확한지 설정 확인 (`checkpoints` 폴더 존재해야 함)

### Q: ComfyUI 모델이 목록에 안 뜹니다
**A**:
1. 설정 대화상자에서 `모델 폴더` 경로 확인 (예: `C:\ComfyUI\models`)
2. 해당 폴더 하위에 `checkpoints` 또는 `unet` / `diffusion_models` 폴더 존재하는지 확인
3. 모델 파일(.safetensors, .gguf)이 해당 폴더에 있는지 확인
4. 프로그램 재시작 후 `모델 새로고침`

---

## 생성 및 품질

### Q: 생성이 너무 오래 걸립니다 / 멈춘 것 같습니다
**A**: 
- **VRAM 부족**: GPU 메모리 꽉 차서 스왑 발생 → 해상도↓, Steps↓, GGUF 모델 사용
- **첫 실행**: 모델 로딩 시간 포함됨 (두 번째부터 빠름)
- **FaceDetailer**: 켜져 있으면 2~5초 추가 소요
- **진행바 확인**: 0%에서 오래 머무르면 모델 로딩 중, 50% 이후면 생성 중

### Q: 얼굴이 이상하게 나옵니다 (기형, 비대칭, 다른 사람)
**A**:
1. **FaceDetailer ON** → 기본값으로 생성
2. 그래도 안 되면: `Denoise 0.25~0.30`, `CFG 3~4`로 낮춤
3. 여러 얼굴: `SAM Hint` → `horizontal-2` 또는 `rect-4` 변경
4. 프롬프트에 `perfect face, symmetrical face, detailed eyes` 추가

### Q: 손/발가락이 이상합니다
**A**: 현재 FaceDetailer는 **얼굴만** 보정합니다. 손/발은 모델 자체 능력에 의존.
- SDXL: `bad hands, missing fingers` 부정 프롬프트에 추가
- FLUX: 상대적으로 손 표현 우수
- 인페인팅/후보정 별도 필요

### Q: 같은 시드인데 결과가 다릅니다
**A**: 다음 설정 중 하나라도 다르면 결과 다름:
- 모델, 해상도, Steps, CFG, Sampler, Scheduler, Denoise
- FaceDetailer ON/OFF 또는 세부 설정
- 프롬프트(공백/줄바꿈 포함) 완전 동일해야 함
- **확인**: 히스토리 썸네일 클릭으로 설정 완전 복원 후 생성

### Q: 검은 화면/깨진 이미지가 나옵니다
**A**:
- VAE 누락: 모델에 맞는 VAE 파일 필요 (FLUX: `ae.safetensors`, SDXL: `sdxl_vae.safetensors`)
- 모델 파일 손상: 재다운로드
- ComfyUI 버전 구형: 최신 버전으로 업데이트

---

## FaceDetailer 전용

### Q: FaceDetailer 체크해도 변화가 없습니다
**A**:
1. ComfyUI에 **Impact Pack** 설치 후 **서버 완전 재시작** 했는가?
2. `sam_vit_b_01ec64.pth` (SAM), `face_yolov8m.pt` (YOLO) 모델 설치했는가?
3. ComfyUI 콘솔에 에러 로그 없는가?
4. 얼굴 크기가 너무 작지 않은가? (`Drop Size` 기본 10px, 더 작으면 `Guide Size` 올리기)

### Q: "SAM 모델이 없습니다" 경고
**A**: ComfyUI Manager → Install Models → `sam_vit_b` 검색 → `sam_vit_b_01ec64.pth` 설치
- 미설치 시 YOLO 박스 기준으로만 동작 (기본값으로도 보통 충분)

### Q: 보정이 너무 느립니다
**A**: 
- `Steps 15~20`으로 낮춤
- `Guide Size 256` 유지 (512로 올리면 4배 느려짐)
- 얼굴 1~2개만 있는 이미지에만 사용

---

## 성능 및 하드웨어

### Q: VRAM 8GB인데 FLUX 돌릴 수 있나요?
**A**: **GGUF 양자화 모델** 사용 시 가능.
- `flux1-dev-Q4_K_S.gguf` → 약 6~7GB VRAM 사용
- `flux1-schnell-Q4_K_S.gguf` → 더 빠름, 약 5~6GB
- 일반 `.safetensors`는 12GB+ 필요

### Q: CPU만으로 돌릴 수 있나요?
**A**: 가능하지만 **매우 느림** (이미지당 수 분~수십 분). GPU 필수 권장.

### Q: 맥(M1/M2/M3)에서 되나요?
**A**: 네. LM Studio Metal 지원, ComfyUI MPS 지원. 단, 일부 노드(CUDA 전용) 호환성 확인 필요.

---

## 설정 및 데이터

### Q: 설정을 초기화하고 싶습니다
**A**: `workflows/` 폴더에서 다음 파일 삭제 후 재실행:
- `app_config.json` (서버 주소, 모델 경로, 생성 설정 등)
- `prompt.json` (프롬프트 템플릿)

### Q: 생성된 이미지는 어디에 저장되나요?
**A**: 프로젝트 폴더 `output/` 하위 폴더에 날짜별 자동 저장.
- 파일명: `{모델명}_{시드}_{날짜시간}.png`
- `📁 출력 폴더 열기` 버튼으로 바로 접근 가능

### Q: 히스토리가 사라졌습니다
**A**: 프로그램 재시작 시 메모리 히스토리는 초기화됩니다. 중요 이미지는 `💾 이미지 저장` 또는 출력 폴더에서 파일로 보관하세요.

---

## 기타

### Q: 다국어 지원 되나요?
**A**: 현재 한국어 UI만 지원. 프롬프트 입력은 한국어 권장 (AI 마법사 최적화됨). 영문 직접 입력도 가능.

### Q: 배치 생성(여러 장 한 번에) 되나요?
**A**: 현재 단일 생성만 지원. 히스토리 썸네일 클릭 → 생성 반복으로 연속 생성 가능.

### Q: LoRA 사용하려면?
**A**: ComfyUI 웹 UI에서 워크플로우에 LoRA 노드 추가 후 모델로 저장 → 이 프로그램에서 해당 모델 선택. 또는 ComfyUI에서 직접 워크플로우 실행 권장.

### Q: 업데이트는 어떻게 하나요?
**A**: `git pull` 후 `pip install -r requirements.txt` 재실행. 설정 파일(`app_config.json`)은 유지됨.

---

## 여전히 해결 안 된다면?

1. **로그 창** 확인 (하단 로그 패널, `❓ 도움말` → 로그 복사)
2. **ComfyUI 콘솔** 에러 메시지 확인
3. **LM Studio 로그** 확인 (Local Server 탭 하단)
4. GitHub Issues에 로그 첨부해 문의

---

## 다음 단계

- [설치 및 필수 노드](08_installation.html) - 상세 설치 가이드
- [FaceDetailer 얼굴 보정](06_facedetailer.html) - 보정 상세 설정
- [단축키/팁](11_shortcuts.html) - 효율적인 작업 팁