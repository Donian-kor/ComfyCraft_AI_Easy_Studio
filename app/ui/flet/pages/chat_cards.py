"""챗봇 대화 카드 3종.

원본 PySide6 UI 의 카드 흐름을 그대로 옮긴 것이다.

    사용자 프롬프트 말풍선
          ↓
    PromptCard      AI 가 정리한 프롬프트  [편집] [되돌리기]
          ↓
    GenerationCard  진행률 + 상태 문구      [중단]
          ↓
    ImageCard       이미지 + 메타           [저장] [복사] [재사용]

각 카드 위에 message.say(AI 발화) 말풍선이 붙는다.
카드는 상태 머신이 아니다 — 메시지 kind/phase 가 바뀌면 새로 그린다.
"""

from __future__ import annotations

from typing import Callable, List, Optional

import flet as ft

from app.models.chat import PHASE_GENERATING, ChatMessageData
from app.ui.flet.components.common import collapsible
from app.ui.flet.theme.tokens import TOKENS, radius

# 원본 ImageCard 의 이미지 표시 폭 제한
IMAGE_MAX_WIDTH = 560
IMAGE_MIN_WIDTH = 260


def format_elapsed(seconds: float) -> str:
    """경과 시간을 한국어로 포매팅."""
    total = int(max(0.0, float(seconds or 0.0)))
    minutes, secs = divmod(total, 60)
    hours, mins = divmod(minutes, 60)
    if hours:
        return f"{hours}시간 {mins}분 {secs}초"
    if mins:
        return f"{mins}분 {secs}초"
    return f"{secs}초"


def text_bubble(message: ChatMessageData) -> ft.Container:
    """사용자/AI 말풍선."""
    is_user = message.role == "user"
    return ft.Container(
        content=ft.Text(message.text or "", size=TOKENS.size_body),
        bgcolor=TOKENS.primary_container if is_user else TOKENS.surface_variant,
        border_radius=radius(TOKENS.radius_lg),
        padding=ft.Padding.symmetric(horizontal=TOKENS.space_lg,
                                     vertical=TOKENS.space_md),
        # 사용자 말풍선은 오른쪽, AI 말풍선은 왼쪽
        margin=ft.Margin(left=120 if is_user else 0, right=0 if is_user else 120),
    )


def say_bubble(message: ChatMessageData) -> Optional[ft.Control]:
    """카드 위에 붙는 AI 발화 말풍선.

    카드는 '무엇을 하고 있는가'를, 이 말풍선은 '지금 내가 뭘 하는지'를 말한다.
    발화가 없으면(레거시 세션) 카드만 둔다.
    """
    say = message.say
    if not say:
        return None
    return text_bubble(ChatMessageData(role="ai", text=say))


def prompt_card(message: ChatMessageData, *,
                on_edit: Optional[Callable[[str], None]] = None,
                on_revert: Optional[Callable[[], None]] = None) -> ft.Container:
    """프롬프트 확인 카드. AI 가 정리한 프롬프트를 보여주고 수정할 수 있다."""
    enhanced = str(message.metadata.get("enhanced", "") or "")
    original = str(message.metadata.get("original", "") or "")
    show_revert = bool(enhanced and enhanced != original and on_revert is not None)

    field = ft.TextField(
        value=enhanced, multiline=True, min_lines=2, max_lines=6,
        border_color=TOKENS.outline, dense=True)

    actions: List[ft.Control] = []
    if on_edit is not None:
        actions.append(ft.TextButton(
            "수정 반영", on_click=lambda _e: on_edit(field.value or "")))
    if show_revert:
        actions.append(ft.TextButton(
            "원문으로", on_click=lambda _e: on_revert()))

    return _card([
        ft.Row(
            controls=[
                ft.Icon(ft.Icons.EDIT, size=TOKENS.size_body, color=TOKENS.secondary),
                ft.Text("프롬프트 확인", size=TOKENS.size_caption,
                        color=TOKENS.on_surface_variant),
            ],
            tight=True),
        field,
        *([ft.Row(controls=actions, spacing=TOKENS.space_sm)] if actions else []),
    ])


def generation_card(message: ChatMessageData, *,
                    on_cancel: Optional[Callable[[], None]] = None) -> ft.Container:
    """생성 중 카드. 진행률과 상태 문구를 보여주고 중단할 수 있다."""
    status_text = str(message.metadata.get("status", "이미지 생성 중..."))
    cancel: List[ft.Control] = (
        [ft.TextButton("중단", on_click=lambda _e: on_cancel())]
        if on_cancel is not None else []
    )
    return _card([
        ft.Row(
            controls=[
                ft.ProgressRing(width=18, height=18, stroke_width=2),
                ft.Text(status_text, size=TOKENS.size_body),
                ft.Container(expand=True),
                *cancel,
            ],
            spacing=TOKENS.space_md,
            vertical_alignment=ft.CrossAxisAlignment.CENTER),
    ])


def _card(controls: List[ft.Control]) -> ft.Container:
    """카드 공통 껍데기."""
    return ft.Container(
        content=ft.Column(controls=controls, spacing=TOKENS.space_sm, tight=True),
        bgcolor=TOKENS.surface,
        border_radius=radius(TOKENS.radius_lg),
        padding=ft.Padding.all(TOKENS.space_lg),
    )



def image_card(message: ChatMessageData, *,
               on_save: Optional[Callable[[str], None]] = None,
               on_reuse: Optional[Callable[[ChatMessageData], None]] = None,
               on_open: Optional[Callable[[ChatMessageData], None]] = None) -> ft.Container:
    """완성 이미지 카드. 이미지 + 메타 + 프롬프트 접기 + 저장/복사/재사용."""
    meta = str(message.metadata.get("meta", "") or "")
    prompt = str(message.metadata.get("prompt", "") or "")
    image_path = str(message.metadata.get("image_path", "") or "")
    elapsed = float(message.metadata.get("elapsed", 0) or 0)

    image = ft.Image(
        src=image_path, fit=ft.BoxFit.CONTAIN,
        width=IMAGE_MAX_WIDTH, height=380,
        border_radius=radius(TOKENS.radius_md))
    if on_open is not None:
        image.on_click = lambda _e, m=message: on_open(m)

    actions: List[ft.Control] = []
    if on_save is not None:
        actions.append(ft.TextButton(
            "저장", icon=ft.Icons.SAVE,
            on_click=lambda _e, p=image_path: on_save(p)))
    actions.append(ft.TextButton(
        "경로 복사", icon=ft.Icons.COPY,
        on_click=lambda _e, p=image_path: _copy_text(p)))
    if on_reuse is not None:
        actions.append(ft.TextButton(
            "이 설정으로", icon=ft.Icons.REPLAY,
            on_click=lambda _e, m=message: on_reuse(m)))
    if on_open is not None:
        actions.append(ft.TextButton(
            "크게", icon=ft.Icons.ZOOM_OUT_MAP,
            on_click=lambda _e, m=message: on_open(m)))

    body: List[ft.Control] = [
        ft.Row(
            controls=[
                ft.Icon(ft.Icons.IMAGE, size=TOKENS.size_body, color=TOKENS.primary),
                ft.Text("Generated", size=TOKENS.size_caption,
                        color=TOKENS.on_surface_variant),
                ft.Container(expand=True),
                ft.Text(format_elapsed(elapsed), size=TOKENS.size_caption,
                        color=TOKENS.outline),
            ],
            tight=True),
        image,
        ft.Text(meta, size=TOKENS.size_caption, color=TOKENS.on_surface_variant),
        ft.Row(controls=actions, spacing=TOKENS.space_sm),
    ]
    if prompt:
        body.append(collapsible(
            "프롬프트", ft.Text(prompt, size=TOKENS.size_caption,
                                color=TOKENS.on_surface_variant)))
    return _card(body)


def render_message(message: ChatMessageData, **kwargs) -> ft.Control:
    """메시지 1개를 컨트롤로 렌더링한다.

    generation 카드는 phase 에 따라 PromptCard / GenerationCard 로 갈리고,
    say 발화가 있으면 카드 위에 말풍선을 붙인다.

    카드마다 받는 콜백이 다르므로(프롬프트=편집/되돌리기,
    이미지=저장/재사용/확대) 종류에 맞는 것만 넘긴다.
    """
    if message.kind == "image":
        card = image_card(message, **kwargs)
    elif message.kind == "generation":
        if message.phase == PHASE_GENERATING:
            card = generation_card(
                message, **{k: v for k, v in kwargs.items()
                            if k in ("on_cancel",)})
        else:
            card = prompt_card(
                message, **{k: v for k, v in kwargs.items()
                            if k in ("on_edit", "on_revert")})
    else:
        return text_bubble(message)

    bubble = say_bubble(message)
    if bubble is None:
        return card
    return ft.Column(controls=[bubble, card], spacing=TOKENS.space_xs, tight=True)


def _copy_text(text: str) -> None:
    """텍스트를 클립보드에 복사한다 (실패해도 흐름을 막지 않는다)."""
    try:
        import flet

        flet.Clipboard.set_data(text)
    except Exception:
        pass

    return text_bubble(ChatMessageData(role="ai", text=message.say))
