"""Application 계층: ComfyUI 전송 계층 (폴링/다운로드/큐 관리).

GenerationService 가 '무엇을 만들지' 결정한다면 이 모듈은
'서버와 어떻게 통신하는지' 만 담당한다.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Callable, Dict, Optional

import requests

from app.core.api_client import ComfyUIApiClient
from app.features.generation.comfy_errors import (
    extract_comfyui_error,
    is_execution_finished,
)

LogFn = Callable[[str], None]
ProgressFn = Callable[[int], None]


class ComfyTransport:
    """ComfyUI 큐 등록 이후의 폴링/다운로드를 담당한다."""

    def __init__(self, api: ComfyUIApiClient, output_dir: Path, *,
                 log: Optional[LogFn] = None) -> None:
        self._api = api
        self._output_dir = output_dir
        self._log = log or (lambda _m: None)
        self._ws = None

    # --- WebSocket 진행률 -------------------------------------------------
    def start_websocket(self, base_url: str, prompt_id: str, *,
                        on_progress: Optional[ProgressFn] = None) -> None:
        """진행률 스트림을 구독한다. 실패해도 HTTP 폴링이 이어지므로 무해하다."""
        from app.core.api_client import ComfyUIWebSocketClient

        try:
            self._ws = ComfyUIWebSocketClient(
                base_url,
                on_progress=(lambda v: on_progress(int(v))) if on_progress else None,
                on_status=lambda v: self._log(f"[소켓 상태] {v}"),
            )
            self._ws.set_prompt_id(prompt_id)
            self._ws.start()

            waited = 0
            while not getattr(self._ws, "_connected", False) and waited < 20:
                time.sleep(0.1)
                waited += 1

            if getattr(self._ws, "_connected", False):
                self._log("ComfyUI WebSocket 연결 성공!")
            else:
                self._log("[⚠️ 경고] WebSocket 연결 지연 - HTTP 폴링으로 진행률을 대체합니다.")
        except Exception as exc:
            self._log(f"WebSocket 초기화 실패: {exc}")
            self._ws = None

    @property
    def last_ws_progress(self) -> float:
        return float(getattr(self._ws, "_last_progress", 0) or 0) if self._ws else 0.0

    def close(self) -> None:
        if self._ws is not None:
            try:
                self._ws.close()
            except Exception:
                pass
            self._ws = None

    # --- 큐 정리 ----------------------------------------------------------
    def prepare_queue(self, model_name: str, last_model: Optional[str]) -> Optional[str]:
        """생성 전 큐를 정리하고, 유지할 모델명을 돌려준다.

        같은 모델이면 free_memory 를 건너뛴다(불필요한 재적재 방지).
        """
        try:
            self._api.interrupt(timeout=2)
            self._api.clear_queue(timeout=2)
            if last_model != model_name:
                self._api.free_memory(timeout=3)
                self._log("사전 큐 정리 완료 (interrupt + clear_queue + free_memory)")
                return model_name
            self._log(f"동일 모델({model_name}) 유지 — free_memory 건너뜀")
            return last_model
        except Exception as exc:
            self._log(f"[⚠️ 경고] 사전 큐 정리 중 오류 (무시하고 진행): {exc}")
            return last_model

    def clear_queue(self) -> None:
        try:
            self._api.clear_queue(timeout=2)
            self._log("ComfyUI 큐 정리 완료")
        except Exception as exc:
            self._log(f"[⚠️ 경고] 큐 정리 실패: {exc}")

    def interrupt(self) -> None:
        """생성 중단 시 큐를 강제 정리한다."""
        try:
            self._api.interrupt(timeout=2)
        except Exception:
            pass

    # --- 조회 -------------------------------------------------------------
    def node_exists(self, node_name: str) -> bool:
        """ComfyUI 서버에 이 노드 타입이 설치돼 있는지 확인한다."""
        try:
            response = self._api.get_object_info(node_name, timeout=(0.5, 1.0))
            if response.status_code != 200:
                return False
            payload = response.json()
            return isinstance(payload, dict) and node_name in payload
        except Exception:
            return False

    def find_sam_model_name(self, preferred: str = "sam_vit_b_01ec64.pth") -> Optional[str]:
        """SAMLoader 가 쓸 SAM 모델 파일명을 서버에서 조회한다."""
        try:
            response = self._api.get_object_info("SAMLoader", timeout=(0.5, 1.0))
            if response.status_code != 200:
                return None
            payload = response.json().get("SAMLoader", {})
            required = (payload.get("input", {}).get("required", {})
                        if isinstance(payload, dict) else {})
            spec = required.get("model_name")
            if not (isinstance(spec, list) and spec and isinstance(spec[0], list)):
                return None
            candidates = [str(n) for n in spec[0] if n]
            if not candidates:
                return None
            return preferred if preferred in candidates else candidates[0]
        except Exception:
            return None

    def download_first_image(self, history_item: Dict[str, Any]) -> Optional[Path]:
        """history 항목의 첫 이미지를 출력 폴더로 내려받는다."""
        for output in history_item.get("outputs", {}).values():
            images = output.get("images", [])
            if not images:
                continue
            image = images[0]
            response = self._api.view({
                "filename": image.get("filename", "output.png"),
                "subfolder": image.get("subfolder", ""),
                "type": image.get("type", "output"),
            }, timeout=30)
            response.raise_for_status()
            self._output_dir.mkdir(parents=True, exist_ok=True)
            destination = self._output_dir / Path(image.get("filename", "output.png")).name
            destination.write_bytes(response.content)
            return destination
        return None

    def wait_for_result(self, prompt_id: str, *, interval: float, max_wait: int,
                        should_stop: Callable[[], bool],
                        on_progress: Optional[ProgressFn] = None) -> Optional[Path]:
        """완료될 때까지 history 를 폴링하고 결과 경로를 돌려준다.

        이미지가 없는데 작업이 종료됐다면 즉시 실패시키고,
        max_wait 까지 오면 RuntimeError 를 던진다.
        중단 신호가 오면 None 을 돌려준다.
        """
        attempts = max(1, int(max_wait / interval))
        last_progress = 0.0
        model_loading_logged = False
        poll_error_logged = False

        for attempt in range(attempts):
            if should_stop():
                return None

            try:
                history = self._api.history(prompt_id, timeout=5)
            except requests.RequestException as exc:
                if not poll_error_logged:
                    self._log("[경고] ComfyUI 상태 조회가 일시적으로 실패했습니다. "
                              f"재시도합니다: {exc}")
                    poll_error_logged = True
                time.sleep(interval)
                continue

            if poll_error_logged:
                self._log("ComfyUI 상태 조회가 복구되었습니다.")
                poll_error_logged = False

            if history.status_code == 200:
                item = (history.json() or {}).get(prompt_id)
                if item:
                    comfy_error = extract_comfyui_error(item)
                    if comfy_error:
                        raise RuntimeError(f"ComfyUI 작업 실패: {comfy_error}")

                    result_path = self.download_first_image(item)
                    if result_path:
                        if on_progress is not None:
                            on_progress(100)
                        self._log(f"이미지 다운로드 완료: {result_path}")
                        self.clear_queue()
                        return result_path

                    if is_execution_finished(item):
                        outputs = item.get("outputs", {})
                        detail = (f"{len(outputs)}개 노드 결과가 있습니다"
                                  if outputs else "결과물이 비어 있습니다")
                        raise RuntimeError(
                            "ComfyUI 작업이 끝났지만 저장된 이미지가 없습니다 "
                            f"({detail}). 워크플로우의 SaveImage 노드를 확인해 주세요.")

            current = self.last_ws_progress
            if current and current > last_progress:
                last_progress = current
                model_loading_logged = False
                if on_progress is not None:
                    on_progress(int(last_progress))

            if last_progress == 0 and not model_loading_logged:
                elapsed = attempt * interval
                if elapsed >= 30:
                    self._log("[모델 로딩 중] 대용량 모델 초기화 대기... "
                              f"({elapsed:.0f}초 경과, 최대 {max_wait}초 대기)")
                    model_loading_logged = True

            time.sleep(interval)

        raise RuntimeError(f"이미지 생성 시간이 초과되었습니다. (최대 {max_wait}초 대기)")
