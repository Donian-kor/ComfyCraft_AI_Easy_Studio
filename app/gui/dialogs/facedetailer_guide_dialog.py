"""FaceDetailer 가이드 다이얼로그 — app/main_controller.py에서 분리됨 (Phase 4)."""

from PySide6.QtWidgets import (
    QDialog,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
)

import logging

from app.paths import BASE_DIR

logger = logging.getLogger(__name__)


def show_facedetailer_guide(controller):
    """❓ 얼굴 보정(FaceDetailer) 초보자 가이드 다이얼로그"""
    dlg = QDialog(controller.window)
    dlg.setWindowTitle("❓ 얼굴 보정(FaceDetailer) 쉬운 설명")
    dlg.resize(760, 640)
    dlg.setStyleSheet(controller.window.styleSheet())
    layout = QVBoxLayout(dlg)

    browser = QTextBrowser(dlg)
    browser.setOpenExternalLinks(True)

    guide_file = BASE_DIR / "assets" / "help" / "facedetailer_guide.html"
    if guide_file.exists():
        try:
            html = guide_file.read_text(encoding="utf-8")
        except Exception:
            logger.debug("FaceDetailer 가이드 파일 읽기 실패", exc_info=True)
            html = "<p>설명서 파일을 불러올 수 없습니다.</p>"
    else:
        html = "<p>설명서 파일이 존재하지 않습니다.</p>"

    browser.setHtml(html)
    layout.addWidget(browser)

    close_btn = QPushButton("닫기", dlg)
    close_btn.clicked.connect(dlg.accept)
    layout.addWidget(close_btn)
    dlg.exec()
