"""챗봇 대화 영역.

원본 UI 의 ChatViewManager 역할: 메시지 데이터로부터 카드를 그리고,
생성 진행 상태에 따라 같은 카드를 제자리에서 바꿔친다.

여기에는 상태가 없다. 상태는 AppState 가 Job 이벤트로 받아 이쪽에
set_messages / replace_message 로 내려보낸다.
"""

from __future__ import annotations

from typing import Dict, List, Optional

import flet as ft

from app.models.chat import ChatMessageData
from app.ui.flet.components.common import safe_update
from app.ui.flet.pages.chat_cards import render_message
from app.ui.flet.theme.tokens import TOKENS


class ChatPanel:
    """메시지 목록(카드 흐름)을 그리는 컨테이너."""

    def __init__(self) -> None:
        self._list = ft.ListView(
            expand=True, spacing=TOKENS.space_md,
            padding=ft.Padding.all(TOKENS.space_lg))
        self._messages: List[ChatMessageData] = []
        self._index: Dict[str, int] = {}
        self._kwargs: Dict[str, object] = {}

    # --- 콜백 주입 -------------------------------------------------------
    def set_card_actions(self, **kwargs) -> None:
        """카드 액션(저장/재사용/확대 등)을 주입한다.

        카드 액션은 메시지 데이터에 붙지 않는다. 화면 구현이 바뀌어도
        세션 파일은 그대로여야 하기 때문이다.
        """
        self._kwargs = dict(kwargs)

    # --- 목록 -------------------------------------------------------------
    def set_messages(self, messages: List[ChatMessageData]) -> None:
        self._messages = list(messages)
        self._reindex()
        self._list.controls = [render_message(m, **self._kwargs)
                               for m in self._messages]
        safe_update(self._list)
        self.scroll_to_bottom()

    def append_message(self, message: ChatMessageData) -> None:
        self._messages.append(message)
        self._index[message.id] = len(self._messages) - 1
        self._list.controls.append(render_message(message, **self._kwargs))
        safe_update(self._list)
        self.scroll_to_bottom()

    def replace_message(self, message: ChatMessageData) -> None:
        """같은 위치의 카드를 통째로 교체한다.

        프롬프트 확인 → 생성 중 → 완료 이미지 전이가 모두 이 경로를 탄다.
        """
        position = self._index.get(message.id)
        if position is None:
            self.append_message(message)
            return
        self._messages[position] = message
        self._list.controls[position] = render_message(message, **self._kwargs)
        safe_update(self._list)
        self.scroll_to_bottom()

    def find(self, message_id: str) -> Optional[ChatMessageData]:
        position = self._index.get(message_id)
        return self._messages[position] if position is not None else None

    def clear(self) -> None:
        self._messages = []
        self._index = {}
        self._list.controls = []
        safe_update(self._list)

    @property
    def messages(self) -> List[ChatMessageData]:
        return list(self._messages)

    def _reindex(self) -> None:
        self._index = {m.id: i for i, m in enumerate(self._messages)}

    def scroll_to_bottom(self) -> None:
        """목록 끝으로 내린다. 아직 page 에 없으면 조용히 넘긴다."""
        if not self._list.controls:
            return
        try:
            result = self._list.scroll_to(len(self._list.controls) - 1,
                                          duration=120)
            # Flet 1.x 의 scroll_to 는 코루틴을 반환한다. 이벤트 루프가 없는
            # 곳(테스트)에서는 실행할 수 없으므로 그냥 닫는다.
            if hasattr(result, "close"):
                result.close()
        except Exception:
            pass

    def build(self) -> ft.Control:
        return self._list
