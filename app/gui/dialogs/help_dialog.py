"""도움말 다이얼로그 — app/main_controller.py에서 분리됨 (Phase 4)."""

from PySide6.QtCore import (
    QEvent,
    QObject,
    Qt,
    QUrl,
)
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QTextBrowser,
)

from app import show_message_box
from app.gui.ui_loader import load_dialog_ui
from app.paths import BASE_DIR, HELP_DIALOG_FILE


def show_help_dialog(controller):
    """도움말 다이얼로그(v2: 좌우 분할)를 표시한다. 비모달 방식으로 메인 화면과 병행 사용 가능."""
    try:
        dlg = load_dialog_ui(HELP_DIALOG_FILE, controller.window)
    except Exception as e:  # noqa: BLE001 (ui 로드 실패 시 알림)
        show_message_box(
            controller.window,
            QMessageBox.Icon.Warning,
            "도움말 열기 실패",
            f"도움말 화면 파일을 열 수 없습니다.\n({HELP_DIALOG_FILE.name}: {e})",
        )
        return

    # UI 위젯 찾기
    section_list = dlg.findChild(QListWidget, "sectionListWidget")
    content_browser = dlg.findChild(QTextBrowser, "helpContentBrowser")
    close_btn = dlg.findChild(QPushButton, "helpCloseBtn")

    if section_list is None or content_browser is None:
        show_message_box(
            controller.window,
            QMessageBox.Icon.Warning,
            "도움말 UI 오류",
            "도움말 창의 필수 위젯을 찾을 수 없습니다.",
        )
        return

    # 뒤로가기/앞으로가기 버튼 생성 (헤더에 추가)
    header_frame = dlg.findChild(QFrame, "headerFrame")
    header_layout = header_frame.layout() if header_frame else None
    if not isinstance(header_layout, QHBoxLayout):
        header_layout = None
    back_btn = None
    forward_btn = None
    if header_layout:
        # 닫기 버튼 앞에 뒤로가기/앞으로가기 버튼 추가
        back_btn = QPushButton("←", header_frame)
        back_btn.setObjectName("helpBackBtn")
        back_btn.setToolTip("뒤로가기 (Alt+Left)")
        back_btn.setFixedSize(32, 32)
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 16px;
                background-color: transparent;
                color: #555;
                font-size: 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                color: #1a1a1a;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
            QPushButton:disabled {
                color: #ccc;
            }
            [data-theme="dark"] QPushButton {
                color: #aaa;
            }
            [data-theme="dark"] QPushButton:hover {
                background-color: #3a3a3a;
                color: #fff;
            }
            [data-theme="dark"] QPushButton:disabled {
                color: #555;
            }
        """)
        back_btn.setEnabled(False)

        forward_btn = QPushButton("→", header_frame)
        forward_btn.setObjectName("helpForwardBtn")
        forward_btn.setToolTip("앞으로가기 (Alt+Right)")
        forward_btn.setFixedSize(32, 32)
        forward_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        forward_btn.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 16px;
                background-color: transparent;
                color: #555;
                font-size: 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                color: #1a1a1a;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
            QPushButton:disabled {
                color: #ccc;
            }
            [data-theme="dark"] QPushButton {
                color: #aaa;
            }
            [data-theme="dark"] QPushButton:hover {
                background-color: #3a3a3a;
                color: #fff;
            }
            [data-theme="dark"] QPushButton:disabled {
                color: #555;
            }
        """)
        forward_btn.setEnabled(False)

        # 닫기 버튼 앞에 삽입 (spacer 다음, close_btn 이전)
        close_btn_index = -1
        for i in range(header_layout.count()):
            item = header_layout.itemAt(i)
            if item and item.widget() == close_btn:
                close_btn_index = i
                break
        if close_btn_index >= 0:
            header_layout.insertWidget(close_btn_index, forward_btn)
            header_layout.insertWidget(close_btn_index, back_btn)
        else:
            header_layout.addWidget(forward_btn)
            header_layout.addWidget(back_btn)

    # HTML 디렉토리
    html_dir = BASE_DIR / "assets" / "help" / "html"

    # 섹션 정의 (아이콘은 Feather Icons 이름, 실제로는 SVG 파일 또는 유니코드 이모지 사용)
    help_sections = [
        {"id": "getting_started", "title": "시작하기", "icon": "🚀", "file": "01_getting_started.html"},
        {"id": "basic_usage", "title": "기본 워크플로우", "icon": "📝", "file": "02_basic_usage.html"},
        {"id": "model_settings", "title": "모델 설정", "icon": "🤖", "file": "03_model_settings.html"},
        {"id": "prompt_writing", "title": "프롬프트 작성 가이드", "icon": "✍️", "file": "04_prompt_writing.html"},
        {"id": "generation_options", "title": "생성 옵션 상세", "icon": "⚙️", "file": "05_generation_options.html"},
        {"id": "facedetailer", "title": "FaceDetailer 얼굴 보정", "icon": "👤", "file": "06_facedetailer.html"},
        {"id": "history_shortcuts", "title": "히스토리 & 단축키", "icon": "🖼️", "file": "07_history_shortcuts.html"},
        {"id": "faq", "title": "문제해결 (FAQ)", "icon": "❓", "file": "08_faq.html"},
    ]

    # 좌측 리스트 채우기
    for section in help_sections:
        item = QListWidgetItem(f"{section['icon']}  {section['title']}")
        item.setData(Qt.ItemDataRole.UserRole, section)
        section_list.addItem(item)

    # HTML 로드 함수
    def load_section_html(section_data):
        html_file = html_dir / section_data["file"]
        if html_file.exists():
            try:
                html = html_file.read_text(encoding="utf-8")
            except Exception:
                html = "<p style='color:red;'>HTML 파일을 읽을 수 없습니다.</p>"
        else:
            html = f"<p style='color:red;'>파일을 찾을 수 없습니다: {section_data['file']}</p>"
        content_browser.setHtml(html)
        # 베이스 URL 설정 (상대 링크/프래그먼트 올바른 해결을 위해)
        content_browser.document().setBaseUrl(QUrl.fromLocalFile(str(html_file)))
        # 스크롤을 맨 위로
        content_browser.verticalScrollBar().setValue(0)

    # 도움말 내부 링크 클릭 처리 (상대 경로 링크 이동 지원)
    def on_help_link_clicked(url: QUrl):
        url_str = url.toString()
        # 프래그먼트(#)만 있는 경우 현재 페이지 내 앵커 이동 -> 기본 동작 유지
        if url_str.startswith("#"):
            return
        # 상대 경로(예: 02_basic_usage.html)인 경우 html_dir 기준으로 절대 경로 변환
        target_file = html_dir / url_str
        if target_file.exists():
            try:
                html = target_file.read_text(encoding="utf-8")
            except Exception:
                html = "<p style='color:red;'>HTML 파일을 읽을 수 없습니다.</p>"
            content_browser.setHtml(html)
            content_browser.document().setBaseUrl(QUrl.fromLocalFile(str(target_file)))
            content_browser.verticalScrollBar().setValue(0)
        # 외부 링크(http/https)는 openExternalLinks=True로 자동 처리됨

    # 리스트 클릭 시 콘텐츠 전환
    def on_section_clicked(item):
        section_data = item.data(Qt.ItemDataRole.UserRole)
        if section_data:
            load_section_html(section_data)

    section_list.itemClicked.connect(on_section_clicked)

    # 내부 링크 클릭 시그널 연결
    content_browser.anchorClicked.connect(on_help_link_clicked)

    # 초기 선택: 첫 번째 항목
    if section_list.count() > 0:
        first_item = section_list.item(0)
        section_list.setCurrentItem(first_item)
        load_section_html(first_item.data(Qt.ItemDataRole.UserRole))

    # 닫기 버튼
    if close_btn is not None:
        close_btn.clicked.connect(dlg.accept)

    # 뒤로가기/앞으로가기 버튼 연결
    if back_btn and forward_btn:
        back_btn.clicked.connect(content_browser.backward)
        forward_btn.clicked.connect(content_browser.forward)
        # 버튼 활성화 상태 동기화
        content_browser.backwardAvailable.connect(back_btn.setEnabled)
        content_browser.forwardAvailable.connect(forward_btn.setEnabled)
        # 키보드 단축키 지원 (Alt+Left/Right)
        back_shortcut = QShortcut(QKeySequence("Alt+Left"), dlg)
        back_shortcut.activated.connect(content_browser.backward)
        forward_shortcut = QShortcut(QKeySequence("Alt+Right"), dlg)
        forward_shortcut.activated.connect(content_browser.forward)

    # 마우스 4/5번 버튼(X1/X2)으로 뒤로가기/앞으로가기 지원 (크롬 스타일)
    # QTextBrowser에 직접 이벤트 필터 설치 (QObject 서브클래스 방식)
    class HelpMouseEventFilter(QObject):
        def __init__(self, browser):
            super().__init__(browser)
            controller.browser = browser

        def eventFilter(self, obj, event):
            if obj is controller.browser and event.type() == QEvent.Type.MouseButtonPress:
                if event.button() == Qt.MouseButton.XButton1:  # 마우스 4번 버튼 (뒤로가기)
                    if controller.browser.isBackwardAvailable():
                        controller.browser.backward()
                        return True
                elif event.button() == Qt.MouseButton.XButton2:  # 마우스 5번 버튼 (앞으로가기)
                    if controller.browser.isForwardAvailable():
                        controller.browser.forward()
                        return True
            return super().eventFilter(obj, event)

    mouse_filter = HelpMouseEventFilter(content_browser)
    content_browser.installEventFilter(mouse_filter)
    # 필터 객체가 가비지 컬렉션되지 않도록 참조 유지
    setattr(dlg, "_help_mouse_filter", mouse_filter)

    # ESC 키로 닫기
    dlg.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
    dlg.setWindowModality(Qt.WindowModality.NonModal)  # 비모달

    # 창 표시 (비모달)
    dlg.show()
    dlg.raise_()
    dlg.activateWindow()
