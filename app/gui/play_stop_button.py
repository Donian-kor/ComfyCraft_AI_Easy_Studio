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

from app.gui.design_tokens import (
    CORNER_RADIUS_PLAYSTOP,
    DISABLED_OPACITY,
    DURATION_FAST,
    DURATION_SLOW,
    EASE_IN_OUT_CUBIC,
    EASE_OUT_CUBIC,
    FOCUS_BORDER_COLOR,
    FOCUS_BORDER_WIDTH,
    LIFT_PLAYSTOP,
    PADDING_H,
    PLAY_TEXT,
    STOP_TEXT,
)


class PlayStopButton(QPushButton):
    """Play/Stop toggle button - merges generate and stop into one animated button.

    Based on play_stop_button\uc0d0\ud50c.py's PlaystopButton(QWidget), adapted as a QPushButton subclass.
    - Unchecked (blue #0078D4): PLAY_TEXT('이미지 생성 시작') text, play icon
    - Checked (red #C42B1C): STOP_TEXT('정지') text, stop icon
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
        self._anim.setDuration(DURATION_SLOW)       # 1000 (token)
        self._anim.setEasingCurve(EASE_IN_OUT_CUBIC)  # Linear → InOutCubic (token)

        self._hover_anim = QVariantAnimation(self)
        self._hover_anim.setDuration(DURATION_FAST) # 180 (token, was 250)
        self._hover_anim.setEasingCurve(EASE_OUT_CUBIC)  # OutCubic (token)
        self._hover_anim.valueChanged.connect(self._set_hover)

        f = QFont("Segoe UI", 14)
        f.setWeight(QFont.Bold)
        self._font = f

        self.toggled.connect(self._on_toggled)
        self.setText(PLAY_TEXT)

    def _on_toggled(self, checked):
        self._anim.stop()
        self._anim.setStartValue(self._t)
        self._anim.setEndValue(1.0 if checked else 0.0)
        self._anim.setDuration(DURATION_SLOW)
        self._anim.start()
        self.setText(STOP_TEXT if checked else PLAY_TEXT)

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
            p.drawRoundedRect(rr, CORNER_RADIUS_PLAYSTOP + i * 0.15, CORNER_RADIUS_PLAYSTOP + i * 0.15)

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
        p.drawRoundedRect(r, CORNER_RADIUS_PLAYSTOP, CORNER_RADIUS_PLAYSTOP)

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

    def _draw_play(self, p, cx, cy):
        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#FFFFFF"))
        p.drawPath(self._play_path(cx, cy, 0.82, 1.0))

    def _draw_content(self, p, r):
        p.setFont(self._font)
        p.setPen(QColor("#FFFFFF"))
        fm = p.fontMetrics()

        t = max(0.0, min(1.0, self._t))
        u = self._ease(t)

        play_w = fm.horizontalAdvance(PLAY_TEXT)
        stop_w = fm.horizontalAdvance(STOP_TEXT)

        cur_text_w = play_w * (1.0 - u) + stop_w * u
        icon_w = 16.0
        gap = 8.0
        total_w = icon_w + gap + cur_text_w

        start_x = r.center().x() - total_w / 2.0
        icon_cx = start_x + icon_w / 2.0
        icon_cy = r.center().y()

        text_start_x = start_x + icon_w + gap
        baseline = r.center().y() + 5

        # 1) 아이콘: Play 삼각형 <-> Stop 막대 (회전 + 페이드 모핑)
        play_op = max(0.0, min(1.0, (0.7 - u) / 0.7))
        if play_op > 0.01:
            p.save()
            p.translate(icon_cx, icon_cy)
            p.rotate(45 * u)
            p.scale(1.0 - 0.2 * u, 1.0 - 0.2 * u)
            p.setOpacity(play_op)
            self._draw_play(p, 0, 0)
            p.restore()
        stop_op = max(0.0, min(1.0, (u - 0.3) / 0.7))
        if stop_op > 0.01:
            p.save()
            p.translate(icon_cx, icon_cy)
            p.rotate(-45 * (1.0 - u))
            p.scale(0.8 + 0.2 * u, 0.8 + 0.2 * u)
            p.setOpacity(stop_op)
            self._stop_bars(p, 0, 0, scale=0.78, x=0)
            p.restore()

        # 2) 텍스트: PLAY_TEXT <-> STOP_TEXT 크로스페이드
        if 1.0 - u > 0.01:
            p.save()
            p.setOpacity(1.0 - u)
            p.drawText(int(text_start_x), int(baseline), PLAY_TEXT)
            p.restore()
        if u > 0.01:
            p.save()
            p.setOpacity(u)
            p.drawText(int(text_start_x), int(baseline), STOP_TEXT)
            p.restore()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.TextAntialiasing, True)
        if not self.isEnabled():
            p.setOpacity(DISABLED_OPACITY)
        pad = PADDING_H  # 16 (token, was 8)
        r = QRectF(pad, 5, max(1, self.width() - 2 * pad), self.height() - 10)
        dy = -LIFT_PLAYSTOP * self._hover + LIFT_PLAYSTOP * self._pressed
        r.translate(0, dy)
        self._draw_shadow(p, r)
        self._background(p, r)
        self._draw_content(p, r)
        if self.hasFocus():
            self._draw_focus_ring(p, r)
        p.end()

    def _draw_focus_ring(self, p, r):
        """키보드 포커스 링 (WCAG 2.1 AA — 2px dashed accent)."""
        p.save()
        p.setBrush(Qt.NoBrush)
        pen = p.pen()
        pen.setColor(QColor(FOCUS_BORDER_COLOR))      # #EC4899 (token, was #FFFFFF)
        pen.setWidth(FOCUS_BORDER_WIDTH)              # 2 (token)
        pen.setStyle(Qt.PenStyle.DashLine)            # DashedLine (token, was SolidLine)
        p.setPen(pen)
        p.drawRoundedRect(r.adjusted(1, 1, -1, -1), CORNER_RADIUS_PLAYSTOP, CORNER_RADIUS_PLAYSTOP)
        p.restore()

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
