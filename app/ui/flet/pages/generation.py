"""Phase 5/6: Main Generation 화면.

기존 PySide6 화면을 복제하지 않는다. 중앙 미리보기 + 우측 설정 패널,
하단 진행 표시로 재구성했다.

이 모듈은 business 로직을 모른다. JobManager/Application 계층이
주입되고, 여기서는 값을 읽어 컨트롤에 반영할 뿐이다.
"""

from __future__ import annotations

from typing import Callable, List, Optional

import flet as ft

from app.constants import PROMPT_MAX_CHARACTERS
from app.features.prompt.prompts import SCHEDULER_NAMES, SAMPLER_NAMES
from app.models.generation import FaceDetailerSettings, GenerationRequest
from app.ui.flet.components.common import (
    collapsible,
    empty_state,
    labeled_field,
    option_row,
    safe_update,
)
from app.ui.flet.theme.tokens import TOKENS, radius

# Sampler 라벨 → 값 매핑을 Dropdown 이 바로 쓸 수 있게 뒤집는다.
SAMPLER_OPTIONS = [(label, value) for label, value in SAMPLER_NAMES.items()]
SCHEDULER_OPTIONS = [(name, name) for name in SCHEDULER_NAMES]


def parse_resolution(text: str, fallback: tuple = (1152, 896)) -> tuple:
    """'1152x896' 같은 해상도 문자열을 (w, h) 로 바꾼다."""
    try:
        w, h = str(text or "").lower().split("x", 1)
        return int(w), int(h)
    except (ValueError, AttributeError):
        return fallback


class GenerationPage:
    """이미지 생성 화면.

    컨트롤 트리와 현재 입력값을 함께 소유한다. 입력값을 그대로
    GenerationRequest 로 바꿔줄 수 있다(to_request).
    """

    def __init__(
        self,
        *,
        model_names: Optional[List[str]] = None,
        on_generate: Optional[Callable[[], None]] = None,
        on_stop: Optional[Callable[[], None]] = None,
        on_prompt_changed: Optional[Callable[[str], None]] = None,
    ) -> None:
        self._on_generate = on_generate
        self._on_stop = on_stop
        self._on_prompt_changed = on_prompt_changed
        self._model_names = list(model_names or [])
        self._facedetailer = FaceDetailerSettings()

        # --- 기본 옵션 ---
        self._model_dropdown = ft.Dropdown(
            options=[ft.DropdownOption(name) for name in self._model_names],
            value=self._model_names[0] if self._model_names else None,
            label="모델", width=220)
        self._resolution_dropdown = ft.Dropdown(
            options=[ft.DropdownOption("1152x896"), ft.DropdownOption("1024x1024"),
                     ft.DropdownOption("896x1152"), ft.DropdownOption("832x1216"),
                     ft.DropdownOption("768x1344"), ft.DropdownOption("512x512")],
            value="1152x896", label="해상도", width=220)
        self._seed_field = ft.TextField(
            label="Seed", hint_text="-1 = 랜덤", value="-1", width=220, dense=True)
        self._prompt_field = ft.TextField(
            label="프롬프트", multiline=True, min_lines=4, max_lines=8,
            max_length=PROMPT_MAX_CHARACTERS,
            hint_text="그릴 장면을 설명해 주세요",
            on_change=self._handle_prompt_change)
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
        # 하위 옵션 패널은 __init__ 에서 만든다. 레이아웃 빌드 여부와
        # 무관하게 상태(_fd_options.visible)를 읽고 쓸 수 있어야 한다.
        self._fd_options = ft.Column(
            controls=[
                option_row("Denoise", self._fd_denoise),
                option_row("Steps", self._fd_steps),
                option_row("CFG", self._fd_cfg),
                option_row("Cycle", self._fd_cycle),
            ],
            spacing=TOKENS.space_sm, tight=True, visible=False)

        # --- 미리보기 / 상태 ---
        self._preview = ft.Container(
            content=empty_state(
                ft.Icons.IMAGE_OUTLINED,
                "아직 만든 이미지가 없습니다",
                "프롬프트를 쓰고 [만들기] 를 눌러보세요"),
            expand=True, alignment=ft.Alignment(0.5, 0.5),
            bgcolor=TOKENS.surface_container,
            border_radius=radius(TOKENS.radius_lg))
        self._status_text = ft.Text("", size=TOKENS.size_caption,
                                    color=TOKENS.on_surface_variant)
        self._progress = ft.ProgressBar(value=0, visible=False)
        self._generate_button = ft.FilledButton(
            "만들기", icon=ft.Icons.AUTO_AWESOME, on_click=self._handle_generate)
        self._stop_button = ft.OutlinedButton(
            "중단", icon=ft.Icons.STOP_CIRCLE_OUTLINED,
            on_click=self._handle_stop, visible=False)

    # --- 이벤트 핸들러 ---------------------------------------------------
    def _handle_generate(self, _event: ft.Event) -> None:
        if self._on_generate is not None:
            self._on_generate()

    def _handle_stop(self, _event: ft.Event) -> None:
        if self._on_stop is not None:
            self._on_stop()

    def _handle_prompt_change(self, event: ft.Event) -> None:
        if self._on_prompt_changed is not None:
            self._on_prompt_changed(event.control.value or "")

    def _handle_fd_toggle(self, event: ft.Event) -> None:
        self._facedetailer.enabled = bool(event.control.value)
        self._fd_options.visible = self._facedetailer.enabled
        safe_update(self._fd_options)


    # --- 레이아웃 ---------------------------------------------------------
    def _build_basic_options(self) -> ft.Control:
        return ft.Column(
            controls=[
                labeled_field("모델", self._model_dropdown),
                labeled_field("해상도", self._resolution_dropdown),
                labeled_field("프롬프트", self._prompt_field),
                labeled_field("Seed", self._seed_field),
                ft.Container(height=TOKENS.space_sm),
                ft.Row(
                    controls=[self._generate_button, self._stop_button],
                    spacing=TOKENS.space_sm),
            ],
            spacing=TOKENS.space_md, tight=True)

    def _build_advanced_options(self) -> ft.Control:
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
        """FaceDetailer 패널. 옵션 컨테이너는 __init__ 에서 이미 만들어졌다."""
        return ft.Column(
            controls=[
                ft.Row(controls=[self._fd_switch, ft.Container(expand=True)],
                       tight=True),
                collapsible("FaceDetailer 상세", self._fd_options,
                            subtitle="선택 항목만 조정"),
            ],
            spacing=0, tight=True)

    def _build_side_panel(self) -> ft.Control:
        """우측 설정 패널. 세로 스크롤로 좁은 화면에서도 밀리지 않게 한다."""
        return ft.Container(
            content=ft.Column(
                controls=[
                    self._build_basic_options(),
                    ft.Divider(height=1, color=TOKENS.outline),
                    self._build_advanced_options(),
                    ft.Divider(height=1, color=TOKENS.outline),
                    self._build_facedetailer(),
                ],
                spacing=TOKENS.space_md,
                scroll=ft.ScrollMode.AUTO),
            width=300,
            padding=ft.Padding.only(left=TOKENS.space_lg),
        )

    def build(self) -> ft.Row:
        """중앙 미리보기 + 우측 설정 패널."""
        return ft.Row(
            controls=[
                ft.Container(content=self._preview, expand=True),
                self._build_side_panel(),
            ],
            expand=True,
            spacing=0,
            tight=True,
        )

    # --- 값 읽기/쓰기 ----------------------------------------------------
    def to_request(self, base: Optional[GenerationRequest] = None) -> GenerationRequest:
        """현재 입력값을 GenerationRequest 로 만든다.

        base 가 주어지면 그 설정을 유지한 채 사용자 입력만 덮어쓴다
        (URL, LM 모델 등 화면에 없는 값이 사라지지 않게 하기 위함).
        """
        request = base or GenerationRequest()
        width, height = parse_resolution(self._resolution_dropdown.value)

        request.prompt = self._prompt_field.value or ""
        request.negative_prompt = self._negative_field.value or ""
        request.comfy_model = self._model_dropdown.value or ""
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
        """ComfyUI 에서 읽어온 모델 목록을 반영한다."""
        self._model_names = list(model_names or [])
        self._model_dropdown.options = [ft.DropdownOption(n) for n in self._model_names]
        if self._model_names:
            self._model_dropdown.value = self._model_names[0]
        safe_update(self._model_dropdown)

    def show_result(self, image_path: str) -> None:
        """생성된 이미지를 미리보기에 표시한다."""
        self._preview.content = ft.Image(
            src=image_path, fit=ft.BoxFit.CONTAIN, expand=True,
            border_radius=radius(TOKENS.radius_md))
        safe_update(self._preview)

    def set_running(self, running: bool, message: str = "") -> None:
        """생성 중 상태에 맞춰 버튼/진행 표시를 바꾼다.

        화면을 다른 곳으로 옮겨도 Job 은 계속 돌기 때문에, 이 화면에
        돌아왔을 때도 상태가 살아 있어야 한다.
        """
        self._generate_button.disabled = running
        self._stop_button.visible = running
        self._progress.visible = running
        if message:
            self._status_text.value = message
        safe_update(self._generate_button, self._stop_button,
                    self._progress, self._status_text)

    def set_progress(self, percent: int) -> None:
        self._progress.value = max(0, min(percent, 100)) / 100.0
        safe_update(self._progress)

    def set_prompt(self, text: str) -> None:
        self._prompt_field.value = text
        safe_update(self._prompt_field)
