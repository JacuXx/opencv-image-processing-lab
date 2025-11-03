"""
Script de verificación de la estructura del proyecto.
"""

from pathlib import Path
import sys


def verificar_estructura():
    """Verifica que todos los archivos y carpetas estén en su lugar."""
    
    print("="*70)
    print("VERIFICACIÓN DE LA ESTRUCTURA DEL PROYECTO")
    print("="*70)
    
    root = Path(__file__).parent
    
    # Directorios esperados
    directorios = [
        "src",
        "src/core",
        "src/processors",
        "src/io",
        "src/visualization",
        "ejercicios",
        "tests",
        "data",
        "data/input",
        "data/output",
        "data/samples",
        "scripts",
        "config",
        "docs",
    ]
    
    # Archivos esperados
    archivos = [
        "README.md",
        "requirements.txt",
        "setup.py",
        ".gitignore",
        "src/__init__.py",
        "src/core/__init__.py",
        "src/core/utils.py",
        "src/core/image_processor.py",
        "src/processors/__init__.py",
        "src/processors/gamma_adjuster.py",
        "src/processors/resizer.py",
        "src/processors/rotator.py",
        "src/processors/text_overlay.py",
        "src/io/__init__.py",
        "src/io/image_loader.py",
        "src/io/image_saver.py",
        "src/visualization/__init__.py",
        "src/visualization/displayer.py",
        "config/__init__.py",
        "config/settings.py",
        "ejercicios/__init__.py",
        "ejercicios/ejemplo_arquitectura.py",
        "tests/__init__.py",
        "tests/test_utils.py",
    ]
    
    print("\n📁 Verificando directorios...")
    errores_dir = 0
    for directorio in directorios:
        path = root / directorio
        if path.exists() and path.is_dir():
            print(f"  ✅ {directorio}")
        else:
            print(f"  ❌ {directorio} - NO ENCONTRADO")
            errores_dir += 1
    
    print(f"\n📄 Verificando archivos...")
    errores_arch = 0
    for archivo in archivos:
        path = root / archivo
        if path.exists() and path.is_file():
            print(f"  ✅ {archivo}")
        else:
            print(f"  ❌ {archivo} - NO ENCONTRADO")
            errores_arch += 1
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70)
    print(f"Directorios verificados: {len(directorios)}")
    print(f"Directorios correctos: {len(directorios) - errores_dir}")
    print(f"Directorios faltantes: {errores_dir}")
    print()
    print(f"Archivos verificados: {len(archivos)}")
    print(f"Archivos correctos: {len(archivos) - errores_arch}")
    print(f"Archivos faltantes: {errores_arch}")
    print("="*70)
    
    if errores_dir == 0 and errores_arch == 0:
        print("\n🎉 ¡ESTRUCTURA COMPLETAMENTE CORRECTA!")
        print("El proyecto está listo para usar.")
        return True
    else:
        print(f"\n⚠️ Se encontraron {errores_dir + errores_arch} problemas.")
        print("Por favor, revise los elementos faltantes.")
        return False


def mostrar_arbol():
    """Muestra un árbol visual de la estructura."""
    
    print("\n\n" + "="*70)
    print("ÁRBOL DE ESTRUCTURA DEL PROYECTO")
    print("="*70)
    
    estructura = """
Practica Inteligencia/
│
├── 📁 src/                      # Código fuente principal
│   ├── 📁 core/                 # Funcionalidades centrales
│   │   ├── image_processor.py
│   │   ├── utils.py
│   │   └── __init__.py
│   │
│   ├── 📁 processors/           # Procesadores específicos
│   │   ├── gamma_adjuster.py
│   │   ├── resizer.py
│   │   ├── rotator.py
│   │   ├── text_overlay.py
│   │   └── __init__.py
│   │
│   ├── 📁 io/                   # Entrada/Salida
│   │   ├── image_loader.py
│   │   ├── image_saver.py
│   │   └── __init__.py
│   │
│   ├── 📁 visualization/        # Visualización
│   │   ├── displayer.py
│   │   └── __init__.py
│   │
│   └── __init__.py
│
├── 📁 ejercicios/               # Scripts de ejercicios
│   ├── ejemplo_arquitectura.py
│   ├── ejercicio1_gamma.py
│   ├── ejercicio2_redimensionar.py
│   ├── ejercicio3_rotacion.py
│   ├── ejercicio4_texto.py
│   └── __init__.py
│
├── 📁 tests/                    # Pruebas unitarias
│   ├── test_utils.py
│   └── __init__.py
│
├── 📁 data/                     # Datos del proyecto
│   ├── 📁 input/                # Imágenes de entrada
│   ├── 📁 output/               # Resultados procesados
│   └── 📁 samples/              # Imágenes de ejemplo
│
├── 📁 scripts/                  # Scripts auxiliares
│   ├── generar_imagenes_ejemplo.py
│   ├── guia_inicio.py
│   └── verificar_instalacion.py
│
├── 📁 config/                   # Configuraciones
│   ├── settings.py
│   └── __init__.py
│
├── 📁 docs/                     # Documentación
│
├── 📄 README.md                 # Documentación principal
├── 📄 requirements.txt          # Dependencias
├── 📄 setup.py                  # Instalación del paquete
└── 📄 .gitignore                # Git ignore
    """
    
    print(estructura)
    print("="*70)


def mostrar_siguientes_pasos():
    """Muestra los siguientes pasos recomendados."""
    
    print("\n\n" + "="*70)
    print("🚀 PRÓXIMOS PASOS RECOMENDADOS")
    print("="*70)
    
    pasos = [
        "1. Probar el ejemplo de arquitectura:",
        "   python ejercicios/ejemplo_arquitectura.py",
        "",
        "2. Ejecutar los ejercicios refactorizados (cuando estén listos)",
        "",
        "3. Instalar el paquete en modo desarrollo:",
        "   pip install -e .",
        "",
        "4. Ejecutar los tests:",
        "   pytest tests/ -v",
        "",
        "5. Agregar más procesadores según necesites",
        "",
        "6. Crear tu propia documentación en docs/",
    ]
    
    for paso in pasos:
        print(paso)
    
    print("="*70)


if __name__ == "__main__":
    estructura_ok = verificar_estructura()
    mostrar_arbol()
    
    if estructura_ok:
        mostrar_siguientes_pasos()
    
    sys.exit(0 if estructura_ok else 1)
