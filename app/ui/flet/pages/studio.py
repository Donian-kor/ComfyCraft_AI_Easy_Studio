"""홈 = 원본의 챗봇 작업 화면 (StudioPage).

원본 main.ui 구조를 그대로 따른다. 단, 좌측 레일(railFrame)은
셸(AppShell)이 전역으로 하나만 둔다 — 여기서 또 만들면 화면에
사이드바가 두 개로 중복된다.

    셸의 레일  │  옵션 패널  │  챗봇 대화
                │             │  ┌──────────────┐
                │  LM 모델    │  │ 카드 흐름     │
                │  해상도     │  │ 프롬프트→생성 │
                │  Seed       │  │ →이미지       │
                │  네거티브   │  └──────────────┘
                │  Steps/CFG  │  ┌──────────────┐
                │  FaceDetail │  │ [모델] 입력칸 │  ← ComfyUI 모델은
                └─────────────┘  │      + 전송  │    입력줄 좌측에 둔다
                                 └──────────────┘
"""

from __future__ import annotations

from typing import Callable, List, Optional

import flet as ft

from app.constants import PROMPT_MAX_CHARACTERS
from app.features.prompt.prompts import (
    enforce_prompt_character_limit,
    prompt_character_count,
)
from app.ui.flet.components.common import safe_update
from app.ui.flet.pages.chat import ChatPanel
from app.ui.flet.pages.options import OptionsPanel
from app.ui.flet.theme.tokens import TOKENS, radius

# 채팅 입력줄 좌측에 놓이는 ComfyUI 모델 드롭다운 폭.
# 옵션 패널 폭(372)을 그대로 쓰면 입력칸이 오른쪽으로 밀려 나므로 줄인다.
MODEL_SELECTOR_WIDTH = 260


class StudioPage:
    """챗봇 작업 화면: 좌측 옵션 + 우측 대화 + 하단 입력."""

    def __init__(self, *, on_send: Optional[Callable[[str], None]] = None,
                 on_stop: Optional[Callable[[], None]] = None,
                 model_registry=None) -> None:
        self._on_send = on_send
        self._on_stop = on_stop
        # 모델 프로필 검색기를 넘겨야 모델 변경 시 최적값을 적용할 수 있다.
        self.options = OptionsPanel(model_registry=model_registry)
        self.chat = ChatPanel()

        # 글자수 카운터는 여기 두지 않는다.
        #
        # 사용자 요청: 카운터는 채팅 입력칸이 아니라 *좌측 옵션 섹션의
        # 포스티프 프롬프트 칸* 안쪽 우측 위에 있어야 한다.
        # (chat 입력은 '짧은 설명' 을 넣는 곳이고, 실제 프롬프트는
        #  옵션쪽 포스티프 칸에 LM Studio 결과가 담긴다)
        # 속성으로 노출해 두는 건 스냅샷 복원/초기화 로직이 참조하므로 남긴다.
        self._counter = self.options.prompt_counter
        self._over_badge = self.options.prompt_over_badge

        self._prompt = ft.TextField(
            multiline=True, min_lines=1, max_lines=5,
            hint_text="그릴 장면을 설명해 주세요",
            border_radius=radius(TOKENS.radius_lg),
            bgcolor=TOKENS.surface_variant,
            on_submit=self._handle_submit,
            on_change=self._handle_prompt_change,
            # 원본 P11: 5000자 제한. 이식에서 빠져 있었다.
            max_length=PROMPT_MAX_CHARACTERS,
            # 회귀 근거(사용자 지적 2회): counter 를 None 으로 두면 Flet 이
            # 'counter 위치에 아무것도 안 나온다'고 해석하지 않는다.
            # max_length 가 있으면 그 자리에 '0 / 5,000' 을 *자동으로* 그린다.
            # 그래서 카운터를 옵션 패널로 옮겨도 채팅 입력칸 아래에 계속 보였다.
            # → 빈 문자열로 명시해 자동 카운터를 확실히 끈다.
            counter="",
        )
        self._send_button = ft.FilledButton(
            "전송", icon=ft.Icons.ARROW_UPWARD, on_click=self._handle_send)
        self._stop_button = ft.OutlinedButton(
            "중단", icon=ft.Icons.STOP_CIRCLE_OUTLINED, on_click=self._handle_stop,
            visible=False)
        self._hint = ft.Text(
            "Enter 로 전송 · Shift+Enter 로 줄바꿈",
            size=TOKENS.size_caption, color=TOKENS.outline)

    # --- 이벤트 ---------------------------------------------------------
    def _handle_send(self, _event: ft.Event) -> None:
        # 5000자를 넘는 부분은 보낼 때 잘라낸다 (원본 _enforce_prompt_limit).
        # max_length 가 입력을 막지만, 코드 경로로 값이 들어올 수 있어 방어한다.
        text = enforce_prompt_character_limit(
            (self._prompt.value or "").strip(), PROMPT_MAX_CHARACTERS)
        if not text:
            return
        self._prompt.value = ""
        self._reset_counter()
        safe_update(self._prompt, self._counter)
        if self._on_send is not None:
            self._on_send(text)

    def _handle_prompt_change(self, _event: ft.Event) -> None:
        """입력 글자 수를 갱신하고 초과하면 경고한다.

        카운터 표시는 *옵션 패널의 포스티프 프롬프트 칸* 이 담당한다.
        (사용자 요청. 카운터 컨트롤은 self._counter 로 참조만 해 둔다)

        회귀 근거: 원본 P11 은 5000자 제한 + 카운터 + 초과 경고를 갖고 있었으나
        Flet 이식에서 통째로 빠졌다. 이제는 상수(PROMPT_MAX_CHARACTERS)만 있고
        아무도 제한하지 않는 상태였다.
        """
        self._sync_counter(self._prompt.value or "")

    def _sync_counter(self, text: str) -> None:
        """글자 수를 카운터/배지/테두리에 반영한다."""
        count = prompt_character_count(text)
        over = count > PROMPT_MAX_CHARACTERS
        self._counter.value = f"{count:,} / {PROMPT_MAX_CHARACTERS:,}"
        self._counter.color = TOKENS.error if over else TOKENS.outline
        self._prompt.border_color = TOKENS.error if over else None
        # 초과 배지도 같이 숨긴다 (안 그러면 0 자여도 '초과'가 남는다)
        self._over_badge.visible = over
        safe_update(self._counter, self._over_badge, self._prompt)

    def _reset_counter(self) -> None:
        """보낸 뒤 카운터를 0 으로 되돌린다 (on_change 는 코드 변경에 안 뜬다)."""
        self._counter.value = f"0 / {PROMPT_MAX_CHARACTERS:,}"
        self._counter.color = TOKENS.outline
        self._prompt.border_color = None
        self._over_badge.visible = False

    def _handle_submit(self, _event: ft.Event) -> None:
        self._handle_send(_event)

    def _handle_stop(self, _event: ft.Event) -> None:
        if self._on_stop is not None:
            self._on_stop()

    # --- 레이아웃 --------------------------------------------------------
    def _build_input_frame(self) -> ft.Control:
        """입력줄: [모델 드롭다운] [입력칸] [중단] [전송]

        ComfyUI 모델 드롭다운은 원래 좌측 옵션 패널의 '기본' 섹션에 있었지만,
        이미지를 설명하는 바로 그 입력줄에 붙이는 편이 자연스럽다.
        컨트롤 자체는 OptionsPanel 이 소유하므로(값/옵션/최적값 적용 배선),
        여기서는 잘라온 '같은 객체' 를 그리기만 한다.
        OptionsPanel.build() 에서는 빼 두었으므로 부모가 둘이 되지 않는다.
        """
        model = self.options.model_selector
        # 옵션 패널 폭(FIELD_WIDTH 372)을 그대로 쓰면 입력칸이 밀려 나므로
        # 입력줄에 알맞게 좁힌 폭을 준다.
        model.width = MODEL_SELECTOR_WIDTH
        return ft.Container(
            content=ft.Row(
                controls=[
                    # '모델' 캡션은 넣지 않는다(사용자 요청). 드롭다운의
                    # label 속성도 쓰지 않는다 - 라벨이 두 번 뜨고 과거
                    # zh-hans 번역이 새어 들었던 회귀가 있기 때문이다.
                    # 모델 이름이 그대로 보이라 제목은 필요 없다.
                    model,
                    self._prompt, self._stop_button, self._send_button,
                ],
                spacing=TOKENS.space_sm,
                vertical_alignment=ft.CrossAxisAlignment.END,
            ),
            padding=ft.Padding.all(TOKENS.space_lg),
            bgcolor=TOKENS.surface,
        )

    def build(self) -> ft.Control:
        """옵션 패널 + 챗봇(대화/입력) 2분할.

        좌측 레일은 셸이 전역으로 하나만 둔다. 여기서 다시 만들면
        사이드바가 중복되므로 넣지 않는다.
        """
        return ft.Row(
            controls=[
                self.options.build(),
                ft.VerticalDivider(width=1, color=TOKENS.outline),
                ft.Column(
                    controls=[
                        ft.Container(content=self.chat.build(), expand=True),
                        self._build_input_frame(),
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

    # --- 상태 ------------------------------------------------------------
    def set_busy(self, running: bool) -> None:
        """생성 중이면 전송을 막고 중단 버튼을 보여준다."""
        self._send_button.disabled = running
        self._stop_button.visible = running
        safe_update(self._send_button, self._stop_button)

    def set_hint(self, text: str) -> None:
        self._hint.value = text
        safe_update(self._hint)

    def focus_prompt(self) -> None:
        try:
            self._prompt.focus()
        except Exception:
            pass

    def set_prompt_input(self, text: str) -> None:
        """프롬프트 입력창에 텍스트를 설정한다 (재작성/다시 만들기용)."""
        self._prompt.value = text
        # 카운터도 업데이트
        from app.features.prompt.prompts import prompt_character_count
        count = prompt_character_count(text)
        self._sync_counter(text)

    def focus_prompt_input(self) -> None:
        """프롬프트 입력창에 포커스를 준다."""
        self.focus_prompt()
