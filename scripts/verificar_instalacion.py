"""
Script de Prueba Rápida
Verifica que todos los módulos estén instalados correctamente.
"""

import sys

print("="*70)
print("VERIFICACIÓN DE INSTALACIÓN")
print("="*70)

# Verificar Python
print(f"\n✓ Python version: {sys.version}")

# Verificar OpenCV
try:
    import cv2
    print(f"✓ OpenCV instalado correctamente - Versión: {cv2.__version__}")
except ImportError as e:
    print(f"❌ Error al importar OpenCV: {e}")
    sys.exit(1)

# Verificar NumPy
try:
    import numpy as np
    print(f"✓ NumPy instalado correctamente - Versión: {np.__version__}")
except ImportError as e:
    print(f"❌ Error al importar NumPy: {e}")
    sys.exit(1)

# Verificar Matplotlib
try:
    import matplotlib
    print(f"✓ Matplotlib instalado correctamente - Versión: {matplotlib.__version__}")
except ImportError as e:
    print(f"❌ Error al importar Matplotlib: {e}")
    sys.exit(1)

print("\n" + "="*70)
print("¡TODAS LAS DEPENDENCIAS INSTALADAS CORRECTAMENTE!")
print("="*70)

print("\n📚 Ejercicios disponibles:")
print("  1. ejercicio1_gamma.py       - Corrección de gamma")
print("  2. ejercicio2_redimensionar.py - Redimensionar imagen")
print("  3. ejercicio3_rotacion.py    - Rotación de imagen")
print("  4. ejercicio4_texto.py       - Texto en imagen")

print("\n💡 Para ejecutar un ejercicio, usa:")
print('   python ejercicio1_gamma.py')
print('   python ejercicio2_redimensionar.py')
print('   python ejercicio3_rotacion.py')
print('   python ejercicio4_texto.py')

print("\n📖 Consulta el archivo README.md para más información.")
print("="*70)
