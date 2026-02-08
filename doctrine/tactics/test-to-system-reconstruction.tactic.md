# Tactic: Test-to-System Reconstruction (Reverse Speccing)

**Invoked by:**
- [Directive 017 (Test-Driven Development)](../directives/017_tdd.md)
- Shorthand: [`/test-readability-check`](../shorthands/test-readability-check.md)
- Approach: [`reverse-speccing.md`](../approaches/reverse-speccing.md)

**Related tactics:**
- [`testing-select-appropriate-level.tactic.md`](./testing-select-appropriate-level.tactic.md)
- [`ATDD_adversarial-acceptance.tactic.md`](./ATDD_adversarial-acceptance.tactic.md)

---

## Intent

Dual-agent validation that reconstructs system understanding purely from test code, measuring how effectively tests serve as executable specifications.

**Apply when:**
- After major test suite refactoring (validate improvement)
- Before significant releases (comprehensive validation)
- Quarterly quality audits (track evolution)
- Onboarding validation (newcomer perspective simulation)

---

## Preconditions

**Required inputs:**
- Target test directory (50-100 tests recommended)
- Scope boundaries clearly defined
- 60-90 minutes allocated for execution
- Scoring rubric prepared

**Exclusions:**
- Modules with <20 tests (insufficient signal)
- Rapidly changing experimental code (high staleness)
- Every commit validation (too time-intensive)

---

## Execution Steps

### Phase 1: Naive Reconstruction (Agent A)

**Duration:** ~30 minutes  
**Constraint:** Test code ONLY (no implementation, no docs)

1. **Read all tests in scope**
   - [ ] Load test files only
   - [ ] Enforce zero external context
   - [ ] Document this constraint

2. **Reconstruct system understanding**
   - [ ] What components exist
   - [ ] What behaviors they exhibit
   - [ ] What edge cases are handled
   - [ ] What workflows are supported

3. **Document inferences**
   - [ ] Write behavior narrative
   - [ ] Flag uncertainties
   - [ ] Note missing context areas

4. **Generate reconstruction report**
   - [ ] Save to: `work/reports/benchmarks/[date]-test-reconstruction-agent-a.md`

**Output:** System behavior narrative based solely on test observations

---

### Phase 2: Expert Review (Agent B)

**Duration:** ~20 minutes  
**Context:** Full access (code, ADRs, docs)

1. **Read Agent A's reconstruction**
   - [ ] Load reconstruction report
   - [ ] Note initial impressions

2. **Compare against ground truth**
   - [ ] Read actual implementation
   - [ ] Review design documentation
   - [ ] Consult relevant ADRs

3. **Score accuracy (three dimensions)**

   **Behavioral (Weight: 50%):**
   - [ ] Functional correctness (what it does)
   - [ ] Edge case coverage
   - [ ] Workflow understanding
   - **Score:** ___/100

   **Architectural (Weight: 30%):**
   - [ ] Design structure understood
   - [ ] Pattern recognition
   - [ ] Rationale discernment
   - **Score:** ___/100

   **Operational (Weight: 20%):**
   - [ ] Runtime context
   - [ ] Scaling considerations
   - [ ] Recovery procedures
   - **Score:** ___/100

4. **Identify discrepancies**
   - [ ] List specific gaps
   - [ ] Categorize by type (behavioral/architectural/operational)
   - [ ] Assign severity (critical/high/medium/low)

5. **Generate improvement recommendations**
   - [ ] Test scenarios to add
   - [ ] Inline comments to clarify
   - [ ] ADR references to embed
   - [ ] Operational context to document

**Output:** Accuracy assessment with gap analysis

---

### Phase 3: Synthesis & Recommendations

**Duration:** ~15 minutes

1. **Calculate overall accuracy**
   - [ ] Weighted average: (Behavioral × 0.5) + (Architectural × 0.3) + (Operational × 0.2)
   - **Overall Score:** ___/100

2. **Categorize gaps by severity**
   | Severity | Count | Examples |
   |----------|-------|----------|
   | Critical | ___ | |
   | High     | ___ | |
   | Medium   | ___ | |
   | Low      | ___ | |

3. **Prioritize improvements**
   - [ ] Impact vs. effort matrix
   - [ ] Quick wins identified
   - [ ] Strategic improvements planned

4. **Generate actionable roadmap**
   - [ ] Immediate fixes (< 1 hour)
   - [ ] Short-term improvements (< 1 day)
   - [ ] Long-term enhancements (next sprint)

5. **Document findings**
   - [ ] Save to: `work/reports/benchmarks/[date]-test-reconstruction-complete.md`
   - [ ] Include scores, gaps, recommendations
   - [ ] Add to benchmark tracking

**Output:** Improvement roadmap with prioritized actions

---

## Scoring Rubric

### Behavioral Accuracy (50%)
- **100%:** Complete, accurate understanding
- **90%:** Minor edge cases unclear; core behaviors clear
- **75%:** Some nuances missed; primary workflows clear
- **50%:** Significant gaps; partial understanding
- **<50%:** Fundamental misunderstanding

### Architectural Accuracy (30%)
- **100%:** Complete design understanding + rationale
- **90%:** Structure understood; rationale requires minor inference
- **75%:** Structure clear; significant rationale gaps
- **50%:** Structure partially understood; rationale unclear
- **<50%:** Design choices misunderstood

### Operational Accuracy (20%)
- **100%:** Full runtime/scaling/recovery understanding
- **90%:** Core operational aspects clear; minor details missing
- **75%:** Basic operation understood; scaling/recovery unclear
- **50%:** Operational context largely absent
- **<50%:** No operational context discernible

---

## Success Metrics

**Target Thresholds:**
- Behavioral: ≥90%
- Architectural: ≥80%
- Operational: ≥75%
- **Overall: ≥85%**

---

## Outputs

1. **Agent A Report:** Naive reconstruction narrative
2. **Agent B Report:** Expert assessment with scores
3. **Synthesis Report:** Gap analysis + improvement roadmap
4. **Benchmark Entry:** Scores tracked over time

---

**Status:** ✅ Active  
**Validated:** Orchestration module (92% accuracy, 2025-11-29)
