"""모델 프로필 수동 등록 폼 (원본 settings_dialog.ui 의 modelManualTab).

원본 설정창은 '자동'/'수동' 두 탭으로 나뉘어 있었다. 수동 탭에서는
모델 파일과 워크플로우를 직접 골라 프로필을 JSON 으로 저장했다.
이 모듈은 그 수동 등록 폼만 담당한다.

저장 위치는 app/model_profiles_json/<이름>.json 이다. ModelRegistry 가
이 폴더를 읽으므로 저장 직후 다시 불러오면 곧바로 반영된다.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import flet as ft

from app.core.model_profiles.base import ModelProfile
from app.core.model_registry import ModelRegistry
from app.paths import BASE_DIR
from app.ui.flet.components.common import safe_update, section_card
from app.ui.flet.theme.tokens import TOKENS

MANUAL_PROFILE_DIR = BASE_DIR / "model_profiles_json"

# 원본 form 의 combo 후보
SAMPLER_CHOICES = ["euler", "euler_ancestral", "dpmpp_2m", "dpmpp_2m_sde",
                   "dpmpp_sde", "heun", "ddim", "uni_pc"]
SCHEDULER_CHOICES = ["normal", "karras", "exponential", "sgm_uniform",
                     "simple", "ddim_uniform", "beta"]
CLIP_TYPE_CHOICES = ["stable_diffusion", "sd3", "flux", "lumina", "hunyuan"]
TEXT_CLASS_CHOICES = ["CLIPTextEncode", "CLIPTextEncodeSDXL",
                      "CLIPTextEncodeFlux", "TextEncodeQwenImageEditPlus"]
WORKFLOW_TYPE_CHOICES = ["checkpoint", "flux_gguf", "unet_clploadergguf",
                         "zimage", "unet_dualclploadergguf", "lumina"]
BASE_CHOICES = ["checkpoint_loadersimple", "unet_loader", "unet_loader_gguf",
                "image_only_checkpoint_loader"]


def safe_file_name(name: str) -> str:
    """프로필 이름을 안전한 파일명으로 바꾼다."""
    cleaned = re.sub(r"[^\w\-가-힣]+", "_", (name or "").strip())
    return cleaned or "profile"


def reload_registry(registry: ModelRegistry) -> None:
    """같은 객체에 프로필 목록을 다시 읽어 온다.

    dataclass 를 통째로 바꾸면 AppServices 가 들고 있던 참조까지 바뀌어
    화면 상태가 어긋난다. __init__ 를 다시 부르면 profiles 리스트만
    갱신되므로 기존 참조가 유지된다.
    """
    registry.__init__()            # type: ignore[misc]


class ProfileEditor:
    """프로필 하나를 편집하는 폼 (원본 modelManualTab 대응)."""

    def __init__(self, registry: ModelRegistry, *,
                 on_saved: Optional[Callable[[str], None]] = None) -> None:
        self._registry = registry
        self._on_saved = on_saved
        self._editing_name: str = ""

        self._name = ft.TextField(label="프로필 이름", width=340, dense=True)
        self._family = ft.TextField(label="패밀리", width=340, dense=True)
        self._model_file = ft.TextField(label="모델 파일", width=340, dense=True)
        self._workflow_file = ft.TextField(label="워크플로우 파일", width=340,
                                          dense=True)
        self._patterns = ft.TextField(
            label="패턴 (쉼표 구분)", width=700, dense=True,
            hint_text="모델 파일명에 이 문자열이 들어오면 이 프로필이 적용됩니다")
        self._aliases = ft.TextField(label="별칭 (쉼표 구분)", width=700, dense=True)

        self._base = ft.Dropdown(
            label="Base", width=340, dense=True,
            options=[ft.DropdownOption(key=b, text=b) for b in BASE_CHOICES],
            value=BASE_CHOICES[0])
        self._workflow_type = ft.Dropdown(
            label="워크플로우 종류", width=340, dense=True,
            options=[ft.DropdownOption(key=w, text=w) for w in WORKFLOW_TYPE_CHOICES],
            value=WORKFLOW_TYPE_CHOICES[0])
        self._clip_type = ft.Dropdown(
            label="CLIP 종류", width=340, dense=True,
            options=[ft.DropdownOption(key=c, text=c) for c in CLIP_TYPE_CHOICES],
            value=CLIP_TYPE_CHOICES[0])
        self._text_class = ft.Dropdown(
            label="텍스트 인코더", width=340, dense=True,
            options=[ft.DropdownOption(key=t, text=t) for t in TEXT_CLASS_CHOICES],
            value=TEXT_CLASS_CHOICES[0])
        self._sampler = ft.Dropdown(
            label="Sampler", width=340, dense=True,
            options=[ft.DropdownOption(key=s, text=s) for s in SAMPLER_CHOICES],
            value=SAMPLER_CHOICES[0])
        self._scheduler = ft.Dropdown(
            label="Scheduler", width=340, dense=True,
            options=[ft.DropdownOption(key=s, text=s) for s in SCHEDULER_CHOICES],
            value=SCHEDULER_CHOICES[0])

        self._guidance = ft.TextField(label="Guidance", value="3.5", width=160, dense=True)
        self._steps = ft.TextField(label="Steps", value="20", width=160, dense=True)
        self._cfg = ft.TextField(label="CFG", value="4.0", width=160, dense=True)
        self._priority = ft.TextField(label="우선순위", value="100", width=160, dense=True)
        self._clip1 = ft.TextField(label="CLIP", width=340, dense=True)
        self._clip2 = ft.TextField(label="CLIP2", width=340, dense=True)
        self._vae = ft.TextField(label="VAE", width=340, dense=True)

        self._message = ft.Text("", size=TOKENS.size_caption,
                                color=TOKENS.on_surface_variant)
        self._saved_list = ft.Column(spacing=TOKENS.space_xs, tight=True)

    # --- 데이터 변환 ------------------------------------------------------
    @staticmethod
    def _split(raw: str) -> List[str]:
        return [part.strip() for part in (raw or "").split(",") if part.strip()]

    def _to_payload(self) -> Dict[str, Any]:
        """폼 값을 JSON 페이로드로 만든다."""
        name = (self._name.value or "").strip()
        return {
            "name": name,
            "family": (self._family.value or "").strip() or name,
            "patterns": self._split(self._patterns.value),
            "aliases": self._split(self._aliases.value),
            "workflow_type": str(self._workflow_type.value or "checkpoint"),
            "base": str(self._base.value or ""),
            "default_clip1": (self._clip1.value or "").strip(),
            "default_clip2": (self._clip2.value or "").strip(),
            "default_vae": (self._vae.value or "").strip(),
            "default_steps": int(self._steps.value or 20),
            "default_cfg": float(self._cfg.value or 4.0),
            "sampler_name": str(self._sampler.value or "euler"),
            "scheduler": str(self._scheduler.value or "normal"),
            "clip_type": str(self._clip_type.value or "stable_diffusion"),
            "text_class": str(self._text_class.value or "CLIPTextEncode"),
            "guidance": float(self._guidance.value or 3.5),
            "priority": int(self._priority.value or 100),
            "workflow_file": (self._workflow_file.value or "").strip(),
        }

    # --- 불러오기 / 초기화 ------------------------------------------------
    def load(self, profile: ModelProfile) -> None:
        """기존 프로필을 폼에 불러온다 (수정용)."""
        self._editing_name = profile.name
        self._name.value = profile.name
        self._family.value = profile.family
        self._model_file.value = ""
        self._workflow_file.value = profile.workflow_file or ""
        self._patterns.value = ", ".join(profile.patterns)
        self._aliases.value = ", ".join(profile.aliases)
        self._base.value = profile.base or BASE_CHOICES[0]
        self._workflow_type.value = profile.workflow_type or WORKFLOW_TYPE_CHOICES[0]
        self._clip_type.value = profile.clip_type or CLIP_TYPE_CHOICES[0]
        self._text_class.value = profile.text_class or TEXT_CLASS_CHOICES[0]
        self._sampler.value = profile.sampler_name or SAMPLER_CHOICES[0]
        self._scheduler.value = profile.scheduler or SCHEDULER_CHOICES[0]
        self._guidance.value = str(profile.guidance)
        self._steps.value = str(profile.default_steps)
        self._cfg.value = str(profile.default_cfg)
        self._priority.value = str(profile.priority)
        self._clip1.value = profile.default_clip1
        self._clip2.value = profile.default_clip2
        self._vae.value = profile.default_vae
        self._set_message(f"'{profile.name}' 프로필을 편집 중입니다.", error=False)

    def reset(self) -> None:
        """새 프로필 작성 상태로 되돌린다."""
        self._editing_name = ""
        for field in (self._name, self._family, self._model_file,
                      self._workflow_file, self._patterns, self._aliases,
                      self._clip1, self._clip2, self._vae):
            field.value = ""
        self._steps.value = "20"
        self._cfg.value = "4.0"
        self._guidance.value = "3.5"
        self._priority.value = "100"
        self._set_message("새 프로필을 입력하세요. 패턴은 최소 1개 필요합니다.",
                          error=False)

    # --- 저장 / 삭제 ------------------------------------------------------
    def save(self, _event: Optional[ft.Event] = None) -> None:
        try:
            payload = self._to_payload()
        except (TypeError, ValueError) as exc:
            self._set_message(f"숫자 항목이 올바르지 않습니다: {exc}", error=True)
            return

        if not payload["name"]:
            self._set_message("프로필 이름을 입력하세요.", error=True)
            return
        if not payload["patterns"]:
            # 패턴이 없으면 ModelRegistry 가 이 프로필을 아예 버린다.
            self._set_message("패턴을 최소 1개 입력하세요. (없으면 등록되지 않습니다)",
                              error=True)
            return

        MANUAL_PROFILE_DIR.mkdir(parents=True, exist_ok=True)
        target: Path = MANUAL_PROFILE_DIR / f"{safe_file_name(payload['name'])}.json"
        try:
            with open(target, "w", encoding="utf-8") as handle:
                json.dump({payload["name"]: payload}, handle,
                          ensure_ascii=False, indent=2)
        except OSError as exc:
            self._set_message(f"저장 실패: {exc}", error=True)
            return

        # 저장 직후 반영되도록 레지스트리를 다시 읽는다.
        reload_registry(self._registry)
        self._editing_name = payload["name"]
        self._set_message(f"'{payload['name']}' 프로필을 저장했습니다. ({target.name})",
                          error=False)
        self._refresh_saved_list()
        if self._on_saved is not None:
            self._on_saved(payload["name"])

    def delete(self, _event: Optional[ft.Event] = None) -> None:
        name = (self._name.value or self._editing_name or "").strip()
        if not name:
            self._set_message("삭제할 프로필을 먼저 선택하세요.", error=True)
            return
        target: Path = MANUAL_PROFILE_DIR / f"{safe_file_name(name)}.json"
        if not target.is_file():
            self._set_message(f"'{name}' 은(는) 수동 저장된 프로필이 아닙니다.", error=True)
            return
        try:
            target.unlink()
        except OSError as exc:
            self._set_message(f"삭제 실패: {exc}", error=True)
            return

        reload_registry(self._registry)
        self.reset()
        self._set_message(f"'{name}' 프로필을 삭제했습니다.", error=False)
        self._refresh_saved_list()

    def _set_message(self, message: str, *, error: bool) -> None:
        self._message.value = message
        self._message.color = TOKENS.error if error else TOKENS.success
        safe_update(self._message)

    def _make_loader(self, profile: ModelProfile):
        def handle(_event: ft.Event) -> None:
            self.load(profile)
            self._refresh_saved_list()
        return handle

    def _refresh_saved_list(self) -> None:
        """등록된 프로필 목록 (자동/수동 구분 포함)."""
        rows: List[ft.Control] = []
        for profile in sorted(self._registry.profiles, key=lambda p: p.name):
            from_json = bool(getattr(profile, "_from_json", False))
            rows.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.IMAGE_OUTLINED if from_json
                                    else ft.Icons.EDIT_OUTLINED,
                                    size=TOKENS.size_body, color=TOKENS.outline),
                            ft.Text(profile.name, size=TOKENS.size_caption),
                            ft.Container(expand=True),
                            ft.Text(f"{profile.default_steps} steps · "
                                    f"CFG {profile.default_cfg} · {profile.workflow_type}",
                                    size=TOKENS.size_caption, color=TOKENS.outline),
                            ft.Text("자동" if from_json else "수동",
                                    size=TOKENS.size_caption, color=TOKENS.outline),
                            ft.TextButton("불러오기",
                                          on_click=self._make_loader(profile)),
                        ],
                        spacing=TOKENS.space_sm, tight=True),
                    padding=ft.Padding.symmetric(vertical=TOKENS.space_xs)))
        self._saved_list.controls = rows
        safe_update(self._saved_list)

    def build(self) -> ft.Control:
        """수동 등록 탭 본문."""
        self._refresh_saved_list()
        return ft.Column(
            controls=[
                section_card("새 프로필 등록", ft.Column(
                    controls=[
                        ft.Row(controls=[self._name, self._family],
                               spacing=TOKENS.space_md, tight=True),
                        ft.Row(controls=[self._model_file, self._workflow_file],
                               spacing=TOKENS.space_md, tight=True),
                        self._patterns,
                        self._aliases,
                        ft.Row(controls=[self._base, self._workflow_type],
                               spacing=TOKENS.space_md, tight=True),
                        ft.Row(controls=[self._clip_type, self._text_class],
                               spacing=TOKENS.space_md, tight=True),
                        ft.Row(controls=[self._guidance, self._steps,
                                         self._cfg, self._priority],
                               spacing=TOKENS.space_md, tight=True),
                        ft.Row(controls=[self._sampler, self._scheduler],
                               spacing=TOKENS.space_md, tight=True),
                        ft.Row(controls=[self._clip1, self._clip2, self._vae],
                               spacing=TOKENS.space_md, tight=True),
                        ft.Row(
                            controls=[
                                ft.FilledButton("저장", icon=ft.Icons.SAVE,
                                                on_click=self.save),
                                ft.OutlinedButton("삭제",
                                                  icon=ft.Icons.DELETE_OUTLINE,
                                                  on_click=self.delete),
                                ft.TextButton("입력 초기화",
                                              on_click=self._handle_reset),
                            ],
                            spacing=TOKENS.space_md, tight=True),
                        self._message,
                    ],
                    spacing=TOKENS.space_sm, tight=True), expand=False),
                section_card(f"등록된 프로필 {len(self._registry.profiles)}개",
                             self._saved_list, expand=False),
            ],
            spacing=TOKENS.space_lg, tight=True, scroll=ft.ScrollMode.AUTO)

    def _handle_reset(self, _event: ft.Event) -> None:
        self.reset()
        safe_update(self._name, self._family, self._model_file,
                    self._workflow_file, self._patterns, self._aliases,
                    self._clip1, self._clip2, self._vae, self._steps,
                    self._cfg, self._guidance, self._priority, self._message)
        self._refresh_saved_list()
