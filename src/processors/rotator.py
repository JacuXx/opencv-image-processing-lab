"""
Procesador para rotar imágenes.
"""

import cv2
import numpy as np
from typing import Tuple, Optional

from ..core.image_processor import ImageProcessor


class ImageRotator(ImageProcessor):
    """
    Procesador para rotar imágenes con diferentes opciones.
    
    Grados positivos: Rotación ANTIHORARIA
    Grados negativos: Rotación HORARIA
    """
    
    def __init__(self):
        """Inicializa el rotador de imágenes."""
        super().__init__(name="ImageRotator")
    
    def process(
        self,
        image: np.ndarray,
        degrees: float = 0,
        expand: bool = True,
        center: Optional[Tuple[int, int]] = None,
        scale: float = 1.0,
        border_color: Tuple[int, int, int] = (255, 255, 255)
    ) -> np.ndarray:
        """
        Rota una imagen.
        
        Args:
            image: Imagen de entrada
            degrees: Grados de rotación (+ antihorario, - horario)
            expand: Si True, expande la imagen para que no se corte
            center: Centro de rotación. Si None, usa el centro de la imagen
            scale: Factor de escala durante la rotación
            border_color: Color del borde (BGR)
            
        Returns:
            Imagen rotada
        """
        self.validate_input(image)
        
        if degrees == 0:
            return image.copy()
        
        # Obtener dimensiones
        height, width = image.shape[:2]
        
        # Determinar centro de rotación
        if center is None:
            center = (width // 2, height // 2)
        
        # Obtener matriz de rotación
        rotation_matrix = cv2.getRotationMatrix2D(center, degrees, scale)
        
        if expand:
            # Calcular nuevas dimensiones para que no se corte
            cos = np.abs(rotation_matrix[0, 0])
            sin = np.abs(rotation_matrix[0, 1])
            
            new_width = int((height * sin) + (width * cos))
            new_height = int((height * cos) + (width * sin))
            
            # Ajustar matriz para centrar la imagen rotada
            rotation_matrix[0, 2] += (new_width / 2) - center[0]
            rotation_matrix[1, 2] += (new_height / 2) - center[1]
            
            output_size = (new_width, new_height)
        else:
            output_size = (width, height)
        
        # Aplicar rotación
        rotated = cv2.warpAffine(
            image,
            rotation_matrix,
            output_size,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=border_color
        )
        
        return rotated
    
    def rotate_90(self, image: np.ndarray, times: int = 1) -> np.ndarray:
        """
        Rota una imagen 90 grados múltiples veces (más eficiente).
        
        Args:
            image: Imagen de entrada
            times: Número de rotaciones de 90° (positivo antihorario)
            
        Returns:
            Imagen rotada
        """
        self.validate_input(image)
        
        # Normalizar times a 0-3
        times = times % 4
        
        if times == 0:
            return image.copy()
        elif times == 1:
            return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif times == 2:
            return cv2.rotate(image, cv2.ROTATE_180)
        else:  # times == 3
            return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    
    def rotate_180(self, image: np.ndarray) -> np.ndarray:
        """
        Rota una imagen 180 grados.
        
        Args:
            image: Imagen de entrada
            
        Returns:
            Imagen rotada 180°
        """
        return self.rotate_90(image, times=2)
    
    def flip_horizontal(self, image: np.ndarray) -> np.ndarray:
        """
        Voltea una imagen horizontalmente.
        
        Args:
            image: Imagen de entrada
            
        Returns:
            Imagen volteada horizontalmente
        """
        self.validate_input(image)
        return cv2.flip(image, 1)
    
    def flip_vertical(self, image: np.ndarray) -> np.ndarray:
        """
        Voltea una imagen verticalmente.
        
        Args:
            image: Imagen de entrada
            
        Returns:
            Imagen volteada verticalmente
        """
        self.validate_input(image)
        return cv2.flip(image, 0)
    
    def flip_both(self, image: np.ndarray) -> np.ndarray:
        """
        Voltea una imagen en ambos ejes (equivalente a 180°).
        
        Args:
            image: Imagen de entrada
            
        Returns:
            Imagen volteada en ambos ejes
        """
        self.validate_input(image)
        return cv2.flip(image, -1)
    
    def rotate_common_angles(self, image: np.ndarray) -> dict:
        """
        Rota una imagen en ángulos comunes.
        
        Args:
            image: Imagen de entrada
            
        Returns:
            Diccionario con ángulo como clave e imagen como valor
        """
        angles = [0, 45, 90, 135, 180, 225, 270, 315]
        results = {}
        
        for angle in angles:
            results[angle] = self.process(image, degrees=angle)
        
        return results


__all__ = ['ImageRotator']
