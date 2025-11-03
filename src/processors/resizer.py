"""
Procesador para redimensionar imágenes.
"""

import cv2
import numpy as np
from typing import Optional, Tuple

from ..core.image_processor import ImageProcessor
from ..core.utils import get_new_dimensions


class ImageResizer(ImageProcessor):
    """
    Procesador para redimensionar imágenes con diferentes métodos de interpolación.
    """
    
    # Métodos de interpolación disponibles
    INTERPOLATION_METHODS = {
        'nearest': cv2.INTER_NEAREST,
        'linear': cv2.INTER_LINEAR,
        'cubic': cv2.INTER_CUBIC,
        'area': cv2.INTER_AREA,
        'lanczos': cv2.INTER_LANCZOS4,
    }
    
    def __init__(self, default_interpolation: str = 'linear'):
        """
        Inicializa el redimensionador.
        
        Args:
            default_interpolation: Método de interpolación por defecto
        """
        super().__init__(name="ImageResizer")
        self.default_interpolation = default_interpolation
    
    def process(
        self,
        image: np.ndarray,
        width: Optional[int] = None,
        height: Optional[int] = None,
        scale: Optional[float] = None,
        maintain_aspect: bool = True,
        interpolation: Optional[str] = None
    ) -> np.ndarray:
        """
        Redimensiona una imagen.
        
        Args:
            image: Imagen de entrada
            width: Ancho objetivo (opcional)
            height: Altura objetivo (opcional)
            scale: Factor de escala (opcional)
            maintain_aspect: Mantener aspect ratio
            interpolation: Método de interpolación
            
        Returns:
            Imagen redimensionada
        """
        self.validate_input(image)
        
        original_height, original_width = image.shape[:2]
        
        # Calcular nuevas dimensiones
        new_width, new_height = get_new_dimensions(
            original_width,
            original_height,
            target_width=width,
            target_height=height,
            scale_factor=scale,
            maintain_aspect=maintain_aspect
        )
        
        # Si las dimensiones no cambian, retornar copia
        if new_width == original_width and new_height == original_height:
            return image.copy()
        
        # Obtener método de interpolación
        interp_method = self._get_interpolation_method(interpolation)
        
        # Redimensionar
        resized = cv2.resize(
            image,
            (new_width, new_height),
            interpolation=interp_method
        )
        
        return resized
    
    def resize_by_percentage(
        self,
        image: np.ndarray,
        percentage: int,
        interpolation: Optional[str] = None
    ) -> np.ndarray:
        """
        Redimensiona una imagen por porcentaje.
        
        Args:
            image: Imagen de entrada
            percentage: Porcentaje del tamaño original (100 = sin cambio)
            interpolation: Método de interpolación
            
        Returns:
            Imagen redimensionada
        """
        scale = percentage / 100.0
        return self.process(image, scale=scale, interpolation=interpolation)
    
    def resize_to_max_dimension(
        self,
        image: np.ndarray,
        max_dimension: int,
        interpolation: Optional[str] = None
    ) -> np.ndarray:
        """
        Redimensiona para que la dimensión más grande sea max_dimension.
        
        Args:
            image: Imagen de entrada
            max_dimension: Dimensión máxima permitida
            interpolation: Método de interpolación
            
        Returns:
            Imagen redimensionada
        """
        self.validate_input(image)
        
        height, width = image.shape[:2]
        
        if max(width, height) <= max_dimension:
            return image.copy()
        
        if width > height:
            return self.process(
                image,
                width=max_dimension,
                maintain_aspect=True,
                interpolation=interpolation
            )
        else:
            return self.process(
                image,
                height=max_dimension,
                maintain_aspect=True,
                interpolation=interpolation
            )
    
    def compare_methods(
        self,
        image: np.ndarray,
        width: Optional[int] = None,
        height: Optional[int] = None,
        scale: Optional[float] = None
    ) -> dict:
        """
        Compara diferentes métodos de interpolación.
        
        Args:
            image: Imagen de entrada
            width: Ancho objetivo
            height: Altura objetivo
            scale: Factor de escala
            
        Returns:
            Diccionario con método como clave e imagen como valor
        """
        results = {}
        
        for method_name in self.INTERPOLATION_METHODS.keys():
            results[method_name] = self.process(
                image,
                width=width,
                height=height,
                scale=scale,
                interpolation=method_name
            )
        
        return results
    
    def _get_interpolation_method(self, interpolation: Optional[str]) -> int:
        """
        Obtiene el método de interpolación de OpenCV.
        
        Args:
            interpolation: Nombre del método o None para usar default
            
        Returns:
            Constante de OpenCV para interpolación
        """
        if interpolation is None:
            interpolation = self.default_interpolation
        
        method = self.INTERPOLATION_METHODS.get(interpolation.lower())
        
        if method is None:
            print(f"⚠️ Método '{interpolation}' no válido. Usando '{self.default_interpolation}'")
            method = self.INTERPOLATION_METHODS[self.default_interpolation]
        
        return method


__all__ = ['ImageResizer']
