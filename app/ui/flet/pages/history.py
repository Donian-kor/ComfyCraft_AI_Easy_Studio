"""Phase 8: History 화면 (독립 Page).

SessionManager(app/sections/session.py)의 기능을 재사용한다.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Optional

import flet as ft

from app.application.services import AppServices
from app.models.chat import messages_from_raw
from app.ui.flet.components.common import empty_state, safe_update
from app.ui.flet.theme.tokens import TOKENS, radius

# 이력 행에 들어갈 썸네일 한 변 길이
THUMBNAIL_SIZE = 56


def group_by_date(entries: List[Dict]) -> Dict[str, List[Dict]]:
    """세션 목록을 날짜(YYYY-MM-DD)별로 묶는다."""
    groups: Dict[str, List[Dict]] = {}
    for entry in entries:
        stamp = str(entry.get("updated_at", ""))[:10] or "날짜 없음"
        groups.setdefault(stamp, []).append(entry)
    return groups


def count_images(session: Dict) -> int:
    """세션에 포함된 이미지 카드 수."""
    return sum(1 for m in messages_from_raw(session.get("messages", []))
               if m.kind == "image")


def image_paths(session: Optional[Dict]) -> List[str]:
    """세션에 들어 있는 이미지 파일 경로 (나타나는 순서대로)."""
    if not session:
        return []
    paths: List[str] = []
    for m in messages_from_raw(session.get("messages", [])):
        path = str(m.metadata.get("image_path", "") or "")
        if path:
            paths.append(path)
    return paths


class HistoryPage:
    """생성 기록 목록. 검색/날짜별 그룹/삭제를 지원한다."""

    def __init__(self, services: AppServices, *,
                 on_open: Optional[Callable[[str], None]] = None,
                 on_reuse: Optional[Callable[[str, str], None]] = None) -> None:
        self._services = services
        self._on_open = on_open
        self._on_reuse = on_reuse
        self._query = ""
        # 이름을 고치는 중인 세션 id. 저장/취소가 끝나면 빠진다.
        self._editing: set = set()
        self._list = ft.ListView(
            expand=True, spacing=TOKENS.space_md, padding=ft.Padding.all(TOKENS.space_lg))
        self._search = ft.TextField(
            label="검색", hint_text="제목으로 검색",
            prefix_icon=ft.Icon(ft.Icons.SEARCH),
            on_change=self._handle_search)

    def _handle_search(self, event: ft.Event) -> None:
        self._query = (event.control.value or "").strip().lower()
        self.refresh()

    def _entries(self) -> List[Dict]:
        entries = self._services.session_manager.list_sessions()
        if not self._query:
            return entries
        return [e for e in entries if self._query in str(e.get("title", "")).lower()]

    def _build_entry_row(self, entry: Dict) -> ft.Control:
        session = self._services.session_manager.load_session(str(entry.get("id")))
        images = count_images(session) if session else 0
        title = str(entry.get("title", "제목 없음"))
        session_id = str(entry.get("id") or "")

        # 썸네일 (원본 _on_thumbnail_clicked). 첫 이미지를 아주 작게 보여준다.
        paths = image_paths(session)
        if paths:
            leading: ft.Control = ft.Container(
                content=ft.Image(src=paths[0], fit=ft.BoxFit.COVER,
                                 width=THUMBNAIL_SIZE, height=THUMBNAIL_SIZE),
                border_radius=radius(TOKENS.radius_md),
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                tooltip="크게 보기",
                on_click=lambda _e, p=paths[0]: self._open_preview(p))
        else:
            leading = ft.Icon(ft.Icons.HISTORY, color=TOKENS.outline)

        actions: List[ft.Control]
        if session_id in self._editing:
            field = ft.TextField(
                value=title, dense=True, width=240, label="이름",
                max_length=60, autofocus=True)
            actions = [
                ft.TextButton("저장", icon=ft.Icons.CHECK,
                              on_click=lambda _e, i=session_id, f=field:
                              self._rename(i, f)),
                ft.TextButton("취소", on_click=lambda _e, i=session_id:
                              self._cancel_rename(i)),
            ]
        else:
            actions = [
                # 원본은 세션 우클릭 메뉴였다. Flet 에는 우클릭 메뉴가
                # 없으므로 '이름' 버튼으로 눈에 보이게 고친다.
                ft.TextButton("이름", icon=ft.Icons.EDIT_OUTLINED,
                              on_click=lambda _e, i=session_id:
                              self._begin_rename(i)),
                ft.TextButton("열기", on_click=lambda _e, i=entry.get("id"):
                              self._open(i)),
                ft.TextButton("삭제", on_click=lambda _e, i=entry.get("id"):
                              self._delete(i)),
            ]

        return ft.Container(
            content=ft.Row(
                controls=[
                    leading,
                    ft.Column(
                        controls=[
                            ft.Text(title, size=TOKENS.size_body),
                            ft.Text(
                                f"{entry.get('updated_at', '')} · 이미지 {images}장",
                                size=TOKENS.size_caption, color=TOKENS.outline),
                        ],
                        spacing=2, tight=True, expand=True),
                    *actions,
                ],
                tight=True,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=TOKENS.surface,
            border_radius=radius(TOKENS.radius_md),
            padding=ft.Padding.all(TOKENS.space_md),
        )

    # --- 이름 변경 ---------------------------------------------------------
    def _begin_rename(self, session_id: Optional[str]) -> None:
        """입력을 열다. 빈칸 이름은 저장되지 않는다 (store 도 거부한다)."""
        if not session_id:
            return
        self._editing.add(str(session_id))
        self.refresh()

    def _cancel_rename(self, session_id: Optional[str]) -> None:
        if not session_id:
            return
        self._editing.discard(str(session_id))
        self.refresh()

    def _rename(self, session_id: Optional[str], field: ft.TextField) -> None:
        """이름을 바꾼다. 실패하면(빈 이름 등) 편집을 그대로 연다."""
        if not session_id:
            return
        title = (field.value or "").strip()
        if not title:
            return
        if self._services.session_manager.rename_session(str(session_id), title):
            self._editing.discard(str(session_id))
            self.refresh()

    # --- 썸네일 크게 보기 -------------------------------------------------
    def _open_preview(self, path: str) -> None:
        """썸네일을 눌러 이미지를 크게 본다 (원본 _on_thumbnail_clicked).

        페이지 참조는 아직 붙어 있지 않을 수 있으므로 컨트롤에서 얻는다.
        아직 화면에 붙지 않았으면(헤드리스/초기화) 조용히 넘긴다.
        """
        if not path:
            return
        # control.page 는 아직 페이지에 안 붙었으면 None 이 아니라
        # RuntimeError 를 던진다. 그래서 try 로 받는다 (헤드리스/초기화 안전).
        try:
            page = self._list.page
        except RuntimeError:
            return
        if page is None:
            return
        dialog = ft.AlertDialog(
            content=ft.Container(
                content=ft.Image(src=path, fit=ft.BoxFit.CONTAIN),
                width=900, height=640),
            actions=[ft.TextButton("닫기", on_click=lambda _e: page.pop_dialog())],
        )
        try:
            page.show_dialog(dialog)
        except Exception:
            pass

    def _open(self, session_id: Optional[str]) -> None:
        if self._on_open is not None and session_id:
            self._on_open(str(session_id))

    def _delete(self, session_id: Optional[str]) -> None:
        if not session_id:
            return
        self._services.session_manager.delete_session(str(session_id))
        self.refresh()

    def refresh(self) -> None:
        """목록을 다시 그린다."""
        entries = self._entries()
        if not entries:
            self._list.controls = []
        else:
            controls: List[ft.Control] = []
            for date, items in group_by_date(entries).items():
                controls.append(ft.Text(date, size=TOKENS.size_caption,
                                        color=TOKENS.on_surface_variant))
                controls.extend(self._build_entry_row(e) for e in items)
            self._list.controls = controls
        safe_update(self._list)

    def build(self) -> ft.Control:
        self.refresh()
        if not self._services.session_manager.list_sessions():
            return ft.Column(
                controls=[
                    ft.Container(content=self._search, padding=ft.Padding.all(TOKENS.space_lg)),
                    empty_state(ft.Icons.HISTORY, "기록이 없습니다",
                                "이미지를 만들면 여기에 쌓입니다"),
                ],
                expand=True, spacing=0, tight=True)
        return ft.Column(
            controls=[
                ft.Container(content=self._search, padding=ft.Padding.all(TOKENS.space_lg)),
                self._list,
            ],
            expand=True, spacing=0, tight=True)
