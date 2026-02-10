# Approach: Evidence-Based Requirements Analysis

**Version:** 1.0.0  
**Date:** 2026-02-10  
**Status:** Active  
**Source:** Ubiquitous Language Experiment Research

---

## Purpose

Ground requirements analysis in **verifiable claims with classified evidence types**, ensuring testable hypotheses and traceable validation. This approach transforms requirements from opinion-driven to evidence-driven.

---

## Core Principle

**Claims Without Evidence Are Assumptions**

Traditional requirements often state:
- "Users need X feature" (unvalidated assumption)
- "System must be fast" (vague, unmeasurable)
- "This will improve productivity" (hope, not hypothesis)

Evidence-based requirements state:
- "Users need X feature" (Source: 5 customer interviews, 2025-Q4)
- "System must respond <200ms" (Empirical: Current baseline 450ms, target 200ms)
- "This will improve productivity" (Testable: Measure task completion time before/after)

---

## Claim Classification System

### Evidence Types

**1. Empirical (Quantitative Data)**
- **What:** Measurable, reproducible data from experiments or production
- **Example:** "Naming inconsistency correlates with defect rates (r=0.67, p<0.01)"
- **Strength:** Highest confidence, falsifiable
- **Weakness:** Expensive to collect, may not generalize

**2. Observational (Qualitative Data)**
- **What:** Patterns observed in practice, case studies, field notes
- **Example:** "Teams that communicate frequently converge on shared terminology"
- **Strength:** Rich context, real-world relevance
- **Weakness:** Subjective interpretation, potential bias

**3. Theoretical (Conceptual Models)**
- **What:** Logical deductions from established principles
- **Example:** "Cognitive load limits vocabulary size per team (per Miller's Law)"
- **Strength:** Broad applicability, builds on prior work
- **Weakness:** May not hold in specific contexts

**4. Prescriptive (Best Practices)**
- **What:** Recommendations from authorities, industry standards
- **Example:** "DDD prescribes ubiquitous language within bounded contexts"
- **Strength:** Expert consensus, proven patterns
- **Weakness:** Context-dependent, may be outdated

---

## Testability Assessment

### ✅ Fully Testable
**Criteria:** Can be validated with concrete experiment in pilot phase

**Examples:**
- "Linguistic inconsistency correlates with defect rates" → Measure correlation in codebase
- "Glossary adoption improves onboarding speed" → Time new developer task completion before/after
- "Context boundary violations increase integration failures" → Track failures at boundaries vs. within contexts

**Action:** Prioritize for pilot validation

---

### ⚠️ Partially Testable
**Criteria:** Can be indirectly measured, requires interpretation

**Examples:**
- "Bounded contexts reduce cognitive load" → Survey developer stress, measure context switching frequency
- "Ubiquitous language improves team alignment" → Survey comprehension, measure decision time
- "Conway's Law predicts semantic boundaries" → Compare org structure to vocabulary clusters (correlation, not causation)

**Action:** Design proxy metrics, acknowledge limitations

---

### ❌ Not Testable
**Criteria:** Subjective, unfalsifiable, or requires years to validate

**Examples:**
- "Better architecture leads to happiness" → Too vague, confounding variables
- "DDD is superior to other approaches" → Depends on context, no universal standard
- "This will transform the organization" → Unmeasurable, timeframe unclear

**Action:** Refine claim or accept as philosophical position (not requirement)

---

## Claim Inventory Structure

### Template

```yaml
claim_id: "CLAIM-001"
category: "Language and Architecture Relationship"
claim: "Language fragmentation predicts system problems"
source: "Eric Evans, Domain-Driven Design (2003), Chapter 2"
evidence_type: "observational"
testability: "testable"
testability_notes: "Measure correlation between terminology inconsistency and defect rates in pilot"
implication: "Language quality is an architectural concern, not just documentation hygiene"
related_claims:
  - "CLAIM-002"
  - "CLAIM-005"
status: "proposed"
validation_status: "pending"
validation_date: null
validation_result: null
```

### Status Lifecycle

1. **Proposed** - Extracted from research, not yet validated
2. **Accepted** - Validated empirically or consensus agreement
3. **Rejected** - Falsified by experiment or evidence
4. **Superseded** - Replaced by refined claim
5. **Deferred** - Not currently testable, revisit later

---

## Requirements Validation Process

Evidence-based requirements follow a five-phase validation cycle:

1. **Research and Claim Extraction** - Build inventory from literature, interviews, production data
2. **Claim Prioritization** - Focus on high-impact, testable claims (avoid analysis paralysis)
3. **Experiment Design** - Define falsifiable hypotheses with clear pass/fail criteria
4. **Validation Execution** - Run experiments, analyze results, update claim status
5. **Requirements Synthesis** - Translate validated claims to requirements with traceability

**Rationale:** This process transforms assumptions into validated knowledge. By testing claims before committing to implementation, teams avoid costly rework from invalidated assumptions. Traceability from requirements → claims → evidence enables confidence-based decision-making.

**See:** [Requirements Validation Workflow Tactic](../tactics/requirements-validation-workflow.tactic.md) for detailed step-by-step procedures

---

## When to Use

✅ **Use Evidence-Based Requirements when:**
- Domain is complex or unfamiliar
- Stakeholder opinions conflict
- Large investment requires justification
- System will be long-lived (validate assumptions early)
- Regulatory or safety-critical (evidence mandatory)

⚠️ **Exercise Caution when:**
- Validation experiments are prohibitively expensive
- Domain experts have strong consensus (empirical validation may be overkill)
- Rapid prototyping phase (defer validation until after feasibility proven)

❌ **Do Not Use when:**
- Simple CRUD systems with well-understood requirements
- Throwaway prototypes or experiments
- Time-to-market pressure exceeds validation value
- No access to validation data (interviews, production metrics, etc.)

---

## Integration with Doctrine Stack

### Related Approaches
- **[Language-First Architecture](language-first-architecture.md)** - Linguistic analysis as architectural signal
- **[Living Glossary Practice](living-glossary-practice.md)** - Terminology validation infrastructure

### Related Directives
- **[Directive 018: Traceable Decisions](../directives/018_traceable_decisions.md)** - ADR-to-evidence traceability
- **[Directive 034: Specification-Driven Development](../directives/034_spec_driven_development.md)** - Requirements quality standards

### Related Tactics
- **[Requirements Validation Workflow](../tactics/requirements-validation-workflow.tactic.md)** - Step-by-step validation procedures
- **[Claim Inventory Development](../tactics/claim-inventory-development.tactic.md)** - Research cataloging methods

---

## Success Metrics

### Claim Quality
- **Claim-to-requirement traceability:** Target 100% (every requirement traces to validated claim)
- **Evidence diversity:** Mix of empirical, observational, theoretical (no single type dominates)
- **Testability rate:** % claims testable (Target >70%)

### Validation Effectiveness
- **Claims validated:** % of proposed claims tested (Target >60% within 6 months)
- **Rejection rate:** % claims falsified (Target 10-30%, indicates intellectual honesty)
- **Confidence level:** Average confidence in accepted claims (Target: High or Medium, few Low)

### Requirements Impact
- **Rework rate:** % requirements changed due to invalidated assumptions (Target <20%)
- **Specification ambiguity:** Survey developer comprehension (Target >80% "clear")
- **Traceability compliance:** % requirements with claim linkage (Target 100%)

---

## Failure Modes and Mitigations

### Failure Mode 1: Analysis Paralysis
**Symptom:** Endless validation, no delivery  
**Cause:** Overvalidation, perfectionism  
**Mitigation:** Time-box validation phase (4-6 weeks max), prioritize high-impact claims only

### Failure Mode 2: Cherry-Picking Evidence
**Symptom:** Ignoring claims that contradict preferences  
**Cause:** Confirmation bias, political pressure  
**Mitigation:** Pre-register hypotheses, document rejected claims, invite challenge

### Failure Mode 3: False Precision
**Symptom:** Claiming statistical certainty from weak evidence  
**Cause:** Misunderstanding statistics, small sample sizes  
**Mitigation:** Report confidence intervals, acknowledge limitations, invite peer review

### Failure Mode 4: Evidence Theater
**Symptom:** Collecting evidence to justify pre-decided requirements  
**Cause:** Requirements locked in before analysis  
**Mitigation:** Analyze before deciding, be willing to reject initial assumptions

---

## Agent Relevance

**Primary Agents:**
- **Researcher Ralph:** Claim extraction, literature review, validation experiments
- **Analyst Annie:** Requirements synthesis, acceptance criteria, traceability

**Supporting Agents:**
- **Architect Alphonso:** Claim prioritization, architectural implications
- **Scribe Simon:** Documentation of findings, traceability reports

---

## References

### Research Sources
- **Claim Inventory:** `docs/architecture/experiments/ubiquitous-language/claim-inventory.md`
- **Research Findings:** `docs/architecture/experiments/ubiquitous-language/research-findings-summary.md`

### Methodological Foundation
- **Evidence-Based Software Engineering:** Kitchenham, Charters (2007)
- **Systematic Literature Reviews:** Petersen et al. (2015)
- **Grounded Theory:** Glaser, Strauss (1967)

### Related Documentation
- **[DDD Core Concepts Reference](../docs/ddd-core-concepts-reference.md)** - Domain terminology
- **[Linguistic Anti-Patterns Catalog](../docs/linguistic-anti-patterns.md)** - Common failures

---

## Version History

- **1.0.0** (2026-02-10): Initial version extracted from ubiquitous language experiment research

---

**Curation Status:** ✅ Claire Approved (Doctrine Stack Compliant)
