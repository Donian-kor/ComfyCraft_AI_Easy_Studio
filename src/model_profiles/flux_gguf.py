from .base import ModelProfile


class FluxGGUFProfile(ModelProfile):
    def __init__(self):
        super().__init__(
            name="flux_gguf",
            family="flux",
            aliases=("flux",),
            patterns=("flux",),
            workflow_type="flux_gguf",
            default_clip1="clip_l.safetensors",
            default_clip2="t5-v1_1-xxl-encoder-Q4_K_M.gguf",
            default_vae="diffusion_pytorch_model.safetensors",
            default_steps=29,
            default_cfg=1.0,
            sampler_name="euler",
            scheduler="simple",
            priority=10,
        )
