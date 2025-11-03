# 🖼️ OpenCV Image Processing Lab

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> Un laboratorio completo de procesamiento de imágenes con OpenCV, diseñado para aprender y experimentar con técnicas de visión por computadora de forma práctica.

## 📋 Descripción

**OpenCV Image Processing Lab** es un proyecto educativo que combina ejercicios prácticos con una biblioteca modular y reutilizable para procesamiento de imágenes. Ideal para estudiantes, desarrolladores y entusiastas de la visión por computadora que desean aprender OpenCV de forma estructurada.

### ✨ Características Principales

- 🎨 **Procesadores Especializados**: Gamma, redimensionamiento, rotación, texto y más
- 🏗️ **Arquitectura Modular**: Código organizado y reutilizable siguiendo principios SOLID
- 📚 **Ejercicios Prácticos**: Scripts educativos paso a paso con explicaciones
- 🧪 **Tests Incluidos**: Pruebas unitarias para asegurar calidad del código
- 📊 **Visualización Avanzada**: Comparación de resultados, histogramas y más
- 🔧 **Fácil Extensión**: Agrega nuevos procesadores sin modificar código existente
- 📖 **Documentación Completa**: Ejemplos de uso y guías detalladas

## 🏗️ Estructura del Proyecto

```
opencv-image-processing-lab/
│
├── 📁 src/                          # Código fuente principal (biblioteca reutilizable)
│   ├── 📁 core/                     # Funcionalidades centrales
│   │   ├── image_processor.py      # Clase base abstracta para procesadores
│   │   ├── utils.py                 # Utilidades compartidas (validación, conversión, etc.)
│   │   └── __init__.py
│   │
│   ├── 📁 processors/               # Procesadores especializados
│   │   ├── gamma_adjuster.py       # Corrección de iluminación con gamma
│   │   ├── resizer.py               # Redimensionamiento con interpolación
│   │   ├── rotator.py               # Rotación y transformaciones
│   │   ├── text_overlay.py          # Superposición de texto
│   │   └── __init__.py
│   │
│   ├── 📁 io/                       # Entrada/Salida de imágenes
│   │   ├── image_loader.py          # Carga desde archivos/directorios
│   │   ├── image_saver.py           # Guardado en múltiples formatos
│   │   └── __init__.py
│   │
│   ├── 📁 visualization/            # Visualización de resultados
│   │   ├── displayer.py             # Matplotlib y OpenCV display
│   │   └── __init__.py
│   │
│   └── __init__.py
│
├── 📁 ejercicios/                   # Scripts de ejercicios prácticos
│   ├── ejemplo_arquitectura.py     # Demo completo de la arquitectura
│   ├── ejercicio1_gamma.py          # Corrección de gamma
│   ├── ejercicio2_redimensionar.py  # Redimensionamiento
│   ├── ejercicio3_rotacion.py       # Rotación de imágenes
│   ├── ejercicio4_texto.py          # Texto en imágenes
│   └── __init__.py
│
├── 📁 tests/                        # Pruebas unitarias
│   ├── test_utils.py                # Tests de utilidades
│   └── __init__.py
│
├── 📁 data/                         # Datos del proyecto
│   ├── 📁 input/                    # Imágenes de entrada
│   ├── 📁 output/                   # Resultados procesados
│   └── 📁 samples/                  # Imágenes de ejemplo
│
├── 📁 scripts/                      # Scripts auxiliares
│   ├── generar_imagenes_ejemplo.py # Generador de imágenes de prueba
│   ├── guia_inicio.py               # Guía interactiva
│   └── verificar_instalacion.py     # Verificador de dependencias
│
├── 📁 config/                       # Configuración
│   ├── settings.py                  # Configuración centralizada
│   └── __init__.py
│
├── 📁 docs/                         # Documentación adicional
│   ├── architecture.md              # Arquitectura del proyecto
│   ├── design-patterns.md           # Patrones de diseño aplicados
│   └── ...
│
├── 📄 README.md                     # Este archivo
├── 📄 requirements.txt              # Dependencias del proyecto
├── 📄 setup.py                      # Configuración de instalación
├── 📄 .gitignore                    # Archivos ignorados por git
├── 📄 LICENSE                       # Licencia del proyecto
└── 📄 verificar_estructura.py       # Script de verificación
```

## 🚀 Instalación

### Requisitos Previos

Asegúrate de tener instalado:

- **Python 3.8 o superior** ([Descargar aquí](https://www.python.org/downloads/))
- **pip** (incluido con Python)
- **git** (opcional, para clonar el repositorio)

### Instalación Paso a Paso

#### 1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/opencv-image-processing-lab.git
cd opencv-image-processing-lab
```

O descarga el ZIP desde GitHub y descomprímelo.

#### 2. Crear entorno virtual (Recomendado)

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 4. (Opcional) Instalar en modo desarrollo

Esto permite importar los módulos desde cualquier lugar:

```bash
pip install -e .
```

#### 5. Verificar instalación

```bash
python verificar_estructura.py
```

Si todo está correcto, verás: ✅ ¡ESTRUCTURA COMPLETAMENTE CORRECTA!

## ⚙️ Configuración

### Variables de Entorno

El proyecto utiliza configuración centralizada en `config/settings.py`. Puedes personalizar:

```python
# config/settings.py

# Rutas del proyecto (se configuran automáticamente)
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"

# Parámetros de procesamiento
DEFAULT_INTERPOLATION = 'linear'  # 'nearest', 'linear', 'cubic', 'area', 'lanczos'
DEFAULT_GAMMA = 1.0
DEFAULT_JPEG_QUALITY = 95         # 0-100
DEFAULT_PNG_COMPRESSION = 3       # 0-9

# Visualización
DEFAULT_FIGSIZE = (10, 8)
USE_RGB_CONVERSION = True         # Convertir BGR a RGB automáticamente
```

### Personalización

No necesitas variables de entorno. Todo se configura en `config/settings.py` o directamente en tu código:

```python
from config.settings import settings

# Ver configuración actual
settings.print_config()

# Usar rutas configuradas
input_path = settings.get_input_path("mi_imagen.jpg")
output_path = settings.get_output_path("resultado.jpg")
```

## 📦 Uso Rápido

### Ejemplo Básico

```python
from src.processors import GammaAdjuster, ImageResizer, ImageRotator, TextOverlay
from src.io import ImageLoader, ImageSaver
from src.visualization import ImageDisplayer

# Cargar imagen
loader = ImageLoader()
image = loader.load('data/input/mi_imagen.jpg')

# Ajustar gamma
gamma_adjuster = GammaAdjuster()
image_clara = gamma_adjuster.process(image, gamma=0.5)

# Redimensionar
resizer = ImageResizer()
image_pequena = resizer.process(image, width=800, maintain_aspect=True)

# Rotar
rotator = ImageRotator()
image_rotada = rotator.process(image, degrees=45)

# Agregar texto
text_overlay = TextOverlay()
image_con_texto = text_overlay.process(
    image, 
    "Hola Mundo", 
    position=(50, 100),
    font='simplex',
    color=(255, 0, 0)
)

# Guardar
saver = ImageSaver()
saver.save(image_con_texto, 'data/output/resultado.jpg')

# Visualizar
displayer = ImageDisplayer()
displayer.show(image_con_texto, title="Imagen Procesada")
```

### Ejecutar Ejercicios

```bash
# Ejercicio 1: Corrección de Gamma
python ejercicios/ejercicio1_gamma.py

# Ejercicio 2: Redimensionamiento
python ejercicios/ejercicio2_redimensionar.py

# Ejercicio 3: Rotación
python ejercicios/ejercicio3_rotacion.py

# Ejercicio 4: Texto en Imagen
python ejercicios/ejercicio4_texto.py
```

## 🧪 Tests

### Ejecutar Tests

El proyecto incluye tests unitarios usando pytest:

```bash
# Instalar pytest si no lo tienes
pip install pytest pytest-cov

# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar tests con cobertura
pytest --cov=src tests/

# Ejecutar un test específico
pytest tests/test_utils.py -v

# Generar reporte de cobertura HTML
pytest --cov=src --cov-report=html tests/
```

### Estructura de Tests

```python
# tests/test_utils.py
import pytest
from src.core.utils import validate_image, get_image_info

def test_validate_image():
    """Test de validación de imágenes"""
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    assert validate_image(image) is True
```

### Tests Disponibles

- ✅ `test_utils.py`: Tests de utilidades (validación, conversión, dimensiones)
- 🔜 `test_processors.py`: Tests de procesadores (próximamente)
- 🔜 `test_io.py`: Tests de entrada/salida (próximamente)

### Agregar Nuevos Tests

1. Crea un archivo `test_*.py` en la carpeta `tests/`
2. Importa `pytest` y los módulos a probar
3. Crea funciones que empiecen con `test_`
4. Usa `assert` para verificar comportamiento

```python
def test_gamma_adjustment():
    adjuster = GammaAdjuster()
    result = adjuster.process(image, gamma=0.5)
    assert result is not None
```

## 📚 Funcionalidades

### Procesadores

- **GammaAdjuster**: Ajuste de gamma para corrección de iluminación
- **ImageResizer**: Redimensionamiento con múltiples métodos de interpolación
- **ImageRotator**: Rotación y volteo de imágenes
- **TextOverlay**: Adición de texto con diferentes fuentes y estilos

### Utilidades

- **ImageLoader**: Carga de imágenes desde archivos
- **ImageSaver**: Guardado de imágenes en múltiples formatos
- **ImageDisplayer**: Visualización con matplotlib y OpenCV

## 🎯 Principios de Diseño

Este proyecto sigue principios de arquitectura limpia:

- **Separación de responsabilidades**: Cada módulo tiene una función específica
- **Reutilización**: Código modular y reutilizable
- **Extensibilidad**: Fácil agregar nuevos procesadores
- **Testabilidad**: Diseño que facilita las pruebas unitarias

## 📝 Licencia

Este proyecto está licenciado bajo la **Licencia MIT** - ver el archivo [LICENSE](LICENSE) para más detalles.

### ¿Qué significa esto?

✅ **Puedes:**
- Usar el código comercialmente
- Modificar el código
- Distribuir el código
- Uso privado

❌ **No puedes:**
- Responsabilizar a los autores
- Usar sin incluir la licencia y copyright

📋 **Debes:**
- Incluir la licencia y copyright en copias
- Documentar cambios significativos

---

## 👥 Créditos y Autores

### Autor Principal

**[Alan Reynoso Jacuinde]**
- 📧 Email: [alan.jxx@tutamail.com](mailto:alan.jxx@tutamail.com)
- 🐙 GitHub: [@JacuXx](https://github.com/JacuXx)
- 💼 LinkedIn: [Alan Reynoso Jacuinde](https://linkedin.com/in/alanrj-dev)

### Contribuidores

¿Quieres contribuir? ¡Las contribuciones son bienvenidas! Ver [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

<!-- Lista de contribuidores -->
<!-- Puedes usar https://github.com/all-contributors/all-contributors -->

### Agradecimientos

- **OpenCV Team**: Por la increíble biblioteca de visión por computadora
- **Python Community**: Por las herramientas y librerías
- **NumPy Team**: Por el manejo eficiente de arrays
- **Matplotlib Team**: Por las capacidades de visualización

### Tecnologías Utilizadas

Este proyecto fue construido con:

- [Python](https://www.python.org/) - Lenguaje de programación
- [OpenCV](https://opencv.org/) - Biblioteca de visión por computadora
- [NumPy](https://numpy.org/) - Computación numérica
- [Matplotlib](https://matplotlib.org/) - Visualización de datos

### Recursos de Aprendizaje

- 📖 [Documentación oficial de OpenCV](https://docs.opencv.org/)
- 📚 [OpenCV-Python Tutorials](https://docs.opencv.org/master/d6/d00/tutorial_py_root.html)
- 🎥 [PyImageSearch](https://www.pyimagesearch.com/)
- 📘 [Computer Vision: Algorithms and Applications](http://szeliski.org/Book/)

---

## 🤝 Contribuir

¡Las contribuciones son lo que hace que la comunidad de código abierto sea un lugar increíble! Cualquier contribución que hagas será **muy apreciada**.

### Cómo Contribuir

1. **Fork** el proyecto
2. Crea tu **Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. Abre un **Pull Request**

### Tipos de Contribuciones

- 🐛 Reportar bugs
- 💡 Sugerir nuevas características
- 📝 Mejorar documentación
- 🧪 Agregar tests
- ✨ Implementar nuevos procesadores
- 🎨 Mejorar ejemplos

### Código de Conducta

Este proyecto sigue el [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).

---

## 📞 Contacto y Soporte

### ¿Necesitas Ayuda?

- 📖 Revisa la [Documentación](docs/)
- 🐛 [Reporta un bug](https://github.com/tuusuario/opencv-image-processing-lab/issues)
- 💬 [Inicia una discusión](https://github.com/tuusuario/opencv-image-processing-lab/discussions)
- 📧 Email: [alan.jxx@tutamail.com](mailto:alan.jxx@tutamail.com)

### Estado del Proyecto

![GitHub last commit](https://img.shields.io/github/last-commit/tuusuario/opencv-image-processing-lab)
![GitHub issues](https://img.shields.io/github/issues/tuusuario/opencv-image-processing-lab)
![GitHub pull requests](https://img.shields.io/github/issues-pr/tuusuario/opencv-image-processing-lab)
![GitHub stars](https://img.shields.io/github/stars/tuusuario/opencv-image-processing-lab)

---

## 🎓 Aprende Más

### Tutoriales Relacionados

- [Guía de Arquitectura](docs/architecture.md)
- [Patrones de Diseño](docs/design-patterns.md)
- [Principios SOLID](docs/solid-principles.md)

### Proyectos Relacionados

- [opencv/opencv](https://github.com/opencv/opencv) - OpenCV oficial
- [PyImageSearch](https://github.com/PyImageSearch) - Tutoriales y código

---

<div align="center">

**⭐ Si este proyecto te fue útil, considera darle una estrella ⭐**

Hecho con ❤️ por [Alan Reynoso Jacuinde]

[⬆ Volver arriba](#-opencv-image-processing-lab)

</div>
