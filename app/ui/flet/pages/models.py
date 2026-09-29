"""Phase 5 부속: Models 화면.

ComfyUI 에서 읽어온 모델 목록과 등록된 프로필을 보여준다.
"""

from __future__ import annotations

from typing import Callable, List, Optional

import flet as ft

from app.application.services import AppServices
from app.ui.flet.components.common import empty_state, safe_update
from app.ui.flet.theme.tokens import TOKENS, radius


class ModelsPage:
    """사용 가능한 ComfyUI 모델 목록 + 프로필 요약."""

    def __init__(self, services: AppServices, *,
                 on_refresh: Optional[Callable[[], None]] = None) -> None:
        self._services = services
        self._on_refresh = on_refresh
        self._model_names: List[str] = []
        self._list = ft.ListView(expand=True, spacing=TOKENS.space_sm,
                                 padding=ft.Padding.all(TOKENS.space_lg))
        self._summary = ft.Text("", size=TOKENS.size_caption,
                                color=TOKENS.on_surface_variant)

    def set_models(self, model_names: List[str]) -> None:
        """ComfyUI 서버에서 읽어온 모델 목록을 표시한다."""
        self._model_names = list(model_names or [])
        if not self._model_names:
            self._list.controls = []
        else:
            self._list.controls = [
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.IMAGE_OUTLINED,
                                    size=TOKENS.size_body, color=TOKENS.outline),
                            ft.Text(name, size=TOKENS.size_body),
                        ],
                        spacing=TOKENS.space_sm, tight=True),
                    bgcolor=TOKENS.surface,
                    border_radius=radius(TOKENS.radius_md),
                    padding=ft.Padding.all(TOKENS.space_md),
                )
                for name in self._model_names
            ]
        registry = self._services.model_registry
        self._summary.value = (f"사용 가능 모델 {len(self._model_names)}개 · "
                               f"등록 프로필 {len(registry.profiles)}개")
        safe_update(self._list, self._summary)

    def _handle_refresh(self, _event: ft.Event) -> None:
        if self._on_refresh is not None:
            self._on_refresh()

    def build(self) -> ft.Control:
        # Row/Column 은 padding 을 받지 않으므로 여백은 Container 가 담당한다.
        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[
                            self._summary,
                            ft.Container(expand=True),
                            ft.OutlinedButton("새로고침", icon=ft.Icons.REFRESH,
                                              on_click=self._handle_refresh),
                        ],
                        spacing=TOKENS.space_md, tight=True),
                    padding=ft.Padding.all(TOKENS.space_lg)),
                (self._list if self._model_names else
                 empty_state(ft.Icons.LAYERS_OUTLINED, "표시할 모델이 없습니다",
                             "ComfyUI 서버가 켜져 있는지 확인하세요")),
            ],
            expand=True, spacing=0, tight=True)
