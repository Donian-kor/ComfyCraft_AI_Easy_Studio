# -*- coding: utf-8 -*-
"""main.py 전체 기동 검증 (offscreen): MainController 생성, 사이드바/탭/홈카드 동작 확인"""
import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PySide6.QtWidgets import QApplication, QFrame, QSplitter, QTabWidget, QPushButton

from main import MainController, load_ui, UI_FILE

app = QApplication(sys.argv)
window = load_ui(UI_FILE)
controller = MainController(window)
window.show()

results = []

def check(label, cond):
    results.append(bool(cond))
    print(f"[{'OK' if cond else 'FAIL'}] {label}")

sidebar = window.findChild(QFrame, "sidebar_frame")
tabs = window.findChild(QTabWidget, "tabWidget")

check("분할자(QSplitter) 완전 제거", window.findChild(QSplitter) is None)
check("사이드바가 레이아웃에 직접 배치됨", sidebar is not None and sidebar.parentWidget() is window.centralWidget())
check("사이드바 접힘 55px", sidebar is not None and sidebar.maximumWidth() == 55)
check("펼침 목표 210px", hasattr(controller, "sidebar_expanded_width") and controller.sidebar_expanded_width == 210)
check("접힘 목표 55px", hasattr(controller, "sidebar_collapsed_width") and controller.sidebar_collapsed_width == 55)
check("탭 8개", tabs is not None and tabs.count() == 8)

# 사이드바 호버 애니메이션 (레이아웃에서 실제 너비가 따라오는지 확인)
from PySide6.QtCore import QEvent
from PySide6.QtTest import QTest

app.processEvents()
check("초기 실제 너비 55px", sidebar.width() == 55)

controller.eventFilter(sidebar, QEvent(QEvent.Type.HoverEnter))
QTest.qWait(450)
app.processEvents()
check("호버 시 펼침(max 210)", sidebar.maximumWidth() == 210)
check("호버 시 실제 너비 확장", sidebar.width() >= 200)

controller.eventFilter(sidebar, QEvent(QEvent.Type.HoverLeave))
QTest.qWait(450)
app.processEvents()
check("호버 해제 시 실제 너비 55px", sidebar.width() == 55)

def click_and_check(btn_name, expected_index, tab_count):
    btn = window.findChild(QPushButton, btn_name)
    if btn is None:
        return False
    tabs.setCurrentIndex(tab_count - 1)  # 마지막 탭으로 보낸 뒤 클릭 테스트
    app.processEvents()
    btn.click()
    app.processEvents()
    ok = tabs.currentIndex() == expected_index
    print(f"[{'OK' if ok else 'FAIL'}] {btn_name} → 탭 {expected_index} (현재: {tabs.currentIndex()})")
    return ok

# 사이드바 버튼
checks = [
    ("homeButton", 0),
    ("comfyButton", 1),
    ("lmstudioButton", 2),
    ("settingsButton", 6),
]
for name, idx in checks:
    click_and_check(name, idx, tabs.count())

# 홈 탭 카드 버튼
for name, idx in [("startButton", 1), ("comfyCardButton", 1), ("lmCardButton", 2)]:
    click_and_check(name, idx, tabs.count())

# 탭별 주요 위젯이 실제로 해당 탭 안에 있는지 확인
page_map = {
    1: ("comfyModelCombo", "widthSpinBox", "generateButton", "facedetailerCheckBox"),
    2: ("lmModelCombo",),
    3: ("positivePromptEdit",),
    4: ("previewLabel", "saveImageButton"),
    5: ("logTextEdit", "toggleLogButton"),
    6: ("loadConfigButton", "saveConfigButton"),
    7: ("helpBrowser",),
}
for tab_idx, names in page_map.items():
    tab = tabs.widget(tab_idx)
    for name in names:
        found = False
        for ch in [tab] + list(tab.findChildren(object)):
            if getattr(ch, "objectName", lambda: "")() == name:
                found = True
                break
        check(f"탭[{tab_idx}]에 {name} 존재", found)

print("\n결과:", sum(results), "/", len(results), "성공")
if not all(results):
    sys.exit(1)
print("ALL PASS")