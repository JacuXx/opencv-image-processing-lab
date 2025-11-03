# 🏗️ Arquitectura Clean - Guía Detallada

## Introducción a Clean Architecture

Clean Architecture es un patrón arquitectónico propuesto por Robert C. Martin que organiza el código de manera que sea:

- **Independiente de frameworks**: La arquitectura no depende de bibliotecas específicas
- **Testeable**: Las reglas de negocio se pueden probar sin UI, BD, servidores web, etc.
- **Independiente de la UI**: La UI puede cambiar sin afectar el resto del sistema
- **Independiente de la base de datos**: Oracle, SQL Server, MongoDB, etc. son detalles
- **Independiente de agencias externas**: Las reglas de negocio no saben nada sobre el mundo exterior

## Las 4 Capas de Clean Architecture

### 1. 🎯 Domain Layer (Entidades)

La capa más interna y estable del sistema. Contiene:

```
domain/
├── entities/          # Objetos de negocio principales
│   ├── Image.ts
│   ├── User.ts
│   └── UpscaleJob.ts
├── value-objects/     # Objetos inmutables con validación
│   ├── ImageFormat.ts
│   ├── Resolution.ts
│   └── Email.ts
├── repositories/      # Interfaces para acceso a datos
│   ├── IImageRepository.ts
│   ├── IUserRepository.ts
│   └── IJobRepository.ts
└── services/          # Servicios de dominio
    ├── ImageValidationService.ts
    └── UpscaleAlgorithmService.ts
```

**Características:**
- No depende de ninguna otra capa
- Contiene las reglas de negocio más importantes
- Define interfaces pero no implementaciones
- Altamente testeable

### 2. 🔧 Application Layer (Casos de Uso)

Contiene la lógica específica de la aplicación:

```
application/
├── use-cases/         # Casos de uso específicos
│   ├── UpscaleImageUseCase.ts
│   ├── GetImageHistoryUseCase.ts
│   ├── RegisterUserUseCase.ts
│   └── DeleteImageUseCase.ts
├── interfaces/        # Interfaces para servicios externos
│   ├── IImageProcessingService.ts
│   ├── IStorageService.ts
│   └── INotificationService.ts
├── dtos/             # Data Transfer Objects
│   ├── UpscaleImageRequest.ts
│   ├── ImageResponse.ts
│   └── UserRegistrationRequest.ts
└── exceptions/       # Excepciones específicas de aplicación
    ├── ImageNotFoundError.ts
    ├── InvalidFormatError.ts
    └── ProcessingError.ts
```

**Características:**
- Orquesta el flujo de datos hacia y desde las entidades
- Depende solo de la capa de dominio
- Define qué hace la aplicación, no cómo lo hace

### 3. 🔌 Infrastructure Layer (Adaptadores de Interface)

Implementa las interfaces definidas en capas internas:

```
infrastructure/
├── repositories/      # Implementaciones de repositorios
│   ├── PostgresImageRepository.ts
│   ├── MongoUserRepository.ts
│   └── RedisJobRepository.ts
├── services/         # Servicios externos
│   ├── S3StorageService.ts
│   ├── OpenAIUpscaleService.ts
│   └── EmailNotificationService.ts
├── database/         # Configuración de base de datos
│   ├── migrations/
│   ├── seeds/
│   └── config.ts
├── config/           # Configuraciones
│   ├── database.config.ts
│   ├── storage.config.ts
│   └── app.config.ts
└── external/         # APIs externas
    ├── ImageProcessingAPI.ts
    └── PaymentGateway.ts
```

### 4. 🖥️ Presentation Layer (Frameworks y Drivers)

La capa más externa que maneja la interacción con el usuario:

```
presentation/
├── controllers/      # Controladores HTTP/API
│   ├── ImageController.ts
│   ├── UserController.ts
│   └── JobController.ts
├── middlewares/      # Middlewares de autenticación, validación, etc.
│   ├── AuthMiddleware.ts
│   ├── ValidationMiddleware.ts
│   └── ErrorHandlerMiddleware.ts
├── routes/           # Definición de rutas
│   ├── imageRoutes.ts
│   ├── userRoutes.ts
│   └── index.ts
├── ui/              # Interfaz de usuario (si aplica)
│   ├── components/
│   ├── pages/
│   └── styles/
└── dto-mappers/     # Mapeo entre DTOs y objetos de dominio
    ├── ImageMapper.ts
    └── UserMapper.ts
```

## Flujo de Dependencias

```
Presentation → Application → Domain
Infrastructure → Application → Domain
```

**Regla de Dependencia**: Las capas internas no deben conocer nada sobre las capas externas.

## Ejemplo Práctico: Upscale de Imagen

### 1. Request (Presentation)
```typescript
// ImageController.ts
@Post('/upscale')
async upscaleImage(@Body() request: UpscaleImageRequest) {
    const useCase = new UpscaleImageUseCase(
        this.imageRepository,
        this.processingService,
        this.storageService
    );

    return await useCase.execute(request);
}
```

### 2. Use Case (Application)
```typescript
// UpscaleImageUseCase.ts
async execute(request: UpscaleImageRequest): Promise<ImageResponse> {
    // Validar entrada
    const image = await this.imageRepository.findById(request.imageId);

    // Procesar imagen
    const upscaledImage = await this.processingService.upscale(image, request.scale);

    // Guardar resultado
    const savedImage = await this.storageService.save(upscaledImage);

    return ImageMapper.toResponse(savedImage);
}
```

### 3. Domain Entity
```typescript
// Image.ts
export class Image {
    constructor(
        private id: string,
        private filename: string,
        private format: ImageFormat,
        private resolution: Resolution
    ) {}

    canBeUpscaled(): boolean {
        return this.resolution.isValid() && this.format.supportsUpscaling();
    }
}
```

## Beneficios de esta Arquitectura

1. **Testabilidad**: Cada capa se puede testear independientemente
2. **Flexibilidad**: Cambiar tecnologías sin afectar la lógica de negocio
3. **Mantenibilidad**: Código organizado y fácil de entender
4. **Escalabilidad**: Estructura preparada para crecimiento
5. **Reutilización**: Casos de uso reutilizables en diferentes interfaces

## Principios Clave

- **Dependency Inversion**: Depender de abstracciones
- **Single Responsibility**: Una clase, una responsabilidad
- **Open/Closed**: Abierto para extensión, cerrado para modificación
- **Interface Segregation**: Interfaces específicas y pequeñas
- **Liskov Substitution**: Objetos intercambiables

## Testing Strategy

```
tests/
├── unit/             # Tests unitarios por capa
│   ├── domain/
│   ├── application/
│   └── infrastructure/
├── integration/      # Tests de integración
│   ├── repositories/
│   └── services/
└── e2e/             # Tests end-to-end
    └── api/
```

Esta arquitectura garantiza que tu aplicación sea robusta, mantenible y preparada para escalar.
