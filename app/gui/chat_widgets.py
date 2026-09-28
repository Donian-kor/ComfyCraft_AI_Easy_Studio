# -*- coding: utf-8 -*-
"""P2: 채팅 말풍선 + 카드 위젯 (껍데기, 로직 없음).

- ChatMessage: role(user/ai/system)별 말풍선. action_row는 P4/P6 버튼이 얹히는 자리.
- PromptCard: AI 가 다듬은 프롬프트 확인 카드 (편집 가능).
- GenerationCard: 생성 중 카드 (상태 + 진행률 + 취소).
- ImageCard: 완성 이미지 + 메타 + 프롬프트 접기 + 저장/복사/수정 요청.

위젯은 상태를 갖지 않는다. 어떤 카드를 그릴지는 ChatViewManager 가
세션 메시지(kind/metadata)로부터 결정한다.
"""
from __future__ import annotations

from typing import Callable, Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFontMetrics, QPixmap
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
    """클릭 시 clicked 시그널을 보내는 라벨 (카드 이미지용).

    4cut(4cut_LocalComic_Studio studio/ui/chat_widgets.py AspectPixmapLabel) 의
    비율 유지 자동 리사이즈 동작을 그대로 이식했다.
    기존에는 생성 시점에 scaledToWidth(480) 로 한 번만 스케일을 고정해
    창을 넓혀도 이미지가 커지지 않았고, 세로로 긴 이미지(1152x896 등)는
    라벨 영역을 벗어났다. 이제 위젯 크기에 맞춰 언제든 다시 맞춘다.
    (색상·테마는 QSS 가 담당하므로 이 클래스는 픽스맵 크기만 다룬다)
    """

    clicked = Signal()

    # 창이 좁아져도 이 폭 아래로는 줄이지 않는다 (아래로 분주해지는 것을 막음).
    MIN_RENDER = 60

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pixmap: Optional[QPixmap] = None
        self._path = ""
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(self.MIN_RENDER, self.MIN_RENDER)

    def set_image_path(self, path: str) -> bool:
        """경로의 이미지를 불러와 크기에 맞춰 표시한다. 실패 시 False."""
        self._path = str(path or "")
        if self._path:
            pixmap = QPixmap(self._path)
            if not pixmap.isNull():
                self._pixmap = pixmap
                self._render()
                return True
        self._pixmap = None
        self.clear()
        return False

    def image_path(self) -> str:
        return self._path

    def source_pixmap(self) -> Optional[QPixmap]:
        return self._pixmap

    def _render(self) -> None:
        """위젯 크기에 맞춰 비율을 유지한 채 다시 스케일한다.

        세로가 Fixed 정책이라 높이는 위젯이 스스로 계산해 갱신해야 한다.
        가로 폭에 맞춰 비율로 높이를 정한 뒤 setFixedHeight 로 알리고,
        다시 그려 반복되는 것을 막기 위해 폭이 실제로 바뀐 경우만 갱신한다.
        """
        if self._pixmap is None or self._pixmap.isNull():
            return
        source = self._pixmap
        width = max(self.MIN_RENDER, self.width())
        # 세로는 가로 폭에서 비율로 계산한다 (위젯 높이에 의존하지 않는다).
        height = max(
            self.MIN_RENDER,
            int(round(width * source.height() / max(1, source.width()))),
        )
        if self.height() != height:
            self.setFixedHeight(height)
        self.setPixmap(source.scaled(
            width,
            height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        ))

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        # 높이 갱신(setFixedHeight)이 다시 resizeEvent 를 부르므로 폭이 실제로
        # 달라졌을 때만 다시 그린다. 무한 재귀를 막는다.
        if self.width() != getattr(self, "_last_render_width", None):
            self._last_render_width = self.width()
            self._render()

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        self._render()

    def mousePressEvent(self, event) -> None:  # noqa: N802
        self.clicked.emit()
        super().mousePressEvent(event)


class ChatMessage(QFrame):
    """대화 메시지 1개. role에 따라 정렬·색상이 달라진다."""

    # 말풍선 최대 폭(기존 body.setMaximumWidth 과 같은 값).
    BUBBLE_MAX_WIDTH = 600
    # 버블 QSS padding(10px 14px)의 좌우 합 + Qt 가 정확히 재지 않는 여유분.
    BUBBLE_PADDING = 32

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
        self.body.setMaximumWidth(self.BUBBLE_MAX_WIDTH)
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

    def set_text(self, text: str) -> None:
        """버블 문구 교체. 최소 폭도 함께 갱신한다."""
        self.bubble.setText(str(text))
        self._apply_bubble_min_width()

    def _bubble_min_width(self) -> int:
        """문장이 한 단어씩 세로로 접히지 않도록 하는 최소 폭.

        wordWrap 이 켜진 QLabel 은 heightForWidth 를 쓰기 때문에, 레이아웃이
        가로 폭을 줄 때 자연폭(sizeHint) 이 아니라 minimumSizeHint — 즉
        가장 긴 단어 하나의 폭 — 을 배정한다. 그 결과 문장이 60px 폭으로
        접혀 한 단어씩 세로로 줄바꿈된다. 그래서 자연폭을 최소 폭으로 명시한다.
        """
        text = self.bubble.text()
        if not text:
            return 0
        width = QFontMetrics(self.bubble.font()).horizontalAdvance(text)
        return min(self.BUBBLE_MAX_WIDTH, width + self.BUBBLE_PADDING)

    def _apply_bubble_min_width(self) -> None:
        self.bubble.setMinimumWidth(self._bubble_min_width())

    def showEvent(self, event):  # noqa: N802
        # 생성 시점에는 스타일이 아직 polish 되기 전이라 폰트 크기가 확정되지
        # 않는다. 실제로 그려질 때 한 번 다시 계산해 테마 전환까지 흡수한다.
        self._apply_bubble_min_width()
        super().showEvent(event)


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

    # 이미지의 최대 표시 폭. 화면 폭에 맞춰 ��하되 이 값을 넘지 않는다.
    IMAGE_MAX_WIDTH = 560
    # 최소 표시 폭. 매우 좁은 화면에서도 이 폭 아래로 줄이지 않는다.
    IMAGE_MIN_WIDTH = 260

    def __init__(
        self,
        image_path: str,
        meta_text: str,
        prompt_text: str,
        on_save: Optional[Callable[[str], None]] = None,
        on_copy_image: Optional[Callable[[str], None]] = None,
        on_reuse: Optional[Callable[[], None]] = None,
        on_open: Optional[Callable[[], None]] = None,
        parent=None,
    ):
        super().__init__(parent)
        self.setObjectName("imageCard")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        # 카드마다 자기 이미지를 기억한다. 콜백이 경로를 받도록 해서
        # 전역 '마지막 생성 이미지(current_image_path)' 에 의존하지 않는다.
        self.image_path = str(image_path or "")

        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        self.image_label = ClickableLabel()
        self.image_label.setObjectName("imageCardImage")
        self.image_label.setCursor(Qt.CursorShape.PointingHandCursor)
        if on_open is not None:
            self.image_label.clicked.connect(on_open)
        if not self.image_label.set_image_path(self.image_path):
            self.image_label.setText("이미지를 불러올 수 없습니다."
                                     if self.image_path else "")
        self.image_label.setMinimumWidth(self.IMAGE_MIN_WIDTH)
        self.image_label.setMaximumWidth(self.IMAGE_MAX_WIDTH)
        # 세로 방향으로는 이미지가 정한 만큼만 차지해야 하므로 Fixed 를 유지한다.
        # (가로는 아래 resizeEvent 에서 위젯 크기에 맞춰 다시 맞춘다)
        self.image_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        layout.addWidget(self.image_label, 0, Qt.AlignmentFlag.AlignHCenter)

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
        prompt_row.addStretch(1)
        layout.addLayout(prompt_row)
        layout.addWidget(self.prompt_label)

        # 액션 버튼
        actions = QHBoxLayout()
        actions.setSpacing(8)
        self.save_button = QPushButton("저장")
        self.save_button.setObjectName("imageCardSave")
        if on_save is not None:
            self.save_button.clicked.connect(
                lambda _checked=False: on_save(self.image_path))
        self.copy_button = QPushButton("복사")
        self.copy_button.setObjectName("imageCardCopy")
        if on_copy_image is not None:
            self.copy_button.clicked.connect(
                lambda _checked=False: on_copy_image(self.image_path))
        # P6: 수정 요청 (프롬프트+옵션 전체 복원). 콜백 없으면 숨김.
        # clicked(bool) 의 bool 이 스냅샷 자리에 매핑되면 스냅샷이 False 로 덮이므로
        # 시그널 인자를 버리고 무인자 호출로 감싼다.
        self.reuse_button = QPushButton("수정 요청")
        self.reuse_button.setObjectName("imageCardReuse")
        if on_reuse is not None:
            self.reuse_button.clicked.connect(
                lambda _checked=False: on_reuse())
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

