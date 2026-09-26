# img2img(참조 이미지 변환) 지원 — 상세 수정 계획서

- 대상 프로젝트: `ComfyCraft_AI_Easy_Studio`
- 작성 기준: `main` 브랜치 / `7eea1c2`
- 목적: txt2img 전용 앱에 **표준 latent img2img**를 최소 변경으로 추가하기 위한 통합 구현 명세
- 통합 출처: `IMG2IMG_IMPLEMENTATION_PLAN.md`(요구사항) + 기존 상세 설계(코드 스펙)

---

## 0. 목표와 변경 범위

### 0.1 목표

기존 txt2img 생성과 다른 기능은 유지하면서, 사용자가 원본 이미지를 선택하고 프롬프트 및 변환 강도를 지정해 img2img를 실행할 수 있게 한다.

### 0.2 구현 범위

- 원본 이미지 선택, 미리보기, 제거, 파일 정보 표시
- img2img 모드 라디오 세그먼트(txt2img / img2img)와 변환 강도(denoise) 컨트롤
- 원본 크기 연동(출력 크기 기본값)
- ComfyUI 이미지 업로드 및 모델별 워크플로 변환
- 기존 프롬프트 향상 버튼의 모드별 동작
- img2img + FaceDetailer 조합 경고 문구(값은 조정하지 않음)
- txt2img 회귀 여부 및 모델별 호환성 검증

### 0.3 범위 밖

- 마스크·인페인트 기반 부분 편집
- 지시형(instruction) 이미지 편집 모델
- 참조 이미지 경로의 프리셋/설정 파일 영속 저장 (현재 실행에만 사용)
- 모드별 샘플링 프리셋 자동 조정(Steps/CFG 자동 변경) — 사용자 값 존중
- FaceDetailer 파라미터 자동 조정 — 경고 문구로만 안내

---

## 1. 현재 구조 요약 (실측 기준)

### 1.1 데이터 흐름

```
UI 위젯 (assets/ui/main.ui)
  └─ main.py capture_snapshot()  →  snapshot dict
        └─ GenerationWorker(controller, snapshot)
              └─ generate()  →  build_workflow(profile, ...)
                    └─ WorkflowManager.render_*_workflow()  →  템플릿 JSON 렌더링
                          └─ /prompt 제출 → 폴링 → /history → /view 다운로드
```

### 1.2 템플릿 공통 구조 (4종 모두 동일 패턴)

| 템플릿 | EmptyLatentImage | KSampler | KSampler.latent_image | VAE |
|---|---|---|---|---|
| `workflows/checkpoint.json` | `"4"` | `"5"` | `["4", 0]` | `CheckpointLoaderSimple` 출력 2 |
| `workflows/gguf_unet.json` | `"6"` | (동일 패턴) | `["6", 0]` | `VAELoader` |
| `workflows/flux_gguf.json` | `"6"` | (동일 패턴) | `["6", 0]` | `VAELoader` |
| `workflows/zimage.json` | `"6"` | `"7"` | `["6", 0]` | `VAELoader` |

**결론:** 4개 템플릿 모두 `EmptyLatentImage → KSampler.latent_image` 연결을 가지며, 그 연결만 교체하면 **단일 공용 변환 경로**로 img2img를 지원할 수 있습니다. 모델별 분기나 신규 템플릿이 필요하지 않습니다.

### 1.3 ZImage 특수성

`zimage.json`의 `TextEncodeZImageOmni`(노드 4, 5)는 이미 `image` 입력을 받지만 그 역할은 **conditioning 생성**이며, KSampler의 latent는 여전히 `EmptyLatentImage`(노드 6)입니다. 따라서 `EmptyLatentImage`를 `LoadImage → VAEEncode`로 교체하면 Omni conditioning은 그대로 유지되면서 latent만 참조 이미지로 바뀌어 **의도한 표준 img2img**가 됩니다.

### 1.4 이미 확보된 자산

- `GenerationSettings.denoise` (기본 1.0) — 템플릿 `__DENOISE__`로 이미 렌더링됨
- `denoiseSpinBox` 위젯 — `main.ui` 957행, 런타임 범위 0.0~1.0 (`main.py` 253행)
- `ComfyUIApiClient` — `requests.Session` 기반이라 multipart 전송에 그대로 활용 가능
- `capture_snapshot()` — 이미 `ValueError` → 경고 대화상자 처리 경로가 존재
- `enhancePromptButton` / `enhance_prompt_only` (295행) — 기존 프롬프트 향상 경로
- `widthSpinBox` / `heightSpinBox` (`main.ui` 652·669행) — 출력 크기 입력, img2img에서 잠금 대상

### 1.5 좌측 UI 배치 기준선 (`main.ui` 실측 행)

| 위치 | 위젯 | 행 |
|---|---|---|
| 스텝 카드 | `step2Card` / `step2Layout` | 472 / 476 |
| 헤더 | `step2HeaderLayout` (배지·제목·자동적용뱃지) | 493~531 |
| 모델 선택 | `modelSelectLayout` | 533 |
| 크기 입력 | `dimensionContainer` (가로/세로) | 630~692 |
| 고급 설정 | `advancedSettingsFrame` (기본 접힘) | 695~ |
| FaceDetailer | `faceDetailerCard` / `facedetailerPanel` | 967~ |

`advancedSettingsFrame`와 `faceDetailerCard`는 `step2Layout`의 형제 아이템이며, **FaceDetailer는 기본 상태에서 항상 보입니다.** `advancedContentWidget`는 `advancedToggleBtn` 체크 시에만 펼쳐집니다.

---

## 2. 설계 결정 및 근거

### 2.1 표준 latent img2img 채택 (지시형 이미지 편집 아님)

| 후보 | 선택 | 근거 |
|---|---|---|
| 표준 latent img2img (`LoadImage → VAEEncode`) | **채택** | 4개 템플릿 공통 적용, ComfyUI 기본 노드만 사용, 커스텀 노드 불필요 |
| 지시형 이미지 편집(instruction edit) | 불채택 | 모델별 전용 노드/프롬프트 규약 필요, 범위 과다 |
| 마스크 인페인트(`VAEEncodeForInpaint`) | 후속 확장 | 마스크 UI/브러시 별도 필요, 이번 범위 제외 |

### 2.2 UI 구조 (배치안 B — 확정)

img2img는 txt2img의 **대안 경로**이므로 별도 카드를 새로 만들지 않고, 기존 2단계 카드("핵심 생성 옵션") 내부에 **모드 세그먼트 + 조건부 옵션 카드**로 삽입합니다. 이로써 스텝 번호(1/2) 흐름이 그대로 유지됩니다.

```text
leftScrollArea
├─ step1Card  "1 아이디어 입력"                     유지
└─ step2Card  "2 핵심 생성 옵션"
   ├─ [ ● 텍스트로 만들기 | 🖼️ 이미지로 변환 ]     ★신규 (항상 보임)
   ├─ 모델 (AI 엔진) 선택                          유지
   ├─ 이미지 비율 프리셋                             유지
   ├─ 가로 / 세로                                   유지 (img2img 시 잠금)
   ├─ 🖼️ img2img 옵션 카드                          ★신규 (img2img일 때만 표시)
   │  ├─ [🖼️ 참조 이미지 선택]        [🗑️ 제거]
   │  ├─ 원본 이미지 미리보기 (비율 유지 축소)
   │  ├─ 파일명 · 가로×세로 크기
   │  └─ 변환 강도 [최소 ─────●── 최대]  0.65
   │     낮을수록 원본 유지, 높을수록 크게 변경
   ├─ ⚙️ 고급 설정 (시드/Steps/CFG/샘플러/스케줄러)  유지 (전부)
   └─ 👤 FaceDetailer                                유지 + 경고 라벨
```

**왜 이 배치를 선택했는가**

| 배치 후보 | 채택 | 근거 |
|---|---|---|
| A. `advancedContentWidget` 내부 `row="2"` | 불채택 | 기본값이 **접혀 있어 발견 불가**. 모드 전환이라는 큰 분기가 숨겨짐 |
| **B. 헤더 직후 + 크기 바로 아래 (채택)** | ✅ | 모드 세그먼트가 **항상 보여** 발견성 확보. img2img 카드를 `dimensionContainer` 바로 아래에 두어 "원본 크기 → 출력 크기" 연동이 눈으로 이어짐 |
| C. `step1Card` 하단 | 불채택 | 프롬프트 카드 과포화. 변환 강도는 생성 옵션이라 1단계에 어색 |

**UI 동작 규칙**

- `● 텍스트로 만들기` 선택 시 기존 txt2img 경로를 사용하며, `🖼️ 이미지로 변환` 관련 카드는 표시되지 않습니다.
- `🖼️ 이미지로 변환` 선택 시 img2img 카드, 변환 강도 슬라이더가 나타나고, 기존 `denoiseSpinBox`은 숨겨집니다(§2.3).
- 이미지를 선택하면 즉시 미리보기와 파일명·크기를 보여줍니다. 미리보기는 비율을 유지하며 표시 영역에 맞게 조정하고, **원본 파일은 변경하지 않습니다**.
- 이미지를 제거하면 미리보기, 파일 정보, 선택 경로를 함께 초기화합니다.
- img2img 모드에서 원본 크기를 출력 크기 기본값으로 사용하고, 폭·높이(`widthSpinBox`/`heightSpinBox`)를 비활성화합니다. txt2img로 돌아오면 원래 값으로 복구합니다.
- 모드를 txt2img로 되돌리면 선택한 참조 이미지는 유지합니다(재전환 시 재사용 가능). 명시적 `제거` 버튼으로만 초기화합니다.

### 2.3 변환 강도 컨트롤 분리

- img2img 변환 강도는 **기존 txt2img `denoiseSpinBox`를 재사용하지 않고 전용 컨트롤**(`img2imgStrengthSlider`)로 둡니다.
- 근거: 두 값의 의미와 기본값이 다릅니다(txt2img `1.0` = 완전 재구성, img2img `0.65` = 원본 유지). 한 컨트롤을 공유하면 모드 전환 시 값이 조작되어 사용자 의도와 어긋납니다.
- 전용 컨트롤의 값은 `capture_snapshot()`에서 `snapshot["denoise"]`로 **변환되어 주입**됩니다. 템플릿 `__DENOISE__` 경로는 그대로 재사용되므로 `build_workflow()` 수정이 필요 없습니다.
- **배치도 분리**합니다. img2img 카드는 `dimensionContainer` 바로 아래에, `img2imgStrengthSlider`는 그 카드 내부에 둡니다. `denoiseSpinBox`는 txt2img 모드에서만 표시됩니다(고급 설정 내부 기존 위치 유지).
- 값 정책: 기본값 `0.65`, 클램프 `0.05 ≤ 강도 ≤ 1.0`. 1.0이면 원본이 사실상 재구성되므로 UI 툴팁으로 안내합니다.

### 2.4 프롬프트 향상 버튼의 모드별 동작

새 버튼을 만들지 않고 기존 `enhancePromptButton` / `enhance_prompt_only` 경로를 재사용합니다.

| 모드 | 프롬프트 향상 지침 |
|---|---|
| txt2img | 새 장면을 생성하는 프롬프트로 향상 (기존 동작 유지) |
| img2img | 요청한 변화를 구체화하고, 요청하지 않은 원본의 주요 요소는 유지하도록 향상 |

- 이미지 파일 자체를 분석한다고 가정하지 않습니다. 버튼은 사용자가 입력한 **텍스트만** 다듬습니다.
- 입력 프롬프트가 비어 있으면 향상 동작을 비활성화하거나 내용을 입력하도록 안내합니다.
- 생성 시작 시 자동 향상 경로가 사용되는 경우에도 같은 모드별 지침을 적용합니다.

### 2.5 프롬프트 필수 검사

- txt2img의 기존 프롬프트 필수 검사를 **그대로 유지**합니다.
- img2img에서는 프롬프트 없이도 생성할 수 있도록 모드별 검사를 적용합니다.
- 두 모드 모두 원본 이미지가 없으면 ComfyUI 요청 전에 한국어 안내로 중단합니다.

### 2.6 UI 소스 우선순위

- 런타임은 `main.py:2842`의 `load_ui(UI_FILE)`로 **`assets/ui/main.ui`(XML)를 직접 로드**합니다.
- 따라서 `main.ui`를 단일 소스로 수정하고, `main_ui.py`는 동일한 이름/구조로 동기화해 정적 참조 일관성을 유지합니다.
- 프로그램 방식 추가(`QWidget`를 런타임 생성 후 레이아웃에 삽입)도 가능하나, `main.py`의 `find()` 기반 조회 패턴과 어긋나고 창 크기 조정이 어려워 `main.ui` 수정을 우선합니다.

### 2.7 subfolder 처리

ComfyUI `/upload/image` 응답은 `{"name": ..., "subfolder": "", "type": "input"}` 형태입니다. `type=input`, 빈 `subfolder`를 사용해 일반 `LoadImage`가 찾을 수 있게 하고, 응답값을 그대로 `LoadImage`에 전달합니다.


### 2.8 img2img 모드의 고급 설정 · FaceDetailer 대응 정책 (확정)

img2img에서도 **기존 고급 설정과 FaceDetailer를 모두 그대로 유지**합니다. 값을 강제로 바꾸지 않으며, 단 한 항목(디노이즈)만 의미가 달라져 별도 컨트롤로 대체합니다.

#### 2.8.1 항목별 정책

| 항목 | img2img 정책 | 근거 |
|---|---|---|
| 시드 번호 / 랜덤 / 고정 | **유지, 값 변경 없음** | latent에 더해지는 노이즈를 결정. 같은 원본+프롬프트로 같은 결과 재현에 필수 |
| 샘플링 스텝 (Steps) | **유지, 값 변경 없음** | ComfyUI KSampler는 `denoise<1`일 때 `int(steps × denoise)`스텝만 실행합니다(강도 0.65 × 24 ≈ 15스텝). 값을 못 바꾸면 사용자가 직접 조정해야 합니다 |
| 프롬프트 충실도 (CFG) | **유지, 값 변경 없음** | 값에 따라 원본 이탈도가 급격히 달라져 img2img에서 오히려 중요 |
| 샘플러 / 스케줄러 | **유지, 값 변경 없음** | 노이즈 제거 방식이 원본 보존 형태에 직접 영향 |
| 디노이즈 (`denoiseSpinBox`) | **숨김** → 강도 슬라이더로 대체 | txt2img `1.0` = 완전 재구성이지만 img2img `0.65` = 원본 유지로 의미가 정반대(§2.3) |
| FaceDetailer | **유지, 값 변경 없음, 경고 문구만** | 실사 사진 → img2img 시 얼굴이 가장 망가지는 구간이라 보정 가치가 txt2img보다 큼 |

#### 2.8.2 FaceDetailer 경고 문구

img2img에서 FD를 켠 경우 KSampler가 2회 연속 실행됩니다.

```
원본 → [img2img KSampler (강도 0.65)] → 이미지A → [FaceDetailer KSampler (denoise 0.40)] → 최종
```

얼굴 영역만 추가로 0.40 재구성되므로 원본 얼굴이 이미 선명한 사진에서는 얼굴만 과하게 다듬어질 수 있습니다. **값을 자동 조정하지 않고** 아래 조건부 문구로만 안내합니다.

| 상태 | `img2imgFdWarningLabel` 표시 |
|---|---|
| txt2img + FD OFF | 숨김 |
| txt2img + FD ON | 숨김 (기존 동작과 동일) |
| **img2img + FD ON** | **표시** |
| img2img + FD OFF | 숨김 |

표시 문구:

> ⚠️ img2img 변환과 FaceDetailer가 연달아 적용됩니다. 원본 얼굴이 이미 선명하면 FaceDetailer를 꺼 두세요.

- 라벨은 `facedetailerPanel` 최상단에 배치합니다(후보 a). "FaceDetailer를 켰는데 왜 이 경고가 붙지" 하는 사용자에게 가장 가까운 위치입니다.
- `setWordWrap(True)` 적용, 경고색 스타일시트를 적용합니다.
- 갱신 트리거는 2곳입니다: `img2imgModeRadio.toggled`, `facedetailerCheckBox.toggled`. 양쪽 모두 `_update_fd_img2img_warning()`을 호출하며, FD 체크 상태만 읽어 표시 여부를 결정합니다.
- FD 슬라이더 값(denoise 0.40, steps 20 등)은 **전혀 건드리지 않습니다**.

#### 2.8.3 채택하지 않은 대안

| 대안 | 불채택 이유 |
|---|---|
| 모드별 프리셋 자동 적용 (img2img 전환 시 Steps 24→36, CFG 3.5→5.0, FD denoise 0.40→0.30) | 사용자가 의도한 값을 덮어씁니다. img2img는 모델·원본에 따라 적정값이 달라 자동 조정이 위험합니다 |
| FaceDetailer를 img2img에서 자동 비활성화 | 실사 사진 보정이라는 핵심 사용 시나리오를 차단합니다. 안내만 하고 선택은 사용자에게 맡깁니다 |

---

---

## 3. 변경 대상 파일 (7개)

| # | 절대 경로 | 변경 성격 |
|---|---|---|
| 1 | `c:\Users\donian\Desktop\python\ComfyCraft_AI_Easy_Studio\app\core\api_client.py` | `upload_image()` 추가 |
| 2 | `c:\Users\donian\Desktop\python\ComfyCraft_AI_Easy_Studio\app\sections\generation.py` | `convert_workflow_to_img2img()` 추가, `generate()` 분기 |
| 3 | `c:\Users\donian\Desktop\python\ComfyCraft_AI_Easy_Studio\assets\ui\main.ui` | img2img 카드 위젯 추가 (단일 소스) |
| 4 | `c:\Users\donian\Desktop\python\ComfyCraft_AI_Easy_Studio\assets\ui\main_ui.py` | 위 UI와 이름/구조 동기화 |
| 5 | `c:\Users\donian\Desktop\python\ComfyCraft_AI_Easy_Studio\main.py` | snapshot 확장, 핸들러, UI 비활성화 목록, 모드별 프롬프트 향상 |
| 6 | `c:\Users\donian\Desktop\python\ComfyCraft_AI_Easy_Studio\app\sections\prompt.py` | img2img용 프롬프트 향상 지침 추가 |
| 7 | `c:\Users\donian\Desktop\python\ComfyCraft_AI_Easy_Studio\tests\test_img2img_support.py` | 신규 테스트 |

> `app/sections/prompt.py`는 2.7의 모드별 향상 지침이 필요할 때만 최소 수정합니다. 기존 txt2img 지침 경로는 변경하지 않습니다.

> 기존 사용자 변경분(`workflows/app_config.json` 수정, `outputs/*.png` 삭제)은 건드리지 않으며 커밋 대상에서 제외합니다.

---

## 4. 단계별 상세 설계

### 단계 1 — `app/core/api_client.py`

#### 4.1.1 모듈 레벨 MIME 헬퍼

`ComfyUIApiClient` 클래스 정의 위, `BaseApiClient` 바로 아래에 배치합니다. 추가 import는 `from pathlib import Path` 하나입니다.

```python
_IMAGE_MIME_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".bmp": "image/bmp",
}


def _guess_mime(suffix: str) -> str:
    """확장자를 MIME 타입으로 변환합니다."""
    return _IMAGE_MIME_TYPES.get(suffix, "application/octet-stream")
```

#### 4.1.2 `ComfyUIApiClient.upload_image()` 추가

`view()` 메서드 바로 아래에 위치시키고 기존 메서드 스타일을 따릅니다.

```python
def upload_image(self, image_path: Any, timeout: Any = 30) -> requests.Response:
    """ComfyUI /upload/image 로 이미지를 multipart 업로드합니다.

    Args:
        image_path: 업로드할 로컬 이미지 경로 (Path 또는 str).
        timeout: requests 타임아웃.
    Returns:
        ComfyUI 응답. 성공 시 JSON에 name/subfolder/type 포함.
    """
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"업로드할 이미지를 찾을 수 없습니다: {path}")

    files = {"image": (path.name, path.read_bytes(), _guess_mime(path.suffix.lower()))}
    data = {"type": "input", "overwrite": "true"}

    return self.session.post(
        self.build_url('/upload/image'),
        files=files,
        data=data,
        timeout=timeout,
    )
```

#### 4.1.3 설계 근거

- `BaseApiClient.post()`는 `json=` 키워드가 강제되어 multipart에 재사용할 수 없으므로 `session.post`를 직접 호출합니다.
- 재시도 어댑터의 `allowed_methods`에 `POST`가 포함되어 큰 파일 업로드도 자동 재시도됩니다.
- 기존 `max_retries=3` 정책과 일치합니다.

---

### 단계 2 — `app/sections/generation.py`

#### 4.2.1 모듈 레벨 변환 함수

테스트 가능하도록 워커 클래스 밖, `build_generation_snapshot()` 아래에 배치합니다. `json` 모듈은 이미 import되어 있어 추가 import가 필요하지 않습니다.

**VAE 링크 해석 헬퍼**

```python
def _resolve_vae_link(workflow: Dict[str, Any]) -> List[Any]:
    """워크플로우에서 사용 중인 VAE 출력 링크를 추출합니다.

    KSampler.model 경로가 UNet/Checkpoint 등으로 다양하므로
    VAEDecode 노드의 vae 입력을 우선 사용하고, 없으면 로더 노드로 폴백합니다.
    """
    for node in workflow.values():
        if isinstance(node, dict) and node.get("class_type") == "VAEDecode":
            vae = node.get("inputs", {}).get("vae")
            if isinstance(vae, list) and len(vae) == 2:
                return [str(vae[0]), int(vae[1])]

    for node_id, node in workflow.items():
        if isinstance(node, dict) and node.get("class_type") == "VAELoader":
            return [str(node_id), 0]

    for node_id, node in workflow.items():
        if isinstance(node, dict) and node.get("class_type") == "CheckpointLoaderSimple":
            return [str(node_id), 2]

    raise ValueError("VAE 출력 링크를 찾을 수 없어 img2img 변환을 실패했습니다.")
```

**변환 본체**

```python
def convert_workflow_to_img2img(
    workflow: Dict[str, Any],
    image_name: str,
    subfolder: str = "",
    upload_type: str = "input",
) -> Dict[str, Any]:
    """txt2img 워크플로우를 img2img 워크플로우로 변환합니다.

    - EmptyLatentImage 노드를 제거합니다.
    - LoadImage + VAEEncode 노드를 추가합니다.
    - KSampler.latent_image 를 VAEEncode 출력으로 재연결합니다.

    원본 dict 는 변경하지 않고 새 dict 를 반환합니다.
    """
    if not isinstance(workflow, dict) or not workflow:
        raise ValueError("변환할 워크플로우가 비어 있습니다.")
    if not image_name:
        raise ValueError("참조 이미지 이름이 비어 있습니다.")

    converted: Dict[str, Any] = json.loads(json.dumps(workflow))

    latent_node_id = None
    for node_id, node in converted.items():
        if isinstance(node, dict) and node.get("class_type") == "EmptyLatentImage":
            latent_node_id = node_id
            break
    if latent_node_id is None:
        raise ValueError("EmptyLatentImage 노드를 찾을 수 없어 img2img 변환을 실패했습니다.")

    ksampler_id = None
    for node_id, node in converted.items():
        if isinstance(node, dict) and node.get("class_type") == "KSampler":
            ksampler_id = node_id
            break
    if ksampler_id is None:
        raise ValueError("KSampler 노드를 찾을 수 없어 img2img 변환을 실패했습니다.")

    vae_link = _resolve_vae_link(converted)
    converted.pop(latent_node_id, None)

    numeric_ids = [int(k) for k in converted if str(k).lstrip("-").isdigit()]
    next_id = (max(numeric_ids) + 1) if numeric_ids else 1
    load_image_id = str(next_id)
    vae_encode_id = str(next_id + 1)

    load_inputs: Dict[str, Any] = {"image": image_name, "upload": upload_type}
    if subfolder:
        load_inputs["subfolder"] = subfolder

    converted[load_image_id] = {
        "inputs": load_inputs,
        "class_type": "LoadImage",
        "_meta": {"title": "Load Image (img2img)"},
    }
    converted[vae_encode_id] = {
        "inputs": {"pixels": [load_image_id, 0], "vae": vae_link},
        "class_type": "VAEEncode",
        "_meta": {"title": "VAE Encode (img2img)"},
    }
    converted[ksampler_id]["inputs"]["latent_image"] = [vae_encode_id, 0]
    return converted
```

**설계 근거**
- `json.loads(json.dumps(...))` 깊은 복사로 호출측 워크플로우 오염을 방지합니다.
- 새 노드 ID를 `max(정수 키) + 1`로 할당해 FaceDetailer 주입분 ID와 충돌하지 않습니다.
- KSampler가 여러 개면 첫 번째를 선택하며, 이는 FaceDetailer 주입 전의 주 샘플러입니다(§4.2.3 참조).

---


#### 4.2.2 `generate()` 내 img2img 분기

기존 `workflow = self.build_workflow(...)` 및 `self._validate_workflow(workflow)` 직전 지점에 삽입합니다.

```python
        # 4-5️⃣ img2img 모드 처리 (denoise 보정 → build_workflow → 변환 순서 준수)
        if snapshot.get("mode") == "img2img":
            source_path = (snapshot.get("source_path") or "").strip()
            if not source_path:
                raise RuntimeError(
                    "참조 이미지가 선택되지 않았습니다. img2img 모드에서는 이미지가 필요합니다."
                )

            denoise = float(snapshot.get("denoise", 1.0) or 1.0)
            if denoise < 0.05:
                denoise = 0.05
                self.emit_log("[img2img] 변환 강도가 0.05 미만이라 0.05로 올립니다.")
            if denoise >= 1.0:
                self.emit_log("[img2img] 변환 강도가 1.00이라 원본이 거의 재구성됩니다.")
            snapshot["denoise"] = denoise

            uploaded = self.comfy_api.upload_image(source_path, timeout=30)
            uploaded.raise_for_status()
            try:
                image_info = uploaded.json()
            except ValueError:
                raise RuntimeError("ComfyUI가 업로드 결과를 올바르게 반환하지 않았습니다.")

            image_name = image_info.get("name")
            if not image_name:
                raise RuntimeError("ComfyUI 업로드 응답에 이미지 이름이 없습니다.")

            workflow = self.build_workflow(profile, model_name, final_positive_prompt, negative, seed)
            workflow = convert_workflow_to_img2img(
                workflow,
                image_name=image_name,
                subfolder=image_info.get("subfolder", "") or "",
                upload_type=image_info.get("type", "input") or "input",
            )
            self.emit_log(
                f"[img2img] 참조 이미지 반영 완료: {image_name} (denoise {denoise:.2f})"
            )
        else:
            workflow = self.build_workflow(profile, model_name, final_positive_prompt, negative, seed)

        self._validate_workflow(workflow)
```

**반드시 지킬 순서 제약**

1. denoise 보정은 `build_workflow()` **호출 이전**에 `snapshot["denoise"]`에 기록해야 합니다. `build_workflow()`가 `s["denoise"]`를 템플릿 `__DENOISE__`에 주입하므로, 순서가 바뀌면 보정값이 KSampler에 반영되지 않습니다.
2. `self.comfy_api`는 `generate()` 상단에서 초기화와 연결 확인이 끝난 상태이므로 그대로 사용합니다.
3. 업로드 재시도는 어댑터가 담당하므로 별도 재시도 루프를 넣지 않습니다.
4. txt2img 분기는 기존 코드와 동일하게 유지하여 회귀 위험을 제거합니다.

#### 4.2.3 FaceDetailer와의 적용 순서

`build_workflow()` 내부에서 FaceDetailer가 마지막에 주입되므로 두 순서가 가능합니다.

| 순서 | 장점 | 위험 |
|---|---|---|
| **A. FaceDetailer 주입 후 img2img 변환 (채택)** | 변환 지점이 한 곳이고 기존 FD 동작을 완전 보존 | 변환은 첫 KSampler를 선택하므로 FD가 만든 KSampler2는 건드리지 않음 |
| B. img2img 변환 후 FaceDetailer 주입 | FD가 최종 latent 기준 | `_inject_facedetailer`가 단일 KSampler를 가정해 별도 수정 필요 |

**채택: A.** `_inject_facedetailer`는 `VAEDecode` 입력을 기준으로 KSampler를 찾으므로 `EmptyLatentImage` 제거의 영향을 받지 않습니다. txt2img + FaceDetailer 기존 동작에 회귀가 없습니다.

---


### 단계 3 — `assets/ui/main.ui`

#### 4.3.1 배치 위치 (2곳 삽입 — 배치안 B)

`step2Layout` 내부에 **두 곳**에 삽입합니다. `advancedContentWidget`는 수정하지 않습니다.

| 삽입 지점 | 위치 | 추가 위젯 | 표시 조건 |
|---|---|---|---|
| **①** | `step2HeaderLayout` 의 `</layout>` 바로 뒤 (현재 532행) — 헤더와 모델 선택 사이 | `img2imgModeRow` (라디오 2개) | **항상 보임** |
| **②** | `dimensionContainer` 의 `</item>` 바로 뒤 (현재 693행) — 크기 입력과 고급 설정 사이 | `img2imgCard` (선택/제거/미리보기/정보/강도) | **img2img 모드일 때만** |
| **③** | `facedetailerPanel` 최상단 (FaceDetailer 카드 내부) | `img2imgFdWarningLabel` | img2img + FD ON |

- ①번 위치는 "무엇으로 만들 것인가"(최상위 분기)를 모델 선택 직전에 두는 것으로, 카드 헤더의 "핵심 생성 옵션" 문구와 자연스럽게 이어집니다.
- ②번 위치는 `dimensionContainer`(가로/세로) 바로 아래이므로 "원본 크기가 출력 크기로 적용된다"는 흐름이 세로로 이어져 읽힙니다.
- ③번 위치는 FD를 켜는 행위 직후 가장 가까운 지점입니다(§2.8.2).

#### 4.3.2 추가 위젯 명세

**① 모드 세그먼트 (항상 보임)**

| objectName | 타입 | 역할 | 기본값 |
|---|---|---|---|
| `img2imgModeRow` | `QWidget` | 라디오 2개를 담는 컨테이너 | 보임 |
| `txt2imgModeRadio` | `QRadioButton` | txt2img 경로 선택 | `● 텍스트로 만들기` (checked) |
| `img2imgModeRadio` | `QRadioButton` | img2img 경로 선택 | `🖼️ 이미지로 변환` |
| `img2imgModeHintLabel` | `QLabel` | 모드별 1줄 안내 | `프롬프트만으로 새 이미지를 만듭니다.` |

**② img2img 옵션 카드 (img2img 모드에서만 표시)**

| objectName | 타입 | 역할 | 기본값 |
|---|---|---|---|
| `img2imgCard` | `QFrame` | StyledPanel 컨테이너 | 숨김 |
| `img2imgCardTitle` | `QLabel` | 카드 제목 | `🖼️ 참조 이미지` |
| `img2imgSelectButton` | `QPushButton` | 파일 선택 다이얼로그 | `🖼️ 이미지 선택` |
| `img2imgClearButton` | `QPushButton` | 선택 해제 | `🗑️ 제거` |
| `img2imgPreviewLabel` | `QLabel` | 썸네일 (비율 유지 축소) | `(선택된 이미지 없음)` |
| `img2imgInfoLabel` | `QLabel` | 파일명 · 가로×세로 | 빈 문자열 |
| `img2imgStrengthLabel` | `QLabel` | 강도 제목 | `변환 강도 (낮을수록 원본 유지)` |
| `img2imgStrengthSlider` | `QSlider` | 강도 입력 (5~100 → 0.05~1.00) | 65 |
| `img2imgStrengthValueLabel` | `QLabel` | 강도 수치 | `0.65` |

**③ FaceDetailer 경고 라벨**

| objectName | 타입 | 역할 | 기본값 |
|---|---|---|---|
| `img2imgFdWarningLabel` | `QLabel` | img2img+FD 조합 경고 | 숨김, wordWrap |

**기존 위젯 변경**

| objectName | 변경 |
|---|---|
| `denoiseCol` (디노이즈 라벨+SpinBox 컨테이너) | img2img 모드에서 `setVisible(False)`, txt2img에서 `setVisible(True)` |

> 두 라디오는 같은 부모(`img2imgModeRow`)에 있어 Qt가 자동으로 상호 배타(mutually exclusive) 처리합니다. 별도 그룹 박스를 만들지 않습니다.

#### 4.3.3 XML 삽입 스니펫 (개념)

**삽입 ① — `step2HeaderLayout` 의 `</layout>` 바로 뒤**

```xml
<item>
 <widget class="QWidget" name="img2imgModeRow" native="true">
  <layout class="QVBoxLayout" name="img2imgModeRowLayout">
   <property name="spacing"><number>4</number></property>
   <item>
    <layout class="QHBoxLayout" name="img2imgRadioRow">
     <item>
      <widget class="QRadioButton" name="txt2imgModeRadio">
       <property name="cursor"><cursorShape>PointingHandCursor</cursorShape></property>
       <property name="text"><string>● 텍스트로 만들기</string></property>
       <property name="checked"><bool>true</bool></property>
      </widget>
     </item>
     <item>
      <widget class="QRadioButton" name="img2imgModeRadio">
       <property name="cursor"><cursorShape>PointingHandCursor</cursorShape></property>
       <property name="toolTip"><string>선택한 이미지를 바탕으로 프롬프트로 변형합니다. (변환 강도가 낮을수록 원본 유지)</string></property>
       <property name="text"><string>🖼️ 이미지로 변환</string></property>
      </widget>
     </item>
     <item>
      <spacer name="img2imgModeSpacer">
       <property name="orientation"><enum>Qt::Orientation::Horizontal</enum></property>
       <property name="sizeHint" stdset="0"><size><width>0</width><height>0</height></size></property>
      </spacer>
     </item>
    </layout>
   </item>
   <item>
    <widget class="QLabel" name="img2imgModeHintLabel">
     <property name="text"><string>프롬프트만으로 새 이미지를 만듭니다.</string></property>
    </widget>
   </item>
  </layout>
 </widget>
</item>
```

**삽입 ② — `dimensionContainer` 의 `</item>` 바로 뒤**

```xml
<item>
 <widget class="QFrame" name="img2imgCard">
  <property name="visible"><bool>false</bool></property>
  <property name="frameShape"><enum>QFrame::Shape::StyledPanel</enum></property>
  <layout class="QVBoxLayout" name="img2imgLayout">
   <property name="spacing"><number>8</number></property>
   <property name="leftMargin"><number>12</number></property>
   <property name="topMargin"><number>10</number></property>
   <property name="rightMargin"><number>12</number></property>
   <property name="bottomMargin"><number>10</number></property>
   <item>
    <widget class="QLabel" name="img2imgCardTitle">
     <property name="text"><string>🖼️ 참조 이미지</string></property>
    </widget>
   </item>
   <item>
    <layout class="QHBoxLayout" name="img2imgButtonRow">
     <item>
      <widget class="QPushButton" name="img2imgSelectButton">
       <property name="cursor"><cursorShape>PointingHandCursor</cursorShape></property>
       <property name="text"><string>🖼️ 이미지 선택</string></property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="img2imgClearButton">
       <property name="cursor"><cursorShape>PointingHandCursor</cursorShape></property>
       <property name="text"><string>🗑️ 제거</string></property>
      </widget>
     </item>
    </layout>
   </item>
   <item>
    <widget class="QLabel" name="img2imgPreviewLabel">
     <property name="minimumSize"><size><width>0</width><height>140</height></size></property>
     <property name="text"><string>(선택된 이미지 없음)</string></property>
     <property name="alignment"><set>Qt::AlignmentFlag::AlignCenter</set></property>
    </widget>
   </item>
   <item>
    <widget class="QLabel" name="img2imgInfoLabel">
     <property name="text"><string/></property>
    </widget>
   </item>
   <item>
    <layout class="QHBoxLayout" name="img2imgStrengthRow">
     <item>
      <widget class="QLabel" name="img2imgStrengthLabel">
       <property name="text"><string>변환 강도 (낮을수록 원본 유지)</string></property>
      </widget>
     </item>
     <item>
      <widget class="QSlider" name="img2imgStrengthSlider">
       <property name="minimum"><number>5</number></property>
       <property name="maximum"><number>100</number></property>
       <property name="value"><number>65</number></property>
       <property name="orientation"><enum>Qt::Orientation::Horizontal</enum></property>
      </widget>
     </item>
     <item>
      <widget class="QLabel" name="img2imgStrengthValueLabel">
       <property name="text"><string>0.65</string></property>
       <property name="minimumSize"><size><width>44</width><height>0</height></size></property>
       <property name="alignment"><set>Qt::AlignmentFlag::AlignRight|Qt::AlignmentFlag::AlignTrailing|Qt::AlignmentFlag::AlignVCenter</set></property>
      </widget>
     </item>
    </layout>
   </item>
  </layout>
 </widget>
</item>
```

**삽입 ③ — `facedetailerPanel` 최상단**

```xml
<item>
 <widget class="QLabel" name="img2imgFdWarningLabel">
  <property name="visible"><bool>false</bool></property>
  <property name="wordWrap"><bool>true</bool></property>
  <property name="text"><string>⚠️ img2img 변환과 FaceDetailer가 연달아 적용됩니다. 원본 얼굴이 이미 선명하면 FaceDetailer를 꺼 두세요.</string></property>
  <property name="styleSheet"><string notr="true">color: #b8860b;</string></property>
 </widget>
</item>
```

슬라이더는 정수 5~100(0.05~1.00)을 사용하고, `main.py`에서 `/100`으로 나누어 `snapshot["denoise"]`에 넣습니다. `FaceDetailer` 슬라이더와 동일한 ValueLabel 동기화 패턴을 따릅니다.

#### 4.3.4 `main_ui.py` 동기화

`assets/ui/main_ui.py`는 Qt Designer 생성 산출물이며 런타임에서는 로드되지 않지만, 동일 이름 위젯 참조가 정적 분석에 노출되므로 `setupUi()`에 동일한 위젯 생성 블록을 추가해 동기화합니다.

- ① `self.step2HeaderLayout` 생성 코드 뒤에 `img2imgModeRow` 블록을 만들고 `self.step2Layout.addWidget(self.img2imgModeRow)`로 배치합니다.
- ② `self.dimensionContainer` 생성 코드 뒤에 `img2imgCard` 블록을 만들고 `self.step2Layout.addWidget(self.img2imgCard)`로 배치합니다.
- ③ `self.facedetailerPanel` 레이아웃 맨 앞에 `img2imgFdWarningLabel`을 추가하고 `setVisible(False)`로 둡니다.
- 라디오 두 개는 `self.img2imgModeRadio` 그룹에 묶어(`btnGroup`) 상호 배타를 명시적으로 보장합니다.

---


### 단계 4 — `main.py`

#### 4.4.1 모드 상수

`FACEDETAILER_SLIDER_SPECS` 정의부 아래에 추가합니다.

```python
IMAGE_FILE_FILTER = (
    "이미지 파일 (*.png *.jpg *.jpeg *.webp *.bmp);;모든 파일 (*.*)"
)
```

#### 4.4.2 상태 변수

컨트롤러 초기화부에서 인스턴스 상태를 초기화합니다. txt2img로 돌아왔을 때 폭·높이를 복구하기 위한 이전 값도 함께 보관합니다.

```python
self._img2img_source_path: str = ""
self._img2img_source_size: tuple = (0, 0)      # (width, height)
self._img2img_prev_size: tuple = (0, 0)         # 비활성화 전 폭·높이 보관용
```

#### 4.4.3 이벤트 연결

기존 시그널 연결부(`advancedToggleBtn` 연결부 근처)에 추가합니다.

```python
img2img_radio = self.find(QRadioButton, "img2imgModeRadio")
if img2img_radio:
    img2img_radio.toggled.connect(self._on_img2img_mode_changed)

img2img_select = self.find(QPushButton, "img2imgSelectButton")
if img2img_select:
    img2img_select.clicked.connect(self._on_img2img_select)

img2img_clear = self.find(QPushButton, "img2imgClearButton")
if img2img_clear:
    img2img_clear.clicked.connect(self._on_img2img_clear)

img2img_slider = self.find(QSlider, "img2imgStrengthSlider")
if img2img_slider:
    img2img_slider.valueChanged.connect(self._on_img2img_strength_changed)

# FaceDetailer 체크 상태가 바뀌면 img2img 조합 경고 문구를 갱신합니다. (§2.8.2)
fd_check = self.find(QCheckBox, "facedetailerCheckBox")
if fd_check:
    fd_check.toggled.connect(lambda _checked: self._update_fd_img2img_warning())
```

#### 4.4.4 핸들러

`capture_snapshot()` 바로 위 영역에 배치합니다.

```python
def _on_img2img_mode_changed(self, checked: bool):
    """img2img 모드 전환 시 카드 표시, 안내 문구, 디노이즈 컨트롤, 폭·높이 잠금,
    FaceDetailer 경고 문구를 함께 갱신합니다.

    txt2img로 되돌릴 때 선택한 참조 이미지는 유지합니다(§2.2 UI 동작 규칙).
    """
    card = self.find(QFrame, "img2imgCard")
    if card is not None:
        card.setVisible(checked)

    hint = self.find(QLabel, "img2imgModeHintLabel")
    if hint is not None:
        hint.setText(
            "선택한 이미지를 바탕으로 프롬프트로 변형합니다. (변환 강도가 낮을수록 원본 유지)"
            if checked
            else "프롬프트만으로 새 이미지를 만듭니다."
        )

    # 디노이즈 SpinBox는 txt2img 전용. img2img에서는 전용 강도 슬라이더를 쓴다. (§2.3)
    denoise_col = self.find(QWidget, "denoiseCol")
    if denoise_col is not None:
        denoise_col.setVisible(not checked)

    self._apply_img2img_size_lock(checked)
    self._update_fd_img2img_warning()


def _update_fd_img2img_warning(self):
    """img2img + FaceDetailer 동시 활성화 시 경고 문구를 표시합니다. (§2.8.2)

    FaceDetailer의 어떤 파라미터도 변경하지 않고, 표시 여부만 갱신합니다.
    """
    label = self.find(QLabel, "img2imgFdWarningLabel")
    if label is None:
        return

    img2img_radio = self.find(QRadioButton, "img2imgModeRadio")
    fd_check = self.find(QCheckBox, "facedetailerCheckBox")

    is_img2img = bool(img2img_radio and img2img_radio.isChecked())
    is_fd_on = bool(fd_check and fd_check.isChecked())
    label.setVisible(is_img2img and is_fd_on)
```

```python
def _apply_img2img_size_lock(self, locked: bool):
    """img2img 모드에서는 폭·높이를 비활성화하고 원본 크기로 덮어씁니다."""
    width_spin = self.find(QSpinBox, "widthSpinBox")
    height_spin = self.find(QSpinBox, "heightSpinBox")
    if width_spin is None or height_spin is None:
        return

    if locked:
        if self._img2img_prev_size == (0, 0):
            self._img2img_prev_size = (width_spin.value(), height_spin.value())
        width_spin.setEnabled(False)
        height_spin.setEnabled(False)
        if self._img2img_source_size != (0, 0):
            width_spin.setValue(self._img2img_source_size[0])
            height_spin.setValue(self._img2img_source_size[1])
    else:
        width_spin.setEnabled(True)
        height_spin.setEnabled(True)
        if self._img2img_prev_size != (0, 0):
            width_spin.setValue(self._img2img_prev_size[0])
            height_spin.setValue(self._img2img_prev_size[1])
            self._img2img_prev_size = (0, 0)


def _on_img2img_strength_changed(self, value: int):
    """변환 강도 슬라이더를 0.05~1.00 수치 라벨과 동기화합니다."""
    label = self.find(QLabel, "img2imgStrengthValueLabel")
    if label is not None:
        label.setText(f"{value / 100.0:.2f}")
```

```python
def _on_img2img_select(self):
    """참조 이미지 파일을 선택하고 미리보기·파일 정보를 갱신합니다."""
    path, _ = QFileDialog.getOpenFileName(
        self.window, "참조 이미지 선택", "", IMAGE_FILE_FILTER
    )
    if not path:
        return

    self._img2img_source_path = path
    self._update_img2img_preview()
    self._apply_img2img_size_lock(True)   # 원본 크기를 출력 크기로 반영
    self.append_log(f"[img2img] 참조 이미지 선택: {path}")
```

```python
def _on_img2img_clear(self):
    """선택된 참조 이미지를 초기화합니다."""
    self._img2img_source_path = ""
    self._img2img_source_size = (0, 0)
    self._update_img2img_preview()


def _update_img2img_preview(self):
    """참조 이미지 썸네일과 파일 정보(파일명 · 가로×세로)를 표시합니다."""
    preview = self.find(QLabel, "img2imgPreviewLabel")
    info = self.find(QLabel, "img2imgInfoLabel")
    if preview is None:
        return

    if not self._img2img_source_path:
        preview.setText("(선택된 이미지 없음)")
        preview.setPixmap(QPixmap())
        if info is not None:
            info.setText("")
        self._img2img_source_size = (0, 0)
        return

    # 원본 파일은 수정하지 않고, 메모리상 QPixmap으로만 축소 표시합니다.
    try:
        pixmap = QPixmap(self._img2img_source_path)
    except Exception:
        preview.setText("(이미지를 불러올 수 없습니다)")
        if info is not None:
            info.setText(Path(self._img2img_source_path).name)
        return

    if pixmap.isNull():
        preview.setText("(이미지를 불러올 수 없습니다)")
        if info is not None:
            info.setText(Path(self._img2img_source_path).name)
        return

    self._img2img_source_size = (pixmap.width(), pixmap.height())
    preview.setPixmap(
        pixmap.scaled(
            320, 320,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
    )
    if info is not None:
        info.setText(f"{Path(self._img2img_source_path).name} · {pixmap.width()}×{pixmap.height()}")
```

필요 import: `QFileDialog`, `QSlider` (PySide6.QtWidgets), `QPixmap`, `Qt`, `Path`.

---


#### 4.4.5 `capture_snapshot()` 확장

기존 `snapshot = { ... }` 딕셔너리 앞에 검증을 추가합니다.

```python
        img2img_radio = self.find(QRadioButton, "img2imgModeRadio")
        is_img2img = bool(img2img_radio and img2img_radio.isChecked())
        source_path = self._img2img_source_path if is_img2img else ""
        if is_img2img and not source_path:
            raise ValueError("img2img 모드에서는 참조 이미지를 먼저 선택해주세요.")
```

그리고 `snapshot` 딕셔너리 내부에 세 키를 추가합니다.

```python
            "mode": "img2img" if is_img2img else "txt2img",
            "source_path": source_path,
            # 변환 강도 전용 컨트롤 값을 denoise로 변환해 전달 (txt2img는 None)
            "img2img_strength": (
                self.find(QSlider, "img2imgStrengthSlider").value() / 100.0
                if is_img2img and self.find(QSlider, "img2imgStrengthSlider")
                else None
            ),
```

그리고 `snapshot["denoise"]`을 **이미 계산된 값**으로 덮어씁니다.

```python
        if is_img2img:
            snapshot["denoise"] = snapshot["img2img_strength"]
```

이렇게 하면 워커는 `snapshot["denoise"]`만 보면 되어 `build_workflow()`와 템플릿 경로가 그대로 유지됩니다(§4.2.2의 순서 제약이 자동 충족).

**설계 근거**
- 기존 `capture_snapshot()`은 Z-ANIME 스타일 미선택 시 이미 `ValueError`를 던지고, 호출측이 이를 경고 대화상자로 처리합니다. 동일 패턴을 재사용하므로 예외 처리 코드 추가가 필요 없습니다.
- 워커 측 검증(§4.2.2)과 이중 방어선을 유지합니다.
- txt2img의 기존 프롬프트 필수 검사는 그대로 두고, img2img에서만 프롬프트 없이 생성 가능하도록 분기합니다(§2.5).

#### 4.4.6 `_set_ui_enabled()` 목록 확장

`targets` 리스트의 `"denoiseSpinBox"` 항목 뒤에 추가합니다.

```python
                "txt2imgModeRadio",
                "img2imgModeRadio",
                "img2imgSelectButton",
                "img2imgClearButton",
                "img2imgStrengthSlider",
```

> `"denoiseSpinBox"` 항목은 그대로 유지합니다. img2img 모드에서는 `denoiseCol` 컨테이너가 숨겨지므로, `denoiseSpinBox`를 `targets`에서 빼면 txt2img에서 생성 중 잠금이 풀립니다.

---

### 단계 5 — `tests/test_img2img_support.py` (신규)

기존 테스트는 `tests/test_core_components.py`, `tests/test_project_basics.py`이며 `unittest` 기반입니다. 같은 스타일로 작성합니다.

#### 4.5.1 테스트 케이스 목록

| # | 테스트 이름 | 검증 내용 |
|---|---|---|
| 1 | `test_upload_image_multipart_format` | `/upload/image`로 multipart POST하고 `files["image"]`가 (파일명, 바이트, MIME) 튜플인지 |
| 2 | `test_upload_image_missing_file` | 없는 경로에 `FileNotFoundError` 발생 |
| 3 | `test_conversion_wires_latent_to_vae_encode` | 변환 후 `KSampler.latent_image`가 새 `VAEEncode`를 가리키는지 |
| 4 | `test_conversion_removes_empty_latent` | 변환 후 `EmptyLatentImage`가 없는지 |
| 5 | `test_conversion_load_image_name` | `LoadImage.inputs.image`가 업로드 응답 `name`과 일치하는지 |
| 6 | `test_conversion_does_not_mutate_input` | 입력 dict 원본이 변경되지 않는지 |
| 7 | `test_conversion_requires_ksampler` | KSampler 없는 워크플로우에서 `ValueError` |
| 8 | `test_all_templates_are_convertible` | 4개 템플릿 각각에 변환 적용 후 3~5 통과 |
| 9 | `test_missing_source_raises_in_snapshot` | img2img 라디오 선택 + 이미지 미선택 시 `capture_snapshot()`이 `ValueError` |
| 10 | `test_txt2img_snapshot_defaults` | txt2img 스냅샷이 `mode="txt2img"`, `source_path=""` 포함 |
| 11 | `test_fd_warning_visibility` | img2img+FD ON에서만 `img2imgFdWarningLabel` 표시, 그 외 숨김 |

---

#### 4.5.2 구현 예시

```python
import json
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from app.core.api_client import ComfyUIApiClient
from app.sections.generation import convert_workflow_to_img2img

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_FILES = [
    "checkpoint.json",
    "gguf_unet.json",
    "flux_gguf.json",
    "zimage.json",
]


class TestApiClientUpload(unittest.TestCase):
    def test_upload_image_multipart_format(self):
        client = ComfyUIApiClient("http://127.0.0.1:8188")
        client.session = MagicMock()
        client.session.post.return_value = MagicMock(status_code=200)

        with patch.object(Path, "exists", return_value=True), \
             patch.object(Path, "read_bytes", return_value=b"\x89PNG"):
            client.upload_image("dummy.png")

        args, kwargs = client.session.post.call_args
        self.assertTrue(args[0].endswith("/upload/image"))
        filename, payload, mime = kwargs["files"]["image"]
        self.assertEqual(filename, "dummy.png")
        self.assertEqual(payload, b"\x89PNG")
        self.assertEqual(mime, "image/png")
        self.assertEqual(kwargs["data"]["type"], "input")

    def test_upload_image_missing_file(self):
        client = ComfyUIApiClient("http://127.0.0.1:8188")
        client.session = MagicMock()
        with self.assertRaises(FileNotFoundError):
            client.upload_image("no_such_file_zzz.png")


class TestWorkflowConversion(unittest.TestCase):
    def test_all_templates_are_convertible(self):
        for name in TEMPLATE_FILES:
            with self.subTest(template=name):
                with open(BASE_DIR / "workflows" / name, "r", encoding="utf-8") as fh:
                    raw = json.load(fh)

                original = json.loads(json.dumps(raw))
                converted = convert_workflow_to_img2img(raw, image_name="ref.png")

                # 원본 불변 확인 (테스트 6)
                self.assertEqual(raw, original)

                classes = [n.get("class_type") for n in converted.values()]
                self.assertNotIn("EmptyLatentImage", classes)
                self.assertIn("LoadImage", classes)
                self.assertIn("VAEEncode", classes)

                ksampler = next(
                    n for n in converted.values() if n.get("class_type") == "KSampler"
                )
                latent_link = ksampler["inputs"]["latent_image"]
                self.assertEqual(converted[latent_link[0]]["class_type"], "VAEEncode")

                load = next(
                    n for n in converted.values() if n.get("class_type") == "LoadImage"
                )
                self.assertEqual(load["inputs"]["image"], "ref.png")


if __name__ == "__main__":
    unittest.main()
```

#### 4.5.3 템플릿 placeholder 처리 주의

`workflows/*.json`은 `__MODEL_NAME__` 같은 placeholder를 포함합니다. `json.dumps` 기반 깊은 복사는 이 문자열을 그대로 보존하므로 변환 테스트에는 문제가 없습니다. 통합 확인 시에는 `WorkflowManager.render_*_workflow()`로 실제 렌더링 결과를 사용합니다.

---

### 단계 6 — `app/sections/prompt.py` (모드별 프롬프트 향상)

기존 `enhance_prompt_only` 경로가 호출하는 지침 문자열에 모드 분기를 추가합니다(§2.4).

```python
IMG2IMG_ENHANCE_INSTRUCTION = (
    "다음 요청을 구체화해 이미지 생성 프롬프트로 다듬어 주세요. "
    "요청한 변화는 구체적으로 묘사하되, 요청하지 않은 원본 이미지의 주요 요소는 유지하도록 하세요. "
    "설명하지 않은 부분을 임의로 새로 만들지 마세요."
)
```

적용 지점:

- `main.py`의 `enhance_prompt_only`에서 현재 모드를 확인해 지침을 선택합니다.
- txt2img일 때는 기존 지침 문자열을 그대로 사용합니다(회귀 없음).
- 프롬프트 입력이 비어 있으면 향상 버튼을 비활성화하거나 안내 메시지를 표시합니다.

---

## 5. 의존성 및 환경

- 신규 외부 의존성 없음. `requests`, `PySide6`는 이미 사용 중입니다.
- `app/gui/ui_loader.py`의 `QUiLoader`는 `QtUiTools`를 통해 `.ui` XML을 런타임 로드하므로, 새 위젯은 표준 Qt 위젯만 사용합니다.
- Python 환경: 프로젝트 루트 `.venv`(venv) 사용.
- `main_ui.py` 동기화는 손동 일치를 우선하고, `pyside6-uic` 재생성은 검증 후 선택합니다.

---


## 6. 검증 계획

### 6.1 자동 테스트

```powershell
cd 'c:\Users\donian\Desktop\python\ComfyCraft_AI_Easy_Studio'
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe -m py_compile main.py app\core\api_client.py app\sections\generation.py tests\test_img2img_support.py
```

### 6.2 회귀 방지 확인 항목

| 항목 | 확인 방법 |
|---|---|
| txt2img 기존 동작 불변 | 변환이 img2img 분기에서만 호출됨을 코드 리뷰 + 테스트 10 |
| 4개 템플릿 모두 변환 성공 | 테스트 8 |
| FaceDetailer + img2img 조합 | 순서 A 기준 노드 ID 충돌 여부 수동 확인(§4.2.3) |
| **고급 설정 값 불변** | img2img 전환 시 Steps/CFG/시드/샘플러/스케줄러가 변경되지 않음을 §6.3-13으로 확인(§2.8.1) |
| **FaceDetailer 값 불변** | 경고 문구 표시만 되고 FD 슬라이더 값이 그대로임을 §6.3-11로 확인(§2.8.2) |
| UI 위젯 로드 성공 | `load_ui(UI_FILE)` 후 `find`로 `img2img*` / `txt2imgModeRadio` / `img2imgFdWarningLabel` 조회 확인 |
| 생성 중 위젯 잠금 | `_set_ui_enabled(False)`로 모드 라디오·선택·제거·슬라이더 5종 비활성화 확인 |
| 업로드 실패 처리 | `raise_for_status()` 및 JSON 파싱 실패 시 한국어 메시지 노출 |

### 6.3 수동 확인 시나리오

1. txt2img로 1회 생성 → 기존과 동일 결과
2. `🖼️ 이미지로 변환` 라디오 선택 → img2img 카드 표시, 가로·세로 잠금, `denoiseSpinBox` 숨김 확인
3. 참조 이미지 선택 → 썸네일·파일 정보(가로×세로) 표시, 가로·세로가 원본 크기로 변경되는지 확인
4. 이미지를 제거 → 미리보기·파일 정보·선택 경로 초기화, 폭·높이 잠금 유지 확인
5. `● 텍스트로 만들기`로 복귀 → 폭·높이 원래 값 복구, img2img 카드 숨김, `denoiseSpinBox` 재표시, **선택한 참조 이미지는 유지되는지** 확인
6. 변환 강도 0.65로 생성 → 원본 형태 유지 + 프롬프트 반영 확인
7. 변환 강도를 0.30으로 낮춰 생성 → 원본에 더 충실한 결과 확인
8. img2img 라디오 상태 + 이미지 미선택 → 생성 시도 시 "참조 이미지를 먼저 선택해주세요" 경고 확인
9. img2img에서 프롬프트를 비우고 생성 → 정상 진행되는지 확인 (txt2img는 차단되는지 확인)
10. Flux / ZImage / GGUF 모델 각각 img2img 생성 확인
11. **img2img + FaceDetailer ON → `facedetailerPanel` 상단에 경고 문구 표시 확인, FD 슬라이더 값이 그대로인지 확인**
12. **경고 문구 상태 전이 4종 확인** (img2img+FD ON → 표시 / img2img+FD OFF → 숨김 / txt2img+FD ON → 숨김 / txt2img+FD OFF → 숨김)
13. **img2img 전환 후 Steps / CFG / 시드 / 샘플러 / 스케줄러 값이 txt2img 상태 그대로 유지되는지 확인** (모드별 프리셋 미적용 검증, §2.8.1)
14. img2img + FaceDetailer 동시 활성화로 실제 생성 → 얼굴이 과하게 재구성되지 않는지 시각 확인
15. 두 모드 각각에서 프롬프트 향상 버튼 → txt2img는 새 장면 지문, img2img는 원본 유지형 지문 확인
16. 생성 중(`_set_ui_enabled(False)`) → 모드 라디오·이미지 선택·제거·강도 슬라이더가 잠기는지 확인

### 6.4 모델별 호환성 확인 기준

지원 여부를 확장자만으로 단정하지 않고, 현재 앱이 생성하는 로더·VAE·샘플러 워크플로를 기준으로 확인합니다.

| 워크플로 | 확인할 모델 |
|---|---|
| 체크포인트 (`checkpoint.json`) | SDXL 체크포인트, ERNIE-AIO, Z-Anime-AIO 등 실제 체크포인트 형식 |
| Flux GGUF (`flux_gguf.json`) | Flux 모델과 필요한 CLIP/VAE 구성 |
| GGUF/UNET (`gguf_unet.json`) | 해당 ComfyUI 로더가 실제 모델 파일을 읽는 경우 |
| Z-Image (`zimage.json`) | 현재 앱의 Z-Image 노드 및 모델 로딩 방식과 일치하는 변형 |

- Flux Schnell, AIO가 아닌 Z-Anime 등 로딩 방식이 다른 변형은 실제 ComfyUI에서 확인하기 전까지 지원을 확정하지 않습니다.
- 일반 img2img는 전체 이미지 변환이며, 특정 영역의 정밀 편집은 마스크·인페인트 같은 별도 기능 범위입니다.

### 6.5 완료 기준

- 원본 이미지 미리보기와 제거가 올바르게 동작합니다.
- 지원 대상으로 검증한 모델에서 img2img 생성이 성공합니다.
- txt2img, 기존 프롬프트 향상, FaceDetailer 및 다른 기존 기능이 회귀하지 않습니다.
- 검증하지 않은 모델 변형은 지원 대상으로 표시하지 않습니다.

---

## 7. 리스크 및 대응

| 리스크 | 영향 | 대응 |
|---|---|---|
| FaceDetailer가 추가한 KSampler2로 잘못 연결 | 얼굴 보정 결과 손실 | 변환은 첫 KSampler를 선택하며 FD는 `VAEDecode` 기준으로 찾으므로 영향 없음. §6.2에서 조합 검증 |
| ComfyUI에 `LoadImage` / `VAEEncode` 미설치 | img2img 실패 | ComfyUI 기본 제공 노드. 서버 오류는 기존 `error` 시그널로 전달 |
| 비표준 이미지 포맷 | MIME 오류 | `QFileDialog` 필터로 확장자 제한 + `application/octet-stream` 폴백 |
| 큰 이미지 업로드 지연 | 타임아웃 | 타임아웃 30초 + 세션 레벨 자동 재시도 |
| 템플릿에 `EmptyLatentImage`가 없는 모델 추가 | 변환 실패 | 명확한 `ValueError` 메시지로 즉시 안내 |
| 원본 크기가 매우 큰 이미지 | `widthSpinBox`/`heightSpinBox` 상한 초과로 값이 잘림 | 잠금 시 `setValue` 결과를 다시 읽어 클램프된 값을 `snapshot["width"]/["height"]`에 사용 |
| 폭·높이 잠금 후 사용자가 txt2img로 복귀하지 않음 | 다음 실행에 이전 크기가 남음 | 모드 전환 시 항상 `_apply_img2img_size_lock(False)`로 복구 경로를 보장 |
| img2img에서 프롬프트가 비어 있음 | 빈 프롬프트로 시작하는 모델은 품질 저하 | §2.5에 따라 허용하되 UI 힌트에 "변환만 원할 때는 비워 두어도 됩니다" 안내 |
| **img2img + FaceDetailer 이중 KSampler로 얼굴 과다 재구성** | 원본 얼굴이 선명한 사진에서 얼굴만 부자연스럽게 변형 | 값 자동 조정 대신 `img2imgFdWarningLabel` 경고 문구로만 안내(§2.8.2). FD 슬라이더 기본값 0.40은 그대로 유지 |
| **img2img에서 `steps`가 낮게 설정됨** | `int(steps × 강도)`가 더 작아져 변환이 뭉개짐 | 값 강제 변경하지 않고 경고만. 필요 시 사용자가 직접 Steps를 올리도록 도움말에 안내(§2.8.3) |
| 모드 라디오를 조작 중 생성 버튼을 누름 | 스냅샷이 전환 중 상태를 캡처 | `_set_ui_enabled()` targets에 라디오 2종를 포함해 생성 중 조작 불가(§4.4.6) |
| txt2img로 복귀 시 `denoiseSpinBox`가 숨김 상태로 남음 | txt2img 디노이즈를 조절할 수 없음 | `_on_img2img_mode_changed()`에서 항상 `denoiseCol.setVisible(not checked)`로 양방향 복원(§4.4.4) |

---

## 8. 구현 순서 (체크리스트)

- [ ] 1. `app/core/api_client.py` — `Path` import, `_guess_mime`, `upload_image()` 추가
- [ ] 2. `app/sections/generation.py` — `_resolve_vae_link()`, `convert_workflow_to_img2img()` 추가
- [ ] 3. `app/sections/generation.py` — `generate()`에 img2img 분기 삽입 (denoise 클램프 선행)
- [ ] 4. `assets/ui/main.ui` — **3곳 삽입**: ① `step2HeaderLayout` 직후에 `img2imgModeRow`(라디오 2개 + 힌트), ② `dimensionContainer` 직후에 `img2imgCard`(제목/선택/제거/미리보기/정보/강도 슬라이더), ③ `facedetailerPanel` 최상단에 `img2imgFdWarningLabel`
- [ ] 5. `assets/ui/main_ui.py` — 동일 위젯 생성 블록으로 동기화 (`img2imgModeRadio` 버튼 그룹 포함)
- [ ] 6. `main.py` — `IMAGE_FILE_FILTER`, `_img2img_source_path/_source_size/_prev_size` 초기화
- [ ] 7. `main.py` — 시그널 연결(모드 라디오/선택/제거/슬라이더/`facedetailerCheckBox`), 핸들러 `_on_img2img_mode_changed` / `_update_fd_img2img_warning` / `_apply_img2img_size_lock` / `_on_img2img_strength_changed` / `_on_img2img_select` / `_on_img2img_clear` / `_update_img2img_preview`
- [ ] 8. `main.py` — `capture_snapshot()`에 `mode` / `source_path` / `img2img_strength` 추가 + 미선택 `ValueError` + 프롬프트 필수 검사 분기
- [ ] 9. `main.py` — `_set_ui_enabled()` targets에 모드 라디오 2종 + 선택/제거/강도 슬라이더 추가
- [ ] 10. `app/sections/prompt.py` — img2img용 프롬프트 향상 지침 추가 (§2.4)
- [ ] 11. `tests/test_img2img_support.py` 신규 작성 (11개 케이스)
- [ ] 12. `pytest` + `py_compile` 실행 및 결과 확인
- [ ] 13. §6.3 수동 시나리오 + §6.4 모델별 호환성 확인

---

## 9. 이번 작업에서 변경하지 않는 것

- `workflows/*.json` 템플릿 (변환은 렌더링 후 메모리에서 수행)
- `app/core/workflow_manager.py` (모델별 렌더링 로직 유지)
- `workflows/app_config.json` (사용자 기존 변경 보존)
- `outputs/*.png` (사용자 기존 삭제 상태 보존)
- 기존 txt2img 경로의 denoise 기본값 `1.0` 및 `denoiseSpinBox` 동작 (img2img에서는 숨길 뿐 값은 그대로)
- FaceDetailer 주입 로직 (`_inject_facedetailer`) 및 모든 FD 파라미터 기본값
- 기존 스텝 카드 번호 구조 (`step1Card` / `step2Card`) — img2img는 2단계 카드 내부에 삽입
- 시드 / Steps / CFG / 샘플러 / 스케줄러의 값 (모드 전환 시 자동 조정하지 않음, §2.8.1)
- 참조 이미지 경로의 프리셋/설정 파일 저장 (현재 실행 전용 상태)

