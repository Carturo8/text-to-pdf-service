# Contributing to Text-to-PDF Service

Thank you for considering contributing to this project! This document provides guidelines for contributing.

## Code of Conduct

This project follows a professional code of conduct. Please be respectful and constructive in all interactions.

## Getting Started

### Prerequisites
- Python 3.11.9 (LTS)
- Poetry 1.8+
- Git

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/text-to-pdf-service.git
cd text-to-pdf-service

# Install dependencies
poetry install

# Run tests
poetry run pytest --cov=src
```

## Development Workflow

This project follows a professional evolution model to ensure stability while allowing active development.

### 1. Workflow Strategy

1.  **Work on Evolution**: The Project Owner works in the `workspace/v1-next` branch.
2.  **Community Contributions**: If you are a contributor, please **base your work on the `develop` branch** and open your PR toward the `develop` branch.
3.  **Mandatory PRs**: All changes must be submitted via Pull Request. Direct pushes to `main` or `develop` are blocked.
4.  **CI Enforcement**: Every PR must pass all Automated Tests and Linting checks in GitHub Actions before it can be merged.
5.  **Review & Approval**: PRs require a positive review. For community contributions, the Project Owner is the final approver.

### 2. Standards

*   **Architecture**: Follow the Hexagonal Architecture (Ports & Adapters) pattern.
*   **Testing**: Write unit and integration tests for new functionality.
*   **Commits**: Use professional commit messages. While strict Conventional Commits are relaxed on `workspace/v1-next`, they are mandatory when merging into `develop` and `main`.

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Follow the existing code structure (Hexagonal Architecture)
- Write tests for new functionality
- Update documentation as needed

### 3. Run Tests
```bash
# All tests must pass
poetry run pytest --cov=src --cov-report=term-missing

# Coverage should be >60% (ideally 70%+)
```

### 4. Submit Pull Request
- Create PR against `develop` branch
- Describe your changes clearly
- Link any related issues

## Code Standards

### Architecture
- **Hexagonal Architecture (Ports & Adapters)** is strictly enforced
- Domain logic must be in `src/domain/`
- Application logic in `src/application/`
- Infrastructure in `src/adapters/` and `src/infrastructure/`

### Code Style
- **Language**: All code, comments, and docstrings in **English**
- **Formatting**: Follow PEP 8
- **Type Hints**: Required for all public functions
- **Docstrings**: Google style for all public APIs

### Example
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

## Testing

### Required
- Unit tests for new functions
- Integration tests for new endpoints
- All tests must pass before PR

### Coverage Goals
- Minimum: 60%
- Target: 70%+
- Ideal: 80%+

## Documentation

### Required Updates
- Update `README.md` (English)
- Update `docs/es/README.md` (Spanish)
- Update relevant files in `docs/`
- Update Swagger docstrings for API changes

### Documentation Standards
- English is primary
- Spanish translation must have 1:1 parity
- Use markdown formatting
- Include code examples where helpful

## Commit Messages

Follow conventional commits:
```
feat: add bulk conversion endpoint
fix: resolve Path import error in fs_adapter
docs: update API documentation
test: add coverage for PDF adapter
refactor: rename shared to infrastructure
```

## Pull Request Process

1. Ensure all tests pass
2. Update documentation
3. **Minimum 1 approval** required for `develop`
4. **Minimum 2 approvals** required for `main`
5. Squash commits before merging

## Questions or Issues?

- Open an issue on GitHub
- Check existing issues first
- Provide clear reproduction steps for bugs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing!**  
Maintained by Carlos Arturo Rojas Bolaños
