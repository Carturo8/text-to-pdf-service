# Referencia de la API

**URL Base**: `http://localhost:8000`  
**Docs Interactivos**: `http://localhost:8000/docs` (Swagger UI)

## Endpoints

### 1. Convertir Archivo Individual
*   **Método**: `POST`
*   **Ruta**: `/convert/`
*   **Resumen**: Convierte un archivo de texto o markdown a PDF.
*   **Parámetros**:
    *   `file` (multipart/form-data): El archivo fuente (.md, .markdown, .txt)
*   **Respuesta**: Flujo binario `application/pdf`.
*   **Límites**: Máx 10MB por archivo.
*   **Cabeceras**: 
    *   `X-Request-ID`: ID único de rastreo
    *   `X-Process-Time`: Tiempo de procesamiento en segundos

### 2. Convertir Múltiples Archivos
*   **Método**: `POST`
*   **Ruta**: `/convert/multiple`
*   **Resumen**: Sube varios archivos y recibe un ZIP con todos los PDFs.
*   **Parámetros**:
    *   `files` (multipart/form-data): Múltiples archivos fuente
*   **Respuesta**: `application/zip` con todos los PDFs generados.
*   **Límites**: 
    *   Máx 20 archivos por petición
    *   Máx 10MB por archivo
    *   Máx 50MB total por petición
*   **Cabeceras**: 
    *   `X-Conversion-Results`: Conteo de éxitos
    *   `X-Request-ID`: ID único de rastreo

### 3. Conversión Masiva de Archivos Locales
*   **Método**: `POST`
*   **Ruta**: `/bulk-convert`
*   **Resumen**: Procesa todos los archivos en el directorio `data/input/`.
*   **Respuesta**: Resumen JSON de los resultados.

### 4. Verificación de Salud (Health Check)
*   **Método**: `GET`
*   **Ruta**: `/health`
*   **Resumen**: Información de estado y versión.
*   **Respuesta**: 
```json
{
  "status": "healthy",
  "service": "text-to-pdf-service",
  "version": "1.0.0"
}
```

### 5. Información Base (Root)
*   **Método**: `GET`
*   **Ruta**: `/`
*   **Resumen**: Metadatos de la API y enlaces a la documentación.
*   **Respuesta**: 
```json
{
  "service": "Text to PDF Converter",
  "version": "1.0.0",
  "status": "operational",
  "documentation": "/docs",
  "health": "/health"
}
```

## Validación y Límites

| Validación | Valor |
|------------|-------|
| Extensiones soportadas | `.md`, `.markdown`, `.txt` |
| Tamaño máx (individual) | 10MB |
| Tamaño máx (múltiple) | 10MB por archivo |
| Tamaño total máx (múltiple) | 50MB |
| Máx archivos (múltiple) | 20 |

## Respuestas de Error

| Estado | Descripción |
|--------|-------------|
| 400 | Tipo de archivo inválido o archivo vacío |
| 413 | El tamaño del archivo excede el límite |
| 500 | Error interno del servidor |

---

**Última Actualización**: 2026-01-18  
**Versión**: 1.0.0
