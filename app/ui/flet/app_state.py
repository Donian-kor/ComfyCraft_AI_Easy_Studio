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


_ui_loop: Optional[asyncio.AbstractEventLoop] = None

# AI 환영 인사. 원본 Qt 의 TEMPLATES["welcome"] 과 같은 문장을 쓴다.
# 톤: "만들다"보다 "그리다" — 사용자가 아티스트와 대화하는 느낌.
WELCOME_TEXT = "안녕하세요? 무엇을 그려드릴까요?"

# 모델 변경 안내. 원본 Qt 의 TEMPLATES["model_changed"] 와 같은 문장.
SAY_MODEL_CHANGED = "{model}에 맞춰 이미지 그릴 준비를 마쳤어요. ({feature})"


def set_ui_loop(loop: Optional[asyncio.AbstractEventLoop]) -> None:
    """Flet 이 만든 이벤트 루프를 기억한다 (앱 시작 시 1회 호출).

    JobManager 는 threading.Thread 에서 돌기 때문에 그 스레드 안에는
    asyncio 루프가 돌고 있지 않다. 그래서 asyncio.get_running_loop() 로는
    UI 스레드를 찾을 수 없고, 진행률이 화면에 반영되지 않는다.
    Flet 의 page.run_task 도 내부적으로 run_coroutine_threadsafe 로
    이 루프에 작업을 넘기므로, 같은 방식으로 안전하게 넘긴다.
    """
    global _ui_loop
    _ui_loop = loop


def _run_on_ui(fn) -> None:
    """백그라운드 스레드의 갱신을 UI 스레드로 넘긴다.

    이벤트 루프가 아직 없으면(테스트/초기화) 조용히 건너뛴다.
    """
    loop = _ui_loop
    if loop is None or loop.is_closed():
        return
    try:
        asyncio.run_coroutine_threadsafe(_call(fn), loop)
    except RuntimeError:
        # 루프가 종료되는 타이밍에 겹친 경우. 앱 종료를 막지 않는다.
        pass


async def _call(fn) -> None:
    try:
        result = fn()
        if asyncio.iscoroutine(result):
            await result
    except Exception:
        # UI 갱신 실패가 Job 이나 앱 전체를 죽이면 안 된다
        pass


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

        self._build_pages()
        self.jobs.add_listener(self._on_job_update)

    # --- 페이지 ---------------------------------------------------------
    def _build_pages(self) -> None:
        self.studio = StudioPage(
            on_send=self.handle_prompt,
            on_stop=self.stop_generation,
            # 모델을 바꾸면 최적값을 적용하므로 레지스트리가 필요하다.
            model_registry=self.services.model_registry,
        )
        self.studio.chat.set_card_actions(
            on_save=self._save_image,
            on_reuse=self._reuse_settings,
            on_open=self._open_image,
        )
        self.pages = {
            "/": self.studio,
            "/options": self.studio,
            "/models": ModelsPage(self.services, on_refresh=self.refresh_models),
            "/history": HistoryPage(self.services, on_open=self._open_session),
            "/settings": SettingsPage(self.services, on_saved=self._notify_saved),
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
        """앱이 뜨자마자 환영 인사를 말하고, 서버 모델을 한 번 읽어 둔다.

        원본(Qt) 동작: 세션이 하나도 없고 채팅이 비었을 때만 AI 가
        환영 인사를 *채팅 말풍선*으로 남긴다 (main_controller._maybe_greet).
        Flet 초안은 이걸 상태 표시줄(set_status) 로 옮겨 버려
        '무엇을 그려드릴까요?' 가 오른쪽 아래 작은 글씨로만 나왔다.
        사용자는 AI 와 대화하는 프로그램이지 상태 표시창이 아니다.

        비동기로 모델을 읽어 서버가 꺼져 있어도 창이 늦게 뜨지 않게 한다.
        """
        import threading

        self.maybe_greet()
        threading.Thread(target=self.refresh_models, daemon=True).start()

    def maybe_greet(self) -> None:
        """저장된 대화가 없을 때만 AI 환영 인사를 채팅에 남긴다.

        회귀 근거: 예전엔 이 인사가 상태 표시줄에만 있었다. 사용자가
        'AI 가 말을 거는 프로그램'이라는 원본 UX 를 잃었다.
        이미 대화가 있으면 붙이면 안 된다(첫 인사가 뒤에 섞여 보인다).
        """
        if self.studio is None:
            return
        try:
            if self.services.session_manager.list_sessions(limit=1):
                return
        except Exception:
            # 세션 목록을 못 읽어도 인사는 보여야 한다(기능 부재로 보이면 안 된다)
            pass
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
        """현재 대화를 세션으로 남긴다 (원본처럼 대화가 이어진다)."""
        if self.studio is None:
            return
        try:
            from app.models.chat import messages_to_raw

            manager = self.services.session_manager
            session = manager.new_session(title="대화", model="")
            session["messages"] = messages_to_raw(self.studio.chat.messages)
            manager.save_session(session)
        except Exception:
            # 저장은 부가 기능이므로 대화 흐름을 막지 않는다
            pass

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


    # --- 카드 액션 -------------------------------------------------------
    def _save_image(self, image_path: str) -> None:
        """이미지를 새 이름으로 복사한다 (경로만 알리면 사용자가 옮긴다)."""
        if not image_path or self.shell is None:
            return
        try:
            from app.features.generation.output_files import copy_image

            output_dir = self.services.output_dir
            stamp = time.strftime("%Y%m%d_%H%M%S")
            target = output_dir / f"copy_{stamp}_{Path(image_path).name}"
            saved = copy_image(image_path, str(target))
            self.shell.set_status(
                f"복사했습니다: {saved}" if saved else "복사에 실패했습니다.",
                "done" if saved else "error")
        except Exception as exc:
            self.shell.set_status(f"복사 실패: {exc}", "error")

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

    def _open_image(self, message: ChatMessageData) -> None:
        """이미지를 크게 보는 Dialog 을 연다."""
        path = str(message.metadata.get("image_path", "") or "")
        if not path or self.shell is None:
            return
        self.shell.show_image_dialog(path, str(message.metadata.get("meta", "")))

    def _open_session(self, session_id: str) -> None:
        """이력에서 세션을 열면 대화로 복원한다."""
        session = self.services.session_manager.load_session(session_id)
        if session is None or self.studio is None:
            return
        from app.models.chat import messages_from_raw

        self.studio.chat.set_messages(messages_from_raw(session.get("messages", [])))
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

        pass
