# Commit Conventions

This project follows **Conventional Commits** specification strictly.

## Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

## Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(api): add multi-file upload endpoint` |
| `fix` | Bug fix | `fix(pdf): resolve list rendering issue` |
| `docs` | Documentation only | `docs(readme): update installation guide` |
| `style` | Formatting, no code change | `style(api): fix indentation` |
| `refactor` | Code change without feature/fix | `refactor(service): rename shared to infrastructure` |
| `perf` | Performance improvement | `perf(pdf): optimize image compression` |
| `test` | Adding/updating tests | `test(api): add coverage for bulk endpoint` |
| `build` | Build system changes | `build(docker): update base image` |
| `ci` | CI configuration | `ci(github): add coverage report` |
| `chore` | Maintenance tasks | `chore(deps): update dependencies` |
| `revert` | Revert previous commit | `revert: revert "feat(api): add endpoint"` |

## Scopes

Use the following scopes for this project:

| Scope | Description |
|-------|-------------|
| `api` | REST API endpoints |
| `cli` | Command line interface |
| `pdf` | PDF generation |
| `domain` | Domain models and logic |
| `service` | Application service |
| `docker` | Docker configuration |
| `docs` | Documentation |
| `deps` | Dependencies |
| `config` | Configuration files |
| `test` | Test files |

## Rules

1. **Always use lowercase** for type and scope
2. **Scope is required** for code changes
3. **Description must be imperative** ("add feature" not "added feature")
4. **Max 72 characters** for subject line
5. **Use body** for complex changes
6. **Reference issues** in footer: `Fixes #123`

## Examples

### Simple commit
```
feat(api): add bulk conversion endpoint
```

### Commit with body
```
fix(pdf): resolve horizontal list rendering

Lists were rendering horizontally due to missing CSS
display property. Added display: list-item to li elements
and markdown preprocessor to inject newlines.

Fixes #42
```

### Breaking change
```
feat(api)!: change endpoint path from /batch-process to /bulk-convert

BREAKING CHANGE: /tools/batch-process is now /bulk-convert
```

## Pre-commit Checklist

- [ ] Type is valid
- [ ] Scope is appropriate
- [ ] Description is imperative and clear
- [ ] Body explains WHY (not what)
- [ ] Related issues are referenced

---

**Enforcement**: This convention is enforced via PR review.
