---
description: how to setup the development environment or fix installation issues
---

1. Ensure Python 3.11.9 (LTS) is installed.
2. Open terminal in the project root.
3. Configure Poetry (local config):
```powershell
poetry config virtualenvs.in-project true
```
4. Configure environment:
```powershell
poetry env use 3.11.9
```
5. Install dependencies:
// turbo
```powershell
poetry install
```
6. Verify with tests:
// turbo
```powershell
poetry run pytest
```

### Docker Setup (Build)

Standard build before running:
// turbo
```powershell
docker-compose build
```

### Starting from Zero (Troubleshooting / Reset)

If you encounter persistent dependency errors or want a 100% fresh start:
// turbo
```powershell
# 1. Deep clean (removes images, volumes, and orphans)
docker-compose down --rmi all --volumes --remove-orphans

# 2. Fresh build and run
docker-compose up -d --build
```
