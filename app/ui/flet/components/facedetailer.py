"""FaceDetailer(안면 보정) 옵션 컴포넌트.

OptionsPanel 에서 분리해 600줄 제한을 지킨다.
원본 Qt UI 의 facedetailerPanel 과 대응된다.
"""
from __future__ import annotations

from typing import Callable, Dict, List, Optional

import flet as ft

from app.constants import FACEDETAILER_SLIDER_SPECS
from app.models.generation import FaceDetailerSettings
from app.ui.flet.components.common import collapsible, option_row, safe_update
from app.ui.flet.pages.fd_sliders import (
    FD_SLIDER_RANGES,
    GRID_DIVIDER_TOTAL,
    build_grid,
    attr_name as _fd_attr_name,
    format_value as _format_fd_value,
    to_qt_value as _fd_to_qt_value,
    to_real_value as _fd_to_real_value,
)
from app.ui.flet.theme.tokens import TOKENS

# FaceDetailer 관련 상수들 (원본 options.py 에서 이동)
_FD_LABELS = {
    "facedetailer_denoise": "Denoise",
    "facedetailer_steps": "Steps",
    "facedetailer_cfg": "CFG",
    "facedetailer_guide_size": "Guide Size",
    "facedetailer_max_size": "Max Size",
    "facedetailer_feather": "Feather",
    "facedetailer_bbox_threshold": "BBox Threshold",
    "facedetailer_bbox_dilation": "BBox Dilation",
    "facedetailer_bbox_crop_factor": "BBox Crop Factor",
    "facedetailer_sam_dilation": "SAM Dilation",
    "facedetailer_sam_threshold": "SAM Threshold",
    "facedetailer_sam_bbox_expansion": "SAM BBox Expansion",
    "facedetailer_sam_mask_hint_threshold": "SAM Mask Hint Threshold",
    "facedetailer_cycle": "Cycle",
    "facedetailer_drop_size": "Drop Size",
}

# SAM 탐지 방식 (원본 facedetailerPanel 의 ComboBox)
# options.py 가 이 이름을 재노출하므로 공개 이름으로 둔다.
SAM_HINT_OPTIONS = [("bbox", "bbox"), ("rect-positive", "rect-positive"),
                     ("rect-negative", "rect-negative"),
                     ("point", "point"), ("point-bbox", "point-bbox")]

# 상세 패널을 3단으로 나눠 한 번에 15개를 다 보여주지 않는다.
# 원본도 facedetailerPanel 안에 스크롤을 두었다.
# 그룹 이름이 '탐지 · SAM' 이면 위쪽 'SAM 탐지' 드롭다운과 헷갈리므로
# '얼굴 탐지' 라고 부른다(같은 대상, 다른 역할임을 구분).
# options.py 가 '_FD_GROUPS' 로 재노출하므로 공개 이름으로 둔다.
FD_GROUPS = [
    ("기본 보정", ["facedetailer_denoise", "facedetailer_steps",
                   "facedetailer_cfg", "facedetailer_cycle"]),
    ("얼굴 영역", ["facedetailer_guide_size", "facedetailer_max_size",
                   "facedetailer_feather", "facedetailer_drop_size"]),
    ("얼굴 탐지", ["facedetailer_bbox_threshold", "facedetailer_bbox_dilation",
                   "facedetailer_bbox_crop_factor", "facedetailer_sam_dilation",
                   "facedetailer_sam_threshold", "facedetailer_sam_bbox_expansion",
                   "facedetailer_sam_mask_hint_threshold"]),
]

# 2열 그리드 폭 계산 (options.py 와 동일한 값을 단일 진실로 유지한다)
# GRID_DIVIDER / GRID_DIVIDER_GAP 은 fd_sliders.build_grid() 가 직접 쓴다.
# 여기서 다시 정의하면 양쪽이 어긋나 칸이 1px 잘린다.
#
# 회귀 근거: 안면 보정을 framed_section 으로 감싸면서 안쪽 여백
# (space_md x2 = 24) 이 생겼다. 그걸 빼지 않으면 슬라이더 우측과
# 오른쪽 열 라벨('Max Size' 옆 값)이 프레임 밖으로 잘렸다.
# options.py 와 똑같이 FRAME_PADDING 을 빼야 두 쪽이 어긋나지 않는다.
PANEL_WIDTH = 420
PANEL_PADDING = 24
CONTENT_WIDTH = PANEL_WIDTH - PANEL_PADDING * 2
FRAME_PADDING = TOKENS.space_md
INNER_WIDTH = CONTENT_WIDTH - FRAME_PADDING * 2
_COLLAPSE_INDENT = TOKENS.space_lg
GRID_AVAILABLE = INNER_WIDTH - _COLLAPSE_INDENT
# //2 로 버림하면 1px 가 남고, 그 1px 때문에 줄 폭이
# GRID_AVAILABLE 보다 작아져 오른쪽에 빈틈이 보인다.
# 정확히 맞추기 위해 /2(실수)로 나눈다. Flet 은 실수 폭을 받는다.
GRID_COLUMN_WIDTH = (GRID_AVAILABLE - GRID_DIVIDER_TOTAL) / 2
FD_SLIDER_WIDTH = GRID_COLUMN_WIDTH
FD_VALUE_WIDTH = 34
FD_LABEL_WIDTH = GRID_COLUMN_WIDTH - FD_VALUE_WIDTH - TOKENS.space_sm


def _build_fd_slider(widget_name: str) -> ft.Slider:
    """원본 Qt 슬라이더와 같은 범위/기본값으로 Flet 슬라이더를 만든다."""
    qt_min, qt_max, qt_default, _factor, _digits = FD_SLIDER_RANGES[widget_name]
    return ft.Slider(
        min=qt_min, max=qt_max,
        value=float(max(qt_min, qt_default)),
        divisions=max(1, qt_max - qt_min),
        width=FD_SLIDER_WIDTH,
        label="{value}")


class FaceDetailerPanel:
    """FaceDetailer 옵션 패널 (스위치 + 3그룹 15슬라이더 + SAM 힌트)."""

    def __init__(self, *, on_open_guide: Optional[Callable[[], None]] = None) -> None:
        self._on_open_guide = on_open_guide
        self._facedetailer = FaceDetailerSettings()

        # FaceDetailer 켜기/끄기 스위치
        self._fd_switch = ft.Switch(
            label="안면 보정", value=False,
            on_change=self._handle_fd_toggle)

        # 가이드 버튼 (P3-3)
        self._fd_guide_button = ft.TextButton(
            "가이드", icon=ft.Icons.HELP_OUTLINE,
            on_click=self._handle_open_guide,
            visible=False)

        self._fd_sliders: Dict[str, ft.Slider] = {}
        self._fd_value_labels: Dict[str, ft.Text] = {}
        self._fd_specs = {key: (default, factor, is64)
                          for key, _name, default, factor, is64
                          in FACEDETAILER_SLIDER_SPECS}

        for key, widget_name, default, factor, is64 in FACEDETAILER_SLIDER_SPECS:
            slider = _build_fd_slider(widget_name)
            slider.on_change = self._make_fd_label_updater(key)
            self._fd_sliders[key] = slider
            self._fd_value_labels[key] = ft.Text(
                _format_fd_value(key, _fd_to_real_value(key, slider.value)),
                size=TOKENS.size_caption, color=TOKENS.on_surface_variant,
                no_wrap=True, width=FD_VALUE_WIDTH,
                text_align=ft.TextAlign.RIGHT)

        # 원본의 SAM 탐지 방식 ComboBox + 네거티브 마스크 체크
        self._fd_sam_hint = ft.Dropdown(
            options=[ft.DropdownOption(key=value, text=label)
                     for label, value in SAM_HINT_OPTIONS],
            value="bbox", width=FD_SLIDER_WIDTH, dense=True)
        self._fd_sam_negative = ft.Switch(
            label="네거티브 마스크 사용", value=False)

        # 15종을 2열로 올린다. 한 칸이 좁으니 슬라이더 위에
        # [라벨][값] 을 올리고, 그 아래에 슬라이더를 온전히 놓는다.
        def _fd_cell(key: str) -> ft.Control:
            return ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(_FD_LABELS.get(key, key),
                                    size=TOKENS.size_caption,
                                    color=TOKENS.on_surface_variant,
                                    no_wrap=True,
                                    width=FD_LABEL_WIDTH,
                                    overflow=ft.TextOverflow.ELLIPSIS),
                            self._fd_value_labels[key],
                        ],
                        spacing=TOKENS.space_sm, tight=True,
                        alignment=ft.MainAxisAlignment.CENTER),
                    self._fd_sliders[key],
                ],
                spacing=2, tight=True, width=GRID_COLUMN_WIDTH)

        self._fd_groups: List[ft.Control] = [
            collapsible(
                title,
                self._grid([_fd_cell(key) for key in keys
                            if key in self._fd_sliders]),
                subtitle=f"{len(keys)}개",
                expanded=True)
            for _index, (title, keys) in enumerate(FD_GROUPS)
        ]

        # 스위치/가이드 버튼은 *맨 위* 헤더 줄에만 둔다.
        #
        # 회귀 근거: 예전엔 아래에 '옵션 영역' 안에서 또 헤더 줄을 만들며
        # 거기 스위치와 가이드 버튼을 또 그렸다. 그래서 options.py 의
        # _build_facedetailer() 헤더와 여기가 그려진 스위치가 겹쳐
        # '토글하면 버튼이 하나씩 늘어난다'는 버그가 났다.
        # Flet 은 한 컨트롤의 부모가 하나뿐이라, 같은 스위치를 두 곳에
        # 넣으면 화면에 두 번 그려진다.
        self._fd_options = ft.Column(
            controls=[
                self._label("얼굴 탐지 방식", self._fd_sam_hint),
                self._fd_sam_negative,
                *self._fd_groups,
            ],
            spacing=TOKENS.space_md, tight=True, visible=False)

    def _grid(self, cells: List[ft.Control]) -> ft.Control:
        """cells 리스트를 2열 그리드로 배치 (구분선 포함)."""
        return build_grid(cells, GRID_COLUMN_WIDTH)

    def _label(self, text: str, control: ft.Control) -> ft.Control:
        """라벨 + 컨트롤 한 줄 구성 (option_row 패턴)."""
        return option_row(text, control)

    def handle_toggle(self, e: ft.Event) -> None:
        """스위치 토글 시 옵션 영역 표시/숨김 + 가이드 버튼 표시."""
        self._facedetailer.enabled = bool(e.control.value)
        self._fd_options.visible = e.control.value
        self._fd_guide_button.visible = e.control.value
        safe_update(self._fd_options, self._fd_guide_button)

    def _handle_fd_toggle(self, e: ft.Event) -> None:
        # 컨트롤이 직접 물고 있는 콜백(Flet 이 호출하는 진입점).
        self.handle_toggle(e)

    def _handle_open_guide(self, _e: ft.Event) -> None:
        """가이드 버튼 클릭 시 콜백 호출."""
        if self._on_open_guide:
            self._on_open_guide()

    def make_label_updater(self, key: str):
        """슬라이더 값이 바뀌면 옆 값 라벨을 실제 값으로 갱신하는 콜백."""
        def _updater(e: ft.Event) -> None:
            label = self._fd_value_labels[key]
            label.value = _format_fd_value(key, _fd_to_real_value(key, e.control.value))
            safe_update(label)
        return _updater

    def _make_fd_label_updater(self, key: str):
        return self.make_label_updater(key)

    # --- 퍼블릭 API ---------------------------------------------------------

    @property
    def control(self) -> ft.Control:
        """메인 컨트롤 반환 (OptionsPanel.build 에서 포함)."""
        return self._fd_options

    @property
    def switch(self) -> ft.Switch:
        return self._fd_switch

    @property
    def guide_button(self) -> ft.TextButton:
        """가이드 버튼.

        options.py 의 _build_facedetailer() 헤더가 이 버튼을 그린다.
        여기서(옵션 영역 안)는 그리지 않는다. 같은 컨트롤을 두 자리에
        넣으면 화면에 두 번 나타나 '누를 때마다 버튼이 늘어난다'는
        버그가 된다.
        """
        return self._fd_guide_button

    @property
    def sliders(self) -> Dict[str, ft.Slider]:
        """키 → 슬라이더 (OptionsPanel 이 이름만 바꿔 위임)."""
        return self._fd_sliders

    @property
    def value_labels(self) -> Dict[str, ft.Text]:
        """키 → 실제 값 표시 라벨."""
        return self._fd_value_labels

    @property
    def sam_hint(self) -> ft.Dropdown:
        return self._fd_sam_hint

    @property
    def sam_negative(self) -> ft.Switch:
        return self._fd_sam_negative

    @property
    def guide_button(self) -> ft.TextButton:
        return self._fd_guide_button

    @property
    def groups(self) -> List[ft.Control]:
        """3개 collapsible 그룹 (테스트가 그룹 수를 확인한다)."""
        return self._fd_groups

    @property
    def settings(self):
        """현재 FaceDetailerSettings (OptionsPanel 이 재노출)."""
        return self._facedetailer

    @property
    def is_enabled(self) -> bool:
        return bool(self._fd_switch.value)

    def apply_to_request(self, request) -> None:
        """GenerationRequest 에 FaceDetailer 설정 반영."""
        for key, _widget, default, _factor, _is64 in FACEDETAILER_SLIDER_SPECS:
            setattr(self._facedetailer, _fd_attr_name(key),
                    _fd_to_real_value(key, self._fd_sliders[key].value))

        self._facedetailer.enabled = bool(self._fd_switch.value)
        self._facedetailer.sam_detection_hint = str(
            self._fd_sam_hint.value or "bbox")
        self._facedetailer.sam_mask_hint_use_negative = bool(
            self._fd_sam_negative.value)
        request.facedetailer = self._facedetailer

    def apply_snapshot(self, snapshot: dict) -> None:
        """스냅샷에서 FaceDetailer 설정 복원."""
        from app.models.generation import GenerationRequest
        request = GenerationRequest.from_dict(snapshot or {})
        self._facedetailer = request.facedetailer

        self._fd_switch.value = self._facedetailer.enabled
        self._fd_options.visible = self._facedetailer.enabled
        self._fd_guide_button.visible = self._facedetailer.enabled

        for key, _widget, _default, _factor, _is64 in FACEDETAILER_SLIDER_SPECS:
            saved = getattr(self._facedetailer, _fd_attr_name(key), None)
            if saved is None:
                continue
            slider = self._fd_sliders.get(key)
            if slider is not None:
                slider.value = _fd_to_qt_value(key, saved)
            label = self._fd_value_labels.get(key)
            if label is not None:
                label.value = _format_fd_value(key, saved)

        self._fd_sam_hint.value = self._facedetailer.sam_detection_hint or "bbox"
        self._fd_sam_negative.value = bool(
            self._facedetailer.sam_mask_hint_use_negative)

        safe_update(self._fd_switch, self._fd_options, self._fd_guide_button,
                    self._fd_sam_hint, self._fd_sam_negative,
                    *self._fd_sliders.values(), *self._fd_value_labels.values())