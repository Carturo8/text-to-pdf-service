# Contribuyendo a Text-to-PDF Service

¡Gracias por considerar contribuir a este proyecto! Este documento proporciona directrices para contribuir.

## Código de Conducta

Este proyecto sigue un código de conducta profesional. Por favor, sé respetuoso y constructivo en todas las interacciones.

## Primeros Pasos

### Prerequisitos
- Python 3.11.9 (LTS)
- Poetry 1.8+
- Git

### Configuración
```bash
# Clonar el repositorio
git clone https://github.com/yourusername/text-to-pdf-service.git
cd text-to-pdf-service

# Instalar dependencias
poetry install

# Ejecutar pruebas
poetry run pytest --cov=src
```

## Flujo de Desarrollo

Este proyecto sigue un modelo de evolución profesional para asegurar la estabilidad permitiendo al mismo tiempo el desarrollo activo.

### 1. Estrategia de Flujo de Trabajo

1.  **Trabajo en Evolución**: El dueño del proyecto trabaja en la rama `workspace/v1-next`.
2.  **Contribuciones de la Comunidad**: Si eres un contribuidor, por favor **basa tu trabajo en la rama `develop`** y abre tu PR hacia la rama `develop`.
3.  **PR Obligatorios**: Todos los cambios deben enviarse mediante Pull Request. Los pushes directos a `main` o `develop` están bloqueados.
4.  **Cumplimiento de CI**: Cada PR debe pasar todas las Pruebas Automatizadas y verificaciones de Linting en GitHub Actions antes de poder ser fusionado.
5.  **Revisión y Aprobación**: Los PRs requieren una revisión positiva. Para contribuciones de la comunidad, el Dueño del Proyecto es el aprobador final.

### 2. Estándares

*   **Arquitectura**: Seguir el patrón de Arquitectura Hexagonal (Puertos y Adaptadores).
*   **Pruebas**: Escribir pruebas unitarias y de integración para nueva funcionalidad.
*   **Commits**: Usar mensajes de commit profesionales. Aunque los Conventional Commits estrictos se relajan en `workspace/v1-next`, son obligatorios al fusionar hacia `develop` y `main`.

### 1. Crear una Rama
```bash
git checkout -b feature/nombre-de-tu-funcionalidad
```

### 2. Realizar Cambios
- Seguir la estructura de código existente (Arquitectura Hexagonal)
- Escribir pruebas para nueva funcionalidad
- Actualizar documentación según sea necesario

### 3. Ejecutar Pruebas
```bash
# Todas las pruebas deben pasar
poetry run pytest --cov=src --cov-report=term-missing

# La cobertura debe ser >60% (idealmente 70%+)
```

### 4. Enviar Pull Request
- Crear PR contra la rama `develop`
- Describir tus cambios claramente
- Enlazar issues relacionados

## Estándares de Código

### Arquitectura
- **Arquitectura Hexagonal (Puertos y Adaptadores)** se aplica estrictamente
- Lógica de dominio debe estar en `src/domain/`
- Lógica de aplicación en `src/application/`
- Infraestructura en `src/adapters/` y `src/infrastructure/`

### Estilo de Código
- **Idioma**: Todo el código, comentarios y docstrings en **Inglés**
- **Formato**: Seguir PEP 8
- **Type Hints**: Requeridos para todas las funciones públicas
- **Docstrings**: Estilo Google para todas las APIs públicas

### Ejemplo
```python
def convert_file(input_path: str, output_path: str) -> str:
    """
    Convert a single file to PDF format.
    
    Args:
        input_path: Absolute path to source file
        output_path: Absolute path for PDF output
        
    Returns:
        Path to generated PDF file
        
    Raises:
        UnsupportedFormatError: If file format is not supported
        ConversionError: If PDF generation fails
    """
    pass
```

## Pruebas

### Requerido
- Pruebas unitarias para nuevas funciones
- Pruebas de integración para nuevos endpoints
- Todas las pruebas deben pasar antes del PR

### Objetivos de Cobertura
- Mínimo: 60%
- Meta: 70%+
- Ideal: 80%+

## Documentación

### Actualizaciones Requeridas
- Actualizar `README.md` (Inglés)
- Actualizar `docs/es/README.md` (Español)
- Actualizar archivos relevantes en `docs/` y `docs/es/`
- Actualizar docstrings de Swagger para cambios de API

### Estándares de Documentación
- El inglés es primario
- La traducción al español debe tener paridad 1:1
- Usar formato markdown
- Incluir ejemplos de código cuando sea útil

## Mensajes de Commit

Seguir conventional commits:
```
feat: agregar endpoint de conversión masiva
fix: resolver error de importación Path en fs_adapter
docs: actualizar documentación de API
test: agregar cobertura para adaptador PDF
refactor: renombrar shared a infrastructure
```

## Proceso de Pull Request

1. Asegurar que todas las pruebas pasen
2. Actualizar documentación
3. **Mínimo 1 aprobación** requerida para `develop`
4. **Mínimo 2 aprobaciones** requeridas para `main`
5. Squash commits antes de hacer merge

## ¿Preguntas o Problemas?

- Abrir un issue en GitHub
- Revisar issues existentes primero
- Proporcionar pasos claros de reproducción para bugs

## Licencia

Al contribuir, aceptas que tus contribuciones serán licenciadas bajo la Licencia MIT.

---

**¡Gracias por contribuir!**  
Mantenido por Carlos Arturo Rojas Bolaños
