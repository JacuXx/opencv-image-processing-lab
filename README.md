# Procesamiento de Imágenes con OpenCV

Proyecto educativo de procesamiento de imágenes usando OpenCV y Python.

## 📋 Descripción

Este proyecto contiene ejercicios prácticos y una biblioteca reutilizable para procesamiento de imágenes con OpenCV. Incluye funcionalidades para ajuste de gamma, redimensionamiento, rotación y adición de texto a imágenes.

## 🏗️ Estructura del Proyecto

```
Practica Inteligencia/
│
├── src/                          # Código fuente principal
│   ├── core/                     # Funcionalidades centrales
│   │   ├── image_processor.py   # Clase base para procesadores
│   │   └── utils.py              # Utilidades compartidas
│   │
│   ├── processors/               # Procesadores específicos
│   │   ├── gamma_adjuster.py    # Ajuste de gamma
│   │   ├── resizer.py            # Redimensionamiento
│   │   ├── rotator.py            # Rotación
│   │   └── text_overlay.py      # Texto en imágenes
│   │
│   ├── io/                       # Entrada/Salida
│   │   ├── image_loader.py      # Carga de imágenes
│   │   └── image_saver.py       # Guardado de imágenes
│   │
│   └── visualization/            # Visualización
│       └── displayer.py          # Visualización de imágenes
│
├── ejercicios/                   # Scripts de ejercicios
│   ├── ejercicio1_gamma.py
│   ├── ejercicio2_redimensionar.py
│   ├── ejercicio3_rotacion.py
│   └── ejercicio4_texto.py
│
├── tests/                        # Pruebas unitarias
│
├── data/                         # Datos del proyecto
│   ├── input/                    # Imágenes de entrada
│   ├── output/                   # Resultados procesados
│   └── samples/                  # Imágenes de ejemplo
│
├── scripts/                      # Scripts auxiliares
│   ├── generar_imagenes_ejemplo.py
│   └── verificar_instalacion.py
│
├── config/                       # Configuraciones
│   └── settings.py
│
└── docs/                         # Documentación
```

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación de Dependencias

```bash
# Crear entorno virtual (recomendado)
python -m venv .venv

# Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## 📦 Uso

### Uso como Biblioteca

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

```bash
# Ejecutar todos los tests
pytest tests/

# Ejecutar con cobertura
pytest --cov=src tests/
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

Este proyecto es educativo y de código abierto.

## 👥 Autor

Tu Nombre

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request.
