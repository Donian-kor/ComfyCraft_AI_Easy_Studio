# 설치 및 환경 설정 가이드 v0.3

## 📋 사전 요구사항

### 필수 소프트웨어

1. **Python 3.10 이상**
   ```powershell
   # 버전 확인
   python --version
   ```

2. **LM Studio** (로컬 서버 모드)
   - 다운로드: https://lmstudio.ai
   - 설치 후 모델 로드 필요
   - 기본 포트: 1234

3. **ComfyUI** (웹 서버 모드)
   - 다운로드: https://github.com/comfyanonymous/ComfyUI
   - 설치 후 가동 필요
   - 기본 포트: 8188

### 선택 사항

- **GPU**: NVIDIA (CUDA), AMD (ROCm), Apple Silicon (Metal)
- **RAM**: 8GB 이상 (16GB 권장)

## 🔧 설치 단계

### Step 1: 프로젝트 다운로드

```bash
# Git 사용
git clone <repository-url>
cd comfyui_Lmstudio_gui

# 또는 ZIP 파일 직접 다운로드
# 압축 해제 후 폴더로 이동
```

### Step 2: 가상 환경 생성 (권장)

```powershell
# Python 가상 환경 생성
python -m venv .venv

# 가상 환경 활성화
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat

# macOS/Linux
source .venv/bin/activate
```

**가상 환경의 장점**:
- 패키지 충돌 방지
- 프로젝트별 독립적인 환경
- 쉬운 삭제 (폴더 삭제만으로 제거)

### Step 3: 의존성 설치

```bash
# 현재 폴더에서 실행 (가상 환경 활성화 상태)
pip install -r comfyui_lmstudio_requirements.txt

# 또는 개별 설치
pip install PySide6>=6.4
pip install requests>=2.28
pip install websocket-client>=1.0
pip install urllib3>=2.0
pip install markdown>=3.5  # v0.3: 도움말 탭 마크다운 렌더링용
```

**설치 확인**:
```bash
# 각 패키지 버전 확인
pip show PySide6 requests websocket-client urllib3 markdown
```

### Step 4: 외부 서비스 준비

#### LM Studio 설정

1. LM Studio 실행
2. 왼쪽 메뉴에서 모델 선택
3. 모델 로드 (크기에 따라 1-5분 소요)
4. 서버 탭 (서버 아이콘) 선택
5. 기본 포트 1234에서 서버 시작

**확인 방법**:
```powershell
# LM Studio 서버 상태 확인
Invoke-WebRequest http://127.0.0.1:1234/v1/models -TimeoutSec 5
```

#### ComfyUI 설정

1. ComfyUI 실행
2. 웹 인터페이스에서 모델 로드
3. 서버가 포트 8188에서 자동으로 실행됨

**확인 방법**:
```powershell
# ComfyUI 서버 상태 확인
Invoke-WebRequest http://127.0.0.1:8188/system_stats -TimeoutSec 5
```

### Step 5: 애플리케이션 실행

```bash
# 가상 환경에서 실행
python main.py
```

**UI가 표시되면 설치 완료!**

## 🎯 초기 설정

### 애플리케이션 시작 후

1. **서버 연결 확인**
   - LM Studio 연결 확인 버튼 클릭
   - ComfyUI 연결 확인 버튼 클릭
   - 모두 "연결 성공" 상태 확인

2. **모델 선택**
   - LM Studio 모델 선택 (프롬프트 개선용)
   - ComfyUI 모델 선택 (이미지 생성용)
   - 자동으로 권장 설정 적용됨

3. **설정 저장**
   - "설정 저장" 버튼으로 현재 설정 저장
   - 다음 실행 시 동일 설정으로 시작

### 설정 파일 위치

```
프로젝트 폴더/
└── workflows/
    ├── app_config.json  ← 사용자 설정 (URL, 모델, 생성 파라미터 등)
    └── prompt.json      ← 시스템 프롬프트
```

**수동 편집 방법 (app_config.json)**:
```json
{
  "lmstudio": {
    "url": "http://127.0.0.1:1234",
    "model": "qwen2.5-7b-instruct"
  },
  "comfyui": {
    "url": "http://127.0.0.1:8188",
    "model": "flux1-dev.safetensors"
  },
  "prompts": {
    "use_korean_prompt": true
  }
}
```

**시스템 프롬프트 편집 (prompt.json)**:
```json
{
  "system_prompt_en": "You are a master AI Image Prompt Engineer...",
  "system_prompt_kr": "당신은 세계 최고 수준의 AI 이미지 프롬프트 엔지니어...",
  "negative_default": "worst quality, low quality, blurry..."
}
```

> **v0.3 변경사항**: 시스템 프롬프트가 `prompt.json`으로 분리되었습니다. 앱 재시작 없이 프롬프트 수정 가능합니다.

## 🐛 트러블슈팅

### 설치 오류

#### 문제: "Python을 찾을 수 없습니다"

**원인**: Python이 PATH에 등록되지 않음

**해결**:
```powershell
# 직접 경로로 실행
C:\Python310\python.exe -m venv .venv
```

#### 문제: "pip: 명령을 찾을 수 없음"

**원인**: Python 설치 시 pip 미포함

**해결**:
```powershell
python -m ensurepip --upgrade
pip install -r comfyui_lmstudio_requirements.txt
```

#### 문제: PySide6 설치 실패

**원인**: 호환되지 않는 Python 버전

**해결**:
```powershell
# Python 3.10+ 필요
python --version

# 필요한 경우 재설치
pip uninstall PySide6
pip install PySide6>=6.4
```

#### 문제: markdown 패키지 설치 실패 (v0.3)

**원인**: 도움말 탭 마크다운 렌더링용 패키지 누락

**해결**:
```powershell
pip install markdown>=3.5
```

### 런타임 오류

#### 문제: "연결 실패" 메시지

**원인 1**: 서버가 실행 중이 아님

**해결**:
```powershell
# LM Studio 확인
Test-NetConnection -ComputerName 127.0.0.1 -Port 1234

# ComfyUI 확인
Test-NetConnection -ComputerName 127.0.0.1 -Port 8188

# 서버 재시작
```

**원인 2**: 방화벽이 차단

**해결**:
```powershell
# Windows Defender 방화벽에서 Python 허용
# 또는 다른 방화벽 설정 확인
```

**원인 3**: 포트 변경됨

**해결**:
```bash
# app_config.json에서 URL 수정
{
  "lmstudio": {
    "url": "http://127.0.0.1:8000"  # 변경된 포트로 수정
  }
}
```

> **v0.3 변경사항**: LAN 스캔 기능이 제거되었습니다. 입력된 URL만 검증하므로, 정확한 URL을 입력해야 합니다.

#### 문제: "로드된 모델 없음" 표시

**원인 1**: 서버에 모델이 로드되지 않음

**해결**:
- LM Studio에서 모델 로드 확인
- ComfyUI에서 모델 폴더 설정 확인

**원인 2**: 네트워크 연결 문제

**해결**:
```powershell
# 직접 API 테스트
Invoke-WebRequest http://127.0.0.1:1234/v1/models
Invoke-WebRequest http://127.0.0.1:8188/system_stats
```

#### 문제: "이미지 생성 시간 초과"

**원인 1**: GPU 메모리 부족

**해결**:
- 해상도 감소
- 스텝 수 감소
- 다른 애플리케이션 종료

**원인 2**: 타임아웃 설정이 너무 짧음

**해결**:
```json
// app_config.json에서 수정
{
  "comfyui": {
    "max_wait_seconds": 1200  // 기본 600 → 1200으로 증가
  }
}
```

#### 문제: 프롬프트 향상 실패 (v0.3 신규)

**원인 1**: LM Studio 모델이 로드되지 않음

**해결**:
- LM Studio에서 모델 로드 확인
- "로드된 모델 없음"이면 모델 선택 후 재시도

**원인 2**: LM Studio 연결 안 됨

**해결**:
- "LM Studio 연결 확인" 버튼으로 연결 상태 확인
- 연결 실패 시 URL 확인 후 재시도

**원인 3**: 시스템 프롬프트 파일 없음

**해결**:
- `workflows/prompt.json` 파일 존재 확인
- 없으면 기본값 사용 (앱 내장 폴백)

### 성능 최적화

#### 느린 모델 로딩

**원인**: 로컬 파일 스캔 느림

**해결**:
```json
// app_config.json에서 모델 경로 직접 지정
{
  "comfyui_model_paths": [
    "C:/ComfyUI/models"
  ]
}
```

#### 높은 CPU 사용률

**원인**: 빈번한 모델 목록 갱신

**해결**:
```json
// app_config.json에서 캐시 TTL 증가
{
  "cache": {
    "model_cache_ttl_seconds": 600  // 300 → 600으로 증가
  }
}
```

> **v0.3 변경사항**: 캐시 키 정규화로 127.0.0.1 ↔ localhost 통일, 캐시 미스 방지

## 📊 시스템 권장사항

### 최소 사양
- **CPU**: Intel Core i5 / AMD Ryzen 5
- **RAM**: 8GB
- **GPU**: NVIDIA GTX 1060 / AMD RX 580
- **저장공간**: 50GB (모델 포함)

### 권장 사양
- **CPU**: Intel Core i7 / AMD Ryzen 7
- **RAM**: 16GB 이상
- **GPU**: NVIDIA RTX 3070 / AMD RX 6800 이상
- **저장공간**: 100GB 이상

### 고성능 사양
- **CPU**: Intel i9 / AMD Ryzen 9
- **RAM**: 32GB 이상
- **GPU**: NVIDIA RTX 4090 / multiple GPUs
- **저장공간**: 500GB 이상 (SSD)

## 🆕 v0.3 신규 기능

| 기능 | 설명 |
|------|------|
| **프롬프트 향상 전용 버튼** | 이미지 생성 없이 프롬프트만 개선 가능 (✨ 버튼) |
| **도움말 탭 내장** | README.md, INSTALLATION.md를 앱 내에서 바로 확인 |
| **연결 주소 자동 해석** | 입력된 URL만 검증, 불필요한 LAN 스캔 제거로 빠른 연결 |
| **프롬프트 설정 외부화** | prompt.json에서 시스템 프롬프트 관리 (단일 진실 공급원) |
| **경과 시간 표시** | 생성 소요 시간 실시간 측정 (분:초 형식) |
| **로그 토글 제거** | 깔끔한 UI를 위해 로그 영역 항상 표시 |
| **캐시 키 정규화** | 127.0.0.1 ↔ localhost 통일로 캐시 미스 방지 |
| **PromptEnhanceWorker 완성** | 비동기 프롬프트 향상, 디버그 시그널, 에러 핸들링 |

## 🔄 업데이트

### 애플리케이션 업데이트

```bash
# 최신 코드 다운로드
git pull origin main

# 새로운 의존성 설치
pip install -r comfyui_lmstudio_requirements.txt --upgrade
```

### 의존성 업데이트

```bash
# 개별 패키지 업데이트
pip install --upgrade PySide6 requests websocket-client markdown

# 모든 패키지 업데이트
pip install -r comfyui_lmstudio_requirements.txt --upgrade
```

## 🗑️ 제거 및 정리

### 애플리케이션 제거

```bash
# 가상 환경 비활성화
deactivate

# 가상 환경 폴더 삭제 (완전 제거)
rmdir /s .venv
```

### 캐시 및 설정 초기화

```powershell
# 설정 파일 삭제 (초기 상태로 리셋)
Remove-Item workflows\app_config.json

# 프롬프트 설정 삭제 (초기 상태로 리셋)
Remove-Item workflows\prompt.json

# 출력 폴더 비우기
Remove-Item outputs\* -Recurse
```

## ✅ 설치 검증

설치가 정상적으로 완료되었는지 확인하려면:

```bash
# 1. Python 버전 확인
python --version
# 출력: Python 3.10.x 이상

# 2. 의존성 확인
pip list | findstr PySide6
# 출력: PySide6 6.x.x 이상

# 3. 애플리케이션 실행
python main.py
# 출력: GUI 창이 표시되어야 함

# 4. 서버 연결 확인
# 애플리케이션에서 "연결 확인" 버튼으로 확인

# 5. v0.3 신규 기능 확인
# - 도움말 탭에서 README/INSTALLATION 표시
# - ✨ 프롬프트 향상 버튼 동작
# - 경과 시간 표시 동작
```

## 📚 추가 리소스

### 공식 문서
- [PySide6 공식 문서](https://doc.qt.io/qtforpython/)
- [requests 문서](https://docs.python-requests.org/)
- [WebSocket-client 문서](https://github.com/websocket-client/websocket-client)
- [markdown 문서](https://python-markdown.github.io/)

### 커뮤니티
- [ComfyUI Discord](https://discord.gg/comfyui)
- [LM Studio Community](https://lmstudio.ai/community)

---

**마지막 업데이트**: 2026-09-03
