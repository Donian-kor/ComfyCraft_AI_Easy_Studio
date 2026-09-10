"""
split_text_button.py

PySide6 recreation of the FIRST (default blue) button from:
https://codepen.io/aaroniker/pen/bGGVMbY  ("Button Hover Effects" by Aaron Iker)

Original CSS behaviour being reproduced:
    - blue pill button (#275efe background, white text, 24px corner radius)
    - on hover it "lifts" a few pixels and its box-shadow grows / softens
    - each letter slides upward and is seamlessly replaced by an identical
      duplicate that slides in from below, with a small stagger between
      letters (the CSS did this with `text-shadow` + `transition-delay`;
      here it's done by drawing every letter twice and animating each
      letter's offset with its own QVariantAnimation + start delay)

--------------------------------------------------------------------------
Using this in Qt Designer
--------------------------------------------------------------------------
1. Drop a normal "Push Button" onto your form.
2. Right click it -> "Promote to...".
3. Fill in:
       Promoted class name : SplitTextButton
       Header file          : split_text_button
   (leave "Global include" UNCHECKED)
4. Click "Add", then "Promote".
5. Save the .ui file.

To actually run the form afterwards, either:
  a) Compile it:  pyside6-uic form.ui -o ui_form.py
     pyside6-uic will automatically emit:
         from split_text_button import SplitTextButton
     as long as split_text_button.py is importable (same folder / on PYTHONPATH).
  b) Or load it dynamically at runtime with QUiLoader - just make sure
     split_text_button.py has been imported before/while the .ui loads so
     the class is registered.

Note: this widget paints itself completely in paintEvent(), so normal
QSS rules like `background-color` / `border` written in Designer's
style sheet editor won't have any visible effect. Use the exposed
Designer properties instead (backgroundColor, textColor, cornerRadius,
animationDuration) - they show up in the Property Editor once promoted.
--------------------------------------------------------------------------
"""

from __future__ import annotations

from typing import ClassVar

from PySide6.QtCore import (
    Property,
    QEasingCurve,
    QPointF,
    QRectF,
    QSize,
    Qt,
    QTimer,
    QVariantAnimation,
)
from PySide6.QtGui import QColor, QFont, QFontMetrics, QIcon, QPainter, QPainterPath
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QPushButton, QWidget


class SplitTextButton(QPushButton):
    """A blue pill button with the 'letters split & slide' hover effect.

    Extended from the `버튼샘플.py` sample: the optional QIcon is drawn
    left of the text (when the designer buttons had one), so buttons such
    as toggleLogButton / enhancePromptButton / exitButton keep their icons.

    테마 색상 지원:
        - setStatus(status) 메서드로 버튼 상태 설정 가능
        - status 값: "none", "accent", "success", "error", "warning", "pending"
        - updateThemeColors(theme_key)로 현재 테마 색상 테이블 갱신
    """

    # 클래스 변수로 테마 색상 테이블 관리 (모든 인스턴스가 공유)
    _theme_colors: ClassVar[dict[str, dict[str, str]]] = {}
    _current_theme: ClassVar[str] = "fluent_dark"

    def __init__(self, text: str = "Button", parent: QWidget | None = None):
        super().__init__(text, parent)

        # ---- style knobs (mirrors the CSS custom properties) --------------
        self._bg_color = QColor("#275efe")  # --background
        self._text_color = QColor("#ffffff")  # --text
        self._corner_radius = 24  # border-radius: 24px
        self._font_px = 16  # --font-size: 16px
        self._duration_ms = 440  # --duration: .44s
        self._lift_px = 4  # --move-hover: -4px
        self._h_pad = 24  # padding: 16px 32px  (slightly reduced to fit UI)
        self._v_pad = 14
        self._letter_delay_ms = 50  # i / 20 * 1000s -> 50ms/letter
        self._icon_gap_px = 8  # space between icon and text

        # 상태 속성 (속성 변경 시 색상 업데이트)
        self._status = "none"  # "none", "accent", "success", "error", "warning", "pending"

        self.setFont(self._make_font())
        self.setCursor(Qt.PointingHandCursor)
        self.setFlat(True)
        # fully custom-painted -> keep the native chrome out of the way
        self.setStyleSheet("QPushButton { border: none; background: transparent; }")

        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setColor(QColor(39, 94, 254, 82))
        self._shadow.setBlurRadius(16)
        self._shadow.setOffset(0, 4)
        self.setGraphicsEffect(self._shadow)

        # init 후 테마 색상 적용 (shadow 생성 후 호출)
        self._apply_theme_color()

        # ---- animated state -------------------------------------------------
        self._hovered = False
        self._rise = 0.0  # current vertical lift, 0..lift_px
        self._shadow_t = 0.0  # 0 = resting shadow, 1 = hover shadow

        self._rise_anim = QVariantAnimation(self)
        self._rise_anim.setDuration(self._duration_ms)
        self._rise_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._rise_anim.valueChanged.connect(self._on_rise_changed)

        self._shadow_anim = QVariantAnimation(self)
        self._shadow_anim.setDuration(self._duration_ms)
        self._shadow_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._shadow_anim.valueChanged.connect(self._on_shadow_changed)

        self._letter_progress: list[float] = []
        self._letter_anims: list[QVariantAnimation] = []
        self._rebuild_letters()

    # ------------------------------------------------------------------ #
    # text handling
    # ------------------------------------------------------------------ #
    def setText(self, text: str) -> None:  # noqa: N802 (Qt override)
        super().setText(text)
        self._rebuild_letters()
        self.updateGeometry()
        self.update()

    def _rebuild_letters(self) -> None:
        for anim in self._letter_anims:
            anim.stop()

        letters = list(self.text())
        self._letter_progress = [0.0] * len(letters)
        self._letter_anims = []
        for _ in letters:
            anim = QVariantAnimation(self)
            anim.setDuration(self._duration_ms)
            anim.setEasingCurve(QEasingCurve.OutCubic)
            self._letter_anims.append(anim)
        for i, anim in enumerate(self._letter_anims):
            anim.valueChanged.connect(lambda v, idx=i: self._on_letter_changed(idx, v))

    def _make_font(self) -> QFont:
        font = QFont("Roboto")
        if font.family().lower() != "roboto":
            font = (
                QFont()
            )  # fall back to the platform default if Roboto isn't installed
        font.setPixelSize(self._font_px)
        font.setWeight(QFont.Weight.Medium)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 0.5)  # letter-spacing: .5px
        return font

    # ------------------------------------------------------------------ #
    # Designer-editable properties
    # ------------------------------------------------------------------ #
    def getBackgroundColor(self) -> QColor:
        return self._bg_color

    def setBackgroundColor(self, color: QColor) -> None:
        self._bg_color = QColor(color)
        self._on_shadow_changed(self._shadow_t)  # refresh shadow tint
        self.update()

    backgroundColor = Property(QColor, getBackgroundColor, setBackgroundColor)

    def getTextColor(self) -> QColor:
        return self._text_color

    def setTextColor(self, color: QColor) -> None:
        self._text_color = QColor(color)
        self.update()

    textColor = Property(QColor, getTextColor, setTextColor)

    def getCornerRadius(self) -> int:
        return self._corner_radius

    def setCornerRadius(self, value: int) -> None:
        self._corner_radius = value
        self.update()

    cornerRadius = Property(int, getCornerRadius, setCornerRadius)

    def getAnimationDuration(self) -> int:
        return self._duration_ms

    def setAnimationDuration(self, ms: int) -> None:
        self._duration_ms = ms
        self._rise_anim.setDuration(ms)
        self._shadow_anim.setDuration(ms)
        for anim in self._letter_anims:
            anim.setDuration(ms)

    animationDuration = Property(int, getAnimationDuration, setAnimationDuration)

    # ------------------------------------------------------------------ #
    # 테마 색상 지원
    # ------------------------------------------------------------------ #

    @classmethod
    def updateThemeColors(
        cls,
        theme_key: str,
        colors: dict[str, dict[str, str]],
    ) -> None:
        """테마 색상 테이블을 갱신하고 모든 인스턴스의 색상을 업데이트한다.

        Args:
            theme_key: 현재 테마 키 (예: "fluent_dark")
            colors: 상태별 색상 딕셔너리
                {
                    "accent": {"bg": "#0078D4", "text": "#ffffff"},
                    "success": {"bg": "#4edea3", "text": "#ffffff"},
                    "error": {"bg": "#ffb4ab", "text": "#ffffff"},
                    "warning": {"bg": "#fbbf24", "text": "#1a1a1a"},
                    "pending": {"bg": "#b8c0cc", "text": "#ffffff"},
                }
        """
        cls._theme_colors = colors
        cls._current_theme = theme_key
        try:
            from PySide6.QtWidgets import QApplication
            app = QApplication.instance()
            if app is not None:
                for widget in app.topLevelWidgets():
                    for child in widget.findChildren(cls):
                        child._apply_theme_color()
        except Exception:
            pass

    def _apply_theme_color(self) -> None:
        """현재 상태에 맞는 테마 색상을 적용한다."""
        theme_colors = self._theme_colors
        if not theme_colors:
            return
        status = self._status
        if status not in theme_colors:
            status = "accent"
        colors = theme_colors.get(status, {})
        bg_hex = colors.get("bg", "#275efe")
        text_hex = colors.get("text", "#ffffff")
        self._bg_color = QColor(bg_hex)
        self._text_color = QColor(text_hex)
        # 섀도우 색상도 배경색에 맞게 업데이트
        self._shadow.setColor(QColor(self._bg_color.red(), self._bg_color.green(),
                                       self._bg_color.blue(), 82))
        self.update()

    def getStatus(self) -> str:
        """현재 버튼 상태 반환."""
        return self._status

    def setStatus(self, status: str) -> None:
        """버튼 상태 설정 (테마 색상 적용).

        Args:
            status: "none", "accent", "success", "error", "warning", "pending"
        """
        valid = ("none", "accent", "success", "error", "warning", "pending")
        if status not in valid:
            status = "none"
        if status != self._status:
            self._status = status
            self._apply_theme_color()

    status = Property(str, getStatus, setStatus)

    # ------------------------------------------------------------------ #
    # sizing
    # ------------------------------------------------------------------ #
    def sizeHint(self) -> QSize:
        fm = QFontMetrics(self.font())
        text = self.text()
        text_w = fm.horizontalAdvance(text) + max(0, len(text) - 1) * 0.5
        icon_w = 0
        if not self.icon().isNull():
            icon_w = self.iconSize().width()
        gap = self._icon_gap_px if (icon_w and text_w) else 0
        w = int(text_w + icon_w + gap) + self._h_pad * 2
        h = self._font_px + self._v_pad * 2 + self._lift_px
        return QSize(w, h)

    def minimumSizeHint(self) -> QSize:
        return self.sizeHint()

    # ------------------------------------------------------------------ #
    # hover handling
    # ------------------------------------------------------------------ #
    def enterEvent(self, event) -> None:
        self._set_hovered(True)
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self._set_hovered(False)
        super().leaveEvent(event)

    def _set_hovered(self, hovered: bool) -> None:
        if hovered == self._hovered:
            return
        self._hovered = hovered

        self._rise_anim.stop()
        self._rise_anim.setStartValue(self._rise)
        self._rise_anim.setEndValue(float(self._lift_px) if hovered else 0.0)
        self._rise_anim.start()

        self._shadow_anim.stop()
        self._shadow_anim.setStartValue(self._shadow_t)
        self._shadow_anim.setEndValue(1.0 if hovered else 0.0)
        self._shadow_anim.start()

        for i, anim in enumerate(self._letter_anims):
            anim.stop()
            start = self._letter_progress[i] if i < len(self._letter_progress) else 0.0
            anim.setStartValue(start)
            anim.setEndValue(1.0 if hovered else 0.0)
            delay = i * self._letter_delay_ms
            if delay:
                QTimer.singleShot(delay, anim.start)
            else:
                anim.start()

    # ------------------------------------------------------------------ #
    # animation callbacks
    # ------------------------------------------------------------------ #
    def _on_rise_changed(self, value) -> None:
        self._rise = float(value)
        self.update()

    def _on_shadow_changed(self, value) -> None:
        self._shadow_t = float(value)
        blur = 16 + (30 - 16) * self._shadow_t  # ~ 0 2px 8px -> 0 4px 20px
        off_y = 4 + (8 - 4) * self._shadow_t
        alpha = int(82 + (128 - 82) * self._shadow_t)  # .32 -> .5 opacity
        c = QColor(self._bg_color)
        c.setAlpha(alpha)
        self._shadow.setBlurRadius(blur)
        self._shadow.setOffset(0, off_y)
        self._shadow.setColor(c)

    def _on_letter_changed(self, idx: int, value) -> None:
        if idx < len(self._letter_progress):
            self._letter_progress[idx] = float(value)
        self.update()

    # ------------------------------------------------------------------ #
    # painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, event) -> None:  # noqa: ARG002
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        rect = self.rect()
        # reserve `lift_px` of head-room at the top for the hover "lift"
        button_rect = QRectF(
            0,
            self._lift_px - self._rise,
            rect.width(),
            rect.height() - self._lift_px,
        )

        path = QPainterPath()
        path.addRoundedRect(button_rect, self._corner_radius, self._corner_radius)
        painter.fillPath(path, self._bg_color)

        painter.setPen(self._text_color)
        painter.setFont(self.font())
        fm = QFontMetrics(self.font())

        icon = self.icon()
        icon_w = 0
        icon_h = 0
        if not icon.isNull():
            icon_w = self.iconSize().width()
            icon_h = self.iconSize().height()
        gap = self._icon_gap_px if (icon_w and self.text()) else 0

        text = self.text()
        total_w = fm.horizontalAdvance(text) + max(0, len(text) - 1) * 0.5
        content_w = icon_w + gap + total_w
        x = button_rect.left() + (button_rect.width() - content_w) / 2.0
        band_top = button_rect.top() + (button_rect.height() - self._font_px) / 2.0

        # draw the icon (if any) left of the text
        if icon_w:
            icon_rect = QRectF(
                x,
                button_rect.top() + (button_rect.height() - icon_h) / 2.0,
                icon_w,
                icon_h,
            )
            mode = QIcon.Mode.Normal if self.isEnabled() else QIcon.Mode.Disabled
            icon.paint(
                painter,
                icon_rect.toRect(),
                Qt.AlignmentFlag.AlignCenter,
                mode,
                QIcon.State.Off,
            )
            x += icon_w + gap

        if not total_w:
            return

        band = QRectF(x - 2, band_top, total_w + 4, self._font_px)

        painter.save()
        painter.setClipRect(band)
        cursor_x = x
        baseline = band_top + fm.ascent()
        for i, ch in enumerate(text):
            ch_w = fm.horizontalAdvance(ch)
            p = self._letter_progress[i] if i < len(self._letter_progress) else 0.0
            off = p * self._font_px
            # the letter sliding up and out of the clipped band
            painter.drawText(QPointF(cursor_x, baseline - off), ch)
            # its identical duplicate sliding in from below (was the
            # CSS `text-shadow` trick)
            painter.drawText(QPointF(cursor_x, baseline + self._font_px - off), ch)
            cursor_x += ch_w + 0.5
        painter.restore()


# ---------------------------------------------------------------------- #
# stand-alone demo:  python split_text_button.py
# ---------------------------------------------------------------------- #
if __name__ == "__main__":
    import sys

    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("SplitTextButton demo")
    window.setStyleSheet("background: #E4ECFA;")
    layout = QVBoxLayout(window)
    layout.setContentsMargins(60, 60, 60, 60)
    layout.setAlignment(Qt.AlignCenter)

    button = SplitTextButton("Button")
    layout.addWidget(button, alignment=Qt.AlignCenter)

    window.resize(320, 200)
    window.show()
    sys.exit(app.exec())
