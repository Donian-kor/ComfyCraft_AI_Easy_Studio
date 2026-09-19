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
    QGraphicsOpacityEffect,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
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


ZANIME_STYLE_CHOICES = (
    ("webtoon", "🇰🇷 웹툰"),
    ("japanime", "🇯🇵 일본애니"),
    ("basic", "✨ 기본"),
)

ZANIME_STYLE_LABELS = {value: label for value, label in ZANIME_STYLE_CHOICES}

from assets.icons import (
    icon_rc,  # noqa: F401  (SVG 아이콘 리소스 등록용 - 직접 사용하진 않지만 import 자체가 필요함)
)
from app.gui.theme_manager import (
    AVAILABLE_THEMES,
    apply_theme,
    load_theme_choice,
    save_theme_choice,
    zanime_style_button_colors,
)
from app.gui.ui_loader import load_dialog_ui, load_ui

BASE_DIR = Path(__file__).resolve().parent

SETTINGS_DIALOG_FILE = BASE_DIR / "assets" / "ui" / "settings_dialog.ui"
HELP_DIALOG_FILE = BASE_DIR / "assets" / "ui" / "help_dialog_v2.ui"

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

        self._zanime_style_buttons = {}

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
        self._setup_zanime_style_buttons()
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
        self.find(QComboBox, "comfyModelCombo").currentTextChanged.connect(
            lambda _text="": self.update_zanime_style_visibility()
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
                    lambda checked=False, button=btn, width=width, height=height: self._on_preset_button_clicked(
                        button, width, height
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
        self._apply_zanime_style_theme(applied)
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

    def _build_zanime_style_qss(self, theme_key: str | None = None) -> str:
        """현재 테마 색상으로 zanime 스타일 버튼의 스타일 문자열을 만든다.

        밝은 테마(fluent_light 등)에서도 글씨가 보이도록,
        배경색과 글자색을 테마별 색상 표에서 가져와 함께 지정한다.
        """
        if not theme_key:
            try:
                theme_key = load_theme_choice()
            except Exception:
                theme_key = ""
        colors = zanime_style_button_colors(theme_key)
        sel_bg = colors.get("selected_bg", "#0078d4")
        sel_border = colors.get("selected_border", "#005a9e")
        sel_text = colors.get("selected_text", "#ffffff")
        unsel_bg = colors.get("unselected_bg", "#e2e2e2")
        unsel_border = colors.get("unselected_border", "#b8b8b8")
        unsel_text = colors.get("unselected_text", "#1a1a1a")

        selected_selector = 'QPushButton[zanimeSelected="true"]'
        unselected_selector = 'QPushButton[zanimeSelected="false"]'

        return (
            "QPushButton { border-radius: 10px; padding: 6px 8px; "
            f"border: 1px solid {unsel_border}; "
            f"background-color: {unsel_bg}; "
            f"color: {unsel_text}; }}"
            "QPushButton:hover { "
            f"border: 2px solid {sel_border}; }}"
            "QPushButton:pressed { padding-top: 8px; padding-bottom: 4px; }"
            f"{selected_selector} {{ border: 2px solid {sel_border}; "
            f"background-color: {sel_bg}; "
            f"font-weight: 700; color: {sel_text}; }}"
            f"{unselected_selector} {{ border: 1px solid {unsel_border}; "
            f"background-color: {unsel_bg}; color: {unsel_text}; }}"
        )

    def _apply_zanime_style_theme(self, theme_key: str | None = None) -> None:
        """테마가 바뀌면 zanime 스타일 버튼 색상을 다시 칠한다."""
        buttons = getattr(self, "_zanime_style_buttons", {}) or {}
        if not buttons:
            return
        qss = self._build_zanime_style_qss(theme_key)
        for button in buttons.values():
            try:
                button.setStyleSheet(qss)
            except Exception:
                pass
        self.refresh_zanime_style_buttons()

    def _should_show_negative_prompt(self, model_name: str) -> bool:
        """부정 프롬프트 입력칸을 보여줄 모델인지 판단한다.

        저거넛(Juggernaut), 리얼비스(RealVis), Z-ANIME 계열일 때만 True.
        FLUX나 Z-Image 등 나머지 모델에서는 표시하지 않는다.
        """
        try:
            if not model_name or model_name == "로드된 모델 없음":
                return False
            lowered = model_name.lower()
            keywords = (
                "juggernaut",
                "ragnarok",
                "realvis",
                "z-anime",
                "z_anime",
                "zanime",
                "anime_aio",
            )
            if any(keyword in lowered for keyword in keywords):
                return True
            # 파일명 규칙이 안 맞아도 프로필 family로 한 번 더 확인
            profile = self.model_registry.detect(model_name)
            return profile.family in ("realvisxl", "juggernautxl", "zanime")
        except Exception:
            return False

    def _apply_negative_prompt_height(self) -> None:
        """부정 프롬프트 입력칸의 높이를 1줄 크기로 고정한다.

        내용이 길어져도 칸이 늘어나지 않아 화면이 아래로 밀리지 않는다.
        넘치는 내용은 세로 스크롤로 볼 수 있다.
        """
        edit = self.find(QPlainTextEdit, "negativePromptEdit")
        if edit is None:
            return
        try:
            metrics = edit.fontMetrics()
            line_height = metrics.lineSpacing()
            frame = edit.frameWidth() * 2
            # 문서/뷰포트 여백을 감안해 1줄만 보이도록 높이를 계산한다
            target = line_height + frame + 8
            edit.setMinimumHeight(target)
            edit.setMaximumHeight(target)
            edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            edit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        except Exception:
            pass

    def _apply_positive_prompt_height(self) -> None:
        """긍정 프롬프트 입력칸 높이를 2줄 크기로 고정한다.

        항상 2줄 높이를 유지하므로 긴 내용을 입력해도
        칸이 커지지 않고 화면이 밀리지 않는다. 넘치는 내용은 스크롤로 본다.
        """
        edit = self.find(QPlainTextEdit, "positivePromptEdit")
        if edit is None:
            return
        try:
            metrics = edit.fontMetrics()
            line_height = metrics.lineSpacing()
            frame = edit.frameWidth() * 2
            # 2줄 + 프레임/여백
            target = line_height * 2 + frame + 10
            edit.setMinimumHeight(target)
            edit.setMaximumHeight(target)
            edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            edit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        except Exception:
            pass

    def _setup_dynamic_enhance_prompt_height(self) -> None:
        """향상 프롬프트 입력칸 높이가 내용에 따라 늘고 줄게 만든다.

        내용이 없으면 최소(2줄), 길어지면 최대(12줄)까지 늘어난다.
        최대를 넘으면 스크롤로 나머지 내용을 본다.
        """
        edit = self.find(QPlainTextEdit, "enhancePromptEdit")
        if edit is None:
            return
        try:
            metrics = edit.fontMetrics()
            line_height = metrics.lineSpacing()
            frame = edit.frameWidth() * 2
            self._enhance_height_extra = frame + 10
            self._enhance_min_height = line_height * 2 + self._enhance_height_extra
            self._enhance_max_height = line_height * 12 + self._enhance_height_extra
            edit.textChanged.connect(self._update_enhance_prompt_height)
            self._update_enhance_prompt_height()
        except Exception:
            pass

    def _update_enhance_prompt_height(self) -> None:
        """향상 프롬프트 내용 높이를 계산해 입력칸 높이를 맞춘다.

        QPlainTextEdit의 document().size().height()는 픽셀 높이가 아니라
        줄 수를 돌려주므로, 각 줄(블록)의 실제 줄 수를 세서 픽셀 높이로 바꾼다.
        """
        edit = self.find(QPlainTextEdit, "enhancePromptEdit")
        if edit is None:
            return
        try:
            metrics = edit.fontMetrics()
            line_height = metrics.lineSpacing()
            # 자동 줄바꿈을 포함한 실제 보이는 줄 수를 센다
            total_lines = 0
            block = edit.document().begin()
            while block.isValid():
                total_lines += max(1, block.layout().lineCount())
                block = block.next()
            margins = edit.contentsMargins()
            extra = getattr(self, "_enhance_height_extra", 10)
            min_height = getattr(self, "_enhance_min_height", 50)
            max_height = getattr(self, "_enhance_max_height", 300)
            doc_height = total_lines * line_height
            target = int(doc_height + margins.top() + margins.bottom() + extra)
            target = max(min_height, min(max_height, target))
            edit.setMinimumHeight(target)
            edit.setMaximumHeight(target)
        except Exception:
            pass

    def _setup_zanime_style_buttons(self):
        """핵심 생성 옵션의 모델 바로 아래에 zanime 스타일 버튼을 만든다."""
        if getattr(self, "_zanime_style_buttons", None) is None:
            self._zanime_style_buttons = {}
        if getattr(self, "_zanime_style_frame", None) is not None:
            self.update_zanime_style_visibility()
            return

        model_layout = self.window.findChild(QVBoxLayout, "modelSelectLayout")
        step_layout = self.window.findChild(QVBoxLayout, "step2Layout")
        if model_layout is None or step_layout is None:
            return

        frame = QFrame()
        frame.setObjectName("zanimeStyleFrame")
        layout = QVBoxLayout(frame)
        layout.setObjectName("zanimeStyleLayout")
        layout.setSpacing(4)
        layout.setContentsMargins(0, 4, 0, 0)

        title = QLabel("🎨 Z-ANIME 스타일 선택 (필수)")
        title.setObjectName("zanimeStyleLabel")
        layout.addWidget(title)

        button_row = QHBoxLayout()
        button_row.setObjectName("zanimeStyleButtonLayout")
        button_row.setSpacing(6)
        base_button_style = self._build_zanime_style_qss()
        for style_value, style_label in ZANIME_STYLE_CHOICES:
            button = QPushButton(style_label)
            button.setObjectName(f"zanimeStyle_{style_value}_Button")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setMinimumHeight(34)
            button.setProperty("zanimeSelected", False)
            button.setStyleSheet(base_button_style)
            effect = QGraphicsOpacityEffect(button)
            effect.setOpacity(1.0)
            button.setGraphicsEffect(effect)
            button.clicked.connect(
                lambda _checked=False, value=style_value: self.select_zanime_style(value)
            )
            button_row.addWidget(button)
            self._zanime_style_buttons[style_value] = button
        layout.addLayout(button_row)

        notice = QLabel("Z-ANIME 모델일 때만 보입니다. 버튼을 누른 뒤 생성해 주세요.")
        notice.setObjectName("zanimeStyleNoticeLabel")
        notice.setWordWrap(True)
        layout.addWidget(notice)

        self._zanime_style_frame = frame

        index = -1
        for i in range(step_layout.count()):
            if step_layout.itemAt(i).layout() is model_layout:
                index = i
                break
        if index >= 0:
            step_layout.insertWidget(index + 1, frame)
        else:
            model_layout.addWidget(frame)

        self.refresh_zanime_style_buttons()
        self.update_zanime_style_visibility()

    def is_zanime_selected(self) -> bool:
        """현재 선택된 ComfyUI 모델이 zanime 계열인지 판단한다."""
        try:
            combo = self.find(QComboBox, "comfyModelCombo")
            model_name = combo.currentText() if combo is not None else ""
            profile = self.model_registry.detect(model_name)
            lowered = (model_name or "").lower()
            return bool(
                "z-anime" in lowered
                or "zanime" in lowered
                or "z_anime_base" in lowered
                or "anime_aio" in lowered
                or profile.family == "zanime"
                or profile.name == "zanime_aio"
            )
        except Exception:
            return False

    def current_zanime_style(self) -> str:
        """저장된 zanime 스타일 값을 소문자로 반환한다."""
        try:
            return (self.config.prompts.zanime_style or "").strip().lower()
        except Exception:
            return ""

    def refresh_zanime_style_buttons(self) -> None:
        """저장된 zanime 스타일을 버튼 선택 상태에 반영한다."""
        buttons = getattr(self, "_zanime_style_buttons", {}) or {}
        if not buttons:
            return
        current = self.current_zanime_style()
        for style_value, button in buttons.items():
            try:
                button.blockSignals(True)
                is_selected = style_value == current
                button.setChecked(is_selected)
                button.setProperty("zanimeSelected", is_selected)
                try:
                    button.style().unpolish(button)
                    button.style().polish(button)
                    button.update()
                except Exception:
                    pass
            finally:
                try:
                    button.blockSignals(False)
                except Exception:
                    pass

    def update_zanime_style_visibility(self) -> None:
        """zanime이 선택됐을 때만 스타일 선택 영역을 보여준다."""
        frame = getattr(self, "_zanime_style_frame", None)
        if frame is None:
            return
        frame.setVisible(self.is_zanime_selected())

    def select_zanime_style(self, style_value: str) -> None:
        """스타일 버튼 선택을 저장하고 UI 선택 상태에 반영한다."""
        normalized = (style_value or "").strip().lower()
        valid_styles = {value for value, _label in ZANIME_STYLE_CHOICES}
        if normalized not in valid_styles:
            return
        try:
            self.config.prompts.zanime_style = normalized
            self.config_manager.set_config(self.config)
            self.config_manager.save(self.config)
        except Exception as exc:
            self.append_log(f"스타일 저장 실패: {exc}")
        self.refresh_zanime_style_buttons()
        self._play_zanime_style_animation(normalized)
        label = ZANIME_STYLE_LABELS.get(normalized, normalized)
        self.append_log(f"Z-ANIME 스타일 선택: {label}")

    def _play_zanime_style_animation(self, style_value: str) -> None:
        """선택된 스타일 버튼에 짧은 강조 애니메이션을 보여준다."""
        buttons = getattr(self, "_zanime_style_buttons", {}) or {}
        self._play_button_pulse_animation(buttons.get(style_value))

    def _play_button_pulse_animation(self, button: QPushButton) -> None:
        """버튼을 눌렀을 때 반짝이는 강조 애니메이션을 보여준다.

        스타일 버튼과 해상도 프리셋 버튼 등에서 함께 쓴다.
        잠깐 어두워졌다가 밝아지고, 다시 살짝 어두웠다가 원래대로 돌아온다.
        """
        if button is None:
            return
        try:
            effect = button.graphicsEffect()
            if not isinstance(effect, QGraphicsOpacityEffect):
                effect = QGraphicsOpacityEffect(button)
                button.setGraphicsEffect(effect)
            animation = QPropertyAnimation(effect, b"opacity", button)
            animation.setDuration(460)
            animation.setKeyValueAt(0.0, 0.40)
            animation.setKeyValueAt(0.45, 1.0)
            animation.setKeyValueAt(0.70, 0.72)
            animation.setKeyValueAt(1.0, 1.0)
            animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
            animation.finished.connect(
                lambda: effect.setOpacity(1.0) if effect is not None else None
            )
            animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
        except Exception:
            return

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

    def update_connection_label(self, which, ok, extra_label=None):
        """연결 상태를 라벨과 배지 버튼에 반영합니다 (속성 기반)."""
        from app.gui.split_text_button import SplitTextButton

        label = self.find(
            QLabel, "lmStatusLabel" if which == "lm" else "comfyStatusLabel"
        )
        badge = self.find(
            QPushButton, "lmStatusBtn" if which == "lm" else "comfyStatusBtn"
        )
        self._apply_status_label(
            label, ok, "🟢연결 성공", "🔴연결 실패", "📡 연결 중..."
        )
        if extra_label is not None:
            self._apply_status_label(
                extra_label, ok, "🟢연결 성공", "🔴연결 실패", "📡 연결 중..."
            )
        status = "pending" if ok is None else ("success" if ok else "error")

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

    def _apply_status_label(self, label, ok: bool | None, ok_text: str, fail_text: str, pending_text: str) -> None:
        """상태 라벨에 텍스트+속성을 한 번에 적용 (메인/다이얼로그 공용)."""
        if label is None:
            return
        if ok is None:
            label.setText(pending_text)
        else:
            label.setText(ok_text if ok else fail_text)
        status = "pending" if ok is None else ("success" if ok else "error")
        label.setProperty("status", status)
        label.style().unpolish(label)
        label.style().polish(label)

    def update_model_path_status(self, path, label=None):
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
        if label is None:
            label = self.find(QLabel, "modelPathStatusLabel")
        self._apply_status_label(
            label,
            valid,
            "✓ ComfyUI 모델 폴더 확인됨",
            "✗ 올바른 모델 폴더가 아닙니다",
            "",
        )
        return valid

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

        self.update_zanime_style_visibility()

        # 부정 프롬프트: 저거넛/리얼비스/Z-ANIME 계열에서만 표시
        neg_frame = self.find(QFrame, "negativePromptFrame")
        if neg_frame:
            neg_frame.setVisible(self._should_show_negative_prompt(model_name))

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

    def _on_preset_button_clicked(self, button, width, height):
        """프리셋 버튼을 눌렀을 때: 값 적용 + 스타일 버튼과 같은 반짝 애니메이션.

        기록 복원처럼 코드에서 직접 apply_preset을 부를 때는
        이 함수를 거치지 않으므로 애니메이션이 실행되지 않는다.
        """
        self.apply_preset(width, height)
        self._play_button_pulse_animation(button)

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

        self.refresh_zanime_style_buttons()
        self.update_zanime_style_visibility()

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
        comfy_model_name = self.find(QComboBox, "comfyModelCombo").currentText()
        # zanime 모델이면 스타일 선택이 끝난 뒤에만 생성 가능
        if self.is_zanime_selected() and self.current_zanime_style() not in (
            "webtoon",
            "japanime",
            "basic",
        ):
            raise ValueError(
                "Z-ANIME 스타일을 먼저 선택해 주세요. (웹툰 / 일본애니 / 기본 중 하나)"
            )
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
            "zanime_style": self.current_zanime_style(),
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
        lowered_model_name = (comfy_model_name or "").lower()
        is_zanime = bool(
            "z-anime" in lowered_model_name
            or "zanime" in lowered_model_name
            or "z_anime_base" in lowered_model_name
            or "anime_aio" in lowered_model_name
            or profile.family == "zanime"
            or profile.name == "zanime_aio"
        )

        # zanime 모델일 때만: 저장된 스타일 설정을 따라 별도 시스템 프롬프트 사용
        zanime_style = (self.config.prompts.zanime_style or "").strip().lower()
        zanime_system_prompt = ""
        if is_zanime and zanime_style in ("webtoon", "japanime", "basic"):
            if zanime_style == "webtoon":
                zanime_system_prompt = ext_prompts.get("system_prompt_zanime_webtoon_en") or ""
            elif zanime_style == "japanime":
                zanime_system_prompt = ext_prompts.get("system_prompt_zanime_anime_en") or ""
            else:
                zanime_system_prompt = ext_prompts.get("system_prompt_zanime_basic_en") or ""
            if zanime_system_prompt:
                self.append_log(
                    f"[ZANIME 스타일] '{zanime_style}' 스타일 프롬프트 지시문을 사용합니다."
                )
            else:
                self.append_log(
                    f"[ZANIME 스타일] '{zanime_style}' 전용 지시문이 없어 기본 문장형 지시문으로 대체합니다."
                )

        # LM Studio에는 영문 시스템 프롬프트 사용 (출력 언어 준수율 향상)
        # use_korean_prompt 설정과 무관하게 영문 프롬프트(_en) 사용
        if zanime_system_prompt:
            system_prompt = zanime_system_prompt
            self.append_log(
                f"[AI 자동 분석] '{comfy_model_name}' 모델 감지: '문장형' 프롬프트 지시문을 사용합니다."
            )
        elif is_flux or is_zimage or is_zanime:
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
            try:
                snapshot = self.capture_snapshot()
            except ValueError as exc:
                show_message_box(
                    self.window,
                    QMessageBox.Icon.Warning,
                    "스타일 선택 필요",
                    str(exc),
                )
                btn = self.find(QPushButton, "generateButton")
                if btn is not None:
                    try:
                        btn.blockSignals(True)
                        btn.setChecked(False)
                    finally:
                        try:
                            btn.blockSignals(False)
                        except Exception:
                            pass
                return
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

        # 6-1. 부정 프롬프트 패널: 저거넛/리얼비스/Z-ANIME 계열에서만 표시하고 1줄 높이로 고정
        neg_frame = self.find(QFrame, "negativePromptFrame")
        if neg_frame:
            curr_model = self.find(QComboBox, "comfyModelCombo").currentText() if self.find(QComboBox, "comfyModelCombo") else ""
            neg_frame.setVisible(self._should_show_negative_prompt(curr_model))
        self._apply_negative_prompt_height()
        self._apply_positive_prompt_height()
        self._setup_dynamic_enhance_prompt_height()

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
        """설정 다이얼로그(.ui 파일 기반)를 표시한다.

        연결 버튼(comfyStatusBtn, lmStatusBtn), 사이드바 설정 버튼(settingsButton)
        모두 이 창으로 연결된다.
        """
        try:
            dlg = load_dialog_ui(SETTINGS_DIALOG_FILE, self.window)
        except Exception as e:  # noqa: BLE001 (ui 로드 실패 시 사용자에게 알림)
            show_message_box(
                self.window,
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

        # 다이얼로그에 현재 메인 화면 값 채우기
        if comfy_url_edit is not None:
            comfy_url_edit.setText(self.find(QLineEdit, "comfyUrlEdit").text())
        if model_path_edit is not None:
            model_path_edit.setText(self.find(QLineEdit, "comfyModelPathEdit").text())
            # 모델 폴더 경로 체크 라벨을 설정창 안에서 바로 보여준다
            self.update_model_path_status(model_path_edit.text(), model_path_dlg_label)
        if lm_url_edit is not None:
            lm_url_edit.setText(self.find(QLineEdit, "lmUrlEdit").text())

        # 연결 확인 버튼 (설정창 라벨에도 결과를 함께 표시)
        comfy_check_btn = _child(QPushButton, "dlgComfyCheckBtn")
        if comfy_check_btn is not None and comfy_url_edit is not None:
            def on_comfy_check():
                self.find(QLineEdit, "comfyUrlEdit").setText(comfy_url_edit.text())
                self.check_connection("comfy")
                # 비동기 결과는 update_connection_label에서 배지/메인 라벨에 반영되고,
                # 설정창 라벨은 "확인 중"으로 먼저 표시해 준다
                self._apply_status_label(
                    comfy_status_dlg_label, None, "", "", "📡 연결 중..."
                )
            comfy_check_btn.clicked.connect(on_comfy_check)

        lm_check_btn = _child(QPushButton, "dlgLmCheckBtn")
        if lm_check_btn is not None and lm_url_edit is not None:
            def on_lm_check():
                self.find(QLineEdit, "lmUrlEdit").setText(lm_url_edit.text())
                self.check_connection("lm")
                self._apply_status_label(
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
                    self.find(QLineEdit, "comfyModelPathEdit").setText(folder)
                    self.update_model_path_status(folder, model_path_dlg_label)
            browse_btn.clicked.connect(on_browse)

        # 설정 불러오기 버튼 -> 기존 load_config() 재사용
        load_btn = _child(QPushButton, "dlgLoadConfigBtn")
        if load_btn is not None:
            def on_load():
                self.load_config()
                # 불러온 값으로 다이얼로그 입력칸도 갱신
                if comfy_url_edit is not None:
                    comfy_url_edit.setText(self.find(QLineEdit, "comfyUrlEdit").text())
                if model_path_edit is not None:
                    model_path_edit.setText(
                        self.find(QLineEdit, "comfyModelPathEdit").text()
                    )
                    self.update_model_path_status(
                        model_path_edit.text(), model_path_dlg_label
                    )
                if lm_url_edit is not None:
                    lm_url_edit.setText(self.find(QLineEdit, "lmUrlEdit").text())
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
                    self.update_model_path_status("", model_path_dlg_label)
                self.append_log("설정 다이얼로그 값을 기본값으로 되돌렸습니다.")
            reset_btn.clicked.connect(on_reset)

        # 저장 후 닫기 버튼
        save_btn = _child(QPushButton, "dlgSaveCloseBtn")
        if save_btn is not None:
            def on_save_close():
                if comfy_url_edit is not None:
                    self.find(QLineEdit, "comfyUrlEdit").setText(
                        comfy_url_edit.text()
                    )
                if model_path_edit is not None:
                    self.find(QLineEdit, "comfyModelPathEdit").setText(
                        model_path_edit.text()
                    )
                    self.update_model_path_status(
                        model_path_edit.text(), model_path_dlg_label
                    )
                if lm_url_edit is not None:
                    self.find(QLineEdit, "lmUrlEdit").setText(lm_url_edit.text())
                self.save_config()
                dlg.accept()
            save_btn.clicked.connect(on_save_close)

        dlg.exec()

    def _show_help_dialog(self):
        """도움말 다이얼로그(v2: 좌우 분할)를 표시한다. 비모달 방식으로 메인 화면과 병행 사용 가능."""
        try:
            dlg = load_dialog_ui(HELP_DIALOG_FILE, self.window)
        except Exception as e:  # noqa: BLE001 (ui 로드 실패 시 알림)
            show_message_box(
                self.window,
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
                self.window,
                QMessageBox.Icon.Warning,
                "도움말 UI 오류",
                "도움말 창의 필수 위젯을 찾을 수 없습니다.",
            )
            return

        # HTML 디렉토리
        html_dir = BASE_DIR / "assets" / "help" / "html"

        # 섹션 정의 (아이콘은 Feather Icons 이름, 실제로는 SVG 파일 또는 유니코드 이모지 사용)
        help_sections = [
            {"id": "getting_started", "title": "시작하기", "icon": "🚀", "file": "01_getting_started.html"},
            {"id": "basic_usage", "title": "기본 사용법", "icon": "📝", "file": "02_basic_usage.html"},
            {"id": "model_settings", "title": "모델 설정", "icon": "🤖", "file": "03_model_settings.html"},
            {"id": "prompt_writing", "title": "프롬프트 작성", "icon": "✍️", "file": "04_prompt_writing.html"},
            {"id": "generation_options", "title": "이미지 생성 옵션", "icon": "⚙️", "file": "05_generation_options.html"},
            {"id": "facedetailer", "title": "FaceDetailer 얼굴 보정", "icon": "👤", "file": "06_facedetailer.html"},
            {"id": "history", "title": "히스토리/썸네일", "icon": "🖼️", "file": "07_history.html"},
            {"id": "installation", "title": "설치 및 필수 노드", "icon": "📦", "file": "08_installation.html"},
            {"id": "lmstudio", "title": "LM Studio 연동", "icon": "💬", "file": "09_lmstudio.html"},
            {"id": "faq", "title": "자주 묻는 질문", "icon": "❓", "file": "10_faq.html"},
            {"id": "shortcuts", "title": "단축키/팁", "icon": "⌨️", "file": "11_shortcuts.html"},
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
            # 스크롤을 맨 위로
            content_browser.verticalScrollBar().setValue(0)

        # 리스트 클릭 시 콘텐츠 전환
        def on_section_clicked(item):
            section_data = item.data(Qt.ItemDataRole.UserRole)
            if section_data:
                load_section_html(section_data)

        section_list.itemClicked.connect(on_section_clicked)

        # 초기 선택: 첫 번째 항목
        if section_list.count() > 0:
            first_item = section_list.item(0)
            section_list.setCurrentItem(first_item)
            load_section_html(first_item.data(Qt.ItemDataRole.UserRole))

        # 닫기 버튼
        if close_btn is not None:
            close_btn.clicked.connect(dlg.accept)

        # ESC 키로 닫기
        dlg.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        dlg.setWindowModality(Qt.WindowModality.NonModal)  # 비모달

        # 창 표시 (비모달)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()

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
        if "zanime_style" in snap and snap.get("zanime_style"):
            try:
                self.config.prompts.zanime_style = str(snap.get("zanime_style", "")).strip().lower()
                self.config_manager.set_config(self.config)
                self.refresh_zanime_style_buttons()
            except Exception:
                pass
        self.update_zanime_style_visibility()

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
