"""
Tests para el módulo de utilidades.
"""

import pytest
import numpy as np
import cv2
from src.core.utils import (
    validate_image,
    get_image_info,
    ensure_color,
    bgr_to_rgb,
    calculate_aspect_ratio,
    get_new_dimensions,
)


class TestValidateImage:
    """Tests para validate_image"""
    
    def test_valid_color_image(self):
        """Test con imagen válida en color"""
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        assert validate_image(image) is True
    
    def test_valid_grayscale_image(self):
        """Test con imagen válida en escala de grises"""
        image = np.zeros((100, 100), dtype=np.uint8)
        assert validate_image(image) is True
    
    def test_none_image(self):
        """Test con imagen None"""
        assert validate_image(None) is False
    
    def test_invalid_type(self):
        """Test con tipo inválido"""
        assert validate_image("not an image") is False
    
    def test_invalid_shape(self):
        """Test con shape inválido"""
        image = np.zeros((100,), dtype=np.uint8)  # 1D
        assert validate_image(image) is False


class TestGetImageInfo:
    """Tests para get_image_info"""
    
    def test_color_image_info(self):
        """Test información de imagen en color"""
        image = np.zeros((100, 200, 3), dtype=np.uint8)
        info = get_image_info(image)
        
        assert info['height'] == 100
        assert info['width'] == 200
        assert info['channels'] == 3
        assert info['color_mode'] == 'Color'
    
    def test_grayscale_image_info(self):
        """Test información de imagen en escala de grises"""
        image = np.zeros((100, 200), dtype=np.uint8)
        info = get_image_info(image)
        
        assert info['height'] == 100
        assert info['width'] == 200
        assert info['channels'] == 1
        assert info['color_mode'] == 'Grayscale'
    
    def test_invalid_image_raises_error(self):
        """Test que lanza error con imagen inválida"""
        with pytest.raises(ValueError):
            get_image_info(None)


class TestEnsureColor:
    """Tests para ensure_color"""
    
    def test_grayscale_to_color(self):
        """Test conversión de escala de grises a color"""
        gray = np.zeros((100, 100), dtype=np.uint8)
        color = ensure_color(gray)
        
        assert len(color.shape) == 3
        assert color.shape[2] == 3
    
    def test_already_color(self):
        """Test con imagen ya en color"""
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        result = ensure_color(image)
        
        assert result.shape == image.shape


class TestCalculateAspectRatio:
    """Tests para calculate_aspect_ratio"""
    
    def test_landscape_aspect(self):
        """Test aspect ratio horizontal"""
        ratio = calculate_aspect_ratio(800, 600)
        assert ratio == pytest.approx(1.333, rel=0.01)
    
    def test_portrait_aspect(self):
        """Test aspect ratio vertical"""
        ratio = calculate_aspect_ratio(600, 800)
        assert ratio == pytest.approx(0.75, rel=0.01)
    
    def test_square_aspect(self):
        """Test aspect ratio cuadrado"""
        ratio = calculate_aspect_ratio(800, 800)
        assert ratio == 1.0
    
    def test_zero_height(self):
        """Test con altura cero"""
        ratio = calculate_aspect_ratio(800, 0)
        assert ratio == 0


class TestGetNewDimensions:
    """Tests para get_new_dimensions"""
    
    def test_scale_factor(self):
        """Test redimensionamiento por factor de escala"""
        width, height = get_new_dimensions(100, 100, scale_factor=2.0)
        assert width == 200
        assert height == 200
    
    def test_target_width_only(self):
        """Test solo con ancho objetivo"""
        width, height = get_new_dimensions(100, 100, target_width=200)
        assert width == 200
        assert height == 200
    
    def test_target_height_only(self):
        """Test solo con altura objetivo"""
        width, height = get_new_dimensions(100, 100, target_height=200)
        assert width == 200
        assert height == 200
    
    def test_both_dimensions_maintain_aspect(self):
        """Test con ambas dimensiones manteniendo aspecto"""
        width, height = get_new_dimensions(
            200, 100, 
            target_width=400, 
            target_height=400,
            maintain_aspect=True
        )
        # Debería ajustar para mantener aspecto 2:1
        assert width <= 400
        assert height <= 400
    
    def test_no_parameters(self):
        """Test sin parámetros retorna dimensiones originales"""
        width, height = get_new_dimensions(100, 100)
        assert width == 100
        assert height == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
