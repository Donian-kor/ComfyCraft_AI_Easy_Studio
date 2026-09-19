from .base import ModelProfile


class ZanimeAioProfile(ModelProfile):
    def __init__(self):
        super().__init__(
            name="zanime_aio",
            family="zanime",
            aliases=(
                "z-anime-base-aio",
                "z_anime_base_aio",
                "z-anime-base-aio-fp8",
                "zanime_aio",
            ),
            patterns=(
                "z-anime-base",
                "z_anime_base",
                "zanime",
                "anime_aio",
            ),
            workflow_type="checkpoint",
            default_clip1="",
            default_clip2="",
            default_vae="",
            default_steps=35,
            default_cfg=4.0,
            sampler_name="euler_ancestral",
            scheduler="beta",
            priority=10,
        )
