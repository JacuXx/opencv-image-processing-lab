"""
Procesador para agregar texto a imágenes.
"""

import cv2
import numpy as np
from typing import Tuple, Optional, Dict

from ..core.image_processor import ImageProcessor


class TextOverlay(ImageProcessor):
    """
    Procesador para agregar texto sobre imágenes con diferentes estilos.
    """
    
    # Fuentes disponibles en OpenCV
    FONTS = {
        'simplex': cv2.FONT_HERSHEY_SIMPLEX,
        'plain': cv2.FONT_HERSHEY_PLAIN,
        'duplex': cv2.FONT_HERSHEY_DUPLEX,
        'complex': cv2.FONT_HERSHEY_COMPLEX,
        'triplex': cv2.FONT_HERSHEY_TRIPLEX,
        'complex_small': cv2.FONT_HERSHEY_COMPLEX_SMALL,
        'script_simplex': cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
        'script_complex': cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
    }
    
    # Colores predefinidos (BGR)
    COLORS = {
        'red': (0, 0, 255),
        'green': (0, 255, 0),
        'blue': (255, 0, 0),
        'yellow': (0, 255, 255),
        'cyan': (255, 255, 0),
        'magenta': (255, 0, 255),
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'orange': (0, 165, 255),
        'purple': (128, 0, 128),
    }
    
    def __init__(
        self,
        default_font: str = 'simplex',
        default_color: Tuple[int, int, int] = (0, 0, 255),
        default_thickness: int = 2,
        default_scale: float = 1.0
    ):
        """
        Inicializa el procesador de texto.
        
        Args:
            default_font: Fuente por defecto
            default_color: Color por defecto (BGR)
            default_thickness: Grosor por defecto
            default_scale: Escala por defecto
        """
        super().__init__(name="TextOverlay")
        self.default_font = default_font
        self.default_color = default_color
        self.default_thickness = default_thickness
        self.default_scale = default_scale
    
    def process(
        self,
        image: np.ndarray,
        text: str,
        position: Tuple[int, int],
        font: Optional[str] = None,
        color: Optional[Tuple[int, int, int]] = None,
        thickness: Optional[int] = None,
        scale: Optional[float] = None,
        line_type: int = cv2.LINE_AA
    ) -> np.ndarray:
        """
        Agrega texto a una imagen.
        
        Args:
            image: Imagen de entrada
            text: Texto a agregar
            position: Posición (x, y) del texto
            font: Nombre de la fuente
            color: Color del texto (BGR)
            thickness: Grosor del texto
            scale: Escala del texto
            line_type: Tipo de línea
            
        Returns:
            Imagen con texto
        """
        self.validate_input(image)
        
        # Usar valores por defecto si no se especifican
        if font is None:
            font = self.default_font
        if color is None:
            color = self.default_color
        if thickness is None:
            thickness = self.default_thickness
        if scale is None:
            scale = self.default_scale
        
        # Obtener fuente
        font_face = self._get_font(font)
        
        # Crear copia de la imagen
        result = image.copy()
        
        # Agregar texto
        cv2.putText(
            result,
            text,
            position,
            font_face,
            scale,
            color,
            thickness,
            line_type
        )
        
        return result
    
    def add_text_with_background(
        self,
        image: np.ndarray,
        text: str,
        position: Tuple[int, int],
        font: Optional[str] = None,
        text_color: Optional[Tuple[int, int, int]] = None,
        bg_color: Tuple[int, int, int] = (0, 0, 0),
        thickness: Optional[int] = None,
        scale: Optional[float] = None,
        padding: int = 10,
        alpha: float = 0.7
    ) -> np.ndarray:
        """
        Agrega texto con fondo semi-transparente.
        
        Args:
            image: Imagen de entrada
            text: Texto a agregar
            position: Posición (x, y) del texto
            font: Nombre de la fuente
            text_color: Color del texto (BGR)
            bg_color: Color de fondo (BGR)
            thickness: Grosor del texto
            scale: Escala del texto
            padding: Padding alrededor del texto
            alpha: Transparencia del fondo (0-1)
            
        Returns:
            Imagen con texto y fondo
        """
        self.validate_input(image)
        
        # Valores por defecto
        if font is None:
            font = self.default_font
        if text_color is None:
            text_color = self.default_color
        if thickness is None:
            thickness = self.default_thickness
        if scale is None:
            scale = self.default_scale
        
        font_face = self._get_font(font)
        
        # Obtener tamaño del texto
        (text_width, text_height), baseline = cv2.getTextSize(
            text, font_face, scale, thickness
        )
        
        # Calcular posición del rectángulo de fondo
        x, y = position
        rect_x1 = x - padding
        rect_y1 = y - text_height - padding
        rect_x2 = x + text_width + padding
        rect_y2 = y + baseline + padding
        
        # Crear copia de la imagen
        result = image.copy()
        overlay = result.copy()
        
        # Dibujar rectángulo de fondo
        cv2.rectangle(overlay, (rect_x1, rect_y1), (rect_x2, rect_y2), bg_color, -1)
        
        # Mezclar con transparencia
        cv2.addWeighted(overlay, alpha, result, 1 - alpha, 0, result)
        
        # Agregar texto
        cv2.putText(
            result,
            text,
            position,
            font_face,
            scale,
            text_color,
            thickness,
            cv2.LINE_AA
        )
        
        return result
    
    def add_multiline_text(
        self,
        image: np.ndarray,
        text_lines: list,
        start_position: Tuple[int, int],
        line_spacing: int = 10,
        **kwargs
    ) -> np.ndarray:
        """
        Agrega múltiples líneas de texto.
        
        Args:
            image: Imagen de entrada
            text_lines: Lista de líneas de texto
            start_position: Posición inicial (x, y)
            line_spacing: Espacio entre líneas
            **kwargs: Argumentos para process()
            
        Returns:
            Imagen con texto multilínea
        """
        result = image.copy()
        x, y = start_position
        
        # Obtener parámetros para calcular altura de línea
        font = kwargs.get('font', self.default_font)
        scale = kwargs.get('scale', self.default_scale)
        thickness = kwargs.get('thickness', self.default_thickness)
        font_face = self._get_font(font)
        
        for line in text_lines:
            # Agregar línea
            result = self.process(result, line, (x, y), **kwargs)
            
            # Calcular altura de la línea
            (_, text_height), baseline = cv2.getTextSize(
                line, font_face, scale, thickness
            )
            
            # Mover a la siguiente línea
            y += text_height + baseline + line_spacing
        
        return result
    
    def get_text_size(
        self,
        text: str,
        font: Optional[str] = None,
        scale: Optional[float] = None,
        thickness: Optional[int] = None
    ) -> Tuple[int, int]:
        """
        Obtiene el tamaño del texto en píxeles.
        
        Args:
            text: Texto a medir
            font: Nombre de la fuente
            scale: Escala del texto
            thickness: Grosor del texto
            
        Returns:
            Tupla (ancho, alto)
        """
        if font is None:
            font = self.default_font
        if scale is None:
            scale = self.default_scale
        if thickness is None:
            thickness = self.default_thickness
        
        font_face = self._get_font(font)
        (width, height), _ = cv2.getTextSize(text, font_face, scale, thickness)
        
        return (width, height)
    
    def _get_font(self, font_name: str) -> int:
        """
        Obtiene la fuente de OpenCV.
        
        Args:
            font_name: Nombre de la fuente
            
        Returns:
            Constante de fuente de OpenCV
        """
        font = self.FONTS.get(font_name.lower())
        
        if font is None:
            print(f"⚠️ Fuente '{font_name}' no válida. Usando '{self.default_font}'")
            font = self.FONTS[self.default_font]
        
        return font
    
    def _get_color(self, color_name: str) -> Tuple[int, int, int]:
        """
        Obtiene el color BGR desde el nombre.
        
        Args:
            color_name: Nombre del color
            
        Returns:
            Tupla BGR
        """
        return self.COLORS.get(color_name.lower(), self.default_color)
    
    @classmethod
    def list_fonts(cls) -> list:
        """Retorna lista de fuentes disponibles."""
        return list(cls.FONTS.keys())
    
    @classmethod
    def list_colors(cls) -> list:
        """Retorna lista de colores disponibles."""
        return list(cls.COLORS.keys())


__all__ = ['TextOverlay']
