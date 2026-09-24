from .base import ModelProfile
from .ernie_aio import ErnieAioBaseProfile, ErnieAioTurboProfile
from .flux_gguf import FluxGGUFProfile
from .zimage_turbo import ZimageTurboProfile
from .zanime_aio import ZanimeAioProfile

__all__ = [
    "ModelProfile",
    "ErnieAioBaseProfile",
    "ErnieAioTurboProfile",
    "FluxGGUFProfile",
    "ZimageTurboProfile",
    "ZanimeAioProfile",
]
