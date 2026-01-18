# Servicio Text to PDF

> **Nota:** Este proyecto es un experimento de ingeniería de software asistido por IA liderado por **Carlos Arturo Rojas Bolaños**, explorando capacidades de desarrollo autónomo mientras mantiene patrones de calidad estrictos y arquitectura hexagonal.

Un servicio profesional para convertir documentos Markdown y Texto a archivos PDF estilizados.

## Licencia

Distribuido bajo la Licencia MIT. Copyright (c) 2026 Carlos Arturo Rojas Bolaños. Ver [LICENSE](LICENSE) para detalles.

## Características

*   **Arquitectura Limpia**: Sigue estrictamente el patrón de Arquitectura Hexagonal (Puertos y Adaptadores)
*   **Múltiples Interfaces**: API REST (FastAPI) y CLI (Typer)
*   **Soporte de Formatos**: Markdown (con tablas, bloques de código) y Texto Plano
*   **Estilo Profesional**: Salida PDF limpia y legible con tipografía adecuada
*   **Carga Multi-archivo**: Sube múltiples archivos y recibe un ZIP con todos los PDFs
*   **Procesamiento Masivo**: Procesa archivos locales vía endpoint de API
*   **Listo para Docker**: Totalmente containerizado con Docker Compose
*   **Registro Completo**: Consola con colores + rotación de archivos en `logs/service.log`
*   **Observabilidad**: Trazabilidad de peticiones (`X-Request-ID`) y monitoreo de rendimiento (`X-Process-Time`) integrados
*   **Documentación Auto-generada**: Swagger UI interactivo en `/docs`

## Estrategia de Ramas

Este proyecto sigue un modelo de ramificación profesional para su evolución continua:

*   **`main`**: Código listo para producción. Solo contiene versiones estables y etiquetadas (v1.x.x).
*   **`develop`**: Rama de integración para el próximo lanzamiento. **IMPORTANTE: Todos los Pull Requests de la comunidad deben apuntar a esta rama.**
*   **`workspace/v1-next`**: **Reservada para el dueño del proyecto.** Rama de desarrollo activo para prototipado y evolución interna.

## Estructura del Proyecto

```
text-to-pdf-service/
├── src/
│   ├── domain/           # Lógica de negocio central (modelos, puertos, excepciones)
│   ├── application/      # Casos de uso (Servicio de Conversión)
│   ├── adapters/
│   │   ├── driving/      # API y CLI
│   │   └── driven/       # Implementaciones de PDF y FileSystem
│   └── infrastructure/   # Concerns transversales (logger)
├── tests/                # Pruebas unitarias e integración
│   ├── unit/
│   └── integration/
├── scripts/              # Scripts de desarrollo
├── data/                 # Directorios de trabajo
│   ├── input/            # Coloca archivos para procesamiento masivo
│   └── output/           # Los PDFs generados aparecen aquí
├── logs/                 # Logs de la aplicación
└── docs/                 # Documentación (con docs/es/ para español)
```

## Inicio Rápido

### Usando Docker (Recomendado)

```bash
docker-compose up --build
```

La API estará disponible en `http://localhost:8000`.

### Iniciando Desde Cero (Docker)

Si deseas realizar una limpieza total y empezar desde una base limpia:

```bash
# 1. Detener y eliminar todo lo relacionado al proyecto
docker-compose down --rmi all --volumes --remove-orphans

# 2. Construir y arrancar desde cero
docker-compose up -d --build
```

**Comandos de Gestión Docker:**
```bash
# Ejecutar en segundo plano (background)
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener y eliminar contenedores
docker-compose down
```

### Desarrollo Local

**Prerequisitos**: Python 3.11.9 (Recomendado), Poetry

```bash
# Instalar dependencias
poetry install

# Ejecutar servidor API
poetry run uvicorn src.adapters.driving.api:app --reload

# O usar CLI
poetry run python -m src.adapters.driving.cli convert entrada.md salida.pdf
```

## Uso

### API REST

**Documentación Interactiva**: Abre `http://localhost:8000/docs` en tu navegador.

#### Convertir Archivo Individual
```bash
curl -X POST "http://localhost:8000/convert/" \
  -F "file=@documento.md" \
  --output resultado.pdf
```

#### Convertir Múltiples Archivos (¡NUEVO!)
Sube múltiples archivos y recibe un ZIP con todos los PDFs:
```bash
curl -X POST "http://localhost:8000/convert/multiple" \
  -F "files=@doc1.md" \
  -F "files=@doc2.md" \
  -F "files=@doc3.txt" \
  --output resultados.zip
```
**Límites**: Máx 20 archivos, 10MB/archivo, 50MB total.

#### Conversión Masiva de Archivos Locales
Procesa todos los archivos en `data/input/`:
```bash
curl -X POST "http://localhost:8000/bulk-convert"
```
Revisa `data/output/` para los PDFs generados.

### Línea de Comandos

```bash
poetry run python -m src.adapters.driving.cli convert entrada.md salida.pdf
```

### Script de Lotes Local

```bash
# Procesar todos los archivos de data/input a data/output
poetry run python scripts/process_local.py
```

### Workflows de Automatización

Este proyecto incluye flujos estandarizados en `.agent/workflows/` para simplificar tareas comunes:

- **Setup**: `setup.md` - Inicialización completa del entorno.
- **Serve**: `serve.md` - Iniciar el servidor API con las rutas correctas.

Si utilizas un IDE Agéntico (como Antigravity), puedes ejecutar estos comandos directamente (ej. `/setup`, `/serve`).

## Documentación

### 📖 Tabla de Contenidos

| Tema | Inglés | Español |
|-------|---------|---------|
| **Arquitectura** | [architecture.md](../architecture.md) | [architecture.md](architecture.md) |
| **Referencia API** | [api.md](../api.md) | [api.md](api.md) |
| **Pruebas** | [tests.md](../tests.md) | [tests.md](tests.md) |
| **Contribución** | [CONTRIBUTING.md](../../CONTRIBUTING.md) | [CONTRIBUTING.md](CONTRIBUTING.md) |
| **Código de Conducta** | [CODE_OF_CONDUCT.md](../../CODE_OF_CONDUCT.md) | [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) |
| **Convenciones Commits** | [COMMIT_CONVENTIONS.md](../COMMIT_CONVENTIONS.md) | [COMMIT_CONVENTIONS.md](COMMIT_CONVENTIONS.md) |
| **Desarrollo con IA** | [AI_DEVELOPMENT.md](../AI_DEVELOPMENT.md) | [AI_DEVELOPMENT.md](AI_DEVELOPMENT.md) |

## Pruebas

```bash
# Ejecutar todas las pruebas con cobertura
poetry run pytest --cov=src --cov-report=term-missing

# Ejecutar archivo de prueba específico
poetry run pytest tests/unit/test_service.py -v
```

**Cobertura Actual**: 62%  
**Cobertura Objetivo**: 70%+

## Observabilidad y Monitoreo

El servicio incluye capacidades profesionales de observabilidad de serie:

- **Trazabilidad de Peticiones**: A cada petición API se le asigna un `X-Request-ID` único. Este ID se devuelve en las cabeceras de respuesta y se incluye en todos los logs relacionados, permitiendo un rastreo preciso de extremo a extremo.
- **Cabeceras de Rendimiento**: La cabecera de respuesta `X-Process-Time` informa el tiempo exacto (en segundos) que el servidor tomó para procesar la conversión.
- **Logs Estructurados**: Los logs de la aplicación se guardan en `logs/service.log` con una estrategia de rotación. La salida por consola está coloreada para un debugging visual rápido.

Colores de logs:
- 🟢 INFO (Verde)
- 🟡 WARNING (Amarillo)
- 🔴 ERROR (Rojo)
- 🟣 CRITICAL (Magenta)

## Desarrollo

### Estilo de Código
*   Todo el código, comentarios y docstrings: **Inglés**
*   Salida/reportes de cara al usuario: **Español**
*   Seguir PEP 8 y principios de Arquitectura Hexagonal

### Convenciones de Commits
Este proyecto usa **Conventional Commits** con scopes requeridos. Ver [COMMIT_CONVENTIONS.md](COMMIT_CONVENTIONS.md).

### Agregar Funcionalidades
1. Definir modelo de dominio en `src/domain/`
2. Crear puerto (interfaz) si es necesario
3. Implementar adaptador en `src/adapters/driven/`
4. Actualizar servicio en `src/application/`
5. Exponer vía API o CLI en `src/adapters/driving/`
6. Escribir pruebas

## Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para directrices detalladas.

Checklist rápido:
*   Las pruebas pasan (`poetry run pytest`)
*   El código sigue la arquitectura del proyecto
*   Los mensajes de commit siguen las convenciones
*   La documentación pública tiene versión en español

## Hoja de Ruta

*   ✅ V1.0: Conversión central, API, CLI, Docker
*   ✅ V1.0: Endpoint de carga multi-archivo
*   ✅ V1.0: Observabilidad y trazabilidad avanzada
*   ✅ V1.0: Documentación profesional (EN/ES)

## Guía Multiplataforma

El servicio está diseñado para ejecutarse sin problemas en Windows, Linux y macOS.

| Característica | Windows (PowerShell/CMD) | Linux / macOS (Bash/Zsh) |
|---------|-------------------------|--------------------------|
| **Rutas** | `data\input`, `.\.venv` | `data/input`, `./.venv` |
| **Activación Env** | `.venv\Scripts\Activate.ps1` | `source .venv/bin/activate` |
| **Comando Python** | `python` o `py` | `python3` |
| **Docker** | Docker Desktop (Hyper-V/WSL2) | Docker Engine (Nativo) |

> [!TIP]
> **¿Por qué Docker?** Usar Docker es la forma **altamente recomendada** de ejecutar el servicio en entornos que no sean Windows o en producción, ya que elimina problemas de compatibilidad al empaquetar todas las dependencias del SO (como las librerías de PDF) en un contenedor consistente.

---

**Mantenedor**: Carlos Arturo Rojas Bolaños  
**Repositorio**: text-to-pdf-service  
**Versión**: 1.0.0
