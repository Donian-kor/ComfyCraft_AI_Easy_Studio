"""Flet 앱 상태 관리.

    Application 계층(JobManager) ──┐
                                   ├──> AppState ──> Page (View)
    UI 계층(Shell/Pages)         ──┘

페이지에는 business 로직이 없다. AppState 가 JobManager 이벤트를 받아
셸/페이지 컨트롤만 갱신한다.
"""

from __future__ import annotations

import asyncio
from typing import Dict, Optional

from app.application.job_manager import JobManager, JobState
from app.application.services import AppServices, build_services
from app.models.chat import ChatMessageData
from app.models.generation import GenerationRequest
from app.ui.flet.pages.chat import ChatPage
from app.ui.flet.pages.generation import GenerationPage
from app.ui.flet.pages.help import HelpPage
from app.ui.flet.pages.history import HistoryPage
from app.ui.flet.pages.home import HomePage
from app.ui.flet.pages.models import ModelsPage
from app.ui.flet.pages.settings import SettingsPage


def _run_on_ui(fn) -> None:
    """백그라운드 스레드에서 호출된 갱신을 UI 스레드로 넘긴다.

    Flet 의 run_task 는 실행 중인 이벤트 루프가 있을 때만 가능하므로,
    루프 밖(테스트/초기화)에서는 조용히 건너뛴다.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return
    loop.create_task(_call(fn))


async def _call(fn) -> None:
    try:
        result = fn()
        if asyncio.iscoroutine(result):
            await result
    except Exception:
        pass


class AppState:
    """앱 전체 상태. 서비스/Job/페이지를 한 곳에 모은다."""

    def __init__(self, services: Optional[AppServices] = None) -> None:
        self.services = services or build_services()
        self.jobs = JobManager(self.services)
        self.shell = None
        self.pages: Dict[str, object] = {}
        self.route = "/"
        self.messages: list = []

        self._build_pages()
        self.jobs.add_listener(self._on_job_update)

    # --- 페이지 ---------------------------------------------------------
    def _build_pages(self) -> None:
        self.pages = {
            "/": HomePage(on_navigate=self.navigate),
            "/generate": GenerationPage(on_generate=self.start_generation,
                                       on_stop=self.stop_generation),
            "/models": ModelsPage(self.services, on_refresh=self.refresh_models),
            "/chat": ChatPage(),
            "/history": HistoryPage(self.services),
            "/settings": SettingsPage(self.services,
                                      on_saved=self._notify_saved),
            "/help": HelpPage(),
        }

    def _notify_saved(self, message: str) -> None:
        if self.shell is not None:
            self.shell.set_status(message, "done")

    def navigate(self, route: str) -> None:
        """라우트를 바꾼다. 생성 Job 은 끊기지 않는다.

        등록되지 않은 라우트가 오면 홈으로 되돌린다. 알 수 없는 주소로
        들어왔을 때 빈 화면만 보여주는 것보다 홈이 낫다.
        """
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
        self._sync_job_into_page(page)

    # --- Job 연동 -------------------------------------------------------
    def _on_job_update(self, job) -> None:
        """Job 상태 변화 → 셸 상태바 + 현재 페이지 갱신.

        백그라운드 스레드에서 호출되므로 UI 갱신은 이벤트 루프로 넘긴다.
        """
        if self.shell is None:
            return

        def apply() -> None:
            self.shell.set_job_progress(
                job.progress if job.is_running else None, job.message)
            self.shell.set_status(job.message, job.state.value)
            self._sync_job_into_page(self.pages.get(self.route))

        _run_on_ui(apply)

        if job.state is JobState.DONE and job.result is not None:
            self._record_completion(job)

    def _sync_job_into_page(self, page) -> None:
        """현재 페이지가 진행 상태를 알고 있다면 반영한다."""
        job = self.jobs.active_job
        if isinstance(page, GenerationPage):
            page.set_running(bool(job and job.is_running), job.message if job else "")
            if job and job.is_running:
                page.set_progress(job.progress)
        elif isinstance(page, HomePage):
            self._sync_connection(page)

    def _record_completion(self, job) -> None:
        """완료된 Job 을 대화 메시지로 남긴다 (Phase 7)."""
        if job.result is None or not job.result.ok:
            return
        message = ChatMessageData(role="ai", kind="image", text="")
        message.become_image(job.result.image_path, meta=job.result.meta,
                             prompt=job.result.prompt, say="다 그렸어요! 어때요?")
        message.metadata["elapsed"] = job.result.elapsed
        self.messages.append(message)
        chat = self.pages.get("/chat")
        if isinstance(chat, ChatPage):
            chat.append_message(message)

    # --- 동작 -----------------------------------------------------------
    def start_generation(self) -> None:
        """현재 생성 화면 입력을 읽어 Job 을 시작한다."""
        page = self.pages.get("/generate")
        if not isinstance(page, GenerationPage):
            return
        config = self.services.config
        base = GenerationRequest(
            comfy_url=config.comfyui.url,
            lm_url=config.lmstudio.url,
            lm_model=config.lmstudio.model,
            poll_interval_seconds=float(config.comfyui.poll_interval_seconds),
            max_wait_seconds=int(config.comfyui.max_wait_seconds),
        )
        try:
            self.jobs.start(page.to_request(base))
        except RuntimeError as exc:
            if self.shell is not None:
                self.shell.set_status(str(exc), "error")

    def stop_generation(self) -> None:
        self.jobs.cancel_active()

    def refresh_models(self) -> None:
        """ComfyUI 에서 모델 목록을 읽어 관련 페이지를 갱신한다."""
        from app.features.connection.service import scan_comfyui_model_names

        names = scan_comfyui_model_names()
        models_page = self.pages.get("/models")
        if isinstance(models_page, ModelsPage):
            models_page.set_models(names)
        generate_page = self.pages.get("/generate")
        if isinstance(generate_page, GenerationPage):
            generate_page.set_model_options(names)

    def _sync_connection(self, home: HomePage) -> None:
        """ComfyUI / LM Studio 연결 상태를 홈 화면과 셸에 반영한다."""
        for service in ("comfy", "lm"):
            status = (self.services.check_comfy() if service == "comfy"
                      else self.services.check_lm())
            home.set_connection(service, status.ok, status.message)
            if self.shell is not None:
                self.shell.set_service_status(service, status.ok)
