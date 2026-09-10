from __future__ import annotations

import random

import sys
import threading
import time
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import (
    QEasingCurve,
    QEvent,
    QObject,
    QPropertyAnimation,
    QRegularExpression,
    Qt,
    QTimer,
    Signal,
)
from PySide6.QtGui import QIcon, QRegularExpressionValidator, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSlider,
    QDialog,
    QSpinBox,
    QTabWidget,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from assets.icons import (
    icon_rc,  # noqa: F401  (SVG 아이콘 리소스 등록용 - 직접 사용하진 않지만 import 자체가 필요함)
)
from app.gui.theme_manager import (
    AVAILABLE_THEMES,
    apply_theme,
    load_theme_choice,
    save_theme_choice,
)
from app.gui.ui_loader import load_ui

BASE_DIR = Path(__file__).resolve().parent

from app import (
    SAMPLER_NAMES,
    SCHEDULER_NAMES,
    ComfyUIApiClient,
    # Section modules
    ConnectionStatus,
    ElapsedTimer,
    GenerationWorker,
    LMStudioApiClient,
    LoadingAnimation,
    PromptEnhanceWorker,
    build_filename_prefix,
    build_generation_snapshot,
    build_negative_prompt,
    check_connection_silent,
    check_connection_status,
    create_execution_status,
    ensure_output_directory,
    get_config_manager,
    get_model_fetcher,
    get_model_registry,
    get_workflow_manager,
    load_external_prompts,
    normalize_prompt,
    open_output_folder,
    resolve_live_url,
    resolve_model_directory,
    save_image_as,
    scan_comfyui_model_names,
    show_image,
    show_message_box,
    update_execution_status,
)

# 추가 모듈 import
from app.core.model_status_service import ModelStatusService

UI_FILE = BASE_DIR / "assets" / "ui" / "main.ui"

# FaceDetailer 슬라이더 설정 명세: (키, 슬라이더 위젯 이름, 기본값, 배율, 64단위 여부)
FACEDETAILER_SLIDER_SPECS = [
    ("facedetailer_denoise", "facedetailerDenoiseSlider", 0.40, 100.0, False),
    ("facedetailer_steps", "facedetailerStepsSlider", 20, 1.0, False),
    ("facedetailer_cfg", "facedetailerCfgSlider", 4.0, 10.0, False),
    ("facedetailer_guide_size", "facedetailerGuideSizeSlider", 256, 1.0, True),
    ("facedetailer_max_size", "facedetailerMaxSizeSlider", 768, 1.0, True),
    ("facedetailer_feather", "facedetailerFeatherSlider", 5, 1.0, False),
    ("facedetailer_bbox_threshold", "facedetailerBboxThresholdSlider", 0.50, 100.0, False),
    ("facedetailer_bbox_dilation", "facedetailerBboxDilationSlider", 10, 1.0, False),
    ("facedetailer_bbox_crop_factor", "facedetailerBboxCropFactorSlider", 1.50, 100.0, False),
    ("facedetailer_sam_dilation", "facedetailerSamDilationSlider", 0, 1.0, False),
    ("facedetailer_sam_threshold", "facedetailerSamThresholdSlider", 0.93, 100.0, False),
    ("facedetailer_sam_bbox_expansion", "facedetailerSamBboxExpansionSlider", 0, 1.0, False),
    ("facedetailer_sam_mask_hint_threshold", "facedetailerSamMaskHintThresholdSlider", 0.70, 100.0, False),
    ("facedetailer_cycle", "facedetailerCycleSlider", 1, 1.0, False),
    ("facedetailer_drop_size", "facedetailerDropSizeSlider", 10, 1.0, False),
]


class MainController(QObject):
    model_list_ready = Signal(list, list)
    connection_result_ready = Signal(str, object)

    def __init__(self, window):
        super().__init__()
        self.window = window
        self._generation_lock = threading.Lock()
        self.config_manager = get_config_manager(
            BASE_DIR / "workflows" / "app_config.json"
        )
        self.config = self.config_manager.get()
        self.model_fetcher = get_model_fetcher(self.config_manager)
        self.model_status_service = ModelStatusService(self.model_fetcher)
        self.model_registry = get_model_registry()
        self.workflow_manager = get_workflow_manager(self.config_manager)
        self.output_dir = ensure_output_directory(
            str((BASE_DIR / self.config.output.directory).resolve())
        )
        self.worker = None
        self.current_image_path = None
        self.generation_started_at = None
        self.execution_status = create_execution_status()

        # 진행 상황 애니메이션
        self.loading_animation = LoadingAnimation(
            self.find(QProgressBar, "progressBar"),
            self.find(QLabel, "progressStatusLabel"),
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
            (
                "widthSpinBox",
                generation.width_min,
                generation.width_max,
                generation.default_width,
            ),
            (
                "heightSpinBox",
                generation.height_min,
                generation.height_max,
                generation.default_height,
            ),
        ):
            widget = self.find(QSpinBox, name)
            if widget:
                widget.setRange(minimum, maximum)
                widget.setValue(value)

        steps_slider = self.find(QSlider, "stepsSlider")
        if steps_slider:
            steps_slider.setRange(generation.steps_min, generation.steps_max)
            steps_slider.setValue(generation.default_steps)
        self.set_steps_value(generation.default_steps)

        cfg_slider = self.find(QSlider, "cfgSlider")
        if cfg_slider:
            cfg_slider.setRange(int(generation.cfg_min * 10), int(generation.cfg_max * 10))
            cfg_slider.setValue(int(round(generation.default_cfg * 10)))
        self.set_cfg_value(generation.default_cfg)
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
        self.find(QPlainTextEdit, "positivePromptEdit").setPlainText(
            "깊은 숲속을 산책중인 현대 한국 여성"
        )
        ext_prompts = load_external_prompts()
        self.find(QPlainTextEdit, "negativePromptEdit").setPlainText(
            ext_prompts.get("negative_default") or ""
        )
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
        # 공식 FaceDetailer sam_detection_hint 옵션과 동일하게 유지
        sam_hint_combo = self.find(QComboBox, "facedetailerSamDetectionHintComboBox")
        if sam_hint_combo is not None:
            sam_hint_combo.clear()
            sam_hint_combo.addItems(
                [
                    "center-1",
                    "horizontal-2",
                    "vertical-2",
                    "rect-4",
                    "diamond-4",
                    "mask-area",
                    "mask-points",
                    "mask-point-bbox",
                    "none",
                ]
            )
            sam_hint_combo.setCurrentText("center-1")

        sam_mask_neg_combo = self.find(
            QComboBox, "facedetailerSamMaskHintUseNegativeComboBox"
        )
        if sam_mask_neg_combo is not None:
            sam_mask_neg_combo.clear()
            sam_mask_neg_combo.addItems(["False", "Small", "Outter"])
            sam_mask_neg_combo.setCurrentText("False")

        # generateButton과 stopButton을 하나의 PlayStopButton으로 통합
        gen_stop_btn = self.find(QPushButton, "generateButton")
        if gen_stop_btn is not None:
            # PlayStopButton이 checkable인지 확인
            gen_stop_btn.setCheckable(True)
            gen_stop_btn.setChecked(False)
            # PlayStopButton의 toggled 시그널에 맞게 연결
            gen_stop_btn.toggled.connect(self._on_gen_stop_state_changed)
        self.find(QPushButton, "enhancePromptButton").clicked.connect(
            self.enhance_prompt_only
        )
        self.find(QPushButton, "loadConfigButton").clicked.connect(self.load_config)
        self.find(QPushButton, "saveConfigButton").clicked.connect(self.save_config)
        self.find(QPushButton, "restoreDefaultsButton").clicked.connect(
            self.restore_defaults
        )
        self.find(QPushButton, "exitButton").clicked.connect(self.close)
        self.find(QPushButton, "resetButton").clicked.connect(self.clear_logs)
        self.find(QPushButton, "openOutputFolderButton").clicked.connect(
            self.open_output_folder
        )
        self.find(QPushButton, "saveImageButton").clicked.connect(self.save_image_as)
        self.find(QPushButton, "lmCheckButton").clicked.connect(
            lambda: self.check_connection("lm")
        )
        self.find(QPushButton, "comfyCheckButton").clicked.connect(
            lambda: self.check_connection("comfy")
        )
        self.find(QPushButton, "browseModelFolderButton").clicked.connect(
            self.browse_model_folder
        )
        self.find(QComboBox, "lmModelCombo").currentTextChanged.connect(
            lambda text: self.log_model_selection("LM Studio", text)
        )
        self.find(QComboBox, "comfyModelCombo").currentTextChanged.connect(
            lambda text: self.log_model_selection("ComfyUI", text)
        )
        self.find(QComboBox, "comfyModelCombo").currentTextChanged.connect(
            self.apply_model_defaults
        )
        presets = {
            "preset_1024x1024": (1024, 1024),
            "preset_896x1152": (896, 1152),
            "preset_1152x896": (1152, 896),
            # 하위 호환용
            "preset_512x512": (512, 512),
            "preset_768x768": (768, 768),
            "preset_832x1216": (832, 1216),
            "preset_1216x832": (1216, 832),
        }
        for button_name, (width, height) in presets.items():
            btn = self.find(QPushButton, button_name)
            if btn is not None:
                btn.clicked.connect(
                    lambda checked=False, width=width, height=height: self.apply_preset(
                        width, height
                    )
                )
        self.find(QPlainTextEdit, "positivePromptEdit").textChanged.connect(
            lambda: self.update_counter(
                "positivePromptEdit", "positivePromptCounterLabel"
            )
        )
        self.find(QPlainTextEdit, "negativePromptEdit").textChanged.connect(
            lambda: self.update_counter(
                "negativePromptEdit", "negativePromptCounterLabel"
            )
        )
        self.find(QPlainTextEdit, "enhancePromptEdit").textChanged.connect(
            lambda: self.update_counter(
                "enhancePromptEdit", "enhancePromptCounterLabel"
            )
        )
        self.update_counter("positivePromptEdit", "positivePromptCounterLabel")
        self.update_counter("negativePromptEdit", "negativePromptCounterLabel")
        self.update_counter("enhancePromptEdit", "enhancePromptCounterLabel")

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
                "homeButton": 0,  # 홈
                "comfyButton": 1,  # ComfyUI
                "lmstudioButton": 2,  # LMStudio
                "settingsButton": 6,  # Settings
            }
            for btn_name, tab_index in tab_map.items():
                btn = self.find(QPushButton, btn_name)
                if btn is not None and tab_index < sidebar_tabs.count():
                    btn.clicked.connect(
                        lambda checked=False, i=tab_index: sidebar_tabs.setCurrentIndex(
                            i
                        )
                    )

        # 홈 탭 카드 버튼 → 해당 탭 전환 (NEW.ui 홈 화면)
        if sidebar_tabs is not None:
            home_tab_map = {
                "startButton": 1,  # 새 프로젝트 시작 → ComfyUI
                "comfyCardButton": 1,  # ComfyUI 카드 → ComfyUI
                "lmCardButton": 2,  # LMStudio 카드 → LMStudio
            }
            for btn_name, tab_index in home_tab_map.items():
                btn = self.find(QPushButton, btn_name)
                if btn is not None and tab_index < sidebar_tabs.count():
                    btn.clicked.connect(
                        lambda checked=False, i=tab_index: sidebar_tabs.setCurrentIndex(
                            i
                        )
                    )

        # ===== 로그창 토글 버튼 (아이콘 버전) =====
        toggle_btn = self.find(QPushButton, "toggleLogButton")
        if toggle_btn:
            toggle_btn.clicked.connect(self.toggle_log)
            self.log_group = self.find(QGroupBox, "logGroupBox")
            self.log_visible = True  # 처음에는 로그가 보이는 상태

            # ✅ Qt 내장 아이콘 사용하기 (별도 이미지 파일 필요 없음)
            # assets/icons 폴더의 실제 파일명과 정확히 일치해야 합니다!
            self.icon_collapse = QIcon(str(BASE_DIR / "assets/icons/toggle-off.svg"))
            self.icon_expand = QIcon(str(BASE_DIR / "assets/icons/toggle-on.svg"))
            # 처음에는 로그가 보이므로 '접기' 설정
            toggle_btn.setIcon(self.icon_collapse)
            toggle_btn.setText("")  # 혹시 모를 텍스트 제거

        # ===== 테마 선택기 (설정 탭) =====
        self._setup_theme_selector()

        # ===== 신규 UI 기능 연동 (ComfyCraft AI Easy Studio) =====
        self._setup_new_studio_features()

    def _setup_theme_selector(self):
        """상단 헤더의 테마 선택 콤보박스를 초기화하고 연결한다."""
        combo = self.find(QComboBox, "themeComboBox")
        if combo is not None:
            combo.blockSignals(True)
            combo.clear()
            for key, display_name in AVAILABLE_THEMES.items():
                combo.addItem(display_name, key)
            current_theme = load_theme_choice()
            idx = combo.findData(current_theme)
            if idx >= 0:
                combo.setCurrentIndex(idx)
            combo.blockSignals(False)
            combo.currentIndexChanged.connect(self._on_theme_changed)
            return

        settings_layout = self.window.findChild(QVBoxLayout, "settingsLayout")
        if settings_layout is None:
            return

        box = QGroupBox("🎨  테마")
        row = QHBoxLayout(box)
        row.setContentsMargins(12, 8, 12, 8)
        row.addWidget(QLabel("테마 선택"))
        combo = QComboBox()
        combo.setObjectName("themeComboBox")
        for key, display_name in AVAILABLE_THEMES.items():
            combo.addItem(display_name, key)
        combo.setCurrentIndex(max(0, combo.findData(load_theme_choice())))
        combo.currentIndexChanged.connect(self._on_theme_changed)
        row.addWidget(combo, 1)
        settings_layout.insertWidget(0, box)

    def _on_theme_changed(self, index: int):
        """테마 선택이 바뀌면 즉시 적용하고 설정 파일에 저장한다."""
        combo = self.sender()
        if not isinstance(combo, QComboBox):
            return
        key = combo.itemData(index)
        if not key:
            return
        app = QApplication.instance()
        if not isinstance(app, QApplication):
            return
        applied = apply_theme(app, key)
        if save_theme_choice(applied):
            display_name = AVAILABLE_THEMES.get(applied, applied)
            self.append_log(f"테마 변경: {display_name}")

    def setup_sidebar_animation(self):
        """사이드바에 마우스 호버 시 왼쪽으로 접히는 폭(maximumWidth) 애니메이션을 적용합니다."""
        sidebar = self.find(QFrame, "sidebar_frame")
        if not sidebar:
            return

        # 마우스 호버 이벤트를 받을 수 있도록 설정
        sidebar.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
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
        self.sidebar_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

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
        if hasattr(self, "sidebar_frame") and obj == self.sidebar_frame:
            if event.type() == QEvent.Type.HoverEnter:
                # 마우스 올림 → 펼치기(왼쪽에서 오른쪽으로 확장)
                self.sidebar_anim.stop()
                self.sidebar_anim.setStartValue(self.sidebar_frame.maximumWidth())
                self.sidebar_anim.setEndValue(self.sidebar_expanded_width)
                self.sidebar_anim.start()
                return True

            elif event.type() == QEvent.Type.HoverLeave:
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
        label.setStyleSheet("QLabel { background-color: transparent; border: none; }")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

    def _setup_elapsed_label_alignment(self):
        """elapsedLabel을 우측끝으로 정렬하기 위해 progressInfoLayout에 spacer 추가"""
        from PySide6.QtWidgets import QBoxLayout

        progress_info_layout = None
        # progressInfoLayout 찾기 (resultPanel 하위에서)
        result_panel = self.find(object, "resultPanel")
        if result_panel:
            for widget in result_panel.findChildren(object):
                if (
                    hasattr(widget, "objectName")
                    and widget.objectName() == "progressInfoLayout"
                ):
                    progress_info_layout = widget
                    break

        # progressInfoLayout를 직접 찾는 다른 방법 - parent의 layout 확인
        elapsed_label = self.find(QLabel, "elapsedLabel")
        if elapsed_label and elapsed_label.parent():
            parent = elapsed_label.parent()
            if hasattr(parent, "layout") and callable(parent.layout):
                progress_info_layout = parent.layout()

        # spacer 추가 (QBoxLayout 이 맞는 경우에만 안전하게 처리)
        if isinstance(progress_info_layout, QBoxLayout):
            spacer = QSpacerItem(
                0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            )
            # elapsedLabel 전에 spacer 삽입 (인덱스를 찾아서)
            elapsed_index = None
            for i in range(progress_info_layout.count()):
                item = progress_info_layout.itemAt(i)
                if item and hasattr(item, "widget") and item.widget() == elapsed_label:
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
            self.append_log(
                "[WARNING] LM Studio 서버를 찾을 수 없습니다. URL을 확인해주세요."
            )
            lm_label = self.find(QLabel, "lmStatusLabel")
            if lm_label:
                lm_label.setText("🔴서버 없음")
                lm_label.setProperty("status", "error")
                lm_label.style().unpolish(lm_label)
                lm_label.style().polish(lm_label)

        if resolved_comfy_url and resolved_comfy_url != comfy_url:
            self.find(QLineEdit, "comfyUrlEdit").setText(resolved_comfy_url)
            comfy_url = resolved_comfy_url
        elif not resolved_comfy_url:
            self.append_log(
                "[WARNING] ComfyUI 서버를 찾을 수 없습니다. URL을 확인해주세요."
            )
            comfy_label = self.find(QLabel, "comfyStatusLabel")
            if comfy_label:
                comfy_label.setText("🔴서버 없음")
                comfy_label.setProperty("status", "error")
                comfy_label.style().unpolish(comfy_label)
                comfy_label.style().polish(comfy_label)

        def fetch():
            # URL이 없으면 모델 목록 조회 건너뛰기
            if not lm_url and not comfy_url:
                self.model_list_ready.emit([], [])
                self.connection_result_ready.emit(
                    "lm",
                    ConnectionStatus(
                        service="LM Studio", url="", ok=False, message="URL 없음"
                    ),
                )
                self.connection_result_ready.emit(
                    "comfy",
                    ConnectionStatus(
                        service="ComfyUI", url="", ok=False, message="URL 없음"
                    ),
                )
                return

            status = self.model_status_service.fetch(lm_url, comfy_url)
            fallback_candidates = self.config_manager.get_model_base_paths()
            fallback_root = resolve_model_directory("", fallback_candidates)
            fallback_models = scan_comfyui_model_names(
                fallback_root, fallback_candidates
            )
            if not status.comfy_models or status.comfy_models == ["로드된 모델 없음"]:
                status.comfy_models = fallback_models or status.comfy_models
            elif not fallback_models:
                status.comfy_models = status.comfy_models
            elif status.comfy_models != fallback_models:
                status.comfy_models = fallback_models[:]

            # 실제 연결 상태 확인 (API 호출로 정확하게)
            lm_ok = check_connection_silent("lm", lm_url) if lm_url else False
            comfy_ok = (
                check_connection_silent("comfy", comfy_url) if comfy_url else False
            )

            self.model_list_ready.emit(status.lm_models, status.comfy_models)
            # 연결 상태도 함께 전달
            lm_status = ConnectionStatus(
                service="LM Studio",
                url=lm_url,
                ok=lm_ok,
                message="연결 성공" if lm_ok else "연결 실패",
            )
            comfy_status = ConnectionStatus(
                service="ComfyUI",
                url=comfy_url,
                ok=comfy_ok,
                message="연결 성공" if comfy_ok else "연결 실패",
            )
            self.connection_result_ready.emit("lm", lm_status)
            self.connection_result_ready.emit("comfy", comfy_status)

        threading.Thread(target=fetch, daemon=True).start()

    def _apply_models_result(self, lm_models, comfy_models):
        self.set_models(lm_models, comfy_models)
        self.loading_animation.stop()
        self.find(QLabel, "progressStatusLabel").setText("준비 완료")

    def set_models(self, lm_models, comfy_models):
        for name, values, selected in (
            ("lmModelCombo", lm_models, self.config.lmstudio.model),
            ("comfyModelCombo", comfy_models, self.config.comfyui.model),
        ):
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
        self.append_log(
            f"{service_name} 모델 목록 로드: {len(items)}개 [{', '.join(preview)}{suffix}]"
        )

    def log_model_selection(self, service_name, model_name):
        if not model_name or model_name == "로드된 모델 없음":
            return
        self.append_log(f"{service_name} 모델 선택 변경: {model_name}")

    def check_connection(self, which):
        raw_url = (
            self.find(QLineEdit, "lmUrlEdit" if which == "lm" else "comfyUrlEdit")
            .text()
            .strip()
        )
        resolved_url = resolve_live_url(which, raw_url)
        if resolved_url and resolved_url != raw_url:
            self.find(
                QLineEdit, "lmUrlEdit" if which == "lm" else "comfyUrlEdit"
            ).setText(resolved_url)
        self.update_connection_label(which, None)

        def check():
            ok = False
            try:
                # 극단적으로 빠른 타임아웃 (0.3초 이내)
                if which == "lm":
                    client = LMStudioApiClient(resolved_url)
                    response = client.get_models(timeout=0.3)
                else:
                    client = ComfyUIApiClient(resolved_url)
                    response = client.get_system_stats(timeout=0.3)
                # 실제 응답이 있고 상태 코드가 400 미만이어야 성공
                ok = bool(
                    response is not None and getattr(response, "status_code", 500) < 400
                )
            except Exception:  # noqa: BLE001  (연결 확인은 어떤 오류든 '연결 실패'로 처리하는 것이 의도)
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
        self.append_log(
            f"{status.service} 상태: {status.message} (실제 주소: {status.url})"
        )

    def is_lm_connected(self):
        if self.lm_connected:
            return True
        label = self.find(QLabel, "lmStatusLabel")
        return bool(label and "연결 성공" in label.text())

    def update_connection_label(self, which, ok):
        """연결 상태를 라벨과 배지 버튼에 반영합니다 (속성 기반)."""
        from app.gui.split_text_button import SplitTextButton

        label = self.find(
            QLabel, "lmStatusLabel" if which == "lm" else "comfyStatusLabel"
        )
        badge = self.find(
            QPushButton, "lmStatusBtn" if which == "lm" else "comfyStatusBtn"
        )
        status = "pending" if ok is None else ("success" if ok else "error")

        if label:
            if ok is None:
                label.setText("📡 연결 중...")
            else:
                label.setText("🟢연결 성공" if ok else "🔴연결 실패")
            # 하드코딩된 색상 대신 속성 설정 (QSS에서 처리)
            label.setProperty("status", status)
            label.style().unpolish(label)
            label.style().polish(label)

        if badge:
            if which == "comfy":
                badge.setText(
                    "🎨 ComfyUI 📡 확인 중..."
                    if ok is None
                    else ("🎨 ComfyUI 🟢 준비 완료" if ok else "🎨 ComfyUI 🔴 미연결")
                )
            else:
                badge.setText(
                    "💬 LM Studio 📡 확인 중..."
                    if ok is None
                    else ("💬 LM Studio 🟢 준비 완료" if ok else "💬 LM Studio 🔴 미연결")
                )
            # SplitTextButton이면 setStatus() 사용, 아니면 속성 설정 (QSS에서 처리)
            if isinstance(badge, SplitTextButton):
                badge.setStatus(status)
            else:
                badge.setProperty("status", status)
                badge.style().unpolish(badge)
                badge.style().polish(badge)

    def browse_model_folder(self):
        folder = QFileDialog.getExistingDirectory(self.window, "ComfyUI 모델 폴더 선택")
        if folder:
            self.find(QLineEdit, "comfyModelPathEdit").setText(folder)
            self.update_model_path_status(folder)

    def update_model_path_status(self, path):
        path_obj = Path(path).expanduser()
        valid = path_obj.exists() and any(
            (path_obj / item).is_dir()
            for item in (
                "checkpoints",
                "unet",
                "diffusion_models",
                "vae",
                "clip",
                "loras",
            )
        )
        label = self.find(QLabel, "modelPathStatusLabel")
        if label:
            label.setText(
                "✓ ComfyUI 모델 폴더 확인됨" if valid else "✗ 올바른 모델 폴더가 아닙니다"
            )
            # 하드코딩된 색상 대신 속성 설정 (QSS에서 처리)
            label.setProperty("status", "success" if valid else "error")
            label.style().unpolish(label)
            label.style().polish(label)

    def get_cfg_value(self) -> float:
        cfg_slider = self.find(QSlider, "cfgSlider")
        return (cfg_slider.value() / 10.0) if cfg_slider else 3.5

    def set_cfg_value(self, val: float):
        cfg_slider = self.find(QSlider, "cfgSlider")
        if cfg_slider:
            cfg_slider.blockSignals(True)
            cfg_slider.setValue(int(round(val * 10)))
            cfg_slider.blockSignals(False)
        cfg_label = self.find(QLabel, "cfgValueLabel")
        if cfg_label:
            cfg_label.setText(f"{val:.1f}")

    def get_steps_value(self) -> int:
        steps_slider = self.find(QSlider, "stepsSlider")
        return steps_slider.value() if steps_slider else 24

    def set_steps_value(self, val: int):
        steps_slider = self.find(QSlider, "stepsSlider")
        if steps_slider:
            steps_slider.blockSignals(True)
            steps_slider.setValue(int(val))
            steps_slider.blockSignals(False)
        steps_label = self.find(QLabel, "stepsValueLabel")
        if steps_label:
            steps_label.setText(str(val))

    def apply_model_defaults(self, model_name):
        if not model_name or model_name == "로드된 모델 없음":
            return
        profile = self.model_registry.detect(model_name)
        self.set_steps_value(profile.default_steps)
        self.set_cfg_value(profile.default_cfg)
        display = next(
            (
                key
                for key, value in SAMPLER_NAMES.items()
                if value == profile.sampler_name
            ),
            profile.sampler_name,
        )
        self.find(QComboBox, "samplerComboBox").setCurrentText(display)

        # 모델별 네거티브 프롬프트 동적 제어 (FLUX/ZImage는 숨김, SDXL은 표시)
        neg_frame = self.find(QFrame, "negativePromptFrame")
        if neg_frame:
            m_lower = model_name.lower()
            is_flux_or_zimage = any(k in m_lower for k in ["flux", "zimage", "z_image", "turbo"])
            neg_frame.setVisible(not is_flux_or_zimage)

        # 추천 설정 안내 배지 갱신
        notice_label = self.find(QLabel, "modelProfileNoticeLabel")
        if notice_label:
            notice_label.setText(f"✓ {profile.name.upper()} 최적 설정 적용됨 (CFG {profile.default_cfg} / {profile.default_steps}스텝)")
        scheduler_combo = self.find(QComboBox, "schedulerComboBox")
        if scheduler_combo is not None:
            scheduler_combo.setCurrentText(
                profile.scheduler if profile.scheduler in SCHEDULER_NAMES else "normal"
            )
        denoise_spin = self.find(QDoubleSpinBox, "denoiseSpinBox")
        if denoise_spin is not None:
            denoise_spin.setValue(1.0)

        # 로드한 모델 프로파일 정보를 로그에 표시
        profile_info = f"모델 프로파일 로드: [{profile.family.upper()}] {profile.name}"
        if profile.workflow_type == "gguf":
            profile_info += " (GGUF)"
        elif profile.workflow_type == "zimage":
            profile_info += " (ZImage-GGUF)"
        elif profile.workflow_type == "flux_gguf":
            profile_info += " (Flux-GGUF)"
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
        self.config_manager.set_config(self.config)

        if file_exists:
            message = f"저장된 설정을 불러왔습니다. ({config_path.name})"
            show_message_box(
                self.window, QMessageBox.Icon.Information, "설정 불러오기", message
            )
            self.append_log(message)
        else:
            message = f"설정 파일이 없어 기본값을 불러왔습니다. ({config_path.name})"
            show_message_box(
                self.window, QMessageBox.Icon.Information, "기본값 로드", message
            )
            self.append_log(message)

        self.find(QLineEdit, "lmUrlEdit").setText(self.config.lmstudio.url)
        self.find(QLineEdit, "comfyUrlEdit").setText(self.config.comfyui.url)
        if self.config.lmstudio.model:
            self.find(QComboBox, "lmModelCombo").setCurrentText(
                self.config.lmstudio.model
            )
        if self.config.comfyui.model:
            self.find(QComboBox, "comfyModelCombo").setCurrentText(
                self.config.comfyui.model
            )

        model_paths = self.config_manager.get_model_base_paths()
        if model_paths:
            first_path = str(model_paths[0])
            self.find(QLineEdit, "comfyModelPathEdit").setText(first_path)
            self.update_model_path_status(first_path)

        self.find(QSpinBox, "widthSpinBox").setValue(
            self.config.generation.default_width
        )
        self.find(QSpinBox, "heightSpinBox").setValue(
            self.config.generation.default_height
        )
        self.set_steps_value(self.config.generation.default_steps)
        self.set_cfg_value(self.config.generation.default_cfg)
        self.find(QSpinBox, "seedSpinBox").setValue(self.config.generation.default_seed)

        sampler_name = self.config.workflow.sampler_name
        sampler_display = next(
            (label for label, value in SAMPLER_NAMES.items() if value == sampler_name),
            sampler_name,
        )
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
        except Exception:  # noqa: BLE001, S110  (화면 배치 실패는 무시하고 계속 진행하는 것이 의도)
            pass
        # (이전 QSplitter 비율 코드는 구조 변경으로 제거됨)

    def _render_markdown_file(self, file_path: Path) -> str:
        """Markdown 파일을 읽어 HTML 문자열로 변환 (공통 헬퍼)"""
        if not file_path.exists():
            return f"<p style='color:red;'>⚠️ {file_path.name} 파일을 찾을 수 없습니다.</p>"
        try:
            readme_text = file_path.read_text(encoding="utf-8")
            try:
                import markdown

                return markdown.markdown(readme_text, extensions=["tables"])
            except ImportError:
                return "<pre>" + readme_text + "</pre>"
        except Exception as e:
            return f"<p style='color:red;'>{file_path.name} 읽기 오류: {e}</p>"

    def _setup_help_tab(self):
        """도움말 탭의 helpBrowser(main.ui에 정의됨)에 README.md와 INSTALLATION.md 내용을 채운다."""
        browser = self.find(QTextBrowser, "helpBrowser")
        if browser is None:
            return

        readme_path = BASE_DIR / "assets" / "help" / "README.md"
        install_path = BASE_DIR / "assets" / "help" / "INSTALLATION.md"

        html_parts = [
            "<h1 style='color: #0f172a; font-size: 24px; margin-bottom: 8px;'>📖 프로그램 도움말 v0.3</h1><hr style='border-color: #e2e8f0;'>",
            self._render_markdown_file(readme_path),
            "<hr style='border-color: #e2e8f0; margin: 24px 0;'><h2 style='color: #0f172a; font-size: 20px;'>🔧 설치 및 트러블슈팅</h2>",
            self._render_markdown_file(install_path),
        ]

        browser.setHtml("\n".join(html_parts))

    def save_config(self):
        """설정 값을 저장합니다."""
        # LM Studio URL 및 모델 업데이트
        self.config.lmstudio.url = self.find(QLineEdit, "lmUrlEdit").text().strip()
        self.config.lmstudio.model = self.find(QComboBox, "lmModelCombo").currentText()

        # ComfyUI URL 및 모델 업데이트
        self.config.comfyui.url = self.find(QLineEdit, "comfyUrlEdit").text().strip()
        self.config.comfyui.model = self.find(
            QComboBox, "comfyModelCombo"
        ).currentText()

        # ComfyUI 모델 경로 업데이트 (첫 번째 경로만 저장하는 방식으로 유지)
        model_path = self.find(QLineEdit, "comfyModelPathEdit").text().strip()
        if model_path:
            self.config.comfyui_model_paths = [model_path] + [
                p for p in self.config.comfyui_model_paths if p != model_path
            ]
        else:
            self.config.comfyui_model_paths = []

        # Generation options 저장
        self.config.generation.default_width = self.find(
            QSpinBox, "widthSpinBox"
        ).value()
        self.config.generation.default_height = self.find(
            QSpinBox, "heightSpinBox"
        ).value()
        self.config.generation.default_steps = self.get_steps_value()
        self.config.generation.default_cfg = self.get_cfg_value()
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
        self.config_manager.set_config(self.config)
        if self.config_manager.save():
            show_message_box(
                self.window,
                QMessageBox.Icon.Information,
                "저장 완료",
                "설정이 성공적으로 저장되었습니다.",
            )
        else:
            show_message_box(
                self.window,
                QMessageBox.Icon.Warning,
                "저장 실패",
                "설정 저장에 실패했습니다. 경로 권한을 확인해주세요.",
            )

    def restore_defaults(self):
        generation = self.config.generation
        self.find(QSpinBox, "widthSpinBox").setValue(generation.default_width)
        self.find(QSpinBox, "heightSpinBox").setValue(generation.default_height)
        self.set_steps_value(generation.default_steps)
        self.set_cfg_value(generation.default_cfg)
        self.find(QSpinBox, "seedSpinBox").setValue(generation.default_seed)
        self.find(QComboBox, "samplerComboBox").setCurrentText("DPM++ 2M·균형")
        scheduler_combo = self.find(QComboBox, "schedulerComboBox")
        if scheduler_combo is not None:
            scheduler_combo.setCurrentText("normal")
        denoise_spin = self.find(QDoubleSpinBox, "denoiseSpinBox")
        if denoise_spin is not None:
            denoise_spin.setValue(1.0)

        # FaceDetailer 옵션도 기본값으로 초기화
        self._reset_facedetailer_to_defaults()

    def _set_fd_slider(self, slider_name, value):
        """FaceDetailer 슬라이더 값을 안전하게 설정 (라벨은 시그널로 자동 갱신)."""
        slider = self.find(QSlider, slider_name)
        if slider is not None:
            try:
                slider.setValue(int(value))
            except Exception:
                pass

    def _reset_facedetailer_to_defaults(self):
        """FaceDetailer 체크박스/슬라이더/콤보박스를 기본값으로 되돌림."""
        fd_check = self.find(QCheckBox, "facedetailerCheckBox")
        if fd_check is not None:
            fd_check.setChecked(False)
        self._set_fd_slider("facedetailerDenoiseSlider", 40)
        self._set_fd_slider("facedetailerStepsSlider", 20)
        self._set_fd_slider("facedetailerCfgSlider", 40)
        self._set_fd_slider("facedetailerFeatherSlider", 5)
        self._set_fd_slider("facedetailerDropSizeSlider", 10)
        self._set_fd_slider("facedetailerGuideSizeSlider", 4)
        self._set_fd_slider("facedetailerMaxSizeSlider", 12)
        self._set_fd_slider("facedetailerCycleSlider", 1)
        self._set_fd_slider("facedetailerBboxThresholdSlider", 50)
        self._set_fd_slider("facedetailerBboxDilationSlider", 10)
        self._set_fd_slider("facedetailerBboxCropFactorSlider", 150)
        self._set_fd_slider("facedetailerSamThresholdSlider", 93)
        self._set_fd_slider("facedetailerSamDilationSlider", 0)
        self._set_fd_slider("facedetailerSamBboxExpansionSlider", 0)
        self._set_fd_slider("facedetailerSamMaskHintThresholdSlider", 70)
        hint_combo = self.find(QComboBox, "facedetailerSamDetectionHintComboBox")
        if hint_combo is not None:
            hint_combo.setCurrentText("center-1")
        neg_combo = self.find(QComboBox, "facedetailerSamMaskHintUseNegativeComboBox")
        if neg_combo is not None:
            neg_combo.setCurrentText("False")

    def capture_snapshot(self):
        prompt_text = self.find(QPlainTextEdit, "positivePromptEdit").toPlainText()
        negative_text = self.find(QPlainTextEdit, "negativePromptEdit").toPlainText()
        # enhancePromptEdit 내용도 스냅샷에 포함 (이미지 생성 시 LM Studio 재요청 방지용)
        enhance_prompt_text = self.find(
            QPlainTextEdit, "enhancePromptEdit"
        ).toPlainText()
        generation_settings = build_generation_snapshot(
            {
                "width": self.find(QSpinBox, "widthSpinBox").value(),
                "height": self.find(QSpinBox, "heightSpinBox").value(),
                "steps": self.get_steps_value(),
                "cfg": self.get_cfg_value(),
                "seed": self.find(QSpinBox, "seedSpinBox").value(),
                "sampler": SAMPLER_NAMES.get(
                    self.find(QComboBox, "samplerComboBox").currentText(), "euler"
                ),
                "scheduler": self.find(QComboBox, "schedulerComboBox").currentText()
                if self.find(QComboBox, "schedulerComboBox") is not None
                else "normal",
                "denoise": float(
                    self.find(QDoubleSpinBox, "denoiseSpinBox").value()
                    if self.find(QDoubleSpinBox, "denoiseSpinBox") is not None
                    else 1.0
                ),
            }
        )
        # FaceDetailer 설정 스냅샷 수집
        fd_values = {}
        for key, slider_name, default, factor, is_step_64 in FACEDETAILER_SLIDER_SPECS:
            s = self.find(QSlider, slider_name)
            if not s:
                fd_values[key] = default
            elif is_step_64:
                fd_values[key] = s.value() * 64
            elif factor != 1.0:
                fd_values[key] = round(s.value() / factor, 2)
            else:
                fd_values[key] = s.value()

        hint_combo = self.find(QComboBox, "facedetailerSamDetectionHintComboBox")
        neg_combo = self.find(QComboBox, "facedetailerSamMaskHintUseNegativeComboBox")
        fd_values["facedetailer_sam_detection_hint"] = (
            hint_combo.currentText() if hint_combo else "center-1"
        )
        fd_values["facedetailer_sam_mask_hint_use_negative"] = (
            neg_combo.currentText() if neg_combo else "False"
        )
        fd_values["facedetailer_enabled"] = bool(
            self.find(QCheckBox, "facedetailerCheckBox").isChecked()
            if self.find(QCheckBox, "facedetailerCheckBox")
            else False
        )

        snapshot = {
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
        }
        snapshot.update(fd_values)
        return snapshot

    def _restore_facedetailer_from_snapshot(self, snap):
        """스냅샷 딕셔너리에서 FaceDetailer 옵션을 UI로 복원."""
        if "facedetailer_enabled" in snap:
            fd_check = self.find(QCheckBox, "facedetailerCheckBox")
            if fd_check is not None:
                fd_check.setChecked(bool(snap.get("facedetailer_enabled", False)))

        for key, slider_name, _default, factor, is_step_64 in FACEDETAILER_SLIDER_SPECS:
            if key in snap:
                try:
                    val = float(snap[key])
                    if is_step_64:
                        slider_val = round(val / 64)
                    elif factor != 1.0:
                        slider_val = round(val * factor)
                    else:
                        slider_val = int(val)
                    self._set_fd_slider(slider_name, slider_val)
                except Exception:
                    pass

        if "facedetailer_sam_detection_hint" in snap:
            hint_combo = self.find(QComboBox, "facedetailerSamDetectionHintComboBox")
            if hint_combo is not None:
                hint_value = str(snap.get("facedetailer_sam_detection_hint", "center-1"))
                if hint_value not in (
                    "center-1", "horizontal-2", "vertical-2", "rect-4",
                    "diamond-4", "mask-area", "mask-points", "mask-point-bbox", "none",
                ):
                    hint_value = "center-1"
                hint_combo.setCurrentText(hint_value)

        if "facedetailer_sam_mask_hint_use_negative" in snap:
            neg_combo = self.find(QComboBox, "facedetailerSamMaskHintUseNegativeComboBox")
            if neg_combo is not None:
                neg_combo.setCurrentText(str(snap.get("facedetailer_sam_mask_hint_use_negative", "False")))

    def enhance_prompt_only(self):
        prompt_text = self.find(QPlainTextEdit, "positivePromptEdit").toPlainText()
        prompt = normalize_prompt(prompt_text)
        if not prompt:
            show_message_box(
                self.window,
                QMessageBox.Icon.Warning,
                "프롬프트 필요",
                "향상시킬 프롬프트를 입력해주세요.",
            )
            return

        lm_url = self.find(QLineEdit, "lmUrlEdit").text().strip()
        lm_model = self.find(QComboBox, "lmModelCombo").currentText()
        if not lm_model or lm_model == "로드된 모델 없음":
            show_message_box(
                self.window,
                QMessageBox.Icon.Warning,
                "모델 필요",
                "LM Studio 모델을 선택해주세요.",
            )
            return

        # LM Studio 연결 확인
        lm_connected = self.is_lm_connected()
        if not lm_connected:
            show_message_box(
                self.window,
                QMessageBox.Icon.Warning,
                "연결 필요",
                "LM Studio가 연결되지 않았습니다. 연결 확인 후 다시 시도해주세요.",
            )
            return

        self.append_log("프롬프트 향상 중...")
        self.find(QLabel, "progressStatusLabel").setText("프롬프트 향상 중...")

        ext_prompts = load_external_prompts()

        # ComfyUI 모델 타입에 따라 시스템 프롬프트 자동 선택 (generation.py와 동일 로직)
        comfy_model_name = self.find(QComboBox, "comfyModelCombo").currentText()
        profile = self.model_registry.detect(comfy_model_name)
        manager = self.workflow_manager

        is_flux = bool(
            profile.workflow_type == "flux_gguf"
            or manager.is_flux_model(comfy_model_name)
            or profile.family == "flux"
        )
        is_zimage = bool(
            manager.is_zimage_model(comfy_model_name)
            or profile.workflow_type == "zimage"
        )

        # LM Studio에는 영문 시스템 프롬프트 사용 (출력 언어 준수율 향상)
        # use_korean_prompt 설정과 무관하게 영문 프롬프트(_en) 사용
        if is_flux or is_zimage:
            self.append_log(
                f"[AI 자동 분석] '{comfy_model_name}' 모델 감지: '문장형' 프롬프트 지시문을 사용합니다."
            )
            system_prompt = ext_prompts.get("system_prompt_flux_en") or ""
        else:
            self.append_log(
                f"[AI 자동 분석] '{comfy_model_name}' 모델 감지: '태그형(쉼표 구분)' 프롬프트 지시문을 사용합니다."
            )
            system_prompt = ext_prompts.get("system_prompt_sdxl_en") or ""

        # 백업용 기본값
        if not system_prompt:
            system_prompt = ext_prompts.get("system_prompt_sdxl_en") or ""

        # PromptEnhanceWorker 사용
        self._prompt_enhance_worker = PromptEnhanceWorker(
            lm_url=lm_url,
            model_name=lm_model,
            prompt=prompt,
            system_prompt=system_prompt,
            timeout=self.config.lmstudio.timeout_seconds,
        )
        self._prompt_enhance_worker.finished_signal.connect(self._on_prompt_enhanced)
        self._prompt_enhance_worker.error_signal.connect(self._on_prompt_enhance_error)
        self._prompt_enhance_worker.debug_signal.connect(
            lambda msg: self.append_log(msg)
        )
        self._prompt_enhance_worker.start()

    def _on_prompt_enhanced(self, enhanced_prompt: str):
        """프롬프트 향상 성공 시 호출"""
        self._apply_enhanced_prompt(enhanced_prompt)

    def _on_prompt_enhance_error(self, error_msg: str):
        """프롬프트 향상 실패 시 호출"""
        self.append_log(f"프롬프트 향상 실패: {error_msg}")
        show_message_box(
            self.window, QMessageBox.Icon.Warning, "프롬프트 향상 실패", error_msg
        )
        self.find(QLabel, "progressStatusLabel").setText("준비 완료")

    def _apply_enhanced_prompt(self, enhanced_prompt):
        """향상된 프롬프트를 enhancePromptEdit에 적용"""
        prompt_edit = self.find(QPlainTextEdit, "enhancePromptEdit")
        if prompt_edit:
            prompt_edit.setPlainText(enhanced_prompt)
        else:
            self.append_log("[ERROR] enhancePromptEdit을 찾을 수 없음!")
        self.append_log(f"프롬프트 향상 완료: {enhanced_prompt[:100]}...")
        self.find(QLabel, "progressStatusLabel").setText("준비 완료")

    def start_generation(self):
        with self._generation_lock:
            if self.worker:
                return
            # 시드 고정이 활성화되어 있지 않으면 매번 새 랜덤 시드 자동 적용
            if not getattr(self, "is_seed_locked", False):
                rand_seed = random.randint(100000000, 999999999)
                seed_spin = self.find(QSpinBox, "seedSpinBox")
                if seed_spin:
                    seed_spin.setValue(rand_seed)
            snapshot = self.capture_snapshot()
            if not snapshot["prompt"]:
                show_message_box(
                    self.window,
                    QMessageBox.Icon.Warning,
                    "프롬프트 필요",
                    "프롬프트를 입력해주세요.",
                )
                return

            # 워커 인스턴스 생성
            self.worker = GenerationWorker(self, snapshot)

        # 🚀 중복되지 않도록 시그널 이벤트를 딱 1번만 연결합니다.
        self.worker.signals.enhanced_prompt.connect(self._apply_enhanced_prompt)
        self.worker.signals.progress.connect(self.set_progress)
        self.worker.signals.status.connect(
            lambda text: self.find(QLabel, "progressStatusLabel").setText(text)
        )
        self.worker.signals.log.connect(self.append_log)
        self.worker.signals.image.connect(lambda path: self.show_image(path, add_history=True))
        self.worker.signals.error.connect(
            lambda text: show_message_box(
                self.window, QMessageBox.Icon.Critical, "생성 오류", text
            )
        )
        self.worker.signals.finished.connect(self.generation_finished)

        # UI 및 타이머 상태 업데이트
        self.generation_started_at = time.monotonic()
        self.elapsed_timer.start()

        self.loading_animation.start("이미지 생성 중...")
        self.append_log("이미지 생성을 시작했습니다.")

        # 🚀 단 1번만 백그라운드 스레드를 가동합니다.
        threading.Thread(target=self.worker.run, daemon=True).start()

    def stop_generation(self):
        with self._generation_lock:
            if self.worker:
                self.worker.stop()
                self.append_log("생성 중지를 요청했습니다.")
                self.find(QLabel, "progressStatusLabel").setText("중단 중...")
        self.loading_animation.stop()

    def _on_gen_stop_state_changed(self, checked):
        """PlayStopButton의 toggled 시그널 핸들러.
        파랑(checked=False, "이미지 생성 시작") 클릭 → 빨강으로 변화 → toggled(True) → 생성 시작
        빨강(checked=True, "정지") 클릭 → 파랑으로 변화 → toggled(False) → 생성 중지
        """
        if checked:
            # 파랑 "이미지 생성 시작"에서 클릭 → 빨강 "정지"로 변화 → 생성 시작
            self.start_generation()
        else:
            # 빨강 "정지"에서 클릭 → 파랑 "이미지 생성 시작"으로 변화 → 생성 중지
            self.stop_generation()

    def generation_finished(self, success):
        self.elapsed_timer.stop()
        self.loading_animation.stop()
        with self._generation_lock:
            self.worker = None
        btn = self.find(QPushButton, "generateButton")
        if btn is not None:
            btn.setChecked(False)
        self.find(QLabel, "progressStatusLabel").setText(
            "생성 완료" if success else "생성 실패 또는 중단"
        )
        bar = self.find(QProgressBar, "progressBar")
        bar.setRange(0, 100)
        bar.setValue(100 if success else 0)
        self.find(QLabel, "progressPercentLabel").setText("100%" if success else "0%")
        update_execution_status(
            self.execution_status,
            100 if success else 0,
            "생성 완료" if success else "생성 실패 또는 중단",
        )
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
        editor.appendPlainText(f"[{datetime.now():%H:%M:%S}] {message}")  # noqa: DTZ005  (로그 표시용 로컬 시간이므로 의도됨)

    def clear_logs(self):
        self.find(QPlainTextEdit, "logTextEdit").clear()
        self.append_log("로그를 초기화했습니다.")

    def show_image(self, path, add_history=False):
        self.current_image_path = path
        show_image(self.find(QLabel, "previewLabel"), path)
        # 새로 생성된 이미지일 때만 히스토리(썸네일)에 추가
        if add_history:
            try:
                snapshot = self.capture_snapshot()
                self.add_to_history(path, snapshot)
            except Exception as e:
                print(f"[경고] 히스토리 추가 실패: {e}")

    def save_image_as(self):
        if not self.current_image_path:
            show_message_box(
                self.window,
                QMessageBox.Icon.Information,
                "알림",
                "저장할 이미지가 없습니다.",
            )
            return
        target = save_image_as(self.window, self.current_image_path, self.output_dir)
        if target:
            self.append_log(f"이미지 저장: {target}")

    def open_output_folder(self):
        if open_output_folder(self.output_dir):
            self.append_log(f"출력 폴더 열기: {self.output_dir}")
        else:
            show_message_box(
                self.window,
                QMessageBox.Icon.Warning,
                "폴더 열기 실패",
                "출력 폴더를 열 수 없습니다.",
            )

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
                btn.setIcon(self.icon_expand)  # ▲


    def _setup_new_studio_features(self):
        """ComfyCraft AI Easy Studio 신규 위젯 및 인터랙션 연결"""
        self.generation_history = []
        self.is_seed_locked = False

        # 1. 슬라이더 동기화 (CFG)
        cfg_slider = self.find(QSlider, "cfgSlider")
        cfg_label = self.find(QLabel, "cfgValueLabel")
        if cfg_slider:
            def on_cfg_slider(val):
                if cfg_label:
                    cfg_label.setText(f"{val / 10.0:.1f}")

            cfg_slider.valueChanged.connect(on_cfg_slider)
            on_cfg_slider(cfg_slider.value())

        # 2. 슬라이더 동기화 (Steps)
        steps_slider = self.find(QSlider, "stepsSlider")
        steps_label = self.find(QLabel, "stepsValueLabel")
        if steps_slider:
            def on_steps_slider(val):
                if steps_label:
                    steps_label.setText(str(val))

            steps_slider.valueChanged.connect(on_steps_slider)
            on_steps_slider(steps_slider.value())

        # 3. 시드 제어 (랜덤 및 고정)
        rand_seed_btn = self.find(QPushButton, "randomSeedButton")
        if rand_seed_btn:
            rand_seed_btn.clicked.connect(self._generate_random_seed)

        lock_seed_btn = self.find(QPushButton, "lockSeedButton")
        if lock_seed_btn:
            lock_seed_btn.toggled.connect(self._on_lock_seed_toggled)

        # 4. 영문 프롬프트 원클릭 복사
        copy_prompt_btn = self.find(QPushButton, "copyPromptButton")
        if copy_prompt_btn:
            copy_prompt_btn.clicked.connect(self._copy_enhanced_prompt)

        # 5. 클립보드 이미지 복사
        copy_img_btn = self.find(QPushButton, "copyImageButton")
        if copy_img_btn:
            copy_img_btn.clicked.connect(self._copy_image_to_clipboard)

        # 6. 얼굴 보정 토글 패널 및 슬라이더 동기화
        fd_check = self.find(QCheckBox, "facedetailerCheckBox")
        fd_panel = self.find(QFrame, "facedetailerPanel")
        if fd_check and fd_panel:
            fd_panel.setVisible(fd_check.isChecked())
            fd_check.toggled.connect(lambda checked: fd_panel.setVisible(checked))

        # 6-0. [?] 얼굴 보정 도움말 버튼 (main.ui의 facedetailerHelpBtn 연동)
        fd_help_btn = self.find(QPushButton, "facedetailerHelpBtn")
        if fd_help_btn:
            fd_help_btn.clicked.connect(self._show_facedetailer_guide)

        # FaceDetailer 슬라이더 -> 수치 라벨(QLabel) 동기화
        # (main.ui에서는 SpinBox가 제거되고 ValueLabel로 교체됨)
        def _sync_fd_label(slider_name, label_name, fmt):
            slider = self.find(QSlider, slider_name)
            label = self.find(QLabel, label_name)
            if slider and label:
                def on_val(val, _lbl=label, _fmt=fmt):
                    try:
                        _lbl.setText(_fmt(val))
                    except Exception:
                        pass
                slider.valueChanged.connect(on_val)
                # 초기 표시도 맞춤
                try:
                    label.setText(fmt(slider.value()))
                except Exception:
                    pass

        _sync_fd_label("facedetailerDenoiseSlider", "facedetailerDenoiseValueLabel", lambda v: f"{v / 100.0:.2f}")
        _sync_fd_label("facedetailerStepsSlider", "facedetailerStepsValueLabel", lambda v: f"{int(v)}")
        _sync_fd_label("facedetailerCfgSlider", "facedetailerCfgValueLabel", lambda v: f"{v / 10.0:.1f}")
        _sync_fd_label("facedetailerFeatherSlider", "facedetailerFeatherValueLabel", lambda v: f"{int(v)}")
        _sync_fd_label("facedetailerDropSizeSlider", "facedetailerDropSizeValueLabel", lambda v: f"{int(v)}")
        _sync_fd_label("facedetailerGuideSizeSlider", "facedetailerGuideSizeValueLabel", lambda v: f"{int(v * 64)}")
        _sync_fd_label("facedetailerMaxSizeSlider", "facedetailerMaxSizeValueLabel", lambda v: f"{int(v * 64)}")
        _sync_fd_label("facedetailerCycleSlider", "facedetailerCycleValueLabel", lambda v: f"{int(v)}")
        _sync_fd_label("facedetailerBboxThresholdSlider", "facedetailerBboxThresholdValueLabel", lambda v: f"{v / 100.0:.2f}")
        _sync_fd_label("facedetailerBboxDilationSlider", "facedetailerBboxDilationValueLabel", lambda v: f"{int(v)}")
        _sync_fd_label("facedetailerBboxCropFactorSlider", "facedetailerBboxCropFactorValueLabel", lambda v: f"{v / 100.0:.2f}")
        _sync_fd_label("facedetailerSamThresholdSlider", "facedetailerSamThresholdValueLabel", lambda v: f"{v / 100.0:.2f}")
        _sync_fd_label("facedetailerSamDilationSlider", "facedetailerSamDilationValueLabel", lambda v: f"{int(v)}")
        _sync_fd_label("facedetailerSamBboxExpansionSlider", "facedetailerSamBboxExpansionValueLabel", lambda v: f"{int(v)}")
        _sync_fd_label("facedetailerSamMaskHintThresholdSlider", "facedetailerSamMaskHintThresholdValueLabel", lambda v: f"{v / 100.0:.2f}")

        # 6-1. 네거티브 프롬프트 패널 초기 표시 상태 (SDXL 등 필요 모델 선택 시에만 표시)
        neg_frame = self.find(QFrame, "negativePromptFrame")
        if neg_frame:
            curr_model = self.find(QComboBox, "comfyModelCombo").currentText() if self.find(QComboBox, "comfyModelCombo") else ""
            if curr_model and curr_model != "로드된 모델 없음":
                m_lower = curr_model.lower()
                is_flux_or_zimage = any(k in m_lower for k in ["flux", "zimage", "z_image", "turbo"])
                neg_frame.setVisible(not is_flux_or_zimage)
            else:
                neg_frame.setVisible(False)

        # 7. 접이식 고급 설정 토글 (얼굴 보정과 동일한 체크박스 방식으로 통일)
        adv_check = self.find(QCheckBox, "advancedToggleBtn")
        adv_content = self.find(QWidget, "advancedContentWidget")
        if adv_check and adv_content:
            adv_content.setVisible(adv_check.isChecked())
            adv_check.toggled.connect(lambda checked: adv_content.setVisible(checked))

        # 8. 연결 상태 배지 및 설정 버튼 다이얼로그 연동
        comfy_btn = self.find(QPushButton, "comfyStatusBtn")
        if comfy_btn:
            comfy_btn.clicked.connect(self._show_settings_dialog)

        lm_btn = self.find(QPushButton, "lmStatusBtn")
        if lm_btn:
            lm_btn.clicked.connect(self._show_settings_dialog)

        settings_btn = self.find(QPushButton, "settingsButton")
        if settings_btn:
            settings_btn.clicked.connect(self._show_settings_dialog)

        # 9. 상단 도움말 버튼 연동
        help_btn = self.find(QPushButton, "helpButton")
        if help_btn:
            help_btn.clicked.connect(self._show_help_dialog)

        # 10. 썸네일 그리드 버튼 4개 바인딩
        for i in range(4):
            btn = self.find(QPushButton, f"thumbBtn_{i}")
            if btn:
                btn.clicked.connect(lambda checked=False, idx=i: self._on_thumbnail_clicked(idx))

    def _generate_random_seed(self):
        new_seed = random.randint(100000000, 999999999)
        seed_spin = self.find(QSpinBox, "seedSpinBox")
        if seed_spin:
            seed_spin.setValue(new_seed)
        self.append_log(f"새 무작위 시드 생성: {new_seed}")

    def _on_lock_seed_toggled(self, checked):
        self.is_seed_locked = checked
        btn = self.find(QPushButton, "lockSeedButton")
        if btn:
            btn.setText("🔒 시드 고정됨" if checked else "🔓 고정 안함")
        self.append_log("시드 고정 모드: " + ("고정됨" if checked else "해제됨"))

    def _copy_enhanced_prompt(self):
        edit = self.find(QPlainTextEdit, "enhancePromptEdit")
        if not edit:
            return
        text = edit.toPlainText().strip()
        if not text:
            # 영문 프롬프트가 비어있으면 한글 프롬프트 복사 시도
            korean_edit = self.find(QPlainTextEdit, "positivePromptEdit")
            text = korean_edit.toPlainText().strip() if korean_edit else ""
        if text:
            QApplication.clipboard().setText(text)
            btn = self.find(QPushButton, "copyPromptButton")
            if btn:
                orig_text = btn.text()
                btn.setText("✓ 복사 완료!")
                QTimer.singleShot(1500, lambda: btn.setText(orig_text))
            self.append_log("프롬프트가 클립보드에 복사되었습니다.")

    def _copy_image_to_clipboard(self):
        label = self.find(QLabel, "previewLabel")
        if label and label.pixmap() and not label.pixmap().isNull():
            QApplication.clipboard().setPixmap(label.pixmap())
            btn = self.find(QPushButton, "copyImageButton")
            if btn:
                orig_text = btn.text()
                btn.setText("✓ 복사 완료!")
                QTimer.singleShot(1500, lambda: btn.setText(orig_text))
            self.append_log("결과 이미지가 클립보드에 복사되었습니다. (Ctrl+V로 붙여넣기 가능)")
        elif self.current_image_path and Path(self.current_image_path).exists():
            pix = QPixmap(str(self.current_image_path))
            if not pix.isNull():
                QApplication.clipboard().setPixmap(pix)
                self.append_log("결과 이미지가 클립보드에 복사되었습니다.")
        else:
            show_message_box(self.window, QMessageBox.Icon.Information, "알림", "복사할 이미지가 없습니다.")

    def _show_settings_dialog(self):
        """연결 상태 배지 및 설정 버튼 클릭 시 모달 설정창 표시"""
        dlg = QDialog(self.window)
        dlg.setWindowTitle("서버 연결 및 모델 폴더 설정")
        dlg.resize(480, 400)
        dlg.setStyleSheet(self.window.styleSheet())
        layout = QVBoxLayout(dlg)
        layout.setSpacing(12)

        # ComfyUI 설정 그룹
        comfy_group = QGroupBox("🎨 ComfyUI 설정", dlg)
        comfy_layout = QVBoxLayout(comfy_group)
        comfy_layout.setSpacing(8)

        comfy_url_row = QHBoxLayout()
        comfy_url_edit = QLineEdit(self.find(QLineEdit, "comfyUrlEdit").text(), comfy_group)
        comfy_check_btn = QPushButton("연결 확인", comfy_group)
        comfy_check_btn.clicked.connect(lambda: (
            self.find(QLineEdit, "comfyUrlEdit").setText(comfy_url_edit.text()),
            self.check_connection("comfy")
        ))
        comfy_url_row.addWidget(QLabel("서버 주소:"))
        comfy_url_row.addWidget(comfy_url_edit)
        comfy_url_row.addWidget(comfy_check_btn)
        comfy_layout.addLayout(comfy_url_row)

        model_path_row = QHBoxLayout()
        model_path_edit = QLineEdit(self.find(QLineEdit, "comfyModelPathEdit").text(), comfy_group)
        browse_btn = QPushButton("찾아보기", comfy_group)
        def on_browse():
            folder = QFileDialog.getExistingDirectory(dlg, "ComfyUI 모델 폴더 선택")
            if folder:
                model_path_edit.setText(folder)
                self.find(QLineEdit, "comfyModelPathEdit").setText(folder)
                self.update_model_path_status(folder)
        browse_btn.clicked.connect(on_browse)
        model_path_row.addWidget(QLabel("모델 폴더:"))
        model_path_row.addWidget(model_path_edit)
        model_path_row.addWidget(browse_btn)
        comfy_layout.addLayout(model_path_row)
        layout.addWidget(comfy_group)

        # LM Studio 설정 그룹
        lm_group = QGroupBox("💬 LM Studio 설정", dlg)
        lm_layout = QVBoxLayout(lm_group)
        lm_layout.setSpacing(8)

        lm_url_row = QHBoxLayout()
        lm_url_edit = QLineEdit(self.find(QLineEdit, "lmUrlEdit").text(), lm_group)
        lm_check_btn = QPushButton("연결 확인", lm_group)
        lm_check_btn.clicked.connect(lambda: (
            self.find(QLineEdit, "lmUrlEdit").setText(lm_url_edit.text()),
            self.check_connection("lm")
        ))
        lm_url_row.addWidget(QLabel("서버 주소:"))
        lm_url_row.addWidget(lm_url_edit)
        lm_url_row.addWidget(lm_check_btn)
        lm_layout.addLayout(lm_url_row)
        layout.addWidget(lm_group)

        # 하단 닫기/저장 버튼
        btn_box = QHBoxLayout()
        save_btn = QPushButton("💾 설정 저장 후 닫기", dlg)
        def on_save_close():
            self.find(QLineEdit, "comfyUrlEdit").setText(comfy_url_edit.text())
            self.find(QLineEdit, "comfyModelPathEdit").setText(model_path_edit.text())
            self.find(QLineEdit, "lmUrlEdit").setText(lm_url_edit.text())
            self.save_config()
            dlg.accept()
        save_btn.clicked.connect(on_save_close)
        btn_box.addStretch()
        btn_box.addWidget(save_btn)
        layout.addLayout(btn_box)

        dlg.exec()

    def _show_help_dialog(self):
        """도움말 다이얼로그 표시"""
        dlg = QDialog(self.window)
        dlg.setWindowTitle("📖 ComfyCraft AI Easy Studio 도움말")
        dlg.resize(750, 580)
        dlg.setStyleSheet(self.window.styleSheet())
        layout = QVBoxLayout(dlg)

        browser = QTextBrowser(dlg)
        browser.setOpenExternalLinks(True)

        readme_path = BASE_DIR / "assets" / "help" / "README.md"
        style_inject = """
        <style>
            h1 { font-size: 24px; font-weight: bold; margin-bottom: 14px; }
            h2 { font-size: 20px; font-weight: bold; margin-top: 20px; margin-bottom: 10px; color: #d0bcff; }
            h3 { font-size: 16px; font-weight: bold; margin-top: 15px; margin-bottom: 8px; color: #e8def8; }
            p, li, td, th { font-size: 14px; line-height: 1.5; }
            strong { font-weight: bold; font-size: 14px; color: #ffffff; }
            hr { border-bottom: 1px solid #33343b; margin: 15px 0; }
            pre, code { background-color: #1e1e1e; color: #e2e2eb; padding: 3px 5px; border-radius: 4px; font-family: Consolas, monospace; font-size: 13px; }
            pre { padding: 10px; }
        </style>
        """
        html_content = (
            style_inject
            + "<h2 style='color:#d0bcff; font-size:24px;'>📖 ComfyCraft AI Easy Studio 도움말</h2><hr>"
            + self._render_markdown_file(readme_path)
        )

        browser.setHtml(html_content)
        layout.addWidget(browser)

        close_btn = QPushButton("닫기", dlg)
        close_btn.clicked.connect(dlg.accept)
        layout.addWidget(close_btn)
        dlg.exec()

    def _show_facedetailer_guide(self):
        """❓ 얼굴 보정(FaceDetailer) 초보자 가이드 다이얼로그"""
        dlg = QDialog(self.window)
        dlg.setWindowTitle("❓ 얼굴 보정(FaceDetailer) 쉬운 설명")
        dlg.resize(760, 640)
        dlg.setStyleSheet(self.window.styleSheet())
        layout = QVBoxLayout(dlg)

        browser = QTextBrowser(dlg)
        browser.setOpenExternalLinks(True)

        guide_file = BASE_DIR / "assets" / "help" / "facedetailer_guide.html"
        if guide_file.exists():
            try:
                html = guide_file.read_text(encoding="utf-8")
            except Exception:
                html = "<p>설명서 파일을 불러올 수 없습니다.</p>"
        else:
            html = "<p>설명서 파일이 존재하지 않습니다.</p>"

        browser.setHtml(html)
        layout.addWidget(browser)

        close_btn = QPushButton("닫기", dlg)
        close_btn.clicked.connect(dlg.accept)
        layout.addWidget(close_btn)
        dlg.exec()

    def _on_thumbnail_clicked(self, index):
        """썸네일 클릭 시 당시 사용했던 프롬프트, 모델, 세부옵션 및 이미지 복원"""
        if index >= len(self.generation_history):
            return
        item = self.generation_history[index]
        img_path = item.get("path")
        snap = item.get("snapshot", {})

        # 1. 이미지 표시
        if img_path and Path(img_path).exists():
            self.show_image(img_path)

        # 2. 프롬프트 복원
        if "prompt" in snap:
            self.find(QPlainTextEdit, "positivePromptEdit").setPlainText(snap.get("prompt", ""))
        if "enhance_prompt" in snap and snap.get("enhance_prompt"):
            self.find(QPlainTextEdit, "enhancePromptEdit").setPlainText(snap.get("enhance_prompt", ""))
        if "negative" in snap:
            self.find(QPlainTextEdit, "negativePromptEdit").setPlainText(snap.get("negative", ""))

        # 3. 모델 및 해상도, 시드, CFG, 스텝 복원
        if "comfy_model" in snap:
            self.find(QComboBox, "comfyModelCombo").setCurrentText(snap.get("comfy_model"))
        if "width" in snap and "height" in snap:
            self.apply_preset(snap["width"], snap["height"])
        if "steps" in snap:
            self.set_steps_value(snap["steps"])
        if "cfg" in snap:
            self.set_cfg_value(snap["cfg"])
        if "seed" in snap and snap["seed"] != -1:
            self.find(QSpinBox, "seedSpinBox").setValue(snap["seed"])
        if "sampler" in snap:
            self.find(QComboBox, "samplerComboBox").setCurrentText(snap["sampler"])
        if "scheduler" in snap:
            self.find(QComboBox, "schedulerComboBox").setCurrentText(snap["scheduler"])

        # 4. FaceDetailer 옵션 복원
        self._restore_facedetailer_from_snapshot(snap)

        self.append_log(f"최근 생성 기록 [{index + 1}번]의 설정 및 프롬프트를 성공적으로 복원했습니다.")

    def add_to_history(self, path, snapshot):
        """새로 생성된 이미지를 최근 기록 히스토리 목록에 추가하고 썸네일 갱신"""
        # 동일한 이미지가 이미 히스토리에 있다면 기존 항목 제거 후 최상단 추가 (중복 방지)
        self.generation_history = [item for item in self.generation_history if item.get("path") != path]
        self.generation_history.insert(0, {"path": path, "snapshot": snapshot})
        if len(self.generation_history) > 4:
            self.generation_history.pop()

        # 썸네일 버튼 갱신
        for i in range(4):
            btn = self.find(QPushButton, f"thumbBtn_{i}")
            if not btn:
                continue
            if i < len(self.generation_history):
                p = self.generation_history[i]["path"]
                if Path(p).exists():
                    pix = QPixmap(str(p))
                    if not pix.isNull():
                        btn.setIcon(QIcon(pix.scaled(72, 72, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)))
                        btn.setIconSize(btn.size())
                        btn.setText("")
                        btn.setToolTip(f"기록 {i+1}: 클릭하여 설정 및 프롬프트 복원")
            else:
                btn.setIcon(QIcon())
                btn.setText("대기 중")
                btn.setToolTip("")


def main():
    app = QApplication(sys.argv)

    theme_key = load_theme_choice()
    apply_theme(app, theme_key)
    print(f"[테마] 적용: {theme_key}")

    window = load_ui(UI_FILE)
    MainController(window)
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
