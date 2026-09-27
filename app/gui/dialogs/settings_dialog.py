"""설정 다이얼로그 — app/main_controller.py에서 분리됨 (Phase 4)."""

import re
from pathlib import Path

from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QSpinBox,
)

from app import show_message_box
from app.gui.ui_loader import load_dialog_ui
from app.paths import SETTINGS_DIALOG_FILE

WORKFLOW_TYPES = ("checkpoint", "gguf", "flux_gguf", "zimage")


def validate_manual_profile(data: dict) -> list:
    """P8: 수동 프로필 검증. 오류 메시지 목록 반환 (비어 있으면 통과)."""
    errors = []
    name = str(data.get("name", "")).strip()
    if not name:
        errors.append("프로필명을 입력하세요.")
    elif not re.fullmatch(r"[A-Za-z0-9_.~-]+", name):
        errors.append("프로필명은 영문·숫자·._~- 만 사용하세요.")
    patterns = [p.strip() for p in str(data.get("patterns", "")).split(",")
                if p.strip()]
    if not patterns:
        errors.append("매칭 패턴을 1개 이상 입력하세요 (모델 파일명의 일부).")
    if data.get("workflow_type") not in WORKFLOW_TYPES:
        errors.append("워크플로우 종류를 선택하세요.")
    try:
        steps = int(data.get("steps", 0))
        if not 1 <= steps <= 200:
            errors.append("Steps는 1~200이어야 합니다.")
    except (TypeError, ValueError):
        errors.append("Steps는 숫자여야 합니다.")
    try:
        cfg = float(data.get("cfg", 0))
        if not 0.1 <= cfg <= 30.0:
            errors.append("CFG는 0.1~30.0이어야 합니다.")
    except (TypeError, ValueError):
        errors.append("CFG는 숫자여야 합니다.")
    return errors


def profile_data_to_registry(data: dict) -> dict:
    """P8: 편집기 데이터를 레지스트리 JSON 스키마로 변환."""
    patterns = [p.strip() for p in str(data.get("patterns", "")).split(",")
                if p.strip()]
    name = str(data.get("name", "")).strip()
    return {
        name: {
            "name": name,
            "family": name,
            "aliases": patterns,
            "patterns": patterns,
            "workflow_type": data.get("workflow_type", "checkpoint"),
            "default_clip1": str(data.get("clip1", "")).strip(),
            "default_clip2": str(data.get("clip2", "")).strip(),
            "default_vae": str(data.get("vae", "")).strip(),
            "default_steps": int(data.get("steps", 20)),
            "default_cfg": float(data.get("cfg", 7.0)),
            "sampler_name": str(data.get("sampler", "euler")),
            "scheduler": str(data.get("scheduler", "normal")),
            "priority": 50,
        }
    }


def save_manual_profile(data: dict, folder: Path | str):
    """P8: 검증 후 JSON 저장. (성공 여부, 메시지) 반환. 실패 시 저장 차단."""
    errors = validate_manual_profile(data)
    if errors:
        return False, " / ".join(errors)
    try:
        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        safe = re.sub(r"[^A-Za-z0-9_.~-]", "_",
                      str(data.get("name", "custom")).strip())
        path = folder / f"{safe or 'custom'}.json"
        import json
        path.write_text(
            json.dumps(profile_data_to_registry(data),
                       ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return True, f"저장됨: {path.name} (앱 재시작 없이 즉시 적용)"
    except Exception as exc:
        return False, f"저장 실패: {exc}"


def model_profiles_json_dir() -> Path:
    """P8: 수동 프로필 저장 폴더 (레지스트리 자동 로드 경로)."""
    return Path(__file__).resolve().parent.parent.parent / "model_profiles_json"


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

    # P8: 이미지 모델 탭 (자동 목록 + 수동 프로필)
    _setup_model_tab(dlg, controller)

    dlg.exec()


def _setup_model_tab(dlg, controller) -> None:
    """P8: 자동 판별 목록 표시 + 수동 프로필 저장/삭제. 위젯 없으면 생략."""
    def _child(widget_type, name):
        try:
            return dlg.findChild(widget_type, name)
        except RuntimeError:
            return None

    def _text(name: str) -> str:
        widget = _child(QLineEdit, name)
        try:
            return widget.text().strip() if widget is not None else ""
        except RuntimeError:
            return ""

    # 자동 목록: 레지스트리 프로필 표시 (읽기 전용)
    auto_list = _child(QListWidget, "profileAutoList")
    if auto_list is not None:
        try:
            auto_list.clear()
            for profile in getattr(controller.model_registry, "profiles", []):
                auto_list.addItem(
                    f"{profile.name} · {profile.family} · "
                    f"{profile.workflow_type} "
                    f"(Steps {profile.default_steps} / CFG {profile.default_cfg})")
        except RuntimeError:
            pass

    validate_label = _child(QLabel, "profileValidateLabel")

    def show_status(message: str, ok: bool) -> None:
        if validate_label is None:
            return
        try:
            prefix = "✓ " if ok else "✗ "
            validate_label.setText(prefix + message)
        except RuntimeError:
            pass
        try:
            controller.append_log(f"수동 프로필: {message}")
        except Exception:
            pass

    def collect_data() -> dict:
        def combo_text(name: str, default: str = "") -> str:
            combo = _child(QComboBox, name)
            try:
                return combo.currentText().strip() if combo is not None else default
            except RuntimeError:
                return default

        def spin_value(name: str, default: int = 0) -> int:
            spin = _child(QSpinBox, name)
            try:
                return spin.value() if spin is not None else default
            except RuntimeError:
                return default

        def double_value(name: str, default: float = 0.0) -> float:
            spin = _child(QDoubleSpinBox, name)
            try:
                return spin.value() if spin is not None else default
            except RuntimeError:
                return default

        return {
            "name": _text("profileNameEdit"),
            "patterns": _text("profilePatternsEdit"),
            "workflow_type": combo_text("profileWorkflowCombo", "checkpoint"),
            "steps": spin_value("profileStepsSpin", 0),
            "cfg": double_value("profileCfgSpin", 0.0),
            "sampler": combo_text("profileSamplerCombo", "euler"),
            "scheduler": combo_text("profileSchedulerCombo", "normal"),
            "clip1": _text("profileClip1Edit"),
            "clip2": _text("profileClip2Edit"),
            "vae": _text("profileVaeEdit"),
        }

    def refresh_file_combo() -> None:
        file_combo = _child(QComboBox, "profileFileCombo")
        if file_combo is None:
            return
        try:
            folder = model_profiles_json_dir()
            files = sorted(p.name for p in folder.glob("*.json")) \
                if folder.exists() else []
            file_combo.blockSignals(True)
            file_combo.clear()
            file_combo.addItems(files or ["(저장된 프로필 없음)"])
            file_combo.blockSignals(False)
        except RuntimeError:
            pass

    refresh_file_combo()

    save_btn = _child(QPushButton, "profileSaveBtn")
    if save_btn is not None:
        def on_profile_save():
            data = collect_data()
            ok, message = save_manual_profile(
                data, model_profiles_json_dir())
            show_status(message, ok)
            if ok:
                # 즉시 적용: 실행 중 레지스트리에 등록
                try:
                    from app.core.model_profiles.base import ModelProfile
                    payload = profile_data_to_registry(data)
                    profile_data = payload[data["name"].strip()]
                    controller.model_registry.register(ModelProfile(
                        name=profile_data["name"],
                        family=profile_data["family"],
                        aliases=tuple(profile_data["aliases"]),
                        patterns=tuple(profile_data["patterns"]),
                        workflow_type=profile_data["workflow_type"],
                        default_clip1=profile_data["default_clip1"],
                        default_clip2=profile_data["default_clip2"],
                        default_vae=profile_data["default_vae"],
                        default_steps=profile_data["default_steps"],
                        default_cfg=profile_data["default_cfg"],
                        sampler_name=profile_data["sampler_name"],
                        scheduler=profile_data["scheduler"],
                        priority=profile_data["priority"],
                    ))
                except Exception:
                    pass
                refresh_file_combo()
                # 자동 목록도 갱신
                _setup_model_tab_refresh_only(dlg, controller)
        save_btn.clicked.connect(on_profile_save)

    delete_btn = _child(QPushButton, "profileDeleteBtn")
    if delete_btn is not None:
        def on_profile_delete():
            file_combo = _child(QComboBox, "profileFileCombo")
            if file_combo is None:
                return
            try:
                filename = file_combo.currentText().strip()
            except RuntimeError:
                return
            if not filename or filename == "(저장된 프로필 없음)":
                show_status("삭제할 프로필을 선택하세요.", False)
                return
            try:
                target = model_profiles_json_dir() / filename
                if target.exists():
                    target.unlink()
                    show_status(f"삭제됨: {filename} (재시작 후 반영)", True)
                    refresh_file_combo()
                else:
                    show_status("파일이 없어요.", False)
            except Exception as exc:
                show_status(f"삭제 실패: {exc}", False)
        delete_btn.clicked.connect(on_profile_delete)


def _setup_model_tab_refresh_only(dlg, controller) -> None:
    """P8: 저장 후 자동 목록만 다시 그리기."""
    try:
        auto_list = dlg.findChild(QListWidget, "profileAutoList")
        if auto_list is None:
            return
        auto_list.clear()
        for profile in getattr(controller.model_registry, "profiles", []):
            auto_list.addItem(
                f"{profile.name} · {profile.family} · "
                f"{profile.workflow_type}")
    except RuntimeError:
        pass
