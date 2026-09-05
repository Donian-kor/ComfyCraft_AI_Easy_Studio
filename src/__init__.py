"""ComfyUI + LM Studio Integration GUI - Source Package"""

from .config_manager import (
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

from .api_client import (
    BaseApiClient,
    LMStudioApiClient,
    ComfyUIApiClient,
    ComfyUIWebSocketClient,
)

from .workflow_manager import WorkflowManager, get_workflow_manager, reset_workflow_manager

from .model_fetcher import ModelFetcher, get_model_fetcher
from .model_registry import ModelRegistry, get_model_registry

# Section modules - use absolute imports since folder names start with numbers
import sys
from pathlib import Path

# Add project root to path for section module imports
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

# Import section modules using importlib to handle numeric folder names
import importlib.util

def _import_section_module(folder_name: str, module_name: str):
    """Import a module from a section folder (e.g., 01_Connection/connection.py)"""
    module_path = _PROJECT_ROOT / folder_name / f"{module_name}.py"
    if not module_path.exists():
        raise ImportError(f"Section module not found: {module_path}")
    module_name_full = f"section_{folder_name}_{module_name}"
    spec = importlib.util.spec_from_file_location(module_name_full, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[module_name_full] = module
    spec.loader.exec_module(module)
    return module

# Import all section modules
_connection_mod = _import_section_module("01_Connection", "connection")
_generation_mod = _import_section_module("02_Generation", "generation")
_prompt_mod = _import_section_module("03_Prompt", "prompt")
_result_mod = _import_section_module("04_Result", "result")
_execution_mod = _import_section_module("05_Execution", "execution")

# Export section module contents
# 01_Connection
ConnectionStatus = _connection_mod.ConnectionStatus
resolve_live_url = _connection_mod.resolve_live_url
check_connection_status = _connection_mod.check_connection_status
check_connection_silent = _connection_mod.check_connection_silent
get_default_comfyui_model_roots = _connection_mod.get_default_comfyui_model_roots
resolve_model_directory = _connection_mod.resolve_model_directory
scan_comfyui_model_names = _connection_mod.scan_comfyui_model_names

# 02_Generation
GenerationSettings = _generation_mod.GenerationSettings
build_generation_snapshot = _generation_mod.build_generation_snapshot
WorkerSignals = _generation_mod.WorkerSignals
GenerationWorker = _generation_mod.GenerationWorker

# 03_Prompt
normalize_prompt = _prompt_mod.normalize_prompt
prompt_character_count = _prompt_mod.prompt_character_count
build_negative_prompt = _prompt_mod.build_negative_prompt
load_external_prompts = _prompt_mod.load_external_prompts
SAMPLER_NAMES = _prompt_mod.SAMPLER_NAMES
SCHEDULER_NAMES = _prompt_mod.SCHEDULER_NAMES
sampler_label_to_value = _prompt_mod.sampler_label_to_value
sampler_value_to_label = _prompt_mod.sampler_value_to_label
enhance_prompt_sync = _prompt_mod.enhance_prompt_sync
PromptEnhanceWorker = _prompt_mod.PromptEnhanceWorker

# 04_Result
ResultInfo = _result_mod.ResultInfo
build_result_info = _result_mod.build_result_info
ensure_output_directory = _result_mod.ensure_output_directory
show_image = _result_mod.show_image
save_image_as = _result_mod.save_image_as
open_output_folder = _result_mod.open_output_folder
build_filename_prefix = _result_mod.build_filename_prefix
show_message_box = _result_mod.show_message_box

# 05_Execution
ExecutionStatus = _execution_mod.ExecutionStatus
create_execution_status = _execution_mod.create_execution_status
update_execution_status = _execution_mod.update_execution_status
format_elapsed = _execution_mod.format_elapsed
LoadingAnimation = _execution_mod.LoadingAnimation
ElapsedTimer = _execution_mod.ElapsedTimer

# 05_Execution
ExecutionStatus = _execution_mod.ExecutionStatus
create_execution_status = _execution_mod.create_execution_status
update_execution_status = _execution_mod.update_execution_status
format_elapsed = _execution_mod.format_elapsed
LoadingAnimation = _execution_mod.LoadingAnimation
ElapsedTimer = _execution_mod.ElapsedTimer

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