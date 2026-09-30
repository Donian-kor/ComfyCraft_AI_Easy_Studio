"""과거 생성 설정(스냅샷) 복원 규칙.

options.py 가 600줄 제한에 걸리지 않도록, '스냅샷 필드 → 컨트롤 이름'
대응표만 여기 둔다. 실제 값 대입은 OptionsPanel.apply_snapshot() 가 한다
(컨트롤을 여기서 만들지 않는다).

새 컨트롤을 옵션에 추가할 때 여기도 한 줄을 더해야 복원이 빠짐없이
일어난다. 빠뜨리면 '이 설정으로 재생성' 이 그 항목만 안 되돌린다.
"""

from __future__ import annotations

from typing import List, Tuple

# 컨트롤 속성 이름 -> GenerationRequest 필드 이름
SNAPSHOT_FIELDS: List[Tuple[str, str]] = [
    ("_model_dropdown", "comfy_model"),
    ("_lm_model_dropdown", "lm_model"),
    ("_resolution_dropdown", "width"),   # f"{w}x{h}" 로 조합 (아래 예외)
    ("_seed_field", "seed"),
    ("_negative_field", "negative_prompt"),
    ("_steps_slider", "steps"),
    ("_cfg_slider", "cfg"),
    ("_sampler_dropdown", "sampler"),
    ("_scheduler_dropdown", "scheduler"),
    ("_denoise_slider", "denoise"),
]

# 갱신 대상 컨트롤 속성 이름 (safe_update 에 넘길 목록)
SNAPSHOT_TARGETS: List[str] = [name for name, _ in SNAPSHOT_FIELDS] + [
    "_positive_field",
]
