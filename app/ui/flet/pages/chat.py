"""Phase 7: Chat / Result 화면.

기존 ChatMessageData(app/models/chat.py)를 그대로 재사용한다.
위젯은 상태를 갖지 않고, 메시지 데이터에서 매번 다시 그린다.
"""

from __future__ import annotations

from typing import Callable, List, Optional

import flet as ft

from app.models.chat import (
    KIND_IMAGE,
    KIND_TEXT,
    ChatMessageData,
)
from app.ui.flet.components.common import empty_state, safe_update
from app.ui.flet.theme.tokens import TOKENS, radius, status_color


def format_elapsed(seconds: float) -> str:
    """경과 시간을 한국어로 포매팅 (app/sections/execution.py 와 동일 규칙)."""
    total = int(max(0.0, float(seconds or 0.0)))
    minutes, secs = divmod(total, 60)
    hours, mins = divmod(minutes, 60)
    if hours:
        return f"{hours}시간 {mins}분 {secs}초"
    if mins:
        return f"{mins}분 {secs}초"
    return f"{secs}초"


def image_card(message: ChatMessageData, *, on_reuse: Optional[Callable[[], None]] = None,
               on_delete: Optional[Callable[[], None]] = None) -> ft.Container:
    """생성 결과 카드: 이미지 + 메타 정보 + 재사용/삭제 액션."""
    meta = str(message.metadata.get("meta", "") or "")
    prompt = str(message.metadata.get("prompt", "") or "")

    actions = []
    if on_reuse is not None:
        actions.append(ft.TextButton("다시 쓰기", on_click=lambda _e: on_reuse()))
    if on_delete is not None:
        actions.append(ft.TextButton("삭제", on_click=lambda _e: on_delete()))

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.IMAGE, size=TOKENS.size_body,
                                color=TOKENS.primary),
                        ft.Text("Generated", size=TOKENS.size_caption,
                                color=TOKENS.on_surface_variant),
                        ft.Container(expand=True),
                        ft.Text(format_elapsed(
                            float(message.metadata.get("elapsed", 0) or 0)),
                            size=TOKENS.size_caption, color=TOKENS.outline),
                    ],
                    tight=True,
                ),
                ft.Image(src=str(message.metadata.get("image_path", "")),
                         fit=ft.BoxFit.CONTAIN, expand=True, height=320,
                         border_radius=radius(TOKENS.radius_md)),
                ft.Text(meta, size=TOKENS.size_caption,
                        color=TOKENS.on_surface_variant),
                *([ft.Text(prompt, size=TOKENS.size_caption, color=TOKENS.outline,
                           max_lines=3)] if prompt else []),
                *([ft.Row(controls=actions, spacing=TOKENS.space_sm)] if actions else []),
            ],
            spacing=TOKENS.space_sm,
            tight=True,
        ),
        bgcolor=TOKENS.surface,
        border_radius=radius(TOKENS.radius_lg),
        padding=ft.Padding.all(TOKENS.space_lg),
    )


def text_bubble(message: ChatMessageData) -> ft.Container:
    """사용자/AI 말풍선."""
    is_user = message.role == "user"
    return ft.Container(
        content=ft.Text(message.text or "", size=TOKENS.size_body),
        bgcolor=TOKENS.primary_container if is_user else TOKENS.surface_variant,
        border_radius=radius(TOKENS.radius_lg),
        padding=ft.Padding.symmetric(horizontal=TOKENS.space_lg,
                                     vertical=TOKENS.space_md),
        # 사용자 말풍선은 오른쪽, AI 말풍선은 왼쪽
        margin=ft.Margin(left=TOKENS.space_xxl * 4 if is_user else 0,
                         right=0 if is_user else TOKENS.space_xxl * 4),
    )


def render_message(message: ChatMessageData, **kwargs) -> ft.Control:
    """메시지 1개를 컨트롤로 렌더링한다 (kind 로 분기)."""
    if message.kind == KIND_IMAGE:
        return image_card(message, **kwargs)
    if message.kind == KIND_TEXT:
        return text_bubble(message)
    return text_bubble(message)


class ChatPage:
    """대화 화면. 메시지 목록만 소유하고 상태를 직접 들지 않는다."""

    def __init__(self) -> None:
        self._list = ft.ListView(
            expand=True, spacing=TOKENS.space_md, padding=ft.Padding.all(TOKENS.space_lg))
        self._messages: List[ChatMessageData] = []

    def set_messages(self, messages: List[ChatMessageData]) -> None:
        self._messages = list(messages)
        self._list.controls = [render_message(m) for m in self._messages]
        safe_update(self._list)

    def append_message(self, message: ChatMessageData) -> None:
        self._messages.append(message)
        self._list.controls.append(render_message(message))
        safe_update(self._list)

    def replace_message(self, message: ChatMessageData) -> None:
        """같은 위치의 카드를 통째로 교체한다 (생성중 → 이미지)."""
        for i, existing in enumerate(self._messages):
            if existing.id == message.id:
                self._messages[i] = message
                self._list.controls[i] = render_message(message)
                safe_update(self._list)
                return
        self.append_message(message)

    def build(self) -> ft.Control:
        if not self._messages:
            return empty_state(ft.Icons.CHAT_BUBBLE_OUTLINE,
                               "대화가 없습니다",
                               "생성 화면에서 프롬프트를 입력해 보세요")
        return self._list
