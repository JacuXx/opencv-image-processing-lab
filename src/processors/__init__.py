"""Procesadores especializados para diferentes operaciones de imagen."""

from .gamma_adjuster import GammaAdjuster
from .resizer import ImageResizer
from .rotator import ImageRotator
from .text_overlay import TextOverlay

__all__ = ['GammaAdjuster', 'ImageResizer', 'ImageRotator', 'TextOverlay']
