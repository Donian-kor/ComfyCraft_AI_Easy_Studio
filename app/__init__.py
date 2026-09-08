"""ComfyUI + LM Studio Integration GUI - App Package"""

from .core.config_manager import (
    get_config_manager,
    ConfigManager,
    AppConfig,
    LMStudioConfig,
    ComfyUIConfig,
    GenerationConfig,
    PromptsConfig,
    WorkflowConfig,
    OutputConfig,
    ThemeConfig,
    UIConfig,
    CacheConfig,
    ModelPresetConfig,
)

from .core.api_client import (
    BaseApiClient,
    LMStudioApiClient,
    ComfyUIApiClient,
    ComfyUIWebSocketClient,
)

from .core.workflow_manager import WorkflowManager, get_workflow_manager, reset_workflow_manager

from .core.model_fetcher import ModelFetcher, get_model_fetcher
from .core.model_registry import ModelRegistry, get_model_registry

# Section modules
from .sections.connection import (
    ConnectionStatus,
    resolve_live_url,
    check_connection_status,
    check_connection_silent,
    get_default_comfyui_model_roots,
    resolve_model_directory,
    scan_comfyui_model_names,
)

from .sections.generation import (
    GenerationSettings,
    build_generation_snapshot,
    WorkerSignals,
    GenerationWorker,
)

from .sections.prompt import (
    normalize_prompt,
    prompt_character_count,
    build_negative_prompt,
    load_external_prompts,
    SAMPLER_NAMES,
    SCHEDULER_NAMES,
    sampler_label_to_value,
    sampler_value_to_label,
    enhance_prompt_sync,
    PromptEnhanceWorker,
)

from .sections.result import (
    ResultInfo,
    build_result_info,
    ensure_output_directory,
    show_image,
    save_image_as,
    open_output_folder,
    build_filename_prefix,
    show_message_box,
)

from .sections.execution import (
    ExecutionStatus,
    create_execution_status,
    update_execution_status,
    format_elapsed,
    LoadingAnimation,
    ElapsedTimer,
)

__version__ = "0.2.0"

__all__ = [
    # Config Manager
    "get_config_manager",
    "ConfigManager",
    "AppConfig",
    "LMStudioConfig",
    "ComfyUIConfig",
    "GenerationConfig",
    "PromptsConfig",
    "WorkflowConfig",
    "OutputConfig",
    "ThemeConfig",
    "UIConfig",
    "CacheConfig",
    "ModelPresetConfig",
    # API Clients
    "BaseApiClient",
    "LMStudioApiClient",
    "ComfyUIApiClient",
    "ComfyUIWebSocketClient",
    # Managers
    "WorkflowManager",
    "get_workflow_manager",
    "reset_workflow_manager",
    "ModelFetcher",
    "get_model_fetcher",
    "ModelRegistry",
    "get_model_registry",
    # 01_Connection
    "ConnectionStatus",
    "resolve_live_url",
    "check_connection_status",
    "check_connection_silent",
    "get_default_comfyui_model_roots",
    "resolve_model_directory",
    "scan_comfyui_model_names",
    # 02_Generation
    "GenerationSettings",
    "build_generation_snapshot",
    "WorkerSignals",
    "GenerationWorker",
    # 03_Prompt
    "normalize_prompt",
    "prompt_character_count",
    "build_negative_prompt",
    "load_external_prompts",
    "SAMPLER_NAMES",
    "SCHEDULER_NAMES",
    "sampler_label_to_value",
    "sampler_value_to_label",
    "enhance_prompt_sync",
    "PromptEnhanceWorker",
    # 04_Result
    "ResultInfo",
    "build_result_info",
    "ensure_output_directory",
    "show_image",
    "save_image_as",
    "open_output_folder",
    "build_filename_prefix",
    "show_message_box",
    # 05_Execution
    "ExecutionStatus",
    "create_execution_status",
    "update_execution_status",
    "format_elapsed",
    "LoadingAnimation",
    "ElapsedTimer",
]