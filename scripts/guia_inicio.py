"""
Guía de Inicio Rápido
Este script proporciona una guía interactiva para ejecutar los ejercicios.
"""

import sys


def mostrar_menu():
    """Muestra el menú principal."""
    print("\n" + "="*70)
    print("PRÁCTICA DE INTELIGENCIA ARTIFICIAL - PROCESAMIENTO DE IMÁGENES")
    print("="*70)
    print("\n📚 EJERCICIOS DISPONIBLES:\n")
    print("  1. Corrección de Gamma")
    print("     - Corrige imágenes con mucha o poca luz")
    print("     - Muestra 3+ correcciones diferentes")
    print("     - Archivo: ejercicio1_gamma.py\n")
    
    print("  2. Redimensionar Imagen")
    print("     - Modifica el tamaño de imágenes")
    print("     - Muestra propiedades (Shape)")
    print("     - Archivo: ejercicio2_redimensionar.py\n")
    
    print("  3. Rotación de Imagen")
    print("     - Rota imágenes según grados especificados")
    print("     - Validación de entrada")
    print("     - Archivo: ejercicio3_rotacion.py\n")
    
    print("  4. Texto en Imagen")
    print("     - Agrega texto personalizado a imágenes")
    print("     - Menú interactivo (letra, color, coordenadas)")
    print("     - Archivo: ejercicio4_texto.py\n")
    
    print("  5. Ejecutar Todos (Demostración)")
    print("     - Ejecuta una demostración de todos los ejercicios\n")
    
    print("  0. Salir\n")
    print("="*70)


def ejecutar_ejercicio(numero):
    """Ejecuta un ejercicio específico."""
    import subprocess
    import os
    
    python_exe = r"C:/Users/alane/Desktop/Practica Inteligencia/.venv/Scripts/python.exe"
    base_path = r"c:\Users\alane\Desktop\Practica Inteligencia"
    
    ejercicios = {
        1: "ejercicio1_gamma.py",
        2: "ejercicio2_redimensionar.py",
        3: "ejercicio3_rotacion.py",
        4: "ejercicio4_texto.py"
    }
    
    if numero in ejercicios:
        archivo = ejercicios[numero]
        ruta_completa = os.path.join(base_path, archivo)
        
        print(f"\n{'='*70}")
        print(f"Ejecutando: {archivo}")
        print(f"{'='*70}\n")
        
        try:
            subprocess.run([python_exe, ruta_completa], check=True)
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Error al ejecutar el ejercicio: {e}")
        except FileNotFoundError:
            print(f"\n❌ Error: No se encontró el archivo {archivo}")
    else:
        print("\n❌ Número de ejercicio no válido")


def mostrar_instrucciones():
    """Muestra instrucciones de uso."""
    print("\n" + "="*70)
    print("INSTRUCCIONES DE USO")
    print("="*70)
    print("\n📝 Cada ejercicio puede:")
    print("   • Usar una imagen que proporciones (ingresa la ruta)")
    print("   • Generar automáticamente una imagen de ejemplo\n")
    
    print("💡 Comandos manuales:")
    print("   python ejercicio1_gamma.py")
    print("   python ejercicio2_redimensionar.py")
    print("   python ejercicio3_rotacion.py")
    print("   python ejercicio4_texto.py\n")
    
    print("📖 Para más detalles, consulta el archivo README.md")
    print("="*70)


def main():
    """Función principal."""
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (0-5): ").strip()
        
        if opcion == '0':
            print("\n¡Hasta luego!")
            break
        elif opcion in ['1', '2', '3', '4']:
            ejecutar_ejercicio(int(opcion))
        elif opcion == '5':
            print("\n" + "="*70)
            print("DEMOSTRACIÓN DE TODOS LOS EJERCICIOS")
            print("="*70)
            print("\nEjecutando todos los ejercicios en secuencia...")
            print("Cada ejercicio usará sus imágenes de ejemplo.\n")
            input("Presione Enter para comenzar...")
            
            for i in range(1, 5):
                ejecutar_ejercicio(i)
                if i < 4:
                    input(f"\nPresione Enter para continuar con el ejercicio {i+1}...")
        elif opcion == 'i':
            mostrar_instrucciones()
        else:
            print("\n❌ Opción no válida. Por favor seleccione 0-5.")
        
        input("\nPresione Enter para volver al menú principal...")


if __name__ == "__main__":
    print("="*70)
    print("GUÍA DE INICIO RÁPIDO")
    print("="*70)
    print("\n✓ Todas las dependencias están instaladas")
    print("✓ 4 ejercicios disponibles")
    print("✓ Cada ejercicio incluye imágenes de ejemplo\n")
    
    continuar = input("¿Desea continuar al menú principal? (s/n): ").strip().lower()
    
    if continuar == 's' or continuar == '':
        main()
    else:
        print("\nPara ejecutar este menú nuevamente, use:")
        print("   python guia_inicio.py")
        print("\nO ejecute los ejercicios directamente:")
        print("   python ejercicio1_gamma.py")
        print("   python ejercicio2_redimensionar.py")
        print("   python ejercicio3_rotacion.py")
        print("   python ejercicio4_texto.py")
