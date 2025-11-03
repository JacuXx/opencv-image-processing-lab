"""
Procesador de ajuste de gamma para corrección de iluminación.
"""

import cv2
import numpy as np
from typing import Union

from ..core.image_processor import ImageProcessor
from ..core.utils import create_lookup_table


class GammaAdjuster(ImageProcessor):
    """
    Procesador para ajustar el gamma de imágenes.
    
    Gamma < 1.0: Aclara la imagen (útil para imágenes oscuras)
    Gamma = 1.0: Sin cambios
    Gamma > 1.0: Oscurece la imagen (útil para imágenes muy claras)
    """
    
    def __init__(self, default_gamma: float = 1.0):
        """
        Inicializa el ajustador de gamma.
        
        Args:
            default_gamma: Valor de gamma por defecto
        """
        super().__init__(name="GammaAdjuster")
        self.default_gamma = default_gamma
    
    def process(self, image: np.ndarray, gamma: float = None) -> np.ndarray:
        """
        Ajusta el gamma de una imagen.
        
        Args:
            image: Imagen de entrada
            gamma: Valor de gamma. Si es None, usa el default_gamma
            
        Returns:
            Imagen con gamma ajustado
        """
        self.validate_input(image)
        
        if gamma is None:
            gamma = self.default_gamma
        
        if gamma == 1.0:
            return image.copy()
        
        # Construir tabla de lookup para mapear valores de píxeles
        inv_gamma = 1.0 / gamma
        lookup_table = create_lookup_table(
            lambda i: ((i / 255.0) ** inv_gamma) * 255
        )
        
        # Aplicar la transformación gamma usando la tabla de lookup
        return cv2.LUT(image, lookup_table)
    
    def process_multiple(
        self,
        image: np.ndarray,
        gamma_values: list
    ) -> dict:
        """
        Aplica múltiples valores de gamma a una imagen.
        
        Args:
            image: Imagen de entrada
            gamma_values: Lista de valores de gamma a aplicar
            
        Returns:
            Diccionario con gamma como clave e imagen procesada como valor
        """
        self.validate_input(image)
        
        results = {}
        for gamma in gamma_values:
            results[gamma] = self.process(image, gamma=gamma)
        
        return results
    
    def auto_gamma(self, image: np.ndarray) -> tuple:
        """
        Calcula un valor de gamma automático basado en el brillo de la imagen.
        
        Args:
            image: Imagen de entrada
            
        Returns:
            Tupla (gamma_sugerido, imagen_corregida)
        """
        self.validate_input(image)
        
        # Convertir a escala de grises si es necesario
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Calcular brillo promedio
        mean_brightness = np.mean(gray)
        
        # Determinar gamma basado en el brillo
        # Imagen oscura (< 85): gamma < 1 para aclarar
        # Imagen normal (85-170): gamma cercano a 1
        # Imagen clara (> 170): gamma > 1 para oscurecer
        if mean_brightness < 85:
            gamma = 0.5 + (mean_brightness / 170)  # 0.5 - 1.0
        elif mean_brightness > 170:
            gamma = 1.0 + ((mean_brightness - 170) / 170)  # 1.0 - 1.5
        else:
            gamma = 1.0
        
        # Aplicar gamma
        corrected = self.process(image, gamma=gamma)
        
        return gamma, corrected
    
    def get_recommended_gamma(self, image: np.ndarray) -> float:
        """
        Obtiene una recomendación de gamma sin aplicarla.
        
        Args:
            image: Imagen de entrada
            
        Returns:
            Valor de gamma recomendado
        """
        gamma, _ = self.auto_gamma(image)
        return gamma


__all__ = ['GammaAdjuster']
