# Convenciones de Commits

Este proyecto sigue estrictamente la especificación de **Conventional Commits**.

## Formato

```
<tipo>(<alcance>): <descripción>

[cuerpo opcional]

[pie opcional]
```

## Tipos

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| `feat` | Nueva funcionalidad | `feat(api): agregar endpoint multi-archivo` |
| `fix` | Corrección de bug | `fix(pdf): resolver problema de listas` |
| `docs` | Solo documentación | `docs(readme): actualizar guía de instalación` |
| `style` | Formato, sin cambio de código | `style(api): corregir indentación` |
| `refactor` | Cambio sin agregar feature/fix | `refactor(service): renombrar shared a infrastructure` |
| `perf` | Mejora de rendimiento | `perf(pdf): optimizar compresión de imagen` |
| `test` | Agregar/actualizar tests | `test(api): agregar cobertura para bulk endpoint` |
| `build` | Cambios en sistema de build | `build(docker): actualizar imagen base` |
| `ci` | Configuración de CI | `ci(github): agregar reporte de cobertura` |
| `chore` | Tareas de mantenimiento | `chore(deps): actualizar dependencias` |
| `revert` | Revertir commit previo | `revert: revertir "feat(api): agregar endpoint"` |

## Alcances (Scopes)

| Alcance | Descripción |
|---------|-------------|
| `api` | Endpoints REST API |
| `cli` | Interfaz de línea de comandos |
| `pdf` | Generación de PDF |
| `domain` | Modelos y lógica de dominio |
| `service` | Servicio de aplicación |
| `docker` | Configuración Docker |
| `docs` | Documentación |
| `deps` | Dependencias |
| `config` | Archivos de configuración |
| `test` | Archivos de pruebas |

## Reglas

1. **Siempre usa minúsculas** para tipo y alcance
2. **Alcance es obligatorio** para cambios de código
3. **Descripción debe ser imperativa** ("agregar feature" no "agregado feature")
4. **Máximo 72 caracteres** en línea de asunto
5. **Usa cuerpo** para cambios complejos
6. **Referencia issues** en pie: `Fixes #123`

## Ejemplos

### Commit simple
```
feat(api): agregar endpoint de conversión masiva
```

### Commit con cuerpo
```
fix(pdf): resolver renderizado horizontal de listas

Las listas se renderizaban horizontalmente debido a propiedad
CSS faltante. Se agregó display: list-item a elementos li
y preprocesador markdown para inyectar saltos de línea.

Fixes #42
```

### Cambio breaking
```
feat(api)!: cambiar ruta de endpoint de /batch-process a /bulk-convert

BREAKING CHANGE: /tools/batch-process ahora es /bulk-convert
```

---

## Checklist Pre-commit

- [ ] El tipo es válido
- [ ] El alcance es apropiado
- [ ] La descripción es imperativa y clara
- [ ] El cuerpo explica el PORQUÉ (no el qué)
- [ ] Los issues relacionados están referenciados

---

**Aplicación**: Esta convención se aplica mediante revisión de PR.
