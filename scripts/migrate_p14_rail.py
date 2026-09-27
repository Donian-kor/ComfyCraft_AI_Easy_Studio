# -*- coding: utf-8 -*-
"""P14: 사이드바 5버튼 + 홈/옵션 역할 분리 (기획서 v5.0).

- railOptionsBtn(옵션) 신설 — 기존 railHomeBtn이 하던 옵션 패널 토글 이관
- railHomeBtn(홈) = 패널 접기 + 채팅 화면 복귀, 선택 강조 없음
- 레일 순서: 홈/옵션/이력 / (spacer) / ?/설정  (상단 3, 하단 2 고정)
- railFrame 폭 70 -> 76px
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

UI_FILE = Path(__file__).resolve().parent.parent / "assets" / "ui" / "main.ui"

RAIL_WIDTH = 76
BTN_SIZE = 55

BTN_SPECS = [
    # (objectName, text, toolTip)
    ("railHomeBtn", "홈", "메인 채팅 화면으로"),
    ("railOptionsBtn", "옵션", "생성 옵션 패널"),
    ("railHistoryBtn", "이력", "대화 이력"),
    ("railHelpBtn", "?", "도움말"),
    ("railSettingsBtn", "설정", "설정"),
]


def _find(root, tag, name):
    for node in root.iter(tag):
        if node.get("name") == name:
            return node
    return None


def _set_prop(parent, name, value_xml):
    """property를 찾아 없으면 추가하고 값을 교체한다."""
    for prop in parent.findall("property"):
        if prop.get("name") == name:
            for child in list(prop):
                prop.remove(child)
            prop.append(ET.fromstring(value_xml))
            return
    new = ET.SubElement(parent, "property", {"name": name})
    new.append(ET.fromstring(value_xml))


def _btn_xml(name, text, tooltip):
    return ET.fromstring(
        f'<widget class="QPushButton" name="{name}">'
        f'<property name="minimumSize"><size><width>{BTN_SIZE}</width>'
        f'<height>{BTN_SIZE}</height></size></property>'
        f'<property name="maximumSize"><size><width>{BTN_SIZE}</width>'
        f'<height>{BTN_SIZE}</height></size></property>'
        f'<property name="cursor"><cursorShape>PointingHandCursor</cursorShape></property>'
        f'<property name="toolTip"><string>{tooltip}</string></property>'
        f'<property name="text"><string>{text}</string></property>'
        f"</widget>"
    )


def rebuild() -> None:
    tree = ET.parse(UI_FILE)
    root = tree.getroot()

    rail = _find(root, "widget", "railFrame")
    assert rail is not None, "railFrame 없음"
    layout = _find(rail, "layout", "railLayout")
    assert layout is not None, "railLayout 없음"

    # 1) 레일 폭 70 -> 76 (min/max 둘 다)
    _set_prop(rail, "minimumSize",
              f"<size><width>{RAIL_WIDTH}</width><height>0</height></size>")
    _set_prop(rail, "maximumSize",
              f"<size><width>{RAIL_WIDTH}</width>"
              f"<height>16777215</height></size>")

    # 2) railLayout 안의 기존 item을 전부 제거하고 5버튼 + spacer로 재구성
    for item in list(layout.findall("item")):
        layout.remove(item)
    _set_prop(layout, "spacing", "<number>6</number>")

    # 상단 3개(홈/옵션/이력) 뒤에 spacer → ?/설정 이 항상 아래로 밀린다.
    for idx, (name, text, tooltip) in enumerate(BTN_SPECS):
        item = ET.SubElement(layout, "item")
        item.append(_btn_xml(name, text, tooltip))
        if idx == 2:  # 이력 다음에 간격 삽입
            gap = ET.SubElement(layout, "item")
            gap.append(ET.fromstring(
                '<spacer name="railSpacer">'
                '<property name="orientation">'
                "<enum>Qt::Orientation::Vertical</enum></property>"
                '<property name="sizeHint" stdset="0">'
                "<size><width>0</width><height>0</height></size>"
                "</property></spacer>"))

    # 3) 목업 규칙: 홈은 강조 대상이 아니므로 accessibleDescription 명시
    home = _find(root, "widget", "railHomeBtn")
    if home is not None:
        _set_prop(home, "accessibleName",
                  "<string>홈 — 메인 채팅 화면으로</string>")
    options = _find(root, "widget", "railOptionsBtn")
    if options is not None:
        _set_prop(options, "accessibleName",
                  "<string>생성 옵션 — 옵션 패널 펼침/접힘</string>")

    tree.write(UI_FILE, encoding="UTF-8", xml_declaration=True)
    print(f"railFrame 폭 {RAIL_WIDTH}px, 버튼 {len(BTN_SPECS)}개 재구성 완료")


if __name__ == "__main__":
    rebuild()
