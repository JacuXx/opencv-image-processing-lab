"""
Ejemplo de uso de la nueva arquitectura modular.
Este script demuestra cómo usar los módulos del proyecto.
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path para importar src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.processors import GammaAdjuster, ImageResizer, ImageRotator, TextOverlay
from src.io import ImageLoader, ImageSaver
from src.visualization import ImageDisplayer
from config.settings import settings


def ejemplo_completo():
    """
    Ejemplo completo que demuestra todas las funcionalidades.
    """
    print("="*70)
    print("EJEMPLO DE USO DE LA ARQUITECTURA MODULAR")
    print("="*70)
    
    # Mostrar configuración
    settings.print_config()
    
    # 1. CARGAR IMAGEN
    print("\n1. CARGANDO IMAGEN...")
    loader = ImageLoader()
    
    # Intentar cargar una imagen de ejemplo
    image_path = input("\nIngrese la ruta de una imagen (o Enter para crear ejemplo): ").strip()
    
    if not image_path:
        # Generar imagen de ejemplo
        print("\nGenerando imagen de ejemplo...")
        from scripts.generar_imagenes_ejemplo import generar_imagen_oscura
        generar_imagen_oscura()
        image_path = "imagen_oscura.jpg"
    
    image = loader.load(image_path)
    
    if image is None:
        print("No se pudo cargar la imagen. Saliendo...")
        return
    
    # 2. PROCESAR CON GAMMA
    print("\n2. AJUSTANDO GAMMA...")
    gamma_adjuster = GammaAdjuster()
    
    # Auto-detectar gamma apropiado
    gamma_sugerido = gamma_adjuster.get_recommended_gamma(image)
    print(f"   Gamma sugerido: {gamma_sugerido:.2f}")
    
    image_gamma = gamma_adjuster.process(image, gamma=gamma_sugerido)
    
    # 3. REDIMENSIONAR
    print("\n3. REDIMENSIONANDO...")
    resizer = ImageResizer()
    image_resized = resizer.process(image_gamma, width=800, maintain_aspect=True)
    
    # 4. ROTAR
    print("\n4. ROTANDO...")
    rotator = ImageRotator()
    image_rotated = rotator.process(image_resized, degrees=15)
    
    # 5. AGREGAR TEXTO
    print("\n5. AGREGANDO TEXTO...")
    text_overlay = TextOverlay()
    image_final = text_overlay.add_text_with_background(
        image_rotated,
        "Procesado con OpenCV",
        position=(50, 100),
        font='simplex',
        text_color=(255, 255, 255),
        bg_color=(0, 0, 0),
        scale=1.5,
        thickness=2
    )
    
    # 6. GUARDAR RESULTADOS
    print("\n6. GUARDANDO RESULTADOS...")
    saver = ImageSaver(default_output_dir=settings.OUTPUT_DIR)
    
    saver.save(image_gamma, settings.OUTPUT_DIR / "01_gamma.jpg")
    saver.save(image_resized, settings.OUTPUT_DIR / "02_resized.jpg")
    saver.save(image_rotated, settings.OUTPUT_DIR / "03_rotated.jpg")
    saver.save(image_final, settings.OUTPUT_DIR / "04_final.jpg")
    
    # 7. VISUALIZAR
    print("\n7. VISUALIZANDO RESULTADOS...")
    displayer = ImageDisplayer()
    
    displayer.show_multiple(
        {
            "Original": image,
            "Gamma Ajustado": image_gamma,
            "Redimensionado": image_resized,
            "Rotado": image_rotated,
            "Con Texto": image_final,
        },
        rows=2,
        cols=3,
        main_title="Pipeline de Procesamiento Completo"
    )
    
    print("\n" + "="*70)
    print("¡PROCESO COMPLETADO EXITOSAMENTE!")
    print(f"Resultados guardados en: {settings.OUTPUT_DIR}")
    print("="*70)


def ejemplo_batch_processing():
    """
    Ejemplo de procesamiento por lotes usando BatchProcessor.
    """
    from src.core.image_processor import BatchProcessor
    
    print("\n" + "="*70)
    print("EJEMPLO DE PROCESAMIENTO POR LOTES")
    print("="*70)
    
    # Crear procesador por lotes
    batch = BatchProcessor()
    
    # Agregar procesadores a la cadena
    batch.add_processor(GammaAdjuster(default_gamma=0.7))
    batch.add_processor(ImageResizer())
    batch.add_processor(ImageRotator())
    
    print(f"\nProcesadores en la cadena: {len(batch)}")
    
    # Cargar imagen
    loader = ImageLoader()
    image = loader.load("imagen_oscura.jpg")
    
    if image is not None:
        # Procesar con todos los procesadores en secuencia
        result = batch.process(image, width=800, degrees=10)
        
        # Visualizar
        displayer = ImageDisplayer()
        displayer.compare(image, result, "Original", "Procesado por Lotes")


def ejemplo_comparacion_metodos():
    """
    Ejemplo de comparación de diferentes métodos de interpolación.
    """
    print("\n" + "="*70)
    print("EJEMPLO DE COMPARACIÓN DE MÉTODOS")
    print("="*70)
    
    # Cargar imagen
    loader = ImageLoader()
    image = loader.load("imagen_oscura.jpg")
    
    if image is None:
        print("No se encontró imagen. Ejecute primero ejemplo_completo()")
        return
    
    # Comparar métodos de interpolación
    resizer = ImageResizer()
    results = resizer.compare_methods(image, scale=0.5)
    
    # Visualizar comparación
    displayer = ImageDisplayer()
    displayer.show_multiple(
        results,
        rows=2,
        cols=3,
        main_title="Comparación de Métodos de Interpolación"
    )


if __name__ == "__main__":
    print("\n¿Qué ejemplo desea ejecutar?")
    print("1. Ejemplo completo (recomendado)")
    print("2. Procesamiento por lotes")
    print("3. Comparación de métodos")
    print("4. Todos")
    
    opcion = input("\nSeleccione una opción (1-4): ").strip()
    
    if opcion == "1":
        ejemplo_completo()
    elif opcion == "2":
        ejemplo_batch_processing()
    elif opcion == "3":
        ejemplo_comparacion_metodos()
    elif opcion == "4":
        ejemplo_completo()
        input("\nPresione Enter para continuar...")
        ejemplo_batch_processing()
        input("\nPresione Enter para continuar...")
        ejemplo_comparacion_metodos()
    else:
        print("Opción no válida. Ejecutando ejemplo completo...")
        ejemplo_completo()
