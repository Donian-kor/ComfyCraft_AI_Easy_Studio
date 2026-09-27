# -*- coding: utf-8 -*-
"""P2: 채팅 메시지 + 이미지 카드 위젯 (껍데기, 로직 없음).

- ChatMessage: role(user/ai/system)별 말풍선. action_row는 P4/P6 버튼이 얹히는 자리.
- ImageCard: 이미지 + 메타 + 프롬프트 접기/복사 + 저장/복사 버튼.
  [수정 요청] 버튼은 P6에서 추가된다.
"""
from __future__ import annotations

from typing import Callable, Optional

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)


class ChatMessage(QFrame):
    """대화 메시지 1개. role에 따라 정렬·색상이 달라진다."""

    def __init__(self, role: str, text: str, parent=None):
        super().__init__(parent)
        self.role = role
        self.setFrameShape(QFrame.Shape.NoFrame)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self.body = QFrame()
        self.body.setMaximumWidth(600)
        self.body_layout = QVBoxLayout(self.body)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(6)

        self.bubble = QLabel(text)
        self.bubble.setWordWrap(True)
        self.bubble.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.body_layout.addWidget(self.bubble)

        # P4/P6 액션 버튼이 얹히는 행 (기본 비어 있음)
        self.action_row = QHBoxLayout()
        self.action_row.setSpacing(8)
        self.body_layout.addLayout(self.action_row)

        if role == "user":
            self.bubble.setObjectName("chatUserBubble")
            outer.addStretch(1)
            outer.addWidget(self.body)
        elif role == "system":
            self.bubble.setObjectName("chatSystemText")
            self.bubble.setAlignment(Qt.AlignmentFlag.AlignCenter)
            outer.addStretch(1)
            outer.addWidget(self.body)
            outer.addStretch(1)
        else:
            self.bubble.setObjectName("chatAiBubble")
            outer.addWidget(self.body)
            outer.addStretch(1)

    def add_action(self, button: QPushButton) -> None:
        """액션 행에 버튼 추가 (P4 스타일 버튼·P6 수정 요청용)."""
        self.action_row.addWidget(button)


class ImageCard(QFrame):
    """생성 이미지 1장 + 메타 + 프롬프트 접기 + 저장/복사."""

    IMAGE_WIDTH = 480

    def __init__(
        self,
        image_path: str,
        meta_text: str,
        prompt_text: str,
        on_save: Optional[Callable[[], None]] = None,
        on_copy_prompt: Optional[Callable[[], None]] = None,
        on_copy_image: Optional[Callable[[], None]] = None,
        parent=None,
    ):
        super().__init__(parent)
        self.setObjectName("imageCard")
        self.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        self.image_label = QLabel()
        self.image_label.setObjectName("imageCardImage")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            self.image_label.setText("이미지를 불러올 수 없습니다.")
        else:
            scaled = pixmap.scaledToWidth(
                self.IMAGE_WIDTH, Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)
        self.image_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        layout.addWidget(self.image_label)

        self.meta_label = QLabel(meta_text)
        self.meta_label.setObjectName("imageCardMeta")
        self.meta_label.setWordWrap(True)
        layout.addWidget(self.meta_label)

        # 사용된 프롬프트 접기 영역
        self.prompt_toggle = QPushButton("▸ 사용된 프롬프트 (향상됨)")
        self.prompt_toggle.setObjectName("imageCardPromptToggle")
        self.prompt_toggle.setCheckable(True)
        self.prompt_toggle.setChecked(False)
        self.prompt_label = QLabel(prompt_text)
        self.prompt_label.setObjectName("imageCardPrompt")
        self.prompt_label.setWordWrap(True)
        self.prompt_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.prompt_label.setVisible(False)
        self.prompt_toggle.toggled.connect(self.prompt_label.setVisible)
        prompt_row = QHBoxLayout()
        prompt_row.addWidget(self.prompt_toggle)
        self.prompt_copy_button = QPushButton("복사")
        self.prompt_copy_button.setObjectName("imageCardPromptCopy")
        if on_copy_prompt is not None:
            self.prompt_copy_button.clicked.connect(on_copy_prompt)
        prompt_row.addWidget(self.prompt_copy_button)
        prompt_row.addStretch(1)
        layout.addLayout(prompt_row)
        layout.addWidget(self.prompt_label)

        # 액션 버튼
        actions = QHBoxLayout()
        actions.setSpacing(8)
        self.save_button = QPushButton("저장")
        self.save_button.setObjectName("imageCardSave")
        if on_save is not None:
            self.save_button.clicked.connect(on_save)
        self.copy_button = QPushButton("복사")
        self.copy_button.setObjectName("imageCardCopy")
        if on_copy_image is not None:
            self.copy_button.clicked.connect(on_copy_image)
        actions.addWidget(self.save_button)
        actions.addWidget(self.copy_button)
        actions.addStretch(1)
        layout.addLayout(actions)


class GenerationStatusBubble(QFrame):
    """P3: 생성 중 상태 말풍선 (상태 텍스트 + 진행률 + 경과 + 취소).

    테두리 펄스는 QTimer 기반 QSS 전환. pulse_enabled=False면 정적
    테두리만 표시한다 (P9에서 모션 감소 설정과 연결 예정).
    """

    PULSE_MS = 600
    BORDER_A = "#0078D4"
    BORDER_B = "#4AA3F0"

    def __init__(self, on_cancel: Optional[Callable[[], None]] = None,
                 parent=None):
        super().__init__(parent)
        self.setObjectName("statusBubble")
        self.pulse_enabled = True
        self._pulse_phase = False
        self._started_at: Optional[float] = None

        layout = QVBoxLayout(self)
        layout.setSpacing(6)

        self.status_label = QLabel("이미지 생성 중...")
        self.status_label.setObjectName("statusBubbleText")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        self.bar = QProgressBar()
        self.bar.setObjectName("statusBubbleBar")
        self.bar.setRange(0, 100)
        self.bar.setValue(0)
        self.bar.setTextVisible(False)
        layout.addWidget(self.bar)

        bottom = QHBoxLayout()
        bottom.setSpacing(8)
        self.elapsed_label = QLabel("")
        self.elapsed_label.setObjectName("statusBubbleElapsed")
        bottom.addWidget(self.elapsed_label)
        bottom.addStretch(1)
        self.cancel_button = QPushButton("■ 취소")
        self.cancel_button.setObjectName("statusBubbleCancel")
        if on_cancel is not None:
            self.cancel_button.clicked.connect(on_cancel)
        bottom.addWidget(self.cancel_button)
        layout.addLayout(bottom)

        self._pulse_timer = QTimer(self)
        self._pulse_timer.setInterval(self.PULSE_MS)
        self._pulse_timer.timeout.connect(self._toggle_pulse)
        self._clock_timer = QTimer(self)
        self._clock_timer.setInterval(1000)
        self._clock_timer.timeout.connect(self._tick_clock)

        self._apply_border(self.BORDER_A)

    def _apply_border(self, color: str) -> None:
        self.setStyleSheet(
            f"#statusBubble {{ border: 2px solid {color}; border-radius: 8px; }}")

    def _toggle_pulse(self) -> None:
        self._pulse_phase = not self._pulse_phase
        self._apply_border(
            self.BORDER_B if self._pulse_phase else self.BORDER_A)

    def start(self, started_at_monotonic: Optional[float] = None) -> None:
        """펄스 + 경과 타이머 시작."""
        self._started_at = started_at_monotonic
        if self.pulse_enabled and not self._pulse_timer.isActive():
            self._pulse_timer.start()
        if self._started_at is not None and not self._clock_timer.isActive():
            self._clock_timer.start()
            self._tick_clock()

    def stop(self) -> None:
        """타이머 정지 + 테두리 원복."""
        self._pulse_timer.stop()
        self._clock_timer.stop()
        self._apply_border(self.BORDER_A)

    def set_status(self, text: str) -> None:
        self.status_label.setText(str(text))

    def set_progress(self, value: int) -> None:
        try:
            self.bar.setValue(max(0, min(100, int(value))))
        except (TypeError, ValueError):
            pass

    def _tick_clock(self) -> None:
        if self._started_at is None:
            return
        import time
        elapsed = int(time.monotonic() - self._started_at)
        self.elapsed_label.setText(f"경과 {elapsed}초")
