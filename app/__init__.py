"""ComfyUI + LM Studio Integration GUI — App Package.

주의: 이 모듈은 더 이상 하위 모듈을 일괄 import 하지 않는다.

예전에는 여기서 app.sections / app.gui 를 그대로 import 했고, 그 결과
`import app.core.config_manager` 만 해도 PySide6 가 함께 로드되었다.
Flet 전환(REFACTOR_PLAN_FLET.md Phase 12)으로 UI 프레임워크를 제거하면서
그 의존성까지 끊으려 한다.

그래서 외부 호환을 위해 남겨둔 이름들만 __getattr__ 로 지연 노출한다.
접근하는 순간에만 해당 모듈이 import 되므로, 실제로 쓰지 않는
PySide6 경로는 아예 로드되지 않는다.
"""

from __future__ import annotations

from typing import Any

__version__ = "0.4.0"

# 이름 → (모듈 경로, 실제 이름)
_LEGACY_EXPORTS: dict[str, tuple[str, str]] = {
    # Config Manager
    "get_config_manager": ("app.core.config_manager", "get_config_manager"),
    "ConfigManager": ("app.core.config_manager", "ConfigManager"),
    "AppConfig": ("app.core.config_manager", "AppConfig"),
    "LMStudioConfig": ("app.core.config_manager", "LMStudioConfig"),
    "ComfyUIConfig": ("app.core.config_manager", "ComfyUIConfig"),
    "GenerationConfig": ("app.core.config_manager", "GenerationConfig"),
    "PromptsConfig": ("app.core.config_manager", "PromptsConfig"),
    "WorkflowConfig": ("app.core.config_manager", "WorkflowConfig"),
    "OutputConfig": ("app.core.config_manager", "OutputConfig"),
    "ThemeConfig": ("app.core.config_manager", "ThemeConfig"),
    "UIConfig": ("app.core.config_manager", "UIConfig"),
    "CacheConfig": ("app.core.config_manager", "CacheConfig"),
    "ModelPresetConfig": ("app.core.config_manager", "ModelPresetConfig"),
    # API Clients
    "BaseApiClient": ("app.core.api_client", "BaseApiClient"),
    "LMStudioApiClient": ("app.core.api_client", "LMStudioApiClient"),
    "ComfyUIApiClient": ("app.core.api_client", "ComfyUIApiClient"),
    "ComfyUIWebSocketClient": ("app.core.api_client", "ComfyUIWebSocketClient"),
    # Managers
    "WorkflowManager": ("app.core.workflow_manager", "WorkflowManager"),
    "get_workflow_manager": ("app.core.workflow_manager", "get_workflow_manager"),
    "reset_workflow_manager": ("app.core.workflow_manager", "reset_workflow_manager"),
    "ModelFetcher": ("app.core.model_fetcher", "ModelFetcher"),
    "get_model_fetcher": ("app.core.model_fetcher", "get_model_fetcher"),
    "ModelRegistry": ("app.core.model_registry", "ModelRegistry"),
    "get_model_registry": ("app.core.model_registry", "get_model_registry"),
    # Connection (Feature 계층)
    "ConnectionStatus": ("app.features.connection.service", "ConnectionStatus"),
    "resolve_live_url": ("app.features.connection.service", "resolve_live_url"),
    "check_connection_status": ("app.features.connection.service", "check_connection_status"),
    "check_connection_silent": ("app.features.connection.service", "check_connection_silent"),
    "get_default_comfyui_model_roots": (
        "app.features.connection.service", "get_default_comfyui_model_roots"),
    "resolve_model_directory": ("app.features.connection.service", "resolve_model_directory"),
    "scan_comfyui_model_names": ("app.features.connection.service", "scan_comfyui_model_names"),
    # Prompt (Feature 계층)
    "normalize_prompt": ("app.features.prompt.prompts", "normalize_prompt"),
    "prompt_character_count": ("app.features.prompt.prompts", "prompt_character_count"),
    "enforce_prompt_character_limit": (
        "app.features.prompt.prompts", "enforce_prompt_character_limit"),
    "build_negative_prompt": ("app.features.prompt.prompts", "build_negative_prompt"),
    "load_external_prompts": ("app.features.prompt.prompts", "load_external_prompts"),
    "SAMPLER_NAMES": ("app.features.prompt.prompts", "SAMPLER_NAMES"),
    "SCHEDULER_NAMES": ("app.features.prompt.prompts", "SCHEDULER_NAMES"),
    "sampler_label_to_value": ("app.features.prompt.prompts", "sampler_label_to_value"),
    "sampler_value_to_label": ("app.features.prompt.prompts", "sampler_value_to_label"),
    "enhance_prompt_sync": ("app.features.prompt.prompts", "enhance_prompt_sync"),
    # Session (Feature 계층)
    "SessionManager": ("app.features.session.store", "SessionManager"),
}


def __getattr__(name: str) -> Any:
    """호환 재수출 이름을 필요할 때만 import 한다 (PEP 562)."""
    target = _LEGACY_EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module 'app' has no attribute {name!r}")

    from importlib import import_module

    module_name, attribute = target
    value = getattr(import_module(module_name), attribute)
    globals()[name] = value          # 두 번째 접근부터는 캐시 사용
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_LEGACY_EXPORTS))
