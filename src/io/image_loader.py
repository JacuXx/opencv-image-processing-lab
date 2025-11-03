"""
Módulo para cargar imágenes desde diferentes fuentes.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Union, Optional

from ..core.utils import safe_path, validate_image


class ImageLoader:
    """
    Clase para cargar imágenes desde diferentes fuentes.
    """
    
    def __init__(self):
        """Inicializa el cargador de imágenes."""
        self.last_loaded = None
        self.last_path = None
    
    def load(
        self,
        path: Union[str, Path],
        mode: str = 'color'
    ) -> Optional[np.ndarray]:
        """
        Carga una imagen desde un archivo.
        
        Args:
            path: Ruta del archivo
            mode: Modo de carga ('color', 'grayscale', 'unchanged')
            
        Returns:
            Imagen cargada o None si falla
        """
        file_path = safe_path(path)
        
        if not file_path.exists():
            print(f"❌ Error: Archivo no encontrado: {file_path}")
            return None
        
        if not file_path.is_file():
            print(f"❌ Error: La ruta no es un archivo: {file_path}")
            return None
        
        # Determinar flag de carga
        if mode.lower() == 'grayscale':
            flag = cv2.IMREAD_GRAYSCALE
        elif mode.lower() == 'unchanged':
            flag = cv2.IMREAD_UNCHANGED
        else:
            flag = cv2.IMREAD_COLOR
        
        # Cargar imagen
        image = cv2.imread(str(file_path), flag)
        
        if image is None:
            print(f"❌ Error: No se pudo cargar la imagen: {file_path}")
            return None
        
        self.last_loaded = image
        self.last_path = file_path
        
        print(f"✅ Imagen cargada: {file_path.name}")
        print(f"   Dimensiones: {image.shape}")
        
        return image
    
    def load_color(self, path: Union[str, Path]) -> Optional[np.ndarray]:
        """
        Carga una imagen en color.
        
        Args:
            path: Ruta del archivo
            
        Returns:
            Imagen en color o None
        """
        return self.load(path, mode='color')
    
    def load_grayscale(self, path: Union[str, Path]) -> Optional[np.ndarray]:
        """
        Carga una imagen en escala de grises.
        
        Args:
            path: Ruta del archivo
            
        Returns:
            Imagen en escala de grises o None
        """
        return self.load(path, mode='grayscale')
    
    def load_with_alpha(self, path: Union[str, Path]) -> Optional[np.ndarray]:
        """
        Carga una imagen con canal alpha si existe.
        
        Args:
            path: Ruta del archivo
            
        Returns:
            Imagen con todos los canales o None
        """
        return self.load(path, mode='unchanged')
    
    def load_multiple(
        self,
        paths: list,
        mode: str = 'color'
    ) -> dict:
        """
        Carga múltiples imágenes.
        
        Args:
            paths: Lista de rutas
            mode: Modo de carga
            
        Returns:
            Diccionario con ruta como clave e imagen como valor
        """
        images = {}
        
        for path in paths:
            image = self.load(path, mode=mode)
            if image is not None:
                images[str(path)] = image
        
        return images
    
    def load_from_directory(
        self,
        directory: Union[str, Path],
        extensions: list = None,
        mode: str = 'color'
    ) -> dict:
        """
        Carga todas las imágenes de un directorio.
        
        Args:
            directory: Ruta del directorio
            extensions: Lista de extensiones permitidas
            mode: Modo de carga
            
        Returns:
            Diccionario con nombre de archivo como clave e imagen como valor
        """
        if extensions is None:
            extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
        
        dir_path = safe_path(directory)
        
        if not dir_path.exists():
            print(f"❌ Error: Directorio no encontrado: {dir_path}")
            return {}
        
        if not dir_path.is_dir():
            print(f"❌ Error: La ruta no es un directorio: {dir_path}")
            return {}
        
        images = {}
        
        for file_path in dir_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in extensions:
                image = self.load(file_path, mode=mode)
                if image is not None:
                    images[file_path.name] = image
        
        print(f"\n📁 Cargadas {len(images)} imágenes del directorio")
        
        return images
    
    def get_last_loaded(self) -> Optional[np.ndarray]:
        """
        Obtiene la última imagen cargada.
        
        Returns:
            Última imagen o None
        """
        return self.last_loaded
    
    def get_last_path(self) -> Optional[Path]:
        """
        Obtiene la ruta de la última imagen cargada.
        
        Returns:
            Ruta de la última imagen o None
        """
        return self.last_path


__all__ = ['ImageLoader']
