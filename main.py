"""ComfyCraft AI Easy Studio — 애플리케이션 진입점.

핵심 제어 로직은 app/main_controller.py의 MainController가 담당한다.
기존 외부 코드/테스트 호환을 위해 MainController 등을 재수출한다.
"""
from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from app.gui.theme_manager import apply_theme, load_theme_choice
from app.gui.ui_loader import load_ui

# 호환 재수출: 기존 테스트/외부 코드가 `from main import ...`로 접근하는 대상
from app.main_controller import (  # noqa: F401
    BASE_DIR,
    UI_FILE,
    MainController,
    logger,
    show_message_box,
)


def main():
    app = QApplication(sys.argv)

    theme_key = load_theme_choice()
    apply_theme(app, theme_key)
    logger.info(f"[테마] 적용: {theme_key}")

    window = load_ui(UI_FILE)
    controller = MainController(window)
    # close()와 무관한 경로로 앱이 종료돼도 스레드 풀이 정리되도록 안전장치
    # (shutdown은 멱등하므로 close()와 중복 호출되어도 무해)
    app.aboutToQuit.connect(controller._close_thread_pools)
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
