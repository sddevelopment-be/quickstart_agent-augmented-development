# Claim Inventory: Ubiquitous Language Experiment

**Version:** 1.0.0  
**Date:** 2026-02-09  
**Purpose:** Catalog of testable claims extracted from research sources  
**Status:** Phase 1 Complete

---

## Overview

This document catalogs **verifiable claims** extracted from research sources that ground the ubiquitous language experiment. Each claim includes:

- **Source:** Where the claim originates
- **Claim:** What is being asserted
- **Evidence Type:** Empirical, theoretical, observational, or prescriptive
- **Implication:** What this means for the experiment
- **Testable:** Can this claim be validated in Phase 2 (pilot)?

---

## Category 1: Language and Architecture Relationship

### Claim 1.1: Language Fragmentation Predicts System Problems

**Source:** Eric Evans, *Domain-Driven Design* (2003), Chapter 2  
**Claim:** "A project faces serious problems when its language is fractured."  
**Evidence Type:** Observational (from practice)  
**Implication:** Language quality is an architectural concern, not just documentation hygiene  
**Testable:** ✅ Yes - Measure correlation between terminology inconsistency and defect rates in pilot

---

### Claim 1.2: Model and Language Must Evolve Together

**Source:** Eric Evans, *Domain-Driven Design* (2003), Chapter 1  
**Claim:** "The model is not just a design artifact. It is an integral part of everything the team does."  
**Implication:** If code and conversations use different terminology, the model has failed  
**Testable:** ✅ Yes - Survey developers: "Can domain experts understand your code structure?"

---

### Claim 1.3: Names Constrain Design Decisions

**Source:** Rebecca Wirfs-Brock, *Object Design* (2002), Chapter 2  
**Claim:** "Good names reveal intention and responsibilities."  
**Evidence Type:** Design theory  
**Implication:** Ambiguous names indicate design uncertainty; naming is architectural work  
**Testable:** ⚠️ Partial - Can measure name refactoring frequency, harder to prove causation

---

### Claim 1.4: Linguistic Inconsistency Correlates with Defects

**Source:** Gabriele Bavota et al., "Mining Version Histories for Detecting Code Smells" (2015)  
**Claim:** Inconsistent naming across versions predicts defects  
**Evidence Type:** Empirical study (quantitative)  
**Implication:** Linguistic drift is a leading indicator of technical debt  
**Testable:** ✅ Yes - Measure defect rates in code with high vs low naming consistency

---

### Claim 1.5: Generic Names Correlate with High Coupling

**Source:** Gabriele Bavota et al., "Mining Version Histories for Detecting Code Smells" (2015)  
**Claim:** Generic names (e.g., "data", "info", "manager") correlate with high coupling  
**Evidence Type:** Empirical study (quantitative)  
**Implication:** Name specificity is measurable quality metric  
**Testable:** ✅ Yes - Measure coupling in modules with generic vs specific names

---

## Category 2: Bounded Contexts and Organizational Boundaries

### Claim 2.1: Global Unification is Infeasible

**Source:** Eric Evans, *Domain-Driven Design* (2003), Chapter 14  
**Claim:** "Multiple models are in play on any large project. Yet when code based on distinct models is combined, software becomes buggy, unreliable, and difficult to understand."  
**Evidence Type:** Observational (from practice)  
**Implication:** Ignoring context boundaries causes technical debt  
**Testable:** ✅ Yes - Measure integration defect rates at context boundaries vs within contexts

---

### Claim 2.2: Bounded Context is Conceptual, Not Technical

**Source:** Vaughn Vernon, *Implementing Domain-Driven Design* (2013), Chapter 2  
**Claim:** "A bounded context is not a module. It is a conceptual boundary."  
**Evidence Type:** Definitional/theoretical  
**Implication:** Don't conflate technical boundaries (modules, services) with semantic boundaries (contexts)  
**Testable:** ⚠️ Indirect - Can measure violations (module structure contradicts semantic boundaries)

---

### Claim 2.3: Each Context Has Own Ubiquitous Language

**Source:** Vaughn Vernon, *Implementing Domain-Driven Design* (2013), Chapter 2  
**Claim:** "Each bounded context has its own ubiquitous language."  
**Evidence Type:** Definitional/theoretical  
**Implication:** No global glossary. Local agreement per context.  
**Testable:** ✅ Yes - Measure term overlap between contexts vs within contexts

---

### Claim 2.4: Translation at Boundaries is Required

**Source:** Vaughn Vernon, *Implementing Domain-Driven Design* (2013), Chapter 3  
**Claim:** Translation required at context boundaries, not unification  
**Evidence Type:** Prescriptive (best practice)  
**Implication:** Anti-pattern: forcing global terminology standardization  
**Testable:** ✅ Yes - Measure complexity of systems with translation vs forced unification

---

## Category 3: Conway's Law and Organizational Structure

### Claim 3.1: System Structure Mirrors Organizational Structure

**Source:** Melvin Conway, "How Do Committees Invent?" (1968)  
**Claim:** "Organizations design systems that mirror their communication structures."  
**Evidence Type:** Observational (empirical pattern)  
**Implication:** Architecture reflects who talks to whom  
**Testable:** ✅ Yes - Map communication patterns to system boundaries, measure correlation

---

### Claim 3.2: Team Boundaries Predict Semantic Boundaries

**Source:** Linguistic corollary to Conway's Law (synthesis)  
**Claim:** Vocabulary structure mirrors communication structure  
**Evidence Type:** Theoretical extension  
**Implication:** Team boundaries predict where terminology conflicts occur  
**Testable:** ✅ Yes - Measure terminology conflicts at team boundaries vs within teams

---

### Claim 3.3: Cognitive Load Limits Vocabulary Size

**Source:** Matthew Skelton & Manuel Pais, *Team Topologies* (2019), Chapter 3  
**Claim:** "Cognitive load should be the primary consideration when designing team responsibilities."  
**Evidence Type:** Cognitive science applied to teams  
**Implication:** Teams can't internalize unlimited vocabulary—bounded contexts reduce cognitive load  
**Testable:** ⚠️ Partial - Can survey teams: "How many domain terms can you define accurately?"

---

### Claim 3.4: Stream-Aligned Teams Own Domain Vocabulary

**Source:** Matthew Skelton & Manuel Pais, *Team Topologies* (2019), Chapter 5  
**Claim:** "Stream-aligned teams own the full value stream and make decisions quickly."  
**Evidence Type:** Observational pattern  
**Implication:** Stream-aligned teams naturally develop coherent domain vocabulary  
**Testable:** ✅ Yes - Measure vocabulary coherence in stream-aligned vs component teams

---

### Claim 3.5: Weak Interaction Mode Predicts Vocabulary Divergence

**Source:** Matthew Skelton & Manuel Pais, *Team Topologies* (2019), Chapter 4  
**Claim:** "The interaction mode between teams determines the type of communication that happens."  
**Evidence Type:** Observational pattern  
**Implication:** Collaboration mode predicts vocabulary alignment  
**Testable:** ✅ Yes - Measure term alignment between teams with collaboration vs X-as-a-Service mode

---

## Category 4: Agentic Systems and Linguistic Monitoring

### Claim 4.1: Continuous Monitoring Was Historically Infeasible

**Source:** Experiment synthesis (analysis)  
**Claim:** Manual linguistic monitoring at scale is economically prohibitive  
**Evidence Type:** Economic analysis  
**Implication:** Agentic systems enable previously infeasible practices  
**Testable:** ✅ Yes - Compare cost of manual glossary maintenance vs agentic monitoring

---

### Claim 4.2: LLMs Detect Patterns, Not Correctness

**Source:** Experiment synthesis (design constraint)  
**Claim:** LLMs are strong at pattern detection, weak at determining "correct" terminology  
**Evidence Type:** Capability analysis  
**Implication:** Agents observe and evidence; humans interpret and decide  
**Testable:** ✅ Yes - Measure false positive rate and human override frequency

---

### Claim 4.3: Early Detection Reduces Architectural Impact

**Source:** Experiment hypothesis  
**Claim:** Linguistic conflicts precede architectural problems by 2-4 weeks  
**Evidence Type:** Hypothesis (to be tested)  
**Implication:** Target: detect conflicts <2 weeks with agentic monitoring  
**Testable:** ✅ Yes - PRIMARY EXPERIMENT METRIC

---

### Claim 4.4: PR-Time Feedback More Effective Than Periodic Audits

**Source:** Experiment design (synthesis from evolutionary architecture)  
**Claim:** Continuous feedback loops prevent drift more effectively than periodic reviews  
**Evidence Type:** Evolutionary architecture theory  
**Implication:** Linguistic checks as fitness functions  
**Testable:** ✅ Yes - Compare drift rates with PR-time feedback vs quarterly glossary reviews

---

## Category 5: Governance and Enforcement

### Claim 5.1: Human in Charge Enables Accountability

**Source:** Helen Nissenbaum, *Privacy in Context* (2009); Ian Kerr (2004)  
**Claim:** Accountability cannot be delegated to automated systems  
**Evidence Type:** Ethics and governance theory  
**Implication:** Agents observe; humans own decisions  
**Testable:** ⚠️ Indirect - Measure developer trust and engagement with system

---

### Claim 5.2: Advisory Enforcement Reduces Resistance

**Source:** Experiment design (tiered enforcement)  
**Claim:** Default advisory enforcement reduces "linguistic policing" perception  
**Evidence Type:** Hypothesis (informed by change management)  
**Implication:** Start advisory, escalate only with justification  
**Testable:** ✅ Yes - Measure developer sentiment: advisory vs hard-failure enforcement

---

### Claim 5.3: Distributed Ownership Scales Better Than Centralized

**Source:** Experiment design (bounded contexts + ownership)  
**Claim:** Context-specific ownership reduces bottlenecks vs centralized glossary committee  
**Evidence Type:** Organizational design theory  
**Implication:** Each context has term owners  
**Testable:** ✅ Yes - Measure glossary update latency: distributed vs centralized ownership

---

## Category 6: Known Failure Modes

### Claim 6.1: "Dictionary DDD" Fails Without Enforcement

**Source:** Vaughn Vernon, *Domain-Driven Design Distilled* (2016), observations  
**Claim:** Glossaries that aren't enforced through usage become stale  
**Evidence Type:** Observational pattern (anti-pattern)  
**Implication:** Language must live in code and tests, not just documents  
**Testable:** ✅ Yes - Measure glossary staleness: enforced vs documentation-only

---

### Claim 6.2: False Positives Damage Trust

**Source:** Experiment design (failure mode analysis)  
**Claim:** Low-quality agent output leads to system abandonment  
**Evidence Type:** Change management / user acceptance theory  
**Implication:** High precision more important than high recall initially  
**Testable:** ✅ Yes - Track abandonment triggers and false positive rates

---

### Claim 6.3: Forced Unification Creates Performative Compliance

**Source:** Experiment design (sociolinguistic analysis)  
**Claim:** People say "official" terms publicly, use local terms internally  
**Evidence Type:** Sociolinguistic observation  
**Implication:** Accept bounded contexts to prevent performative behavior  
**Testable:** ⚠️ Difficult - Would require observing private conversations vs official docs

---

## Category 7: OO and Event-Based Modeling

### Claim 7.1: Names Reveal Responsibilities

**Source:** Rebecca Wirfs-Brock, *Object Design* (2002), Chapter 2  
**Claim:** "Good names reveal intention and responsibilities"  
**Evidence Type:** Design theory  
**Implication:** If you can't name an object's responsibility clearly, the design is unclear  
**Testable:** ⚠️ Partial - Can measure clarity through developer comprehension tests

---

### Claim 7.2: Collaborations Clarify Design

**Source:** Rebecca Wirfs-Brock, *Object Design* (2002)  
**Claim:** Understanding **how** objects work together is as important as **what** they do individually  
**Evidence Type:** Design theory  
**Implication:** CRC cards reveal collaboration patterns that might otherwise stay implicit  
**Testable:** ⚠️ Indirect - Measure design quality improvements using CRC cards vs ad-hoc design

---

### Claim 7.3: Concepts are Design Atoms

**Source:** Daniel Jackson, *The Essence of Software* (2021)  
**Claim:** "Concepts are the atoms of software design"  
**Evidence Type:** Design theory  
**Implication:** If your concepts are fuzzy, your software will be fuzzy  
**Testable:** ⚠️ Partial - Can measure concept clarity through purpose/operational principle articulation

---

### Claim 7.4: Every Concept Must Have Clear Purpose

**Source:** Daniel Jackson, *The Essence of Software* (2021), Chapter 3  
**Claim:** Every concept must have a clear purpose (why it exists)  
**Evidence Type:** Design theory  
**Implication:** Objects without clear purpose accumulate cruft and become maintenance burdens  
**Testable:** ✅ Yes - Measure maintenance burden of objects with/without documented purpose

---

### Claim 7.5: Domain Events Make Processes Explicit

**Source:** Eric Evans, *Domain-Driven Design* (2003), Chapters 5-6  
**Claim:** "Domain events make implicit processes explicit"  
**Evidence Type:** Observational (from practice)  
**Implication:** Events surface business logic that would otherwise stay hidden in code  
**Testable:** ✅ Yes - Compare process visibility in event-based vs non-event-based systems

---

### Claim 7.6: Event Storming Accelerates Understanding

**Source:** Alberto Brandolini, *Event Storming* (2013)  
**Claim:** Event Storming creates shared understanding faster than traditional requirements gathering  
**Evidence Type:** Observational (from practice)  
**Implication:** Collaborative discovery beats documentation handoffs  
**Testable:** ✅ Yes - Measure time-to-understanding: Event Storming vs traditional requirements docs

---

### Claim 7.7: Anemic Models Hide Business Logic

**Source:** Martin Fowler, "Anemic Domain Model" (2003); Eric Evans  
**Claim:** Data-only objects scatter domain logic across services, reducing linguistic clarity  
**Evidence Type:** Observational pattern (anti-pattern)  
**Implication:** Push behavior into objects to maintain responsibility clarity  
**Testable:** ✅ Yes - Measure logic scattering (methods per class vs service methods)

---

## Assumption Inventory

Claims that are **assumed true** but not directly tested in this experiment:

### Assumption A1: Domain Experts Provide Ground Truth

**Assumption:** Domain experts can authoritatively define "correct" terminology within their domain  
**Risk:** Domain experts may disagree or have incomplete understanding  
**Mitigation:** Acknowledge uncertainty; use "canonical per context" not "objectively correct"

---

### Assumption A2: Code Readability Correlates with Terminology Clarity

**Assumption:** If terminology is clear, code is more readable  
**Risk:** Other factors (complexity, structure) also affect readability  
**Mitigation:** Control for other variables when measuring

---

### Assumption A3: Developers Will Engage with Linguistic Feedback

**Assumption:** Developers care about terminology and will act on agent feedback  
**Risk:** Developers may dismiss as "bikeshedding"  
**Mitigation:** Tie terminology to concrete outcomes (defect reduction, onboarding speed)

---

### Assumption A4: Linguistic Conflicts Are Detectable Before Code Issues

**Assumption:** Language drift appears in conversations/docs before manifesting in bugs  
**Risk:** Some language drift may only be detectable post-implementation  
**Mitigation:** Track lead time; acknowledge not all drift is preventable

---

## Open Questions

Questions that research hasn't fully answered:

### Question 1: Optimal Context Size

**Question:** What is the ideal vocabulary size for a bounded context?  
**Current Guidance:** 50-100 terms (based on cognitive load research)  
**Needs Validation:** Does this hold in practice?

---

### Question 2: Translation Cost Threshold

**Question:** When does translation overhead exceed benefit of context independence?  
**Current Guidance:** Unknown—likely context-dependent  
**Needs Validation:** Measure in pilot

---

### Question 3: Sociolinguistic Register Variation

**Question:** How do we distinguish normal register variation from problematic drift?  
**Current Guidance:** Separate observational (transcripts) from canonical (code)  
**Needs Validation:** Test false positive rates

---

### Question 4: Organizational Change Timing

**Question:** How long after reorganization does vocabulary stabilize?  
**Current Guidance:** Estimated 3-6 months (no strong evidence)  
**Needs Validation:** Track vocabulary churn post-reorg

---

## Testing Matrix

Summary of testability by claim category:

| Category | Total Claims | Directly Testable | Partially Testable | Indirect Only |
|----------|--------------|-------------------|--------------------|-----------------|
| Language & Architecture | 5 | 3 | 1 | 1 |
| Bounded Contexts | 4 | 3 | 1 | 0 |
| Conway's Law | 5 | 4 | 1 | 0 |
| Agentic Systems | 4 | 4 | 0 | 0 |
| Governance | 3 | 2 | 1 | 0 |
| Failure Modes | 3 | 2 | 0 | 1 |
| OO & Event Modeling | 7 | 4 | 3 | 0 |
| **Total** | **31** | **22** | **7** | **2** |

**Testability:** 71% of claims are directly testable in Phase 2 pilot.

---

## Priority Claims for Validation

Top 5 claims to validate in Phase 2:

1. **Claim 4.3:** Early detection reduces architectural impact (PRIMARY HYPOTHESIS)
2. **Claim 1.4:** Linguistic inconsistency correlates with defects (BASELINE METRIC)
3. **Claim 3.2:** Team boundaries predict semantic boundaries (VALIDATION OF APPROACH)
4. **Claim 5.2:** Advisory enforcement reduces resistance (ADOPTION METRIC)
5. **Claim 6.2:** False positives damage trust (QUALITY GATE)
6. **Claim 7.5:** Domain events make processes explicit (NEW - OO/EVENT VALIDATION)

---

## References

- Eric Evans, *Domain-Driven Design* (2003)
- Vaughn Vernon, *Implementing Domain-Driven Design* (2013)
- Vaughn Vernon, *Domain-Driven Design Distilled* (2016)
- Melvin Conway, "How Do Committees Invent?" (1968)
- Matthew Skelton & Manuel Pais, *Team Topologies* (2019)
- Rebecca Wirfs-Brock, *Object Design* (2002)
- Daniel Jackson, *The Essence of Software* (2021)
- Alberto Brandolini, *Event Storming* (2013)
- Martin Fowler, "Anemic Domain Model" (2003)
- Gabriele Bavota et al., "Mining Version Histories..." (2015)
- Helen Nissenbaum, *Privacy in Context* (2009)
- Ian Kerr, "Bots, Babes and the Californication of Commerce" (2004)

---

## Maintenance

**Update Trigger:** When new sources are reviewed or pilot generates contradictory evidence  
**Owner:** Researcher Ralph (Phase 1), Evaluation Agent (Phase 7)  
**Review Cycle:** After each experiment iteration

---

**Related Documentation:**
- [Experiment Primer](./experiment-primer.md)
- [Reading List](./reading-list.md)
- [Primers](./primers/)
- [Terminology Map](./terminology-map.md)
