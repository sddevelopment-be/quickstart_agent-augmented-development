# Tactic: Requirements Validation Workflow (Evidence-Based)

**Version:** 1.0.0  
**Date:** 2026-02-10  
**Status:** Active  
**Source:** Extracted from Evidence-Based Requirements Analysis Approach

---

## Purpose

Provide step-by-step procedures for validating requirements through evidence-based claim analysis, ensuring requirements are grounded in testable hypotheses rather than assumptions.

---

## When to Use

Use this tactic when:
- Starting a new project with complex or unfamiliar domain
- Stakeholder opinions conflict significantly
- Large investment requires empirical justification
- System will be long-lived (validate assumptions early to avoid costly rework)
- Regulatory or safety-critical domains (evidence mandatory)

**Prerequisites:**
- Access to research sources (literature, stakeholder interviews, production data)
- Ability to design and run validation experiments
- Commitment to intellectual honesty (willingness to reject initial assumptions)

---

## Procedure

### Phase 1: Research and Claim Extraction

**Objective:** Build comprehensive inventory of testable claims about the domain and requirements.

**Duration:** 1-2 weeks for typical project

**Activities:**

**1.1 Literature Review**
1. **Identify relevant sources:**
   - Academic papers (Google Scholar, ACM, IEEE)
   - Industry books and reports
   - Domain-specific standards and regulations
   - Competitor analysis and market research

2. **Extract claims systematically:**
   - Document author, publication year, citation
   - Quote original text verbatim
   - Classify evidence type (empirical, observational, theoretical, prescriptive)
   - Note limitations or caveats

3. **Create claim entries:**
   ```yaml
   claim_id: "CLAIM-001"
   category: "User Behavior"
   claim: "Users abandon forms with >5 fields"
   source: "Nielsen Norman Group (2019), Form Usability Study"
   evidence_type: "empirical"
   testability: "testable"
   ```

**1.2 Stakeholder Interviews**
1. **Identify stakeholders:**
   - Domain experts (business side)
   - Users or customer representatives
   - Developers and technical leads
   - Product managers and designers

2. **Conduct semi-structured interviews:**
   - Ask open-ended questions about domain challenges
   - Capture assertions, beliefs, assumptions
   - Probe for evidence: "What makes you believe that?"
   - Record quotes with attribution

3. **Extract implicit claims:**
   - "We need feature X" → "Feature X solves problem Y for user segment Z"
   - "System must be fast" → "Current performance of N ms causes user frustration"
   - Restate vague requirements as testable claims

**1.3 Production Data Analysis**
1. **Collect baseline metrics:**
   - Current system performance (if applicable)
   - User behavior analytics
   - Error rates, support tickets
   - Competitive benchmarks

2. **Identify patterns:**
   - Correlations (X increases when Y occurs)
   - Anomalies (unexpected spikes, outliers)
   - Trends over time

3. **Formulate data-driven claims:**
   - "95th percentile response time is 450ms"
   - "Users retry failed actions 3.2 times on average"
   - "Mobile users abandon at 2x rate of desktop"

**Output:** Claim inventory with 20-50 claims, each classified by evidence type

**Responsible:** Researcher Ralph (lead), Analyst Annie (synthesis)

---

### Phase 2: Claim Prioritization

**Objective:** Focus validation effort on high-impact, testable claims.

**Duration:** 1-2 days

**Activities:**

**2.1 Assess Testability**
For each claim, determine:
- ✅ **Fully Testable:** Can validate with concrete experiment in pilot phase
- ⚠️ **Partially Testable:** Can measure indirectly via proxy metrics
- ❌ **Not Testable:** Subjective, unfalsifiable, or requires years to validate

**Examples:**
- "Glossary adoption improves onboarding speed" → ✅ Time task completion before/after
- "Bounded contexts reduce cognitive load" → ⚠️ Survey stress, measure context switching
- "This will transform the organization" → ❌ Unmeasurable, vague

**2.2 Evaluate Business Impact**
Rate each claim:
- **High:** Directly affects core user value or major business metrics
- **Medium:** Improves secondary features or operational efficiency
- **Low:** Nice-to-have, aesthetic, or minor convenience

**2.3 Estimate Validation Effort**
Estimate time to design and run validation:
- **Quick:** <1 week (simple data collection, existing metrics)
- **Moderate:** 1-4 weeks (survey design, A/B test, small experiment)
- **Lengthy:** >4 weeks (longitudinal study, extensive data collection)

**2.4 Prioritize**
Apply decision matrix:

| Impact | Testability | Effort | Priority |
|--------|-------------|--------|----------|
| High | ✅ Testable | Quick | **Validate Immediately** |
| High | ✅ Testable | Moderate | **Validate Soon** |
| High | ⚠️ Partial | Moderate | **Design Proxy Metrics** |
| Medium | ✅ Testable | Quick | **Validate if Time** |
| Low | Any | Any | **Defer or Reframe** |
| Any | ❌ Not Testable | Any | **Document as Assumption** |

**Output:** Prioritized backlog of claims to validate (typically 5-15 high-priority claims)

**Responsible:** Analyst Annie, Architect Alphonso (joint decision)

---

### Phase 3: Experiment Design

**Objective:** Design rigorous validation experiments with clear pass/fail criteria.

**Duration:** 1-3 days per claim

**Activities:**

**3.1 Define Falsifiable Hypothesis**
Restate claim as testable hypothesis:
- **Claim:** "Terminology inconsistency causes defects"
- **Hypothesis:** "Terminology inconsistency correlates with defect rates (r > 0.5, p < 0.05)"

**3.2 Design Validation Experiment**
Specify:
1. **Metrics to collect:**
   - Independent variable: Terminology consistency score (0-100)
   - Dependent variable: Defect density (defects per KLOC)

2. **Data collection method:**
   - AST analysis for naming consistency
   - Historical bug database for defects
   - Git log for code age (confound control)

3. **Analysis plan:**
   - Statistical test: Pearson correlation coefficient
   - Significance level: α = 0.05
   - Sample size: Minimum 30 modules for statistical power

4. **Success criteria:**
   - **Accept hypothesis:** r > 0.5 with p < 0.05
   - **Reject hypothesis:** r < 0.3 or p > 0.05
   - **Inconclusive:** 0.3 ≤ r ≤ 0.5 (design better experiment)

**3.3 Identify Confounding Variables**
List alternative explanations:
- Code age (older code may have both inconsistency and defects)
- Team experience (junior teams cause both problems)
- Module complexity (complex modules harder to name and test)

**Control strategy:**
- Measure confounds and use multivariate analysis
- Match modules on confounds (paired comparison)
- Stratify by confound (analyze separately per experience level)

**3.4 Document Experiment Plan**
```markdown
## Validation Experiment: CLAIM-001

**Hypothesis:** Terminology inconsistency correlates with defect rates (r > 0.5)

**Data Collection:**
- Scan 50 modules across codebase
- Calculate naming consistency score (AST analysis)
- Extract defect counts from Jira (last 12 months)
- Control for code age, team experience, complexity

**Analysis:**
- Pearson correlation: consistency_score vs. defect_density
- Partial correlation controlling for confounds
- Significance test: α = 0.05

**Success Criteria:**
- r > 0.5 with p < 0.05 → Accept claim
- r < 0.3 or p > 0.05 → Reject claim
- Otherwise → Inconclusive, refine experiment

**Timeline:** 1 week (3 days collection, 2 days analysis)
```

**Output:** Experiment plan document with clear pass/fail criteria

**Responsible:** Analyst Annie (design), Researcher Ralph (review)

---

### Phase 4: Validation Execution

**Objective:** Run experiments and update claim status based on results.

**Duration:** 1-4 weeks depending on experiment complexity

**Activities:**

**4.1 Collect Data**
1. **Follow experiment plan:**
   - Execute data collection procedures exactly as designed
   - Document any deviations or issues
   - Record data in structured format (CSV, database)

2. **Quality checks:**
   - Verify completeness (no missing data)
   - Check for outliers (legitimate or data errors?)
   - Validate assumptions (e.g., normal distribution for parametric tests)

**4.2 Analyze Results**
1. **Run statistical tests:**
   - Execute planned analysis (correlation, t-test, ANOVA, etc.)
   - Calculate effect sizes, confidence intervals
   - Check assumptions (normality, homoscedasticity)

2. **Interpret findings:**
   - Compare results to success criteria
   - Consider practical significance (not just statistical)
   - Assess confound impact

3. **Qualitative analysis (if applicable):**
   - Code interview transcripts (grounded theory)
   - Identify themes and patterns
   - Triangulate with quantitative data

**4.3 Update Claim Status**
Based on results, change claim status:
- **Accepted:** Evidence supports claim with high confidence
- **Rejected:** Evidence refutes claim, alternative explanation better
- **Superseded:** Claim refined based on findings, new claim created
- **Deferred:** Inconclusive results, need more data or better experiment

**4.4 Document Findings**
Create validation report:
```markdown
## Validation Report: CLAIM-001

**Claim:** Terminology inconsistency correlates with defect rates

**Status:** ✅ **Accepted**

**Evidence Summary:**
- Pearson correlation: r = 0.72 (p < 0.01)
- Partial correlation (controlling for age, experience): r = 0.68 (p < 0.01)
- Effect size: Large (Cohen's d = 0.85)

**Confidence Level:** High

**Interpretation:**
Strong positive correlation between naming inconsistency and defects remains significant even after controlling for confounds. Terminology quality is a legitimate architectural concern.

**Limitations:**
- Observational study (correlation, not causation)
- Single codebase (generalizability unknown)
- Retrospective data (historical bias possible)

**Recommendation:** Proceed with glossary enforcement in pilot project.
```

**Output:** Validated claims with confidence levels, evidence summaries

**Responsible:** Researcher Ralph (execution), Analyst Annie (interpretation)

---

### Phase 5: Requirements Synthesis

**Objective:** Translate validated claims into evidence-backed requirements with traceability.

**Duration:** 3-5 days

**Activities:**

**5.1 Claim-to-Requirement Translation**
For each accepted claim, derive requirements:

**Template:**
```markdown
**Requirement REQ-001:** [Feature/Constraint]

**Rationale:**
- **Claim:** [CLAIM-ID]: [Claim statement]
- **Evidence:** [Summary of validation results]
- **Confidence:** [High/Medium/Low] [✅/⚠️/❌]

**Acceptance Criteria:**
1. [Testable condition 1]
2. [Testable condition 2]
3. [Testable condition 3]
```

**Example:**
```markdown
**Requirement REQ-001:** Implement PR-level glossary validation

**Rationale:**
- **Claim CLAIM-003:** Early terminology feedback reduces integration defects
- **Evidence:** Validated empirically in pilot (r=0.72, p<0.01)
- **Confidence:** High ✅

**Acceptance Criteria:**
1. PR checks flag cross-context terminology violations
2. Developers receive advisory-level feedback (not blocking by default)
3. Response time <2 seconds per PR
4. False positive rate <10%
```

**5.2 Define Acceptance Criteria**
For each requirement, specify testable conditions:
- **Functional:** What behavior must system exhibit?
- **Non-functional:** Performance, security, usability constraints
- **Quality:** Metrics to measure success (with thresholds)

**5.3 Establish Traceability**
Create bidirectional links:
```
Requirements ↔ Claims ↔ Evidence
```

**Traceability Matrix:**
| Requirement ID | Claim ID(s) | Evidence Type | Confidence | Validation Date |
|----------------|-------------|---------------|------------|-----------------|
| REQ-001 | CLAIM-003 | Empirical | High ✅ | 2026-02-05 |
| REQ-002 | CLAIM-007, CLAIM-009 | Observational | Medium ⚠️ | 2026-02-08 |
| REQ-003 | CLAIM-012 | Theoretical | Low ❌ | Not validated |

**5.4 Document Assumptions**
For deferred or untestable claims used in requirements:
```markdown
## Assumptions

**ASSUMPTION-001:** Users prefer terminology consistency over flexibility

**Status:** Not validated (validation cost exceeds benefit)

**Risk:** If assumption false, glossary enforcement may cause resentment

**Mitigation:** Start with advisory-only enforcement, gather feedback, adjust based on usage patterns
```

**Output:** Evidence-backed specification with full traceability

**Responsible:** Analyst Annie (lead), Scribe Simon (documentation)

---

## Success Criteria

✅ **Workflow is effective when:**
- Every requirement traces to at least one validated claim
- Claim inventory includes mix of evidence types (no single type dominates)
- 60%+ of proposed claims validated within 6 months
- Rejection rate is 10-30% (indicates intellectual honesty, not confirmation bias)
- Specification ambiguity surveys show >80% developer comprehension
- Requirements rework rate <20% (few invalidated assumptions)

---

## Common Pitfalls

### Pitfall 1: Analysis Paralysis
**Symptom:** Endless validation, no delivery  
**Solution:** Time-box validation phase (4-6 weeks max). Prioritize high-impact claims only. Accept some assumptions for low-risk areas.

### Pitfall 2: Cherry-Picking Evidence
**Symptom:** Ignoring claims that contradict preferences  
**Solution:** Pre-register hypotheses publicly. Document all claims, even rejected ones. Invite external challenge.

### Pitfall 3: False Precision
**Symptom:** Claiming statistical certainty from weak evidence  
**Solution:** Report confidence intervals, not just point estimates. Acknowledge limitations. Invite peer review before finalizing.

### Pitfall 4: Evidence Theater
**Symptom:** Collecting evidence to justify pre-decided requirements  
**Solution:** Extract claims **before** designing solutions. Be willing to reject initial assumptions. Measure confirmation bias rate.

---

## Related Documentation

### Related Approaches
- **[Evidence-Based Requirements Analysis](../approaches/evidence-based-requirements.md)** - Strategic rationale (WHY)
- **[Language-First Architecture](../approaches/language-first-architecture.md)** - Linguistic validation context

### Related Tactics
- **[Claim Inventory Development](claim-inventory-development.tactic.md)** - Detailed claim extraction procedures
- **[Terminology Extraction and Mapping](terminology-extraction-mapping.tactic.md)** - Domain terminology analysis

### Related Directives
- **[Directive 018: Traceable Decisions](../directives/018_traceable_decisions.md)** - ADR traceability to claims
- **[Directive 034: Specification-Driven Development](../directives/034_spec_driven_development.md)** - Specification quality standards

---

## Version History

- **1.0.0** (2026-02-10): Initial version extracted from Evidence-Based Requirements Analysis approach

---

**Curation Status:** ✅ Claire Approved (Doctrine Stack Compliant - Procedural content properly placed in Tactics layer)
