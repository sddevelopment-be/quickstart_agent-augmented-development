# PR Comment Templates for Code Review
**Version:** 1.0.0  
**Status:** Active  
**Purpose:** Standardized comment templates for terminology and code quality review  
**Audience:** Code reviewers (Code-reviewer Cindy, Python Pedro, Backend Benny)

---

## Template Categories

1. **Terminology Issues** - Glossary alignment, naming consistency
2. **Documentation Issues** - Docstring quality, ADR references
3. **Generic Naming** - Manager/Handler/Processor anti-patterns
4. **Domain Concepts** - New terms, missing definitions

---

## 1. Terminology Issues

### Advisory: Preferred Term Suggestion

```markdown
ℹ️ **Terminology:** Consider using "{preferred_term}" (from {context} glossary) 
instead of "{current_term}" for consistency with domain vocabulary. (Advisory)

See: .contextive/contexts/{context}.yml
```

**When to use:** First occurrence, low impact, suggestion for improvement.

**Example:**
```markdown
ℹ️ **Terminology:** Consider using "task_file" (from orchestration glossary) 
instead of "yaml_path" for consistency with domain vocabulary. (Advisory)

See: .contextive/contexts/orchestration.yml
```

---

### Acknowledgment Required: Inconsistent Usage

```markdown
⚠️ **Terminology Inconsistency:** This code uses "{term_variant_1}" but other 
modules use "{preferred_term}". For consistency, please:
- Update to "{preferred_term}" (recommended)
- OR document rationale for divergence

(Acknowledgment Required)

See: .contextive/contexts/{context}.yml, Line {line_number}
```

**When to use:** Second occurrence, inconsistency with established terms.

---

## 2. Generic Naming Anti-Patterns

### Generic Suffix Warning (Domain Code)

```markdown
⚠️ **Generic Naming:** `{ClassName}` uses generic "{suffix}" suffix without 
clear domain context. Consider:
- `{Alternative1}` (if {rationale})
- `{Alternative2}` (if {rationale})

Please acknowledge if keeping current name with justification.
(Acknowledgment Required)

See: doctrine/docs/styleguides/domain-driven-naming.md
```

**When to use:** Manager/Handler/Processor in domain code.

**Example:**
```markdown
⚠️ **Generic Naming:** `TemplateManager` uses generic "Manager" suffix without 
clear domain context. Consider:
- `TemplateRenderer` (if rendering templates)
- `TemplateCache` (if caching templates)
- `TemplateValidator` (if validating template syntax)

Please acknowledge if keeping current name with justification.
(Acknowledgment Required)

See: doctrine/docs/styleguides/domain-driven-naming.md
```

---

### Handler Not Event-Driven

```markdown
ℹ️ **Naming Convention:** `{ClassName}Handler` implies event-driven architecture, 
but this appears to be synchronous service. Consider:
- `{ClassName}Service` (if orchestrating multiple operations)
- `{ClassName}Executor` (if executing single responsibility)
- Keep Handler only if implementing FileSystemEventHandler or similar

(Advisory)

See: .doctrine-config/styleguides/python-naming-conventions.md
```

**When to use:** Handler suffix in non-event code.

---

## 3. Domain Concepts

### New Domain Concept Question

```markdown
❓ **New Domain Concept?** This introduces "{term}" concept. Please:
1. Add to glossary (if new domain term)
2. Use existing term (if synonym: {existing_term})
3. Document distinction (if different from {similar_term})

cc: @curator-claire @architect-alphonso

(Blocks merge until resolved)
```

**When to use:** New domain terms without glossary entry.

**Example:**
```markdown
❓ **New Domain Concept?** This introduces "WorkflowStage" concept. Please:
1. Add to glossary (if new domain term distinct from TaskStatus)
2. Use existing term (if synonym: TaskStatus)
3. Document distinction (if different from TaskStatus lifecycle states)

cc: @curator-claire @architect-alphonso

(Blocks merge until resolved)
```

---

### Missing Glossary Entry

```markdown
📚 **Glossary Gap:** This code uses "{term}" which appears to be a domain concept 
but lacks glossary definition. Please:
- Add definition to `.contextive/contexts/{context}.yml`
- Include source (ADR, module, specification)
- Cross-reference related terms

cc: @curator-claire

(Acknowledgment Required)
```

**When to use:** Established domain terms not in glossary.

---

## 4. Documentation Issues

### Missing Docstring Elements

```markdown
📝 **Docstring Enhancement:** Consider adding:
- Related ADRs: ADR-{number} ({title})
- Glossary terms: {term1}, {term2} (from {context}.yml)
- Key features: (bulleted list for scannability)

This strengthens traceability and helps newcomers. (Advisory)

See: .doctrine-config/styleguides/python-naming-conventions.md
```

**When to use:** Module/class docstrings missing context.

---

### Missing ADR Reference

```markdown
🔗 **Traceability:** This code implements {pattern} from ADR-{number}. 
Please add ADR reference to module docstring:

\`\`\`python
"""
{Module Name} - {Purpose}.

Implements ADR-{number}: {ADR Title}.
"""
\`\`\`

This helps trace architectural decisions. (Advisory)
```

**When to use:** Code implementing ADR patterns.

**Example:**
```markdown
🔗 **Traceability:** This code implements file-based coordination from ADR-008. 
Please add ADR reference to module docstring:

\`\`\`python
"""
Agent Orchestrator - File-based task coordination and assignment.

Implements ADR-008: File-Based Async Coordination.
"""
\`\`\`

This helps trace architectural decisions. (Advisory)
```

---

### Hype Language Detected

```markdown
ℹ️ **Style:** Consider replacing hype language ("{hype_term}") with more 
technical description. Suggested alternatives:
- "effective solution" (instead of "brilliant")
- "recommended approach" (instead of "best practice")
- "current implementation" (instead of "cutting-edge")

(Advisory - Style consistency)

See: doctrine/docs/styleguides/domain-driven-naming.md
```

**When to use:** Revolutionary, brilliant, best practice, world-class.

---

## 5. Style & Quality

### Weasel Words in Technical Doc

```markdown
ℹ️ **Technical Writing:** Consider replacing uncertainty ("{weasel_word}") with:
- Specific conditional: "If X, then Y"
- Probabilistic: "60% likely" (if quantified)
- Definitive: "Will/Will not" (if decided)

Technical documentation benefits from precision. (Advisory)
```

**When to use:** Probably, might, maybe, sort of, kind of.

---

### Em-Dash YAML Conflict

```markdown
⚠️ **Markdown Formatting:** `---` conflicts with YAML frontmatter. Please use:
- `—` (em-dash character)
- OR restructure sentence to avoid dash

(Acknowledgment Required if YAML parsing fails)
```

**When to use:** `---` used as em-dash in markdown files.

---

## 6. Context-Specific Comments

### Orchestration Context

```markdown
✅ **Good Alignment:** This code uses orchestration vocabulary consistently 
("Agent", "Task File", "work_dir"). Well done!

Note: Consider adding TaskStatus enum instead of string literal for state checks.

See: .contextive/contexts/orchestration.yml
```

**When to use:** Positive reinforcement for good practices.

---

### Dashboard Context (Missing Glossary)

```markdown
📋 **Bounded Context:** This module introduces rich portfolio management 
vocabulary (Specification, Initiative, Feature) not yet documented in glossary.

Suggest creating `.contextive/contexts/portfolio-domain.yml` to capture:
- Specification definition
- Initiative vs Feature distinction  
- Portfolio View semantics

cc: @curator-claire @architect-alphonso

(Advisory - improves long-term maintainability)
```

**When to use:** Rich domain vocabulary without glossary.

---

## 7. Escalation Comments

### Third Occurrence Escalation

```markdown
🚨 **Escalation:** This is the third occurrence of {issue_pattern} in recent PRs.

Previous occurrences:
- PR #{pr_number_1}: {file_path_1}
- PR #{pr_number_2}: {file_path_2}

Escalating to:
- @curator-claire (if glossary-related)
- @architect-alphonso (if architectural pattern)
- @lexical-larry (if style convention)

Please align on standard approach before merging.

(Blocks merge until escalation resolved)
```

**When to use:** Pattern appears 3+ times without resolution.

---

### Conflicting Definitions

```markdown
⚠️ **Terminology Conflict:** "{term}" is used with two different meanings:

**This PR:** {definition_new}  
**Existing usage:** {definition_existing} (see {file_path})

This indicates:
1. Potential bounded context boundary
2. Need for context-specific glossaries
3. OR need for term disambiguation

cc: @architect-alphonso @curator-claire

(Blocks merge until conflict resolved)
```

**When to use:** Same term with different semantics.

---

## Quick Reference

### Emoji Key

- ℹ️ **Advisory** - Suggestion, author decides
- ⚠️ **Acknowledgment Required** - Author must respond
- ❓ **Question / Blocker** - Blocks merge until resolved
- 📝 **Documentation** - Docs improvement suggestion
- 📚 **Glossary** - Glossary-related issue
- 🔗 **Traceability** - ADR/decision linkage
- ✅ **Positive** - Reinforcement of good practices
- 🚨 **Escalation** - Pattern requires team decision

---

## Enforcement Levels

| Level | When | Action | Merge Block |
|-------|------|--------|-------------|
| **Advisory** | First occurrence, low impact | Comment with suggestion | No |
| **Acknowledgment** | Second occurrence, medium impact | Author must respond | Optional |
| **Blocker** | Third occurrence, high impact | Escalate to specialist | Yes |

---

## Context-Aware Templates

Use these based on file location:

### For `src/framework/orchestration/`
- Strong alignment expected
- Use orchestration glossary references
- Framework patterns acceptable

### For `src/llm_service/dashboard/`
- Domain-rich, missing glossary
- Suggest bounded context creation
- Watch for generic naming

### For `src/common/types.py`
- Enums should be in glossary
- Reference ADRs for type decisions
- Strong type safety expected

---

## Related Resources

**Checklists:**
- `.doctrine-config/tactics/terminology-validation-checklist.tactic.md`

**Style Guides:**
- `doctrine/docs/styleguides/domain-driven-naming.md`
- `.doctrine-config/styleguides/python-naming-conventions.md`

**Glossaries:**
- `.contextive/contexts/orchestration.yml`
- `.contextive/contexts/task-domain.yml`
- `.contextive/contexts/portfolio-domain.yml`

**Reports:**
- `work/terminology-validation-report.md`
- `docs/reports/assessments/conceptual-alignment-assessment-summary.md`

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-10  
**Next Review:** After 30 days usage feedback  
**Maintainer:** Code-reviewer Cindy, Curator Claire

---

*Use these templates consistently to build shared understanding and reduce review friction.*
