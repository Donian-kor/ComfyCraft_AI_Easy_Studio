# ComfyCraft AI Easy Studio — Flet 전환형 리팩토링 계획서

> **목적:** 기존 PySide6 UI를 유지보수하는 리팩토링이 아니라, 현재 프로젝트의 기능 계층을 보존하면서 **Flet 기반의 새로운 Material/AI Studio UI로 전면 전환**한다.
>
> **기준:** 현재 `ComfyCraft_AI_Easy_Studio.zip` 및 기존 `REFACTOR_PLAN.md` 분석 결과를 기반으로 작성한다.
>
> **중요:** 구현 전에 이 문서를 기준 계획으로 확정하고, 각 단계 완료 후 테스트를 통과한 뒤 다음 단계로 진행한다.

---

## 1. 이번 개정의 핵심

기존 계획은 PySide6를 유지하면서 구조와 UI를 정리하는 방향이었다.

이번 계획에서는 목표를 다음과 같이 변경한다.

### 기존 목표

```text
PySide6 유지
    ↓
코드 구조 개선
    ↓
QSS/UI 개선
```

### 새로운 목표

```text
기존 프로젝트
    ↓
기능 계층 분리
    ↓
UI 프레임워크 독립
    ↓
Flet 기반 새 UI/UX 설계
    ↓
기존 기능 연결
    ↓
PySide6 제거
```

핵심은 **기능을 Flet로 다시 작성하는 것이 아니라, PySide6에 묶인 UI 계층을 교체하는 것**이다.

---

# 2. Flet 전환을 선택하는 이유

현재 PySide6 UI 자체가 만족스럽지 않기 때문에 기존 UI를 계속 개선하는 것은 중복 작업이 될 가능성이 높다.

Flet 전환의 목적은 다음과 같다.

- Material Design 계열의 현대적인 UI 구성
- AI Studio에 적합한 카드/패널/Navigation UI
- Python 기반 UI 구성
- QSS 의존성 제거
- Qt Designer `.ui` 의존성 제거
- 향후 Web/모바일 확장 가능성 확보
- UI와 기능 계층의 명확한 분리

단, Flet이 자동으로 좋은 디자인을 만들어주는 것은 아니다.

**Material 계열 컴포넌트를 기반으로 ComfyCraft에 맞는 UX를 새로 설계한다.**

---

# 3. 절대 유지해야 하는 원칙

## 3.1 기능 코드는 UI 프레임워크를 몰라야 한다

다음 구조를 목표로 한다.

```text
features/
application/
core/
models/
    ↑
    │
    └── Flet UI
```

기능 계층에서 다음을 import하지 않는다.

```python
import flet
from PySide6 ...
```

UI 계층만 Flet을 사용한다.

---

## 3.2 PySide6를 Flet로 1:1 번역하지 않는다

다음 방식은 금지한다.

```text
QPushButton → Flet Button
QComboBox  → Flet Dropdown
QDialog    → Flet Dialog
QSplitter  → Flet ...
```

이런 식으로 기존 UI를 그대로 복제하지 않는다.

**화면의 기능과 데이터 흐름은 보존하되 UI/UX는 새로 설계한다.**

---

## 3.3 기존 기능은 최대한 재사용한다

다음 영역은 우선 보존 대상이다.

- ComfyUI API
- Workflow 처리
- 모델 검색/등록
- 설정 관리
- 연결 상태
- 세션 관리
- Prompt 처리
- 이미지 생성 기능
- Chat 데이터 모델
- Help 콘텐츠
- 기존 Workflow 데이터
- 테스트 가능한 순수 Python 코드

---

# 4. 현재 코드에서 주요 전환 대상

현재 분석에서 특히 문제가 되는 부분:

```text
main_controller.py
약 4,323줄
```

이 파일을 Flet용 대형 Controller로 다시 만드는 것은 금지한다.

또한 다음 계층은 PySide6 의존성을 분리해야 한다.

```text
sections/generation.py
sections/prompt.py
sections/execution.py
sections/result.py
gui/
```

특히 `GenerationWorker`가 Controller와 UI를 직접 참조하는 구조를 제거한다.

---

# 5. 목표 프로젝트 구조

```text
app/
├─ core/
│  ├─ api/
│  ├─ config/
│  ├─ model/
│  ├─ workflow/
│  └─ connection/
│
├─ models/
│  ├─ chat.py
│  ├─ generation.py
│  ├─ model.py
│  ├─ session.py
│  └─ settings.py
│
├─ features/
│  ├─ generation/
│  ├─ prompt/
│  ├─ workflow/
│  ├─ model/
│  ├─ connection/
│  ├─ session/
│  └─ config/
│
├─ application/
│  ├─ generation_service.py
│  ├─ prompt_service.py
│  ├─ session_service.py
│  ├─ model_service.py
│  └─ settings_service.py
│
├─ ui/
│  └─ flet/
│     ├─ app.py
│     ├─ shell.py
│     ├─ navigation.py
│     ├─ theme/
│     ├─ pages/
│     │  ├─ home.py
│     │  ├─ generation.py
│     │  ├─ chat.py
│     │  ├─ history.py
│     │  ├─ settings.py
│     │  └─ help.py
│     ├─ components/
│     └─ dialogs/
│
└─ common/
```

정확한 폴더명은 실제 코드 이동 과정에서 조정할 수 있지만 **계층의 책임은 변경하지 않는다.**

---

# 6. 폐기 대상

Flet 전환이 완료되면 다음은 제거 대상이다.

```text
*.ui
```

및 PySide6 전용:

```text
PySide6 Widget 코드
QSS 기반 Theme
Qt Designer 로딩 코드
PySide6 전용 Controller 연결 코드
QThread/QObject 기반 UI Worker
```

단, 해당 코드 안에 기능 로직이 들어 있으면 먼저 기능 계층으로 이동한 후 제거한다.

---

# 7. 보존 대상

다음은 우선 보존한다.

```text
app/core/
app/models/
workflows/
도움말 콘텐츠
설정 데이터 구조
모델 데이터
ComfyUI 통신
LM Studio 통신
이미지 생성 로직
세션/히스토리 데이터
순수 Python 테스트
```

기존 코드가 완벽히 분리되어 있지 않으면 **복사해서 새 코드와 중복시키지 말고 기존 구현을 이동/정리한다.**

---

# 8. Phase 0 — 안전망 구축

목표:

> Flet 작업 전에 기존 기능이 정상적으로 동작하는 상태를 확보한다.

### 작업

- 기존 테스트 실행
- 테스트 실패 목록 기록
- 핵심 기능별 최소 동작 확인
- ComfyUI 연결 확인
- 모델 목록 확인
- Workflow 실행 확인
- 이미지 생성 확인
- 설정 저장/로드 확인
- 세션/History 확인
- Prompt 기능 확인

### 원칙

현재 실패하는 테스트를 새 UI 문제와 섞지 않는다.

---

# 9. Phase 1 — 기능 계층 분리

목표:

> PySide6가 없어도 이미지 생성 기능을 실행할 수 있는 구조를 만든다.

분리 대상:

```text
Generation
Prompt
Workflow
Model
Connection
Session
Config
```

각 기능은 UI가 아니라 서비스/모델을 통해 동작하게 한다.

예:

```python
result = generation_service.generate(settings)
```

UI에서:

```python
await generation_service.generate(...)
```

와 같이 호출할 수 있어야 한다.

---

# 10. Phase 2 — Generation 완전 분리

가장 중요하다.

현재 `GenerationWorker`의 Controller 역참조를 제거한다.

기존:

```text
GenerationWorker
    ↓
MainController
    ↓
Qt Widget / Config / Model / Workflow
```

목표:

```text
GenerationService
    ↓
GenerationSettings
    ↓
WorkflowService
    ↓
ComfyUI Client
    ↓
GenerationResult
```

결과 모델:

```text
GenerationResult
├─ status
├─ image_path
├─ elapsed
├─ metadata
└─ error
```

진행 상태:

```text
GenerationProgress
├─ status
├─ progress
├─ message
└─ preview
```

이렇게 하면 UI가 사라져도 생성 작업을 계속할 수 있다.

---

# 11. Phase 3 — 비동기 작업 구조 정리

이미지 생성은 장시간 작업이므로 화면과 작업의 생명주기를 분리한다.

목표:

```text
Generate 클릭
    ↓
Job 생성
    ↓
UI는 계속 사용 가능
    ↓
ComfyUI 실행
    ↓
Progress Event
    ↓
완료/실패
    ↓
Session 저장
```

사용자가:

- History로 이동
- Settings 열기
- Chat 이동
- 다른 페이지 이동

을 하더라도 생성 작업이 중단되지 않아야 한다.

---

# 12. Phase 4 — Flet App Shell

기존 UI를 옮기지 않고 새 Shell을 만든다.

구성:

```text
App
├─ TopBar
├─ NavigationRail
├─ MainContent
└─ Optional SidePanel
```

Material 기반의 공통 Theme를 만든다.

### 기본 디자인 방향

- Material 3 계열
- Dark 기본 테마
- 명확한 Surface 계층
- 과도한 테두리 제거
- 카드/패널 간격 통일
- 상태 색상 체계 통일
- 아이콘 + 짧은 텍스트
- 작은 화면에서도 레이아웃 유지

---

# 13. Phase 5 — Main Generation 화면 재설계

기존 화면을 그대로 복제하지 않는다.

목표:

```text
┌──────────────────────────────────────────────────────────┐
│ ComfyCraft                         ComfyUI ●  LM Studio ●│
├──────────┬───────────────────────────┬───────────────────┤
│          │                           │ Generation        │
│ Home     │                           │                   │
│ Generate │       Image Preview       │ Model             │
│ Models   │                           │ Resolution        │
│ Workflow │                           │ Sampling          │
│ Chat     │                           │ Prompt            │
│ History  │                           │ Advanced ▼        │
│ Settings │                           │ FaceDetailer ▼    │
│ Help     │                           │                   │
│          │                           │ [Generate]        │
├──────────┴───────────────────────────┴───────────────────┤
│ Status / Generation Progress / Current Job                │
└──────────────────────────────────────────────────────────┘
```

화면 폭에 따라 중앙 Preview와 설정 패널이 자연스럽게 조정되도록 한다.

---

# 14. Phase 6 — Generation 옵션 UX

현재 옵션을 전부 한 번에 보여주지 않는다.

### 기본

```text
Model
Resolution
Prompt
Seed
Generate
```

### Advanced

```text
Steps
CFG
Sampler
Scheduler
Denoise
```

### FaceDetailer

```text
ON/OFF

기본
Advanced
```

### FaceDetailer 상세 옵션

기존 기능은 보존하되 접어서 표시한다.

목표는 **기능 삭제가 아니라 정보 밀도 조절**이다.

---

# 15. Phase 7 — Chat / Result 화면

기존 ChatMessageData는 최대한 재사용한다.

구성:

```text
Chat
├─ User Message
├─ AI Message
├─ Prompt Card
├─ Generation Card
├─ Image Card
└─ Progress Card
```

이미지 결과 카드:

```text
┌──────────────────────────┐
│ Generated                │
│                          │
│       Image              │
│                          │
│ Model / Resolution       │
│ Generation Time          │
│                          │
│ Save  Reuse  Edit        │
└──────────────────────────┘
```

---

# 16. Phase 8 — History

History는 독립 Page로 구성한다.

기능:

- 검색
- 날짜별 그룹
- 생성 결과 미리보기
- Prompt 확인
- 설정 확인
- 이미지 재사용
- 다시 생성
- 삭제

SessionManager의 기능은 재사용한다.

---

# 17. Phase 9 — Settings

Settings는 Dialog 중심 구조에서 **독립 Settings Page** 중심으로 변경한다.

```text
Settings
├─ General
├─ Appearance
├─ Connections
│  ├─ ComfyUI
│  └─ LM Studio
├─ Models
├─ Generation
├─ Storage
└─ Logs
```

현재 저장되는 설정값과 데이터 구조를 임의로 삭제하지 않는다.

---

# 18. Phase 10 — Help

기존 도움말 콘텐츠를 유지한다.

UI만 변경한다.

```text
Help
├─ Getting Started
├─ Generation
├─ Models
├─ Prompt
├─ FaceDetailer
├─ History
└─ FAQ
```

좌측 목차 + 우측 콘텐츠 구조를 사용한다.

---

# 19. Phase 11 — Theme 시스템

QSS를 Flet Theme으로 교체한다.

### Theme 토큰

```text
Background
Surface
SurfaceVariant
Primary
Secondary
Text
TextSecondary
Success
Warning
Error
Border
Spacing
Radius
Elevation
```

색상 값을 여러 UI에 직접 하드코딩하지 않는다.

---

# 20. Phase 12 — 기존 UI 제거

Flet 화면이 모든 기능을 대체하고 테스트가 통과한 후에만 제거한다.

순서:

```text
Flet 기능 완성
    ↓
회귀 테스트
    ↓
PySide6 UI 사용 여부 확인
    ↓
PySide6 전용 코드 제거
    ↓
*.ui 제거
    ↓
QSS 제거
    ↓
Qt dependency 제거
```

중간에 기존 PySide6와 Flet을 장기간 이중 유지하지 않는다.

---

# 21. Phase 13 — 테스트

테스트를 세 계층으로 나눈다.

## Core / Feature

UI와 무관하게 테스트.

```text
API
Workflow
Model
Generation
Prompt
Session
Config
```

## Application

서비스 호출과 데이터 흐름 테스트.

## Flet UI

최소한 다음을 테스트한다.

```text
앱 시작
Navigation
Generate 버튼
설정 변경
Prompt 입력
Generation 진행 표시
완료 결과 표시
History 이동
Settings 이동
Help 이동
```

UI 테스트에 과도하게 내부 구현을 결합하지 않는다.

---

# 22. 금지사항

### 1. Flet UI 안에 비즈니스 로직 작성 금지

```python
on_click:
    # 200줄의 이미지 생성 로직
```

금지.

### 2. 거대한 Flet Controller 금지

```text
flet_controller.py
3000줄
```

같은 구조를 만들지 않는다.

### 3. 기존 PySide6 코드를 Flet UI 안에서 호출하지 않는다

```python
from app.gui.xxx import ...
```

금지.

### 4. 동일 기능을 두 군데 구현하지 않는다

기존 구현을 새 구현으로 복사한 뒤 둘 다 유지하지 않는다.

### 5. 기능 삭제를 리팩토링으로 포장하지 않는다

기능이 필요 없다고 판단되면 별도로 기록하고 승인받는다.

---

# 23. 화면 설계 우선순위

구현 순서는 다음으로 한다.

```text
1. App Shell
2. Generation
3. Image Result
4. Prompt
5. Chat
6. History
7. Settings
8. Help
9. 기타 Dialog
```

가장 핵심적인 이미지 생성 흐름을 먼저 완성하고 나머지를 연결한다.

---

# 24. 완료 기준

Flet 전환 완료는 다음을 모두 만족해야 한다.

### 기능

- ComfyUI 연결
- 모델 확인
- Workflow 실행
- 이미지 생성
- Prompt
- FaceDetailer
- History
- Session
- Settings
- Chat
- Help

### 구조

- UI → Application → Feature/Core 구조
- Feature에서 Flet import 없음
- Feature에서 PySide6 import 없음
- 거대한 Controller 없음
- GenerationWorker의 Controller 직접 참조 없음

### UI

- Flet 기반
- Material 계열 Theme
- 기존 PySide6 화면을 그대로 복제하지 않음
- 반응형/패널 구조
- Advanced 옵션 접기
- Generation 작업과 화면 이동 분리

### 정리

- PySide6 제거
- QSS 제거
- `.ui` 제거
- 사용하지 않는 Qt 코드 제거
- 중복 코드 제거

---

# 25. 최종 아키텍처

```text
┌─────────────────────────────────────────────┐
│                  Flet UI                    │
│                                             │
│ Shell / Navigation / Pages / Components     │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│             Application Layer               │
│                                             │
│ Generation / Prompt / Session / Settings   │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│              Feature Layer                  │
│                                             │
│ Generation / Workflow / Model / Connection │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│                Core / Models                │
│                                             │
│ API / Config / Workflow / Data Models      │
└──────────────────────┬──────────────────────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
          ComfyUI           LM Studio
```

---

# 26. 기존 REFACTOR_PLAN과의 변경점

| 기존 계획 | 개정 계획 |
|---|---|
| PySide6 유지 | PySide6 제거 |
| QSS 개선 | Flet Theme |
| `.ui` 개선 | `.ui` 폐기 |
| Qt Designer 유지 | Python/Flet UI |
| 기존 UI 개선 | UI 전면 재설계 |
| MainController 분리 | Application/Feature 계층 분리 |
| Qt Worker 정리 | UI 독립 Job/Service 구조 |
| 기존 화면 중심 | 기능 중심 새 화면 |
| PySide6 테스트 중심 | Core/Application/Flet 계층별 테스트 |
| 4cut 스타일 UI 개선 | Material Card/Selector로 재설계 |

---

# 27. 핵심 판단

이번 리팩토링의 목표는:

> **"PySide6 코드를 예쁘게 정리하는 것"이 아니다.**

정확한 목표는:

> **"ComfyCraft의 이미지 생성/모델/워크플로/세션/설정 기능을 UI 프레임워크로부터 독립시키고, Flet + Material 기반의 새로운 AI Studio UI를 구축하는 것"이다.**

따라서 기존 PySide6 UI에 대한 추가적인 대규모 디자인 작업은 하지 않는다.

**기능 계층을 먼저 안정화하고, Flet에서 새 UI를 만든다.**

---

## 작업 순서 요약

```text
[현재 프로젝트]
      │
      ▼
Phase 0  안전망
      │
      ▼
Phase 1  Feature 분리
      │
      ▼
Phase 2  Generation 분리
      │
      ▼
Phase 3  Async Job 분리
      │
      ▼
Phase 4  Flet Shell
      │
      ▼
Phase 5  Generation UI
      │
      ▼
Phase 6  Advanced / FaceDetailer
      │
      ▼
Phase 7  Chat / Result
      │
      ▼
Phase 8  History
      │
      ▼
Phase 9  Settings
      │
      ▼
Phase 10 Help
      │
      ▼
Phase 11 Theme / UX
      │
      ▼
Phase 12 PySide6 제거
      │
      ▼
Phase 13 전체 테스트 / 패키징
      │
      ▼
[ComfyCraft Flet Edition]
```

**이 문서를 Flet 전환을 위한 새로운 기준 `REFACTOR_PLAN.md`로 사용하면 된다.**
