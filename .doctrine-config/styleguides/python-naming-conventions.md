# Python Naming Conventions
**Version:** 1.0.0  
**Status:** Active  
**Purpose:** Python-specific naming conventions for this repository  
**Source:** Extracted from Lexical Style Guide (2026-02-10)

---

## Variable Names - Domain Terms

✅ **Prefer specific over generic:**
```python
# ✅ Good - uses glossary terms
task_file = Path("work/collaboration/inbox/task-001.yaml")
work_dir = Path("work/collaboration")
repo_root = Path.cwd()

# ❌ Avoid - generic and ambiguous
file = Path("...")
directory = Path("...")
root = Path("...")
```

✅ **Consistency trumps brevity:**
Use the same variable name for the same concept throughout a module, even if longer.

---

## Class Names - Domain vs. Framework

### Domain code (`src/llm_service`, domain-specific modules):

❌ **Avoid generic suffixes:**
```python
# ❌ Generic - masks domain responsibility
class TemplateManager:
class TaskAssignmentHandler:  # Not event-driven
class SpecificationCache:     # Implementation detail
```

✅ **Prefer specific verbs or DDD patterns:**
```python
# ✅ Domain-specific naming
class TemplateRenderer:
class TaskAssignmentService:
class SpecificationRepository:
```

### Framework code (`src/framework`, base classes):

✅ **Generic suffixes acceptable when following established patterns:**
```python
# ✅ Framework conventions
class FileSystemEventHandler(EventHandler):  # Library interface
class BaseOrchestrator(ABC):                 # Abstract base
```

**Acknowledgment required:** If using generic suffix in domain code, include justification in PR description.

---

## Module Docstrings

**Format:** Google style (Args, Returns, Raises)

**Required sections:**
1. **Purpose statement** (first line, under 80 chars)
2. **Related ADRs** (if applicable)
3. **Key features or patterns** (bulleted list)

**Example:**
```python
"""
Task Query - Filter and search task collections.

Implements ADR-003: Task Lifecycle Management.

Features:
- Status filtering (terminal/active/pending)
- Agent assignment queries
- Date range filtering
"""
```

---

## Glossary Term Usage in Code

**When to use glossary terms:**
- When introducing a domain concept for the first time
- In module and class docstrings
- In user-facing error messages
- In documentation that may be read by newcomers

**How to reinforce glossary terms:**
- Use the exact term from glossary (case-sensitive in prose)
- Link to glossary on first use: `[Task File](.contextive/contexts/orchestration.yml)`
- Include brief inline definition when helpful: "Task File (YAML descriptor)"

**Example:**
```python
def load_task_file(path: Path) -> dict:
    """
    Load Task File from specified path.
    
    A Task File is a YAML file containing a task descriptor,
    following the schema defined in ADR-004.
    
    See: .contextive/contexts/orchestration.yml - "Task File"
    """
```

**Optional: Glossary Terms Used section** (for high-traffic modules):
```python
"""
Module Name - Brief purpose.

Glossary Terms Used:
- Task File (Orchestration): YAML file containing task descriptor
- Task Status (Task Domain): Lifecycle state enum
- Agent Identity (Task Domain): Type-safe agent identifier

See: .contextive/contexts/orchestration.yml
"""
```

---

## Anti-Patterns to Avoid

### ❌ Generic Class Naming (Domain Code)

| Pattern | Problem | Better Alternative |
|---------|---------|-------------------|
| `*Manager` | Vague responsibility | `*Renderer`, `*Service`, `*Builder` |
| `*Handler` (non-event) | Confusing context | `*Service`, `*Processor`, `*Executor` |
| `*Processor` | Generic | `*Validator`, `*Transformer`, `*Parser` |
| `*Wrapper` | Implementation detail | `*Executor`, `*Client`, domain name |
| `*Helper` / `*Utils` | Kitchen sink | Extract to domain-specific modules |

### ✅ Green Flags for Framework Code

| Pattern | Acceptable When | Example |
|---------|----------------|---------|
| `*Handler` | Event handler (watchdog, etc.) | `TaskFileHandler(FileSystemEventHandler)` |
| `*Adapter` | Adapter pattern implementation | `ClaudeCodeAdapter(ToolAdapter)` |
| `*Wrapper` | Thin technical wrapper | `SubprocessWrapper` (debatable) |

---

## Enforcement Philosophy

**Start Permissive**

1. **First occurrence:** Advisory comment with style guide reference
2. **Second occurrence:** Acknowledgment required
3. **Third occurrence:** Escalate to architect or senior reviewer

**Goal:** Education over enforcement. Build shared understanding.

---

## Related Documentation

**Glossary Files:**
- `.contextive/contexts/orchestration.yml` - Operational terms
- `.contextive/contexts/task-domain.yml` - Task-specific vocabulary
- `.contextive/contexts/portfolio-domain.yml` - Portfolio management terms

**Style Guides:**
- `docs/styleguides/python_conventions.md` - Repository-wide Python rules
- `doctrine/docs/styleguides/domain-driven-naming.md` - Generic DDD naming principles

**Practices:**
- `doctrine/approaches/living-glossary-practice.md` - Glossary governance
- `doctrine/approaches/language-first-architecture.md` - Terminology as architecture

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-10  
**Next Review:** 2026-05-10 (quarterly)  
**Owner:** Python Pedro, Curator Claire
