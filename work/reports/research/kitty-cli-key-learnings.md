# kitty-cli Key Learnings

**Date:** 2026-02-05  
**Researcher:** Researcher Ralph  
**Source:** Analysis of spec-kitty-cli v0.14.1

---

## Executive Summary

kitty-cli (spec-kitty-cli) provides:
- ✅ **MCP Integration Pattern** (declarative, passive)
- ✅ **CLI Design Patterns** (Rich output, StepTracker)
- ✅ **Config Management** (Single source of truth)
- ❌ **MCP Server Management** (Missing - opportunity for us)

---

## 1. MCP Integration: What We Learned

### Pattern: Mission-Based Tool Declarations

```yaml
# missions/software-dev/mission.yaml
mcp_tools:
  required: [filesystem, git]
  recommended: [code-search, test-runner]
  optional: [github, gitlab]
```

**Insight:** Three-tier system (required/recommended/optional) provides clear guidance.

### What kitty-cli Does

✅ Declares tool requirements per mission type
✅ Restricts tools based on workflow role (implementation vs. review)
✅ Documents expected capabilities

### What kitty-cli Does NOT Do

❌ Start/stop MCP servers
❌ Validate tool availability
❌ Configure MCP connections
❌ Health check servers

**Opportunity:** We can implement active MCP server management.

---

## 2. Commands Architecture

### Typer Framework

```python
app = typer.Typer(name="spec-kitty")

def register_commands(app: typer.Typer):
    app.command()(simple_command)
    app.add_typer(sub_app, name="group")
```

**Decision:** Stick with Click (already using), but adopt patterns:
- ✅ Centralized registration
- ✅ Rich console output
- ✅ StepTracker pattern

### StepTracker Pattern (HIGH PRIORITY)

```python
tracker = StepTracker()

tracker.add("validate", "Validating configuration")
# ... do work ...
tracker.complete("validate", "93 lines checked")

# On error:
tracker.error("validate", "Invalid agent reference")
```

**Value:** Clear progress visualization, error context, user confidence.

### Rich Console Output (HIGH PRIORITY)

```python
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Colored output
console.print("[green]✓[/green] Success!")

# Panels
console.print(Panel("Config validated", border_style="green"))

# Tables
table = Table(title="Agents")
table.add_column("ID", style="cyan")
table.add_row("claude", "✓")
console.print(table)
```

**Action:** Add `rich>=13.0.0` to requirements.txt in M3.

---

## 3. Configuration Management

### Single Source of Truth Pattern

```yaml
# .kittify/config.yaml
agents:
  available: [claude, gemini, codex]
  selection:
    strategy: preferred
    preferred_implementer: claude
```

**Principle (ADR-6):**
- Config file is authoritative
- Migrations update config (don't recreate)
- CLI commands respect config decisions

### Config Management Commands

```bash
$ spec-kitty agent config add qwen
$ spec-kitty agent config remove codex
$ spec-kitty agent config list
```

**Action:** Implement similar for M4:

```bash
$ llm-service config agents add research-agent --tool claude-code
$ llm-service config agents list
$ llm-service config agents remove research-agent
```

---

## 4. Agent System

### Invoker Protocol

```python
class AgentInvoker(Protocol):
    agent_id: str
    command: str
    uses_stdin: bool
    
    def is_installed(self) -> bool: ...
    def build_command(...) -> list[str]: ...
    def parse_output(...) -> InvocationResult: ...
```

**Comparison to Our Adapter:**

| kitty-cli | Our LLM Service |
|-----------|-----------------|
| Protocol-based | ABC-based |
| Requires code per agent | Generic YAML adapter |
| 12 agent classes | Single adapter |

**Advantage:** We have config-only extensibility (already ahead).

### Role-Based Tool Access

```python
# specify_cli/orchestrator/agents/claude.py
if role == "implementation":
    cmd.extend(["--allowedTools", "Read,Write,Edit,Bash"])
elif role == "review":
    cmd.extend(["--allowedTools", "Read,Grep"])  # Read-only
```

**Learning:** Restrict tool permissions based on task type.

**Action for M4:** Add role-based MCP tool allowlists.

---

## 5. Validation Framework

### Pre-Flight Validation

```python
# Before expensive operations
def validate_agent_config(agent_id):
    errors = []
    
    if agent_id not in config.agents:
        errors.append(f"Agent '{agent_id}' not configured")
    
    tool = config.tools[agent.preferred_tool]
    if not shutil.which(tool.binary):
        errors.append(f"Tool '{tool.binary}' not in PATH")
    
    return ValidationResult(valid=len(errors) == 0, errors=errors)
```

**Action for M3:** Implement similar validation before tool invocation.

### Cross-Reference Validation

```python
# Validate agent → tool → model references
for agent in config.agents:
    if agent.preferred_tool not in config.tools:
        errors.append(f"Unknown tool '{agent.preferred_tool}'")
    
    tool = config.tools[agent.preferred_tool]
    if agent.preferred_model not in tool.models:
        errors.append(f"Model not supported by tool")
```

**Action for M3:** Add to config loader.

---

## 6. What to Adopt

### HIGH PRIORITY (M3)

1. ✅ **Rich Console Output**
   - Add `rich` dependency
   - Replace `print()` with `console.print()`
   - Add colored success/error messages

2. ✅ **StepTracker Pattern**
   - Implement `src/llm_service/cli/step_tracker.py`
   - Use in `config init`, `config validate`

3. ✅ **MCP Tools Config (Passive)**
   - Add `mcp_tools` section to `tools.yaml`
   - Three tiers: required/recommended/optional
   - No server management yet

4. ✅ **Config Validation**
   - Pre-flight checks before operations
   - Cross-reference validation
   - Tool binary availability

### MEDIUM PRIORITY (M4)

5. ⭐ **Active MCP Server Management**
   - Start/stop servers automatically
   - Health checks
   - Connection validation
   - **This is where we improve on kitty-cli**

6. ✅ **Config Management Commands**
   - `config agents add/remove/list`
   - `config tools add/remove/list`
   - Single source of truth enforcement

7. ✅ **Template-Based Init**
   - `config init --template quickstart`
   - Pre-built configs for common scenarios

---

## 7. What NOT to Adopt

### ❌ Typer Framework

- We're already on Click
- Migration cost not justified
- Typer benefits (type hints) not critical for our use case
- **Decision:** Stay with Click, adopt patterns only

### ❌ Slash Command Generation

- kitty-cli generates `.claude/commands/`, `.gemini/commands/`, etc.
- We don't orchestrate multiple agents
- Not applicable to our architecture

### ❌ Git Worktree Orchestration

- kitty-cli manages isolated worktrees per work package
- We're tool execution layer, not workflow orchestration
- Different problem domain

---

## 8. Competitive Advantages

### Where We're Already Ahead

✅ **Config-Only Extensibility**
- kitty-cli requires Python class per agent
- We use generic YAML adapter
- Add tools without code changes

✅ **Cost Optimization**
- kitty-cli doesn't address costs
- We have model selection, budget limits, telemetry

✅ **Runtime Routing**
- kitty-cli is static setup
- We make dynamic routing decisions

### Where We Can Improve on kitty-cli

⭐ **Active MCP Server Management**
- kitty-cli: passive declarations
- Us (M4): start/stop/health/validation

⭐ **Tool Discovery**
- kitty-cli: static config
- Us (M4): dynamic runtime discovery

⭐ **Validation**
- kitty-cli: no tool availability checks
- Us (M3): pre-flight validation

---

## 9. Implementation Checklist

### M3 (Immediate)

- [ ] Add `rich>=13.0.0` to `requirements.txt`
- [ ] Implement `src/llm_service/cli/step_tracker.py`
- [ ] Add MCP tools section to `tools.yaml` schema
- [ ] Implement config validation with cross-refs
- [ ] Add tool binary availability checks
- [ ] Replace key `print()` calls with `console.print()`

### M4 (Telemetry Phase)

- [ ] Implement MCP server lifecycle manager
- [ ] Add `config agents add/remove/list` commands
- [ ] Add `config tools add/remove/list` commands
- [ ] Implement dynamic MCP tool discovery
- [ ] Add template-based config initialization
- [ ] Implement role-based tool restrictions

---

## 10. Code Examples for Integration

### StepTracker Implementation

```python
# src/llm_service/cli/step_tracker.py
from rich.console import Console

class StepTracker:
    def __init__(self):
        self.console = Console()
        self.steps = {}
    
    def add(self, key: str, description: str):
        self.steps[key] = {"status": "running", "desc": description}
        self.console.print(f"[cyan]⋯[/cyan] {description}")
    
    def complete(self, key: str, detail: str = ""):
        self.steps[key]["status"] = "complete"
        desc = self.steps[key]["desc"]
        self.console.print(f"[green]✓[/green] {desc} {detail}")
    
    def error(self, key: str, error_msg: str):
        self.steps[key]["status"] = "error"
        desc = self.steps[key]["desc"]
        self.console.print(f"[red]✗[/red] {desc}: {error_msg}")
```

### Usage Example

```python
@click.command()
def init():
    """Initialize LLM Service configuration."""
    tracker = StepTracker()
    
    tracker.add("schema", "Creating configuration schema")
    create_config_dirs()
    tracker.complete("schema", "4 files created")
    
    tracker.add("validate", "Validating defaults")
    try:
        validate_config()
        tracker.complete("validate", "All checks passed")
    except ValidationError as e:
        tracker.error("validate", str(e))
        raise
```

### MCP Tools Config Extension

```yaml
# config/tools.yaml (NEW mcp_tools section)
tools:
  claude-code:
    binary: claude
    command_template: "{binary} {prompt_file} --model {model}"
    models: [claude-opus-20240229, claude-sonnet-20240229]
    
    # NEW: MCP tool requirements
    mcp_tools:
      required: [filesystem, git]
      recommended: [code-search]
      optional: [github]
    
    # NEW: MCP server connections (M4)
    mcp_servers:
      filesystem:
        package: "@modelcontextprotocol/server-filesystem"
        command: "npx -y @modelcontextprotocol/server-filesystem /allowed/path"
        auto_start: true
      git:
        package: "@modelcontextprotocol/server-git"
        command: "npx -y @modelcontextprotocol/server-git"
        auto_start: true
```

---

## 11. Risk Mitigation

### Rich Library Concerns

**Risk:** Breaks in headless/CI environments

**Mitigation:**

```python
from rich.console import Console

console = Console()

# Auto-detects TTY, falls back to plain output
console.print("[green]Success[/green]")  # Green in TTY, plain in CI
```

### Typer Temptation

**Risk:** Team wants to switch to Typer after seeing kitty-cli

**Mitigation:**
- Document decision to stay with Click
- Show Click can achieve same results with patterns
- Highlight migration cost vs. benefit

### Over-Engineering Config

**Risk:** Adding 38 migrations like kitty-cli

**Mitigation:**
- Keep config schema stable
- Version config files (schema_version field)
- Only add migrations for breaking changes

---

## 12. References

- **kitty-cli Package:** spec-kitty-cli v0.14.1 on PyPI
- **GitHub:** https://github.com/Priivacy-ai/spec-kitty
- **Previous Analysis:** docs/architecture/design/comparative_study/2026-02-05-spec-kitty-comparative-analysis.md
- **This Analysis:** work/reports/research/2026-02-05-kitty-cli-architecture-analysis.md

---

**Document Status:** COMPLETE ✅  
**Action Items:** 6 for M3, 6 for M4  
**Confidence:** HIGH (primary source code analyzed)
