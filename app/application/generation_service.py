"""Application 계층: 이미지 생성 Use Case.

기존 GenerationWorker(Qt Signal + Controller 역참조)를 순수 Python
서비스로 다시 만들었다.

    GenerationService
        ↓
    GenerationRequest / FaceDetailerSettings
        ↓
    WorkflowService
        ↓
    ComfyTransport (ComfyUI 통신)
        ↓
    GenerationResult

UI(Flet)는 Job 을 시작하고 진행 콜백만 받는다. 화면을 옮겨도 작업은 계속된다.
"""

from __future__ import annotations

import json
import logging
import random
import time
from typing import Callable, List, Optional

from app.application.comfy_transport import ComfyTransport
from app.application.services import AppServices
from app.features.generation.workflow_builder import build_workflow, validate_workflow
from app.features.prompt.prompts import (
    enhance_prompt_sync,
    load_external_prompts,
    resolve_negative_prompt,
)
from app.features.prompt.system_prompt import select_system_prompt
from app.models.generation import (
    STATUS_CANCELLED,
    STATUS_CONNECTING,
    STATUS_DONE,
    STATUS_ENHANCING,
    STATUS_FAILED,
    STATUS_GENERATING,
    STATUS_SUBMITTING,
    GenerationProgress,
    GenerationRequest,
    GenerationResult,
    StopToken,
)

logger = logging.getLogger(__name__)

ProgressFn = Callable[[GenerationProgress], None]
LogFn = Callable[[str], None]


class GenerationService:
    """이미지 생성 1건을 수행하는 서비스.

    Qt Signal 대신 일반 콜백을 쓴다. 그러면 어떤 UI 프레임워크에서도
    (Flet, CLI, 테스트) 그대로 재사용할 수 있다.

    서버 통신은 ComfyTransport 가 담당하고, 여기서는 '무엇을 생성할지'
    (프롬프트 확정 → 워크플로우 조립 → 결과 정리)만 다룬다.
    """

    def __init__(self, services: AppServices) -> None:
        self.services = services
        self._last_model_name: Optional[str] = None
        self._transport: Optional[ComfyTransport] = None
        self._stop = StopToken()
        self._logs: List[str] = []

    # -- 진행/로그 콜백 --------------------------------------------------
    def _emit_log(self, message: str, log: Optional[LogFn] = None) -> None:
        text = str(message)
        self._logs.append(text)
        logger.debug(text)
        if log is not None:
            log(text)

    def _progress(
        self,
        on_progress: Optional[ProgressFn],
        *,
        status: str,
        progress: int,
        message: str = "",
        log: str = "",
        preview: str = "",
        enhanced_prompt: str = "",
    ) -> None:
        if on_progress is None:
            return
        on_progress(GenerationProgress(
            status=status,
            progress=max(0, min(int(progress), 100)),
            message=message,
            log=log,
            preview=preview,
            enhanced_prompt=enhanced_prompt,
            elapsed_seconds=0.0,
        ))

    # -- 중단 -------------------------------------------------------------
    def request_stop(self) -> None:
        """생성 중단을 요청한다 (즉시 반영되지 않을 수 있다)."""
        self._stop.request_stop()
        if self._transport is not None:
            self._transport.interrupt()

    @property
    def stop_requested(self) -> bool:
        return self._stop.is_set()

    # -- 메인 엔트리 ------------------------------------------------------
    def generate(
        self,
        request: GenerationRequest,
        on_progress: Optional[ProgressFn] = None,
        log: Optional[LogFn] = None,
    ) -> GenerationResult:
        """생성 1건을 수행하고 결과를 반환한다.

        예외를 던지지 않는다 — 실패는 GenerationResult.status 로 표현한다.
        """
        self._stop.reset()
        self._logs = []
        started = time.monotonic()

        try:
            return self._generate_inner(request, on_progress, log, started)
        except Exception as exc:
            logger.exception("생성 실패")
            self._emit_log(f"[ERROR] {exc}", log)
            return GenerationResult(
                status=STATUS_CANCELLED if self._stop.is_set() else STATUS_FAILED,
                prompt=request.prompt,
                model=request.comfy_model,
                width=request.width,
                height=request.height,
                seed=request.seed,
                snapshot=request.to_dict(),
                logs=list(self._logs),
                error=str(exc),
                elapsed=time.monotonic() - started,
            )
        finally:
            self._cleanup()

    def _cleanup(self) -> None:
        if self._transport is not None:
            self._transport.clear_queue()
            self._transport.close()
            self._transport = None

    # -- 내부 구현 --------------------------------------------------------
    def _generate_inner(
        self,
        request: GenerationRequest,
        on_progress: Optional[ProgressFn],
        log: Optional[LogFn],
        started: float,
    ) -> GenerationResult:
        # UI 는 "Seed = -1"을 '랜덤'이라는 뜻으로 쓰지만, 아래 build_workflow 는
        # request.seed 를 그대로 KSampler 에 넘긴다. KSampler 의 seed 범위는
        # min=0 이라 -1 을 받으면 서버가 400(value_smaller_than_min) 으로 거절해
        # 이미지가 전혀 만들어지지 않는다. 연결 확인보다 먼저 확정해 두면
        # 어느 경로로 실패하든 스냅샷에 실제 시드가 남는다.
        seed = request.seed if request.seed >= 0 else random.randint(1, 2**31 - 1)
        request.seed = seed

        # 1) ComfyUI 연결 확인
        self._progress(on_progress, status=STATUS_CONNECTING, progress=0,
                       message="ComfyUI 연결 확인 중...")
        api = self.services.comfy_client(request.comfy_url)
        api.get_system_stats(timeout=3).raise_for_status()
        self._transport = ComfyTransport(
            api, self.services.output_dir,
            log=lambda m: self._emit_log(m, log))

        model_name = request.comfy_model
        if not model_name or model_name in ("없음", "로드된 모델 없음"):
            raise RuntimeError("ComfyUI 모델을 선택해주세요.")

        profile = self.services.model_registry.detect(model_name)

        # 2) 프롬프트 결정 (enhance 입력이 있으면 LM Studio 호출을 건너뛴다)
        prompt = self._resolve_prompt(request, profile, on_progress, log)
        # 네거티브 확정. 원본 Qt 는 빈칸이면 기본 문구를 강제했는데,
        # 여기서는 설정값(비어 있음)만 보고 그대로 보내 네거티브가
        # 통째로 빠졌다. 저품질/흐림/왜곡 억제가 사라져 결과물이 나빠졌다.
        negative = resolve_negative_prompt(
            request.negative_prompt,
            self.services.config.prompts.negative_default,
            profile=profile,
            model_name=model_name,
        )

        # 3) 워크플로우 조립 + 검증
        node_exists = self._transport.node_exists
        workflow = build_workflow(
            request,
            profile,
            manager=self.services.workflow_manager,
            filename_prefix=self._build_filename_prefix(request),
            log=lambda m: self._emit_log(m, log),
            node_exists=node_exists,
            get_clips=lambda: self.services.model_fetcher.get_comfyui_clips(request.comfy_url),
            get_vaes=lambda: self.services.model_fetcher.get_comfyui_vaes(request.comfy_url),
            find_sam_model=self._transport.find_sam_model_name,
        )
        validate_workflow(workflow, node_exists=node_exists)

        if self._stop.is_set():
            return self._cancelled(request, seed, started)


        # 4) 사전 큐 정리 (재실행 400 에러 방지)
        self._last_model_name = self._transport.prepare_queue(
            model_name, self._last_model_name)
        time.sleep(0.5)

        workflow_json = json.dumps(workflow, indent=2, ensure_ascii=False)
        # 전체 JSON은 파일 로그에만 남기고, 화면에는 노드 수 요약만 표시한다.
        logger.debug("워크플로우 JSON (전체):\n%s", workflow_json)
        # 실제로 무엇이 ComfyUI 로 나갔는지 한 줄로 남긴다.
        #
        # 회귀 근거: app.log 에 '생성' 관련 줄이 0개였다(Flet 디버그뿐).
        # 그래서 옵션이 잘 못 갔어도 추적이 불가능했다. 이상 징후가 보일 때
        # 이 줄 하나로 값이 제대로 나갔는지 바로 확인한다.
        logger.info("[전송요약] model=%s steps=%s cfg=%s sampler=%s sched=%s "
                    "denoise=%s size=%sx%s seed=%s fd=%s", model_name,
                    request.steps, request.cfg, request.sampler,
                    request.scheduler, request.denoise, request.width,
                    request.height, seed, request.facedetailer.enabled)
        logger.info("[전송요약] positive=%r negative=%r", prompt[:300],
                    negative[:300])
        self._emit_log(f"워크플로우 준비: 노드 {len(workflow)}개", log)

        # 5) 큐 등록
        self._progress(on_progress, status=STATUS_SUBMITTING, progress=0,
                       message="워크플로우 큐 등록 중...")
        response = None
        timeout = self.services.config.comfyui.timeout_seconds
        try:
            response = api.prompt(workflow, timeout=timeout)
            response.raise_for_status()
        except Exception as exc:
            detail = ""
            try:
                if getattr(response, "text", ""):
                    detail = f" / 응답: {response.text[:1000]}"
                if getattr(response, "status_code", None):
                    detail = f" / 상태코드: {response.status_code}{detail}"
            except Exception:
                pass
            self._emit_log(f"[ERROR] ComfyUI 프롬프트 등록 실패: {exc}{detail}", log)
            logger.debug("실패한 워크플로우 JSON:\n%s", workflow_json)
            raise

        prompt_id = (response.json() or {}).get("prompt_id")
        if not prompt_id:
            raise RuntimeError("ComfyUI에서 prompt_id를 받지 못했습니다.")
        self._emit_log(f"워크플로우 큐 등록 완료: {prompt_id}", log)

        # 6) WebSocket 진행률 구독 (실패해도 HTTP 폴링으로 진행)
        self._transport.start_websocket(
            request.comfy_url, prompt_id,
            on_progress=lambda v: self._progress(
                on_progress, status=STATUS_GENERATING, progress=int(v)))

        # 7) 완료까지 폴링
        self._progress(on_progress, status=STATUS_GENERATING, progress=0,
                       message="이미지 생성 중...")
        image_path = self._transport.wait_for_result(
            prompt_id,
            interval=max(float(request.poll_interval_seconds or 1.0), 0.2),
            max_wait=int(request.max_wait_seconds or 600),
            should_stop=self._stop.is_set,
            on_progress=lambda v: self._progress(
                on_progress, status=STATUS_GENERATING, progress=int(v)),
        )
        if image_path is None:
            return self._cancelled(request, seed, started)

        return GenerationResult(
            status=STATUS_DONE,
            image_path=str(image_path),
            prompt=prompt,
            meta=f"{request.width}x{request.height}",
            elapsed=time.monotonic() - started,
            model=model_name,
            width=request.width,
            height=request.height,
            seed=seed,
            enhanced_prompt=prompt,
            snapshot=request.to_dict(),
            logs=list(self._logs),
        )


    # -- 프롬프트 ---------------------------------------------------------
    def _resolve_prompt(
        self,
        request: GenerationRequest,
        profile,
        on_progress: Optional[ProgressFn],
        log: Optional[LogFn],
    ) -> str:
        """최종 ComfyUI 로 보낼 프롬프트를 확정한다.

        입력창에 이미 프롬프트가 있고 스타일이 그대로면 LM Studio 호출을 건너뛴다.
        """
        prompt = request.prompt
        pre_existing = (request.enhanced_prompt or "").strip()

        saved_style = (request.zanime_style or "").strip().lower()
        current_style = (self.services.config.prompts.zanime_style or "").strip().lower()
        style_changed = bool(saved_style) and saved_style != current_style

        if pre_existing and not style_changed:
            self._emit_log("입력창에 이미 프롬프트가 있어 LM Studio 향상을 건너뜁니다.", log)
            return pre_existing

        if not self._lm_connected():
            self._emit_log("LM Studio 미연결로 프롬프트 강화 생략 (원본 사용)", log)
            return prompt

        self._progress(on_progress, status=STATUS_ENHANCING, progress=0,
                       message="LM Studio를 통해 프롬프트 향상 중...")
        if style_changed:
            self._emit_log(
                f"[ZANIME 스타일 변경] '{saved_style}' → '{current_style}' : "
                "프롬프트 향상을 새로 수행합니다.", log)
        else:
            self._emit_log("LM Studio를 통해 프롬프트 향상 중...", log)

        enhanced = self._enhance_prompt(request, profile, log)
        if enhanced:
            self._emit_log("LM Studio 프롬프트 강화 완료.", log)
            self._progress(on_progress, status=STATUS_ENHANCING, progress=0,
                           enhanced_prompt=enhanced)
            return enhanced

        self._emit_log("LM Studio 응답이 올바르지 않아 원본 프롬프트를 사용합니다.", log)
        return prompt

    def _enhance_prompt(
        self, request: GenerationRequest, profile, log: Optional[LogFn]
    ) -> Optional[str]:
        model = request.lm_model
        if not model or model == "로드된 모델 없음":
            self._emit_log("LM Studio 모델이 없어 원본 프롬프트를 사용합니다.", log)
            return None

        registry = self.services.model_registry
        use_korean = self.services.config.prompts.use_korean_prompt
        ext = load_external_prompts()

        system_prompt = select_system_prompt(
            comfy_model_name=request.comfy_model,
            is_flux=registry.is_flux(request.comfy_model),
            is_zimage=registry.is_zimage(request.comfy_model),
            is_ernie=registry.is_ernie(request.comfy_model),
            is_zanime=registry.is_zanime(request.comfy_model),
            zanime_style=self.services.config.prompts.zanime_style or "",
            use_korean=use_korean,
            ext_prompts=ext,
            log=lambda m: self._emit_log(m, log),
        )
        if not system_prompt:
            # json 매핑 문제로 해당 키가 안 읽히면 태그형 지시문으로 대체한다
            system_prompt = select_system_prompt(
                comfy_model_name=request.comfy_model,
                is_flux=False, is_zimage=False, is_ernie=False, is_zanime=False,
                use_korean=use_korean,
                ext_prompts=ext,
            )

        return enhance_prompt_sync(
            lm_url=request.lm_url,
            model=model,
            prompt=request.prompt,
            system_prompt=system_prompt,
            timeout=self.services.config.lmstudio.timeout_seconds,
        )

    def _lm_connected(self) -> bool:
        from app.features.connection.service import check_connection_silent
        try:
            url = self.services.config.lmstudio.url
            return bool(url) and check_connection_silent("lm", url, timeout=0.5)
        except Exception:
            return False

    # -- 기타 -------------------------------------------------------------
    def _build_filename_prefix(self, request: GenerationRequest) -> str:
        from datetime import datetime

        prefix = (request.filename_prefix
                  or self.services.config.output.filename_prefix
                  or "ComfyUI")
        now = datetime.now()
        output_dir = self.services.output_dir
        replacements = {
            "%date%": now.strftime("%Y%m%d"),
            "%time%": now.strftime("%H%M%S"),
            "%datetime%": now.strftime("%Y%m%d_%H%M%S"),
            "%counter%": f"{len(list(output_dir.glob('*.png'))) + 1:04d}",
        }
        for token, value in replacements.items():
            prefix = prefix.replace(token, value)
        return prefix

    def _cancelled(
        self, request: GenerationRequest, seed: int, started: float
    ) -> GenerationResult:
        return GenerationResult(
            status=STATUS_CANCELLED,
            prompt=request.prompt,
            model=request.comfy_model,
            width=request.width,
            height=request.height,
            seed=seed,
            snapshot=request.to_dict(),
            logs=list(self._logs),
            error="생성이 중단되었습니다.",
            elapsed=time.monotonic() - started,
        )

        return self._stop.is_set()
