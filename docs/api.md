# API Reference

**Base URL**: `http://localhost:8000`  
**Interactive Docs**: `http://localhost:8000/docs` (Swagger UI)

## Endpoints

### 1. Convert Single File
*   **Method**: `POST`
*   **Path**: `/convert/`
*   **Summary**: Convert a single text or markdown file to PDF.
*   **Parameters**:
    *   `file` (multipart/form-data): The source file (.md, .markdown, .txt)
*   **Response**: `application/pdf` binary stream.
*   **Limits**: Max 10MB per file.
*   **Headers**: 
    *   `X-Request-ID`: Unique tracing ID
    *   `X-Process-Time`: Server processing time in seconds

### 2. Convert Multiple Files
*   **Method**: `POST`
*   **Path**: `/convert/multiple`
*   **Summary**: Upload multiple files and receive a ZIP with all PDFs.
*   **Parameters**:
    *   `files` (multipart/form-data): Multiple source files
*   **Response**: `application/zip` containing all generated PDFs.
*   **Limits**: 
    *   Max 20 files per request
    *   Max 10MB per file
    *   Max 50MB total request size
*   **Headers**: 
    *   `X-Conversion-Results`: Success count
    *   `X-Request-ID`: Unique tracing ID

### 3. Bulk Convert Local Files
*   **Method**: `POST`
*   **Path**: `/bulk-convert`
*   **Summary**: Process all files in `data/input/` directory.
*   **Response**: JSON with processing results.

### 4. Health Check
*   **Method**: `GET`
*   **Path**: `/health`
*   **Summary**: Liveness and version info.
*   **Response**: 
```json
{
  "status": "healthy",
  "service": "text-to-pdf-service",
  "version": "1.0.0"
}
```

### 5. Base Information (Root)
*   **Method**: `GET`
*   **Path**: `/`
*   **Summary**: API metadata and documentation links.
*   **Response**: 
```json
{
  "service": "Text to PDF Converter",
  "version": "1.0.0",
  "status": "operational",
  "documentation": "/docs",
  "health": "/health"
}
```

## Validation & Limits

| Validation | Value |
|------------|-------|
| Supported extensions | `.md`, `.markdown`, `.txt` |
| Max file size (single) | 10MB |
| Max file size (multiple) | 10MB per file |
| Max total size (multiple) | 50MB |
| Max files (multiple) | 20 |

## Error Responses

| Status | Description |
|--------|-------------|
| 400 | Invalid file type or empty file |
| 413 | File size exceeds limit |
| 500 | Internal server error |

---

**Last Updated**: 2026-01-18  
**Version**: 1.0.0
