"""
Módulo para guardar imágenes en diferentes formatos.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Union, Optional

from ..core.utils import safe_path, ensure_dir, validate_image


class ImageSaver:
    """
    Clase para guardar imágenes en diferentes formatos y con diferentes opciones.
    """
    
    # Parámetros de compresión por defecto
    DEFAULT_JPEG_QUALITY = 95
    DEFAULT_PNG_COMPRESSION = 3
    DEFAULT_WEBP_QUALITY = 90
    
    def __init__(self, default_output_dir: Optional[Union[str, Path]] = None):
        """
        Inicializa el guardador de imágenes.
        
        Args:
            default_output_dir: Directorio de salida por defecto
        """
        self.default_output_dir = default_output_dir
        if default_output_dir:
            ensure_dir(default_output_dir)
    
    def save(
        self,
        image: np.ndarray,
        path: Union[str, Path],
        **kwargs
    ) -> bool:
        """
        Guarda una imagen en un archivo.
        
        Args:
            image: Imagen a guardar
            path: Ruta de destino
            **kwargs: Parámetros adicionales según el formato
            
        Returns:
            True si se guardó correctamente
        """
        if not validate_image(image):
            print("❌ Error: Imagen inválida")
            return False
        
        file_path = safe_path(path)
        
        # Crear directorio si no existe
        ensure_dir(file_path.parent)
        
        # Determinar parámetros según la extensión
        params = self._get_save_params(file_path.suffix, **kwargs)
        
        # Guardar imagen
        success = cv2.imwrite(str(file_path), image, params)
        
        if success:
            print(f"✅ Imagen guardada: {file_path}")
            print(f"   Tamaño del archivo: {file_path.stat().st_size / 1024:.2f} KB")
        else:
            print(f"❌ Error al guardar imagen: {file_path}")
        
        return success
    
    def save_jpeg(
        self,
        image: np.ndarray,
        path: Union[str, Path],
        quality: int = None
    ) -> bool:
        """
        Guarda una imagen en formato JPEG.
        
        Args:
            image: Imagen a guardar
            path: Ruta de destino
            quality: Calidad JPEG (0-100)
            
        Returns:
            True si se guardó correctamente
        """
        if quality is None:
            quality = self.DEFAULT_JPEG_QUALITY
        
        return self.save(image, path, jpeg_quality=quality)
    
    def save_png(
        self,
        image: np.ndarray,
        path: Union[str, Path],
        compression: int = None
    ) -> bool:
        """
        Guarda una imagen en formato PNG.
        
        Args:
            image: Imagen a guardar
            path: Ruta de destino
            compression: Nivel de compresión (0-9)
            
        Returns:
            True si se guardó correctamente
        """
        if compression is None:
            compression = self.DEFAULT_PNG_COMPRESSION
        
        return self.save(image, path, png_compression=compression)
    
    def save_webp(
        self,
        image: np.ndarray,
        path: Union[str, Path],
        quality: int = None
    ) -> bool:
        """
        Guarda una imagen en formato WebP.
        
        Args:
            image: Imagen a guardar
            path: Ruta de destino
            quality: Calidad WebP (0-100)
            
        Returns:
            True si se guardó correctamente
        """
        if quality is None:
            quality = self.DEFAULT_WEBP_QUALITY
        
        return self.save(image, path, webp_quality=quality)
    
    def save_with_timestamp(
        self,
        image: np.ndarray,
        base_name: str,
        extension: str = '.jpg',
        directory: Optional[Union[str, Path]] = None
    ) -> bool:
        """
        Guarda una imagen con timestamp en el nombre.
        
        Args:
            image: Imagen a guardar
            base_name: Nombre base del archivo
            extension: Extensión del archivo
            directory: Directorio de destino
            
        Returns:
            True si se guardó correctamente
        """
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{base_name}_{timestamp}{extension}"
        
        if directory is None:
            directory = self.default_output_dir or Path.cwd()
        
        file_path = safe_path(directory) / filename
        
        return self.save(image, file_path)
    
    def save_multiple(
        self,
        images: dict,
        directory: Optional[Union[str, Path]] = None,
        prefix: str = "",
        suffix: str = "",
        **kwargs
    ) -> int:
        """
        Guarda múltiples imágenes.
        
        Args:
            images: Diccionario con nombre como clave e imagen como valor
            directory: Directorio de destino
            prefix: Prefijo para los nombres
            suffix: Sufijo para los nombres
            **kwargs: Parámetros adicionales para save()
            
        Returns:
            Número de imágenes guardadas exitosamente
        """
        if directory is None:
            directory = self.default_output_dir or Path.cwd()
        
        dir_path = safe_path(directory)
        ensure_dir(dir_path)
        
        count = 0
        
        for name, image in images.items():
            # Construir nombre de archivo
            filename = f"{prefix}{name}{suffix}"
            file_path = dir_path / filename
            
            if self.save(image, file_path, **kwargs):
                count += 1
        
        print(f"\n📁 Guardadas {count}/{len(images)} imágenes en {dir_path}")
        
        return count
    
    def _get_save_params(self, extension: str, **kwargs) -> list:
        """
        Obtiene los parámetros de guardado según la extensión.
        
        Args:
            extension: Extensión del archivo
            **kwargs: Parámetros proporcionados
            
        Returns:
            Lista de parámetros para cv2.imwrite
        """
        params = []
        ext = extension.lower()
        
        if ext in ['.jpg', '.jpeg']:
            quality = kwargs.get('jpeg_quality', self.DEFAULT_JPEG_QUALITY)
            params = [cv2.IMWRITE_JPEG_QUALITY, quality]
        
        elif ext == '.png':
            compression = kwargs.get('png_compression', self.DEFAULT_PNG_COMPRESSION)
            params = [cv2.IMWRITE_PNG_COMPRESSION, compression]
        
        elif ext == '.webp':
            quality = kwargs.get('webp_quality', self.DEFAULT_WEBP_QUALITY)
            params = [cv2.IMWRITE_WEBP_QUALITY, quality]
        
        return params


__all__ = ['ImageSaver']
