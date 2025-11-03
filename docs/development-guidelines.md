# 📐 Guías de Desarrollo - Estándares y Mejores Prácticas

Esta guía establece los estándares de desarrollo, convenciones de código y mejores prácticas para mantener la calidad y consistencia en nuestro proyecto de upscale de imágenes.

## 📋 Tabla de Contenidos

- [🎨 Estilo de Código](#-estilo-de-código)
- [📁 Estructura de Archivos](#-estructura-de-archivos)
- [🏷️ Convenciones de Nomenclatura](#️-convenciones-de-nomenclatura)
- [📝 Documentación](#-documentación)
- [🔧 Git Workflow](#-git-workflow)
- [🐛 Debugging](#-debugging)
- [⚡ Optimización](#-optimización)
- [🔒 Seguridad](#-seguridad)

## 🎨 Estilo de Código

### TypeScript/JavaScript

#### Configuración ESLint

```javascript
// .eslintrc.js
module.exports = {
    extends: [
        '@typescript-eslint/recommended',
        'prettier',
        'plugin:import/typescript'
    ],
    plugins: ['@typescript-eslint', 'import'],
    rules: {
        // Imports
        'import/order': ['error', {
            'groups': [
                'builtin',
                'external',
                'internal',
                'parent',
                'sibling',
                'index'
            ],
            'newlines-between': 'always'
        }],
        'import/no-relative-parent-imports': 'error',

        // TypeScript
        '@typescript-eslint/explicit-function-return-type': 'error',
        '@typescript-eslint/no-explicit-any': 'error',
        '@typescript-eslint/no-unused-vars': 'error',
        '@typescript-eslint/prefer-readonly': 'error',

        // General
        'prefer-const': 'error',
        'no-var': 'error',
        'no-console': 'warn',
        'max-len': ['error', { code: 100 }],
        'complexity': ['warn', 10]
    }
};
```

#### Configuración Prettier

```javascript
// .prettierrc.js
module.exports = {
    semi: true,
    trailingComma: 'es5',
    singleQuote: true,
    printWidth: 100,
    tabWidth: 4,
    useTabs: false,
    bracketSpacing: true,
    arrowParens: 'avoid'
};
```

### Ejemplos de Código Bien Formateado

#### ✅ Buenas Prácticas

```typescript
// domain/entities/Image.ts
import { ImageId } from '../value-objects/ImageId';
import { UserId } from '../value-objects/UserId';
import { ImageDimensions } from '../value-objects/ImageDimensions';
import { ImageFormat } from '../enums/ImageFormat';
import { ImageStatus } from '../enums/ImageStatus';

import { InvalidImageStatusError } from '../errors/InvalidImageStatusError';

/**
 * Represents an image entity in the domain
 */
export class Image {
    constructor(
        public readonly id: ImageId,
        public readonly userId: UserId,
        public readonly filename: string,
        public readonly originalFilename: string,
        public readonly fileSize: number,
        public readonly dimensions: ImageDimensions,
        public readonly format: ImageFormat,
        public readonly storagePath: string,
        public readonly thumbnailPath: string | null = null,
        private status: ImageStatus = ImageStatus.UPLOADED,
        public readonly createdAt: Date = new Date(),
        private updatedAt: Date = new Date()
    ) {}

    /**
     * Checks if the image can be processed
     * @returns true if the image is in a valid state for processing
     */
    public canBeProcessed(): boolean {
        return (
            this.status === ImageStatus.UPLOADED ||
            this.status === ImageStatus.PROCESSED
        );
    }

    /**
     * Marks the image as currently being processed
     * @throws InvalidImageStatusError if image cannot be processed
     */
    public markAsProcessing(): void {
        if (!this.canBeProcessed()) {
            throw new InvalidImageStatusError(
                `Cannot process image with status: ${this.status}`
            );
        }

        this.status = ImageStatus.PROCESSING;
        this.updatedAt = new Date();
    }

    /**
     * Gets the current status of the image
     */
    public getStatus(): ImageStatus {
        return this.status;
    }

    /**
     * Calculates if this is considered a large file
     */
    public get isLargeFile(): boolean {
        const LARGE_FILE_THRESHOLD = 10 * 1024 * 1024; // 10MB
        return this.fileSize > LARGE_FILE_THRESHOLD;
    }
}
```

#### ❌ Malas Prácticas

```typescript
// Evitar esto:
export class image {  // PascalCase para clases
    constructor(
        public id: string,  // Usar value objects
        public user_id: string,  // camelCase para propiedades
        public file_name: string,
        // ... otros campos sin tipos específicos
        private _status: string  // No usar underscore prefix
    ) {}

    // Método sin documentación y tipo de retorno
    canProcess() {
        return this._status == "uploaded";  // Usar === y enum
    }

    // Método que hace demasiadas cosas (viola SRP)
    processAndSave(processingType, params, database, storage) {
        // validación
        if (!this.canProcess()) return false;

        // procesamiento
        let result = this.doProcessing(processingType, params);

        // guardado en base de datos
        database.save(result);

        // guardado en storage
        storage.upload(result);

        return true;
    }
}
```

## 📁 Estructura de Archivos

### Organización por Capas

```
src/
├── domain/                         # Capa de Dominio
│   ├── entities/                   # Entidades de negocio
│   │   ├── Image.ts
│   │   ├── User.ts
│   │   └── ProcessingJob.ts
│   ├── value-objects/              # Objetos de valor
│   │   ├── ImageId.ts
│   │   ├── UserId.ts
│   │   ├── Email.ts
│   │   └── ImageDimensions.ts
│   ├── enums/                      # Enumeraciones
│   │   ├── ImageFormat.ts
│   │   ├── ImageStatus.ts
│   │   └── PlanType.ts
│   ├── errors/                     # Errores de dominio
│   │   ├── DomainError.ts
│   │   ├── InvalidEmailError.ts
│   │   └── StorageLimitExceededError.ts
│   ├── repositories/               # Interfaces de repositorios
│   │   ├── IImageRepository.ts
│   │   └── IUserRepository.ts
│   └── services/                   # Servicios de dominio
│       ├── ImageValidationService.ts
│       └── StorageQuotaService.ts
├── application/                    # Capa de Aplicación
│   ├── use-cases/                  # Casos de uso
│   │   ├── images/
│   │   │   ├── UploadImageUseCase.ts
│   │   │   ├── UpscaleImageUseCase.ts
│   │   │   └── GetImageHistoryUseCase.ts
│   │   └── users/
│   │       ├── RegisterUserUseCase.ts
│   │       └── AuthenticateUserUseCase.ts
│   ├── dtos/                       # Data Transfer Objects
│   │   ├── requests/
│   │   │   ├── UploadImageRequest.ts
│   │   │   └── UpscaleImageRequest.ts
│   │   └── responses/
│   │       ├── ImageResponse.ts
│   │       └── UserResponse.ts
│   ├── interfaces/                 # Interfaces de servicios
│   │   ├── IImageProcessingService.ts
│   │   ├── IStorageService.ts
│   │   └── INotificationService.ts
│   └── mappers/                    # Mappers entre capas
│       ├── ImageMapper.ts
│       └── UserMapper.ts
├── infrastructure/                 # Capa de Infraestructura
│   ├── database/
│   │   ├── repositories/
│   │   │   ├── PostgresImageRepository.ts
│   │   │   └── PostgresUserRepository.ts
│   │   ├── migrations/
│   │   └── config/
│   ├── storage/
│   │   ├── S3StorageService.ts
│   │   └── LocalStorageService.ts
│   ├── external-services/
│   │   ├── OpenAIImageService.ts
│   │   └── EmailService.ts
│   └── config/
│       ├── database.config.ts
│       └── app.config.ts
└── presentation/                   # Capa de Presentación
    ├── controllers/
    │   ├── ImageController.ts
    │   └── UserController.ts
    ├── middlewares/
    │   ├── AuthMiddleware.ts
    │   └── ValidationMiddleware.ts
    ├── routes/
    │   ├── imageRoutes.ts
    │   └── userRoutes.ts
    └── validators/
        ├── ImageUploadValidator.ts
        └── UserRegistrationValidator.ts
```

### Convenciones de Archivos

- **Archivos de entidades**: PascalCase (ej: `Image.ts`, `User.ts`)
- **Archivos de servicios**: PascalCase + sufijo Service (ej: `ImageProcessingService.ts`)
- **Archivos de interfaces**: PascalCase + prefijo I (ej: `IImageRepository.ts`)
- **Archivos de tests**: Mismo nombre + `.test.ts` (ej: `Image.test.ts`)
- **Archivos de configuración**: camelCase + `.config.ts` (ej: `database.config.ts`)

## 🏷️ Convenciones de Nomenclatura

### Variables y Funciones (camelCase)

```typescript
// ✅ Correcto
const imageProcessor = new ImageProcessor();
const uploadedImages = await getUploadedImages();
const canUserUploadImage = user.hasStorageSpace();

// ❌ Incorrecto
const ImageProcessor = new ImageProcessor();  // PascalCase solo para clases
const uploaded_images = await get_uploaded_images();  // snake_case no se usa
const CanUserUploadImage = user.hasStorageSpace();  // PascalCase no se usa
```

### Clases y Interfaces (PascalCase)

```typescript
// ✅ Correcto
class ImageUpscaler implements IImageProcessor {
    // ...
}

interface INotificationService {
    // ...
}

// ❌ Incorrecto
class imageUpscaler implements iImageProcessor {  // Debe ser PascalCase
    // ...
}
```

### Constantes (UPPER_SNAKE_CASE)

```typescript
// ✅ Correcto
const MAX_FILE_SIZE = 10 * 1024 * 1024;  // 10MB
const SUPPORTED_FORMATS = ['jpeg', 'png', 'webp'];
const API_BASE_URL = 'https://api.example.com';

// ❌ Incorrecto
const maxFileSize = 10 * 1024 * 1024;  // Debe ser UPPER_SNAKE_CASE
const supportedFormats = ['jpeg', 'png', 'webp'];
```

### Métodos Booleanos

```typescript
// ✅ Correcto - Usar prefijos is, has, can, should
const isImageValid = image.isValid();
const hasPermission = user.hasPermission('upload');
const canProcess = job.canProcess();
const shouldRetry = error.shouldRetry();

// ❌ Incorrecto
const imageValid = image.valid();  // Falta prefijo
const permission = user.permission();  // No es claro que retorna boolean
```

### Eventos y Callbacks

```typescript
// ✅ Correcto - Usar 'on' prefix para eventos
class ImageProcessor {
    onProcessingStarted(callback: (imageId: string) => void): void { }
    onProgressUpdated(callback: (progress: number) => void): void { }
    onProcessingCompleted(callback: (result: ProcessedImage) => void): void { }
}

// ✅ Correcto - Usar 'handle' prefix para handlers
class ImageController {
    handleUploadImage(request: Request, response: Response): Promise<void> { }
    handleGetImages(request: Request, response: Response): Promise<void> { }
}
```

## 📝 Documentación

### JSDoc para Métodos Públicos

```typescript
/**
 * Uploads an image file to the storage system
 *
 * @param file - The image file to upload
 * @param userId - The ID of the user uploading the image
 * @param options - Optional configuration for the upload
 * @returns Promise that resolves to the uploaded image metadata
 *
 * @throws {InvalidFileFormatError} When the file format is not supported
 * @throws {StorageLimitExceededError} When user's storage limit is exceeded
 * @throws {UploadError} When the upload process fails
 *
 * @example
 * ```typescript
 * const imageFile = new File([buffer], 'photo.jpg', { type: 'image/jpeg' });
 * const result = await uploadImage(imageFile, 'user-123', {
 *   generateThumbnail: true
 * });
 * console.log(`Image uploaded: ${result.id}`);
 * ```
 */
public async uploadImage(
    file: File,
    userId: string,
    options: UploadOptions = {}
): Promise<UploadResult> {
    // Implementation...
}
```

### README para Módulos

```typescript
// src/domain/README.md
/**
 * # Domain Layer
 *
 * This layer contains the core business logic and rules of the application.
 * It is independent of any external concerns like databases, APIs, or UI frameworks.
 *
 * ## Structure
 *
 * - `entities/` - Core business entities with behavior
 * - `value-objects/` - Immutable objects that represent domain concepts
 * - `repositories/` - Interfaces for data access
 * - `services/` - Domain services that don't belong to a specific entity
 * - `errors/` - Domain-specific error types
 *
 * ## Key Principles
 *
 * 1. **No dependencies on outer layers** - Domain should not import from application, infrastructure, or presentation layers
 * 2. **Rich domain model** - Entities should contain business logic, not just data
 * 3. **Ubiquitous language** - Use the same terms that business stakeholders use
 *
 * ## Examples
 *
 * ```typescript
 * // Creating a new image entity
 * const image = new Image(
 *     new ImageId('img-123'),
 *     new UserId('user-456'),
 *     'vacation-photo.jpg',
 *     1920,
 *     1080,
 *     ImageFormat.JPEG
 * );
 *
 * // Business rule enforcement
 * if (image.canBeUpscaled()) {
 *     image.markAsProcessing();
 * }
 * ```
 */
```

## 🔧 Git Workflow

### Convenciones de Commits

#### Formato de Commit Messages

```
type(scope): description

[optional body]

[optional footer]
```

#### Tipos de Commits

- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Cambios de formato (no afectan la lógica)
- `refactor`: Refactoring de código
- `test`: Agregar o modificar tests
- `chore`: Mantenimiento (build, deps, etc.)

#### Ejemplos

```bash
# ✅ Correcto
feat(upload): add support for WebP format
fix(auth): resolve token expiration issue
docs(api): update upload endpoint documentation
test(user): add unit tests for user registration
refactor(image): extract validation logic to service

# ❌ Incorrecto
add webp support  # Falta tipo y scope
fixed bug  # Muy vago
Updated code  # No es descriptivo
```

### Branch Strategy

```
main
├── develop
│   ├── feature/image-upload-validation
│   ├── feature/user-authentication
│   └── feature/ai-upscaling-integration
├── release/v1.2.0
└── hotfix/fix-storage-leak
```

#### Reglas de Branching

1. **main**: Solo código de producción
2. **develop**: Integración de features
3. **feature/***: Nuevas funcionalidades
4. **release/***: Preparación de releases
5. **hotfix/***: Correcciones urgentes

### Pull Request Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No console logs left
- [ ] Performance impact considered

## Screenshots (if applicable)
[Add screenshots here]

## Related Issues
Closes #123
```

## 🐛 Debugging

### Logging Strategy

```typescript
// utils/Logger.ts
import winston from 'winston';

export class Logger {
    private static instance: winston.Logger;

    static getInstance(): winston.Logger {
        if (!Logger.instance) {
            Logger.instance = winston.createLogger({
                level: process.env.LOG_LEVEL || 'info',
                format: winston.format.combine(
                    winston.format.timestamp(),
                    winston.format.errors({ stack: true }),
                    winston.format.json()
                ),
                defaultMeta: { service: 'upscale-service' },
                transports: [
                    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
                    new winston.transports.File({ filename: 'logs/combined.log' }),
                    new winston.transports.Console({
                        format: winston.format.simple()
                    })
                ]
            });
        }
        return Logger.instance;
    }
}

// Uso en casos de uso
export class UpscaleImageUseCase {
    private readonly logger = Logger.getInstance();

    async execute(request: UpscaleImageRequest): Promise<UpscaleImageResponse> {
        this.logger.info('Starting image upscale', {
            imageId: request.imageId,
            scale: request.scale,
            userId: request.userId
        });

        try {
            // Lógica del caso de uso...
            this.logger.info('Image upscale completed successfully', {
                imageId: request.imageId,
                jobId: job.id
            });

            return response;
        } catch (error) {
            this.logger.error('Image upscale failed', {
                imageId: request.imageId,
                error: error.message,
                stack: error.stack
            });
            throw error;
        }
    }
}
```

### Error Handling

```typescript
// domain/errors/DomainError.ts
export abstract class DomainError extends Error {
    abstract readonly code: string;

    constructor(message: string, public readonly details?: any) {
        super(message);
        this.name = this.constructor.name;
    }
}

// domain/errors/ImageErrors.ts
export class ImageNotFoundError extends DomainError {
    readonly code = 'IMAGE_NOT_FOUND';

    constructor(imageId: string) {
        super(`Image with ID ${imageId} not found`);
    }
}

export class InvalidImageFormatError extends DomainError {
    readonly code = 'INVALID_IMAGE_FORMAT';

    constructor(format: string, supportedFormats: string[]) {
        super(`Format ${format} not supported. Supported: ${supportedFormats.join(', ')}`);
    }
}

// presentation/middlewares/ErrorHandlerMiddleware.ts
export class ErrorHandlerMiddleware {
    handle(error: Error, req: Request, res: Response, next: NextFunction): void {
        const logger = Logger.getInstance();

        if (error instanceof DomainError) {
            logger.warn('Domain error occurred', {
                code: error.code,
                message: error.message,
                details: error.details
            });

            res.status(400).json({
                error: {
                    code: error.code,
                    message: error.message
                }
            });
            return;
        }

        // Error no manejado
        logger.error('Unhandled error', {
            message: error.message,
            stack: error.stack
        });

        res.status(500).json({
            error: {
                code: 'INTERNAL_SERVER_ERROR',
                message: 'An unexpected error occurred'
            }
        });
    }
}
```

## ⚡ Optimización

### Performance Guidelines

#### Database Queries

```typescript
// ✅ Correcto - Usar índices y pagination
export class PostgresImageRepository implements IImageRepository {
    async findByUserId(
        userId: string,
        page: number = 1,
        limit: number = 20
    ): Promise<PaginatedResult<Image>> {
        const offset = (page - 1) * limit;

        // Query optimizada con índices
        const query = `
            SELECT i.*, COUNT(*) OVER() as total_count
            FROM images i
            WHERE i.user_id = $1
            AND i.status != 'deleted'
            ORDER BY i.created_at DESC
            LIMIT $2 OFFSET $3
        `;

        const result = await this.db.query(query, [userId, limit, offset]);

        return new PaginatedResult(
            result.rows.map(row => this.mapToEntity(row)),
            result.rows[0]?.total_count || 0,
            page,
            limit
        );
    }
}

// ❌ Incorrecto - Cargar todos los registros
async findByUserId(userId: string): Promise<Image[]> {
    const query = 'SELECT * FROM images WHERE user_id = $1';  // Sin paginación
    const result = await this.db.query(query, [userId]);
    return result.rows.map(row => this.mapToEntity(row));  // Puede ser miles de registros
}
```

#### Memory Management

```typescript
// ✅ Correcto - Procesar imágenes en streams
export class ImageProcessingService {
    async processLargeImage(imagePath: string): Promise<ProcessedImage> {
        return new Promise((resolve, reject) => {
            const readStream = fs.createReadStream(imagePath);
            const writeStream = fs.createWriteStream(outputPath);

            readStream
                .pipe(sharp().resize(3840, 2160))  // Procesar en chunks
                .pipe(writeStream)
                .on('finish', () => resolve(new ProcessedImage(outputPath)))
                .on('error', reject);
        });
    }
}

// ❌ Incorrecto - Cargar toda la imagen en memoria
async processLargeImage(imagePath: string): Promise<ProcessedImage> {
    const buffer = fs.readFileSync(imagePath);  // Carga completa en memoria
    const processed = await sharp(buffer).resize(3840, 2160).toBuffer();
    fs.writeFileSync(outputPath, processed);
    return new ProcessedImage(outputPath);
}
```

### Caching Strategy

```typescript
// infrastructure/cache/RedisCache.ts
export class RedisCache implements ICache {
    private client: Redis;

    async get<T>(key: string): Promise<T | null> {
        const value = await this.client.get(key);
        return value ? JSON.parse(value) : null;
    }

    async set<T>(key: string, value: T, ttl: number = 3600): Promise<void> {
        await this.client.setex(key, ttl, JSON.stringify(value));
    }

    async invalidate(pattern: string): Promise<void> {
        const keys = await this.client.keys(pattern);
        if (keys.length > 0) {
            await this.client.del(...keys);
        }
    }
}

// application/use-cases/GetImageHistoryUseCase.ts
export class GetImageHistoryUseCase {
    constructor(
        private imageRepository: IImageRepository,
        private cache: ICache
    ) {}

    async execute(request: GetImageHistoryRequest): Promise<GetImageHistoryResponse> {
        const cacheKey = `user_images:${request.userId}:${request.page}:${request.limit}`;

        // Intentar obtener del cache
        const cached = await this.cache.get<GetImageHistoryResponse>(cacheKey);
        if (cached) {
            return cached;
        }

        // Si no está en cache, obtener de la base de datos
        const result = await this.imageRepository.findByUserId(
            request.userId,
            request.page,
            request.limit
        );

        const response = new GetImageHistoryResponse(result);

        // Guardar en cache por 5 minutos
        await this.cache.set(cacheKey, response, 300);

        return response;
    }
}
```

## 🔒 Seguridad

### Input Validation

```typescript
// presentation/validators/ImageUploadValidator.ts
import Joi from 'joi';

export class ImageUploadValidator {
    private static readonly schema = Joi.object({
        filename: Joi.string()
            .pattern(/^[a-zA-Z0-9._-]+$/)  // Solo caracteres seguros
            .max(255)
            .required(),

        fileSize: Joi.number()
            .positive()
            .max(50 * 1024 * 1024)  // 50MB máximo
            .required(),

        mimeType: Joi.string()
            .valid('image/jpeg', 'image/png', 'image/webp')
            .required()
    });

    static validate(data: any): ValidationResult {
        const { error, value } = this.schema.validate(data);

        if (error) {
            return new ValidationResult(false, error.details[0].message);
        }

        return new ValidationResult(true, null, value);
    }
}

// presentation/middlewares/ValidationMiddleware.ts
export class ValidationMiddleware {
    static validateImageUpload(req: Request, res: Response, next: NextFunction): void {
        const file = req.file;

        if (!file) {
            return res.status(400).json({ error: 'No file provided' });
        }

        const validation = ImageUploadValidator.validate({
            filename: file.originalname,
            fileSize: file.size,
            mimeType: file.mimetype
        });

        if (!validation.isValid) {
            return res.status(400).json({ error: validation.error });
        }

        next();
    }
}
```

### Authentication & Authorization

```typescript
// presentation/middlewares/AuthMiddleware.ts
export class AuthMiddleware {
    static authenticate(req: Request, res: Response, next: NextFunction): void {
        const token = req.headers.authorization?.replace('Bearer ', '');

        if (!token) {
            return res.status(401).json({ error: 'No token provided' });
        }

        try {
            const decoded = jwt.verify(token, process.env.JWT_SECRET!);
            req.user = decoded as UserPayload;
            next();
        } catch (error) {
            return res.status(401).json({ error: 'Invalid token' });
        }
    }

    static authorize(permissions: string[]) {
        return (req: Request, res: Response, next: NextFunction): void => {
            const user = req.user;

            if (!user) {
                return res.status(401).json({ error: 'User not authenticated' });
            }

            const hasPermission = permissions.some(permission =>
                user.permissions.includes(permission)
            );

            if (!hasPermission) {
                return res.status(403).json({ error: 'Insufficient permissions' });
            }

            next();
        };
    }
}
```

### Data Sanitization

```typescript
// utils/Sanitizer.ts
export class Sanitizer {
    static sanitizeFilename(filename: string): string {
        return filename
            .replace(/[^a-zA-Z0-9._-]/g, '_')  // Reemplazar caracteres peligrosos
            .substring(0, 255);  // Limitar longitud
    }

    static sanitizeImageMetadata(metadata: any): SafeImageMetadata {
        return {
            width: this.sanitizeNumber(metadata.width, 1, 50000),
            height: this.sanitizeNumber(metadata.height, 1, 50000),
            format: this.sanitizeString(metadata.format, ['jpeg', 'png', 'webp']),
            colorSpace: this.sanitizeString(metadata.colorSpace, ['srgb', 'rgb', 'cmyk'])
        };
    }

    private static sanitizeNumber(value: any, min: number, max: number): number {
        const num = parseInt(value, 10);
        if (isNaN(num) || num < min || num > max) {
            throw new InvalidDataError(`Invalid number: ${value}`);
        }
        return num;
    }

    private static sanitizeString(value: any, allowedValues: string[]): string {
        const str = String(value).toLowerCase();
        if (!allowedValues.includes(str)) {
            throw new InvalidDataError(`Invalid value: ${value}`);
        }
        return str;
    }
}
```

### Rate Limiting

```typescript
// presentation/middlewares/RateLimitMiddleware.ts
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';
import Redis from 'ioredis';

export class RateLimitMiddleware {
    private static redis = new Redis(process.env.REDIS_URL);

    static createUploadLimit() {
        return rateLimit({
            store: new RedisStore({
                client: this.redis,
                prefix: 'rl:upload:'
            }),
            windowMs: 15 * 60 * 1000,  // 15 minutos
            max: 10,  // Máximo 10 uploads por ventana
            message: {
                error: 'Too many upload attempts, please try again later'
            },
            standardHeaders: true,
            legacyHeaders: false
        });
    }

    static createApiLimit() {
        return rateLimit({
            store: new RedisStore({
                client: this.redis,
                prefix: 'rl:api:'
            }),
            windowMs: 15 * 60 * 1000,
            max: 100,  // 100 requests por 15 minutos
            message: {
                error: 'Too many API requests, please try again later'
            }
        });
    }
}
```

Esta guía de desarrollo asegura que el código sea consistente, mantenible y seguro en todo el proyecto.
