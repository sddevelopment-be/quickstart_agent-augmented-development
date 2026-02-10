# Lexical Style Guide Recommendations

**Source:** Lexical Analysis Report (2026-02-10)  
**Purpose:** Actionable style guidance for writing and terminology  
**Audience:** All contributors, especially documentation writers and code reviewers

---

## Quick Reference

### Documentation Style

**Tone:** Technical, clear, sincere. No hype, no flattery.

**Voice:** Active voice preferred (80%+). Passive acceptable for technical precision.

**Sentence rhythm:** Mix short (5-10 words) and long (20-30 words). Vary structure.

**Paragraphs:** 2-4 sentences ideal. Break dense blocks. Use lists for >3 items.

**Em-dash:** Use `—` (em-dash character), not `---` (conflicts with YAML).

---

## Python Naming Conventions

### Variable Names - Domain Terms

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

### Class Names - Domain vs. Framework

**Domain code** (`src/llm_service`, domain-specific modules):

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

**Framework code** (`src/framework`, base classes):

✅ **Generic suffixes acceptable when following established patterns:**
```python
# ✅ Framework conventions
class FileSystemEventHandler(EventHandler):  # Library interface
class BaseOrchestrator(ABC):                 # Abstract base
```

**Acknowledgment required:** If using generic suffix in domain code, include justification in PR description.

---

## Documentation Conventions

### Module Docstrings

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

### Glossary Term Usage

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

### ADR Writing Style

**Structure:** Status → Context → Decision → Rationale → Consequences

**Context section:**
- Start with problem/need
- Provide background (what led us here)
- State constraints
- Explain why now (timing/trigger)

**Decision section:**
- Clear statement: "We will..." or "We have decided to..."
- Bullet points for multiple parts
- Avoid hedging ("probably", "might", "should consider")

**Rationale section:**
- Explain the *why* behind the decision
- Technical reasoning
- Business value
- Risk mitigation

**Example tone:**
> "We have adopted a modular agent directive system consisting of..."  
> ✅ Clear, decisive, confident

Not:
> "We're thinking about maybe using a system that could potentially..."  
> ❌ Hedging, uncertain, weak

---

## Markdown Hygiene

### Heading Hierarchy

✅ **Use semantic structure:**
```markdown
# Title (H1) - Document name
## Section (H2) - Major divisions  
### Subsection (H3) - Detailed topics
#### Detail (H4) - Sub-components
```

❌ **Avoid skipping levels:**
```markdown
# Title
### Subsection  # ❌ Skipped H2
```

---

### List Formatting

✅ **Keep list items scannable (under 80 chars when possible):**
```markdown
- Understand the five-layer model: [DOCTRINE_STACK.md](doctrine/DOCTRINE_STACK.md)
- Browse available tactics: [tactics/README.md](doctrine/tactics/README.md)
- Core principles: [general_guidelines.md](doctrine/guidelines/general_guidelines.md)
```

⚠️ **Avoid wall-of-text lists:**
```markdown
- Read [doctrine/DOCTRINE_STACK.md](doctrine/DOCTRINE_STACK.md) to understand the five-layer model
- Browse [doctrine/tactics/README.md](doctrine/tactics/README.md) to see available tactics
```

**Pattern:** Frontload the action verb, keep link labels brief.

---

### Code Blocks

✅ **Always use language tags:**
````markdown
```python
def example():
    pass
```

```bash
echo "Example"
```
````

✅ **Use inline code for:**
- Variable names: `task_file`
- Function calls: `load_task()`
- File paths: `path/to/file.py`
- Status values: `status="done"`

---

## Anti-Patterns to Avoid

### ❌ Hype Language

**Avoid:**
- "Revolutionary approach"
- "Best practice"
- "Cutting-edge"
- "Game-changing"
- "World-class"

**Use instead:**
- "This approach..."
- "Recommended pattern"
- "Current / modern"
- "Significant improvement"
- "High-quality"

---

### ❌ Flattery

**Avoid:**
- "Brilliant solution"
- "Genius idea"
- "Incredible work"
- Excessive praise in code reviews

**Use instead:**
- "Effective solution"
- "Well-designed"
- "Clear implementation"
- Specific, technical feedback

---

### ❌ Weasel Words

**Avoid:**
- "Probably"
- "Might"
- "Maybe"
- "Sort of"
- "Kind of"

**Use instead:**
- "Will" / "Will not"
- "Is" / "Is not"
- Specific probability: "60% likely"
- Conditional: "If X, then Y"

---

### ❌ Dictionary DDD

**Anti-pattern:** Glossary document exists but is never updated or referenced.

**Symptoms:**
- Last glossary update >6 months ago
- Code uses terms not in glossary
- Glossary terms not used in code

**Mitigation:**
- Integrate glossary into workflow (IDE plugins, PR checks)
- Assign ownership per bounded context
- Quarterly review and update
- Reference glossary in docstrings

---

## Enforcement Philosophy

**Start Permissive**

1. **First occurrence:** Advisory comment with style guide reference
2. **Second occurrence:** Acknowledgment required
3. **Third occurrence:** Escalate to architect or senior reviewer

**Goal:** Education over enforcement. Build shared understanding.

**Example advisory comment:**
```markdown
ℹ️ **Terminology:** Consider using "Task File" (from orchestration glossary) 
instead of "yaml file" for consistency with domain vocabulary. This helps 
newcomers understand the concept. (Advisory)

See: work/LEX/LEXICAL_STYLE_GUIDE.md, Section "Glossary Term Usage"
```

**Example acknowledgment comment:**
```markdown
⚠️ **Generic Naming:** `TaskManager` uses generic "Manager" suffix without 
clear domain context. Consider:
- `TaskOrchestrator` (if coordinating multiple tasks)
- `TaskExecutor` (if executing single task)
- `TaskRepository` (if managing persistence)

Please acknowledge if keeping current name, or rename per style guide.
(Acknowledgment Required)

See: work/LEX/LEXICAL_STYLE_GUIDE.md, Section "Class Names"
```

---

## Medium-Specific Variants

### ADRs (Architecture Decision Records)
- **Tone:** Formal, analytical
- **Structure:** Strict (Status → Context → Decision → Rationale → Consequences)
- **Audience:** Engineers, architects, future maintainers

### Module Docstrings
- **Tone:** Technical, precise
- **Structure:** Purpose → Details → Examples
- **Audience:** Developers using the module

### README Files
- **Tone:** Welcoming, clear
- **Structure:** Quick Start → Details → References
- **Audience:** Newcomers, all experience levels

### Glossaries (YAML)
- **Tone:** Definitional, concise
- **Structure:** Term → Definition → Metadata → Examples
- **Audience:** All (reference material)

### Work Logs
- **Tone:** Chronological, structured
- **Structure:** Task → Actions → Deliverables → Status
- **Audience:** Agents, coordinators, reviewers

---

## Resources

**Glossary Files:**
- `.contextive/contexts/ddd.yml` - DDD concepts
- `.contextive/contexts/doctrine.yml` - Framework vocabulary
- `.contextive/contexts/orchestration.yml` - Operational terms (proposed)
- `.contextive/contexts/organizational.yml` - Team patterns
- `.contextive/contexts/software-design.yml` - Architecture patterns

**Related Documentation:**
- `doctrine/approaches/living-glossary-practice.md` - Glossary governance
- `doctrine/approaches/language-first-architecture.md` - Terminology as architecture
- `work/terminology-quick-reference.md` - Quick lookup for code reviewers
- `work/LEX/LEXICAL_ANALYSIS_REPORT.md` - Full analysis (this distillation)

**Style Guides:**
- `docs/styleguides/python_conventions.md` - Python-specific guidance
- `docs/styleguides/version_control_hygiene.md` - Git commit style

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-10  
**Next Review:** 2026-05-10 (quarterly)

---

_This style guide distills patterns from lexical analysis and codifies implicit conventions. Treat as living document - propose changes via PR._
