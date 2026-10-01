"""이미지 전체화면 미리보기 모달 (줌·팬·회전·이전/다음 + 포커스 관리).

원본 Qt ImagePreviewModal 을 Flet 1.0 로 이식했다.
- InteractiveViewer: 줌/팬 (마우스 휠/드래그)
- 직접 구현: 회전(90°), 이전/다음, 저장, 폴더 열기
- ESC/닫기 버튼으로 닫기, 열 때 포커스 복원
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable, List, Optional

import flet as ft

from app.ui.flet.theme.tokens import TOKENS


class ImagePreviewModal:
    """이미지 전체화면 미리보기 모달.

    사용법:
        modal = ImagePreviewModal(
            page=page,
            on_save=lambda path: ...,
            on_open_folder=lambda: ...,
        )
        modal.open_with(["out/1.png", "out/2.png"], index=0, return_focus_widget=some_control)
    """

    ZOOM_STEP = 1.25
    MIN_ZOOM = 0.2
    MAX_ZOOM = 8.0

    def __init__(
        self,
        page: ft.Page,
        *,
        on_save: Optional[Callable[[str], None]] = None,
        on_open_folder: Optional[Callable[[], None]] = None,
    ) -> None:
        self._page = page
        self._on_save = on_save
        self._on_open_folder = on_open_folder

        self._paths: List[str] = []
        self._index = 0
        self._zoom = 1.0
        self._rotation = 0
        self._return_focus_widget: Optional[ft.Control] = None

        # --- 컨트롤 구성 ----------------------------------------------------
        self._image = ft.Image(src="", fit=ft.BoxFit.CONTAIN)

        self._viewer = ft.InteractiveViewer(
            content=self._image,
            min_scale=self.MIN_ZOOM,
            max_scale=self.MAX_ZOOM,
            pan_enabled=True,
            scale_enabled=True,
            expand=True,
        )

        self._position_label = ft.Text(
            "0 / 0",
            size=TOKENS.size_caption,
            color=TOKENS.on_surface_variant,
            text_align=ft.TextAlign.CENTER,
        )

        self._prev_button = ft.IconButton(icon=ft.Icons.CHEVRON_LEFT, tooltip="이전", on_click=self._show_prev, disabled=True)
        self._next_button = ft.IconButton(icon=ft.Icons.CHEVRON_RIGHT, tooltip="다음", on_click=self._show_next, disabled=True)
        self._zoom_in_button = ft.IconButton(icon=ft.Icons.ZOOM_IN, tooltip="확대", on_click=self._zoom_in)
        self._zoom_out_button = ft.IconButton(icon=ft.Icons.ZOOM_OUT, tooltip="축소", on_click=self._zoom_out)
        self._rotate_button = ft.IconButton(icon=ft.Icons.ROTATE_RIGHT, tooltip="회전 (90°)", on_click=self._rotate)
        self._save_button = ft.FilledTonalButton("저장", icon=ft.Icons.SAVE, on_click=self._on_save_clicked)
        self._folder_button = ft.FilledTonalButton("폴더 열기", icon=ft.Icons.FOLDER_OPEN, on_click=lambda _e: self._on_open_folder and self._on_open_folder())
        self._close_button = ft.FilledButton("닫기", icon=ft.Icons.CLOSE, on_click=self.close)

        self._dialog: Optional[ft.AlertDialog] = None

    # --- 내부 헬퍼 ----------------------------------------------------------
    def _update_image(self) -> None:
        if not self._paths:
            return
        path = self._paths[self._index]
        if not Path(path).exists():
            self._image.src = ""
            self._image.tooltip = "이미지를 불러올 수 없습니다."
        else:
            self._image.src = path
            self._image.tooltip = path
        self._image.rotate = self._rotation * 3.14159 / 180.0
        self._viewer.scale = self._zoom
        self._position_label.value = f"{self._index + 1} / {len(self._paths)}"
        has_many = len(self._paths) > 1
        self._prev_button.disabled = not has_many
        self._next_button.disabled = not has_many

    def _apply_zoom(self) -> None:
        self._viewer.scale = self._zoom

    def _apply_rotation(self) -> None:
        self._image.rotate = self._rotation * 3.14159 / 180.0
        self._safe_update(self._image)

    # --- 조작 ---------------------------------------------------------------
    def _show_prev(self, _e) -> None:
        if len(self._paths) > 1:
            self._index = (self._index - 1) % len(self._paths)
            self._zoom = 1.0
            self._rotation = 0
            self._update_image()
            self._safe_update(self._viewer, self._position_label,
                              self._prev_button, self._next_button)

    def _show_next(self, _e) -> None:
        if len(self._paths) > 1:
            self._index = (self._index + 1) % len(self._paths)
            self._zoom = 1.0
            self._rotation = 0
            self._update_image()
            self._safe_update(self._viewer, self._position_label,
                              self._prev_button, self._next_button)

    def _zoom_in(self, _e) -> None:
        self._zoom = min(self.MAX_ZOOM, self._zoom * self.ZOOM_STEP)
        self._apply_zoom()

    def _zoom_out(self, _e) -> None:
        self._zoom = max(self.MIN_ZOOM, self._zoom / self.ZOOM_STEP)
        self._apply_zoom()

    def _rotate(self, _e) -> None:
        self._rotation = (self._rotation + 90) % 360
        self._apply_rotation()

    def _on_save_clicked(self, _e) -> None:
        if self._on_save is not None and self._paths:
            try:
                self._on_save(self._paths[self._index])
            except Exception:
                pass

    # --- 열기/닫기 ----------------------------------------------------------
    def open_with(
        self,
        paths: List[str],
        index: int = 0,
        return_focus_widget: Optional[ft.Control] = None,
    ) -> None:
        """이미지 목록 중 index를 표시."""
        self._paths = [p for p in paths if p and Path(p).exists()]
        if not self._paths:
            return
        self._index = max(0, min(index, len(self._paths) - 1))
        self._zoom = 1.0
        self._rotation = 0
        self._return_focus_widget = return_focus_widget

        self._update_image()

        # 다이얼로그 구성
        self._dialog = ft.AlertDialog(
            title=ft.Text("이미지 미리보기", size=TOKENS.size_body),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(content=self._viewer, expand=True),
                        ft.Divider(height=1, color=TOKENS.outline),
                        ft.Row(
                            controls=[
                                self._prev_button,
                                self._next_button,
                                ft.VerticalDivider(width=1),
                                self._zoom_out_button,
                                self._zoom_in_button,
                                ft.VerticalDivider(width=1),
                                self._rotate_button,
                                ft.Container(expand=True),
                                self._folder_button,
                                self._save_button,
                                self._close_button,
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=TOKENS.space_sm,
                        ),
                        ft.Container(height=TOKENS.space_xs),
                        self._position_label,
                    ],
                    spacing=TOKENS.space_sm,
                    tight=True,
                    scroll=ft.ScrollMode.AUTO,
                ),
                width=1000,
                height=700,
            ),
            modal=True,
            actions=[],
        )

        try:
            self._page.show_dialog(self._dialog)
            try:
                self._close_button.focus()
            except Exception:
                pass
        except Exception:
            pass

    def close(self, _e=None) -> None:
        """다이얼로그 닫기 + 포커스 복원."""
        if self._dialog is not None:
            try:
                self._page.pop_dialog()
            except Exception:
                pass
            self._dialog = None
        if self._return_focus_widget is not None:
            try:
                self._return_focus_widget.focus()
            except Exception:
                pass

    @staticmethod
    def _safe_update(*controls: ft.Control) -> None:
        from app.ui.flet.components.common import safe_update
        safe_update(*controls)