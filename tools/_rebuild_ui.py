# -*- coding: utf-8 -*-
"""
main.ui 재구축 스크립트

기존 main.ui 의 위젯 블록(스타일/툴팁/속성 일체 보존)을 추출해서
NEW.ui 스타일의 "사이드바 + 탭" 구조로 재조립한 새 main.ui 를 생성한다.

탭 구성(8개):
  index 0 : Home     - NEW.ui 홈 카드(hero / comfy 카드 / lm 카드 / 최근 / 시스템)
  index 1 : ComfyUI  - Comfy 연결(ComfygroupBox) + 생성옵션 + 실행 + FaceDetailer
  index 2 : LMStudio - LM 연결(lmgroupBox)
  index 3 : Prompt   - promptPanel (positive/negative/enhance)
  index 4 : Result   - resultPanel (이미지 미리보기 + 저장)
  index 5 : Log      - toggleLogButton + logGroupBox
  index 6 : Settings - 설정 불러오기/저장/기본값 + Exit
  index 7 : Help     - helpBrowser

주의사항:
  - main.py 가 find()로 참조하는 objectName 을 반드시 보존한다.
  - NEW.ui 의 comfyTab 내 progressBar/generateButton(가짜 위젯)은
    기존 위젯과 objectName 이 충돌하므로 가져오지 않는다.
"""
from __future__ import annotations

import copy
import xml.etree.ElementTree as ET

OLD = "assets/ui/main.ui"
NEWF = "assets/ui/NEW.ui"
OUT = "assets/ui/main.ui"


# ---------------------------------------------------------------- helpers
def el(tag, cls=None, name=None, **attrs):
    node = ET.Element(tag)
    if cls is not None:
        node.set("class", cls)
    if name is not None:
        node.set("name", name)
    for k, v in attrs.items():
        node.set(k, v)
    return node


def sub(parent, tag, cls=None, name=None, **attrs):
    """ET.SubElement + class/name 편의 헬퍼"""
    node = ET.SubElement(parent, tag)
    if cls is not None:
        node.set("class", cls)
    if name is not None:
        node.set("name", name)
    for k, v in attrs.items():
        node.set(k, v)
    return node


def children(parent, tag=None):
    return [c for c in parent if tag is None or c.tag == tag]


def findw(parent, name):
    """direct 자식 <widget name=...> 를 찾는다."""
    for c in children(parent, "widget"):
        if c.get("name") == name:
            return c
    raise KeyError("widget not found: " + name)


def findw_any(parent, name):
    """하위 전체(재귀)에서 <widget name=...> 를 찾는다."""
    for c in parent.iter():
        if c.tag == "widget" and c.get("name") == name:
            return c
    raise KeyError("widget not found: " + name)


def get_prop(parent, name):
    for p in children(parent, "property"):
        if p.get("name") == name:
            return p
    return None


def deep(node):
    return copy.deepcopy(node)


def squish(node):
    """해당 요소의 geometry 프로퍼티 제거 (레이아웃에 들어가므로)."""
    if node is None:
        return node
    for p in list(children(node, "property")):
        if p.get("name") == "geometry":
            node.remove(p)
    return node


# ---------------------------------------------------------------- props
def str_prop(name, text, notr=False):
    p = el("property", name=name)
    s = ET.SubElement(p, "string")
    if notr:
        s.set("notr", "true")
    s.text = text
    return p


def enum_prop(name, value):
    p = el("property", name=name)
    e = ET.SubElement(p, "enum")
    e.text = value
    return p


def num_prop(name, value):
    p = el("property", name=name)
    n = ET.SubElement(p, "number")
    n.text = str(value)
    return p


def bool_prop(name, value):
    p = el("property", name=name)
    b = ET.SubElement(p, "bool")
    b.text = "true" if value else "false"
    return p


def set_min_size(node, w, h):
    for p in list(children(node, "property")):
        if p.get("name") == "minimumSize":
            node.remove(p)
    p = el("property", name="minimumSize")
    s = ET.SubElement(p, "size")
    ET.SubElement(s, "width").text = str(w)
    ET.SubElement(s, "height").text = str(h)
    node.insert(0, p)


def set_max_size(node, w, h):
    for p in list(children(node, "property")):
        if p.get("name") == "maximumSize":
            node.remove(p)
    p = el("property", name="maximumSize")
    s = ET.SubElement(p, "size")
    ET.SubElement(s, "width").text = str(w)
    ET.SubElement(s, "height").text = str(h)
    node.insert(0, p)


def spacer_elem(name, orientation, w, h):
    sp = el("spacer", name=name)
    p = ET.SubElement(sp, "property")
    p.set("name", "orientation")
    e = ET.SubElement(p, "enum")
    e.text = orientation
    p2 = ET.SubElement(sp, "property")
    p2.set("name", "sizeHint")
    p2.set("stdset", "0")
    size = ET.SubElement(p2, "size")
    ET.SubElement(size, "width").text = str(w)
    ET.SubElement(size, "height").text = str(h)
    return sp


# ----------------------------------------------------------- page builders
def make_page(page_name, title, widget_list, stretch_last=True):
    """탭 페이지 생성. widget_list 의 각 요소는 squish 된 widget 요소."""
    page = el("widget", cls="QWidget", name=page_name)
    attr = ET.SubElement(page, "attribute")
    attr.set("name", "title")
    st = ET.SubElement(attr, "string")
    st.text = title
    layout = el("layout", cls="QVBoxLayout", name=page_name + "Layout")
    layout.append(num_prop("spacing", 10))
    page.append(layout)
    for w in widget_list:
        item = ET.SubElement(layout, "item")
        item.append(squish(deep(w)))
    if stretch_last:
        item = ET.SubElement(layout, "item")
        item.append(spacer_elem(page_name + "Spacer", "Qt::Orientation::Vertical", 20, 40))
    return page


def item_row(row_name, widgets, stretch=True):
    row = el("layout", cls="QHBoxLayout", name=row_name)
    row.append(num_prop("spacing", 10))
    for w in widgets:
        item = ET.SubElement(row, "item")
        item.append(squish(deep(w)))
    if stretch:
        item = ET.SubElement(row, "item")
        item.append(spacer_elem(row_name + "Spacer", "Qt::Orientation::Horizontal", 40, 20))
    return row


# ================================================================ EXTRACT
o = ET.parse(OLD).getroot()
wm = findw(o, "MainWindow")
mwc = findw(wm, "centralWidget")

window_title_prop = get_prop(wm, "windowTitle")
window_style_prop = get_prop(wm, "styleSheet")
window_font_prop = get_prop(wm, "font")
central_style_prop = get_prop(mwc, "styleSheet")

old_splitter = findw(mwc, "mainSplitter")
split_style_prop = get_prop(old_splitter, "styleSheet")

old_tabs = findw_any(old_splitter, "mainModeTabWidget")
tab_style_prop = get_prop(old_tabs, "styleSheet")

help_browser = findw_any(old_tabs, "helpBrowser")

comfy_group = findw_any(mwc, "ComfygroupBox")
lm_group = findw_any(mwc, "lmgroupBox")
gen_panel = findw(mwc, "generationPanel")
exec_panel = findw(mwc, "executionPanel")
face_panel = findw(mwc, "facedetailerGroupBox")
log_box = findw(mwc, "logGroupBox")
result_panel = findw(mwc, "resultPanel")
toggle_log = findw(mwc, "toggleLogButton")
cfg_row = findw(mwc, "layoutWidget0")
exit_btn = findw(mwc, "exitButton")
old_sidebar = findw(mwc, "sidebar_frame")
net_btn = findw(old_sidebar, "pushButton")

# NEW.ui 추출
n = ET.parse(NEWF).getroot()
nw = findw(n, "MainWindow")
nc = findw(nw, "centralwidget")
new_sidebar = findw_any(nc, "sidebar")
new_tabs_old = findw_any(nc, "tabWidget")
home_tab_new = findw_any(new_tabs_old, "homeTab")
# ================================================================ ASSEMBLY
ui = el("ui", version="4.0")
cls = ET.SubElement(ui, "class")
cls.text = "MainWindow"

mw = sub(ui, "widget", cls="QMainWindow", name="MainWindow")

# geometry (New 구조 + 탭이 많아 넉넉하게)
geom = ET.SubElement(mw, "property")
geom.set("name", "geometry")
gr = ET.SubElement(geom, "rect")
ET.SubElement(gr, "x").text = "0"
ET.SubElement(gr, "y").text = "0"
ET.SubElement(gr, "width").text = "1500"
ET.SubElement(gr, "height").text = "950"

set_min_size(mw, 1100, 720)
mw.append(deep(window_title_prop))
mw.append(deep(window_font_prop))
mw.append(deep(window_style_prop))

# --- centralWidget ---
central = sub(mw, "widget", cls="QWidget", name="centralWidget")
central.append(deep(central_style_prop))
main_layout = el("layout", cls="QHBoxLayout", name="mainLayout")
main_layout.append(num_prop("spacing", 0))
for m in ("leftMargin", "topMargin", "rightMargin", "bottomMargin"):
    main_layout.append(num_prop(m, 0))
central.append(main_layout)

# --- mainSplitter (objectName 보존! main.py 가 참조) ---
split_item = ET.SubElement(main_layout, "item")
split_widget = sub(split_item, "widget", cls="QSplitter", name="mainSplitter")
split_widget.append(deep(split_style_prop))
split_widget.append(enum_prop("orientation", "Qt::Orientation::Horizontal"))

# --- sidebar (NEW 의 sidebar 재사용, objectName 은 sidebar_frame 유지) ---
sb = deep(new_sidebar)
sb.set("name", "sidebar_frame")
set_min_size(sb, 210, 0)
set_max_size(sb, 210, 16777215)
sidebar_style = (
    "background-color: #14161f;\n"
    "border-right: 1px solid #262b3a;\n"
    "QPushButton { text-align: left; padding: 10px 14px; border: none; border-radius: 8px; "
    "background-color: transparent; color: #cdd2e0; font-size: 14px; }\n"
    "QPushButton:hover { background-color: #1d212c; color: #f4f5f8; }\n"
    "QPushButton:pressed { background-color: #221e3d; color: #cdc4ff; }\n"
    "QLabel { background-color: transparent; color: #9aa2b8; }\n"
)
sb.insert(0, str_prop("styleSheet", sidebar_style, notr=True))

# 사이드바 레이아웃에서 bottomSpacer 뒤에 기존 연결 상태 pushButton 삽입
sbl = None
for cld in children(sb, "layout"):
    if cld.get("name") == "sidebarLayout":
        sbl = cld
        break
if sbl is not None:
    items = children(sbl, "item")
    insert_idx = None
    for i, it in enumerate(items):
        for ch in it:
            if ch.tag == "spacer" and ch.get("name") == "bottomSpacer":
                insert_idx = i + 1
                break
    if insert_idx is not None:
        it = ET.Element("item")
        it.append(squish(deep(net_btn)))
        sbl.insert(insert_idx, it)

split_widget.append(sb)

# --- content 영역 ---
content = sub(split_widget, "widget", cls="QWidget", name="contentWidget")
cl = el("layout", cls="QVBoxLayout", name="contentLayout")
cl.append(num_prop("spacing", 12))
for m in ("leftMargin", "topMargin", "rightMargin", "bottomMargin"):
    cl.append(num_prop(m, 26 if m in ("leftMargin", "rightMargin") else 22))
content.append(cl)
ci = ET.SubElement(cl, "item")

tabs = sub(ci, "widget", cls="QTabWidget", name="tabWidget")
tabs.append(deep(tab_style_prop))
tabs.append(num_prop("currentIndex", 0))

# ============================== 페이지들 ==============================
# 페이지 0: 홈 (NEW.ui 그대로)
tabs.append(deep(home_tab_new))

# 페이지 1: ComfyUI (연결 + 생성옵션 + 실행 + FaceDetailer)
c1 = squish(deep(comfy_group))
set_min_size(c1, 351, 301)
g1 = squish(deep(gen_panel))
set_min_size(g1, 441, 251)
e1 = squish(deep(exec_panel))
f1 = squish(deep(face_panel))
set_min_size(f1, 751, 181)
tabs.append(make_page("comfyTab", "◈   ComfyUI", [c1, g1, e1, f1]))

# 페이지 2: LMStudio
l1 = squish(deep(lm_group))
set_min_size(l1, 351, 201)
tabs.append(make_page("lmstudioTab", "◆   LMStudio", [l1]))

# 페이지 3: Prompt
prompt_panel = findw(mwc, "promptPanel")
tabs.append(make_page("promptTab", "✍️   Prompt", [prompt_panel]))

# 페이지 4: Result
tabs.append(make_page("resultTab", "🖼️   Result", [result_panel]))

# 페이지 5: Log (toggleLogButton + logGroupBox)
def make_log_page():
    page = el("widget", cls="QWidget", name="logTab")
    attr = ET.SubElement(page, "attribute")
    attr.set("name", "title")
    st = ET.SubElement(attr, "string")
    st.text = "📋   Log"
    ll = ET.SubElement(page, "layout", **{"class": "QVBoxLayout", "name": "logLayout"})
    ll.append(num_prop("spacing", 10))
    li1 = ET.SubElement(ll, "item")
    li1.append(item_row("logHeaderRow", [toggle_log]))
    li2 = ET.SubElement(ll, "item")
    li2.append(squish(deep(log_box)))
    li3 = ET.SubElement(ll, "item")
    li3.append(spacer_elem("logSpacer", "Qt::Orientation::Vertical", 20, 40))
    return page

tabs.append(make_log_page())

# 페이지 6: Settings (설정 불러오기/저장/기본값 + Exit)
def make_settings_page():
    page = el("widget", cls="QWidget", name="settingsTab")
    attr = ET.SubElement(page, "attribute")
    attr.set("name", "title")
    st = ET.SubElement(attr, "string")
    st.text = "⚙️   Settings"
    sl = ET.SubElement(page, "layout", **{"class": "QVBoxLayout", "name": "settingsLayout"})
    sl.append(num_prop("spacing", 12))
    si1 = ET.SubElement(sl, "item")
    si1.append(squish(deep(cfg_row)))
    si2 = ET.SubElement(sl, "item")
    si2.append(item_row("exitRow", [exit_btn]))
    si3 = ET.SubElement(sl, "item")
    si3.append(spacer_elem("settingsSpacer", "Qt::Orientation::Vertical", 20, 40))
    return page

tabs.append(make_settings_page())

# 페이지 7: Help
tabs.append(make_page("helpTab", "❓   Help", [help_browser]))

# ============================== 저장 ==============================
ui.append(ET.Element("resources"))
ui.append(ET.Element("connections"))

ET.indent(ui, space=" ")
tree = ET.ElementTree(ui)
tree.write(OUT, encoding="utf-8", xml_declaration=True)
print("OK ->", OUT)