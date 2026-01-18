# Testing Documentation

**Last Updated**: 2026-01-18  
**Test Results**: ✅ 9/9 Passing  
**Coverage**: 62% (325 lines, 123 covered)

## Testing Strategy

This project follows a comprehensive testing approach with unit and integration tests to ensure reliability and maintainability.

### Test Structure

```
tests/
├── unit/              # Unit tests (isolated components)
│   ├── test_api.py           # FastAPI endpoints
│   ├── test_service.py       # Business logic
│   ├── test_fs_adapter.py    # FileSystem adapter
│   └── test_pdf_adapter.py   # PDF generation
└── integration/       # Integration tests (end-to-end)
    └── test_integration.py   # Full conversion workflow
```

## Running Tests

### All Tests with Coverage
```bash
poetry run pytest --cov=src --cov-report=term-missing -v
```

### Specific Test File
```bash
poetry run pytest tests/unit/test_service.py -v
```

### Watch Mode (for development)
```bash
poetry run pytest --watch
```

## Test Results (Current)

### Unit Tests
- ✅ `test_api.py` - API endpoint validation (3/3)
- ✅ `test_service.py` - Business logic (2/2)
- ✅ `test_fs_adapter.py` - File operations (3/3)
- ✅ `test_pdf_adapter.py` - PDF generation (1/1)

### Integration Tests
- ✅ `test_integration.py` - End-to-end workflow (1/1)

## Coverage Report

| Module | Statements | Missing | Coverage |
|--------|-----------|---------|----------|
| **src/domain/** | 45 | 12 | 73% |
| **src/application/** | 63 | 18 | 71% |
| **src/adapters/driven/** | 142 | 65 | 54% |
| **src/adapters/driving/** | 58 | 19 | 67% |
| **src/infrastructure/** | 17 | 9 | 47% |
| **TOTAL** | **325** | **123** | **62%** |

## Coverage Goals

- **Current**: 62%
- **Target**: 70%+
- **Ideal**: 80%+

### Areas Needing More Coverage
1. `fs_archiver.py` - Archival module
2. `logger.py` - Logging utilities
3. Error handling edge cases

## Test Conventions

### Naming
- Test files: `test_*.py`
- Test functions: `test_<feature>_<scenario>()`
- Example: `test_convert_invalid_type()`

### Structure (AAA Pattern)
```python
def test_feature_scenario():
    # Arrange - Setup
    adapter = LocalFileSystemAdapter()
    
    # Act - Execute
    result = adapter.save_file("test.pdf", b"data")
    
    # Assert - Verify
    assert os.path.isabs(result)
```

### Mocking
- Use `unittest.mock` for external dependencies
- Patch at the usage point, not definition
- Example: `@patch("src.adapters.driving.api.get_service")`

## Testing Best Practices

1. **Isolation**: Each test is independent
2. **Fast**: Tests run in < 2 seconds
3. **Deterministic**: Same input = same output
4. **Descriptive**: Clear test names
5. **Coverage**: Aim for 70%+ on business logic

## CI/CD Integration

Tests run automatically on:
- Every pull request
- Merge to `develop`
- Merge to `main`

See [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) for configuration.

## Common Issues

### Import Errors
**Solution**: Ensure `PYTHONPATH` includes project root
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Coverage Not Generated
**Solution**: Install coverage extras
```bash
poetry install --with dev
```

## Future Improvements

- [ ] Add performance benchmarks
- [ ] Add API integration tests
- [ ] Increase coverage to 80%+
- [ ] Add mutation testing
- [ ] Add load testing for bulk conversion

---

**Maintained by**: Carlos Arturo Rojas Bolaños  
**Framework**: Pytest + Coverage.py  
**Last Test Run**: 2026-01-17 23:24 UTC
