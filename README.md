# Text to PDF Service

> **Note:** This project is an AI-assisted software engineering experiment led by **Carlos Arturo Rojas Bolaños**, exploring autonomous development capabilities while maintaining strict quality patterns and hexagonal architecture.

A professional service to convert Markdown and Text documents to styled PDF files.

## License

Distributed under the MIT License. Copyright (c) 2026 Carlos Arturo Rojas Bolaños. See [LICENSE](LICENSE) for details.

## Features

*   **Clean Architecture**: Strictly follows Hexagonal Architecture (Ports & Adapters) pattern
*   **Multiple Interfaces**: REST API (FastAPI) and CLI (Typer)
*   **Format Support**: Markdown (with tables, code blocks) and Plain Text
*   **Professional Styling**: Clean, readable PDF output with proper typography
*   **Multi-file Upload**: Upload multiple files and get a ZIP with all PDFs
*   **Bulk Processing**: Process local files via API endpoint
*   **Docker Ready**: Fully containerized with Docker Compose
*   **Comprehensive Logging**: Color-coded console + file rotation in `logs/service.log`
*   **Observability**: Integrated request tracing (`X-Request-ID`) and performance monitoring (`X-Process-Time`)
*   **Auto-generated Documentation**: Interactive Swagger UI at `/docs`

## Branching Strategy

This project follows a professional branching model for continuous evolution:

*   **`main`**: Production-ready code. Only contains stable, tagged releases (v1.x.x).
*   **`develop`**: Integration branch for the next release. **IMPORTANT: All Pull Requests from the community must target this branch.**
*   **`workspace/v1-next`**: **Reserved for project owner.** Active development branch for upcoming version prototyping and internal evolution.

## Project Structure

```
text-to-pdf-service/
├── src/
│   ├── domain/           # Core business logic (models, ports, exceptions)
│   ├── application/      # Use cases (Conversion Service)
│   ├── adapters/
│   │   ├── driving/      # API and CLI
│   │   └── driven/       # PDF and FileSystem implementations
│   └── infrastructure/   # Cross-cutting concerns (logger)
├── tests/                # Unit and integration tests
│   ├── unit/
│   └── integration/
├── scripts/              # Development scripts
├── data/                 # Working directories
│   ├── input/            # Place source files for bulk processing
│   └── output/           # Generated PDFs appear here
├── logs/                 # Application logs
└── docs/                 # Documentation (with docs/es/ for Spanish)
```

## Quick Start

### Using Docker (Recommended)

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

### Starting from Zero (Docker)

If you want to perform a clean-wipe and start fresh:

```bash
# 1. Stop and remove everything related to the project
docker-compose down --rmi all --volumes --remove-orphans

# 2. Build and start from scratch
docker-compose up -d --build
```

**Docker Management Commands:**
```bash
# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop and remove containers
docker-compose down
```

### Local Development

**Prerequisites**: Python 3.11.9 (Recommended), Poetry

```bash
# Install dependencies
poetry install

# Run API server
poetry run uvicorn src.adapters.driving.api:app --reload

# Or use CLI
poetry run python -m src.adapters.driving.cli convert input.md output.pdf
```

## Usage

### REST API

**Interactive Documentation**: Open `http://localhost:8000/docs` in your browser.

#### Convert Single File
```bash
curl -X POST "http://localhost:8000/convert/" \
  -F "file=@document.md" \
  --output result.pdf
```

#### Convert Multiple Files (NEW!)
Upload multiple files and receive a ZIP with all PDFs:
```bash
curl -X POST "http://localhost:8000/convert/multiple" \
  -F "files=@doc1.md" \
  -F "files=@doc2.md" \
  -F "files=@doc3.txt" \
  --output results.zip
```
**Limits**: Max 20 files, 10MB/file, 50MB total.

#### Bulk Convert Local Files
Process all files in `data/input/`:
```bash
curl -X POST "http://localhost:8000/bulk-convert"
```
Check `data/output/` for generated PDFs.

### Command Line

```bash
poetry run python -m src.adapters.driving.cli convert input.md output.pdf
```

### Local Batch Script

```bash
# Process all files from data/input to data/output
poetry run python scripts/process_local.py
```

### Automation Workflows

This project includes standardized workflows in `.agent/workflows/` to simplify common tasks:

- **Setup**: `setup.md` - Complete environment initialization.
- **Serve**: `serve.md` - Start the API server with correct paths.

If using an Agentic IDE (like Antigravity), you can run these directly via slash commands (e.g., `/setup`, `/serve`).

## Documentation

### 📖 Table of Contents

| Topic | English | Español |
|-------|---------|---------|
| **Architecture** | [architecture.md](docs/architecture.md) | [architecture.md](docs/es/architecture.md) |
| **API Reference** | [api.md](docs/api.md) | [api.md](docs/es/api.md) |
| **Testing** | [tests.md](docs/tests.md) | [tests.md](docs/es/tests.md) |
| **Contributing** | [CONTRIBUTING.md](CONTRIBUTING.md) | [CONTRIBUTING.md](docs/es/CONTRIBUTING.md) |
| **Code of Conduct** | [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | [CODE_OF_CONDUCT.md](docs/es/CODE_OF_CONDUCT.md) |
| **Commit Conventions** | [COMMIT_CONVENTIONS.md](docs/COMMIT_CONVENTIONS.md) | [COMMIT_CONVENTIONS.md](docs/es/COMMIT_CONVENTIONS.md) |
| **AI Development** | [AI_DEVELOPMENT.md](docs/AI_DEVELOPMENT.md) | [AI_DEVELOPMENT.md](docs/es/AI_DEVELOPMENT.md) |

## Testing

```bash
# Run all tests with coverage
poetry run pytest --cov=src --cov-report=term-missing

# Run specific test file
poetry run pytest tests/unit/test_service.py -v
```

**Current Coverage**: 62%  
**Target Coverage**: 70%+

## Observability & Monitoring

The service includes professional observability features out-of-the-box:

- **Request Tracing**: Every API request is assigned a unique `X-Request-ID`. This ID is returned in the response headers and included in all logs related to that request, enabling precise end-to-end tracing.
- **Performance Headers**: The `X-Process-Time` response header reports the exact time (in seconds) the server took to process the conversion.
- **Structured Logs**: Application logs are stored in `logs/service.log` with a rotating strategy. Console output is color-coded for fast visual debugging.

Log colors:
- 🟢 INFO (Green)
- 🟡 WARNING (Yellow)
- 🔴 ERROR (Red)
- 🟣 CRITICAL (Magenta)

## Development

### Code Style
*   All code, comments, and docstrings: **English**
*   User-facing output/reports: **Spanish**
*   Follow PEP 8 and Hexagonal Architecture principles

### Commit Conventions
This project uses **Conventional Commits** with required scopes. See [COMMIT_CONVENTIONS.md](docs/COMMIT_CONVENTIONS.md).

### Adding Features
1. Define domain model in `src/domain/`
2. Create port (interface) if needed
3. Implement adapter in `src/adapters/driven/`
4. Update service in `src/application/`
5. Expose via API or CLI in `src/adapters/driving/`
6. Write tests

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

Quick checklist:
*   Tests pass (`poetry run pytest`)
*   Code follows project architecture
*   Commit messages follow conventions
*   Public documentation has Spanish version

## Roadmap

*   ✅ V1.0: Core conversion, API, CLI, Docker
*   ✅ V1.0: Multi-file upload endpoint
*   ✅ V1.0: Advanced observability and tracing
*   ✅ V1.0: Professional documentation (EN/ES)

## Cross-Platform Guide

The service is designed to run seamlessly on Windows, Linux, and macOS.

| Feature | Windows (PowerShell/CMD) | Linux / macOS (Bash/Zsh) |
|---------|-------------------------|--------------------------|
| **Paths** | `data\input`, `.\.venv` | `data/input`, `./.venv` |
| **Env Activation** | `.venv\Scripts\Activate.ps1` | `source .venv/bin/activate` |
| **Python Command** | `python` or `py` | `python3` |
| **Docker** | Docker Desktop (Hyper-V/WSL2) | Docker Engine (Native) |

> [!TIP]
> **Why Docker?** Using Docker is the **highly recommended** way to run the service in non-Windows environments or production, as it eliminates "it works on my machine" issues by packaging all OS dependencies (like PDF libraries) into a consistent container.

---

**Maintainer**: Carlos Arturo Rojas Bolaños  
**Repository**: text-to-pdf-service  
**Version**: 1.0.0
