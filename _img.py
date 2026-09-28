import os, tempfile
os.environ.setdefault("QT_QPA_PLATFORM","offscreen")
from pathlib import Path
from PySide6.QtWidgets import QApplication, QScrollArea, QWidget, QVBoxLayout
app = QApplication([])
from PySide6.QtGui import QImage, QPainter, QColor
from app.gui.chat_widgets import ImageCard

tmp = Path(tempfile.mkdtemp())
def mk(name, w, h):
    p = tmp/name
    img = QImage(w, h, QImage.Format_RGB32); q = QPainter(img)
    q.fillRect(img.rect(), QColor("#3a7")); q.end(); img.save(str(p)); return str(p)

cases = [("landscape", 1600, 600), ("portrait", 800, 1200), ("square", 900, 900)]

scroll = QScrollArea(); content = QWidget(); QVBoxLayout(content)
scroll.setWidget(content); scroll.setWidgetResizable(True)
scroll.resize(700, 900); scroll.show()
cards = []
for name, w, h in cases:
    c = ImageCard(mk(f"{name}.png", w, h), f"{name} meta", "prompt")
    QVBoxLayout(content).addWidget(c)
    cards.append(c)
app.processEvents()

print("=== 종횡비별 표시 검증 (카드 폭 700 창) ===")
for c, (name, w, h) in zip(cards, cases):
    lbl = c.image_label; pm = lbl.pixmap()
    print(f"{name}: src={w}x{h} label={lbl.width()}x{lbl.height()} pixmap={pm.width()}x{pm.height()}")
    # 잘림 검증: 픽스맵이 라벨을 넘지 않아야 한다
    assert pm.width() <= lbl.width() + 1, f"{name} 가로 잘림"
    assert pm.height() <= lbl.height() + 1, f"{name} 세로 잘림"
    # 비율 검증: 원본 비율 유지
    src_ratio = w/h; pm_ratio = pm.width()/pm.height()
    assert abs(src_ratio - pm_ratio) < 0.02, f"{name} 비율 깨짐 {src_ratio} vs {pm_ratio}"

print()
print("=== 창을 넓혔을 때 이미지가 커지는가 (반응성) ===")
lbl = cards[0].image_label
before = lbl.pixmap().width()
scroll.resize(1200, 900)
app.processEvents()
after = lbl.pixmap().width()
print(f"landscape 카드: 창 700->1200, pixmap 폭 {before} -> {after}, label 폭 {lbl.width()}")
assert after > before, "창을 넓혀도 이미지가 커지지 않는다 (반응성 결함)"

print()
print("=== 창을 좁혔을 때 ===")
scroll.resize(360, 900)
app.processEvents()
lbl = cards[0].image_label
pm = lbl.pixmap()
print(f"좁은 창: label={lbl.width()}x{lbl.height()} pixmap={pm.width()}x{pm.height()}")
assert pm.width() <= lbl.width() + 1
print()
print("모든 검증 통과")
