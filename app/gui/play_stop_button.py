from __future__ import annotations

from typing import ClassVar

from PySide6.QtCore import (
    QEasingCurve,
    QPointF,
    QRectF,
    Qt,
    QVariantAnimation,
)
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QRadialGradient
from PySide6.QtWidgets import QPushButton


class PlayStopButton(QPushButton):
    """Play/Stop toggle button - merges generate and stop into one animated button.

    Based on play_stop_button\uc0d0\ud50c.py's PlaystopButton(QWidget), adapted as a QPushButton subclass.
    - Unchecked (red #C42B1C): '이미지생성 시작' text, play icon
    - Checked (blue #0078D4): '정지' text, stop icon
    """

    # 클래스 변수로 테마 색상 관리 (모든 인스턴스가 공유)
    _theme_colors: ClassVar[dict[str, dict[str, str]]] = {}
    _current_theme: ClassVar[str] = "fluent_dark"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMinimumHeight(42)
        self.setCheckable(True)
        self.setAutoDefault(False)
        self.setChecked(False)

        self._t = 0.0
        self._hover = 0.0
        self._pressed = 0.0

        # 색상 초기화 (테마 색상이 있으면 사용, 없으면 기본값)
        self._apply_theme_color()

        self._anim = QVariantAnimation(self)
        self._anim.setDuration(800)
        self._anim.setEasingCurve(QEasingCurve.Linear)
        self._anim.valueChanged.connect(self._set_t)

        self._hover_anim = QVariantAnimation(self)
        self._hover_anim.setDuration(250)
        self._hover_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._hover_anim.valueChanged.connect(self._set_hover)

        f = QFont("Segoe UI", 14)
        f.setWeight(QFont.Bold)
        self._font = f

        self.toggled.connect(self._on_toggled)
        self.setText("이미지생성 시작")

    def _on_toggled(self, checked):
        self._anim.stop()
        self._anim.setStartValue(self._t)
        self._anim.setEndValue(1.0 if checked else 0.0)
        self._anim.setDuration(1000)
        self._anim.start()
        self.setText("정지" if checked else "이미지생성 시작")

    def _set_t(self, v):
        self._t = float(v)
        self.update()

    def _set_hover(self, v):
        self._hover = float(v)
        self.update()

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
                    "play": {"bg": "#0078D4"},
                    "stop": {"bg": "#C42B1C"},
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
        """현재 테마에 맞는 색상을 적용한다."""
        theme_colors = self._theme_colors
        if not theme_colors:
            # 테마 색상이 없으면 기본값 사용
            self._play_color = QColor("#0078D4")
            self._stop_color = QColor("#C42B1C")
            return

        play_colors = theme_colors.get("play", {"bg": "#0078D4"})
        stop_colors = theme_colors.get("stop", {"bg": "#C42B1C"})
        self._play_color = QColor(play_colors.get("bg", "#0078D4"))
        self._stop_color = QColor(stop_colors.get("bg", "#C42B1C"))
        self.update()

    @staticmethod
    def _ease(t):
        t = max(0.0, min(1.0, t))
        return t * t * (3.0 - 2.0 * t)

    def _draw_shadow(self, p, r):
        shadow = self._stop_color if self._t > 0.5 else self._play_color
        for i in range(8, 0, -1):
            c = QColor(shadow)
            c.setAlpha(int(5 + i * 2))
            rr = QRectF(r)
            rr.translate(0, 6 + i * 0.55)
            rr.adjust(-i * 0.55, -i * 0.20, i * 0.55, i * 0.20)
            p.setPen(Qt.NoPen)
            p.setBrush(c)
            p.drawRoundedRect(rr, 22 + i * 0.15, 22 + i * 0.15)

    def _background(self, p, r):
        play_color = self._play_color  # 파랑 - 이미지 생성 시작
        stop_color = self._stop_color  # 빨강 - 정지
        t = max(0.0, min(1.0, self._t))

        def mix(a, b, amount):
            amount = max(0.0, min(1.0, amount))
            return QColor(
                round(a.red() * (1.0 - amount) + b.red() * amount),
                round(a.green() * (1.0 - amount) + b.green() * amount),
                round(a.blue() * (1.0 - amount) + b.blue() * amount),
            )

        base = mix(play_color, stop_color, t)
        brightness = 1.0 + 0.15 * self._hover
        base.setRed(min(255, round(base.red() * brightness)))
        base.setGreen(min(255, round(base.green() * brightness)))
        base.setBlue(min(255, round(base.blue() * brightness)))

        p.setPen(Qt.NoPen)
        p.setBrush(base)
        p.drawRoundedRect(r, 22, 22)

        fade = 4.0 * t * (1.0 - t)
        if fade > 0.001:
            cx = r.left() + r.width() * (0.15 + 0.70 * t)
            cy = r.top() + r.height() * (0.10 + 0.80 * t)
            radius = max(r.width(), r.height()) * 1.55
            grad = QRadialGradient(QPointF(cx, cy), radius)
            highlight = QColor("#FFFFFF")
            highlight.setAlphaF(0.08 * fade)
            transparent = QColor("#FFFFFF")
            transparent.setAlphaF(0.0)
            grad.setColorAt(0.0, highlight)
            grad.setColorAt(0.55, transparent)
            grad.setColorAt(1.0, transparent)
            p.setBrush(grad)
            p.drawRoundedRect(r, 22, 22)

    def _play_path(self, cx, cy, s=1.0, squash=1.0):
        path = QPainterPath()
        path.moveTo(cx - 6 * s, cy - 11 * s * squash)
        path.lineTo(cx + 10 * s, cy)
        path.lineTo(cx - 6 * s, cy + 11 * s * squash)
        path.closeSubpath()
        return path

    def _stop_bars(self, p, cx, cy, scale=1.0, x=0.0, sy=1.0):
        p.save()
        p.translate(cx + x, cy)
        p.scale(1, sy)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#FFFFFF"))
        p.drawRoundedRect(
            QRectF(-7 * scale, -11 * scale, 4 * scale, 22 * scale), 1.0, 1.0
        )
        p.drawRoundedRect(
            QRectF(3 * scale, -11 * scale, 4 * scale, 22 * scale), 1.0, 1.0
        )
        p.restore()

    def _draw_icon(self, p, cx, cy):
        t = max(0.0, min(1.0, self._t))
        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#FFFFFF"))

        if t < 0.60:
            if t < 0.15:
                sy = 1.0 + 0.10 * self._ease(t / 0.15)
            elif t < 0.30:
                sy = 1.10 - 0.20 * self._ease((t - 0.15) / 0.15)
            elif t < 0.45:
                sy = 0.90 + 0.25 * self._ease((t - 0.30) / 0.15)
            else:
                sy = 1.15 - 0.15 * self._ease((t - 0.45) / 0.15)
            self._stop_bars(p, cx, cy, 0.78, x=6, sy=sy)
        elif t < 1.0:
            u = self._ease((t - 0.60) / 0.40)
            p.save()
            p.translate(cx + 6 * (1 - u), cy + 9 * u)
            p.rotate(-270 * u)
            p.scale(max(0.001, 1 - u), max(0.001, 1 - u))
            p.drawRoundedRect(QRectF(-1.5, -6, 3, 12), 1, 1)
            p.restore()
            p.save()
            p.setOpacity(u)
            p.drawPath(self._play_path(cx, cy, 0.82, 1.0))
            p.restore()
        else:
            self._draw_play(p, cx, cy)

    def _draw_play(self, p, cx, cy):
        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#FFFFFF"))
        p.drawPath(self._play_path(cx, cy, 0.82, 1.0))

    def _draw_stop(self, p, cx, cy):
        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#FFFFFF"))
        p.drawRoundedRect(QRectF(cx - 4, cy - 11, 8, 22), 1.0, 1.0)

    def _draw_text(self, p, r):
        p.setFont(self._font)
        p.setPen(QColor("#FFFFFF"))
        t = max(0.0, min(1.0, self._t))
        u = self._ease(t)
        baseline = r.center().y() + 5

        stop_text = "이미지 생성 시작"
        play_text = "정지"

        stop_alpha = 1.0 - u
        play_alpha = u

        if stop_alpha > 0.0:
            p.save()
            p.setOpacity(stop_alpha)
            stop_width = p.fontMetrics().horizontalAdvance(stop_text)
            stop_x = r.center().x() - stop_width // 2
            p.drawText(stop_x, baseline, stop_text)
            p.restore()
        if play_alpha > 0.0:
            p.save()
            p.setOpacity(play_alpha)
            play_width = p.fontMetrics().horizontalAdvance(play_text)
            play_x = r.center().x() - play_width // 2
            p.drawText(play_x, baseline, play_text)
            p.restore()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.TextAntialiasing, True)
        if not self.isEnabled():
            p.setOpacity(0.5)
        pad = 8
        r = QRectF(pad, 5, max(1, self.width() - 2 * pad), self.height() - 10)
        dy = -1.0 * self._hover + 1.0 * self._pressed
        r.translate(0, dy)
        self._draw_shadow(p, r)
        self._background(p, r)
        self._draw_text(p, r)

    def enterEvent(self, event):
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover)
        self._hover_anim.setEndValue(1.0)
        self._hover_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover)
        self._hover_anim.setEndValue(0.0)
        self._hover_anim.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._pressed = 1.0
            self.update()
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._pressed = 0.0
            self.update()
            if self.rect().contains(event.position().toPoint()):
                self.toggle()
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Space, Qt.Key_Return, Qt.Key_Enter):
            self.toggle()
            event.accept()
            return
        super().keyPressEvent(event)
