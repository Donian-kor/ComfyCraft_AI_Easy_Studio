from .base import ModelProfile


class ErnieAioBaseProfile(ModelProfile):
    def __init__(self):
        super().__init__(
            name="ernie-aio-base",
            family="ernie",
            aliases=("ernie-aio-base", "ernie_aio_base"),
            patterns=("ernie-aio-base", "ernie_aio_base"),
            workflow_type="checkpoint",
            default_clip1="",
            default_clip2="",
            default_vae="",
            default_steps=50,
            default_cfg=4.0,
            sampler_name="euler",
            scheduler="simple",
            priority=4,
        )


class ErnieAioTurboProfile(ModelProfile):
    def __init__(self):
        super().__init__(
            name="ernie-aio-turbo",
            family="ernie",
            aliases=("ernie-aio-turbo", "ernie_aio_turbo"),
            patterns=("ernie-aio-turbo", "ernie_aio_turbo"),
            workflow_type="checkpoint",
            default_clip1="",
            default_clip2="",
            default_vae="",
            default_steps=8,
            default_cfg=1.0,
            sampler_name="euler",
            scheduler="simple",
            priority=3,
        )