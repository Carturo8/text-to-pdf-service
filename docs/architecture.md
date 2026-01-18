# Architecture Documentation

## Overview
The **Text-to-PDF Service** follows a strict **Hexagonal Architecture (Ports and Adapters)**. This pattern allows the application to be independent of frameworks, UI, databases, and external agencies.

## Core Concepts

### 1. Domain (Core)
Located in `src/domain/`.
*   **Entities**: `ConversionRequest`, `ConversionResult` (Pure Python dataclasses).
*   **Ports (Interfaces)**: Defines *how* the outside world interacts with the application (`Input Ports`) and how the application interacts with external tools (`Output Ports`).
    *   `PDFConverterPort`: Interface for PDF generation.
    *   `FileSystemPort`: Interface for reading/writing files.

### 2. Application (Business Logic)
Located in `src/application/`.
*   **Services**: `ConversionService`.
*   **Responsibility**: Orchestrates the flow of data. It receives a command, validates it using Domain rules, triggers the adapter via a Port, and returns a result. It does **not** know about HTTP or CLI.

### 3. Adapters (Infrastructure)
Located in `src/adapters/`.

#### Driving Adapters (Primary)
They trigger the application.
*   **API (`src/adapters/driving/api.py`)**: FastAPI implementation. Exposes REST endpoints.
*   **CLI (`src/adapters/driving/cli.py`)**: Typer implementation. Allows command-line execution.

#### Driven Adapters (Secondary)
They are triggered by the application.
*   **Xhtml2PdfAdapter (`src/adapters/driven/pdf_adapter.py`)**: Implements `PDFConverterPort`. Uses `xhtml2pdf` library to generate PDFs from HTML/CSS.
*   **LocalFileSystemAdapter (`src/adapters/driven/fs_adapter.py`)**: Implements `FileSystemPort`. Handles local disk I/O.

## Dependency Flow
The dependency rule is strictly observed: **Source Code dependencies can only point inward.**
*   `Adapters` -> depend on -> `Domain` & `Ports`
*   `Application` -> depends on -> `Domain` & `Ports`
*   `Domain` -> depends on -> **Nothing**

## Diagram (Conceptual)

```
        USER / HTTP                    FILESYSTEM / LIBS
             |                                 |
   [ Driving Adapter ]               [ Driven Adapter ]
      (FastAPI/CLI)                  (xhtml2pdf / FS)
             |                                 |
             V                                 ^
      +-------------+                   +-------------+
      | Input Port  |                   | Output Port |
      +------+------+                   +------+------+
             |                                 ^
             v                                 |
      +-------------------------------------------+
      |           APPLICATION SERVICE             |
      +-------------------------------------------+
      |                 DOMAIN                    |
      +-------------------------------------------+
```
