# Primer: Conway's Law and Semantic Boundaries

**Reading Time:** ~10 minutes  
**Version:** 1.0.0  
**Date:** 2026-02-09  
**Concept:** Conway's Law applied to vocabulary and linguistic drift

---

## What It Is

**Conway's Law** (1968): "Organizations design systems that mirror their communication structures."

**Applied to language:** Team boundaries predict semantic boundaries. How people are organized shapes what words mean and where terminology conflicts occur.

**Not:** A suggestion or best practice  
**Not:** Prescriptive (telling you how to organize)  
**Is:** **Descriptive** (observing what actually happens)

---

## The Original Observation

Melvin Conway noticed that system architecture **is isomorphic to** organizational structure:

> "If you have four teams working on a compiler, you'll get a four-pass compiler."

**Why this happens:**
- Teams communicate most within themselves
- Cross-team communication is expensive
- System boundaries form where communication boundaries exist
- Architecture reflects who talks to whom

**Implication:** If you don't design your organization, your organization will design your software anyway—just badly.

---

## Conway's Law Applied to Vocabulary

### The Linguistic Corollary

**If system structure mirrors communication structure, then vocabulary structure mirrors communication structure too.**

**Observable patterns:**

| Organizational Pattern | Linguistic Pattern |
|-----------------------|-------------------|
| Teams rarely talk | Same word, different meanings |
| Teams talk frequently | Converged vocabulary |
| Hierarchical reporting | Vocabulary flows downward (executives' terms become "official") |
| Siloed departments | Each develops distinct jargon |
| Cross-functional collaboration | Hybrid vocabulary emerges |
| Reorganization | Vocabulary churn and confusion |

**Key Insight:** Language drift is often a **symptom** of organizational structure, not just lack of discipline.

---

## How Team Boundaries Predict Semantic Boundaries

### Example: E-Commerce Platform

Consider a company with these teams:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Frontend   │     │   Backend    │     │  Data Team   │
│   Team       │────▶│   Team       │────▶│              │
└──────────────┘     └──────────────┘     └──────────────┘
     (5 people)           (8 people)           (4 people)
```

**Conway's Law predicts:**
- Strong vocabulary convergence **within** each team
- Weaker alignment **between** teams
- Translation friction at handoff points

**Observed terminology for "user action":**

| Team | Term Used | Why |
|------|-----------|-----|
| **Frontend** | "click event" | Think in UI interactions |
| **Backend** | "action request" | Think in API calls |
| **Data** | "user behavior event" | Think in analytics schema |

**Result:** Same concept, three names. Not because teams are sloppy—because **they operate in different communication contexts.**

---

### The Reverse Implication

**If linguistic boundaries appear, check for organizational boundaries.**

**Diagnostic:**
- Two parts of the codebase use the same word differently?
  - **Hypothesis:** Different teams own those parts
- Documentation from two sources conflicts on terminology?
  - **Hypothesis:** Owned by teams with weak communication
- New term suddenly proliferates?
  - **Hypothesis:** New team or reorganization introduced it

**Actionable:** Linguistic conflicts are often **team topology problems** disguised as vocabulary problems.

---

## Team Topologies and Vocabulary Prediction

### The Four Fundamental Team Types

Matthew Skelton and Manuel Pais (2019) identified four team patterns:

| Team Type | Vocabulary Responsibility | Example Terms |
|-----------|-------------------------|---------------|
| **Stream-Aligned** | Owns domain vocabulary for their value stream | "Order," "Shipment," "Customer" |
| **Platform** | Provides shared technical vocabulary | "Authentication," "Deployment," "Logging" |
| **Enabling** | Teaches practice vocabulary | "Pair Programming," "TDD," "Refactoring" |
| **Complicated Subsystem** | Encapsulates specialized vocabulary | "ML Model," "Tax Calculation," "Fraud Detection" |

**Key Insight:** Different team types have **different vocabulary concerns**. Trying to unify them creates confusion.

---

### Stream-Aligned Teams and Bounded Contexts

**Stream-aligned teams** (teams aligned to value streams) naturally map to **bounded contexts**:

| Team | Value Stream | Bounded Context | Vocabulary |
|------|-------------|----------------|------------|
| **Checkout Team** | Purchase flow | Checkout Context | Cart, Payment, Billing Address |
| **Fulfillment Team** | Order processing | Fulfillment Context | Order, Shipment, Warehouse, Inventory |
| **Support Team** | Customer issues | Support Context | Ticket, Resolution, Escalation |

**Conway's Law in action:** Each team develops **local linguistic coherence** because they talk to each other daily. Attempting global unification fights this natural convergence.

---

### Cognitive Load and Vocabulary Size

**Cognitive load** (Skelton & Pais): The mental capacity required to understand and modify a system.

**Applied to vocabulary:**
- Teams can internalize ~50-100 terms with precise meanings
- Beyond that, cognitive overload → people ignore the glossary
- Global glossaries often contain 500+ terms → unusable

**Implication:** **Bounded contexts are not optional—they're a cognitive load management strategy.**

---

## When Language Drift Signals Topology Problems

### Symptom 1: Persistent Terminology Conflicts

**Observation:** Two teams keep re-litigating what "customer" means.

**Conway's Law diagnosis:** Teams have **misaligned incentives** or **unclear ownership boundaries**.

**Fix:** Not a glossary—fix the team topology.

---

### Symptom 2: Vocabulary Churn After Reorganization

**Observation:** After reorg, terms shift, old terminology conflicts with new.

**Conway's Law diagnosis:** New communication structure → new vocabulary structure (expected).

**Fix:** Expect linguistic turbulence. Document transitions explicitly.

---

### Symptom 3: "Translation Layer" Teams

**Observation:** A team exists primarily to mediate between two other teams.

**Conway's Law diagnosis:** Communication gap between teams → vocabulary gap → need for translator.

**Fix:** Reconsider if the two teams should be separate or merged.

---

### Symptom 4: Vocabulary Overlap Without Shared Understanding

**Observation:** Two teams use the same term but mean different things.

**Conway's Law diagnosis:** Teams don't talk to each other but share a domain concern → collision.

**Fix:** Either increase communication (shared understanding) or formalize separate contexts (accept difference).

---

## What Conway's Law Does NOT Mean

### Misconception 1: "Just Copy the Org Chart"

Conway's Law is **descriptive**, not **prescriptive**. It observes what happens, not what should happen.

**Wrong approach:** "We have 5 teams, so we need 5 bounded contexts."  
**Right approach:** "We have linguistic conflicts. Where do they align with team boundaries? Should we adjust teams or contexts?"

---

### Misconception 2: "Conway's Law Justifies Any Structure"

**No.** Conway's Law says your architecture will mirror your organization—not that your organization is optimal.

**Implication:** If your team structure is dysfunctional, your architecture will be dysfunctional.

---

### Misconception 3: "Language Standardization Defeats Conway's Law"

**No.** Forcing vocabulary unification across teams that don't communicate creates **performative compliance**, not genuine alignment.

**Result:** People say the "official" terms in meetings, use their own terms internally. The glossary diverges from reality.

---

## Known Failure Modes

### Failure Mode 1: Ignoring the Law

**Symptom:** Architecture team designs "ideal" bounded contexts that don't align with team structure.

**Why it fails:** Teams will reinterpret the model to match their communication patterns anyway. Official architecture diverges from reality.

**Mitigation:** Design contexts **with** team structure in mind. If contexts and teams don't align, one will change—usually the contexts.

---

### Failure Mode 2: Using Conway's Law as Excuse for Dysfunction

**Symptom:** "We can't align terminology because Conway's Law says we're stuck with our org structure."

**Why it fails:** Conway's Law observes reality—it doesn't prevent you from changing reality.

**Mitigation:** If team structure causes linguistic chaos, **change the team structure**.

---

### Failure Mode 3: Over-Fragmenting Contexts

**Symptom:** Every team gets its own bounded context, even for small teams or teams with high collaboration.

**Why it fails:** Too many contexts → too much translation overhead.

**Mitigation:** Contexts should align with **value streams**, not just team boundaries. Multiple teams can share a context if they collaborate closely.

---

### Failure Mode 4: Vocabulary-Driven Reorganizations

**Symptom:** "We need to reorganize so that our org chart matches our glossary."

**Why it fails:** Reorganizations are expensive. Vocabulary is cheaper to adjust.

**Mitigation:** Start with vocabulary alignment (translation at boundaries). Reorganize only if fundamental misalignment persists.

---

## Applicability in This Context (Agentic Monitoring)

### How Agentic Systems Use Conway's Law

**Prediction:** Use team structure to **predict** where linguistic conflicts will occur.

```yaml
teams:
  - name: Checkout Team
    bounded_context: Checkout
    expected_terms: [Cart, Payment, Checkout, BillingAddress]
  
  - name: Fulfillment Team
    bounded_context: Fulfillment
    expected_terms: [Order, Shipment, Warehouse, Inventory]

boundaries:
  - from: Checkout
    to: Fulfillment
    translation_required: true
    conflict_risk: high  # Different teams, handoff point
```

**Agent behavior:**
- Monitor terminology **within** each context
- Flag drift when Checkout Team uses Fulfillment vocabulary (or vice versa)
- Expect translation at Checkout → Fulfillment boundary
- Alert if translation layer is missing (boundary leak)

---

### Detecting Topology Misalignment

**Agent observation patterns:**

| Pattern | Diagnosis | Recommendation |
|---------|-----------|----------------|
| High conflict rate between two teams | Unclear boundary or missing communication | Increase collaboration or formalize boundary |
| Team using terms from multiple contexts | Team spans multiple concerns | Consider splitting responsibilities |
| Translation code growing complex | Boundary not aligned with value stream | Re-examine context boundaries |
| Vocabulary churn after reorg | Expected Conway's Law effect | Document transition, expect stabilization in 3-6 months |

**Value:** Agents surface organizational problems through linguistic evidence.

---

## Glossary Seed Terms

| Term | Definition | Context |
|------|------------|---------|
| **Conway's Law** | Observation that system architecture mirrors organizational communication structure | Organizational Theory |
| **Isomorphism** | Structural similarity/correspondence between two domains | Theory |
| **Linguistic Corollary** | Extension of Conway's Law: vocabulary structure mirrors communication structure | Applied Theory |
| **Stream-Aligned Team** | Team organized around a value stream (product, service, or user journey) | Team Topologies |
| **Platform Team** | Team providing foundational capabilities to stream-aligned teams | Team Topologies |
| **Enabling Team** | Team that helps other teams improve capabilities | Team Topologies |
| **Complicated Subsystem Team** | Team owning specialized domain requiring deep expertise | Team Topologies |
| **Cognitive Load** | Mental capacity required to understand and modify a system | Team Topologies |
| **Vocabulary Churn** | Rapid terminology changes, often following organizational restructuring | Symptom |
| **Performative Compliance** | Saying "official" terms publicly while using different terms internally | Anti-pattern |

---

## Key Claims (Source-Grounded)

### Melvin Conway, "How Do Committees Invent?" (1968)

**Claim 1:** "Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations."
- **Implication:** Architectural independence requires organizational independence.

**Claim 2:** "Because the design that occurs first is almost never the best possible, the prevailing system concept may need to change."
- **Implication:** First organizational structure is rarely optimal—expect evolution.

---

### Matthew Skelton & Manuel Pais, *Team Topologies* (2019)

**Claim 3:** "Cognitive load should be the primary consideration when designing team responsibilities."
- **Implication:** Teams can't internalize unlimited vocabulary—bounded contexts reduce cognitive load.

**Claim 4:** "Stream-aligned teams own the full value stream and make decisions quickly."
- **Implication:** Stream-aligned teams naturally develop coherent domain vocabulary.

**Claim 5:** "The interaction mode between teams determines the type of communication that happens."
- **Implication:** Collaboration mode predicts vocabulary alignment. Weak interaction → vocabulary divergence.

---

## How to Act Differently

### Before This Primer
- Treat vocabulary conflicts as discipline problems
- Design bounded contexts independent of team structure
- Expect global glossary to overcome organizational silos
- Reorganize without anticipating linguistic turbulence

### After This Primer
- Treat vocabulary conflicts as signals of organizational structure
- Design bounded contexts informed by team communication patterns
- Accept that local vocabulary convergence is natural and valuable
- Expect and document vocabulary churn after reorganizations

### Concrete Actions
1. **Map teams to contexts:** Where do team boundaries and context boundaries align? Where do they diverge?
2. **Identify high-conflict zones:** Where do two teams keep re-litigating terminology? Is there a topology issue?
3. **Use Conway's Law predictively:** Before launching a new team, predict what vocabulary conflicts will emerge
4. **Monitor reorgs linguistically:** After reorganization, track terminology churn—stabilization signals successful transition
5. **Don't fight the law:** If team structure and context structure can't align, adjust one or the other—don't pretend it doesn't matter

---

## Connection to Other Concepts

- **Primer 01: Ubiquitous Language** - Conway's Law explains why alignment is hard
- **Primer 02: Bounded Contexts** - Team structure informs context boundaries
- **Primer 04: Agentic Feasibility** - Agents detect topology issues through linguistic evidence

---

## Quality Gate Check

✅ **Can a tired engineer read this in ~10 minutes?** Yes (~2,000 words)  
✅ **Does it answer "how do I act differently?"** Yes (concrete actions section)  
✅ **Are failure modes explicit?** Yes (4 documented)  
✅ **Are limitations clear?** Yes (what it doesn't mean)  
✅ **Are glossary terms extractable?** Yes (10 seed terms)

---

## References

- Melvin Conway, "How Do Committees Invent?" (1968)
- Matthew Skelton & Manuel Pais, *Team Topologies* (2019)
- Eric Evans, *Domain-Driven Design* (2003), Chapter 14
- [Experiment Primer](../experiment-primer.md)
- [Reading List](../reading-list.md)

---

**Previous:** [Primer 02: Bounded Contexts](./02-bounded-contexts-linguistic-governance.md)  
**Next:** [Claim Inventory](../claim-inventory.md)
