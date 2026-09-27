# -*- coding: utf-8 -*-
"""P2: input row counter label + placeholder update."""
import xml.etree.ElementTree as ET
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
UI_FILE = BASE / "assets" / "ui" / "main.ui"

tree = ET.parse(str(UI_FILE))
root = tree.getroot()

# placeholder 교체
for w in root.iter("widget"):
    if w.get("name") == "chatInputEdit":
        for prop in w.findall("property"):
            if prop.get("name") == "placeholderText":
                s = prop.find("string")
                assert s is not None
                s.text = "메시지를 입력하세요... 예: 이쁘고 귀여운 고양이 3마리 그려줘"

# inputRowLayout에서 chatInputEdit item 다음에 카운터 라벨 삽입
for layout in root.iter("layout"):
    if layout.get("name") == "inputRowLayout":
        items = list(layout)
        idx = None
        for i, item in enumerate(items):
            w = item.find("widget")
            if w is not None and w.get("name") == "chatInputEdit":
                idx = i
        assert idx is not None
        assert not any(
            (it.find("widget") is not None
             and it.find("widget").get("name") == "chatCounterLabel")
            for it in items
        ), "already added"
        label_item = ET.fromstring(
            '<item><widget class="QLabel" name="chatCounterLabel">'
            '<property name="text"><string>0 / 5000</string></property>'
            "</widget></item>"
        )
        layout.insert(idx + 1, label_item)

names = [w.get("name") for w in root.iter("widget")]
assert names.count("chatCounterLabel") == 1
try:
    ET.indent(tree, space=" ")
except Exception:
    pass
tree.write(str(UI_FILE), encoding="utf-8", xml_declaration=True)
print("P2 ui OK")
