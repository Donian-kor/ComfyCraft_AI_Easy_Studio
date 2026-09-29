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


class HistoryPage:
    """생성 기록 목록. 검색/날짜별 그룹/삭제를 지원한다."""

    def __init__(self, services: AppServices, *,
                 on_open: Optional[Callable[[str], None]] = None,
                 on_reuse: Optional[Callable[[str, str], None]] = None) -> None:
        self._services = services
        self._on_open = on_open
        self._on_reuse = on_reuse
        self._query = ""
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

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.HISTORY, color=TOKENS.outline),
                    ft.Column(
                        controls=[
                            ft.Text(title, size=TOKENS.size_body),
                            ft.Text(
                                f"{entry.get('updated_at', '')} · 이미지 {images}장",
                                size=TOKENS.size_caption, color=TOKENS.outline),
                        ],
                        spacing=2, tight=True, expand=True),
                    ft.TextButton("열기", on_click=lambda _e, i=entry.get("id"):
                                  self._open(i)),
                    ft.TextButton("삭제", on_click=lambda _e, i=entry.get("id"):
                                  self._delete(i)),
                ],
                tight=True,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=TOKENS.surface,
            border_radius=radius(TOKENS.radius_md),
            padding=ft.Padding.all(TOKENS.space_md),
        )

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
