"""MainController — main.py에서 분리됨 (Phase 2).

애플리케이션의 핵심 제어 로직을 담당한다.
"""

from __future__ import annotations

import random

from collections import deque

import logging
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
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
    QUrl,
)
import shiboken6 as shiboken
from PySide6.QtGui import QIcon, QRegularExpressionValidator, QPixmap, QShortcut, QKeySequence
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
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMenu,
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
    QToolButton,
    QVBoxLayout,
    QWidget,
)


from app.constants import (
    FACEDETAILER_SLIDER_SPECS,
    PROMPT_MAX_CHARACTERS,
    ZANIME_STYLE_CHOICES,
    ZANIME_STYLE_LABELS,
)

from assets.icons import (
    icon_rc,  # noqa: F401  (SVG 아이콘 리소스 등록용 - 직접 사용하진 않지만 import 자체가 필요함)
)
from app.gui.design_tokens import CORNER_RADIUS
from app.gui.theme_manager import (
    AVAILABLE_THEMES,
    apply_theme,
    load_theme_choice,
    save_theme_choice,
    zanime_style_button_colors,
)
from app.gui.ui_loader import load_dialog_ui, load_ui

from app.paths import BASE_DIR, HELP_DIALOG_FILE, SETTINGS_DIALOG_FILE

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
    SessionManager,
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
    resize_preview,
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
from app.sections.prompt import enforce_prompt_character_limit

# P9: 금지어 최소 목록 (제출 시 검증용). 명백한 성적·폭력·혐오 표현만 포함.
BLOCKED_WORDS = (
    "violencia", "porn", "porno", "xxx", "nsfw", "rape", "loli",
    "야동", "음란", "강간", "살인", "자살방법",
)
from app.logging_config import setup_logging
from app.gui.dialogs.settings_dialog import show_settings_dialog
from app.gui.dialogs.help_dialog import show_help_dialog
from app.gui.image_preview import ImagePreviewModal
from app.gui.dialogs.facedetailer_guide_dialog import show_facedetailer_guide
from app.gui.chat_widgets import (
    ChatMessage,
    GenerationStatusBubble,
    ImageCard,
    describe_model,
)

# P9: 상태 템플릿 11종 (기획서 §8). 고정 문장 + 빈칸 채움.
# 기존 동작 경로의 인라인 문구는 테스트 호환을 위해 유지하고,
# 신규 분기(환영·LM 미연결·금지어)는 이 표를 사용한다.
TEMPLATES = {
    "welcome": "안녕하세요! 어떤 이미지를 만들어드릴까요?",
    "done": "{model}으로 그렸어요. ({elapsed} 소요)",
    "edited": "{style} 스타일로 수정했어요.",
    "generating": "{summary} 이미지를 만들고 있어요...",
    "model_changed": "{model} 모델 최적 설정이 적용되었어요 ({feature}).",
    "options_reset": "생성 옵션을 기본값으로 되돌렸어요.",
    "failed": "이미지 생성에 실패했어요. 원인: {reason}",
    "lm_off": "프롬프트 향상 없이 원문으로 생성해요.",
    "blocked": "이 표현은 사용할 수 없어요.",
    "busy": "생성 중이에요. 기다리거나 취소해주세요.",
    "style_pick": "Z-Anime 스타일을 골라주세요.",
}

UI_FILE = BASE_DIR / "assets" / "ui" / "main.ui"

setup_logging(BASE_DIR)
logger = logging.getLogger(__name__)


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
        self._io_pool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="IoWorker")
        self._gen_pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="GenWorker")
        self.generation_started_at = None
        self.execution_status = create_execution_status()
        # P11: 로그 링버퍼 (메인 로그창 삭제 → 설정 로그 탭이 구독)
        self._log_buffer: deque = deque(maxlen=5000)
        self._log_tab_edit = None

        # 진행 상황 애니메이션
        self.loading_animation = LoadingAnimation(
            self.find(QProgressBar, "progressBar"),
            self.find(QLabel, "progressStatusLabel"),
        )

        # 경과 시간 타이머
        self.elapsed_timer = ElapsedTimer(self.find(QLabel, "elapsedLabel"))

        self.close_timer = QTimer(window)
        self.close_timer.setSingleShot(True)
        self.close_timer.timeout.connect(self._finalize_window_close)

        # 창 X 버튼으로 닫힐 때도 close() 정리(스레드 풀 등)를 거치도록 상태 플래그.
        # (MainController는 QObject라 closeEvent 오버라이드는 Qt가 호출하지 않으므로
        #  window.installEventFilter + eventFilter로 대체 배선한다.)
        self._closing = False
        self._close_allowed = False

        self.model_list_ready.connect(self._apply_models_result)
        self.connection_result_ready.connect(self._apply_connection_result)
        self.lm_connected = False
        self.setup()
        # 창의 close(X 버튼) 이벤트를 가로채서 정리 절차를 보장
        window.installEventFilter(self)

    def find(self, widget_type, name):
        return self.window.findChild(widget_type, name)

    def _find_or_raise(self, widget_type, name):
        widget = self.find(widget_type, name)
        if widget is None:
            raise RuntimeError(f"필수 UI 위젯 '{name}'을(를) 찾을 수 없습니다.")
        return widget

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
        # 그룹A 3개 위젯 제거 완료 (2단계): self.config가 유일한 원본
        # URL/경로는 설정창에서 self.config로 저장 후 save_config()로 파일 기록
        # 초기 표시값은 self.config에서 직접 읽음 (위젯 경유 없음)
        # URL 입력 validator는 설정창(dlg*)에서 처리
        regex = QRegularExpression(r"^[a-zA-Z0-9.:/\-]*$")
        # lmUrlEdit / comfyUrlEdit / comfyModelPathEdit 위젯 삭제됨 — self.config 직접 사용
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
        reset_button = self.find(QPushButton, "resetButton")
        if reset_button is not None:
            reset_button.clicked.connect(self.clear_logs)
        self.find(QPushButton, "openOutputFolderButton").clicked.connect(
            self.open_output_folder
        )
        save_button = self.find(QPushButton, "saveImageButton")
        if save_button is not None:
            save_button.clicked.connect(self.save_image_as)
        self.find(QComboBox, "lmModelCombo").currentTextChanged.connect(
            lambda text: self.log_model_selection("LM Studio", text)
        )
        # P4: 표시명 텍스트가 아닌 itemData(정확한 파일명) 기준으로 동작
        comfy_combo = self.find(QComboBox, "comfyModelCombo")
        if comfy_combo is not None:
            comfy_combo.currentIndexChanged.connect(self._on_comfy_model_changed)
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
                # 버튼 폰트 볼드 설정 (일관된 시각적 강조)
                font = btn.font()
                font.setBold(True)
                btn.setFont(font)
                
                btn.clicked.connect(
                    lambda checked=False, button=btn, width=width, height=height: self._on_preset_button_clicked(
                        button, width, height
                    )
                )
        self.find(QPlainTextEdit, "positivePromptEdit").textChanged.connect(
            lambda: self._enforce_prompt_limit("positivePromptEdit")
        )
        self.find(QPlainTextEdit, "negativePromptEdit").textChanged.connect(
            lambda: self._enforce_prompt_limit("negativePromptEdit")
        )
        self.find(QPlainTextEdit, "enhancePromptEdit").textChanged.connect(
            lambda: self._enforce_prompt_limit("enhancePromptEdit")
        )
        self._enforce_prompt_limit("positivePromptEdit")
        self._enforce_prompt_limit("negativePromptEdit")
        self._enforce_prompt_limit("enhancePromptEdit")

        # P2: 채팅 입력 행 연결 (카운터 + 전송 버튼 + Enter 전송)
        chat_input = self.find(QPlainTextEdit, "chatInputEdit")
        self._chat_input = chat_input
        if chat_input is not None:
            chat_input.textChanged.connect(self._on_chat_input_changed)
            chat_input.installEventFilter(self)
        send_button = self.find(QPushButton, "sendBtn")
        if send_button is not None:
            send_button.clicked.connect(self._on_chat_send_or_stop)
        self._pending_chat = None
        self._status_bubble = None
        self._pending_zanime_style = False
        self._refresh_send_state()

        # P9: 접근성 이름 + 라이브 리전 + 인라인 에러 라벨
        self._setup_chat_accessibility()

        # P11: 메인 로그창 삭제됨 — 로그는 설정 다이얼로그 로그 탭이 담당.
        # (구 logTextEdit/toggleLogButton/resetButton 없음)
        # ===== 에러 배너 클릭 → 설정 다이얼로그 열기 (로그 탭이 유일한 경로) =====
        banner = self.find(QLabel, "errorBannerLabel")
        if banner is not None:
            banner.setCursor(Qt.CursorShape.PointingHandCursor)
            banner.mousePressEvent = lambda event: self._show_settings_dialog()

        self.loading_animation.start("초기화 중...")
        QTimer.singleShot(150, self.refresh_models)

        # 사이드바 애니메이션 설정
        self.setup_sidebar_animation()

        # P1: 좌측 레일 버튼 연결 (클릭 토글, 호버 펼침 없음)
        self._setup_rail_buttons()

        # P6: 세션·이력 (session.json + ◷ 패널 + ▾ 메뉴)
        self._setup_sessions()

        # P11: 되돌리기 버튼을 옵션 레이아웃 끝에 추가 (step2Layout 삭제됨)
        options_layout = self.find(QVBoxLayout, "optionsLayout")
        if options_layout is not None and self.find(
                QPushButton, "resetOptionsButton") is None:
            reset_button = QPushButton("기본값으로 되돌리기")
            reset_button.setObjectName("resetOptionsButton")
            reset_button.setCursor(Qt.CursorShape.PointingHandCursor)
            reset_button.clicked.connect(self._reset_options_to_defaults)
            options_layout.addWidget(reset_button)

        # 미리보기 라벨: 창 크기 변경 시 이미지도 함께 확대/축소되도록 필터 설치
        preview_label = self.find(QLabel, "previewLabel")
        if preview_label is not None:
            self._preview_label = preview_label
            preview_label.installEventFilter(self)

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

        # ===== 에러 배너 클릭 → 로그창 펼치기 (UI/UX 4단계) =====
        banner = self.find(QLabel, "errorBannerLabel")
        if banner is not None:
            banner.setCursor(Qt.CursorShape.PointingHandCursor)
            banner.mousePressEvent = lambda event: self._on_error_banner_clicked()

        # ===== 테마 선택기 (설정 탭) =====
        self._setup_theme_selector()

        # ===== 신규 UI 기능 연동 (ComfyCraft AI Easy Studio) =====
        self._setup_new_studio_features()

    def _setup_theme_selector(self):
        """상단 헤더의 테마 선택 콤보박스를 초기화하고 연결한다."""
        from app.gui.theme_manager import VISIBLE_THEMES
        combo = self.find(QComboBox, "themeComboBox")
        if combo is not None:
            combo.blockSignals(True)
            combo.clear()
            for key in VISIBLE_THEMES:
                display_name = AVAILABLE_THEMES.get(key, key)
                combo.addItem(display_name, key)
            current_theme = load_theme_choice()
            if current_theme not in VISIBLE_THEMES:
                current_theme = "fluent_dark"
            idx = combo.findData(current_theme)
            if idx >= 0:
                combo.setCurrentIndex(idx)
            combo.blockSignals(False)
            combo.currentIndexChanged.connect(self._on_theme_changed)
            return

        # 폴백 제거 완료 (3단계): themeComboBox는 UI에 직접 존재함
        return

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

    def _reset_options_to_defaults(self) -> None:
        """P5: 현재 모델 최적값 + FaceDetailer 기본값으로 되돌리기."""
        try:
            exact = self._comfy_model_file()
            if not exact or exact == "로드된 모델 없음":
                self.append_log("모델을 먼저 선택해주세요.")
                return
            self.apply_model_defaults(exact)
            self._reset_facedetailer_to_defaults()
            self.append_log(f"옵션을 기본값으로 되돌렸습니다 ({exact}).")
            self._append_chat_message(
                "system", "생성 옵션을 기본값으로 되돌렸어요.")
        except RuntimeError:
            logger.debug("옵션 되돌리기 실패", exc_info=True)

    def _setup_rail_buttons(self) -> None:
        """P1: 좌측 레일 버튼 연결.

        P14(기획서 v5.0)에서 역할이 분리되었다:
        - railOptionsBtn(옵션): 생성 옵션 패널 토글
        - railHistoryBtn(이력): 대화 이력 페이지
        - railHomeBtn(홈): 패널 접기 + 채팅 복귀 (선택 강조 없음)
        - railSettingsBtn/railHelpBtn: 기존 다이얼로그
        - newChatBtn: 새 대화
        존재하지 않는 위젯은 조용히 건너뛴다.
        """
        panel = self.find(QWidget, "leftScrollArea")

        def toggle_panel() -> None:
            try:
                if panel is not None:
                    panel.setVisible(not panel.isVisible())
            except RuntimeError:
                logger.debug("옵션 패널 토글 실패", exc_info=True)

        # 홈은 여기서 연결하지 않는다 — P6에서 전용 핸들러로 재연결한다.
        for name in ("railOptionsBtn", "railHistoryBtn"):
            button = self.find(QPushButton, name)
            if button is not None:
                button.clicked.connect(toggle_panel)
        settings_button = self.find(QPushButton, "railSettingsBtn")
        if settings_button is not None:
            settings_button.clicked.connect(self._show_settings_dialog)
        help_button = self.find(QPushButton, "railHelpBtn")
        if help_button is not None:
            help_button.clicked.connect(self._show_help_dialog)
        new_chat_button = self.find(QPushButton, "newChatBtn")
        if new_chat_button is not None:
            new_chat_button.clicked.connect(self._on_new_chat_clicked)

    def _on_new_chat_clicked(self) -> None:
        """P1: 채팅 영역 비우기. P6: 세션 저장 후 새 세션 생성."""
        if self._is_generating():
            self.append_log("생성 중에는 새 대화를 시작할 수 없어요. 기다리거나 취소해주세요.")
            return
        try:
            self._flush_session()
            manager = getattr(self, "session_manager", None)
            if manager is not None:
                self._current_session = manager.new_session(
                    model=self._comfy_model_file())
                manager.save_session(self._current_session)
                self._refresh_session_views()
            self._chat_log = []
            self._clear_chat_widgets()
        except RuntimeError:
            logger.debug("새 대화 시작 실패", exc_info=True)

    def _clear_chat_widgets(self) -> None:
        """채팅 위젯 전부 제거 (spacer 유지)."""
        try:
            container = self.find(QWidget, "chatContentWidget")
            layout = container.layout() if container is not None else None
            if layout is None:
                return
            spacer = None
            leftovers = []
            for i in range(layout.count()):
                widget = layout.itemAt(i).widget()
                if widget is None:
                    continue
                if widget.objectName() == "chatSpacer":
                    spacer = widget
                else:
                    leftovers.append(widget)
            for widget in leftovers:
                layout.removeWidget(widget)
                widget.setParent(None)
                widget.deleteLater()
            if spacer is not None and layout.indexOf(spacer) < 0:
                layout.addWidget(spacer)
        except RuntimeError:
            logger.debug("채팅 비우기 실패", exc_info=True)

    # ──────────────────────────────────────────────────────────────────────
    # P6: 세션·이력 (session.json + ◷ 패널 + ▾ 메뉴 + 수정 요청)
    # ──────────────────────────────────────────────────────────────────────

    def _setup_sessions(self) -> None:
        """P6: 세션 관리자 + 이력 페이지 + 새 대화 스플릿 메뉴."""
        try:
            self.session_manager = SessionManager(
                self.output_dir / ".sessions")
        except Exception as exc:
            logger.debug("세션 관리자 초기화 실패: %s", exc_info=True)
            self.session_manager = None
        self._chat_log = []
        self._current_session = None
        self._history_shown = 50
        self._panel_page = "options"

        # 이력 페이지 (숨김 상태로 옵션 컨테이너에 추가)
        try:
            options_layout = self.find(QVBoxLayout, "optionsLayout")
            if options_layout is not None and self.find(
                    QWidget, "historyPage") is None:
                page = QWidget()
                page.setObjectName("historyPage")
                page_layout = QVBoxLayout(page)
                title = QLabel("대화 이력")
                title.setObjectName("historyPageTitle")
                page_layout.addWidget(title)
                history_list = QListWidget()
                history_list.setObjectName("historyList")
                history_list.itemClicked.connect(self._on_history_item_clicked)
                history_list.setContextMenuPolicy(
                    Qt.ContextMenuPolicy.CustomContextMenu)
                history_list.customContextMenuRequested.connect(
                    self._on_history_context_menu)
                page_layout.addWidget(history_list)
                self._history_list = history_list
                page.setVisible(False)
                options_layout.addWidget(page)
                self._history_page = page
            else:
                self._history_page = self.find(QWidget, "historyPage")
                self._history_list = self.find(QListWidget, "historyList")
        except RuntimeError:
            logger.debug("이력 페이지 생성 실패", exc_info=True)
            self._history_page = None
            self._history_list = None

        # P14: railOptions(옵션)/railHistory(이력) → 페이지 전환.
        # railHome(홈) → P1에서 옵션 토글로 연결돼 있었으므로 해제하고
        # "패널 접기 + 채팅 복귀"로 재연결한다 (기획서 v5.0 목업 1-A).
        try:
            home = self.find(QPushButton, "railHomeBtn")
            if home is not None:
                try:
                    home.clicked.disconnect()
                except (RuntimeError, TypeError):
                    pass  # 아직 연결된 슬롯이 없음 (P14에서 P1 연결을 제거)
                home.clicked.connect(self._rail_home_clicked)
            opt = self.find(QPushButton, "railOptionsBtn")
            if opt is not None:
                try:
                    opt.clicked.disconnect()
                except Exception:
                    pass
                opt.clicked.connect(lambda: self._rail_page_toggle("options"))
            hist = self.find(QPushButton, "railHistoryBtn")
            if hist is not None:
                try:
                    hist.clicked.disconnect()
                except Exception:
                    pass
                hist.clicked.connect(lambda: self._rail_page_toggle("history"))
        except RuntimeError:
            logger.debug("레일 페이지 연결 실패", exc_info=True)

        # 새 대화 버튼 → 스플릿(QToolButton) 교체: 클릭=새 세션, ▾=최근 5개
        try:
            old = self.find(QPushButton, "newChatBtn")
            if old is not None:
                from PySide6.QtWidgets import QToolButton as _QToolButton
                parent = old.parentWidget()
                layout = parent.layout() if parent is not None else None
                if layout is not None:
                    tool = _QToolButton(parent)
                    tool.setObjectName("newChatBtn")
                    tool.setText("＋ 새 대화")
                    tool.setCursor(Qt.CursorShape.PointingHandCursor)
                    tool.setPopupMode(
                        _QToolButton.ToolButtonPopupMode.MenuButtonPopup)
                    menu = QMenu(tool)
                    menu.aboutToShow.connect(self._rebuild_recent_menu)
                    tool.setMenu(menu)
                    self._recent_menu = menu
                    tool.clicked.connect(self._on_new_chat_clicked)
                    index = layout.indexOf(old)
                    layout.removeWidget(old)
                    old.setParent(None)
                    old.deleteLater()
                    layout.insertWidget(max(0, index), tool)
        except RuntimeError:
            logger.debug("새 대화 스플릿 교체 실패", exc_info=True)

        # 시작 시 마지막 세션 복원
        try:
            manager = getattr(self, "session_manager", None)
            if manager is not None:
                recent = manager.list_sessions(limit=1)
                if recent:
                    self._switch_session(recent[0].get("id", ""), silent=True)
        except Exception:
            logger.debug("시작 세션 복원 실패", exc_info=True)

        # P14: 첫 실행은 패널이 접혀 있으므로 강조도 없다(기획서 목업 1).
        self._update_rail_selection("")

        # P9: 저장된 세션이 없고 채팅이 비었을 때만 환영 메시지
        self._maybe_greet()

    # -- 페이지 전환 ------------------------------------------------------
    def _options_widgets(self):
        """P11 재빌드 대응: 옵션 컨테이너 하위 전부 (historyPage 계통 제외).

        행들이 중첩 QHBoxLayout 안에 있으므로 직접 자식만 뒤지면
        행 전체가 남는다 — 하위 findChildren으로 전부 처리한다.
        """
        widgets = []
        # 항상 숨김 유지 (히든 홀더)
        always_hidden = {"historyPage", "enhancePromptEdit", "positivePromptEdit"}
        try:
            container = self.find(QWidget, "leftContentWidget")
            if container is None:
                return widgets
            for widget in container.findChildren(QWidget):
                try:
                    if widget.objectName() in always_hidden:
                        continue
                    node = widget
                    inside_hidden = False
                    while node is not None and node is not container:
                        if node.objectName() in always_hidden:
                            inside_hidden = True
                            break
                        node = node.parentWidget()
                    if not inside_hidden:
                        widgets.append(widget)
                except RuntimeError:
                    continue
        except RuntimeError:
            pass
        return widgets

    def _rail_page_toggle(self, page: str) -> None:
        """P6: 같은 버튼 재클릭이면 패널 접힘, 아니면 내용 교체+펼침."""
        try:
            panel = self.find(QWidget, "leftScrollArea")
            if panel is None:
                return
            if panel.isVisible() and self._panel_page == page:
                panel.setVisible(False)
                self._update_rail_selection("")
                return
            panel.setVisible(True)
            self._show_panel_page(page)
            self._update_rail_selection(page)
        except RuntimeError:
            logger.debug("레일 페이지 토글 실패", exc_info=True)

    def _rail_home_clicked(self) -> None:
        """P14(기획서 v5.0 목업 1-A): 홈 = 패널 접기 + 채팅 화면 복귀.

        홈은 선택 강조를 받지 않는다 — 강조는 "패널이 떠 있다"를 뜻하므로
        홈을 누르면 강조까지 함께 사라져야 어긋나지 않는다.
        """
        try:
            panel = self.find(QWidget, "leftScrollArea")
            if panel is not None and panel.isVisible():
                panel.setVisible(False)
            self._panel_page = "none"
            self._update_rail_selection("")
        except RuntimeError:
            logger.debug("홈 버튼 처리 실패", exc_info=True)

    def _update_rail_selection(self, page: str) -> None:
        """P14: 강조는 railOptionsBtn / railHistoryBtn 에만 붙는다.

        홈·?·설정은 강조 대상이 아니다(기획서 v5.0 설계원칙).
        page가 "" 이면 강조를 전부 해제한다.
        """
        mapping = {"options": "railOptionsBtn", "history": "railHistoryBtn"}
        try:
            for key, name in mapping.items():
                button = self.find(QPushButton, name)
                if button is None:
                    continue
                if key == page:
                    button.setStyleSheet(
                        "QPushButton { background-color: #0078D4; "
                        "color: white; border: 2px solid #4AA3F0; "
                        "border-radius: 8px; }")
                else:
                    button.setStyleSheet("")
        except RuntimeError:
            logger.debug("레일 선택 강조 실패", exc_info=True)

    def _show_panel_page(self, page: str) -> None:
        self._panel_page = page
        show_history = (page == "history")
        for widget in self._options_widgets():
            try:
                widget.setVisible(not show_history)
            except RuntimeError:
                pass
        try:
            if self._history_page is not None:
                self._history_page.setVisible(show_history)
        except RuntimeError:
            pass
        if show_history:
            self._refresh_history_list()

    # -- 세션 저장/복원 ----------------------------------------------------
    def _ensure_session(self) -> None:
        manager = getattr(self, "session_manager", None)
        if manager is None:
            return
        if self._current_session is None:
            self._current_session = manager.new_session(
                model=self._comfy_model_file())

    def _flush_session(self) -> bool:
        """현재 세션을 파일에 저장. 성공 시 True."""
        try:
            manager = getattr(self, "session_manager", None)
            session = getattr(self, "_current_session", None)
            if manager is None or session is None:
                return False
            session["messages"] = list(getattr(self, "_chat_log", []))
            session["model"] = self._comfy_model_file()
            last_snapshot: dict = {}
            for record in reversed(session["messages"]):
                if record.get("kind") == "image" and record.get("snapshot"):
                    last_snapshot = record["snapshot"]
                    break
            session["last_snapshot"] = last_snapshot
            ok = manager.save_session(session)
            if ok:
                self._refresh_session_views()
            return ok
        except Exception:
            logger.debug("세션 저장 실패", exc_info=True)
            return False

    def _switch_session(self, session_id: str, silent: bool = False) -> bool:
        """P6: 세션 전환 (생성 중 차단)."""
        if self._is_generating():
            if not silent:
                self.append_log("생성 중에는 세션을 전환할 수 없어요.")
            return False
        try:
            manager = getattr(self, "session_manager", None)
            if manager is None or not session_id:
                return False
            self._flush_session()
            session = manager.load_session(session_id)
            if session is None:
                if not silent:
                    self.append_log("세션을 불러올 수 없어요.")
                return False
            self._current_session = session
            self._chat_log = []
            self._clear_chat_widgets()
            for record in session.get("messages", []):
                if not isinstance(record, dict):
                    continue
                kind = record.get("kind", "ai")
                if kind == "image":
                    self._chat_log.append(record)
                    self._render_card(record)
                else:
                    self._chat_log.append(record)
                    self._render_message(record)
            self._refresh_session_views()
            return True
        except Exception:
            logger.debug("세션 전환 실패", exc_info=True)
            return False

    def _refresh_session_views(self) -> None:
        """▾ 메뉴·◷ 목록용 단일 원천 갱신 (구독 뷰 새로고침)."""
        try:
            self._refresh_history_list()
        except Exception:
            logger.debug("세션 뷰 갱신 실패", exc_info=True)

    # -- 이력 목록 ----------------------------------------------------------
    def _refresh_history_list(self, reset_paging: bool = True) -> None:
        history_list = getattr(self, "_history_list", None)
        manager = getattr(self, "session_manager", None)
        if history_list is None or manager is None:
            return
        try:
            if reset_paging:
                self._history_shown = 50
            history_list.blockSignals(True)
            history_list.clear()
            entries = manager.list_sessions()
            current_id = (getattr(self, "_current_session", None) or {}).get(
                "session_id", "")
            for entry in entries[: self._history_shown]:
                title = entry.get("title", "새 대화") or "새 대화"
                try:
                    profile = self.model_registry.detect(
                        entry.get("model", ""))
                    short, _feature, _tooltip = describe_model(
                        profile, entry.get("model", ""))
                except Exception:
                    short = "모델"
                meta = f"{short} · {str(entry.get('updated_at', ''))[:16]}"
                item = QListWidgetItem(f"{title}\n{meta}")
                item.setData(Qt.ItemDataRole.UserRole, entry.get("id", ""))
                if entry.get("id", "") == current_id:
                    item.setText(f"● {title}\n{meta}")
                history_list.addItem(item)
            if len(entries) > self._history_shown:
                more = QListWidgetItem(
                    f"더 보기 ({len(entries) - self._history_shown}개)")
                more.setData(Qt.ItemDataRole.UserRole, "__more__")
                history_list.addItem(more)
            history_list.blockSignals(False)
        except RuntimeError:
            logger.debug("이력 목록 갱신 실패", exc_info=True)

    def _on_history_item_clicked(self, item) -> None:
        try:
            sid = item.data(Qt.ItemDataRole.UserRole)
            if sid == "__more__":
                self._history_shown += 50
                self._refresh_history_list(reset_paging=False)
                return
            if sid:
                self._switch_session(str(sid))
        except RuntimeError:
            logger.debug("이력 항목 클릭 실패", exc_info=True)

    def _on_history_context_menu(self, position) -> None:
        history_list = getattr(self, "_history_list", None)
        manager = getattr(self, "session_manager", None)
        if history_list is None or manager is None:
            return
        try:
            item = history_list.itemAt(position)
            if item is None:
                return
            sid = str(item.data(Qt.ItemDataRole.UserRole) or "")
            if not sid or sid == "__more__":
                return
            menu = QMenu(history_list)
            rename_action = menu.addAction("이름 변경")
            delete_action = menu.addAction("삭제")
            copy_action = menu.addAction("프롬프트 복사")
            chosen = menu.exec(history_list.mapToGlobal(position))
            if chosen == rename_action:
                if self._is_generating():
                    self.append_log("생성 중에는 이름을 변경할 수 없어요.")
                    return
                new_title, ok = QInputDialog.getText(
                    self.window, "이름 변경", "세션 이름:",
                    text=self._session_title_of(sid))
                if ok and manager.rename_session(sid, new_title):
                    self._refresh_session_views()
            elif chosen == delete_action:
                if self._is_generating():
                    self.append_log("생성 중에는 삭제할 수 없어요.")
                    return
                answer = show_message_box(
                    self.window, QMessageBox.Icon.Question, "세션 삭제",
                    "이 대화를 삭제할까요? (이미지 파일은 유지됩니다.)",
                    QMessageBox.StandardButton.Yes
                    | QMessageBox.StandardButton.No,
                )
                if answer == QMessageBox.StandardButton.Yes:
                    if manager.delete_session(sid):
                        current = getattr(self, "_current_session", None) or {}
                        if current.get("session_id") == sid:
                            self._current_session = None
                            self._chat_log = []
                            self._clear_chat_widgets()
                        self._refresh_session_views()
            elif chosen == copy_action:
                prompt = self._session_first_prompt(sid)
                if prompt:
                    QApplication.clipboard().setText(prompt)
                    self.append_log("프롬프트를 복사했어요.")
        except RuntimeError:
            logger.debug("이력 메뉴 실패", exc_info=True)

    def _session_title_of(self, session_id: str) -> str:
        try:
            manager = getattr(self, "session_manager", None)
            session = manager.load_session(session_id) if manager else None
            return (session or {}).get("title", "")
        except Exception:
            return ""

    def _session_first_prompt(self, session_id: str) -> str:
        try:
            manager = getattr(self, "session_manager", None)
            session = manager.load_session(session_id) if manager else None
            for record in (session or {}).get("messages", []):
                if isinstance(record, dict) and record.get("kind") == "user":
                    return str(record.get("text", ""))
            return ""
        except Exception:
            return ""

    # -- ▾ 최근 메뉴 ---------------------------------------------------------
    def _rebuild_recent_menu(self) -> None:
        menu = getattr(self, "_recent_menu", None)
        manager = getattr(self, "session_manager", None)
        if menu is None or manager is None:
            return
        try:
            menu.clear()
            for entry in manager.list_sessions(limit=5):
                title = entry.get("title", "새 대화") or "새 대화"
                action = menu.addAction(title)
                action.setData(entry.get("id", ""))
                action.triggered.connect(
                    lambda _checked=False, sid=entry.get("id", ""):
                    self._switch_session(str(sid)))
            menu.addSeparator()
            menu.addAction("전체 보기는 ◷ 대화 이력").setEnabled(False)
        except RuntimeError:
            logger.debug("최근 메뉴 갱신 실패", exc_info=True)

    # -- 수정 요청 ------------------------------------------------------------
    def _open_preview(self, image_path: str,
                        return_focus_widget=None) -> None:
        """P7: 채팅 이미지 목록으로 미리보기 모달 열기."""
        try:
            paths = []
            for record in getattr(self, "_chat_log", []):
                if not isinstance(record, dict):
                    continue
                if record.get("kind") == "image":
                    candidate = str(record.get("image_path", ""))
                    if candidate and Path(candidate).exists():
                        paths.append(candidate)
            if image_path and Path(image_path).exists() and image_path not in paths:
                paths.append(image_path)
            if not paths:
                return
            try:
                index = paths.index(image_path)
            except ValueError:
                index = len(paths) - 1
            modal = ImagePreviewModal(
                self.window, on_save=self._save_preview_image)
            modal.open_with(paths, index,
                            return_focus_widget=return_focus_widget)
        except RuntimeError:
            logger.debug("미리보기 열기 실패", exc_info=True)

    def _save_preview_image(self, image_path: str) -> None:
        """P7: 미리보기에서 보는 이미지 저장."""
        try:
            target = save_image_as(self.window, image_path, self.output_dir)
            if target:
                self.append_log(f"이미지 저장: {target}")
        except RuntimeError:
            logger.debug("미리보기 저장 실패", exc_info=True)

    def _on_reuse_request(self, snapshot: dict) -> None:
        """P6: 해당 생성의 프롬프트+옵션 전체 복원 후 입력창 포커스."""
        if self._is_generating():
            self.append_log("생성 중에는 수정 요청을 할 수 없어요.")
            return
        try:
            self._restore_snapshot(snapshot or {})
            edit = self.find(QPlainTextEdit, "chatInputEdit")
            prompt_text = ""
            enhanced = self.find(QPlainTextEdit, "enhancePromptEdit")
            if enhanced is not None:
                prompt_text = enhanced.toPlainText().strip()
            if not prompt_text and isinstance(snapshot, dict):
                prompt_text = str(snapshot.get("prompt", ""))
            if edit is not None:
                edit.setPlainText(prompt_text)
                edit.setFocus()
            preview = (prompt_text[:30] + "…") if len(prompt_text) > 30 else prompt_text
            self._append_chat_message("system", f"편집 중: {preview}")
        except RuntimeError:
            logger.debug("수정 요청 실패", exc_info=True)

    # ──────────────────────────────────────────────────────────────────────
    # P2: 채팅 송수신 (ChatMessage/ImageCard + 전송 배선)
    # ──────────────────────────────────────────────────────────────────────

    def _chat_layout(self):
        """채팅 메시지 컨테이너 레이아웃 (없으면 None)."""
        try:
            container = self.find(QWidget, "chatContentWidget")
            return container.layout() if container is not None else None
        except RuntimeError:
            return None

    def _scroll_chat_to_bottom(self) -> None:
        try:
            scroll = self.find(object, "chatScrollArea")
            if scroll is None:
                return
            bar = scroll.verticalScrollBar()
            bar.setValue(bar.maximum())
        except RuntimeError:
            logger.debug("채팅 스크롤 실패", exc_info=True)

    def _append_chat_message(self, role: str, text: str):
        """채팅에 메시지 1개 추가하고 위젯 반환 (실패 시 None)."""
        from datetime import datetime
        record = {"kind": role, "text": text,
                  "timestamp": datetime.now().isoformat(timespec="seconds")}
        try:
            self._chat_log.append(record)
        except AttributeError:
            self._chat_log = [record]
        return self._render_message(record)

    def _render_message(self, record: dict):
        """P6: 기록 dict에서 위젯만 생성 (불러오기 경로, 기록 없음)."""
        layout = self._chat_layout()
        if layout is None:
            return None
        try:
            message = ChatMessage(record.get("kind", "ai"),
                                  record.get("text", ""), self.window)
            # 하단 spacer 앞으로 삽입 (spacer가 있으면 그 앞, 없으면 맨 뒤)
            insert_at = layout.count()
            for i in range(layout.count()):
                widget = layout.itemAt(i).widget()
                if widget is not None and widget.objectName() == "chatSpacer":
                    insert_at = i
                    break
            layout.insertWidget(insert_at, message)
            self._scroll_chat_to_bottom()
            return message
        except RuntimeError:
            logger.debug("채팅 메시지 추가 실패", exc_info=True)
            return None

    def _append_image_card(self, image_path: str, snapshot: dict,
                           elapsed_text: str, prompt_text: str):
        """AI 응답 + 이미지 카드 추가."""
        from datetime import datetime
        model_name = str(snapshot.get("comfy_model", ""))
        model_stem = Path(model_name).stem if model_name else "모델"
        meta = (f"{model_stem} · {snapshot.get('width', '?')}x{snapshot.get('height', '?')} "
                f"· 시드 {snapshot.get('seed', '?')} · {elapsed_text} 소요")
        record = {"kind": "image", "text": "이미지를 생성했어요!",
                  "timestamp": datetime.now().isoformat(timespec="seconds"),
                  "image_path": image_path, "meta": meta,
                  "prompt": prompt_text or "(프롬프트 없음)",
                  "snapshot": dict(snapshot)}
        try:
            self._chat_log.append(record)
        except AttributeError:
            self._chat_log = [record]
        self._append_chat_message("ai", "이미지를 생성했어요!")
        return self._render_card(record)

    def _render_card(self, record: dict):
        """P6: 기록 dict에서 이미지 카드 위젯만 생성 (불러오기 경로)."""
        layout = self._chat_layout()
        if layout is None:
            return None
        try:
            snapshot = record.get("snapshot", {})
            card = ImageCard(
                record.get("image_path", ""), record.get("meta", ""),
                record.get("prompt", ""),
                on_save=self.save_image_as,
                on_copy_prompt=self._copy_enhanced_prompt,
                on_copy_image=self._copy_image_to_clipboard,
                on_reuse=lambda: self._on_reuse_request(snapshot),
                parent=self.window,
            )
            try:
                card.image_label.clicked.connect(
                    lambda _c=False, path=record.get("image_path", ""),
                    focus=card.image_label:
                    self._open_preview(path, focus))
            except RuntimeError:
                pass
            # P9: 카드 접근성 이름
            try:
                prompt_preview = str(record.get("prompt", ""))[:100]
                card.image_label.setAccessibleName("생성된 이미지")
                card.image_label.setAccessibleDescription(prompt_preview)
                card.save_button.setAccessibleName("이미지 저장")
                card.copy_button.setAccessibleName("이미지 복사")
                card.reuse_button.setAccessibleName("프롬프트 불러와 수정")
                card.prompt_toggle.setAccessibleName("사용된 프롬프트 보기")
                card.prompt_copy_button.setAccessibleName("프롬프트 복사")
            except RuntimeError:
                pass
            insert_at = layout.count()
            for i in range(layout.count()):
                widget = layout.itemAt(i).widget()
                if widget is not None and widget.objectName() == "chatSpacer":
                    insert_at = i
                    break
            layout.insertWidget(insert_at, card)
            self._scroll_chat_to_bottom()
            return card
        except RuntimeError:
            logger.debug("이미지 카드 추가 실패", exc_info=True)
            return None

    def _show_status_bubble(self):
        """P3: 생성 중 상태 버블을 채팅에 추가하고 반환."""
        layout = self._chat_layout()
        if layout is None:
            return None
        try:
            self._hide_status_bubble()
            bubble = GenerationStatusBubble(
                on_cancel=self.stop_generation, parent=self.window)
            bubble.pulse_enabled = not self._reduced_motion()
            insert_at = layout.count()
            for i in range(layout.count()):
                widget = layout.itemAt(i).widget()
                if widget is not None and widget.objectName() == "chatSpacer":
                    insert_at = i
                    break
            layout.insertWidget(insert_at, bubble)
            bubble.start(time.monotonic())
            self._status_bubble = bubble
            self._scroll_chat_to_bottom()
            return bubble
        except RuntimeError:
            logger.debug("상태 버블 표시 실패", exc_info=True)
            return None

    def _hide_status_bubble(self) -> None:
        """P3: 상태 버블 제거 (완료·실패·취소 시)."""
        bubble = getattr(self, "_status_bubble", None)
        self._status_bubble = None
        if bubble is None:
            return
        try:
            bubble.stop()
            layout = self._chat_layout()
            if layout is not None:
                layout.removeWidget(bubble)
            bubble.setParent(None)
            bubble.deleteLater()
        except RuntimeError:
            logger.debug("상태 버블 제거 실패", exc_info=True)

    def _setup_chat_accessibility(self) -> None:
        """P9: 접근성 이름, 스크린 리더 알림용 라이브 라벨, 인라인 에러 라벨."""
        try:
            send_button = self.find(QPushButton, "sendBtn")
            if send_button is not None:
                send_button.setAccessibleName("이미지 생성하기")
                send_button.setAccessibleDescription(
                    "채팅 입력 내용을 이미지로 생성합니다.")
            picker = self.find(QComboBox, "comfyModelCombo")
            if picker is not None:
                picker.setAccessibleName("이미지 생성 모델 선택")
            chat_input = self.find(QPlainTextEdit, "chatInputEdit")
            if chat_input is not None:
                chat_input.setAccessibleName("이미지 설명 입력")
                chat_input.setAccessibleDescription(
                    "Enter로 전송, Shift+Enter로 줄바꿈합니다.")
            history_list = self.find(QListWidget, "historyList")
            if history_list is not None:
                history_list.setAccessibleName("대화 이력 목록")
            for name, label in (
                ("railHomeBtn", "홈 — 메인 채팅 화면으로"),
                ("railOptionsBtn", "생성 옵션 — 옵션 패널 펼침/접힘"),
                ("railHistoryBtn", "대화 이력"),
                ("railHelpBtn", "도움말"),
                ("railSettingsBtn", "설정"),
            ):
                button = self.find(QPushButton, name)
                if button is not None:
                    button.setAccessibleName(label)
            # 스크린 리더 알림용 숨김 라벨
            container = self.find(QWidget, "chatContentWidget")
            if container is not None and self.find(
                    QLabel, "chatLiveLabel") is None:
                live = QLabel(container)
                live.setObjectName("chatLiveLabel")
                live.setVisible(False)
                live.setAccessibleName("생성 상태 알림")
            # 인라인 에러 라벨 (입력 행 끝, 기본 숨김)
            if self.find(QLabel, "chatInputErrorLabel") is None:
                input_row = self.find(QHBoxLayout, "inputRowLayout")
                if input_row is not None:
                    error = QLabel()
                    error.setObjectName("chatInputErrorLabel")
                    error.setStyleSheet("color: #C42B1C;")
                    error.setVisible(False)
                    input_row.addWidget(error)
        except RuntimeError:
            logger.debug("채팅 접근성 설정 실패", exc_info=True)

    def _announce(self, message: str) -> None:
        """P9: 스크린 리더에 상태 알림 (실패해도 조용히 무시)."""
        try:
            live = self.find(QLabel, "chatLiveLabel")
            if live is None:
                return
            live.setText(message)
            from PySide6.QtGui import QAccessible, QAccessibleAnnouncementEvent
            QAccessible.updateAccessibility(
                QAccessibleAnnouncementEvent(live, message))
        except Exception:
            logger.debug("스크린 리더 알림 실패", exc_info=True)

    def _show_input_error(self, message: str) -> None:
        """P9: 입력 행 인라인 에러 + 입력창 포커스."""
        try:
            error = self.find(QLabel, "chatInputErrorLabel")
            if error is not None:
                error.setText(message)
                error.setVisible(True)
            edit = self.find(QPlainTextEdit, "chatInputEdit")
            if edit is not None:
                edit.setFocus()
        except RuntimeError:
            logger.debug("인라인 에러 표시 실패", exc_info=True)

    def _clear_input_error(self) -> None:
        try:
            error = self.find(QLabel, "chatInputErrorLabel")
            if error is not None:
                error.clear()
                error.setVisible(False)
        except RuntimeError:
            pass

    def _validate_chat_text(self, text: str):
        """P9: 금지어 검증. (통과 여부, 위반 단어) 반환."""
        lowered = (text or "").lower()
        for word in BLOCKED_WORDS:
            if word and word.lower() in lowered:
                return False, word
        return True, ""

    def _maybe_greet(self) -> None:
        """P9: 저장된 세션이 하나도 없고 채팅이 비었을 때만 환영 메시지."""
        try:
            manager = getattr(self, "session_manager", None)
            if manager is not None and manager.list_sessions(limit=1):
                return
            if getattr(self, "_chat_log", None):
                return
            self._append_chat_message("ai", TEMPLATES["welcome"])
        except Exception:
            logger.debug("환영 메시지 실패", exc_info=True)

    def _reduced_motion(self) -> bool:
        """P9: 모션 감소 환경 (환경 변수로/opt-out)."""
        try:
            import os
            return os.environ.get("COMFYCRAFT_REDUCE_MOTION", "") == "1"
        except Exception:
            return False

    def _on_chat_input_changed(self) -> None:
        """P11: 채팅 입력 변경 → 5000자 강제 + 초과 시 빨간 테두리·인라인 경고."""
        try:
            ok = self._enforce_prompt_limit("chatInputEdit")
            edit = self.find(QPlainTextEdit, "chatInputEdit")
            if edit is not None:
                if ok:
                    edit.setStyleSheet("")
                    self._clear_input_error()
                else:
                    edit.setStyleSheet("border: 1px solid #C42B1C;")
                    self._show_input_error("5000자를 초과할 수 없습니다.")
        except RuntimeError:
            logger.debug("채팅 카운터 갱신 실패", exc_info=True)
        self._refresh_send_state()

    def _has_input_error_text(self) -> bool:
        try:
            error = self.find(QLabel, "chatInputErrorLabel")
            return bool(error is not None and error.text())
        except RuntimeError:
            return False

    def _is_generating(self) -> bool:
        return getattr(self, "worker", None) is not None

    def _set_send_button_state(self, generating: bool) -> None:
        try:
            button = self.find(QPushButton, "sendBtn")
            if button is None:
                return
            if generating:
                button.setText("■")
                button.setToolTip("생성 중지")
                button.setAccessibleName("생성 중지")
                button.setEnabled(True)
            else:
                button.setText("➤")
                button.setToolTip("이미지 생성하기")
                button.setAccessibleName("이미지 생성하기")
                self._refresh_send_state()
        except RuntimeError:
            logger.debug("전송 버튼 상태 변경 실패", exc_info=True)

    def _refresh_send_state(self) -> None:
        """빈 입력이면 전송 비활성화. 생성 중이면 _set_send_button_state가 관리."""
        try:
            if self._is_generating():
                return
            button = self.find(QPushButton, "sendBtn")
            edit = self.find(QPlainTextEdit, "chatInputEdit")
            if button is None or edit is None:
                return
            button.setEnabled(bool(edit.toPlainText().strip()))
        except RuntimeError:
            logger.debug("전송 버튼 갱신 실패", exc_info=True)

    def _on_send_btn_clicked(self) -> None:
        """전송 버튼: 생성 중이면 중지, 아니면 채팅 전송."""
        if self._is_generating():
            self.stop_generation()
            return
        self._send_chat_text()

    def _on_chat_enter_pressed(self) -> None:
        """Enter: 생성 중이면 무시하고 안내, 아니면 채팅 전송."""
        if self._is_generating():
            self.append_log("생성 중이에요. 기다리거나 정지 버튼(■)으로 취소해주세요.")
            return
        self._send_chat_text()

    def _on_chat_send_or_stop(self) -> None:
        """하위 호환 별칭 (버튼 클릭과 동일)."""
        self._on_send_btn_clicked()

    def _needs_zanime_style(self) -> bool:
        """P4: zanime 모델인데 스타일 미선택이면 True."""
        try:
            return bool(
                self.model_registry.is_zanime(self._comfy_model_file())
                and not self.current_zanime_style()
            )
        except Exception:
            logger.debug("zanime 스타일 필요 여부 판별 실패", exc_info=True)
            return False

    def _request_zanime_style(self, pending_text: str) -> None:
        """P4: 스타일 선택 요청 메시지 + 인라인 버튼 3개. 선택 시 자동 생성."""
        self._pending_chat = {"text": pending_text}
        self._pending_zanime_style = True
        try:
            message = self._append_chat_message(
                "ai", "Z-Anime 스타일을 골라주세요.")
            if message is None:
                return
            for style_value, style_label in ZANIME_STYLE_CHOICES:
                button = QPushButton(style_label)
                button.setObjectName(f"chatZanime_{style_value}_Btn")
                button.clicked.connect(
                    lambda _checked=False, value=style_value:
                    self._on_zanime_style_picked(value))
                message.add_action(button)
        except RuntimeError:
            logger.debug("스타일 선택 요청 실패", exc_info=True)

    def _on_zanime_style_picked(self, style_value: str) -> None:
        """P4: 인라인 스타일 선택 → 저장 + 대기 메시지 자동 생성."""
        try:
            self.select_zanime_style(style_value)
        except Exception as exc:
            self.append_log(f"스타일 저장 실패: {exc}")
            return
        self._pending_zanime_style = False
        pending = getattr(self, "_pending_chat", None)
        if pending and pending.get("text"):
            self._begin_send(pending["text"], append_user=False)

    def _send_chat_text(self) -> None:
        try:
            edit = self.find(QPlainTextEdit, "chatInputEdit")
            if edit is None:
                return
            text = normalize_prompt(edit.toPlainText())
            if not text:
                return
            ok, _hit = self._validate_chat_text(text)
            if not ok:
                self._show_input_error(TEMPLATES["blocked"])
                return
            self._clear_input_error()
            if self._needs_zanime_style():
                # 생성하지 않고 스타일 선택 요청 (원문 보관)
                self._ensure_session()
                self._append_chat_message("user", text)
                session = getattr(self, "_current_session", None)
                if isinstance(session, dict) and session.get("title", "새 대화") in ("새 대화", ""):
                    session["title"] = text[:20]
                self._flush_session()
                edit.clear()
                self._request_zanime_style(text)
                return
            self._begin_send(text, append_user=True)
        except RuntimeError:
            logger.debug("채팅 전송 실패", exc_info=True)

    def _begin_send(self, text: str, append_user: bool = True) -> None:
        """P4: 실제 전송 코어 (일반 전송·스타일 선택 후 자동 생성 공용)."""
        try:
            self._ensure_session()
            if append_user:
                self._append_chat_message("user", text)
                # 첫 사용자 메시지로 세션 제목 자동 부여
                session = getattr(self, "_current_session", None)
                if isinstance(session, dict) and session.get("title", "새 대화") in ("새 대화", ""):
                    session["title"] = text[:20]
                self._flush_session()
            # 기존 프롬프트 경로와 동기화 + 오래된 향상문 초기화 (오염 방지)
            positive = self.find(QPlainTextEdit, "positivePromptEdit")
            if positive is not None:
                positive.setPlainText(text)
            enhanced = self.find(QPlainTextEdit, "enhancePromptEdit")
            if enhanced is not None:
                enhanced.clear()
            self._pending_chat = {"text": text}
            edit = self.find(QPlainTextEdit, "chatInputEdit")
            if edit is not None:
                edit.clear()
            # P9: LM 미연결이면 향상 생략 안내
            if not self.is_lm_connected():
                self._append_chat_message("ai", TEMPLATES["lm_off"])
            self.start_generation()
            # P3: 채팅 경로로 시작됐으면 상태 버블 표시 + 신호 연결
            if self._is_generating():
                bubble = self._show_status_bubble()
                if bubble is not None and self.worker is not None:
                    try:
                        self.worker.signals.progress.connect(bubble.set_progress)
                        self.worker.signals.status.connect(bubble.set_status)
                        self.worker.signals.finished.connect(
                            lambda _ok: self._hide_status_bubble())
                    except RuntimeError:
                        logger.debug("상태 버블 신호 연결 실패", exc_info=True)
        except RuntimeError:
            logger.debug("채팅 전송 실패", exc_info=True)

    def eventFilter(self, obj, event):
        # 프로세스 종료 시점(atexit)에는 C++ Qt 객체가 이미 파괴된 뒤
        # 이 필터가 호출될 수 있다 — 무효한 객체는 조용히 통과시킨다.
        try:
            if not shiboken.isValid(obj) or not shiboken.isValid(event):
                return False
        except RuntimeError:
            return False

        try:
            # 창 종료(X 버튼) → close() 정리가 끝날 때까지 종료를 보류하고,
            # 정리 완료 후 close_timer의 _finalize_window_close가 실제 종료를 수행
            if obj is self.window and event.type() == QEvent.Type.Close:
                if getattr(self, "_close_allowed", False):
                    return False  # 정리 완료 → 실제 종료 허용
                if not getattr(self, "_closing", False):
                    self.close()
                return True  # 소비: close()가 완료될 때까지 창을 닫지 않음

            # 미리보기 라벨 크기가 바뀌면 원본 이미지를 새 크기에 맞춰 다시 스케일
            if obj is getattr(self, "_preview_label", None):
                if event.type() == QEvent.Type.Resize:
                    resize_preview(obj)
                return super().eventFilter(obj, event)

            # P2: 채팅 입력창 Enter=전송, Shift+Enter=줄바꿈
            if obj is getattr(self, "_chat_input", None):
                if event.type() == QEvent.Type.KeyPress:
                    key = event.key()
                    if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                        if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                            return False
                        self._on_chat_enter_pressed()
                        return True
                return super().eventFilter(obj, event)

            # 마우스가 사이드바에 들어오고 나갈 때 애니메이션을 실행합니다.
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
        except RuntimeError:
            # 종료 중 C++ 객체가 파괴되어 Python 오버라이드를 호출할 수 없음
            # (libshiboken: Internal C++ object already deleted) — 무시한다.
            return False

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
            f"QPushButton {{ border-radius: {CORNER_RADIUS}px; padding: 6px 8px; "
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
            # 키보드 포커스 링 (WCAG 2.1 AA) — 선택/비선택 규칙보다 뒤에 두어 항상 우선되게 한다.
            "QPushButton:focus { "
            f"border: 2px solid {sel_border}; }}"
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
                logger.debug("zanime 스타일 버튼 적용 실패: %s", button.objectName(), exc_info=True)
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
            logger.debug("부정 프롬프트 표시 판별 실패", exc_info=True)
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
            logger.debug("부정 프롬프트 높이 계산 실패", exc_info=True)

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
            logger.debug("긍정 프롬프트 높이 계산 실패", exc_info=True)

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
            logger.debug("향상 프롬프트 높이 설정 실패", exc_info=True)

    def _setup_zanime_style_buttons(self):
        """P11: 옵션 레이아웃에 zanime 스타일 버튼을 만든다."""
        if getattr(self, "_zanime_style_buttons", None) is None:
            self._zanime_style_buttons = {}
        if getattr(self, "_zanime_style_frame", None) is not None:
            self.update_zanime_style_visibility()
            return

        options_layout = self.window.findChild(QVBoxLayout, "optionsLayout")
        if options_layout is None:
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

        # P11: 옵션 레이아웃 끝에 배치 (구 step2Layout/modelSelectLayout 삭제됨)
        try:
            options_layout = self.window.findChild(QVBoxLayout, "optionsLayout")
            if options_layout is not None:
                options_layout.addWidget(frame)
            else:
                logger.debug("zanime 옵션 레이아웃 없음", exc_info=True)
        except Exception:
            logger.debug("zanime 스타일 프레임 배치 실패", exc_info=True)

        self.refresh_zanime_style_buttons()
        self.update_zanime_style_visibility()

    def is_zanime_selected(self) -> bool:
        """현재 선택된 ComfyUI 모델이 zanime 계열인지 판단한다."""
        try:
            return self.model_registry.is_zanime(self._comfy_model_file())
        except Exception:
            logger.debug("zanime 선택 판별 실패", exc_info=True)
            return False

    def current_zanime_style(self) -> str:
        """저장된 zanime 스타일 값을 소문자로 반환한다."""
        try:
            return (self.config.prompts.zanime_style or "").strip().lower()
        except Exception:
            logger.debug("zanime 스타일 가져오기 실패", exc_info=True)
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
                    logger.debug("zanime 버튼 UI 강제 업데이트 실패", exc_info=True)
            finally:
                try:
                    button.blockSignals(False)
                except Exception:
                    logger.debug("zanime 버튼 시그널 차단 해제 실패", exc_info=True)

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
        # ★ 새 스타일 선택 시 이전 향상 프롬프트 초기화 (스타일별 그림체 적용 보장)
        try:
            enhance_prompt_edit = self.find(QPlainTextEdit, "enhancePromptEdit")
            if enhance_prompt_edit is not None:
                enhance_prompt_edit.clear()
        except Exception as exc:
            self.append_log(f"프롬프트 편집창 초기화 실패: {exc}")

    def _play_zanime_style_animation(self, style_value: str) -> None:
        """선택된 스타일 버튼에 짧은 강조 애니메이션을 보여준다."""
        buttons = getattr(self, "_zanime_style_buttons", {}) or {}
        self._play_button_pulse_animation(buttons.get(style_value))

    def _play_button_pulse_animation(self, button: QPushButton | None) -> None:
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
            logger.debug("버튼 애니메이션 시작 실패", exc_info=True)
            return

    def _setup_progress_label_overlay(self):
        """P11: 진행 위젯 삭제됨 — 상태 버블이 대신 표시하므로 아무 것도 안 함."""
        return

    def _setup_elapsed_label_alignment(self):
        """P11: 진행 위젯 삭제됨 — 상태 버블이 대신 표시하므로 아무 것도 안 함."""
        return

    def _set_progress_status(self, text: str) -> None:
        """P11: 진행 상태 텍스트 (위젯이 없으면 무시)."""
        try:
            label = self.find(QLabel, "progressStatusLabel")
            if label is not None:
                label.setText(text)
        except RuntimeError:
            pass

    def _set_progress_percent(self, text: str) -> None:
        """P11: 진행률 텍스트 (위젯이 없으면 무시)."""
        try:
            label = self.find(QLabel, "progressPercentLabel")
            if label is not None:
                label.setText(text)
            bar = self.find(QProgressBar, "progressBar")
            if bar is not None:
                try:
                    bar.setValue(int(str(text).rstrip("%")))
                except (ValueError, TypeError):
                    pass
        except RuntimeError:
            pass

    def refresh_models(self):
        self._set_progress_status("모델 목록 로딩 중...")        # 그룹A 위젯(lmUrlEdit/comfyUrlEdit) 삭제 완료 — self.config 직접 사용
        lm_url = self.config.lmstudio.url or ""
        comfy_url = self.config.comfyui.url or ""

        # 이전에 성공한 URL들을 후보로 전달 (설정에서 가져오기)
        lm_candidates = [self.config.lmstudio.url] if self.config.lmstudio.url else []
        comfy_candidates = [self.config.comfyui.url] if self.config.comfyui.url else []

        resolved_lm_url = resolve_live_url("lm", lm_url, lm_candidates)
        resolved_comfy_url = resolve_live_url("comfy", comfy_url, comfy_candidates)

        # 살아있는 URL을 찾았을 때만 설정 갱신 (UI 위젯 없음 — self.config만 사용)
        if resolved_lm_url and resolved_lm_url != lm_url:
            self.config.lmstudio.url = resolved_lm_url
            lm_url = resolved_lm_url
        elif not resolved_lm_url:
            self.append_log(
                "[WARNING] LM Studio 서버를 찾을 수 없습니다. URL을 확인해주세요."
            )
            # lmStatusLabel 삭제 완료 (그룹C) — 라벨 참조 제거

        if resolved_comfy_url and resolved_comfy_url != comfy_url:
            self.config.comfyui.url = resolved_comfy_url
            comfy_url = resolved_comfy_url
        elif not resolved_comfy_url:
            self.append_log(
                "[WARNING] ComfyUI 서버를 찾을 수 없습니다. URL을 확인해주세요."
            )
            # comfyStatusLabel 삭제 완료 (그룹C) — 라벨 참조 제거

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
            # 서버 목록(object_info 기준)이 있으면 항상 우선한다.
            # 폴더 스캔은 서버에 닿지 않을 때의 예비 수단일 뿐,
            # 서버 목록을 덮어쓰지 않는다 (이상한 파일 노출 방지).
            if not status.comfy_models or status.comfy_models == ["로드된 모델 없음"]:
                status.comfy_models = fallback_models or status.comfy_models

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

        self._io_pool.submit(fetch)

    def _apply_models_result(self, lm_models, comfy_models):
        self.set_models(lm_models, comfy_models)
        self.loading_animation.stop()
        self._set_progress_status("준비 완료")

    def _comfy_model_file(self) -> str:
        """P4: 피커 표시명과 무관하게 정확한 ComfyUI 모델 파일명을 반환."""
        try:
            combo = self.find(QComboBox, "comfyModelCombo")
            if combo is None:
                return ""
            data = combo.currentData()
            if data:
                return str(data)
            return combo.currentText() or ""
        except RuntimeError:
            return ""

    def _set_comfy_model_file(self, filename: str) -> bool:
        """P4: 정확한 파일명으로 피커 선택 (표시명 기준 setCurrentText 대체)."""
        try:
            combo = self.find(QComboBox, "comfyModelCombo")
            if combo is None or not filename:
                return False
            index = combo.findData(filename)
            if index < 0:
                return False
            combo.setCurrentIndex(index)
            return True
        except RuntimeError:
            return False

    def _on_comfy_model_changed(self, index: int) -> None:
        """P4: 모델 변경 → 로그 + 최적값 자동 적용 + 시스템 메시지."""
        try:
            combo = self.find(QComboBox, "comfyModelCombo")
            if combo is None:
                return
            exact = str(combo.itemData(index) or combo.currentText() or "")
            if not exact or exact == "로드된 모델 없음":
                return
            self.log_model_selection("ComfyUI", exact)
            self.apply_model_defaults(exact)
            self.update_zanime_style_visibility()
            try:
                profile = self.model_registry.detect(exact)
                short, feature, _tooltip = describe_model(profile, exact)
                try:
                    current_label = self.find(QLabel, "modelCurrentLabel")
                    if current_label is not None:
                        current_label.setText(f"현재 모델: {short}")
                except RuntimeError:
                    pass
                self._append_chat_message(
                    "system",
                    f"{short} 모델 최적 설정이 적용되었어요 ({feature}).",
                )
            except RuntimeError:
                logger.debug("모델 변경 시스템 메시지 실패", exc_info=True)
        except RuntimeError:
            logger.debug("모델 변경 처리 실패", exc_info=True)

    def set_models(self, lm_models, comfy_models):
        lm_combo = self.find(QComboBox, "lmModelCombo")
        lm_combo.blockSignals(True)
        lm_combo.clear()
        lm_combo.addItems(lm_models or ["로드된 모델 없음"])
        if self.config.lmstudio.model in (lm_models or []):
            lm_combo.setCurrentText(self.config.lmstudio.model)
        lm_combo.blockSignals(False)
        # P4: ComfyUI 콤보는 짧은 표시명 + itemData(정확한 파일명)로 적재
        # 지원 프로필이 있는 모델만 표시한다 (registered/inferred).
        # 순수 generic 판별(매칭 패턴 없음)은 숨김 — 새 모델은 수동 프로필로 등록.
        comfy_combo = self.find(QComboBox, "comfyModelCombo")
        comfy_combo.blockSignals(True)
        comfy_combo.clear()
        supported = []
        for filename in comfy_models or []:
            try:
                profile = self.model_registry.detect(filename)
            except Exception:
                profile = None
            if profile is None or profile.name == "generic":
                continue
            supported.append(filename)
        if supported:
            used_shorts: set = set()
            for filename in supported:
                try:
                    profile = self.model_registry.detect(filename)
                except Exception:
                    profile = None
                short, feature, tooltip = describe_model(
                    profile, filename, used_shorts)
                row = comfy_combo.count()
                comfy_combo.addItem(f"{short} — {feature}", filename)
                comfy_combo.setItemData(
                    row, tooltip, Qt.ItemDataRole.ToolTipRole)
            if self.config.comfyui.model in supported:
                self._set_comfy_model_file(self.config.comfyui.model)
        else:
            comfy_combo.addItem("로드된 모델 없음")
        comfy_combo.blockSignals(False)
        self.log_model_list("LM Studio", lm_models)
        hidden = [f for f in (comfy_models or []) if f not in supported]
        self.log_model_list("ComfyUI", supported)
        if hidden:
            self.append_log(
                f"지원 프로필 없음으로 숨김: {len(hidden)}개")
        # P11: 옵션 읽기 전용 현재 모델 표시 갱신
        try:
            current_label = self.find(QLabel, "modelCurrentLabel")
            if current_label is not None:
                exact = self._comfy_model_file()
                if exact and exact != "로드된 모델 없음":
                    profile = self.model_registry.detect(exact)
                    short, _feature, _tooltip = describe_model(profile, exact)
                    current_label.setText(f"현재 모델: {short}")
        except (RuntimeError, AttributeError):
            pass
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
        # 그룹A 위젯(lmUrlEdit/comfyUrlEdit) 삭제 완료 — self.config 직접 사용
        raw_url = self.config.lmstudio.url if which == "lm" else self.config.comfyui.url
        raw_url = (raw_url or "").strip()
        resolved_url = resolve_live_url(which, raw_url)
        if resolved_url and resolved_url != raw_url:
            if which == "lm":
                self.config.lmstudio.url = resolved_url
            else:
                self.config.comfyui.url = resolved_url
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

        self._io_pool.submit(check)

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
        return bool(self.lm_connected)

    def update_connection_label(self, which, ok, extra_label=None):
        """연결 상태를 라벨과 배지 버튼에 반영합니다 (속성 기반)."""
        from app.gui.split_text_button import SplitTextButton

        # 메인 상태 라벨(lmStatusLabel/comfyStatusLabel)은 삭제됨 (그룹C) —
        # 표시는 항상 배지 버튼(lmStatusBtn/comfyStatusBtn)으로만 수행한다.
        badge = self.find(
            QPushButton, "lmStatusBtn" if which == "lm" else "comfyStatusBtn"
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
            # comfyModelPathEdit 삭제 완료 (그룹A) — self.config 직접 사용
            # comfyui_model_paths 리스트에 추가 (중복 제거, 최신 순)
            self.config.comfyui_model_paths = [folder] + [
                p for p in self.config.comfyui_model_paths if p != folder
            ]
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
            # modelPathStatusLabel 삭제 완료 (그룹C) — 라벨 참조 제거
            pass
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

        # 그룹A 위젯 삭제 완료 — self.config 직접 사용 (UI 입력칸 없음)
        # self.find(QLineEdit, "lmUrlEdit").setText(self.config.lmstudio.url)  # 삭제됨
        # self.find(QLineEdit, "comfyUrlEdit").setText(self.config.comfyui.url)  # 삭제됨
        if self.config.lmstudio.model:
            self.find(QComboBox, "lmModelCombo").setCurrentText(
                self.config.lmstudio.model
            )
        if self.config.comfyui.model:
            # P4: 표시명이 아닌 itemData(정확한 파일명) 기준으로 복원
            self._set_comfy_model_file(self.config.comfyui.model)

        model_paths = self.config_manager.get_model_base_paths()
        if model_paths:
            first_path = str(model_paths[0])
            # comfyModelPathEdit 위젯 삭제됨 (그룹A) — 경로는 self.config에 있으므로 검증만 갱신
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
            logger.debug("스플리터/사이드바 비율 적용 실패", exc_info=True)
        # (이전 QSplitter 비율 코드는 구조 변경으로 제거됨)
        # (helpBrowser 전용 헬퍼 _render_markdown_file/_setup_help_tab은
        #  helpBrowser 위젯 삭제와 함께 제거됨 — 도움말은 help_dialog_v2가 담당)

    def save_config(self):
        """설정 값을 저장합니다."""
        # LM Studio URL 및 모델 업데이트 (그룹A 위젯 삭제 — self.config 직접 사용)
        # self.config.lmstudio.url = self.find(QLineEdit, "lmUrlEdit").text().strip()  # 삭제됨
        self.config.lmstudio.model = self.find(QComboBox, "lmModelCombo").currentText()

        # ComfyUI URL 및 모델 업데이트
        # self.config.comfyui.url = self.find(QLineEdit, "comfyUrlEdit").text().strip()  # 삭제됨
        self.config.comfyui.model = self._comfy_model_file()

        # ComfyUI 모델 경로 업데이트 (그룹A 위젯 삭제 — self.config 직접 사용)
        # model_path = self.find(QLineEdit, "comfyModelPathEdit").text().strip()  # 삭제됨
        model_path = self.config.comfyui_model_paths[0] if self.config.comfyui_model_paths else ""
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
                logger.debug("FaceDetailer 슬라이더 '%s' 설정 실패", slider_name, exc_info=True)

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
        prompt_text = self._find_or_raise(QPlainTextEdit, "positivePromptEdit").toPlainText()
        negative_text = self._find_or_raise(QPlainTextEdit, "negativePromptEdit").toPlainText()
        # P4: 표시명이 아닌 itemData(정확한 파일명) 기준. 빈 값은
        # GenerationWorker가 "ComfyUI 모델을 선택해주세요."로 처리한다.
        comfy_model_name = self._comfy_model_file()
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
        enhance_prompt_text = self._find_or_raise(
            QPlainTextEdit, "enhancePromptEdit"
        ).toPlainText()
        generation_settings = build_generation_snapshot(
            {
                "width": self._find_or_raise(QSpinBox, "widthSpinBox").value(),
                "height": self._find_or_raise(QSpinBox, "heightSpinBox").value(),
                "steps": self.get_steps_value(),
                "cfg": self.get_cfg_value(),
                "seed": self._find_or_raise(QSpinBox, "seedSpinBox").value(),
                "sampler": SAMPLER_NAMES.get(
                    self._find_or_raise(QComboBox, "samplerComboBox").currentText(), "euler"
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
            "lm_url": self.config.lmstudio.url or "",
            "lm_model": self.find(QComboBox, "lmModelCombo").currentText(),
            "comfy_url": self.config.comfyui.url or "",
            "comfy_model": self._comfy_model_file(),
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
                    logger.debug("FD 스냅샷 키 '%s' 복원 실패", key, exc_info=True)

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

        lm_url = self.config.lmstudio.url or ""
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
        self._set_progress_status("프롬프트 향상 중...")

        ext_prompts = load_external_prompts()

        # ComfyUI 모델 타입에 따라 시스템 프롬프트 자동 선택 (generation.py와 동일 로직)
        # P4: 표시명이 아닌 정확한 파일명 기준
        comfy_model_name = self._comfy_model_file()
        profile = self.model_registry.detect(comfy_model_name)
        manager = self.workflow_manager

        is_flux = self.model_registry.is_flux(comfy_model_name)
        is_zimage = self.model_registry.is_zimage(comfy_model_name)
        is_ernie = self.model_registry.is_ernie(comfy_model_name)
        is_zanime = self.model_registry.is_zanime(comfy_model_name)

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
        elif is_ernie:
            self.append_log(
                f"[AI 자동 분석] '{comfy_model_name}' 모델 감지: 'ERNIE 전용' 프롬프트 지시문을 사용합니다."
            )
            system_prompt = ext_prompts.get("system_prompt_ernie_en") or ext_prompts.get("system_prompt_flux_en") or ""
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

        # 기존 워커가 실행 중이면 먼저 중단 (메모리 누수/스레드 누수 방지)
        old_worker = getattr(self, '_prompt_enhance_worker', None)
        if old_worker is not None and old_worker.isRunning():
            old_worker.quit()
            old_worker.wait(2000)

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
        self.show_error_banner(f"✖ 프롬프트 향상 실패 — {error_msg}")
        self._reveal_log_on_error()
        show_message_box(
            self.window, QMessageBox.Icon.Warning, "프롬프트 향상 실패", error_msg
        )
        self._set_progress_status("준비 완료")

    def _apply_enhanced_prompt(self, enhanced_prompt):
        """향상된 프롬프트를 enhancePromptEdit에 적용"""
        prompt_edit = self.find(QPlainTextEdit, "enhancePromptEdit")
        if prompt_edit:
            prompt_edit.setPlainText(enhanced_prompt)
        else:
            self.append_log("[ERROR] enhancePromptEdit을 찾을 수 없음!")
        self.append_log(f"프롬프트 향상 완료: {enhanced_prompt[:100]}...")
        self._set_progress_status("준비 완료")

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
                            logger.debug("생성 버튼 시그널 복원 실패", exc_info=True)
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

        # 새 생성 시작 시 이전 에러 배너를 지운다
        self.clear_error_banner()

        # 🚀 중복되지 않도록 시그널 이벤트를 딱 1번만 연결합니다.
        self.worker.signals.enhanced_prompt.connect(self._apply_enhanced_prompt)
        self.worker.signals.progress.connect(self.set_progress)
        self.worker.signals.status.connect(
            lambda text: self._set_progress_status(text)
        )
        self.worker.signals.log.connect(self.append_log)
        self.worker.signals.image.connect(lambda path: self.show_image(path, add_history=True))
        self.worker.signals.error.connect(self._on_generation_error)
        self.worker.signals.finished.connect(self.generation_finished)

        # UI 및 타이머 상태 업데이트
        self.generation_started_at = time.monotonic()
        self.elapsed_timer.start()

        self.loading_animation.start("이미지 생성 중...")
        self.append_log("이미지 생성을 시작했습니다.")

        # 🌟 생성 시작: 다른 모든 입력/선택 위젯 비활성화 (실수 방지)
        self._set_ui_enabled(False)
        # P2: 채팅 전송 버튼을 정지 버튼으로 전환
        self._set_send_button_state(True)

        # 🚀 단 1번만 백그라운드 스레드를 가동합니다.
        self._gen_pool.submit(self.worker.run)

    def stop_generation(self):
        with self._generation_lock:
            if self.worker:
                self.worker.stop()
                self.append_log("생성 중지를 요청했습니다.")
                self._set_progress_status("중단 중...")
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

    # ──────────────────────────────────────────────────────────────────────
    # UI 활성화/비활성화 토글 (이미지 생성 중 실수 방지용)
    # ──────────────────────────────────────────────────────────────────────

    def _set_ui_enabled(self, enabled: bool):
        """이미지 생성 시작/종료 시 모든 입력·선택 위젯의 사용 가능 여부를 토글합니다.

        생성 버튼(generateButton) 자체는 정지 기능을 위해 항상 활성 상태로 둡니다.
        """
        if not hasattr(self, "_ui_enabled_widgets"):
            self._ui_enabled_widgets = []
            # 빈도가 높은 위젯은 한 번만 찾아서 저장해 둔다.
            targets = [
                # --- P2 채팅 입력 행 (생성 중 잠금, sendBtn은 정지용으로 제외) ---
                "chatInputEdit",
                "newChatBtn",
                # --- 프롬프트 ---
                "positivePromptEdit",
                "negativePromptEdit",
                "enhancePromptEdit",
                "enhancePromptButton",
                # --- 모델 선택 ---
                "lmModelCombo",
                "comfyModelCombo",
                # --- 생성 파라미터 ---
                "widthSpinBox",
                "heightSpinBox",
                "seedSpinBox",
                "cfgSlider",
                "stepsSlider",
                "samplerComboBox",
                "schedulerComboBox",
                "denoiseSpinBox",
                "randomSeedButton",
                "lockSeedButton",
                # --- 프리셋 ---
                "preset_1024x1024",
                "preset_896x1152",
                "preset_1152x896",
                "preset_512x512",
                "preset_768x768",
                "preset_832x1216",
                "preset_1216x832",
                # --- 기타 기능 버튼 ---
                "openOutputFolderButton",
                "facedetailerHelpBtn",
            ]
            for name in targets:
                for widget in self.window.findChildren(QWidget, name):
                    self._ui_enabled_widgets.append(widget)
            # 썸네일 버튼 4개
            for i in range(4):
                for widget in self.window.findChildren(QPushButton, f"thumbBtn_{i}"):
                    self._ui_enabled_widgets.append(widget)
            # 중복 제거
            self._ui_enabled_widgets = list(dict.fromkeys(self._ui_enabled_widgets))

        for widget in self._ui_enabled_widgets:
            try:
                widget.setEnabled(enabled)
            except Exception:
                logger.debug("위젯 활성화 토글 실패: %s", getattr(widget, 'objectName', lambda: '?')(), exc_info=True)

    # ──────────────────────────────────────────────────────────────────────
    # 생성 시작/종료 시 UI 토글 통합 호출부
    # ──────────────────────────────────────────────────────────────────────


    def _on_generation_error(self, text: str):
        """이미지 생성 중 오류 발생 시 호출 (채팅 메시지 + 로그)."""
        self.append_log(f"생성 오류: {text}")
        self.show_error_banner(text)
        self._announce(TEMPLATES["failed"].format(reason=text))

    def generation_finished(self, success):
        self.elapsed_timer.stop()
        self.loading_animation.stop()
        with self._generation_lock:
            self.worker = None
        btn = self.find(QPushButton, "generateButton")
        if btn is not None:
            btn.setChecked(False)
        # P11: 진행 위젯 삭제됨 — 상태 버블이 대신 표시
        self._set_progress_status(
            "생성 완료" if success else "생성 실패 또는 중단")
        self._set_progress_percent("100%" if success else "0%")
        update_execution_status(
            self.execution_status,
            100 if success else 0,
            "생성 완료" if success else "생성 실패 또는 중단",
        )
        # 🌟 생성 완료: 다른 모든 입력/선택 위젯 다시 활성화
        self._set_ui_enabled(True)
        # P2: 채팅 전송 버튼을 전송 상태로 복원
        self._set_send_button_state(False)
        # P3: 상태 버블 제거 (finished 신호에서도 제거되므로 중복 안전)
        self._hide_status_bubble()
        # P9: 완료 알림
        self._announce("이미지 생성이 완료되었습니다." if success else
                       "이미지 생성이 실패 또는 중단되었습니다.")

        if success:
            self.append_log("이미지 생성이 완료되었습니다.")

    def set_progress(self, value):
        """진행 상황을 표시. 실제 진행률이 들어오면 애니메이션 정지."""
        update_execution_status(self.execution_status, value, "이미지 생성 중")

        if value > 0:
            self.loading_animation.stop()

        self.loading_animation.set_real_progress(value)
        # P11: 진행 위젯 삭제됨 — 상태 버블이 대신 표시
        self._set_progress_percent(f"{value}%")

    def update_counter(self, edit_name, label_name=None):
        """P11: 카운터 라벨 삭제됨 — 길이 제한 강제만 수행한다."""
        return self._enforce_prompt_limit(edit_name)

    def _enforce_prompt_limit(self, edit_name: str) -> bool:
        """입력 길이를 5000자로 강제. 초과분을 잘랐으면 False."""
        try:
            editor = self._find_or_raise(QPlainTextEdit, edit_name)
        except RuntimeError:
            return True
        try:
            text = editor.toPlainText()
            limited_text = enforce_prompt_character_limit(
                text, PROMPT_MAX_CHARACTERS
            )
            if limited_text != text:
                editor.setPlainText(limited_text)
                return False
            return True
        except RuntimeError:
            return True

    def append_log(self, message):
        # Qt 로깅 핸들러 위임 (QPlainTextEditLogger + FileHandler)
        logger.info("%s", message)
        stamped = f"[{datetime.now():%H:%M:%S}] {message}"  # noqa: DTZ005
        try:
            self._log_buffer.append(stamped)
        except AttributeError:
            from collections import deque
            self._log_buffer = deque([stamped], maxlen=5000)
        editor = self.find(QPlainTextEdit, "logTextEdit")
        if editor:
            try:
                editor.appendPlainText(stamped)
            except RuntimeError:
                pass
        # P11: 로그 탭이 열려 있으면 flush
        try:
            tab = getattr(self, "_log_tab_edit", None)
            if tab is not None and shiboken.isValid(tab):
                tab.appendPlainText(stamped)
                bar = tab.verticalScrollBar()
                bar.setValue(bar.maximum())
                while tab.document().blockCount() > 5000:
                    cursor = tab.textCursor()
                    cursor.movePosition(cursor.MoveMode.Start)
                    cursor.select(cursor.SelectionType.LineUnderCursor)
                    cursor.removeSelectedText()
                    cursor.deleteChar()
        except (RuntimeError, AttributeError):
            pass

    def get_log_lines(self) -> list:
        """P11: 설정 로그 탭 초기 표시용."""
        try:
            return list(self._log_buffer)
        except AttributeError:
            return []

    # ──────────────────────────────────────────────────────────────────────
    # 에러 배너 (UI/UX 4단계: 실패 시 뷰어 헤더에 한 줄 요약을 보여줌)
    # 사용법: show_error_banner("메시지") → 표시 / clear_error_banner() → 숨기기
    # 배너를 클릭하면 로그창을 펼쳐 자세한 오류 내용을 보여준다.
    # ──────────────────────────────────────────────────────────────────────

    def show_error_banner(self, message: str):
        """에러를 채팅 AI 메시지로 표시한다 (배너 위젯 없음).

        [다시 시도] [프롬프트 수정] [로그 보기] 버튼 포함.
        빈 메시지면 아무 것도 안 한다 (메시지는 기록으로 남는다).
        """
        if not message:
            return
        try:
            chat_message = self._append_chat_message("ai", f"이미지 생성에 실패했어요. 원인: {message}")
            if chat_message is None:
                return
            retry_button = QPushButton("다시 시도")
            retry_button.setObjectName("chatErrRetryBtn")
            retry_button.clicked.connect(self._retry_last_request)
            edit_button = QPushButton("프롬프트 수정")
            edit_button.setObjectName("chatErrEditBtn")
            edit_button.clicked.connect(self._reuse_last_snapshot)
            log_button = QPushButton("로그 보기")
            log_button.setObjectName("chatErrLogBtn")
            log_button.clicked.connect(
                lambda: self._show_settings_dialog(initial_tab="로그"))
            chat_message.add_action(retry_button)
            chat_message.add_action(edit_button)
            chat_message.add_action(log_button)
            self._scroll_chat_to_bottom()
        except RuntimeError:
            logger.debug("채팅 오류 메시지 표시 실패", exc_info=True)

    def clear_error_banner(self):
        """채팅 방식에서는 지울 배너가 없다 (기록 유지). 호환용 유지."""
        return

    def _last_user_text(self) -> str:
        """마지막 사용자 메시지 텍스트 (다시 시도용)."""
        try:
            for record in reversed(getattr(self, "_chat_log", [])):
                if isinstance(record, dict) and record.get("kind") == "user":
                    return str(record.get("text", ""))
        except Exception:
            pass
        return ""

    def _last_snapshot(self) -> dict:
        """마지막 생성 스냅샷 (프롬프트 수정용)."""
        try:
            for record in reversed(getattr(self, "_chat_log", [])):
                if (isinstance(record, dict) and record.get("kind") == "image"
                        and record.get("snapshot")):
                    return dict(record["snapshot"])
        except Exception:
            pass
        return {}

    def _retry_last_request(self) -> None:
        """[다시 시도] 마지막 사용자 요청으로 재생성."""
        if self._is_generating():
            self.append_log("생성 중이에요. 기다리거나 취소해주세요.")
            return
        text = self._last_user_text()
        if text:
            self._begin_send(text, append_user=False)

    def _reuse_last_snapshot(self) -> None:
        """[프롬프트 수정] 마지막 스냅샷으로 수정 요청."""
        snapshot = self._last_snapshot()
        if snapshot:
            self._on_reuse_request(snapshot)
        else:
            self.append_log("수정할 이전 생성 결과가 없어요.")

    def _reveal_log_on_error(self):
        """에러 발생 시 접혀 있던 로그창을 자동으로 펼쳐준다."""
        log_group = getattr(self, "log_group", None)
        if log_group is not None and not log_group.isVisible():
            log_group.setVisible(True)
            self.log_visible = True
            btn = self.find(QPushButton, "toggleLogButton")
            if btn and hasattr(self, "icon_collapse"):
                btn.setIcon(self.icon_collapse)

    def _on_error_banner_clicked(self):
        """에러 배너 클릭 시 로그창을 펼쳐 자세한 오류를 보여준다."""
        self._reveal_log_on_error()

    def clear_logs(self):
        # P11: 링버퍼 + 열린 로그 탭을 비운다 (메인 로그창 삭제됨)
        try:
            self._log_buffer.clear()
        except AttributeError:
            from collections import deque
            self._log_buffer = deque(maxlen=5000)
        try:
            tab = getattr(self, "_log_tab_edit", None)
            if tab is not None and shiboken.isValid(tab):
                tab.clear()
        except (RuntimeError, AttributeError):
            pass
        self.append_log("로그를 초기화했습니다.")

    def show_image(self, path, add_history=False):
        self.current_image_path = path
        # P11: 미리보기 라벨 삭제됨 — 채팅 카드+모달이 대신 표시
        preview_label = self.find(QLabel, "previewLabel")
        if preview_label is not None:
            show_image(preview_label, path)
        # 새로 생성된 이미지일 때만 히스토리(썸네일)에 추가
        if add_history:
            try:
                snapshot = self.capture_snapshot()
                self.add_to_history(path, snapshot)
            except Exception as e:
                logger.warning("히스토리 추가 실패: %s", e, exc_info=True)
        # P2: 채팅 전송 대기 건이 있으면 AI 응답 + 이미지 카드 추가
        pending = getattr(self, "_pending_chat", None)
        if pending:
            self._pending_chat = None
            try:
                snapshot = self.capture_snapshot()
                started = getattr(self, "generation_started_at", None)
                if started is not None:
                    elapsed = format_elapsed(int(time.monotonic() - started))
                else:
                    elapsed = "?초"
                enhanced = self.find(QPlainTextEdit, "enhancePromptEdit")
                prompt_text = ""
                if enhanced is not None:
                    prompt_text = enhanced.toPlainText().strip()
                if not prompt_text:
                    prompt_text = pending.get("text", "")
                self._append_image_card(path, snapshot, elapsed, prompt_text)
                # P6: 생성 완료 시점 저장 (트리거 ②)
                self._flush_session()
            except Exception as e:
                logger.warning("채팅 이미지 카드 추가 실패: %s", e, exc_info=True)

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

    def _close_thread_pools(self):
        """스레드 풀을 안전하게 종료 (cancel_futures로 대기 중 작업 취소)"""
        for pool in (self._io_pool, self._gen_pool):
            if pool is not None:
                try:
                    pool.shutdown(wait=False, cancel_futures=True)
                except Exception:
                    logger.debug("스레드 풀 종료 실패", exc_info=True)

    def close(self):
        self._closing = True
        self._close_thread_pools()
        if self.close_timer.isActive():
            return
        self.window.setEnabled(False)

        progress_label = self.find(QLabel, "progressStatusLabel")
        if progress_label is not None:
            progress_label.setText("종료 중...")
        percent_label = self.find(QLabel, "progressPercentLabel")
        if percent_label is not None:
            percent_label.setText("")

        # PromptEnhanceWorker 정리
        pw = getattr(self, '_prompt_enhance_worker', None)
        if pw is not None and pw.isRunning():
            pw.quit()
            pw.wait(2000)

        if self.worker:
            self.worker.stop()
            self.append_log("작업을 정리한 뒤 종료합니다...")
            # Worker 완료 시그널 연결 + 최대 1.5초 대기 후 강제 종료
            # (stop()이 interrupt/clear_queue를 호출하므로 정상 워커는 1초 내 종료됨)
            self.worker.signals.finished.connect(
                lambda _: self.close_timer.start(100)
            )
            from PySide6.QtCore import QTimer
            QTimer.singleShot(1500, lambda: self.close_timer.start(0) if not self.close_timer.isActive() else None)
        else:
            self.close_timer.start(100)

    def _finalize_window_close(self):
        """정리(close())가 모두 끝난 뒤 실제 창 종료를 허용하고 수행한다."""
        # P6: 종료 시 마지막 세션 저장 (트리거 ④)
        try:
            self._flush_session()
        except Exception:
            logger.debug("종료 시 세션 저장 실패", exc_info=True)
        self._close_allowed = True
        self.window.close()

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
                        logger.debug("FD 슬라이더 라벨 동기화 실패", exc_info=True)
                slider.valueChanged.connect(on_val)
                # 초기 표시도 맞춤
                try:
                    label.setText(fmt(slider.value()))
                except Exception:
                    logger.debug("FD 슬라이더 초기 라벨 설정 실패", exc_info=True)

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
            neg_frame.setVisible(self._should_show_negative_prompt(self._comfy_model_file()))
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
        # 항상 원본 파일 우선 복사 (미리보기용으로 축소된 픽스맵 화질 손실 방지)
        if self.current_image_path and Path(self.current_image_path).exists():
            pix = QPixmap(str(self.current_image_path))
            if not pix.isNull():
                QApplication.clipboard().setPixmap(pix)
                btn = self.find(QPushButton, "copyImageButton")
                if btn:
                    orig_text = btn.text()
                    btn.setText("✓ 복사 완료!")
                    QTimer.singleShot(1500, lambda: btn.setText(orig_text))
                self.append_log("결과 이미지가 클립보드에 복사되었습니다. (Ctrl+V로 붙여넣기 가능)")
                return

        label = self.find(QLabel, "previewLabel")
        if label and label.pixmap() and not label.pixmap().isNull():
            QApplication.clipboard().setPixmap(label.pixmap())
            btn = self.find(QPushButton, "copyImageButton")
            if btn:
                orig_text = btn.text()
                btn.setText("✓ 복사 완료!")
                QTimer.singleShot(1500, lambda: btn.setText(orig_text))
            self.append_log("결과 이미지가 클립보드에 복사되었습니다. (Ctrl+V로 붙여넣기 가능)")
        else:
            show_message_box(self.window, QMessageBox.Icon.Information, "알림", "복사할 이미지가 없습니다.")

    def _show_settings_dialog(self, initial_tab: str | None = None):
        """설정 다이얼로그(.ui 파일 기반)를 표시한다.

        연결 버튼(comfyStatusBtn, lmStatusBtn), 사이드바 설정 버튼(settingsButton)
        모두 이 창으로 연결된다.
        실제 구현은 app/gui/dialogs/settings_dialog.py에 있다.
        """
        show_settings_dialog(self, initial_tab=initial_tab)

    def _show_help_dialog(self):
        """도움말 다이얼로그(v2: 좌우 분할)를 표시한다. 비모달 방식으로 메인 화면과 병행 사용 가능.

        실제 구현은 app/gui/dialogs/help_dialog.py에 있다.
        """
        show_help_dialog(self)

    def _show_facedetailer_guide(self):
        """❓ 얼굴 보정(FaceDetailer) 초보자 가이드 다이얼로그.

        실제 구현은 app/gui/dialogs/facedetailer_guide_dialog.py에 있다.
        """
        show_facedetailer_guide(self)

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

        self._restore_snapshot(snap)
        self.append_log(f"최근 생성 기록 [{index + 1}번]의 설정 및 프롬프트를 성공적으로 복원했습니다.")

    def _restore_snapshot(self, snap: dict) -> None:
        """P6: 스냅샷 전체를 UI에 복원 (프롬프트+모델+옵션). 썸네일·재사용 공용."""
        if not isinstance(snap, dict) or not snap:
            return
        try:
            # 2. 프롬프트 복원
            if "prompt" in snap:
                self.find(QPlainTextEdit, "positivePromptEdit").setPlainText(snap.get("prompt", ""))
            if "enhance_prompt" in snap and snap.get("enhance_prompt"):
                self.find(QPlainTextEdit, "enhancePromptEdit").setPlainText(snap.get("enhance_prompt", ""))
            if "negative" in snap:
                self.find(QPlainTextEdit, "negativePromptEdit").setPlainText(snap.get("negative", ""))

            # 3. 모델 및 해상도, 시드, CFG, 스텝 복원
            if "comfy_model" in snap:
                # P4: 정확한 파일명으로 복원 (표시명 기준 setCurrentText 대체)
                self._set_comfy_model_file(snap.get("comfy_model"))
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
                    logger.debug("zanime 스타일 복원 실패", exc_info=True)
            self.update_zanime_style_visibility()

            # 4. FaceDetailer 옵션 복원
            self._restore_facedetailer_from_snapshot(snap)
        except RuntimeError:
            logger.debug("스냅샷 복원 실패", exc_info=True)

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
