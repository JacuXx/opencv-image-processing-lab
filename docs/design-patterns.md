# 🎨 Patrones de Diseño - Aplicación Práctica

Los patrones de diseño son soluciones reutilizables a problemas comunes en el diseño de software. En nuestra aplicación de upscale de imágenes, aplicaremos varios patrones clave.

## 🏭 Patrones Creacionales

### Factory Pattern

**Problema**: Crear diferentes tipos de procesadores de imagen sin acoplar el código a clases específicas.

```typescript
interface ImageProcessor {
    process(image: Image): Promise<ProcessedImage>;
}

class AIImageProcessor implements ImageProcessor {
    async process(image: Image): Promise<ProcessedImage> {
        // Procesamiento con IA
        return this.processWithAI(image);
    }
}

class TraditionalImageProcessor implements ImageProcessor {
    async process(image: Image): Promise<ProcessedImage> {
        // Procesamiento tradicional
        return this.processWithAlgorithms(image);
    }
}

class ImageProcessorFactory {
    static create(type: ProcessorType): ImageProcessor {
        switch (type) {
            case ProcessorType.AI:
                return new AIImageProcessor();
            case ProcessorType.TRADITIONAL:
                return new TraditionalImageProcessor();
            default:
                throw new Error(`Unsupported processor type: ${type}`);
        }
    }
}

// Uso
const processor = ImageProcessorFactory.create(ProcessorType.AI);
const result = await processor.process(image);
```

### Builder Pattern

**Problema**: Construir objetos complejos de configuración paso a paso.

```typescript
class UpscaleConfigBuilder {
    private config: UpscaleConfig;

    constructor() {
        this.config = new UpscaleConfig();
    }

    setScale(scale: number): UpscaleConfigBuilder {
        this.config.scale = scale;
        return this;
    }

    setQuality(quality: Quality): UpscaleConfigBuilder {
        this.config.quality = quality;
        return this;
    }

    setFormat(format: ImageFormat): UpscaleConfigBuilder {
        this.config.outputFormat = format;
        return this;
    }

    setFilters(filters: Filter[]): UpscaleConfigBuilder {
        this.config.filters = filters;
        return this;
    }

    enableNoiseReduction(): UpscaleConfigBuilder {
        this.config.noiseReduction = true;
        return this;
    }

    build(): UpscaleConfig {
        this.validate();
        return this.config;
    }

    private validate(): void {
        if (this.config.scale <= 0) {
            throw new Error('Scale must be positive');
        }
        // Más validaciones...
    }
}

// Uso
const config = new UpscaleConfigBuilder()
    .setScale(4)
    .setQuality(Quality.HIGH)
    .setFormat(ImageFormat.PNG)
    .enableNoiseReduction()
    .build();
```

### Singleton Pattern

**Problema**: Garantizar una sola instancia de configuración global.

```typescript
class AppConfig {
    private static instance: AppConfig;
    private configuration: ConfigData;

    private constructor() {
        this.loadConfiguration();
    }

    static getInstance(): AppConfig {
        if (!AppConfig.instance) {
            AppConfig.instance = new AppConfig();
        }
        return AppConfig.instance;
    }

    get databaseUrl(): string {
        return this.configuration.database.url;
    }

    get maxFileSize(): number {
        return this.configuration.upload.maxFileSize;
    }

    private loadConfiguration(): void {
        // Cargar configuración desde archivo/variables de entorno
    }
}

// Uso
const config = AppConfig.getInstance();
const dbUrl = config.databaseUrl;
```

## 🔧 Patrones Estructurales

### Adapter Pattern

**Problema**: Integrar servicios de terceros con interfaces incompatibles.

```typescript
// Servicio externo con interfaz diferente
class ExternalAIService {
    enhanceImage(imageData: Buffer, options: any): Promise<Buffer> {
        // Implementación del servicio externo
    }
}

// Nuestra interfaz estándar
interface ImageProcessor {
    process(image: Image): Promise<ProcessedImage>;
}

// Adapter para el servicio externo
class ExternalAIServiceAdapter implements ImageProcessor {
    constructor(private externalService: ExternalAIService) {}

    async process(image: Image): Promise<ProcessedImage> {
        // Adaptar nuestros datos al formato externo
        const buffer = image.toBuffer();
        const options = {
            scale: image.targetScale,
            quality: image.quality
        };

        // Llamar al servicio externo
        const resultBuffer = await this.externalService.enhanceImage(buffer, options);

        // Adaptar la respuesta a nuestro formato
        return ProcessedImage.fromBuffer(resultBuffer, image.metadata);
    }
}

// Uso
const externalService = new ExternalAIService();
const adapter = new ExternalAIServiceAdapter(externalService);
const result = await adapter.process(image);
```

### Decorator Pattern

**Problema**: Agregar funcionalidades adicionales sin modificar clases existentes.

```typescript
interface ImageProcessor {
    process(image: Image): Promise<ProcessedImage>;
}

class BaseImageProcessor implements ImageProcessor {
    async process(image: Image): Promise<ProcessedImage> {
        // Procesamiento básico
        return new ProcessedImage(image.data);
    }
}

// Decoradores
class LoggingDecorator implements ImageProcessor {
    constructor(private processor: ImageProcessor) {}

    async process(image: Image): Promise<ProcessedImage> {
        console.log(`Processing image: ${image.id}`);
        const start = Date.now();

        const result = await this.processor.process(image);

        const duration = Date.now() - start;
        console.log(`Processed in ${duration}ms`);

        return result;
    }
}

class CachingDecorator implements ImageProcessor {
    constructor(
        private processor: ImageProcessor,
        private cache: Cache
    ) {}

    async process(image: Image): Promise<ProcessedImage> {
        const cacheKey = this.generateCacheKey(image);

        const cached = await this.cache.get(cacheKey);
        if (cached) {
            return cached;
        }

        const result = await this.processor.process(image);
        await this.cache.set(cacheKey, result);

        return result;
    }
}

class CompressionDecorator implements ImageProcessor {
    constructor(private processor: ImageProcessor) {}

    async process(image: Image): Promise<ProcessedImage> {
        const result = await this.processor.process(image);
        return this.compressImage(result);
    }
}

// Uso combinado
let processor: ImageProcessor = new BaseImageProcessor();
processor = new LoggingDecorator(processor);
processor = new CachingDecorator(processor, cache);
processor = new CompressionDecorator(processor);

const result = await processor.process(image);
```

## ⚡ Patrones Comportamentales

### Strategy Pattern

**Problema**: Seleccionar algoritmos de procesamiento dinámicamente.

```typescript
interface UpscaleStrategy {
    upscale(image: Image, scale: number): Promise<ProcessedImage>;
}

class BilinearUpscaleStrategy implements UpscaleStrategy {
    async upscale(image: Image, scale: number): Promise<ProcessedImage> {
        // Implementación bilinear
        return this.bilinearUpscale(image, scale);
    }
}

class BicubicUpscaleStrategy implements UpscaleStrategy {
    async upscale(image: Image, scale: number): Promise<ProcessedImage> {
        // Implementación bicubic
        return this.bicubicUpscale(image, scale);
    }
}

class AIUpscaleStrategy implements UpscaleStrategy {
    async upscale(image: Image, scale: number): Promise<ProcessedImage> {
        // Implementación con IA
        return this.aiUpscale(image, scale);
    }
}

class ImageUpscaler {
    constructor(private strategy: UpscaleStrategy) {}

    setStrategy(strategy: UpscaleStrategy): void {
        this.strategy = strategy;
    }

    async upscale(image: Image, scale: number): Promise<ProcessedImage> {
        return await this.strategy.upscale(image, scale);
    }
}

// Uso
const upscaler = new ImageUpscaler(new BilinearUpscaleStrategy());

// Cambiar estrategia basado en condiciones
if (image.size > LARGE_SIZE_THRESHOLD) {
    upscaler.setStrategy(new AIUpscaleStrategy());
} else {
    upscaler.setStrategy(new BicubicUpscaleStrategy());
}

const result = await upscaler.upscale(image, 4);
```

### Observer Pattern

**Problema**: Notificar a múltiples componentes sobre el progreso del procesamiento.

```typescript
interface ProgressObserver {
    onProgressUpdate(progress: ProcessingProgress): void;
}

class ProcessingProgress {
    constructor(
        public readonly imageId: string,
        public readonly percentage: number,
        public readonly stage: ProcessingStage,
        public readonly message: string
    ) {}
}

class ImageProcessingService {
    private observers: ProgressObserver[] = [];

    addObserver(observer: ProgressObserver): void {
        this.observers.push(observer);
    }

    removeObserver(observer: ProgressObserver): void {
        const index = this.observers.indexOf(observer);
        if (index > -1) {
            this.observers.splice(index, 1);
        }
    }

    private notifyObservers(progress: ProcessingProgress): void {
        this.observers.forEach(observer => {
            observer.onProgressUpdate(progress);
        });
    }

    async processImage(image: Image): Promise<ProcessedImage> {
        this.notifyObservers(new ProcessingProgress(
            image.id, 0, ProcessingStage.LOADING, 'Loading image...'
        ));

        // Procesamiento paso a paso
        await this.loadImage(image);
        this.notifyObservers(new ProcessingProgress(
            image.id, 25, ProcessingStage.PREPROCESSING, 'Preprocessing...'
        ));

        await this.preprocess(image);
        this.notifyObservers(new ProcessingProgress(
            image.id, 50, ProcessingStage.UPSCALING, 'Upscaling...'
        ));

        const result = await this.upscale(image);
        this.notifyObservers(new ProcessingProgress(
            image.id, 100, ProcessingStage.COMPLETE, 'Processing complete!'
        ));

        return result;
    }
}

// Observadores concretos
class WebSocketNotifier implements ProgressObserver {
    onProgressUpdate(progress: ProcessingProgress): void {
        this.websocket.send(JSON.stringify(progress));
    }
}

class DatabaseLogger implements ProgressObserver {
    onProgressUpdate(progress: ProcessingProgress): void {
        this.database.logProgress(progress);
    }
}

class EmailNotifier implements ProgressObserver {
    onProgressUpdate(progress: ProcessingProgress): void {
        if (progress.percentage === 100) {
            this.emailService.sendCompletionEmail(progress.imageId);
        }
    }
}

// Uso
const processor = new ImageProcessingService();
processor.addObserver(new WebSocketNotifier(websocket));
processor.addObserver(new DatabaseLogger(database));
processor.addObserver(new EmailNotifier(emailService));
```

### Command Pattern

**Problema**: Encapsular operaciones como objetos para deshacer, hacer cola, etc.

```typescript
interface Command {
    execute(): Promise<void>;
    undo(): Promise<void>;
}

class UpscaleImageCommand implements Command {
    constructor(
        private imageId: string,
        private scale: number,
        private processor: ImageProcessor,
        private repository: ImageRepository
    ) {}

    async execute(): Promise<void> {
        const image = await this.repository.findById(this.imageId);
        const processed = await this.processor.process(image);
        await this.repository.save(processed);

        // Guardar estado para deshacer
        this.originalImage = image;
    }

    async undo(): Promise<void> {
        if (this.originalImage) {
            await this.repository.save(this.originalImage);
        }
    }
}

class CommandInvoker {
    private history: Command[] = [];
    private currentPosition = -1;

    async executeCommand(command: Command): Promise<void> {
        // Eliminar comandos posteriores si estamos en medio del historial
        this.history = this.history.slice(0, this.currentPosition + 1);

        await command.execute();
        this.history.push(command);
        this.currentPosition++;
    }

    async undo(): Promise<void> {
        if (this.currentPosition >= 0) {
            const command = this.history[this.currentPosition];
            await command.undo();
            this.currentPosition--;
        }
    }

    async redo(): Promise<void> {
        if (this.currentPosition < this.history.length - 1) {
            this.currentPosition++;
            const command = this.history[this.currentPosition];
            await command.execute();
        }
    }
}
```

## 🏗️ Patrones Arquitecturales

### Repository Pattern

```typescript
interface ImageRepository {
    findById(id: string): Promise<Image | null>;
    findByUserId(userId: string): Promise<Image[]>;
    save(image: Image): Promise<void>;
    delete(id: string): Promise<void>;
}

class DatabaseImageRepository implements ImageRepository {
    constructor(private database: Database) {}

    async findById(id: string): Promise<Image | null> {
        const row = await this.database.query(
            'SELECT * FROM images WHERE id = $1', [id]
        );
        return row ? this.mapToEntity(row) : null;
    }

    async save(image: Image): Promise<void> {
        const data = this.mapToData(image);
        await this.database.query(
            'INSERT INTO images (id, filename, data) VALUES ($1, $2, $3)',
            [data.id, data.filename, data.data]
        );
    }
}
```

### Unit of Work Pattern

```typescript
class UnitOfWork {
    private repositories: Map<string, Repository> = new Map();
    private newEntities: Entity[] = [];
    private modifiedEntities: Entity[] = [];
    private deletedEntities: Entity[] = [];

    registerNew(entity: Entity): void {
        this.newEntities.push(entity);
    }

    registerModified(entity: Entity): void {
        this.modifiedEntities.push(entity);
    }

    registerDeleted(entity: Entity): void {
        this.deletedEntities.push(entity);
    }

    async commit(): Promise<void> {
        await this.database.beginTransaction();

        try {
            // Insertar nuevas entidades
            for (const entity of this.newEntities) {
                await this.getRepository(entity.constructor.name).insert(entity);
            }

            // Actualizar entidades modificadas
            for (const entity of this.modifiedEntities) {
                await this.getRepository(entity.constructor.name).update(entity);
            }

            // Eliminar entidades
            for (const entity of this.deletedEntities) {
                await this.getRepository(entity.constructor.name).delete(entity);
            }

            await this.database.commit();
            this.clear();
        } catch (error) {
            await this.database.rollback();
            throw error;
        }
    }
}
```

## Aplicación Integrada

```typescript
// Combinando múltiples patrones en un caso de uso
class UpscaleImageUseCase {
    constructor(
        private processorFactory: ImageProcessorFactory,
        private repository: ImageRepository,
        private unitOfWork: UnitOfWork,
        private commandInvoker: CommandInvoker
    ) {}

    async execute(request: UpscaleImageRequest): Promise<UpscaleImageResponse> {
        // Factory Pattern: Crear el procesador adecuado
        const processor = this.processorFactory.create(request.processorType);

        // Decorator Pattern: Agregar logging y cache
        const decoratedProcessor = new LoggingDecorator(
            new CachingDecorator(processor, this.cache)
        );

        // Command Pattern: Encapsular la operación
        const command = new UpscaleImageCommand(
            request.imageId,
            request.scale,
            decoratedProcessor,
            this.repository
        );

        // Strategy Pattern: El procesador usa diferentes estrategias
        decoratedProcessor.setStrategy(
            this.selectStrategy(request.quality, request.imageSize)
        );

        // Observer Pattern: Notificar progreso
        decoratedProcessor.addObserver(this.progressNotifier);

        // Ejecutar comando
        await this.commandInvoker.executeCommand(command);

        // Unit of Work: Confirmar cambios
        await this.unitOfWork.commit();

        return new UpscaleImageResponse(request.imageId);
    }
}
```

Los patrones de diseño nos permiten crear código más flexible, mantenible y reutilizable, facilitando la evolución y extensión de nuestra aplicación.
