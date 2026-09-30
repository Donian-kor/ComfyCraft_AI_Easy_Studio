"""좌측 생성 옵션 패널 (원본 UI 의 leftScrollArea / optionsLayout).

원본 구조에서 옵션은 좌측에 붙어 있고, 프롬프트 입력과 전송은
챗봇 화면 아래에 있다. 따라서 이 패널에는 '무엇을 만들지 대한 설정'만
들고, 프롬프트 입력창은 두지 않는다.
"""

from __future__ import annotations

from typing import Callable, List, Optional

import flet as ft

from app.features.prompt.prompts import SCHEDULER_NAMES, SAMPLER_NAMES
from app.models.generation import GenerationRequest
from app.ui.flet.components.common import (
    framed_box,
    framed_section,
    overlayed_counter,
    collapsible,
    option_row,
    safe_update,
)
from app.ui.flet.components.facedetailer import (
    FD_GROUPS as _FD_GROUPS,
)
from app.ui.flet.components.facedetailer import (
    SAM_HINT_OPTIONS,
)
from app.ui.flet.components.facedetailer import (
    FD_LABEL_WIDTH,
    FD_SLIDER_WIDTH,
    FD_VALUE_WIDTH,
    GRID_COLUMN_WIDTH,
    FaceDetailerPanel,
)
from app.ui.flet.pages.fd_sliders import (
    GRID_DIVIDER,
    GRID_DIVIDER_GAP,
    GRID_DIVIDER_TOTAL,
    build_grid,
)
from app.ui.flet.pages.model_defaults import (
    format_notice,
    model_supports_negative,
    resolve_cfg,
    resolve_sampler,
    resolve_scheduler,
    resolve_steps,
)
from app.ui.flet.theme.tokens import TOKENS, radius
from app.ui.flet.ui_loop import is_ui_thread, run_on_ui

SAMPLER_OPTIONS = [(label, value) for label, value in SAMPLER_NAMES.items()]
SCHEDULER_OPTIONS = [(name, name) for name in SCHEDULER_NAMES]

RESOLUTION_PRESETS = ["1152x896", "1024x1024", "896x1152",
                      "832x1216", "768x1344", "512x512"]

# --- 좌측 옵션 패널 폭 ------------------------------------------------------
# 패널 폭은 '화면에서 얼마나 자주 보이는가' 로 정한다.
# 2열로 압축했으므로 항목 수는 줄지만, 슬라이더는 값 조절하는 컨트롤이라
# 좁으면 조작하기 힘들다. 그래서 원본(420)과 비슷한 420 을 쓴다.
#   420 - 여백 48 = 372, 들여쓰기 16 차감 = 356, 2열 한 칸 = 172
PANEL_WIDTH = 420          # 패널 전체 폭
PANEL_PADDING = 24         # 패널 안쪽 여백 (TOKENS.space_lg)
CONTENT_WIDTH = PANEL_WIDTH - PANEL_PADDING * 2   # 실제 본문 폭(372)

# 각 섹션은 framed_section 으로 감싸져 있고, 거기에 안쪽 여백이 있다.
# 이 여백만큼 빼지 않으면 안쪽 컨트롤이 프레임 밖으로 나가서
# 우측이 잘린다(라벨/드롭다운 화살표/슬라이더 끝이 보인다).
#
# 회귀 근거: 프레임을 넣은 뒤 FIELD_WIDTH 를 그대로 써서 24px 넘침이
# 났다. 화면에선 '오른쪽이 잘려 보인다'로만 보였고 이유를 알기 어려웠다.
FRAME_PADDING = TOKENS.space_md          # framed_section 의 padding.all
INNER_WIDTH = CONTENT_WIDTH - FRAME_PADDING * 2   # 프레임 안쪽 본문 폭(348)

FIELD_WIDTH = INNER_WIDTH            # 1열로 쓸 때 (드롭다운/텍스트 필드)
# 2열 그리드. 두 곳에서 쓰이는데, 들어갈 공간이 서로 다르다.
#   * 패널 본문 직속(_grid)          : INNER_WIDTH (348)
#   * collapsible 안쪽(들여쓰기 16) : 348 - 16 = 332
# 두 곳 중 좁은 쪽에 맞춰야, 안쪽에서 2열이 조용히 1줄로 접히지 않는다.
# (줄은 build_grid() 가 두 개씩 묶어 직접 만들므로 자동 줄바꿈에 의존하지 않는다)
_COLLAPSE_INDENT = TOKENS.space_lg
GRID_AVAILABLE = INNER_WIDTH - _COLLAPSE_INDENT        # 332
# 한 줄 폭 = 칸 + (왼쪽 여백 + 구분선 + 칸) 이므로 구분선 자리를 빼고
# 두 칸에 나눠야 한다. 이걸 빠뜨리면 한 줄이 GRID_AVAILABLE 를 넘겨
# collapsible 안쪽에서 칸이 잘린다.
# GRID_COLUMN_WIDTH / FD_* 는 FaceDetailer 패널과 공유해야 한 칸이 어긋나지
# 않는다. 컴포넌트가 실제 값을 계산해owns 하고, 여기서는 재노출만 한다.
# //2 로 버림하면 1px 가 남아 줄 폭이 GRID_AVAILABLE 보다 작아지고,
# 오른쪽에 빈틈이 보인다. /2(실수)로 나눠 정확히 맞춘다.
assert GRID_COLUMN_WIDTH == (GRID_AVAILABLE - GRID_DIVIDER_TOTAL) / 2, (
    "FaceDetailer 패널의 2열 칸 폭이 옵션 패널 계산과 어긋난다")
# 2열로 배치한 입력 필드도 한 칸 폭에 맞춘다.
GRID_FIELD_WIDTH = GRID_COLUMN_WIDTH
# option_row 는 [라벨][컨트롤] 2조각이라 컨트롤 폭을 줄여야 라벨까지 들어간다.
# labelColumnWidth 는 라벨을 '고정폭' 으로 잡아 정렬을 맞춘다.
# (길이가 다른 라벨이 매 줄마다 다른 자리에서 시작하면 답답해 보인다)
ROW_LABEL_WIDTH = 78                # 라벨(최장 "Scheduler" + 여백)
# 회귀 근거(사용자 지적 2회): '기본 옵션' 은 framed_box(여백 12) 안의
# collapsible 안에 있다. collapsible 본문(panel) 에 padding.left=16 이
# 있어서, 실제 쓸 수 있는 폭은 INNER_WIDTH - 16 이다. 이 16px 를 빼먹어
# 드롭다운 화살표가 프레임 밖으로 잘렸다.
COLLAPSE_BODY_INDENT = TOKENS.space_lg
ROW_AVAILABLE = INNER_WIDTH - COLLAPSE_BODY_INDENT
ROW_CONTROL_WIDTH = ROW_AVAILABLE - ROW_LABEL_WIDTH - TOKENS.space_sm


# --- FaceDetailer ----------------------------------------------------------
# 원본 Qt UI 는 슬라이더마다 (Label + Slider + 값 Label) 3개 위젯을 .ui 에
# 직접 적어 15종을 노출했다. 슬라이더를 하나라도 빼면 그 항목은 화면에서
# 조용히 사라지고 사용자는 "원래 없던 기능 같다"고 느낀다.
#
# 그래서 여기서 목록을 하드코딩하지 않는다. app.constants 의 스펙을 그대로
# 읽어 15종을 만들고, 스펙이 늘면 화면도 따라 늘어나게 한다.
#
# 스펙 형식: (키, 위젷 이름, 기본값, 배율, 64단위 여부)
#   - 배율 100.0 이면 Qt 의 0~100 정수 슬라이더를 원래 값(0~1 실수)으로 되돌린다.
#   - 64단위면 0~16 정수(×64)였고, 원래 값은 guide_size=256 처럼 64의 배수다.

# FaceDetailer 의 라벨·그룹·드롭다운 항목과 슬라이더는 모두
# components/facedetailer.py 가 소유한다(600줄 제한 + 중복 방지).
# 아래는 기존 테스트와 외부 호출이 이름을 직접 참조하므로 재노출한다.
# 실제 컨트롤은 한 벌만 존재하며, 여기서 만드는 것이 아니라 위임한다.



def parse_resolution(text: str, fallback: tuple = (1152, 896)) -> tuple:
    """'1152x896' 같은 해상도 문자열을 (w, h) 로 바꾼다."""
    try:
        w, h = str(text or "").lower().split("x", 1)
        return int(w), int(h)
    except (ValueError, AttributeError):
        return fallback


class OptionsPanel:
    """생성 옵션 (모델 / 해상도 / Steps / CFG / Seed / FaceDetailer)."""

    def __init__(self, *, model_names: Optional[List[str]] = None,
                 model_registry=None) -> None:
        self._model_names = list(model_names or [])
        # 모델 프로필 검색기. 모델을 바꾸면 최적값을 적용하는 데 쓴다.
        # (원본 Qt 의 MainController.model_registry 와 같은 역할)
        self._registry = model_registry

        # Dropdown 의 label 속성에는 라벨을 두지 않는다.
        # 바깥에서 _label() 로 제목 Text 를 붙이므로, 둘 다 넣으면
        # 'ComfyUI 모델' 위에 '모델' 이 겹쳐 보이고, 남은 zh-hans 글자
        # ('模型')까지 그대로 노출된다. 한 곳에서만 라벨을 만든다.
        self._model_dropdown = ft.Dropdown(
            options=[ft.DropdownOption(key=n, text=n) for n in self._model_names],
            value=self._model_names[0] if self._model_names else None,
            width=FIELD_WIDTH, dense=True)
        self._lm_model_dropdown = ft.Dropdown(
            options=[], width=FIELD_WIDTH, dense=True)
        self._resolution_dropdown = ft.Dropdown(
            options=[ft.DropdownOption(key=r, text=r) for r in RESOLUTION_PRESETS],
            value=RESOLUTION_PRESETS[0], width=FIELD_WIDTH, dense=True)
        self._seed_field = ft.TextField(
            hint_text="-1 = 랜덤", value="-1", width=FIELD_WIDTH, dense=True)
        # 포스티프 프롬프트. 채팅 입력칸의 짧은 설명을 LM Studio 가
        # '향상된 프롬프트'로 바꿔 여기 돌려준다(원본 Qt 의
        # positivePromptEdit). 읽기 전용: 직접 고치면
        # '향상을 건너뛴다' 경로로 빠져 Enhancing 이 안 일어난다.
        # 글자수 카운터 + 초과 배지. 채팅 입력칸이 아니라 *여기*
        # (포스티프 칸) 안쪽 우측 위에 보여야 한다(사용자 요청).
        self._prompt_counter = ft.Text(
            "0 / 5,000", size=TOKENS.size_caption, color=TOKENS.outline,
            no_wrap=True)
        self._prompt_over_badge = ft.Container(
            content=ft.Text("초과", size=TOKENS.size_caption,
                            weight=ft.FontWeight.W_600,
                            color=TOKENS.on_primary, no_wrap=True),
            bgcolor=TOKENS.error,
            border_radius=radius(TOKENS.radius_pill),
            padding=ft.Padding.symmetric(horizontal=TOKENS.space_sm,
                                         vertical=1),
            visible=False)

        # 폭을 명시한다. 없으면 Flet 이 *내용 크기*로만 그려서 박스가
        # 프레임보다 좁아진다(회귀 근거: 스크린샷에서 우측이 안 맞았다).
        # '기본 옵션' 처럼 다른 구획과 우측을 맞춰야 한다.
        self._positive_field = ft.TextField(
            label="포스티프 프롬프트", multiline=True, min_lines=2, max_lines=4,
            read_only=True, width=FIELD_WIDTH,
            hint_text="LM Studio가 향상한 프롬프트가 여기에 표시됩니다",
            # 카운터가 겹치므로 위 여백을 조금 둔다.
            content_padding=ft.Padding.only(
                top=TOKENS.space_xl, bottom=TOKENS.space_sm,
                left=TOKENS.space_md, right=TOKENS.space_md))
        self._negative_field = ft.TextField(
            label="네거티브 프롬프트", multiline=True, min_lines=2, max_lines=4,
            width=FIELD_WIDTH)
        # 포스티프 칸 + 카운터를 겹친다. 겹침 규칙은
        # components.common.overlayed_counter() 가 맡는다(Stack 함정 존재).
        # 프레임 제목은 두지 않는다. 입력칸 label 이 위로 떠서 제목을 대신하며,
        # 함께 있으면 '포스티프 프롬프트' 가 두 번 보인다(사용자 요청).
        self._positive_slot = framed_box(overlayed_counter(
            self._positive_field, self._prompt_counter,
            self._prompt_over_badge))
        # 모델에 따라 통째로 숨기려고 컨테이너를 둔다(제목은 label 이 대신).
        self._negative_slot = framed_box(self._negative_field)

        # --- 기본 옵션 (기본 펼침) ---
        # option_row 안에서 라벨이 왼쪽을 먹으므로 컨트롤만 줄인다.
        self._steps_slider = ft.Slider(min=1, max=60, value=20, divisions=59,
                                       width=ROW_CONTROL_WIDTH, label="{value}")
        self._cfg_slider = ft.Slider(min=0, max=20, value=4.5, divisions=80,
                                     width=ROW_CONTROL_WIDTH, label="{value}")
        self._sampler_dropdown = ft.Dropdown(
            options=[ft.DropdownOption(key=value, text=label)
                     for label, value in SAMPLER_OPTIONS],
            value="euler", width=ROW_CONTROL_WIDTH, dense=True)
        self._scheduler_dropdown = ft.Dropdown(
            # SCHEDULER_OPTIONS 는 (label, value) 튜플이므로 반드시 풀어야 한다.
            # 튜플을 그대로 key 에 넣으면 어떤 key 와도 매칭되지 않아
            # 박스가 빈칸으로 보이고, to_request() 가 튜플을 문자열로 실어
            # 보낸다(회귀 근거: test_model_defaults_fill_sampler_... 가 잡음).
            options=[ft.DropdownOption(key=value, text=label)
                     for label, value in SCHEDULER_OPTIONS],
            value="normal", width=ROW_CONTROL_WIDTH, dense=True)
        self._denoise_slider = ft.Slider(min=0.0, max=1.0, value=1.0,
                                         divisions=20, width=ROW_CONTROL_WIDTH,
                                         label="{value}")

        # --- FaceDetailer ---
        # 15종 슬라이더·SAM 드롭다운·가이드 버튼은 components/facedetailer.py
        # 가 소유한다. 여기서는 그 패널 하나를 들고 위임만 한다(컨트롤이 두 벌
        # 생기면 Flet 은 부모를 하나만 허용하므로 깨진다).
        self._fd_panel = FaceDetailerPanel(
            on_open_guide=self._handle_open_fd_guide)

    @property
    def prompt_counter(self) -> ft.Text:
        """포스티프 프롬프트 칸의 글자수 카운터 컨트롤.

        StudioPage 가 채팅 입력 대신 여기를 갱신한다.
        """
        return self._prompt_counter

    @property
    def prompt_over_badge(self) -> ft.Control:
        """초과 배지 컨트롤 (초과 시만 보인다)."""
        return self._prompt_over_badge

    @property
    def model_selector(self) -> ft.Dropdown:
        """ComfyUI 모델 드롭다운 (StudioPage 가 채팅 입력줄에 그린다).

        컨트롤 소유는 계속 OptionsPanel 이 한다. 여기서 그리지 않을 뿐이라
        값 읽기·옵션 채움·최적값 자동 적용 배선은 그대로 살아 있다.
        """
        return self._model_dropdown

    # --- FaceDetailer 위임 (속성 이름은 기존 테스트/호출자와 호환) -----------
    # 같은 객체를 가리키므로 복사본을 고칠 필요가 없고 부모도 하나뿐이다.

    @property
    def _fd_switch(self) -> ft.Switch:
        return self._fd_panel.switch

    @property
    def _fd_options(self) -> ft.Control:
        return self._fd_panel.control

    @property
    def _fd_sliders(self) -> Dict[str, ft.Slider]:
        return self._fd_panel.sliders

    @property
    def _fd_value_labels(self) -> Dict[str, ft.Text]:
        return self._fd_panel.value_labels

    @property
    def _fd_sam_hint(self) -> ft.Dropdown:
        return self._fd_panel.sam_hint

    @property
    def _fd_sam_negative(self) -> ft.Switch:
        return self._fd_panel.sam_negative

    @property
    def _facedetailer(self):
        return self._fd_panel.settings

    @property
    def facedetailer_panel(self) -> FaceDetailerPanel:
        """가이드 버튼 배선 등 외부에서 쓰는 패널 핸들."""
        return self._fd_panel

    def _make_fd_label_updater(self, key: str):
        """슬라이더를 움직이면 옆 값 라벨을 갱신하는 콜백 (컴포넌트 위임)."""
        return self._fd_panel.make_label_updater(key)

    def _handle_fd_toggle(self, event: ft.Event) -> None:
        self._fd_panel.handle_toggle(event)

    def _handle_open_fd_guide(self) -> None:
        """가이드 버튼 → 셸(알림 다이얼로그) → 도움말 '안면 보정' 문서."""
        shell = self._fd_guide_handler
        if shell is not None:
            shell.show_facedetailer_guide()

    @property
    def _fd_guide_handler(self):
        """앱 런타임에서 주입되는 셸. 테스트 등에서는 None 이다."""
        return self.__dict__.get("_fd_guide_shell")

    def set_guide_handler(self, handler) -> None:
        """셸을 연결한다. (pages 는 셸을 모르고 셸만 pages 를 안다)"""
        self.__dict__["_fd_guide_shell"] = handler


    # --- 레이아웃 ---------------------------------------------------------
    def _label(self, text: str, control: ft.Control,
               *, width: int = FIELD_WIDTH) -> ft.Control:
        """제목 + 컨트롤 세로 묶음 (라벨은 여기서만 만든다).

        width 를 주면 그 폭으로 고정한다. 2열 그리드에서는 GRID_COLUMN_WIDTH
        를 넘지 않도록 build() 에서 계산해 넘긴다.
        """
        return ft.Column(
            controls=[ft.Text(text, size=TOKENS.size_caption,
                              color=TOKENS.on_surface_variant), control],
            spacing=TOKENS.space_xs, tight=True, width=width)

    @staticmethod
    def _grid(cells: List[ft.Control]) -> ft.Control:
        """제목+컨트롤 묶음을 2열로 배치하고 열 사이에 구분선을 세운다.

        실제 줄 만들기/구분선은 fd_sliders.build_grid() 가 담당한다.
        여길 지우면 2열이 조용히 1열로 접힌다.
        """
        return build_grid(cells, GRID_COLUMN_WIDTH)

    def _section(self, title: str, controls: List[ft.Control],
                 *, accent: Optional[str] = None,
                 subtitle: str = "") -> ft.Control:
        """테두리 프레임으로 감싼 섹션.

        예전에는 제목 텍스트만 있어서 스크롤이 길어지면 '어디부터가
        어느 그룹인지' 알 수 없었다. 프레임이 그 경계를 만들어 준다.
        """
        return framed_section(
            title, ft.Column(controls=list(controls),
                              spacing=TOKENS.space_md, tight=True),
            accent=accent, subtitle=subtitle)

    def _build_advanced(self) -> ft.Control:
        """생성 기본값 패널. 이름은 '기본 옵션', 기본으로 펼쳐 둔다.

        사용자가 요구한 변경: '고급 옵션' 이라는 이름이 부담스러워서
        '기본 옵션' 으로 바꾸고, 별도 클릭 없이 보이게 한다.
        Steps/CFG/Sampler/Scheduler/Denoise 는 실제로 자주 바꾸는 값이라
        숨겨 두는 것이 오히려 불편했다.
        """
        body = ft.Column(
            controls=[
                # 해상도/시드는 '기본' 이라는 이름에 어울리는 항목이라
                # 여기로 옮겼다(사용자 요청). 1열로 넓게 두면 값이 잘리지 않는다.
                option_row("해상도", self._resolution_dropdown,
                           width=ROW_CONTROL_WIDTH, label_width=ROW_LABEL_WIDTH),
                option_row("Seed", self._seed_field,
                           width=ROW_CONTROL_WIDTH, label_width=ROW_LABEL_WIDTH),
                option_row("Steps", self._steps_slider, width=ROW_CONTROL_WIDTH,
                           label_width=ROW_LABEL_WIDTH),
                option_row("CFG", self._cfg_slider, width=ROW_CONTROL_WIDTH,
                           label_width=ROW_LABEL_WIDTH),
                option_row("Sampler", self._sampler_dropdown,
                           width=ROW_CONTROL_WIDTH, label_width=ROW_LABEL_WIDTH),
                option_row("Scheduler", self._scheduler_dropdown,
                           width=ROW_CONTROL_WIDTH, label_width=ROW_LABEL_WIDTH),
                option_row("Denoise", self._denoise_slider,
                           width=ROW_CONTROL_WIDTH, label_width=ROW_LABEL_WIDTH),
            ],
            spacing=TOKENS.space_sm, tight=True)
        # 헤더 우측의 'Steps · CFG · ...' 안내를 뺀다.
        # 1) 펼치면 아래에 이미 각 항목 라벨이 보인다(중복)
        # 2) 그 긴 안내가 좁은 폭에서 잘려 'Scheduler · Denoise' 처럼
        #    반쪽만 보인다(오른쪽이 짤린 것처럼 보임)
        return framed_box(collapsible("기본 옵션", body, expanded=True))

    def _build_facedetailer(self) -> ft.Control:
        """안면 보정 스위치 하나를 누르면 15종이 바로 펼쳐진다.

        예전에는 'FaceDetailer 상세' 접기를 한 번 더 눌러야 해서
        '켜놨는데 안 보이니 왜 안 되지?' 하는 혼란이 있었다.
        접기 헤더를 두지 않고 스위치가 곧 펼치기 역할을 한다.
        """
        count = len(self._fd_sliders)
        return framed_section(
            "안면 보정", ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            self._fd_switch,
                            ft.Container(expand=True),
                            self._fd_panel.guide_button,
                            ft.Text(f"{count}개 항목", size=TOKENS.size_caption,
                                    color=TOKENS.on_surface_variant),
                        ],
                        spacing=TOKENS.space_sm, tight=True),
                    self._fd_options,
                ],
                spacing=TOKENS.space_md, tight=True),
            accent=TOKENS.secondary, subtitle="얼굴 자동 보정")


    def build(self) -> ft.Control:
        """좌측 옵션 패널 (세로 스크롤).

        기본 항목은 2열로 올린다. 모델처럼 값이 긴 항목은 1줄을 다 쓰고
        (모델 / LM 모델), 해상도·Seed처럼 짧은 짝은 한 줄에 두 개씩
        배치해 세로 길이를 줄인다.

        ComfyUI 모델 드롭다운은 여기서 그리지 않는다. StudioPage 가 채팅
        입력줄 좌측에 그리기 때문이다. Flet 컨트롤은 부모가 하나뿐이라
        양쪽에 넣으면 깨진다. 여기서는 소유만 하고 model_selector 로 넘긴다.
        """
        # 해상도/시드는 기본 옵션에서 1열(ROW_CONTROL_WIDTH)로 그려진다.
        # 여기서 2열 폭으로 덮어쓰면 option_row 안에서 잘린다.
        for control in (self._resolution_dropdown, self._seed_field):
            control.width = ROW_CONTROL_WIDTH

        return ft.Container(
            content=ft.Column(
                controls=[
                    # LM Studio 모델은 설정 화면에서 고르므로 여기선 뺀다.
                    # (같은 값이 두 곳에 있으면 어느 쪽이 진짜인지 애매해진다)
                    # 해상도/시드도 '기본 옵션' 으로 옮겼다.
                    self._positive_slot,
                    self._negative_slot,
                    self._build_advanced(),
                    self._build_facedetailer(),
                ],
                spacing=TOKENS.space_md,
                scroll=ft.ScrollMode.AUTO),
            width=PANEL_WIDTH,
            bgcolor=TOKENS.surface,
            padding=ft.Padding.all(PANEL_PADDING),
        )


    # --- 값 읽기/쓰기 ----------------------------------------------------
    def apply_model_defaults(self, model_name: str) -> Optional[str]:
        """선택한 모델의 최적 생성 설정값을 옵션에 적용한다.

        원본(Qt) 의 MainController.apply_model_defaults() 와 같은 역할:
        Steps / CFG / Sampler / Scheduler / Denoise 를 모델 프로필 값으로
        덮어쓴다.

        회귀 근거: 이 기능이 Flet 전환에서 통째로 빠졌다. 모델을 바꿔도
        아무 반응이 없어 '자동 최적 설정이 고장났다'는 인상을 준다.
        반환값은 배지에 쓸 한 줄 안내(또는 None).
        """
        name = str(model_name or "").strip()
        if not name or name == "로드된 모델 없음":
            return None
        profile = self._registry.detect(name) if self._registry else None
        if profile is None:
            return None

        steps, cfg = resolve_steps(profile), resolve_cfg(profile)
        if steps:
            self._steps_slider.value = float(steps)
        if cfg:
            self._cfg_slider.value = cfg
        # 프로필은 내부 값(euler), 드롭다운은 표시명(Euler)이라 변환이 필요하다.
        self._sampler_dropdown.value = resolve_sampler(profile)
        self._scheduler_dropdown.value = resolve_scheduler(profile)

        # FLUX / ZImage 계열은 네거티브 프롬프트를 쓰지 않는다.
        # (워크플로우에 네거티브 입력이 아예 없다) 입력창까지 보여주면
        #  넣은 값이 조용히 버려지므로 숨긴다.
        self._apply_negative_visibility(profile, name)

        safe_update(self._steps_slider, self._cfg_slider,
                    self._sampler_dropdown, self._scheduler_dropdown,
                    self._negative_slot)
        return format_notice(profile, cfg, steps or 0)

    def on_job_update(self, job) -> None:
        """Job 갱신을 받아 포스티프 프롬프트 칸을 채운다.

        JobManager 의 리스너로 등록된다(백그라운드 스레드에서 불린다).
        그래서 값만 받아두고 실제 갱신은 UI 스레드로 넘긴다.
        """
        enhanced = str(getattr(job, "enhanced_prompt", "") or "")
        if not enhanced:
            return
        # UI 스레드면 바로 쓴다. run_on_ui 는 루프가 없으면 조용히
        # 건너뛰기 때문에, 루프 등록 전(테스트/초기 렌더)에 값이 안 붙는다.
        if is_ui_thread():
            self.set_enhanced_prompt(enhanced)
        else:
            run_on_ui(lambda: self.set_enhanced_prompt(enhanced))

    def clear_enhanced_prompt(self) -> None:
        """새 입력을 받으면 이전 향상 결과를 비운다.

        안 비우면 새 프롬프트를 보냈는데 화면엔 옛 프롬프트가 남아
        '제출한 내용을 안 쓰는가?' 하는 혼선이 생긴다.
        """
        self.set_enhanced_prompt("")

    def set_enhanced_prompt(self, text: str) -> None:
        """LM Studio 가 향상해 준 프롬프트를 포스티프 칸에 표시한다.

        원본 Qt 의 positivePromptEdit 에 해당한다. 채팅 입력칸에 짧은
        설명을 보내면 진행 콜백(enhanced_prompt) 으로enhanced 값이 오고,
        그걸 여기 보여준다. 사용자가 최종적으로 무엇이 ComfyUI 로 들어가는지
        확인할 수 있어야 한다.

        read_only 라 사용자가 건드릴 수 없고, 안 읽히면 '향상이 왜 안
        되나?' 할 수 있어서 채운 뒤 갱신을 한 번 건다.
        """
        value = str(text or "")
        if self._positive_field.value == value:
            return
        self._positive_field.value = value
        safe_update(self._positive_field)

    def _apply_negative_visibility(self, profile, model_name: str = "") -> None:
        """네거티브 프롬프트 입력칸을 모델에 따라 켜고 끈다.

        모델 이름을 함께 줘야 한다. 프로필만 보면 generic 으로 떨어지는
        모델(예: z-image-turbo.safetensors)을 못 잡아서다.
        """
        self._negative_slot.visible = model_supports_negative(profile, model_name)
        if not self._negative_slot.visible:
            # 숨길 때 값을 비운다. 안 그러면 모델을 다시 바꿨을 때
            # 예전에 입력한 값이 되살아나 '방금 지웠는데 왜 나오지?' 한다.
            self._negative_field.value = ""

    def to_request(self, base: Optional[GenerationRequest] = None) -> GenerationRequest:
        """현재 옵션을 GenerationRequest 로 만든다.

        base 가 주어지면 유지한 채 옵션만 덮어쓴다 (프롬프트 등 화면 밖 값 보존).
        실제 값 변환은 option_request.build_request() 가 맡는다(600줄 규칙).
        """
        from app.ui.flet.pages import option_request

        return option_request.build_request(self, base)

    def set_model_options(self, model_names: List[str],
                          on_change: Optional[Callable] = None) -> None:
        """모델 목록을 채우고, 선택이 바뀌면 on_change 로 알린다.

        회귀 근거: 예전엔 on_change 가 아예 없어 모델을 바꿔도 아무
        반응이 없었다(최적값 자동 적용 + 채팅 안내가 통째로 빠진 상태).

        또 한 번 더: Flet 의 Dropdown 에는 on_change 가 *없다*
        (on_select / on_text_change 만 있다). on_change 로 주면 파이썬이
        새 속성을 만들어 넣어 버릴 뿐 Flet 은 이벤트를 아예 안 보내서
        클릭해도 아무 일도 일어나지 않는다. 반드시 on_select 를 쓴다.
        """
        self._model_names = list(model_names or [])
        # DropdownOption 에 문자열을 직접 주면 key/text 가 빈칸이 되어
        # 화면에 아무것도 안 보인다. 반드시 key 와 text 를 함께 준다.
        self._model_dropdown.options = [
            ft.DropdownOption(key=name, text=name) for name in self._model_names]
        if self._model_names:
            self._model_dropdown.value = self._model_names[0]
        self._model_dropdown.on_select = on_change
        safe_update(self._model_dropdown)

    def set_lm_model_options(self, model_names: List[str]) -> None:
        names = list(model_names or [])
        self._lm_model_dropdown.options = [
            ft.DropdownOption(key=name, text=name) for name in names]
        if names:
            self._lm_model_dropdown.value = names[0]
        safe_update(self._lm_model_dropdown)


    def apply_snapshot(self, snapshot: dict) -> None:
        """이미지 카드의 '이 설정으로' — 지난 생성 설정을 되돌린다."""
        from app.ui.flet.pages.option_snapshot import (
            SNAPSHOT_FIELDS,
            SNAPSHOT_TARGETS,
        )

        request = GenerationRequest.from_dict(snapshot or {})
        for attr, field in SNAPSHOT_FIELDS:
            control = getattr(self, attr)
            value = getattr(request, field)
            # 해상도만 '1152x896' 조합 문자열이라 따로 처리한다.
            if attr == "_resolution_dropdown":
                control.value = f"{request.width}x{request.height}"
                continue
            control.value = str(value) if attr == "_seed_field" else value

        # FaceDetailer 설정은 컴포넌트가 복원한다(스위치 15종 슬라이더 +
        # SAM 드롭다운 + 가이드 버튼). 실제값을 Qt 슬라이더 값으로 되돌려
        # 넣어야 하므로, 환산 규칙이 있는 컴포넌트에 맡긴다.
        self._fd_panel.apply_snapshot(snapshot)

        safe_update(*[getattr(self, name) for name in SNAPSHOT_TARGETS])
