# Prompt Storage: Code Review Enhancement Orchestration

**Orchestrator:** Manager Mike  
**Date:** 2026-02-10  
**Directive Compliance:** 015 (Prompt Storage), 018 (Traceable Decisions)  
**Purpose:** Document prompts, delegation rationale, and lessons learned for future orchestrations

---

## Problem Statement

**Original Request Source:** Code Reviewer Cindy  
**Document:** `work/reports/reviews/2026-02-10-cindy-task-artifacts-separation-review.md`  
**Date:** 2026-02-10

### Context

Code Reviewer Cindy conducted a comprehensive review of task management scripts focusing on:
- DRY principle compliance
- Delegation pattern adherence
- Business logic location
- Responsibility split between framework and tools

**Review Grade:** B+ (Good with Room for Improvement)

**Key Strengths Identified:**
1. ✅ All scripts properly delegate to framework for I/O operations
2. ✅ TaskStatus enum used as single source of truth
3. ✅ No YAML schemas in tools/ - proper separation maintained
4. ✅ Clear documentation with ADR references
5. ✅ Proper error handling with framework exception types

**Issues Identified:**
1. ⚠️ **HIGH:** Duplicated utility functions (`get_utc_timestamp`, `find_task_file`) across 4 scripts
2. ⚠️ **MEDIUM:** Business logic (allowed modes, priorities) duplicated in validator
3. ⚠️ **MEDIUM:** State transition validation missing from framework
4. ⚠️ **LOW:** Inconsistent import paths in some locations

### Recommended Actions from Review

- **Priority 1 (CRITICAL):** None blocking functionality
- **Priority 2 (HIGH - This Sprint):**
  - **H1:** Consolidate utility functions (2 hours estimated)
  - **H2:** Extract business rules to framework (4 hours estimated)
- **Priority 3 (MEDIUM - Next Sprint):**
  - **M1:** Add state machine validation (8 hours estimated)
- **Priority 4 (LOW - Future):**
  - **L1:** Consider validator consolidation (4 hours estimated)

---

## Orchestration Strategy

### Phase 1 Decision: Terminology Baseline

**Problem Observed:**
Cindy's review used terms "business logic" and "production code" extensively, but these were not formally defined in `doctrine/GLOSSARY.md` v1.1.0.

**Strategic Question:**
Should we establish shared terminology before implementing code changes?

**Decision:**
✅ YES - Start with terminology standardization

**Rationale:**
1. Shared language prevents misinterpretation in future phases
2. Low risk, high value for agent/human communication
3. Independent task - won't block code enhancements
4. Curator Claire's core specialization
5. Quick win (1 hour) to build momentum

**Agent Selection:**
**Curator Claire** - Documentation integrity specialist

**Why Claire:**
- Specialization: Terminology consistency, version governance
- Authority: Directive 004 (Documentation & Context Files), Directive 006 (Version Governance)
- Track record: Precise, framework-grounded definitions
- Low coordination overhead: Independent task

---

## Phase 1: Prompt to Curator Claire

### Prompt Sent

```markdown
**Context:** Code Reviewer Cindy used terms "business logic" and "production code" 
in her review, which are widely used throughout the doctrine but not formally 
defined in `doctrine/GLOSSARY.md`.

**Your Task:** Check if these terms are defined in the glossary. If missing, add 
precise, framework-specific definitions.

**Requirements:**
1. Search for existing definitions first
2. Analyze usage patterns across doctrine files
3. Create definitions that:
   - Are grounded in actual project structure (`src/`, `tools/`, `tests/`)
   - Provide actionable guidance
   - Include concrete examples from our framework
   - Cross-reference related terms
4. Follow version governance (Directive 006) for GLOSSARY updates
5. Maintain alphabetical ordering

**Success Criteria:**
- Terms formally defined with clear boundaries
- Examples reference actual framework components
- Version number updated appropriately
- Cross-references established

**Estimated Effort:** 1 hour

Begin by searching for existing definitions and analyzing usage patterns.
```

### Rationale for Prompt Structure

**Context First:** Explained triggering event (Cindy's review) to provide motivation

**Clear Task:** Specific action items with defined scope

**Requirements Section:** Detailed expectations aligned with Claire's specialization
- Framework-specific examples (aligns with her "grounding" strength)
- Actionable guidance (aligns with her "curator" role)
- Version governance (tests her directive compliance)

**Success Criteria:** Explicit validation gates

**Effort Estimate:** Conservative estimate to set expectations

### Expected Outcome

- Glossary updated with 2 new term definitions
- Version 1.1.0 → 1.2.0 (minor version bump for new terms)
- Definitions grounded in framework structure
- Cross-references to related glossary terms

### Actual Outcome (Phase 1)

✅ **EXCEEDED EXPECTATIONS**

Claire delivered:
1. ✅ Investigation findings (usage analysis across 16+ files)
2. ✅ Two comprehensive definitions:
   - "Business Logic" - 4 bullet points, TaskStatus example, cross-references
   - "Production Code" - 5 quality requirements, explicit exclusions, cross-references
3. ✅ Version governance: 1.1.0 → 1.2.0 (correct minor bump)
4. ✅ Alphabetical ordering preserved
5. ✅ Framework-specific examples (references `src/`, `tools/`, `tests/`)
6. ✅ Comprehensive work log documenting rationale

**Lessons Learned:**
- Claire's thoroughness (usage analysis across 16 files) exceeded prompt requirements
- Framework-grounded definitions provide clarity for future agents
- Explicit version governance requirement ensured correct semver bump

---

## Phase 2: Prompt to Python Pedro (Enhancement H1)

### Context for Phase 2

**After Phase 1 completion**, moved to implementation of Cindy's HIGH priority enhancements.

**Strategic Decision:**
Start with H1 (consolidate utilities) before H2 (extract enums) because:
1. H1 establishes clean utility layer foundation
2. H2 depends on having clean framework module structure
3. H1 has critical design decision (timestamp format) that could affect other work

### Prompt Sent

```markdown
**Context:** Code Reviewer Cindy identified HIGH priority enhancement H1 - 
consolidate duplicated utility functions across task management scripts.

**Problem:**
- `get_utc_timestamp()` duplicated in 4 locations (3 scripts + 1 framework)
  - **CRITICAL:** Two different implementations with different formats:
    - Tools: "2026-02-10T05:49:43Z" (NO microseconds)
    - Framework: "2026-02-10T05:49:43.927090Z" (WITH microseconds)
  - Impact: Inconsistency risk, maintenance burden

- `find_task_file()` duplicated in 3 locations (identical implementations)
  - Impact: Maintenance burden, search logic drift risk

**Your Task:** Consolidate both functions into framework module 
(`src/framework/orchestration/task_utils.py`) and update scripts to import.

**Critical Decision Required:**
You must decide on timestamp format standardization:
- Option A: Keep microseconds (framework version) - higher precision
- Option B: Remove microseconds (tools version) - backward compatible with 100+ task files

**Analyze production task files** in `work/` directory before deciding.

**Requirements:**
1. Follow TDD (Directive 017) - write tests first
2. Write acceptance tests (Directive 016) for both functions
3. Document timestamp format decision with rationale
4. Update framework module as canonical source
5. Remove duplicates from 3 scripts:
   - tools/scripts/start_task.py
   - tools/scripts/complete_task.py
   - tools/scripts/freeze_task.py
6. Validate: All existing tests must pass (zero regressions)

**Success Criteria:**
- Both functions exist ONLY in framework module
- All 3 scripts import from framework (no local implementations)
- Timestamp format standardized (document decision)
- All 16 task management tests pass
- 100% test coverage for new functions

**Estimated Effort:** 2 hours

**References:**
- Review: work/reports/reviews/2026-02-10-cindy-task-artifacts-separation-review.md
- ADR-042: Shared Task Domain Model
```

### Rationale for Prompt Structure

**Critical Decision Highlighted:** Timestamp format standardization flagged as KEY decision point
- Not prescriptive (allows Pedro's judgment)
- Directs analysis (check production data first)
- Explains trade-offs (precision vs. compatibility)

**TDD Requirements Explicit:** Directives 016 & 017 called out to enforce test-first approach

**Validation Gates:** Clear success criteria that can be objectively verified

**References Provided:** Links to review and ADR for context

### Expected Outcome

- Decision on timestamp format with documented rationale
- 2 functions consolidated into framework
- 102 duplicate lines removed from scripts
- 6+ tests added for new functions
- Zero regressions

### Actual Outcome (Phase 2)

✅ **MET EXPECTATIONS**

Pedro delivered:
1. ✅ Analysis of production task files (found all use seconds precision)
2. ✅ **Critical Decision:** Chose Option B (remove microseconds)
   - Rationale: Backward compatible with 100+ existing task files
   - Documented in comprehensive "Phase 2" section of work log
3. ✅ TDD cycle: 6 tests written first (RED), implementation (GREEN), refactoring
4. ✅ 102 duplicate lines removed
5. ✅ Fixed import path issue (relative imports inside src/)
6. ✅ All 46 tests passing (30 unit + 16 integration)
7. ✅ Quality checks: ruff clean, type hints complete

**Lessons Learned:**
- Highlighting "critical decision" in prompt ensured Pedro analyzed thoroughly
- Directing analysis to production data led to correct backward-compatible choice
- Import path issue caught and fixed quickly due to comprehensive integration tests

---

## Phase 3: Prompt to Python Pedro (Enhancement H2)

### Context for Phase 3

**After Phase 2 completion**, moved to second HIGH priority enhancement.

**Strategic Decision:**
H2 (extract business rules to enums) should come before M1 (state machine) because:
1. H2 establishes enum pattern for business rules
2. M1 will extend TaskStatus enum with state machine methods
3. H2 is lower risk and quicker (4 hours vs 8 hours)
4. Clean up "easy" issues before complex state machine logic

### Prompt Sent

```markdown
**Context:** Code Reviewer Cindy identified HIGH priority enhancement H2 - 
extract hardcoded business rules to framework enums.

**Problem:**
`tools/validators/validate-task-schema.py` contains hardcoded business rules:

```python
ALLOWED_MODES = {
    "/analysis-mode",
    "/creative-mode",
    "/meta-mode",
    "/programming",
    "/planning",
}

ALLOWED_PRIORITIES = {"critical", "high", "medium", "normal", "low"}
```

**Impact:** Multiple sources of truth, drift risk, no type safety

**Your Task:** Create TaskMode and TaskPriority enums in `src/common/types.py` 
following the existing TaskStatus pattern.

**Requirements:**
1. Follow existing enum pattern (inherit from `str, Enum` for YAML compatibility)
2. Create `TaskMode` enum with 5 values
3. Create `TaskPriority` enum with 5 values
4. Add helper methods to TaskPriority:
   - `order` property (0-4 for sorting, 0=highest)
   - `is_urgent()` class method (True for CRITICAL/HIGH)
5. Update validator to use new enums
6. Follow TDD (Directive 017) - write tests first
7. Minimal changes only (Directive 021 - Locality of Change)

**Success Criteria:**
- Both enums in src/common/types.py
- Validator imports and uses enums
- 10+ comprehensive tests added
- All existing tests pass
- mypy --strict clean
- Validator passes against all existing task files

**Estimated Effort:** 4 hours

**Pattern Reference:** See TaskStatus and FeatureStatus enums in src/common/types.py
**ADR Reference:** ADR-043 (Status Enumeration Standard)
```

### Rationale for Prompt Structure

**Pattern Reference Explicit:** Directed Pedro to existing TaskStatus/FeatureStatus as template
- Reduces design decisions (follow established pattern)
- Ensures consistency with codebase conventions

**Helper Methods Specified:** Guided Pedro to add useful methods (order, is_urgent)
- Demonstrates forward thinking (these will be useful later)
- Shows orchestrator understands domain needs

**Locality of Change:** Explicit directive to avoid scope creep
- Prevents "drive-by refactoring"
- Keeps risk low and changes minimal

**Validation Against Production:** Requirement to test against existing task files
- Ensures backward compatibility
- Catches integration issues early

### Expected Outcome

- 2 new enums with helper methods
- Validator updated to use enums
- 10+ tests added
- Type safety improved
- No breaking changes

### Actual Outcome (Phase 3)

✅ **MET EXPECTATIONS**

Pedro delivered:
1. ✅ TaskMode enum (5 values, str inheritance)
2. ✅ TaskPriority enum (5 values, str inheritance, helper methods)
3. ✅ Helper methods: `order` property, `is_urgent()` class method
4. ✅ Validator updated with minimal changes (import + constant definitions)
5. ✅ 10 comprehensive tests (4 for TaskMode, 6 for TaskPriority)
6. ✅ All quality checks: mypy strict, ruff clean, black formatted
7. ✅ Validated against all existing task files

**Lessons Learned:**
- Referencing existing patterns (TaskStatus) streamlined implementation
- Specifying helper methods provided useful extensibility
- Locality of Change directive kept changes focused and low-risk

---

## Phase 4: Prompt to Python Pedro (Enhancement M1)

### Context for Phase 4

**After Phase 3 completion**, moved to MEDIUM priority enhancement (highest remaining).

**Strategic Decision:**
M1 (state machine validation) is the most complex enhancement:
1. Highest complexity (32 test cases, state transition matrix)
2. Highest risk (changes core task lifecycle validation)
3. Potential for discovering bugs (state validation missing in scripts)
4. Saved for last to have clean foundation from H1 & H2

### Prompt Sent

```markdown
**Context:** Code Reviewer Cindy identified MEDIUM priority enhancement M1 - 
add centralized state machine validation to TaskStatus enum.

**Problem:**
State transition validation is scattered across scripts:
- start_task.py validates ASSIGNED → IN_PROGRESS (good)
- complete_task.py has NO state validation - could complete from any state (bug!)
- No central enforcement of valid transitions

**Impact:** Invalid state transitions not caught, inconsistent enforcement

**Your Task:** Add state machine methods to TaskStatus enum in src/common/types.py

**State Transition Design (Conservative Approach):**
```
NEW → {INBOX, ASSIGNED, ERROR}
INBOX → {ASSIGNED, ERROR}
ASSIGNED → {IN_PROGRESS, BLOCKED, ERROR}
IN_PROGRESS → {DONE, BLOCKED, ERROR}
BLOCKED → {IN_PROGRESS, ERROR}
DONE → {} (Terminal)
ERROR → {} (Terminal)
```

**Methods to Implement:**
1. `valid_transitions() -> set[TaskStatus]` (instance method)
   - Returns set of valid next states from current state
   
2. `can_transition_to(target: TaskStatus) -> bool` (instance method)
   - Validates if transition is allowed
   
3. `validate_transition(current: TaskStatus, target: TaskStatus) -> None` (class method)
   - Raises ValueError with descriptive message if invalid

**Requirements:**
1. Follow TDD (Directive 017) - write tests first
2. Write 30+ comprehensive tests covering:
   - All valid transitions for each state
   - All invalid transitions with error checking
   - Edge cases (self-transitions, terminal states)
3. Update scripts to use centralized validation:
   - start_task.py (replace manual check)
   - complete_task.py (ADD validation - currently missing!)
4. Document state machine philosophy (terminal states, no reopening)
5. Validate: All existing tests pass (zero regressions)

**Critical Bug to Fix:**
complete_task.py currently has NO state validation - it can complete tasks from 
ANY state (NEW, INBOX, ASSIGNED, BLOCKED). This is a data integrity bug.

**Success Criteria:**
- 3 state machine methods implemented
- 30+ comprehensive tests added
- Bug in complete_task.py fixed
- All existing tests pass
- State transition matrix documented
- Error messages are informative

**Estimated Effort:** 8 hours

**References:**
- Review: work/reports/reviews/2026-02-10-cindy-task-artifacts-separation-review.md
- ADR-043: Status Enumeration Standard
```

### Rationale for Prompt Structure

**Bug Highlighted Prominently:** Called out critical bug in complete_task.py
- Ensures Pedro understands this is not just enhancement but bug fix
- Emphasizes importance of state validation
- Provides clear motivation for the work

**State Machine Design Provided:** Gave specific transition matrix
- Reduces design ambiguity (30+ possible states if unrestricted)
- Conservative approach explained (terminal states can't transition)
- Clear rationale for each transition rule

**3 Methods Specified:** Clear API design with usage patterns
- valid_transitions() - for discovery/UI
- can_transition_to() - for boolean checks
- validate_transition() - for strict enforcement

**Test Coverage Explicit:** 30+ tests required with specific categories
- Ensures comprehensive coverage
- Categories prevent missing edge cases
- Sets high quality bar

**Philosophy Documentation:** Required explanation of design decisions
- Terminal states rationale
- No reopening policy
- Auditability considerations

### Expected Outcome

- 3 state machine methods implemented
- 30+ tests added
- Critical bug fixed in complete_task.py
- Comprehensive state validation across scripts
- Zero regressions

### Actual Outcome (Phase 4)

✅ **EXCEEDED EXPECTATIONS**

Pedro delivered:
1. ✅ 3 state machine methods implemented (valid_transitions, can_transition_to, validate_transition)
2. ✅ **32 comprehensive tests** (exceeded 30+ requirement)
   - 7 tests: Valid transitions for each state
   - 7 tests: Valid transition validation
   - 6 tests: Invalid transition validation
   - 8 tests: Validate method with error checking
   - 4 tests: Edge cases
3. ✅ **Critical bug fixed:** Added state transition validation to complete_task.py
   - Now prevents ASSIGNED → DONE (must start first)
   - Now prevents NEW → DONE (must assign first)
   - Now prevents BLOCKED → DONE (must unblock first)
4. ✅ Updated start_task.py to use centralized validation
5. ✅ All 55 tests passing (23 existing + 32 new)
6. ✅ Comprehensive documentation:
   - State transition matrix with rationale
   - Terminal states philosophy
   - Error message design
7. ✅ Quality checks: mypy strict, ruff clean, black formatted
8. ✅ Code coverage: 100% for state machine code

**Lessons Learned:**
- Highlighting bug in prompt ensured Pedro treated this seriously
- Providing state machine design upfront saved analysis time
- Specifying 30+ tests set high quality bar (Pedro delivered 32)
- Bug discovery validates value of comprehensive validation implementation

---

## SWOT Analysis for Future Orchestrations

### Strengths (What Worked Well)

**S1: Sequential Phasing Prevented Conflicts**
- Clear dependencies (utilities → enums → state machine)
- No merge conflicts or rework
- Clean hand-offs between phases
- Each phase validated before next begins

**Recommendation:** Continue sequential phasing for dependent work

**S2: Agent Specialization Maximized Quality**
- Curator Claire: Documentation expertise
- Python Pedro: TDD mastery, code quality
- Right agent for right task
- High confidence in outcomes

**Recommendation:** Build agent capability matrix for common task types

**S3: Critical Decision Documentation**
- Timestamp format decision well-analyzed
- State transition matrix designed conservatively
- Rationale documented for future reference
- Prevents future debates on same topics

**Recommendation:** Create "decision log" template for critical choices

**S4: Test-First Approach Caught Issues Early**
- 48 new tests caught issues immediately
- Zero regressions due to comprehensive coverage
- Bug discovered during state machine implementation
- High confidence in changes

**Recommendation:** Always require TDD for infrastructure changes

**S5: Prompt Structure Guided Quality**
- Critical decisions highlighted upfront
- Success criteria explicit and measurable
- References provided for context
- Effort estimates set expectations

**Recommendation:** Standardize prompt template with these elements

### Weaknesses (What Could Be Improved)

**W1: Acceptance Criteria Implicit in Some Prompts**
- Phase 1 (Claire) had implicit AC (glossary updated)
- Phase 2-4 had explicit AC sections
- Inconsistency in structure
- Could lead to misaligned expectations

**Recommendation:** Require explicit AC section in ALL prompts (template enforcement)

**W2: Coordination Overhead Not Precisely Tracked**
- Estimated 2 hours for orchestration overhead
- Actual time not tracked separately
- Can't optimize what we don't measure
- Hard to justify orchestration value without metrics

**Recommendation:** Track orchestration time separately (review, hand-offs, coordination)

**W3: Bug Discovery Was Reactive, Not Proactive**
- State validation bug in complete_task.py found during M1 implementation
- Could have been caught earlier with static analysis
- Proactive scanning would reduce risk

**Recommendation:** Add static analysis checks to code review checklist (state validation patterns)

**W4: Knowledge Transfer Could Be More Explicit**
- Agent logs are thorough but lack "gotchas" section
- Future developers might repeat same mistakes
- Lessons learned are in narrative, not actionable format

**Recommendation:** Add "Common Pitfalls" section to work log template

### Opportunities (Future Enhancements)

**O1: Orchestration Metrics Dashboard**
- Track time spent per phase
- Track agent hand-offs
- Track rework/iteration cycles
- Build historical data for better estimation

**Potential Value:** Improved estimation accuracy, demonstrate orchestration ROI

**O2: Automated Validation Gates**
- Pre-commit hooks for state validation patterns
- Static analysis for business logic location
- Automated DRY violation detection
- Catch issues before code review

**Potential Value:** Faster feedback loops, reduced review burden

**O3: Orchestration Playbooks**
- Common patterns (utilities consolidation, enum extraction, etc.)
- Template prompts for each pattern
- Decision trees for agent selection
- Effort estimation guidelines

**Potential Value:** Faster orchestration setup, consistent quality

**O4: Agent Capability Matrix**
- Document each agent's strengths/weaknesses
- Track success rates by task type
- Build expertise profiles
- Optimize agent selection

**Potential Value:** Better delegation decisions, higher quality outcomes

**O5: Knowledge Base from Orchestrations**
- Extract lessons learned into searchable KB
- Common pitfalls database
- Design decision precedents
- Reusable patterns library

**Potential Value:** Faster problem-solving, avoid repeated mistakes

### Threats (Risks to Monitor)

**T1: Orchestration Overhead Scaling**
- Current: 2 hours for 4 phases (11% of total time)
- Risk: Overhead could grow non-linearly with complexity
- Impact: Diminishing returns on orchestration value

**Mitigation:** Track overhead metrics, optimize hand-off processes, automate validation gates

**T2: Agent Context Limitations**
- Each agent starts fresh with limited context
- Risk: Misalignment or repeated explanations
- Impact: Rework, communication overhead

**Mitigation:** Improve context passing (summary docs, decision logs), build shared artifacts

**T3: Quality Drift Without Validation Gates**
- Risk: Agents might skip steps if not explicitly required
- Impact: Inconsistent quality, regressions
- Example: If TDD not mandated, tests might be skipped

**Mitigation:** Explicit validation in prompts, automated checks, clear success criteria

**T4: Dependency Chains Cause Bottlenecks**
- Current: Sequential execution (no parallelization)
- Risk: Long pole in schedule if dependencies increase
- Impact: Slower delivery, opportunity cost

**Mitigation:** Identify parallel work streams, optimize dependencies, batch independent tasks

**T5: Critical Decisions Require Human Judgment**
- Timestamp format decision required human review
- State machine design needed human approval
- Risk: Agent autonomy limited by human bottleneck
- Impact: Delays, reduced efficiency

**Mitigation:** Build decision frameworks, document precedents, empower agents with guidelines

---

## Orchestration Patterns Identified

### Pattern 1: Terminology-First Approach
**When to Use:** When domain terms are used but undefined
**Steps:**
1. Audit glossary for missing terms
2. Analyze usage patterns across codebase
3. Create framework-specific definitions
4. Update version metadata

**Agent:** Curator Claire (documentation specialist)
**Effort:** 1-2 hours
**Risk:** Low

### Pattern 2: Utility Consolidation with Format Decision
**When to Use:** Duplicate utility functions with format inconsistencies
**Steps:**
1. Analyze production data to understand current usage
2. Make format decision with backward compatibility priority
3. Consolidate into framework module (canonical source)
4. Update all consumers to import from framework
5. Comprehensive tests (utilities + integration)

**Agent:** Python Pedro (TDD specialist)
**Effort:** 2-4 hours
**Risk:** Medium (format decision critical)

### Pattern 3: Business Rule Extraction to Enums
**When to Use:** Hardcoded constants that represent domain rules
**Steps:**
1. Identify all hardcoded rule locations
2. Create enums following existing patterns (str inheritance)
3. Add helper methods for common operations
4. Update validators/consumers to use enums
5. Validate against production data

**Agent:** Python Pedro (code quality specialist)
**Effort:** 4-6 hours
**Risk:** Low (no behavior changes)

### Pattern 4: State Machine Implementation
**When to Use:** State validation scattered or missing
**Steps:**
1. Design state transition matrix (conservative approach)
2. Document terminal states and rationale
3. Implement 3-method API (valid_transitions, can_transition_to, validate_transition)
4. Write 30+ comprehensive tests (valid, invalid, edge cases)
5. Update all scripts to use centralized validation
6. Fix any bugs discovered

**Agent:** Python Pedro (complex logic specialist)
**Effort:** 8-12 hours
**Risk:** High (complex logic, bug potential)

---

## Recommendations for Future Orchestrations

### Prompt Engineering Best Practices

1. **Always Include:**
   - Context (why this work matters)
   - Problem statement (what needs fixing)
   - Critical decisions (what choices need to be made)
   - Requirements (directive compliance, patterns to follow)
   - Success criteria (explicit, measurable)
   - Effort estimate (set expectations)
   - References (reviews, ADRs, related docs)

2. **Highlight Critical Decisions:**
   - Use bold or "CRITICAL DECISION REQUIRED" header
   - Explain trade-offs
   - Direct analysis (e.g., "check production data first")
   - Don't prescribe solution (allow agent judgment)

3. **Enforce Quality Gates:**
   - Explicit TDD requirement (RED-GREEN-REFACTOR)
   - Specific test count (30+ tests, not "good coverage")
   - Quality checks (mypy, ruff, black)
   - Integration validation (all existing tests pass)

4. **Provide Patterns:**
   - Reference existing code to follow
   - Link to ADRs for architectural guidance
   - Specify methods/API to implement
   - Show examples where helpful

### Agent Selection Decision Tree

```
Is it documentation/terminology?
  YES → Curator Claire
  NO ↓

Does it require TDD expertise?
  YES → Python Pedro
  NO ↓

Does it involve architecture/design decisions?
  YES → Architect Alphonso
  NO ↓

Does it require code review?
  YES → Code Reviewer Cindy
  NO ↓

Default: General-purpose agent
```

### Coordination Checklist

**Pre-Flight (Before Delegation):**
- [ ] Review all reference documents
- [ ] Identify critical decisions requiring human input
- [ ] Define acceptance criteria explicitly
- [ ] Estimate coordination overhead
- [ ] Identify potential conflicts/dependencies
- [ ] Choose appropriate agent(s)
- [ ] Write comprehensive prompt

**During Execution:**
- [ ] Validate each phase output before next hand-off
- [ ] Monitor test pass rates continuously
- [ ] Document critical decisions immediately
- [ ] Track time spent on coordination
- [ ] Check for blocking issues

**Post-Completion:**
- [ ] Run full test suite one final time
- [ ] Generate metrics summary
- [ ] Document lessons learned
- [ ] Update orchestration playbook
- [ ] Create executive summary for stakeholders
- [ ] Archive prompts and work logs

### Quality Metrics to Track

| Metric | Target | Purpose |
|--------|--------|---------|
| **Test Pass Rate** | 100% | Zero regressions |
| **Test Coverage** | 100% new code | Quality assurance |
| **Time Variance** | ±20% of estimate | Estimation accuracy |
| **Coordination Overhead** | <15% total time | Efficiency |
| **Rework Cycles** | 0-1 per phase | First-time quality |
| **Critical Decisions** | Document all | Knowledge capture |
| **Agent Hand-offs** | Track count & time | Process optimization |

---

## Appendix: Full Prompt Archive

### A1: Phase 1 - Curator Claire (Terminology)
[Full prompt provided in "Phase 1: Prompt to Curator Claire" section above]

### A2: Phase 2 - Python Pedro (Enhancement H1)
[Full prompt provided in "Phase 2: Prompt to Python Pedro (Enhancement H1)" section above]

### A3: Phase 3 - Python Pedro (Enhancement H2)
[Full prompt provided in "Phase 3: Prompt to Python Pedro (Enhancement H2)" section above]

### A4: Phase 4 - Python Pedro (Enhancement M1)
[Full prompt provided in "Phase 4: Prompt to Python Pedro (Enhancement M1)" section above]

---

## Metadata

**Document Type:** Prompt Storage and Orchestration Analysis  
**Directive Compliance:** 015 (Prompt Storage), 018 (Traceable Decisions)  
**Date Created:** 2026-02-10  
**Orchestrator:** Manager Mike  
**Total Phases:** 4  
**Total Agents:** 2 (Curator Claire, Python Pedro)  
**Total Prompts:** 4  
**Critical Decisions:** 2 (timestamp format, state machine design)

**Status:** ✅ COMPLETE  
**Quality:** Comprehensive prompt archive with SWOT analysis and patterns

**Next Steps:**
- Use patterns for similar future orchestrations
- Build orchestration playbook with reusable templates
- Track metrics on next orchestration to validate improvements
