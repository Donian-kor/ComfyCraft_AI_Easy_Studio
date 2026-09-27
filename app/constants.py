"""공통 상수 정의 — main.py에서 분리됨 (Phase 1)."""

ZANIME_STYLE_CHOICES = (
    ("webtoon", "🇰🇷 웹툰"),
    ("japanime", "🇯🇵 일본애니"),
    ("basic", "✨ 기본"),
)

ZANIME_STYLE_LABELS = {value: label for value, label in ZANIME_STYLE_CHOICES}

PROMPT_MAX_CHARACTERS = 5000

# FaceDetailer 슬라이더 설정 명세: (키, 슬라이더 위젯 이름, 기본값, 배율, 64단위 여부)
FACEDETAILER_SLIDER_SPECS = [
    ("facedetailer_denoise", "facedetailerDenoiseSlider", 0.40, 100.0, False),
    ("facedetailer_steps", "facedetailerStepsSlider", 20, 1.0, False),
    ("facedetailer_cfg", "facedetailerCfgSlider", 4.0, 10.0, False),
    ("facedetailer_guide_size", "facedetailerGuideSizeSlider", 256, 1.0, True),
    ("facedetailer_max_size", "facedetailerMaxSizeSlider", 768, 1.0, True),
    ("facedetailer_feather", "facedetailerFeatherSlider", 5, 1.0, False),
    ("facedetailer_bbox_threshold", "facedetailerBboxThresholdSlider", 0.50, 100.0, False),
    ("facedetailer_bbox_dilation", "facedetailerBboxDilationSlider", 10, 1.0, False),
    ("facedetailer_bbox_crop_factor", "facedetailerBboxCropFactorSlider", 1.50, 100.0, False),
    ("facedetailer_sam_dilation", "facedetailerSamDilationSlider", 0, 1.0, False),
    ("facedetailer_sam_threshold", "facedetailerSamThresholdSlider", 0.93, 100.0, False),
    ("facedetailer_sam_bbox_expansion", "facedetailerSamBboxExpansionSlider", 0, 1.0, False),
    ("facedetailer_sam_mask_hint_threshold", "facedetailerSamMaskHintThresholdSlider", 0.70, 100.0, False),
    ("facedetailer_cycle", "facedetailerCycleSlider", 1, 1.0, False),
    ("facedetailer_drop_size", "facedetailerDropSizeSlider", 10, 1.0, False),
]
