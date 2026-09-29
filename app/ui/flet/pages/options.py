"""좌측 생성 옵션 패널 (원본 UI 의 leftScrollArea / optionsLayout).

원본 구조에서 옵션은 좌측에 붙어 있고, 프롬프트 입력과 전송은
챗봇 화면 아래에 있다. 따라서 이 패널에는 '무엇을 만들지 대한 설정'만
들고, 프롬프트 입력창은 두지 않는다.
"""

from __future__ import annotations

from typing import Callable, List, Optional

import flet as ft

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
            options=[ft.DropdownOption(n) for n in self._model_names],
            value=self._model_names[0] if self._model_names else None,
            label="모델", width=240)
        self._lm_model_dropdown = ft.Dropdown(
            options=[], label="LM Studio 모델", width=240)
        self._resolution_dropdown = ft.Dropdown(
            options=[ft.DropdownOption(r) for r in RESOLUTION_PRESETS],
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
            options=[ft.DropdownOption(name) for name in SCHEDULER_OPTIONS],
            value="normal", width=190, dense=True)
        self._denoise_slider = ft.Slider(min=0.0, max=1.0, value=1.0,
                                         divisions=20, label="{value}")

        # --- FaceDetailer ---
        self._fd_switch = ft.Switch(label="안면 보정", value=False,
                                    on_change=self._handle_fd_toggle)
        self._fd_denoise = ft.Slider(min=0.0, max=1.0, value=0.40, divisions=20,
                                     label="{value}")
        self._fd_steps = ft.Slider(min=1, max=60, value=20, divisions=59,
                                   label="{value}")
        self._fd_cfg = ft.Slider(min=0, max=20, value=4.0, divisions=80,
                                 label="{value}")
        self._fd_cycle = ft.Slider(min=1, max=8, value=1, divisions=7,
                                   label="{value}")
        self._fd_options = ft.Column(
            controls=[
                option_row("Denoise", self._fd_denoise),
                option_row("Steps", self._fd_steps),
                option_row("CFG", self._fd_cfg),
                option_row("Cycle", self._fd_cycle),
            ],
            spacing=TOKENS.space_sm, tight=True, visible=False)

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
        return ft.Column(
            controls=[
                self._fd_switch,
                collapsible("FaceDetailer 상세", self._fd_options,
                            subtitle="선택 항목만 조정"),
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

        self._facedetailer.denoise = float(self._fd_denoise.value or 0.40)
        self._facedetailer.steps = int(self._fd_steps.value or 20)
        self._facedetailer.cfg = float(self._fd_cfg.value or 4.0)
        self._facedetailer.cycle = int(self._fd_cycle.value or 1)
        request.facedetailer = self._facedetailer
        return request

    def set_model_options(self, model_names: List[str]) -> None:
        self._model_names = list(model_names or [])
        self._model_dropdown.options = [ft.DropdownOption(n) for n in self._model_names]
        if self._model_names:
            self._model_dropdown.value = self._model_names[0]
        safe_update(self._model_dropdown)

    def set_lm_model_options(self, model_names: List[str]) -> None:
        self._lm_model_dropdown.options = [ft.DropdownOption(n) for n in model_names]
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
        safe_update(self._model_dropdown, self._lm_model_dropdown,
                    self._resolution_dropdown, self._seed_field,
                    self._negative_field, self._steps_slider, self._cfg_slider,
                    self._sampler_dropdown, self._scheduler_dropdown,
                    self._denoise_slider, self._fd_switch, self._fd_options)
