"""
Clase base para procesamiento de imágenes.
Proporciona funcionalidad común para todos los procesadores.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Optional, Union
from abc import ABC, abstractmethod

from .utils import validate_image, safe_path


class ImageProcessor(ABC):
    """
    Clase base abstracta para procesadores de imágenes.
    Define la interfaz común para todos los procesadores.
    """
    
    def __init__(self, name: str = "ImageProcessor"):
        """
        Inicializa el procesador.
        
        Args:
            name: Nombre descriptivo del procesador
        """
        self.name = name
        self._last_result = None
    
    @abstractmethod
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        """
        Método abstracto para procesar una imagen.
        Debe ser implementado por las subclases.
        
        Args:
            image: Imagen a procesar
            **kwargs: Parámetros específicos del procesador
            
        Returns:
            Imagen procesada
        """
        pass
    
    def validate_input(self, image: np.ndarray) -> None:
        """
        Valida que la imagen de entrada sea válida.
        
        Args:
            image: Imagen a validar
            
        Raises:
            ValueError: Si la imagen no es válida
        """
        if not validate_image(image):
            raise ValueError(f"{self.name}: Imagen de entrada inválida")
    
    def load_image(self, path: Union[str, Path]) -> np.ndarray:
        """
        Carga una imagen desde un archivo.
        
        Args:
            path: Ruta del archivo
            
        Returns:
            Imagen cargada
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si no se pudo cargar la imagen
        """
        file_path = safe_path(path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"{self.name}: Archivo no encontrado: {file_path}")
        
        image = cv2.imread(str(file_path))
        
        if image is None:
            raise ValueError(f"{self.name}: No se pudo cargar la imagen: {file_path}")
        
        return image
    
    def save_image(self, image: np.ndarray, path: Union[str, Path]) -> bool:
        """
        Guarda una imagen en un archivo.
        
        Args:
            image: Imagen a guardar
            path: Ruta de destino
            
        Returns:
            True si se guardó correctamente, False si no
        """
        self.validate_input(image)
        file_path = safe_path(path)
        
        # Crear el directorio si no existe
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        success = cv2.imwrite(str(file_path), image)
        
        if success:
            print(f"{self.name}: Imagen guardada en {file_path}")
        else:
            print(f"{self.name}: Error al guardar imagen en {file_path}")
        
        return success
    
    def process_and_save(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        **kwargs
    ) -> Optional[np.ndarray]:
        """
        Carga una imagen, la procesa y la guarda.
        
        Args:
            input_path: Ruta de la imagen de entrada
            output_path: Ruta de la imagen de salida
            **kwargs: Parámetros para el procesamiento
            
        Returns:
            Imagen procesada o None si hubo error
        """
        try:
            image = self.load_image(input_path)
            processed = self.process(image, **kwargs)
            self.save_image(processed, output_path)
            self._last_result = processed
            return processed
        except Exception as e:
            print(f"{self.name}: Error en procesamiento: {e}")
            return None
    
    def get_last_result(self) -> Optional[np.ndarray]:
        """
        Obtiene el último resultado procesado.
        
        Returns:
            Última imagen procesada o None
        """
        return self._last_result
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"


class BatchProcessor:
    """
    Procesador por lotes que puede aplicar múltiples procesadores.
    """
    
    def __init__(self):
        """Inicializa el procesador por lotes."""
        self.processors = []
    
    def add_processor(self, processor: ImageProcessor) -> 'BatchProcessor':
        """
        Añade un procesador a la cadena.
        
        Args:
            processor: Procesador a añadir
            
        Returns:
            Self para encadenamiento
        """
        self.processors.append(processor)
        return self
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        """
        Procesa una imagen aplicando todos los procesadores en secuencia.
        
        Args:
            image: Imagen a procesar
            **kwargs: Parámetros para los procesadores
            
        Returns:
            Imagen procesada
        """
        result = image.copy()
        
        for processor in self.processors:
            result = processor.process(result, **kwargs)
        
        return result
    
    def clear(self) -> None:
        """Limpia todos los procesadores."""
        self.processors.clear()
    
    def __len__(self) -> int:
        return len(self.processors)


__all__ = ['ImageProcessor', 'BatchProcessor']
