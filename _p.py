import io, sys, inspect
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import flet as ft
c = [p for p in inspect.signature(ft.Container.__init__).parameters if p not in ("self","args","kwargs")]
print("Container margin?", "margin" in c, "| bgcolor?", "bgcolor" in c, "| width?", "width" in c)
print("Padding.symmetric?", hasattr(ft.Padding, "symmetric"))
print("CrossAxisAlignment:", [x for x in dir(ft.CrossAxisAlignment) if x.isupper()])
print("Row vertical_alignment?", "vertical_alignment" in [p for p in inspect.signature(ft.Row.__init__).parameters])
r = ft.Row(controls=[ft.Text("a"), ft.Text("b")], vertical_alignment=ft.CrossAxisAlignment.STRETCH)
print("STRETCH ok:", r.vertical_alignment)
