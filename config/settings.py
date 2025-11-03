"""
Configuración del proyecto de procesamiento de imágenes.
"""

from pathlib import Path
from typing import Dict, Any


class Settings:
    """
    Configuración centralizada del proyecto.
    """
    
    def __init__(self):
        # Rutas del proyecto
        self.PROJECT_ROOT = Path(__file__).parent.parent
        self.DATA_DIR = self.PROJECT_ROOT / "data"
        self.INPUT_DIR = self.DATA_DIR / "input"
        self.OUTPUT_DIR = self.DATA_DIR / "output"
        self.SAMPLES_DIR = self.DATA_DIR / "samples"
        
        # Configuración de procesamiento
        self.DEFAULT_INTERPOLATION = 'linear'
        self.DEFAULT_GAMMA = 1.0
        self.DEFAULT_JPEG_QUALITY = 95
        self.DEFAULT_PNG_COMPRESSION = 3
        
        # Configuración de visualización
        self.DEFAULT_FIGSIZE = (10, 8)
        self.USE_RGB_CONVERSION = True
        
        # Extensiones de imagen soportadas
        self.SUPPORTED_EXTENSIONS = [
            '.jpg', '.jpeg', '.png', '.bmp', 
            '.tiff', '.tif', '.webp'
        ]
        
        # Crear directorios si no existen
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        """Crea los directorios necesarios si no existen."""
        for directory in [self.DATA_DIR, self.INPUT_DIR, 
                         self.OUTPUT_DIR, self.SAMPLES_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_input_path(self, filename: str) -> Path:
        """
        Obtiene la ruta completa de un archivo de entrada.
        
        Args:
            filename: Nombre del archivo
            
        Returns:
            Path completo
        """
        return self.INPUT_DIR / filename
    
    def get_output_path(self, filename: str) -> Path:
        """
        Obtiene la ruta completa de un archivo de salida.
        
        Args:
            filename: Nombre del archivo
            
        Returns:
            Path completo
        """
        return self.OUTPUT_DIR / filename
    
    def get_sample_path(self, filename: str) -> Path:
        """
        Obtiene la ruta completa de un archivo de ejemplo.
        
        Args:
            filename: Nombre del archivo
            
        Returns:
            Path completo
        """
        return self.SAMPLES_DIR / filename
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la configuración a diccionario.
        
        Returns:
            Diccionario con la configuración
        """
        return {
            'project_root': str(self.PROJECT_ROOT),
            'data_dir': str(self.DATA_DIR),
            'input_dir': str(self.INPUT_DIR),
            'output_dir': str(self.OUTPUT_DIR),
            'samples_dir': str(self.SAMPLES_DIR),
            'default_interpolation': self.DEFAULT_INTERPOLATION,
            'default_gamma': self.DEFAULT_GAMMA,
            'supported_extensions': self.SUPPORTED_EXTENSIONS,
        }
    
    def print_config(self) -> None:
        """Imprime la configuración actual."""
        print("\n" + "="*70)
        print("CONFIGURACIÓN DEL PROYECTO")
        print("="*70)
        print(f"Directorio raíz: {self.PROJECT_ROOT}")
        print(f"Directorio de datos: {self.DATA_DIR}")
        print(f"  • Entrada: {self.INPUT_DIR}")
        print(f"  • Salida: {self.OUTPUT_DIR}")
        print(f"  • Ejemplos: {self.SAMPLES_DIR}")
        print(f"\nInterpolación por defecto: {self.DEFAULT_INTERPOLATION}")
        print(f"Gamma por defecto: {self.DEFAULT_GAMMA}")
        print(f"Calidad JPEG: {self.DEFAULT_JPEG_QUALITY}")
        print(f"Compresión PNG: {self.DEFAULT_PNG_COMPRESSION}")
        print(f"\nExtensiones soportadas: {', '.join(self.SUPPORTED_EXTENSIONS)}")
        print("="*70)


# Instancia global de configuración
settings = Settings()


__all__ = ['settings', 'Settings']
