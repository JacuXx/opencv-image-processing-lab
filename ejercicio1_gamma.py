"""
Ejercicio 1: Corrección de Gamma en Imágenes
Este programa corrige imágenes con mucha o poca luz usando la función adjust_gamma.
Muestra 3 diferentes correcciones y permite determinar la mejor.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


def adjust_gamma(image, gamma=1.0):
    """
    Ajusta el gamma de una imagen.
    
    Args:
        image: Imagen de entrada
        gamma: Valor de gamma (< 1 aclara, > 1 oscurece)
    
    Returns:
        Imagen con gamma ajustado
    """
    # Construir tabla de lookup para mapear valores de píxeles
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    
    # Aplicar la transformación gamma usando la tabla de lookup
    return cv2.LUT(image, table)


def corregir_imagen_con_gamma(ruta_imagen):
    """
    Carga una imagen y aplica diferentes valores de gamma para corregirla.
    
    Args:
        ruta_imagen: Ruta de la imagen a corregir
    """
    # Cargar la imagen
    imagen = cv2.imread(ruta_imagen)
    
    if imagen is None:
        print(f"Error: No se pudo cargar la imagen '{ruta_imagen}'")
        print("Por favor, asegúrate de que el archivo existe.")
        return
    
    # Convertir de BGR a RGB para matplotlib
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    
    # Aplicar diferentes valores de gamma
    # Gamma < 1: Aclara la imagen (útil para imágenes oscuras)
    # Gamma > 1: Oscurece la imagen (útil para imágenes muy claras)
    gamma_valores = [0.5, 1.0, 1.5, 2.0]
    
    # Crear figura para mostrar resultados
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Corrección de Gamma en Imagen', fontsize=16, fontweight='bold')
    
    # Mostrar imágenes con diferentes gammas
    for idx, gamma in enumerate(gamma_valores):
        row = idx // 2
        col = idx % 2
        
        if gamma == 1.0:
            imagen_corregida = imagen_rgb
            titulo = f'Imagen Original (Gamma = {gamma})'
        else:
            imagen_corregida_bgr = adjust_gamma(imagen, gamma)
            imagen_corregida = cv2.cvtColor(imagen_corregida_bgr, cv2.COLOR_BGR2RGB)
            titulo = f'Gamma = {gamma}'
        
        axes[row, col].imshow(imagen_corregida)
        axes[row, col].set_title(titulo, fontsize=12, fontweight='bold')
        axes[row, col].axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # Análisis de las correcciones
    print("\n" + "="*70)
    print("ANÁLISIS DE CORRECCIONES DE GAMMA")
    print("="*70)
    print("\nValores de Gamma aplicados:")
    print("  • Gamma = 0.5  → Aclara la imagen (útil para imágenes oscuras)")
    print("  • Gamma = 1.0  → Imagen original (sin cambios)")
    print("  • Gamma = 1.5  → Oscurece ligeramente la imagen")
    print("  • Gamma = 2.0  → Oscurece más la imagen (útil para imágenes muy claras)")
    print("\nRECOMENDACIÓN:")
    print("  - Si la imagen original está OSCURA, use Gamma = 0.5")
    print("  - Si la imagen original está MUY CLARA, use Gamma = 1.5 o 2.0")
    print("  - Para imágenes balanceadas, Gamma = 1.0 es adecuado")
    print("="*70)


def crear_imagen_ejemplo():
    """
    Crea una imagen de ejemplo oscura para demostración si no hay imagen disponible.
    """
    print("Creando imagen de ejemplo oscura...")
    
    # Crear una imagen con degradado oscuro
    altura, ancho = 400, 600
    imagen = np.zeros((altura, ancho, 3), dtype=np.uint8)
    
    # Crear un degradado oscuro
    for i in range(altura):
        for j in range(ancho):
            # Valores bajos para simular poca luz
            r = int((i / altura) * 80)
            g = int((j / ancho) * 60)
            b = int(((i + j) / (altura + ancho)) * 70)
            imagen[i, j] = [b, g, r]
    
    # Añadir algunos elementos más oscuros
    cv2.rectangle(imagen, (50, 50), (250, 200), (30, 30, 30), -1)
    cv2.circle(imagen, (450, 300), 80, (40, 40, 40), -1)
    
    # Guardar la imagen
    cv2.imwrite('imagen_oscura_ejemplo.jpg', imagen)
    print("Imagen de ejemplo creada: 'imagen_oscura_ejemplo.jpg'")
    return 'imagen_oscura_ejemplo.jpg'


def main():
    """
    Función principal del programa.
    """
    print("="*70)
    print("EJERCICIO 1: CORRECCIÓN DE GAMMA EN IMÁGENES")
    print("="*70)
    print("\nEste programa corrige imágenes con mucha o poca luz usando adjust_gamma")
    print("y muestra 3 diferentes correcciones para elegir la mejor.\n")
    
    ruta_imagen = input("Ingrese la ruta de la imagen a corregir\n(o presione Enter para usar imagen de ejemplo): ").strip()
    
    if not ruta_imagen or ruta_imagen == "":
        ruta_imagen = crear_imagen_ejemplo()
    
    corregir_imagen_con_gamma(ruta_imagen)
    
    print("\n¡Proceso completado!")


if __name__ == "__main__":
    main()
