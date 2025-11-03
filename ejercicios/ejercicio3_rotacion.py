"""
Ejercicio 3: Rotación de Imagen
Este programa permite rotar una imagen según los grados especificados por el usuario.
Incluye validación de grados de rotación.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


def validar_grados(grados_str):
    """
    Valida que los grados ingresados sean un número válido.
    
    Args:
        grados_str: String con los grados a validar
    
    Returns:
        tuple: (bool, float) - (es_valido, grados_convertidos)
    """
    try:
        grados = float(grados_str)
        return True, grados
    except ValueError:
        return False, 0


def rotar_imagen(imagen, grados):
    """
    Rota una imagen el número de grados especificado.
    
    Args:
        imagen: Imagen a rotar
        grados: Grados de rotación (positivo = antihorario, negativo = horario)
    
    Returns:
        Imagen rotada
    """
    # Obtener dimensiones de la imagen
    altura, ancho = imagen.shape[:2]
    
    # Calcular el centro de la imagen
    centro = (ancho // 2, altura // 2)
    
    # Obtener la matriz de rotación
    # El valor positivo rota en sentido antihorario, negativo en sentido horario
    matriz_rotacion = cv2.getRotationMatrix2D(centro, grados, 1.0)
    
    # Calcular las nuevas dimensiones de la imagen para que no se corte
    cos = np.abs(matriz_rotacion[0, 0])
    sin = np.abs(matriz_rotacion[0, 1])
    
    nuevo_ancho = int((altura * sin) + (ancho * cos))
    nuevo_alto = int((altura * cos) + (ancho * sin))
    
    # Ajustar la matriz de rotación para tener en cuenta la traslación
    matriz_rotacion[0, 2] += (nuevo_ancho / 2) - centro[0]
    matriz_rotacion[1, 2] += (nuevo_alto / 2) - centro[1]
    
    # Aplicar la rotación
    imagen_rotada = cv2.warpAffine(imagen, matriz_rotacion, (nuevo_ancho, nuevo_alto),
                                   borderMode=cv2.BORDER_CONSTANT,
                                   borderValue=(255, 255, 255))
    
    return imagen_rotada


def procesar_rotacion(ruta_imagen):
    """
    Procesa la rotación de una imagen según los grados especificados por el usuario.
    
    Args:
        ruta_imagen: Ruta de la imagen a rotar
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
    print("INFORMACIÓN SOBRE ROTACIÓN")
    print("="*70)
    print("\n  • Grados positivos: Rotación ANTIHORARIA (sentido contrario a las agujas del reloj)")
    print("  • Grados negativos: Rotación HORARIA (sentido de las agujas del reloj)")
    print("\nEjemplos:")
    print("  • 90° → Rota 90 grados antihorario")
    print("  • -90° → Rota 90 grados horario")
    print("  • 180° → Voltea la imagen completamente")
    print("  • 45° → Rota 45 grados antihorario")
    
    while True:
        print("\n" + "="*70)
        grados_input = input("Ingrese los grados de rotación (o 'q' para salir): ").strip()
        
        if grados_input.lower() == 'q':
            print("Saliendo del programa...")
            break
        
        # Validar los grados
        es_valido, grados = validar_grados(grados_input)
        
        if not es_valido:
            print("❌ ERROR: Debe ingresar un número válido.")
            print("   Ejemplos válidos: 90, -45, 180, 30.5, -120")
            continue
        
        # Normalizar los grados al rango [0, 360)
        grados_normalizados = grados % 360
        
        print(f"\n✓ Grados válidos: {grados}°")
        if grados != grados_normalizados:
            print(f"  (Equivalente a {grados_normalizados}° en el rango 0-360)")
        
        # Rotar la imagen
        print(f"\nRotando imagen {grados}°...")
        imagen_rotada = rotar_imagen(imagen_rgb, grados)
        
        # Mostrar comparación
        fig, axes = plt.subplots(1, 2, figsize=(15, 7))
        fig.suptitle(f'Rotación de Imagen: {grados}°', fontsize=16, fontweight='bold')
        
        axes[0].imshow(imagen_rgb)
        axes[0].set_title('Imagen Original', fontsize=12, fontweight='bold')
        axes[0].axis('off')
        
        axes[1].imshow(imagen_rotada)
        direccion = "Antihoraria" if grados > 0 else "Horaria" if grados < 0 else "Sin rotación"
        axes[1].set_title(f'Imagen Rotada {grados}°\n({direccion})', 
                         fontsize=12, fontweight='bold')
        axes[1].axis('off')
        
        plt.tight_layout()
        plt.show()
        
        # Preguntar si desea guardar
        guardar = input("\n¿Desea guardar la imagen rotada? (s/n): ").strip().lower()
        if guardar == 's':
            nombre_archivo = f"imagen_rotada_{int(grados)}_grados.jpg"
            imagen_bgr = cv2.cvtColor(imagen_rotada, cv2.COLOR_RGB2BGR)
            cv2.imwrite(nombre_archivo, imagen_bgr)
            print(f"Imagen guardada como: {nombre_archivo}")
        
        # Preguntar si desea rotar nuevamente
        otra = input("\n¿Desea probar otra rotación? (s/n): ").strip().lower()
        if otra != 's':
            break


def crear_imagen_ejemplo():
    """
    Crea una imagen de ejemplo para demostración de rotación.
    """
    print("Creando imagen de ejemplo...")
    
    # Crear una imagen de 600x400
    altura, ancho = 400, 600
    imagen = np.ones((altura, ancho, 3), dtype=np.uint8) * 255
    
    # Crear un fondo degradado
    for i in range(altura):
        for j in range(ancho):
            r = int((i / altura) * 200 + 55)
            g = int((j / ancho) * 200 + 55)
            b = 200
            imagen[i, j] = [b, g, r]
    
    # Añadir una flecha para indicar orientación
    # Flecha apuntando hacia arriba
    puntos = np.array([
        [300, 100],   # Punta superior
        [250, 200],   # Esquina izquierda
        [280, 200],   # Interior izquierdo
        [280, 320],   # Base izquierda
        [320, 320],   # Base derecha
        [320, 200],   # Interior derecho
        [350, 200]    # Esquina derecha
    ], np.int32)
    
    cv2.fillPoly(imagen, [puntos], (0, 0, 255))
    
    # Añadir texto indicando la parte superior
    cv2.putText(imagen, 'ARRIBA', (240, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (0, 0, 0), 2)
    cv2.putText(imagen, 'Ejemplo de Rotacion', (160, 370), cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, (0, 0, 0), 2)
    
    # Guardar la imagen
    cv2.imwrite('imagen_ejemplo_rotacion.jpg', imagen)
    print("Imagen de ejemplo creada: 'imagen_ejemplo_rotacion.jpg'")
    return 'imagen_ejemplo_rotacion.jpg'


def main():
    """
    Función principal del programa.
    """
    print("="*70)
    print("EJERCICIO 3: ROTACIÓN DE IMAGEN")
    print("="*70)
    print("\nEste programa permite rotar una imagen según los grados especificados.")
    print("Incluye validación de grados y muestra la imagen original y rotada.\n")
    
    ruta_imagen = input("Ingrese la ruta de la imagen a rotar\n(o presione Enter para usar imagen de ejemplo): ").strip()
    
    if not ruta_imagen or ruta_imagen == "":
        ruta_imagen = crear_imagen_ejemplo()
    
    procesar_rotacion(ruta_imagen)
    
    print("\n¡Proceso completado!")


if __name__ == "__main__":
    main()
