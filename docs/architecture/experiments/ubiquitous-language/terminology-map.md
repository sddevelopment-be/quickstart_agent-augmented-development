# Terminology Map: Glossary Seed Terms

**Version:** 1.0.0  
**Date:** 2026-02-09  
**Purpose:** Early terminology catalog extracted from Phase 1 primers  
**Status:** Seed terms (20-30) for Phase 2 expansion

---

## Overview

This document catalogs **seed terms** extracted from Phase 1 research and primers. These terms form the foundation for a living glossary to be expanded during Phase 2 (pilot).

**Structure:**
- **Term:** Canonical name
- **Definition:** Clear, concise explanation
- **Context:** Where this term applies (DDD Core, specific bounded context, etc.)
- **Source:** Which primer or document introduced it
- **Related Terms:** Connections to other terms
- **Status:** Canonical | Candidate | Under Review

---

## Core DDD Concepts (Foundational)

### Ubiquitous Language

**Definition:** Shared vocabulary between domain experts and developers, used consistently in all communication—conversations, documentation, code, and tests.

**Context:** DDD Core (applies universally)  
**Source:** Primer 01  
**Related Terms:** Bounded Context, Translation Error, Linguistic Collaboration  
**Status:** Canonical

**Why it matters:** Primary mechanism for eliminating translation errors between business and technical domains.

---

### Bounded Context

**Definition:** Explicit boundary within which a domain model and its ubiquitous language have clear, consistent meaning. Outside that boundary, the same words may mean different things.

**Context:** DDD Core (applies universally)  
**Source:** Primer 02  
**Related Terms:** Ubiquitous Language, Semantic Boundary, Context Map  
**Status:** Canonical

**Why it matters:** Legitimizes local vocabulary differences; prevents forced global unification.

---

### Semantic Boundary

**Definition:** Division based on meaning (how terms are used), not technology or organizational structure.

**Context:** DDD Strategic Design  
**Source:** Primer 02  
**Related Terms:** Bounded Context, Translation, Conway's Law  
**Status:** Canonical

**Why it matters:** Distinguishes linguistic boundaries from technical or team boundaries.

---

### Context Map

**Definition:** Visual diagram showing relationships between bounded contexts, including upstream/downstream flows and translation patterns.

**Context:** DDD Strategic Design  
**Source:** Primer 02  
**Related Terms:** Bounded Context, Anti-Corruption Layer, Published Language  
**Status:** Canonical

**Why it matters:** Makes context relationships explicit; informs architectural decisions.

---

### Translation (at boundaries)

**Definition:** Deliberate conversion of concepts when information crosses from one bounded context to another.

**Context:** DDD Strategic Design  
**Source:** Primer 02  
**Related Terms:** Anti-Corruption Layer, Context Map, Bounded Context  
**Status:** Canonical

**Why it matters:** Acknowledges that forcing global terminology unification creates brittleness.

---

## Context Mapping Patterns

### Anti-Corruption Layer (ACL)

**Definition:** Translation layer protecting downstream context from upstream changes. Isolates local model from external influence.

**Context:** Context Mapping Pattern  
**Source:** Primer 02  
**Related Terms:** Upstream/Downstream, Translation, Bounded Context  
**Status:** Canonical

**Why it matters:** Preserves linguistic autonomy of downstream context.

---

### Upstream/Downstream

**Definition:** Data flow relationship where upstream context provides information, downstream context consumes it. Upstream changes can impact downstream.

**Context:** Context Mapping Pattern  
**Source:** Primer 02  
**Related Terms:** Anti-Corruption Layer, Context Map  
**Status:** Canonical

**Why it matters:** Defines power dynamics and risk in context relationships.

---

### Published Language

**Definition:** Stable API that upstream context exposes for multiple downstream consumers. Often uses industry-standard format (JSON, XML, etc.).

**Context:** Context Mapping Pattern  
**Source:** Primer 02  
**Related Terms:** Open Host Service, Upstream/Downstream  
**Status:** Canonical

**Why it matters:** Decouples upstream from knowing all downstream consumers.

---

### Shared Kernel

**Definition:** Small, carefully controlled subset of model shared between contexts. Requires high coordination.

**Context:** Context Mapping Pattern  
**Source:** Primer 02  
**Related Terms:** Bounded Context, Partnership  
**Status:** Canonical

**Why it matters:** Sharing creates coupling; keep minimal.

---

### Conformist

**Definition:** Downstream context accepts upstream model without translation. Surrenders linguistic autonomy.

**Context:** Context Mapping Pattern  
**Source:** Primer 02  
**Related Terms:** Upstream/Downstream, Anti-Corruption Layer (alternative)  
**Status:** Canonical

**Why it matters:** Sometimes pragmatic (authoritative upstream), but loses local control.

---

## Organizational and Process Terms

### Conway's Law

**Definition:** Observation that system architecture mirrors organizational communication structure. "Organizations design systems that mirror their communication structures."

**Context:** Organizational Theory  
**Source:** Primer 03  
**Related Terms:** Team Topologies, Semantic Boundary, Linguistic Corollary  
**Status:** Canonical

**Why it matters:** Predicts where linguistic and architectural boundaries will form based on team structure.

---

### Linguistic Corollary (to Conway's Law)

**Definition:** Extension of Conway's Law: vocabulary structure mirrors communication structure. Teams that communicate frequently converge on shared terminology.

**Context:** Applied Theory  
**Source:** Primer 03  
**Related Terms:** Conway's Law, Semantic Boundary  
**Status:** Canonical

**Why it matters:** Explains why team boundaries predict terminology conflicts.

---

### Stream-Aligned Team

**Definition:** Team organized around a value stream (product, service, or user journey). Owns domain vocabulary for their stream.

**Context:** Team Topologies  
**Source:** Primer 03  
**Related Terms:** Platform Team, Bounded Context, Cognitive Load  
**Status:** Canonical

**Why it matters:** Stream-aligned teams naturally develop coherent domain vocabulary; often map to bounded contexts.

---

### Platform Team

**Definition:** Team providing foundational capabilities (infrastructure, tooling) to stream-aligned teams. Provides shared technical vocabulary.

**Context:** Team Topologies  
**Source:** Primer 03  
**Related Terms:** Stream-Aligned Team, Shared Language  
**Status:** Canonical

**Why it matters:** Platform vocabulary (e.g., "authentication," "deployment") distinct from domain vocabulary.

---

### Enabling Team

**Definition:** Team that helps other teams improve capabilities through coaching and facilitation. Teaches practice vocabulary.

**Context:** Team Topologies  
**Source:** Primer 03  
**Related Terms:** Stream-Aligned Team  
**Status:** Canonical

**Why it matters:** Introduces practice terms (e.g., "TDD," "pair programming") across teams.

---

### Complicated Subsystem Team

**Definition:** Team owning specialized domain requiring deep expertise. Encapsulates specialized vocabulary.

**Context:** Team Topologies  
**Source:** Primer 03  
**Related Terms:** Stream-Aligned Team, Bounded Context  
**Status:** Canonical

**Why it matters:** Protects rest of organization from needing to understand complex specialized terms.

---

### Cognitive Load

**Definition:** Mental capacity required to understand and modify a system. Limits how much vocabulary a team can internalize.

**Context:** Team Topologies / Psychology  
**Source:** Primer 03  
**Related Terms:** Bounded Context, Vocabulary Size  
**Status:** Canonical

**Why it matters:** Justifies why bounded contexts are necessary (humans can't memorize unlimited precise terms).

---

## Practice and Process Terms

### Linguistic Collaboration

**Definition:** Continuous conversation between domain experts and developers to refine shared vocabulary. Ubiquitous language emerges through this process.

**Context:** DDD Practice  
**Source:** Primer 01  
**Related Terms:** Ubiquitous Language, Living Documentation  
**Status:** Canonical

**Why it matters:** Language isn't created through workshops—it emerges through ongoing modeling conversations.

---

### Living Documentation

**Definition:** Documentation (tests, code) that stays synchronized with domain understanding because it uses ubiquitous language directly.

**Context:** DDD Practice  
**Source:** Primer 01  
**Related Terms:** Ubiquitous Language, Acceptance Tests  
**Status:** Canonical

**Why it matters:** If code speaks domain language, code becomes documentation.

---

### Translation Error

**Definition:** Misunderstanding caused by converting between domain language and technical language in developers' heads.

**Context:** Problem Space  
**Source:** Primer 01  
**Related Terms:** Ubiquitous Language (solution)  
**Status:** Canonical

**Why it matters:** Quantifies the cost of not having ubiquitous language.

---

### Register Variation

**Definition:** Normal differences in how people speak based on role, context, or seniority. Same person uses different formality in meetings vs. code comments.

**Context:** Sociolinguistics  
**Source:** Primer 01  
**Related Terms:** Performative Compliance (anti-pattern when forced)  
**Status:** Canonical

**Why it matters:** Helps distinguish normal variation from problematic drift; prevents false positives.

---

## Anti-Patterns and Failure Modes

### Dictionary DDD

**Definition:** Anti-pattern where team creates a glossary document, considers DDD "done," never updates it. Glossary becomes stale instantly.

**Context:** DDD Anti-pattern  
**Source:** Primer 01  
**Related Terms:** Living Documentation (correct approach)  
**Status:** Canonical

**Why it matters:** Language must be enforced through usage (code, tests), not just documented.

---

### Linguistic Autonomy

**Definition:** Ability of a bounded context to define its own vocabulary without external imposition. Prerequisite for effective bounded contexts.

**Context:** Governance  
**Source:** Primer 02  
**Related Terms:** Bounded Context, Human in Charge  
**Status:** Canonical

**Why it matters:** Centralized glossary control violates autonomy; creates resistance.

---

### Translation Cost

**Definition:** Maintenance burden of converting concepts at context boundaries. Includes code complexity and cognitive overhead.

**Context:** Economics  
**Source:** Primer 02  
**Related Terms:** Anti-Corruption Layer, Bounded Context  
**Status:** Canonical

**Why it matters:** Too many contexts → too much translation. Balance independence against integration cost.

---

### Vocabulary Churn

**Definition:** Rapid terminology changes, often following organizational restructuring. Indicates linguistic turbulence.

**Context:** Symptom / Organizational Change  
**Source:** Primer 03  
**Related Terms:** Conway's Law, Reorganization  
**Status:** Canonical

**Why it matters:** Expected after reorgs; stabilization timeline (~3-6 months) predicts successful transition.

---

### Performative Compliance

**Definition:** Anti-pattern where people say "official" terms publicly while using different terms internally. Indicates forced unification has failed.

**Context:** Sociolinguistic Anti-pattern  
**Source:** Primer 03  
**Related Terms:** Register Variation, Linguistic Autonomy  
**Status:** Canonical

**Why it matters:** Signal that enforcement is too rigid or context boundaries are wrong.

---

## Agentic Monitoring Terms (Experiment-Specific)

### Human in Charge

**Definition:** Governance principle where humans retain ultimate accountability, authority, and decision-making power. Distinct from "human in the loop" (oversight only).

**Context:** Governance Principle (Experiment)  
**Source:** Experiment Primer  
**Related Terms:** Linguistic Autonomy, Agent as Sensor  
**Status:** Canonical

**Why it matters:** Agents observe and evidence; humans interpret, decide, and own outcomes.

---

### Agent as Sensor

**Definition:** Design pattern where agents detect and report linguistic patterns but do not make terminology decisions. Observation role, not authority role.

**Context:** Agentic Design (Experiment)  
**Source:** Experiment Primer  
**Related Terms:** Human in Charge  
**Status:** Canonical

**Why it matters:** Clarifies agent responsibility boundaries; prevents "glossary bot" perception.

---

### Linguistic Drift Detection

**Definition:** Automated observation of terminology usage patterns to identify conflicts (same word, multiple meanings) or divergence (different words, same concept).

**Context:** Agentic Capability (Experiment)  
**Source:** Experiment Primer  
**Related Terms:** Agent as Sensor, Early Detection  
**Status:** Canonical

**Why it matters:** Core experiment hypothesis—agents can surface drift before architectural impact.

---

### Enforcement Tiers

**Definition:** Graduated levels of terminology feedback: Advisory (comment only) → Acknowledgment (require confirmation) → Hard Failure (block merge).

**Context:** Governance (Experiment)  
**Source:** Experiment Primer  
**Related Terms:** Human in Charge, Linguistic Autonomy  
**Status:** Canonical

**Why it matters:** Default advisory prevents "linguistic policing"; escalate only with explicit human decision.

---

## Term Relationships

### Primary Dependencies

```
Ubiquitous Language
    ↓ scoped by
Bounded Context
    ↓ mapped via
Context Map
    ↓ shows relationships
Anti-Corruption Layer, Published Language, Shared Kernel
    ↓ implement
Translation (at boundaries)
```

### Organizational Foundation

```
Conway's Law
    ↓ predicts
Semantic Boundaries
    ↓ should align with
Team Topologies (Stream-Aligned, Platform, etc.)
    ↓ constrained by
Cognitive Load
    ↓ justifies
Bounded Contexts
```

### Agentic Layer

```
Agent as Sensor
    ↓ detects
Linguistic Drift
    ↓ surfaces via
Enforcement Tiers (Advisory → Acknowledgment → Hard)
    ↓ governed by
Human in Charge
    ↓ owns
Linguistic Autonomy (per context)
```

---

## Usage Statistics

**Total Seed Terms:** 30  
**Status Breakdown:**
- Canonical: 30 (100%)
- Candidate: 0
- Under Review: 0

**Category Breakdown:**
- Core DDD: 5 terms
- Context Mapping: 5 terms
- Organizational: 7 terms
- Practice: 4 terms
- Anti-patterns: 4 terms
- Agentic Monitoring: 5 terms

---

## Expansion Plan (Phase 2)

### Expected Growth

**Phase 2 (Pilot):**
- Add 20-30 context-specific terms from selected bounded context
- Add 10-15 technical terms from implementation
- Total vocabulary: 60-75 terms

**Phase 3+ (Ongoing):**
- Expand per bounded context (50-100 terms each)
- Maintain core glossary (these 30 terms stay stable)

---

### Quality Gates for New Terms

Before adding a term to the glossary:

1. ✅ **Is it used consistently?** (Not one-off usage)
2. ✅ **Does it have a clear owner?** (Context or team responsible)
3. ✅ **Is definition unambiguous?** (Domain expert can validate)
4. ✅ **Does it relate to existing terms?** (Not isolated)
5. ✅ **Is it non-obvious?** (Not generic like "data" or "info")

---

## Governance

**Ownership:** These 30 seed terms owned by **Experiment Core Team** (cross-context)  
**Update Trigger:** Refinement based on Phase 2 pilot feedback  
**Review Cycle:** After each experiment stage  
**Deprecation Policy:** Mark as deprecated (don't delete) if superseded

---

## References

- [Primer 01: Ubiquitous Language](./primers/01-ubiquitous-language-operational-practice.md)
- [Primer 02: Bounded Contexts](./primers/02-bounded-contexts-linguistic-governance.md)
- [Primer 03: Conway's Law](./primers/03-conways-law-semantic-boundaries.md)
- [Experiment Primer](./experiment-primer.md)
- [Claim Inventory](./claim-inventory.md)

---

**Status:** ✅ Seed terms extracted and documented  
**Next:** Phase 2 pilot selection and glossary expansion
