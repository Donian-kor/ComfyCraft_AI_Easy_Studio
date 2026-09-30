"""Application 계층: 생성 Job 관리 (Phase 3).

목표: "History 로 이동 / Settings 열기 / 다른 페이지로 이동해도
생성 작업이 중단되지 않는다."

Job 은 UI 를 모른다. UI 는 Job 에 이벤트를 구독할 뿐이다.
"""

from __future__ import annotations

import logging
import threading
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional

from app.application.generation_service import GenerationService
from app.application.services import AppServices
from app.models.generation import (
    STATUS_CANCELLED,
    STATUS_DONE,
    GenerationProgress,
    GenerationRequest,
    GenerationResult,
)

logger = logging.getLogger(__name__)


class JobState(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class GenerationJob:
    """생성 1건의 수명주기. 화면 상태와 분리되어 있다."""

    job_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    request: Optional[GenerationRequest] = None
    state: JobState = JobState.PENDING
    progress: int = 0
    message: str = "대기 중"
    logs: List[str] = field(default_factory=list)
    result: Optional[GenerationResult] = None
    started_at: float = 0.0
    finished_at: float = 0.0
    # LM Studio 가 향상해 준 프롬프트. 옵션창의 '포스티프 프롬프트' 칸이
    # 이 값을 본다.
    #
    # 회귀 근거: GenerationProgress 에 enhanced_prompt 가 있는데 job 으로
    # 옮기는 코드가 없어서 값이 여기서 조용히 사라졌다. 그 결과 포스티프
    # 칸이 영영 비어 있어 '기능이 있나?' 싶었다.
    enhanced_prompt: str = ""

    @property
    def is_running(self) -> bool:
        return self.state == JobState.RUNNING

    @property
    def elapsed_seconds(self) -> float:
        if not self.started_at:
            return 0.0
        end = self.finished_at or time.monotonic()
        return end - self.started_at




class JobManager:
    """생성 Job 을 백그라운드 스레드로 돌리고 상태를 알린다.

    - 한 번에 하나의 활성 Job (ComfyUI 큐와 1:1 대응)
    - 화면을 어디로 옮겨도 스레드는 살아 있다
    - lock 으로 상태를 보호한다
    """

    def __init__(self, services: AppServices) -> None:
        self._services = services
        self._lock = threading.RLock()
        self._jobs: Dict[str, GenerationJob] = {}
        self._listeners: List[ProgressListener] = []
        self._active_id: Optional[str] = None
        self._thread: Optional[threading.Thread] = None
        self._service: Optional[GenerationService] = None

    # -- 구독 -------------------------------------------------------------
    def add_listener(self, listener: ProgressListener) -> None:
        with self._lock:
            self._listeners.append(listener)

    def remove_listener(self, listener: ProgressListener) -> None:
        with self._lock:
            if listener in self._listeners:
                self._listeners.remove(listener)

    def _notify(self, job: GenerationJob) -> None:
        # 리스너 예외가 Job 을 죽이면 안 되므로 각각 격리한다.
        for listener in list(self._listeners):
            try:
                listener(job)
            except Exception:
                logger.exception("Job 리스너 실행 중 오류")

    # -- 조회 -------------------------------------------------------------
    @property
    def active_job(self) -> Optional[GenerationJob]:
        with self._lock:
            if not self._active_id:
                return None
            return self._jobs.get(self._active_id)

    def get_job(self, job_id: str) -> Optional[GenerationJob]:
        with self._lock:
            return self._jobs.get(job_id)

    def list_jobs(self) -> List[GenerationJob]:
        with self._lock:
            return sorted(self._jobs.values(),
                          key=lambda j: j.started_at, reverse=True)

    @property
    def is_busy(self) -> bool:
        job = self.active_job
        return bool(job and job.is_running)

    # -- 실행 -------------------------------------------------------------
    def start(self, request: GenerationRequest) -> GenerationJob:
        """생성을 백그라운드에서 시작한다. 이미 돌고 있으면 에러.

        점유 확인과 등록을 한 번의 lock 안에서 해야 한다. 따로 하면
        "이미 돌고 있음" 검사를 통과한 뒤 다른 스레드가 Job 을 끼워 넣어
        두 개가 동시에 돌거나, 활성 Job 아닌데 start 가 통과하는 raced 상태가 생긴다.
        """
        with self._lock:
            current = self._jobs.get(self._active_id) if self._active_id else None
            if current is not None and current.is_running:
                raise RuntimeError("이미 생성이 진행 중입니다. 먼저 중단해 주세요.")

            job = GenerationJob(request=request, state=JobState.RUNNING,
                                started_at=time.monotonic())
            service = GenerationService(self._services)
            thread = threading.Thread(target=self._run, args=(job, service),
                                      daemon=True)

            self._jobs[job.job_id] = job
            self._active_id = job.job_id
            self._service = service
            self._thread = thread

        thread.start()
        self._notify(job)
        return job

    def _run(self, job: GenerationJob, service: GenerationService) -> None:
        def on_progress(progress: GenerationProgress) -> None:
            with self._lock:
                job.progress = progress.progress
                job.message = progress.message or job.message
                # 향상된 프롬프트가 오면 잡아둔다(화면 표시용).
                # 결과로도 덮을 수 있지만, '향상은 됐는데 생성은
                # 실패한' 경우 결과에 값이 없으므로 여기서 반드시 받아야 한다.
                if progress.enhanced_prompt:
                    job.enhanced_prompt = progress.enhanced_prompt
            self._notify(job)

        def on_log(message: str) -> None:
            with self._lock:
                job.logs.append(message)
            self._notify(job)

        try:
            result = service.generate(job.request, on_progress=on_progress,
                                      log=on_log)
            with self._lock:
                job.result = result
                if result.enhanced_prompt:
                    job.enhanced_prompt = result.enhanced_prompt
                job.finished_at = time.monotonic()
                job.progress = 100 if result.status == STATUS_DONE else job.progress
                if result.status == STATUS_DONE:
                    job.state = JobState.DONE
                    job.message = "완료"
                elif result.status == STATUS_CANCELLED:
                    job.state = JobState.CANCELLED
                    job.message = "중단됨"
                else:
                    job.state = JobState.FAILED
                    job.message = result.error or "생성 실패"
        except Exception as exc:  # 방어적: 스레드가 죽어도 UI 는 알아야 한다
            logger.exception("Job 실행 중 예외")
            with self._lock:
                job.state = JobState.FAILED
                job.message = str(exc)
                job.finished_at = time.monotonic()
        finally:
            with self._lock:
                if self._active_id == job.job_id:
                    self._active_id = None
            self._notify(job)

    def cancel_active(self) -> bool:
        """진행 중인 Job 을 중단한다. 진행 중이 아니면 False."""
        with self._lock:
            job = self._jobs.get(self._active_id) if self._active_id else None
            service = self._service
        if service is None or job is None or not job.is_running:
            return False
        service.request_stop()
        return True

    def clear_finished(self) -> int:
        """완료된 Job 기록을 비운다 (활성 Job 은 남긴다)."""
        with self._lock:
            removable = [jid for jid, j in self._jobs.items() if not j.is_running]
            for jid in removable:
                del self._jobs[jid]
            return len(removable)

    def wait_for_idle(self, timeout: Optional[float] = None) -> bool:
        """활성 Job 이 끝날 때까지 대기한다 (테스트/종료 처리용).

        lock 밖에서 join 해야 한다. Job 스레드가 상태를 갱신할 때 같은 lock 을
        잡으므로, 안에서 join 하면 서로를 영원히 기다리는 교착이 된다.
        """
        with self._lock:
            thread = self._thread
        if thread is None:
            return True
        thread.join(timeout=timeout)
        return not thread.is_alive()

ProgressListener = Callable[[GenerationJob], None]
