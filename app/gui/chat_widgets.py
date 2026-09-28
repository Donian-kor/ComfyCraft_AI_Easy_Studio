# -*- coding: utf-8 -*-
"""P2: 채팅 말풍선 + 카드 위젯 (껍데기, 로직 없음).

- ChatMessage: role(user/ai/system)별 말풍선. action_row는 P4/P6 버튼이 얹히는 자리.
- PromptCard: AI 가 다듬은 프롬프트 확인 카드 (편집 가능).
- GenerationCard: 생성 중 카드 (상태 + 진행률 + 취소).
- ImageCard: 완성 이미지 + 메타 + 프롬프트 접기/복사 + 저장/복사/수정 요청.

위젯은 상태를 갖지 않는다. 어떤 카드를 그릴지는 ChatViewManager 가
세션 메시지(kind/metadata)로부터 결정한다.
"""
from __future__ import annotations

from typing import Callable, Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)

# P4: family/프로필 → 짧은 표시명 + 한 줄 특징 (UI층 딕셔너리, 코어 변경 없음).
# 표시명은 목록에만 쓰고, 내부 로직은 항상 정확한 파일명을 사용한다.
PROFILE_SHORT = {
    "flux_gguf": "FLUX",
    "zimage_turbo": "ZImage",
    "zanime_aio": "Z-Anime",
    "ernie-aio-base": "ERNIE Base",
    "ernie-aio-turbo": "ERNIE Turbo",
}
FAMILY_SHORT = {
    "flux": "FLUX",
    "zimage": "ZImage",
    "zanime": "Z-Anime",
    "ernie": "ERNIE",
}
PROFILE_FEATURE = {
    "flux_gguf": "사실적·고품질",
    "zimage_turbo": "빠른 생성",
    "zanime_aio": "애니·웹툰",
    "ernie-aio-base": "정밀·네거티브 강함",
    "ernie-aio-turbo": "초고속·8스텝",
}
FAMILY_FEATURE = {
    "flux": "사실적·고품질",
    "zimage": "빠른 생성",
    "zanime": "애니·웹툰",
    "ernie": "포스터·타이포",
}


def describe_model(profile, filename: str, used_shorts=None):
    """프로필+파일명 → (짧은 표시명, 특징, 툴팁).

    동 family 파일이 2개 이상이면 파일 stem 일부를 병기하여 구분한다.
    """
    from pathlib import Path
    used_shorts = used_shorts if used_shorts is not None else set()
    stem = Path(filename).stem if filename else ""
    name = getattr(profile, "name", "") or ""
    family = getattr(profile, "family", "") or ""
    short = PROFILE_SHORT.get(name) or FAMILY_SHORT.get(family) or stem
    feature = PROFILE_FEATURE.get(name) or FAMILY_FEATURE.get(family) or "범용 체크포인트"
    if short in used_shorts and stem:
        short = f"{short} ({stem[:14]})"
    used_shorts.add(short)
    tooltip = f"{filename} — {feature}" if filename else feature
    return short, feature, tooltip


class ClickableLabel(QLabel):
    """클릭 시 clicked 시그널을 보내는 라벨 (카드 이미지용)."""

    clicked = Signal()

    def mousePressEvent(self, event) -> None:  # noqa: N802
        self.clicked.emit()
        super().mousePressEvent(event)


class ChatMessage(QFrame):
    """대화 메시지 1개. role에 따라 정렬·색상이 달라진다."""

    def __init__(self, role: str, text: str, parent=None):
        super().__init__(parent)
        self.role = role
        self.setFrameShape(QFrame.Shape.NoFrame)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(8)

        def make_avatar(text: str) -> QLabel:
            avatar = QLabel(text)
            avatar.setObjectName("chatAvatar")
            avatar.setFixedSize(32, 32)
            avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
            return avatar

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
            outer.addWidget(make_avatar("나"),
                            alignment=Qt.AlignmentFlag.AlignTop)
        elif role == "system":
            self.bubble.setObjectName("chatSystemText")
            self.bubble.setAlignment(Qt.AlignmentFlag.AlignCenter)
            outer.addStretch(1)
            outer.addWidget(self.body)
            outer.addStretch(1)
        else:
            self.bubble.setObjectName("chatAiBubble")
            outer.addWidget(make_avatar("AI"),
                            alignment=Qt.AlignmentFlag.AlignTop)
            outer.addWidget(self.body)
            outer.addStretch(1)

    def add_action(self, button: QPushButton) -> None:
        """액션 행에 버튼 추가 (P4 스타일 버튼·P6 수정 요청용)."""
        self.action_row.addWidget(button)


class PromptCard(QFrame):
    """P20: AI가 다듬은 프롬프트 확인 카드 (편집 가능).

    enhancePromptEdit 를 그대로 재사용하지 않고 카드 안에 편집기를 두어,
    "AI 가 뭘로 만들었는지 확인 → 고쳐서 쓰기" 를 한눈에 보여준다.
    편집 내용은 on_edit 로 알려주고, 원문은 on_revert 로 되돌린다.
    """

    def __init__(self, prompt_text: str = "",
                 on_edit: Optional[Callable[[str], None]] = None,
                 on_revert: Optional[Callable[[], None]] = None,
                 parent=None):
        super().__init__(parent)
        self.setObjectName("promptCard")
        self.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        head = QHBoxLayout()
        head.setSpacing(8)
        title = QLabel("✨ AI가 다듬은 프롬프트")
        title.setObjectName("promptCardTitle")
        head.addWidget(title)
        head.addStretch(1)
        self.revert_button = QPushButton("원문으로 되돌리기")
        self.revert_button.setObjectName("promptCardRevert")
        self.revert_button.setAccessibleName("프롬프트 원문으로 되돌리기")
        self.revert_button.setVisible(False)
        if on_revert is not None:
            self.revert_button.clicked.connect(on_revert)
        head.addWidget(self.revert_button)
        layout.addLayout(head)

        self.prompt_edit = QPlainTextEdit(prompt_text)
        self.prompt_edit.setObjectName("promptCardEdit")
        self.prompt_edit.setAccessibleName("AI가 다듬은 프롬프트")
        self.prompt_edit.setPlaceholderText(
            "AI가 다듬은 프롬프트가 여기에 표시됩니다. 직접 고친 뒤 그대로 생성됩니다.")
        self.prompt_edit.setMinimumHeight(76)
        self.prompt_edit.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        layout.addWidget(self.prompt_edit)

        self.hint_label = QLabel(
            "내용을 고쳐도 됩니다 — 고친 내용이 그대로 이미지 생성에 쓰입니다.")
        self.hint_label.setObjectName("promptCardHint")
        self.hint_label.setWordWrap(True)
        layout.addWidget(self.hint_label)

        self._on_edit = on_edit
        if on_edit is not None:
            self.prompt_edit.textChanged.connect(self._emit_edit)

    def _emit_edit(self) -> None:
        if self._on_edit is not None:
            self._on_edit(self.prompt_edit.toPlainText())

    def set_prompt(self, text: str, revert_visible: bool = False) -> None:
        """내용을 채우고 되돌리기 버튼 노출 여부를 정한다."""
        self.prompt_edit.setPlainText(text or "")
        self.revert_button.setVisible(bool(revert_visible))

    def text(self) -> str:
        return self.prompt_edit.toPlainText().strip()


class ImageCard(QFrame):
    """완성 이미지 1장 + 메타 + 프롬프트 접기 + 저장/복사.

    생성 중 상태는 이 카드가 아니라 GenerationCard 가 담당한다.
    (생성 중 → 완료 전환은 메시지 kind 변경으로 표현되므로 카드를
     상태 머신으로 두지 않는다)
    """

    IMAGE_WIDTH = 480

    def __init__(
        self,
        image_path: str,
        meta_text: str,
        prompt_text: str,
        on_save: Optional[Callable[[], None]] = None,
        on_copy_prompt: Optional[Callable[[], None]] = None,
        on_copy_image: Optional[Callable[[], None]] = None,
        on_reuse: Optional[Callable[[], None]] = None,
        on_open: Optional[Callable[[], None]] = None,
        parent=None,
    ):
        super().__init__(parent)
        self.setObjectName("imageCard")
        self.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        self.image_label = ClickableLabel()
        self.image_label.setObjectName("imageCardImage")
        self.image_label.setCursor(Qt.CursorShape.PointingHandCursor)
        if on_open is not None:
            self.image_label.clicked.connect(on_open)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap(image_path) if image_path else QPixmap()
        if pixmap.isNull():
            self.image_label.setText("이미지를 불러올 수 없습니다."
                                     if image_path else "")
        else:
            scaled = pixmap.scaledToWidth(
                self.IMAGE_WIDTH, Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)
        self.image_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        layout.addWidget(self.image_label)

        # P20: 생성 중 표시 (같은 카드에서 상태만 전환)
        self.pending_label = QLabel("이미지 생성 중...")
        self.pending_label.setObjectName("imageCardPending")
        self.pending_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pending_label.setWordWrap(True)
        self.pending_label.setMinimumHeight(180)
        self.pending_label.setVisible(False)
        layout.addWidget(self.pending_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("imageCardProgress")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

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
        # P6: 수정 요청 (프롬프트+옵션 전체 복원). 콜백 없으면 숨김.
        self.reuse_button = QPushButton("수정 요청")
        self.reuse_button.setObjectName("imageCardReuse")
        if on_reuse is not None:
            self.reuse_button.clicked.connect(on_reuse)
        else:
            self.reuse_button.setVisible(False)
        actions.addWidget(self.save_button)
        actions.addWidget(self.copy_button)
        actions.addWidget(self.reuse_button)
        actions.addStretch(1)
        layout.addLayout(actions)


class GenerationCard(QFrame):
    """P20: 생성 중 카드 (프로그레스 + 상태 텍스트 + 취소).

    4cut 의 GenerationCard 를 단일 이미지 생성에 맞게 줄인 버전이다.
    상태를 갖지 않으며 set_status/set_progress 로만 갱신된다.
    """

    def __init__(self, on_cancel: Optional[Callable[[], None]] = None,
                 parent=None):
        super().__init__(parent)
        self.setObjectName("generationCard")
        self.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        self.status_label = QLabel("이미지 생성 중...")
        self.status_label.setObjectName("generationCardStatus")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("generationCardBar")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        layout.addWidget(self.progress_bar)

        self.cancel_button = QPushButton("■ 취소")
        self.cancel_button.setObjectName("generationCardCancel")
        self.cancel_button.setAccessibleName("생성 취소")
        if on_cancel is not None:
            self.cancel_button.clicked.connect(on_cancel)
        layout.addWidget(self.cancel_button)

    def set_status(self, text: str) -> None:
        self.status_label.setText(str(text))

    def set_progress(self, percent: int) -> None:
        try:
            self.progress_bar.setValue(max(0, min(100, int(percent))))
        except (TypeError, ValueError):
            pass

