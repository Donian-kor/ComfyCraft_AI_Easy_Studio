"""Z-ANIME 프롬프트 스타일 버튼 — 테마 색상 대응 커스텀 버튼.

기능
-----
* 일반 QPushButton을 상속해 Z-ANIME 전용 스타일을 유지한다.
* 테마 변경 시 색상 테이블을 받아 버튼별 색상을 갱신할 수 있다.
* 생성된 모든 인스턴스를 클래스 레벨에서 추적해 테마 적용 시 일괄 갱신한다.
"""
from __future__ import annotations

import weakref
from typing import ClassVar, Dict

from PySide6.QtWidgets import QPushButton, QStyle

from app.gui.design_tokens import (
    CORNER_RADIUS,
    DISABLED_OPACITY,
    DEFAULT_BG,
    DEFAULT_TEXT,
    DEFAULT_UNSELECTED_BG,
    DEFAULT_UNSELECTED_BORDER,
    DEFAULT_UNSELECTED_TEXT,
    PADDING_H,
    PADDING_V,
)


class ZAnimeStyleButton(QPushButton):
    """Z-ANIME 프롬프트 스타일 선택용 버튼.

    * checkable로 쓰이며, 선택/비선택 상태에 따라 다른 색상을 적용한다.
    * 테마가 바뀌면 ``update_theme_colors()``로 전체 색상을 갱신한다.
    """

    _instances: ClassVar["weakref.WeakSet[ZAnimeStyleButton]"] = weakref.WeakSet()
    _current_key: ClassVar[str | None] = None
    _current_colors: ClassVar[dict[str, str] | None] = None

    def __init__(self, text: str = "", parent=None) -> None:
        super().__init__(text, parent)
        self.setCheckable(True)
        self._base_style_sheet = ""
        ZAnimeStyleButton._instances.add(self)
        self._apply_current_colors()

    @classmethod
    def update_theme_colors(cls, key: str, colors: dict[str, str]) -> None:
        """현재 테마 키와 색상 테이블을 저장하고, 기존 버튼 색상을 갱신한다."""
        cls._current_key = key
        cls._current_colors = dict(colors or {})
        for instance in cls._instances:
            try:
                instance.update_colors(cls._current_colors)
            except Exception:
                pass

    @classmethod
    def _apply_current_colors(cls, instance: ZAnimeStyleButton | None = None) -> None:
        """저장된 테마 색상이 있으면 해당 인스턴스에 적용한다."""
        if cls._current_colors is None:
            return
        target = instance or cls._instances
        if isinstance(target, ZAnimeStyleButton):
            target.update_colors(dict(cls._current_colors))
        else:
            for btn in target:
                try:
                    btn.update_colors(dict(cls._current_colors))
                except Exception:
                    pass

    def update_colors(self, colors: dict[str, str]) -> None:
        """개별 버튼의 색상 사전을 받아 스타일을 다시 적용한다."""
        if not colors:
            return
        self._base_style_sheet = _build_stylesheet(colors)
        try:
            self.setStyleSheet(self._base_style_sheet)
            # Qt 스타일이 갱신되도록 unpolish/polish를 시도한다.
            style = self.style()
            if style is not None:
                style.unpolish(self)
                style.polish(self)
        except Exception:
            pass
        self.update()

    def set_selected(self, selected: bool) -> None:
        """선택 상태를 바꾸고, 그에 맞는 스타일만 갱신한다."""
        self.setChecked(selected)
        self._sync_style_from_state()

    def _sync_style_from_state(self) -> None:
        colors = ZAnimeStyleButton._current_colors or {}
        selected = bool(self.isChecked())
        self._apply_state_colors(colors, selected)

    def _apply_state_colors(self, colors: dict[str, str], selected: bool) -> None:
        if selected:
            bg = colors.get("selected_bg", DEFAULT_BG)
            text = colors.get("selected_text", DEFAULT_TEXT)
            border = colors.get("selected_border", DEFAULT_UNSELECTED_BORDER)
        else:
            bg = colors.get("unselected_bg", DEFAULT_UNSELECTED_BG)
            text = colors.get("unselected_text", DEFAULT_UNSELECTED_TEXT)
            border = colors.get("unselected_border", DEFAULT_UNSELECTED_BORDER)
        base = _build_stylesheet({
            "bg": bg,
            "text": text,
            "border": border,
            "selected_bg": colors.get("selected_bg", DEFAULT_BG),
            "selected_text": colors.get("selected_text", DEFAULT_TEXT),
            "selected_border": colors.get("selected_border", DEFAULT_UNSELECTED_BORDER),
            "unselected_bg": colors.get("unselected_bg", DEFAULT_UNSELECTED_BG),
            "unselected_text": colors.get("unselected_text", DEFAULT_UNSELECTED_TEXT),
            "unselected_border": colors.get("unselected_border", DEFAULT_UNSELECTED_BORDER),
        }, selected=selected)
        try:
            self.setStyleSheet(base)
        except Exception:
            pass
        self.update()


def _build_stylesheet(colors: dict[str, str], selected: bool = False) -> str:
    """색상 사전으로 Z-ANIME 스타일 버튼의 스타일시트를 만든다."""
    if selected:
        bg = colors.get("selected_bg", DEFAULT_BG)
        text = colors.get("selected_text", DEFAULT_TEXT)
        border = colors.get("selected_border", DEFAULT_UNSELECTED_BORDER)
    else:
        bg = colors.get("unselected_bg", DEFAULT_UNSELECTED_BG)
        text = colors.get("unselected_text", DEFAULT_UNSELECTED_TEXT)
        border = colors.get("unselected_border", DEFAULT_UNSELECTED_BORDER)

    r = CORNER_RADIUS
    ph, pv = PADDING_H, PADDING_V

    return (
        f"QPushButton {{"
        f" background-color: {bg};"
        f" color: {text};"
        f" border: 1px solid {border};"
        f" border-radius: {r}px;"
        f" padding: {pv}px {ph}px; font-weight: 600; font-size: 13px;"
        f"}}"
        f"QPushButton:hover {{"
        f" background-color: {border};"
        f" color: {'#ffffff' if not selected else '#ffffff'};"
        f"}}"
        f"QPushButton:pressed {{"
        f" background-color: {border};"
        f" color: #ffffff;"
        f"}}"
        f"QPushButton:checked {{"
        f" background-color: {bg};"
        f" color: {text};"
        f" border: 2px solid {border};"
        f"}}"
    )
