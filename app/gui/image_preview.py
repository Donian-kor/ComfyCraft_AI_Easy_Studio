# -*- coding: utf-8 -*-
"""P7: 전체화면 이미지 미리보기 모달 (줌·회전·이전/다음 + 포커스 관리)."""
from __future__ import annotations

from pathlib import Path
from typing import Callable, List, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QShortcut, QKeySequence
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class ClickableLabel(QLabel):
    """클릭 시 clicked 시그널을 보내는 라벨 (카드 이미지용)."""

    clicked = Signal()

    def mousePressEvent(self, event) -> None:  # noqa: N802
        self.clicked.emit()
        super().mousePressEvent(event)


class ImagePreviewModal(QDialog):
    """이미지 전체화면 미리보기.

    - 이미지 목록(paths) + 시작 인덱스로 열기, ◀ ▶ 탐색
    - ＋/－ 줌, 회전, 저장, Esc 닫기
    - 닫을 때 포커스를 트리거 위젯으로 복원 (P7 포커스 관리)
    """

    ZOOM_STEP = 1.25
    MIN_ZOOM = 0.2
    MAX_ZOOM = 8.0

    def __init__(self, parent: Optional[QWidget] = None,
                 on_save: Optional[Callable[[str], None]] = None,
                 on_rewrite: Optional[Callable[[str], None]] = None,
                 on_regenerate: Optional[Callable[[str], None]] = None,
                 on_open_folder: Optional[Callable[[], None]] = None):
        super().__init__(parent)
        self.setObjectName("imagePreviewModal")
        self.setWindowTitle("이미지 미리보기")
        self.setModal(True)
        self.setMinimumSize(640, 480)
        self._on_save = on_save
        self._on_rewrite = on_rewrite
        self._on_regenerate = on_regenerate
        self._on_open_folder = on_open_folder

        self._paths: List[str] = []
        self._index = 0
        self._zoom = 1.0
        self._rotation = 0
        self._base_pixmap = QPixmap()
        self._return_focus_widget: Optional[QWidget] = None

        layout = QVBoxLayout(self)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll.setWidget(self.image_label)
        layout.addWidget(self.scroll, 1)

        self.position_label = QLabel("0 / 0")
        self.position_label.setObjectName("previewPositionLabel")
        self.position_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.position_label)

        bar = QHBoxLayout()
        bar.setSpacing(8)
        self.prev_button = QPushButton("◀")
        self.prev_button.setObjectName("previewPrevBtn")
        self.prev_button.clicked.connect(self.show_prev)
        self.next_button = QPushButton("▶")
        self.next_button.setObjectName("previewNextBtn")
        self.next_button.clicked.connect(self.show_next)
        self.zoom_in_button = QPushButton("＋")
        self.zoom_in_button.setObjectName("previewZoomInBtn")
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button = QPushButton("－")
        self.zoom_out_button.setObjectName("previewZoomOutBtn")
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.rotate_button = QPushButton("회전")
        self.rotate_button.setObjectName("previewRotateBtn")
        self.rotate_button.clicked.connect(self.rotate)
        self.save_button = QPushButton("저장")
        self.save_button.setObjectName("previewSaveBtn")
        self.save_button.clicked.connect(self._on_save_clicked)
        self.close_button = QPushButton("✕ 닫기")
        self.close_button.setObjectName("previewCloseBtn")
        self.close_button.setAccessibleName("미리보기 닫기")
        self.close_button.clicked.connect(self.close)
        for button in (self.prev_button, self.next_button,
                       self.zoom_in_button, self.zoom_out_button,
                       self.rotate_button, self.save_button,
                       self.close_button):
            bar.addWidget(button)
        layout.addLayout(bar)

        # P19: 결과 컨텍스트 액션 행 (프롬프트 재작성 · 다시 만들기 · 폴더)
        self.actions_bar = QHBoxLayout()
        self.actions_bar.setSpacing(8)
        self.rewrite_button = QPushButton("✏️ 프롬프트 재작성")
        self.rewrite_button.setObjectName("previewRewriteBtn")
        self.rewrite_button.setAccessibleName("프롬프트 재작성")
        self.rewrite_button.setToolTip(
            "이 이미지를 만든 프롬프트와 옵션을 불러와 다시 편집합니다.")
        self.rewrite_button.clicked.connect(self._on_rewrite_clicked)
        self.regenerate_button = QPushButton("↻ 다시 만들기")
        self.regenerate_button.setObjectName("previewRegenerateBtn")
        self.regenerate_button.setAccessibleName("다시 만들기")
        self.regenerate_button.setToolTip(
            "이 이미지를 만들 때 사용한 프롬프트와 옵션으로 바로 다시 생성합니다.")
        self.regenerate_button.clicked.connect(self._on_regenerate_clicked)
        self.folder_button = QPushButton("📁 폴더 열기")
        self.folder_button.setObjectName("previewFolderBtn")
        self.folder_button.setAccessibleName("출력 폴더 열기")
        self.folder_button.setToolTip("이미지가 저장된 폴더를 엽니다.")
        self.folder_button.clicked.connect(self._on_folder_clicked)
        for button in (self.rewrite_button, self.regenerate_button,
                       self.folder_button):
            self.actions_bar.addWidget(button)
        self.actions_bar.addStretch(1)
        layout.addLayout(self.actions_bar)

        self._register_shortcut("Esc", self.close)
        self._register_shortcut("Left", self.show_prev)
        self._register_shortcut("Right", self.show_next)
        self._register_shortcut("+", self.zoom_in)
        self._register_shortcut("-", self.zoom_out)

    # -- P19 액션 ----------------------------------------------------------
    def _current_path(self) -> str:
        """현재 보고 있는 이미지 경로 (없으면 빈 문자열)."""
        if not self._paths:
            return ""
        return self._paths[self._index]

    def _run_and_close(self, callback, *args) -> None:
        """액션 실행 후 모달을 닫는다 (콜백 오류는 무시)."""
        if callback is None:
            return
        try:
            callback(*args)
        except Exception:
            pass
        self.close()

    def _on_rewrite_clicked(self) -> None:
        """프롬프트 재작성: 현재 이미지의 스냅샷으로 입력창을 복원."""
        self._run_and_close(self._on_rewrite, self._current_path())

    def _on_regenerate_clicked(self) -> None:
        """다시 만들기: 현재 이미지의 스냅샷으로 즉시 재생성."""
        self._run_and_close(self._on_regenerate, self._current_path())

    def _on_folder_clicked(self) -> None:
        """출력 폴더 열기 (모달은 닫지 않는다)."""
        if self._on_open_folder is not None:
            try:
                self._on_open_folder()
            except Exception:
                pass

    def _register_shortcut(self, key: str, slot) -> None:
        try:
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.setContext(
                Qt.ShortcutContext.WidgetWithChildrenShortcut)
            shortcut.activated.connect(slot)
        except Exception:
            pass

    # -- 열기/닫기 ---------------------------------------------------------
    def open_with(self, paths: List[str], index: int = 0,
                  return_focus_widget: Optional[QWidget] = None,
                  modal: bool = True) -> None:
        """이미지 목록 중 index를 표시. modal=False면 show()만 (테스트용)."""
        self._paths = [p for p in paths if p and Path(p).exists()]
        if not self._paths:
            return
        self._index = max(0, min(index, len(self._paths) - 1))
        self._zoom = 1.0
        self._rotation = 0
        self._return_focus_widget = return_focus_widget
        self._render_current()
        self.close_button.setFocus()
        if modal:
            self.exec()
        else:
            self.show()

    def closeEvent(self, event) -> None:  # noqa: N802
        super().closeEvent(event)
        try:
            target = self._return_focus_widget
            if target is not None:
                target.setFocus()
        except Exception:
            pass

    # -- 렌더링 -------------------------------------------------------------
    def _render_current(self) -> None:
        if not self._paths:
            return
        path = self._paths[self._index]
        pixmap = QPixmap(path)
        if pixmap.isNull():
            self.image_label.setText("이미지를 불러올 수 없습니다.")
            return
        self._base_pixmap = pixmap
        self._apply_transform()
        self.position_label.setText(f"{self._index + 1} / {len(self._paths)}")
        has_many = len(self._paths) > 1
        self.prev_button.setEnabled(has_many)
        self.next_button.setEnabled(has_many)

    def _apply_transform(self) -> None:
        if self._base_pixmap.isNull():
            return
        pixmap = self._base_pixmap
        if self._rotation:
            from PySide6.QtGui import QTransform
            transform = QTransform()
            transform.rotate(self._rotation)
            pixmap = pixmap.transformed(transform,
                                        Qt.TransformationMode.SmoothTransformation)
        w = max(1, int(pixmap.width() * self._zoom))
        scaled = pixmap.scaledToWidth(
            w, Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(scaled)

    # -- 조작 ---------------------------------------------------------------
    def show_prev(self) -> None:
        if len(self._paths) > 1:
            self._index = (self._index - 1) % len(self._paths)
            self._zoom = 1.0
            self._rotation = 0
            self._render_current()

    def show_next(self) -> None:
        if len(self._paths) > 1:
            self._index = (self._index + 1) % len(self._paths)
            self._zoom = 1.0
            self._rotation = 0
            self._render_current()

    def zoom_in(self) -> None:
        self._zoom = min(self.MAX_ZOOM, self._zoom * self.ZOOM_STEP)
        self._apply_transform()

    def zoom_out(self) -> None:
        self._zoom = max(self.MIN_ZOOM, self._zoom / self.ZOOM_STEP)
        self._apply_transform()

    def rotate(self) -> None:
        self._rotation = (self._rotation + 90) % 360
        self._apply_transform()

    def _on_save_clicked(self) -> None:
        if self._on_save is not None and self._paths:
            try:
                self._on_save(self._paths[self._index])
            except Exception:
                pass
