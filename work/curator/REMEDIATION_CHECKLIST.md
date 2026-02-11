# Remediation Checklist: Doctrine Dependency Violations

**Date:** 2026-02-11  
**Based on:** [Full Report](2026-02-11-doctrine-dependency-violations-report.md)  
**Validation:** Run `bash work/curator/validate-dependencies.sh` after each phase

---

## Phase 1: Critical Fixes (Priority 1) ⏰ 4-6 hours

### [ ] 1.1 - Directive 023 (Clarification Before Execution)
**File:** `doctrine/directives/023_clarification_before_execution.md`

- [ ] Line 9: Remove "Related: ADR-023" reference
  - Replace with: "Related: Prompt optimization and reducing clarification overhead"
- [ ] Line 11: Remove "from ADR-023" text
- [ ] Line 86: Remove "Phase 2 of ADR-023" reference
- [ ] Line 141: Remove ADR-023 link from references section

**Test:** `grep -n "ADR-023" doctrine/directives/023_clarification_before_execution.md` should return nothing

---

### [ ] 1.2 - Directive 034 (Spec-Driven Development)
**File:** `doctrine/directives/034_spec_driven_development.md`

- [ ] Line 305: Remove "**ADR (ADR-032):**"
  - Replace with generic placeholder or remove section
- [ ] Lines 457-460: Replace ADR-028 reference
  - Change to: "See your project's ADR for technology choices (e.g., WebSocket library selection)"

**Test:** `grep -n "ADR-028\|ADR-032" doctrine/directives/034_spec_driven_development.md` should return nothing

---

### [ ] 1.3 - GLOSSARY.md (Primer Definition)
**File:** `doctrine/GLOSSARY.md`

- [ ] Find Primer entry (around line 2461)
- [ ] Remove ADR-011 reference from definition
  - Replace with: "Defined in Directive 010 (Mode Protocol) and Directive 011"
- [ ] Update any other ADR-003 references to use Directive numbers instead

**Test:** `grep -n "ADR-011\|ADR-003" doctrine/GLOSSARY.md` should return nothing

---

### [ ] 1.4 - Directive 019 (File-Based Collaboration)
**File:** `doctrine/directives/019_file_based_collaboration.md`

- [ ] Lines 120-121: Remove references section with ADR-002, ADR-003
  - Option A: Delete references section
  - Option B: Replace with: "See Directive 007 (Task Lifecycle) and Directive 008 (Async Coordination)"

**Test:** `grep -n "ADR-002\|ADR-003" doctrine/directives/019_file_based_collaboration.md` should return nothing

---

### [ ] 1.5 - Directive 025 (Framework Guardian) ⚠️ COMPLEX
**File:** `doctrine/directives/025_framework_guardian.md`

**Decision Required:** Choose Option A or B

#### Option A: Inline Decision Content
- [ ] Line 283: Remove "Per ADR-011" reference
- [ ] Lines 293-294: Remove ADR-013, ADR-014 references
  - Inline key decision points into directive text

#### Option B: Create Framework Decisions (Recommended)
- [ ] Create `doctrine/decisions/` directory
- [ ] Migrate ADR-013 → FD-002 (Zip-Based Distribution)
- [ ] Migrate ADR-014 → FD-003 (Framework Guardian)
- [ ] Update references to use FD-NNN instead of ADR-NNN

**Test:** `grep -n "ADR-013\|ADR-014" doctrine/directives/025_framework_guardian.md` should return nothing OR valid FD references

---

### [ ] 1.6 - Directive 018 (Traceable Decisions)
**File:** `doctrine/directives/018_traceable_decisions.md`

- [ ] Line 188: Remove "ADR-017: Self-referential" entry
  - Replace with: "This directive may be documented in your repository's ADR index (e.g., ADR-017 in reference implementation)"

**Test:** `grep -n "ADR-017" doctrine/directives/018_traceable_decisions.md` should return nothing OR generic example only

---

### [ ] 1.7 - Delete Backup File
**File:** `doctrine/GLOSSARY.md.backup`

- [ ] Delete file (should not be in version control)

**Command:** `rm doctrine/GLOSSARY.md.backup`

---

### [ ] Phase 1 Validation
- [ ] Run: `bash work/curator/validate-dependencies.sh`
- [ ] Expected: 0 critical violations (all 🔴 resolved)
- [ ] Violations remaining: ~54 (moderate + agent profiles)

---

## Phase 2: Moderate Fixes (Priority 2) ⏰ 2-3 hours

### [ ] 2.1 - Exception Handling Pattern

#### Files to Update:
- [ ] `doctrine/directives/016_acceptance_test_driven_development.md` (Line 12)
- [ ] `doctrine/directives/017_test_driven_development.md` (Lines 13, 83)

**Change:**
```markdown
# OLD:
- Exception: trivial utilities noted per ADR-012

# NEW:
- Exception: trivial utilities (document rationale in work log per Directive 014)
```

**Test:** `grep -n "ADR-012" doctrine/directives/016*.md doctrine/directives/017*.md` should return nothing

---

### [ ] 2.2 - Primer Reference Updates

#### Files to Update:
- [ ] `doctrine/directives/010_mode_protocol.md` (Line 43)
- [ ] `doctrine/directives/011_risk_escalation.md` (Line 21)
- [ ] `doctrine/directives/014_worklog_creation.md` (Line 122)
- [ ] `doctrine/directives/015_store_prompts.md` (Line 83)

**Change:**
```markdown
# OLD:
see ADR-011 / Reference ADR-011 / per ADR-011

# NEW:
see Directive 010 and GLOSSARY.md for primer definitions
```

**Test:** `grep -n "ADR-011" doctrine/directives/*.md` should return nothing

---

### [ ] 2.3 - Directive 036 (Boy Scout Rule)
**File:** `doctrine/directives/036_boy_scout_rule.md`

- [ ] Lines 393, 401: Remove ADR-043 references from examples
- [ ] Lines 419, 428, 433, 441: Remove ADR-001 references
  - These are EXAMPLES of broken links, can be genericized

**Change:**
```markdown
# OLD:
See [ADR-001](../adrs/ADR-001.md) for details.

# NEW:
See [Architecture Decision](../docs/architecture/adrs/ADR-NNN.md) for details.
```

**Test:** `grep -n "ADR-001\|ADR-043" doctrine/directives/036_boy_scout_rule.md` should return nothing OR generic examples only

---

### [ ] 2.4 - Directive 026 (Commit Protocol)
**File:** `doctrine/directives/026_commit_protocol.md`

- [ ] Line 62: Update example commit message
  - This is LOW priority - just an example

**Change:**
```markdown
# OLD:
architect: document API decision - add ADR-023 for REST vs GraphQL

# NEW:
architect: document API decision - add ADR-NNN for REST vs GraphQL
```

**Test:** Not critical - example only

---

### [ ] 2.5 - Directive 035 (Specification Frontmatter)
**File:** `doctrine/directives/035_specification_frontmatter_standards.md`

- [ ] Line 24: Remove "(ADR-037)" reference
- [ ] Line 582: Remove "ADR-037:" reference
  - Replace with generic context or remove

**Test:** `grep -n "ADR-037" doctrine/directives/035_specification_frontmatter_standards.md` should return nothing

---

### [ ] 2.6 - Agent Profile Boilerplate (23 files)

**Batch Update Required:**

All files in `doctrine/agents/*.agent.md` contain:
```markdown
**Primer Requirement:** Follow the Primer Execution Matrix (ADR-011) defined in Directive 010
```

**Change to:**
```markdown
**Primer Requirement:** Follow the Primer Execution Matrix defined in Directive 010 and documented in GLOSSARY.md
```

**Files:**
- [ ] architect.agent.md
- [ ] backend-dev.agent.md
- [ ] bootstrap-bill.agent.md
- [ ] build-automation.agent.md
- [ ] curator.agent.md
- [ ] diagrammer.agent.md
- [ ] framework-guardian.agent.md
- [ ] frontend.agent.md
- [ ] lexical.agent.md
- [ ] manager.agent.md
- [ ] project-planner.agent.md
- [ ] python-pedro.agent.md
- [ ] researcher.agent.md
- [ ] scribe.agent.md
- [ ] synthesizer.agent.md
- [ ] translator.agent.md
- [ ] writer-editor.agent.md
- [ ] (and any others in doctrine/agents/)

**Test Command:**
```bash
grep -l "ADR-011" doctrine/agents/*.agent.md | wc -l
# Should return 0 after updates
```

---

### [ ] 2.7 - Framework Guardian Agent
**File:** `doctrine/agents/framework-guardian.agent.md`

- [ ] Line 174: Remove ADR-013/014 reference
- [ ] Lines 189-190: Update references section
  - If using Framework Decisions: change to FD-002, FD-003
  - If not: remove or genericize

---

### [ ] 2.8 - Python Pedro Agent
**File:** `doctrine/agents/python-pedro.agent.md`

- [ ] Lines 186, 194: Remove ADR-015 references (these are examples)

---

### [ ] Phase 2 Validation
- [ ] Run: `bash work/curator/validate-dependencies.sh`
- [ ] Expected: ~3-5 violations remaining (approaches/examples only)

---

## Phase 3: Prevention (Priority 3) ⏰ 2-3 hours

### [ ] 3.1 - Move Validation Script
- [ ] Copy `work/curator/validate-dependencies.sh` to `doctrine/scripts/`
- [ ] Make executable: `chmod +x doctrine/scripts/validate-dependencies.sh`
- [ ] Test from root: `./doctrine/scripts/validate-dependencies.sh`

---

### [ ] 3.2 - Create Dependency Direction Guide
- [ ] Create: `doctrine/docs/dependency-direction-rules.md`
- [ ] Content: See report Section 4.3 for full template
- [ ] Include: ✅ DO / ❌ DON'T examples

---

### [ ] 3.3 - Update doctrine/README.md
- [ ] Add "Dependency Direction Rules" section
- [ ] Link to guide
- [ ] Explain FD vs ADR distinction (if using Framework Decisions)

---

### [ ] 3.4 - Create Pre-Commit Hook Template
- [ ] Create: `.doctrine-config/hooks/pre-commit-validate-dependencies`
- [ ] Content: See report Section 4.2 for template
- [ ] Document in .doctrine-config/README.md

---

### [ ] 3.5 - Add CI Validation
**File:** `.github/workflows/doctrine-validation.yml` (create if needed)

```yaml
name: Doctrine Validation
on: [push, pull_request]
jobs:
  validate-dependencies:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check dependency direction
        run: bash doctrine/scripts/validate-dependencies.sh
```

---

### [ ] Phase 3 Validation
- [ ] Trigger CI build
- [ ] Confirm validation runs
- [ ] Test pre-commit hook locally

---

## Phase 4: Framework Decisions (Priority 4) ⏰ 4-6 hours

**Decision Required:** Approve Framework Decision pattern before proceeding

### [ ] 4.1 - Create Framework Decision Directory
- [ ] Create: `doctrine/decisions/`
- [ ] Create: `doctrine/decisions/README.md` (explain FD vs ADR)
- [ ] Create: `doctrine/decisions/template.md` (based on ADR template)

---

### [ ] 4.2 - Migrate Framework Decisions

#### [ ] FD-001: Primer Execution Patterns
- [ ] Copy content from ADR-011
- [ ] Adapt context to framework scope
- [ ] Update title: "Framework Decision 001: Primer Execution Patterns"
- [ ] File: `doctrine/decisions/FD-001-primer-execution-patterns.md`

#### [ ] FD-002: Zip-Based Distribution
- [ ] Copy content from ADR-013
- [ ] Adapt context to framework scope
- [ ] File: `doctrine/decisions/FD-002-zip-based-distribution.md`

#### [ ] FD-003: Framework Guardian Agent
- [ ] Copy content from ADR-014
- [ ] Adapt context to framework scope
- [ ] File: `doctrine/decisions/FD-003-framework-guardian-agent.md`

---

### [ ] 4.3 - Update All References
- [ ] Search: `grep -r "ADR-011" doctrine/`
  - Replace with: `FD-001` where applicable
- [ ] Search: `grep -r "ADR-013" doctrine/`
  - Replace with: `FD-002`
- [ ] Search: `grep -r "ADR-014" doctrine/`
  - Replace with: `FD-003`

**Note:** Some references may be examples/approaches that reference repository-local ADRs - those should remain as examples, not changed to FD-NNN

---

### [ ] 4.4 - Update Validation Script
- [ ] Add exception for FD-NNN pattern in validation script
- [ ] Test: References to FD-001, FD-002, FD-003 should NOT trigger violations

---

### [ ] Phase 4 Validation
- [ ] Run: `bash doctrine/scripts/validate-dependencies.sh`
- [ ] Expected: 0 violations (or only intentional examples)
- [ ] All framework artifacts use FD-NNN, not ADR-NNN

---

## Final Validation

### [ ] Complete System Check
```bash
# Should pass cleanly:
bash doctrine/scripts/validate-dependencies.sh

# Should return 0 or only intentional examples:
grep -r "ADR-[0-9]" doctrine/ | grep -v '${DOC_ROOT}' | grep -v 'spec-kitty' | grep -v 'Example:' | wc -l
```

### [ ] Documentation Review
- [ ] Dependency direction guide created
- [ ] doctrine/README.md updated
- [ ] .doctrine-config/README.md updated (if using hooks)
- [ ] CI pipeline configured

### [ ] Training Materials
- [ ] Update agent training to mention dependency direction
- [ ] Add to onboarding checklist
- [ ] Document in contribution guidelines

---

## Rollback Plan

If issues arise during remediation:

1. **Git Branch:** Create `fix/doctrine-dependency-violations` branch before starting
2. **Checkpoint Commits:** Commit after each phase
3. **Validation:** Run validation script after each file change
4. **Rollback:** `git revert` or `git reset` to last known good state

---

## Success Criteria

- [ ] Validation script passes with 0 violations
- [ ] All 🔴 critical violations resolved
- [ ] All 🟡 moderate violations resolved
- [ ] Prevention automation in place (CI + hooks)
- [ ] Documentation updated
- [ ] Framework Decision pattern documented (if approved)

---

## Effort Tracking

| Phase | Estimated | Actual | Notes |
|-------|-----------|--------|-------|
| Phase 1 | 4-6h | | |
| Phase 2 | 2-3h | | |
| Phase 3 | 2-3h | | |
| Phase 4 | 4-6h | | |
| **Total** | **12-18h** | | |

---

**Next Step:** Review with @stijn-dejongh and obtain approval to proceed

**Questions?** See [Full Report](2026-02-11-doctrine-dependency-violations-report.md) for detailed analysis and rationale
