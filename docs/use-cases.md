# 📝 Casos de Uso - Especificación Detallada

Los casos de uso definen las funcionalidades específicas de nuestra aplicación de upscale de imágenes desde la perspectiva del usuario.

## 👤 Actores del Sistema

### Usuario Registrado
- Puede subir imágenes
- Puede procesar imágenes (upscale, filtros, etc.)
- Puede gestionar su historial
- Puede descargar resultados

### Usuario Administrador
- Todas las funciones del usuario registrado
- Puede gestionar usuarios
- Puede ver estadísticas del sistema
- Puede configurar parámetros globales

### Sistema Externo
- APIs de procesamiento de IA
- Servicios de almacenamiento
- Sistemas de pago

## 🎯 Casos de Uso Principales

### UC-001: Registrar Usuario

**Descripción**: Un usuario se registra en el sistema para acceder a las funcionalidades.

**Actor Principal**: Usuario no registrado

**Precondiciones**:
- El usuario no está registrado en el sistema
- El sistema está disponible

**Flujo Principal**:
1. El usuario ingresa a la página de registro
2. El usuario proporciona email, contraseña y datos personales
3. El sistema valida los datos ingresados
4. El sistema verifica que el email no esté registrado
5. El sistema crea la cuenta del usuario
6. El sistema envía email de confirmación
7. El usuario confirma su email
8. El sistema activa la cuenta

**Flujos Alternativos**:
- **3a**: Datos inválidos → Mostrar errores de validación
- **4a**: Email ya registrado → Sugerir recuperación de contraseña
- **6a**: Error en envío de email → Permitir reenvío
- **7a**: Usuario no confirma → Cuenta permanece inactiva

**Postcondiciones**:
- Usuario registrado y activo en el sistema
- Email de bienvenida enviado

```typescript
// Implementación del caso de uso
class RegisterUserUseCase {
    constructor(
        private userRepository: IUserRepository,
        private emailService: IEmailService,
        private passwordHasher: IPasswordHasher
    ) {}

    async execute(request: RegisterUserRequest): Promise<RegisterUserResponse> {
        // Validar datos de entrada
        this.validateRequest(request);

        // Verificar que el email no exista
        const existingUser = await this.userRepository.findByEmail(request.email);
        if (existingUser) {
            throw new UserAlreadyExistsError(request.email);
        }

        // Crear usuario
        const hashedPassword = await this.passwordHasher.hash(request.password);
        const user = new User({
            email: request.email,
            password: hashedPassword,
            name: request.name,
            confirmationToken: this.generateToken()
        });

        // Guardar usuario
        await this.userRepository.save(user);

        // Enviar email de confirmación
        await this.emailService.sendConfirmation(user.email, user.confirmationToken);

        return new RegisterUserResponse(user.id);
    }
}
```

### UC-002: Subir Imagen

**Descripción**: Un usuario autenticado sube una imagen al sistema para procesamiento.

**Actor Principal**: Usuario Registrado

**Precondiciones**:
- Usuario autenticado en el sistema
- Usuario tiene cuota disponible
- Archivo es una imagen válida

**Flujo Principal**:
1. El usuario selecciona "Subir imagen"
2. El usuario elige el archivo de imagen
3. El sistema valida el formato y tamaño del archivo
4. El sistema verifica la cuota del usuario
5. El sistema almacena la imagen temporalmente
6. El sistema crea registro en base de datos
7. El sistema muestra confirmación de subida exitosa

**Flujos Alternativos**:
- **3a**: Formato inválido → Mostrar formatos soportados
- **3b**: Archivo muy grande → Mostrar límite de tamaño
- **4a**: Cuota agotada → Sugerir upgrade de plan
- **5a**: Error de almacenamiento → Reintentar o mostrar error

**Postcondiciones**:
- Imagen almacenada en el sistema
- Registro creado en base de datos
- Cuota del usuario actualizada

```typescript
class UploadImageUseCase {
    constructor(
        private imageRepository: IImageRepository,
        private storageService: IStorageService,
        private userRepository: IUserRepository,
        private quotaService: IQuotaService
    ) {}

    async execute(request: UploadImageRequest): Promise<UploadImageResponse> {
        // Validar archivo
        this.validateImageFile(request.file);

        // Verificar cuota
        const user = await this.userRepository.findById(request.userId);
        await this.quotaService.checkQuota(user);

        // Almacenar imagen
        const storageUrl = await this.storageService.store(request.file);

        // Crear entidad imagen
        const image = new Image({
            userId: request.userId,
            filename: request.file.name,
            originalSize: request.file.size,
            format: this.detectFormat(request.file),
            storageUrl: storageUrl,
            status: ImageStatus.UPLOADED
        });

        // Guardar en base de datos
        await this.imageRepository.save(image);

        // Actualizar cuota
        await this.quotaService.updateQuota(user, request.file.size);

        return new UploadImageResponse(image.id, image.filename);
    }
}
```

### UC-003: Procesar Imagen (Upscale)

**Descripción**: Un usuario procesa una imagen subida aplicando upscaling.

**Actor Principal**: Usuario Registrado

**Precondiciones**:
- Usuario autenticado
- Imagen previamente subida
- Imagen en estado válido para procesamiento

**Flujo Principal**:
1. El usuario selecciona una imagen de su galería
2. El usuario configura parámetros de procesamiento (escala, calidad, etc.)
3. El sistema valida los parámetros
4. El sistema inicia el procesamiento en segundo plano
5. El sistema notifica el progreso al usuario
6. El sistema completa el procesamiento
7. El sistema notifica al usuario de la finalización
8. El usuario puede descargar el resultado

**Flujos Alternativos**:
- **3a**: Parámetros inválidos → Mostrar valores válidos
- **4a**: Sistema sobrecargado → Añadir a cola con tiempo estimado
- **6a**: Error en procesamiento → Notificar error y sugerir ajustes
- **8a**: Error en descarga → Permitir reintento

**Postcondiciones**:
- Imagen procesada disponible
- Historial de procesamiento actualizado
- Notificación enviada al usuario

```typescript
class UpscaleImageUseCase {
    constructor(
        private imageRepository: IImageRepository,
        private processingService: IImageProcessingService,
        private queueService: IQueueService,
        private notificationService: INotificationService
    ) {}

    async execute(request: UpscaleImageRequest): Promise<UpscaleImageResponse> {
        // Obtener imagen original
        const image = await this.imageRepository.findById(request.imageId);
        if (!image) {
            throw new ImageNotFoundError(request.imageId);
        }

        // Validar parámetros
        this.validateUpscaleParameters(request.parameters);

        // Crear job de procesamiento
        const job = new ProcessingJob({
            imageId: image.id,
            userId: image.userId,
            type: ProcessingType.UPSCALE,
            parameters: request.parameters,
            status: JobStatus.QUEUED
        });

        // Añadir a cola de procesamiento
        await this.queueService.addJob(job);

        // Iniciar procesamiento asíncrono
        this.processImageAsync(job);

        return new UpscaleImageResponse(job.id, job.estimatedTime);
    }

    private async processImageAsync(job: ProcessingJob): Promise<void> {
        try {
            // Actualizar estado
            job.updateStatus(JobStatus.PROCESSING);
            await this.notificationService.notifyProgress(job.userId, job.progress);

            // Procesar imagen
            const result = await this.processingService.upscale(
                job.imageId,
                job.parameters
            );

            // Guardar resultado
            await this.imageRepository.saveProcessed(result);

            // Notificar finalización
            job.updateStatus(JobStatus.COMPLETED);
            await this.notificationService.notifyCompletion(job.userId, result.id);

        } catch (error) {
            job.updateStatus(JobStatus.FAILED);
            await this.notificationService.notifyError(job.userId, error.message);
        }
    }
}
```

### UC-004: Gestionar Historial de Imágenes

**Descripción**: Un usuario visualiza y gestiona su historial de imágenes procesadas.

**Actor Principal**: Usuario Registrado

**Precondiciones**:
- Usuario autenticado
- Usuario tiene imágenes en el sistema

**Flujo Principal**:
1. El usuario accede a su historial
2. El sistema muestra lista paginada de imágenes
3. El usuario puede filtrar por fecha, estado, tipo
4. El usuario puede ordenar la lista
5. El usuario puede ver detalles de cada imagen
6. El usuario puede descargar imágenes
7. El usuario puede eliminar imágenes

**Flujos Alternativos**:
- **2a**: No hay imágenes → Mostrar mensaje y opción de subir
- **6a**: Imagen no disponible → Mostrar error
- **7a**: Error al eliminar → Mostrar mensaje de error

```typescript
class GetImageHistoryUseCase {
    constructor(
        private imageRepository: IImageRepository,
        private userRepository: IUserRepository
    ) {}

    async execute(request: GetImageHistoryRequest): Promise<GetImageHistoryResponse> {
        // Verificar usuario
        const user = await this.userRepository.findById(request.userId);
        if (!user) {
            throw new UserNotFoundError(request.userId);
        }

        // Construir filtros
        const filters = new ImageFilters({
            userId: request.userId,
            status: request.status,
            dateFrom: request.dateFrom,
            dateTo: request.dateTo,
            type: request.type
        });

        // Obtener imágenes paginadas
        const images = await this.imageRepository.findByFilters(
            filters,
            request.page,
            request.pageSize,
            request.sortBy,
            request.sortOrder
        );

        // Mapear a DTOs
        const imageDTOs = images.map(image => ImageDTO.fromEntity(image));

        return new GetImageHistoryResponse(
            imageDTOs,
            images.totalCount,
            request.page,
            request.pageSize
        );
    }
}
```

## 🎛️ Casos de Uso Administrativos

### UC-005: Gestionar Usuarios (Admin)

**Descripción**: Un administrador gestiona los usuarios del sistema.

**Actor Principal**: Usuario Administrador

```typescript
class ManageUsersUseCase {
    constructor(
        private userRepository: IUserRepository,
        private auditService: IAuditService
    ) {}

    async listUsers(request: ListUsersRequest): Promise<ListUsersResponse> {
        const users = await this.userRepository.findWithFilters(
            request.filters,
            request.pagination
        );

        return new ListUsersResponse(users);
    }

    async suspendUser(userId: string, reason: string): Promise<void> {
        const user = await this.userRepository.findById(userId);
        user.suspend(reason);

        await this.userRepository.save(user);
        await this.auditService.logAction('USER_SUSPENDED', userId, reason);
    }

    async reactivateUser(userId: string): Promise<void> {
        const user = await this.userRepository.findById(userId);
        user.reactivate();

        await this.userRepository.save(user);
        await this.auditService.logAction('USER_REACTIVATED', userId);
    }
}
```

### UC-006: Ver Estadísticas del Sistema

**Descripción**: Un administrador visualiza estadísticas y métricas del sistema.

```typescript
class GetSystemStatsUseCase {
    constructor(
        private statsRepository: IStatsRepository,
        private imageRepository: IImageRepository,
        private userRepository: IUserRepository
    ) {}

    async execute(request: GetStatsRequest): Promise<GetStatsResponse> {
        const dateRange = new DateRange(request.startDate, request.endDate);

        const stats = await Promise.all([
            this.getUserStats(dateRange),
            this.getImageStats(dateRange),
            this.getProcessingStats(dateRange),
            this.getSystemStats(dateRange)
        ]);

        return new GetStatsResponse({
            userStats: stats[0],
            imageStats: stats[1],
            processingStats: stats[2],
            systemStats: stats[3]
        });
    }
}
```

## 🔄 Casos de Uso de Integración

### UC-007: Procesar con IA Externa

**Descripción**: El sistema utiliza servicios de IA externos para procesamiento avanzado.

```typescript
class ProcessWithExternalAIUseCase {
    constructor(
        private aiServiceAdapter: IAIServiceAdapter,
        private fallbackService: IFallbackService,
        private billingService: IBillingService
    ) {}

    async execute(request: ProcessWithAIRequest): Promise<ProcessWithAIResponse> {
        try {
            // Verificar disponibilidad del servicio
            if (!await this.aiServiceAdapter.isAvailable()) {
                return await this.fallbackService.process(request);
            }

            // Verificar créditos
            await this.billingService.checkCredits(request.userId);

            // Procesar con IA
            const result = await this.aiServiceAdapter.process(request.image);

            // Descontar créditos
            await this.billingService.deductCredits(request.userId, result.cost);

            return new ProcessWithAIResponse(result);

        } catch (error) {
            // Fallback en caso de error
            return await this.fallbackService.process(request);
        }
    }
}
```

## 📊 Matriz de Casos de Uso

| Caso de Uso                | Actor   | Complejidad | Prioridad | Estado |
| -------------------------- | ------- | ----------- | --------- | ------ |
| UC-001 Registrar Usuario   | Usuario | Media       | Alta      | ✅      |
| UC-002 Subir Imagen        | Usuario | Media       | Alta      | ✅      |
| UC-003 Procesar Imagen     | Usuario | Alta        | Alta      | ✅      |
| UC-004 Gestionar Historial | Usuario | Media       | Media     | ✅      |
| UC-005 Gestionar Usuarios  | Admin   | Alta        | Media     | 🔄      |
| UC-006 Ver Estadísticas    | Admin   | Media       | Baja      | 📋      |
| UC-007 Procesar con IA     | Sistema | Alta        | Media     | 📋      |

**Leyenda**: ✅ Completado | 🔄 En progreso | 📋 Pendiente

## 🧪 Casos de Prueba

Cada caso de uso debe incluir:

1. **Tests unitarios** para la lógica de negocio
2. **Tests de integración** para interacciones entre capas
3. **Tests end-to-end** para flujos completos
4. **Tests de rendimiento** para casos críticos

```typescript
describe('UpscaleImageUseCase', () => {
    let useCase: UpscaleImageUseCase;
    let mockImageRepo: MockImageRepository;
    let mockProcessingService: MockProcessingService;

    beforeEach(() => {
        mockImageRepo = new MockImageRepository();
        mockProcessingService = new MockProcessingService();
        useCase = new UpscaleImageUseCase(mockImageRepo, mockProcessingService);
    });

    it('should process image successfully', async () => {
        // Arrange
        const request = new UpscaleImageRequest('image-123', { scale: 2 });
        mockImageRepo.setImage(new Image('image-123', 'test.jpg'));

        // Act
        const response = await useCase.execute(request);

        // Assert
        expect(response.jobId).toBeDefined();
        expect(mockProcessingService.processCallCount).toBe(1);
    });

    it('should throw error when image not found', async () => {
        // Arrange
        const request = new UpscaleImageRequest('non-existent', { scale: 2 });

        // Act & Assert
        await expect(useCase.execute(request))
            .rejects.toThrow(ImageNotFoundError);
    });
});
```

Los casos de uso son el corazón de nuestra aplicación y definen claramente qué funcionalidades ofrecemos y cómo interactúan los usuarios con el sistema.
