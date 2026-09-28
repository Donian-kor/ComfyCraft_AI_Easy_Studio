# -*- coding: utf-8 -*-
"""채팅 화면 렌더러.

설계 원칙 (4cut LocalComic_Studio 벤치마크):
- 위젯은 상태를 갖지 않는다. render() 는 세션 메시지로부터 전체를 다시 그린다.
- 카드 전환은 데이터의 kind/metadata 변경이다. 이 모듈은 "무엇을 그릴지"만
  결정하고, 상태를 바꾸지 않는다.
- 스크롤은 하단 고정 상태머신으로 관리한다. 사용자가 하단을 벗어나면
  자동 스크롤을 멈추고 위치를 보존한다.

컨트롤러는 이 모듈에 id 와 데이터만 전달하며, 위젯 레퍼런스를 유지하지 않는다.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QScrollArea, QVBoxLayout, QWidget

from app.gui.chat_widgets import (
    ChatMessage,
    GenerationCard,
    ImageCard,
    PromptCard,
)
from app.models.chat import (
    KIND_GENERATION,
    KIND_IMAGE,
    KIND_TEXT,
    PHASE_GENERATING,
    ChatMessageData,
)

logger = logging.getLogger(__name__)


class ChatViewManager:
    """ChatScrollArea와 카드의 생성/갱신만 담당한다."""

    NEAR_BOTTOM_THRESHOLD = 40

    def __init__(self, scroll: QScrollArea, content: QWidget,
                 on_save=None, on_copy_prompt=None, on_copy_image=None,
                 on_reuse=None, on_open_preview=None, on_edit_prompt=None,
                 on_revert_prompt=None, on_cancel=None):
        self.scroll = scroll
        self.content = content
        self._layout: QVBoxLayout = content.layout()
        self._on_save = on_save
        self._on_copy_prompt = on_copy_prompt
        self._on_copy_image = on_copy_image
        self._on_reuse = on_reuse
        self._on_open_preview = on_open_preview
        self._on_edit_prompt = on_edit_prompt
        self._on_revert_prompt = on_revert_prompt
        self._on_cancel = on_cancel
        # message_id -> (row, card) : 진행 중 카드만 빠르게 찾기 위한 색인
        self._gen_widgets: Dict[str, Any] = {}
        self._install_scroll_state_machine()


    # ── 스크롤 상태머신 (하단 고정) ──────────────────────────────────────
    def _install_scroll_state_machine(self) -> None:
        self._stick_to_bottom = True
        self._programmatic_scroll = False
        self._rendering = False
        self._snap_pending = False
        self._restore_guard = 0
        try:
            bar = self.scroll.verticalScrollBar()
            bar.rangeChanged.connect(self._on_range_changed)
            bar.valueChanged.connect(self._on_value_changed)
        except (RuntimeError, AttributeError):
            logger.debug("스크롤 상태머신 설치 실패", exc_info=True)

    def is_near_bottom(self) -> bool:
        try:
            bar = self.scroll.verticalScrollBar()
            return bar.value() >= bar.maximum() - self.NEAR_BOTTOM_THRESHOLD
        except (RuntimeError, AttributeError):
            return True

    def _on_range_changed(self, _start, _end) -> None:
        # 콘텐츠 높이가 바뀔 때마다(카드 추가/제거, 이미지 로드) 하단 고정
        # 상태면 다시 맞춘다. 위치 복구 중에는 하단으로 끌지 않는다.
        if self._restore_guard > 0:
            return
        self._schedule_snap()

    def _on_value_changed(self, _value) -> None:
        # 복구 중에는 clear() 로 값이 0 으로 클램프되는 게 사용자의 동작이
        # 아니므로 하단 고정 상태를 덮어쓰지 않는다.
        if self._programmatic_scroll or self._rendering or self._restore_guard > 0:
            return
        self._stick_to_bottom = self.is_near_bottom()

    def _schedule_snap(self) -> None:
        if self._snap_pending:
            return
        self._snap_pending = True
        QTimer.singleShot(0, self._snap_to_bottom)

    def _snap_to_bottom(self) -> None:
        self._snap_pending = False
        if not self._stick_to_bottom:
            return
        try:
            bar = self.scroll.verticalScrollBar()
            self._programmatic_scroll = True
            bar.setValue(bar.maximum())
        except (RuntimeError, AttributeError):
            logger.debug("하단 정렬 실패", exc_info=True)
        finally:
            self._programmatic_scroll = False

    def scroll_to_bottom(self) -> None:
        """사용자 동작으로 새 카드가 추가될 때 명시적으로 하단 이동."""
        self._stick_to_bottom = True
        self._schedule_snap()

    def _spacer_index(self) -> int:
        """spacer 가 놓인 인덱스 (없으면 -1).

        QSpacerItem 과 layout.itemAt() 이 돌려주는 QLayoutItem 래퍼는 서로
        다른 객체다. itemAt(i).spacerItem() 으로 확인해야 한다.
        (구코드는 widget.objectName() 로 비교해 항상 실패했다)
        """
        for i in range(self._layout.count()):
            item = self._layout.itemAt(i)
            if item is None:
                continue
            if item.widget() is not None:
                continue
            if item.spacerItem() is not None:
                return i
        return -1

    def _insert_at(self) -> int:
        """spacer 바로 위 인덱스 (카드가 항상 스택 끝에 붙는다)."""
        index = self._spacer_index()
        return index if index >= 0 else self._layout.count()

    def _append(self, widget: QWidget) -> None:
        self._layout.insertWidget(self._insert_at(), widget)

    def clear(self) -> None:
        """채팅 위젯 전부 제거 (spacer 유지).

        removeWidget() 가 레이아웃 크기를 줄이므로 인덱스를 실시간으로
        돌면 항목을 건너뛴다. 제거 대상을 먼저 스냅샷으로 모은 뒤 처리한다.
        """
        self._gen_widgets.clear()
        leftovers = []
        for i in range(self._layout.count()):
            item = self._layout.itemAt(i)
            if item is None:
                continue
            widget = item.widget()
            if widget is not None:
                leftovers.append(widget)
        for widget in leftovers:
            self._layout.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()

    def _current_value(self) -> int:
        try:
            return int(self.scroll.verticalScrollBar().value())
        except (RuntimeError, AttributeError):
            return 0

    def _restore_value(self, value: int) -> None:
        """레이아웃이 확정된 뒤 이전 스크롤 위치로 되돌린다.

        곧바로 setValue 하면 콘텐츠 높이가 아직 0 이라 Qt 가 다시 0 으로
        클램프한다. 최대 몇 프레임 뒤에 적용하고, 그동안 하단 고정으로
        되돌아가지 않도록 가드를 건다.
        """
        self._restore_guard = 4

        def apply() -> None:
            if self._restore_guard <= 0:
                return
            self._restore_guard -= 1
            if not self._stick_to_bottom:
                try:
                    bar = self.scroll.verticalScrollBar()
                    bar.setValue(min(int(value), max(0, bar.maximum())))
                except (RuntimeError, AttributeError):
                    logger.debug("스크롤 위치 복구 실패", exc_info=True)
            if self._restore_guard > 0:
                QTimer.singleShot(0, apply)

        apply()

    # ── 렌더 (유일한 진입점) ─────────────────────────────────────────────
    def render(self, messages: List[ChatMessageData]) -> None:
        """세션 메시지 전체를 다시 그린다. 상태가 남을 수 없다.

        clear() 로 레이아웃이 비는 순간 Qt 가 스크롤바를 0 으로 클램프한다.
        하단을 벗어난 사용자의 위치가 튀지 않도록 이전 값을 기억해 둔다.
        """
        keep = None if self._stick_to_bottom else self._current_value()
        self._rendering = True
        try:
            self.clear()
            for message in messages:
                try:
                    self._build_row(message)
                except RuntimeError:
                    logger.debug("메시지 렌더 실패", exc_info=True)
        finally:
            self._rendering = False
        if keep is not None:
            # clear() 로 0 으로 클램프된 위치를 되돌리고 하단 고정도 유지한다.
            # 하단 스냅은 하지 않는다 — 사용자가 하단을 떠난 상태이므로.
            self._stick_to_bottom = False
            self._restore_value(keep)
            return
        self._schedule_snap()

    def _build_row(self, message: ChatMessageData) -> Optional[QWidget]:
        if message.kind == KIND_TEXT:
            return self._build_text(message)
        if message.kind == KIND_GENERATION:
            return self._build_generation(message)
        if message.kind == KIND_IMAGE:
            return self._build_image(message)
        return None

    def _build_text(self, message: ChatMessageData) -> Optional[QWidget]:
        row = ChatMessage(message.role, message.text, self.content)
        self._append(row)
        return row

    def _build_generation(self, message: ChatMessageData) -> Optional[QWidget]:
        """프롬프트 확인 카드 또는 생성 중 카드."""
        row = ChatMessage("ai", "", self.content)
        if message.phase == PHASE_GENERATING:
            card = GenerationCard(
                on_cancel=self._on_cancel, parent=self.content)
            card.set_status(str(message.metadata.get("status", "이미지 생성 중...")))
            row.body_layout.addWidget(card)
        else:
            original = str(message.metadata.get("original", ""))
            enhanced = str(message.metadata.get("enhanced", ""))
            card = PromptCard(
                enhanced,
                on_edit=(lambda text, mid=message.id:
                         self._on_edit_prompt(mid, text)) if self._on_edit_prompt else None,
                on_revert=(lambda mid=message.id, orig=original:
                           self._on_revert_prompt(mid, orig)) if self._on_revert_prompt else None,
                parent=self.content,
            )
            card.set_prompt(enhanced, revert_visible=bool(
                enhanced and enhanced != original))
            row.body_layout.addWidget(card)
        self._gen_widgets[message.id] = (row, card)
        self._append(row)
        return row

    def _build_image(self, message: ChatMessageData) -> Optional[QWidget]:
        """완성 이미지 카드."""
        meta = message.metadata
        image_path = str(meta.get("image_path", ""))
        snapshot = dict(meta.get("snapshot", {}))
        row = ChatMessage("ai", "", self.content)
        card = ImageCard(
            image_path, str(meta.get("meta", "")), str(meta.get("prompt", "")),
            on_save=self._on_save,
            on_copy_prompt=self._on_copy_prompt,
            on_copy_image=self._on_copy_image,
            on_reuse=(lambda s=snapshot: self._on_reuse(s)) if self._on_reuse else None,
            parent=self.content,
        )
        if self._on_open_preview:
            card.image_label.clicked.connect(
                lambda _c=False, p=image_path, focus=card.image_label:
                self._on_open_preview(p, focus))
        self._set_accessibility(card, str(meta.get("prompt", "")))
        row.body_layout.addWidget(card)
        self._append(row)
        return row

    @staticmethod
    def _set_accessibility(card: ImageCard, prompt: str) -> None:
        try:
            card.image_label.setAccessibleName("생성된 이미지")
            card.image_label.setAccessibleDescription(prompt[:100])
            card.save_button.setAccessibleName("이미지 저장")
            card.copy_button.setAccessibleName("이미지 복사")
            card.reuse_button.setAccessibleName("프롬프트 불러와 수정")
            card.prompt_toggle.setAccessibleName("사용된 프롬프트 보기")
            card.prompt_copy_button.setAccessibleName("프롬프트 복사")
        except (RuntimeError, AttributeError):
            pass

    # ── 진행 중 카드 갱신 (전체 재렌더 없이) ─────────────────────────────
    def update_generation(self, message_id: str, status: str = "",
                          progress: Optional[int] = None,
                          enhanced: Optional[str] = None) -> None:
        """생성 카드의 상태만 바꾼다 (같은 메시지, 같은 카드)."""
        entry = self._gen_widgets.get(message_id)
        if not entry:
            return
        _row, card = entry
        try:
            if isinstance(card, GenerationCard):
                if status:
                    card.set_status(status)
                if progress is not None:
                    card.set_progress(progress)
            elif enhanced is not None and isinstance(card, PromptCard):
                card.set_prompt(enhanced, revert_visible=True)
        except RuntimeError:
            logger.debug("생성 카드 갱신 실패", exc_info=True)

    def has_message(self, message_id: str) -> bool:
        return message_id in self._gen_widgets
