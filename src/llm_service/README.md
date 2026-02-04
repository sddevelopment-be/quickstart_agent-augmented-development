# LLM Service Layer

**Version:** 0.1.0  
**Status:** Milestone 1 Complete (Foundation)  
**Python:** 3.10+  
**Dependencies:** Pydantic v2, Click, PyYAML

## Overview

The LLM Service Layer is a configuration-driven routing system that intelligently directs agent requests to appropriate LLM tools based on cost optimization, agent preferences, and availability. It provides a unified CLI interface for agent-to-LLM interactions with automatic fallback handling.

### Key Features

✅ **Configuration-Driven** - YAML-based configuration for agents, tools, models, and policies  
✅ **Smart Routing** - Automatic tool and model selection based on agent preferences and task type  
✅ **Cost Optimization** - Routes simple tasks to cheaper models automatically  
✅ **Fallback Chains** - Graceful degradation when primary tools/models unavailable  
✅ **Validation** - Comprehensive schema and cross-reference validation with Pydantic v2  
✅ **CLI Interface** - User-friendly command-line interface with Click

---

## Architecture

```
src/llm_service/
├── __init__.py          # Public API exports
├── cli.py               # Command-line interface
├── routing.py           # Routing engine logic
└── config/
    ├── __init__.py      # Config exports
    ├── schemas.py       # Pydantic validation models
    └── loader.py        # YAML configuration loader
```

### Core Components

1. **Configuration Schemas** (`config/schemas.py`)
   - Pydantic v2 models for validation
   - Agents, Tools, Models, Policies
   - Cross-reference validation

2. **Configuration Loader** (`config/loader.py`)
   - YAML file loading (`.yaml` or `.yml`)
   - Schema validation
   - Cross-reference checking

3. **Routing Engine** (`routing.py`)
   - Agent-to-tool mapping
   - Model selection (preferences + task types)
   - Cost optimization logic
   - Fallback chain traversal

4. **CLI Interface** (`cli.py`)
   - `llm-service exec` - Execute agent requests
   - `llm-service config validate` - Validate configuration
   - `llm-service config init` - Initialize config directory
   - `llm-service version` - Display version info

---

## Installation

```bash
# Install package with dependencies
pip install -e .

# Or install dependencies manually
pip install pydantic>=2.0 click>=8.0 PyYAML>=6.0

# Development dependencies
pip install -r requirements-dev.txt
```

---

## Configuration

### Directory Structure

```
config/
├── agents.yaml    # Agent preferences and task mappings
├── tools.yaml     # LLM tool definitions (claude-code, codex, etc.)
├── models.yaml    # Model specifications and costs
└── policies.yaml  # Budget limits and optimization rules
```

### Example Configuration

**agents.yaml**
```yaml
agents:
  backend-dev:
    preferred_tool: claude-code
    preferred_model: claude-sonnet-20240229
    fallback_chain:
      - claude-code:claude-sonnet-20240229
      - codex:gpt-4
      - claude-code:claude-haiku-20240307
    task_types:
      coding: claude-sonnet-20240229
      debugging: gpt-4
      simple: claude-haiku-20240307
```

**tools.yaml**
```yaml
tools:
  claude-code:
    binary: claude
    command_template: "{binary} {prompt_file} --model {model} --output {output_file}"
    platforms:
      linux: /usr/local/bin/claude
      macos: /usr/local/bin/claude
      windows: /usr/bin/claude
    models:
      - claude-opus-20240229
      - claude-sonnet-20240229
      - claude-haiku-20240307
    capabilities:
      - code_generation
      - code_review
      - long_context
```

**models.yaml**
```yaml
models:
  claude-sonnet-20240229:
    provider: anthropic
    cost_per_1k_tokens:
      input: 0.003
      output: 0.015
    context_window: 200000
    task_suitability:
      - coding
      - long_documents
      - balanced_performance
```

**policies.yaml**
```yaml
policies:
  default:
    daily_budget_usd: 10.00
    monthly_budget_usd: 200.00
    limit:
      type: soft
      threshold_percent: 80
    auto_fallback_on_rate_limit: true
    log_prompts: false
    log_metadata: true

cost_optimization:
  simple_task_threshold_tokens: 1500
  simple_task_models:
    - claude-haiku-20240307
    - gpt-3.5-turbo
  complex_task_models:
    - gpt-4-turbo
    - claude-opus-20240229
```

---

## Usage

### CLI Commands

#### Validate Configuration
```bash
llm-service --config-dir ./config config validate
```

Output:
```
✓ Configuration is valid!

  Agents:   3 configured
  Tools:    3 configured
  Models:   7 configured
  Policies: 3 configured
```

#### Execute Agent Request
```bash
llm-service --config-dir ./config exec \
  --agent backend-dev \
  --prompt-file task.md \
  --task-type coding
```

#### Initialize Configuration
```bash
llm-service --config-dir ./myconfig config init
```

#### Display Version
```bash
llm-service version
```

### Python API

```python
from llm_service import load_configuration, RoutingEngine

# Load configuration
config = load_configuration('./config')

# Create routing engine
engine = RoutingEngine(
    config['agents'],
    config['tools'],
    config['models'],
    config['policies']
)

# Route agent request
decision = engine.route(
    agent_name='backend-dev',
    task_type='coding',
    prompt_size_tokens=2500
)

print(f"Tool: {decision.tool_name}")
print(f"Model: {decision.model_name}")
print(f"Reason: {decision.reason}")
print(f"Fallback used: {decision.fallback_used}")

# Get model cost information
cost = engine.get_model_cost('claude-sonnet-20240229')
print(f"Input cost: ${cost['input']}/1K tokens")
print(f"Output cost: ${cost['output']}/1K tokens")

# List agent capabilities
caps = engine.list_agent_capabilities('backend-dev')
print(f"Preferred tool: {caps['preferred_tool']}")
print(f"Task types: {caps['task_types']}")
```

---

## Routing Logic

### Decision Flow

1. **Agent Preferences** - Start with agent's `preferred_tool` and `preferred_model`
2. **Task Type Override** - Check if agent has specific model for task type
3. **Cost Optimization** - For small prompts (<1500 tokens), use cheaper model
4. **Tool Availability** - Verify tool exists, else use fallback chain
5. **Model Compatibility** - Ensure tool supports selected model
6. **Fallback Chain** - Try fallback options if primary unavailable

### Precedence Rules

1. Task-specific model override (highest)
2. Cost optimization (if enabled and threshold met)
3. Agent preferred model
4. Fallback chain (lowest)

### Example Routing

```python
# Agent: backend-dev
# Preferred: claude-code + claude-sonnet-20240229
# Task: "coding"
# Prompt: 1000 tokens

# Decision:
# 1. Task type "coding" → claude-sonnet-20240229 ✓
# 2. Prompt <1500 tokens → cost optimization triggers
# 3. Switch to claude-haiku-20240307 (cheaper) ✓
# 4. Verify claude-code supports haiku ✓
# → Route to: claude-code + claude-haiku-20240307
```

---

## Validation

### Schema Validation

All configuration files are validated with Pydantic v2:

- **Type checking** - Ensures correct data types
- **Required fields** - Validates all required fields present
- **Constraints** - Enforces value constraints (e.g., costs ≥0, context >0)
- **Format validation** - Checks fallback chain format (`tool:model`)

### Cross-Reference Validation

After loading, the system validates:

- Agent's `preferred_tool` exists in tools
- Agent's `preferred_model` exists in models
- Agent's `preferred_model` is supported by `preferred_tool` ✨ **NEW**
- All fallback chain tools exist
- All fallback chain models exist
- All task type models exist

### Error Examples

```
✗ Configuration validation failed!

Configuration cross-reference validation failed:
  - Agent 'backend-dev' references unknown tool: nonexistent-tool
  - Agent 'backend-dev' preferred_model 'gpt-4' is not supported by tool 'claude-code'
  - Agent 'planner' fallback references unknown model: invalid-model
```

---

## Testing

### Run Tests

```bash
# Run all tests
PYTHONPATH=src pytest tests/unit/ -v

# Run with coverage
PYTHONPATH=src coverage run -m pytest tests/unit/
coverage report --include="src/llm_service/*"

# Run specific test file
PYTHONPATH=src pytest tests/unit/config/test_schemas.py -v
```

### Test Coverage

**Current Coverage: 93%**

| Module | Coverage | Lines | Tests |
|--------|----------|-------|-------|
| `schemas.py` | 100% | 93 | 25 |
| `loader.py` | 93% | 81 | 19 |
| `routing.py` | 97% | 89 | 14 |
| `cli.py` | 83% | 104 | 7 |
| **TOTAL** | **93%** | **374** | **65** |

### Test Categories

- **Schema validation tests** (25) - Field validators, constraints, cross-references
- **Loader tests** (19) - YAML parsing, error handling, validation
- **Routing tests** (14) - Decision logic, fallbacks, cost optimization
- **CLI tests** (7) - Commands, error messages, output formatting

---

## Error Handling

### ConfigurationError

Raised when configuration loading/validation fails:

```python
from llm_service import load_configuration, ConfigurationError

try:
    config = load_configuration('./config')
except ConfigurationError as e:
    print(f"Configuration error: {e}")
    # Handle invalid configuration
```

### RoutingError

Raised when routing cannot determine valid tool/model:

```python
from llm_service import RoutingEngine, RoutingError

try:
    decision = engine.route('nonexistent-agent')
except RoutingError as e:
    print(f"Routing error: {e}")
    # Handle routing failure
```

---

## Development

### Code Style

- **Python 3.10+** with type hints
- **PEP 8** compliant
- **Pydantic v2** for validation
- **Click** for CLI
- **Docstrings** on all public APIs

### Adding a New Tool

1. Add tool definition to `config/tools.yaml`
2. Specify supported models
3. Define command template with placeholders: `{binary}`, `{prompt_file}`, `{model}`
4. Add platform-specific paths if needed
5. Validate configuration: `llm-service config validate`

### Adding a New Agent

1. Add agent to `config/agents.yaml`
2. Specify `preferred_tool` and `preferred_model`
3. Define fallback chain (optional)
4. Map task types to models (optional)
5. Ensure all references exist in tools.yaml and models.yaml

---

## Roadmap

### ✅ Milestone 1: Foundation (Complete)
- Configuration schema and validation
- CLI interface foundation
- Routing engine core
- Unit tests (>90% coverage)

### 🔄 Milestone 2: Tool Integration (Next)
- Tool adapter architecture
- Claude-Code adapter implementation
- Codex adapter implementation
- Generic YAML-based adapter
- Integration tests

### 📋 Milestone 3: Cost Optimization & Telemetry
- SQLite telemetry database
- Budget enforcement
- Usage tracking and reporting
- Stats command

### 📋 Milestone 4: End-to-End Integration
- Acceptance tests (Gherkin scenarios)
- Cross-platform testing
- Documentation finalization
- Packaging and distribution

---

## Contributing

### Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests with coverage
PYTHONPATH=src pytest tests/unit/ --cov=src/llm_service --cov-report=html

# Format code
black src/ tests/

# Lint code
ruff check src/ tests/
```

### Test-Driven Development

This project follows TDD principles:

1. **RED** - Write failing test
2. **GREEN** - Implement minimum code to pass
3. **REFACTOR** - Improve code quality

All new features must include tests.

---

## License

See LICENSE file in repository root.

---

## Support

For issues and questions:
- **Repository:** See `docs/architecture/design/llm-service-layer-prestudy.md`
- **Planning:** See `docs/planning/llm-service-layer-implementation-plan.md`
- **Tests:** See `tests/unit/` for usage examples

---

**Status:** Milestone 1 Complete ✅  
**Coverage:** 93% ✅  
**Tests:** 65 passing ✅  
**Next:** Milestone 2 - Tool Integration 🔄
