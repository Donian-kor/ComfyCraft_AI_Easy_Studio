"""설정 다이얼로그 — app/main_controller.py에서 분리됨 (Phase 4)."""

from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
)

from app import show_message_box
from app.gui.ui_loader import load_dialog_ui
from app.paths import SETTINGS_DIALOG_FILE


def show_settings_dialog(controller):
    """설정 다이얼로그(.ui 파일 기반)를 표시한다.

    연결 버튼(comfyStatusBtn, lmStatusBtn), 사이드바 설정 버튼(settingsButton)
    모두 이 창으로 연결된다.
    """
    try:
        dlg = load_dialog_ui(SETTINGS_DIALOG_FILE, controller.window)
    except Exception as e:  # noqa: BLE001 (ui 로드 실패 시 사용자에게 알림)
        show_message_box(
            controller.window,
            QMessageBox.Icon.Warning,
            "설정창 열기 실패",
            f"설정 화면 파일을 열 수 없습니다.\n({SETTINGS_DIALOG_FILE.name}: {e})",
        )
        return

    def _child(widget_type, name):
        return dlg.findChild(widget_type, name)

    comfy_url_edit = _child(QLineEdit, "dlgComfyUrlEdit")
    model_path_edit = _child(QLineEdit, "dlgModelPathEdit")
    lm_url_edit = _child(QLineEdit, "dlgLmUrlEdit")
    comfy_status_dlg_label = _child(QLabel, "dlgComfyStatusLabel")
    model_path_dlg_label = _child(QLabel, "dlgModelPathStatusLabel")
    lm_status_dlg_label = _child(QLabel, "dlgLmStatusLabel")

    # 다이얼로그에 현재 메인 화면 값 채우기 (그룹A 위젯 삭제 완료 — controller.config 직접 사용)
    if comfy_url_edit is not None:
        comfy_url_edit.setText(controller.config.comfyui.url or "")
    if model_path_edit is not None:
        model_path = controller.config.comfyui_model_paths[0] if controller.config.comfyui_model_paths else ""
        model_path_edit.setText(model_path)
        # 모델 폴더 경로 체크 라벨을 설정창 안에서 바로 보여준다
        controller.update_model_path_status(model_path, model_path_dlg_label)
    if lm_url_edit is not None:
        lm_url_edit.setText(controller.config.lmstudio.url or "")

    # 연결 확인 버튼 (설정창 라벨에도 결과를 함께 표시)
    comfy_check_btn = _child(QPushButton, "dlgComfyCheckBtn")
    if comfy_check_btn is not None and comfy_url_edit is not None:
        def on_comfy_check():
            controller.config.comfyui.url = comfy_url_edit.text()
            controller.check_connection("comfy")
            # 비동기 결과는 update_connection_label에서 배지/메인 라벨에 반영되고,
            # 설정창 라벨은 "확인 중"으로 먼저 표시해 준다
            controller._apply_status_label(
                comfy_status_dlg_label, None, "", "", "📡 연결 중..."
            )
        comfy_check_btn.clicked.connect(on_comfy_check)

    lm_check_btn = _child(QPushButton, "dlgLmCheckBtn")
    if lm_check_btn is not None and lm_url_edit is not None:
        def on_lm_check():
            controller.config.lmstudio.url = lm_url_edit.text()
            controller.check_connection("lm")
            controller._apply_status_label(
                lm_status_dlg_label, None, "", "", "📡 연결 중..."
            )
        lm_check_btn.clicked.connect(on_lm_check)

    # 찾아보기 버튼
    browse_btn = _child(QPushButton, "dlgBrowseBtn")
    if browse_btn is not None and model_path_edit is not None:
        def on_browse():
            folder = QFileDialog.getExistingDirectory(dlg, "ComfyUI 모델 폴더 선택")
            if folder:
                model_path_edit.setText(folder)
                # 그룹A 위젯 삭제 완료 — controller.config 직접 사용
                controller.config.comfyui_model_paths = [folder] + [
                    p for p in controller.config.comfyui_model_paths if p != folder
                ]
                controller.update_model_path_status(folder, model_path_dlg_label)
        browse_btn.clicked.connect(on_browse)

    # 설정 불러오기 버튼 -> 기존 load_config() 재사용
    load_btn = _child(QPushButton, "dlgLoadConfigBtn")
    if load_btn is not None:
        def on_load():
            controller.load_config()
            # 불러온 값으로 다이얼로그 입력칸도 갱신
            if comfy_url_edit is not None:
                comfy_url_edit.setText(controller.config.comfyui.url or "")
            if model_path_edit is not None:
                model_path = controller.config.comfyui_model_paths[0] if controller.config.comfyui_model_paths else ""
                model_path_edit.setText(model_path)
                controller.update_model_path_status(model_path, model_path_dlg_label)
            if lm_url_edit is not None:
                lm_url_edit.setText(controller.config.lmstudio.url or "")
        load_btn.clicked.connect(on_load)

    # 초기화 버튼 -> 프로그램 기본값으로 다이얼로그 입력칸 되돌리기
    reset_btn = _child(QPushButton, "dlgResetDefaultsBtn")
    if reset_btn is not None:
        def on_reset():
            from app.core.config_manager import ComfyUIConfig, LMStudioConfig
            if comfy_url_edit is not None:
                comfy_url_edit.setText(ComfyUIConfig.url)
            if lm_url_edit is not None:
                lm_url_edit.setText(LMStudioConfig.url)
            if model_path_edit is not None:
                model_path_edit.setText("")
                controller.update_model_path_status("", model_path_dlg_label)
            controller.append_log("설정 다이얼로그 값을 기본값으로 되돌렸습니다.")
        reset_btn.clicked.connect(on_reset)

    # 저장 후 닫기 버튼
    save_btn = _child(QPushButton, "dlgSaveCloseBtn")
    if save_btn is not None:
        def on_save_close():
            if comfy_url_edit is not None:
                controller.config.comfyui.url = comfy_url_edit.text()
            if model_path_edit is not None:
                path = model_path_edit.text()
                controller.config.comfyui_model_paths = [path] + [
                    p for p in controller.config.comfyui_model_paths if p != path
                ]
                controller.update_model_path_status(path, model_path_dlg_label)
            if lm_url_edit is not None:
                controller.config.lmstudio.url = lm_url_edit.text()
            controller.save_config()
            dlg.accept()
        save_btn.clicked.connect(on_save_close)

    dlg.exec()
