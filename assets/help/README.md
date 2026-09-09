# ComfyUI + LM Studio 통합 이미지 생성 GUI v0.3

LM Studio의 강력한 LLM 프롬프트 엔지니어링 능력과 ComfyUI의 정교한 이미지 생성 파이프라인을 결합한 통합 GUI 도구입니다. v0.3에서는 전체 시스템의 모듈화 리팩토링을 통해 안정성과 확장성을 극대화하였습니다.

## 🚀 주요 특징 (v0.3 업데이트)

- **모듈형 파이프라인**: 연결부터 실행까지 5단계의 독립된 모듈 구조로 설계되어 유지보수와 기능 확장이 용이합니다.
- **지능형 모델 프로필**: 모델별(Flux, ZImage 등) 최적의 스케줄러, 우선순위, 파라미터를 자동으로 적용하는 프로필 시스템을 도입하였습니다.
- **UI/로직 완전 분리**: PySide6 기반의 UI 디자인과 기능 로직을 엄격히 분리하여, Qt Designer를 통한 UI 수정이 로직에 영향을 주지 않습니다.
- **비동기 처리 최적화**: `QThread`와 Worker 패턴을 적용하여 이미지 생성 중에도 UI가 멈추지 않는 쾌적한 사용자 경험을 제공합니다.
- **유연한 설정 관리**: JSON 기반의 설정 파일(`workflows/`)을 통해 코드 수정 없이 워크플로우와 모델 경로를 변경할 수 있습니다.

---

## 🛠️ 5단계 운영 파이프라인

본 프로그램은 다음과 같은 순차적 흐름으로 작동합니다.

### 1. 연결 단계 (`01_Connection`)
- **LM Studio 연결**: 로컬 LLM 서버와 연결하여 프롬프트 확장 준비를 합니다.
- **ComfyUI 연결**: 이미지 생성 백엔드인 ComfyUI API 서버와의 연결 상태를 확인합니다.

### 2. 생성 설정 단계 (`02_Generation`)
- **모델 선택**: 사용 가능한 모델 프로필(Flux GGUF, ZImage Turbo 등) 중 하나를 선택합니다.
- **파라미터 설정**: 선택한 모델 프로필에 따라 최적의 스케줄러와 기본 설정값이 자동으로 로드됩니다.

### 3. 프롬프트 최적화 단계 (`03_Prompt`)
- **프롬프트 확장**: 사용자가 입력한 단순한 아이디어를 LM Studio의 LLM을 통해 상세한 이미지 생성용 프롬프트로 확장합니다.
- **역할 부여**: LLM에게 전문 프롬프트 엔지니어의 역할을 부여하여 고품질의 묘사를 생성합니다.

### 4. 결과 미리보기 및 조정 단계 (`04_Result`)
- **워크플로우 매핑**: 확장된 프롬프트를 ComfyUI의 JSON 워크플로우 노드에 정확하게 매핑합니다.
- **최종 확인**: 생성 전 최종 프롬프트와 설정값을 확인하고 필요 시 수정합니다.

### 5. 실행 및 출력 단계 (`05_Execution`)
- **API 요청**: 구성된 워크플로우를 ComfyUI 서버로 전송합니다.
- **실시간 추적**: 생성 프로세스를 추적하고, 완료된 이미지를 `outputs/` 폴더에 저장하며 화면에 표시합니다.

---

## 📦 모델 프로필 및 설정 시스템

### 모델 프로필 (`app/core/model_profiles/`)
각 모델은 `ModelProfile` 클래스를 상속받아 정의되며, 다음과 같은 속성을 관리합니다.
- **Scheduler**: 모델에 최적화된 스케줄러 (예: Flux $\rightarrow$ `simple`, ZImage $\rightarrow$ `karras`)
- **Priority**: 모델 로드 우선순위 설정
- **Custom Params**: 모델별 특화 파라미터

### 설정 파일 (`workflows/`)
- `app_config.json`: ComfyUI 모델 경로 및 전역 애플리케이션 설정.
- `default_profiles.json`: 기본 모델 프리셋 및 매핑 정보.
- `*.json` (워크플로우 파일): 각 모델별 ComfyUI 노드 구성 정보.

---

## ⚙️ 설치 및 실행

상세한 설치 방법은 [INSTALLATION.md](./INSTALLATION.md) 파일을 참조하십시오.

**빠른 실행:**
```bash
pip install -r comfyui_lmstudio_requirements.txt
python main.py
```

---

## 📝 기술 스택
- **Language**: Python 3.10+
- **GUI Framework**: PySide6
- **Backend**: ComfyUI API, LM Studio Local Server
- **Config**: JSON

**버전**: v0.3  
**마지막 업데이트**: 2026-09-03  
**라이선스**: MIT
