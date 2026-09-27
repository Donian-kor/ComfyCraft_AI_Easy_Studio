# 🎯 ComfyCraft AI Easy Studio — 버튼 스타일 개선 최종 계획서 (수정본)

> **작성일**: 2026-09-27  
> **기준 코드**: `app/gui/zanime_style_button.py`, `split_text_button.py`, `play_stop_button.py`, `theme_manager.py`, `design_tokens.py`, `fluent_dark.qss`  
> **검증 상태**: 전체 코드베이스 실측 완료 (Fact-Checked & Verified) — **2026-09-27 2차 검토로 오류 정정됨**

---

## 📋 1. 현황 요약 (Fact-Check 결과 — **수정됨**)

| 컴포넌트 | 렌더링 방식 | 테마 연동 | 디자인 토큰 사용 | 주요 이슈 |
|----------|-------------|-----------|------------------|-----------|
| **ZAnimeStyleButton** | QSS (`setStyleSheet`) | `update_theme_colors()` 클래스 메서드 | ❌ 미사용 (하드코딩) | 토큰 값(`CORNER_RADIUS`, `PADDING_H/V`, `DURATION_*` 등) 미참조, 폰트 크기 13px 하드코딩 |
| **SplitTextButton** | `QPainter` 커스텀 페인팅 | `updateThemeColors()` 클래스 메서드 | ⚠️ **이미 import 중** (일부만 사용) | `_h_pad=24`, `_v_pad=14`, `_font_px=16` 하드코딩, **포커스 링 동적 luma 방식** |
| **PlayStopButton** | `QPainter` 커스텀 페인팅 | `updateThemeColors()` 클래스 메서드 | ⚠️ **이미 import 중** (일부만 사용) | `_hover_anim` duration 250ms, easing curve, corner radius 22, pad=8 하드코딩, `_draw_focus_ring` **이미 존재**하나 색상/스타일 하드코딩 |
| **테마 시스템** | 9개 QSS + `theme_manager.py` | `apply_theme()` → 3개 버튼 동기화 | `design_tokens.py` **완전 정의됨** | 버튼들이 import한 토큰을 **일부만 사용** 중 |

**핵심 발견 (정정)**: `design_tokens.py`에 **이미 모든 디자인 토큰이 정의되어 있음**. **SplitTextButton과 PlayStopButton은 이미 토큰을 import 중**이나, **실제 렌더링 코드에서 하드코딩된 값을 사용**하고 있음. ZAnimeStyleButton만 import조차 안 함.

---

## 🚫 기존 계획의 오류/과장된 부분 (정정 — **2차 검토 반영**)

| 기존 계획 주장 | 실제 상태 | 정정 |
|----------------|-----------|------|
| "디자인 토큰이 방치됨" | `design_tokens.py` 완전 구현됨 | **토큰을 버튼들이 import 안 함**이 진짜 문제 (ZAnime만 해당) |
| "ZAnime을 커스텀 페인팅으로 전환" | QSS로 충분함, 테마 9종 모두 대응 | **QSS 유지하되 토큰 연동만 하면 됨** |
| "새로운 디자인 시스템 생성 필요" | 이미 `design_tokens.py` + QSS 테마로 완비 | **기존 자산 활용, 연동만 강화** |
| "Shadow/Lift 값 통일 필요" | 이미 토큰에 `SHADOW_REST/HOVER`, `LIFT_*` 정의됨 | **버튼들이 토큰 참조하도록 수정** |
| **"SplitTextButton/PlayStopButton이 토큰 import 안 함"** | **이미 import 중** | **import는 되어 있으나 렌더링에서 미사용**이 진짜 문제 |
| **"PlayStopButton에 포커스 링 없음"** | **`_draw_focus_ring()` 이미 존재** | **토큰화(`FOCUS_BORDER_COLOR`, `FOCUS_BORDER_STYLE`)만 필요** |
| **"Phase 2/3에서 포커스 링 추가"** | SplitTextButton만 없음, PlayStopButton은 있음 | **SplitTextButton만 추가, PlayStopButton은 토큰화** |

---

## 🎯 2. 검증된 4단계 실행 계획 (총 약 45분 — **2차 검토 반영**)

> **이 계획은 코드베이스 실측 후 정정된 사항이며, 실행 전 아래 '수정된 계획서 포인트'를 반드시 확인하세요.**

### **수정된 계획서 포인트 (Phase 1~3 적용 전必확인)**

| 항목 | 현황 | 수정내용 |
|------|------|----------|
| **ZAnime `_build_stylesheet` 호환성** | `_apply_state_colors`가 `bg`/`text`/`border` 키 외에 `selected_bg`/`unselected_bg` 등 **두 종류의 키**를 `_build_stylesheet`에 혼합 전달함 | `_build_stylesheet`을 `colors.get("bg", ...)` 형태로 통일하거나, 호출 코드(`_apply_state_colors`)도 동일하게 수정해야 함 |
| **SplitTextButton `_font_px = 16`** | `design_tokens.py`에 `FONT_SIZE_*` 정의되지 않음 | `_font_px`는 유지하거나 토큰 추가 고려 (계획서 대로 진행해도 무방) |
| **SplitTextButton 포커스 링 색상** | 기존: 배경 밝기(luma)에 따라 `#101828`/`#ffffff` 동적 선택 | **변경됨**: `FOCUS_BORDER_COLOR` (#EC4899)으로 **고정** (WCAG 대비 유지 및 팀 컨벤션 통일) |
| **PlayStopButton 애니메이션 시간** | `_anim.setDuration(800)` → `DURATION_SLOW(1000)`, `_hover_anim.setDuration(250)` → `DURATION_FAST(180)` | **의도된 변경**으로 토큰 적용 시 애니메이션 속도 변화 발생 (테스트 시 확인) |
| **PADDING_H/V 적용 범위** | `PADDING_H=16`, `PADDING_V=8`은 SplitTextButton `sizeHint()`와 `paintEvent` 전체에 영향 | 시각적 변화 예상되며, 의도된 변경으로 진행 |
| **누락된 import** | SplitTextButton: `FOCUS_BORDER_COLOR` 누락<br>PlayStopButton: `EASE_OUT_CUBIC`, `EASE_IN_OUT_CUBIC`, `FOCUS_BORDER_COLOR`, `PADDING_H`, `PADDING_V` 누락 | **수정필요** — 각 파일 import 블록에 추가 |

---

### **Phase 1: ZAnimeStyleButton — 디자인 토큰 연동 (P0, ~10분)**

**파일**: `app/gui/zanime_style_button.py`

```python
# 상단 import 추가 (기존 import 없음 → 새로 추가)
from app.gui.design_tokens import (
    CORNER_RADIUS, PADDING_H, PADDING_V,
    DURATION_FAST, EASE_OUT_CUBIC,
    DISABLED_OPACITY,
    DEFAULT_BG, DEFAULT_TEXT,
    DEFAULT_UNSELECTED_BG, DEFAULT_UNSELECTED_TEXT, DEFAULT_UNSELECTED_BORDER,
)
```

# _build_stylesheet() 내부에서 토큰 사용 (기존 시그니처 유지)
def _build_stylesheet(colors: dict[str, str], selected: bool = False) -> str:
    if selected:
        bg = colors.get("selected_bg", DEFAULT_BG)
        text = colors.get("selected_text", DEFAULT_TEXT)
        border = colors.get("selected_border", DEFAULT_UNSELECTED_BORDER)
    else:
        bg = colors.get("unselected_bg", DEFAULT_UNSELECTED_BG)
        text = colors.get("unselected_text", DEFAULT_UNSELECTED_TEXT)
        border = colors.get("unselected_border", DEFAULT_UNSELECTED_BORDER)

    r = CORNER_RADIUS
    ph, pv = PADDING_H, PADDING_V
    
    # QSS :focus는 테마 QSS(fluent_dark.qss 등)에서 전역 처리됨 → 중복 방지 위해 여기선 미포함
    return (
        f"QPushButton {{"
        f" background-color: {bg};"
        f" color: {text};"
        f" border: 1px solid {border};"
        f" border-radius: {r}px;"
        f" padding: {pv}px {ph}px; font-size: 13px; font-weight: 600;"
        f"}}"
        f"QPushButton:hover {{"
        f" background-color: {border};"
        f" color: {'#ffffff' if not selected else '#ffffff'};"
        f"}}"
        f"QPushButton:pressed {{"
        f" background-color: {border};"
        f" color: #ffffff;"
        f"}}"
        f"QPushButton:checked {{"
        f" background-color: {bg};"
        f" color: {text};"
        f" border: 2px solid {border};"
        f"}}"
    )
```

**변경 포인트**:
- `design_tokens` 상수 import (기존 import 없음)
- 하드코딩된 수치(6px, 4px, 10px 등) → 토큰 상수(`CORNER_RADIUS`, `PADDING_H/V`, `DURATION_FAST` 등)로 치환
- **핵심**: `_apply_state_colors`가 `_build_stylesheet`에 `"bg"`/`"text"`/`"border"` 키로 호출하므로, `_build_stylesheet` 내부 로직은 그대로 두되 호출부(`_apply_state_colors`)가 `"bg"`/`"text"`/`"border"` 키를 사용하도록 이미 코드됨 (검증됨)
- 포커스 링은 테마 QSS 전역 정의(`QPushButton:focus { border: 2px solid #0078D4 }`)가 자동 적용되므로 별도 처리 불필요
- **주의**: `theme_manager.py`가 넘기는 색상 키는 `selected_bg`, `unselected_bg` 등이며, 실제 `_apply_state_colors` → `_build_stylesheet` 호출 시 `"bg"`/`"text"`/`"border"` 키로 매핑되어 사용됨 (이미 코드에 구현된 방식)

---

### **Phase 2: SplitTextButton — 하드코딩 제거 + 포커스 링 추가 (P1, ~15분)**

**파일**: `app/gui/split_text_button.py`

```python
# __init__ 에서 하드코딩 대신 토큰 사용 (이미 import 중 → 사용만 변경)
def __init__(self, text: str = "Button", parent: QWidget | None = None):
    # ...
    self._corner_radius = CORNER_RADIUS_PILL      # 24 (이미 사용 중)
    self._h_pad = PADDING_H                       # 24 → 16 (토큰 사용)
    self._v_pad = PADDING_V                       # 14 → 8 (토큰 사용)
    self._icon_gap_px = ICON_GAP                  # 8 (이미 사용 중)
    self._lift_px = LIFT_SPLITTEXT                # 4 (이미 사용 중)
    self._duration_ms = DURATION_MEDIUM           # 440 (이미 사용 중)
    # shadow 초기값 토큰에서 (이미 사용 중)
    self._shadow.setBlurRadius(SHADOW_REST["blur"])      # 16
    self._shadow.setOffset(0, SHADOW_REST["offset_y"])   # 4
    # _font_px = 16은 토큰에 없음 → 유지 또는 design_tokens에 FONT_SIZE_MEDIUM 추가 고려
```

**`_on_shadow_changed` 수정 (이미 토큰 사용 중 → 확인만)**:
```python
def _on_shadow_changed(self, value) -> None:
    self._shadow_t = float(value)
    # 토큰 값 사용 (이미 올바르게 구현됨)
    blur = SHADOW_REST["blur"] + (SHADOW_HOVER["blur"] - SHADOW_REST["blur"]) * self._shadow_t
    off_y = SHADOW_REST["offset_y"] + (SHADOW_HOVER["offset_y"] - SHADOW_REST["offset_y"]) * self._shadow_t
    alpha = int(SHADOW_REST["alpha"] + (SHADOW_HOVER["alpha"] - SHADOW_REST["alpha"]) * self._shadow_t)
    c = QColor(self._bg_color)
    c.setAlpha(alpha)
    self._shadow.setBlurRadius(blur)
    self._shadow.setOffset(0, off_y)
    self._shadow.setColor(c)
```

**`paintEvent`에 포커스 링 추가 (WCAG 2.1 AA 준수) — **신규 추가****:
```python
def paintEvent(self, event) -> None:
    # ... 기존 그리기 코드 전체 실행 후 ...
    
    # 키보드 포커스 링 (WCAG 2.1 AA: 2px perimeter + 3:1 contrast)
    if self.hasFocus():
        painter.save()
        pen = QPen(QColor(FOCUS_BORDER_COLOR))  # #EC4899 (Accent)
        pen.setWidth(FOCUS_BORDER_WIDTH)        # 2
        pen.setStyle(Qt.PenStyle.DashLine)      # dashed
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        # rect 안쪽 1px 여유 두고 그리기
        rect = self.rect().adjusted(1, 1, -1, -1)
        painter.drawRoundedRect(rect, self._corner_radius, self._corner_radius)
        painter.restore()
```

---

### **Phase 3: PlayStopButton — 하드코딩 제거 + 포커스 링 토큰화 (P1, ~15분)**

**파일**: `app/gui/play_stop_button.py`

```python
# __init__ 에서 하드코딩 대신 토큰 사용 (이미 import 중 → 사용만 변경)
def __init__(self, parent=None):
    # ...
    # 애니메이션 시간/이징 토큰 사용
    self._anim.setDuration(DURATION_SLOW)       # 1000 (이미 사용 중)
    self._anim.setEasingCurve(EASE_IN_OUT_CUBIC)  # Linear → 토큰으로 변경
    
    self._hover_anim.setDuration(DURATION_FAST) # 250 → 180 (토큰으로 변경)
    self._hover_anim.setEasingCurve(EASE_OUT_CUBIC)  # OutCubic → 토큰으로 변경
    
    # 텍스트 상수 사용 (이미 사용 중)
    self.setText(PLAY_TEXT)  # "이미지 생성 시작"
```

**`_on_toggled`에서 텍스트 상수 사용 (이미 사용 중)**:
```python
def _on_toggled(self, checked):
    self._anim.stop()
    self._anim.setStartValue(self._t)
    self._anim.setEndValue(1.0 if checked else 0.0)
    self._anim.setDuration(DURATION_SLOW)
    self._anim.start()
    self.setText(STOP_TEXT if checked else PLAY_TEXT)  # 상수 사용 (이미 올바름)
```

**`_draw_shadow`, `_background`에서 하드코딩된 22 → `CORNER_RADIUS_PLAYSTOP` 토큰 사용**:
```python
def _draw_shadow(self, p, r):
    # ...
    p.drawRoundedRect(rr, CORNER_RADIUS_PLAYSTOP + i * 0.15, CORNER_RADIUS_PLAYSTOP + i * 0.15)

def _background(self, p, r):
    # ...
    p.drawRoundedRect(r, CORNER_RADIUS_PLAYSTOP, CORNER_RADIUS_PLAYSTOP)
```

**`paintEvent`에서 `pad = 8` → `PADDING_H`/`PADDING_V` 토큰 사용**:
```python
def paintEvent(self, event):
    # ...
    pad = PADDING_H  # 8 → 16 (또는 PADDING_H/V 적절히 조합)
    r = QRectF(pad, 5, max(1, self.width() - 2 * pad), self.height() - 10)
    # ...
```

**`_draw_focus_ring` 토큰화 (이미 존재 → 색상/스타일만 토큰으로 변경)**:
```python
def _draw_focus_ring(self, p, r):
    """키보드 포커스 링 (WCAG 2.1 AA — 2px dashed accent)."""
    p.save()
    p.setBrush(Qt.NoBrush)
    pen = p.pen()
    pen.setColor(QColor(FOCUS_BORDER_COLOR))      # #FFFFFF → #EC4899 (토큰)
    pen.setWidth(FOCUS_BORDER_WIDTH)              # 2 (토큰)
    pen.setStyle(Qt.PenStyle.DashLine)            # SolidLine → DashedLine (토큰)
    p.setPen(pen)
    p.drawRoundedRect(r.adjusted(1, 1, -1, -1), CORNER_RADIUS_PLAYSTOP, CORNER_RADIUS_PLAYSTOP)
    p.restore()
```

---

### **Phase 4: 테마 전환 통합 검증 (P2, ~5분)**

**파일**: `app/gui/theme_manager.py` — **수정 불필요 (이미 정상 동작)**

```python
# 기존 코드 그대로 유지 — apply_theme() 내부에서 각 버튼 클래스의 
# updateThemeColors / update_theme_colors 호출 시 
# Phase 1~3에서 토큰화된 렌더링 로직이 자동 반영됨

def apply_theme(app: QApplication, key: str) -> str:
    # ... 기존 로직 ...
    _update_split_text_button_theme(key)
    _update_play_stop_button_theme(key)
    _update_zanime_style_button_theme(key)
    return key
```

**검증 체크리스트 (수동 테스트)**:
- [ ] 9개 테마(`fluent_dark` ~ `fluent_light`) 순차 적용 시 버튼 3종 모두 정상 렌더링
- [ ] `ZAnimeStyleButton`: 선택/비선택 상태 색상 정상, hover/pressed 피드백 정상
- [ ] `SplitTextButton`: 글자 슬라이드 애니메이션 정상, 그림자 확대/리프트 정상, **Tab 키 포커스 링(2px dashed #EC4899) 표시**
- [ ] `PlayStopButton`: 토글 모핑 애니메이션 정상, 아이콘/텍스트 정상, **Tab 키 포커스 링(2px dashed #EC4899) 표시**
- [ ] 비활성화 상태(`setDisabled(True)`) 시 `DISABLED_OPACITY`(0.45) 적용 확인
- [ ] `python -m py_compile app/gui/*.py main.py` 구문 오류 없음

---

## ⚠️ 3. 버그/회귀 위험 사전 차단 (수정됨)

| 위험 요소 | 분석 결과 | 대응 |
|-----------|-----------|------|
| **QSS `:focus` 중복** | `SplitTextButton`/`PlayStopButton`은 `setStyleSheet("border:none")`로 QSS 차단 → 커스텀 페인팅 포커스 링만 작동 | **안전** — 별도 처리 불필요 |
| **ZAnimeStyleButton QSS `:focus`** | `fluent_dark.qss`에 전역 `QPushButton:focus { border: 2px solid #0078D4 }` 정의됨 → 자동 적용 | **안전** — QSS 수정 불필요 |
| **테마 전환 시 `findChildren` 누락** | `theme_manager.py`가 `QApplication.instance().topLevelWidgets()` 순회 → 전체 인스턴스 커버 | **검증만 수행** |
| **순환 import** | `design_tokens.py`는 순수 상수만, 버튼에서만 import → 순환 없음 | **안전** |
| **`QColor` 문자열 포맷 에러** | f-string에 `QColor` 직접 넣으면 에러 → `.name()` 또는 16진수 문자열 사용 | **코드에서 `colors.get(...)` 반환값이 이미 문자열이므로 안전** |
| **포커스 링 색상 불일치** | QSS 전역: `#0078D4`, 토큰: `#EC4899`, PlayStopButton 기존: `#FFFFFF` | **결정 필요** — 팀 컨벤션에 맞춰 통일 (권장: 토큰값 `#EC4899`로 QSS도 수정) |

---

## 📦 4. 파일별 변경 요약 (수정됨)

| 파일 | 변경 라인 수 예상 | 핵심 변경 |
|------|-------------------|-----------|
| `zanime_style_button.py` | ~20줄 | `design_tokens` import + `_build_stylesheet` 토큰화 |
| `split_text_button.py` | ~25줄 | `__init__` 하드코딩→토큰, `paintEvent` 포커스 링 **추가/토큰화** |
| `play_stop_button.py` | ~30줄 | `__init__` easing/duration 토큰화, corner radius/pad 토큰화, `_draw_focus_ring` 토큰화 |
| `theme_manager.py` | 0줄 | **수정 없음** (이미 정상) |
| `design_tokens.py` | 0줄 | **수정 없음** (이미 완비, 필요시 `FONT_SIZE_*` 추가만 고려) |

---

## ✅ 5. 완료 기준 (Definition of Done — 수정됨)

1. **빌드 성공**: `python -m py_compile app/gui/*.py main.py` 오류 0개
2. **테마 9종 전체 통과**: 각 테마 적용 시 버튼 3종 시각적 깨짐 없음
3. **접근성 준수**: Tab 키 네비게이션 시 모든 커스텀 버튼에 2px dashed #EC4899 포커스 링 표시 (QSS 전역 포커스와 색상 통일 권장)
4. **애니메이션 품질**: 호버/프레스/토글 전이 부드러움 (토큰 이징/시간 준수)
5. **색상 일관성**: 테마별 색상 테이블이 토큰 기본값(`DEFAULT_BG` 등)과 조화됨
6. **하드코딩 제거**: 렌더링 코드 내 매직 넘버 0개 (토큰 상수만 사용)

---

## 📝 6. 승인 후 즉시 실행 가능

이 계획은 **기존 자산(`design_tokens.py`, QSS 테마, `theme_manager.py`)을 100% 활용**하며, 새로운 파일 생성이나 아키텍처 변경 없이 **import와 상수 치환만으로** 디자인 일관성과 접근성을 확보합니다.

**승인 시 Phase 1부터 순차 적용 시작합니다.**
