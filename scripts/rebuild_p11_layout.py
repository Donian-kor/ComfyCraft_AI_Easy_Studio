# -*- coding: utf-8 -*-
"""P11: main.ui 구조 재빌드 (목업 기준 3층 레이아웃).

원칙: 위젯 objectName 유지 (컨트롤러 호환). 컨테이너·레이아웃은 새로 짠다.
순서: (1) 필요 위젯 추출 → (2) 잔여 컨테이너 삭제 → (3) 신규 조립 → (4) 검증.
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

UI_FILE = Path(r"C:\Users\donian\Desktop\python\ComfyCraft_AI_Easy_Studio\assets\ui\main.ui")


def wrap(node: ET.Element) -> ET.Element:
    item = ET.Element("item")
    item.append(node)
    return item


def qlabel(name: str, text: str) -> ET.Element:
    return ET.fromstring(
        f'<widget class="QLabel" name="{name}">'
        f"<property name=\"text\"><string>{text}</string></property>"
        "</widget>")


def main() -> int:
    tree = ET.parse(str(UI_FILE))
    root = tree.getroot()

    def pmap():
        return {c: p for p in root.iter() for c in p}

    def take_widget(name: str) -> ET.Element:
        pm = pmap()
        for widget in root.iter("widget"):
            if widget.get("name") == name:
                item = pm.get(widget)
                assert item is not None and item.tag == "item", name
                pm.get(item).remove(item)
                return widget
        raise AssertionError(f"widget missing: {name}")

    def take_layout(name: str) -> ET.Element:
        pm = pmap()
        for layout in root.iter("layout"):
            if layout.get("name") == name:
                item = pm.get(layout)
                assert item is not None and item.tag == "item", name
                pm.get(item).remove(item)
                return layout
        raise AssertionError(f"layout missing: {name}")

    def drop_widget(name: str) -> None:
        try:
            take_widget(name)
        except AssertionError:
            pass

    def drop_layout(name: str) -> None:
        try:
            take_layout(name)
        except AssertionError:
            pass

    # ---- 1. 헤더 ----
    drop_widget("badgeLabel")
    drop_widget("headerDivider")
    for widget in root.iter("widget"):
        if widget.get("name") == "headerFrame":
            for prop in widget.findall("property"):
                if prop.get("name") in ("minimumSize", "maximumSize"):
                    h = prop.find("size/height")
                    if h is not None:
                        h.text = "60"
        if widget.get("name") == "newChatBtn":
            for prop in widget.findall("property"):
                if prop.get("name") == "minimumSize":
                    w = prop.find("size/width")
                    if w is not None:
                        w.text = "120"

    # ---- 2. 입력 행 확보 (구 inputRowLayout에서 추출) ----
    combo = take_widget("comfyModelCombo")
    chat_edit = take_widget("chatInputEdit")
    send_btn = take_widget("sendBtn")
    drop_widget("modelSelectLabel")
    drop_widget("chatCounterLabel")
    drop_layout("modelSelectLayout")
    drop_layout("inputRowLayout")
    for prop in chat_edit.findall("property"):
        if prop.get("name") in ("minimumSize", "maximumSize"):
            h = prop.find("size/height")
            if h is not None:
                h.text = "34"
    for prop in send_btn.findall("property"):
        if prop.get("name") in ("minimumSize", "maximumSize"):
            w = prop.find("size/width")
            h = prop.find("size/height")
            if w is not None:
                w.text = "34"
            if h is not None:
                h.text = "34"

    # ---- 3. 옵션 위젯 확보 ----
    kept_layouts = {
        "lmModelSelectLayout": take_layout("lmModelSelectLayout"),
        "presetsButtonLayout": take_layout("presetsButtonLayout"),
    }
    drop_layout("negHeaderLayout")  # 프레임 안 제목/카운터 행
    kept = {}
    for wname in [
        "widthLabel", "widthSpinBox", "heightLabel", "heightSpinBox",
        "stepsLabelTitle", "stepsSlider", "stepsValueLabel",
        "cfgLabelTitle", "cfgSlider", "cfgValueLabel",
        "seedTitleLabel", "seedSpinBox", "randomSeedButton", "lockSeedButton",
        "samplerLabel", "samplerComboBox",
        "schedulerLabel", "schedulerComboBox",
        "denoiseLabel", "denoiseSpinBox",
        "negativePromptFrame",
        "enhancePromptButton", "enhancePromptEdit",
        "positivePromptEdit",
        "facedetailerCheckBox", "facedetailerHelpBtn",
        "facedetailerPanel",
        "openOutputFolderButton",
    ]:
        kept[wname] = take_widget(wname)
    for hidden_name in ("enhancePromptEdit", "positivePromptEdit"):
        w = kept[hidden_name]
        vis = w.find("./property[@name='visible']")
        if vis is None:
            prop = ET.SubElement(w, "property", {"name": "visible"})
            ET.SubElement(prop, "bool").text = "false"
        else:
            vis.find("bool").text = "false"
    for lname in ("widthLabel", "heightLabel", "stepsLabelTitle",
                  "cfgLabelTitle", "seedTitleLabel", "samplerLabel",
                  "schedulerLabel", "denoiseLabel"):
        w = kept[lname]
        prop = ET.SubElement(w, "property", {"name": "minimumSize"})
        prop.append(ET.fromstring(
            "<size><width>64</width><height>0</height></size>"))

    # ---- 4. 잔여 구 컨테이너 삭제 ----
    for gone in ("step1Card", "step2Card", "aspectRatioLayout",
                 "dimensionContainer", "advancedSettingsFrame",
                 "enhancePromptCard", "leftContentLayout",
                 "viewerCard", "generateButton", "logGroupBox",
                 "logSectionFrame"):
        try:
            take_widget(gone)
        except AssertionError:
            pass
        try:
            take_layout(gone)
        except AssertionError:
            pass

    # ---- 4. 잔여 구 컨테이너 삭제 ----
    for gone in ("step1Card", "step2Card", "aspectRatioLayout",
                 "dimensionContainer", "advancedSettingsFrame",
                 "enhancePromptCard", "leftContentLayout",
                 "viewerCard", "generateButton", "logGroupBox",
                 "logSectionFrame"):
        try:
            take_widget(gone)
        except AssertionError:
            pass
        try:
            take_layout(gone)
        except AssertionError:
            pass

    # ---- 5. 옵션 레이아웃 조립 ----
    options = ET.Element("layout", {"class": "QVBoxLayout", "name": "optionsLayout"})
    ET.SubElement(options, "property", {"name": "spacing"}).append(
        ET.fromstring("<number>8</number>"))

    def row(*widgets):
        hbox = ET.Element("layout", {"class": "QHBoxLayout"})
        ET.SubElement(hbox, "property", {"name": "spacing"}).append(
            ET.fromstring("<number>8</number>"))
        for w in widgets:
            hbox.append(wrap(w))
        options.append(wrap(hbox))

    def cap(name, text):
        options.append(wrap(qlabel(name, text)))

    K = kept
    cap("capModel", "모델")
    options.append(wrap(qlabel("modelCurrentLabel", "현재 모델: -")))
    options.append(wrap(kept_layouts["lmModelSelectLayout"]))
    cap("capResolution", "해상도")
    options.append(wrap(kept_layouts["presetsButtonLayout"]))
    row(K["widthLabel"], K["widthSpinBox"], K["heightLabel"], K["heightSpinBox"])
    cap("capSampling", "샘플링")
    row(K["stepsLabelTitle"], K["stepsSlider"], K["stepsValueLabel"])
    row(K["cfgLabelTitle"], K["cfgSlider"], K["cfgValueLabel"])
    row(K["seedTitleLabel"], K["seedSpinBox"], K["randomSeedButton"],
        K["lockSeedButton"])
    row(K["samplerLabel"], K["samplerComboBox"])
    row(K["schedulerLabel"], K["schedulerComboBox"])
    row(K["denoiseLabel"], K["denoiseSpinBox"])
    cap("capPrompt", "프롬프트")
    options.append(wrap(K["negativePromptFrame"]))
    options.append(wrap(K["enhancePromptButton"]))
    options.append(wrap(K["enhancePromptEdit"]))
    options.append(wrap(K["positivePromptEdit"]))
    cap("capFace", "FaceDetailer")
    row(K["facedetailerCheckBox"], K["facedetailerHelpBtn"])
    options.append(wrap(K["facedetailerPanel"]))
    options.append(wrap(K["openOutputFolderButton"]))

    left_widget = None
    for widget in root.iter("widget"):
        if widget.get("name") == "leftContentWidget":
            left_widget = widget
    assert left_widget is not None
    for child in list(left_widget):
        left_widget.remove(child)
    left_widget.append(options)

    for widget in root.iter("widget"):
        if widget.get("name") == "leftScrollArea":
            for prop in widget.findall("property"):
                if prop.get("name") == "maximumSize":
                    w = prop.find("size/width")
                    if w is not None:
                        w.text = "290"
            vis = widget.find("./property[@name='visible']")
            if vis is None:
                prop = ET.SubElement(widget, "property", {"name": "visible"})
                ET.SubElement(prop, "bool").text = "false"
            else:
                vis.find("bool").text = "false"

    # ---- 6. 채팅: 여백 18 (에러는 별도 배너 없이 채팅 메시지로 표시) ----
    for layout in root.iter("layout"):
        if layout.get("name") == "chatLayout":
            for tag in ("leftMargin", "topMargin", "rightMargin", "bottomMargin"):
                if layout.find(f"./property[@name='{tag}']") is None:
                    prop = ET.SubElement(layout, "property", {"name": tag})
                    ET.SubElement(prop, "number").text = "18"
    # (에러 배너 위젯 없음 — 오류는 채팅 AI 메시지로 표시)

    # ---- 7. 입력 프레임 (그리드 row2) ----
    input_frame = ET.fromstring(
        """<widget class="QFrame" name="inputFrame">
        <property name="frameShape"><enum>QFrame::Shape::NoFrame</enum></property>
        <property name="minimumSize"><size><width>0</width><height>58</height></size></property>
        <property name="maximumSize"><size><width>16777215</width><height>58</height></size></property>
        <layout class="QHBoxLayout" name="inputRowLayout">
        <property name="spacing"><number>8</number></property>
        <property name="leftMargin"><number>14</number></property>
        <property name="topMargin"><number>12</number></property>
        <property name="rightMargin"><number>14</number></property>
        <property name="bottomMargin"><number>12</number></property>
        </layout></widget>""")
    new_input_row = None
    for layout in input_frame.iter("layout"):
        if layout.get("name") == "inputRowLayout":
            new_input_row = layout
    assert new_input_row is not None
    new_input_row.append(wrap(combo))
    new_input_row.append(wrap(chat_edit))
    new_input_row.append(wrap(send_btn))
    grid = None
    for layout in root.iter("layout"):
        if layout.get("name") == "gridLayout_3":
            grid = layout
    assert grid is not None
    row_item = ET.Element("item", {"row": "2", "column": "0"})
    row_item.append(input_frame)
    grid.append(row_item)

    # ---- 8. studio spacing 0 ----
    for layout in root.iter("layout"):
        if layout.get("name") == "studioLayout":
            for prop in layout.findall("property"):
                if prop.get("name") == "spacing":
                    num = prop.find("number")
                    if num is not None:
                        num.text = "0"

    # ---- 9. 검증 ----
    names = [w.get("name") for w in root.iter("widget")]
    counts = Counter(names)
    layouts_present = {l.get("name") for l in root.iter("layout")}
    for name in ("headerFrame", "railFrame", "leftScrollArea",
                 "leftContentWidget", "chatFrame", "chatScrollArea",
                 "chatContentWidget", "inputFrame",
                 "modelCurrentLabel", "comfyModelCombo", "chatInputEdit",
                 "sendBtn", "openOutputFolderButton", "enhancePromptButton",
                 "enhancePromptEdit", "positivePromptEdit",
                 "negativePromptFrame", "negativePromptEdit",
                 "facedetailerCheckBox", "facedetailerHelpBtn",
                 "facedetailerPanel", "themeComboBox", "newChatBtn",
                 "comfyStatusBtn", "lmStatusBtn", "lmModelCombo",
                 "lmModelSelectLabel", "widthSpinBox", "heightSpinBox",
                 "stepsSlider", "cfgSlider", "seedSpinBox",
                 "samplerComboBox", "schedulerComboBox", "denoiseSpinBox",
                 "randomSeedButton", "lockSeedButton",
                 "preset_1024x1024", "preset_896x1152", "preset_1152x896"):
        assert counts.get(name, 0) == 1, f"{name}: {counts.get(name, 0)}"
    for gone in ("viewerCard", "generateButton", "logGroupBox", "logTextEdit",
                 "thumbBtn_0", "saveImageButton", "resetButton",
                 "copyImageButton", "toggleLogButton", "previewLabel",
                 "progressBar", "progressStatusLabel", "progressPercentLabel",
                 "elapsedLabel", "step1Card", "step2Card",
                 "modelSelectLabel", "chatCounterLabel", "badgeLabel",
                 "headerDivider", "helpButton", "settingsButton",
                 "positivePromptCounterLabel", "negativePromptCounterLabel",
                 "enhancePromptCounterLabel", "copyPromptButton",
                 "modelProfileNoticeLabel", "errorBannerLabel"):
        assert counts.get(gone, 0) == 0, f"still present: {gone}"
    for gone_layout in ("leftContentLayout", "step2Layout",
                        "modelSelectLayout", "aspectRatioLayout",
                        "dimensionContainer", "dimensionLayout",
                        "advancedSettingsFrame", "step1Layout",
                        "enhancePromptCard", "negHeaderLayout", "rightContainer",
                        "logSectionFrame", "logSectionLayout"):
        assert gone_layout not in layouts_present, f"layout left: {gone_layout}"
    for must_layout in ("optionsLayout", "inputRowLayout", "chatLayout",
                        "chatMainLayout", "studioLayout", "gridLayout_3",
                        "headerLayout", "railLayout"):
        assert must_layout in layouts_present, f"layout missing: {must_layout}"

    try:
        ET.indent(tree, space=" ")
    except Exception:
        pass
    tree.write(str(UI_FILE), encoding="utf-8", xml_declaration=True)
    print(f"P11 OK: widgets={len(names)} rebuilt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
