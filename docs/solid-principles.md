# 📋 Principios SOLID - Guía Completa

Los principios SOLID son cinco principios de diseño orientado a objetos que nos ayudan a crear software más mantenible, flexible y comprensible.

## S - Single Responsibility Principle (SRP)
### 🎯 Principio de Responsabilidad Única

> *"Una clase debe tener una sola razón para cambiar"*

### ❌ Violación del SRP
```typescript
class ImageProcessor {
    // Múltiples responsabilidades en una sola clase
    processImage(image: Image): ProcessedImage {
        // Responsabilidad 1: Validación
        if (!image.isValid()) {
            throw new Error('Invalid image');
        }

        // Responsabilidad 2: Procesamiento
        const processed = this.upscaleImage(image);

        // Responsabilidad 3: Guardado
        this.saveToDatabase(processed);

        // Responsabilidad 4: Notificación
        this.sendEmailNotification(processed);

        return processed;
    }
}
```

### ✅ Aplicando SRP
```typescript
class ImageValidator {
    validate(image: Image): ValidationResult {
        // Solo responsabilidad de validación
        return new ValidationResult(image.isValid());
    }
}

class ImageUpscaler {
    upscale(image: Image, scale: number): ProcessedImage {
        // Solo responsabilidad de procesamiento
        return this.applyUpscaleAlgorithm(image, scale);
    }
}

class ImageRepository {
    save(image: ProcessedImage): Promise<void> {
        // Solo responsabilidad de persistencia
        return this.database.save(image);
    }
}

class NotificationService {
    sendProcessingComplete(image: ProcessedImage): Promise<void> {
        // Solo responsabilidad de notificación
        return this.emailService.send(image.userId, 'Processing complete');
    }
}
```

## O - Open/Closed Principle (OCP)
### 🔓 Principio Abierto/Cerrado

> *"Las entidades deben estar abiertas para extensión pero cerradas para modificación"*

### ❌ Violación del OCP
```typescript
class ImageProcessor {
    process(image: Image, type: string): ProcessedImage {
        if (type === 'upscale') {
            return this.upscaleImage(image);
        } else if (type === 'compress') {
            return this.compressImage(image);
        } else if (type === 'filter') {
            return this.applyFilter(image);
        }
        // Necesitamos modificar esta clase para agregar nuevos tipos
    }
}
```

### ✅ Aplicando OCP
```typescript
interface ImageProcessingStrategy {
    process(image: Image): ProcessedImage;
}

class UpscaleStrategy implements ImageProcessingStrategy {
    process(image: Image): ProcessedImage {
        return this.upscaleImage(image);
    }
}

class CompressStrategy implements ImageProcessingStrategy {
    process(image: Image): ProcessedImage {
        return this.compressImage(image);
    }
}

class FilterStrategy implements ImageProcessingStrategy {
    process(image: Image): ProcessedImage {
        return this.applyFilter(image);
    }
}

class ImageProcessor {
    constructor(private strategy: ImageProcessingStrategy) {}

    process(image: Image): ProcessedImage {
        return this.strategy.process(image);
    }

    // Podemos cambiar la estrategia sin modificar esta clase
    setStrategy(strategy: ImageProcessingStrategy): void {
        this.strategy = strategy;
    }
}
```

## L - Liskov Substitution Principle (LSP)
### 🔄 Principio de Sustitución de Liskov

> *"Los objetos derivados deben ser sustituibles por sus objetos base"*

### ❌ Violación del LSP
```typescript
class Rectangle {
    constructor(protected width: number, protected height: number) {}

    setWidth(width: number): void {
        this.width = width;
    }

    setHeight(height: number): void {
        this.height = height;
    }

    getArea(): number {
        return this.width * this.height;
    }
}

class Square extends Rectangle {
    setWidth(width: number): void {
        this.width = width;
        this.height = width; // Viola LSP: comportamiento inesperado
    }

    setHeight(height: number): void {
        this.width = height;
        this.height = height; // Viola LSP: comportamiento inesperado
    }
}
```

### ✅ Aplicando LSP
```typescript
interface Shape {
    getArea(): number;
}

class Rectangle implements Shape {
    constructor(private width: number, private height: number) {}

    getArea(): number {
        return this.width * this.height;
    }
}

class Square implements Shape {
    constructor(private side: number) {}

    getArea(): number {
        return this.side * this.side;
    }
}

// Ambas implementaciones son sustituibles
function calculateArea(shape: Shape): number {
    return shape.getArea(); // Funciona correctamente con ambas implementaciones
}
```

## I - Interface Segregation Principle (ISP)
### 🎭 Principio de Segregación de Interfaces

> *"Los clientes no deben depender de interfaces que no usan"*

### ❌ Violación del ISP
```typescript
interface ImageProcessor {
    upscale(image: Image): ProcessedImage;
    compress(image: Image): ProcessedImage;
    applyFilter(image: Image): ProcessedImage;
    convertFormat(image: Image): ProcessedImage;
    generateThumbnail(image: Image): ProcessedImage;
    addWatermark(image: Image): ProcessedImage;
}

class SimpleUpscaler implements ImageProcessor {
    upscale(image: Image): ProcessedImage {
        // Implementación del upscale
    }

    // Obligado a implementar métodos que no necesita
    compress(image: Image): ProcessedImage {
        throw new Error('Not supported');
    }

    applyFilter(image: Image): ProcessedImage {
        throw new Error('Not supported');
    }
    // ... más métodos no necesarios
}
```

### ✅ Aplicando ISP
```typescript
interface ImageUpscaler {
    upscale(image: Image): ProcessedImage;
}

interface ImageCompressor {
    compress(image: Image): ProcessedImage;
}

interface ImageFilter {
    applyFilter(image: Image): ProcessedImage;
}

interface ImageConverter {
    convertFormat(image: Image): ProcessedImage;
}

class SimpleUpscaler implements ImageUpscaler {
    upscale(image: Image): ProcessedImage {
        // Solo implementa lo que necesita
        return this.performUpscale(image);
    }
}

class AdvancedProcessor implements ImageUpscaler, ImageCompressor, ImageFilter {
    upscale(image: Image): ProcessedImage {
        return this.performUpscale(image);
    }

    compress(image: Image): ProcessedImage {
        return this.performCompression(image);
    }

    applyFilter(image: Image): ProcessedImage {
        return this.performFiltering(image);
    }
}
```

## D - Dependency Inversion Principle (DIP)
### 🔄 Principio de Inversión de Dependencias

> *"Depender de abstracciones, no de concreciones"*

### ❌ Violación del DIP
```typescript
class ImageUpscaler {
    private database: PostgreSQLDatabase; // Dependencia concreta
    private storage: AmazonS3Storage;     // Dependencia concreta

    constructor() {
        this.database = new PostgreSQLDatabase(); // Fuertemente acoplado
        this.storage = new AmazonS3Storage();     // Fuertemente acoplado
    }

    async upscale(image: Image): Promise<ProcessedImage> {
        const processed = this.performUpscale(image);
        await this.database.save(processed);
        await this.storage.upload(processed);
        return processed;
    }
}
```

### ✅ Aplicando DIP
```typescript
interface ImageRepository {
    save(image: ProcessedImage): Promise<void>;
}

interface StorageService {
    upload(image: ProcessedImage): Promise<string>;
}

class ImageUpscaler {
    constructor(
        private repository: ImageRepository,  // Dependencia abstracta
        private storage: StorageService       // Dependencia abstracta
    ) {}

    async upscale(image: Image): Promise<ProcessedImage> {
        const processed = this.performUpscale(image);
        await this.repository.save(processed);
        await this.storage.upload(processed);
        return processed;
    }
}

// Implementaciones concretas
class PostgreSQLImageRepository implements ImageRepository {
    async save(image: ProcessedImage): Promise<void> {
        // Implementación específica para PostgreSQL
    }
}

class S3StorageService implements StorageService {
    async upload(image: ProcessedImage): Promise<string> {
        // Implementación específica para S3
    }
}

// Inyección de dependencias
const upscaler = new ImageUpscaler(
    new PostgreSQLImageRepository(),
    new S3StorageService()
);
```

## Aplicación Práctica en el Proyecto

### Estructura Recomendada

```typescript
// Domain Layer - Interfaces (DIP)
interface IImageRepository {
    findById(id: string): Promise<Image>;
    save(image: Image): Promise<void>;
}

interface IImageProcessor {
    process(image: Image): Promise<ProcessedImage>;
}

// Application Layer - Use Cases (SRP)
class UpscaleImageUseCase {
    constructor(
        private imageRepository: IImageRepository,
        private imageProcessor: IImageProcessor,
        private notificationService: INotificationService
    ) {} // DIP: Depende de abstracciones

    async execute(request: UpscaleRequest): Promise<UpscaleResponse> {
        // SRP: Solo maneja la lógica de upscale
        const image = await this.imageRepository.findById(request.imageId);
        const processed = await this.imageProcessor.process(image);
        await this.imageRepository.save(processed);
        await this.notificationService.notify(request.userId, 'Completed');
        return new UpscaleResponse(processed);
    }
}

// Infrastructure Layer - Implementaciones concretas
class PostgreSQLImageRepository implements IImageRepository {
    // ISP: Solo implementa lo que necesita
    async findById(id: string): Promise<Image> { /* ... */ }
    async save(image: Image): Promise<void> { /* ... */ }
}

// LSP: Diferentes implementaciones intercambiables
class AIImageProcessor implements IImageProcessor {
    async process(image: Image): Promise<ProcessedImage> { /* ... */ }
}

class TraditionalImageProcessor implements IImageProcessor {
    async process(image: Image): Promise<ProcessedImage> { /* ... */ }
}
```

## Beneficios de Aplicar SOLID

1. **Mantenibilidad**: Código más fácil de modificar y extender
2. **Testabilidad**: Fácil mockear dependencias y testear unitariamente
3. **Flexibilidad**: Intercambiar implementaciones sin afectar el código cliente
4. **Reutilización**: Componentes reutilizables en diferentes contextos
5. **Escalabilidad**: Estructura preparada para crecimiento del proyecto

## Checklist SOLID

- [ ] ¿Cada clase tiene una sola responsabilidad? (SRP)
- [ ] ¿Puedo agregar nueva funcionalidad sin modificar código existente? (OCP)
- [ ] ¿Las subclases pueden sustituir a sus clases base? (LSP)
- [ ] ¿Las interfaces son específicas y cohesivas? (ISP)
- [ ] ¿Dependo de abstracciones en lugar de implementaciones concretas? (DIP)

Aplicar estos principios desde el inicio del proyecto garantiza un código robusto y mantenible a largo plazo.
