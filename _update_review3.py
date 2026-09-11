# -*- coding: utf-8 -*-
from pathlib import Path

path = Path('코드리뷰.md')
content = path.read_text(encoding='utf-8')

# 테마 시스템 개선 섹션 추가 (잘 된 점 다음)
old_section = """---

## 📊 요약 — 우선순위별 분류"""

new_section = """---

## 🆕 테마 시스템 개선 (2026-09-10)

### 변경 내용

**문제**: 커스텀 버튼(`SplitTextButton`, `PlayStopButton`)이 QSS 기반 테마 변경의 영향을 받지 않고, 하드코딩된 색상(`#275efe`, `#0078D4`, `#C42B1C`)으로 고정되어 있었습니다.

**해결**: 각 커스텀 버튼에 `updateThemeColors()` 클래스 메서드를 추가하고, `theme_manager.py`에 테마별 색상 테이블을 정의하여 테마 변경 시 모든 버튼 인스턴스의 색상이 자동으로 업데이트되도록 개선했습니다.

### 수정 파일

| 파일 | 변경 내용 |
|------|-----------|
| `app/gui/split_text_button.py` | `setStatus()`/`getStatus()`, `updateThemeColors()`, `_apply_theme_color()` 추가 |
| `app/gui/play_stop_button.py` | `_play_color`/`_stop_color` 인스턴스 변수, `updateThemeColors()`, `_apply_theme_color()` 추가 |
| `app/gui/theme_manager.py` | `_SPLIT_TEXT_BUTTON_COLORS`, `_PLAY_STOP_BUTTON_COLORS` 테이블 추가 (9개 테마) |

### 작동 흐름

```
테마 변경 → apply_theme()
  → app.setStyleSheet(QSS)
  → _update_split_text_button_theme(key)
  → _update_play_stop_button_theme(key)
  → 모든 버튼 인스턴스._apply_theme_color()
```

### 버튼 상태값 (SplitTextButton)

| 상태 | 의미 |
|------|------|
| `"none"` | 기본 (파랑) |
| `"accent"` | 테마 액센트 색상 |
| `"success"` | 성공 (초록) |
| `"error"` | 오류 (빨강) |
| `"warning"` | 경고 (노랑) |
| `"pending"` | 대기 (회색) |

---

## 📊 요약 — 우선순위별 분류"""

content = content.replace(old_section, new_section)

path.write_text(content, encoding='utf-8')
print('3단계 완료: 테마 시스템 개선 섹션 추가')
