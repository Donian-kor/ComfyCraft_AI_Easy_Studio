"""옵션 컨트롤 -> GenerationRequest 변환.

options.py 가 600줄 제한에 걸리지 않도록 값 변환을 여기 뺀다.
컨트롤을 *만들지* 않고, 이미 만들어진 컨트롤에서 값만 읽어
GenerationRequest 를 채운다. (Flet 을 모르는 순수 로직 아님 - 컨트롤을
읽기만 하므로 UI 계층 안이다)
"""

from __future__ import annotations

from typing import Optional

from app.models.generation import GenerationRequest


def build_request(panel, base: Optional[GenerationRequest] = None) -> GenerationRequest:
    """옵션 패널의 현재 값을 요청 객체로 만든다."""
    from app.ui.flet.pages.options import parse_resolution

    request = base or GenerationRequest()
    width, height = parse_resolution(panel._resolution_dropdown.value)

    request.negative_prompt = panel._negative_field.value or ""
    request.comfy_model = panel._model_dropdown.value or ""
    request.lm_model = panel._lm_model_dropdown.value or ""
    request.width = width
    request.height = height

    try:
        request.seed = int((panel._seed_field.value or "-1").strip())
    except (TypeError, ValueError):
        request.seed = -1

    request.steps = int(panel._steps_slider.value or 20)
    request.cfg = float(panel._cfg_slider.value or 4.5)
    request.sampler = str(panel._sampler_dropdown.value or "euler")
    request.scheduler = str(panel._scheduler_dropdown.value or "normal")
    request.denoise = float(panel._denoise_slider.value or 1.0)

    # FaceDetailer 15종을 빠짐없이 요청에 반영한다. 하드코딩으로 몇 개만
    # 넣으면 화면에서 고른 값이 조용히 버려진다. 배율 환산 규칙은
    # 컴포넌트에 있으므로 여기서는 위임만 한다.
    panel._fd_panel.apply_to_request(request)
    return request
