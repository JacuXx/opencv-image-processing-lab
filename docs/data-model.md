# 🗃️ Modelo de Datos - Diseño de Base de Datos

El modelo de datos define la estructura de información que maneja nuestra aplicación de upscale de imágenes, siguiendo principios de normalización y optimización.

## 📊 Diagrama de Entidades y Relaciones (ERD)

```
┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
│       Users         │      │      Images         │      │   ProcessingJobs    │
├─────────────────────┤      ├─────────────────────┤      ├─────────────────────┤
│ id (PK)            │◄────┐│ id (PK)            │◄────┐│ id (PK)            │
│ email (UNIQUE)     │     ││ user_id (FK)       │     ││ image_id (FK)      │
│ password_hash      │     ││ filename           │     ││ user_id (FK)       │
│ name               │     ││ original_filename  │     ││ type               │
│ plan_type          │     ││ file_size          │     ││ status             │
│ storage_used       │     ││ width              │     ││ parameters         │
│ storage_limit      │     ││ height             │     ││ started_at         │
│ is_active          │     ││ format             │     ││ completed_at       │
│ email_verified     │     ││ storage_path       │     ││ error_message      │
│ created_at         │     ││ thumbnail_path     │     ││ progress           │
│ updated_at         │     ││ status             │     ││ estimated_time     │
│ last_login         │     ││ created_at         │     ││ created_at         │
└─────────────────────┘     ││ updated_at         │     ││ updated_at         │
                            │└─────────────────────┘     │└─────────────────────┘
                            │                            │
                            └────────────────────────────┘

┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
│    ImageVersions    │      │    UserSessions     │      │    SystemStats      │
├─────────────────────┤      ├─────────────────────┤      ├─────────────────────┤
│ id (PK)            │      │ id (PK)            │      │ id (PK)            │
│ original_image_id   │      │ user_id (FK)       │      │ date               │
│ version_type        │      │ token              │      │ total_users        │
│ file_size          │      │ expires_at         │      │ active_users       │
│ width              │      │ created_at         │      │ images_processed   │
│ height             │      │ last_accessed      │      │ storage_used       │
│ storage_path       │      │ ip_address         │      │ api_calls          │
│ processing_params  │      │ user_agent         │      │ errors_count       │
│ created_at         │      └─────────────────────┘      │ avg_processing_time│
│ updated_at         │                                   │ created_at         │
└─────────────────────┘                                   └─────────────────────┘
```

## 🏗️ Entidades del Dominio

### User (Usuario)

```typescript
export class User {
    constructor(
        public readonly id: UserId,
        public readonly email: Email,
        private passwordHash: string,
        public readonly name: string,
        public readonly planType: PlanType,
        private storageUsed: number = 0,
        private readonly storageLimit: number,
        public readonly isActive: boolean = true,
        public readonly emailVerified: boolean = false,
        public readonly createdAt: Date = new Date(),
        private updatedAt: Date = new Date(),
        private lastLogin?: Date
    ) {}

    // Métodos de negocio
    canUploadImage(imageSize: number): boolean {
        return this.isActive &&
               this.emailVerified &&
               (this.storageUsed + imageSize) <= this.storageLimit;
    }

    updateStorageUsed(additionalSize: number): void {
        if (this.storageUsed + additionalSize > this.storageLimit) {
            throw new StorageLimitExceededError();
        }
        this.storageUsed += additionalSize;
        this.updatedAt = new Date();
    }

    recordLogin(): void {
        this.lastLogin = new Date();
        this.updatedAt = new Date();
    }

    // Value Objects
    public get storageUsedMB(): number {
        return this.storageUsed / (1024 * 1024);
    }

    public get storageUsagePercentage(): number {
        return (this.storageUsed / this.storageLimit) * 100;
    }
}

// Value Objects relacionados
export class Email {
    constructor(private readonly value: string) {
        if (!this.isValid(value)) {
            throw new InvalidEmailError(value);
        }
    }

    private isValid(email: string): boolean {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    toString(): string {
        return this.value;
    }
}

export enum PlanType {
    FREE = 'free',
    BASIC = 'basic',
    PREMIUM = 'premium',
    ENTERPRISE = 'enterprise'
}
```

### Image (Imagen)

```typescript
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
        public readonly thumbnailPath?: string,
        private status: ImageStatus = ImageStatus.UPLOADED,
        public readonly createdAt: Date = new Date(),
        private updatedAt: Date = new Date()
    ) {}

    // Métodos de negocio
    canBeProcessed(): boolean {
        return this.status === ImageStatus.UPLOADED ||
               this.status === ImageStatus.PROCESSED;
    }

    markAsProcessing(): void {
        if (!this.canBeProcessed()) {
            throw new InvalidImageStatusError(this.status);
        }
        this.status = ImageStatus.PROCESSING;
        this.updatedAt = new Date();
    }

    markAsProcessed(): void {
        this.status = ImageStatus.PROCESSED;
        this.updatedAt = new Date();
    }

    markAsFailed(error: string): void {
        this.status = ImageStatus.FAILED;
        this.updatedAt = new Date();
    }

    // Propiedades calculadas
    public get isLargeFile(): boolean {
        return this.fileSize > 10 * 1024 * 1024; // 10MB
    }

    public get aspectRatio(): number {
        return this.dimensions.width / this.dimensions.height;
    }
}

// Value Objects
export class ImageDimensions {
    constructor(
        public readonly width: number,
        public readonly height: number
    ) {
        if (width <= 0 || height <= 0) {
            throw new InvalidDimensionsError(width, height);
        }
    }

    public get totalPixels(): number {
        return this.width * this.height;
    }

    public get megapixels(): number {
        return this.totalPixels / 1000000;
    }
}

export enum ImageStatus {
    UPLOADED = 'uploaded',
    PROCESSING = 'processing',
    PROCESSED = 'processed',
    FAILED = 'failed',
    DELETED = 'deleted'
}

export enum ImageFormat {
    JPEG = 'jpeg',
    PNG = 'png',
    WEBP = 'webp',
    TIFF = 'tiff'
}
```

### ProcessingJob (Trabajo de Procesamiento)

```typescript
export class ProcessingJob {
    constructor(
        public readonly id: JobId,
        public readonly imageId: ImageId,
        public readonly userId: UserId,
        public readonly type: ProcessingType,
        public readonly parameters: ProcessingParameters,
        private status: JobStatus = JobStatus.QUEUED,
        private progress: number = 0,
        private estimatedTime?: number,
        public readonly createdAt: Date = new Date(),
        private startedAt?: Date,
        private completedAt?: Date,
        private errorMessage?: string
    ) {}

    // Métodos de negocio
    start(): void {
        if (this.status !== JobStatus.QUEUED) {
            throw new InvalidJobStatusError(this.status);
        }
        this.status = JobStatus.PROCESSING;
        this.startedAt = new Date();
    }

    updateProgress(progress: number): void {
        if (progress < 0 || progress > 100) {
            throw new InvalidProgressError(progress);
        }
        this.progress = progress;
    }

    complete(): void {
        this.status = JobStatus.COMPLETED;
        this.progress = 100;
        this.completedAt = new Date();
    }

    fail(error: string): void {
        this.status = JobStatus.FAILED;
        this.errorMessage = error;
        this.completedAt = new Date();
    }

    // Propiedades calculadas
    public get duration(): number | null {
        if (!this.startedAt || !this.completedAt) {
            return null;
        }
        return this.completedAt.getTime() - this.startedAt.getTime();
    }

    public get isInProgress(): boolean {
        return this.status === JobStatus.PROCESSING;
    }
}

export enum JobStatus {
    QUEUED = 'queued',
    PROCESSING = 'processing',
    COMPLETED = 'completed',
    FAILED = 'failed',
    CANCELLED = 'cancelled'
}

export enum ProcessingType {
    UPSCALE = 'upscale',
    COMPRESS = 'compress',
    FILTER = 'filter',
    FORMAT_CONVERT = 'format_convert'
}

export class ProcessingParameters {
    constructor(
        public readonly scale?: number,
        public readonly quality?: number,
        public readonly algorithm?: string,
        public readonly filters?: string[],
        public readonly outputFormat?: ImageFormat
    ) {}
}
```

## 🗄️ Schema de Base de Datos

### SQL Schema (PostgreSQL)

```sql
-- Extensiones
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabla de usuarios
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    plan_type VARCHAR(50) NOT NULL DEFAULT 'free',
    storage_used BIGINT NOT NULL DEFAULT 0,
    storage_limit BIGINT NOT NULL DEFAULT 1073741824, -- 1GB
    is_active BOOLEAN NOT NULL DEFAULT true,
    email_verified BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE
);

-- Índices para usuarios
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_plan_type ON users(plan_type);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Tabla de imágenes
CREATE TABLE images (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_size BIGINT NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    format VARCHAR(10) NOT NULL,
    storage_path TEXT NOT NULL,
    thumbnail_path TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'uploaded',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para imágenes
CREATE INDEX idx_images_user_id ON images(user_id);
CREATE INDEX idx_images_status ON images(status);
CREATE INDEX idx_images_created_at ON images(created_at);
CREATE INDEX idx_images_format ON images(format);

-- Tabla de trabajos de procesamiento
CREATE TABLE processing_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    image_id UUID NOT NULL REFERENCES images(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'queued',
    parameters JSONB,
    progress INTEGER NOT NULL DEFAULT 0,
    estimated_time INTEGER,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para trabajos
CREATE INDEX idx_jobs_image_id ON processing_jobs(image_id);
CREATE INDEX idx_jobs_user_id ON processing_jobs(user_id);
CREATE INDEX idx_jobs_status ON processing_jobs(status);
CREATE INDEX idx_jobs_type ON processing_jobs(type);
CREATE INDEX idx_jobs_created_at ON processing_jobs(created_at);

-- Tabla de versiones de imagen
CREATE TABLE image_versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    original_image_id UUID NOT NULL REFERENCES images(id) ON DELETE CASCADE,
    version_type VARCHAR(50) NOT NULL,
    file_size BIGINT NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    storage_path TEXT NOT NULL,
    processing_params JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para versiones
CREATE INDEX idx_versions_original_id ON image_versions(original_image_id);
CREATE INDEX idx_versions_type ON image_versions(version_type);

-- Tabla de sesiones
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_accessed TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT
);

-- Índices para sesiones
CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_sessions_token ON user_sessions(token);
CREATE INDEX idx_sessions_expires_at ON user_sessions(expires_at);

-- Tabla de estadísticas del sistema
CREATE TABLE system_stats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    date DATE NOT NULL UNIQUE,
    total_users INTEGER NOT NULL DEFAULT 0,
    active_users INTEGER NOT NULL DEFAULT 0,
    images_processed INTEGER NOT NULL DEFAULT 0,
    storage_used BIGINT NOT NULL DEFAULT 0,
    api_calls INTEGER NOT NULL DEFAULT 0,
    errors_count INTEGER NOT NULL DEFAULT 0,
    avg_processing_time REAL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índice para estadísticas
CREATE INDEX idx_stats_date ON system_stats(date);

-- Triggers para updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_images_updated_at
    BEFORE UPDATE ON images
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_jobs_updated_at
    BEFORE UPDATE ON processing_jobs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

## 📋 Consultas Importantes

### Consultas de Rendimiento

```sql
-- Obtener imágenes de un usuario con paginación
SELECT i.*, COUNT(*) OVER() as total_count
FROM images i
WHERE i.user_id = $1
  AND i.status = $2
ORDER BY i.created_at DESC
LIMIT $3 OFFSET $4;

-- Estadísticas de uso por usuario
SELECT
    u.id,
    u.name,
    u.email,
    COUNT(i.id) as total_images,
    SUM(i.file_size) as total_storage,
    AVG(pj.estimated_time) as avg_processing_time
FROM users u
LEFT JOIN images i ON u.id = i.user_id
LEFT JOIN processing_jobs pj ON i.id = pj.image_id
WHERE u.created_at >= $1
GROUP BY u.id, u.name, u.email;

-- Jobs pendientes en cola
SELECT
    pj.*,
    i.filename,
    u.name as user_name
FROM processing_jobs pj
JOIN images i ON pj.image_id = i.id
JOIN users u ON pj.user_id = u.id
WHERE pj.status = 'queued'
ORDER BY pj.created_at ASC;
```

## 🔍 Índices y Optimizaciones

### Índices Compuestos

```sql
-- Para consultas complejas
CREATE INDEX idx_images_user_status_created
ON images(user_id, status, created_at DESC);

CREATE INDEX idx_jobs_status_type_created
ON processing_jobs(status, type, created_at);

-- Para búsquedas de texto
CREATE INDEX idx_images_filename_text
ON images USING gin(to_tsvector('english', filename));
```

### Particionamiento (Para grandes volúmenes)

```sql
-- Particionar por fecha para logs y estadísticas
CREATE TABLE processing_jobs_y2024m01 PARTITION OF processing_jobs
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE processing_jobs_y2024m02 PARTITION OF processing_jobs
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
```

## 🔒 Seguridad y Constraints

```sql
-- Constraints de validación
ALTER TABLE users ADD CONSTRAINT check_storage_limit
CHECK (storage_used <= storage_limit);

ALTER TABLE images ADD CONSTRAINT check_file_size
CHECK (file_size > 0);

ALTER TABLE processing_jobs ADD CONSTRAINT check_progress
CHECK (progress >= 0 AND progress <= 100);

-- Policies de Row Level Security (RLS)
ALTER TABLE images ENABLE ROW LEVEL SECURITY;

CREATE POLICY images_user_policy ON images
FOR ALL TO authenticated_user
USING (user_id = current_user_id());
```

## 📊 Datos de Ejemplo

```sql
-- Insertar datos de prueba
INSERT INTO users (email, password_hash, name, plan_type) VALUES
('user1@example.com', '$2b$10$...', 'Usuario Uno', 'free'),
('user2@example.com', '$2b$10$...', 'Usuario Dos', 'premium');

INSERT INTO images (user_id, filename, original_filename, file_size, width, height, format, storage_path) VALUES
((SELECT id FROM users WHERE email = 'user1@example.com'), 'img_001.jpg', 'photo.jpg', 2048576, 1920, 1080, 'jpeg', '/storage/images/img_001.jpg');
```

Este modelo de datos proporciona una base sólida para nuestra aplicación, con consideraciones de rendimiento, escalabilidad y seguridad.
