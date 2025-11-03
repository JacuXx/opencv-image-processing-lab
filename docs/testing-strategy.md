# 🧪 Estrategia de Testing - Guía Completa

Una estrategia de testing robusta es fundamental para garantizar la calidad, confiabilidad y mantenibilidad de nuestra aplicación de upscale de imágenes.

## 🎯 Pirámide de Testing

```
                    🔺 E2E Tests
                   /   (Pocos)   \
                  /               \
                 🔺 Integration Tests
                /    (Algunos)      \
               /                     \
              🔺    Unit Tests        🔺
             /       (Muchos)          \
            /_________________________\
```

### Distribución Recomendada
- **70%** Unit Tests
- **20%** Integration Tests
- **10%** End-to-End Tests

## 🧪 Unit Tests (Tests Unitarios)

### Objetivo
Probar componentes individuales de manera aislada.

### Estructura de Testing por Capa

#### Domain Layer Tests

```typescript
// tests/unit/domain/entities/User.test.ts
describe('User Entity', () => {
    describe('canUploadImage', () => {
        it('should return true when user is active, verified and has storage space', () => {
            // Arrange
            const user = new User(
                new UserId('123'),
                new Email('test@example.com'),
                'hashedPassword',
                'Test User',
                PlanType.FREE,
                0, // storage used
                1000000, // storage limit (1MB)
                true, // active
                true  // verified
            );

            // Act
            const canUpload = user.canUploadImage(500000); // 0.5MB

            // Assert
            expect(canUpload).toBe(true);
        });

        it('should return false when storage limit would be exceeded', () => {
            // Arrange
            const user = new User(
                new UserId('123'),
                new Email('test@example.com'),
                'hashedPassword',
                'Test User',
                PlanType.FREE,
                900000, // 0.9MB used
                1000000, // 1MB limit
                true,
                true
            );

            // Act
            const canUpload = user.canUploadImage(200000); // 0.2MB (would exceed)

            // Assert
            expect(canUpload).toBe(false);
        });

        it('should return false when user is not active', () => {
            // Arrange
            const user = new User(
                new UserId('123'),
                new Email('test@example.com'),
                'hashedPassword',
                'Test User',
                PlanType.FREE,
                0,
                1000000,
                false, // not active
                true
            );

            // Act
            const canUpload = user.canUploadImage(100000);

            // Assert
            expect(canUpload).toBe(false);
        });
    });

    describe('updateStorageUsed', () => {
        it('should update storage used when within limit', () => {
            // Arrange
            const user = new User(
                new UserId('123'),
                new Email('test@example.com'),
                'hashedPassword',
                'Test User',
                PlanType.FREE,
                100000,
                1000000,
                true,
                true
            );

            // Act
            user.updateStorageUsed(200000);

            // Assert
            expect(user.storageUsedMB).toBe(0.286); // (300000 / 1024 / 1024)
        });

        it('should throw error when storage limit would be exceeded', () => {
            // Arrange
            const user = new User(
                new UserId('123'),
                new Email('test@example.com'),
                'hashedPassword',
                'Test User',
                PlanType.FREE,
                900000,
                1000000,
                true,
                true
            );

            // Act & Assert
            expect(() => user.updateStorageUsed(200000))
                .toThrow(StorageLimitExceededError);
        });
    });
});
```

#### Application Layer Tests

```typescript
// tests/unit/application/use-cases/UpscaleImageUseCase.test.ts
describe('UpscaleImageUseCase', () => {
    let useCase: UpscaleImageUseCase;
    let mockImageRepository: jest.Mocked<IImageRepository>;
    let mockProcessingService: jest.Mocked<IImageProcessingService>;
    let mockQueueService: jest.Mocked<IQueueService>;
    let mockNotificationService: jest.Mocked<INotificationService>;

    beforeEach(() => {
        mockImageRepository = {
            findById: jest.fn(),
            save: jest.fn(),
            saveProcessed: jest.fn()
        } as jest.Mocked<IImageRepository>;

        mockProcessingService = {
            upscale: jest.fn()
        } as jest.Mocked<IImageProcessingService>;

        mockQueueService = {
            addJob: jest.fn()
        } as jest.Mocked<IQueueService>;

        mockNotificationService = {
            notifyProgress: jest.fn(),
            notifyCompletion: jest.fn(),
            notifyError: jest.fn()
        } as jest.Mocked<INotificationService>;

        useCase = new UpscaleImageUseCase(
            mockImageRepository,
            mockProcessingService,
            mockQueueService,
            mockNotificationService
        );
    });

    describe('execute', () => {
        it('should create processing job and return job id', async () => {
            // Arrange
            const imageId = 'image-123';
            const userId = 'user-456';
            const image = new Image(
                new ImageId(imageId),
                new UserId(userId),
                'test.jpg',
                'original.jpg',
                1000000,
                new ImageDimensions(1920, 1080),
                ImageFormat.JPEG,
                '/storage/test.jpg'
            );

            const request = new UpscaleImageRequest(
                imageId,
                new ProcessingParameters(4, 90, 'bicubic')
            );

            mockImageRepository.findById.mockResolvedValue(image);
            mockQueueService.addJob.mockResolvedValue();

            // Act
            const response = await useCase.execute(request);

            // Assert
            expect(response).toBeInstanceOf(UpscaleImageResponse);
            expect(response.jobId).toBeDefined();
            expect(mockImageRepository.findById).toHaveBeenCalledWith(imageId);
            expect(mockQueueService.addJob).toHaveBeenCalled();
        });

        it('should throw ImageNotFoundError when image does not exist', async () => {
            // Arrange
            const request = new UpscaleImageRequest(
                'non-existent',
                new ProcessingParameters(4)
            );

            mockImageRepository.findById.mockResolvedValue(null);

            // Act & Assert
            await expect(useCase.execute(request))
                .rejects.toThrow(ImageNotFoundError);
        });

        it('should validate upscale parameters', async () => {
            // Arrange
            const imageId = 'image-123';
            const image = createValidImage(imageId);
            const invalidRequest = new UpscaleImageRequest(
                imageId,
                new ProcessingParameters(-1) // Invalid scale
            );

            mockImageRepository.findById.mockResolvedValue(image);

            // Act & Assert
            await expect(useCase.execute(invalidRequest))
                .rejects.toThrow(InvalidParametersError);
        });
    });
});
```

#### Infrastructure Layer Tests

```typescript
// tests/unit/infrastructure/repositories/PostgresImageRepository.test.ts
describe('PostgresImageRepository', () => {
    let repository: PostgresImageRepository;
    let mockDatabase: jest.Mocked<Database>;

    beforeEach(() => {
        mockDatabase = {
            query: jest.fn(),
            beginTransaction: jest.fn(),
            commit: jest.fn(),
            rollback: jest.fn()
        } as jest.Mocked<Database>;

        repository = new PostgresImageRepository(mockDatabase);
    });

    describe('findById', () => {
        it('should return image when found', async () => {
            // Arrange
            const imageId = 'image-123';
            const mockRow = {
                id: imageId,
                user_id: 'user-456',
                filename: 'test.jpg',
                file_size: 1000000,
                width: 1920,
                height: 1080,
                format: 'jpeg',
                storage_path: '/storage/test.jpg',
                created_at: new Date()
            };

            mockDatabase.query.mockResolvedValue({ rows: [mockRow] });

            // Act
            const result = await repository.findById(imageId);

            // Assert
            expect(result).toBeInstanceOf(Image);
            expect(result!.id.value).toBe(imageId);
            expect(mockDatabase.query).toHaveBeenCalledWith(
                'SELECT * FROM images WHERE id = $1',
                [imageId]
            );
        });

        it('should return null when not found', async () => {
            // Arrange
            const imageId = 'non-existent';
            mockDatabase.query.mockResolvedValue({ rows: [] });

            // Act
            const result = await repository.findById(imageId);

            // Assert
            expect(result).toBeNull();
        });
    });

    describe('save', () => {
        it('should insert new image', async () => {
            // Arrange
            const image = createValidImage();
            mockDatabase.query.mockResolvedValue({ rows: [] });

            // Act
            await repository.save(image);

            // Assert
            expect(mockDatabase.query).toHaveBeenCalledWith(
                expect.stringContaining('INSERT INTO images'),
                expect.arrayContaining([
                    image.id.value,
                    image.userId.value,
                    image.filename
                ])
            );
        });
    });
});
```

## 🔗 Integration Tests (Tests de Integración)

### Objetivo
Probar la interacción entre múltiples componentes.

```typescript
// tests/integration/api/ImageController.test.ts
describe('ImageController Integration', () => {
    let app: Application;
    let database: TestDatabase;
    let storageService: TestStorageService;

    beforeAll(async () => {
        database = new TestDatabase();
        await database.setup();

        storageService = new TestStorageService();

        app = createTestApp({
            database,
            storageService
        });
    });

    afterAll(async () => {
        await database.cleanup();
    });

    beforeEach(async () => {
        await database.reset();
    });

    describe('POST /api/images/upload', () => {
        it('should upload image successfully', async () => {
            // Arrange
            const user = await createTestUser();
            const token = generateTestToken(user.id);
            const imageFile = createTestImageFile();

            // Act
            const response = await request(app)
                .post('/api/images/upload')
                .set('Authorization', `Bearer ${token}`)
                .attach('image', imageFile.buffer, imageFile.filename)
                .expect(201);

            // Assert
            expect(response.body).toMatchObject({
                id: expect.any(String),
                filename: expect.any(String),
                status: 'uploaded'
            });

            // Verify database
            const savedImage = await database.findImageById(response.body.id);
            expect(savedImage).toBeDefined();

            // Verify storage
            const storedFile = await storageService.exists(savedImage.storagePath);
            expect(storedFile).toBe(true);
        });

        it('should reject invalid file format', async () => {
            // Arrange
            const user = await createTestUser();
            const token = generateTestToken(user.id);
            const invalidFile = createTestTextFile();

            // Act & Assert
            await request(app)
                .post('/api/images/upload')
                .set('Authorization', `Bearer ${token}`)
                .attach('image', invalidFile.buffer, invalidFile.filename)
                .expect(400);
        });

        it('should reject when storage limit exceeded', async () => {
            // Arrange
            const user = await createTestUser({ storageUsed: 999000000 }); // Near limit
            const token = generateTestToken(user.id);
            const largeImageFile = createTestImageFile({ size: 50000000 }); // 50MB

            // Act & Assert
            await request(app)
                .post('/api/images/upload')
                .set('Authorization', `Bearer ${token}`)
                .attach('image', largeImageFile.buffer, largeImageFile.filename)
                .expect(413); // Payload Too Large
        });
    });

    describe('POST /api/images/:id/upscale', () => {
        it('should queue upscale job successfully', async () => {
            // Arrange
            const user = await createTestUser();
            const image = await createTestImage(user.id);
            const token = generateTestToken(user.id);

            // Act
            const response = await request(app)
                .post(`/api/images/${image.id}/upscale`)
                .set('Authorization', `Bearer ${token}`)
                .send({
                    scale: 4,
                    quality: 90,
                    algorithm: 'bicubic'
                })
                .expect(202);

            // Assert
            expect(response.body).toMatchObject({
                jobId: expect.any(String),
                estimatedTime: expect.any(Number)
            });

            // Verify job was created
            const job = await database.findJobById(response.body.jobId);
            expect(job.status).toBe('queued');
            expect(job.imageId).toBe(image.id);
        });
    });
});
```

### Repository Integration Tests

```typescript
// tests/integration/repositories/ImageRepository.test.ts
describe('ImageRepository Integration', () => {
    let repository: PostgresImageRepository;
    let database: TestDatabase;

    beforeAll(async () => {
        database = new TestDatabase();
        await database.setup();
        repository = new PostgresImageRepository(database.connection);
    });

    afterAll(async () => {
        await database.cleanup();
    });

    beforeEach(async () => {
        await database.reset();
    });

    it('should persist and retrieve image correctly', async () => {
        // Arrange
        const originalImage = createValidImage();

        // Act - Save
        await repository.save(originalImage);

        // Act - Retrieve
        const retrievedImage = await repository.findById(originalImage.id.value);

        // Assert
        expect(retrievedImage).toBeDefined();
        expect(retrievedImage!.id.value).toBe(originalImage.id.value);
        expect(retrievedImage!.filename).toBe(originalImage.filename);
        expect(retrievedImage!.fileSize).toBe(originalImage.fileSize);
    });

    it('should handle concurrent saves correctly', async () => {
        // Arrange
        const images = Array.from({ length: 10 }, () => createValidImage());

        // Act
        await Promise.all(images.map(image => repository.save(image)));

        // Assert
        const allImages = await repository.findByUserId(images[0].userId.value);
        expect(allImages).toHaveLength(10);
    });
});
```

## 🌐 End-to-End Tests (Tests E2E)

### Objetivo
Probar flujos completos desde la perspectiva del usuario.

```typescript
// tests/e2e/image-upscale-flow.test.ts
describe('Image Upscale Flow E2E', () => {
    let browser: Browser;
    let page: Page;

    beforeAll(async () => {
        browser = await puppeteer.launch({
            headless: process.env.CI === 'true'
        });
    });

    afterAll(async () => {
        await browser.close();
    });

    beforeEach(async () => {
        page = await browser.newPage();
        await page.goto('http://localhost:3000');
    });

    afterEach(async () => {
        await page.close();
    });

    it('should complete full upscale workflow', async () => {
        // 1. User Registration
        await page.click('[data-testid="register-button"]');
        await page.fill('[data-testid="email-input"]', 'test@example.com');
        await page.fill('[data-testid="password-input"]', 'password123');
        await page.fill('[data-testid="name-input"]', 'Test User');
        await page.click('[data-testid="submit-register"]');

        // Wait for email verification (mock)
        await page.waitForSelector('[data-testid="verification-success"]');

        // 2. Login
        await page.click('[data-testid="login-button"]');
        await page.fill('[data-testid="login-email"]', 'test@example.com');
        await page.fill('[data-testid="login-password"]', 'password123');
        await page.click('[data-testid="submit-login"]');

        // Wait for dashboard
        await page.waitForSelector('[data-testid="dashboard"]');

        // 3. Upload Image
        const fileInput = await page.$('[data-testid="file-input"]');
        await fileInput!.uploadFile('./tests/fixtures/test-image.jpg');

        // Wait for upload completion
        await page.waitForSelector('[data-testid="upload-success"]');

        // 4. Configure Upscale
        await page.click('[data-testid="upscale-button"]');
        await page.selectOption('[data-testid="scale-select"]', '4');
        await page.selectOption('[data-testid="quality-select"]', '90');
        await page.click('[data-testid="start-processing"]');

        // 5. Monitor Progress
        await page.waitForSelector('[data-testid="processing-started"]');

        // Wait for completion (with timeout)
        await page.waitForSelector('[data-testid="processing-completed"]', {
            timeout: 60000
        });

        // 6. Download Result
        const downloadPromise = page.waitForEvent('download');
        await page.click('[data-testid="download-button"]');
        const download = await downloadPromise;

        // Verify download
        expect(download.suggestedFilename()).toMatch(/upscaled.*\.jpg$/);

        // 7. Verify in History
        await page.click('[data-testid="history-tab"]');
        const historyItems = await page.$$('[data-testid="history-item"]');
        expect(historyItems.length).toBe(1);
    });

    it('should handle upload errors gracefully', async () => {
        // Login as existing user
        await loginTestUser(page);

        // Try to upload invalid file
        const fileInput = await page.$('[data-testid="file-input"]');
        await fileInput!.uploadFile('./tests/fixtures/test-document.pdf');

        // Should show error message
        await page.waitForSelector('[data-testid="upload-error"]');
        const errorText = await page.textContent('[data-testid="error-message"]');
        expect(errorText).toContain('Invalid file format');
    });
});
```

## 🎭 Mocking y Test Doubles

### Service Mocks

```typescript
// tests/mocks/MockImageProcessingService.ts
export class MockImageProcessingService implements IImageProcessingService {
    private processingResults: Map<string, ProcessedImage> = new Map();
    private processingDelay: number = 100;
    private shouldFail: boolean = false;

    setProcessingResult(imageId: string, result: ProcessedImage): void {
        this.processingResults.set(imageId, result);
    }

    setProcessingDelay(delay: number): void {
        this.processingDelay = delay;
    }

    setShouldFail(shouldFail: boolean): void {
        this.shouldFail = shouldFail;
    }

    async upscale(imageId: string, parameters: ProcessingParameters): Promise<ProcessedImage> {
        await new Promise(resolve => setTimeout(resolve, this.processingDelay));

        if (this.shouldFail) {
            throw new ProcessingError('Mock processing failure');
        }

        const result = this.processingResults.get(imageId);
        if (!result) {
            return new ProcessedImage(imageId, `/storage/upscaled_${imageId}.jpg`);
        }

        return result;
    }
}

// tests/mocks/MockStorageService.ts
export class MockStorageService implements IStorageService {
    private files: Map<string, Buffer> = new Map();

    async store(file: File, path: string): Promise<string> {
        this.files.set(path, file.buffer);
        return `mock://storage/${path}`;
    }

    async retrieve(path: string): Promise<Buffer | null> {
        return this.files.get(path) || null;
    }

    async delete(path: string): Promise<void> {
        this.files.delete(path);
    }

    async exists(path: string): Promise<boolean> {
        return this.files.has(path);
    }

    // Helper for tests
    getStoredFiles(): string[] {
        return Array.from(this.files.keys());
    }

    clear(): void {
        this.files.clear();
    }
}
```

## 🏗️ Test Setup y Utilities

### Base Test Class

```typescript
// tests/utils/BaseTest.ts
export abstract class BaseTest {
    protected mockImageRepository: jest.Mocked<IImageRepository>;
    protected mockUserRepository: jest.Mocked<IUserRepository>;
    protected mockStorageService: MockStorageService;
    protected mockNotificationService: jest.Mocked<INotificationService>;

    protected setup(): void {
        this.mockImageRepository = createMockImageRepository();
        this.mockUserRepository = createMockUserRepository();
        this.mockStorageService = new MockStorageService();
        this.mockNotificationService = createMockNotificationService();
    }

    protected createTestUser(overrides: Partial<UserProps> = {}): User {
        return new User(
            new UserId(overrides.id || 'test-user-id'),
            new Email(overrides.email || 'test@example.com'),
            overrides.passwordHash || 'hashedPassword',
            overrides.name || 'Test User',
            overrides.planType || PlanType.FREE,
            overrides.storageUsed || 0,
            overrides.storageLimit || 1000000,
            overrides.isActive !== undefined ? overrides.isActive : true,
            overrides.emailVerified !== undefined ? overrides.emailVerified : true
        );
    }

    protected createTestImage(overrides: Partial<ImageProps> = {}): Image {
        return new Image(
            new ImageId(overrides.id || 'test-image-id'),
            new UserId(overrides.userId || 'test-user-id'),
            overrides.filename || 'test.jpg',
            overrides.originalFilename || 'original.jpg',
            overrides.fileSize || 1000000,
            overrides.dimensions || new ImageDimensions(1920, 1080),
            overrides.format || ImageFormat.JPEG,
            overrides.storagePath || '/storage/test.jpg'
        );
    }
}
```

### Test Database

```typescript
// tests/utils/TestDatabase.ts
export class TestDatabase {
    private connection: Database;

    async setup(): Promise<void> {
        this.connection = await createTestConnection();
        await this.runMigrations();
    }

    async cleanup(): Promise<void> {
        await this.connection.close();
    }

    async reset(): Promise<void> {
        await this.connection.query('TRUNCATE TABLE users CASCADE');
        await this.connection.query('TRUNCATE TABLE images CASCADE');
        await this.connection.query('TRUNCATE TABLE processing_jobs CASCADE');
    }

    async findImageById(id: string): Promise<any> {
        const result = await this.connection.query(
            'SELECT * FROM images WHERE id = $1',
            [id]
        );
        return result.rows[0];
    }

    async findJobById(id: string): Promise<any> {
        const result = await this.connection.query(
            'SELECT * FROM processing_jobs WHERE id = $1',
            [id]
        );
        return result.rows[0];
    }
}
```

## 📊 Test Coverage y Métricas

### Configuración de Jest

```javascript
// jest.config.js
module.exports = {
    preset: 'ts-jest',
    testEnvironment: 'node',
    roots: ['<rootDir>/src', '<rootDir>/tests'],
    collectCoverageFrom: [
        'src/**/*.{ts,tsx}',
        '!src/**/*.d.ts',
        '!src/**/*.interface.ts',
        '!src/main.ts'
    ],
    coverageThreshold: {
        global: {
            branches: 80,
            functions: 80,
            lines: 80,
            statements: 80
        }
    },
    setupFilesAfterEnv: ['<rootDir>/tests/setup.ts'],
    testMatch: [
        '<rootDir>/tests/**/*.test.{ts,tsx}'
    ],
    moduleNameMapping: {
        '^@/(.*)$': '<rootDir>/src/$1'
    }
};
```

### Scripts de Testing

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:unit": "jest tests/unit",
    "test:integration": "jest tests/integration",
    "test:e2e": "jest tests/e2e",
    "test:ci": "jest --ci --coverage --watchAll=false"
  }
}
```

## 🚀 Testing en CI/CD

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v2

      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm run test:unit

      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/testdb

      - name: Run E2E tests
        run: npm run test:e2e

      - name: Upload coverage
        uses: codecov/codecov-action@v2
        with:
          file: ./coverage/lcov.info
```

## 📈 Métricas y Reporting

### Test Quality Metrics

1. **Code Coverage**: Mínimo 80%
2. **Test Execution Time**: < 5 minutos para suite completa
3. **Flaky Test Rate**: < 2%
4. **Test Maintenance Ratio**: 1:3 (1 hora mantenimiento por 3 horas desarrollo)

### Continuous Monitoring

```typescript
// tests/utils/TestMetrics.ts
export class TestMetrics {
    static async reportTestExecution(testSuite: string, duration: number, passed: number, failed: number): Promise<void> {
        const metrics = {
            testSuite,
            duration,
            passed,
            failed,
            timestamp: new Date(),
            environment: process.env.NODE_ENV
        };

        // Enviar métricas a sistema de monitoreo
        await this.sendToMonitoring(metrics);
    }

    private static async sendToMonitoring(metrics: any): Promise<void> {
        // Implementación específica del sistema de monitoreo
    }
}
```

Esta estrategia de testing garantiza la calidad y confiabilidad de nuestra aplicación en todas las capas de la arquitectura.
