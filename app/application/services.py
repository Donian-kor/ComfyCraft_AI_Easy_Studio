"""애플리케이션 서비스 컨테이너.

Core/Feature 계층의 싱글턴들을 한 곳에 모아 UI 에 주입한다.
UI(Flet)는 이 컨테이너만 알고 있으면 되고, Controller 를 직접 만들지 않는다.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from app.core.api_client import ComfyUIApiClient, LMStudioApiClient
from app.core.config_manager import ConfigManager, get_config_manager
from app.core.model_fetcher import ModelFetcher, get_model_fetcher
from app.core.model_registry import ModelRegistry, get_model_registry
from app.core.workflow_manager import WorkflowManager, get_workflow_manager
from app.features.session.store import SessionManager
from app.paths import BASE_DIR
from app.application.internal_transport import InternalTransport


@dataclass
class AppServices:
    """UI 가 사용할 모든 서비스의 진입점."""

    config_manager: ConfigManager
    model_registry: ModelRegistry
    model_fetcher: ModelFetcher
    workflow_manager: WorkflowManager
    session_manager: SessionManager

    @property
    def config(self):
        return self.config_manager.get()

    @property
    def output_dir(self) -> Path:
        """이미지 출력 폴더. 설정의 directory 값을 따른다."""
        raw = self.config.output.directory or "outputs"
        path = Path(raw)
        if not path.is_absolute():
            path = BASE_DIR / path
        return path

    def internal_transport(self) -> InternalTransport:
        """내부 생성 엔진(ComfyUI 없이 직접 생성)을 위한 전송 계층."""
        return InternalTransport(self.output_dir)

    def comfy_client(self, url: Optional[str] = None, max_retries: int = 0) -> ComfyUIApiClient:
        """ComfyUI 클라이언트.

        기본 재시도 0회: 연결 실패는 대체로 "서버가 안 떠 있는 상태"이고,
        requests 의 기본 재시도+백오프가 11초나 붙잡고 있어서 사용자가
        버튼을 눌렀는데 아무 반응이 없는 것처럼 보인다. 상태 조회 폴링은
        호출 측에서 자체 재시도하므로 여기서는 한 번만 시도한다.
        """
        return ComfyUIApiClient(url or self.config.comfyui.url, max_retries=max_retries)

    def lm_client(self, url: Optional[str] = None, max_retries: int = 0) -> LMStudioApiClient:
        """LM Studio 클라이언트. ComfyUI 와 같은 이유로 기본 재시도 0회."""
        return LMStudioApiClient(url or self.config.lmstudio.url)

    # --- 연결 상태 -------------------------------------------------------
    def check_comfy(self, url: Optional[str] = None):
        from app.features.connection.service import check_connection_status
        return check_connection_status("comfy", url or self.config.comfyui.url)

    def check_lm(self, url: Optional[str] = None):
        from app.features.connection.service import check_connection_status
        return check_connection_status("lm", url or self.config.lmstudio.url)


def build_services() -> AppServices:
    """기본 경로로 서비스 컨테이너를 만든다."""
    config_manager = get_config_manager()
    return AppServices(
        config_manager=config_manager,
        model_registry=get_model_registry(),
        model_fetcher=get_model_fetcher(),
        workflow_manager=get_workflow_manager(),
        session_manager=SessionManager(BASE_DIR / "outputs" / ".sessions"),
    )
