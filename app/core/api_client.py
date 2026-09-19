"""Thin client wrappers for LM Studio and ComfyUI HTTP/WebSocket APIs."""

from __future__ import annotations

import json
import threading
import time
from typing import Any, Callable, Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

try:
    import websocket
except ImportError:  # pragma: no cover
    websocket = None


class BaseApiClient:
    """Common HTTP helper for server API access with automatic retry logic."""

    def __init__(self, base_url: str, max_retries: int = 3):
        self.base_url = base_url.rstrip('/')
        self.max_retries = max_retries
        self.session = self._create_session(max_retries)

    def _create_session(self, max_retries: int) -> requests.Session:
        """Create a requests session with automatic retry logic."""
        session = requests.Session()
        
        # Configure retry strategy
        # Pylance가 urllib3 버전을 잘못 인식해서 생기는 오탐지 회피용:
        # 옵션은 생성자 키워드로 넣지 않고, 만든 뒤 직접 넣어줍니다.
        retry_strategy = Retry()
        retry_strategy.total = max_retries
        retry_strategy.backoff_factor = 0.5
        retry_strategy.status_forcelist = [429, 500, 502, 503, 504]
        retry_strategy.allowed_methods = ["GET", "POST", "HEAD"]
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session

    def build_url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path: str, timeout: Any = 10, **kwargs) -> requests.Response:
        return self.session.get(self.build_url(path), timeout=timeout, **kwargs)

    def post(self, path: str, *, json: Optional[Dict[str, Any]] = None, timeout: Any = 10, **kwargs) -> requests.Response:
        return self.session.post(self.build_url(path), json=json, timeout=timeout, **kwargs)


class LMStudioApiClient(BaseApiClient):
    def __init__(self, base_url: str):
        super().__init__(base_url)

    def get_models(self, timeout: Any = (0.5, 1.0)) -> requests.Response:
        return self.get('/v1/models', timeout=timeout)

    def chat_completion(self, payload: Dict[str, Any], timeout: Any = 30) -> requests.Response:
        return self.post('/v1/chat/completions', json=payload, timeout=timeout)


class ComfyUIApiClient(BaseApiClient):
    def __init__(self, base_url: str):
        super().__init__(base_url)

    def get_system_stats(self, timeout: Any = (0.5, 0.8)) -> requests.Response:
        return self.get('/system_stats', timeout=timeout)

    def interrupt(self, timeout: Any = 2) -> requests.Response:
        return self.post('/interrupt', timeout=timeout)

    def clear_queue(self, timeout: Any = 2) -> requests.Response:
        return self.post('/queue', json={"clear": True}, timeout=timeout)

    def free_memory(self, timeout: Any = 3) -> requests.Response:
        return self.post('/free', json={"unload_models": True, "free_memory": True}, timeout=timeout)

    def prompt(self, workflow: Dict[str, Any], timeout: Any = 30) -> requests.Response:
        return self.post('/prompt', json={"prompt": workflow}, timeout=timeout)

    def history(self, prompt_id: str, timeout: Any = 5) -> requests.Response:
        return self.get(f'/history/{prompt_id}', timeout=timeout)

    def get_object_info(self, node_name: str, timeout: Any = (0.5, 1.0)) -> requests.Response:
        return self.get(f'/object_info/{node_name}', timeout=timeout)

    def view(self, params: Dict[str, Any], timeout: Any = 30) -> requests.Response:
        return requests.get(self.build_url('/view'), params=params, timeout=timeout)


class ComfyUIWebSocketClient:
    """Wrap ComfyUI websocket events for real-time progress updates."""

    def __init__(self, base_url: str, on_progress: Optional[Callable[[float], None]] = None, on_status: Optional[Callable[[Dict[str, Any]], None]] = None):
        self.base_url = base_url.rstrip('/')
        self.client_id = self._generate_client_id()
        self.ws_url = self._to_ws_url(self.base_url, self.client_id)
        self.on_progress = on_progress
        self.on_status = on_status
        self.active_prompt_id: Optional[str] = None
        self.ws_app = None
        self.lock = threading.Lock()
        self._connected = False
        self._last_progress = 0.0  # 🌟 마지막 수신 진행률 저장 (폴링 루프에서 참조용)

    @staticmethod
    def _generate_client_id() -> str:
        import uuid
        return uuid.uuid4().hex

    # 👍 [Source 7번 파일 - 수정 후]
    @staticmethod
    def _to_ws_url(base_url: str, client_id: Optional[str] = None) -> str:
        url = base_url.strip()
        
        # http:// 나 https:// 가 없는 경우 붙여서 처리
        if not url.startswith(("http://", "https://", "ws://", "wss://")):
            url = "http://" + url
            
        if url.startswith('https://'):
            ws_base = 'wss://' + url[len('https://'):]
        elif url.startswith('http://'):
            ws_base = 'ws://' + url[len('http://'):]
        else:
            ws_base = url

        # 🌟 ComfyUI WebSocket 엔드포인트는 보통 /ws 경로를 사용
        # 이미 경로가 있는 경우(예: /api)엔 추가하지 않음
        from urllib.parse import urlparse
        parsed = urlparse(ws_base)
        if not parsed.path or parsed.path == '/':
            ws_base = ws_base.rstrip('/') + '/ws'

        if client_id:
            separator = '&' if '?' in ws_base else '?'
            return f"{ws_base}{separator}clientId={client_id}"
        return ws_base


    @staticmethod
    def parse_progress_payload(payload: Dict[str, Any]) -> Optional[float]:
        if not isinstance(payload, dict):
            return None

        data = payload.get('data', {})
        if not isinstance(data, dict):
            return None

        value = data.get('value')
        max_value = data.get('max')
        if value is None and isinstance(data.get('status'), dict):
            status = data.get('status', {})
            if isinstance(status.get('progress'), (int, float)):
                value = status['progress']
            if isinstance(status.get('max'), (int, float)):
                max_value = status['max']

        if value is None:
            return None

        try:
            value = float(value)
            max_value = float(max_value or 0)
        except (TypeError, ValueError):
            return None

        if max_value <= 0:
            return 0.0

        percent = (value / max_value) * 100.0
        return max(0.0, min(100.0, percent))

    @staticmethod
    def parse_status_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(payload, dict):
            return {}

        def _coerce_number(value: Any) -> Optional[int]:
            if isinstance(value, bool):
                return None
            if isinstance(value, (int, float)):
                return int(value)
            if isinstance(value, str):
                try:
                    return int(float(value))
                except ValueError:
                    return None
            return None

        def _extract_node(node: Any, keys: tuple[str, ...]) -> Optional[Any]:
            if not isinstance(node, dict):
                return None
            for key in keys:
                if key in node:
                    return node[key]
            return None

        def _walk(node: Any, seen: set[int]):
            if isinstance(node, dict):
                oid = id(node)
                if oid in seen:
                    return
                seen.add(oid)
                for key, value in node.items():
                    if key in {'step', 'current_step', 'current', 'progress', 'value'} and value is not None:
                        parsed = _coerce_number(value)
                        if parsed is not None:
                            result['step'] = parsed
                    if key in {'max', 'total_steps', 'total', 'steps'} and value is not None:
                        parsed = _coerce_number(value)
                        if parsed is not None:
                            result['total_steps'] = parsed
                    if key in {'eta', 'estimated_time', 'remaining_time'} and value is not None:
                        result.setdefault('eta', value)
                    if key in {'queue_remaining', 'queue_size', 'queue', 'remaining'} and value is not None:
                        result.setdefault('queue', value)
                    _walk(value, seen)

        result: Dict[str, Any] = {}
        data = payload.get('data', {})
        if not isinstance(data, dict):
            return result

        _walk(data, set())

        if 'step' in result and 'total_steps' in result and result['total_steps'] <= 0:
            result.pop('total_steps')

        if 'step' in result and 'total_steps' in result and result['step'] > result['total_steps']:
            result['step'] = result['total_steps']

        return result

    def set_prompt_id(self, prompt_id: Optional[str]) -> None:
        self.active_prompt_id = prompt_id

    def start(self) -> None:
        if websocket is None:
            raise RuntimeError('websocket-client 패키지가 설치되지 않았습니다. requirements에 websocket-client를 추가하세요.')
        if self.ws_app is not None and self._connected:
            return

        # 👍 [Source 7번 파일 - ComfyUIWebSocketClient 내 on_message 함수 교체]
        def on_message(_, message: str) -> None:
            try:
                # 문자열 데이터가 아니면 파싱 생략
                if not isinstance(message, str):
                    return
                payload = json.loads(message)
            except Exception:
                return

            if not isinstance(payload, dict):
                return

            msg_type = str(payload.get('type', '')).lower()
            data = payload.get('data', {}) if isinstance(payload.get('data'), dict) else {}
            
            # prompt_id 검증
            prompt_id = data.get('prompt_id')
            if self.active_prompt_id and prompt_id and prompt_id != self.active_prompt_id:
                return

            # ⭐ [수정 핵심] ComfyUI의 실제 progress 표준 패킷 구조를 완벽하게 강제 수집합니다.
            percent = None
            
            # 형태 1: 표준 progress 타입인 경우 (data: {value: 12, max: 20})
            if msg_type == 'progress' or 'progress' in msg_type:
                current_val = data.get('value')
                max_val = data.get('max')
                if current_val is not None and max_val is not None and float(max_val) > 0:
                    percent = (float(current_val) / float(max_val)) * 100.0
            
            # 형태 2: KSampler 내부 세부 스텝 진행률 데이터 역추적 (data: {step: 5, max: 20})
            elif 'step' in data and ('max' in data or 'total' in data or 'steps' in data):
                current_step = data.get('step', 0)
                total_steps = data.get('max') or data.get('total') or data.get('steps', 0)
                if current_step is not None and total_steps is not None and float(total_steps) > 0:
                    percent = (float(current_step) / float(total_steps)) * 100.0

            # 파싱 성공 시 진행률 시그널 송출 (0~100 사이 제한)
            if percent is not None and self.on_progress is not None:
                final_percent = max(0.0, min(100.0, float(percent)))
                self._last_progress = final_percent  # 🌟 진행률 저장 (폴링 루프에서 참조)
                self.on_progress(final_percent)
                return

            # 기존 상태 로그 수집 파트 유지
            status_like = any(key in str(payload).lower() for key in ('step', 'eta', 'queue', 'total_steps', 'exec_info'))
            if self.on_status is not None and (msg_type in {'status', 'executing', 'execution_start'} or status_like):
                status_data = self.parse_status_payload(payload)
                if status_data:
                    self.on_status(status_data)


        def on_open(_) -> None:
            self._connected = True

        def on_close(_, __, ___) -> None:
            self._connected = False

        def on_error(_, error: Exception) -> None:
            self._connected = False
            self.emit_log(f"[WebSocket 에러] {error}")  # 🌟 에러 로깅 추가
            self.ws_app = None

        self.ws_app = websocket.WebSocketApp(
            self.ws_url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
        )
        self.thread = threading.Thread(target=self.ws_app.run_forever, kwargs={"ping_interval": 20, "ping_timeout": 10}, daemon=True)
        self.thread.start()

    def close(self) -> None:
        """WebSocket 연결을 안전하게 종료합니다."""
        try:
            if self.ws_app is not None:
                # WebSocket 연결 종료 요청
                self.ws_app.close()
        except Exception:
            pass
        
        # 스레드 종료 대기 (최대 2초)
        if hasattr(self, 'thread') and self.thread is not None and self.thread.is_alive():
            self.thread.join(timeout=2.0)
        
        self.ws_app = None
        self.thread = None
        self._connected = False

    def __del__(self):
        """소멸자에서 정리 보장"""
        try:
            self.close()
        except Exception:
            pass
