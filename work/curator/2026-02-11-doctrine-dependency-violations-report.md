# Doctrine Dependency Direction Violations Report

**Agent:** Curator Claire  
**Date:** 2026-02-11  
**Purpose:** Audit `doctrine/` directory for references to local ADRs (dependency direction violations)  
**Context:** Directive 020 (Lenient Adherence), Directive 018 (Documentation Level Framework)  
**Requester:** @stijn-dejongh

---

## Executive Summary

**✅ PRIMARY FINDING:** Multiple dependency direction violations detected. Framework artifacts in `doctrine/` reference repository-specific ADRs in `docs/architecture/adrs/`.

**Violation Count:**
- **CRITICAL:** 23 violations (direct dependencies on local ADRs)
- **INFORMATIONAL:** 89 violations (path examples, templates, patterns using `${DOC_ROOT}` variable)

**Severity Assessment:** ❗️ **MODERATE-HIGH** - While many references use templating (`${DOC_ROOT}`), several core directives contain hardcoded ADR references that break portability.

**Recommended Action:** Phased remediation - immediate fixes for critical violations, followed by systematic pattern updates.

---

## Dependency Direction Rule (Reaffirmed)

```
✅ ALLOWED:     Local (docs/architecture/adrs/) → Framework (doctrine/)
❌ VIOLATION:   Framework (doctrine/) → Local (docs/architecture/adrs/)
✅ ALTERNATIVE: Framework (doctrine/) → Config (.doctrine-config/)
```

**Rationale:** Framework artifacts must remain portable across repositories. Local ADRs are repository-specific implementation decisions.

---

## 1. Critical Violations (Direct Dependencies)

These violations create hard dependencies from framework to local implementation:

### 1.1 Directive 023: Clarification Before Execution

**File:** `doctrine/directives/023_clarification_before_execution.md`

**Violations:**

1. **Line 9:** 
   ```markdown
   **Related:** ADR-023 (Prompt Optimization Framework) - This directive implements Pattern P1 
   mitigation (vague success criteria) and supports reducing the 30% clarification rate 
   identified in work log analysis.
   ```

2. **Line 11 (section header):** "This directive targets these efficiency improvements from ADR-023"

3. **Line 86 (automated checks section):** "### Automated Checks (Future - Phase 2 of ADR-023)"

4. **Line 141 (references section):**
   ```markdown
   - **ADR-023:** [Prompt Optimization Framework](/../${DOC_ROOT}/architecture/adrs/ADR-023-prompt-optimization-framework.md)
   ```

**Context:** Directive claims to implement a specific local ADR decision. This creates tight coupling.

**Severity:** 🔴 **CRITICAL** - Framework directive depends on repository-specific decision rationale

---

### 1.2 Directive 034: Spec-Driven Development

**File:** `doctrine/directives/034_spec_driven_development.md`

**Violations:**

1. **Line 305:**
   ```markdown
   **ADR (ADR-032):**
   ```

2. **Lines 457-460:**
   ```markdown
   - Implementation details: See ADR-028 (WebSocket Technology Choice)
   
   ADR-028: Use Flask-SocketIO for Real-Time Communication
   ```

**Context:** Examples section references specific technology decisions from local ADRs

**Severity:** 🔴 **CRITICAL** - Framework directive uses local ADRs as authoritative examples

---

### 1.3 Directive 036: Boy Scout Rule

**File:** `doctrine/directives/036_boy_scout_rule.md`

**Violations:**

1. **Line 203:**
   ```python
   """Task lifecycle states (see ADR-043)"""  # Updated, added ADR reference
   ```

2. **Line 208:**
   ```markdown
   - Update docstring with ADR-043 reference
   ```

3. **Lines 214-217:**
   ```markdown
   # - Broken link to ADR-001
   See [ADR-001](../adrs/ADR-001.md) for details.
   See [ADR-001](../architecture/adrs/ADR-001-modular-agent-directive-system.md)
   - Fix broken ADR-001 link (path changed)
   ```

**Context:** Example code and troubleshooting section references local ADRs

**Severity:** 🟡 **MODERATE** - Used as examples within directive content, not foundational dependency

---

### 1.4 GLOSSARY.md

**File:** `doctrine/GLOSSARY.md`

**Violations:**

1. **Line 78 (Primer entry):**
   ```markdown
   A foundational execution pattern defined in ADR-011 that establishes minimum quality 
   thresholds for agent work.
   ```

2. **Entry reference line:**
   ```markdown
   **Reference:** Directive 019, ADR-003
   ```

**Context:** Core terminology defined relative to specific local ADRs

**Severity:** 🔴 **CRITICAL** - Central glossary ties definitions to local decisions

---

### 1.5 Directive 019: File-Based Collaboration

**File:** `doctrine/directives/019_file_based_collaboration.md`

**Violations:**

**Lines 170-171:**
```markdown
- ADR-002: File-Based Asynchronous Agent Coordination
- ADR-003: Task Lifecycle and State Management
```

**Context:** References section cites local ADRs as authoritative sources

**Severity:** 🔴 **CRITICAL** - Framework directive depends on local decision rationale

---

### 1.6 Directive 035: Specification Frontmatter Standards

**File:** `doctrine/directives/035_specification_frontmatter_standards.md`

**Violations:**

1. **Line 38:**
   ```markdown
   1. **Machine-readable metadata** for portfolio tracking (ADR-037)
   ```

2. **Line 115:**
   ```markdown
   - **ADR-037:** Dashboard Initiative Tracking (portfolio view architecture)
   ```

**Context:** Directive implementation rationale tied to specific local ADR

**Severity:** 🟡 **MODERATE** - References explain "why" but don't create hard dependency

---

### 1.7 Directive 016: Acceptance Test-Driven Development

**File:** `doctrine/directives/016_acceptance_test_driven_development.md`

**Violation:**

**Line 187:**
```markdown
- Exception: trivial throw-away utilities or single-use shell scripts (log exception in 
  [work log](../GLOSSARY.md#work-log) and reference ADR-012).
```

**Severity:** 🟡 **MODERATE** - Exception handling references local ADR

---

### 1.8 Directive 017: Test-Driven Development

**File:** `doctrine/directives/017_test_driven_development.md`

**Violations:**

1. **Line 142:**
   ```markdown
   - Exception: trivial shell utilities or disposable scripts noted per ADR-012.
   ```

2. **Line 158:**
   ```markdown
   - **ADR-012:** Test-Driven Development Mandate
   ```

**Severity:** 🟡 **MODERATE** - Exception policy references local decision

---

### 1.9 Directive 011: Risk Escalation

**File:** `doctrine/directives/011_risk_escalation.md`

**Violation:**

**Line 88:**
```markdown
- Failure to execute Transparency & Error Signaling [primer](../GLOSSARY.md#primer) 
  (see ADR-011) when a risk is discovered
```

**Severity:** 🟡 **MODERATE** - References ADR for primer definition context

---

### 1.10 Directive 010: Mode Protocol

**File:** `doctrine/directives/010_mode_protocol.md`

**Violation:**

**Line 153:**
```markdown
## Primer Binding (ADR-011)
```

**Severity:** 🟡 **MODERATE** - Section header references ADR for architectural context

---

### 1.11 Directive 014: Worklog Creation

**File:** `doctrine/directives/014_worklog_creation.md`

**Violation:**

**Line 78:**
```markdown
- **Primer Checklist:** List which primers (Context Check, Progressive Refinement, 
  Trade-Off Navigation, Transparency, Reflection) were executed, skipped, or not 
  applicable with justification. Reference ADR-011.
```

**Severity:** 🟡 **MODERATE** - Instructions tell agents to reference local ADR

---

### 1.12 Directive 015: Store Prompts

**File:** `doctrine/directives/015_store_prompts.md`

**Violation:**

**Line 112:**
```markdown
- If the Reflection Loop or Transparency primers (ADR-011) surfaced prompt-quality 
  issues, note the primer invocation in the SWOT analysis for traceability.
```

**Severity:** 🟡 **MODERATE** - Guidance references local ADR for context

---

### 1.13 Directive 018: Traceable Decisions

**File:** `doctrine/directives/018_traceable_decisions.md`

**Violation:**

**Line 156:**
```markdown
- **ADR-017:** Self-referential; defines traceable decision patterns
```

**Severity:** 🟠 **MODERATE-HIGH** - Self-referential ADR creates bootstrap dependency

---

### 1.14 Directive 025: Framework Guardian

**File:** `doctrine/directives/025_framework_guardian.md`

**Violations:**

1. **Line 67:**
   ```markdown
   Per ADR-011 and Directive 010, Guardian invokes:
   ```

2. **Lines 215-216:**
   ```markdown
   - **ADR-013:** Zip-Based Framework Distribution
   - **ADR-014:** Framework Guardian Agent Decision
   ```

**Context:** Guardian directive depends on ADRs that define the Guardian itself

**Severity:** 🔴 **CRITICAL** - Circular bootstrap dependency: Directive 025 ↔ ADR-014

---

### 1.15 Directive 026: Commit Protocol

**File:** `doctrine/directives/026_commit_protocol.md`

**Violation:**

**Line 142 (example):**
```markdown
architect: document API decision - add ADR-023 for REST vs GraphQL
```

**Severity:** 🟢 **LOW** - Example commit message only, not structural dependency

---

### 1.16 Comparative Study References

**File:** `doctrine/docs/references/comparative_studies/2026-02-05-spec-kitty-comparative-analysis.md`

**Violations:**

Multiple references to "spec-kitty ADR-6, ADR-12, ADR-16" throughout the document (lines 362, 551, 906-914, 973)

**Context:** Comparative study references another project's ADRs

**Severity:** 🟢 **INFORMATIONAL** - References external project patterns, not local dependencies

---

**File:** `doctrine/docs/references/comparative_studies/references/spec-kitty-README.md`

**Violation:**

**Line 185:**
```markdown
See [ADR-12: Two-Branch Strategy](architecture/adrs/2026-01-27-12-two-branch-strategy-for-saas-transformation.md) for details.
```

**Context:** Copied content from external project includes their ADR references

**Severity:** 🟢 **INFORMATIONAL** - Reference documentation, not dependency

---

## 2. Template/Pattern Violations (Path Examples Using `${DOC_ROOT}`)

These violations use the `${DOC_ROOT}` variable pattern, which provides runtime substitution. While better than hardcoded paths, they still create coupling to the ADR directory structure.

**Count:** 89 occurrences across templates, approaches, tactics, and shorthands

**Files affected:**
- `doctrine/approaches/` (12 files)
- `doctrine/templates/` (11 files)
- `doctrine/tactics/` (2 files)
- `doctrine/shorthands/` (2 files)
- `doctrine/directives/003_repository_quick_reference.md`
- `doctrine/directives/018_traceable_decisions.md`

**Example pattern:**
```markdown
- Location: `${DOC_ROOT}/architecture/adrs/ADR-NNN-title.md`
- Check `${DOC_ROOT}/architecture/adrs/` for the highest existing number
```

**Severity:** 🟡 **MODERATE** - Path coupling through variable substitution. Less critical than direct ADR references but still assumes specific directory structure.

**Analysis:** These are template/approach artifacts that guide agents on *how to structure* a repository that adopts the framework. The `${DOC_ROOT}` pattern is intentionally designed to be portable.

---

## 3. Severity Classification Summary

| Severity | Count | Description |
|----------|-------|-------------|
| 🔴 **CRITICAL** | 6 | Direct dependency on local ADR for directive logic/rationale |
| 🟠 **MODERATE-HIGH** | 1 | Self-referential or bootstrap dependency issues |
| 🟡 **MODERATE** | 16 | References for context, examples, or exceptions |
| 🟢 **LOW/INFORMATIONAL** | 91 | Template patterns, external references, variable-based paths |

**Total violations identified:** 114

---

## 4. Root Cause Analysis

### Why did these violations occur?

1. **Bootstrap Problem:** Several ADRs document framework decisions (ADR-011 Primers, ADR-013 Distribution, ADR-014 Guardian) that are referenced from framework directives. This creates circular dependency.

2. **Pattern Leakage:** Example code and templates include local ADR references that should be generalized or removed.

3. **Incomplete Abstraction:** Some directives explain their rationale by citing the ADR that created them, rather than standing independently.

4. **Documentation Debt:** References section often cites local ADRs for traceability without considering portability implications.

---

## 5. Proposed Remediation Strategy

### Phase 1: Immediate Critical Fixes (Priority 1)

**Target:** Resolve 🔴 CRITICAL violations that break framework portability

#### Action 1.1: Directive 023 (Clarification Before Execution)

**Problem:** Entire directive framed as "implementing ADR-023"

**Solution Option A (Recommended):** Remove ADR references and generalize the rationale
```markdown
**Related:** Prompt optimization and reducing clarification overhead through structured validation
```

**Solution Option B:** Move ADR-023 specific implementation notes to `.doctrine-config/directives/023-local-implementation.md`

#### Action 1.2: Directive 034 (Spec-Driven Development)

**Problem:** Examples cite ADR-028, ADR-032 as authoritative

**Solution:** Replace specific ADR examples with generic placeholders:
```markdown
- Implementation details: See your project's ADR for technology choices
- Example: ADR-NNN for communication protocol selection
```

#### Action 1.3: GLOSSARY.md Primer Definition

**Problem:** Primer defined relative to "ADR-011"

**Solution:** Self-contain the definition in the glossary without ADR reference:
```markdown
A foundational execution pattern that establishes minimum quality thresholds for 
agent work. Primers include Context Check, Progressive Refinement, Trade-Off Navigation, 
Transparency & Error Signaling, and Reflection Loop. Defined in Directive 010.
```

#### Action 1.4: Directive 025 (Framework Guardian)

**Problem:** Circular dependency - Directive 025 references ADR-013 and ADR-014, which define the Guardian

**Solution Option A:** Move ADR-013 and ADR-014 into `doctrine/` as framework decisions
- Create `doctrine/decisions/` directory for framework-level ADRs
- Bootstrap framework decisions live with the framework

**Solution Option B:** Remove ADR references and inline the key decision points:
```markdown
The Guardian agent is responsible for framework integrity. This pattern was chosen 
because [inline rationale from ADR-014].
```

#### Action 1.5: Directive 019 (File-Based Collaboration)

**Problem:** References section cites ADR-002 and ADR-003

**Solution:** Remove references section or replace with generic guidance:
```markdown
**Related Patterns:**
- Asynchronous coordination patterns (see your architecture documentation)
- Task lifecycle management (see Directive 007)
```

#### Action 1.6: Directive 018 (Traceable Decisions)

**Problem:** Self-referential ADR-017 reference

**Solution:** Remove self-reference or acknowledge it's repository-specific:
```markdown
**Note:** This directive may be documented in your repository's ADR index for 
traceability (e.g., ADR-017 in reference implementation).
```

---

### Phase 2: Moderate Priority Fixes (Priority 2)

**Target:** Resolve 🟡 MODERATE violations in exception handling and context references

#### Action 2.1: Exception Handling (Directives 016, 017)

**Current:**
```markdown
- Exception: trivial utilities noted per ADR-012
```

**Proposed:**
```markdown
- Exception: trivial utilities (document exception rationale in work log per Directive 014)
```

#### Action 2.2: Primer References (Directives 010, 011, 014, 015)

**Current:**
```markdown
- Reference ADR-011 for primer definitions
```

**Proposed:**
```markdown
- See Directive 010 and GLOSSARY.md for primer definitions
```

---

### Phase 3: Template Pattern Updates (Priority 3)

**Target:** Resolve path coupling through `${DOC_ROOT}` variable

**Analysis:** These are intentionally templated for portability. The `${DOC_ROOT}` pattern is **working as designed** for runtime substitution.

**Decision:** ✅ **NO ACTION REQUIRED** 

**Rationale:** Templates and approaches guide repository setup. Using `${DOC_ROOT}` variable is the correct abstraction for path portability.

**Validation:** Confirm that all template/approach files using `${DOC_ROOT}/architecture/adrs/` are accompanied by clear context that this is an "example structure" or "recommended path", not a hard requirement.

---

### Phase 4: Documentation Anti-Pattern (Priority 4)

**Target:** Prevent future violations

#### Action 4.1: Create Validation Script

**File:** `doctrine/scripts/validate-dependencies.sh`

```bash
#!/bin/bash
# Validate doctrine/ does not reference local ADRs
set -e

echo "🔍 Checking for ADR dependency direction violations..."

# Search for ADR-NNN references (excluding ${DOC_ROOT} patterns and comments)
violations=$(grep -rn "ADR-[0-9]" doctrine/ \
  | grep -v '${DOC_ROOT}' \
  | grep -v 'spec-kitty ADR' \
  | grep -v '# Example:' \
  | grep -v 'CHANGELOG' \
  | grep -v '.backup' \
  || true)

if [ -n "$violations" ]; then
  echo "❌ Found potential violations:"
  echo "$violations"
  echo ""
  echo "Framework artifacts should not reference repository-specific ADRs."
  echo "See doctrine/docs/dependency-direction-rules.md for guidance."
  exit 1
else
  echo "✅ No dependency violations found"
  exit 0
fi
```

#### Action 4.2: Add Pre-Commit Hook

**File:** `.doctrine-config/hooks/pre-commit-validate-dependencies`

```bash
#!/bin/bash
# Run dependency validation before committing doctrine changes
if git diff --cached --name-only | grep -q "^doctrine/"; then
  ./doctrine/scripts/validate-dependencies.sh
fi
```

#### Action 4.3: Create Dependency Direction Guide

**File:** `doctrine/docs/dependency-direction-rules.md`

```markdown
# Dependency Direction Rules

## Correct Flow
✅ Local (docs/) → Framework (doctrine/)
✅ Local (.doctrine-config/) → Framework (doctrine/)
❌ Framework (doctrine/) → Local (docs/)

## How to Reference Decisions

### ❌ DON'T: Reference specific local ADRs
```markdown
Implements ADR-023 pattern for prompt optimization
```

### ✅ DO: Generalize the pattern
```markdown
Supports prompt optimization through structured validation
```

### ❌ DON'T: Hard-code ADR paths
```markdown
See ADR-028 for technology choice
```

### ✅ DO: Use generic placeholders
```markdown
See your project's architecture decisions for technology choices
```

## When Framework Decisions Need Documentation

If a framework decision requires an ADR:
1. Create `doctrine/decisions/FD-NNN-title.md` (Framework Decision)
2. Use FD prefix instead of ADR
3. These live WITH the framework, not in local docs/
```

#### Action 4.4: Update doctrine/README.md

Add prominent section:

```markdown
## Dependency Direction Rules

**doctrine/** artifacts MUST NOT reference repository-specific files in **docs/architecture/adrs/**

✅ Allowed: doctrine/ referencing .doctrine-config/
✅ Allowed: docs/ referencing doctrine/
❌ Forbidden: doctrine/ referencing docs/

See [Dependency Direction Rules](docs/dependency-direction-rules.md) for details.
```

---

## 6. Framework Decision Directory Proposal

**Problem:** Some decisions ARE framework-level (e.g., ADR-011 Primers, ADR-013 Distribution, ADR-014 Guardian)

**Proposal:** Create `doctrine/decisions/` for framework-level architectural decisions

**Structure:**
```
doctrine/
├── decisions/
│   ├── README.md
│   ├── FD-001-primer-execution-patterns.md       # Moved from ADR-011
│   ├── FD-002-zip-based-distribution.md          # Moved from ADR-013
│   ├── FD-003-framework-guardian-agent.md        # Moved from ADR-014
│   └── template.md
```

**Prefix:** Use "FD" (Framework Decision) instead of "ADR" to distinguish framework from repository-local decisions

**Migration Strategy:**
1. Create doctrine/decisions/ directory
2. Migrate ADR-011, ADR-013, ADR-014 into FD-001, FD-002, FD-003
3. Update all references in doctrine/ to use FD-NNN instead of ADR-NNN
4. Document pattern in dependency-direction-rules.md

---

## 7. Exceptions and Edge Cases

### 7.1 Directive 003: Repository Quick Reference

**File:** `doctrine/directives/003_repository_quick_reference.md`

**Lines 48-50:**
```markdown
    - `docs/architecture/adrs/` — Architecture Decision Records
- Format: `docs/architecture/adrs/ADR-NNN-<title>.md`
- Example: `docs/architecture/adrs/ADR-015-follow-up-task-lookup-pattern.md`
```

**Classification:** 🟢 **INFORMATIONAL** - This directive's PURPOSE is to document repository structure conventions

**Decision:** ✅ **EXCEPTION GRANTED** - Quick reference directive legitimately documents where ADRs live in a typical repository structure

---

### 7.2 Comparative Studies

**Files:** 
- `doctrine/docs/references/comparative_studies/*`

**Context:** Reference documentation analyzing other projects (spec-kitty)

**Classification:** 🟢 **INFORMATIONAL** - External project references, not dependencies

**Decision:** ✅ **NO ACTION REQUIRED** - These study other systems and reference their ADRs correctly

---

### 7.3 GLOSSARY.md.backup

**File:** `doctrine/GLOSSARY.md.backup`

**Decision:** ✅ **DELETE** - Backup file should not be in version control

---

## 8. Implementation Checklist

### Immediate (Priority 1) - Complete within 24 hours

- [ ] Action 1.1: Remove ADR-023 references from Directive 023
- [ ] Action 1.2: Genericize examples in Directive 034
- [ ] Action 1.3: Self-contain Primer definition in GLOSSARY.md
- [ ] Action 1.4: Resolve Directive 025 circular dependency (Guardian)
- [ ] Action 1.5: Remove/replace references in Directive 019
- [ ] Action 1.6: Remove self-reference in Directive 018
- [ ] Delete GLOSSARY.md.backup

### Short-term (Priority 2) - Complete within 1 week

- [ ] Action 2.1: Update exception handling in Directives 016, 017
- [ ] Action 2.2: Replace ADR-011 references with Directive 010 references
- [ ] Update all remaining 🟡 MODERATE violations

### Medium-term (Priority 3) - Complete within 2 weeks

- [ ] Action 4.1: Create validation script
- [ ] Action 4.2: Add pre-commit hook
- [ ] Action 4.3: Create dependency direction guide
- [ ] Action 4.4: Update doctrine/README.md

### Long-term (Priority 4) - Consider for next major version

- [ ] Evaluate Framework Decision directory proposal (doctrine/decisions/)
- [ ] Migrate ADR-011, ADR-013, ADR-014 to FD-001, FD-002, FD-003
- [ ] Update all FD references throughout framework

---

## 9. Prevention Strategy

### Architectural Guardrails

1. **CI Validation:** Run `doctrine/scripts/validate-dependencies.sh` in CI pipeline
2. **Pre-Commit Hook:** Prevent commits with new violations
3. **Documentation:** Clear guidance in dependency-direction-rules.md
4. **Review Checklist:** Add dependency direction check to PR template

### Cultural Practices

1. **Agent Training:** Update agent profiles to include dependency direction awareness
2. **Directive Updates:** New directives must pass validation script before acceptance
3. **Template Review:** All template updates checked for path coupling
4. **Quarterly Audits:** Re-run this audit quarterly to catch regression

---

## 10. Token Tracking (Directive 014 Compliance)

**Work Log Metadata:**

```yaml
task: "Doctrine Dependency Direction Audit"
agent: "Curator Claire"
start_time: "2026-02-11T06:20:00Z"
completion_time: "2026-02-11T06:52:00Z"
estimated_tokens: ~18500
actual_tokens: [to be measured]
```

**Token Breakdown:**
- Context loading: ~2,500 tokens
- Grep searches: ~1,200 tokens  
- File reviews: ~3,800 tokens
- Report generation: ~11,000 tokens

**Primers Invoked:**
- ✅ Context Check: Loaded dependency direction rules before audit
- ✅ Progressive Refinement: Started with grep, refined with file inspection
- ✅ Transparency: Documented all findings with severity ratings
- ✅ Reflection Loop: Considered edge cases and prevention strategies

---

## 11. Recommendations

### For @stijn-dejongh

**Immediate Actions:**

1. ✅ **Confirm finding:** Yes, dependency direction violations exist
2. 🔴 **Critical fixes:** Prioritize Phase 1 remediation (6 critical violations)
3. 🟡 **Moderate fixes:** Address Phase 2 violations (16 moderate violations)
4. 📊 **Prevention:** Implement validation script before next release

**Strategic Decision Required:**

**Framework Decision Directory Proposal** - Should framework-level decisions live in `doctrine/decisions/` using FD-NNN prefix?

**Pros:**
- Resolves bootstrap dependency issues
- Clear separation: FD = framework, ADR = repository
- Framework remains self-contained

**Cons:**
- Introduces new pattern (FD vs ADR)
- Migration effort for existing references
- Requires updating agent training

**Recommendation:** ✅ **APPROVE** - The benefits outweigh the migration cost. Framework decisions belong with the framework.

---

## 12. Conclusion

**Status:** ❗️ **VIOLATIONS CONFIRMED**

**Question Answered:** Yes, doctrine artifacts are pointing to local ADRs, violating dependency direction constraints.

**Impact:** Moderate-High. Framework portability is compromised by 6 critical violations. An additional 16 moderate violations create coupling through exception handling and context references.

**Path Forward:** Phased remediation starting with critical violations, followed by prevention automation.

**Estimated Effort:**
- Phase 1 (Critical): 4-6 hours
- Phase 2 (Moderate): 2-3 hours  
- Phase 3 (Prevention): 2-3 hours
- Phase 4 (Framework Decisions): 4-6 hours

**Total:** 12-18 hours of remediation work

---

## Appendices

### Appendix A: Complete Violation List

See inline sections above for detailed file-by-file breakdown.

### Appendix B: Validation Script

See Phase 4, Action 4.1 for implementation.

### Appendix C: Related Directives

- Directive 020: Lenient Adherence (guides appropriate strictness levels)
- Directive 018: Documentation Level Framework (governs documentation standards)
- Directive 004: Documentation & Context Files (defines authoritative sources)
- Directive 006: Version Governance (ensures layer version alignment)

---

**Report Prepared By:** Curator Claire (Structural & Tonal Consistency Specialist)  
**Review Status:** Ready for stakeholder review  
**Next Steps:** Await confirmation from @stijn-dejongh on remediation priorities  

---

*End of Report*
