# ADR-030: Rich Terminal UI for CLI Feedback

**status**: Accepted  
**date**: 2026-02-05  
**author**: Architect Alphonso  
**approved-by**: Human-in-Charge

## Context

The current `llm-service` CLI outputs plain text to the console, which presents several usability challenges:

**Current State Problems:**
1. **Poor Visual Hierarchy** - All text appears the same, making it hard to distinguish important information
2. **Difficult to Parse** - No structure or color coding for errors, warnings, success messages
3. **No Progress Indication** - Long-running operations provide no feedback until completion
4. **Unprofessional Appearance** - Plain text output lacks polish compared to modern CLI tools
5. **Debugging Difficulty** - Output from multiple components intermixed without clear boundaries

**Example Current Output:**
```
Executing LLM tool: claude-code
Model: claude-3.5-sonnet
Prompt file: /tmp/prompt.txt
Running command...
Output: [long raw text]
Tokens used: 1523
Cost: $0.0234
Done.
```

**Comparative Analysis Finding:**

The [spec-kitty comparative analysis](../design/comparative_study/2026-02-05-spec-kitty-comparative-analysis.md) identified extensive use of the `rich` Python library for terminal UI as a key differentiator. spec-kitty leverages:
- Colored panels for structured output
- Progress bars for long operations
- Tables for structured data
- Syntax highlighting for code/YAML
- Status indicators (✅ ✗ ⚠️)

**User Feedback:**
- Human-in-Charge rated dashboard interface (which includes rich terminal feedback) as ⭐⭐⭐⭐⭐ priority
- Spec-kitty's CLI experience was noted as "professional and easy to follow"

## Decision

**We will integrate the `rich` Python library to provide structured, colorful, and easy-to-parse CLI output.**

All CLI commands in `llm-service` will be enhanced with:
1. **Panels** - Structured information grouped in bordered boxes
2. **Progress Bars** - Real-time progress for long operations
3. **Tables** - Structured data (models, tools, metrics)
4. **Syntax Highlighting** - YAML, JSON, and code output
5. **Status Indicators** - Visual symbols for success/error/warning states
6. **Colors** - Semantic color coding (green=success, red=error, yellow=warning)

**Implementation Approach:**
```python
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress

console = Console()

# Example usage in CLI command
def execute_command():
    console.print(Panel.fit(
        "LLM Service Execution",
        subtitle="claude-code"
    ))
    
    with Progress() as progress:
        task = progress.add_task("Executing...", total=100)
        # ... operation ...
        progress.update(task, completed=100)
    
    table = Table(title="Execution Metrics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_row("Tokens", "1,523")
    table.add_row("Cost", "$0.0234")
    console.print(table)
```

## Rationale

### Why `rich` Library?

**Strengths:**

1. **Battle-Tested**
   - Used extensively in production by popular tools (pip, httpie, etc.)
   - spec-kitty demonstrates effective patterns we can adapt
   - Stable API, actively maintained

2. **Comprehensive Feature Set**
   - Panels, tables, progress bars, syntax highlighting
   - Markdown rendering, tree structures, columns
   - Covers all our use cases in single library

3. **Zero Learning Curve**
   - Intuitive API: `console.print()` replaces `print()`
   - Extensive documentation and examples
   - Similar to standard library conventions

4. **Automatic Fallback**
   - Detects non-TTY environments (CI/CD, redirected output)
   - Automatically degrades to plain text
   - No special handling required

5. **No Dependencies**
   - Pure Python implementation
   - No C extensions or platform-specific code
   - Works on all platforms (Windows, Linux, macOS)

6. **Performance**
   - Minimal overhead (< 10ms per render)
   - Efficient rendering engine
   - Suitable for interactive commands

**Trade-offs Accepted:**

1. **Additional Dependency**
   - *Mitigation*: `rich` is widely used, well-maintained, pure Python
   - *Impact*: Minimal - adds ~500KB to distribution

2. **Non-TTY Compatibility**
   - *Concern*: Output looks different when piped or in CI
   - *Mitigation*: `rich` auto-detects and falls back to plain text
   - *Impact*: None - graceful degradation

3. **Potential Complexity**
   - *Concern*: Overuse could make output cluttered
   - *Mitigation*: Design guidelines for consistent usage
   - *Impact*: Low - proper design prevents this

### Why NOT Alternatives?

**Alternative 1: `colorama`**
- ✅ Lightweight (basic color support)
- ❌ No structured output (panels, tables)
- ❌ No progress bars
- ❌ No syntax highlighting
- **Rejected:** Too basic for our needs

**Alternative 2: `termcolor`**
- ✅ Simple color API
- ❌ Similar limitations to colorama
- ❌ Less actively maintained
- **Rejected:** Insufficient features

**Alternative 3: `blessed`**
- ✅ Powerful terminal control
- ✅ Full-screen TUI support
- ❌ Overkill for simple CLI feedback
- ❌ Steeper learning curve
- ❌ Requires full-screen mode (not suitable for CLI commands)
- **Rejected:** Too complex, wrong abstraction level

**Alternative 4: Custom Implementation**
- ✅ Full control over output
- ✅ No dependencies
- ❌ Weeks of development time
- ❌ Reinventing the wheel
- ❌ Maintenance burden
- **Rejected:** Not worth the effort

### Design Guidelines for Rich Usage

To maintain consistency and avoid cluttered output:

**DO:**
- ✅ Use panels for logical groupings (execution summary, metrics)
- ✅ Use progress bars for operations > 2 seconds
- ✅ Use tables for structured data (≥ 3 rows)
- ✅ Use syntax highlighting for code/config output
- ✅ Use status symbols (✅ ✗ ⚠️) for quick scanning

**DON'T:**
- ❌ Nest panels more than 2 levels deep
- ❌ Use colors without semantic meaning
- ❌ Overuse panels for single-line output
- ❌ Mix multiple UI styles in same command
- ❌ Disable fallback to plain text

## Envisioned Consequences

### Positive Consequences

1. ✅ **Dramatically Improved Usability**
   - Users can quickly identify important information
   - Visual hierarchy guides attention
   - Errors stand out immediately

2. ✅ **Professional Appearance**
   - CLI looks modern and polished
   - Matches quality of commercial tools
   - Enhances project credibility

3. ✅ **Better Debugging Experience**
   - Structured output makes logs easier to parse
   - Clear separation between components
   - Progress indicators reduce user confusion

4. ✅ **Reduced Support Burden**
   - Visual feedback answers common questions ("Is it working?")
   - Status indicators clarify success/failure
   - Users less likely to interrupt operations

5. ✅ **Consistent User Experience**
   - All commands follow same visual patterns
   - Predictable output structure
   - Easier to document and teach

### Negative Consequences

1. ⚠️ **Dependency Addition**
   - Adds `rich` to requirements
   - *Mitigation*: Widely used, stable library
   - *Impact*: Minimal (< 1MB installed size)

2. ⚠️ **Output Differs in CI/CD**
   - Automated environments get plain text
   - *Mitigation*: Automatic fallback works transparently
   - *Impact*: None - plain text is appropriate for logs

3. ⚠️ **Learning Curve for Contributors**
   - Developers must learn `rich` API
   - *Mitigation*: Simple API, good documentation
   - *Impact*: Low (< 1 hour to learn basics)

4. ⚠️ **Potential for Overuse**
   - Risk of cluttered, over-designed output
   - *Mitigation*: Design guidelines enforced in code reviews
   - *Impact*: Low - guidelines prevent this

### Risk Mitigation Strategies

**Non-TTY Compatibility:**
```python
# Rich auto-detects, but we can force modes if needed
console = Console(force_terminal=True)   # Force TTY mode
console = Console(force_terminal=False)  # Force plain text
console = Console()                      # Auto-detect (default)
```

**Graceful Degradation:**
```python
# Always works, even if Rich fails to import
try:
    from rich.console import Console
    console = Console()
except ImportError:
    class FallbackConsole:
        def print(self, *args, **kwargs):
            print(*args)
    console = FallbackConsole()
```

**Color Disable Flag:**
```bash
# Users can disable colors if needed
llm-service execute --no-color
# Or via environment variable
NO_COLOR=1 llm-service execute
```

## Implementation Guidance

### Phase 1: Core Integration (2 hours)

**1. Add Dependency:**
```bash
# pyproject.toml or requirements.txt
rich>=13.0.0
```

**2. Create Console Wrapper:**
```python
# src/llm_service/ui/console.py

from rich.console import Console as RichConsole
from typing import Optional

_console: Optional[RichConsole] = None

def get_console() -> RichConsole:
    """Get singleton console instance."""
    global _console
    if _console is None:
        _console = RichConsole()
    return _console

# Convenience exports
console = get_console()
print = console.print
```

**3. Update CLI Commands:**
```python
# src/llm_service/cli/execute.py

from llm_service.ui.console import console
from rich.panel import Panel
from rich.table import Table

@click.command()
def execute(prompt: str, model: str):
    """Execute LLM tool with rich output."""
    
    # Header panel
    console.print(Panel.fit(
        "[bold cyan]LLM Service Execution[/bold cyan]",
        border_style="blue"
    ))
    
    # Execution logic...
    result = run_execution(prompt, model)
    
    # Results table
    table = Table(title="Execution Metrics", show_header=True)
    table.add_column("Metric", style="cyan", width=15)
    table.add_column("Value", style="magenta")
    table.add_row("Tool", result.tool)
    table.add_row("Model", result.model)
    table.add_row("Tokens", f"{result.tokens:,}")
    table.add_row("Cost", f"${result.cost:.4f}")
    table.add_row("Duration", f"{result.duration:.2f}s")
    
    console.print(table)
    
    # Output panel with syntax highlighting
    console.print(Panel(
        result.output,
        title="Output",
        border_style="green"
    ))
```

### Phase 2: Progress Indicators (1 hour)

```python
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn

def long_running_operation():
    """Example with progress bar."""
    with Progress(
        SpinnerColumn(),
        *Progress.get_default_columns(),
        TimeElapsedColumn(),
    ) as progress:
        
        task1 = progress.add_task("[cyan]Loading configuration...", total=100)
        # ... operation ...
        progress.update(task1, completed=100)
        
        task2 = progress.add_task("[cyan]Executing tool...", total=100)
        # ... operation ...
        progress.update(task2, completed=100)
```

### Phase 3: Error Handling (30 minutes)

```python
from rich.panel import Panel

def handle_error(error: Exception):
    """Display errors with rich formatting."""
    console.print(Panel(
        f"[bold red]Error:[/bold red] {str(error)}\n\n"
        f"[dim]{error.__class__.__name__}[/dim]",
        title="❌ Execution Failed",
        border_style="red"
    ))
```

### Testing Strategy

**Unit Tests:**
```python
def test_console_output():
    """Test rich output generation."""
    from rich.console import Console
    from io import StringIO
    
    buffer = StringIO()
    console = Console(file=buffer, width=80)
    
    console.print("[green]Success[/green]")
    output = buffer.getvalue()
    
    assert "Success" in output
```

**Integration Tests:**
```python
def test_cli_with_rich():
    """Test CLI command output."""
    result = runner.invoke(execute, ["--prompt", "test"])
    
    assert result.exit_code == 0
    assert "Execution Metrics" in result.output
    assert "✅" in result.output or "Success" in result.output
```

**Visual Tests (Manual):**
```bash
# Test in TTY mode
llm-service execute --prompt "test"

# Test in non-TTY mode (should fallback)
llm-service execute --prompt "test" | cat

# Test color disable
NO_COLOR=1 llm-service execute --prompt "test"
```

## Usage Examples

### Example 1: Basic Execution

**Before (Plain Text):**
```
Executing claude-code with model claude-3.5-sonnet
Output: Hello! How can I help you today?
Tokens: 15
Cost: $0.0012
```

**After (Rich):**
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  LLM Service Execution             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌────────────────────────────────────┐
│ Execution Metrics                  │
├───────────┬────────────────────────┤
│ Tool      │ claude-code            │
│ Model     │ claude-3.5-sonnet      │
│ Tokens    │ 15                     │
│ Cost      │ $0.0012                │
│ Duration  │ 1.2s                   │
└───────────┴────────────────────────┘

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Output                             ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Hello! How can I help you today?   │
└────────────────────────────────────┘
```

### Example 2: Error Display

**Before:**
```
Error: Model 'gpt-5' not found in configuration
```

**After:**
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ❌ Execution Failed                     ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Error: Model 'gpt-5' not found          │
│                                         │
│ Available models:                       │
│   - claude-3.5-sonnet                   │
│   - claude-3-opus                       │
│   - gpt-4-turbo                         │
│                                         │
│ ValidationError                         │
└─────────────────────────────────────────┘
```

### Example 3: Progress Indication

```
Setting up telemetry
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:05

┌────────────────────────────────────────────┐
│ ✅ Installing dependencies        Complete │
│ ✅ Configuring environment        Complete │
│ ⏳ Running validation            In progress│
└────────────────────────────────────────────┘
```

## Considered Alternatives

### Alternative 1: colorama

**Description:** Basic cross-platform colored terminal text.

**Pros:**
- ✅ Lightweight (~50KB)
- ✅ Simple API
- ✅ Cross-platform

**Cons:**
- ❌ No structured output (panels, tables)
- ❌ No progress bars
- ❌ No syntax highlighting
- ❌ Manual layout management

**Rejected Because:** Insufficient features for modern CLI UX. Would need additional libraries for progress bars and structured output.

### Alternative 2: blessed

**Description:** Powerful full-screen terminal interface library.

**Pros:**
- ✅ Full terminal control
- ✅ TUI capabilities (full-screen apps)
- ✅ Event handling

**Cons:**
- ❌ Overkill for CLI feedback
- ❌ Requires full-screen mode
- ❌ Steeper learning curve
- ❌ More complex error handling

**Rejected Because:** Wrong abstraction level. We need CLI enhancements, not TUI framework.

### Alternative 3: Custom Implementation

**Description:** Build our own colored output system.

**Pros:**
- ✅ Full control
- ✅ No dependencies
- ✅ Exactly what we need

**Cons:**
- ❌ 2-3 weeks development time
- ❌ Ongoing maintenance burden
- ❌ Reinventing the wheel
- ❌ Less battle-tested

**Rejected Because:** Not cost-effective. `rich` provides everything we need with better quality than we could build in reasonable time.

## Validation from kitty-cli Research

**Research Confirmation:** The [kitty-cli architecture analysis](../../../work/reports/research/2026-02-05-kitty-cli-architecture-analysis.md) by Researcher Ralph (2026-02-05) provides **HIGH-confidence validation** of this decision.

**Evidence from Production Usage:**
- ✅ kitty-cli uses Rich library extensively across 17 command modules (6,327 LOC)
- ✅ Consistent patterns: panels for structured output, tables for data, progress bars
- ✅ Professional terminal UX matches modern tools (pip, httpie)
- ✅ Automatic TTY detection and plain-text fallback confirmed working in production

**Implementation Patterns from kitty-cli:**
```python
# Panel usage for execution results
console.print(Panel.fit(
    "[bold cyan]Execution Complete[/bold cyan]",
    subtitle=f"Agent: {agent_name}",
    border_style="green"
))

# Table usage for structured metrics
table = Table(title="Execution Metrics")
table.add_column("Metric", style="cyan")
table.add_column("Value", style="magenta")
table.add_row("Tokens", f"{tokens:,}")
table.add_row("Cost", f"${cost:.4f}")
console.print(table)

# Progress bars for long operations
with Progress() as progress:
    task = progress.add_task("[cyan]Processing...", total=100)
    # ... operation ...
    progress.update(task, completed=100)
```

**Confidence Boost:** This ADR's technical decisions are validated by real-world production usage in kitty-cli, reducing implementation risk.

## References

**Related ADRs:**
- [ADR-027: Click CLI Framework](ADR-027-click-cli-framework.md) - CLI structure
- [ADR-032: Real-Time Execution Dashboard](ADR-032-real-time-execution-dashboard.md) - Dashboard UI
- [ADR-033: Step Tracker Pattern](ADR-033-step-tracker-pattern.md) - Progress tracking
- [ADR-034: MCP Server Integration](ADR-034-mcp-server-integration-strategy.md) - MCP CLI output

**Related Documents:**
- [Architecture Impact Analysis](../../../work/reports/architecture/2026-02-05-kitty-cli-architecture-impact-analysis.md) - Research validation
- [kitty-cli Architecture Analysis](../../../work/reports/research/2026-02-05-kitty-cli-architecture-analysis.md) - Detailed findings
- [spec-kitty Comparative Analysis](../design/comparative_study/2026-02-05-spec-kitty-comparative-analysis.md)
- [spec-kitty Inspired Enhancements](../design/spec-kitty-inspired-enhancements.md) - Overall architecture

**External References:**
- [Rich Library Documentation](https://rich.readthedocs.io/)
- [Rich GitHub Repository](https://github.com/Textualize/rich)
- [spec-kitty Repository](https://github.com/Priivacy-ai/spec-kitty) - Production usage examples

---

**Status:** ✅ Accepted & Implemented (Validated by kitty-cli production usage)  
**Implementation Status:** Completed in Milestone 4, Phase 1 (originally targeted for Milestone 3, Phase 1)  
**Actual Effort:** 2.5 hours (within 2-3h estimate)  
**Dependencies:** None (foundational)
