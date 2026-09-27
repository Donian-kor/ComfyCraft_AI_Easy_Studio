# -*- coding: utf-8 -*-
"""P8: 설정 다이얼로그 탭화 (AI 서버 + 이미지 모델) + 수동 프로필 위젯.

- 기존 comfyGroupBox/lmGroupBox/하단 버튼은 그대로 이동 (로직 변경 없음).
- 이미지 모델 탭: 자동 목록(읽기 전용) + 수동 프로필 편집기 + 검증 라벨.
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
UI_FILE = BASE_DIR / "assets" / "ui" / "settings_dialog.ui"

REQUIRED_ONCE = [
    "settingsTabWidget", "tabAiServer", "tabModel",
    "comfyGroupBox", "lmGroupBox",
    "dlgComfyUrlEdit", "dlgModelPathEdit", "dlgLmUrlEdit",
    "dlgComfyCheckBtn", "dlgLmCheckBtn", "dlgBrowseBtn",
    "dlgLoadConfigBtn", "dlgResetDefaultsBtn", "dlgSaveCloseBtn",
    "profileAutoList", "profileNameEdit", "profilePatternsEdit",
    "profileWorkflowCombo", "profileStepsSpin", "profileCfgSpin",
    "profileSamplerCombo", "profileSchedulerCombo",
    "profileClip1Edit", "profileClip2Edit", "profileVaeEdit",
    "profileFileCombo", "profileDeleteBtn", "profileValidateLabel",
    "profileSaveBtn",
]


def _label_row(label_text: str, widget_xml: str) -> str:
    return (
        '<item><layout class="QHBoxLayout">'
        '<property name="spacing"><number>8</number></property>'
        f"<item><widget class=\"QLabel\"><property name=\"text\">"
        f"<string>{label_text}</string></property></widget></item>"
        f"<item>{widget_xml}</item>"
        "</layout></item>"
    )


def _spin(name: str, minimum: str, maximum: str, value: str,
          single_step: str = "1") -> str:
    return (
        f'<widget class="QSpinBox" name="{name}">'
        f"<property name=\"minimum\"><number>{minimum}</number></property>"
        f"<property name=\"maximum\"><number>{maximum}</number></property>"
        f"<property name=\"value\"><number>{value}</number></property>"
        f"<property name=\"singleStep\"><number>{single_step}</number></property>"
        "</widget>"
    )


def _double_spin(name: str, minimum: str, maximum: str, value: str,
                 single_step: str = "0.1") -> str:
    return (
        f'<widget class="QDoubleSpinBox" name="{name}">'
        f"<property name=\"minimum\"><double>{minimum}</double></property>"
        f"<property name=\"maximum\"><double>{maximum}</double></property>"
        f"<property name=\"value\"><double>{value}</double></property>"
        f"<property name=\"singleStep\"><double>{single_step}</double></property>"
        "</widget>"
    )


def _combo(name: str, items: list) -> str:
    parts = [f'<widget class="QComboBox" name="{name}">']
    for text in items:
        parts.append(
            f"<item><property name=\"text\"><string>{text}</string></property></item>")
    parts.append("</widget>")
    return "".join(parts)


def _button(name: str, text: str) -> str:
    return (
        f'<widget class="QPushButton" name="{name}">'
        f"<property name=\"cursor\"><cursorShape>PointingHandCursor</cursorShape></property>"
        f"<property name=\"text\"><string>{text}</string></property>"
        "</widget>"
    )


def _line_edit(name: str, placeholder: str = "") -> str:
    ph = (f"<property name=\"placeholderText\"><string>{placeholder}</string></property>"
          if placeholder else "")
    return f'<widget class="QLineEdit" name="{name}">{ph}</widget>'


def main() -> int:
    tree = ET.parse(str(UI_FILE))
    root = tree.getroot()

    dialog_layout = None
    for layout in root.iter("layout"):
        if layout.get("name") == "dialogLayout":
            dialog_layout = layout
    assert dialog_layout is not None

    # 기존 항목 분류
    group_items = []
    other_items = []
    for item in list(dialog_layout):
        widget = item.find("widget")
        layout = item.find("layout")
        name = ""
        if widget is not None:
            name = widget.get("name", "")
        elif layout is not None:
            name = layout.get("name", "")
        if name in ("comfyGroupBox", "lmGroupBox"):
            group_items.append(item)
        else:
            other_items.append(item)
    assert len(group_items) == 2, f"groups: {len(group_items)}"
    for item in group_items:
        dialog_layout.remove(item)

    # 탭 위젯 생성
    tabs = ET.fromstring(
        """<item><widget class="QTabWidget" name="settingsTabWidget">
        <property name="currentIndex"><number>0</number></property>
        <widget class="QWidget" name="tabAiServer">
        <attribute name="title"><string>AI 서버</string></attribute>
        <layout class="QVBoxLayout" name="tabAiServerLayout"/>
        </widget>
        <widget class="QWidget" name="tabModel">
        <attribute name="title"><string>이미지 모델</string></attribute>
        <layout class="QVBoxLayout" name="tabModelLayout"/>
        </widget>
        </widget></item>""")
    ai_layout = None
    model_layout = None
    for layout in tabs.iter("layout"):
        if layout.get("name") == "tabAiServerLayout":
            ai_layout = layout
        elif layout.get("name") == "tabModelLayout":
            model_layout = layout
    assert ai_layout is not None and model_layout is not None
    for item in group_items:
        ai_layout.append(item)

    # 이미지 모델 탭 내용
    model_layout.append(ET.fromstring(
        '<item><widget class="QLabel" name="profileAutoLabel">'
        '<property name="text"><string>자동 판별 모델 (읽기 전용)</string>'
        "</property></widget></item>"))
    model_layout.append(ET.fromstring(
        '<item><widget class="QListWidget" name="profileAutoList">'
        '<property name="minimumSize"><size><width>0</width><height>90</height></size></property>'
        '<property name="maximumSize"><size><width>16777215</width><height>140</height></size></property>'
        "</widget></item>"))
    model_layout.append(ET.fromstring(
        '<item><widget class="QLabel" name="profileManualLabel">'
        '<property name="text"><string>수동 프로필 (고급 · 신규/예외 모델용)</string>'
        "</property></widget></item>"))
    model_layout.append(ET.fromstring(_label_row(
        "프로필명", _line_edit("profileNameEdit", "예: my-model"))))
    model_layout.append(ET.fromstring(_label_row(
        "매칭 패턴",
        _line_edit("profilePatternsEdit", "파일명 일부, 쉼표 구분"))))
    model_layout.append(ET.fromstring(_label_row(
        "워크플로우 종류",
        _combo("profileWorkflowCombo",
               ["checkpoint", "gguf", "flux_gguf", "zimage"]))))
    model_layout.append(ET.fromstring(_label_row(
        "Steps", _spin("profileStepsSpin", "1", "200", "20"))))
    model_layout.append(ET.fromstring(_label_row(
        "CFG", _double_spin("profileCfgSpin", "0.1", "30.0", "7.0"))))
    model_layout.append(ET.fromstring(_label_row(
        "샘플러",
        _combo("profileSamplerCombo",
               ["euler", "dpmpp_2m", "dpmpp_2m_sde", "euler_ancestral",
                "lcm", "ddim"]))))
    model_layout.append(ET.fromstring(_label_row(
        "스케줄러",
        _combo("profileSchedulerCombo",
               ["normal", "karras", "exponential", "simple"]))))
    model_layout.append(ET.fromstring(_label_row(
        "CLIP 1", _line_edit("profileClip1Edit", "선택 사항"))))
    model_layout.append(ET.fromstring(_label_row(
        "CLIP 2", _line_edit("profileClip2Edit", "선택 사항"))))
    model_layout.append(ET.fromstring(_label_row(
        "VAE", _line_edit("profileVaeEdit", "선택 사항"))))
    model_layout.append(ET.fromstring(
        '<item><layout class="QHBoxLayout">'
        '<property name="spacing"><number>8</number></property>'
        + _combo("profileFileCombo", [])
        + "<item>" + _button("profileDeleteBtn", "프로필 삭제") + "</item>"
        + "</layout></item>"))
    model_layout.append(ET.fromstring(
        '<item><widget class="QLabel" name="profileValidateLabel">'
        '<property name="text"><string/></property>'
        '<property name="wordWrap"><bool>true</bool></property>'
        "</widget></item>"))
    model_layout.append(ET.fromstring(
        "<item>" + _button("profileSaveBtn", "모델 정보 저장") + "</item>"))

    dialog_layout.insert(0, tabs)

    # 검증
    names = [w.get("name") for w in root.iter("widget")]
    counts = Counter(names)
    for name in REQUIRED_ONCE:
        assert counts.get(name, 0) == 1, f"{name}: {counts.get(name, 0)}"

    try:
        ET.indent(tree, space=" ")
    except Exception:
        pass
    tree.write(str(UI_FILE), encoding="utf-8", xml_declaration=True)
    print(f"P8 OK: widgets={len(names)} settings tabbed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
