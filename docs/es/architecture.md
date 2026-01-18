# Documentación de Arquitectura

## Visión General
El **Servicio Text-to-PDF** sigue una estricta **Arquitectura Hexagonal (Puertos y Adaptadores)**. Este patrón permite que la aplicación sea independiente de frameworks, interfaces de usuario, bases de datos y agencias externas.

## Conceptos Clave

### 1. Dominio (Núcleo)
Ubicado en `src/domain/`.
*   **Entidades**: `ConversionRequest`, `ConversionResult` (Dataclasses puros de Python).
*   **Puertos (Interfaces)**: Definen *cómo* el mundo exterior interactúa con la aplicación (`Puertos de Entrada`) y cómo la aplicación interactúa con herramientas externas (`Puertos de Salida`).
    *   `PDFConverterPort`: Interfaz para la generación de PDF.
    *   `FileSystemPort`: Interfaz para lectura/escritura de archivos.

### 2. Aplicación (Lógica de Negocio)
Ubicado en `src/application/`.
*   **Servicios**: `ConversionService`.
*   **Responsabilidad**: Orquesta el flujo de datos. Recibe un comando, lo valida usando reglas de Dominio, dispara el adaptador vía un Puerto, y retorna un resultado. **No** conoce sobre HTTP o CLI.

### 3. Adaptadores (Infraestructura)
Ubicado en `src/adapters/`.

#### Adaptadores Conductores (Primary/Driving)
Inician acciones en la aplicación.
*   **API (`src/adapters/driving/api.py`)**: Implementación con FastAPI. Expone endpoints REST.
*   **CLI (`src/adapters/driving/cli.py`)**: Implementación con Typer. Permite ejecución por línea de comandos.

#### Adaptadores Conducidos (Secondary/Driven)
Son llamados por la aplicación.
*   **Xhtml2PdfAdapter (`src/adapters/driven/pdf_adapter.py`)**: Implementa `PDFConverterPort`. Usa la librería `xhtml2pdf` para generar PDFs desde HTML/CSS.
*   **LocalFileSystemAdapter (`src/adapters/driven/fs_adapter.py`)**: Implementa `FileSystemPort`. Maneja I/O de disco local.

## Flujo de Dependencias
Se respeta estrictamente la regla de dependencia: **Las dependencias de código fuente solo pueden apuntar hacia adentro.**
*   `Adaptadores` -> dependen de -> `Dominio` y `Puertos`
*   `Aplicación` -> depende de -> `Dominio` y `Puertos`
*   `Dominio` -> depende de -> **Nada**
38: 
39: ## Diagrama (Conceptual)
40: 
41: ```
42:         USUARIO / HTTP                 FILESYSTEM / LIBS
43:              |                                 |
44:    [ Adaptador Conductor ]           [ Adaptador Conducido ]
45:       (FastAPI/CLI)                  (xhtml2pdf / FS)
46:              |                                 |
47:              V                                 ^
48:       +-------------+                   +-------------+
49:       | Puerto Entr.|                   | Puerto Sal. |
50:       +------+------+                   +------+------+
51:              |                                 ^
52:              v                                 |
53:       +-------------------------------------------+
54:       |           SERVICIO DE APLICACIÓN          |
55:       +-------------------------------------------+
56:       |                 DOMINIO                   |
57:       +-------------------------------------------+
58: ```
