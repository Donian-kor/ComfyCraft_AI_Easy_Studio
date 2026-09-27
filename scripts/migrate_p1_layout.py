# -*- coding: utf-8 -*-
"""P1: main.ui 레이아웃 재배치 (채팅형 껍데기).

- 헤더 60px + helpButton/settingsButton 제거 + newChatBtn 추가
- 레일(railHomeBtn/railHistoryBtn/railHelpBtn/railSettingsBtn) 신설
- step1/step2 카드 통째로 옵션 스크롤에 유지, modelSelectLayout만 입력 행으로 이동
- viewerCard/generateButton/logGroupBox를 옵션 스크롤 하단으로 이동
- historyCard(thumbBtn_*) 삭제 (기획서: 채팅 스크롤백으로 대체)
- errorBannerLabel 중복 해소 (1개만 유지)
- 채팅 컨테이너(chatScrollArea) + 입력 행(chatInputEdit/sendBtn) 신설
- 위젯 objectName은 유지하므로 컨트롤러 로직 변경 없음
"""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
UI_FILE = BASE_DIR / "assets" / "ui" / "main.ui"

REQUIRED_ONCE = [
    "themeComboBox", "comfyStatusBtn", "lmStatusBtn", "newChatBtn",
    "railHomeBtn", "railHistoryBtn", "railHelpBtn", "railSettingsBtn",
    "chatScrollArea", "chatContentWidget",
    "chatInputEdit", "sendBtn", "chatFrame",
    "comfyModelCombo", "positivePromptEdit", "negativePromptEdit",
    "enhancePromptEdit", "lmModelCombo", "samplerComboBox", "seedSpinBox",
    "enhancePromptButton", "resetButton", "openOutputFolderButton",
    "saveImageButton", "logTextEdit", "progressBar", "progressStatusLabel",
    "progressPercentLabel", "elapsedLabel", "previewLabel", "generateButton",
    "toggleLogButton", "copyImageButton", "copyPromptButton",
    "randomSeedButton", "lockSeedButton", "logGroupBox", "errorBannerLabel",
    "step1Card", "step2Card", "viewerCard",
]
FORBIDDEN = ["helpButton", "settingsButton", "historyCard",
             "rightContainer", "logSectionFrame"]
LAYOUT_REQUIRED_ONCE = [
    "chatLayout", "chatMainLayout", "inputRowLayout",
    "railLayout", "modelSelectLayout",
]


def build_parent_map(root):
    return {child: parent for parent in root.iter() for child in parent}


def find_item_holding(root, parent_map, widget_name):
    """widget_name 위젯을 직접 자식으로 가진 <item>과 그 부모를 반환."""
    for widget in root.iter("widget"):
        if widget.get("name") == widget_name:
            item = parent_map.get(widget)
            assert item is not None and item.tag == "item", widget_name
            return item, parent_map.get(item)
    raise AssertionError(f"widget not found: {widget_name}")


def find_item_holding_layout(root, parent_map, layout_name):
    for layout in root.iter("layout"):
        if layout.get("name") == layout_name:
            item = parent_map.get(layout)
            assert item is not None and item.tag == "item", layout_name
            return item, parent_map.get(item)
    raise AssertionError(f"layout not found: {layout_name}")


def make_button(name, text, tooltip, size=38):
    widget = ET.Element("widget", {"class": "QPushButton", "name": name})
    ET.SubElement(widget, "property", {"name": "minimumSize"})
    widget[-1].append(ET.fromstring(
        f"<size><width>{size}</width><height>{size}</height></size>"))
    ET.SubElement(widget, "property", {"name": "maximumSize"})
    widget[-1].append(ET.fromstring(
        f"<size><width>{size}</width><height>{size}</height></size>"))
    ET.SubElement(widget, "property", {"name": "cursor"})
    widget[-1].append(ET.fromstring(
        "<cursorShape>PointingHandCursor</cursorShape>"))
    ET.SubElement(widget, "property", {"name": "toolTip"})
    widget[-1].append(ET.fromstring(f"<string>{tooltip}</string>"))
    ET.SubElement(widget, "property", {"name": "text"})
    widget[-1].append(ET.fromstring(f"<string>{text}</string>"))
    item = ET.Element("item")
    item.append(widget)
    return item


def main() -> int:
    tree = ET.parse(str(UI_FILE))
    root = tree.getroot()

    # 1. 헤더 60px
    header = None
    for widget in root.iter("widget"):
        if widget.get("name") == "headerFrame":
            header = widget
    assert header is not None
    for prop in header.findall("property"):
        size = prop.find("size/height")
        if size is not None and prop.find("size/width") is not None:
            if size.text == "50":
                size.text = "60"

    parent_map = build_parent_map(root)

    # 2. 헤더 버튼 제거 + newChatBtn 추가 (appTitle 뒤)
    header_layout = None
    for layout in root.iter("layout"):
        if layout.get("name") == "headerLayout":
            header_layout = layout
    assert header_layout is not None
    app_title_idx = None
    remove_items = []
    for idx, item in enumerate(list(header_layout)):
        widget = item.find("widget")
        if widget is not None:
            if widget.get("name") == "appTitle":
                app_title_idx = idx
            if widget.get("name") in ("helpButton", "settingsButton"):
                remove_items.append(item)
    assert app_title_idx is not None, "appTitle missing"
    for item in remove_items:
        header_layout.remove(item)
    new_chat_item = make_button("newChatBtn", "＋ 새 대화", "새 대화를 시작합니다", size=30)
    new_chat_item.find("widget").attrib["class"] = "QPushButton"
    # 높이만 30, 너비는 내용에 맞춤 (maximumSize 제거)
    for prop in list(new_chat_item.find("widget")):
        ms = prop.find("size/width")
        if prop.get("name") == "maximumSize":
            new_chat_item.find("widget").remove(prop)
    # minimumSize 너비 0 유지
    header_layout.insert(app_title_idx + 1, new_chat_item)

    parent_map = build_parent_map(root)

    # 3. errorBannerLabel 중복 해소 (두 번째 제거)
    banners = [w for w in root.iter("widget")
               if w.get("name") == "errorBannerLabel"]
    assert len(banners) == 2, f"expected 2 banners, got {len(banners)}"
    parent_map = build_parent_map(root)
    second_item = parent_map.get(banners[1])
    assert second_item is not None and second_item.tag == "item"
    parent_map.get(second_item).remove(second_item)

    # 4. historyCard 삭제 (thumbBtn_* 포함, 기획서: 스크롤백으로 대체)
    parent_map = build_parent_map(root)
    hist_item, hist_parent = find_item_holding(root, parent_map, "historyCard")
    # historyCard는 widget이므로 그 부모 item을 제거
    hist_parent.remove(hist_item)

    # 5. modelSelectLayout을 step2Card에서 분리 (입력 행으로 이동 예정)
    parent_map = build_parent_map(root)
    model_item, _ = find_item_holding_layout(root, parent_map, "modelSelectLayout")
    model_parent = parent_map.get(model_item)
    model_parent.remove(model_item)

    # 6. viewerCard / generateButton / logGroupBox를 옵션 스크롤로 이동
    parent_map = build_parent_map(root)
    left_layout = None
    for layout in root.iter("layout"):
        if layout.get("name") == "leftContentLayout":
            left_layout = layout
    assert left_layout is not None
    for wname in ("viewerCard", "generateButton", "logGroupBox"):
        parent_map = build_parent_map(root)
        item, parent = find_item_holding(root, parent_map, wname)
        parent.remove(item)
        left_layout.append(item)

    # 7. logSectionFrame(빈 프레임) + rightContainer(껍데기) 제거
    parent_map = build_parent_map(root)
    for wname in ("logSectionFrame", "rightContainer"):
        item, parent = find_item_holding(root, parent_map, wname)
        parent.remove(item)

    # 8. leftScrollArea 너비 제한 (옵션 패널 340px)
    for widget in root.iter("widget"):
        if widget.get("name") == "leftScrollArea":
            prop = ET.SubElement(widget, "property", {"name": "maximumSize"})
            prop.append(ET.fromstring(
                "<size><width>340</width><height>16777215</height></size>"))

    # 9. 레일 + 채팅 프레임 신설 후 studioLayout에 배치 [rail, options, chat]
    parent_map = build_parent_map(root)
    studio = None
    for layout in root.iter("layout"):
        if layout.get("name") == "studioLayout":
            studio = layout
    assert studio is not None

    rail = ET.fromstring(
        """<item><widget class="QFrame" name="railFrame">
        <property name="minimumSize"><size><width>55</width><height>0</height></size></property>
        <property name="maximumSize"><size><width>55</width><height>16777215</height></size></property>
        <property name="frameShape"><enum>QFrame::Shape::NoFrame</enum></property>
        <layout class="QVBoxLayout" name="railLayout">
        <property name="spacing"><number>6</number></property>
        </layout></widget></item>""")
    rail_layout = rail.find("widget").find("layout")
    for name, text, tip in (("railHomeBtn", "⌂", "홈 (생성 옵션 패널)"),
                            ("railHistoryBtn", "◷", "대화 이력 (P6에서 제공)"),
                            ("railHelpBtn", "?", "도움말"),
                            ("railSettingsBtn", "⚙", "설정")):
        rail_layout.append(make_button(name, text, tip))
    # 하단 여백 스프레서
    rail_layout.append(ET.fromstring(
        """<item><spacer name="railSpacer">
        <property name="orientation"><enum>Qt::Orientation::Vertical</enum></property>
        <property name="sizeHint" stdset="0"><size><width>0</width><height>0</height></size></property>
        </spacer></item>"""))

    chat = ET.fromstring(
        """<item><widget class="QFrame" name="chatFrame">
        <property name="frameShape"><enum>QFrame::Shape::NoFrame</enum></property>
        <property name="sizePolicy"><sizepolicy hsizetype="Expanding" vsizetype="Expanding">
        <horstretch>1</horstretch><verstretch>0</verstretch></sizepolicy></property>
        <layout class="QVBoxLayout" name="chatMainLayout">
        <property name="spacing"><number>8</number></property>
        <item><widget class="QScrollArea" name="chatScrollArea">
        <property name="frameShape"><enum>QFrame::Shape::NoFrame</enum></property>
        <property name="widgetResizable"><bool>true</bool></property>
        <property name="horizontalScrollBarPolicy"><enum>Qt::ScrollBarPolicy::ScrollBarAlwaysOff</enum></property>
        <widget class="QWidget" name="chatContentWidget">
        <layout class="QVBoxLayout" name="chatLayout">
        <property name="spacing"><number>12</number></property>
        </layout></widget></widget></item>
        <item><layout class="QHBoxLayout" name="inputRowLayout">
        <property name="spacing"><number>8</number></property>
        </layout></item>
        </layout></widget></item>""")
    chat_layout_el = None
    input_row = None
    for layout in chat.iter("layout"):
        if layout.get("name") == "chatLayout":
            chat_layout_el = layout
        if layout.get("name") == "inputRowLayout":
            input_row = layout
    assert chat_layout_el is not None and input_row is not None
    # 채팅 메시지 상단 정렬용 스프레서
    chat_layout_el.append(ET.fromstring(
        """<item><spacer name="chatSpacer">
        <property name="orientation"><enum>Qt::Orientation::Vertical</enum></property>
        <property name="sizeHint" stdset="0"><size><width>0</width><height>0</height></size></property>
        </spacer></item>"""))
    # 입력 행: modelSelectLayout + chatInputEdit + sendBtn
    input_row.append(model_item)
    chat_input = ET.fromstring(
        """<item><widget class="QPlainTextEdit" name="chatInputEdit">
        <property name="minimumSize"><size><width>0</width><height>80</height></size></property>
        <property name="maximumSize"><size><width>16777215</width><height>80</height></size></property>
        <property name="placeholderText"><string>메시지를 입력하세요... (P2에서 전송 연결)</string></property>
        </widget></item>""")
    input_row.append(chat_input)
    input_row.append(make_button("sendBtn", "➤", "이미지 생성하기 (P2에서 연결)", size=48))

    studio.insert(0, rail)
    studio.append(chat)

    # 10. 검증
    names = [w.get("name") for w in root.iter("widget")]
    from collections import Counter
    counts = Counter(names)
    for name in REQUIRED_ONCE:
        assert counts.get(name, 0) == 1, f"{name}: {counts.get(name, 0)}"
    layout_counts = Counter(
        layout.get("name") for layout in root.iter("layout"))
    for name in LAYOUT_REQUIRED_ONCE:
        assert layout_counts.get(name, 0) == 1, f"layout {name}: {layout_counts.get(name, 0)}"
    for name in FORBIDDEN:
        assert counts.get(name, 0) == 0, f"forbidden present: {name}"

    try:
        ET.indent(tree, space=" ")
    except Exception:
        pass
    tree.write(str(UI_FILE), encoding="utf-8", xml_declaration=True)
    print(f"P1 OK: widgets={len(names)} rail/chat/input relocated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
