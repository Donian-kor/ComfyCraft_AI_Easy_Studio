import sys
from PySide6.QtWidgets import QApplication, QMainWindow
# 기존 코드: from ui_main import Ui_MainWindow
from main_ui import Ui_MainWindow  # 👈 ui_main을 main_ui로 수정!
from qfluentwidgets import setTheme, Theme

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # 💡 여기에 Fluent 디자인 시스템 테마를 적용해줍니다!
        setTheme(Theme.DARK)  # 다크 모드 적용 (밝은 화면은 Theme.LIGHT)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
