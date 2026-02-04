# ADR-027: Use Click for CLI Framework

**status**: Accepted  
**date**: 2026-02-04

## Context

The LLM Service Layer requires a command-line interface (CLI) to provide user interaction for:

1. **Configuration Management**: Validate and initialize configuration files
2. **Agent Execution**: Execute agent requests with LLM tool routing (`llm-service exec`)
3. **Utility Commands**: Display version information and help text
4. **Developer Experience**: Provide clear help text, error messages, and argument validation

During Milestone 1 implementation (2026-02-04), the team needed to select a CLI framework. The interface must support:
- Hierarchical command structure (e.g., `llm-service config validate`)
- Context sharing between commands (e.g., `--config-dir` global option)
- Comprehensive testing without requiring subprocess execution
- Clear error handling and user-friendly output

**Key Forces:**
- Need for professional CLI with subcommands and option parsing
- Requirement for testability (unit tests without subprocess overhead)
- Desire for minimal boilerplate and clean code
- Balance between type safety and development speed
- Team familiarity with Python CLI patterns

**Reference Documentation:**
- Implementation: `src/llm_service/cli.py`
- Technical Prestudy: `docs/architecture/design/llm-service-layer-prestudy.md`
- Implementation Plan: `docs/planning/llm-service-layer-implementation-plan.md`

## Decision

**We will use Click for the CLI framework in the LLM Service Layer.**

Click will be used to:
1. Define command hierarchy using decorators (`@click.group()`, `@click.command()`)
2. Parse command-line arguments and options with type validation
3. Share context between commands using `@click.pass_context`
4. Provide comprehensive testing via `CliRunner` fixture

**Key Implementation Pattern:**

```python
import click

@click.group()
@click.option('--config-dir', type=click.Path(...), default='./config')
@click.pass_context
def cli(ctx, config_dir):
    """LLM Service Layer - Configuration-driven agent-to-LLM routing."""
    ctx.ensure_object(dict)
    ctx.obj['config_dir'] = config_dir

@cli.command(name='exec')
@click.option('--agent', required=True, help='Agent name')
@click.option('--prompt-file', type=click.Path(exists=True), required=True)
@click.pass_context
def exec_command(ctx, agent, prompt_file):
    """Execute agent request via configured LLM tool."""
    config_dir = ctx.obj['config_dir']
    # Implementation...
```

## Rationale

### Why Click?

**Strengths:**
1. **Mature Ecosystem**
   - Widely adopted (used by Flask, Django-admin, AWS CLI v1)
   - Extensive documentation with many examples
   - Large community and Stack Overflow support
   - Active development since 2014

2. **Excellent Testing Support**
   - `CliRunner` fixture for testing without subprocess
   - Captures stdout/stderr and exit codes
   - Isolated testing environment
   - Fast test execution (no actual CLI invocation)

3. **Composable Architecture**
   - Hierarchical commands via `@click.group()`
   - Context passing for shared state (`@click.pass_context`)
   - Plugin support for extensibility
   - Clean separation of command logic

4. **Developer Experience**
   - Decorator-based API reduces boilerplate
   - Automatic help text generation from docstrings
   - Built-in parameter types (Path, Choice, IntRange, etc.)
   - Good error messages for invalid arguments

5. **Production-Ready Features**
   - Color output support (`click.secho`)
   - Progress bars and prompts
   - Environment variable integration
   - Shell completion support (bash, zsh, fish)

**Trade-offs Accepted:**
1. **Not Type-Safe by Default**
   - Unlike Typer, Click doesn't use type hints for parameter definition
   - Must explicitly declare types: `@click.option('--count', type=int)`
   - *Mitigation*: Acceptable trade-off; explicit types are clear and testable

2. **Decorator Learning Curve**
   - Team must learn Click-specific decorators and patterns
   - Multiple decorators per function can be verbose
   - *Mitigation*: Patterns are well-documented and consistent across codebase

3. **Requires Explicit Type Declarations**
   - Cannot infer types from function signatures
   - More verbose than Typer's annotation-based approach
   - *Mitigation*: Explicit types improve clarity and are easy to understand

### Why NOT Alternative Options?

**argparse (Python stdlib):**
- ❌ Verbose API with significant boilerplate
- ❌ Poor testing story (requires subprocess or mocking)
- ❌ No built-in support for subcommands (must use subparsers manually)
- ❌ Less elegant error handling

**Typer (type-safe CLI based on Click):**
- ✅ Type-safe via function annotations
- ✅ Less boilerplate than Click
- ❌ Less mature ecosystem (released 2019 vs. Click 2014)
- ❌ Smaller community and fewer examples
- ❌ One more layer of abstraction over Click
- **Decision**: Click chosen for maturity and extensive testing support; type safety less critical for CLI layer

**docopt (declarative CLI):**
- ❌ Declarative approach harder to debug
- ❌ Limited type checking
- ❌ Poor testing support
- ❌ Smaller ecosystem

**Raw sys.argv parsing:**
- ❌ Massive boilerplate
- ❌ Error-prone argument handling
- ❌ No automatic help generation
- ❌ Poor user experience

### Why Click Over Typer Specifically?

This was the closest alternative. Key deciding factors:

| Factor | Click | Typer |
|--------|-------|-------|
| **Maturity** | ✅ 10+ years, battle-tested | ⚠️ 4 years, less proven |
| **Community** | ✅ Massive ecosystem | ⚠️ Smaller community |
| **Testing** | ✅ `CliRunner` extensively documented | ✅ Same (Typer uses Click) |
| **Type Safety** | ⚠️ Explicit declarations | ✅ Annotation-based |
| **Boilerplate** | ⚠️ More verbose | ✅ Less verbose |
| **Documentation** | ✅ Extensive examples | ⚠️ Growing but fewer examples |

**Decision Rationale:**
- **Maturity and ecosystem** matter more than type safety for CLI layer
- Testing support is critical → both use `CliRunner` (Typer wraps Click)
- Explicit types in Click are **clearer** for CLI options (self-documenting)
- Click patterns are more widely known in Python community
- Type safety less critical in CLI boundary (already validated by Pydantic in config layer)

## Envisioned Consequences

### Positive Consequences

1. ✅ **Excellent Testability**
   - `CliRunner` enables fast unit tests without subprocess overhead
   - Test coverage: 83% for CLI layer (27 tests)
   - Isolated test environment for predictable results

2. ✅ **Professional User Experience**
   - Automatic help text generation: `llm-service --help`
   - Color-coded output for success/error messages
   - Consistent command structure across all commands
   - Clear error messages for invalid input

3. ✅ **Developer Productivity**
   - Decorator-based API reduces boilerplate
   - Context passing simplifies shared state management
   - Well-documented patterns accelerate feature development

4. ✅ **Extensibility**
   - Easy to add new commands via decorators
   - Plugin support for community contributions
   - Hierarchical commands support future growth

### Negative Consequences

1. ⚠️ **Not Type-Safe**
   - Cannot use Python type hints for automatic validation
   - Must explicitly declare types: `type=click.Path(...)`
   - *Mitigation*: Explicit types are clear and testable; not a significant issue

2. ⚠️ **Decorator Complexity**
   - Multiple decorators per command can be verbose
   - Learning curve for Click patterns
   - *Mitigation*: Patterns documented in `cli.py`; consistency reduces complexity

3. ⚠️ **External Dependency**
   - Adds Click as required dependency
   - Version pinning required: `click>=8.0,<9.0`
   - *Mitigation*: Acceptable; Click is stable and widely-used

### Risk Mitigation Strategies

**Type Safety:**
- Explicit type declarations are self-documenting and clear
- Pydantic validates configuration data (where type safety matters most)
- Click handles CLI boundary validation (less critical layer)

**Decorator Complexity:**
- Document common patterns in `src/llm_service/cli.py`
- Use consistent decorator ordering across all commands
- Provide examples in code comments

**Dependency Management:**
- Pin Click version: `click>=8.0,<9.0`
- Monitor Click releases for security updates
- Click v8 is stable with long-term support

## Considered Alternatives

### Alternative 1: argparse (Python stdlib)

**Description:** Use Python's built-in argument parsing library.

**Pros:**
- No external dependency (stdlib)
- Familiar to Python developers
- Good documentation

**Cons:**
- Verbose API with significant boilerplate
- Poor testing story (requires subprocess or complex mocking)
- Manual subcommand management with subparsers
- Less elegant error handling

**Rejected Because:** Poor testing support, excessive boilerplate, inferior developer experience.

### Alternative 2: Typer (type-safe CLI)

**Description:** Modern CLI framework using Python type hints for parameter definition.

**Pros:**
- Type-safe via function annotations
- Less boilerplate than Click
- Built on top of Click (same `CliRunner` testing)
- Automatic parameter validation from types

**Cons:**
- Less mature (released 2019 vs. Click 2014)
- Smaller community and fewer examples
- Additional abstraction layer over Click
- Less widely adopted in Python ecosystem

**Rejected Because:** Click's maturity and extensive documentation outweigh Typer's type safety benefits for CLI layer. Type safety is less critical at CLI boundary compared to configuration validation layer (where Pydantic provides strong guarantees).

### Alternative 3: docopt (declarative CLI)

**Description:** Define CLI interface via docstring format.

**Pros:**
- Declarative approach
- Minimal code
- Help text is the interface definition

**Cons:**
- Declarative approach harder to debug
- Limited type checking and validation
- Poor testing support
- Smaller ecosystem and community

**Rejected Because:** Declarative approach reduces debuggability, poor testing support, limited ecosystem.

### Alternative 4: Raw sys.argv parsing

**Description:** Manual argument parsing from `sys.argv`.

**Pros:**
- No dependencies
- Maximum control

**Cons:**
- Massive boilerplate for subcommands
- Error-prone argument handling
- No automatic help generation
- Poor error messages
- Significant testing complexity

**Rejected Because:** Reinventing the wheel with poor testing and user experience outcomes.

## Implementation Evidence

**CLI Implementation:**
- `src/llm_service/cli.py` - Complete CLI with 4 commands
  - `llm-service exec` - Execute agent request
  - `llm-service config validate` - Validate configuration
  - `llm-service config init` - Initialize configuration
  - `llm-service version` - Display version info

**Command Structure:**
```
llm-service
├── --config-dir (global option)
├── exec --agent --prompt-file --task-type
├── config
│   ├── validate
│   └── init --force
└── version
```

**Test Coverage:**
- `tests/unit/test_cli.py` - 27 CLI tests
- **83% CLI test coverage** - All command paths tested
- `CliRunner` used for isolated testing
- No subprocess overhead in tests

**User Experience Examples:**

```bash
# Automatic help text
$ llm-service --help
Usage: llm-service [OPTIONS] COMMAND [ARGS]...

  LLM Service Layer - Configuration-driven agent-to-LLM routing.

# Color-coded output
$ llm-service config validate
✓ Configuration is valid!

  Agents:   3 configured
  Tools:    2 configured
  Models:   5 configured

# Clear error messages
$ llm-service exec --agent unknown
✗ Agent 'unknown' not found in configuration
Available agents: architect, backend-dev, planner
```

**Key Achievements:**
- ✅ Professional CLI with hierarchical commands
- ✅ Comprehensive testing via `CliRunner`
- ✅ Context sharing for global options
- ✅ Color-coded output for user feedback
- ✅ Clear error handling and messages

## References

**External Documentation:**
- [Click Documentation](https://click.palletsprojects.com/)
- [Click Testing Guide](https://click.palletsprojects.com/en/8.1.x/testing/)

**Related ADRs:**
- [ADR-025: LLM Service Layer for Agent-Tool Orchestration](ADR-025-llm-service-layer.md) - Approved architecture
- [ADR-026: Pydantic V2 for Schema Validation](ADR-026-pydantic-v2-validation.md) - Configuration validation

**Related Documents:**
- `docs/architecture/design/llm-service-layer-prestudy.md` - Original architecture vision
- `docs/planning/llm-service-layer-implementation-plan.md` - Implementation roadmap
- `src/llm_service/README.md` - Usage examples

**Community Usage:**
- Flask CLI (uses Click)
- Django management commands (Click-based)
- AWS CLI v1 (Click-based)
- pip (uses Click internally)

---

**Decision Made By:** Backend-dev Benny (implementation), Architect Alphonso (architecture review)  
**Date:** 2026-02-04  
**Status:** Accepted (Milestone 1 implementation complete, 83% CLI test coverage achieved)
