"""Phase 10: Help 화면.

기존 도움말 콘텐츠(assets/help/md/*.md)를 그대로 재사용한다.
UI 만 좌측 목차 + 우측 콘텐츠로 바뀐다.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import flet as ft

from app.paths import BASE_DIR
from app.ui.flet.components.common import safe_update
from app.ui.flet.theme.tokens import TOKENS, radius

HELP_DIR = BASE_DIR / "assets" / "help" / "md"

# (화면 라벨, 파일 접두사) — 순서대로 좌측 목차에 놓인다.
HELP_TOPICS = [
    ("시작하기", "01_getting_started"),
    ("기본 사용법", "02_basic_usage"),
    ("모델 설정", "03_model_settings"),
    ("프롬프트 작성", "04_prompt_writing"),
    ("생성 옵션", "05_generation_options"),
    ("안면 보정", "06_facedetailer"),
    ("기록과 단축키", "07_history_shortcuts"),
    ("자주 묻는 질문", "08_faq"),
]


@dataclass(frozen=True)
class HelpTopic:
    label: str
    slug: str

    @property
    def path(self) -> Path:
        return HELP_DIR / f"{self.slug}.md"

    def load(self) -> str:
        """마크다운 본문을 읽는다. 없으면 안내 문구를 반환."""
        try:
            return self.path.read_text(encoding="utf-8")
        except OSError:
            return f"### {self.label}\n\n도움말 파일을 찾을 수 없습니다: {self.path.name}"


TOPICS = [HelpTopic(label, slug) for label, slug in HELP_TOPICS]


class HelpPage:
    """좌측 목차 + 우측 콘텐츠 구조의 도움말."""

    def __init__(self) -> None:
        self._topics = TOPICS
        self._current = self._topics[0]
        self._content = ft.Markdown("", expand=True, selectable=True)
        self._nav = ft.ListView(
            expand=True, spacing=2, padding=ft.Padding.all(TOKENS.space_sm))

    def _select(self, topic: HelpTopic) -> None:
        self._current = topic
        self._content.value = topic.load()
        self._render_nav()
        safe_update(self._content)

    def _render_nav(self) -> None:
        self._nav.controls = [
            ft.Container(
                content=ft.Text(
                    topic.label, size=TOKENS.size_body,
                    color=(TOKENS.primary if topic.slug == self._current.slug
                           else TOKENS.on_surface_variant),
                    weight=(ft.FontWeight.W_600 if topic.slug == self._current.slug
                            else ft.FontWeight.NORMAL),
                ),
                bgcolor=(TOKENS.primary_container
                         if topic.slug == self._current.slug else None),
                border_radius=radius(TOKENS.radius_sm),
                padding=ft.Padding.symmetric(horizontal=TOKENS.space_md,
                                             vertical=TOKENS.space_sm),
                on_click=lambda _e, t=topic: self._select(t),
            )
            for topic in self._topics
        ]
        safe_update(self._nav)

    def build(self) -> ft.Control:
        self._select(self._current)
        # 좌측 목차 + 우측 본문. Row 는 padding 을 받지 않으므로
        # 바깥 Container 로 여백을 준다.
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=self._nav, width=220,
                        bgcolor=TOKENS.surface,
                        border_radius=radius(TOKENS.radius_lg),
                        padding=ft.Padding.all(TOKENS.space_sm),
                    ),
                    ft.Container(
                        content=ft.Container(
                            content=self._content, expand=True,
                            padding=ft.Padding.all(TOKENS.space_xl),
                            bgcolor=TOKENS.surface,
                            border_radius=radius(TOKENS.radius_lg),
                        ),
                        expand=True,
                    ),
                ],
                expand=True,
                spacing=TOKENS.space_lg,
            ),
            padding=ft.Padding.all(TOKENS.space_lg),
            expand=True,
        )

    @property
    def current_topic(self) -> HelpTopic:
        return self._current
