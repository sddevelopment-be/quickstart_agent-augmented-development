# Glossary Terminology Update — Business Logic & Production Code

**Agent:** Curator Claire  
**Date:** 2026-02-10  
**Work Type:** Terminology Standardization  
**Directive Reference:** Directive 014 (Work Log Creation), Directive 004 (Documentation & Context Files)

---

## Context

Code Reviewer Cindy used the terms "business logic" and "production code" in her review assessment, which are widely used throughout the doctrine but were not formally defined in `doctrine/GLOSSARY.md`. This created a gap where agents and humans might interpret these terms differently, reducing consistency and clarity.

**Triggering Event:** Request from human to check and add these definitions if missing.

---

## Investigation Findings

### Current State Assessment

**Searched for existing definitions:**
1. ✅ Reviewed `doctrine/GLOSSARY.md` (v1.1.0) — No definitions for "business logic" or "production code"
2. ✅ Searched all doctrine files for usage patterns

**Usage Analysis:**

**"Business Logic" usage found in:**
- `directives/034_spec_driven_development.md`
- `approaches/spec-driven-development.md`
- `templates/specifications/feature-spec-template.md`
- `tactics/test-boundaries-by-responsibility.tactic.md`

**"Production Code" usage found in:**
- `directives/028_bugfixing_techniques.md` (4 occurrences)
- `directives/017_test_driven_development.md` (3 occurrences)
- `approaches/test-first-bug-fixing.md` (5 occurrences)
- `approaches/bug-fixing-checklist.md` (3 occurrences)
- `agents/java-jenny.agent.md`, `frontend.agent.md`, `backend-dev.agent.md`
- `tactics/repository-initialization.tactic.md`

**Conclusion:** Both terms are heavily used but undefined. This represents a documentation gap that can lead to inconsistent interpretation.

---

## Actions Taken

### 1. Added "Business Logic" Definition

**Location:** After "Bootstrap" entry (alphabetical order maintained)

**Definition Structure:**
- **Summary:** Core rules, workflows, and domain-specific behaviors
- **Characteristics:** 4 bullet points covering key attributes
- **Location guidance:** `src/` directory context
- **Example:** TaskStatus enum reference
- **Related terms:** Production Code, TDD, Specification

**Rationale:**
- Framework-specific: References actual codebase structure (`src/`, `tools/`, `tests/`)
- Actionable: Clear boundaries distinguishing business logic from infrastructure/utility code
- Example-driven: Uses concrete example from the framework (TaskStatus)
- Cross-referenced: Links to related concepts already in glossary

### 2. Added "Production Code" Definition

**Location:** After "Primer" entry (alphabetical order maintained)

**Definition Structure:**
- **Summary:** Code executing in production with highest quality standards
- **Quality Requirements:** 5 bullet points specifying expectations
- **Location guidance:** `src/` directory and deployment context
- **Exclusions:** Explicit list of what is NOT production code
- **Related terms:** Business Logic, TDD, Testing Pyramid

**Rationale:**
- Quality-focused: Emphasizes testing, security, performance requirements
- Boundary-setting: Clear exclusions prevent ambiguity
- Framework-aligned: References actual directory structure
- Process-connected: Links to TDD and Testing Pyramid practices

### 3. Updated Glossary Metadata

**Version bump:** 1.1.0 → 1.2.0 (minor version per Directive 006)
- **Reason:** New terms added (not just clarifications)
- **Updated date:** 2026-02-10

---

## Alignment Validation

✅ **Alphabetical ordering preserved:** Both entries inserted in correct alphabetical positions  
✅ **Formatting consistency:** Matches existing entry structure (summary, bullets, location, related)  
✅ **Cross-referencing:** Both terms reference each other and link to existing glossary terms  
✅ **Framework-specific:** Definitions grounded in actual project structure (`src/`, `tools/`, `tests/`)  
✅ **Actionable guidance:** Clear boundaries and examples for agent/human usage  
✅ **Version governance:** Proper version bump per Directive 006 guidelines

---

## Artifacts Produced

| Artifact | Location | Purpose |
|----------|----------|---------|
| Updated GLOSSARY.md | `doctrine/GLOSSARY.md` | Added 2 new term definitions |
| This work log | `work/reports/logs/curator-claire/2026-02-10-glossary-terminology-update.md` | Document rationale and process |

---

## Outcomes

### Immediate
- ✅ "Business logic" formally defined with framework context
- ✅ "Production code" formally defined with quality standards
- ✅ Glossary version updated (1.1.0 → 1.2.0)
- ✅ Cross-references established between related terms

### Downstream Benefits
- Agents can reference authoritative definitions when using these terms
- Code reviewers have clear criteria for assessing code placement (`src/` vs `tools/`)
- New contributors have explicit guidance on framework expectations
- Reduces ambiguity in directive interpretation and agent collaboration

---

## Lessons Learned

### Pattern Recognition
**Terminology audit trigger:** When agents use terms consistently but without formal definitions, that's a signal to update the glossary proactively.

### Quality Indicators
1. **Good coverage:** Searching for term usage across doctrine revealed heavy usage (16+ files)
2. **Clear boundaries:** Definitions included both what terms ARE and what they EXCLUDE
3. **Framework grounding:** References to actual directory structure prevent abstraction drift

### Process Refinement
- **Search before define:** Examining existing usage patterns informed better definitions
- **Cross-reference early:** Linking related terms during initial authoring improves discoverability
- **Version governance:** Following Directive 006 strictly ensures predictable evolution

---

## Recommendations

### Immediate Actions
None required — definitions are complete and aligned.

### Future Considerations
1. **Periodic terminology audit:** Review agent outputs quarterly for undefined but commonly used terms
2. **Directive cross-check:** When adding glossary terms, check if directives need updates to reference them
3. **Usage monitoring:** Track whether agents consistently reference new definitions in their work logs

---

## Metadata

**Primers Applied:**
- Context Check: Verified glossary structure, version governance requirements, existing usage patterns
- Progressive Refinement: Searched → Drafted → Cross-referenced → Validated
- Transparency: This work log documents full rationale and decision process

**Mode Transitions:**
- `/analysis-mode` (default): Investigation and structure review
- `/creative-mode`: Definition authoring with framework-specific examples
- `/analysis-mode` (return): Validation and alignment checking

**Confidence Level:** ✅ High
- Definitions grounded in actual framework usage
- Alphabetical ordering verified
- Version governance followed
- Cross-references complete

---

**Work Log Complete**  
**Next Steps:** Await human review/approval of glossary changes
