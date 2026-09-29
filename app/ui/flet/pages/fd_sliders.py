"""FaceDetailer 슬라이더의 실제 범위 (원본 Qt 슬라이더에서 추출).

assets/ui/main_ui.py 의 QSlider.setMinimum/setMaximum 값을 그대로 옮긴 표다.
슬라이더마다 범위가 모두 다르므로 이 표를 단일 진실로 삼는다.

    Qt 정수 슬라이더 값 --배율--> 실제 값

- steps / feather / drop_size / cycle / *_dilation / *_expansion / guide_size
  는 그대로 실수 값이 된다.
- cfg 는 Qt 값/10 (Qt 40 -> cfg 4.0)
- guide_size, max_size 는 Qt 값×64 (Qt 4 -> 256)
- bbox_threshold, sam_threshold, sam_mask_hint_threshold 는 Qt 값/100
- bbox_crop_factor 는 Qt 값/100 (Qt 150 -> 1.50)
"""

from __future__ import annotations

from typing import Dict, Tuple

# 위젯 이름 -> (qt 최소, qt 최대, qt 기본값, 실제값 배제, 표시 자릿수)
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
