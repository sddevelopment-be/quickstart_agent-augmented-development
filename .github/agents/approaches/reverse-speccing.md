# Approach: Reverse Speccing (Test-to-System Reconstruction)

**Category:** Quality Validation  
**Status:** Active  
**Version:** 1.0.0  
**Created:** 2026-02-08  
**Source:** work/reports/benchmarks/agent-test-validation-experiment-report.md  
**Related:** Test Readability and Clarity Check Approach

---

## Overview

**Reverse Speccing** is a dual-agent validation technique that reconstructs system understanding purely from test code, then compares that reconstruction against actual implementation and design documentation. This approach measures how effectively tests serve as executable specifications and identifies documentation gaps in behavioral, architectural, and operational dimensions.

**Key Insight:** If tests allow accurate system reconstruction without external context, they prove their value as living specification documents. Discrepancies reveal where architectural rationale, operational context, or behavioral nuances are under-documented.

---

## Core Principles

1. **Tests as Primary Documentation:** Well-written tests should comprehensively document system behavior so newcomers can understand "what" and "how" without reading implementation code.

2. **Dual Perspective Validation:** Combine naive analysis (tests-only) with expert review (full context) to quantify test documentation quality with measurable accuracy metrics.

3. **Three-Dimensional Assessment:** Evaluate tests across behavioral (what it does), architectural (why it's designed this way), and operational (how it runs in production) dimensions.

4. **Gap-Driven Improvement:** Use reconstruction accuracy scores to identify specific areas where additional test scenarios, inline comments, or ADR references would improve documentation value.

5. **Lightweight Execution:** Target 60-90 minute execution cycles for focused subsystems, making the approach practical for milestone reviews and quarterly audits.

---

## When to Use

**Recommended:**
- ✅ After major test suite refactoring (validate improvement)
- ✅ Before significant releases (comprehensive validation)
- ✅ Quarterly quality audits (track evolution)
- ✅ Onboarding validation (newcomer perspective simulation)
- ✅ Post-architectural changes (verify test-doc alignment)

**Avoid:**
- ❌ Every commit or daily development (too time-intensive)
- ❌ Modules with <20 tests (insufficient reconstruction signal)
- ❌ Rapidly changing experimental code (high staleness risk)

---

## Process Overview

### Phase 1: Naive Reconstruction (Agent A - "Ralph")

**Input:** Test code only (no implementation, no docs, no ADRs)  
**Duration:** ~30 minutes  
**Constraint:** Zero external context allowed

**Tasks:**
1. Read all tests in target scope
2. Reconstruct system understanding:
   - What components exist
   - What behaviors they exhibit
   - What edge cases are handled
   - What workflows are supported
3. Document inferences and uncertainties
4. Generate reconstruction report

**Output:** System behavior narrative based solely on test observations

---

### Phase 2: Expert Review (Agent B - "Alphonso")

**Input:** Reconstruction report + full context (code, ADRs, docs)  
**Duration:** ~20 minutes  
**Constraint:** Compare reconstruction against ground truth

**Tasks:**
1. Read Agent A's reconstruction
2. Compare against actual implementation and design documentation
3. Score accuracy across three dimensions:
   - **Behavioral:** Functional correctness (what it does)
   - **Architectural:** Design rationale (why it's structured this way)
   - **Operational:** Runtime context (how it runs, scales, recovers)
4. Identify discrepancies and root causes
5. Generate improvement recommendations

**Output:** Accuracy assessment with gap analysis

---

### Phase 3: Synthesis & Recommendations

**Duration:** ~15 minutes  
**Tasks:**
1. Calculate overall accuracy score (weighted average)
2. Categorize gaps by severity (critical, high, medium, low)
3. Prioritize improvements by impact vs effort
4. Generate actionable recommendations:
   - Test scenarios to add
   - Inline comments to clarify intent
   - ADR references to embed
   - Operational context to document

**Output:** Improvement roadmap with prioritized actions

---

## Scoring Rubric

### Behavioral Accuracy (Weight: 50%)

| Score | Criteria |
|-------|----------|
| 100%  | Complete, accurate understanding of all behaviors and edge cases |
| 90%   | Minor edge cases unclear; core behaviors fully understood |
| 75%   | Some behavioral nuances missed; primary workflows clear |
| 50%   | Significant behavioral gaps; partial understanding only |
| <50%  | Fundamental misunderstanding of system behavior |

### Architectural Accuracy (Weight: 30%)

| Score | Criteria |
|-------|----------|
| 100%  | Complete understanding of design choices and their rationale |
| 90%   | Design structure understood; rationale requires minor inference |
| 75%   | Structure clear; significant rationale gaps present |
| 50%   | Structure partially understood; rationale unclear |
| <50%  | Design choices misunderstood or invisible in tests |

### Operational Accuracy (Weight: 20%)

| Score | Criteria |
|-------|----------|
| 100%  | Full understanding of runtime, scaling, recovery, and deployment |
| 90%   | Core operational aspects clear; minor details missing |
| 75%   | Basic operation understood; scaling/recovery unclear |
| 50%   | Operational context largely absent from tests |
| <50%  | No operational context discernible from tests |

**Overall Accuracy = (Behavioral × 0.5) + (Architectural × 0.3) + (Operational × 0.2)**

---

## Example: Orchestration Module Results

**Scope:** 66 tests, 1,985 lines (task_utils, agent_orchestrator, e2e workflows)  
**Duration:** 65 minutes total  
**Date:** 2025-11-29

### Scores

- **Behavioral:** 95% ✅
  - Task schema, workflows, error handling all clear
  - Edge cases well-documented through test scenarios
  
- **Architectural:** 90% ✅  
  - File-based approach visible, but "why file-based" required inference
  - Single-orchestrator pattern clear, rationale implicit

- **Operational:** 85% ⚠️
  - Agent lifecycle understood from tests
  - Cron cadence, recovery procedures not documented
  - Security boundaries (Git trust model) invisible

**Overall Accuracy:** 92% ✅

### Key Findings

**Strengths:**
- Clear test names conveyed intent effectively
- Fixtures made complex scenarios readable
- Edge cases explicitly tested (timeouts, conflicts, archival)

**Blind Spots:**
- "Why file-based?" (answer: portability, simplicity) — needed ADR reference
- "How often does it run?" (answer: cron-based) — needed operational test
- "What's the security model?" (answer: Git-level, no auth layer) — needed clarification

### Improvements Applied

1. Added ADR-NNN (coordination pattern) reference to orchestrator tests (architectural context)
2. Created operational scenario test for cron cadence (runtime context)
3. Added inline comment about Git-based trust model (security boundary)

**Post-Improvement Accuracy:** 97% (estimated)

---

## Common Gaps and Fixes

| Gap Type | Symptom | Fix |
|----------|---------|-----|
| **Design Rationale** | Tests show "what" but not "why" | Add ADR reference in test docstring |
| **Operational Context** | Runtime behavior unclear from tests | Add scenario test for deployment/scaling |
| **Security Boundaries** | Trust model invisible | Add inline comment or dedicated test |
| **Performance Expectations** | No sense of scale/throughput | Add performance boundary test |
| **Recovery Procedures** | Failure handling unclear | Add failure recovery scenario test |
| **Integration Contracts** | External dependencies opaque | Add integration boundary tests |

---

## Anti-Patterns

❌ **Scoring Without Rubric:** Subjective assessments drift over time  
✅ **Use standardized rubric:** Maintain consistency across runs

❌ **Analyzing Entire Codebase:** Too time-intensive, low signal  
✅ **Scope to cohesive modules:** 50-100 tests per run

❌ **One-Time Exercise:** Outputs stale quickly  
✅ **Quarterly cadence:** Track improvement trends

❌ **Ignoring Operational Dimension:** Tests focus only on behavior  
✅ **Include runtime scenarios:** Document how system runs in production

❌ **Agent A Cheats (reads docs):** Inflates accuracy scores  
✅ **Strict isolation:** Tests-only constraint enforced

---

## Implementation Checklist

**Preparation:**
- [ ] Select target module/subsystem (50-100 tests recommended)
- [ ] Define scope boundaries clearly
- [ ] Allocate 60-90 minutes for execution
- [ ] Prepare scoring rubric with examples

**Phase 1: Naive Reconstruction**
- [ ] Agent A reads tests only (no implementation, no docs)
- [ ] Generate system behavior narrative
- [ ] Document inferences and uncertainties
- [ ] Flag areas of low confidence

**Phase 2: Expert Review**
- [ ] Agent B reads reconstruction + full context
- [ ] Score accuracy across three dimensions
- [ ] Identify specific discrepancies
- [ ] Categorize gaps by type and severity

**Phase 3: Synthesis**
- [ ] Calculate weighted overall accuracy
- [ ] Prioritize improvements by impact
- [ ] Generate actionable recommendations
- [ ] Document findings in benchmark report

**Follow-Up:**
- [ ] Implement high-priority improvements
- [ ] Update test suite and documentation
- [ ] Schedule next review cycle (quarterly recommended)
- [ ] Track accuracy trends over time

---

## Tool Support

**Prompts:**
- `doctrine/templates/prompts/TEST_READABILITY_CHECK.prompt.md`

**Shorthands:**
- `/test-readability-check` — Launch dual-agent validation

**Scripts:**
- `tools/validators/test-reconstruction-validator.py` (future)

---

## Success Metrics

**Target Accuracy Thresholds:**
- **Behavioral:** ≥90% (tests effectively document behavior)
- **Architectural:** ≥80% (design rationale discoverable)
- **Operational:** ≥75% (runtime context documented)
- **Overall:** ≥85% (acceptable documentation quality)

**Improvement Velocity:**
- **First run:** Baseline accuracy
- **Post-fixes:** +5-10% improvement expected
- **Quarterly trend:** Stable or improving scores

**Time Investment:**
- **Initial run:** 60-90 minutes
- **Follow-up runs:** 45-60 minutes (familiarity effect)
- **ROI:** 10-20x faster onboarding for newcomers

---

## Relationship to Other Approaches

**Complements:**
- **Test-Driven Development (TDD):** Validates that TDD produces comprehensible tests
- **Acceptance Test-Driven Development (ATDD):** Measures spec-to-test traceability
- **Traceable Decisions (Directive 018 (Traceable Decisions)):** Identifies where ADR references improve test clarity

**Differs From:**
- **Code Review:** Focuses on test documentation quality, not implementation correctness
- **Test Coverage Analysis:** Measures breadth, not documentation effectiveness
- **Specification Validation:** Works backward from tests to reconstruct specs

---

## References

- **Source Report:** `work/reports/benchmarks/agent-test-validation-experiment-report.md`
- **Related Approach:** `doctrine/approaches/test-readability-clarity-check.md`
- **Directive 017:** Test-Driven Development
- **Directive 016:** Acceptance Test-Driven Development
- **Directive 017 (TDD):** Test-Driven Development Mandate

---

**Maintained by:** Curator Claire  
**Last Updated:** 2026-02-08  
**Status:** ✅ Active  
**Validation:** Applied to orchestration module (92% accuracy, 2025-11-29)
