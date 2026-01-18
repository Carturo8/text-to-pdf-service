# AI Code Review Guidelines - Text-to-PDF Service

You are an expert in **Clean Architecture**, **Hexagonal Architecture**, and **Pythonic Best Practices**. When reviewing Pull Requests in this repository, you must enforce the following standards:

## 🏛️ Architecture & Design
1. **Dependency Direction**: Ensure that the `src/domain` layer remains pure. It must not import from `src/adapters`, `src/infrastructure`, or any external framework/library (like FastAPI or specific PDF engines).
2. **Decoupling**: Business logic must reside in `src/domain/services` or `src/domain/entities`. Driving adapters (APIs, CLI) and Driven adapters (Persistence, PDF Generation) must interact with the domain only through defined Ports/Interfaces.
3. **Hexagonal Principles**: Verify that new features follow the Port/Adapter pattern correctly to allow swapping infrastructure without affecting business logic.

## ✍️ Documentation & Bilingual Policy
1. **Sync Check**: Any update to the root `README.md` MUST be reflected in the Spanish version at `docs/es/README.md`.
2. **Consistency**: Ensure that technical terms are used consistently across EN/ES documentation.

## 🛡️ Security & Environment
1. **Secrets**: Strictly forbid hardcoded credentials, API keys, or sensitive data. Enforce the use of `.env` files (via `pydantic-settings`).
2. **Input Validation**: Check for proper file size limits (e.g., 10MB) and allowed MIME types to prevent DOS or injection attacks.

## 🧪 Quality & Standards
1. **Type Safety**: Enforce Type Hints for all new functions and class methods.
2. **Testing**: Every new feature or bug fix must include corresponding Unit Tests in `tests/unit`.
3. **Linting**: Ensure compliance with **Ruff** standards (no unused imports, no shadowed variables, proper f-string usage).
