# Multi-Tier Agentic Framework

Version: 0.1.0  
Status: Development / Scaffold

## Overview

Python implementation of the four-tier agentic runtime architecture defined in ADR-020 and ADR-021. This framework separates concerns across interface, orchestration, routing, and execution layers to enable portable, vendor-neutral agent workflows.

## Architecture

### Tier 0: Human Interface & Utilities (`interface/`)

User-facing entry points and convenience APIs:

- `framework_client.py`: `FrameworkClient` - High-level client for common operations
- `create_client.py`: `create_client()` - Factory function with auto-initialization

**Use cases:**
- Quick task execution
- Model listing and selection
- Interactive prototyping

### Tier 1: Orchestration & Governance (`core/`)

Core orchestration logic implementing AGENTS.md specification:

- `orchestrator.py`: `Orchestrator` - Task assignment, lifecycle management, agent coordination
- `task.py`: `Task` - Task descriptor with validation
- `agent_profile.py`: `AgentProfile` - Agent metadata and capabilities
- `task_status.py`: `TaskStatus` - Lifecycle state enumeration

**Use cases:**
- Agent profile loading and validation
- Task-to-agent assignment
- Status transitions and handoffs
- Directive context assembly

### Tier 2 & 3: Model Routing & Execution (`execution/`)

Multi-vendor model interfaces with routing and fallback:

- `model_router.py`: `ModelRouter` - Router-first selection per ADR-021
- `execution_client.py`: `ExecutionClient` - Base interface for model invocation
- `ollama_client.py`: `OllamaClient` - Local model execution (privacy, offline)
- `model_config.py`: `ModelConfig` - Model configuration dataclass
- `model_capabilities.py`: `ModelCapabilities` - Capability metadata
- `model_provider.py`: `ModelProvider` - Provider enumeration

**Use cases:**

- Cost-aware model selection
- Fallback chain execution
- Direct API calls (OpenAI, Anthropic)
- Local batch operations (Ollama)

## Installation

Framework is currently under development. To use:

```bash
# Add framework to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run tests
python -m pytest validation/test_framework_*.py -v
```

## Usage Examples

### Basic Client Usage

```python
from pathlib import Path
from framework.interface import create_client

# Create and initialize client
client = create_client(
    config_path=Path(".github/agents/config.yaml"),
    mode="analysis",
    auto_initialize=True
)

# Execute a task
result = client.execute_task(Path("work/inbox/task.yaml"))

# List available models
models = client.list_available_models()
```

### Orchestration

```python
from pathlib import Path
from framework.core import Orchestrator, Task, TaskStatus

# Initialize orchestrator
orchestrator = Orchestrator(
    agents_dir=Path(".github/agents"),
    work_dir=Path("work")
)

# Load agent profiles
orchestrator.load_agent_profiles()

# Create and assign task
task = Task(
    id="2025-11-30-example-task",
    title="Example Task",
    status=TaskStatus.INBOX,
    priority="high"
)

agent = orchestrator.assign_task(task)
print(f"Assigned to: {agent.name}")
```

### Model Selection

```python
from framework.execution import ModelRouter

# Initialize router
router = ModelRouter(config_path="ops/config/model_router.yaml")
router.load_config()

# Select model based on requirements
model = router.select_model(
    task_type="repo-refactor-safe",
    constraints={
        "context_window": 100000,
        "requires_tools": True,
        "cost_ceiling": 0.03
    }
)

print(f"Selected: {model.name} ({model.provider.value})")

# Get fallback chain
fallbacks = router.get_fallback_chain(model.id)
```

### Local Execution

```python
from framework.execution import OllamaClient

# Connect to local Ollama instance
client = OllamaClient(base_url="http://localhost:11434")

# Execute task locally
response = client.invoke(
    model_id="llama3:70b",
    prompt="Analyze this code structure...",
    temperature=0.7
)

print(response["content"])
```

## Development Status

Current phase: **Scaffold with test coverage**

### Implemented

- ✅ Module structure (interface, core, execution)
- ✅ Core data models and enums
- ✅ Type hints and docstrings
- ✅ Comprehensive test scaffolds (Quad-A pattern)
- ✅ Guard clause validation
- ✅ ADR-aligned architecture

### TODO

- [ ] Configuration loading (YAML parsing)
- [ ] Agent profile parser (markdown → AgentProfile)
- [ ] Directive loader and context assembly
- [ ] Task file I/O (read/write YAML)
- [ ] Model router config and selection logic
- [ ] Direct API clients (OpenAI, Anthropic)
- [ ] Ollama HTTP API integration
- [ ] Fallback chain execution
- [ ] Metrics collection (ADR-009)
- [ ] Integration tests

## Testing

Tests follow Quad-A pattern (Arrange, Assumption Check, Act, Assert) per Python conventions:

```bash
# Run all framework tests
python -m pytest validation/framework/ -v

# Run specific module tests
python -m pytest validation/framework/test_interface.py -v
python -m pytest validation/framework/test_core.py -v
python -m pytest validation/framework/test_execution.py -v

# With coverage
python -m pytest validation/framework/ --cov=framework --cov-report=term-missing
```

## Configuration

Framework expects configuration files at:

- `.github/agents/config.yaml` (main framework config)
- `ops/config/model_router.yaml` (router and model catalog)
- `ops/config/ollama_models.yaml` (local model definitions)
- `.github/agents/*.agent.md` (agent profiles)
- `.github/agents/directives/*.md` (directive files)

See `docs/architecture/assessments/platform_next_steps.md` for detailed setup.

## References

- [ADR-020: Multi-Tier Agentic Runtime](../docs/architecture/adrs/ADR-020-multi-tier-agentic-runtime.md)
- [ADR-021: Model Routing Strategy](../docs/architecture/adrs/ADR-021-model-routing-strategy.md)
- [ADR-002: OpenCode Portability](../docs/architecture/adrs/ADR-002-portability-enhancement-opencode.md)
- [ADR-009: Orchestration Metrics](../docs/architecture/adrs/ADR-009-orchestration-metrics-standard.md)
- [Python Conventions](../docs/styleguides/python_conventions.md)
- [Architectural Vision](../docs/architecture/architectural_vision.md)
- [Platform Next Steps](../docs/architecture/assessments/platform_next_steps.md)

## Contributing

Follow Python conventions defined in `docs/styleguides/python_conventions.md`:

- Use Black for formatting (`python -m black framework/`)
- Use Ruff for linting (`python -m ruff check framework/ --fix`)
- Write Quad-A tests with assumption checks
- Add type hints to all functions
- Document with docstrings (Google style)

---

Prepared by: DevOps Danny  
Mode: `/analysis-mode`  
Date: 2025-11-30
