"""설정 화면 (원본 settings_dialog.ui 의 3탭 구조).

    탭1 AI 서버 : ComfyUI 주소/상태/모델경로, LM Studio 주소/상태
    탭2 모델     : 자동 목록 + 수동 등록 (pages.profiles.ProfileEditor)
    탭3 로그     : 로그 창 (pages.log_panel.LogPanel)

저장되는 설정값과 데이터 구조(ConfigManager)는 변경하지 않는다.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Callable, List, Optional

import flet as ft

from app.application.services import AppServices
from app.paths import BASE_DIR
from app.ui.flet.components.common import safe_update, section_card
from app.ui.flet.pages.log_panel import LogPanel
from app.ui.flet.pages.profiles import ProfileEditor
from app.ui.flet.theme.tokens import TOKENS



def _join_paths(paths: List[Any]) -> str:
    """경로 목록을 설정 텍스트필드용 한 줄로 합친다."""
    return "; ".join(str(p) for p in paths or [])


def _split_paths(raw: str) -> List[str]:
    """'C:\\a; D:\\b' 같은 한 줄을 경로 목록으로 되돌린다."""
    return [part.strip() for part in (raw or "").split(";") if part.strip()]


def _model_base_paths(config: Any) -> List[str]:
    try:
        return [str(p) for p in (config.comfyui_model_paths or [])]
    except AttributeError:
        return []


def _lm_models(services: AppServices) -> List[str]:
    """LM Studio 모델 목록을 읽는다. 서버가 꺼져 있으면 빈 목록."""
    try:
        return list(services.model_fetcher.get_lmstudio_models() or [])
    except Exception:
        return []


class SettingsPage:
    """설정 화면. 원본 settings_dialog.ui 의 3탭 구조(서버/모델/로그)를 따른다.

    저장되는 설정값과 데이터 구조(ConfigManager)는 변경하지 않는다.
    """

    def __init__(self, services: AppServices, *,
                 on_saved: Optional[Callable[[str], None]] = None) -> None:
        self._services = services
        self._on_saved = on_saved
        config = services.config

        # --- 탭1: AI 서버 ---
        self._comfy_url = ft.TextField(label="ComfyUI 주소", width=460,
                                       value=config.comfyui.url)
        self._comfy_status = ft.Text("", size=TOKENS.size_caption)
        self._model_base_paths = ft.TextField(
            label="ComfyUI 模型 경로", width=460,
            value=_join_paths(_model_base_paths(config)))
        self._model_path_status = ft.Text("", size=TOKENS.size_caption)

        self._lm_url = ft.TextField(label="LM Studio 주소", width=460,
                                    value=config.lmstudio.url)
        lm_names = _lm_models(services)
        self._lm_model = ft.Dropdown(
            label="LM Studio 모델", width=460,
            options=[ft.DropdownOption(key=m, text=m) for m in lm_names],
            value=config.lmstudio.model if config.lmstudio.model in lm_names
            else (lm_names[0] if lm_names else None))
        self._lm_status = ft.Text("", size=TOKENS.size_caption)

        # --- 저장 항목 ---
        self._output_dir = ft.TextField(label="출력 폴더", width=460,
                                        value=config.output.directory)
        self._filename_prefix = ft.TextField(label="파일 이름 접두사", width=460,
                                             value=config.output.filename_prefix)
        self._max_wait = ft.TextField(label="최대 대기 시간(초)", width=220,
                                      value=str(config.comfyui.max_wait_seconds))
        self._poll_interval = ft.TextField(label="폴링 간격(초)", width=220,
                                           value=str(config.comfyui.poll_interval_seconds))
        self._status = ft.Text("", size=TOKENS.size_caption, color=TOKENS.success)

        # --- 탭2 / 탭3 ---
        self._profiles = ProfileEditor(services.model_registry)
        self._log_panel = LogPanel()

    # --- 탭 빌더 ---------------------------------------------------------
    def _build_servers_tab(self) -> ft.Control:
        """탭1: 원본의 tabAiServer (ComfyUI 그룹 + LM Studio 그룹)."""
        return ft.Container(
            content=ft.Column(
                controls=[
                    section_card("ComfyUI", ft.Column(
                        controls=[
                            ft.Row(controls=[
                                self._comfy_url,
                                ft.OutlinedButton("연결 확인", icon=ft.Icons.LINK,
                                                  on_click=self._check_comfy),
                            ], spacing=TOKENS.space_md, tight=True),
                            self._comfy_status,
                            self._model_base_paths,
                            ft.Row(controls=[
                                ft.TextButton("ComfyUI 폴더 열기",
                                              icon=ft.Icons.FOLDER_OPEN,
                                              on_click=self._open_model_path),
                                self._model_path_status,
                            ], spacing=TOKENS.space_md, tight=True),
                        ],
                        spacing=TOKENS.space_sm, tight=True), expand=False),
                    section_card("LM Studio", ft.Column(
                        controls=[
                            ft.Row(controls=[
                                self._lm_url,
                                ft.OutlinedButton("연결 확인", icon=ft.Icons.LINK,
                                                  on_click=self._check_lm),
                            ], spacing=TOKENS.space_md, tight=True),
                            self._lm_status,
                            self._lm_model,
                        ],
                        spacing=TOKENS.space_sm, tight=True), expand=False),
                    section_card("생성 · 출력", ft.Column(
                        controls=[
                            ft.Row(controls=[self._max_wait, self._poll_interval],
                                   spacing=TOKENS.space_md, tight=True),
                            self._output_dir,
                            self._filename_prefix,
                            ft.Text(f"현재 출력 폴더: {self._services.output_dir}",
                                    size=TOKENS.size_caption,
                                    color=TOKENS.on_surface_variant),
                        ],
                        spacing=TOKENS.space_sm, tight=True), expand=False),
                ],
                spacing=TOKENS.space_lg, tight=True, scroll=ft.ScrollMode.AUTO),
            padding=ft.Padding.all(TOKENS.space_lg), expand=True)

    def _build_models_tab(self) -> ft.Control:
        """탭2: 원본의 tabModel (자동 / 수동)."""
        return ft.Container(content=self._profiles.build(),
                            padding=ft.Padding.all(TOKENS.space_lg), expand=True)

    def _build_logs_tab(self) -> ft.Control:
        """탭3: 원본의 tabLog."""
        return ft.Container(content=self._log_panel.build(),
                            padding=ft.Padding.all(TOKENS.space_lg), expand=True)

    # --- 동작 -------------------------------------------------------------
    def _check_comfy(self, _event: Optional[ft.Event] = None) -> None:
        url = (self._comfy_url.value or "").strip()
        self._comfy_status.value = "확인 중..."
        self._comfy_status.color = TOKENS.on_surface_variant
        safe_update(self._comfy_status)

        status = self._services.check_comfy(url)
        if status.ok:
            models = self._services.model_fetcher.get_comfyui_models(url) or []
            self._comfy_status.value = f"연결됨 · 모델 {len(models)}개"
            self._comfy_status.color = TOKENS.success
        else:
            self._comfy_status.value = f"연결 실패: {getattr(status, 'message', '')}"
            self._comfy_status.color = TOKENS.error
        safe_update(self._comfy_status)

    def _check_lm(self, _event: Optional[ft.Event] = None) -> None:
        url = (self._lm_url.value or "").strip()
        self._lm_status.value = "확인 중..."
        self._lm_status.color = TOKENS.on_surface_variant
        safe_update(self._lm_status)

        status = self._services.check_lm(url)
        if status.ok:
            models = self._services.model_fetcher.get_lmstudio_models(url) or []
            options = [ft.DropdownOption(key=m, text=m) for m in models]
            self._lm_model.options = options
            if models:
                self._lm_model.value = models[0]
            self._lm_status.value = f"연결됨 · 모델 {len(models)}개"
            self._lm_status.color = TOKENS.success
        else:
            self._lm_status.value = f"연결 실패: {getattr(status, 'message', '')}"
            self._lm_status.color = TOKENS.error
        safe_update(self._lm_status, self._lm_model)

    def _open_model_path(self, _event: Optional[ft.Event] = None) -> None:
        """모델 경로 폴더를 파일 탐색기로 연다 (원본 dlgBrowseBtn)."""
        import os
        import subprocess
        import sys

        raw = (self._model_base_paths.value or "").split(";")[0].strip()
        if not raw:
            self._model_path_status.value = "모델 경로를 먼저 입력하세요."
            self._model_path_status.color = TOKENS.error
            safe_update(self._model_path_status)
            return

        path = Path(os.path.expanduser(raw))
        if not path.is_dir():
            self._model_path_status.value = f"폴더가 없습니다: {path}"
            self._model_path_status.color = TOKENS.error
            safe_update(self._model_path_status)
            return

        try:
            if sys.platform.startswith("win"):
                os.startfile(str(path))          # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(path)])
            else:
                subprocess.Popen(["xdg-open", str(path)])
            self._model_path_status.value = f"열었습니다: {path}"
            self._model_path_status.color = TOKENS.success
        except OSError as exc:
            self._model_path_status.value = f"열기 실패: {exc}"
            self._model_path_status.color = TOKENS.error
        safe_update(self._model_path_status)


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
            safe_update(self._status)
            return

        # 모델 경로도 함께 저장한다 (원본 dlgModelPathEdit).
        config.comfyui_model_paths = _split_paths(self._model_base_paths.value)

        if self._services.config_manager.save():
            self._status.value = "저장했습니다."
            self._status.color = TOKENS.success
        else:
            self._status.value = "저장에 실패했습니다."
            self._status.color = TOKENS.error
        safe_update(self._status)
        if self._on_saved is not None:
            self._on_saved(self._status.value)

    def build(self) -> ft.Control:
        """원본 설정창 구조: 상단 탭(서버/모델/로그) + 하단 버튼줄.

        Flet 1.x 의 탭은 TabBar(목록) 와 Tabs(본문) 가 따로다.
            TabBar: Tab(label="AI 서버") 들
            Tabs  : content=<한 Column>, length=<탭 개수>
        """
        tab_bar = ft.TabBar(
            expand=False,
            tabs=[
                ft.Tab(label="AI 서버"),
                ft.Tab(label="모델"),
                ft.Tab(label="로그"),
            ])
        tab_body = ft.Tabs(
            content=ft.Column(controls=[
                self._build_servers_tab(),
                self._build_models_tab(),
                self._build_logs_tab(),
            ], spacing=0, tight=True, expand=True),
            length=3, selected_index=0, animation_duration=200, expand=True)

        return ft.Column(
            controls=[
                tab_bar,
                tab_body,
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.FilledButton("저장", icon=ft.Icons.SAVE,
                                            on_click=self.save),
                            self._status,
                            ft.Container(expand=True),
                        ],
                        spacing=TOKENS.space_md, tight=True),
                    padding=ft.Padding.all(TOKENS.space_lg)),
            ],
            spacing=0, expand=True, tight=True)

