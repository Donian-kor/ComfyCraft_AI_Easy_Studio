from .base import ModelProfile


class ZimageTurboProfile(ModelProfile):
    def __init__(self):
        super().__init__(
            name="zimage_turbo",
            family="zimage",
            aliases=("zimage", "zimage-turbo", "zimage_turbo"),
            patterns=("zimage", "z_image", "zimage-turbo", "zimage_turbo"),
            workflow_type="zimage",
            base="unet_clploadergguf",
            default_clip1="Z-Image-Engineer-V6-Q5_K_M.gguf",
            default_clip2="",
            default_vae="ae.safetensors",
            default_steps=8,
            default_cfg=2.0,
            sampler_name="dpmpp_2m",  # ComfyUI에서 사용하는 샘플러 이름
            scheduler="karras",  # Turbo 모델에 맞는 스케줄러
            priority=5,
        )
