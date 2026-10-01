"""Flet 앱 상태 관리.

챗봇 흐름을 그대로 살린다.

    입력창 전송
        ↓
    사용자 말풍선
        ↓
    프롬프트 확인 카드 (PromptCard)
        ↓  생성 시작
    생성 중 카드 (GenerationCard)  ← 중단 가능
        ↓  완료
    이미지 카드 (ImageCard)

Application 계층(JobManager)이 위 상태 변화를 알려주고, 이 계층은
그것을 카드 전환으로 번역할 뿐이다. 카드의 상태 머신은 아니다.
"""

from __future__ import annotations

import asyncio
import time
from pathlib import Path
from typing import Dict, List, Optional

import flet as ft

from app.application.job_manager import JobManager, JobState
from app.application.services import AppServices, build_services
from app.models.chat import (
    KIND_GENERATION,
    PHASE_GENERATING,
    SAY_DONE,
    ChatMessageData,
)
from app.models.generation import GenerationRequest
from app.ui.flet.pages.help import HelpPage
from app.ui.flet.pages.history import HistoryPage
from app.ui.flet.pages.model_desc import describe_model
from app.ui.flet.pages.models import ModelsPage
from app.ui.flet.pages.settings import SettingsPage
from app.ui.flet.pages.studio import StudioPage
from app.ui.flet.theme.switcher import save_theme_mode
from app.ui.flet.theme.tokens import apply_theme, set_theme_mode, toggle_theme_mode


_ui_loop: Optional[asyncio.AbstractEventLoop] = None

# AI 환영 인사. 원본 Qt 의 TEMPLATES["welcome"] 과 같은 문장을 쓴다.
# 톤: "만들다"보다 "그리다" — 사용자가 아티스트와 대화하는 느낌.
WELCOME_TEXT = "안녕하세요? 무엇을 그려드릴까요?"

# 세션이 아직 제목을 못 받은 상태의 기본값.
# SessionManager.new_session() 의 기본 제목과 같아야 "제목 미정" 판별이 된다.
DEFAULT_SESSION_TITLE = "새 대화"

# 첫 사용자 발화에서 잘라 쓸 제목 길이 (원본 _begin_send 와 같은 규칙)
SESSION_TITLE_LENGTH = 20

# 모델 변경 안내. 원본 Qt 의 TEMPLATES["model_changed"] 와 같은 문장.
SAY_MODEL_CHANGED = "{model}에 맞춰 이미지 그릴 준비를 마쳤어요. ({feature})"
# UI 스레드 통로는 ui_loop 모듈이 소유한다(순환 참조 방지).
# 여기서 이름만 다시 노출해 기존 호출(app.set_ui_loop 등)을 유지한다.
from app.ui.flet.ui_loop import (  # noqa: E402  (파일 끝자리 재수출)
    run_on_ui as _run_on_ui,
    set_ui_loop,
)


class AppState:
    """앱 전체 상태. 서비스/Job/페이지를 한 곳에 모은다."""

    def __init__(self, services: Optional[AppServices] = None) -> None:
        self.services = services or build_services()
        self.jobs = JobManager(self.services)
        self.shell = None
        self.studio: Optional[StudioPage] = None
        self.pages: Dict[str, object] = {}
        self.route = "/"

        # 현재 생성과 연결된 generation 메시지 (카드 전환에 쓴다)
        self._active_message_id: Optional[str] = None

        # 지금 이어 쓰고 있는 세션 ID. None 이면 아직 세션이 없다.
        # 회귀 근거: 예전에는 이 값이 없어서 _save_session() 이 매번
        # new_session() 으로 새 세션을 만들었다 (이력이 "대화"로만 쌓임).
        self._current_session_id: Optional[str] = None

        self._build_pages()
        self.jobs.add_listener(self._on_job_update)
        # 포스티프 프롬프트 표시도 옵션창이 job 을 직접 듣는다.
        self.jobs.add_listener(self.studio.options.on_job_update)

    # --- 페이지 ---------------------------------------------------------
    def _build_pages(self) -> None:
        from app.ui.flet.actions import (
            make_save_image_action,
            make_reuse_settings_action,
            make_open_image_action,
            make_open_output_folder_action,
            make_rewrite_action,
            make_regenerate_action,
        )
        self.studio = StudioPage(
            on_send=self.handle_prompt,
            on_stop=self.stop_generation,
            # 모델을 바꾸면 최적값을 적용하므로 레지스트리가 필요하다.
            model_registry=self.services.model_registry,
        )
        self.studio.chat.set_card_actions(
            on_save=make_save_image_action(self.services, lambda: self.shell),
            on_reuse=make_reuse_settings_action(
                lambda: self.studio, lambda: self.shell),
            on_open=make_open_image_action(
                lambda: self.shell,
                lambda: self.studio.chat.messages,
            ),
            on_open_folder=make_open_output_folder_action(
                self.services, lambda: self.shell),
            on_rewrite=make_rewrite_action(
                lambda: self.studio, lambda: self.shell),
            on_regenerate=make_regenerate_action(
                lambda: self.studio, lambda: self.shell, lambda: self),
        )
        self.pages = {
            "/": self.studio,
            "/options": self.studio,
            "/models": ModelsPage(self.services, on_refresh=self.refresh_models),
            "/history": HistoryPage(self.services, on_open=self._open_session),
            "/settings": SettingsPage(self.services, on_saved=self._notify_saved,
                                      on_theme_change=self.set_theme),
            "/help": HelpPage(),
        }

    def _notify_saved(self, message: str) -> None:
        if self.shell is not None:
            self.shell.set_status(message, "done")

    def navigate(self, route: str) -> None:
        """라우트를 바꾼다. 생성 Job 은 끊기지 않는다."""
        if route not in self.pages:
            route = "/"
        self.route = route
        if self.shell is None:
            return
        self.shell.sync_route(route)
        page = self.pages.get(route)
        if page is None:
            return
        self.shell.set_content(page.build())
        self._sync_job_state()

        # 모델 화면에 들어오면 서버에서 목록을 다시 읽는다.
        # (한 번만 읽으면 서버가 늦게 켜졌을 때 목록이 비어 보일 수 있다)
        if route == "/models":
            self.refresh_models()

    def start(self) -> None:
        """앱이 뜨자마자 지난 대화를 이어 주고(없으면 환영 인사), 모델을 읽는다.

        원본(Qt) 동작: 저장된 세션이 있으면 가장 최근 대화를 복원하고,
        하나도 없으면 AI 환영 인사를 채팅 말풍선으로 남긴다.
        (main_controller._maybe_greet / _switch_session)

        회귀 근거: Flet 초안은 세션을 복원하지 않았다. 그래서 대화가 있는
        상태로 실행하면 인사도 안 나고(세션이 있다고 보고) 화면은 비어
        있어 아무 말도 없는 상태가 됐다.
        """
        import threading

        if not self._restore_latest_session():
            self.maybe_greet()
        threading.Thread(target=self.refresh_models, daemon=True).start()
        # 우측 위 연결 표시등은 예전처럼 주기적으로 확인해야 한다.
        threading.Thread(target=self._poll_connections, daemon=True).start()

    def _poll_connections(self, interval: float = 10.0) -> None:
        """ComfyUI / LM Studio 연결을 주기적으로 확인해 표시등을 바꾼다.

        회귀 근거: AppShell.set_service_status() 가 존재만 하고 *아무도
        호출하지 않았다*. 그래서 표시등은 처음 회색(on_surface_variant)인
        채로였고, 서버가 켜져 있든 꺼져 있든 아무 반응이 없었다.
        원본은 check_connection() -> apply_connection_result() ->
        update_connection_label() 로 표시등을 갱신했다.
        """
        import time

        while True:
            for which in ("comfy", "lm"):
                try:
                    checker = (self.services.check_comfy if which == "comfy"
                               else self.services.check_lm)
                    ok = bool(checker().ok)
                except Exception:
                    ok = False
                if self.shell is not None:
                    self.shell.set_service_status(which, ok)
            time.sleep(interval)

    def check_connections_now(self) -> None:
        """연결 상태를 지금 한 번 확인한다(설정 저장 후 등)."""
        for which in ("comfy", "lm"):
            try:
                checker = (self.services.check_comfy if which == "comfy"
                           else self.services.check_lm)
                ok = bool(checker().ok)
            except Exception:
                ok = False
            if self.shell is not None:
                self.shell.set_service_status(which, ok)

    def _restore_latest_session(self) -> bool:
        """가장 최근 저장 세션을 채팅으로 복원한다. 복원했으면 True.

        원본과 같은 정책: 저장된 세션이 있으면 인사를 붙이지 않는다.
        """
        if self.studio is None:
            return False
        try:
            recent = self.services.session_manager.list_sessions(limit=1)
        except Exception:
            return False
        if not recent:
            return False
        session_id = str(recent[0].get("id", "") or "")
        if not session_id:
            return False
        session = self.services.session_manager.load_session(session_id)
        if not session or not session.get("messages"):
            return False
        from app.models.chat import messages_from_raw

        self.studio.chat.set_messages(
            messages_from_raw(session.get("messages", [])))
        # 이어서 대화하면 이 세션에 덮어써야 한다 (새 세션을 만들면 안 됨)
        self._current_session_id = session_id
        return True
    def maybe_greet(self) -> None:
        """저장된 대화가 없을 때만 AI 환영 인사를 채팅에 남긴다.

        회귀 근거: 예전엔 이 인사가 상태 표시줄에만 있었다. 사용자가
        'AI 가 말을 거는 프로그램'이라는 원본 UX 를 잃었다.
        이미 대화가 있으면 붙이면 안 된다(첫 인사가 뒤에 섞여 보인다).
        """
        if self.studio is None:
            return
        if self.studio.chat.messages:
            return
        self.studio.chat.append_message(
            ChatMessageData(role="ai", kind="text", text=WELCOME_TEXT))
    # --- 챗봇 흐름 -------------------------------------------------------
    def handle_prompt(self, text: str) -> None:
        """입력창에서 프롬프트를 받았다.

        사용자가 한 말 → 프롬프트 확인 카드 → 곧바로 생성을 시작한다.
        (원본 UX: 확인 카드가 곧 생성 카드로 이어진다)
        """
        prompt = (text or "").strip()
        if not prompt or self.studio is None:
            return

        user_message = ChatMessageData(role="user", kind="text", text=prompt)
        self.studio.chat.append_message(user_message)

        card = ChatMessageData(role="ai", kind=KIND_GENERATION)
        card.metadata.update({
            "phase": "prompt",
            "original": prompt,
            "enhanced": prompt,
            "status": "프롬프트를 확인 중입니다",
        })
        card.say = "이렇게 그릴게요"
        self.studio.chat.append_message(card)
        self._active_message_id = card.id
        self._save_session()

        self.start_generation(prompt)

    def _save_session(self) -> None:
        """현재 대화를 '진행 중인 세션 하나'에 계속 덮어쓴다.

        회귀 근거: 예전 구현은 부를 때마다 new_session() 으로 **새 세션을
        만들어** 저장했다. 그래서 프롬프트를 보낼 때마다 이력이 "대화"
        한 줄씩 늘었고(실제 저장소에 제목이 모두 "대화"인 세션 6개),
        직전 대화가 아니라 최근 1회분만 남아 대화가 이어지지 않았다.
        원본은 _current_session 하나를 _flush_session() 으로 덮어썼다.

        세션 파일은 첫 프롬프트 때 만든다. '새 대화'를 누를 때마다 만들면
        아무것도 안 한 빈 세션이 이력에 쌓인다.
        """
        if self.studio is None:
            return
        messages = self.studio.chat.messages
        # 새 세션은 사용자가 실제로 무언가 보낸 뒤에만 만든다.
        # 환영 인사만 있는 상태를 저장하면 이력이 빈 세션으로 채워진다
        # ('새 대화'를 연속으로 눌러도 세션이 쌓이지 않아야 한다).
        if self._current_session_id is None:
            if not any(m.role == "user" for m in messages):
                return
        try:
            from app.models.chat import messages_to_raw

            manager = self.services.session_manager
            session = (manager.load_session(self._current_session_id)
                       if self._current_session_id else None)
            if session is None:
                session = manager.new_session(model=self._current_model())
                self._current_session_id = str(session.get("session_id", ""))
            else:
                session["model"] = self._current_model()

            # 제목은 사용자가 아직 안 바꿨을 때만 첫 발화로 채운다.
            # (P2-1 이름 변경을 나중에 붙여도 덮어쓰지 않는다)
            if str(session.get("title", "") or "").strip() in (
                    "", DEFAULT_SESSION_TITLE):
                first = self._first_user_text()
                if first:
                    session["title"] = first[:SESSION_TITLE_LENGTH]

            session["messages"] = messages_to_raw(self.studio.chat.messages)
            manager.save_session(session)
        except Exception:
            # 저장은 부가 기능이므로 대화 흐름을 막지 않는다
            pass

    def _current_model(self) -> str:
        """지금 선택된 ComfyUI 모델 파일명 (세션에 남겨 이력에 보여준다)."""
        if self.studio is None:
            return ""
        try:
            return str(self.studio.options.to_request().comfy_model or "")
        except Exception:
            return ""

    def _first_user_text(self) -> str:
        """세션 제목으로 쓸 첫 사용자 발화 (없으면 빈 문자열)."""
        if self.studio is None:
            return ""
        for message in self.studio.chat.messages:
            if message.role == "user" and message.text.strip():
                return message.text.strip()
        return ""

    def new_chat(self) -> bool:
        """새 대화를 시작한다. 생성 중이면 거부하고 False 를 준다.

        회귀 근거: Flet 전환에서 이 기능이 통째로 빠졌다. 원본
        _on_new_chat_clicked() 는 진행 중이던 세션을 저장하고 채팅을 비운
        뒤 새 세션으로 갈아탔다.

        저장된 대화는 지우지 않는다 — 이력에 남고 화면만 새로 시작한다.
        세션 파일은 다음 프롬프트에서 만들어지므로, 연속으로 눌러도
        빈 세션이 이력에 쌓이지 않는다.
        """
        if self.studio is None:
            return False
        if self.jobs.is_busy:
            self._set_status("생성 중에는 새 대화를 시작할 수 없어요.", "error")
            return False

        self._save_session()            # 지금까지의 대화를 이력에 남긴다
        self.studio.chat.clear()
        self._active_message_id = None
        self._current_session_id = None  # 다음 프롬프트에서 새 세션이 열린다
        self.maybe_greet()
        if self.shell is not None:
            self.shell.set_status("새 대화를 시작했습니다.", "done")
        return True

    def toggle_theme(self) -> str:
        """다크 ↔ 라이트를 바꿔 화면 전체에 적용한다. 바뀐 모드를 돌려준다.

        원본 Qt 의 available_themes()/apply_theme() 에 해당한다.
        QSS 8종을 옮기는 대신, 다크/라이트 두 벌의 토큰만 정의했다.
        """
        return self.set_theme(toggle_theme_mode())

    def set_theme(self, mode: str) -> str:
        """지정된 모드로 화면을 다시 칠한다. 적용된 모드를 돌려준다."""
        mode = set_theme_mode(mode)
        if self.shell is not None:
            apply_theme(self.shell.page, mode, self.shell.root)
        save_theme_mode(self.services, mode)
        if self.shell is not None:
            self.shell.set_status(
                "밝은 테마로 전환했습니다." if mode == "light"
                else "어두운 테마로 전환했습니다.", "done")
        return mode

    def start_generation(self, prompt: str = "") -> Optional[object]:
        """Job 을 시작한다. 이미 돌고 있으면 예외 대신 상태로 알린다."""
        if self.studio is None:
            return None
        config = self.services.config
        base = GenerationRequest(
            comfy_url=config.comfyui.url,
            lm_url=config.lmstudio.url,
            max_wait_seconds=int(config.comfyui.max_wait_seconds),
            poll_interval_seconds=float(config.comfyui.poll_interval_seconds),
        )
        request = self.studio.options.to_request(base)
        if prompt:
            request.prompt = prompt
            request.enhanced_prompt = ""   # 새 입력은 다시 enhancement 를 탄다
            _run_on_ui(self.studio.options.clear_enhanced_prompt)

        try:
            return self.jobs.start(request)
        except RuntimeError as exc:
            if self.shell is not None:
                self.shell.set_status(str(exc), "error")
            return None

    def stop_generation(self) -> None:
        self.jobs.cancel_active()

    def _mark_generating(self) -> None:
        """프롬프트 확인 카드 → 생성 중 카드로 제자리 전환."""
        if self.studio is None or not self._active_message_id:
            return
        message = self.studio.chat.find(self._active_message_id)
        if message is None:
            return
        message.metadata["phase"] = PHASE_GENERATING
        message.metadata["status"] = "이미지 생성 중..."
        message.say = "그릴게요"
        self.studio.chat.replace_message(message)

    def _mark_finished(self, result) -> None:
        """생성 중 카드 → 이미지 카드로 제자리 전환."""
        if self.studio is None or not self._active_message_id:
            return
        message = self.studio.chat.find(self._active_message_id)
        if message is None:
            return
        if result is not None and result.ok:
            message.become_image(
                result.image_path, meta=result.meta, prompt=result.prompt,
                snapshot=result.snapshot, say=SAY_DONE)
            message.metadata["elapsed"] = result.elapsed
        else:
            error = (result.error if result is not None else "") or "생성에 실패했습니다"
            message.metadata["phase"] = "failed"
            message.metadata["status"] = error
            message.say = error
        self.studio.chat.replace_message(message)
        self._active_message_id = None
        # 카드가 이미지로 바뀐 '뒤'에 저장한다. handle_prompt() 시점에
        # 저장하면 결과물이 만들어지기 전이라 이력에 이미지가 남지 않는다.
        self._save_session()


    # --- Job 연동 -------------------------------------------------------
    def _on_job_update(self, job) -> None:
        """Job 상태를 카드 전환과 셸 상태 표시로 번역한다.

        Job 은 백그라운드 스레드에서 오므로 UI 갱신은 모두 이벤트 루프로 넘긴다.
        """
        if self.shell is not None:
            def apply() -> None:
                self.shell.set_job_progress(
                    job.progress if job.is_running else None, job.message)
                self.shell.set_status(job.message, job.state.value)
                self._sync_job_state()

            _run_on_ui(apply)

        _run_on_ui(lambda: self._advance_card(job))

    def _advance_card(self, job) -> None:
        """카드 상태를 Job 상태에 맞춰 제자리에서 바꾼다."""
        if self.studio is None or not self._active_message_id:
            return
        if job.is_running:
            if job.request is not None:
                message = self.studio.chat.find(self._active_message_id)
                if message is not None and message.phase != PHASE_GENERATING:
                    self._mark_generating()
            return
        if job.state in (JobState.DONE, JobState.FAILED, JobState.CANCELLED):
            self._mark_finished(job.result)

    def _sync_job_state(self) -> None:
        """현재 화면에 생성 중 상태를 반영한다."""
        if self.studio is None:
            return
        job = self.jobs.active_job
        self.studio.set_busy(bool(job and job.is_running))


    def _open_session(self, session_id: str) -> None:
        """이력에서 세션을 열면 대화로 복원한다."""
        session = self.services.session_manager.load_session(session_id)
        if session is None or self.studio is None:
            return
        from app.models.chat import messages_from_raw

        self.studio.chat.set_messages(messages_from_raw(session.get("messages", [])))
        # 이 세션을 이어 쓰는 상태로 만든다 (새 세션 난립 방지)
        self._current_session_id = session_id
        self._active_message_id = None
        self.navigate("/")

    # --- 모델 -------------------------------------------------------------
    def on_comfy_model_changed(self, event: ft.Event) -> None:
        """ComfyUI 모델이 바뀌면 최적 설정값을 적용하고 AI 가 말한다.

        원본(Qt) 의 _on_comfy_model_changed() 와 같은 역할:
            로그 + apply_model_defaults() + AI 채팅 메시지

        회귀 근거: 이 기능이 Flet 전환에서 통째로 빠졌다. 모델을 바꿔도
        Steps/CFG 가 그대로여서 '자동 최적 설정이 고장났다'는 인상이 들고,
        AI 도 아무 말을 하지 않았다.
        """
        if self.studio is None:
            return
        options = self.studio.options
        name = str(options.to_request().comfy_model or "").strip()
        if not name or name == "로드된 모델 없음":
            return

        # 1) 최적값 자동 적용
        try:
            notice = options.apply_model_defaults(name)
        except Exception as exc:   # 프로필이 틀려도 앱은 계속 돌아야 한다
            self._set_status(f"최적 설정 적용 실패: {exc}", "error")
            return

        # 2) AI 채팅 안내
        try:
            profile = self.services.model_registry.detect(name)
            short, feature, _tooltip = describe_model(profile, name)
            self.studio.chat.append_message(ChatMessageData(
                role="ai", kind="text",
                text=SAY_MODEL_CHANGED.format(model=short, feature=feature)))
        except Exception:
            pass

        if self.shell is not None and notice:
            self.shell.set_status(notice, "done")

    def refresh_models(self, *, lm: bool = True) -> None:
        """ComfyUI / LM Studio 서버에서 모델 목록을 읽어 화면에 반영한다.

        로컬 파일 스캔(scan_comfyui_model_names)은 서버가 꺼져 있으면 빈
        목록을 준다. 그래서 사용자가 볼 모델 combobox 는 반드시 서버 조회
        (ModelFetcher) 로 채운다.
        """
        fetcher = self.services.model_fetcher

        names: List[str] = []
        try:
            names = list(fetcher.get_comfyui_models() or [])
        except Exception as exc:      # 서버가 꺼져 있어도 앱은 계속 뜨게 둔다
            self._set_status(f"ComfyUI 모델 조회 실패: {exc}", "error")
        if not names:
            # 서버 조회가 비면 로컬 스캔으로 최소한 무엇이 있는지는 보여준다
            try:
                from app.features.connection.service import scan_comfyui_model_names

                names = list(scan_comfyui_model_names() or [])
            except Exception:
                names = []

        if self.studio is not None:
            self.studio.options.set_model_options(
                names, on_change=self.on_comfy_model_changed)
        models_page = self.pages.get("/models")
        if isinstance(models_page, ModelsPage):
            models_page.set_models(names)

        if lm:
            self.refresh_lm_models()

    def refresh_lm_models(self) -> None:
        """LM Studio 모델 목록을 읽어 옵션 패널에 넣는다."""
        try:
            names = list(self.services.model_fetcher.get_lmstudio_models() or [])
        except Exception:
            names = []
        if self.studio is not None:
            self.studio.options.set_lm_model_options(names)

    def _set_status(self, message: str, kind: str) -> None:
        if self.shell is not None:
            self.shell.set_status(message, kind)

    # --- 기존 테스트 호환용 델리게이트 ---------------------------------------
    def _reuse_settings(self, message: ChatMessageData) -> None:
        """이미지 카드의 '이 설정으로' — 지난 옵션을 좌측 패널에 되돌린다."""
        if self.studio is None:
            return
        snapshot = message.metadata.get("snapshot") or {}
        if not snapshot:
            return
        self.studio.options.apply_snapshot(snapshot)
        if self.shell is not None:
            self.shell.set_status("지난 생성 설정을 불러왔습니다.", "done")
