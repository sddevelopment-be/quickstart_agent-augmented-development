# src/ - Production Code

**Purpose:** Production code that powers the SDD Agentic Framework runtime.

## Directory Structure

```
src/
├── framework/           # Core framework runtime
│   ├── core/           # Task, Agent, Orchestrator abstractions
│   ├── execution/      # Task execution engine
│   ├── interface/      # Client interfaces (CLI, API)
│   ├── orchestration/  # Runtime orchestration (agent dispatch, task routing)
│   ├── context/        # Context assembly & directive loading
│   ├── config/         # Framework configuration (model routing)
│   └── schemas/        # Production JSON schemas (prompt validation)
└── llm_service/        # LLM dashboard web service
    ├── adapters/       # LLM provider adapters
    ├── config/         # Service configuration
    ├── dashboard/      # Dashboard implementation
    ├── telemetry/      # Telemetry collection
    └── ui/             # User interface
```

## What Belongs Here

**Production code** - code that runs in production or is imported by production systems:
- Core abstractions (Task, Agent, Orchestrator)
- Runtime execution logic (task dispatch, agent coordination)
- Framework interfaces (CLI, API, client libraries)
- Production schemas and configuration
- Service implementations (dashboards, APIs)

## What Does NOT Belong Here

- **Development tooling** → `tools/` (exporters, validators, release scripts)
- **Tests** → `tests/` (unit, integration, e2e)
- **Test fixtures** → `fixtures/` (example data, mock files)
- **Documentation** → `docs/` or `doctrine/docs/`
- **Operational scripts** → `tools/scripts/` (unless part of runtime)

## Key Principle

> **If it's imported by production code or runs in production, it belongs in `src/`.**  
> **If it's only used during development/testing/deployment, it belongs in `tools/`.**

## Examples

✅ **Belongs in src/**
- `src/framework/orchestration/agent_orchestrator.py` - Runtime agent dispatch
- `src/framework/context/load_directives.py` - Loads directives at runtime
- `.doctrine-config/model_router.yaml` - Production LLM routing config (template: `doctrine/templates/project/model_router.template.yaml`)
- `src/framework/schemas/prompt-schema.json` - Validates prompts at runtime

❌ **Does NOT belong in src/**
- Exporters for Copilot/Claude skill files → `tools/exporters/`
- Schema validators for CI → `tools/validators/`
- Release automation scripts → `tools/release/`
- Test fixtures → `fixtures/`

## Import Guidelines

Production code in `src/` may:
- Import from other `src/` modules
- Import from `doctrine/` (framework definitions)
- Import standard library and external dependencies

Production code should NOT:
- Import from `tools/` (creates circular dependencies)
- Import from `tests/` (wrong direction)
- Import from `fixtures/` (test data doesn't belong in production)

## Related Documentation

- Architecture decision: See refactoring proposal in session artifacts
- Framework documentation: `doctrine/docs/`
- Development tooling: `tools/README.md`
