"""
Setup script para instalar el paquete de procesamiento de imágenes.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Leer el README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="procesamiento-imagenes",
    version="1.0.0",
    author="Tu Nombre",
    author_email="tu@email.com",
    description="Biblioteca de procesamiento de imágenes con OpenCV",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tuusuario/practica-inteligencia",
    packages=find_packages(include=['src', 'src.*', 'config']),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.8.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
)
