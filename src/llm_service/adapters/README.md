# LLM Tool Adapters

Foundation for integrating external LLM tools (claude-code, codex, etc.) with the routing engine.

## Overview

This package provides the base infrastructure for Milestone 2 (Tool Integration):
- **Abstract base class** for tool adapters (ADR-029)
- **Template parser** with security mitigations
- **Subprocess wrapper** for safe CLI execution
- **Output normalizer** for standardizing tool responses

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Routing Engine                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
           ┌───────────────────────┐
           │    ToolAdapter ABC    │  (base.py)
           │  - execute()          │
           │  - validate_config()  │
           │  - get_tool_name()    │
           └───────────┬───────────┘
                       │
       ┌───────────────┼───────────────┐
       │               │               │
       ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ClaudeCode   │ │   Codex     │ │   Generic   │
│Adapter      │ │  Adapter    │ │   Adapter   │
│(M2 Batch2.2)│ │(M2 Batch2.3)│ │(M2 Batch2.4)│
└─────────────┘ └─────────────┘ └─────────────┘
       │               │               │
       └───────────────┼───────────────┘
                       │
       ┌───────────────┴───────────────┐
       │                               │
       ▼                               ▼
┌─────────────────┐         ┌──────────────────┐
│TemplateParser   │         │SubprocessWrapper │
│- parse()        │────────▶│- execute()       │
│- security checks│         │- timeout mgmt    │
└─────────────────┘         └────────┬─────────┘
                                     │
                                     ▼
                           ┌──────────────────┐
                           │OutputNormalizer  │
                           │- normalize()     │
                           │- extract metadata│
                           └──────────────────┘
```

## Components

### 1. Base Adapter (`base.py`)

Abstract base class enforcing consistent interface across all tool adapters.

**Key Classes:**
- `ToolAdapter` - ABC with required methods
- `ToolResponse` - Standardized response dataclass

**Design Decision (ADR-029):**
- Chose ABC over Protocol for runtime validation
- Ensures incomplete adapters fail at instantiation (fail-fast)
- Clear contract for contributors

**Example:**
```python
from src.llm_service.adapters import ToolAdapter, ToolResponse

class MyToolAdapter(ToolAdapter):
    def execute(self, prompt: str, model: str, **kwargs) -> ToolResponse:
        # Implementation
        return ToolResponse(
            status="success",
            output="Generated text",
            tool_name=self.get_tool_name()
        )
    
    def validate_config(self, config: dict) -> bool:
        return "binary" in config
    
    def get_tool_name(self) -> str:
        return "my-tool"
```

### 2. Template Parser (`template_parser.py`)

Parses command templates with `{{placeholder}}` syntax and security mitigations.

**Security Features:**
- Whitelist validation for placeholders
- Shell metacharacter handling
- Command injection prevention (works with shell=False)
- Proper argument splitting via shlex

**Example:**
```python
from src.llm_service.adapters import TemplateParser

parser = TemplateParser(allowed_placeholders=["binary", "model", "prompt"])
command = parser.parse(
    "{{binary}} --model {{model}} --prompt {{prompt}}",
    {
        "binary": "/usr/bin/cli",
        "model": "claude-3-opus",
        "prompt": "test"
    }
)
# Returns: ["/usr/bin/cli", "--model", "claude-3-opus", "--prompt", "test"]
```

### 3. Subprocess Wrapper (`subprocess_wrapper.py`)

Safe subprocess execution with timeout and error handling.

**Security Features:**
- **Always uses shell=False** (hardcoded)
- Command passed as list (not string)
- No shell expansion
- Controlled environment variables

**Example:**
```python
from src.llm_service.adapters import SubprocessWrapper

wrapper = SubprocessWrapper(timeout=30)
result = wrapper.execute(["echo", "hello"])

print(f"Exit code: {result.exit_code}")
print(f"Output: {result.stdout}")
print(f"Duration: {result.duration_seconds}s")
print(f"Timed out: {result.timed_out}")
```

### 4. Output Normalizer (`output_normalizer.py`)

Standardizes outputs from different tool formats (JSON, plain text).

**Features:**
- Auto-detects format (JSON vs text)
- Extracts response text from various JSON structures
- Parses metadata (tokens, cost, model)
- Identifies errors and warnings
- Plugin architecture for tool-specific formats

**Example:**
```python
from src.llm_service.adapters import OutputNormalizer

normalizer = OutputNormalizer()
result = normalizer.normalize('{"response": "text", "usage": {"total_tokens": 100}}')

print(f"Response: {result.response_text}")
print(f"Tokens: {result.metadata.get('tokens')}")
print(f"Errors: {result.errors}")
```

## Usage Pattern

Typical flow for a concrete adapter:

```python
from src.llm_service.adapters import (
    ToolAdapter,
    ToolResponse,
    TemplateParser,
    SubprocessWrapper,
    OutputNormalizer,
)

class ClaudeCodeAdapter(ToolAdapter):
    def __init__(self, tool_config: dict):
        super().__init__(tool_config)
        self.parser = TemplateParser()
        self.wrapper = SubprocessWrapper(timeout=tool_config.get("timeout", 30))
        self.normalizer = OutputNormalizer()
    
    def execute(self, prompt: str, model: str, **kwargs) -> ToolResponse:
        # 1. Build command from template
        command = self.parser.parse(
            self.tool_config["command_template"],
            {"binary": self.tool_config["binary"], "model": model, "prompt": prompt}
        )
        
        # 2. Execute via subprocess
        exec_result = self.wrapper.execute(command)
        
        # 3. Normalize output
        normalized = self.normalizer.normalize(exec_result.stdout, format="json")
        
        # 4. Return standardized response
        return ToolResponse(
            status="success" if exec_result.exit_code == 0 else "error",
            output=normalized.response_text,
            tool_name=self.get_tool_name(),
            exit_code=exec_result.exit_code,
            stdout=exec_result.stdout,
            stderr=exec_result.stderr,
            duration_seconds=exec_result.duration_seconds,
            metadata=normalized.metadata
        )
    
    def validate_config(self, config: dict) -> bool:
        required = ["binary", "command_template", "models"]
        return all(key in config for key in required)
    
    def get_tool_name(self) -> str:
        return "claude-code"
```

## Testing

All components have comprehensive test coverage:

- **Base Adapter:** 14 tests, 88% coverage
- **Template Parser:** 19 tests, 94% coverage (security scenarios)
- **Subprocess Wrapper:** 22 tests, 93% coverage (platform compat)
- **Output Normalizer:** 23 tests, 94% coverage (format handling)

**Total:** 78 tests, 93% overall coverage

Run tests:
```bash
pytest tests/unit/adapters/ -v --cov=src.llm_service.adapters
```

## Security

All components follow security review recommendations:

1. **Template Parser:**
   - Whitelist validation prevents unknown placeholders
   - Works with shell=False (no shell expansion)
   - Proper argument splitting

2. **Subprocess Wrapper:**
   - Shell=False enforcement (hardcoded)
   - Command as list prevents injection
   - No shell metacharacter interpretation

3. **Integration:**
   - Template → subprocess flow is secure
   - Tested against injection attacks

## Next Steps (M2 Batches 2.2-2.4)

This foundation enables concrete adapter implementations:

- **Batch 2.2:** ClaudeCodeAdapter using base adapter
- **Batch 2.3:** CodexAdapter for OpenAI Codex
- **Batch 2.4:** Generic YAML-based adapter for custom tools

## References

- **ADR-029:** Adapter Interface Design (ABC approach)
- **Security Review:** `work/analysis/llm-service-command-template-security.md`
- **Implementation Plan:** `docs/planning/llm-service-layer-implementation-plan.md`
- **Work Log:** `work/logs/2026-02-05-backend-dev-m2-batch-2.1-completion.md`
