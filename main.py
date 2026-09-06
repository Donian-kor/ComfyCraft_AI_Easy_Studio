from __future__ import annotations

import sys
import threading
import time
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QObject, QTimer, Qt, Signal, QRegularExpression, QPropertyAnimation, QEasingCurve, QEvent
from PySide6.QtGui import QPixmap, QRegularExpressionValidator, QIcon
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QFileDialog,
    QLabel, QLineEdit, QMessageBox, QPlainTextEdit, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QTabWidget, QTextBrowser, QWidget, QFrame, QGroupBox, QStyle
)
from assets.ui.ui_loader import load_ui
from assets.icons import icon_rc  # noqa: F401  (SVG 아이콘 리소스 등록용 - 직접 사용하진 않지만 import 자체가 필요함)
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"


# src 패키지를 sys.path 에 추가하여 모듈 import 가능하게 함
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from src import (
    ComfyUIApiClient,
    ComfyUIWebSocketClient,
    LMStudioApiClient,
    get_config_manager,
    get_model_fetcher,
    get_workflow_manager,
    get_model_registry,
    # Section modules
    ConnectionStatus,
    resolve_live_url,
    check_connection_status,
    check_connection_silent,
    get_default_comfyui_model_roots,
    resolve_model_directory,
    scan_comfyui_model_names,
    GenerationSettings,
    build_generation_snapshot,
    WorkerSignals,
    GenerationWorker,
    normalize_prompt,
    prompt_character_count,
    build_negative_prompt,
    load_external_prompts,
    SAMPLER_NAMES,
    SCHEDULER_NAMES,
    sampler_label_to_value,
    sampler_value_to_label,
    enhance_prompt_sync,
    PromptEnhanceWorker,
    ResultInfo,
    build_result_info,
    ensure_output_directory,
    show_image,
    save_image_as,
    open_output_folder,
    build_filename_prefix,
    show_message_box,
    ExecutionStatus,
    create_execution_status,
    update_execution_status,
    format_elapsed,
    LoadingAnimation,
    ElapsedTimer,
)

# 추가 모듈 import
from src.model_status_service import ModelStatusService

UI_FILE = BASE_DIR / "assets" / "ui" / "main.ui"


class MainController(QObject):
    model_list_ready = Signal(list, list)
    connection_result_ready = Signal(str, object)

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.config_manager = get_config_manager(BASE_DIR / "workflows" / "app_config.json")
        self.config = self.config_manager.get()
        self.model_fetcher = get_model_fetcher(self.config_manager)
        self.model_status_service = ModelStatusService(self.model_fetcher)
        self.model_registry = get_model_registry()
        self.workflow_manager = get_workflow_manager(self.config_manager)
        self.output_dir = ensure_output_directory(str((BASE_DIR / self.config.output.directory).resolve()))
        self.worker = None
        self.current_image_path = None
        self.generation_started_at = None
        self.execution_status = create_execution_status()
        
        # 진행 상황 애니메이션
        self.loading_animation = LoadingAnimation(
            self.find(QProgressBar, "progressBar"),
            self.find(QLabel, "progressStatusLabel")
        )
        
        # 경과 시간 타이머
        self.elapsed_timer = ElapsedTimer(self.find(QLabel, "elapsedLabel"))

        self.close_timer = QTimer(window)
        self.close_timer.setSingleShot(True)
        self.close_timer.timeout.connect(self.window.close)

        self.model_list_ready.connect(self._apply_models_result)
        self.connection_result_ready.connect(self._apply_connection_result)
        self.lm_connected = False
        self.setup()

    def find(self, widget_type, name):
        return self.window.findChild(widget_type, name)

    def setup(self):
        generation = self.config.generation
        for name, minimum, maximum, value in (
            ("widthSpinBox", generation.width_min, generation.width_max, generation.default_width),
            ("heightSpinBox", generation.height_min, generation.height_max, generation.default_height),
            ("stepsSpinBox", generation.steps_min, generation.steps_max, generation.default_steps)):
            widget = self.find(QSpinBox, name)
            widget.setRange(minimum, maximum)
            widget.setValue(value)
        cfg = self.find(QDoubleSpinBox, "cfgSpinBox")
        cfg.setRange(generation.cfg_min, generation.cfg_max)
        cfg.setSingleStep(generation.cfg_increment)
        cfg.setValue(generation.default_cfg)
        seed = self.find(QSpinBox, "seedSpinBox")
        seed.setRange(-1, 2147483647)
        seed.setValue(generation.default_seed)
        lm_url_widget = self.find(QLineEdit, "lmUrlEdit")
        lm_url_widget.setText(self.config.lmstudio.url)
        # URL 입력을 위한 유연한 정규식 (영문, 숫자, 특수문자 허용)
        regex = QRegularExpression(r"^[a-zA-Z0-9.:/\-]*$")
        lm_url_widget.setValidator(QRegularExpressionValidator(regex, self.window))
        self.find(QLineEdit, "comfyUrlEdit").setText(self.config.comfyui.url)
        paths = self.config_manager.get_model_base_paths()
        if paths:
            self.find(QLineEdit, "comfyModelPathEdit").setText(str(paths[0]))
            self.update_model_path_status(str(paths[0]))
        self.find(QPlainTextEdit, "positivePromptEdit").setPlainText("깊은 숲속을 산책중인 현대 한국 여성")
        ext_prompts = load_external_prompts()
        self.find(QPlainTextEdit, "negativePromptEdit").setPlainText(ext_prompts.get("negative_default"))
        sampler = self.find(QComboBox, "samplerComboBox")
        sampler.clear()
        sampler.addItems(list(SAMPLER_NAMES))
        sampler.setCurrentText("DPM++ 2M·균형")
        sampler.currentTextChanged.connect(self._on_sampler_changed)

        scheduler_combo = self.find(QComboBox, "schedulerComboBox")
        if scheduler_combo is not None:
            scheduler_combo.clear()
            scheduler_combo.addItems(SCHEDULER_NAMES)
            scheduler_combo.setCurrentText("normal")
            scheduler_combo.setCurrentIndex(0)

        denoise_spin = self.find(QDoubleSpinBox, "denoiseSpinBox")
        if denoise_spin is not None:
            denoise_spin.setRange(0.0, 1.0)
            denoise_spin.setSingleStep(0.1)
            denoise_spin.setValue(1.0)

        # FaceDetailer ComboBox 초기화
        sam_hint_combo = self.find(QComboBox, "facedetailerSamDetectionHintComboBox")
        if sam_hint_combo is not None:
            sam_hint_combo.clear()
            sam_hint_combo.addItems(["center-1", "center-2", "center-3", "center-4", "all"])
            sam_hint_combo.setCurrentText("center-1")

        sam_mask_neg_combo = self.find(QComboBox, "facedetailerSamMaskHintUseNegativeComboBox")
        if sam_mask_neg_combo is not None:
            sam_mask_neg_combo.clear()
            sam_mask_neg_combo.addItems(["False", "Small", "Outter"])
            sam_mask_neg_combo.setCurrentText("False")

        self.find(QPushButton, "generateButton").clicked.connect(self.start_generation)
        self.find(QPushButton, "stopButton").clicked.connect(self.stop_generation)
        self.find(QPushButton, "enhancePromptButton").clicked.connect(self.enhance_prompt_only)
        self.find(QPushButton, "loadConfigButton").clicked.connect(self.load_config)
        self.find(QPushButton, "saveConfigButton").clicked.connect(self.save_config)
        self.find(QPushButton, "restoreDefaultsButton").clicked.connect(self.restore_defaults)
        self.find(QPushButton, "exitButton").clicked.connect(self.close)
        self.find(QPushButton, "resetButton").clicked.connect(self.clear_logs)
        self.find(QPushButton, "openOutputFolderButton").clicked.connect(self.open_output_folder)
        self.find(QPushButton, "saveImageButton").clicked.connect(self.save_image_as)
        self.find(QPushButton, "lmCheckButton").clicked.connect(lambda: self.check_connection("lm"))
        self.find(QPushButton, "comfyCheckButton").clicked.connect(lambda: self.check_connection("comfy"))
        self.find(QPushButton, "browseModelFolderButton").clicked.connect(self.browse_model_folder)
        self.find(QComboBox, "lmModelCombo").currentTextChanged.connect(lambda text: self.log_model_selection("LM Studio", text))
        self.find(QComboBox, "comfyModelCombo").currentTextChanged.connect(lambda text: self.log_model_selection("ComfyUI", text))
        self.find(QComboBox, "comfyModelCombo").currentTextChanged.connect(self.apply_model_defaults)
        presets = {
            "preset_512x512": (512, 512),
            "preset_768x768": (768, 768),
            "preset_1024x1024": (1024, 1024),
            "preset_832x1216": (832, 1216),
            "preset_1216x832": (1216, 832),
        }
        for button_name, (width, height) in presets.items():
            self.find(QPushButton, button_name).clicked.connect(
                lambda checked=False, width=width, height=height: self.apply_preset(width, height)
            )
        self.find(QPlainTextEdit, "positivePromptEdit").textChanged.connect(lambda: self.update_counter("positivePromptEdit", "positivePromptCounterLabel"))
        self.find(QPlainTextEdit, "negativePromptEdit").textChanged.connect(lambda: self.update_counter("negativePromptEdit", "negativePromptCounterLabel"))
        self.find(QPlainTextEdit, "enhancePromptEdit").textChanged.connect(lambda: self.update_counter("enhancePromptEdit", "enhancePromptCounterLabel"))
        self.update_counter("positivePromptEdit", "positivePromptCounterLabel")
        self.update_counter("negativePromptEdit", "negativePromptCounterLabel")
        self.update_counter("enhancePromptEdit", "enhancePromptCounterLabel")

        self.find(QPushButton, "stopButton").setEnabled(False)
        self.find(QPlainTextEdit, "logTextEdit").setVisible(True)
        # QSplitter를 사용하지 않는 레이아웃 구조이므로, 초기 배치는 레이아웃이 자동 처리
        QTimer.singleShot(0, lambda: self._apply_main_splitter_ratio())
        # progressPercentLabel을 로딩바 정중앙에 배치하도록 설정
        self._setup_progress_label_overlay()
        # elapsedLabel을 우측끝으로 정렬
        self._setup_elapsed_label_alignment()
        self.loading_animation.start("초기화 중...")
        self.find(QLabel, "progressPercentLabel").setText("0%")
        QTimer.singleShot(150, self.refresh_models)

        # 도움말 탭 설정 (추가)
        self._setup_help_tab()
        
        # 사이드바 애니메이션 설정
        self.setup_sidebar_animation()

        # 사이드바 버튼 → 해당 탭 전환 (NEW.ui 구조)
        sidebar_tabs = self.find(QTabWidget, "tabWidget")
        if sidebar_tabs is not None:
            tab_map = {
                "homeButton": 0,       # 홈
                "comfyButton": 1,      # ComfyUI
                "lmstudioButton": 2,   # LMStudio
                "settingsButton": 6,   # Settings
            }
            for btn_name, tab_index in tab_map.items():
                btn = self.find(QPushButton, btn_name)
                if btn is not None and tab_index < sidebar_tabs.count():
                    btn.clicked.connect(
                        lambda checked=False, i=tab_index: sidebar_tabs.setCurrentIndex(i)
                    )

        # 홈 탭 카드 버튼 → 해당 탭 전환 (NEW.ui 홈 화면)
        if sidebar_tabs is not None:
            home_tab_map = {
                "startButton": 1,        # 새 프로젝트 시작 → ComfyUI
                "comfyCardButton": 1,    # ComfyUI 카드 → ComfyUI
                "lmCardButton": 2,       # LMStudio 카드 → LMStudio
            }
            for btn_name, tab_index in home_tab_map.items():
                btn = self.find(QPushButton, btn_name)
                if btn is not None and tab_index < sidebar_tabs.count():
                    btn.clicked.connect(
                        lambda checked=False, i=tab_index: sidebar_tabs.setCurrentIndex(i)
                    )
        
        # ===== 로그창 토글 버튼 (아이콘 버전) =====
        toggle_btn = self.find(QPushButton, "toggleLogButton")
        if toggle_btn:
            toggle_btn.clicked.connect(self.toggle_log)
            self.log_group = self.find(QGroupBox, "logGroupBox")
            self.log_visible = True   # 처음에는 로그가 보이는 상태

            # ✅ Qt 내장 아이콘 사용하기 (별도 이미지 파일 필요 없음)
            from PySide6.QtWidgets import QStyle
            
            # assets/icons 폴더의 실제 파일명과 정확히 일치해야 합니다!
            self.icon_collapse = QIcon(str(BASE_DIR / "assets/icons/toggle-off.svg"))
            self.icon_expand = QIcon(str(BASE_DIR / "assets/icons/toggle-on.svg"))            
            # 처음에는 로그가 보이므로 '접기' 설정
            toggle_btn.setIcon(self.icon_collapse)
            toggle_btn.setText("")  # 혹시 모를 텍스트 제거        

    def setup_sidebar_animation(self):
        """사이드바에 마우스 호버 시 왼쪽으로 접히는 폭(maximumWidth) 애니메이션을 적용합니다."""
        sidebar = self.find(QFrame, "sidebar_frame")
        if not sidebar:
            return

        # 마우스 호버 이벤트를 받을 수 있도록 설정
        sidebar.setAttribute(Qt.WA_Hover, True)
        sidebar.installEventFilter(self)

        # 레이아웃 안에서도 최대 너비(210px)까지 확실히 펼쳐지도록 가로 정책을 Expanding 으로 변경
        policy = sidebar.sizePolicy()
        policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
        sidebar.setSizePolicy(policy)

        # 접힌 상태 너비(55px), 펼친 상태 너비는 UI의 maximumWidth(210px 근처) 사용
        self.sidebar_collapsed_width = 55
        self.sidebar_expanded_width = min(max(55, sidebar.maximumWidth()), 255)

        # splitter/레이아웃 안에서는 geometry 대신 maximumWidth 를 애니메이션 (왼쪽으로 접힘)
        self.sidebar_anim = QPropertyAnimation(sidebar, b"maximumWidth")
        self.sidebar_anim.setDuration(300)  # 0.3초 동안 움직임
        self.sidebar_anim.setEasingCurve(QEasingCurve.InOutQuad)

        # 레이아웃이 임의로 폭을 줄이지 못하도록 최소 너비도 애니메이션 값에 맞춘다
        # (min == max -> 요청한 폭이 정확히 유지됨)
        self.sidebar_anim.valueChanged.connect(self._sync_sidebar_min_width)

        # 이벤트 필터에서 사용하기 위해 저장
        self.sidebar_frame = sidebar

        # 처음에는 접힌 상태(55px)로 시작
        sidebar.setMinimumWidth(self.sidebar_collapsed_width)
        sidebar.setMaximumWidth(self.sidebar_collapsed_width)

    def _sync_sidebar_min_width(self, value):
        """사이드바 애니메이션 중 최소 너비도 함께 맞춰 레이아웃이 정확한 폭을 유지하게 한다."""
        if getattr(self, "sidebar_frame", None) is not None:
            self.sidebar_frame.setMinimumWidth(int(value))

    def eventFilter(self, obj, event):
        """마우스가 사이드바에 들어오고 나갈 때 애니메이션을 실행합니다."""
        # 사이드바에서 발생한 이벤트인지 확인
        if hasattr(self, 'sidebar_frame') and obj == self.sidebar_frame:
            if event.type() == QEvent.HoverEnter:
                # 마우스 올림 → 펼치기(왼쪽에서 오른쪽으로 확장)
                self.sidebar_anim.stop()
                self.sidebar_anim.setStartValue(self.sidebar_frame.maximumWidth())
                self.sidebar_anim.setEndValue(self.sidebar_expanded_width)
                self.sidebar_anim.start()
                return True

            elif event.type() == QEvent.HoverLeave:
                # 마우스 내림 → 접기(오른쪽에서 왼쪽으로 축소, 55px)
                self.sidebar_anim.stop()
                self.sidebar_anim.setStartValue(self.sidebar_frame.maximumWidth())
                self.sidebar_anim.setEndValue(self.sidebar_collapsed_width)
                self.sidebar_anim.start()
                return True

        # 다른 위젯의 이벤트는 원래대로 처리
        return super().eventFilter(obj, event)
    def _on_sampler_changed(self, sampler_label: str):
        """ComfyUI KSampler와 호환되는 scheduler 값으로 보정한다."""
        scheduler_combo = self.find(QComboBox, "schedulerComboBox")
        if scheduler_combo is None:
            return

        current_scheduler = scheduler_combo.currentText()
        if current_scheduler not in SCHEDULER_NAMES:
            scheduler_combo.blockSignals(True)
            scheduler_combo.setCurrentText("normal")
            scheduler_combo.blockSignals(False)

    def _setup_progress_label_overlay(self):
        """progressPercentLabel을 로딩바 정중앙에 overlay로 배치"""
        label = self.find(QLabel, "progressPercentLabel")
        label.setStyleSheet(
            "QLabel { "
            "background-color: transparent; "
            "border: none; "
            "}"
        )
        label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

    def _setup_elapsed_label_alignment(self):
        """elapsedLabel을 우측끝으로 정렬하기 위해 progressInfoLayout에 spacer 추가"""
        from PySide6.QtWidgets import QLayout
        progress_info_layout = None
        # progressInfoLayout 찾기 (resultPanel 하위에서)
        result_panel = self.find(object, "resultPanel")
        if result_panel:
            for widget in result_panel.findChildren(object):
                if hasattr(widget, 'objectName') and widget.objectName() == "progressInfoLayout":
                    progress_info_layout = widget
                    break
        
        # progressInfoLayout를 직접 찾는 다른 방법 - parent의 layout 확인
        elapsed_label = self.find(QLabel, "elapsedLabel")
        if elapsed_label and elapsed_label.parent():
            parent = elapsed_label.parent()
            if hasattr(parent, 'layout') and callable(parent.layout):
                progress_info_layout = parent.layout()
        
        # spacer 추가
        if progress_info_layout is not None:
            spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
            # elapsedLabel 전에 spacer 삽입 (인덱스를 찾아서)
            elapsed_index = None
            for i in range(progress_info_layout.count()):
                item = progress_info_layout.itemAt(i)
                if item and hasattr(item, 'widget') and item.widget() == elapsed_label:
                    elapsed_index = i
                    break
            if elapsed_index is not None and elapsed_index > 0:
                progress_info_layout.insertItem(elapsed_index, spacer)

    def refresh_models(self):
        self.find(QLabel, "progressStatusLabel").setText("모델 목록 로딩 중...")
        lm_url = self.find(QLineEdit, "lmUrlEdit").text().strip()
        comfy_url = self.find(QLineEdit, "comfyUrlEdit").text().strip()

        # 이전에 성공한 URL들을 후보로 전달 (설정에서 가져오기)
        lm_candidates = [self.config.lmstudio.url] if self.config.lmstudio.url else []
        comfy_candidates = [self.config.comfyui.url] if self.config.comfyui.url else []

        resolved_lm_url = resolve_live_url("lm", lm_url, lm_candidates)
        resolved_comfy_url = resolve_live_url("comfy", comfy_url, comfy_candidates)

        # 살아있는 URL을 찾았을 때만 UI 업데이트 (못 찾으면 사용자 입력 유지)
        if resolved_lm_url and resolved_lm_url != lm_url:
            self.find(QLineEdit, "lmUrlEdit").setText(resolved_lm_url)
            lm_url = resolved_lm_url
        elif not resolved_lm_url:
            self.append_log("[WARNING] LM Studio 서버를 찾을 수 없습니다. URL을 확인해주세요.")
            self.find(QLabel, "lmStatusLabel").setText("🔴서버 없음")
            self.find(QLabel, "lmStatusLabel").setStyleSheet("color:#E45757;")
        
        if resolved_comfy_url and resolved_comfy_url != comfy_url:
            self.find(QLineEdit, "comfyUrlEdit").setText(resolved_comfy_url)
            comfy_url = resolved_comfy_url
        elif not resolved_comfy_url:
            self.append_log("[WARNING] ComfyUI 서버를 찾을 수 없습니다. URL을 확인해주세요.")
            self.find(QLabel, "comfyStatusLabel").setText("🔴서버 없음")
            self.find(QLabel, "comfyStatusLabel").setStyleSheet("color:#E45757;")

        def fetch():
            # URL이 없으면 모델 목록 조회 건너뛰기
            if not lm_url and not comfy_url:
                self.model_list_ready.emit([], [])
                self.connection_result_ready.emit("lm", ConnectionStatus(service="LM Studio", url="", ok=False, message="URL 없음"))
                self.connection_result_ready.emit("comfy", ConnectionStatus(service="ComfyUI", url="", ok=False, message="URL 없음"))
                return
            
            status = self.model_status_service.fetch(lm_url, comfy_url)
            fallback_candidates = self.config_manager.get_model_base_paths()
            fallback_root = resolve_model_directory("", fallback_candidates)
            fallback_models = scan_comfyui_model_names(fallback_root, fallback_candidates)
            if not status.comfy_models or status.comfy_models == ["로드된 모델 없음"]:
                status.comfy_models = fallback_models or status.comfy_models
            elif not fallback_models:
                status.comfy_models = status.comfy_models
            elif status.comfy_models != fallback_models:
                status.comfy_models = fallback_models[:]
            
            # 실제 연결 상태 확인 (API 호출로 정확하게)
            lm_ok = check_connection_silent("lm", lm_url) if lm_url else False
            comfy_ok = check_connection_silent("comfy", comfy_url) if comfy_url else False
            
            self.model_list_ready.emit(status.lm_models, status.comfy_models)
            # 연결 상태도 함께 전달
            lm_status = ConnectionStatus(service="LM Studio", url=lm_url, ok=lm_ok, message="연결 성공" if lm_ok else "연결 실패")
            comfy_status = ConnectionStatus(service="ComfyUI", url=comfy_url, ok=comfy_ok, message="연결 성공" if comfy_ok else "연결 실패")
            self.connection_result_ready.emit("lm", lm_status)
            self.connection_result_ready.emit("comfy", comfy_status)
        
        threading.Thread(target=fetch, daemon=True).start()

    def _apply_models_result(self, lm_models, comfy_models):
        self.set_models(lm_models, comfy_models)
        self.loading_animation.stop()
        self.find(QLabel, "progressStatusLabel").setText("준비 완료")

    def set_models(self, lm_models, comfy_models):
        for name, values, selected in (("lmModelCombo", lm_models, self.config.lmstudio.model), ("comfyModelCombo", comfy_models, self.config.comfyui.model)):
            combo = self.find(QComboBox, name)
            combo.blockSignals(True)
            combo.clear()
            combo.addItems(values or ["로드된 모델 없음"])
            if selected in values:
                combo.setCurrentText(selected)
            combo.blockSignals(False)
        self.log_model_list("LM Studio", lm_models)
        self.log_model_list("ComfyUI", comfy_models)
        # 모델 목록의 유무로 연결을 판정하지 않음 (refresh_models에서 별도로 처리)

    def log_model_list(self, service_name, values):
        items = list(values or [])
        if not items:
            self.append_log(f"{service_name} 모델 목록 로드: 없음")
            return
        if items == ["로드된 모델 없음"]:
            self.append_log(f"{service_name} 모델 목록 로드: 로드된 모델 없음")
            return
        preview = items[:5]
        suffix = f" 외 {len(items) - 5}개" if len(items) > 5 else ""
        self.append_log(f"{service_name} 모델 목록 로드: {len(items)}개 [{', '.join(preview)}{suffix}]")

    def log_model_selection(self, service_name, model_name):
        if not model_name or model_name == "로드된 모델 없음":
            return
        self.append_log(f"{service_name} 모델 선택 변경: {model_name}")

    def check_connection(self, which):
        raw_url = self.find(QLineEdit, "lmUrlEdit" if which == "lm" else "comfyUrlEdit").text().strip()
        resolved_url = resolve_live_url(which, raw_url)
        if resolved_url and resolved_url != raw_url:
            self.find(QLineEdit, "lmUrlEdit" if which == "lm" else "comfyUrlEdit").setText(resolved_url)
        self.update_connection_label(which, None)

        def check():
            ok = False
            try:
                # 극단적으로 빠른 타임아웃 (0.3초 이내)
                client = LMStudioApiClient(resolved_url) if which == "lm" else ComfyUIApiClient(resolved_url)
                response = client.get_models(timeout=0.3) if which == "lm" else client.get_system_stats(timeout=0.3)
                # 실제 응답이 있고 상태 코드가 400 미만이어야 성공
                ok = bool(response is not None and getattr(response, "status_code", 500) < 400)
            except Exception:
                ok = False

            status = check_connection_status(which, resolved_url)
            # API 호출 결과로 최종 판정
            status.ok = ok
            status.message = "연결 성공" if status.ok else "연결 실패"
            self.connection_result_ready.emit(which, status)
        threading.Thread(target=check, daemon=True).start()

    def _apply_connection_result(self, which, status):
        self.apply_connection_result(which, status)

    def apply_connection_result(self, which, status):
        if which == "lm":
            self.lm_connected = bool(status.ok)
        self.update_connection_label(which, status.ok)
        self.append_log(f"{status.service} 상태: {status.message} (실제 주소: {status.url})")

    def is_lm_connected(self):
        if self.lm_connected:
            return True
        label = self.find(QLabel, "lmStatusLabel")
        return bool(label and "연결 성공" in label.text())

    def update_connection_label(self, which, ok):
        label = self.find(QLabel, "lmStatusLabel" if which == "lm" else "comfyStatusLabel")
        if ok is None:
            label.setText("📡 연결 중...")
            label.setStyleSheet("color:#B8C0CC;")
            return

        text = "🟢연결 성공" if ok else "🔴연결 실패"
        color = "#26C66D" if ok else "#E45757"
        label.setText(text)
        label.setStyleSheet(f"color:{color};")

    def browse_model_folder(self):
        folder = QFileDialog.getExistingDirectory(self.window, "ComfyUI 모델 폴더 선택")
        if folder:
            self.find(QLineEdit, "comfyModelPathEdit").setText(folder)
            self.update_model_path_status(folder)

    def update_model_path_status(self, path):
        path_obj = Path(path).expanduser()
        valid = path_obj.exists() and any((path_obj / item).is_dir() for item in ("checkpoints", "unet", "diffusion_models", "vae", "clip", "loras"))
        label = self.find(QLabel, "modelPathStatusLabel")
        label.setText("✓ ComfyUI 모델 폴더 확인됨" if valid else "✗ 올바른 모델 폴더가 아닙니다")
        label.setStyleSheet(f"color:{'#26C66D' if valid else '#E45757'};")

    def apply_model_defaults(self, model_name):
        if not model_name or model_name == "로드된 모델 없음":
            return
        profile = self.model_registry.detect(model_name)
        self.find(QSpinBox, "stepsSpinBox").setValue(profile.default_steps)
        self.find(QDoubleSpinBox, "cfgSpinBox").setValue(profile.default_cfg)
        display = next((key for key, value in SAMPLER_NAMES.items() if value == profile.sampler_name), profile.sampler_name)
        self.find(QComboBox, "samplerComboBox").setCurrentText(display)
        scheduler_combo = self.find(QComboBox, "schedulerComboBox")
        if scheduler_combo is not None:
            scheduler_combo.setCurrentText(profile.scheduler if profile.scheduler in SCHEDULER_NAMES else "normal")
        denoise_spin = self.find(QDoubleSpinBox, "denoiseSpinBox")
        if denoise_spin is not None:
            denoise_spin.setValue(1.0)
        
        # 로드한 모델 프로파일 정보를 로그에 표시
        profile_info = f"모델 프로파일 로드: [{profile.family.upper()}] {profile.name}"
        if profile.workflow_type == "gguf":
            profile_info += f" (GGUF)"
        elif profile.workflow_type == "zimage":
            profile_info += f" (ZImage-GGUF)"
        elif profile.workflow_type == "flux_gguf":
            profile_info += f" (Flux-GGUF)"
        profile_info += f" | Steps: {profile.default_steps}, CFG: {profile.default_cfg}, Sampler: {display}"
        self.append_log(profile_info)
        
        # 보조 모델 정보 표시
        if profile.default_vae:
            self.append_log(f"  └─ VAE: {profile.default_vae}")
        
        if profile.default_clip1 or profile.default_clip2:
            clip_info = "  └─ CLIP:"
            clips = []
            if profile.default_clip1:
                clips.append(profile.default_clip1)
            if profile.default_clip2:
                clips.append(profile.default_clip2)
            clip_info += " " + ", ".join(clips)
            self.append_log(clip_info)

    def apply_preset(self, width, height):
        self.find(QSpinBox, "widthSpinBox").setValue(width)
        self.find(QSpinBox, "heightSpinBox").setValue(height)
        self.append_log(f"해상도 프리셋 적용: {width}x{height}")

    def load_config(self):
        config_path = self.config_manager.config_path
        file_exists = config_path.exists()
        self.config = self.config_manager.load()
        self.config_manager._config = self.config

        if file_exists:
            message = f"저장된 설정을 불러왔습니다. ({config_path.name})"
            show_message_box(self.window, QMessageBox.Icon.Information, "설정 불러오기", message)
            self.append_log(message)
        else:
            message = f"설정 파일이 없어 기본값을 불러왔습니다. ({config_path.name})"
            show_message_box(self.window, QMessageBox.Icon.Information, "기본값 로드", message)
            self.append_log(message)

        self.find(QLineEdit, "lmUrlEdit").setText(self.config.lmstudio.url)
        self.find(QLineEdit, "comfyUrlEdit").setText(self.config.comfyui.url)
        if self.config.lmstudio.model:
            self.find(QComboBox, "lmModelCombo").setCurrentText(self.config.lmstudio.model)
        if self.config.comfyui.model:
            self.find(QComboBox, "comfyModelCombo").setCurrentText(self.config.comfyui.model)

        model_paths = self.config_manager.get_model_base_paths()
        if model_paths:
            first_path = str(model_paths[0])
            self.find(QLineEdit, "comfyModelPathEdit").setText(first_path)
            self.update_model_path_status(first_path)

        self.find(QSpinBox, "widthSpinBox").setValue(self.config.generation.default_width)
        self.find(QSpinBox, "heightSpinBox").setValue(self.config.generation.default_height)
        self.find(QSpinBox, "stepsSpinBox").setValue(self.config.generation.default_steps)
        self.find(QDoubleSpinBox, "cfgSpinBox").setValue(self.config.generation.default_cfg)
        self.find(QSpinBox, "seedSpinBox").setValue(self.config.generation.default_seed)

        sampler_name = self.config.workflow.sampler_name
        sampler_display = next((label for label, value in SAMPLER_NAMES.items() if value == sampler_name), sampler_name)
        self.find(QComboBox, "samplerComboBox").setCurrentText(sampler_display)
        
        # Scheduler 복구
        scheduler_name = self.config.workflow.scheduler
        scheduler_combo = self.find(QComboBox, "schedulerComboBox")
        if scheduler_combo is not None:
            if scheduler_name in SCHEDULER_NAMES:
                scheduler_combo.setCurrentText(scheduler_name)
            else:
                scheduler_combo.setCurrentIndex(0)
        
        # Denoise 복구
        denoise_spin = self.find(QDoubleSpinBox, "denoiseSpinBox")
        if denoise_spin is not None:
            denoise_spin.setValue(self.config.workflow.denoise)

    def _apply_main_splitter_ratio(self):
        # QSplitter 를 쓰지 않는 레이아웃 구조에서는 사이드바가 최대 너비만큼,
        # 나머지 콘텐츠가 남은 공간을 차지하도록 한다.
        try:
            sidebar = self.find(QFrame, "sidebar_frame")
            if sidebar is not None:
                sidebar.setMinimumWidth(55)
                # 접힘/펼침 상태는 setup_sidebar_animation 이 관리하므로
                # 여기서는 최대 너비를 펼친 상태(210px)로 열어둔다.
                sidebar.setMaximumWidth(sidebar.maximumWidth() or 210)
        except Exception:
            pass
        # (이전 QSplitter 비율 코드는 구조 변경으로 제거됨)

    def _setup_help_tab(self):
        """도움말 탭의 helpBrowser(main.ui에 정의됨)에 README.md와 INSTALLATION.md 내용을 채운다."""
        browser = self.find(QTextBrowser, "helpBrowser")
        if browser is None:
            return

        # 파일 읽기
        readme_path = BASE_DIR / "assets" / "help" / "README.md"
        install_path = BASE_DIR / "assets" / "help" / "INSTALLATION.md"

        html_parts = ["<h1 style='color: #0f172a; font-size: 24px; margin-bottom: 8px;'>📖 프로그램 도움말 v0.3</h1><hr style='border-color: #e2e8f0;'>"]

        # README.md 요약
        if readme_path.exists():
            try:
                with open(readme_path, "r", encoding="utf-8") as f:
                    readme_text = f.read()
                    # markdown → HTML 변환 (패키지 없으면 텍스트 그대로)
                    try:
                        import importlib
                        markdown = importlib.import_module("markdown")
                        html_parts.append(markdown.markdown(readme_text, extensions=["tables"]))
                    except ImportError:
                        html_parts.append("<pre>" + readme_text + "</pre>")
            except Exception as e:
                html_parts.append(f"<p style='color:red;'>README.md 읽기 오류: {e}</p>")
        else:
            html_parts.append("<p style='color:red;'>⚠️ README.md 파일을 찾을 수 없습니다.</p>")

        html_parts.append("<hr style='border-color: #e2e8f0; margin: 24px 0;'><h2 style='color: #0f172a; font-size: 20px;'>🔧 설치 및 트러블슈팅</h2>")

        # INSTALLATION.md 요약
        if install_path.exists():
            try:
                with open(install_path, "r", encoding="utf-8") as f:
                    install_text = f.read()
                    try:
                        import importlib
                        markdown = importlib.import_module("markdown")
                        html_parts.append(markdown.markdown(install_text, extensions=["tables"]))
                    except ImportError:
                        html_parts.append("<pre>" + install_text + "</pre>")
            except Exception as e:
                html_parts.append(f"<p style='color:red;'>INSTALLATION.md 읽기 오류: {e}</p>")
        else:
            html_parts.append("<p style='color:red;'>⚠️ INSTALLATION.md 파일을 찾을 수 없습니다.</p>")

        browser.setHtml("\n".join(html_parts))

    def save_config(self):
        """설정 값을 저장합니다."""
        # LM Studio URL 및 모델 업데이트
        self.config.lmstudio.url = self.find(QLineEdit, "lmUrlEdit").text().strip()
        self.config.lmstudio.model = self.find(QComboBox, "lmModelCombo").currentText()
        
        # ComfyUI URL 및 모델 업데이트
        self.config.comfyui.url = self.find(QLineEdit, "comfyUrlEdit").text().strip()
        self.config.comfyui.model = self.find(QComboBox, "comfyModelCombo").currentText()
        
        # ComfyUI 모델 경로 업데이트 (첫 번째 경로만 저장하는 방식으로 유지)
        model_path = self.find(QLineEdit, "comfyModelPathEdit").text().strip()
        if model_path:
            self.config.comfyui_model_paths = [model_path] + [p for p in self.config.comfyui_model_paths if p != model_path]
        else:
             self.config.comfyui_model_paths = []

        # Generation options 저장
        generation = self.config.generation
        self.config.generation.default_width = self.find(QSpinBox, "widthSpinBox").value()
        self.config.generation.default_height = self.find(QSpinBox, "heightSpinBox").value()
        self.config.generation.default_steps = self.find(QSpinBox, "stepsSpinBox").value()
        self.config.generation.default_cfg = self.find(QDoubleSpinBox, "cfgSpinBox").value()
        self.config.generation.default_seed = self.find(QSpinBox, "seedSpinBox").value()
        
        # Sampler는 실제 값으로 저장 (라벨->값 매핑)
        sampler_label = self.find(QComboBox, "samplerComboBox").currentText()
        self.config.workflow.sampler_name = SAMPLER_NAMES.get(sampler_label, "euler")
        
        # Scheduler 저장
        scheduler_combo = self.find(QComboBox, "schedulerComboBox")
        if scheduler_combo is not None:
            self.config.workflow.scheduler = scheduler_combo.currentText()
        
        # Denoise 저장
        denoise_spin = self.find(QDoubleSpinBox, "denoiseSpinBox")
        if denoise_spin is not None:
            self.config.workflow.denoise = denoise_spin.value()

        # 설정 객체 업데이트 및 저장 시도
        self.config_manager._config = self.config
        if self.config_manager.save():
            show_message_box(self.window, QMessageBox.Icon.Information, "저장 완료", "설정이 성공적으로 저장되었습니다.")
        else:
            show_message_box(self.window, QMessageBox.Icon.Warning, "저장 실패", "설정 저장에 실패했습니다. 경로 권한을 확인해주세요.")

    def restore_defaults(self):
        generation = self.config.generation
        self.find(QSpinBox, "widthSpinBox").setValue(generation.default_width)
        self.find(QSpinBox, "heightSpinBox").setValue(generation.default_height)
        self.find(QSpinBox, "stepsSpinBox").setValue(generation.default_steps)
        self.find(QDoubleSpinBox, "cfgSpinBox").setValue(generation.default_cfg)
        self.find(QSpinBox, "seedSpinBox").setValue(generation.default_seed)
        self.find(QComboBox, "samplerComboBox").setCurrentText("DPM++ 2M·균형")
        scheduler_combo = self.find(QComboBox, "schedulerComboBox")
        if scheduler_combo is not None:
            scheduler_combo.setCurrentText("normal")
        denoise_spin = self.find(QDoubleSpinBox, "denoiseSpinBox")
        if denoise_spin is not None:
            denoise_spin.setValue(1.0)

    def capture_snapshot(self):
        prompt_text = self.find(QPlainTextEdit, "positivePromptEdit").toPlainText()
        negative_text = self.find(QPlainTextEdit, "negativePromptEdit").toPlainText()
        # enhancePromptEdit 내용도 스냅샷에 포함 (이미지 생성 시 LM Studio 재요청 방지용)
        enhance_prompt_text = self.find(QPlainTextEdit, "enhancePromptEdit").toPlainText()
        generation_settings = build_generation_snapshot({
            "width": self.find(QSpinBox, "widthSpinBox").value(),
            "height": self.find(QSpinBox, "heightSpinBox").value(),
            "steps": self.find(QSpinBox, "stepsSpinBox").value(),
            "cfg": self.find(QDoubleSpinBox, "cfgSpinBox").value(),
            "seed": self.find(QSpinBox, "seedSpinBox").value(),
            "sampler": SAMPLER_NAMES.get(self.find(QComboBox, "samplerComboBox").currentText(), "euler"),
            "scheduler": self.find(QComboBox, "schedulerComboBox").currentText() if self.find(QComboBox, "schedulerComboBox") is not None else "normal",
            "denoise": float(self.find(QDoubleSpinBox, "denoiseSpinBox").value() if self.find(QDoubleSpinBox, "denoiseSpinBox") is not None else 1.0),
        })
        # FaceDetailer 설정도 스냅샷에 포함
        facedetailer_enabled = self.find(QCheckBox, "facedetailerCheckBox").isChecked()
        facedetailer_denoise = self.find(QDoubleSpinBox, "facedetailerDenoiseSpinBox").value()
        facedetailer_steps = self.find(QSpinBox, "facedetailerStepsSpinBox").value()
        facedetailer_cfg = self.find(QDoubleSpinBox, "facedetailerCfgSpinBox").value()
        facedetailer_guide_size = self.find(QSpinBox, "facedetailerGuideSizeSpinBox").value()
        facedetailer_max_size = self.find(QSpinBox, "facedetailerMaxSizeSpinBox").value()
        facedetailer_feather = self.find(QSpinBox, "facedetailerFeatherSpinBox").value()
        facedetailer_bbox_threshold = self.find(QDoubleSpinBox, "facedetailerBboxThresholdSpinBox").value()
        facedetailer_bbox_dilation = self.find(QSpinBox, "facedetailerBboxDilationSpinBox").value()
        facedetailer_bbox_crop_factor = self.find(QDoubleSpinBox, "facedetailerBboxCropFactorSpinBox").value()
        facedetailer_sam_detection_hint = self.find(QComboBox, "facedetailerSamDetectionHintComboBox").currentText()
        facedetailer_sam_dilation = self.find(QSpinBox, "facedetailerSamDilationSpinBox").value()
        facedetailer_sam_threshold = self.find(QDoubleSpinBox, "facedetailerSamThresholdSpinBox").value()
        facedetailer_sam_bbox_expansion = self.find(QSpinBox, "facedetailerSamBboxExpansionSpinBox").value()
        facedetailer_sam_mask_hint_threshold = self.find(QDoubleSpinBox, "facedetailerSamMaskHintThresholdSpinBox").value()
        facedetailer_sam_mask_hint_use_negative = self.find(QComboBox, "facedetailerSamMaskHintUseNegativeComboBox").currentText()
        facedetailer_cycle = self.find(QSpinBox, "facedetailerCycleSpinBox").value()
        facedetailer_drop_size = self.find(QSpinBox, "facedetailerDropSizeSpinBox").value()
        
        return {
            "prompt": normalize_prompt(prompt_text),
            "negative": build_negative_prompt(negative_text),
            "enhance_prompt": enhance_prompt_text,  # enhancePromptEdit 내용 추가
            "lm_url": self.find(QLineEdit, "lmUrlEdit").text().strip(),
            "lm_model": self.find(QComboBox, "lmModelCombo").currentText(),
            "comfy_url": self.find(QLineEdit, "comfyUrlEdit").text().strip(),
            "comfy_model": self.find(QComboBox, "comfyModelCombo").currentText(),
            "width": generation_settings.width,
            "height": generation_settings.height,
            "steps": generation_settings.steps,
            "cfg": generation_settings.cfg,
            "seed": generation_settings.seed,
            "sampler": generation_settings.sampler,
            "scheduler": generation_settings.scheduler,
            "denoise": generation_settings.denoise,
            # FaceDetailer 설정
            "facedetailer_enabled": facedetailer_enabled,
            "facedetailer_denoise": facedetailer_denoise,
            "facedetailer_steps": facedetailer_steps,
            "facedetailer_cfg": facedetailer_cfg,
            "facedetailer_guide_size": facedetailer_guide_size,
            "facedetailer_max_size": facedetailer_max_size,
            "facedetailer_feather": facedetailer_feather,
            "facedetailer_bbox_threshold": facedetailer_bbox_threshold,
            "facedetailer_bbox_dilation": facedetailer_bbox_dilation,
            "facedetailer_bbox_crop_factor": facedetailer_bbox_crop_factor,
            "facedetailer_sam_detection_hint": facedetailer_sam_detection_hint,
            "facedetailer_sam_dilation": facedetailer_sam_dilation,
            "facedetailer_sam_threshold": facedetailer_sam_threshold,
            "facedetailer_sam_bbox_expansion": facedetailer_sam_bbox_expansion,
            "facedetailer_sam_mask_hint_threshold": facedetailer_sam_mask_hint_threshold,
            "facedetailer_sam_mask_hint_use_negative": facedetailer_sam_mask_hint_use_negative,
            "facedetailer_cycle": facedetailer_cycle,
            "facedetailer_drop_size": facedetailer_drop_size,
        }

    def enhance_prompt_only(self):
        """이미지 생성 없이 프롬프트만 LM Studio로 향상시켜 positivePromptEdit에 적용"""
        self.append_log("[DEBUG] enhance_prompt_only 호출됨")
        prompt_text = self.find(QPlainTextEdit, "positivePromptEdit").toPlainText()
        prompt = normalize_prompt(prompt_text)
        if not prompt:
            show_message_box(self.window, QMessageBox.Icon.Warning, "프롬프트 필요", "향상시킬 프롬프트를 입력해주세요.")
            return

        lm_url = self.find(QLineEdit, "lmUrlEdit").text().strip()
        lm_model = self.find(QComboBox, "lmModelCombo").currentText()
        self.append_log(f"[DEBUG] lm_url={lm_url}, lm_model={lm_model}")
        if not lm_model or lm_model == "로드된 모델 없음":
            show_message_box(self.window, QMessageBox.Icon.Warning, "모델 필요", "LM Studio 모델을 선택해주세요.")
            return

        # LM Studio 연결 확인
        lm_connected = self.is_lm_connected()
        self.append_log(f"[DEBUG] is_lm_connected={lm_connected}")
        if not lm_connected:
            show_message_box(self.window, QMessageBox.Icon.Warning, "연결 필요", "LM Studio가 연결되지 않았습니다. 연결 확인 후 다시 시도해주세요.")
            return

        self.append_log("프롬프트 향상 중...")
        self.find(QLabel, "progressStatusLabel").setText("프롬프트 향상 중...")

        ext_prompts = load_external_prompts()
        use_korean = self.config.prompts.use_korean_prompt

        # ComfyUI 모델 타입에 따라 시스템 프롬프트 자동 선택 (generation.py와 동일 로직)
        comfy_model_name = self.find(QComboBox, "comfyModelCombo").currentText()
        profile = self.model_registry.detect(comfy_model_name)
        manager = self.workflow_manager

        is_flux = bool(profile.workflow_type == "flux_gguf" or manager.is_flux_model(comfy_model_name) or profile.family == "flux")
        is_zimage = bool(manager.is_zimage_model(comfy_model_name) or profile.workflow_type == "zimage")

        # LM Studio에는 영문 시스템 프롬프트 사용 (출력 언어 준수율 향상)
        # use_korean_prompt 설정과 무관하게 영문 프롬프트(_en) 사용
        if is_flux or is_zimage:
            self.append_log(f"[AI 자동 분석] '{comfy_model_name}' 모델 감지: '문장형' 프롬프트 지시문을 사용합니다.")
            system_prompt = ext_prompts.get("system_prompt_flux_en")
        else:
            self.append_log(f"[AI 자동 분석] '{comfy_model_name}' 모델 감지: '태그형(쉼표 구분)' 프롬프트 지시문을 사용합니다.")
            system_prompt = ext_prompts.get("system_prompt_sdxl_en")

        # 백업용 기본값
        if not system_prompt:
            system_prompt = ext_prompts.get("system_prompt_sdxl_en")

        # PromptEnhanceWorker 사용 (test2.py 완전 호환 버전)
        self._prompt_enhance_worker = PromptEnhanceWorker(
            lm_url=lm_url,
            model_name=lm_model,
            prompt=prompt,
            system_prompt=system_prompt,
            timeout=self.config.lmstudio.timeout_seconds
        )
        self._prompt_enhance_worker.finished_signal.connect(self._on_prompt_enhanced)
        self._prompt_enhance_worker.error_signal.connect(self._on_prompt_enhance_error)
        self._prompt_enhance_worker.debug_signal.connect(lambda msg: self.append_log(msg))
        self.append_log("[DEBUG] 워커 시작...")
        self._prompt_enhance_worker.start()

    def _on_prompt_enhanced(self, enhanced_prompt: str):
        """프롬프트 향상 성공 시 호출"""
        self.append_log(f"[DEBUG] 프롬프트 향상 성공: {enhanced_prompt[:50]}...")
        self._apply_enhanced_prompt(enhanced_prompt)

    def _on_prompt_enhance_error(self, error_msg: str):
        """프롬프트 향상 실패 시 호출"""
        self.append_log(f"[DEBUG] 프롬프트 향상 실패: {error_msg}")
        show_message_box(self.window, QMessageBox.Icon.Warning, "프롬프트 향상 실패", error_msg)
        self.find(QLabel, "progressStatusLabel").setText("준비 완료")

    def _apply_enhanced_prompt(self, enhanced_prompt):
        """향상된 프롬프트를 enhancePromptEdit에 적용"""
        self.append_log(f"[DEBUG] _apply_enhanced_prompt 호출됨: {enhanced_prompt[:50]}...")
        prompt_edit = self.find(QPlainTextEdit, "enhancePromptEdit")
        self.append_log(f"[DEBUG] prompt_edit 찾음: {prompt_edit is not None}")
        if prompt_edit:
            prompt_edit.setPlainText(enhanced_prompt)
            self.append_log(f"[DEBUG] setPlainText 완료")
        else:
            self.append_log(f"[ERROR] enhancePromptEdit을 찾을 수 없음!")
        self.append_log(f"프롬프트 향상 완료: {enhanced_prompt[:100]}...")
        self.find(QLabel, "progressStatusLabel").setText("준비 완료")

    def start_generation(self):
        if self.worker:
            return
        snapshot = self.capture_snapshot()
        if not snapshot["prompt"]:
            show_message_box(self.window, QMessageBox.Icon.Warning, "프롬프트 필요", "프롬프트를 입력해주세요.")
            return
            
        # 워커 인스턴스 생성
        self.worker = GenerationWorker(self, snapshot)
        
        # 🚀 중복되지 않도록 시그널 이벤트를 딱 1번만 연결합니다.
        self.worker.signals.enhanced_prompt.connect(self._apply_enhanced_prompt)
        self.worker.signals.progress.connect(self.set_progress)
        self.worker.signals.status.connect(lambda text: self.find(QLabel, "progressStatusLabel").setText(text))
        self.worker.signals.log.connect(self.append_log)
        self.worker.signals.image.connect(self.show_image)
        self.worker.signals.error.connect(lambda text: show_message_box(self.window, QMessageBox.Icon.Critical, "생성 오류", text))
        self.worker.signals.finished.connect(self.generation_finished)
        
        # UI 및 타이머 상태 업데이트
        self.find(QPushButton, "generateButton").setEnabled(False)
        self.find(QPushButton, "stopButton").setEnabled(True)
        self.generation_started_at = time.monotonic()
        self.elapsed_timer.start()

        self.loading_animation.start("이미지 생성 중...")
        self.append_log("이미지 생성을 시작했습니다.")
        
        # 🚀 단 1번만 백그라운드 스레드를 가동합니다.
        threading.Thread(target=self.worker.run, daemon=True).start()

    def stop_generation(self):
        if self.worker:
            self.worker.stop()
            self.append_log("생성 중지를 요청했습니다.")
            self.find(QLabel, "progressStatusLabel").setText("중단 중...")
        self.loading_animation.stop()

    def generation_finished(self, success):
        self.elapsed_timer.stop()
        self.loading_animation.stop()
        self.worker = None
        self.find(QPushButton, "generateButton").setEnabled(True)
        self.find(QPushButton, "stopButton").setEnabled(False)
        self.find(QLabel, "progressStatusLabel").setText("생성 완료" if success else "생성 실패 또는 중단")
        bar = self.find(QProgressBar, "progressBar")
        bar.setRange(0, 100)
        bar.setValue(100 if success else 0)
        self.find(QLabel, "progressPercentLabel").setText("100%" if success else "0%")
        update_execution_status(self.execution_status, 100 if success else 0, "생성 완료" if success else "생성 실패 또는 중단")
        if success:
            self.append_log("이미지 생성이 완료되었습니다.")

    def set_progress(self, value):
        """진행 상황을 표시. 실제 진행률이 들어오면 애니메이션 정지."""
        update_execution_status(self.execution_status, value, "이미지 생성 중")

        if value > 0:
            self.loading_animation.stop()

        self.loading_animation.set_real_progress(value)
        self.find(QLabel, "progressPercentLabel").setText(f"{value}%")

    def update_counter(self, edit_name, label_name):
        editor = self.find(QPlainTextEdit, edit_name)
        text = editor.toPlainText()
        if len(text) > 2000:
            editor.setPlainText(text[:2000])
            text = text[:2000]
        self.find(QLabel, label_name).setText(f"{len(text)} / 2000")

    def append_log(self, message):
        editor = self.find(QPlainTextEdit, "logTextEdit")
        editor.appendPlainText(f"[{datetime.now():%H:%M:%S}] {message}")

    def clear_logs(self):
        self.find(QPlainTextEdit, "logTextEdit").clear()
        self.append_log("로그를 초기화했습니다.")

    def show_image(self, path):
        self.current_image_path = path
        show_image(self.find(QLabel, "previewLabel"), path)

    def save_image_as(self):
        if not self.current_image_path:
            show_message_box(self.window, QMessageBox.Icon.Information, "알림", "저장할 이미지가 없습니다.")
            return
        target = save_image_as(self.window, self.current_image_path, self.output_dir)
        if target:
            self.append_log(f"이미지 저장: {target}")

    def open_output_folder(self):
        if open_output_folder(self.output_dir):
            self.append_log(f"출력 폴더 열기: {self.output_dir}")
        else:
            show_message_box(self.window, QMessageBox.Icon.Warning, "폴더 열기 실패", "출력 폴더를 열 수 없습니다.")

    def build_filename_prefix(self):
        return build_filename_prefix(self.config.output, self.output_dir)

    def close(self):
        if self.close_timer.isActive():
            return
        self.window.setEnabled(False)
        if self.worker:
            self.worker.stop()
            self.append_log("작업을 정리한 뒤 종료합니다...")

        self.find(QLabel, "progressStatusLabel").setText("종료 중...")
        self.find(QLabel, "progressPercentLabel").setText("")
        self.close_timer.start(300)
        
    def toggle_log(self):
        """로그창을 보이거나 숨기는 토글 함수 (아이콘 변경 포함)"""
        self.log_visible = not self.log_visible
        self.log_group.setVisible(self.log_visible)

        btn = self.find(QPushButton, "toggleLogButton")
        if btn:
            # 로그가 보이면 → 접기 아이콘(▼), 로그가 숨겨져 있으면 → 펼치기 아이콘(▲)
            if self.log_visible:
                btn.setIcon(self.icon_collapse)  # ▼
            else:
                btn.setIcon(self.icon_expand)    # ▲


def main():
    app = QApplication(sys.argv)

    qss_path = BASE_DIR / "assets" / "ui" / "style.qss"
    if qss_path.exists():
        app.setStyleSheet(qss_path.read_text(encoding="utf-8"))
    else:
        print(f"[QSS] 파일을 찾을 수 없음: {qss_path}")

    window = load_ui(UI_FILE)
    MainController(window)
    window.show()

    return app.exec()

if __name__ == "__main__":
    raise SystemExit(main())