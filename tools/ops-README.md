# Operations Automation

This directory contains automation scripts for repository operations, organized by functional domain.

## Directory Structure

```
ops/
├── orchestration/      # Agent task orchestration and workflow management
├── planning/           # Issue creation, work structure, and iteration metrics
├── dashboards/         # Metrics capture and dashboard generation
├── portability/        # Configuration conversion and validation
├── framework-core/     # Core framework utilities (context assembly, directives)
└── scripts/            # Legacy location (being phased out)
```

## Orchestration

**Location:** `ops/orchestration/`

Agent-based task orchestration system for managing multi-agent workflows.

### Key Modules

- `agent_orchestrator.py` - Main orchestration engine
- `agent_base.py` - Base class for agents
- `task_utils.py` - Task file reading/writing utilities
- `example_agent.py` - Example agent implementation
- `benchmark_orchestrator.py` - Performance benchmarking

### Documentation

See `ops/orchestration/README.md` for detailed usage and architecture.

### Related Tests

- `validation/test_agent_orchestrator.py` - Unit tests
- `validation/test_orchestration_e2e.py` - End-to-end tests
- `validation/test_task_utils.py` - Task utilities tests

## Planning

**Location:** `ops/planning/`

Issue creation, work structure initialization, and iteration metrics aggregation.

### Scripts

#### `create-issues-from-definitions.sh`

Data-driven issue creation engine supporting multiple tasksets.

**Usage:**
```bash
# List available tasksets
ops/planning/create-issues-from-definitions.sh --list-tasksets

# Preview issues (dry run)
ops/planning/create-issues-from-definitions.sh --taskset housekeeping --dry-run

# Create issues
export GH_TOKEN="your_token"
ops/planning/create-issues-from-definitions.sh --taskset housekeeping
```

#### `init-work-structure.sh`

Initialize work directory structure for new agents or projects.

#### `aggregate-iteration-metrics.py`

Analyze and aggregate metrics across multiple iterations.

**Usage:**
```bash
# Generate markdown report
ops/planning/aggregate-iteration-metrics.py

# Generate JSON output
ops/planning/aggregate-iteration-metrics.py --format json

# Save to file
ops/planning/aggregate-iteration-metrics.py --output work/metrics/trends.md
```

### GitHub Helpers

**Location:** `ops/planning/github-helpers/`

Low-level GitHub issue creation utilities used by the planning scripts.

### Documentation

See `ops/planning/README.md` for detailed documentation.

## Dashboards

**Location:** `ops/dashboards/`

Metrics capture and dashboard generation for observability and performance analysis.

### Scripts

#### `capture-metrics.py`

Extracts ADR-009 orchestration metrics from work logs and task YAML files.

**Usage:**
```bash
python3 ops/dashboards/capture-metrics.py [options]
```

**Options:**
- `--work-dir PATH` - Path to work directory (default: `work/`)
- `--output-format FMT` - Output format: `json` or `csv` (default: `json`)
- `--output-file PATH` - Output file path (default: stdout)
- `--include-logs` - Include metrics from work logs
- `--include-tasks` - Include metrics from task YAML files
- `--verbose` - Enable verbose logging

**Metrics Extracted:**
- Duration (minutes)
- Token usage (input/output/total)
- Context files loaded
- Artifacts created/modified
- Agent handoffs
- Per-artifact timing breakdowns

**Examples:**
```bash
# Extract to JSON
python3 ops/dashboards/capture-metrics.py --output-file metrics.json

# Extract to CSV
python3 ops/dashboards/capture-metrics.py --output-format csv --output-file metrics.csv

# Verbose mode
python3 ops/dashboards/capture-metrics.py --verbose
```

#### `generate-dashboard.py`

Generates markdown dashboard files from metrics data.

**Usage:**
```bash
python3 ops/dashboards/generate-dashboard.py [options]
```

**Options:**
- `--input PATH` - Input metrics JSON file
- `--dashboard-type TYPE` - Dashboard type: `summary`, `detail`, `trends`, or `all` (default: `all`)
- `--output-dir DIR` - Output directory (default: `work/reports/dashboards`)
- `--output-file PATH` - Output file (use `-` for stdout)
- `--update` - Update existing dashboards
- `--verbose` - Enable verbose logging

**Dashboard Types:**

1. **Summary** - Overall statistics, top agents, recent activity
2. **Detail** - Per-agent breakdowns, task completion, artifacts
3. **Trends** - Daily activity, timeline, token usage trends

**Examples:**
```bash
# Generate all dashboards
python3 ops/dashboards/generate-dashboard.py --input metrics.json

# Generate summary to stdout
python3 ops/dashboards/generate-dashboard.py --dashboard-type summary --output-file -

# Update existing dashboards
python3 ops/dashboards/generate-dashboard.py --update --verbose
```

### Test Scripts

- `test-capture-metrics.sh` - Validation tests for capture-metrics.py
- `test-generate-dashboard.sh` - Validation tests for generate-dashboard.py

### Documentation

- `METRICS_USAGE_EXAMPLES.md` - Detailed metrics usage examples
- `DASHBOARD_USAGE_EXAMPLES.md` - Dashboard generation examples

### Related

- ADR-009: `docs/architecture/adrs/ADR-009-orchestration-metrics-standard.md`

## Portability

**Location:** `ops/portability/`

Configuration conversion and validation for cross-platform agent portability.

### Scripts

#### `convert-agents-to-opencode.py`

Converts agent markdown files to OpenCode JSON format.

**Usage:**
```bash
python3 ops/portability/convert-agents-to-opencode.py [options]
```

**Options:**
- `-i, --input-dir PATH` - Agent files directory (default: `.github/agents`)
- `-o, --output PATH` - Output JSON file (default: `opencode-config.json`)
- `-v, --verbose` - Enable verbose logging
- `--validate` - Validate output using validator

**Examples:**
```bash
# Convert with default settings
python3 ops/portability/convert-agents-to-opencode.py

# Convert and validate
python3 ops/portability/convert-agents-to-opencode.py --validate --verbose

# Custom paths
python3 ops/portability/convert-agents-to-opencode.py \
  -i .github/agents \
  -o config/opencode.json \
  --validate
```

#### `opencode-spec-validator.py`

Validates JSON configuration files against OpenCode specification.

**Usage:**
```bash
python3 ops/portability/opencode-spec-validator.py <config-file.json>
```

**Options:**
- `-q, --quiet` - Suppress output, use exit codes only
- `--warnings-as-errors` - Treat warnings as validation errors

**Exit Codes:**
- `0` - Valid configuration
- `1` - Invalid configuration
- `2` - File error (not found, invalid JSON)

**Examples:**
```bash
# Validate configuration
python3 ops/portability/opencode-spec-validator.py opencode-config.json

# Quiet mode for CI/CD
python3 ops/portability/opencode-spec-validator.py -q config.json
echo $?  # Check exit code
```

### OpenCode Specification

The OpenCode format provides vendor-neutral agent configuration:

```json
{
  "version": "string",
  "agents": [
    {
      "name": "string",
      "description": "string", 
      "instructions": "string (markdown)",
      "tools": ["array"]
    }
  ],
  "metadata": {
    "source": "string",
    "generated": "ISO timestamp",
    "agent_count": 0
  }
}
```

### GitHub Actions Integration

Automated via `.github/workflows/reusable-config-mapping.yml`:
- Triggers on changes to `.github/agents/**`
- Runs conversion and validation
- Commits updated configuration

## Framework Core

**Location:** `ops/framework-core/`

Core framework utilities for agent context assembly and directive loading.

### Scripts

#### `assemble-agent-context.sh`

Emits agent context bundle to STDOUT for easy copy/paste into agent prompts.

**Usage:**
```bash
ops/framework-core/assemble-agent-context.sh [options]
```

**Options:**
- `--agent <name|path>` - Specialist profile (e.g., `backend-dev`)
- `--mode minimal|full` - Context depth (default: `minimal`)
- `--directives <codes>` - Space-separated directive codes (e.g., `001 006`)
- `--no-aliases` - Skip alias inclusion

**Examples:**
```bash
# Minimal context with directives
ops/framework-core/assemble-agent-context.sh \
  --agent backend-dev \
  --mode minimal \
  --directives 001 006

# Full context for high-stakes work
ops/framework-core/assemble-agent-context.sh \
  --agent backend-dev \
  --mode full
```

**Modes:**
- `minimal` - Runtime sheet + profile + aliases + specified directives
- `full` - Adds general and operational guidelines

**Tip:** Use `.github/agents/load_directives.sh --list` to see available directives.

#### `load_directives.sh`

On-demand loading of externalized directive markdown blocks.

**Usage:**
```bash
ops/framework-core/load_directives.sh [--list] <codes...>
```

**Examples:**
```bash
# List available directives
ops/framework-core/load_directives.sh --list

# Load specific directives
ops/framework-core/load_directives.sh 001 006

# Use in pipeline
source <(ops/framework-core/load_directives.sh 001 003)
```

#### `template-status-checker.sh`

Automate status reporting for run-iteration.md issue template.

**Usage:**
```bash
ops/framework-core/template-status-checker.sh [options]
```

**Options:**
- `--validate` - Check success criteria and output validation report
- `--format=json` - Output in JSON format
- `--help` - Show help message

## Development

### Requirements

- Python 3.8+
- Standard library (no external dependencies for core scripts)
- PyYAML for metrics and orchestration scripts

### Installation

```bash
# Install Python dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Code Style

All Python code follows the conventions in `docs/styleguides/python_conventions.md`:
- Black formatting (88 character line length)
- Ruff linting
- Type hints for public functions
- Quad-A test structure (Arrange, Assumption, Act, Assert)
- Guard clauses for validation

### Testing

Tests are located in `validation/` directory, organized by subdirectory:

```
validation/
├── test_agent_orchestrator.py     # Orchestration unit tests
├── test_orchestration_e2e.py      # Orchestration E2E tests
├── test_task_utils.py             # Task utilities tests
├── dashboards/                     # Dashboard script tests
├── portability/                    # Portability script tests
└── framework-core/                 # Framework core tests
```

Run tests:
```bash
# All tests
python3 -m pytest validation/ -v

# Specific module
python3 -m pytest validation/test_agent_orchestrator.py -v

# With coverage
python3 -m pytest validation/ --cov=ops --cov-report=term-missing
```

### Linting

```bash
# Format code
python3 -m black ops/

# Lint and auto-fix
python3 -m ruff check ops/ --fix

# Type checking (if configured)
python3 -m mypy ops/
```

## Migration Notes

The ops directory has been restructured from a flat `ops/scripts/` layout to a domain-organized structure. Old references have been updated in documentation.

### Path Changes

| Old Path | New Path |
|----------|----------|
| `ops/scripts/orchestration/` | `ops/orchestration/` |
| `ops/scripts/planning/` | `ops/planning/` |
| `ops/scripts/capture-metrics.py` | `ops/dashboards/capture-metrics.py` |
| `ops/scripts/generate-dashboard.py` | `ops/dashboards/generate-dashboard.py` |
| `ops/scripts/opencode-spec-validator.py` | `ops/portability/opencode-spec-validator.py` |
| `ops/scripts/convert-agents-to-opencode.py` | `ops/portability/convert-agents-to-opencode.py` |
| `ops/scripts/assemble-agent-context.sh` | `ops/framework-core/assemble-agent-context.sh` |
| `ops/scripts/load_directives.sh` | `ops/framework-core/load_directives.sh` |
| `ops/scripts/template-status-checker.sh` | `ops/framework-core/template-status-checker.sh` |

## Contributing

When adding new operations scripts:

1. Choose the appropriate directory based on function
2. Follow Python conventions (see `docs/styleguides/python_conventions.md`)
3. Write tests before implementation (TDD/ATDD)
4. Update this README with usage documentation
5. Add type hints and docstrings
6. Ensure scripts are idempotent and safe to re-run

## References

- Python Conventions: `docs/styleguides/python_conventions.md`
- Version Control Hygiene: `docs/styleguides/version_control_hygiene.md`
- ADR-009 Orchestration Metrics: `docs/architecture/adrs/ADR-009-orchestration-metrics-standard.md`
- Agent Orchestration: `ops/orchestration/README.md`
- Planning Scripts: `ops/planning/README.md`
