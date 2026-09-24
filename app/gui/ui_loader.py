from __future__ import annotations

from pathlib import Path
from typing import cast

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QDialog, QPushButton

from app.gui.play_stop_button import PlayStopButton
from app.gui.split_text_button import SplitTextButton


def _in_sidebar(widget) -> bool:
    """위젯이 사이드바(sidebar_frame) 안에 있는지 확인한다."""
    parent = widget.parentWidget()
    while parent is not None:
        if parent.objectName() == "sidebar_frame":
            return True
        parent = parent.parentWidget()
    return False


def _replace_in_layouts(layout, old_widget, new_widget) -> bool:
    """중첩된 레이아웃 트리에서 old_widget을 new_widget으로 교체한다."""
    if layout is None:
        return False
    for i in range(layout.count()):
        item = layout.itemAt(i)
        if item.widget() is old_widget:
            layout.replaceWidget(old_widget, new_widget)
            return True
        child = item.layout()
        if child is not None and _replace_in_layouts(child, old_widget, new_widget):
            return True
    return False


def _upgrade_buttons(root) -> None:
    """이름에 'Button'이 들어간 QPushButton을 SplitTextButton으로 교체한다.

    - sidebar_frame 안에 있는 버튼(homeButton, pushButton, comfyButton,
      lmstudioButton, settingsButton)은 사이드바 디자인을 유지한다.
    - PlayStopButton(generateButton)은 이미 전용 디자인이므로 건드리지 않는다.
    """
    for old in list(root.findChildren(QPushButton)):
        name = old.objectName() or ""
        if "Button" not in name:
            continue
        if isinstance(old, SplitTextButton):
            continue
        if isinstance(old, PlayStopButton):
            continue
        if _in_sidebar(old):
            continue

        parent = old.parentWidget()
        if parent is None:
            continue

        new_btn = SplitTextButton(old.text(), parent)

        # --- 기존 버튼의 속성/동작 복사 ---
        new_btn.setObjectName(old.objectName())
        new_btn.setToolTip(old.toolTip())
        new_btn.setStatusTip(old.statusTip())
        new_btn.setWhatsThis(old.whatsThis())
        new_btn.setEnabled(old.isEnabled())
        new_btn.setCheckable(old.isCheckable())
        new_btn.setChecked(old.isChecked())
        new_btn.setAutoDefault(old.autoDefault())
        new_btn.setDefault(old.isDefault())
        new_btn.setIcon(old.icon())
        new_btn.setIconSize(old.iconSize())
        new_btn.setMinimumSize(old.minimumSize())
        new_btn.setMaximumSize(old.maximumSize())
        new_btn.setSizePolicy(old.sizePolicy())
        new_btn.setFocusPolicy(old.focusPolicy())
        new_btn.setGeometry(old.geometry())

        # 레이아웃 안에 있는 경우 위치 유지, 아닌 경우(geometry 배치)도 유지
        layout = parent.layout()
        replaced = _replace_in_layouts(layout, old, new_btn) if layout else False
        if not replaced:
            new_btn.setGeometry(old.geometry())

        # 중요: deleteLater()만 호출하면 이벤트 루프가 돌 때까지 옛 버튼이
        # 위젯 트리에 남아 있어서, main.py 의 findChild()가 삭제 예정인
        # 옛 버튼을 먼저 찾아 시그널이 연결되고 나중에 삭제돼 버린다.
        # 따라서 위젯 트리에서 즉시 제거(setParent(None))한 뒤 지운다.
        old.setParent(None)
        old.deleteLater()


def load_dialog_ui(path: Path, parent=None) -> QDialog:
    """QDialog용 .ui 파일을 로드한다 (버튼 업그레이드 없이 그대로 반환).

    설정/도움말 다이얼로그처럼 레이아웃을 그대로 유지해야 하는 경우 사용.
    """
    loader = QUiLoader()
    file = QFile(str(path))
    if not file.open(QIODevice.ReadOnly):
        raise RuntimeError(f"UI 파일을 열 수 없습니다: {path}")
    try:
        obj = loader.load(file, parent)
    finally:
        file.close()
    if obj is None:
        raise RuntimeError(f"Qt가 UI 파일을 읽지 못했습니다: {path}")
    # QUiLoader.load()는 QWidget으로 추론되지만, 이 함수가 로드하는 .ui 파일은
    # 루트가 QDialog이므로 Pylance에 알려주기 위해 cast()로 감싼다.
    return cast(QDialog, obj)


def load_ui(path: Path):
    loader = QUiLoader()
    loader.registerCustomWidget(PlayStopButton)
    file = QFile(str(path))
    if not file.open(QIODevice.ReadOnly):
        raise RuntimeError(f"UI 파일을 열 수 없습니다: {path}")
    try:
        obj = loader.load(file)
    finally:
        file.close()
    if obj is None:
        raise RuntimeError(f"Qt가 UI 파일을 읽지 못했습니다: {path}")
    _upgrade_buttons(obj)
    return obj
