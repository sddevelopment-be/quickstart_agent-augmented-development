# Architecture Review: Generic YAML-Driven Adapter vs. Concrete Adapters

**Date:** 2026-02-05  
**Reviewer:** Orchestration Coordinator  
**Context:** M2 Batch 2.2 Complete - ClaudeCodeAdapter Implementation  
**Raised By:** Human-in-Charge

---

## Questions Raised

1. **Do we need specific adapter classes for each tool when YAML config handles it?**
2. **Would a generic YAML config parser with tool name registration be more extensible?**
3. **Is the adapter wrapper there to parse outcomes/deal with specific issues?**
4. **Do we support passing ENV variables with API keys to command invocations?**

---

## Current State Analysis

### What We Built (M2 Batches 2.1 & 2.2)

**Batch 2.1 - Infrastructure:**
- `ToolAdapter` (ABC base class)
- `TemplateParser` (placeholder substitution: `{{model}}`, `{{prompt}}`)
- `SubprocessWrapper` (command execution with timeout, env support)
- `OutputNormalizer` (response standardization)

**Batch 2.2 - Concrete Adapter:**
- `ClaudeCodeAdapter` (~400 lines of code)
- Model mapping (claude-3.5-sonnet → CLI parameter)
- Binary path resolution (cross-platform)
- Error handling (user-friendly messages)

### What the YAML Config Already Defines

From `config/tools.yaml.example` (per prestudy):
```yaml
tools:
  claude-code:
    binary: claude-code
    command_template: "{binary} --model {model} --prompt {prompt_file}"
    platforms:
      linux: /usr/local/bin/claude-code
      macos: /usr/local/bin/claude-code
      windows: C:\Program Files\claude-code\claude.exe
    models:
      - claude-3-opus-20240229
      - claude-3-5-sonnet-20240620
      - claude-3-haiku-20240307
```

---

## Analysis: Are Concrete Adapters Over-Engineering?

### What ClaudeCodeAdapter Actually Does

**Current Implementation (~400 lines):**
1. Model name mapping (convenience aliases)
2. Binary path resolution (shutil.which + platform defaults)
3. Command template usage (delegates to TemplateParser)
4. Subprocess execution (delegates to SubprocessWrapper)
5. Output parsing (delegates to OutputNormalizer)
6. Error handling (user-friendly messages)

**What YAML Already Provides:**
- ✅ Tool binary location
- ✅ Command template
- ✅ Supported models
- ✅ Platform-specific paths

**Redundancy Analysis:**
- ❌ Model mapping is redundant (YAML lists models)
- ❌ Binary paths are redundant (YAML has platform paths)
- ⚠️ Command template usage is just delegation
- ✅ Error messages add value (user-friendly)
- ⚠️ Output parsing might be tool-specific

---

## Proposal: Generic YAML-Driven Adapter

### Original Plan (Task 8 - Not Yet Implemented)

From `llm-service-layer-implementation-plan.md`:
```
8. 2026-02-04T1707-backend-dev-generic-yaml-adapter.yaml
   - Generic YAML-configured adapter
   - Demonstrate adding a new tool without code changes
   - Extensibility documentation
```

**This was always the plan!** We just implemented concrete adapters first for validation.

### How a Generic Adapter Would Work

```python
class GenericYAMLAdapter(ToolAdapter):
    """
    Generic adapter that reads tool configuration from YAML.
    No code changes needed to add new tools.
    """
    
    def __init__(self, tool_name: str, tool_config: ToolConfig):
        self.tool_name = tool_name
        self.tool_config = tool_config
        self.template_parser = TemplateParser()
        self.subprocess_wrapper = SubprocessWrapper()
        self.output_normalizer = OutputNormalizer()
    
    def execute(self, prompt: str, model: str, params: Dict = None) -> ToolResponse:
        # 1. Validate model is supported
        if model not in self.tool_config.models:
            raise InvalidModelError(f"Model {model} not in {self.tool_config.models}")
        
        # 2. Resolve binary path
        binary = self._resolve_binary()
        
        # 3. Generate command from template
        context = {"binary": binary, "model": model, "prompt": prompt}
        command = self.template_parser.parse(self.tool_config.command_template, context)
        
        # 4. Execute via subprocess
        result = self.subprocess_wrapper.execute(
            command,
            timeout=self.tool_config.get("timeout", 30),
            env=self._prepare_env(params)
        )
        
        # 5. Normalize output
        normalized = self.output_normalizer.normalize(result.stdout, self.tool_name)
        
        return ToolResponse(output=normalized.response_text, metadata=normalized.metadata)
    
    def _resolve_binary(self) -> str:
        """Resolve binary path from config or PATH."""
        # Check config override first
        if self.tool_config.binary_path:
            return self.tool_config.binary_path
        
        # Check shutil.which()
        binary = shutil.which(self.tool_config.binary)
        if binary:
            return binary
        
        # Check platform-specific paths
        platform_paths = self.tool_config.platforms.get(platform.system().lower())
        if platform_paths and os.path.isfile(platform_paths):
            return platform_paths
        
        raise BinaryNotFoundError(f"{self.tool_config.binary} not found")
    
    def _prepare_env(self, params: Dict) -> Dict[str, str]:
        """Prepare environment variables from params."""
        env = os.environ.copy()
        if params and "env" in params:
            env.update(params["env"])
        return env
```

### Benefits of Generic Approach

✅ **No code changes to add new tools** - Just update YAML:
```yaml
tools:
  gemini-cli:
    binary: gemini
    command_template: "{binary} --model {model} < {prompt_file}"
    models: [gemini-1.5-pro, gemini-1.5-flash]
```

✅ **Simpler codebase** - ~100 lines vs. 400 lines per adapter

✅ **Community contributions** - Add tools via YAML, not Python

✅ **Centralized logic** - Binary resolution, env handling in one place

❌ **Less tool-specific optimization** - Can't customize per-tool behavior

---

## ENV Variable Support

### Current Implementation (Batch 2.1)

**YES, we have ENV support!** In `SubprocessWrapper`:

```python
def execute(
    self,
    command: List[str],
    timeout: int = 30,
    env: Optional[Dict[str, str]] = None,
) -> ExecutionResult:
    """
    Execute command with optional environment variables.
    
    Args:
        env: Optional environment variables dictionary
    """
    # Merge with current environment
    proc_env = os.environ.copy()
    if env:
        proc_env.update(env)
    
    result = subprocess.run(
        command,
        env=proc_env,  # ← ENV support here
        ...
    )
```

**Usage for API keys:**
```python
adapter.execute(
    prompt="Generate code",
    model="claude-3-opus",
    params={
        "env": {
            "ANTHROPIC_API_KEY": "sk-ant-...",
            "OPENAI_API_KEY": "sk-..."
        }
    }
)
```

**Missing:** YAML config for default env vars per tool:
```yaml
tools:
  claude-code:
    binary: claude-code
    env_vars:  # ← Not yet implemented
      ANTHROPIC_API_KEY: "${ANTHROPIC_API_KEY}"  # Read from system env
```

---

## When Are Concrete Adapters Valuable?

### Tool-Specific Behavior That YAML Can't Handle

1. **Complex Output Parsing:**
   - claude-code returns JSON with specific structure
   - codex returns plain text with markers
   - gemini returns JSONL stream
   - → Generic normalizer might not handle all cases

2. **Multi-Step Tool Invocations:**
   - Tool requires `init` command first
   - Tool needs session management
   - Tool has interactive prompts

3. **Platform-Specific Quirks:**
   - Windows requires `.exe` suffix handling
   - macOS requires app bundle navigation
   - Tool-specific permission issues

4. **Performance Optimizations:**
   - Tool-specific caching strategies
   - Batch request optimizations
   - Tool-specific timeout tuning

**For claude-code:** Probably doesn't need concrete adapter!  
**For complex tools:** Concrete adapter might add value.

---

## Recommendations

### Short Term (Current State)

**Keep ClaudeCodeAdapter for now** as reference implementation and validation:
- ✅ Proves the infrastructure works
- ✅ Provides working example for contributors
- ✅ Documents best practices for tool integration

### Medium Term (Next Batch)

**Implement GenericYAMLAdapter (Task 8):**
1. Create `GenericYAMLAdapter` class
2. Use it for simple tools (codex, gemini)
3. Compare complexity vs. concrete adapters
4. **Measure:** Lines of code, extensibility, maintainability

**Migration Path:**
```python
# Option 1: Generic for most tools, concrete for complex ones
adapter_factory = {
    "claude-code": ClaudeCodeAdapter,  # Concrete (if needed)
    "codex": GenericYAMLAdapter,       # Generic
    "gemini": GenericYAMLAdapter,      # Generic
}

# Option 2: Pure generic (simplest)
adapter = GenericYAMLAdapter(tool_name, tool_config)
```

### Long Term (Post-MVP)

**Decision Point:** After implementing both approaches, **measure and decide**:
- If generic adapter handles 90%+ of tools → deprecate concrete adapters
- If concrete adapters add significant value → keep hybrid approach
- Document the trade-offs in ADR

---

## ENV Variable Enhancement Proposal

### Add to YAML Config Schema

```yaml
tools:
  claude-code:
    binary: claude-code
    command_template: "{binary} --model {model} --prompt {prompt_file}"
    env_vars:
      ANTHROPIC_API_KEY: "${ANTHROPIC_API_KEY}"  # From system env
      CLAUDE_HOME: "${HOME}/.claude"             # From system env
    env_required:  # Validation
      - ANTHROPIC_API_KEY
```

### Implementation

```python
def _prepare_env(self, tool_config: ToolConfig, params: Dict) -> Dict[str, str]:
    """Prepare environment variables."""
    env = os.environ.copy()
    
    # Add tool-specific env vars from YAML
    if hasattr(tool_config, 'env_vars'):
        for key, value in tool_config.env_vars.items():
            # Expand ${VAR} references
            env[key] = os.path.expandvars(value)
    
    # Override with params
    if params and "env" in params:
        env.update(params["env"])
    
    # Validate required env vars
    if hasattr(tool_config, 'env_required'):
        for var in tool_config.env_required:
            if var not in env:
                raise EnvironmentError(f"Required env var {var} not set")
    
    return env
```

---

## Conclusion

### Answers to Questions

1. **Do we need specific adapters?** 
   - No for simple tools, Maybe for complex tools
   - **Recommendation:** Implement generic adapter (Task 8) and compare

2. **Would generic YAML parser be more extensible?**
   - **Yes!** This was always the plan (Task 8)
   - Current concrete adapter validates infrastructure first

3. **Is wrapper for parsing outcomes/specific issues?**
   - **Partially** - Wrappers add user-friendly errors
   - **Mostly** - Output parsing might need tool-specific logic
   - **Recommendation:** Generic adapter + pluggable normalizers

4. **ENV variable support?**
   - **Yes** - SubprocessWrapper already supports it
   - **Missing** - YAML config for default env vars
   - **Recommendation:** Add env_vars to YAML schema

### Next Steps

**Option A: Continue as planned (Batches 2.3-2.4 concrete adapters)**
- Implement codex adapter (concrete)
- Then implement generic adapter (Task 8)
- Compare and decide

**Option B: Skip to generic adapter now (faster to MVP)**
- Implement GenericYAMLAdapter (Task 8)
- Add env_vars to YAML schema
- Use for all tools (claude-code, codex, gemini)
- Add concrete adapters only if needed

**Recommendation:** **Option B** - Faster to MVP, more extensible, aligns with YAML-driven design philosophy.

---

**Question for Human-in-Charge:** Which option do you prefer?
- Continue with concrete adapters (validate more edge cases)?
- Skip to generic adapter (faster, more extensible)?
- Hybrid (generic + concrete for complex tools)?
