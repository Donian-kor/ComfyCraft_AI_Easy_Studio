"""Flet App Shell (Phase 4).

    App
    ├─ TopBar
    ├─ NavigationRail
    ├─ MainContent
    └─ StatusBar

셸은 레이아웃과 탐색만 책임진다. 업무 로직은 pages/ 아래로 내려간다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional

import flet as ft

from app.ui.flet.theme.tokens import TOKENS, status_color
from app.ui.flet.components.facedetailer_guide import show_facedetailer_guide
from app.ui.flet.components.image_preview import ImagePreviewModal


@dataclass(frozen=True)
class NavItem:
    """내비게이션 항목 1개."""

    route: str
    label: str
    icon: str           # 선택되지 않았을 때
    selected_icon: str  # 선택되었을 때


NAV_ITEMS: List[NavItem] = [
    NavItem("/", "챗봇", ft.Icons.CHAT_BUBBLE_OUTLINE, ft.Icons.CHAT_BUBBLE),
    NavItem("/models", "모델", ft.Icons.LAYERS_OUTLINED, ft.Icons.LAYERS),
    NavItem("/history", "이력", ft.Icons.HISTORY, ft.Icons.HISTORY),
    NavItem("/help", "도움말", ft.Icons.HELP_OUTLINE, ft.Icons.HELP),
    NavItem("/settings", "설정", ft.Icons.SETTINGS_OUTLINED, ft.Icons.SETTINGS),
]


def route_index(route: str) -> int:
    """라우트 문자열을 NavigationRail 인덱스로 바꾼다."""
    for i, item in enumerate(NAV_ITEMS):
        if item.route == route:
            return i
    return 0


def index_route(index: Optional[int]) -> str:
    """NavigationRail 인덱스를 라우트로 되돌린다."""
    if index is None or index < 0 or index >= len(NAV_ITEMS):
        return NAV_ITEMS[0].route
    return NAV_ITEMS[index].route


class AppShell:
    """TopBar + NavigationRail + 본문 + 상태바를 묶는 컨테이너.

    컨트롤 트리만 만든다. 상태 변경은 update_* 메서드로 국소적으로 한다
    (전체 rebuild 는 진행 표시가 깜빡이게 만든다).
    """

    def __init__(self, on_navigate: Callable[[str], None],
                 on_new_chat: Optional[Callable[[], None]] = None,
                 on_open_help: Optional[Callable[[], None]] = None,
                 on_toggle_theme: Optional[Callable[[], str]] = None) -> None:
        self._on_navigate = on_navigate
        # 새 대화 버튼. 원본 Qt 의 newChatBtn 에 해당한다.
        # 콜백이 없으면(테스트 등) 버튼을 숨겨 죽은 버튼을 남기지 않는다.
        self._on_new_chat = on_new_chat
        # 가이드 다이얼로그에서 '도움말에서 보기' 를 눌렀을 때 쓸 경로.
        self._on_open_help = on_open_help
        # 다크/라이트 토글. None 이면 버튼을 숨긴다(테스트 등).
        self._on_toggle_theme = on_toggle_theme
        self._theme_button = ft.IconButton(
            icon=ft.Icons.LIGHT_MODE_OUTLINED,
            tooltip="밝게 보기",
            visible=on_toggle_theme is not None,
            on_click=self._handle_toggle_theme)
        self._new_chat_button = ft.FilledTonalButton(
            "새 대화", icon=ft.Icons.ADD_COMMENT_OUTLINED,
            on_click=self._handle_new_chat,
            visible=on_new_chat is not None,
            tooltip="지금 대화를 저장하고 새로 시작합니다")
        self._page = None
        self._root = None
        self._content_area = ft.Container(expand=True)
        self._status_text = ft.Text("", size=TOKENS.size_caption,
                                    color=TOKENS.on_surface_variant)
        self._job_bar = ft.ProgressBar(value=0, visible=False, height=4)
        self._job_label = ft.Text("", size=TOKENS.size_caption, color=TOKENS.primary)
        self._status_dot = ft.Container(
            width=8, height=8, border_radius=ft.BorderRadius(4, 4, 4, 4),
            bgcolor=TOKENS.on_surface_variant,
        )
        self._title = ft.Text("ComfyCraft", size=TOKENS.size_title,
                              weight=ft.FontWeight.W_600)
        self._rail = self._build_rail()
        self._comfy_indicator, self._comfy_dot = self._build_service_indicator(
            "ComfyUI")
        self._lm_indicator, self._lm_dot = self._build_service_indicator(
            "LM Studio")

    # --- 구성 -------------------------------------------------------------
    def _build_rail(self) -> ft.NavigationRail:
        return ft.NavigationRail(
            bgcolor=TOKENS.surface,
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=88,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(item.icon),
                    selected_icon=ft.Icon(item.selected_icon),
                    label=item.label,
                    padding=ft.Padding.symmetric(vertical=TOKENS.space_xs),
                )
                for item in NAV_ITEMS
            ],
            on_change=self._handle_rail_change,
        )

    def _build_service_indicator(self, name: str):
        """연결 상태 표시등. (컨테이너, 색칠할 dot) 을 돌려준다.

        회귀 근거: 예전엔 dot 을 data 에 숨겼다. 그랬더니 색을 바꿀 때
        바깥 컨테이너만 갱신해야 했고, Flet 은 자손의 속성 변경을
        자동으로 감지하지 않아 화면에 반영되지 않았다. dot 을 직접 들고
        갱신하도록 바꿨다.
        """
        dot = ft.Container(
            width=8, height=8,
            border_radius=ft.BorderRadius(4, 4, 4, 4),
            bgcolor=TOKENS.on_surface_variant,
        )
        return (
            ft.Container(
                content=ft.Row(
                    controls=[
                        dot,
                        ft.Text(name, size=TOKENS.size_caption,
                                color=TOKENS.on_surface_variant),
                    ],
                    spacing=TOKENS.space_sm,
                    tight=True,
                ),
                tooltip=name,
            ),
            dot,
        )

    def _handle_rail_change(self, event: ft.Event) -> None:
        index = getattr(event.control, "selected_index", 0)
        self._on_navigate(index_route(index))

    def _handle_new_chat(self, _event: Optional[ft.Event] = None) -> None:
        """'새 대화' 버튼. 실제 처리는 AppState.new_chat() 이 한다."""
        if self._on_new_chat is not None:
            self._on_new_chat()

    def _handle_toggle_theme(self, _event: Optional[ft.Event] = None) -> None:
        """'밝게/어둡게' 버튼. 실제로 칠하는 쪽은 AppState.toggle_theme()."""
        if self._on_toggle_theme is None:
            return
        mode = self._on_toggle_theme()
        if mode == "light":
            self._theme_button.icon = ft.Icons.DARK_MODE_OUTLINED
            self._theme_button.tooltip = "어둡게 보기"
        else:
            self._theme_button.icon = ft.Icons.LIGHT_MODE_OUTLINED
            self._theme_button.tooltip = "밝게 보기"
        self._safe_update(self._theme_button)

    def _build_topbar(self) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                controls=[
                    self._title,
                    ft.Text("AI Easy Studio", size=TOKENS.size_caption,
                            color=TOKENS.on_surface_variant),
                    ft.Container(width=TOKENS.space_lg),
                    self._new_chat_button,
                    ft.Container(expand=True),
                    self._theme_button,
                    ft.Container(width=TOKENS.space_sm),
                    self._comfy_indicator,
                    ft.Container(width=TOKENS.space_md),
                    self._lm_indicator,
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=TOKENS.space_xl,
                                         vertical=TOKENS.space_md),
            bgcolor=TOKENS.surface,
        )

    def _build_statusbar(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    self._job_bar,
                    ft.Row(
                        controls=[
                            self._status_dot,
                            self._status_text,
                            ft.Container(expand=True),
                            self._job_label,
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                spacing=TOKENS.space_xs,
                tight=True,
            ),
            padding=ft.Padding.symmetric(horizontal=TOKENS.space_xl,
                                         vertical=TOKENS.space_sm),
            bgcolor=TOKENS.surface,
        )

    def build(self) -> ft.Row:
        """전체 셸 컨트롤 트리를 만든다."""
        root = ft.Row(
            controls=[
                self._rail,
                ft.VerticalDivider(width=1, color=TOKENS.outline),
                ft.Column(
                    controls=[
                        self._build_topbar(),
                        self._build_hairline(),
                        self._content_area,
                        self._build_statusbar(),
                    ],
                    expand=True,
                    spacing=0,
                    tight=True,
                ),
            ],
            expand=True,
            spacing=0,
            tight=True,
        )
        # 테마 전환 시 이 트리를 통째로 다시 칠한다(재빌드 아님).
        self._root = root
        return root

    @property
    def root(self):
        """테마 적용 대상인 셸 루트 컨트롤 (build() 전이면 None)."""
        return self._root

    @property
    def page(self):
        """페이지 참조 (테마 적용 시 page.theme 을 갱신하는 데 쓴다)."""
        return self._page

    @staticmethod
    def _build_hairline() -> ft.Container:
        """1px 구분선. VerticalDivider 는 높이 지정이 안 되므로 Container 를 쓴다."""
        return ft.Container(height=1, bgcolor=TOKENS.outline)

    # --- 상태 갱신 --------------------------------------------------------
    # 공용 safe_update 를 재사용한다. 여기서 따로 update() 를 부르면
    # (1) 아직 page 에 안 붙어 있을 때 조용히 실패하고,
    # (2) 백그라운드 스레드(연결 확인)에서 부르면 갱신이 사라진다.

    @staticmethod
    def _safe_update(*controls: ft.Control) -> None:
        from app.ui.flet.components.common import safe_update

        safe_update(*controls)

    def set_content(self, control: ft.Control) -> None:
        self._content_area.content = control
        self._safe_update(self._content_area)

    def sync_route(self, route: str) -> None:
        """라우트에 맞춰 레일 선택 표시를 맞춘다."""
        self._rail.selected_index = route_index(route)
        self._safe_update(self._rail)

    def set_service_status(self, service: str, ok: Optional[bool]) -> None:
        """ComfyUI / LM Studio 연결 표시등을 갱신한다.

        색칠할 대상은 'dot' 컨트롤이다. 바깥 컨테이너를 갱신하면 Flet 이
        자손의 bgcolor 변경을 감지하지 못해 화면에 반영되지 않는다.
        """
        dot = self._comfy_dot if service == "comfy" else self._lm_dot
        dot.bgcolor = (TOKENS.on_surface_variant if ok is None
                       else status_color("connected" if ok else "disconnected"))
        # 안전한 갱신이 아니라 '갱신 실패를 알 수 없는' 로직이라 가린다.
        # 대신 아래 공용 safe_update 를 쓴다(스레드 밖이면 UI 스레드로
        # 넘겨 준다). 연결 확인은 백그라운드 스레드에서 도기 때문이다.
        from app.ui.flet.components.common import safe_update

        safe_update(dot)

    def set_status(self, message: str, kind: str = "idle") -> None:
        """하단 상태줄을 갱신한다."""
        self._status_text.value = message
        self._status_dot.bgcolor = status_color(kind)
        self._safe_update(self._status_text, self._status_dot)

    def set_job_progress(self, progress: Optional[int], label: str = "") -> None:
        """생성 진행률을 표시한다. None 이면 숨긴다.

        화면을 옮겨도 Job 이 살아 있으므로, 이 표시도 페이지와 무관하다.
        """
        if progress is None:
            self._job_bar.visible = False
            self._job_label.value = ""
        else:
            self._job_bar.visible = True
            self._job_bar.value = max(0, min(progress, 100)) / 100.0
            self._job_label.value = label
        self._safe_update(self._job_bar, self._job_label)

    def attach_page(self, page) -> None:
        """Dialog 등 페이지 단위 기능을 쓰기 위해 page 참조를 보관한다."""
        self._page = page

    def show_image_dialog(self, image_path: str, meta: str = "") -> None:
        """이미지 카드에서 '크게' 를 눌렀을 때 상세 Dialog 을 연다."""
        page = self._page
        if page is None or not image_path:
            return
        dialog = ft.AlertDialog(
            title=ft.Text(meta or "이미지", size=TOKENS.size_body),
            content=ft.Container(
                content=ft.Image(src=image_path, fit=ft.BoxFit.CONTAIN),
                width=900, height=640),
            actions=[
                ft.TextButton("닫기", on_click=lambda _e: page.pop_dialog()),
            ],
        )
        try:
            page.show_dialog(dialog)
        except Exception:
            # 헤드리스 환경에서는 열지 못해도 흐름을 막지 않는다
            pass

    def show_save_dialog(self, file_name: str, initial_directory: str,
                         callback: Callable[[Optional[str]], None]) -> None:
        """파일 저장 다이얼로그를 열고 사용자 선택 경로를 콜백으로 돌려준다.

        Flet FilePicker.save_file 은 비동기다. 결과는 on_result 로 오는데,
        여기서는 단일 사용이므로 래퍼로 감싼다.
        """
        page = self._page
        if page is None:
            callback(None)
            return

        def on_result(e: ft.FilePickerResultEvent) -> None:
            # 사용자가 취소하면 e.path 가 None
            callback(e.path)

        picker = ft.FilePicker(on_result=on_result)
        page.overlay.append(picker)
        page.update()

        # save_file 은 코루틴이므로 UI 루프에서 실행
        async def _run() -> None:
            await picker.save_file(
                dialog_title="이미지 저장",
                file_name=file_name,
                initial_directory=initial_directory,
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["png", "jpg", "jpeg", "webp"],
            )
        import asyncio
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(_run())
        except RuntimeError:
            # 루프가 없으면 동기로 돌림 (테스트 환경 등)
            asyncio.run(_run())

    def show_facedetailer_guide(self) -> None:
        """안면 보정 가이드 다이얼로그를 연다 (P3-3).

        다이얼로그 구성은 components/facedetailer_guide.py 가 맡는다.
        셸은 page 접근과 '도움말에서 보기' 라우트만 넘긴다.
        """
        show_facedetailer_guide(
            self._page, on_open_help=self._on_open_help)

    def show_image_preview_modal(
        self,
        paths: List[str],
        index: int = 0,
        return_focus_widget: Optional[ft.Control] = None,
        on_save: Optional[Callable[[str], None]] = None,
    ) -> None:
        """이미지 미리보기 모달을 연다 (줌/팬/회전/이전·다음).

        - paths: 이미지 경로 리스트
        - index: 처음 보여줄 인덱스
        - return_focus_widget: 닫을 때 포커스를 돌려줄 위젯
        - on_save: 저장 버튼 콜백 (선택한 이미지 경로 전달)
        """
        if not paths:
            return
        modal = ImagePreviewModal(
            self._page,
            on_save=on_save,
            on_open_folder=self._open_output_folder if hasattr(self, '_open_output_folder') else None,
        )
        modal.open_with(paths, index, return_focus_widget)
