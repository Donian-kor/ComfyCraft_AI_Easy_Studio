"""
Configuration Manager for ComfyUI + LMStudio Integration GUI
설정 파일 로드, 저장, 검증, 기본값 관리를 담당하는 클래스
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass, field

# 프롬프트 로더 (prompt.json에서 시스템 프롬프트 등 로드)
from app.sections.prompt import load_external_prompts


@dataclass
class LMStudioConfig:
    url: str = "http://127.0.0.1:1234"
    model: str = ""
    timeout_seconds: int = 30
    enhance_temperature: float = 0.7
    enhance_max_tokens: int = 5000


@dataclass
class ComfyUIConfig:
    url: str = "http://127.0.0.1:8188"
    model: str = ""
    timeout_seconds: int = 10
    poll_interval_seconds: int = 1
    max_wait_seconds: int = 600


@dataclass
class GenerationConfig:
    default_width: int = 1024
    default_height: int = 1024
    default_steps: int = 20
    default_cfg: float = 7.0
    default_seed: int = -1
    width_min: int = 256
    width_max: int = 2048
    height_min: int = 256
    height_max: int = 2048
    steps_min: int = 1
    steps_max: int = 100
    cfg_min: float = 1.0
    cfg_max: float = 30.0
    width_increment: int = 64
    height_increment: int = 64
    cfg_increment: float = 0.5


@dataclass
class WorkflowConfig:
    checkpoint_template: str = "workflows/checkpoint.json"
    gguf_template: str = "workflows/gguf_unet.json"
    flux_gguf_template: str = "workflows/flux_gguf.json"
    zimage_template: str = "workflows/zimage.json"
    sampler_name: str = "euler"
    scheduler: str = "normal"
    denoise: float = 1.0
    use_facedetailer: bool = False


@dataclass
class OutputConfig:
    directory: str = "outputs"
    filename_prefix: str = "ComfyUI_%date%"


@dataclass
class ThemeConfig:
    bg_color: str = "#0f172a"
    fg_color: str = "#e2e8f0"
    accent_color: str = "#38bdf8"
    panel_color: str = "#111827"
    surface_color: str = "#1f2937"
    border_color: str = "#334155"
    success_color: str = "#34d399"
    warning_color: str = "#fbbf24"
    error_color: str = "#f87171"


@dataclass
class UIConfig:
    window_width: int = 960
    window_height: int = 780
    window_min_width: int = 840
    window_min_height: int = 640
    startup_window_width: int = 540
    startup_window_height: int = 360
    font_family: str = "NanumGothic"
    font_fallback: str = "Arial"
    font_size: int = 11
    theme: ThemeConfig = field(default_factory=ThemeConfig)
    resolution_presets: list = field(default_factory=list)


@dataclass
class CacheConfig:
    model_cache_ttl_seconds: float = 10.0


@dataclass
class ModelPresetConfig:
    type: str = "flux_gguf"
    clip1: str = ""
    clip2: str = ""
    vae: str = ""
    default_steps: int = 29
    default_cfg: float = 1.0
    sampler_name: str = "euler"
    scheduler: str = "simple"


@dataclass
class PromptsConfig:
    # 프롬프트 설정은 prompt.json에서 로드됨 (load_external_prompts 사용)
    system_prompt_flux_en: str = ""
    system_prompt_flux_kr: str = ""
    system_prompt_ernie_en: str = ""
    system_prompt_ernie_kr: str = ""
    system_prompt_sdxl_en: str = ""
    system_prompt_sdxl_kr: str = ""
    system_prompt_zanime_webtoon_en: str = ""
    system_prompt_zanime_webtoon_kr: str = ""
    system_prompt_zanime_anime_en: str = ""
    system_prompt_zanime_anime_kr: str = ""
    system_prompt_zanime_basic_en: str = ""
    system_prompt_zanime_basic_kr: str = ""
    negative_default: str = ""
    use_korean_prompt: bool = False
    zanime_style: str = ""


@dataclass
class AppConfig:
    lmstudio: LMStudioConfig = field(default_factory=LMStudioConfig)
    comfyui: ComfyUIConfig = field(default_factory=ComfyUIConfig)
    generation: GenerationConfig = field(default_factory=GenerationConfig)
    prompts: PromptsConfig = field(default_factory=PromptsConfig)
    workflow: WorkflowConfig = field(default_factory=WorkflowConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    comfyui_model_paths: list = field(default_factory=list)
    model_presets: dict = field(default_factory=dict)


class ConfigManager:
    """설정 관리 클래스 - JSON 파일 기반 설정 로드/저장/검증"""

    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    DEFAULT_CONFIG_PATH = ROOT_DIR / "workflows" / "app_config.json"

    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        if config_path is None:
            resolved_path = self.DEFAULT_CONFIG_PATH
        else:
            resolved_path = Path(config_path)

        self.config_path = resolved_path
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self._config: Optional[AppConfig] = None
        self._raw_config: Dict[str, Any] = {}
    
    def load(self) -> AppConfig:
        """설정 파일 로드, 없으면 기본값으로 생성"""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self._raw_config = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                print(f"[ConfigManager] 설정 파일 읽기 실패, 기본값 사용: {e}")
                self._raw_config = {}
        else:
            self._raw_config = {}
        
        self._config = self._parse_config(self._raw_config)
        return self._config
    
    def _parse_config(self, raw: Dict[str, Any]) -> AppConfig:
        """원시 딕셔너리를 데이터클래스 구조로 파싱"""
        # LMStudio 설정
        lm_raw = raw.get("lmstudio", {})
        lmstudio = LMStudioConfig(
            url=lm_raw.get("url", LMStudioConfig.url),
            model=lm_raw.get("model", ""),
            timeout_seconds=lm_raw.get("timeout_seconds", 30),
            enhance_temperature=lm_raw.get("enhance_temperature", 0.7),
            enhance_max_tokens=lm_raw.get("enhance_max_tokens", 5000),
        )
        
        # ComfyUI 설정
        comfy_raw = raw.get("comfyui", {})
        comfyui = ComfyUIConfig(
            url=comfy_raw.get("url", ComfyUIConfig.url),
            model=comfy_raw.get("model", ""),
            timeout_seconds=comfy_raw.get("timeout_seconds", 10),
            poll_interval_seconds=comfy_raw.get("poll_interval_seconds", 1),
            max_wait_seconds=comfy_raw.get("max_wait_seconds", 600),
        )
        
        # 생성 설정
        gen_raw = raw.get("generation", {})
        generation = GenerationConfig(
            default_width=gen_raw.get("default_width", 1024),
            default_height=gen_raw.get("default_height", 1024),
            default_steps=gen_raw.get("default_steps", 20),
            default_cfg=gen_raw.get("default_cfg", 7.0),
            default_seed=gen_raw.get("default_seed", -1),
            width_min=gen_raw.get("width_min", 256),
            width_max=gen_raw.get("width_max", 2048),
            height_min=gen_raw.get("height_min", 256),
            height_max=gen_raw.get("height_max", 2048),
            steps_min=gen_raw.get("steps_min", 1),
            steps_max=gen_raw.get("steps_max", 100),
            cfg_min=gen_raw.get("cfg_min", 1.0),
            cfg_max=gen_raw.get("cfg_max", 30.0),
            width_increment=gen_raw.get("width_increment", 64),
            height_increment=gen_raw.get("height_increment", 64),
            cfg_increment=gen_raw.get("cfg_increment", 0.5),
        )
        
        # 프롬프트 설정 - prompt.json에서 로드 (load_external_prompts 사용)
        ext_prompts = load_external_prompts()
        # use_korean_prompt만 app_config.json에서 로드 (사용자 설정 유지)
        prompt_raw = raw.get("prompts", {})
        prompts = PromptsConfig(
            system_prompt_flux_en=ext_prompts.get("system_prompt_flux_en", ""),
            system_prompt_flux_kr=ext_prompts.get("system_prompt_flux_kr", ""),
            system_prompt_ernie_en=ext_prompts.get("system_prompt_ernie_en", ""),
            system_prompt_ernie_kr=ext_prompts.get("system_prompt_ernie_kr", ""),
            system_prompt_sdxl_en=ext_prompts.get("system_prompt_sdxl_en", ""),
            system_prompt_sdxl_kr=ext_prompts.get("system_prompt_sdxl_kr", ""),
            system_prompt_zanime_webtoon_en=ext_prompts.get("system_prompt_zanime_webtoon_en", ""),
            system_prompt_zanime_webtoon_kr=ext_prompts.get("system_prompt_zanime_webtoon_kr", ""),
            system_prompt_zanime_anime_en=ext_prompts.get("system_prompt_zanime_anime_en", ""),
            system_prompt_zanime_anime_kr=ext_prompts.get("system_prompt_zanime_anime_kr", ""),
            system_prompt_zanime_basic_en=ext_prompts.get("system_prompt_zanime_basic_en", ""),
            system_prompt_zanime_basic_kr=ext_prompts.get("system_prompt_zanime_basic_kr", ""),
            negative_default=ext_prompts.get("negative_default", ""),
            use_korean_prompt=prompt_raw.get("use_korean_prompt", True),
            zanime_style=prompt_raw.get("zanime_style", ""),
        )
  
        # 워크플로우 설정
        wf_raw = raw.get("workflow", {})
        workflow = WorkflowConfig(
            checkpoint_template=wf_raw.get("checkpoint_template", "workflows/checkpoint.json"),
            gguf_template=wf_raw.get("gguf_template", "workflows/gguf_unet.json"),
            flux_gguf_template=wf_raw.get("flux_gguf_template", "workflows/flux_gguf.json"),
            zimage_template=wf_raw.get("zimage_template", "workflows/zimage.json"),
            sampler_name=wf_raw.get("sampler_name", "euler"),
            scheduler=wf_raw.get("scheduler", "normal"),
            denoise=wf_raw.get("denoise", 1.0),
        )
        
        # 출력 설정
        out_raw = raw.get("output", {})
        output = OutputConfig(
            directory=out_raw.get("directory", "outputs"),
            filename_prefix=out_raw.get("filename_prefix", "ComfyUI_%date%"),
        )
        
        # UI 설정
        ui_raw = raw.get("ui", {})
        theme_raw = ui_raw.get("theme", {})
        theme = ThemeConfig(
            bg_color=theme_raw.get("bg_color", "#0f172a"),
            fg_color=theme_raw.get("fg_color", "#e2e8f0"),
            accent_color=theme_raw.get("accent_color", "#38bdf8"),
            panel_color=theme_raw.get("panel_color", "#111827"),
            surface_color=theme_raw.get("surface_color", "#1f2937"),
            border_color=theme_raw.get("border_color", "#334155"),
            success_color=theme_raw.get("success_color", "#34d399"),
            warning_color=theme_raw.get("warning_color", "#fbbf24"),
            error_color=theme_raw.get("error_color", "#f87171"),
        )
        
        presets_raw = ui_raw.get("resolution_presets", [])
        resolution_presets = [
            {"label": p.get("label", ""), "width": p.get("width", 512), "height": p.get("height", 512)}
            for p in presets_raw
        ] if presets_raw else [
            {"label": "512x512 (SD 1.5)", "width": 512, "height": 512},
            {"label": "768x768 (중간)", "width": 768, "height": 768},
            {"label": "1024x1024 (SDXL)", "width": 1024, "height": 1024},
            {"label": "832x1216 (세로)", "width": 832, "height": 1216},
            {"label": "1216x832 (가로)", "width": 1216, "height": 832},
        ]
        
        ui = UIConfig(
            window_width=ui_raw.get("window_width", 960),
            window_height=ui_raw.get("window_height", 780),
            window_min_width=ui_raw.get("window_min_width", 840),
            window_min_height=ui_raw.get("window_min_height", 640),
            startup_window_width=ui_raw.get("startup_window_width", 540),
            startup_window_height=ui_raw.get("startup_window_height", 360),
            font_family=ui_raw.get("font_family", "NanumGothic"),
            font_fallback=ui_raw.get("font_fallback", "Arial"),
            font_size=ui_raw.get("font_size", 11),
            theme=theme,
            resolution_presets=resolution_presets,
        )
        
        # 캐시 설정
        cache_raw = raw.get("cache", {})
        cache = CacheConfig(
            model_cache_ttl_seconds=cache_raw.get("model_cache_ttl_seconds", 10.0),
        )
        
        # ComfyUI 모델 경로
        comfyui_model_paths = raw.get("comfyui_model_paths", [
            "~/AppData/Local/Comfy-Desktop/ComfyUI-Shared/models",
            "~/AppData/Local/Comfy-Desktop/ComfyUI-Installs/ComfyUI/ComfyUI/models",
            "C:/ComfyUI/models",
            "C:/ComfyUI_windows_portable/ComfyUI/models",
        ])
        
        # 모델 프리셋
        model_presets_raw = raw.get("model_presets", {})
        model_presets = {}
        for preset_name, preset_data in model_presets_raw.items():
            if isinstance(preset_data, dict):
                model_presets[preset_name] = ModelPresetConfig(
                    type=preset_data.get("type", "flux_gguf"),
                    clip1=preset_data.get("clip1", ""),
                    clip2=preset_data.get("clip2", ""),
                    vae=preset_data.get("vae", ""),
                    default_steps=preset_data.get("default_steps", 29),
                    default_cfg=preset_data.get("default_cfg", 1),
                    sampler_name=preset_data.get("sampler_name", "euler"),
                    scheduler=preset_data.get("scheduler", "simple"),
                )
        
        return AppConfig(
            lmstudio=lmstudio,
            comfyui=comfyui,
            generation=generation,
            prompts=prompts,
            workflow=workflow,
            output=output,
            ui=ui,
            cache=cache,
            comfyui_model_paths=comfyui_model_paths,
            model_presets=model_presets,
        )
    
    def save(self, config: Optional[AppConfig] = None) -> bool:
        """설정을 JSON 파일로 저장"""
        if config is not None:
            self._config = config
        
        if self._config is None:
            return False
        
        temp_path = None
        try:
            raw = self._config_to_dict(self._config)
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.config_path.parent,
                prefix=f".{self.config_path.name}.",
                suffix=".tmp",
                delete=False,
            ) as f:
                temp_path = Path(f.name)
                json.dump(raw, f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(temp_path, self.config_path)
            return True
        except OSError as e:
            print(f"[ConfigManager] 설정 저장 실패: {e}")
            return False
        finally:
            if temp_path is not None:
                try:
                    temp_path.unlink(missing_ok=True)
                except OSError:
                    pass
    
    def _config_to_dict(self, config: AppConfig) -> Dict[str, Any]:
        """데이터클래스를 딕셔너리로 변환"""
        return {
            "lmstudio": {
                "url": config.lmstudio.url,
                "model": config.lmstudio.model,
                "timeout_seconds": config.lmstudio.timeout_seconds,
                "enhance_temperature": config.lmstudio.enhance_temperature,
                "enhance_max_tokens": config.lmstudio.enhance_max_tokens,
            },
            "comfyui": {
                "url": config.comfyui.url,
                "model": config.comfyui.model,
                "timeout_seconds": config.comfyui.timeout_seconds,
                "poll_interval_seconds": config.comfyui.poll_interval_seconds,
                "max_wait_seconds": config.comfyui.max_wait_seconds,
            },
            "generation": {
                "default_width": config.generation.default_width,
                "default_height": config.generation.default_height,
                "default_steps": config.generation.default_steps,
                "default_cfg": config.generation.default_cfg,
                "default_seed": config.generation.default_seed,
                "width_min": config.generation.width_min,
                "width_max": config.generation.width_max,
                "height_min": config.generation.height_min,
                "height_max": config.generation.height_max,
                "steps_min": config.generation.steps_min,
                "steps_max": config.generation.steps_max,
                "cfg_min": config.generation.cfg_min,
                "cfg_max": config.generation.cfg_max,
                "width_increment": config.generation.width_increment,
                "height_increment": config.generation.height_increment,
                "cfg_increment": config.generation.cfg_increment,
            },
            "prompts": {
                # 프롬프트 설정은 prompt.json에서 관리하므로 use_korean_prompt만 저장
                "use_korean_prompt": config.prompts.use_korean_prompt,
                "zanime_style": config.prompts.zanime_style,
            },
            "workflow": {
                "checkpoint_template": config.workflow.checkpoint_template,
                "gguf_template": config.workflow.gguf_template,
                "flux_gguf_template": config.workflow.flux_gguf_template,
                "zimage_template": config.workflow.zimage_template,
                "sampler_name": config.workflow.sampler_name,
                "scheduler": config.workflow.scheduler,
                "denoise": config.workflow.denoise,
            },
            "output": {
                "directory": config.output.directory,
                "filename_prefix": config.output.filename_prefix,
            },
            "ui": {
                "window_width": config.ui.window_width,
                "window_height": config.ui.window_height,
                "window_min_width": config.ui.window_min_width,
                "window_min_height": config.ui.window_min_height,
                "startup_window_width": config.ui.startup_window_width,
                "startup_window_height": config.ui.startup_window_height,
                "font_family": config.ui.font_family,
                "font_fallback": config.ui.font_fallback,
                "font_size": config.ui.font_size,
                "theme": {
                    "bg_color": config.ui.theme.bg_color,
                    "fg_color": config.ui.theme.fg_color,
                    "accent_color": config.ui.theme.accent_color,
                    "panel_color": config.ui.theme.panel_color,
                    "surface_color": config.ui.theme.surface_color,
                    "border_color": config.ui.theme.border_color,
                    "success_color": config.ui.theme.success_color,
                    "warning_color": config.ui.theme.warning_color,
                    "error_color": config.ui.theme.error_color,
                },
                "resolution_presets": config.ui.resolution_presets,
            },
            "cache": {
                "model_cache_ttl_seconds": config.cache.model_cache_ttl_seconds,
            },
            "comfyui_model_paths": config.comfyui_model_paths,
            "model_presets": {
                name: {
                    "type": preset.type,
                    "clip1": preset.clip1,
                    "clip2": preset.clip2,
                    "vae": preset.vae,
                    "default_steps": preset.default_steps,
                    "default_cfg": preset.default_cfg,
                    "sampler_name": preset.sampler_name,
                    "scheduler": preset.scheduler,
                }
                for name, preset in config.model_presets.items()
            },
        }
    
    def get(self) -> AppConfig:
        """현재 설정 반환 (로드되지 않았으면 로드)"""
        if self._config is None:
            return self.load()
        return self._config

    def set_config(self, config: AppConfig) -> None:
        """설정 객체를 안전하게 업데이트"""
        self._config = config

    @property
    def config(self) -> AppConfig:
        """현재 설정 반환"""
        return self.get()

    @config.setter
    def config(self, config: AppConfig) -> None:
        """설정 객체 설정"""
        self.set_config(config)
    
    def update_from_legacy(self, legacy_config: Dict[str, Any]) -> AppConfig:
        """기존 설정 형식(lm_url, comfy_url 등)을 새 형식으로 마이그레이션"""
        if "lm_url" in legacy_config:
            self._raw_config.setdefault("lmstudio", {})["url"] = legacy_config["lm_url"]
        if "comfy_url" in legacy_config:
            self._raw_config.setdefault("comfyui", {})["url"] = legacy_config["comfy_url"]
        if "lm_model" in legacy_config:
            self._raw_config.setdefault("lmstudio", {})["model"] = legacy_config["lm_model"]
        if "comfy_model" in legacy_config:
            self._raw_config.setdefault("comfyui", {})["model"] = legacy_config["comfy_model"]
        if "use_lm_enhancer" in legacy_config:
            # 프롬프트 강화 사용 여부는 별도 저장 필요 시 추가
            pass
        
        return self.load()
    
    def expand_path(self, path_str: str) -> Path:
        """경로 문자열에서 ~, 환경변수 확장"""
        return Path(os.path.expanduser(os.path.expandvars(path_str))).resolve()
    
    def get_model_base_paths(self) -> list:
        """ComfyUI 모델 기본 경로 리스트 반환 (확장됨)"""
        config = self.get()
        return [self.expand_path(p) for p in config.comfyui_model_paths]


# 전역 인스턴스 (싱글톤 패턴)
_config_manager: Optional[ConfigManager] = None


def get_config_manager(config_path: Optional[Union[str, Path]] = None) -> ConfigManager:
    """ConfigManager 싱글톤 인스턴스 반환"""
    global _config_manager
    target_path = Path(config_path) if config_path is not None else None

    if _config_manager is None:
        _config_manager = ConfigManager(target_path)
    elif target_path is not None and _config_manager.config_path != target_path:
        _config_manager = ConfigManager(target_path)

    _config_manager.load()
    return _config_manager


def reset_config_manager():
    """ConfigManager 인스턴스 리셋 (테스트용)"""
    global _config_manager
    _config_manager = None
