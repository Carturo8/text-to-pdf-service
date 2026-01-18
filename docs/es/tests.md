# Documentación de Pruebas

**Última Actualización**: 2026-01-18  
**Resultados de Pruebas**: ✅ 9/9 Pasando  
**Cobertura**: 62% (325 líneas, 123 cubiertas)

## Estrategia de Testing

Este proyecto sigue un enfoque de testing integral con pruebas unitarias e de integración para asegurar confiabilidad y mantenibilidad.

### Estructura de Pruebas

```
tests/
├── unit/              # Pruebas unitarias (componentes aislados)
│   ├── test_api.py           # Endpoints FastAPI
│   ├── test_service.py       # Lógica de negocio
│   ├── test_fs_adapter.py    # Adaptador FileSystem
│   └── test_pdf_adapter.py   # Generación de PDF
└── integration/       # Pruebas de integración (flujo completo)
    └── test_integration.py   # Flujo de conversión completo
```

## Ejecutar Pruebas

### Todas las Pruebas con Cobertura
```bash
poetry run pytest --cov=src --cov-report=term-missing -v
```

### Archivo de Prueba Específico
```bash
poetry run pytest tests/unit/test_service.py -v
```

### Modo Watch (para desarrollo)
```bash
poetry run pytest --watch
```

## Resultados de Pruebas (Actual)

### Pruebas Unitarias
- ✅ `test_api.py` - Validación de endpoints API (3/3)
- ✅ `test_service.py` - Lógica de negocio (2/2)
- ✅ `test_fs_adapter.py` - Operaciones de archivos (3/3)
- ✅ `test_pdf_adapter.py` - Generación de PDF (1/1)

### Pruebas de Integración
- ✅ `test_integration.py` - Flujo end-to-end (1/1)

## Reporte de Cobertura

| Módulo | Sentencias | Faltantes | Cobertura |
|--------|-----------|-----------|-----------|
| **src/domain/** | 45 | 12 | 73% |
| **src/application/** | 63 | 18 | 71% |
| **src/adapters/driven/** | 142 | 65 | 54% |
| **src/adapters/driving/** | 58 | 19 | 67% |
| **src/infrastructure/** | 17 | 9 | 47% |
| **TOTAL** | **325** | **123** | **62%** |

## Objetivos de Cobertura

- **Actual**: 62%
- **Meta**: 70%+
- **Ideal**: 80%+

### Áreas que Necesitan Más Cobertura
1. `fs_archiver.py` - Módulo de archivado
2. `logger.py` - Utilidades de logging
3. Casos edge de manejo de errores

## Convenciones de Testing

### Nomenclatura
- Archivos de prueba: `test_*.py`
- Funciones de prueba: `test_<feature>_<scenario>()`
- Ejemplo: `test_convert_invalid_type()`

### Estructura (Patrón AAA)
```python
def test_feature_scenario():
    # Arrange - Preparación
    adapter = LocalFileSystemAdapter()
    
    # Act - Ejecución
    result = adapter.save_file("test.pdf", b"data")
    
    # Assert - Verificación
    assert os.path.isabs(result)
```

### Mocking
- Usar `unittest.mock` para dependencias externas
- Parchear en el punto de uso, no en la definición
- Ejemplo: `@patch("src.adapters.driving.api.get_service")`

## Mejores Prácticas de Testing

1. **Aislamiento**: Cada prueba es independiente
2. **Rapidez**: Las pruebas corren en < 2 segundos
3. **Determinista**: Mismo input = mismo output
4. **Descriptivo**: Nombres de prueba claros
5. **Cobertura**: Apuntar a 70%+ en lógica de negocio

## Integración CI/CD

Las pruebas corren automáticamente en:
- Cada pull request
- Merge a `develop`
- Merge a `main`

Ver [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) para configuración.

## Problemas Comunes

### Errores de Importación
**Solución**: Asegurar que `PYTHONPATH` incluya la raíz del proyecto
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Cobertura No Generada
**Solución**: Instalar extras de desarrollo
```bash
poetry install --with dev
```

## Mejoras Futuras

- [ ] Agregar benchmarks de rendimiento
- [ ] Agregar pruebas de integración de API
- [ ] Aumentar cobertura a 80%+
- [ ] Agregar mutation testing
- [ ] Agregar load testing para conversión masiva

---

**Mantenido por**: Carlos Arturo Rojas Bolaños  
**Framework**: Pytest + Coverage.py  
**Última Ejecución**: 2026-01-17 23:24 UTC
