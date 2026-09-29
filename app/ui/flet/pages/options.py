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
from app.ui.flet.theme.tokens import TOKENS, radius

SAMPLER_OPTIONS = [(label, value) for label, value in SAMPLER_NAMES.items()]
SCHEDULER_OPTIONS = [(name, name) for name in SCHEDULER_NAMES]

RESOLUTION_PRESETS = ["1152x896", "1024x1024", "896x1152",
                      "832x1216", "768x1344", "512x512"]

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
_FD_GROUPS = [
    ("기본 보정", ["facedetailer_denoise", "facedetailer_steps",
                   "facedetailer_cfg", "facedetailer_cycle"]),
    ("얼굴 영역", ["facedetailer_guide_size", "facedetailer_max_size",
                   "facedetailer_feather", "facedetailer_drop_size"]),
    ("탐지 · SAM", ["facedetailer_bbox_threshold", "facedetailer_bbox_dilation",
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


# 값 표시/역변환이 스펙 정보를 바로 참조하므로 키를 앞에 만든다.
_FD_SPEC_BY_KEY = {key: (default, factor, is64)
                   for key, _name, default, factor, is64
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
    default, factor, is64 = _FD_SPEC_BY_KEY.get(key, (0, 1.0, False))
    try:
        if is64:
            return f"{int(float(value) * 64)}"
        if key in _FD_INT_KEYS:
            return f"{int(round(float(value)))}"
        if factor == 100.0:
            return f"{float(value):.2f}"
        return f"{float(value):.1f}"
    except (TypeError, ValueError):
        return str(value)


def _build_fd_slider(default, factor: float, is_step_64: bool) -> ft.Slider:
    """스펙 한 항목을 Flet 슬라이더로 만든다 (Qt 배율 환산 되돌리기)."""
    if is_step_64:
        # 원본: 0~16 정수 슬라이더, 실제값 = 값 * 64
        return ft.Slider(min=0, max=16, value=float(default) // 64,
                         divisions=16, label="{value} × 64")
    if factor == 100.0:
        # 원본: 0~100 정수 슬라이더, 실제값 = 값 / 100 (0~1 실수)
        return ft.Slider(min=0.0, max=1.0, value=float(default),
                         divisions=100, label="{value}")
    return ft.Slider(min=0.0, max=float(default) * 2, value=float(default),
                     divisions=20, label="{value}")



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

        self._model_dropdown = ft.Dropdown(
            options=[ft.DropdownOption(key=n, text=n) for n in self._model_names],
            value=self._model_names[0] if self._model_names else None,
            label="모델", width=240)
        self._lm_model_dropdown = ft.Dropdown(
            options=[], label="LM Studio 모델", width=240)
        self._resolution_dropdown = ft.Dropdown(
            options=[ft.DropdownOption(key=r, text=r) for r in RESOLUTION_PRESETS],
            value=RESOLUTION_PRESETS[0], label="해상도", width=240)
        self._seed_field = ft.TextField(
            label="Seed", hint_text="-1 = 랜덤", value="-1", width=240, dense=True)
        self._negative_field = ft.TextField(
            label="네거티브 프롬프트", multiline=True, min_lines=2, max_lines=4)

        # --- 고급 옵션 (기본값은 접힘) ---
        self._steps_slider = ft.Slider(min=1, max=60, value=20, divisions=59,
                                       label="{value}")
        self._cfg_slider = ft.Slider(min=0, max=20, value=4.5, divisions=80,
                                     label="{value}")
        self._sampler_dropdown = ft.Dropdown(
            options=[ft.DropdownOption(key=value, text=label)
                     for label, value in SAMPLER_OPTIONS],
            value="euler", width=190, dense=True)
        self._scheduler_dropdown = ft.Dropdown(
            options=[ft.DropdownOption(key=name, text=name) for name in SCHEDULER_OPTIONS],
            value="normal", width=190, dense=True)
        self._denoise_slider = ft.Slider(min=0.0, max=1.0, value=1.0,
                                         divisions=20, label="{value}")

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

        for key, _name, default, factor, is64 in FACEDETAILER_SLIDER_SPECS:
            slider = _build_fd_slider(default, factor, is64)
            slider.on_change = self._make_fd_label_updater(key)
            self._fd_sliders[key] = slider
            self._fd_value_labels[key] = ft.Text(
                _format_fd_value(key, default),
                size=TOKENS.size_caption, color=TOKENS.on_surface_variant,
                width=64, text_align=ft.TextAlign.RIGHT)

        # 원본의 SAM 탐지 방식 ComboBox + 네거티브 마스크 체크
        self._fd_sam_hint = ft.Dropdown(
            options=[ft.DropdownOption(key=value, text=label)
                     for label, value in SAM_HINT_OPTIONS],
            value="bbox", label="SAM 탐지", width=190, dense=True)
        self._fd_sam_negative = ft.Switch(
            label="네거티브 마스크 사용", value=False)


        self._fd_groups: List[ft.Control] = [
            collapsible(
                title,
                ft.Column(
                    controls=[ft.Row(
                                controls=[
                                    ft.Text(_FD_LABELS.get(key, key),
                                            size=TOKENS.size_caption,
                                            color=TOKENS.on_surface_variant),
                                    ft.Container(expand=True),
                                    self._fd_value_labels[key],
                                    self._fd_sliders[key],
                                ],
                                spacing=TOKENS.space_sm, tight=True)
                              for key in keys if key in self._fd_sliders],
                    spacing=TOKENS.space_xs, tight=True),
                subtitle=f"{len(keys)}項",
                expanded=(index == 0))
            for index, (title, keys) in enumerate(_FD_GROUPS)
        ]

        self._fd_options = ft.Column(
            controls=[
                option_row("SAM 탐지", self._fd_sam_hint),
                self._fd_sam_negative,
                *self._fd_groups,
            ],
            spacing=TOKENS.space_sm, tight=True, visible=False)

    def _make_fd_label_updater(self, key: str):
        """슬라이더를 움직이면 옆 값 라벨을 갱신하는 콜백을 만든다."""
        def handle(_event: ft.Event) -> None:
            label = self._fd_value_labels.get(key)
            if label is not None:
                label.value = _format_fd_value(key, self._fd_sliders[key].value)
                safe_update(label)
        return handle

    def _handle_fd_toggle(self, event: ft.Event) -> None:
        self._facedetailer.enabled = bool(event.control.value)
        self._fd_options.visible = self._facedetailer.enabled
        safe_update(self._fd_options)


    # --- 레이아웃 ---------------------------------------------------------
    def _label(self, text: str, control: ft.Control) -> ft.Control:
        return ft.Column(
            controls=[ft.Text(text, size=TOKENS.size_caption,
                              color=TOKENS.on_surface_variant), control],
            spacing=TOKENS.space_xs, tight=True)

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
                option_row("Steps", self._steps_slider),
                option_row("CFG", self._cfg_slider),
                option_row("Sampler", self._sampler_dropdown),
                option_row("Scheduler", self._scheduler_dropdown),
                option_row("Denoise", self._denoise_slider),
            ],
            spacing=TOKENS.space_sm, tight=True)
        return collapsible("고급 옵션", body,
                           subtitle="Steps · CFG · Sampler · Scheduler · Denoise")

    def _build_facedetailer(self) -> ft.Control:
        count = len(FACEDETAILER_SLIDER_SPECS)
        return ft.Column(
            controls=[
                self._fd_switch,
                collapsible("FaceDetailer 상세", self._fd_options,
                            subtitle=f"{count}개 항목"),
            ],
            spacing=TOKENS.space_xs, tight=True)


    def build(self) -> ft.Control:
        """좌측 옵션 패널 (세로 스크롤)."""
        return ft.Container(
            content=ft.Column(
                controls=[
                    self._section("기본", [
                        self._label("ComfyUI 모델", self._model_dropdown),
                        self._label("LM Studio 모델", self._lm_model_dropdown),
                        self._label("해상도", self._resolution_dropdown),
                        self._label("Seed", self._seed_field),
                    ]),
                    self._section("네거티브", [self._negative_field]),
                    self._build_advanced(),
                    ft.Divider(height=1, color=TOKENS.outline),
                    self._build_facedetailer(),
                ],
                spacing=TOKENS.space_md,
                scroll=ft.ScrollMode.AUTO),
            width=280,
            bgcolor=TOKENS.surface,
            padding=ft.Padding.all(TOKENS.space_lg),
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
        for key, _widget, default, _factor, is64 in FACEDETAILER_SLIDER_SPECS:
            name = _fd_attr_name(key)
            raw = self._fd_sliders[key].value
            try:
                if is64:
                    value: object = int(float(raw) * 64)
                elif name in _FD_INT_KEYS:
                    value = int(round(float(raw)))
                else:
                    value = float(raw)
            except (TypeError, ValueError):
                value = _default
            setattr(self._facedetailer, name, value)

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
        for key, _widget, _default, _factor, is64 in FACEDETAILER_SLIDER_SPECS:
            saved = getattr(self._facedetailer, _fd_attr_name(key), None)
            if saved is None:
                continue
            slider = self._fd_sliders.get(key)
            if slider is not None:
                slider.value = (float(saved) / 64.0) if is64 else float(saved)
            label = self._fd_value_labels.get(key)
            if label is not None:
                # 라벨은 슬라이더 값(표시 단위)을 받는다.
                # 실제값을 다시 넣으면 64단위 항목이 이중으로 곱해진다.
                label.value = _format_fd_value(key, slider.value)
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

