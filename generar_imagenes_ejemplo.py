"""
Script para generar diferentes tipos de imágenes de ejemplo
para usar en los ejercicios de procesamiento de imágenes.
"""

import cv2
import numpy as np


def generar_imagen_oscura():
    """Genera una imagen muy oscura para ejercicio 1."""
    print("Generando imagen oscura...")
    
    altura, ancho = 600, 800
    imagen = np.zeros((altura, ancho, 3), dtype=np.uint8)
    
    # Crear un paisaje nocturno oscuro
    # Cielo nocturno degradado
    for i in range(300):
        for j in range(ancho):
            r = int(10 + (i / 300) * 20)
            g = int(8 + (i / 300) * 15)
            b = int(20 + (i / 300) * 30)
            imagen[i, j] = [b, g, r]
    
    # Tierra/suelo oscuro
    for i in range(300, altura):
        for j in range(ancho):
            r = int(5 + (j / ancho) * 15)
            g = int(8 + (j / ancho) * 12)
            b = int(3 + (j / ancho) * 10)
            imagen[i, j] = [b, g, r]
    
    # Luna pequeña (única fuente de luz)
    cv2.circle(imagen, (650, 100), 40, (180, 180, 200), -1)
    cv2.circle(imagen, (650, 100), 35, (140, 140, 160), -1)
    
    # Siluetas de árboles (muy oscuros)
    puntos_arbol1 = np.array([[100, 300], [80, 500], [120, 500]], np.int32)
    cv2.fillPoly(imagen, [puntos_arbol1], (5, 5, 5))
    cv2.circle(imagen, (100, 280), 30, (8, 8, 8), -1)
    
    puntos_arbol2 = np.array([[300, 320], [280, 500], [320, 500]], np.int32)
    cv2.fillPoly(imagen, [puntos_arbol2], (3, 3, 3))
    cv2.circle(imagen, (300, 300), 35, (6, 6, 6), -1)
    
    # Casa oscura a lo lejos
    cv2.rectangle(imagen, (500, 350), (600, 450), (20, 15, 10), -1)
    cv2.rectangle(imagen, (520, 370), (540, 400), (80, 70, 50), -1)  # Ventana con luz tenue
    
    cv2.imwrite('imagen_muy_oscura.jpg', imagen)
    print("✓ Creada: imagen_muy_oscura.jpg (imagen con POCA luz)")
    return 'imagen_muy_oscura.jpg'


def generar_imagen_clara():
    """Genera una imagen muy clara para ejercicio 1."""
    print("Generando imagen muy clara...")
    
    altura, ancho = 600, 800
    imagen = np.ones((altura, ancho, 3), dtype=np.uint8) * 220
    
    # Cielo muy claro (casi blanco)
    for i in range(350):
        for j in range(ancho):
            r = int(220 + (i / 350) * 35)
            g = int(225 + (i / 350) * 30)
            b = int(240 + (i / 350) * 15)
            imagen[i, j] = [min(b, 255), min(g, 255), min(r, 255)]
    
    # Suelo claro
    for i in range(350, altura):
        for j in range(ancho):
            r = int(200 + (j / ancho) * 40)
            g = int(210 + (j / ancho) * 35)
            b = int(190 + (j / ancho) * 45)
            imagen[i, j] = [min(b, 255), min(g, 255), min(r, 255)]
    
    # Sol muy brillante
    cv2.circle(imagen, (650, 120), 60, (255, 255, 255), -1)
    cv2.circle(imagen, (650, 120), 80, (250, 250, 255), -1)
    cv2.circle(imagen, (650, 120), 45, (245, 245, 250), -1)
    
    # Nubes muy claras
    cv2.ellipse(imagen, (200, 100), (80, 30), 0, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(imagen, (400, 150), (70, 25), 0, 0, 360, (250, 250, 255), -1)
    
    cv2.imwrite('imagen_muy_clara.jpg', imagen)
    print("✓ Creada: imagen_muy_clara.jpg (imagen con MUCHA luz)")
    return 'imagen_muy_clara.jpg'


def generar_imagen_normal():
    """Genera una imagen con iluminación normal para comparación."""
    print("Generando imagen con iluminación normal...")
    
    altura, ancho = 600, 800
    imagen = np.zeros((altura, ancho, 3), dtype=np.uint8)
    
    # Cielo con iluminación normal
    for i in range(350):
        for j in range(ancho):
            r = int(100 + (i / 350) * 80)
            g = int(120 + (i / 350) * 100)
            b = int(200 + (i / 350) * 40)
            imagen[i, j] = [b, g, r]
    
    # Césped verde
    for i in range(350, altura):
        for j in range(ancho):
            r = int(40 + (j / ancho) * 30)
            g = int(120 + (j / ancho) * 60)
            b = int(30 + (j / ancho) * 25)
            imagen[i, j] = [b, g, r]
    
    # Sol
    cv2.circle(imagen, (650, 120), 50, (100, 200, 255), -1)
    
    # Casa
    cv2.rectangle(imagen, (300, 300), (500, 500), (80, 100, 140), -1)
    cv2.rectangle(imagen, (330, 350), (370, 410), (150, 180, 200), -1)  # Ventana
    cv2.rectangle(imagen, (430, 350), (470, 410), (150, 180, 200), -1)  # Ventana
    cv2.rectangle(imagen, (370, 420), (430, 500), (60, 40, 30), -1)  # Puerta
    
    # Techo
    puntos_techo = np.array([[280, 300], [400, 200], [520, 300]], np.int32)
    cv2.fillPoly(imagen, [puntos_techo], (120, 70, 50))
    
    # Árbol
    cv2.rectangle(imagen, (120, 400), (160, 500), (60, 40, 30), -1)  # Tronco
    cv2.circle(imagen, (140, 350), 60, (40, 120, 60), -1)  # Copa
    
    cv2.imwrite('imagen_iluminacion_normal.jpg', imagen)
    print("✓ Creada: imagen_iluminacion_normal.jpg (imagen balanceada)")
    return 'imagen_iluminacion_normal.jpg'


def generar_imagen_subexpuesta():
    """Genera una imagen subexpuesta (foto típica de cámara con error)."""
    print("Generando imagen subexpuesta...")
    
    altura, ancho = 600, 800
    imagen = np.zeros((altura, ancho, 3), dtype=np.uint8)
    
    # Fondo degradado oscuro
    for i in range(altura):
        for j in range(ancho):
            r = int(30 + (i / altura) * 50 + (j / ancho) * 40)
            g = int(35 + (i / altura) * 55 + (j / ancho) * 45)
            b = int(40 + (i / altura) * 60 + (j / ancho) * 50)
            imagen[i, j] = [b, g, r]
    
    # Formas geométricas apenas visibles
    cv2.rectangle(imagen, (100, 100), (300, 250), (70, 75, 80), -1)
    cv2.circle(imagen, (500, 400), 100, (60, 65, 70), -1)
    cv2.rectangle(imagen, (550, 150), (700, 300), (65, 70, 75), -1)
    
    # Texto apenas visible
    cv2.putText(imagen, 'Subexpuesta', (250, 450), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (90, 95, 100), 3)
    
    cv2.imwrite('imagen_subexpuesta.jpg', imagen)
    print("✓ Creada: imagen_subexpuesta.jpg (foto con error de exposición)")
    return 'imagen_subexpuesta.jpg'


def main():
    """Genera todas las imágenes de ejemplo."""
    print("="*70)
    print("GENERADOR DE IMÁGENES DE EJEMPLO PARA EJERCICIO 1")
    print("="*70)
    print("\nEste script crea diferentes tipos de imágenes para demostrar")
    print("la corrección de gamma en el Ejercicio 1.\n")
    
    imagenes_creadas = []
    
    # Generar todas las imágenes
    imagenes_creadas.append(generar_imagen_oscura())
    imagenes_creadas.append(generar_imagen_clara())
    imagenes_creadas.append(generar_imagen_normal())
    imagenes_creadas.append(generar_imagen_subexpuesta())
    
    print("\n" + "="*70)
    print("✅ IMÁGENES CREADAS EXITOSAMENTE")
    print("="*70)
    print("\nImágenes generadas:")
    for idx, img in enumerate(imagenes_creadas, 1):
        print(f"  {idx}. {img}")
    
    print("\n📝 CÓMO USARLAS EN EL EJERCICIO 1:")
    print("\n1. Ejecuta: python ejercicio1_gamma.py")
    print("2. Cuando pregunte por la ruta, ingresa:")
    print("   • imagen_muy_oscura.jpg       (mejor con gamma 0.5)")
    print("   • imagen_muy_clara.jpg        (mejor con gamma 1.5-2.0)")
    print("   • imagen_iluminacion_normal.jpg (mejor con gamma 1.0)")
    print("   • imagen_subexpuesta.jpg      (mejor con gamma 0.5)")
    
    print("\n💡 RECOMENDACIÓN:")
    print("   Para la evaluación, usa 'imagen_muy_oscura.jpg' o 'imagen_subexpuesta.jpg'")
    print("   Ya que demuestran claramente la mejora con gamma < 1")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
