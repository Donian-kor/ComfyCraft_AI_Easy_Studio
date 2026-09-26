# 📋 5, 7, 8, 9번 항목 상세 수정 계획서

> **문서 상태**: 각 항목은 `A. 기존 계획(원본 보존)` / `B. 재검증 결과` / `C. 개선 계획` 3절로 구성됩니다.
> **기존 계획(A절)은 삭제·덮어쓰지 않고 원문 그대로 보존**했으며, 코드베이스 재검증으로 발견된
> 결함과 그에 대한 수정안을 B/C절에 병기했습니다.

## 📌 검증 기준선 (2026-09-26 재검증)

| 항목 | 값 |
|---|---|
| Python | 3.14.7 (`.venv`) |
| PySide6 | 6.11.2 |
| pytest | **미설치** → `unittest`만 사용 |
| 기존 테스트 | `unittest` 14개 **전부 통과** (6.5s) |
| `tests/__init__.py` | **없음** (`unittest discover` 방식) |
| `basicConfig` / `FileHandler` | **전무** → 현재 로그는 어디로도 출력되지 않음 |
| 기준선 실행 명령 | `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` |

> ⚠️ **검색 오염 주의**: `.kilo/worktrees/full-care/`, `.kilo/worktrees/majestic-condition/`에
> 프로젝트 전체 사본이 존재해 grep 결과가 **3벌**로 출력됩니다.
> 이 문서의 모든 라인번호는 **저장소 루트본 기준**입니다.

## 📊 항목별 재검증 판정

| 항목 | 원 판정 | 재검증 판정 | 핵심 리스크 |
|---|---|---|---|
| [5번] 모델 타입 판별 통합 | 🟡 | 🟡 조건부 승인 | `WorkflowManager()` 무인스턴스화로 디스크 I/O 증가, 중복 4곳 중 2곳 누락 |
| [7번] 스레드 관리 개선 | 🟡 | 🔴 **재수정** | 논데몬 전환 시 **프로세스 종료 블로킹 실측 확인(3714ms)**, `closeEvent` 미배선 |
| [8번] 테스트 추가 | 🟢 | 🔴 **재수정** | pytest 미설치, 위젯 Mock 불가, **라운드트립이 사용자 설정 파괴** |
| [9번] 로깅 시스템 통합 | 🟢 | 🟡 조건부 승인 | `append_log`이 Qt 슬롯 → 삭제 시 `AttributeError`, FileHandler 누락 |

**권장 적용 순서**: [5번] → [9번] → [8번] → **[7번은 마지막]**

---

## 🟡 [5번] 모델 타입 판별 통합 (Phase 2)

### A. 기존 계획 (원본 보존)

**목표**: Zanime 판별 로직 통합에 이어, 남은 모델 타입(`flux`, `zimage`, `ernie`) 판별 로직도 `ModelRegistry`로 통합하여 중복을 제거합니다.

**수정 대상 파일**:
- `app/core/model_registry.py`
- `main.py`
- `app/sections/generation.py`

**상세 계획**:
1. **ModelRegistry 개선**: `ModelRegistry` 클래스에 아래 세 가지 메서드를 추가합니다.
   ```python
   def is_flux(self, model_name: str) -> bool:
       from app.core.workflow_manager import WorkflowManager
       profile = self.detect(model_name)
       return bool(profile.workflow_type == "flux_gguf" or WorkflowManager().is_flux_model(model_name) or profile.family == "flux")

   def is_zimage(self, model_name: str) -> bool:
       from app.core.workflow_manager import WorkflowManager
       profile = self.detect(model_name)
       return bool(WorkflowManager().is_zimage_model(model_name) or profile.workflow_type == "zimage")

   def is_ernie(self, model_name: str) -> bool:
       profile = self.detect(model_name)
       return bool(profile.family == "ernie")
   ```
2. **main.py / generation.py 중복 제거**:
   - `main.py`의 `enhance_prompt_only()` 내부 하드코딩 교체
   - `generation.py`의 `run()` 내부 하드코딩 교체
   - 교체 예시: `is_flux = get_model_registry().is_flux(comfy_model_name)`

### B. 재검증 결과 (2026-09-26)

#### ✅ 유효한 부분
중복이 실제로 존재하며, `main.py:1773` 주석이 "generation.py와 동일 로직"이라고 명시하므로 **의도된 중복 제거**입니다.
신규 메서드가 기존 판별 결과를 바꾸지 않음을 실행으로 확인했습니다.

| 입력 | `family` | `workflow_type` | 판별 결과 |
|---|---|---|---|
| `ERNIE-AIO-Base-fp8.safetensors` | `ernie` | `checkpoint` | `is_ernie=True` ✅ |
| `flux1-dev-Q4_0.gguf` | `flux` | `flux_gguf` | `is_flux=True` ✅ |
| `unknown_sdxl.safetensors` | `generic` | `checkpoint` | 모두 `False` ✅ |

#### 🔴 결함 1 — `WorkflowManager()` 무인스턴스화 (성능 회귀)
A절 코드는 매 호출마다 `WorkflowManager()`를 새로 만듭니다. `app/core/workflow_manager.py:26-30`:

```python
def __init__(self, config_manager=None):
    self.config = self.config_manager.get()
    self._load_templates()      # ← JSON 템플릿 4개를 매번 디스크에서 로드
```

`is_flux()`는 `enhance_prompt_only()` 및 모델 combo change 경로에서 호출되므로
**UI 이벤트마다 디스크 I/O 4회가 추가**됩니다. 기존 `is_zanime()`이 이 패턴을 쓰지 않는다는 점과도 어긋납니다.

#### 🔴 결함 2 — 중복은 4곳인데 2곳만 언급
| 실제 위치 | 조건식 | A절 언급 여부 |
|---|---|---|
| `main.py:1778-1787` | flux/zimage/ernie/zanime | ✅ |
| `app/sections/generation.py:833-836` | flux/zimage/ernie/zanime | ✅ |
| `app/sections/generation.py:463` | zimage 조건식 | ❌ **누락** |
| `app/sections/generation.py:507` | flux 조건식 | ❌ **누락** |

#### 🟡 결함 3 — 함수명 오류
A절은 "`generation.py`의 `run()` 내부"라 서술했으나, `run()`은 L101에 있고 판별 로직이 없습니다.
실제 위치는 **`enhance_prompt()` (L816)** 입니다.
호출 체인: `run()`(L101) → `generate()`(L122) → `enhance_prompt()`(L158).

#### 🟡 참고 — 선행 선례 존재 (계획서 작성 이후 실제 적용됨)
작업 트리에 `ModelRegistry.is_zanime()` 통합이 **이미 적용**되어 있습니다(미커밋).
따라서 신규 3개 메서드는 아래 개선안 스타일로 추가해야 프로젝트 관례에 부합하며,
검증 방식도 `is_zanime`과 동일하게 삼아야 합니다.

#### 🟡 계층 역전 (의도된 trade-off)
`model_registry` → `workflow_manager` 의존이 새로 생깁니다.
현재 `workflow_manager`는 `config_manager`만 import하므로 **순환은 없음**(import 실행 확인).
다만 지연 import로 안전성을 확보하는 것을 권장합니다.

### C. 개선 계획

**1. `ModelRegistry` 메서드 3종 추가** — `get_workflow_manager()` 싱글턴 사용

```python
def is_flux(self, model_name: str) -> bool:
    from app.core.workflow_manager import get_workflow_manager   # ← WorkflowManager가 아님
    profile = self.detect(model_name)
    return bool(
        profile.workflow_type == "flux_gguf"
        or get_workflow_manager().is_flux_model(model_name)
        or profile.family == "flux"
    )

def is_zimage(self, model_name: str) -> bool:
    from app.core.workflow_manager import get_workflow_manager
    profile = self.detect(model_name)
    return bool(
        get_workflow_manager().is_zimage_model(model_name)
        or profile.workflow_type == "zimage"
    )

def is_ernie(self, model_name: str) -> bool:
    profile = self.detect(model_name)
    return bool(profile.family == "ernie")
```

**2. 중복 제거 — 4곳 모두 교체** (누락 2곳 포함)

| 파일:라인 | 교체 |
|---|---|
| `main.py:1778-1787` | `is_flux` / `is_zimage` / `is_ernie` / `is_zanime` 4줄로 축약 |
| `app/sections/generation.py:833-836` | 동일 4줄로 축약 |
| `app/sections/generation.py:463` | `manager.is_zimage_model(model_name) or profile.workflow_type == "zimage"` → `registry.is_zimage(model_name)` |
| `app/sections/generation.py:507` | `profile.workflow_type == "flux_gguf" or manager.is_flux_model(...) or profile.family == "flux"` → `registry.is_flux(model_name)` |

> ⚠️ L507은 `base_wf is None and (...)` 형태이므로 `base_wf is None` 조건은 **반드시 유지**해야 합니다.

**3. 회귀 방지 테스트 추가** (`tests/test_core_components.py`)
기존 `test_core_components.py`에 다음 케이스를 고정해, 판별 결과가 교체 전후 100% 동일함을 보장합니다.
- `is_flux("flux1-dev-Q4_0.gguf")` → `True`
- `is_zimage("z_image_turbo_fp8.safetensors")` → `True`
- `is_zimage("ERNIE-AIO-Turbo-fp8.safetensors")` → `False` (기존 `test_is_zimage_model_no_longer_matches_bare_turbo`와 일관성 확인)
- `is_ernie("ERNIE-AIO-Base-fp8.safetensors")` → `True`
- `is_flux("unknown_sdxl.safetensors")` / `is_ernie(...)` → `False`

**4. 검증 명령**
```
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
기준선: **14개 통과 → 회귀 0건 유지**

---

## 🟡 [7번] 스레드 관리 개선 (Phase 3)

### A. 기존 계획 (원본 보존)

**목표**: 무분별하게 생성되고 버려지는 데몬(`daemon=True`) 스레드를 추적 가능하고 안전하게 종료할 수 있는 스레드 풀로 교체합니다.

**수정 대상 파일**:
- `main.py`

**상세 계획**:
1. **스레드 풀 초기화**: `MainController.__init__`에 `ThreadPoolExecutor` 인스턴스 생성 추가.
   ```python
   from concurrent.futures import ThreadPoolExecutor

   def __init__(self, window):
       # ...
       self._thread_pool = ThreadPoolExecutor(max_workers=3, thread_name_prefix="BgWorker")
   ```
2. **데몬 스레드 교체**: `threading.Thread(...)` 호출을 모두 `submit`으로 변경합니다.
   - **L1070 부근 (`refresh_models`)**:
     - 기존: `threading.Thread(target=fetch, daemon=True).start()`
     - 변경: `self._thread_pool.submit(fetch)`
   - **L1148 부근 (`check_connection`)**:
     - 기존: `threading.Thread(target=check, daemon=True).start()`
     - 변경: `self._thread_pool.submit(check)`
   - **L1944 부근 (`start_generation`)**:
     - 기존: `threading.Thread(target=self.worker.run, daemon=True).start()`
     - 변경: `self._thread_pool.submit(self.worker.run)` (※ QThread/QRunnable로 전환하는 방안도 고려 가능)
3. **종료 대기**: `close()` 메서드 내에서 `self._thread_pool.shutdown(wait=False)` 호출로 누수 방지.

### B. 재검증 결과 (2026-09-26)

#### 🔴 치명적 — 데몬→논데몬 전환 시 프로세스가 종료되지 않음 (실측 증명)
`ThreadPoolExecutor` 워커는 **논데몬(non-daemon) 스레드**입니다.
`concurrent/futures/thread.py`가 `threading._register_atexit(_python_exit)`로 **인터프리터 종료 시 모든 워커를 join**합니다.
`shutdown(wait=False)`는 이를 막지 못합니다 — join은 인터프리터 레벨 동작입니다.

**실측 결과**:
```
submit(3초 sleep) → shutdown(wait=False) → print("main done")
elapsed = 3714ms
```

즉 A절 3번의 "누수 방지"라는 서술은 **사실과 반대**입니다.
전환 후에는 `refresh_models`의 네트워크 타임아웃(수 초~수십 초)만큼 **창이 닫혀도 프로세스가 멈춥니다.**
(근거: `concurrent/futures/thread.py` 내 `# shutting down. Must be held while mutating _threads_queues and _shutdown` 및 `threading._register_atexit(_python_exit)`)

#### 🔴 `max_workers=3` + 장시간 작업 = 큐잉
`self.worker.run`(`app/sections/generation.py:101`)은 이미지 생성 전체를 수행하는 **수 분~수십 분 작업**입니다.
이것이 풀 워커 하나를 점유하면, 사용자가 생성 중 `refresh_models`나 `check_connection`을 눌렀을 때
남은 2개 워커는 그 동안 **큐에 쌓여 실행되지 않고**, UI가 멈춘 것처럼 보입니다.
데몬 스레드에서는 매번 새 스레드가 생성되어 **절대 발생하지 않던 문제**입니다.

#### 🟡 라인번호 오류 (3곳 전부)
| A절 표기 | 실제 | 함수 |
|---|---|---|
| L1070 | **L1074** | `refresh_models` |
| L1148 | **L1152** | `check_connection` |
| L1944 | **L1947** | `start_generation` |

#### 🟡 `close()` 배선 누락 — 절반만 해결됨
`MainController.close()`는 `main.py:313`의 종료 버튼(`exitButton`)에만 연결되어 있고,
**`closeEvent` 오버라이드가 없습니다.**
창 X 버튼으로 닫으면 `close()`가 호출되지 않아 **풀 정리가 영영 실행되지 않습니다.**

#### ✅ 유효한 부분
- `ThreadPoolExecutor` 도입 의도는 타당 (스레드 추적/재사용/취소 가능)
- A절이 "QThread/QRunnable 전환도 고려 가능"이라 적었는데, **생성 작업은 실제로 QThread가 정답**입니다.
  `PromptEnhanceWorker`(`main.py:1843`)와 `GenerationWorker`는 이미 `WorkerSignals` 패턴이므로 QThread화 비용이 낮습니다.
- `refresh_models` / `check_connection`은 **짧은 I/O**라 풀 도입 적합성이 높습니다.

#### 🟡 참고 — 범위 밖 스레드
`app/core/api_client.py:320`(웹소켓 `run_forever`)과 `app/core/model_fetcher.py:443-448`(`join()`으로 즉시 대기)는
본 항목의 데몬 스레드 문제가 아니므로 **변경 대상이 아닙니다.**

### C. 개선 계획

**1. 풀 분리 — 단일 풀 대신 2개** (작업 성격이 다름)
```python
# MainController.__init__
from concurrent.futures import ThreadPoolExecutor

# 짧은 I/O (네트워크 타임아웃 수 초)
self._io_pool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="IoWorker")
# 장시간 작업 1개 (수 분~수십 분)
self._gen_pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="GenWorker")
```
- `submit()`은 풀이 가득 차면 새 스레드를 생성하므로, 데몬 스레드와 유사한 탄력성을 가집니다.
- 논데몬 종료 지연은 **짧은 I/O에만** 적용되어 감수 가능합니다.

**2. 데몬 스레드 교체** (라인번호 정정)
| 함수 | 실제 라인 | 기존 | 변경 |
|---|---|---|---|
| `refresh_models` | **L1074** | `threading.Thread(target=fetch, daemon=True).start()` | `self._io_pool.submit(fetch)` |
| `check_connection` | **L1152** | `threading.Thread(target=check, daemon=True).start()` | `self._io_pool.submit(check)` |
| `start_generation` | **L1947** | `threading.Thread(target=self.worker.run, daemon=True).start()` | `self._gen_pool.submit(self.worker.run)` **(권장: QThread)** |

**3. QThread 전환 (권장안)**
`GenerationWorker`가 이미 `WorkerSignals(QObject)`를 보유하므로, `GenerationWorker`가 `QThread`를 상속하거나
`QRunnable`로 감싸면 `signals` 구조를 그대로 유지할 수 있습니다.
장시간 작업이므로 논데몬 종료 지연 문제를 **완전히 제거**할 수 있는 유일한 방법입니다.

**4. 종료 처리 — `closeEvent` 후킹 필수 추가**
```python
# MainController에 신규 추가
def closeEvent(self, event):
    self._close_thread_pools()
    super().closeEvent(event)

def _close_thread_pools(self):
    for pool in (self._io_pool, self._gen_pool):
        if pool is not None:
            pool.shutdown(wait=False, cancel_futures=True)

# 기존 close()에도 호출 추가
def close(self):
    ...
    self._close_thread_pools()   # ← 추가
```

> ⚠️ `cancel_futures=True`(Python 3.9+)로 대기 중 작업을 취소해야 종료 지연을 최소화할 수 있습니다.

**5. 검증 방법**
- 자동: `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` → 14개 통과 유지
- **수동 필수**:
  - 생성 진행 중 `refresh_models` 클릭 → 모델 목록이 **즉시** 갱신되는지 (큐잉 회귀 확인)
  - 생성 중 앱 종료 → 창이 닫힌 뒤 **즉시** 프로세스가 사라지는지 (3714ms 블로킹 재현 여부)
  - 창 X 버튼 종료 → 풀 정리가 정상 동작하는지 (`closeEvent` 배선 확인)

---

## 🟢 [8번] 테스트 추가 (Phase 4)

### A. 기존 계획 (원본 보존)

**목표**: 핵심 데이터 처리 및 UI 로직의 안정성을 담보하기 위한 테스트 코드를 작성합니다.

**수정 대상 파일**:
- `tests/test_main_controller.py` (신규)
- `tests/test_generation.py` (신규)

**상세 계획**:
1. **스냅샷 정합성 테스트 (`test_capture_snapshot`)**:
   - UI 위젯들을 Mocking(가짜 객체)하여 `capture_snapshot()`이 올바른 딕셔너리를 반환하는지, 필수 키(`prompt`, `seed`, `cfg` 등)가 누락되지 않았는지 검증합니다.
2. **에러 핸들링 테스트 (`test_error_handling`)**:
   - 필수 위젯이 없을 때 `_find_or_raise`가 `RuntimeError`를 정상적으로 뿜어내는지 확인.
3. **프롬프트 강화 테스트 (`test_prompt_enhance`)**:
   - Zanime, Flux, Ernie 등 모델별로 올바른 시스템 프롬프트가 매핑되는지 단위 테스트.
4. **설정 라운드트립 테스트 (`test_config_roundtrip`)**:
   - `save_config()`로 저장한 데이터가 `load_config()`로 100% 원복되는지 검증.

### B. 재검증 결과 (2026-09-26)

#### 🔴 pytest 미설치 — 기존 관례와 충돌
- `pytest`는 **설치되어 있지 않습니다** (실측 `ModuleNotFoundError`)
- 기존 `tests/test_core_components.py`, `tests/test_project_basics.py`는 **모두 `unittest.TestCase`**
- `tests/__init__.py`도 없어 `python -m unittest discover -s tests` 방식

A절대로 작성하면 테스트 실행 방법이 둘로 갈라집니다 → **`unittest`로 작성**해야 합니다.

#### 🔴 `capture_snapshot` 위젯 Mocking은 현실적으로 불가능
`capture_snapshot`(`main.py:1612-1695`)은 표면상 단순하나 실제로는 다음에 연쇄 접근합니다.
- `get_steps_value()`, `get_cfg_value()` → 내부에서 실제 위젯 트리 탐색
- `is_zanime_selected()` → `find(QComboBox, "comfyModelCombo")`
- `current_zanime_style()` → `self.config` 접근
- `FACEDETAILER_SLIDER_SPECS` 15개 슬라이더 + 최소 12개 위젯

게다가 `MainController.__init__`가 **즉시 `setup()`(L195-459, 260줄)을 호출**해 수십 개 위젯에 손댑니다.
`main.py`는 패키지가 아닌 루트 파일이고, import 시 `assets.icons.icon_rc`를 로드합니다.
**평범한 Mock으로는 이 테스트를 만들 수 없습니다.**

#### 🔴 `test_config_roundtrip`이 사용자 설정을 파괴 (가장 위험)
- `ConfigManager`는 **프로세스 전역 싱글턴** (`app/core/config_manager.py:513`)
- `save()`는 `workflows/app_config.json`에 씁니다
- 이 파일은 `git ls-files workflows` 기준 **git에 추적된 실제 사용자 설정**입니다

즉 `save_config()` → `load_config()` 라운드트립은 **사용자의 실설정을 덮어씁니다.**
테스트 실패 시 사용자가 실세를 잃을 수 있습니다.

#### 🟡 기존 테스트와 중복
`tests/test_core_components.py`에 이미 다음이 존재합니다.
- `test_ernie_system_prompts_are_configured`
- `test_is_zimage_model_no_longer_matches_bare_turbo`
- `test_prompt_request_uses_5000_output_token_limit`
- `test_config_manager_accessors`

A절 `test_prompt_enhance`는 1·2번과 **부분 중복**입니다.

#### ✅ 유효한 부분
- `test_error_handling`(`_find_or_raise`가 `RuntimeError` 발생, `main.py:189-193`)은
  **현실적으로 작성 가능한 유일한 항목**입니다. 해당 메서드는 작업 트리에서 이미 추가·검증된 상태입니다.
- `capture_snapshot`이 `prompt`, `seed`, `cfg` 등 필수 키를 반환한다는 **검증 의도는 타당**합니다.
  (실제로 L1676-1695에 해당 키들이 존재함을 확인)

### C. 개선 계획

**1. 프레임워크 — `unittest` 사용 (pytest 금지)**
```python
import unittest   # ← pytest 아님
```

**2. `test_capture_snapshot` — Mock 대신 offscreen QApplication**
```python
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")   # CI/헤드리스 환경

from PySide6.QtWidgets import QApplication
from app.gui.ui_loader import load_ui

_app = QApplication.instance() or QApplication([])     # 앱당 1회만 생성
```
- `PySide6.QtWidgets.QApplication` 임포트와 `app.gui.ui_loader.load_ui` 존재를 **실물 확인**했습니다.
- ⚠️ 단, `MainController.__init__`가 설정 파일을 읽으므로 `workflows/`를 임시 경로로 분리해야 합니다.
- 검증할 키: `prompt`, `negative`, `seed`, `cfg`, `steps`, `width`, `height`, `sampler`, `scheduler`, `denoise`

**3. `test_error_handling` — 그대로 구현 (최우선)**
```python
def test_error_handling(self):
    controller = ...  # 최소 구성
    with self.assertRaises(RuntimeError):
        controller._find_or_raise(QPlainTextEdit, "존재하지않는위젯")
```

**4. `test_config_roundtrip` — `tempfile` 격리 필수**
```python
import tempfile
from pathlib import Path
from app.core.config_manager import ConfigManager

with tempfile.TemporaryDirectory() as tmpdir:
    mgr = ConfigManager(Path(tmpdir) / "app_config.json")   # ← 절대 get_config_manager() 금지
    saved = mgr.get()
    mgr.save()
    reloaded = ConfigManager(Path(tmpdir) / "app_config.json").load()
```
> ⚠️ `ConfigManager`는 모듈 전역 싱글턴이므로, 테스트 후 `_config_manager` 상태를 복원해야 합니다.

**5. `test_prompt_enhance` — 중복 제거 후 신규 판별 메서드 테스트로 대체**
[5번] C절 3번에서 정의한 `is_flux` / `is_zimage` / `is_ernie` 케이스를
`tests/test_core_components.py`에 추가하는 편이 중복 없이 가치가 높습니다.

**6. 신규 파일 권장**
| 파일 | 내용 |
|---|---|
| `tests/test_main_controller.py` | `test_error_handling`, `test_capture_snapshot`(offscreen) |
| `tests/test_generation.py` | 프롬프트 강화 분기, `build_generation_snapshot` 정규화 |

**7. 검증 명령**
```
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
기준선: 기존 14개 **모두 통과 유지** + 신규 테스트 추가 통과
(확인 완료: 현재 14개 전부 `ok`, 6.506s)

---

## 🟢 [9번] 로깅 시스템 통합 (Phase 5)

### A. 기존 계획 (원본 보존)

**목표**: `print()` 문과 `self.append_log()`를 분리해 사용하던 것을 Python 표준 `logging` 시스템 하나로 완벽하게 통합합니다.

**수정 대상 파일**:
- `main.py` (기반 작업)
- 프로젝트 전체 `.py` 파일 (로깅 교체)

**상세 계획**:
1. **커스텀 Qt 로깅 핸들러 추가 (`main.py`)**:
   ```python
   class QPlainTextEditLogger(logging.Handler):
       def __init__(self, widget):
           super().__init__()
           self.widget = widget
           self.setFormatter(logging.Formatter('[%(asctime)s] %(message)s', "%H:%M:%S"))

       def emit(self, record):
           msg = self.format(record)
           # UI 스레드에서 안전하게 appendPlainText 실행
           QMetaObject.invokeMethod(self.widget, "appendPlainText",
                                    Qt.ConnectionType.QueuedConnection,
                                    Q_ARG(str, msg))
   ```
2. **전역 로거 설정**: `MainController.setup()` 완료 직후 `logger.addHandler(QPlainTextEditLogger(log_widget))` 적용.
3. **print() 및 append_log 제거**:
   - `print("[경고]...")` ➔ `logger.warning(...)`
   - `self.append_log(...)` ➔ `logger.info(...)`
   - 모든 정보성 메시지는 `logger.info`로 통일하면 콘솔 파일과 UI 양쪽에 동시에 남게 됩니다.

### B. 재검증 결과 (2026-09-26)

#### ✅ 유효한 부분
**A절의 핸들러 코드는 기술적으로 유효합니다.** 실측 확인:
```
Q_ARG exists: True
appendPlainText is slot: True   ← QPlainTextEdit에 Qt 슬롯으로 등록되어 있음
```
따라서 `QMetaObject.invokeMethod(..., QueuedConnection, Q_ARG(str, msg))`는 정상 동작합니다.

#### ✅ A절이 과소평가한 부분 — 이미 절반 구현됨
- `main.py:122`에 `logger = logging.getLogger(__name__)` **이미 존재**
- `append_log`(L2099-2104)는 위젯이 없으면 이미 `logger.info`로 폴백
- `logger.warning` / `logger.debug` 이미 다수 사용 중 (L837, L845, L1907, L2121)
- `pass`로 무음 처리되던 예외 12곳이 이미 `logger.debug(..., exc_info=True)`로 개선됨 (작업 트리)

**A절의 "기반 작업"은 사실상 완료된 상태이므로, 추가 구현은 핸들러 연결 + FileHandler 추가에 집중하면 됩니다.**

#### 🔴 치명적 — `append_log`을 "제거"하면 앱이 죽음
`main.py:1927`:
```python
self.worker.signals.log.connect(self.append_log)
```
`WorkerSignals.log`는 **`app/sections/generation.py:240`의 웹소켓 진행률 콜백에서 actively emit**됩니다.

A절 3번처럼 `self.append_log(...)`를 `logger.info(...)`로 대체해 **메서드를 삭제하면**
`start_generation()` 실행 시 즉시
**`AttributeError: 'MainController' object has no attribute 'append_log'`** 가 발생하여
**이미지 생성 전체가 실패**합니다.

→ **메서드 삭제 금지, 위임만 변경**해야 합니다.

#### 🔴 핸들러 중복 출력
`logger`에 UI 핸들러를 붙이면서 `append_log`이 위젯에 직접 쓰면
**로그가 2줄씩 중복 출력**됩니다. 위젯 직접 쓰기 제거가 필수입니다.

#### 🔴 "콘솔 파일"을 약속하지만 FileHandler 계획이 없음
A절 본문은 "콘솔 **파일**과 UI 양쪽에 동시에"라고 서술하지만, 제시된 핸들러는 **UI용 1개뿐**입니다.
현재 `basicConfig`/`StreamHandler`/`FileHandler`가 **전무**하여
**지금 로그는 어디로도 출력되지 않습니다.** 파일 로그를 원하면 반드시 추가해야 합니다.

#### 🟡 "프로젝트 전체 .py"는 과장
실측 `print()` 분포:
| 파일 | 건수 | 대상 여부 |
|---|---|---|
| `main.py` | 1 (L2867) | ✅ |
| `app/core/config_manager.py` | 2 (L175, L365) | ✅ |
| `app/gui/theme_manager.py` | 8 (L51~98) | ✅ |
| `scripts/build_help.py` | 8 | ❌ **독립 CLI 빌드 스크립트 — 제외** |

`scripts/build_help.py`는 GUI 로거와 통합할 대상이 아니며, 굳이 넣으면 불필요한 리스크만 발생합니다.

#### 🟡 시작 순서 문제
`theme_manager.py`의 `print()` 다수와 `main.py:2867`은 **`MainController`가 생성되기 전에** 실행됩니다.
A절 2번처럼 `MainController.setup()`에 핸들러를 붙이면 이 로그는 UI 로그창에 안 뜹니다(콘솔/파일만).
의도한 것인지 확인이 필요합니다.

### C. 개선 계획

**1. `append_log` — 삭제 금지, 위임만 변경** (Qt 슬롯 유지 필수)
```python
def append_log(self, message: str) -> None:
    logger.info("%s", message)      # 핸들러가 UI로 포워딩
    # 위젯 직접 appendPlainText 제거 → 중복 출력 방지
```

**2. 커스텀 Qt 로깅 핸들러 추가** (A절 코드 채택, 검증 완료)
```python
class QPlainTextEditLogger(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.setFormatter(logging.Formatter('[%(asctime)s] %(message)s', "%H:%M:%S"))

    def emit(self, record):
        msg = self.format(record)
        # UI 스레드에서 안전하게 appendPlainText 실행
        QMetaObject.invokeMethod(self.widget, "appendPlainText",
                                 Qt.ConnectionType.QueuedConnection,
                                 Q_ARG(str, msg))
```
필요 import: `from PySide6.QtCore import Q_ARG, QMetaObject`

**3. FileHandler 추가 — A절 누락분 (콘솔 파일 제공)**
```python
from logging.handlers import RotatingFileHandler

# main() 진입부 또는 MainController.__init__에서
log_path = BASE_DIR / "logs" / "app.log"
log_path.parent.mkdir(parents=True, exist_ok=True)
file_handler = RotatingFileHandler(
    log_path, maxBytes=2_000_000, backupCount=3, encoding="utf-8"
)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
```

**4. 핸들러 등록 위치 — 2곳으로 분리**
| 위치 | 대상 | 이유 |
|---|---|---|
| `main()` 진입부 (L2862 부근) | FileHandler | `MainController` 생성 전 로그를 파일에 남김 |
| `MainController.setup()` 완료 직후 | UI 핸들러 | `logTextEdit` 존재 시점 (A절 2번 유지) |

**5. `print()` 교체 (11건, `scripts/` 제외)**
| 파일 | 라인 | 레벨 |
|---|---|---|
| `main.py` | 2867 | `logger.info` |
| `app/core/config_manager.py` | 175, 365 | `logger.warning` |
| `app/gui/theme_manager.py` | 51, 53, 60, 70, 80, 88, 91, 98 | `logger.warning` |

**6. 검증 방법**
- 자동: `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` → 14개 통과 유지
- 수동: 로그 메시지가 **2줄씩 중복 출력되지 않는지** 확인 (중복 출력 회귀)
- 수동: `logs/app.log` 파일이 생성되고 콘솔과 내용이 일치하는지 확인

---

## 📌 전체 적용 순서 및 체크리스트

| 순서 | 항목 | 위험도 | 선행 조건 |
|---|---|---|---|
| 1 | [5번] 모델 타입 판별 통합 | 🟢 낮음 | 없음 (기존 `is_zanime` 선례 있음) |
| 2 | [9번] 로깅 시스템 통합 | 🟡 중간 | `append_log` 위임만 변경, 메서드 유지 |
| 3 | [8번] 테스트 추가 | 🟡 중간 | `tempfile` 격리 필수 |
| 4 | **[7번] 스레드 관리** | 🔴 **높음** | **반드시 마지막** — 수동 테스트 필수 |

**전 항목 공통 검증 명령**:
```
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
**기준선: 14개 통과 (6.5s) → 변경 후 회귀 0건 유지**

**미커밋 선행 작업 유의**:
`ModelRegistry.is_zanime()` 통합이 이미 작업 트리에 적용되어 있습니다(`app/core/model_registry.py`,
`app/sections/generation.py`, `main.py` 3개 파일). [5번] 작업 시 이 변경 위에 이어서 적용해야 합니다.
