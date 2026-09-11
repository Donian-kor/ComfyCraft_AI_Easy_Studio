# -*- coding: utf-8 -*-
from pathlib import Path

path = Path('코드리뷰.md')
content = path.read_text(encoding='utf-8')

# 1. #15 PlayStopButton 텍스트 불일치 제거 (수정됨)
old_15 = """### 15. `PlayStopButton` 텍스트 불일치

[play_stop_button.py:58](file:///c:/Users/donian/Desktop/python/comfyui_Lmstudio_gui%20v0.3/app/gui/play_stop_button.py#L58)

```python
def _on_toggled(self, checked):
    self.setText("이미지생성 시작" if checked else "정 지")
    #                                              ↑ 공백 있음 "정 지"
```

반면 L50에서는: `self.setText("이미지생성 시작")` — 체크됐을 때와 안 됐을 때의 텍스트 로직이 **반전**되어 있고, "정 지"에 불필요한 공백이 있습니다.

---

## ✅ 잘 된 점"""

new_15 = """### 15. (수정됨) ~~`PlayStopButton` 텍스트 불일치~~

> **조치 완료**: `play_stop_button.py` L67에서 `"정지" if checked else "이미지생성 시작"`으로 수정되었습니다.

---

## ✅ 잘 된 점"""

content = content.replace(old_15, new_15)

# 2. 우선순위 요약 테이블 업데이트
old_priority = """| 우선순위 | 항목 | 설명 |
|---|---|---|
| 🔴 높음 | #1 `check_connection_silent` | 잘못된 import로 항상 실패 반환 |
| 🔴 높음 | #2 `processEvents()` | 백그라운드 스레드에서 Qt 이벤트 처리 |
| 🟡 중간 | #3 `_config` 직접 접근 | private 속성 외부 수정 |
| 🟡 중간 | #4 main.py 크기 | 2,139줄 단일 파일 |
| 🟡 중간 | #5 FaceDetailer 반복 | 동일 패턴 17회 반복 |
| 🟡 중간 | #8 메시지박스 테마 | 다크테마 하드코딩 |
| 🟢 낮음 | #6 HTML 하드코딩 | 도움말을 별도 파일로 |
| 🟢 낮음 | #7 도움말 코드 중복 | 2곳에서 같은 로직 |
| 🟢 낮음 | #9 중복 requirements | 파일 2개가 동일 |
| 🟢 낮음 | #10 일본어 기본값 | "未確認" → "미확인" |
| 🟢 낮음 | #11 스레드 안전성 | worker 접근 보호 |
| 🟢 낮음 | #12 디버그 로그 | 프로덕션에 DEBUG 메시지 |
| 🟢 낮음 | #13 예외 삼킴 | `except: pass` 패턴 |
| 🟢 낮음 | #14 테스트 부족 | 핵심 로직 테스트 없음 |
| 🟢 낮음 | #15 버튼 텍스트 | 텍스트 반전 + 공백 |"""

new_priority = """| 우선순위 | 항목 | 설명 |
|---|---|---|
| 🔴 높음 | #1 `check_connection_silent` | 잘못된 import로 항상 실패 반환 |
| 🔴 높음 | #2 `processEvents()` | 백그라운드 스레드에서 Qt 이벤트 처리 |
| 🟡 중간 | #3 `_config` 직접 접근 | private 속성 외부 수정 |
| 🟡 중간 | #4 main.py 크기 | 단일 파일 |
| 🟡 중간 | #5 FaceDetailer 반복 | 동일 패턴 17회 반복 |
| 🟡 중간 | #8 메시지박스 테마 | 다크테마 하드코딩 |
| 🟢 낮음 | #6 HTML 하드코딩 | 도움말을 별도 파일로 |
| 🟢 낮음 | #7 도움말 코드 중복 | 2곳에서 같은 로직 |
| 🟢 낮음 | #9 중복 requirements | 파일 2개가 동일 |
| 🟢 낮음 | #10 일본어 기본값 | "未確認" → "미확인" |
| 🟢 낮음 | #11 스레드 안전성 | worker 접근 보호 |
| 🟢 낮음 | #12 디버그 로그 | 프로덕션에 DEBUG 메시지 |
| 🟢 낮음 | #13 예외 삼킴 | `except: pass` 패턴 |
| 🟢 낮음 | #14 테스트 부족 | 핵심 로직 테스트 없음 |
| ✅ 완료 | #15 버튼 텍스트 | 텍스트 반전 + 공백 → **수정됨** |"""

content = content.replace(old_priority, new_priority)

path.write_text(content, encoding='utf-8')
print('2단계 완료: #15 제거 및 우선순위 테이블 업데이트')
