# Terminology Issue Tracker - Code Review Reference

**Purpose:** Quick lookup for common terminology issues during code review  
**Source:** Lexical Analysis Report (2026-02-10)  
**Audience:** Code reviewers (Code-reviewer Cindy, Python Pedro, Backend Benny)

---

## How to Use This Guide

1. **During code review:** Check for patterns listed below
2. **First occurrence:** Advisory comment with link to style guide
3. **Second occurrence:** Acknowledgment required
4. **Third occurrence:** Escalate to Curator Claire or Architect Alphonso

**Enforcement philosophy:** Education over enforcement. Build shared understanding.

---

## Common Issues by Category

### 1. Generic Class Naming (Domain Code)

#### ❌ **Anti-Patterns**

| Pattern | Issue | Review Comment |
|---------|-------|----------------|
| `*Manager` | Vague responsibility | "Consider specific verb: Renderer, Service, Builder" |
| `*Handler` (non-event) | Confusing context | "Handler implies events - is this event-driven?" |
| `*Processor` | Generic | "What specific processing? Validator, Transformer, Parser?" |
| `*Wrapper` | Implementation detail | "What domain concept does this represent?" |
| `*Helper` / `*Utils` | Kitchen sink | "Extract to domain-specific module or rename specifically" |

#### ✅ **Good Alternatives**

```python
# ❌ Generic
class TemplateManager:
class TaskProcessor:
class DataHandler:

# ✅ Specific
class TemplateRenderer:
class TaskValidator:
class SpecificationRepository:
```

**Comment Template:**
```markdown
⚠️ **Generic Naming:** `{ClassName}` uses generic suffix without clear 
domain context. Consider:
- Option A (with rationale)
- Option B (with rationale)

Or acknowledge if keeping current name with justification.

See: work/LEX/LEXICAL_STYLE_GUIDE.md, Section "Class Names"
```

**Enforcement:** Acknowledgment Required

---

### 2. Inconsistent Operational Vocabulary

#### ⚠️ **Variable Naming Variants**

| Concept | ❌ Avoid | ✅ Prefer | Glossary Source |
|---------|----------|-----------|-----------------|
| Task YAML file | `file`, `yaml`, `path` | `task_file` | orchestration.yml |
| Work directory | `dir`, `collab_dir`, `base` | `work_dir` | orchestration.yml |
| Repository root | `root`, `base_dir`, `path` | `repo_root` | convention |

**Comment Template:**
```markdown
ℹ️ **Terminology:** Consider using `{preferred_term}` (from orchestration 
glossary) instead of `{current_term}` for consistency with domain vocabulary.

See: .contextive/contexts/orchestration.yml
```

**Enforcement:** Advisory (first occurrence), Acknowledgment Required (repeat)

---

### 3. Missing Glossary Terms

#### 🆕 **Candidate Terms (Document These)**

If code introduces these concepts **without glossary entry**:

| Term | Definition Needed | Priority | Owner |
|------|-------------------|----------|-------|
| New status values | Add to TaskStatus enum or document rationale | HIGH | Python Pedro |
| New lifecycle states | Document state machine transition | HIGH | Architect Alphonso |
| New domain concepts | Add to appropriate glossary | MEDIUM | Curator Claire |
| New UI vocabulary | Add to collaboration.yml (proposed) | MEDIUM | Frontend Freddy |

**Comment Template:**
```markdown
❓ **New Domain Concept?** This introduces `{term}` concept. Should we:
1. Add to glossary (if domain term)
2. Use existing term (if synonym of known term)
3. Document distinction (if different from similar term)

cc: @curator-claire @architect-alphonso
```

**Enforcement:** Question (blocks merge until resolved)

---

### 4. Docstring Quality Issues

#### ⚠️ **Missing Elements**

Check for these in **module and class docstrings**:

- [ ] **Purpose statement** (first line, <80 chars)
- [ ] **Related ADRs** (if architectural decision involved)
- [ ] **Key features** (bulleted list if >2 features)
- [ ] **Glossary term usage** (if introduces domain concepts)

**Comment Template:**
```markdown
📝 **Docstring Enhancement:** Consider adding:
- Related ADRs: ADR-XXX (if applicable)
- Glossary terms used: {term} (from {context}.yml)
- Key features: (bulleted list)

This helps newcomers understand context and domain vocabulary.

See: work/LEX/LEXICAL_STYLE_GUIDE.md, Section "Module Docstrings"
```

**Enforcement:** Advisory (nice-to-have for existing code, recommended for new)

---

### 5. ADR Cross-Reference Missing

#### ℹ️ **When to Require ADR References**

If code implements or modifies:
- Status enums (ADR-043)
- Agent identity handling (ADR-044)
- Task lifecycle management (ADR-003)
- File-based coordination (ADR-008)
- Configuration templates (ADR-031)

**Comment Template:**
```markdown
🔗 **Traceability:** This code implements {pattern} from ADR-{number}. 
Please add ADR reference to module docstring:

\`\`\`python
"""
{Module Name} - {Purpose}.

Implements ADR-{number}: {ADR Title}.
"""
\`\`\`
```

**Enforcement:** Advisory (strengthens traceability)

---

## Quick Checklist

### For New Classes

- [ ] Class name uses domain language (not generic suffix)?
- [ ] If generic suffix, is it justified (framework convention)?
- [ ] Domain concepts documented in glossary?
- [ ] ADR reference included if architectural?

### For New Domain Terms

- [ ] Term defined in relevant glossary?
- [ ] Definition includes source (ADR, module, spec)?
- [ ] Related terms cross-referenced?
- [ ] Enforcement tier specified?

### For Documentation

- [ ] Module docstring includes purpose + ADRs + features?
- [ ] Glossary terms reinforced in docstrings?
- [ ] Code examples show term usage?
- [ ] No hype language ("revolutionary", "best practice")?

---

## Style Violations Reference

### ❌ Anti-Patterns to Flag

**Hype Language:**
- "Revolutionary", "cutting-edge", "best practice", "world-class"
- **Suggest:** "Current approach", "recommended pattern", "effective solution"

**Flattery:**
- "Brilliant", "genius", "incredible work" (excessive praise)
- **Suggest:** "Well-designed", "clear implementation", specific technical feedback

**Weasel Words:**
- "Probably", "might", "maybe", "sort of", "kind of" (in technical docs)
- **Suggest:** "Will", "is", conditional statements, specific probabilities

**Em-dash Issues:**
- `---` (conflicts with YAML frontmatter)
- **Suggest:** `—` (em-dash character) or restructure sentence

---

## Context-Specific Guidance

### Orchestration Context (`src/framework/orchestration/`)

**Strong alignment** - Use as reference

✅ **Do:**
- Use "Agent", "Task", "Orchestrator" consistently
- Reference TaskStatus enum for state checks
- Document file-based coordination patterns

⚠️ **Watch:**
- "Status" vs. "State" - code uses "Status"
- Directory naming: `work_dir` (not `WORK_DIR` or `collab_dir`)

---

### Dashboard Context (`src/llm_service/dashboard/`)

**Weak alignment** - Rich domain, missing glossary

✅ **Do:**
- Use Specification, Initiative, Feature consistently
- Document portfolio management concepts
- Propose bounded context glossary

⚠️ **Watch:**
- Generic class names (TaskAssignmentHandler, SpecificationCache)
- Domain vocabulary not in any glossary
- Missing bounded context documentation

---

### Common Types (`src/common/types.py`)

**Good alignment potential** - Strong types, need glossary

✅ **Do:**
- Use enums (TaskStatus, FeatureStatus, TaskPriority, TaskMode)
- Validate agent IDs with AgentIdentity
- Reference state machine semantics

⚠️ **Watch:**
- Enums not in glossary (should be!)
- No ADR cross-references in glossary
- Type safety decisions undocumented

---

## Resources for Review Comments

**Glossary Files:**
- `.contextive/contexts/ddd.yml` - DDD concepts
- `.contextive/contexts/doctrine.yml` - Framework terms
- `.contextive/contexts/orchestration.yml` - Operational vocabulary (proposed)
- `.contextive/contexts/organizational.yml` - Team patterns

**Style Guides:**
- `work/LEX/LEXICAL_STYLE_GUIDE.md` - Writing and naming conventions
- `docs/styleguides/python_conventions.md` - Python-specific rules

**Analysis Reports:**
- `work/LEX/LEXICAL_ANALYSIS_REPORT.md` - Comprehensive analysis
- `work/terminology-quick-reference.md` - Term usage reference (Cindy's work)

**Architectural Context:**
- `docs/architecture/assessments/strategic-linguistic-assessment-2026-02-10.md` - Alphonso's assessment
- `doctrine/approaches/living-glossary-practice.md` - Glossary governance
- `doctrine/docs/linguistic-anti-patterns.md` - Common terminology misuse

---

## Comment Templates Library

### Advisory Comment
```markdown
ℹ️ **Terminology:** Consider using "{preferred_term}" (from {context} glossary) 
instead of "{current_term}" for consistency with domain vocabulary. (Advisory)

See: .contextive/contexts/{context}.yml, work/LEX/LEXICAL_STYLE_GUIDE.md
```

### Acknowledgment Required
```markdown
⚠️ **Generic Naming:** `{ClassName}` uses generic "{suffix}" suffix without 
clear domain context. Consider:
- `{Alternative1}` (if {rationale})
- `{Alternative2}` (if {rationale})

Please acknowledge if keeping current name with justification.
(Acknowledgment Required)

See: work/LEX/LEXICAL_STYLE_GUIDE.md, Section "Class Names"
```

### Question / Blocker
```markdown
❓ **New Domain Concept?** This introduces "{term}" concept. Please:
1. Add to glossary (if new domain term)
2. Use existing term (if synonym: {existing_term})
3. Document distinction (if different from {similar_term})

cc: @curator-claire @architect-alphonso

(Blocks merge until resolved)
```

### Enhancement Suggestion
```markdown
📝 **Docstring Enhancement:** Consider adding:
- Related ADRs: ADR-{number} ({title})
- Glossary terms: {term1}, {term2} (from {context}.yml)
- Key features: (bulleted list for scannability)

This strengthens traceability and helps newcomers. (Advisory)

See: work/LEX/LEXICAL_STYLE_GUIDE.md, Section "Module Docstrings"
```

---

## Escalation Path

**Level 1 (Advisory):** Reviewer suggests, author decides  
**Level 2 (Acknowledgment):** Author must respond (agree or justify)  
**Level 3 (Blocker):** Escalate to:

- **Glossary terms:** Curator Claire
- **Architecture decisions:** Architect Alphonso  
- **Style conventions:** Lexical Larry
- **Python patterns:** Python Pedro

**When to escalate:**
- Third occurrence of same issue
- Disagreement on domain terminology
- New bounded context identification
- Glossary term conflicts

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-10  
**Next Review:** After orchestration.yml approval

---

_Quick reference companion to LEXICAL_STYLE_GUIDE.md - optimized for PR review workflow._
