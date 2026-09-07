"""UI 파일들의 위젯 목록과 스타일시트 비교"""
import sys
import xml.etree.ElementTree as ET

def get_widgets(path):
    tree = ET.parse(path)
    root = tree.getroot()
    widgets = []
    styled = set()
    def walk(elem):
        for child in elem:
            if child.tag in ("widget", "layout"):
                name = child.get("name", "?")
                class_name = child.get("class", "?")
                has_style = False
                for prop in child.findall("property"):
                    if prop.get("name") == "styleSheet":
                        has_style = True
                widgets.append((class_name, name))
                if has_style:
                    styled.add(name)
                walk(child)
    walk(root)
    return widgets, styled

files = [
    r"assets\ui\main.ui",
    r"assets\ui\main-백업.ui",
    r"assets\ui\main_sidebar_backup.ui",
    r"assets\ui\NEW.ui",
]

all_w = {}
all_s = {}
for f in files:
    w, s = get_widgets(f)
    all_w[f] = set(w)
    all_s[f] = s
    print(f"{f}: 위젯 {len(w)}개, 스타일시트 {len(s)}개")

print()
base = files[0]
for f in files[1:]:
    only_main = all_w[base] - all_w[f]
    only_other = all_w[f] - all_w[base]
    print(f"--- {f} 비교 ---")
    if only_main:
        print(f"  main에만 있음: {sorted(only_main)[:20]}")
    if only_other:
        print(f"  비교대상에만 있음: {sorted(only_other)[:20]}")
    if not only_main and not only_other:
        print("  위젯 구성 동일")
    print()

# 스타일시트가 있는 위젯 이름 비교
print("--- 스타일시트 있는 위젯 이름 비교 ---")
print(f"main-백업: {sorted(all_s[files[1]])}")
print(f"sidebar_backup: {sorted(all_s[files[2]])}")
print(f"두 백업의 차이: {all_s[files[1]] ^ all_s[files[2]]}")