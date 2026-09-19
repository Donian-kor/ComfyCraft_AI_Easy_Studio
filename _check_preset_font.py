"""프리셋 버튼 3개 글꼴/스타일 비교용 임시 확인 스크립트.

목적:
- 정사각 프리셋(preset_1024x1024)만 처음 실행 시 굵게 안 보이는지 원인 좁히기
- 글꼴 weight / bold / 스타일시트 / 텍스트 구성 비교
"""
import os

os.environ["QT_QPA_PLATFORM"] = "offscreen"

from pathlib import Path

from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QPushButton, QFont

import main
from app.gui.ui_loader import load_ui

app = QApplication([])
window = load_ui(Path("assets/ui/main.ui"))
controller = main.MainController(window)
window.resize(1500, 1100)
window.show()
QTest.qWait(250)

theme = main.load_theme_choice()
print("현재 테마:", theme)
print("=" * 60)

for name in ("preset_1024x1024", "preset_896x1152", "preset_1152x896"):
    btn = controller.find(QPushButton, name)
    if btn is None:
        print(f"[{name}] 버튼 없음")
        continue

    font = btn.font()
    style = btn.styleSheet()
    print(f"\n[{name}]")
    print("  font.bold()     :", font.bold())
    print("  font.weight()   :", font.weight())
    print("  font.weightName :", QFont.Weight(font.weight()).name)
    print("  font.family     :", font.family())
    print("  btn.text()      :", repr(btn.text()))
    print("  스타일시트      :", (style if style else "(없음)"))
    # 자식 위젯(라벨/텍스트) 정보도 확인 가능한 경우 같이 보기
    try:
        children = [c.objectName() or type(c).__name__ for c in btn.findChildren(QPushButton)]
        print("  자식 QPushButton:", children)
    except Exception as exc:
        print("  자식 확인 예외:", exc)