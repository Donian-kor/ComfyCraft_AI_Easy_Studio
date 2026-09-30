"""챗봇 대화 영역.

원본 UI 의 ChatViewManager 역할: 메시지 데이터로부터 카드를 그리고,
생성 진행 상태에 따라 같은 카드를 제자리에서 바꿔친다.

여기에는 상태가 없다. 상태는 AppState 가 Job 이벤트로 받아 이쪽에
set_messages / replace_message 로 내려보낸다.

스크롤: 채팅방과 같은 하단 고정 방식이다. on_scroll 로 사용자의
스크롤 위치를 보고, 바닥 근처에 있을 때만(near_bottom) 자동으로
끝으로 내린다. 사용자가 위를 보고 있으면 업데이트를 멈추고
'아래로' 플로팅 버튼을 보여준다.
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

    # 바닥으로 간주하는 여유(px). 이 안에 들어오면 '바닥에 붙음'으로 본다.
    NEAR_BOTTOM_PX = 48.0

    def __init__(self) -> None:
        self._list = ft.ListView(
            expand=True, spacing=TOKENS.space_md,
            padding=ft.Padding.all(TOKENS.space_lg),
            on_scroll=self._handle_scroll)
        self._messages: List[ChatMessageData] = []
        self._index: Dict[str, int] = {}
        self._kwargs: Dict[str, object] = {}
        # 사용자가 바닥 근처에 있는가. True 면 새 메시지마다 끝으로 이동.
        # False 면(위로 올려다보는 중) 자동스크롤을 멈추고 버튼을 보여준다.
        self._near_bottom = True
        self._jump_button = ft.FloatingActionButton(
            icon=ft.Icons.ARROW_DOWNWARD,
            tooltip="맨 아래로 이동",
            mini=True,
            visible=False,
            on_click=lambda _e: self.scroll_to_bottom(force=True),
        )

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

    # --- 스크롤 상태 머신 ---------------------------------------------------
    # 상태: near_bottom(바닥 근처?) × 일시정지
    #   near + 새 메시지  → 끝으로 이동, 버튼 숨김
    #   위로 올림        → 일시정지, 버튼 표시
    #   버튼 클릭        → 끝으로 이동, 일시정지 해제 (force=True)
    def _handle_scroll(self, event: ft.OnScrollEvent) -> None:
        """사용자가 직접 스크롤하면 바닥 부착 여부를 갱신한다.

        Flet 1.0 의 OnScrollEvent 에 `extent_after`(Qt 의 값) 가 없다.
        대신 아래 세 값이 온다. (플러터 ScrollMetrics 와 같다)

            pixels             현재 스크롤 오프셋
            viewport_dimension 화면(=뷰포트) 높이
            max_scroll_extent  맨 아래일 때의 오프셋

        즉 남은 거리 = max_scroll_extent - (pixels + viewport_dimension).
        이 값을 못 얻으면(헤드리스 테스트 등) 바닥에 있다고 보고,
        자동스크롤을 멈추지 않게 한다(멈추는 쪽이 더 위험).
        """
        remaining = self._remaining_from_bottom(event)
        if remaining is None:
            return
        self._near_bottom = remaining <= self.NEAR_BOTTOM_PX
        self._jump_button.visible = not self._near_bottom
        safe_update(self._jump_button)

    @staticmethod
    def _remaining_from_bottom(event) -> Optional[float]:
        """맨 아래까지 남은 거리(px). 알 수 없으면 None."""
        try:
            pixels = float(getattr(event, "pixels", 0.0) or 0.0)
            viewport = float(getattr(event, "viewport_dimension", 0.0) or 0.0)
            maximum = float(getattr(event, "max_scroll_extent", 0.0) or 0.0)
        except (TypeError, ValueError):
            return None
        if maximum <= 0.0:
            # 아직 스크롤할 게 없는(목록이 짧은) 경우 → 바닥이다.
            return 0.0
        return max(0.0, maximum - (pixels + viewport))

    def scroll_to_bottom(self, *, force: bool = False) -> None:
        """목록 끝으로 내린다. 아직 page 에 없으면 조용히 넘긴다.

        force=False(기본): 사용자가 바닥 근처에 있을 때만 이동한다.
        force=True(버튼 클릭): 위치와 무관하게 이동한다.
        """
        if force:
            self._near_bottom = True
            self._jump_button.visible = False
            safe_update(self._jump_button)
        elif not self._near_bottom:
            return
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
        return ft.Stack(controls=[self._list, self._jump_button],
                        alignment=ft.Alignment(1.0, 1.0))
