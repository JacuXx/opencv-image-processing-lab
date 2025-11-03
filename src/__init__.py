"""
Paquete principal de procesamiento de imágenes.
Contiene módulos para procesar, visualizar y manipular imágenes con OpenCV.
"""

__version__ = "1.0.0"
__author__ = "Tu Nombre"

from .core.image_processor import ImageProcessor
from .core.utils import *

__all__ = ['ImageProcessor']
