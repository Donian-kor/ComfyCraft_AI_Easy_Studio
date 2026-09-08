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
from PySide6.QtGui import QColor, QFont, QFontMetrics, QPainter, QPainterPath
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QPushButton, QWidget


class SplitTextButton(QPushButton):
    """A blue pill button with the 'letters split & slide' hover effect."""

    def __init__(self, text: str = "Button", parent: QWidget | None = None):
        super().__init__(text, parent)

        # ---- style knobs (mirrors the CSS custom properties) --------------
        self._bg_color = QColor("#275efe")  # --background
        self._text_color = QColor("#ffffff")  # --text
        self._corner_radius = 24  # border-radius: 24px
        self._font_px = 16  # --font-size: 16px
        self._duration_ms = 440  # --duration: .44s
        self._lift_px = 4  # --move-hover: -4px
        self._h_pad = 32  # padding: 16px 32px
        self._v_pad = 16
        self._letter_delay_ms = 50  # i / 20 * 1000s -> 50ms/letter

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
    # sizing
    # ------------------------------------------------------------------ #
    def sizeHint(self) -> QSize:
        fm = QFontMetrics(self.font())
        text = self.text()
        text_w = fm.horizontalAdvance(text) + max(0, len(text) - 1) * 0.5
        w = int(text_w) + self._h_pad * 2
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

        text = self.text()
        total_w = fm.horizontalAdvance(text) + max(0, len(text) - 1) * 0.5
        x = button_rect.left() + (button_rect.width() - total_w) / 2.0
        band_top = button_rect.top() + (button_rect.height() - self._font_px) / 2.0
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
