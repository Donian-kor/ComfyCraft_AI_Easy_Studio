# -*- coding: utf-8 -*-
"""P11: 설정 다이얼로그에 로그 탭 추가."""
import xml.etree.ElementTree as ET
from pathlib import Path

UI_FILE = Path(r"C:\Users\donian\Desktop\python\ComfyCraft_AI_Easy_Studio\assets\ui\settings_dialog.ui")

tree = ET.parse(str(UI_FILE))
root = tree.getroot()

tabs = None
for w in root.iter("widget"):
    if w.get("name") == "settingsTabWidget":
        tabs = w
assert tabs is not None
assert not any(
    w.get("name") == "tabLog" for w in tabs.iter("widget")), "already added"

page = ET.fromstring(
    """<widget class="QWidget" name="tabLog">
    <attribute name="title"><string>로그</string></attribute>
    <layout class="QVBoxLayout" name="tabLogLayout">
    <property name="spacing"><number>8</number></property>
    <item><widget class="QLabel" name="logTabTitle">
    <property name="text"><string>실행 로그 (읽기 전용, 최대 5000줄)</string></property>
    </widget></item>
    <item><widget class="QTextEdit" name="logTabEdit">
    <property name="readOnly"><bool>true</bool></property>
    </widget></item>
    <item><layout class="QHBoxLayout" name="logTabButtons">
    <property name="spacing"><number>8</number></property>
    <item><widget class="QPushButton" name="logClearBtn">
    <property name="text"><string>로그 초기화</string></property>
    </widget></item>
    <item><widget class="QPushButton" name="logSaveBtn">
    <property name="text"><string>파일로 저장</string></property>
    </widget></item>
    <item><widget class="QPushButton" name="logCopyBtn">
    <property name="text"><string>전체 복사</string></property>
    </widget></item>
    </layout></item>
    </layout></widget>""")
tabs.append(page)

names = [w.get("name") for w in root.iter("widget")]
from collections import Counter
counts = Counter(names)
for name in ("tabLog", "logTabEdit", "logClearBtn", "logSaveBtn", "logCopyBtn"):
    assert counts.get(name, 0) == 1, f"{name}: {counts.get(name, 0)}"

try:
    ET.indent(tree, space=" ")
except Exception:
    pass
tree.write(str(UI_FILE), encoding="utf-8", xml_declaration=True)
print("P11 settings log tab OK")
