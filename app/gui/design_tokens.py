"""공통 디자인 토큰 — ZAnimeStyleButton / SplitTextButton / PlayStopButton 공유.

세 버튼이 동일한 디자인 언어(곡률, 그림자, 애니메이션 곡선, 포커스 스타일)를
공유할 수 있도록 색상·크기·시간·이asing 값을 한 곳에서 관리한다.
"""
from __future__ import annotations

from PySide6.QtCore import QEasingCurve

# --------------------------------------------------------------------------- #
# 곡률 / 스페이스
# --------------------------------------------------------------------------- #
CORNER_RADIUS = 8          # px — 모든 버튼의 모서리 둥글기
CORNER_RADIUS_LARGE = 14   # px — SplitTextButton pill
PADDING_H = 16             # px — 가로 내부 여백
PADDING_V = 8              # px — 세로 내부 여백
ICON_GAP = 8               # px — 아이콘과 텍스트 사이 간격

# --------------------------------------------------------------------------- #
# 그림자 (resting / hover)
# --------------------------------------------------------------------------- #
SHADOW_REST = {
    "blur": 8,
    "offset_y": 4,
    "alpha": 0.22,
}
SHADOW_HOVER = {
    "blur": 18,
    "offset_y": 8,
    "alpha": 0.40,
}

# --------------------------------------------------------------------------- #
# hover lift (위로 올라가는 픽셀)
# --------------------------------------------------------------------------- #
LIFT_ZANIME = 2
LIFT_SPLITTEXT = 4
LIFT_PLAYSTOP = 2

# --------------------------------------------------------------------------- #
# 애니메이션 시간 (ms)
# --------------------------------------------------------------------------- #
DURATION_FAST = 180       # ZAnime chip hover
DURATION_MEDIUM = 260     # SplitText hover
DURATION_SLOW = 420       # PlayStop toggle transition

# --------------------------------------------------------------------------- #
# 이징 곡선
# --------------------------------------------------------------------------- #
EASE_OUT_CUBIC = QEasingCurve.Type.OutCubic
EASE_IN_OUT_CUBIC = QEasingCurve.Type.InOutCubic
EASE_OUT_QUART = QEasingCurve.Type.OutQuart

# --------------------------------------------------------------------------- #
# 포커스 링 (키보드 네비게이션용 — WCAG 2.1 AA)
# --------------------------------------------------------------------------- #
FOCUS_BORDER_WIDTH = 2
FOCUS_BORDER_STYLE = "dashed"
FOCUS_BORDER_COLOR = "#EC4899"  # Accent

# --------------------------------------------------------------------------- #
# 기본 색상 (테마 색상이 없을 때의 폴백)
# --------------------------------------------------------------------------- #
DEFAULT_BG = "#0078D4"        # Primary (Fluent Blue)
DEFAULT_TEXT = "#FFFFFF"
DEFAULT_UNSELECTED_BG = "#2C2C2C"
DEFAULT_UNSELECTED_TEXT = "#E0E0E0"
DEFAULT_UNSELECTED_BORDER = "#404040"
DEFAULT_STOP_BG = "#C42B1C"   # Destructive
DEFAULT_SUCCESS_BG = "#4ED9A3"
DEFAULT_WARNING_BG = "#F0B90B"

# --------------------------------------------------------------------------- #
# 텍스트 샘플 (PlayStopButton 텍스트 크로스페이드용)
# --------------------------------------------------------------------------- #
PLAY_TEXT = "이미지 생성 시작"
STOP_TEXT = "정지"