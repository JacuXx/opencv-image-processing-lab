"""
Utilidades comunes para procesamiento de imágenes.
Funciones helper reutilizables en todo el proyecto.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Optional, Tuple, Union


def validate_image(image: np.ndarray) -> bool:
    """
    Valida que un objeto sea una imagen válida.
    
    Args:
        image: Array de numpy que representa la imagen
        
    Returns:
        True si es válida, False si no
    """
    if image is None:
        return False
    if not isinstance(image, np.ndarray):
        return False
    if len(image.shape) not in [2, 3]:
        return False
    return True


def get_image_info(image: np.ndarray) -> dict:
    """
    Obtiene información detallada de una imagen.
    
    Args:
        image: Imagen a analizar
        
    Returns:
        Diccionario con propiedades de la imagen
    """
    if not validate_image(image):
        raise ValueError("Imagen inválida")
    
    info = {
        'shape': image.shape,
        'dtype': str(image.dtype),
        'size': image.size,
        'nbytes': image.nbytes,
        'height': image.shape[0],
        'width': image.shape[1],
    }
    
    if len(image.shape) == 3:
        info['channels'] = image.shape[2]
        info['color_mode'] = 'Color' if image.shape[2] == 3 else 'RGBA'
    else:
        info['channels'] = 1
        info['color_mode'] = 'Grayscale'
    
    return info


def print_image_info(image: np.ndarray, title: str = "Imagen") -> None:
    """
    Imprime información formateada de una imagen.
    
    Args:
        image: Imagen a analizar
        title: Título descriptivo
    """
    info = get_image_info(image)
    
    print(f"\n{title}:")
    print(f"  • Shape (Forma): {info['shape']}")
    print(f"  • Altura: {info['height']} píxeles")
    print(f"  • Ancho: {info['width']} píxeles")
    print(f"  • Canales: {info['channels']}")
    print(f"  • Modo: {info['color_mode']}")
    print(f"  • Tipo de datos: {info['dtype']}")
    print(f"  • Tamaño total: {info['size']} píxeles")
    print(f"  • Memoria: {info['nbytes']} bytes ({info['nbytes'] / 1024:.2f} KB)")


def ensure_color(image: np.ndarray) -> np.ndarray:
    """
    Asegura que una imagen esté en formato RGB de 3 canales.
    
    Args:
        image: Imagen de entrada
        
    Returns:
        Imagen en formato RGB
    """
    if len(image.shape) == 2:
        return cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    return image


def bgr_to_rgb(image: np.ndarray) -> np.ndarray:
    """
    Convierte una imagen de BGR (OpenCV) a RGB (matplotlib).
    
    Args:
        image: Imagen en formato BGR
        
    Returns:
        Imagen en formato RGB
    """
    if len(image.shape) == 3 and image.shape[2] == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def rgb_to_bgr(image: np.ndarray) -> np.ndarray:
    """
    Convierte una imagen de RGB a BGR (OpenCV).
    
    Args:
        image: Imagen en formato RGB
        
    Returns:
        Imagen en formato BGR
    """
    if len(image.shape) == 3 and image.shape[2] == 3:
        return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image


def create_lookup_table(func, dtype=np.uint8) -> np.ndarray:
    """
    Crea una tabla de lookup para transformaciones de píxeles.
    
    Args:
        func: Función que toma un valor y retorna el valor transformado
        dtype: Tipo de datos de salida
        
    Returns:
        Tabla de lookup
    """
    return np.array([func(i) for i in range(256)]).astype(dtype)


def calculate_aspect_ratio(width: int, height: int) -> float:
    """
    Calcula el aspect ratio de una imagen.
    
    Args:
        width: Ancho de la imagen
        height: Altura de la imagen
        
    Returns:
        Aspect ratio (ancho/alto)
    """
    return width / height if height != 0 else 0


def get_new_dimensions(
    original_width: int,
    original_height: int,
    target_width: Optional[int] = None,
    target_height: Optional[int] = None,
    scale_factor: Optional[float] = None,
    maintain_aspect: bool = True
) -> Tuple[int, int]:
    """
    Calcula las nuevas dimensiones de una imagen.
    
    Args:
        original_width: Ancho original
        original_height: Altura original
        target_width: Ancho objetivo (opcional)
        target_height: Altura objetivo (opcional)
        scale_factor: Factor de escala (opcional)
        maintain_aspect: Mantener aspect ratio
        
    Returns:
        Tupla (nuevo_ancho, nueva_altura)
    """
    if scale_factor is not None:
        return (
            int(original_width * scale_factor),
            int(original_height * scale_factor)
        )
    
    if target_width and target_height:
        if maintain_aspect:
            aspect = calculate_aspect_ratio(original_width, original_height)
            target_aspect = calculate_aspect_ratio(target_width, target_height)
            
            if target_aspect > aspect:
                new_height = target_height
                new_width = int(new_height * aspect)
            else:
                new_width = target_width
                new_height = int(new_width / aspect)
            
            return (new_width, new_height)
        return (target_width, target_height)
    
    if target_width:
        aspect = calculate_aspect_ratio(original_width, original_height)
        return (target_width, int(target_width / aspect))
    
    if target_height:
        aspect = calculate_aspect_ratio(original_width, original_height)
        return (int(target_height * aspect), target_height)
    
    return (original_width, original_height)


def safe_path(path: Union[str, Path]) -> Path:
    """
    Convierte una ruta a Path y valida que sea segura.
    
    Args:
        path: Ruta como string o Path
        
    Returns:
        Path objeto
    """
    return Path(path).resolve()


def ensure_dir(path: Union[str, Path]) -> Path:
    """
    Asegura que un directorio exista, creándolo si es necesario.
    
    Args:
        path: Ruta del directorio
        
    Returns:
        Path objeto del directorio
    """
    dir_path = safe_path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


__all__ = [
    'validate_image',
    'get_image_info',
    'print_image_info',
    'ensure_color',
    'bgr_to_rgb',
    'rgb_to_bgr',
    'create_lookup_table',
    'calculate_aspect_ratio',
    'get_new_dimensions',
    'safe_path',
    'ensure_dir',
]
