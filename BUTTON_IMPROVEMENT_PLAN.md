# 🎨 버튼 스타일 시스템 개선 계획서 (v2.0 - 사실 검증 기반 정정본)

> **문서 상태**: 2026-09-26 코드베이스 실측 재검증 완료 (Fact-Checked & Verified)  
> **기준 환경**: Python 3.12+ / PySide6 6.11.2 / Windows 11

---

## 🔍 1. 기존 계획서 재검증 및 현황 분석 (Fact-Check)

기존 계획서(v1.0)의 진단 중 상당수가 실제 코드베이스의 동작 및 Qt 프레임워크 제약과 불일치함을 확인하였으며, 아래와 같이 정정합니다.

### 1.1 `zanime_style_button.py` (ZAnimeStyleButton)
- **기존 진단**: 단순 색상만 적용됨, #e2e2e2 배경이 밋밋함, 호버/프레스 상태 미흡.
- **실제 현황 (Fact)**:
  - 🚨 **미사용 코드(Dead Code)**: 실제 메인 화면(`main.py:818`)에서는 `ZAnimeStyleButton`을 인스턴스화하지 않고 일반 `QPushButton`에 `main.py:_build_zanime_style_qss()`를 직접 적용하고 있음.
  - `zanime_style_button.py`를 아무리 수정해도 화면에는 아무런 변화가 없음.
  - 실제 사용 중인 `main.py`의 QSS는 이미 10px radius, hover 테두리 강조, pressed 패딩 시프트, `zanimeSelected` 속성 기반 선택 상태가 적용되어 있음.
  - `#e2e2e2`는 라이트 테마(`fluent_light`)의 정상 색상이며, 기본 테마인 `midnight_navy`에서는 `#2b3a4d`가 정상 적용됨.

### 1.2 `split_text_button.py` (SplitTextButton)
- **기존 진단**: 호버 시 lift 효과 미적용, 그림자가 작고 테마 미지원, 50ms 딜레이가 안 보임.
- **실제 현황 (Fact)**:
  - ❌ **진단 오류 (이미 정상 동작)**: 실측 결과 호버 시 `_rise`는 0.0 → 4.0px, 그림자 blur는 16px → 30px, offset Y는 4px → 8px, alpha는 82 → 128로 완벽하게 확대되며 작동 중임.
  - 50ms 딜레이는 원본 CSS(CodePen) 명세(`i / 20 * 1000s`)와 정확히 일치하며 텍스트 분할 슬라이드가 정상 시연됨.
  - 테마 색상 역시 `theme_manager.py:121`과 `setStatus()`를 통해 정상 연동되어 있음.
  - 기존 계획서의 Phase 3 코드를 적용할 경우 도리어 애니메이션 인터럽트 시 점프 현상 및 비대칭 반경 버그가 발생하는 퇴행(Regression) 위험이 있었음.

### 1.3 `play_stop_button.py` (PlayStopButton)
- **기존 진단**: 텍스트와 아이콘이 겹침.
- **실제 현황 (Fact)**:
  - 🚨 **진짜 원인은 아이콘 호출 누락**: `paintEvent()`에서 `_draw_icon()` 메서드가 전혀 호출되지 않아 아이콘이 렌더링조차 되지 않고 있었음. (텍스트와 겹치는 게 아니라 아이콘이 증발한 상태)
  - 🚨 **텍스트 불일치 결함**: `__init__`에서는 `"이미지생성 시작"`(공백 없음), `_draw_text()`에서는 `"이미지 생성 시작"`(공백 있음)으로 하드코딩되어 접근성 라벨과 화면 표기가 일치하지 않음.
  - 만약 `_draw_icon()`을 단순히 복구하면 아이콘은 `cx+6` 고정 좌표에, 텍스트는 버튼 정중앙에 그려지므로 실제로 충돌이 발생함. 따라서 **아이콘+텍스트 결합 수평 레이아웃 재계산**이 필수적임.

### 1.4 `design_tokens.py` 연동 상태
- `app/gui/design_tokens.py`가 이미 생성되어 있으나, 3개 버튼 파일 모두에서 import되지 않은 채 방치되어 있음.

### 1.5 Qt QSS 기술적 한계 주의점
- Qt 스타일시트(QSS)는 브라우저 CSS3 엔진과 다름.
  - `box-shadow`, `inset shadow` 미지원 (위젯의 `paintEvent`나 `QGraphicsDropShadowEffect`로만 구현 가능).
  - `transform: scale()` 미지원 (패딩/마진 조정으로 대체).
  - `prefers-reduced-motion` 미디어 쿼리 미지원 (애플리케이션 전역 설정 플래그로 제어).
  - Python 코드에서 문자열 포맷팅 시 `QColor` 객체를 넣으면 포맷 에러 발생 (반드시 `.name()` 문자열 사용 필요).

---

## 💡 2. 개선 방향 및 원칙

1. **실제 동작 코드 우선 (Pragmatic Focus)**:
   화면에 실제 표시되는 `main.py`의 Z-ANIME 버튼과 `PlayStopButton`, `SplitTextButton`에 집중.
2. **단일 진실 공급원 (Single Source of Truth)**:
   기존 방치된 `app/gui/design_tokens.py`를 모든 버튼의 상수 소스로 실연동.
3. **Qt 네이티브 최적화 (Native Compliance)**:
   QSS 미지원 기법을 무리하게 도입하지 않고, QPainter 및 Qt 속성 시스템 기반으로 안정적인 시각 효과 완성.
4. **접근성 및 일관성 (WCAG 2.1 AA)**:
   키보드 포커스 링 통일, 버튼 내부 라벨과 접근성 텍스트의 100% 일치 보장.

---

## 📋 3. 단계별 개선 실행 로드맵

### Phase 1: [P0] PlayStopButton 핵심 결함 수정 및 레이아웃 통합
**목표**: 누락된 아이콘 복구, 텍스트-아이콘 중앙 결합 레이아웃 구축, 텍스트 불일치 해결.

1. **텍스트 소스 단일화**:
   `app/gui/design_tokens.py`의 `PLAY_TEXT = "이미지 생성 시작"`, `STOP_TEXT = "정지"` 상수를 임포트하여 `__init__`, `setText`, `_draw_text` 전체에서 일원화 (불일치 해소).
2. **아이콘 + 텍스트 통합 수평 레이아웃 계산**:
   - `cx+6` 하드코딩 좌표 제거.
   - 아이콘 폭(14px) + 간격(8px) + 텍스트 폭을 합산한 전체 컨텐츠 폭을 구하고, 버튼 중앙(`r.center().x()`)을 기준으로 좌우 대칭 배치.
3. **`paintEvent()` 복구**:
   `_draw_icon`과 `_draw_text`를 통합된 `_draw_content(p, r)`로 호출하여 누락된 아이콘 복원.

### Phase 2: [P1] Z-ANIME 스타일 버튼 실제 경로 개선 & 죽은 코드 정리
**목표**: 실제 렌더링 경로인 `main.py`의 스타일시트 고도화 및 `zanime_style_button.py` 아키텍처 정리.

1. **`main.py:_build_zanime_style_qss` 보강**:
   - `design_tokens.py`의 반경(10px) 및 테마 색상 연동.
   - 키보드 포커스 상태(`QPushButton:focus`)를 추가하여 접근성 표준 준수.
   - 클릭 시의 물리적 깊이감(pressed 시 패딩 미세 조정) 강화.
2. **`zanime_style_button.py` 정리**:
   - `main.py:818`에서 일반 `QPushButton` 대신 `ZAnimeStyleButton`을 실제로 생성하도록 승격시키거나, 불필요한 인스턴스 캐싱 누수 코드 정리.

### Phase 3: [P1] 공통 디자인 토큰 실참조 연결 (`design_tokens.py`)
**목표**: 방치되어 있던 `design_tokens.py`를 3개 컴포넌트가 실제로 공유하도록 import 연결.

- `split_text_button.py`:
  - `_corner_radius = CORNER_RADIUS_LARGE` (14px 또는 22px)
  - `_lift_px = LIFT_SPLITTEXT` (4px)
  - `_icon_gap_px = ICON_GAP` (8px)
- `play_stop_button.py`:
  - `PLAY_TEXT`, `STOP_TEXT` 참조
  - `LIFT_PLAYSTOP`, `EASE_OUT_CUBIC` 참조
- `main.py` / `zanime_style_button.py`:
  - 기본 fallback 컬러 및 패딩, 반경 토큰 참조

### Phase 4: [P2] 포커스 링 및 키보드 내비게이션 표준화
**목표**: 테마 시스템(Theme QSS)과 커스텀 페인팅 버튼 간의 포커스 표시 일치.

- `SplitTextButton`과 `PlayStopButton`은 직접 `paintEvent`를 사용하므로, `self.hasFocus()`일 때 외곽선에 테마 액센트 컬러의 2px 포커스 링을 그리도록 지원.
- 키보드 탭 네비게이션 시 시각적 표시 완벽 지원.

---

## 📐 4. 컴포넌트별 기술 사양 요약

| 항목 | ZAnimeStyleButton (칩) | SplitTextButton (액션/배지) | PlayStopButton (주 실행) |
|---|---|---|---|
| **렌더링 방식** | QSS (Qt StyleSheet) | QPainter (전체 커스텀) | QPainter (전체 커스텀) |
| **코너 반경** | 10px | 22~24px (Pill 형태) | 22px (Pill 형태) |
| **호버 효과** | 테두리 하이라이트 + 밝기 증가 | Y축 -4px Lift + 그림자 확장 + 글자 슬라이드 | 미세 Lift + 방사형 하이라이트 그라디언트 |
| **클릭 효과** | 패딩 이동 (시각적 눌림) | 기본 클릭 이벤트 | Y축 +1px 인셋 피드백 + 토글 상태 모핑 |
| **상태 전환** | checked (`zanimeSelected`) | status 속성 (accent, success 등) | checked (생성시작 ⇄ 정지 모핑) |
| **애니메이션** | CSS 전환 | OutCubic 440ms (50ms 글자차등) | InOut 모핑 800~1000ms |

---

## 🧪 5. 검증 및 테스트 계획

1. **단위 테스트 (Regression Check)**:
   - `python -m unittest discover -s tests -v` (33개 테스트 전체 통과 필수 유지)
   - 테마 포커스 링 검증(`test_step2_focus_ring_*`) 준수.
2. **오프스크린 렌더링 검사**:
   - `PlayStopButton`: 정지/시작 양쪽 상태에서 아이콘 영역 픽셀과 텍스트 영역 픽셀이 겹치지 않고 정상 분기되는지 스크립트로 검증.
   - `SplitTextButton`: 호버 전후 `_rise` 및 drop shadow 속성 수치 실측.
3. **구문 및 컴파일 검사**:
   - `python -m py_compile app/gui/*.py main.py` 이상 없음 확인.

---

## 💎 6. UI/UX Pro Max 디자인 시스템 검토 및 규격 가이드

`ui-ux-pro-max` 스킬을 통해 AI 이미지 생성 데스크톱 인터페이스 기준(AI-Native UI 스타일, WCAG 2.1/2.2 AA 접근성, 마이크로 인터랙션)을 검토한 결과, 본 프로젝트에 적용해야 할 핵심 UI/UX 기준은 다음과 같습니다.

### 6.1 WCAG 2.2 AA/AAA 포커스 및 접근성 지침
- **Focus Appearance (2 CSS px Perimeter + 3:1 명도 대비)**:
  - 데스크톱 Qt UI에서 마우스 클릭 시에는 포커스 링이 거슬리지 않아야 하지만, `Tab` 키를 통한 키보드 탐색 시에는 **2px 두께의 테두리(`outline: 2px solid Accent`)**가 확실하게 인지되어야 함.
  - `PlayStopButton` 및 `SplitTextButton`의 `paintEvent`에 `self.hasFocus()` 체크 후 `FOCUS_BORDER_COLOR` 2px 링 렌더링 필수.
- **최소 타깃 크기 (Target Size)**:
  - 데스크톱 마우스 및 터치 겸용 환경을 위해 모든 액션 버튼의 높이를 최소 **34px ~ 44px 이상**으로 유지 (`PlayStopButton`: 46px, `SplitTextButton`: 42px+, `Z-ANIME`: 34px).

### 6.2 모션 및 애니메이션 원칙 (Context-Aware Timing)
- **속도 위계 (Duration Hierarchy)**:
  - 미세 피드백(Hover/Press): **150ms ~ 200ms** (즉각적 반응성, 지연감 배제).
  - 상태 전환(Play ⇄ Stop 토글 모핑): **400ms ~ 600ms** (부드러운 시각적 연속성 제공).
- **이징(Easing)**:
  - 물리적 반동은 `OutCubic` 또는 `OutBack`을 사용하여 기계적 선형 이동이 아닌 유기적이고 탄성 있는 피드백 제공.
- **안티패턴 차단**:
  - 이모지 아이콘 사용 금지 (벡터 기반 QPainterPath 또는 SVG 아이콘 사용).
  - 텍스트-배경 대비율 최소 4.5:1 준수 (다크 모드와 라이트 모드 공통).

---

## 🔍 7. 추가 정밀 검토로 발굴된 누락 요소 및 보완책

코드베이스와 UI/UX 프로토콜을 전체 검토한 결과, 기존 계획서에서 누락되었던 **4가지 실무 핵심 결함**을 발굴하여 보완 항목으로 추가합니다.

### 7.1 비활성화(Disabled) 상태의 시각 피드백 부재 (Critical UX)
- **현상**: 생성 진행 중(`main.py:1989`) 입력 컨트롤들이 `setEnabled(False)` 처리될 때, `PlayStopButton`은 50% opacity로 어두워지지만 `SplitTextButton`은 배경색(`_bg_color`), 텍스트색, 그림자가 활성 상태와 완전히 동일하게 100% 진하게 유지됨 (실측: `#275efe` 유지).
- **문제점**: 사용자가 버튼이 잠겼는지 누를 수 있는지 시각적으로 전혀 구분할 수 없음.
- **해결책**:
  ```python
  # SplitTextButton.paintEvent() 상단에 비활성화 피드백 추가
  if not self.isEnabled():
      painter.setOpacity(0.45)  # 전체 위젯을 45% 불투명도로 Dim 처리
  ```

### 7.2 마우스 누름(Pressed) 시 촉각적(Tactile) 물리 피드백 누락
- **현상**: `SplitTextButton`은 호버 시 위로 4px 들리는(Lift) 효과는 있으나, 실제 마우스로 클릭하는 순간(`isDown() == True`) 아무런 Y축 눌림 변화가 없음.
- **해결책**:
  - `button_rect` 계산 시 `self.isDown()`일 때 Y축으로 +1~2px 인셋 하강 및 그림자 축소 처리.
  - 마우스를 누르는 순간 물리적으로 쑥 들어가는 정밀한 손맛(Tactile Feedback) 완성.

### 7.3 테마 배지 색상의 WCAG 2.1 AA 명도 대비 미달 (Contrast Flaw)
- **현상**: 실측 명도 대비 계산 결과, `_SPLIT_TEXT_BUTTON_COLORS`의 밝은 파스텔 배경 위에 흰색 텍스트(`#ffffff`)를 얹어 WCAG 2.1 AA 기준(4.5:1)에 대폭 미달하는 상태가 다수 확인됨.
  - `midnight_navy` (accent: `#4cc2ff` 배경에 흰 글자 → **2.01:1**)
  - `fluent_dark` (success: `#4edea3` 배경에 흰 글자 → **1.71:1**)
  - `emerald_forest` (accent: `#34d399` 배경에 흰 글자 → **1.92:1**)
- **해결책**:
  - 밝은 파스텔톤 배경(`luma > 0.4`)의 텍스트 색상을 어두운 검정 계열(`#111827` 또는 `#0b1b2b`)로 수정하여 **대비율 10:1 이상**의 완벽한 가독성 확보.

### 7.4 인스턴스 추적 메모리 누수 방지 (Weakref 도입)
- **현상**: `ZAnimeStyleButton._instances`가 강한 참조 리스트(`list[ZAnimeStyleButton]`)로 인스턴스를 보관하여, 향후 다이얼로그나 동적 위젯에서 버튼 생성 시 가비지 컬렉션(GC)되지 않는 잠재적 누수 구조를 가짐.
- **해결책**:
  - `weakref.WeakSet()`으로 인스턴스를 관리하거나, `main.py`의 중앙 관리 체계로 일원화.


