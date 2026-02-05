# ADR-031: Template-Based Configuration Generation

**status**: Accepted  
**date**: 2026-02-05  
**author**: Architect Alphonso  
**approved-by**: Human-in-Charge

## Context

The current `llm-service` requires users to manually create YAML configuration files, which presents significant onboarding friction:

**Current State Problems:**

1. **High Barrier to Entry**
   - New users must understand YAML syntax
   - Must know all configuration options and their meanings
   - Must correctly structure tool definitions, model mappings, etc.
   - No validation until first execution attempt

2. **Time-Consuming Setup**
   - Average time to first execution: **~30 minutes**
   - Users must reference documentation repeatedly
   - Trial-and-error process to get configuration working

3. **Error-Prone Manual Configuration**
   - Typos in model names, tool paths, environment variables
   - Incorrect YAML indentation breaking parsing
   - Missing required fields discovered only at runtime

4. **Tool Management Requires Code Changes**
   - Adding new tools requires editing configuration files manually
   - No CLI commands for tool management
   - Risk of breaking existing configuration

**Example Manual Configuration:**
```yaml
# Users must create this from scratch
service:
  name: "my-llm-service"
  log_level: "INFO"
  
tools:
  claude-code:
    binary: "/usr/local/bin/claude"
    command_template: "{binary} --model {model} < {prompt_file}"
    models:
      - claude-3.5-sonnet
      - claude-3-opus
    env_vars:
      ANTHROPIC_API_KEY: "${ANTHROPIC_API_KEY}"
    platform:
      darwin: "/usr/local/bin/claude"
      linux: "/usr/bin/claude"
      windows: "C:\\Program Files\\Claude\\claude.exe"
```

**Comparative Analysis Finding:**

The [spec-kitty comparative analysis](../design/comparative_study/2026-02-05-spec-kitty-comparative-analysis.md) identified template-based configuration generation as a key usability feature:

- `spec-kitty init` generates agent-specific directories and commands
- Template system with variable substitution (`${VAR}`)
- Platform-specific path resolution
- Environment scanning for API keys

**User Feedback:**
- Human-in-Charge rated template-based configuration as ⭐⭐⭐⭐⭐ priority
- Target: **Reduce time to first execution from 30 minutes to 2 minutes**

## Decision

**We will implement a template-based configuration generation system with CLI commands for initialization and tool management.**

### Core Features

1. **`llm-service config init` Command**
   - Generate working configuration from predefined templates
   - Variable substitution (environment variables, user input)
   - Platform-specific path resolution
   - Environment scanning (detect API keys, find binaries)

2. **Multiple Template Types**
   - `quick-start` - Minimal setup with claude-code (default)
   - `claude-only` - Claude-focused configuration
   - `cost-optimized` - Multi-model with aggressive cost routing
   - `development` - Local testing with mock tools

3. **`llm-service tool` Commands**
   - `llm-service tool add <name>` - Add new tool to configuration
   - `llm-service tool remove <name>` - Remove tool from configuration
   - `llm-service tool list` - Display configured tools
   - `llm-service tool validate` - Validate tool configuration

4. **Environment Scanning**
   - Detect API keys in environment (`ANTHROPIC_API_KEY`, etc.)
   - Find tool binaries in PATH
   - Platform detection (Darwin/Linux/Windows)
   - Warn about missing dependencies

**Implementation Approach:**

```python
# Template structure
templates/
├── quick-start.yaml      # Minimal setup
├── claude-only.yaml      # Claude-focused
├── cost-optimized.yaml   # Multi-model
└── development.yaml      # Testing/dev

# CLI usage
$ llm-service config init --template quick-start
✅ Configuration generated: ~/.config/llm-service/config.yaml
✅ Tool definitions created: ~/.config/llm-service/tools.yaml
✅ API keys detected: ANTHROPIC_API_KEY ✓, OPENAI_API_KEY ✗

Next steps:
  1. Set missing API keys (OPENAI_API_KEY)
  2. Review configuration: llm-service config show
  3. Test execution: llm-service execute --prompt "Hello" --model auto
```

## Rationale

### Why Template-Based Generation?

**Strengths:**

1. **Dramatically Reduces Onboarding Time**
   - From **30 minutes** (manual) to **2 minutes** (template)
   - Working configuration out-of-the-box
   - Users can start executing immediately

2. **Eliminates Configuration Errors**
   - Templates are pre-validated
   - Correct YAML structure guaranteed
   - Model names, tool paths validated

3. **Guides Users Through Setup**
   - Environment scanning detects missing dependencies
   - Clear next-step instructions
   - Validation before first execution

4. **Enables Tool Ecosystem**
   - Community can contribute templates
   - Easy to add new tools (CLI commands)
   - No code changes required

5. **Platform-Agnostic**
   - Templates adapt to operating system
   - Path resolution handles Windows/Linux/macOS
   - Binary detection finds tools automatically

**Trade-offs Accepted:**

1. **Templates Must Be Maintained**
   - *Concern*: Templates can become outdated
   - *Mitigation*: CI/CD validates templates on every change
   - *Impact*: Low - templates are simple YAML files

2. **Variable Substitution Adds Complexity**
   - *Concern*: Template system introduces new syntax
   - *Mitigation*: Simple `${VAR}` syntax, well-documented
   - *Impact*: Low - users rarely edit templates directly

3. **Limited Customization in Generated Config**
   - *Concern*: Templates may not cover all use cases
   - *Mitigation*: Users can edit generated config manually
   - *Impact*: Low - templates cover 80% of use cases

### Why NOT Alternatives?

**Alternative 1: Interactive Wizard**

**Description:** Prompt users for each configuration option.

**Pros:**
- ✅ Fully customized configuration
- ✅ No template maintenance

**Cons:**
- ❌ Time-consuming (many prompts)
- ❌ Overwhelming for new users
- ❌ No working defaults

**Rejected Because:** Increases onboarding time instead of reducing it. Templates with sensible defaults are faster.

**Alternative 2: Copy-Paste Examples**

**Description:** Documentation provides example configurations to copy.

**Pros:**
- ✅ Simple to implement
- ✅ No tooling required

**Cons:**
- ❌ Still manual process
- ❌ Copy-paste errors common
- ❌ No environment-specific adaptation

**Rejected Because:** Doesn't solve the onboarding problem. Still requires manual editing.

**Alternative 3: Auto-Detection Only**

**Description:** Automatically detect all tools and generate config.

**Pros:**
- ✅ Zero user input
- ✅ Always correct paths

**Cons:**
- ❌ Unpredictable configuration
- ❌ May detect unwanted tools
- ❌ No control over model selection

**Rejected Because:** Too opinionated. Users need control over which tools are configured.

### Design Principles

1. **Convention Over Configuration**
   - Sensible defaults that work out-of-the-box
   - Users only configure what's necessary

2. **Progressive Enhancement**
   - Start with minimal template
   - Add complexity as needed
   - Advanced options available but not required

3. **Fail-Fast Validation**
   - Validate template syntax before writing files
   - Check for missing dependencies immediately
   - Clear error messages with resolution steps

4. **Platform Awareness**
   - Detect operating system
   - Use appropriate paths and conventions
   - Handle Windows/Linux/macOS differences

## Envisioned Consequences

### Positive Consequences

1. ✅ **Dramatically Faster Onboarding**
   - Time to first execution: **30 minutes → 2 minutes** (93% reduction)
   - Working configuration guaranteed
   - Users productive immediately

2. ✅ **Reduced Support Burden**
   - Fewer configuration errors
   - Self-service tool management
   - Clear validation feedback

3. ✅ **Improved User Experience**
   - Professional setup process
   - Matches expectations from modern CLIs
   - Confidence-building (setup just works)

4. ✅ **Enables Community Contributions**
   - Easy to add new tool templates
   - No code knowledge required
   - Template marketplace potential

5. ✅ **Better Tool Ecosystem**
   - Adding tools is simple (CLI command)
   - Removing tools is safe (preserves config)
   - Tool discovery (list available tools)

### Negative Consequences

1. ⚠️ **Template Maintenance Overhead**
   - Templates must stay current with config schema
   - *Mitigation*: CI/CD validates templates automatically
   - *Impact*: Low - simple YAML files

2. ⚠️ **Variable Substitution Edge Cases**
   - Complex environment variable patterns may fail
   - *Mitigation*: Clear documentation of supported syntax
   - *Impact*: Low - simple variables cover 95% of cases

3. ⚠️ **Tool Management State Complexity**
   - Config files can be edited manually and via CLI
   - *Mitigation*: CLI validates config before modifications
   - *Impact*: Medium - careful state management required

4. ⚠️ **Path Detection May Fail**
   - Binaries not in PATH won't be found
   - *Mitigation*: Provide manual path override option
   - *Impact*: Low - clear error messages guide user

### Risk Mitigation Strategies

**Template Validation:**
```python
# CI/CD pipeline validates templates
def test_template_validity():
    """Ensure all templates are valid YAML and pass schema."""
    for template in templates_dir.glob("*.yaml"):
        config = load_yaml(template)
        schema.validate(config)  # Pydantic validation
        assert config.service.name  # Required fields present
```

**Variable Substitution Safety:**
```python
# Only allow known environment variables
ALLOWED_VARS = {
    "USER", "HOME", "PATH",
    "ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY",
    "CLAUDE_CODE_PATH", "LOG_LEVEL"
}

def substitute_variables(template: str) -> str:
    """Safe variable substitution."""
    for var in extract_variables(template):
        if var not in ALLOWED_VARS:
            raise ValueError(f"Variable ${{{var}}} not allowed")
    return os.path.expandvars(template)
```

**Tool Management Atomicity:**
```python
# Atomic config updates with rollback
def add_tool(tool_config: ToolConfig):
    """Add tool with atomic write."""
    backup = config_file.read_text()
    try:
        config = load_config()
        config.tools[tool_config.name] = tool_config
        validate_config(config)  # Fail-fast
        write_config(config)
    except Exception as e:
        config_file.write_text(backup)  # Rollback
        raise
```

## Implementation Guidance

### Phase 1: Template System (2 hours)

**1. Template Directory Structure:**
```
src/llm_service/templates/
├── __init__.py
├── quick-start.yaml       # Default template
├── claude-only.yaml
├── cost-optimized.yaml
└── development.yaml
```

**2. Template Manager:**
```python
# src/llm_service/templates/manager.py

from pathlib import Path
from typing import Dict, Any
import os
import yaml

class TemplateManager:
    """Manages configuration templates."""
    
    def __init__(self):
        self.template_dir = Path(__file__).parent
    
    def list_templates(self) -> List[str]:
        """List available templates."""
        return [t.stem for t in self.template_dir.glob("*.yaml")]
    
    def load_template(self, name: str) -> str:
        """Load template file."""
        path = self.template_dir / f"{name}.yaml"
        if not path.exists():
            raise ValueError(f"Template '{name}' not found")
        return path.read_text()
    
    def substitute_variables(self, template: str) -> str:
        """Replace ${VAR} with environment variables."""
        # Safe substitution with allowed list
        result = template
        for var in self._extract_variables(template):
            if var in ALLOWED_VARS:
                value = os.getenv(var, "")
                result = result.replace(f"${{{var}}}", value)
        return result
    
    def generate_config(
        self, 
        template_name: str, 
        output_path: Path,
        overrides: Dict[str, Any] = None
    ) -> None:
        """Generate configuration from template."""
        # 1. Load template
        template = self.load_template(template_name)
        
        # 2. Substitute variables
        config_text = self.substitute_variables(template)
        
        # 3. Parse and validate
        config = yaml.safe_load(config_text)
        if overrides:
            config = self._apply_overrides(config, overrides)
        
        # 4. Validate with Pydantic
        from llm_service.config import ServiceConfig
        validated = ServiceConfig(**config)
        
        # 5. Write to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(yaml.dump(config, default_flow_style=False))
```

### Phase 2: CLI Commands (2 hours)

**1. Config Init Command:**
```python
# src/llm_service/cli/config.py

import click
from llm_service.templates import TemplateManager
from llm_service.ui.console import console
from rich.panel import Panel
from rich.table import Table

@click.group()
def config():
    """Configuration management commands."""
    pass

@config.command()
@click.option(
    "--template", 
    default="quick-start",
    help="Template to use (quick-start, claude-only, cost-optimized, development)"
)
@click.option(
    "--output",
    type=click.Path(),
    default=None,
    help="Output path (default: ~/.config/llm-service/config.yaml)"
)
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite existing configuration"
)
def init(template: str, output: str, force: bool):
    """Generate configuration from template."""
    
    manager = TemplateManager()
    output_path = Path(output) if output else get_default_config_path()
    
    # Check if config exists
    if output_path.exists() and not force:
        console.print(Panel(
            f"Configuration already exists: {output_path}\n"
            "Use --force to overwrite",
            title="⚠️  Configuration Exists",
            border_style="yellow"
        ))
        return 1
    
    # Generate config
    try:
        manager.generate_config(template, output_path)
        
        # Scan environment
        env_status = scan_environment()
        
        # Display results
        console.print(Panel.fit(
            f"[green]✅[/green] Configuration generated: {output_path}",
            title="Configuration Created",
            border_style="green"
        ))
        
        # Show environment status
        table = Table(title="Environment Status")
        table.add_column("Dependency", style="cyan")
        table.add_column("Status", style="magenta")
        
        for dep, status in env_status.items():
            symbol = "✅" if status else "❌"
            table.add_row(dep, f"{symbol} {'Found' if status else 'Missing'}")
        
        console.print(table)
        
        # Next steps
        console.print(Panel(
            "1. Set missing API keys\n"
            "2. Review: llm-service config show\n"
            "3. Test: llm-service execute --prompt 'Hello' --model auto",
            title="Next Steps",
            border_style="blue"
        ))
        
    except Exception as e:
        console.print(Panel(
            f"[red]Error:[/red] {str(e)}",
            title="❌ Configuration Failed",
            border_style="red"
        ))
        return 1

@config.command()
def templates():
    """List available templates."""
    manager = TemplateManager()
    
    table = Table(title="Available Templates")
    table.add_column("Template", style="cyan")
    table.add_column("Description", style="white")
    
    templates = {
        "quick-start": "Minimal setup with claude-code (recommended)",
        "claude-only": "Claude-focused configuration",
        "cost-optimized": "Multi-model with aggressive cost routing",
        "development": "Local testing with mock tools"
    }
    
    for name, desc in templates.items():
        table.add_row(name, desc)
    
    console.print(table)

@config.command()
def show():
    """Display current configuration."""
    config = load_config()
    
    # Display as formatted YAML with syntax highlighting
    from rich.syntax import Syntax
    yaml_text = yaml.dump(config.dict(), default_flow_style=False)
    syntax = Syntax(yaml_text, "yaml", theme="monokai", line_numbers=True)
    console.print(syntax)
```

**2. Tool Management Commands:**
```python
@click.group()
def tool():
    """Tool management commands."""
    pass

@tool.command()
@click.argument("name")
@click.option("--binary", required=True, help="Tool binary path or command")
@click.option("--models", required=True, help="Comma-separated list of models")
@click.option("--env", multiple=True, help="Environment variables (KEY=VALUE)")
def add(name: str, binary: str, models: str, env: List[str]):
    """Add a new tool to configuration."""
    
    # Parse inputs
    model_list = [m.strip() for m in models.split(",")]
    env_vars = dict(e.split("=") for e in env)
    
    # Create tool config
    tool_config = {
        "binary": binary,
        "command_template": "{binary} --model {model} < {prompt_file}",
        "models": model_list,
        "env_vars": env_vars
    }
    
    # Load existing config
    config = load_config()
    
    # Check if tool exists
    if name in config.tools and not click.confirm(f"Tool '{name}' exists. Overwrite?"):
        return 1
    
    # Add tool
    config.tools[name] = ToolConfig(**tool_config)
    
    # Validate
    try:
        validate_config(config)
    except Exception as e:
        console.print(Panel(
            f"[red]Validation Error:[/red] {str(e)}",
            title="❌ Invalid Configuration",
            border_style="red"
        ))
        return 1
    
    # Save
    save_config(config)
    
    console.print(Panel.fit(
        f"[green]✅[/green] Tool '{name}' added successfully",
        border_style="green"
    ))

@tool.command()
@click.argument("name")
def remove(name: str):
    """Remove a tool from configuration."""
    
    config = load_config()
    
    if name not in config.tools:
        console.print(f"[yellow]Tool '{name}' not found[/yellow]")
        return 1
    
    if not click.confirm(f"Remove tool '{name}'? This will delete its configuration."):
        return 0
    
    del config.tools[name]
    save_config(config)
    
    console.print(f"[green]✅ Tool '{name}' removed[/green]")

@tool.command()
def list():
    """List configured tools."""
    config = load_config()
    
    table = Table(title="Configured Tools")
    table.add_column("Tool", style="cyan")
    table.add_column("Models", style="magenta")
    table.add_column("Status", style="green")
    
    for name, tool_config in config.tools.items():
        models = ", ".join(tool_config.models)
        
        # Check if binary exists
        status = "✓" if check_binary_exists(tool_config.binary) else "✗"
        
        table.add_row(name, models, status)
    
    console.print(table)
```

### Phase 3: Environment Scanning (1-2 hours)

```python
# src/llm_service/utils/env_scanner.py

from pathlib import Path
import shutil
import os
from typing import Dict, Optional

class EnvironmentScanner:
    """Scan environment for dependencies."""
    
    def scan_api_keys(self) -> Dict[str, bool]:
        """Check for API keys in environment."""
        keys = {
            "ANTHROPIC_API_KEY": bool(os.getenv("ANTHROPIC_API_KEY")),
            "OPENAI_API_KEY": bool(os.getenv("OPENAI_API_KEY")),
            "GOOGLE_API_KEY": bool(os.getenv("GOOGLE_API_KEY")),
        }
        return keys
    
    def find_binary(self, name: str) -> Optional[Path]:
        """Find binary in PATH."""
        path = shutil.which(name)
        return Path(path) if path else None
    
    def detect_platform(self) -> str:
        """Detect operating system."""
        import platform
        system = platform.system().lower()
        return {
            "darwin": "darwin",
            "linux": "linux",
            "windows": "windows"
        }.get(system, "linux")
    
    def scan_all(self) -> Dict[str, Any]:
        """Complete environment scan."""
        return {
            "api_keys": self.scan_api_keys(),
            "binaries": {
                "claude": self.find_binary("claude"),
                "codex": self.find_binary("codex"),
            },
            "platform": self.detect_platform(),
        }
```

### Testing Strategy

**Template Validation Tests:**
```python
def test_all_templates_valid():
    """Ensure all templates pass validation."""
    manager = TemplateManager()
    for template_name in manager.list_templates():
        config_text = manager.load_template(template_name)
        config = yaml.safe_load(config_text)
        
        # Should validate without errors
        ServiceConfig(**config)

def test_variable_substitution():
    """Test variable substitution logic."""
    os.environ["TEST_VAR"] = "test_value"
    template = "key: ${TEST_VAR}"
    
    manager = TemplateManager()
    result = manager.substitute_variables(template)
    
    assert "test_value" in result
```

**CLI Command Tests:**
```python
def test_config_init_command():
    """Test config init CLI command."""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        result = runner.invoke(init, ["--template", "quick-start", "--output", "test-config.yaml"])
        
        assert result.exit_code == 0
        assert Path("test-config.yaml").exists()
        
        # Validate generated config
        config = yaml.safe_load(Path("test-config.yaml").read_text())
        ServiceConfig(**config)

def test_tool_add_command():
    """Test tool add CLI command."""
    runner = CliRunner()
    
    result = runner.invoke(
        add, 
        ["gemini", "--binary", "gemini-cli", "--models", "gemini-1.5-pro,gemini-1.5-flash"]
    )
    
    assert result.exit_code == 0
    
    # Verify tool was added
    config = load_config()
    assert "gemini" in config.tools
    assert len(config.tools["gemini"].models) == 2
```

## Usage Examples

### Example 1: Quick Start Setup

```bash
# New user initializes configuration
$ llm-service config init

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Configuration Created            ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ✅ Config: ~/.config/llm-service/config.yaml
└──────────────────────────────────┘

┌─────────────────────────────────┐
│ Environment Status              │
├──────────────────┬──────────────┤
│ ANTHROPIC_API_KEY│ ✅ Found     │
│ OPENAI_API_KEY   │ ❌ Missing   │
│ claude-code      │ ✅ Found     │
└──────────────────┴──────────────┘

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Next Steps                       ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1. Set missing API keys          │
│ 2. Review: llm-service config show
│ 3. Test: llm-service execute ... │
└──────────────────────────────────┘

# Total time: ~30 seconds (vs. 30 minutes manual)
```

### Example 2: List Available Templates

```bash
$ llm-service config templates

┌─────────────────────────────────────────────────────┐
│ Available Templates                                 │
├─────────────────┬───────────────────────────────────┤
│ quick-start     │ Minimal setup with claude-code    │
│ claude-only     │ Claude-focused configuration      │
│ cost-optimized  │ Multi-model with cost routing     │
│ development     │ Local testing with mock tools     │
└─────────────────┴───────────────────────────────────┘
```

### Example 3: Add New Tool

```bash
$ llm-service tool add gemini \
  --binary gemini-cli \
  --models "gemini-1.5-pro,gemini-1.5-flash" \
  --env GOOGLE_API_KEY=${GOOGLE_API_KEY}

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ✅ Tool 'gemini' added           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

### Example 4: List Configured Tools

```bash
$ llm-service tool list

┌─────────────────────────────────────────────────┐
│ Configured Tools                                │
├──────────────┬──────────────────────┬──────────┤
│ Tool         │ Models               │ Status   │
├──────────────┼──────────────────────┼──────────┤
│ claude-code  │ claude-3.5-sonnet, …│ ✓        │
│ gemini       │ gemini-1.5-pro, …   │ ✓        │
│ codex        │ gpt-4-turbo         │ ✗        │
└──────────────┴──────────────────────┴──────────┘
```

## Considered Alternatives

### Alternative 1: Interactive Wizard
**Rejected:** Increases setup time instead of reducing it.

### Alternative 2: Copy-Paste Examples
**Rejected:** Still requires manual editing; no environment adaptation.

### Alternative 3: Auto-Detection Only
**Rejected:** Too opinionated; users need control over configuration.

(See Rationale section for detailed analysis)

## References

**Related ADRs:**
- [ADR-025: LLM Service Layer](ADR-025-llm-service-layer.md) - Configuration schema
- [ADR-026: Pydantic V2 Validation](ADR-026-pydantic-v2-validation.md) - Config validation
- [ADR-030: Rich Terminal UI](ADR-030-rich-terminal-ui-cli-feedback.md) - CLI output

**Related Documents:**
- [spec-kitty Comparative Analysis](../design/comparative_study/2026-02-05-spec-kitty-comparative-analysis.md)
- [spec-kitty Inspired Enhancements](../design/spec-kitty-inspired-enhancements.md)

**External References:**
- [spec-kitty Template System](https://github.com/Priivacy-ai/spec-kitty) - Inspiration
- [Click Documentation](https://click.palletsprojects.com/) - CLI framework

---

**Status:** ✅ Accepted  
**Implementation Target:** Milestone 4, Phase 1 (Week 1)  
**Estimated Effort:** 4-6 hours  
**Dependencies:** ADR-030 (Rich CLI) for output formatting
