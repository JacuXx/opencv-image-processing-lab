"""
Ejercicio 2: Modificación de Tamaño de Imagen
Este programa modifica el tamaño de una imagen y muestra sus propiedades (Shape).
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


def mostrar_propiedades_imagen(imagen, titulo="Imagen"):
    """
    Muestra las propiedades de una imagen.
    
    Args:
        imagen: Imagen a analizar
        titulo: Título descriptivo de la imagen
    """
    print(f"\n{titulo}:")
    print(f"  • Shape (Forma): {imagen.shape}")
    
    if len(imagen.shape) == 3:
        altura, ancho, canales = imagen.shape
        print(f"  • Altura: {altura} píxeles")
        print(f"  • Ancho: {ancho} píxeles")
        print(f"  • Canales: {canales}")
    else:
        altura, ancho = imagen.shape
        print(f"  • Altura: {altura} píxeles")
        print(f"  • Ancho: {ancho} píxeles")
        print(f"  • Canales: 1 (Escala de grises)")
    
    print(f"  • Tipo de datos: {imagen.dtype}")
    print(f"  • Tamaño total (píxeles): {imagen.size}")
    print(f"  • Tamaño en memoria: {imagen.nbytes} bytes ({imagen.nbytes / 1024:.2f} KB)")


def redimensionar_imagen(ruta_imagen):
    """
    Redimensiona una imagen y muestra las propiedades antes y después.
    
    Args:
        ruta_imagen: Ruta de la imagen a redimensionar
    """
    # Cargar la imagen
    imagen = cv2.imread(ruta_imagen)
    
    if imagen is None:
        print(f"Error: No se pudo cargar la imagen '{ruta_imagen}'")
        print("Por favor, asegúrate de que el archivo existe.")
        return
    
    # Convertir de BGR a RGB para matplotlib
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    
    print("\n" + "="*70)
    print("PROPIEDADES DE LA IMAGEN ORIGINAL")
    print("="*70)
    mostrar_propiedades_imagen(imagen_rgb, "Imagen Original")
    
    # Solicitar nuevas dimensiones
    print("\n" + "="*70)
    print("OPCIONES DE REDIMENSIONAMIENTO")
    print("="*70)
    print("\n1. Especificar ancho y alto manualmente")
    print("2. Escalar por porcentaje")
    print("3. Tamaños predefinidos (320x240, 640x480, 800x600, 1024x768)")
    
    opcion = input("\nSeleccione una opción (1-3): ").strip()
    
    if opcion == "1":
        # Opción manual
        try:
            nuevo_ancho = int(input("Ingrese el nuevo ancho (píxeles): "))
            nuevo_alto = int(input("Ingrese el nuevo alto (píxeles): "))
        except ValueError:
            print("Error: Debe ingresar números enteros válidos.")
            return
    
    elif opcion == "2":
        # Escalar por porcentaje
        try:
            escala = float(input("Ingrese el porcentaje de escala (ej: 50 para 50%, 200 para 200%): "))
            factor = escala / 100.0
            alto_original, ancho_original = imagen.shape[:2]
            nuevo_ancho = int(ancho_original * factor)
            nuevo_alto = int(alto_original * factor)
        except ValueError:
            print("Error: Debe ingresar un número válido.")
            return
    
    elif opcion == "3":
        # Tamaños predefinidos
        print("\nTamaños disponibles:")
        print("1. 320x240 (QVGA)")
        print("2. 640x480 (VGA)")
        print("3. 800x600 (SVGA)")
        print("4. 1024x768 (XGA)")
        
        sub_opcion = input("Seleccione un tamaño (1-4): ").strip()
        tamaños = {
            "1": (320, 240),
            "2": (640, 480),
            "3": (800, 600),
            "4": (1024, 768)
        }
        
        if sub_opcion in tamaños:
            nuevo_ancho, nuevo_alto = tamaños[sub_opcion]
        else:
            print("Opción no válida.")
            return
    else:
        print("Opción no válida.")
        return
    
    # Validar dimensiones
    if nuevo_ancho <= 0 or nuevo_alto <= 0:
        print("Error: Las dimensiones deben ser mayores a 0.")
        return
    
    # Redimensionar la imagen
    print(f"\nRedimensionando imagen a {nuevo_ancho}x{nuevo_alto}...")
    imagen_redimensionada = cv2.resize(imagen_rgb, (nuevo_ancho, nuevo_alto), 
                                       interpolation=cv2.INTER_LINEAR)
    
    print("\n" + "="*70)
    print("PROPIEDADES DE LA IMAGEN REDIMENSIONADA")
    print("="*70)
    mostrar_propiedades_imagen(imagen_redimensionada, "Imagen Redimensionada")
    
    # Calcular el factor de cambio
    alto_original, ancho_original = imagen_rgb.shape[:2]
    factor_ancho = (nuevo_ancho / ancho_original) * 100
    factor_alto = (nuevo_alto / alto_original) * 100
    
    print(f"\n  • Factor de cambio en ancho: {factor_ancho:.2f}%")
    print(f"  • Factor de cambio en alto: {factor_alto:.2f}%")
    
    # Mostrar comparación
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    fig.suptitle('Comparación: Original vs Redimensionada', fontsize=16, fontweight='bold')
    
    axes[0].imshow(imagen_rgb)
    axes[0].set_title(f'Original\n{ancho_original}x{alto_original}', fontsize=12, fontweight='bold')
    axes[0].axis('off')
    
    axes[1].imshow(imagen_redimensionada)
    axes[1].set_title(f'Redimensionada\n{nuevo_ancho}x{nuevo_alto}', fontsize=12, fontweight='bold')
    axes[1].axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # Guardar imagen redimensionada
    guardar = input("\n¿Desea guardar la imagen redimensionada? (s/n): ").strip().lower()
    if guardar == 's':
        nombre_archivo = f"imagen_redimensionada_{nuevo_ancho}x{nuevo_alto}.jpg"
        imagen_bgr = cv2.cvtColor(imagen_redimensionada, cv2.COLOR_RGB2BGR)
        cv2.imwrite(nombre_archivo, imagen_bgr)
        print(f"Imagen guardada como: {nombre_archivo}")


def crear_imagen_ejemplo():
    """
    Crea una imagen de ejemplo para demostración.
    """
    print("Creando imagen de ejemplo...")
    
    # Crear una imagen colorida de 800x600
    altura, ancho = 600, 800
    imagen = np.zeros((altura, ancho, 3), dtype=np.uint8)
    
    # Crear gradientes de colores
    for i in range(altura):
        for j in range(ancho):
            r = int((i / altura) * 255)
            g = int((j / ancho) * 255)
            b = int(((i + j) / (altura + ancho)) * 255)
            imagen[i, j] = [b, g, r]
    
    # Añadir formas
    cv2.rectangle(imagen, (100, 100), (350, 300), (0, 255, 255), -1)
    cv2.circle(imagen, (600, 400), 100, (255, 0, 255), -1)
    cv2.putText(imagen, 'Ejemplo', (300, 450), cv2.FONT_HERSHEY_SIMPLEX, 
                2, (255, 255, 255), 3)
    
    # Guardar la imagen
    cv2.imwrite('imagen_ejemplo_redimensionar.jpg', imagen)
    print("Imagen de ejemplo creada: 'imagen_ejemplo_redimensionar.jpg'")
    return 'imagen_ejemplo_redimensionar.jpg'


def main():
    """
    Función principal del programa.
    """
    print("="*70)
    print("EJERCICIO 2: MODIFICACIÓN DE TAMAÑO DE IMAGEN")
    print("="*70)
    print("\nEste programa modifica el tamaño de una imagen")
    print("y muestra sus propiedades (Shape).\n")
    
    ruta_imagen = input("Ingrese la ruta de la imagen\n(o presione Enter para usar imagen de ejemplo): ").strip()
    
    if not ruta_imagen or ruta_imagen == "":
        ruta_imagen = crear_imagen_ejemplo()
    
    redimensionar_imagen(ruta_imagen)
    
    print("\n¡Proceso completado!")


if __name__ == "__main__":
    main()
