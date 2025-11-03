"""
Módulo para visualizar imágenes con matplotlib y OpenCV.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import Union, List, Tuple, Optional

from ..core.utils import validate_image, bgr_to_rgb


class ImageDisplayer:
    """
    Clase para visualizar imágenes de diferentes formas.
    """
    
    def __init__(self, use_rgb: bool = True):
        """
        Inicializa el visualizador.
        
        Args:
            use_rgb: Si True, convierte BGR a RGB automáticamente
        """
        self.use_rgb = use_rgb
    
    def show(
        self,
        image: np.ndarray,
        title: str = "Imagen",
        figsize: Tuple[int, int] = (10, 8),
        cmap: Optional[str] = None
    ) -> None:
        """
        Muestra una imagen usando matplotlib.
        
        Args:
            image: Imagen a mostrar
            title: Título de la imagen
            figsize: Tamaño de la figura
            cmap: Colormap (para imágenes en escala de grises)
        """
        if not validate_image(image):
            print("❌ Error: Imagen inválida")
            return
        
        plt.figure(figsize=figsize)
        
        # Convertir BGR a RGB si es necesario
        display_image = self._prepare_image(image)
        
        # Determinar colormap
        if cmap is None and len(display_image.shape) == 2:
            cmap = 'gray'
        
        plt.imshow(display_image, cmap=cmap)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    def show_multiple(
        self,
        images: Union[List[np.ndarray], dict],
        titles: Optional[List[str]] = None,
        rows: Optional[int] = None,
        cols: Optional[int] = None,
        figsize: Tuple[int, int] = (15, 10),
        main_title: Optional[str] = None
    ) -> None:
        """
        Muestra múltiples imágenes en una grilla.
        
        Args:
            images: Lista o diccionario de imágenes
            titles: Lista de títulos (opcional)
            rows: Número de filas (calculado automáticamente si es None)
            cols: Número de columnas (calculado automáticamente si es None)
            figsize: Tamaño de la figura
            main_title: Título principal de la figura
        """
        # Convertir diccionario a lista si es necesario
        if isinstance(images, dict):
            if titles is None:
                titles = list(images.keys())
            images = list(images.values())
        
        num_images = len(images)
        
        if num_images == 0:
            print("❌ No hay imágenes para mostrar")
            return
        
        # Calcular filas y columnas si no se especifican
        if rows is None and cols is None:
            cols = int(np.ceil(np.sqrt(num_images)))
            rows = int(np.ceil(num_images / cols))
        elif rows is None:
            rows = int(np.ceil(num_images / cols))
        elif cols is None:
            cols = int(np.ceil(num_images / rows))
        
        # Crear figura
        fig, axes = plt.subplots(rows, cols, figsize=figsize)
        
        if main_title:
            fig.suptitle(main_title, fontsize=16, fontweight='bold')
        
        # Aplanar axes si es necesario
        if rows * cols > 1:
            axes = axes.flatten()
        else:
            axes = [axes]
        
        # Mostrar imágenes
        for idx in range(rows * cols):
            ax = axes[idx]
            
            if idx < num_images:
                image = self._prepare_image(images[idx])
                
                # Determinar colormap
                cmap = 'gray' if len(image.shape) == 2 else None
                
                ax.imshow(image, cmap=cmap)
                
                # Título
                if titles and idx < len(titles):
                    ax.set_title(titles[idx], fontsize=10, fontweight='bold')
            
            ax.axis('off')
        
        plt.tight_layout()
        plt.show()
    
    def compare(
        self,
        image1: np.ndarray,
        image2: np.ndarray,
        title1: str = "Imagen 1",
        title2: str = "Imagen 2",
        figsize: Tuple[int, int] = (15, 7)
    ) -> None:
        """
        Compara dos imágenes lado a lado.
        
        Args:
            image1: Primera imagen
            image2: Segunda imagen
            title1: Título de la primera imagen
            title2: Título de la segunda imagen
            figsize: Tamaño de la figura
        """
        self.show_multiple(
            [image1, image2],
            titles=[title1, title2],
            rows=1,
            cols=2,
            figsize=figsize
        )
    
    def show_with_histogram(
        self,
        image: np.ndarray,
        title: str = "Imagen",
        figsize: Tuple[int, int] = (15, 5)
    ) -> None:
        """
        Muestra una imagen junto con su histograma.
        
        Args:
            image: Imagen a mostrar
            title: Título
            figsize: Tamaño de la figura
        """
        if not validate_image(image):
            print("❌ Error: Imagen inválida")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        fig.suptitle(title, fontsize=16, fontweight='bold')
        
        # Mostrar imagen
        display_image = self._prepare_image(image)
        cmap = 'gray' if len(display_image.shape) == 2 else None
        axes[0].imshow(display_image, cmap=cmap)
        axes[0].set_title("Imagen")
        axes[0].axis('off')
        
        # Mostrar histograma
        axes[1].set_title("Histograma")
        
        if len(image.shape) == 2:
            # Imagen en escala de grises
            hist = cv2.calcHist([image], [0], None, [256], [0, 256])
            axes[1].plot(hist, color='black')
            axes[1].set_xlim([0, 256])
        else:
            # Imagen en color
            colors = ('b', 'g', 'r')
            for i, color in enumerate(colors):
                hist = cv2.calcHist([image], [i], None, [256], [0, 256])
                axes[1].plot(hist, color=color, label=color.upper())
            axes[1].legend()
            axes[1].set_xlim([0, 256])
        
        axes[1].set_xlabel('Valor de píxel')
        axes[1].set_ylabel('Frecuencia')
        
        plt.tight_layout()
        plt.show()
    
    def show_opencv(
        self,
        image: np.ndarray,
        title: str = "Imagen",
        wait_key: int = 0
    ) -> None:
        """
        Muestra una imagen usando ventana de OpenCV.
        
        Args:
            image: Imagen a mostrar
            title: Título de la ventana
            wait_key: Tiempo de espera en ms (0 = esperar tecla)
        """
        if not validate_image(image):
            print("❌ Error: Imagen inválida")
            return
        
        cv2.imshow(title, image)
        cv2.waitKey(wait_key)
        cv2.destroyAllWindows()
    
    def _prepare_image(self, image: np.ndarray) -> np.ndarray:
        """
        Prepara una imagen para visualización.
        
        Args:
            image: Imagen a preparar
            
        Returns:
            Imagen preparada
        """
        if not validate_image(image):
            raise ValueError("Imagen inválida")
        
        # Si es imagen en color y use_rgb está activo, convertir
        if self.use_rgb and len(image.shape) == 3 and image.shape[2] == 3:
            return bgr_to_rgb(image)
        
        return image


__all__ = ['ImageDisplayer']
