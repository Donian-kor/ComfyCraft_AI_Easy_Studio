"""2열 그리드(구분선 포함) 배치 헬퍼.

options.py 가 600줄 제한에 걸리지 않도록, 2열 배치 계산과 줄 만들기를
여기로 뺀다. 이 모듈은 '몇 px 인지'만 알고, 컨트롤 내용(FaceDetailer
슬라이더 등)은 모른다.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

import flet as ft

from app.constants import FACEDETAILER_SLIDER_SPECS
from app.ui.flet.theme.tokens import TOKENS
# 두 열 사이에 세로 구분선을 세운다.
#   칸 175 + 여백 5 + 선 1 + 칸 175 = 356  (사용 가능 폭과 정확히 일치)
# 구분선이 없으면 '왼쪽 칸 값인지 오른쪽 칸 값인지' 헷갈리는데,
# 특히 값 라벨이 오른쪽 정렬이라 왼쪽 칸의 값이 오른쪽에 붙어 보인다.
GRID_DIVIDER = 1                        # 구분선 두께(px)
# 여백을 5 -> 12 로 넓힌 이유: 값 라벨(0.40, 4.0)이 오른쪽 정렬이라
# 구분선 바로 옆까지 차오른다. 5px 였을 때 숫자가 선에 달라붙어
# '4.0|Steps' 처럼 보여 어느 칸 값인지 읽기 어려웠다.
GRID_DIVIDER_GAP = 12                   # 구분선 좌우 여백(px)
GRID_ROW_SPACING = TOKENS.space_md      # 줄(세로) 사이 간격
# 한 줄 폭 = 칸 + (여백 + 구분선 + 칸) 이므로 구분선 자리를 빼고 나눈다.
# 이걸 빠뜨리면 한 줄이 GRID_AVAILABLE 를 넘겨 collapsible 안쪽에서 잘린다.
GRID_DIVIDER_TOTAL = GRID_DIVIDER + GRID_DIVIDER_GAP * 2   # 25


def build_grid(cells: List[ft.Control],
               column_width: int) -> ft.Control:
    """제목+컨트롤 묶음을 2열로 배치하고 열 사이에 구분선을 세운다.

    자동 줄바꿈(Row(wrap=True)) 대신 '두 개씩 묶어 줄을 직접 만든다'.
    줄마다 구분선을 정확히 같은 자리에 세우려면 Flet 이 알아서 줄을
    나누게 하면 안 된다 — 어느 칸 뒤에 줄이 접힐지 알 수 없어
    구분선이 칸 사이에 있지 않게 되기 때문이다.

    구분선은 '구분선 컨트롤'을 세우는 대신 '오른쪽 칸의 왼쪽 테두리'
    (border) 로 그린다. 세로로 늘어나는 컨트롤(STRETCH 등)을 넣으면
    스크롤 Column 안에서 높이가 무한대가 되어 아래 전부 화면에서
    밀려나기 때문이다. 테두리는 내용 높이에 딱 붙는다.

    항목 수가 홀수면 마지막 줄은 한 칸만 둔다. (빈 칸에 구분선을
    그리면 '항목이 하나 빠졌다'고 오해하게 된다)
    """
    rows: List[ft.Control] = []
    for start in range(0, len(cells), 2):
        pair = cells[start:start + 2]
        if len(pair) == 1:                      # 홀수: 마지막 한 칸
            rows.append(ft.Row(controls=pair, spacing=0))
            continue
        rows.append(ft.Row(
            controls=[
                # 왼쪽 칸: 오른쪽에 여백을 두어 값 라벨이 구분선에 붙지 않게
                ft.Container(
                    content=pair[0],
                    padding=ft.Padding.only(right=GRID_DIVIDER_GAP),
                    width=column_width + GRID_DIVIDER_GAP),
                ft.Container(
                    content=pair[1],
                    # 왼쪽 테두리가 곧 구분선이다. 내용 높이를 그대로
                    # 따라가므로 세로로 늘어나는 컨트롤이 필요 없다.
                    border=ft.Border(
                        left=ft.BorderSide(GRID_DIVIDER,
                                           TOKENS.outline_variant)),
                    padding=ft.Padding.only(left=GRID_DIVIDER_GAP),
                    width=column_width + GRID_DIVIDER_GAP + GRID_DIVIDER),
            ],
            spacing=0))
    return ft.Column(controls=rows, spacing=GRID_ROW_SPACING, tight=True)

# ---------------------------------------------------------------------------
# FaceDetailer 슬라이더의 실제 범위 (원본 Qt 슬라이더에서 추출)
# ---------------------------------------------------------------------------

# assets/ui/main_ui.py 의 QSlider.setMinimum/setMaximum 값을 그대로 옮긴 표다.
# 슬라이더마다 범위가 모두 다르므로 이 표를 단일 진실로 삼는다.
#
#     Qt 정수 슬라이더 값 --배율--> 실제 값
#
# - steps / feather / drop_size / cycle / *_dilation / *_expansion / guide_size
#   는 그대로 실수 값이 된다.
# - cfg 는 Qt 값/10 (Qt 40 -> cfg 4.0)
# - guide_size, max_size 는 Qt 값×64 (Qt 4 -> 256)
# - bbox_threshold, sam_threshold, sam_mask_hint_threshold 는 Qt 값/100
# - bbox_crop_factor 는 Qt 값/100 (Qt 150 -> 1.50)

# 위젯 이름 -> (qt 최소, qt 최대, qt 기본값, 실제값 배율, 표시 자릿수)
FD_SLIDER_RANGES: Dict[str, Tuple[int, int, int, float, int]] = {
    "facedetailerDenoiseSlider": (0, 100, 40, 100.0, 2),
    "facedetailerStepsSlider": (1, 50, 20, 1.0, 0),
    "facedetailerCfgSlider": (0, 200, 40, 10.0, 1),
    "facedetailerFeatherSlider": (0, 20, 5, 1.0, 0),
    "facedetailerDropSizeSlider": (1, 100, 10, 1.0, 0),
    "facedetailerGuideSizeSlider": (1, 16, 4, 64.0, 0),
    "facedetailerMaxSizeSlider": (2, 32, 12, 64.0, 0),
    "facedetailerCycleSlider": (1, 10, 1, 1.0, 0),
    "facedetailerBboxThresholdSlider": (10, 100, 50, 100.0, 2),
    "facedetailerBboxDilationSlider": (-20, 100, 10, 1.0, 0),
    "facedetailerBboxCropFactorSlider": (100, 500, 150, 100.0, 2),
    "facedetailerSamThresholdSlider": (10, 100, 93, 100.0, 2),
    "facedetailerSamDilationSlider": (0, 100, 0, 1.0, 0),
    "facedetailerSamBboxExpansionSlider": (0, 100, 0, 1.0, 0),
    "facedetailerSamMaskHintThresholdSlider": (10, 100, 70, 100.0, 2),
}

# Qt 값에 64 를 곱해 실제 픽셀 값으로 되돌리는 항목
_STEP_64_WIDGETS = {"facedetailerGuideSizeSlider", "facedetailerMaxSizeSlider"}


def is_step_64(widget_name: str) -> bool:
    return widget_name in _STEP_64_WIDGETS

# --- Qt 슬라이더 값 <-> 실제 설정값 변환 (원본 배율 규칙) ---
#
# Qt 는 정수 슬라이더였고 실제 값은 배율/64단위로 환산했다. 화면에는
# Qt 값(정수)을 그대로 보여주고 to_request() 에서 여기서 되돌린다. 배량을
# 화면에서 되돌리면 슬라이더가 max 범위를 벗어나 죽는다.
SPEC_BY_KEY: Dict[str, tuple] = {
    key: (default, factor, is64, widget_name)
    for key, widget_name, default, factor, is64 in FACEDETAILER_SLIDER_SPECS
}

# 정수처럼 보여줄 항목 (소수점은 슬라이더 값만 보이면 되므로 생략)
INT_KEYS = {
    "facedetailer_steps", "facedetailer_guide_size", "facedetailer_max_size",
    "facedetailer_feather", "facedetailer_bbox_dilation",
    "facedetailer_sam_dilation", "facedetailer_sam_bbox_expansion",
    "facedetailer_cycle", "facedetailer_drop_size",
}

def attr_name(key: str) -> str:
    """'facedetailer_denoise' -> 'denoise' (FaceDetailerSettings 필드명)."""
    return key[len("facedetailer_"):]

def to_real_value(key: str, qt_value) -> object:
    """Qt 슬라이더 값을 실제 설정값으로 환산한다."""
    name = attr_name(key)
    widget = SPEC_BY_KEY.get(key, (0, 1.0, False, ""))[3]
    try:
        raw = float(qt_value)
    except (TypeError, ValueError):
        return SPEC_BY_KEY.get(key, (0, 1.0, False, ""))[0]
    if widget in FD_SLIDER_RANGES:
        _qmin, _qmax, _qdef, factor, _d = FD_SLIDER_RANGES[widget]
        if is_step_64(widget):
            value: object = int(round(raw * 64))
        elif name in INT_KEYS:
            value = int(round(raw))
        else:
            value = round(raw / factor, 6)
        return value
    if name in INT_KEYS:
        return int(round(raw))
    return raw

def to_qt_value(key: str, real_value) -> float:
    """실제 설정값을 Qt 슬라이더 값으로 되돌린다 (스냅샷 복원용)."""
    widget = SPEC_BY_KEY.get(key, (0, 1.0, False, ""))[3]
    if widget not in FD_SLIDER_RANGES:
        return 0.0
    qt_min, qt_max, _qdef, factor, _d = FD_SLIDER_RANGES[widget]
    try:
        raw = float(real_value)
    except (TypeError, ValueError):
        return float(qt_min)
    qt_value = raw / 64.0 if is_step_64(widget) else raw * factor
    # 슬라이더가 값을 받는 순간 예외를 던지므로 범위를 여기서 지킨다.
    return min(float(qt_max), max(float(qt_min), qt_value))

def format_value(key: str, value) -> str:
    """슬라이더 옆에 표시할 실제 값 (Qt 배율/64단위를 되돌린 값)."""
    digits = 2
    if key in SPEC_BY_KEY:
        widget = SPEC_BY_KEY[key][3]
        digits = FD_SLIDER_RANGES.get(widget, (0, 100, 0, 1.0, 2))[4]
    try:
        text = f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return str(value)
    # 20.00 -> 20, 0.40 은 그대로
    return text[:-3] if text.endswith(".00") else text
