"""Phase 9: Settings (독립 Page).

기존 설정 다이얼로그를 7개 섹션 구조로 재구성한다.
저장되는 설정값과 데이터 구조(ConfigManager)는 그대로 유지된다.
"""

from __future__ import annotations

from typing import Callable, List, Optional

import flet as ft

from app.application.services import AppServices
from app.ui.flet.components.common import padded_column
from app.ui.flet.theme.tokens import TOKENS, radius

SETTINGS_SECTIONS = ["General", "Appearance", "Connections", "Models",
                     "Generation", "Storage", "Logs"]


def _safe_update(control: ft.Control) -> None:
    try:
        control.update()
    except RuntimeError:
        pass


class SettingsPage:
    """설정 화면. 변경을 ConfigManager 로 즉시 저장한다."""

    def __init__(self, services: AppServices, *,
                 on_saved: Optional[Callable[[str], None]] = None) -> None:
        self._services = services
        self._on_saved = on_saved
        config = services.config

        self._comfy_url = ft.TextField(label="ComfyUI 주소", value=config.comfyui.url,
                                       width=360)
        self._lm_url = ft.TextField(label="LM Studio 주소", value=config.lmstudio.url,
                                    width=360)
        self._lm_model = ft.TextField(label="LM Studio 모델", value=config.lmstudio.model,
                                      width=360)
        self._output_dir = ft.TextField(label="출력 폴더",
                                        value=config.output.directory, width=360)
        self._filename_prefix = ft.TextField(label="파일 이름 접두사",
                                             value=config.output.filename_prefix,
                                             width=360)
        self._max_wait = ft.TextField(
            label="최대 대기 시간(초)", value=str(config.comfyui.max_wait_seconds),
            width=360)
        self._poll_interval = ft.TextField(
            label="폴링 간격(초)", value=str(config.comfyui.poll_interval_seconds),
            width=360)
        self._status = ft.Text("", size=TOKENS.size_caption, color=TOKENS.success)

    # --- 섹션 빌더 -------------------------------------------------------
    @staticmethod
    def _section(title: str, controls: List[ft.Control]) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[ft.Text(title, size=TOKENS.size_body,
                                  weight=ft.FontWeight.W_600), *controls],
                spacing=TOKENS.space_sm, tight=True),
            bgcolor=TOKENS.surface,
            border_radius=radius(TOKENS.radius_lg),
            padding=ft.Padding.all(TOKENS.space_lg),
        )

    def _build_general(self) -> ft.Control:
        return self._section("General", [self._output_dir, self._filename_prefix])

    def _build_appearance(self) -> ft.Control:
        return self._section(
            "Appearance",
            [ft.Text("테마는 Material 3 다크 테마로 고정되어 있습니다.",
                     size=TOKENS.size_caption, color=TOKENS.on_surface_variant)])

    def _build_connections(self) -> ft.Control:
        return self._section("Connections",
                             [self._comfy_url, self._lm_url, self._lm_model])

    def _build_models(self) -> ft.Control:
        registry = self._services.model_registry
        names = ", ".join(p.name for p in registry.profiles[:12])
        return self._section(
            "Models",
            [ft.Text(f"등록된 모델 프로필 {len(registry.profiles)}개",
                     size=TOKENS.size_caption, color=TOKENS.on_surface_variant),
             ft.Text(names, size=TOKENS.size_caption, color=TOKENS.outline)])

    def _build_generation(self) -> ft.Control:
        return self._section("Generation", [self._max_wait, self._poll_interval])

    def _build_storage(self) -> ft.Control:
        return self._section(
            "Storage",
            [ft.Text(f"현재 출력 폴더: {self._services.output_dir}",
                     size=TOKENS.size_caption, color=TOKENS.on_surface_variant)])

    def _build_logs(self) -> ft.Control:
        return self._section(
            "Logs",
            [ft.Text("로그 파일: app.log", size=TOKENS.size_caption,
                     color=TOKENS.on_surface_variant)])


    # --- 저장 ------------------------------------------------------------
    def save(self, _event: Optional[ft.Event] = None) -> None:
        """입력값을 ConfigManager 에 반영하고 저장한다."""
        config = self._services.config
        try:
            config.comfyui.url = (self._comfy_url.value or "").strip()
            config.lmstudio.url = (self._lm_url.value or "").strip()
            config.lmstudio.model = (self._lm_model.value or "").strip()
            config.output.directory = (self._output_dir.value or "outputs").strip()
            config.output.filename_prefix = (self._filename_prefix.value or "").strip()
            config.comfyui.max_wait_seconds = int(self._max_wait.value or 600)
            config.comfyui.poll_interval_seconds = float(self._poll_interval.value or 1)
        except (TypeError, ValueError) as exc:
            self._status.value = f"숫자 항목이 올바르지 않습니다: {exc}"
            self._status.color = TOKENS.error
            _safe_update(self._status)
            return

        if self._services.config_manager.save():
            self._status.value = "저장했습니다."
            self._status.color = TOKENS.success
        else:
            self._status.value = "저장에 실패했습니다."
            self._status.color = TOKENS.error
        _safe_update(self._status)
        if self._on_saved is not None:
            self._on_saved(self._status.value)

    def build(self) -> ft.Control:
        builders = [self._build_general, self._build_appearance,
                    self._build_connections, self._build_models,
                    self._build_generation, self._build_storage, self._build_logs]

        return padded_column(
            controls=[
                ft.Row(
                    controls=[
                        ft.FilledButton("저장", icon=ft.Icons.SAVE, on_click=self.save),
                        self._status,
                    ],
                    spacing=TOKENS.space_md, tight=True),
                *[builder() for builder in builders],
            ],
            padding=TOKENS.space_lg,
            spacing=TOKENS.space_lg,
        )
