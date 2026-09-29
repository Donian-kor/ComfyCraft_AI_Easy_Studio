"""좌측 생성 옵션 패널 (원본 UI 의 leftScrollArea / optionsLayout).

원본 구조에서 옵션은 좌측에 붙어 있고, 프롬프트 입력과 전송은
챗봇 화면 아래에 있다. 따라서 이 패널에는 '무엇을 만들지 대한 설정'만
들고, 프롬프트 입력창은 두지 않는다.
"""

from __future__ import annotations

from typing import Callable, List, Optional

import flet as ft

from app.constants import FACEDETAILER_SLIDER_SPECS
from app.features.prompt.prompts import SCHEDULER_NAMES, SAMPLER_NAMES
from app.models.generation import FaceDetailerSettings, GenerationRequest
from app.ui.flet.components.common import (
    collapsible,
    option_row,
    safe_update,
)
from app.ui.flet.pages.fd_sliders import FD_SLIDER_RANGES, is_step_64
from app.ui.flet.theme.tokens import TOKENS, radius

SAMPLER_OPTIONS = [(label, value) for label, value in SAMPLER_NAMES.items()]
SCHEDULER_OPTIONS = [(name, name) for name in SCHEDULER_NAMES]

RESOLUTION_PRESETS = ["1152x896", "1024x1024", "896x1152",
                      "832x1216", "768x1344", "512x512"]

# --- 좌측 옵션 패널 폭 ------------------------------------------------------
# 패널 폭은 '화면에서 얼마나 자주 보이는가' 로 정한다.
# 원본 Qt 는 420 이었지만, 지금은 2열 그리드로 정보를 압축하므로
# 그보다 좁게 380 을 쓰면 챗봇 화면이 그만큼 더 넓어진다.
# 여기선 패널 안에서 '몇 열로 나눌지' 만 결정하고, 각 컨트롤의 폭은
# build() 에서 열 수에 맞춰 계산한다(하드코딩 폭을 두지 않는다).
PANEL_WIDTH = 380          # 패널 전체 폭
PANEL_PADDING = 24         # 패널 안쪽 여백 (TOKENS.space_lg)
CONTENT_WIDTH = PANEL_WIDTH - PANEL_PADDING * 2   # 실제 본문 폭(332)
FIELD_WIDTH = CONTENT_WIDTH            # 1열로 쓸 때 (드롭다운/텍스트 필드)
# 2열 그리드: 본문을 2등분하고 사이 간격만큼 뺀다.
GUTTER = TOKENS.space_md
# 2열 × GRID_COLUMN_WIDTH + GUTTER 가 CONTENT_WIDTH 를 넘지 않아야 한다.
# // 로 나눈 나머지를 한쪽에 몰아주지 않으면 1~3px 넘친다.
GRID_COLUMN_WIDTH = (CONTENT_WIDTH - GUTTER) // 2   # 2열 한 칸 폭
# option_row 는 [라벨][컨트롤] 2조각이라 컨트롤 폭을 줄여야 라벨까지 들어간다.
ROW_CONTROL_WIDTH = CONTENT_WIDTH - 88   # 라벨(최장 "Scheduler") + 여백
# FaceDetailer 행은 [라벨][값][슬라이더] 3조각이라 한 줄에 두면 너무 좁아진다.
# 라벨과 값을 한 줄 위쪽에 두고 슬라이더를 아래에 온전히 넓힌다.
FD_SLIDER_WIDTH = GRID_COLUMN_WIDTH - 8             # 2열 칸 안에 맞추되 살짝 여유


# --- FaceDetailer ----------------------------------------------------------
# 원본 Qt UI 는 슬라이더마다 (Label + Slider + 값 Label) 3개 위젯을 .ui 에
# 직접 적어 15종을 노출했다. 슬라이더를 하나라도 빼면 그 항목은 화면에서
# 조용히 사라지고 사용자는 "원래 없던 기능 같다"고 느낀다.
#
# 그래서 여기서 목록을 하드코딩하지 않는다. app.constants 의 스펙을 그대로
# 읽어 15종을 만들고, 스펙이 늘면 화면도 따라 늘어나게 한다.
#
# 스펙 형식: (키, 위젷 이름, 기본값, 배율, 64단위 여부)
#   - 배율 100.0 이면 Qt 의 0~100 정수 슬라이더를 원래 값(0~1 실수)으로 되돌린다.
#   - 64단위면 0~16 정수(×64)였고, 원래 값은 guide_size=256 처럼 64의 배수다.

_FD_LABELS = {
    "facedetailer_denoise": "Denoise",
    "facedetailer_steps": "Steps",
    "facedetailer_cfg": "CFG",
    "facedetailer_guide_size": "Guide Size",
    "facedetailer_max_size": "Max Size",
    "facedetailer_feather": "Feather",
    "facedetailer_bbox_threshold": "BBox Threshold",
    "facedetailer_bbox_dilation": "BBox Dilation",
    "facedetailer_bbox_crop_factor": "BBox Crop Factor",
    "facedetailer_sam_dilation": "SAM Dilation",
    "facedetailer_sam_threshold": "SAM Threshold",
    "facedetailer_sam_bbox_expansion": "SAM BBox Expansion",
    "facedetailer_sam_mask_hint_threshold": "SAM Mask Hint Threshold",
    "facedetailer_cycle": "Cycle",
    "facedetailer_drop_size": "Drop Size",
}

# 상세 패널을 3단으로 나눠 한 번에 15개를 다 보여주지 않는다.
# 원본도 facedetailerPanel 안에 스크롤을 두었다.
# 그룹 이름이 '탐지 · SAM' 이면 위쪽 'SAM 탐지' 드롭다운과 헷갈리므로
# '얼굴 탐지' 라고 부른다(같은 대상, 다른 역할임을 구분).
_FD_GROUPS = [
    ("기본 보정", ["facedetailer_denoise", "facedetailer_steps",
                   "facedetailer_cfg", "facedetailer_cycle"]),
    ("얼굴 영역", ["facedetailer_guide_size", "facedetailer_max_size",
                   "facedetailer_feather", "facedetailer_drop_size"]),
    ("얼굴 탐지", ["facedetailer_bbox_threshold", "facedetailer_bbox_dilation",
                   "facedetailer_bbox_crop_factor", "facedetailer_sam_dilation",
                   "facedetailer_sam_threshold", "facedetailer_sam_bbox_expansion",
                   "facedetailer_sam_mask_hint_threshold"]),
]

# SAM 탐지 방식 (원본 facedetailerPanel 의 ComboBox)
SAM_HINT_OPTIONS = [("bbox", "bbox"), ("rect-positive", "rect-positive"),
                    ("rect-negative", "rect-negative"),
                    ("point", "point"), ("point-bbox", "point-bbox")]


def _fd_attr_name(key: str) -> str:
    """'facedetailer_denoise' -> 'denoise' (FaceDetailerSettings 필드명)."""
    return key[len("facedetailer_"):]


# 값 표시/역변환이 범위 정보를 바로 참조하므로 키를 앞에 만든다.
_FD_SPEC_BY_KEY = {key: (default, factor, is64, widget_name)
                   for key, widget_name, default, factor, is64
                   in FACEDETAILER_SLIDER_SPECS}

# 정수처럼 보여줄 항목 (소수점은 슬라이더 값만 보이면 되므로 생략)
_FD_INT_KEYS = {
    "facedetailer_steps", "facedetailer_guide_size", "facedetailer_max_size",
    "facedetailer_feather", "facedetailer_bbox_dilation",
    "facedetailer_sam_dilation", "facedetailer_sam_bbox_expansion",
    "facedetailer_cycle", "facedetailer_drop_size",
}


def _format_fd_value(key: str, value) -> str:
    """슬라이더 옆에 표시할 실제 값 (Qt 배율/64단위를 되돌린 값)."""
    digits = 2
    if key in _FD_SPEC_BY_KEY:
        widget = _FD_SPEC_BY_KEY[key][3]
        digits = FD_SLIDER_RANGES.get(widget, (0, 100, 0, 1.0, 2))[4]
    try:
        text = f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return str(value)
    # 20.00 -> '20', 0.40 -> '0.40'
    return text[:-3] if text.endswith(".00") else text


def _build_fd_slider(widget_name: str) -> ft.Slider:
    """원본 Qt 슬라이더와 같은 범위/기본값으로 Flet 슬라이더를 만든다.

    Qt 는 정수 슬라이더였고, 실제 값은 배율로 환산했다. 화면에는 Qt 값
    (정수)을 그대로 보여주고 to_request() 에서 환산하므로 스냅샷 복원도
    같은 경로를 탄다. 배량을 여기서 되돌리면 범위가 어긋나
    'value must be less than or equal to max' 로 죽는다.
    """
    qt_min, qt_max, qt_default, _factor, _digits = FD_SLIDER_RANGES[widget_name]
    return ft.Slider(
        min=qt_min, max=qt_max,
        value=float(max(qt_min, qt_default)),
        divisions=max(1, qt_max - qt_min),
        width=FD_SLIDER_WIDTH,
        label="{value}")


def _fd_to_real_value(key: str, qt_value) -> object:
    """Qt 슬라이더 값을 실제 설정값으로 환산한다."""
    name = _fd_attr_name(key)
    widget = _FD_SPEC_BY_KEY.get(key, (0, 1.0, False, ""))[3]
    try:
        raw = float(qt_value)
    except (TypeError, ValueError):
        return _FD_SPEC_BY_KEY.get(key, (0, 1.0, False, ""))[0]
    if widget in FD_SLIDER_RANGES:
        _qmin, _qmax, _qdef, factor, _d = FD_SLIDER_RANGES[widget]
        if is_step_64(widget):
            value: object = int(round(raw * 64))
        elif name in _FD_INT_KEYS:
            value = int(round(raw))
        else:
            value = round(raw / factor, 6)
        return value
    if name in _FD_INT_KEYS:
        return int(round(raw))
    return raw


def _fd_to_qt_value(key: str, real_value) -> float:
    """실제 설정값을 Qt 슬라이더 값으로 되돌린다 (스냅샷 복원용)."""
    widget = _FD_SPEC_BY_KEY.get(key, (0, 1.0, False, ""))[3]
    if widget not in FD_SLIDER_RANGES:
        return 0.0
    qt_min, qt_max, _qdef, factor, _d = FD_SLIDER_RANGES[widget]
    try:
        raw = float(real_value)
    except (TypeError, ValueError):
        return float(qt_min)
    if is_step_64(widget):
        qt_value = raw / 64.0
    else:
        qt_value = raw * factor
    # 슬라이더가 값을 받는 순간 예외를 던지므로 범위를 여기서 지킨다.
    return min(float(qt_max), max(float(qt_min), qt_value))


def parse_resolution(text: str, fallback: tuple = (1152, 896)) -> tuple:
    """'1152x896' 같은 해상도 문자열을 (w, h) 로 바꾼다."""
    try:
        w, h = str(text or "").lower().split("x", 1)
        return int(w), int(h)
    except (ValueError, AttributeError):
        return fallback


class OptionsPanel:
    """생성 옵션 (모델 / 해상도 / Steps / CFG / Seed / FaceDetailer)."""

    def __init__(self, *, model_names: Optional[List[str]] = None) -> None:
        self._model_names = list(model_names or [])
        self._facedetailer = FaceDetailerSettings()

        # Dropdown 의 label 속성에는 라벨을 두지 않는다.
        # 바깥에서 _label() 로 제목 Text 를 붙이므로, 둘 다 넣으면
        # 'ComfyUI 모델' 위에 '모델' 이 겹쳐 보이고, 남은 zh-hans 글자
        # ('模型')까지 그대로 노출된다. 한 곳에서만 라벨을 만든다.
        self._model_dropdown = ft.Dropdown(
            options=[ft.DropdownOption(key=n, text=n) for n in self._model_names],
            value=self._model_names[0] if self._model_names else None,
            width=FIELD_WIDTH, dense=True)
        self._lm_model_dropdown = ft.Dropdown(
            options=[], width=FIELD_WIDTH, dense=True)
        self._resolution_dropdown = ft.Dropdown(
            options=[ft.DropdownOption(key=r, text=r) for r in RESOLUTION_PRESETS],
            value=RESOLUTION_PRESETS[0], width=FIELD_WIDTH, dense=True)
        self._seed_field = ft.TextField(
            hint_text="-1 = 랜덤", value="-1", width=FIELD_WIDTH, dense=True)
        self._negative_field = ft.TextField(
            label="네거티브 프롬프트", multiline=True, min_lines=2, max_lines=4)

        # --- 고급 옵션 (기본값은 접힘) ---
        # 필드는 패널 본문(FIELD_WIDTH) 을 한 줄로 다 쓴다.
        # option_row 안에서는 라벨이 왼쪽을 먹으므로 컨트롤만 줄인다.
        self._steps_slider = ft.Slider(min=1, max=60, value=20, divisions=59,
                                       width=ROW_CONTROL_WIDTH, label="{value}")
        self._cfg_slider = ft.Slider(min=0, max=20, value=4.5, divisions=80,
                                     width=ROW_CONTROL_WIDTH, label="{value}")
        self._sampler_dropdown = ft.Dropdown(
            options=[ft.DropdownOption(key=value, text=label)
                     for label, value in SAMPLER_OPTIONS],
            value="euler", width=ROW_CONTROL_WIDTH, dense=True)
        self._scheduler_dropdown = ft.Dropdown(
            options=[ft.DropdownOption(key=name, text=name) for name in SCHEDULER_OPTIONS],
            value="normal", width=ROW_CONTROL_WIDTH, dense=True)
        self._denoise_slider = ft.Slider(min=0.0, max=1.0, value=1.0,
                                         divisions=20, width=ROW_CONTROL_WIDTH,
                                         label="{value}")

        # --- FaceDetailer ---
        # 스펙(15종)으로 슬라이더를 만든다. 하나라도 빠뜨려도 화면에서
        # 조용히 사라지므로 반드시 스펙을 소스로 삼는다.
        self._fd_switch = ft.Switch(label="안면 보정", value=False,
                                    on_change=self._handle_fd_toggle)
        self._fd_sliders: Dict[str, ft.Slider] = {}
        self._fd_value_labels: Dict[str, ft.Text] = {}
        self._fd_specs = {key: (default, factor, is64)
                          for key, _name, default, factor, is64
                          in FACEDETAILER_SLIDER_SPECS}

        for key, widget_name, default, factor, is64 in FACEDETAILER_SLIDER_SPECS:
            slider = _build_fd_slider(widget_name)
            slider.on_change = self._make_fd_label_updater(key)
            self._fd_sliders[key] = slider
            self._fd_value_labels[key] = ft.Text(
                _format_fd_value(key, _fd_to_real_value(key, slider.value)),
                size=TOKENS.size_caption, color=TOKENS.on_surface_variant,
                # 2열이라 값 라벨이 칸을 많이 먹는다. 가장 긴 값
                # ('123.45' 같은 6자) 기준으로 42px 면 충분하다.
                width=42, no_wrap=True, text_align=ft.TextAlign.RIGHT)

        # 원본의 SAM 탐지 방식 ComboBox + 네거티브 마스크 체크
        self._fd_sam_hint = ft.Dropdown(
            options=[ft.DropdownOption(key=value, text=label)
                     for label, value in SAM_HINT_OPTIONS],
            value="bbox", width=FIELD_WIDTH, dense=True)
        self._fd_sam_negative = ft.Switch(
            label="네거티브 마스크 사용", value=False)


        # 15종을 2열로 올린다. 한 칸 폭이 좁으니 슬라이더 위에
        # [라벨 ..... 값] 을 두고, 그 아래에 슬라이더를 온전히 놓는다.
        self._fd_groups: List[ft.Control] = [
            collapsible(
                title,
                ft.Column(
                    controls=self._grid([
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text(_FD_LABELS.get(key, key),
                                                size=TOKENS.size_caption,
                                                color=TOKENS.on_surface_variant,
                                                no_wrap=True,
                                                overflow=ft.TextOverflow.ELLIPSIS),
                                        ft.Container(expand=True),
                                        self._fd_value_labels[key],
                                    ],
                                    spacing=TOKENS.space_xs, tight=True),
                                self._fd_sliders[key],
                            ],
                            spacing=2, tight=True, width=GRID_COLUMN_WIDTH)
                        for key in keys if key in self._fd_sliders
                    ]),
                    spacing=TOKENS.space_md, tight=True),
                subtitle=f"{len(keys)}項",
                expanded=(index == 0))
            for index, (title, keys) in enumerate(_FD_GROUPS)
        ]

        self._fd_options = ft.Column(
            controls=[
                # 라벨은 _label() 로 통일한다. option_row 는 라벨을 왼쪽에
                # 두고 컨트롤 폭을 줄이는 쪽이라, 2열 그리드와 어긋난다.
                self._label("얼굴 탐지 방식", self._fd_sam_hint),
                self._fd_sam_negative,
                *self._fd_groups,
            ],
            spacing=TOKENS.space_md, tight=True, visible=False)

    def _make_fd_label_updater(self, key: str):
        """슬라이더를 움직이면 옆 값 라벨을 실제 값으로 갱신하는 콜백."""
        def handle(_event: ft.Event) -> None:
            label = self._fd_value_labels.get(key)
            if label is not None:
                real = _fd_to_real_value(key, self._fd_sliders[key].value)
                label.value = _format_fd_value(key, real)
                safe_update(label)
        return handle

    def _handle_fd_toggle(self, event: ft.Event) -> None:
        self._facedetailer.enabled = bool(event.control.value)
        self._fd_options.visible = self._facedetailer.enabled
        safe_update(self._fd_options)


    # --- 레이아웃 ---------------------------------------------------------
    def _label(self, text: str, control: ft.Control,
               *, width: int = FIELD_WIDTH) -> ft.Control:
        """제목 + 컨트롤 세로 묶음 (라벨은 여기서만 만든다).

        width 를 주면 그 폭으로 고정한다. 2열 그리드에서는 GRID_COLUMN_WIDTH
        를 넘지 않도록 build() 에서 계산해 넘긴다.
        """
        return ft.Column(
            controls=[ft.Text(text, size=TOKENS.size_caption,
                              color=TOKENS.on_surface_variant), control],
            spacing=TOKENS.space_xs, tight=True, width=width)

    @staticmethod
    def _grid(cells: List[ft.Control]) -> ft.Control:
        """제목+컨트롤 묶음을 2열로 배치한다.

        해상도/Seed 처럼 짝이 자연스러운 항목은 한 줄에 두 개씩 올린다.
        셀 개수가 홀수면 마지막 칸은 비워 두고, 셀 폭은 2열 폭을 넘지
        않게 build() 에서 이미 맞춰둔다.
        """
        return ft.Row(
            controls=list(cells),
            spacing=GUTTER, wrap=True, run_spacing=GUTTER, tight=True)

    def _section(self, title: str, controls: List[ft.Control]) -> ft.Control:
        return ft.Container(
            content=ft.Column(
                controls=[ft.Text(title, size=TOKENS.size_caption,
                                  weight=ft.FontWeight.W_600,
                                  color=TOKENS.primary),
                          *controls],
                spacing=TOKENS.space_sm, tight=True),
            padding=ft.Padding.only(bottom=TOKENS.space_md),
        )

    def _build_advanced(self) -> ft.Control:
        body = ft.Column(
            controls=[
                option_row("Steps", self._steps_slider, width=ROW_CONTROL_WIDTH),
                option_row("CFG", self._cfg_slider, width=ROW_CONTROL_WIDTH),
                option_row("Sampler", self._sampler_dropdown, width=ROW_CONTROL_WIDTH),
                option_row("Scheduler", self._scheduler_dropdown,
                           width=ROW_CONTROL_WIDTH),
                option_row("Denoise", self._denoise_slider, width=ROW_CONTROL_WIDTH),
            ],
            spacing=TOKENS.space_sm, tight=True)
        return collapsible("고급 옵션", body,
                           subtitle="Steps · CFG · Sampler · Scheduler · Denoise")

    def _build_facedetailer(self) -> ft.Control:
        """안면 보정 스위치 하나를 누르면 15종이 바로 펼쳐진다.

        예전에는 'FaceDetailer 상세' 접기를 한 번 더 눌러야 해서
        '켜놨는데 안 보이니 왜 안 되지?' 하는 혼란이 있었다.
        접기 헤더를 두지 않고 스위치가 곧 펼치기 역할을 한다.
        """
        count = len(FACEDETAILER_SLIDER_SPECS)
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        self._fd_switch,
                        ft.Container(expand=True),
                        ft.Text(f"{count}개 항목", size=TOKENS.size_caption,
                                color=TOKENS.on_surface_variant),
                    ],
                    spacing=TOKENS.space_sm, tight=True),
                self._fd_options,
            ],
            spacing=TOKENS.space_xs, tight=True)


    def build(self) -> ft.Control:
        """좌측 옵션 패널 (세로 스크롤).

        기본 항목은 2열로 올린다. 모델처럼 값이 긴 항목은 1줄을 다 쓰고
        (모델 / LM 모델), 해상도·Seed처럼 짧은 짝은 한 줄에 두 개씩
        배치해 세로 길이를 줄인다.
        """
        # 2열 셀 폭: 한 칸이 CONTENT_WIDTH 를 넘지 않게 컨트롤까지 맞춘다.
        half = GRID_COLUMN_WIDTH
        for control in (self._resolution_dropdown, self._seed_field):
            control.width = half

        return ft.Container(
            content=ft.Column(
                controls=[
                    self._section("기본", [
                        self._label("ComfyUI 모델", self._model_dropdown),
                        self._label("LM Studio 모델", self._lm_model_dropdown),
                        self._grid([
                            self._label("해상도", self._resolution_dropdown,
                                        width=half),
                            self._label("Seed", self._seed_field, width=half),
                        ]),
                    ]),
                    self._section("네거티브", [self._negative_field]),
                    self._build_advanced(),
                    ft.Divider(height=1, color=TOKENS.outline),
                    self._build_facedetailer(),
                ],
                spacing=TOKENS.space_md,
                scroll=ft.ScrollMode.AUTO),
            width=PANEL_WIDTH,
            bgcolor=TOKENS.surface,
            padding=ft.Padding.all(PANEL_PADDING),
        )


    # --- 값 읽기/쓰기 ----------------------------------------------------
    def to_request(self, base: Optional[GenerationRequest] = None) -> GenerationRequest:
        """현재 옵션을 GenerationRequest 로 만든다.

        base 가 주어지면 유지한 채 옵션만 덮어쓴다 (프롬프트 등 화면 밖 값 보존).
        """
        request = base or GenerationRequest()
        width, height = parse_resolution(self._resolution_dropdown.value)

        request.negative_prompt = self._negative_field.value or ""
        request.comfy_model = self._model_dropdown.value or ""
        request.lm_model = self._lm_model_dropdown.value or ""
        request.width = width
        request.height = height

        try:
            request.seed = int((self._seed_field.value or "-1").strip())
        except (TypeError, ValueError):
            request.seed = -1

        request.steps = int(self._steps_slider.value or 20)
        request.cfg = float(self._cfg_slider.value or 4.5)
        request.sampler = str(self._sampler_dropdown.value or "euler")
        request.scheduler = str(self._scheduler_dropdown.value or "normal")
        request.denoise = float(self._denoise_slider.value or 1.0)

        # FaceDetailer: 스펙 15종을 빠짐없이 요청에 반영한다.
        # 하드코딩으로 몇 개만 넣으면 화면의 값이 조용히 버려진다.
        for key, _widget, default, _factor, _is64 in FACEDETAILER_SLIDER_SPECS:
            setattr(self._facedetailer, _fd_attr_name(key),
                    _fd_to_real_value(key, self._fd_sliders[key].value))

        self._facedetailer.enabled = bool(self._fd_switch.value)
        self._facedetailer.sam_detection_hint = str(
            self._fd_sam_hint.value or "bbox")
        self._facedetailer.sam_mask_hint_use_negative = bool(
            self._fd_sam_negative.value)
        request.facedetailer = self._facedetailer
        return request

    def set_model_options(self, model_names: List[str]) -> None:
        self._model_names = list(model_names or [])
        # DropdownOption 에 문자열을 직접 주면 key/text 가 빈칸이 되어
        # 화면에 아무것도 안 보인다. 반드시 key 와 text 를 함께 준다.
        self._model_dropdown.options = [
            ft.DropdownOption(key=name, text=name) for name in self._model_names]
        if self._model_names:
            self._model_dropdown.value = self._model_names[0]
        safe_update(self._model_dropdown)

    def set_lm_model_options(self, model_names: List[str]) -> None:
        names = list(model_names or [])
        self._lm_model_dropdown.options = [
            ft.DropdownOption(key=name, text=name) for name in names]
        if names:
            self._lm_model_dropdown.value = names[0]
        safe_update(self._lm_model_dropdown)


    def apply_snapshot(self, snapshot: dict) -> None:
        """이미지 카드의 '이 설정으로' — 지난 생성 설정을 되돌린다."""
        request = GenerationRequest.from_dict(snapshot or {})
        self._model_dropdown.value = request.comfy_model or None
        self._lm_model_dropdown.value = request.lm_model or None
        self._resolution_dropdown.value = f"{request.width}x{request.height}"
        self._seed_field.value = str(request.seed)
        self._negative_field.value = request.negative_prompt
        self._steps_slider.value = request.steps
        self._cfg_slider.value = request.cfg
        self._sampler_dropdown.value = request.sampler
        self._scheduler_dropdown.value = request.scheduler
        self._denoise_slider.value = request.denoise

        self._facedetailer = request.facedetailer
        self._fd_switch.value = self._facedetailer.enabled
        self._fd_options.visible = self._facedetailer.enabled

        # 스냅샷의 15종 값을 슬라이더와 표시 라벨에 되돌린다.
        # 실제값 -> Qt 슬라이더 값으로 환산한 뒤 넣는다. 그냥 넣으면
        # guide_size=256 처럼 max(16) 를 넘겨 Flet 이 예외를 던진다.
        for key, _widget, _default, _factor, _is64 in FACEDETAILER_SLIDER_SPECS:
            saved = getattr(self._facedetailer, _fd_attr_name(key), None)
            if saved is None:
                continue
            slider = self._fd_sliders.get(key)
            if slider is not None:
                slider.value = _fd_to_qt_value(key, saved)
            label = self._fd_value_labels.get(key)
            if label is not None:
                label.value = _format_fd_value(key, saved)
        self._fd_sam_hint.value = self._facedetailer.sam_detection_hint or "bbox"
        self._fd_sam_negative.value = bool(
            self._facedetailer.sam_mask_hint_use_negative)

        safe_update(self._model_dropdown, self._lm_model_dropdown,
                    self._resolution_dropdown, self._seed_field,
                    self._negative_field, self._steps_slider, self._cfg_slider,
                    self._sampler_dropdown, self._scheduler_dropdown,
                    self._denoise_slider, self._fd_switch, self._fd_options,
                    self._fd_sam_hint, self._fd_sam_negative,
                    *self._fd_sliders.values(), *self._fd_value_labels.values())

