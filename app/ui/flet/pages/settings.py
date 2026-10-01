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
from app.core.config_manager import AppConfig
from app.paths import BASE_DIR
from app.ui.flet.components.common import safe_update, section_card
from app.ui.flet.pages.log_panel import LogPanel
from app.ui.flet.pages.profiles import ProfileEditor
from app.ui.flet.theme.tokens import TOKENS, theme_mode



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
                 on_saved: Optional[Callable[[str], None]] = None,
                 on_theme_change: Optional[Callable[[str], None]] = None) -> None:
        self._services = services
        self._on_saved = on_saved
        # 테마 적용은 app_state 가 한다(페이지를 아는 쪽이 거기뿐이다).
        self._on_theme_change = on_theme_change
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

        # --- 테마 ---
        # 원본 Qt 의 available_themes()/apply_theme() 대체물.
        # 상단바 토글 버튼이 주 경로이고, 여기는 '지금 어떤 모드인가'를
        # 확인하고 지정하는 자리다.
        # Flet 1.0 의 Dropdown 은 콜백 이름이 on_select 이다(on_change 없음).
        self._theme_mode = ft.Dropdown(
            label="화면 테마", width=220,
            options=[ft.DropdownOption(key="dark", text="다크"),
                     ft.DropdownOption(key="light", text="라이트")],
            value=theme_mode(),
            on_select=self._change_theme)

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
                    section_card("화면 테마", ft.Column(
                        controls=[
                            self._theme_mode,
                            ft.Text("위쪽 막대의 아이콘 버튼으로도 바로 바꿀 수 있습니다.",
                                    size=TOKENS.size_caption,
                                    color=TOKENS.on_surface_variant),
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

    # --- 불러오기 / 기본값 복원 -------------------------------------------
    def _set_status(self, message: str, color: str = TOKENS.on_surface_variant) -> None:
        self._status.value = message
        self._status.color = color
        safe_update(self._status)

    def _apply_config(self, config: Any) -> None:
        """config 값을 폼에 옮긴다 ('불러오기' 와 '기본값 복원' 이 함께쓴다)."""
        self._comfy_url.value = config.comfyui.url
        self._lm_url.value = config.lmstudio.url
        # 드롭다운은 옵션에 없는 값을 주면 화면이 빈칸이 된다. 목록에 없으면
        # 첫 항목을 준다 (생성 시 __init__ 과 같은 규칙).
        lm = str(config.lmstudio.model or "")
        keys = [opt.key for opt in self._lm_model.options]
        self._lm_model.value = lm if lm in keys else (keys[0] if keys else None)
        self._output_dir.value = config.output.directory
        self._filename_prefix.value = config.output.filename_prefix
        self._max_wait.value = str(config.comfyui.max_wait_seconds)
        self._poll_interval.value = str(config.comfyui.poll_interval_seconds)
        self._model_base_paths.value = _join_paths(_model_base_paths(config))
        safe_update(self._comfy_url, self._lm_url, self._lm_model,
                    self._output_dir, self._filename_prefix, self._max_wait,
                    self._poll_interval, self._model_base_paths)

    def reload_config(self, _event: Optional[ft.Event] = None) -> None:
        """저장된 설정 파일을 다시 읽어 폼에 반영한다 (원본 dlgLoadConfigBtn).

        회귀 근거: 원본엔 '설정 불러오기' 버튼이 있었으나 Flet 로 빠졌다.
        손으로 고친 값을 파일에서 다시 되돌려 올 수 없었다.
        """
        try:
            config = self._services.config_manager.load()
        except Exception as exc:
            self._set_status(f"설정 불러오기 실패: {exc}", TOKENS.error)
            return
        self._apply_config(config)
        self._set_status("저장된 설정을 불러왔습니다.", TOKENS.success)

    def reset_defaults(self, _event: Optional[ft.Event] = None) -> None:
        """입력칸을 기본값으로 되돌린다 (원본 dlgResetDefaultsBtn).

        아직 저장하지 않는다 — 사용자가 '저장' 을 눌러야 반영된다
        (원본 restore_defaults 도 위젯만 바꾸고 저장은 따로 했다).
        """
        try:
            self._apply_config(AppConfig())
            self._set_status("기본값으로 되돌렸습니다. 저장하면 적용됩니다.",
                              TOKENS.success)
        except Exception as exc:
            self._set_status(f"기본값 복원 실패: {exc}", TOKENS.error)

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


    # --- 테마 -------------------------------------------------------------
    def _change_theme(self, event: ft.Event) -> None:
        """설정 화면의 테마 드롭다운. 화면을 칠하고 설정에 저장한다.

        실제로 칠하는 일은 AppState.toggle/set 이 한다(화면을 아는 쪽은
        app_state 뿐이므로 콜백으로 받는다). 여기서는 값만 넘긴다.
        """
        mode = getattr(event.control, "value", None) or "dark"
        if self._on_theme_change is not None:
            self._on_theme_change(mode)

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

        Flet 1.x 의 정식 구조는 Tabs.content 안의 Column 에
        [TabBar(탭 목록), TabBarView(본문)] 을 넣는 것이다.

            TabBar     : Tab(label="AI 서버") 등 탭 버튼
            TabBarView : controls=[탭0 본문, 탭1 본문, 탭2 본문]
            Tabs       : length=<탭 개수> (TabBar.tabs / TabBarView.controls 와 동일해야 함)

        TabBar 는 반드시 Tabs 안에 있어야 하고(형제 노드로 두면
        'TabBar must be used within a Tabs control' 오류),
        본문은 반드시 TabBarView 안에 있어야 한다(TabBarView 가 없으면
        selected_index 가 바뀌어도 화면이 그대로 유지된다).
        """
        tab_bar = ft.TabBar(
            expand=False,
            divider_color=TOKENS.outline,
            indicator_color=TOKENS.primary,
            label_color=TOKENS.primary,
            tabs=[
                ft.Tab(label="AI 서버"),
                ft.Tab(label="모델"),
                ft.Tab(label="로그"),
            ])
        # 탭 본문: TabBarView.controls 의 개수 == Tabs.length == TabBar.tabs
        tab_body = ft.TabBarView(
            expand=True,
            controls=[
                self._build_servers_tab(),
                self._build_models_tab(),
                self._build_logs_tab(),
            ])
        tabs = ft.Tabs(
            content=ft.Column(
                controls=[tab_bar, tab_body],
                spacing=0, tight=True, expand=True),
            length=3, selected_index=0, animation_duration=200, expand=True)

        return ft.Column(
            controls=[
                tabs,
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.OutlinedButton("불러오기", icon=ft.Icons.DOWNLOAD,
                                              on_click=self.reload_config),
                            ft.OutlinedButton("기본값 복원",
                                              icon=ft.Icons.RESTART_ALT,
                                              on_click=self.reset_defaults),
                            ft.FilledButton("저장", icon=ft.Icons.SAVE,
                                            on_click=self.save),
                            self._status,
                            ft.Container(expand=True),
                        ],
                        spacing=TOKENS.space_md, tight=True),
                    padding=ft.Padding.all(TOKENS.space_lg)),
            ],
            spacing=0, expand=True, tight=True)

