---
description: how to run the API server
---

### Local Execution (Poetry)

1. Run the FastAPI server:
// turbo
```powershell
poetry run uvicorn src.adapters.driving.api:app --reload
```
2. Access Swagger UI at `http://localhost:8000/docs`.

---

### Docker Execution

1. Run the containerized service:
// turbo
```powershell
docker-compose up -d
```
2. Access the server at `http://localhost:8000/docs`.

**Manage Docker containers:**
```powershell
# View real-time logs
docker-compose logs -f

# Stop the service
docker-compose down
```

> [!TIP]
> If the container fails to start, refer to the **Clean Wipe** guide in **setup.md**.
