# Framework Module

> **DEPRECATED** -- This module is scheduled for removal. Do not add new code here.

## Migration Status

The contents of `src/framework/` are being relocated to canonical locations established by the domain restructuring (ADR-046) and codebase conventions:

| Subdirectory | Current Contents | Target Location |
|---|---|---|
| `context/` | Agent context assembly, directive loading | `src/domain/doctrine/` (governance loading) or `tools/` (CLI utilities) |
| `orchestration/` | Agent base class, orchestrator, task utilities | `src/domain/collaboration/` (domain logic) or `src/llm_service/` (execution infrastructure) |
| `config/` | Framework configuration | `src/llm_service/config/` |
| `schemas/` | JSON schemas | `src/llm_service/` or `fixtures/` depending on usage |

## Why This Module Is Deprecated

The original `src/framework/` predates the bounded context structure introduced by ADR-046. Its responsibilities overlap with and are now better served by:

- **`src/domain/collaboration/`** -- Task lifecycle, orchestration domain logic
- **`src/domain/doctrine/`** -- Agent profiles, directive loading, governance
- **`src/llm_service/`** -- Execution infrastructure, adapters, routing
- **`tools/`** -- Development-time utilities and scripts

## For Contributors

- **Do not** add new modules or classes to this directory.
- **Do not** create new imports from `src.framework` in other modules.
- Existing references will be migrated as part of the ongoing restructuring.

## Related ADRs

- **ADR-046**: Domain Module Refactoring -- established the bounded context structure replacing this module
- **ADR-047**: CQRS Pattern -- defines where orchestration logic should live
