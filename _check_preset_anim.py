"""프리셋 버튼 반짝 애니메이션 확인용 임시 스크립트."""
import os

os.environ["QT_QPA_PLATFORM"] = "offscreen"

from pathlib import Path

from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QGraphicsOpacityEffect, QPushButton

import main
from app.gui.ui_loader import load_ui

app = QApplication([])
window = load_ui(Path("assets/ui/main.ui"))
controller = main.MainController(window)
window.resize(1500, 1100)
window.show()
QTest.qWait(200)

width_spin = controller.find(main.QSpinBox, "widthSpinBox")
height_spin = controller.find(main.QSpinBox, "heightSpinBox")

for name in ("preset_1024x1024", "preset_896x1152", "preset_1152x896"):
    button = controller.find(QPushButton, name)
    button.click()
    QTest.qWait(80)
    effect = button.graphicsEffect()
    kind = type(effect).__name__ if effect is not None else "없음"
    opacity = round(effect.opacity(), 3) if effect is not None else None
    print(f"{name}: 효과={kind} | 클릭 직후 opacity={opacity}")

QTest.qWait(600)
button = controller.find(QPushButton, "preset_1152x896")
effect = button.graphicsEffect()
print("마지막 버튼 애니메이션 끝난 후 opacity:", round(effect.opacity(), 3))
# 스타일 버튼 애니메이션(래퍼 함수)도 여전히 동작하는지 확인
print("=== 스타일 버튼 애니메이션 ===")
controller.select_zanime_style("japanime")
QTest.qWait(80)
style_button = controller._zanime_style_buttons["japanime"]
style_effect = style_button.graphicsEffect()
print(
    "스타일 버튼 효과:",
    type(style_effect).__name__ if style_effect is not None else "없음",
    "| opacity:",
    round(style_effect.opacity(), 3) if style_effect is not None else None,
)
QTest.qWait(600)
print(
    "스타일 버튼 애니메이션 끝난 후 opacity:",
    round(style_effect.opacity(), 3),
)

# 기록 복원처럼 apply_preset을 코드에서 직접 호출 → 애니메이션 없어야 함
print("=== 기록 복원(코드 호출) 시 애니메이션 없음 확인 ===")
other = controller.find(QPushButton, "preset_896x1152")
other.setGraphicsEffect(None)
controller.apply_preset(896, 1152)
QTest.qWait(100)
eff = other.graphicsEffect()
print(
    "복원 호출 후 효과:",
    type(eff).__name__ if eff is not None else "없음 (정상)",
)
print("적용된 크기:", width_spin.value(), "x", height_spin.value())