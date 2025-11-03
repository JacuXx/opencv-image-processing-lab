"""
Ejercicio 4: Texto en Imagen con Menú Interactivo
Este programa permite al usuario seleccionar tipo de letra, color y coordenadas
para mostrar texto en una imagen.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


# Diccionario de tipos de letras disponibles en OpenCV
TIPOS_LETRAS = {
    "1": ("SIMPLEX", cv2.FONT_HERSHEY_SIMPLEX),
    "2": ("PLAIN", cv2.FONT_HERSHEY_PLAIN),
    "3": ("DUPLEX", cv2.FONT_HERSHEY_DUPLEX),
    "4": ("COMPLEX", cv2.FONT_HERSHEY_COMPLEX),
    "5": ("TRIPLEX", cv2.FONT_HERSHEY_TRIPLEX),
    "6": ("COMPLEX SMALL", cv2.FONT_HERSHEY_COMPLEX_SMALL),
    "7": ("SCRIPT SIMPLEX", cv2.FONT_HERSHEY_SCRIPT_SIMPLEX),
    "8": ("SCRIPT COMPLEX", cv2.FONT_HERSHEY_SCRIPT_COMPLEX),
}

# Diccionario de colores disponibles (BGR format for OpenCV)
COLORES = {
    "1": ("ROJO", (0, 0, 255)),
    "2": ("VERDE", (0, 255, 0)),
    "3": ("AZUL", (255, 0, 0)),
    "4": ("AMARILLO", (0, 255, 255)),
}


def mostrar_menu_letras():
    """
    Muestra el menú de tipos de letras disponibles.
    
    Returns:
        dict: Diccionario con los tipos de letras
    """
    print("\n" + "="*70)
    print("TIPOS DE LETRAS DISPONIBLES")
    print("="*70)
    for clave, (nombre, _) in TIPOS_LETRAS.items():
        print(f"  {clave}. {nombre}")
    print("="*70)
    return TIPOS_LETRAS


def mostrar_menu_colores():
    """
    Muestra el menú de colores disponibles.
    
    Returns:
        dict: Diccionario con los colores
    """
    print("\n" + "="*70)
    print("COLORES DISPONIBLES")
    print("="*70)
    for clave, (nombre, _) in COLORES.items():
        print(f"  {clave}. {nombre}")
    print("="*70)
    return COLORES


def validar_coordenadas(x_str, y_str, ancho_imagen, alto_imagen):
    """
    Valida que las coordenadas sean números válidos y estén dentro de los límites.
    
    Args:
        x_str: String con la coordenada X
        y_str: String con la coordenada Y
        ancho_imagen: Ancho de la imagen
        alto_imagen: Alto de la imagen
    
    Returns:
        tuple: (bool, int, int) - (es_valido, x, y)
    """
    try:
        x = int(x_str)
        y = int(y_str)
        
        # Validar que estén dentro de los límites
        # El texto se dibuja desde la esquina inferior izquierda
        # Por eso Y debe ser > 0 (para que se vea)
        if x < 0 or x >= ancho_imagen:
            print(f"❌ ERROR: La coordenada X debe estar entre 0 y {ancho_imagen-1}")
            return False, 0, 0
        
        if y <= 0 or y > alto_imagen:
            print(f"❌ ERROR: La coordenada Y debe estar entre 1 y {alto_imagen}")
            print("   (Y es la línea base del texto, debe ser > 0)")
            return False, 0, 0
        
        return True, x, y
    
    except ValueError:
        print("❌ ERROR: Las coordenadas deben ser números enteros válidos.")
        return False, 0, 0


def agregar_texto_a_imagen(ruta_imagen):
    """
    Agrega texto a una imagen según las preferencias del usuario.
    
    Args:
        ruta_imagen: Ruta de la imagen base
    """
    # Cargar la imagen
    imagen = cv2.imread(ruta_imagen)
    
    if imagen is None:
        print(f"Error: No se pudo cargar la imagen '{ruta_imagen}'")
        print("Por favor, asegúrate de que el archivo existe.")
        return
    
    # Obtener dimensiones
    alto_imagen, ancho_imagen = imagen.shape[:2]
    print(f"\n📐 Dimensiones de la imagen: {ancho_imagen} x {alto_imagen} píxeles")
    print(f"   Coordenadas válidas: X [0 - {ancho_imagen-1}], Y [1 - {alto_imagen}]")
    
    # Convertir a RGB para mostrar
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    
    # PASO 1: Seleccionar tipo de letra
    tipos_letras = mostrar_menu_letras()
    while True:
        opcion_letra = input("\nSeleccione el tipo de letra (1-8): ").strip()
        if opcion_letra in tipos_letras:
            nombre_letra, fuente = tipos_letras[opcion_letra]
            print(f"✓ Tipo de letra seleccionado: {nombre_letra}")
            break
        else:
            print("❌ ERROR: Opción no válida. Debe seleccionar un número del 1 al 8.")
    
    # PASO 2: Seleccionar color
    colores = mostrar_menu_colores()
    while True:
        opcion_color = input("\nSeleccione el color (1-4): ").strip()
        if opcion_color in colores:
            nombre_color, color_bgr = colores[opcion_color]
            print(f"✓ Color seleccionado: {nombre_color}")
            break
        else:
            print("❌ ERROR: Opción no válida. Debe seleccionar un número del 1 al 4.")
    
    # PASO 3: Ingresar el texto
    texto = input("\nIngrese el texto a mostrar en la imagen: ").strip()
    if not texto:
        print("❌ ERROR: Debe ingresar un texto válido.")
        return
    print(f"✓ Texto: '{texto}'")
    
    # PASO 4: Seleccionar coordenadas
    print("\n" + "="*70)
    print("COORDENADAS DEL TEXTO")
    print("="*70)
    print(f"Ingrese las coordenadas donde desea colocar el texto.")
    print(f"Recordatorio: X [0 - {ancho_imagen-1}], Y [1 - {alto_imagen}]")
    
    while True:
        x_input = input("\nCoordenada X: ").strip()
        y_input = input("Coordenada Y: ").strip()
        
        es_valido, x, y = validar_coordenadas(x_input, y_input, ancho_imagen, alto_imagen)
        
        if es_valido:
            print(f"✓ Coordenadas válidas: ({x}, {y})")
            break
    
    # PASO 5: Crear imagen con texto
    print("\n" + "="*70)
    print("GENERANDO IMAGEN CON TEXTO")
    print("="*70)
    print(f"\nParámetros seleccionados:")
    print(f"  • Tipo de letra: {nombre_letra}")
    print(f"  • Color: {nombre_color}")
    print(f"  • Texto: '{texto}'")
    print(f"  • Coordenadas: ({x}, {y})")
    
    # Crear copia de la imagen para agregar texto
    imagen_con_texto = imagen.copy()
    
    # Agregar texto a la imagen
    # Parámetros: imagen, texto, posición (x,y), fuente, escala, color, grosor
    cv2.putText(imagen_con_texto, texto, (x, y), fuente, 1, color_bgr, 2, cv2.LINE_AA)
    
    # Convertir a RGB para mostrar
    imagen_con_texto_rgb = cv2.cvtColor(imagen_con_texto, cv2.COLOR_BGR2RGB)
    
    # Mostrar comparación
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    fig.suptitle('Resultado: Imagen con Texto', fontsize=16, fontweight='bold')
    
    axes[0].imshow(imagen_rgb)
    axes[0].set_title('Imagen Original', fontsize=12, fontweight='bold')
    axes[0].axis('off')
    
    axes[1].imshow(imagen_con_texto_rgb)
    axes[1].set_title(f'Con Texto: "{texto}"\n{nombre_letra} - {nombre_color} - ({x},{y})', 
                     fontsize=12, fontweight='bold')
    axes[1].axis('off')
    
    # Marcar el punto de inserción en la imagen con texto
    imagen_con_marca = imagen_con_texto_rgb.copy()
    cv2.circle(imagen_con_marca, (x, y), 5, (255, 0, 0), -1)
    axes[1].imshow(imagen_con_marca)
    
    plt.tight_layout()
    plt.show()
    
    # Guardar imagen
    guardar = input("\n¿Desea guardar la imagen con texto? (s/n): ").strip().lower()
    if guardar == 's':
        nombre_archivo = f"imagen_con_texto_{nombre_letra.replace(' ', '_')}_{nombre_color}.jpg"
        cv2.imwrite(nombre_archivo, imagen_con_texto)
        print(f"Imagen guardada como: {nombre_archivo}")


def crear_imagen_ejemplo():
    """
    Crea una imagen de ejemplo para demostración.
    """
    print("Creando imagen de ejemplo...")
    
    # Crear una imagen de 800x600 con un fondo degradado suave
    altura, ancho = 600, 800
    imagen = np.zeros((altura, ancho, 3), dtype=np.uint8)
    
    # Crear fondo degradado suave
    for i in range(altura):
        for j in range(ancho):
            r = int(200 - (i / altura) * 50)
            g = int(220 - (j / ancho) * 40)
            b = 240
            imagen[i, j] = [b, g, r]
    
    # Añadir un rectángulo decorativo
    cv2.rectangle(imagen, (50, 50), (750, 550), (100, 100, 100), 3)
    
    # Añadir círculos decorativos en las esquinas
    cv2.circle(imagen, (100, 100), 30, (150, 150, 200), -1)
    cv2.circle(imagen, (700, 100), 30, (150, 200, 150), -1)
    cv2.circle(imagen, (100, 500), 30, (200, 150, 150), -1)
    cv2.circle(imagen, (700, 500), 30, (200, 200, 150), -1)
    
    # Guardar la imagen
    cv2.imwrite('imagen_ejemplo_texto.jpg', imagen)
    print("Imagen de ejemplo creada: 'imagen_ejemplo_texto.jpg'")
    return 'imagen_ejemplo_texto.jpg'


def ejecutar_demostracion():
    """
    Ejecuta una demostración automática con diferentes configuraciones.
    """
    print("\n" + "="*70)
    print("MODO DEMOSTRACIÓN")
    print("="*70)
    print("\nEsta demostración mostrará diferentes combinaciones de:")
    print("  • Tipos de letras")
    print("  • Colores")
    print("  • Coordenadas válidas e inválidas")
    
    input("\nPresione Enter para comenzar la demostración...")
    
    # Crear imagen de ejemplo
    ruta_imagen = crear_imagen_ejemplo()
    imagen = cv2.imread(ruta_imagen)
    alto_imagen, ancho_imagen = imagen.shape[:2]
    
    # Configuraciones de demostración
    demos = [
        {
            "nombre": "Demo 1: SIMPLEX - ROJO - Coordenadas válidas (400, 300)",
            "letra": ("SIMPLEX", cv2.FONT_HERSHEY_SIMPLEX),
            "color": ("ROJO", (0, 0, 255)),
            "texto": "Hola Mundo",
            "x": 400,
            "y": 300,
            "valido": True
        },
        {
            "nombre": "Demo 2: COMPLEX - VERDE - Coordenadas válidas (100, 150)",
            "letra": ("COMPLEX", cv2.FONT_HERSHEY_COMPLEX),
            "color": ("VERDE", (0, 255, 0)),
            "texto": "OpenCV",
            "x": 100,
            "y": 150,
            "valido": True
        },
        {
            "nombre": "Demo 3: SCRIPT COMPLEX - AZUL - Coordenadas válidas (200, 450)",
            "letra": ("SCRIPT COMPLEX", cv2.FONT_HERSHEY_SCRIPT_COMPLEX),
            "color": ("AZUL", (255, 0, 0)),
            "texto": "Inteligencia Artificial",
            "x": 200,
            "y": 450,
            "valido": True
        },
        {
            "nombre": "Demo 4: DUPLEX - AMARILLO - Coordenadas inválidas (-50, 300)",
            "letra": ("DUPLEX", cv2.FONT_HERSHEY_DUPLEX),
            "color": ("AMARILLO", (0, 255, 255)),
            "texto": "Error",
            "x": -50,
            "y": 300,
            "valido": False
        },
        {
            "nombre": f"Demo 5: TRIPLEX - ROJO - Coordenadas inválidas (400, {alto_imagen + 100})",
            "letra": ("TRIPLEX", cv2.FONT_HERSHEY_TRIPLEX),
            "color": ("ROJO", (0, 0, 255)),
            "texto": "Fuera de rango",
            "x": 400,
            "y": alto_imagen + 100,
            "valido": False
        }
    ]
    
    for i, demo in enumerate(demos, 1):
        print("\n" + "="*70)
        print(demo["nombre"])
        print("="*70)
        print(f"\nParámetros:")
        print(f"  • Tipo de letra: {demo['letra'][0]}")
        print(f"  • Color: {demo['color'][0]}")
        print(f"  • Texto: '{demo['texto']}'")
        print(f"  • Coordenadas: ({demo['x']}, {demo['y']})")
        
        # Validar coordenadas
        es_valido, x, y = validar_coordenadas(str(demo['x']), str(demo['y']), 
                                              ancho_imagen, alto_imagen)
        
        if es_valido and demo['valido']:
            print(f"✓ Coordenadas válidas")
            
            # Crear imagen con texto
            imagen_demo = imagen.copy()
            cv2.putText(imagen_demo, demo['texto'], (x, y), demo['letra'][1], 
                       1, demo['color'][1], 2, cv2.LINE_AA)
            
            # Mostrar
            imagen_rgb = cv2.cvtColor(imagen_demo, cv2.COLOR_BGR2RGB)
            plt.figure(figsize=(10, 7))
            plt.imshow(imagen_rgb)
            plt.title(f"Demo {i}: {demo['letra'][0]} - {demo['color'][0]}", 
                     fontsize=14, fontweight='bold')
            plt.axis('off')
            plt.tight_layout()
            plt.show()
        else:
            print(f"❌ Validación falló como se esperaba (demostración de coordenadas inválidas)")
        
        if i < len(demos):
            input("\nPresione Enter para continuar con la siguiente demostración...")
    
    print("\n¡Demostración completada!")


def main():
    """
    Función principal del programa.
    """
    print("="*70)
    print("EJERCICIO 4: TEXTO EN IMAGEN CON MENÚ INTERACTIVO")
    print("="*70)
    print("\nEste programa permite agregar texto a una imagen con:")
    print("  • Selección de tipo de letra")
    print("  • Selección de color")
    print("  • Selección de coordenadas (con validación)")
    
    print("\n" + "="*70)
    print("MODO DE EJECUCIÓN")
    print("="*70)
    print("1. Modo Interactivo (elegir manualmente)")
    print("2. Modo Demostración (ver ejemplos automáticos)")
    
    modo = input("\nSeleccione el modo (1-2): ").strip()
    
    if modo == "2":
        ejecutar_demostracion()
    else:
        ruta_imagen = input("\nIngrese la ruta de la imagen\n(o presione Enter para usar imagen de ejemplo): ").strip()
        
        if not ruta_imagen or ruta_imagen == "":
            ruta_imagen = crear_imagen_ejemplo()
        
        agregar_texto_a_imagen(ruta_imagen)
    
    print("\n¡Proceso completado!")


if __name__ == "__main__":
    main()
