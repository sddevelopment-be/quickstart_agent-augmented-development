# Tactic: Terminology Validation Checklist
**Version:** 1.0.0  
**Status:** Active  
**Purpose:** Quick reference for terminology validation during code review  
**Context:** Pull request review, code quality checks  
**Enforcement:** Advisory → Acknowledgment → Blocker (progressive)

---

## When to Apply

Use this tactic when reviewing:
- New classes, modules, or packages
- Changes to public APIs
- Documentation updates
- Glossary modifications
- Domain model changes

---

## Quick Decision Tree

### 1. Does this introduce new domain concepts?

- ✅ **YES** → Check if term exists in glossary
- ❌ **NO** → Proceed to step 2

### 2. Is glossary term available?

- ✅ **YES** → Use glossary term consistently
- ❌ **NO** → Add to glossary candidates list

### 3. Is this a generic name (Manager/Handler/Processor)?

- ✅ **YES** → Check if domain-specific name would be clearer
- ❌ **NO** → Proceed to step 4

### 4. Does term usage match glossary definition?

- ✅ **YES** → Approve
- ❌ **NO** → Request alignment or glossary update

---

## Well-Established Terms (Use Consistently)

| Term | Usage | Context | Files |
|------|-------|---------|-------|
| **Agent** | Identity and orchestration | Orchestration | 87 |
| **Task** | Work unit in orchestration | Task Domain | Pervasive |
| **Orchestrator** | Coordination component | Orchestration | 6 |
| **TaskStatus** | Lifecycle state enum | Task Domain | 8 |
| **Specification** | Requirements document | Portfolio | 10 |
| **Initiative** | High-level project grouping | Portfolio | 5 |
| **Feature** | Specific capability in spec | Portfolio | 19 |

**Action:** Verify consistent usage. Flag deviations for review.

---

## Inconsistent Terms (Standardize)

| What You'll See | Prefer | Notes |
|-----------------|--------|-------|
| task_file / file_path / YAML | **task_file** | Variable naming |
| Task File | **Task File** | Documentation (title case) |
| work dir / WORK_DIR / work/ | **work_dir** | Variable naming |
| Work Directory | **Work Directory** | Documentation |
| read_task / load / load_task | **read_task** | Function name (Pythonic) |
| write_task / save / persist | **write_task** | Function name (Pythonic) |

**Action:** Comment with preferred term and glossary reference.

---

## Generic Anti-Patterns (Avoid or Justify)

### RED FLAGS in Domain Code

| Pattern | Problem | Better Alternative |
|---------|---------|-------------------|
| `*Manager` | Vague responsibility | `*Renderer`, `*Service`, `*Builder` |
| `*Handler` (non-event) | Confusing context | `*Service`, `*Processor`, `*Executor` |
| `*Wrapper` | Implementation detail | `*Executor`, `*Client`, domain name |
| `*Helper` / `*Utils` | Kitchen sink | Extract to domain-specific modules |

### GREEN FLAGS for Framework Code

| Pattern | Acceptable When | Example |
|---------|----------------|---------|
| `*Handler` | Event handler (watchdog, etc.) | `TaskFileHandler(FileSystemEventHandler)` |
| `*Adapter` | Adapter pattern implementation | `ClaudeCodeAdapter(ToolAdapter)` |
| `*Wrapper` | Thin technical wrapper | `SubprocessWrapper` (with justification) |

**Action:** For domain code, require acknowledgment or better name.

---

## Missing from Glossary (High Priority)

These terms appear frequently but lack glossary entries:

| Term | Files | Definition Needed | Context |
|------|-------|-------------------|---------|
| **TaskStatus** | 8 | Task lifecycle enum | Task Domain |
| **FeatureStatus** | 4 | Feature implementation enum | Task Domain |
| **TaskPriority** | 3 | Priority levels enum | Task Domain |
| **TaskMode** | 1 | Agent operating modes | Task Domain |
| **AgentIdentity** | 2 | Type-safe agent ID | Task Domain |
| **Configuration** | 15 | System settings | Infrastructure |
| **Template** | 12 | Jinja2 config generator | Infrastructure |

**Action:** Flag for glossary addition. Escalate to Curator Claire.

---

## Code Review Checklist

### For New Classes

- [ ] Class name uses domain language (not generic suffix)?
- [ ] If generic suffix used, is it justified (framework convention)?
- [ ] Domain concepts documented in glossary?
- [ ] ADR exists for architectural decisions?

### For New Domain Terms

- [ ] Term defined in relevant glossary?
- [ ] Definition includes source (ADR, module, spec)?
- [ ] Related terms cross-referenced?
- [ ] Enforcement tier specified?

### For Terminology Changes

- [ ] Glossary updated to reflect code?
- [ ] OR code updated to reflect glossary?
- [ ] Rationale documented if diverging?
- [ ] Migration path specified if renaming?

### For Documentation

- [ ] Module docstring includes purpose + ADRs + features?
- [ ] Glossary terms reinforced in docstrings?
- [ ] Code examples show term usage?
- [ ] No hype language ("revolutionary", "best practice")?

---

## Review Comment Templates

### Advisory Comment (Suggestion)

```markdown
ℹ️ **Terminology:** Consider using "{preferred_term}" (from {context} glossary) 
instead of "{current_term}" for consistency with domain vocabulary. (Advisory)

See: .contextive/contexts/{context}.yml
```

**When to use:** First occurrence, low impact, suggestion for improvement.

---

### Acknowledgment Required Comment

```markdown
⚠️ **Generic Naming:** `{ClassName}` uses generic "{suffix}" suffix without 
clear domain context. Consider:
- `{Alternative1}` (if {rationale})
- `{Alternative2}` (if {rationale})

Please acknowledge if keeping current name with justification.
(Acknowledgment Required)

See: doctrine/docs/styleguides/domain-driven-naming.md
```

**When to use:** Second occurrence, medium impact, patterns that reduce clarity.

---

### Question Comment (Blocker)

```markdown
❓ **New Domain Concept?** This introduces "{term}" concept. Please:
1. Add to glossary (if new domain term)
2. Use existing term (if synonym: {existing_term})
3. Document distinction (if different from {similar_term})

cc: @curator-claire @architect-alphonso

(Blocks merge until resolved)
```

**When to use:** New domain concepts, unclear boundaries, third occurrence.

---

### Enhancement Suggestion

```markdown
📝 **Docstring Enhancement:** Consider adding:
- Related ADRs: ADR-{number} ({title})
- Glossary terms: {term1}, {term2} (from {context}.yml)
- Key features: (bulleted list for scannability)

This strengthens traceability and helps newcomers. (Advisory)

See: .doctrine-config/styleguides/python-naming-conventions.md
```

**When to use:** Documentation improvements, optional but beneficial.

---

## Context-Specific Guidance

### Orchestration Context (`src/framework/orchestration/`)

**Alignment Status:** ✅ Strong

**Do:**
- Use "Agent", "Task", "Orchestrator" consistently
- Reference TaskStatus enum for state checks
- Document file-based coordination patterns

**Watch:**
- "Status" vs. "State" - code uses "Status", some docs say "State"
- Directory naming: `work_dir` (not `WORK_DIR` or `collab_dir`)

---

### Dashboard Context (`src/llm_service/dashboard/`)

**Alignment Status:** ⚠️ Weak (rich domain, missing glossary)

**Do:**
- Use Specification, Initiative, Feature consistently
- Document portfolio management concepts
- Propose bounded context glossary

**Watch:**
- Generic class names (TaskAssignmentHandler, SpecificationCache)
- Domain vocabulary not in any glossary
- Missing bounded context documentation

---

### Common Types (`src/common/types.py`)

**Alignment Status:** ⚠️ Good potential (strong types, need glossary)

**Do:**
- Use enums (TaskStatus, FeatureStatus, TaskPriority, TaskMode)
- Validate agent IDs with AgentIdentity
- Reference state machine semantics

**Watch:**
- Enums not in glossary (should be!)
- No ADR cross-references in glossary
- Type safety decisions undocumented

---

## Enforcement Philosophy

**Progressive Escalation:**

1. **First occurrence:** Advisory comment with link to style guide
2. **Second occurrence:** Acknowledgment required
3. **Third occurrence:** Escalate to architect or curator

**Goal:** Education over enforcement. Build shared understanding.

**When to escalate:**
- Third occurrence of same issue
- Disagreement on domain terminology
- New bounded context identification
- Glossary term conflicts

**Escalation Path:**
- **Glossary terms:** Curator Claire (`@curator-claire`)
- **Architecture decisions:** Architect Alphonso (`@architect-alphonso`)
- **Style conventions:** Lexical Larry (`@lexical-larry`)
- **Language-specific patterns:** Python Pedro (`@python-pedro`)

---

## Success Metrics

Track these over time to measure improvement:

| Metric | Current Baseline | Target (3 months) |
|--------|------------------|-------------------|
| Glossary term usage | 25% | 45% |
| Domain concepts documented | 0/21 | 13/21 |
| Generic anti-patterns | 19 | 12 |
| Terminology conflicts | 3 | 0 |

---

## Related Resources

**Glossaries:**
- `.contextive/contexts/orchestration.yml` - Operational terms
- `.contextive/contexts/task-domain.yml` - Task vocabulary
- `.contextive/contexts/portfolio-domain.yml` - Portfolio terms

**Style Guides:**
- `doctrine/docs/styleguides/domain-driven-naming.md` - Generic DDD principles
- `.doctrine-config/styleguides/python-naming-conventions.md` - Python-specific

**Practices:**
- `doctrine/approaches/living-glossary-practice.md` - Glossary governance
- `doctrine/approaches/language-first-architecture.md` - Terminology as architecture

**Reports:**
- `work/terminology-validation-report.md` - Full analysis
- `docs/reports/assessments/conceptual-alignment-assessment-summary.md` - Executive summary

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-10  
**Next Review:** After new glossary approval  
**Maintainer:** Curator Claire, Code-reviewer Cindy

---

*"Good terminology is invisible - you only notice it when it's missing." - Code-reviewer Cindy*
