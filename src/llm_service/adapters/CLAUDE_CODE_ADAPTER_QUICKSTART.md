# ClaudeCodeAdapter Quick Reference

## Basic Usage

```python
from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter

# Minimal configuration (auto-detects binary in PATH)
config = {}
adapter = ClaudeCodeAdapter(config)

# Execute with supported model
response = adapter.execute(
    prompt="Write a Python function to calculate fibonacci",
    model="claude-3-opus"
)

print(f"Status: {response.status}")
print(f"Output: {response.output}")
```

## Configuration Options

```python
config = {
    # Optional: Explicit binary path (overrides auto-detection)
    "binary_path": "/usr/local/bin/claude-code",
    
    # Optional: Supported models (informational only)
    "models": ["claude-3-opus", "claude-3.5-sonnet", "claude-3-haiku"],
    
    # Optional: Command timeout in seconds (default: 30)
    "timeout": 60,
    
    # Optional: Custom command template
    "template": '{{binary}} --model {{model}} --prompt "{{prompt}}"'
}

adapter = ClaudeCodeAdapter(config)
```

## Supported Models

```python
# Full names
"claude-3.5-sonnet"  # Maps to: claude-3-5-sonnet-20240620
"claude-3-opus"      # Maps to: claude-3-opus-20240229
"claude-3-haiku"     # Maps to: claude-3-haiku-20240307

# Convenient aliases
"claude-3.5"         # Same as claude-3.5-sonnet
"claude-opus"        # Same as claude-3-opus
"claude-haiku"       # Same as claude-3-haiku
```

## Binary Resolution

The adapter finds the claude-code binary using this 3-tier strategy:

1. **Explicit Config:** `config["binary_path"]` (highest priority)
2. **System PATH:** `shutil.which("claude-code")`
3. **Default Paths:** Platform-specific locations

### Platform-Specific Paths

**Linux:**
- `/usr/local/bin/claude-code`
- `~/.local/bin/claude-code`
- `/usr/bin/claude-code`

**macOS:**
- `/usr/local/bin/claude-code`
- `~/bin/claude-code`
- `/opt/homebrew/bin/claude-code`

**Windows:**
- `C:\Program Files\claude-code\claude.exe`
- `C:\Program Files (x86)\claude-code\claude.exe`
- `~/AppData/Local/Programs/claude-code/claude.exe`

## Response Structure

```python
response = adapter.execute(prompt="...", model="...")

# Standard fields
response.status           # "success" or "error"
response.output          # Primary LLM response text
response.tool_name       # "claude-code"

# Execution details
response.exit_code       # Process exit code (0 = success)
response.stdout          # Raw stdout
response.stderr          # Raw stderr
response.duration_seconds  # Execution time

# Metadata (from JSON responses)
response.metadata        # Dict with tokens, cost, model, etc.
```

## Error Handling

```python
from src.llm_service.adapters.claude_code_adapter import (
    ClaudeCodeAdapter,
    BinaryNotFoundError,
    InvalidModelError
)

try:
    adapter = ClaudeCodeAdapter(config)
    response = adapter.execute(prompt="...", model="...")
    
    if response.status == "error":
        print(f"CLI Error: {response.stderr}")
    else:
        print(f"Success: {response.output}")
        
except BinaryNotFoundError as e:
    print(f"Binary not found: {e}")
    # Error includes installation instructions
    
except InvalidModelError as e:
    print(f"Invalid model: {e}")
    # Error lists supported models
```

## Common Scenarios

### 1. Use Explicit Binary Path

```python
config = {
    "binary_path": "/opt/claude/bin/claude-code"
}
adapter = ClaudeCodeAdapter(config)
```

### 2. Increase Timeout for Long Responses

```python
config = {
    "timeout": 120  # 2 minutes
}
adapter = ClaudeCodeAdapter(config)
```

### 3. Handle Special Characters in Prompts

```python
# Adapter automatically handles quotes and special characters
prompt = 'Write code with "quotes" and $pecial characters'
response = adapter.execute(prompt=prompt, model="claude-3-opus")
# Works correctly!
```

### 4. Parse JSON Output

```python
response = adapter.execute(prompt="...", model="...")

if response.status == "success":
    # Access metadata extracted from JSON
    tokens = response.metadata.get("tokens", 0)
    cost = response.metadata.get("cost_usd", 0.0)
    model = response.metadata.get("model", "unknown")
```

## Testing

### Unit Tests

```bash
pytest tests/unit/adapters/test_claude_code_adapter.py -v
# 29 tests, 92% coverage
```

### Integration Tests (with fake CLI)

```bash
pytest tests/integration/adapters/test_claude_code_adapter.py -v
# 16 end-to-end tests
```

### Complete Test Suite

```bash
pytest tests/unit/adapters/ tests/integration/adapters/ -v
# 123 total tests
```

## Installation of claude-code CLI

If binary is not found, install with:

```bash
npm install -g @anthropic-ai/claude-code
```

Or specify explicit path in config.

## Validation

```python
# Validate configuration before use
adapter = ClaudeCodeAdapter(config)
is_valid = adapter.validate_config(config)

if is_valid:
    print("Configuration is valid")
```

## Tool Name

```python
adapter = ClaudeCodeAdapter(config)
assert adapter.get_tool_name() == "claude-code"
```

---

**Related Files:**
- Implementation: `src/llm_service/adapters/claude_code_adapter.py`
- Unit Tests: `tests/unit/adapters/test_claude_code_adapter.py`
- Integration Tests: `tests/integration/adapters/test_claude_code_adapter.py`
- Fake CLI: `tests/fixtures/fake_claude_cli.py`

**Dependencies:**
- Base: `ToolAdapter`, `ToolResponse` from `base.py`
- Infrastructure: `TemplateParser`, `SubprocessWrapper`, `OutputNormalizer`

**Coverage:** 92% (29 unit tests, 16 integration tests)
