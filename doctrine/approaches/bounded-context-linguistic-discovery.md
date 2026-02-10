# Approach: Bounded Context Discovery via Linguistic Analysis

**Version:** 1.0.0  
**Date:** 2026-02-10  
**Status:** Active  
**Source:** Ubiquitous Language Experiment Research

---

## Purpose

Use **terminology patterns to identify hidden context boundaries** in software systems. This approach recognizes that semantic conflicts signal architectural boundaries that should be made explicit.

---

## Core Insight

**Same Words, Different Meanings = Hidden Boundary**

Bounded contexts are not arbitrary divisions—they emerge from genuine semantic boundaries in the domain. When the same term means different things to different teams, a context boundary already exists implicitly. Making it explicit prevents accidental coupling.

---

## Theoretical Foundation

### Conway's Law Applied to Semantics

**Observation:** Organizational communication structure predicts system architecture.

**Linguistic Corollary:** Vocabulary structure mirrors communication structure. Teams that communicate frequently converge on shared terminology. Teams with infrequent communication develop different vocabularies.

**Implication:** Team boundaries predict semantic boundaries. Where teams differ linguistically, context boundaries belong.

### Cognitive Load as Boundary Justification

**Constraint:** Humans can internalize ~50-100 precise domain terms effectively.

**Evidence:** Miller's Law (7±2 chunks), Working Memory limits, Team Topologies research.

**Implication:** Bounded contexts are necessary because no team can master unlimited terminology. Boundaries manage cognitive complexity.

---

## Discovery Techniques

### 1. Terminology Conflict Detection

**Pattern: Same Term, Different Meanings**

**Example:**
- **Sales Context:** "Order" = customer intent to purchase
- **Fulfillment Context:** "Order" = warehouse picking instruction
- **Accounting Context:** "Order" = revenue recognition trigger

**Signal:** Same word appears in multiple contexts with non-identical definitions.

**Action:** Propose context boundary at semantic divergence. Require translation layer.

---

**Pattern: Different Terms, Same Concept**

**Example:**
- **Frontend:** "User", "Account", "Profile"
- **Backend:** "Principal", "Identity", "Entity"
- **DB:** "User Record", "Auth Token", "Session"

**Signal:** Three different vocabularies for the same underlying concept.

**Action:** Consolidate within contexts, translate between contexts. Do not force global unification.

---

### 2. Communication Structure Analysis

**Method: Team Interaction Mapping**

Map organizational communication patterns to identify vocabulary clusters. This systematic analysis reveals where semantic boundaries align with (or contradict) team structure.

**See:** [Team Interaction Mapping Tactic](../../tactics/team-interaction-mapping.tactic.md) for detailed procedure

**Core Insight:** Teams that communicate infrequently develop different vocabularies. Where vocabulary diverges, context boundaries likely exist (Conway's Law).

**Validation Approach:** Ask teams to define the same term independently. If definitions differ significantly, a boundary exists.

---

### 3. Code and Documentation Analysis

**Technique: Semantic Cluster Analysis**

Extract terminology from codebase and documentation to identify implicit context boundaries through semantic clustering and ownership patterns.

**See:** [Code and Documentation Analysis Tactic](../../tactics/code-documentation-analysis.tactic.md) for step-by-step procedure

**Tools:** grep/rg, AST parsers, git log analysis, LLM-based semantic similarity

**Key Insight:** Terms that co-occur frequently and are owned by the same team likely belong to same bounded context. Terms with same name but different meanings signal hidden boundary.

---

### 4. Event Storming for Boundary Discovery

**Collaborative Workshop Technique**

Visual workshop using sticky notes to discover domain events, processes, and bounded contexts through collaborative mapping with domain experts.

**See:** [Event Storming Discovery Tactic](../../tactics/event-storming-discovery.tactic.md) for facilitation guide and PlantUML template

**Outcome:** Visual map of bounded contexts grounded in business processes and terminology, validated by stakeholders in real-time.

**Best For:** Complex domains, cross-functional alignment, rapid boundary discovery (2-4 hours vs weeks of analysis).

---

## Context Mapping Patterns

Once contexts are identified, define their relationships:

### Upstream/Downstream
**Definition:** Data flows from upstream (provider) to downstream (consumer). Upstream changes impact downstream.

**Linguistic Signal:** Downstream adopts upstream terminology, or translates it.

**Example:** Sales (upstream) → Fulfillment (downstream)

---

### Anti-Corruption Layer (ACL)
**Definition:** Translation layer protecting downstream from upstream changes. Downstream maintains its own model.

**Linguistic Signal:** Explicit term mapping at boundary (e.g., "Order" → "PickingInstruction").

**When to Use:** Downstream context must maintain linguistic independence.

---

### Shared Kernel
**Definition:** Small, carefully controlled subset of model shared between contexts. High coordination required.

**Linguistic Signal:** Exact same terms with identical definitions in both contexts.

**When to Use:** Rare. Only for core domain concepts requiring perfect synchronization.

**Warning:** Sharing creates coupling. Keep minimal.

---

### Published Language
**Definition:** Stable API using industry-standard format (JSON Schema, OpenAPI, etc.).

**Linguistic Signal:** Formal schema with explicit term definitions.

**When to Use:** Upstream serves multiple downstream consumers. Prevents tight coupling.

---

### Conformist
**Definition:** Downstream accepts upstream model without translation. Surrenders linguistic autonomy.

**Linguistic Signal:** Downstream uses upstream terminology exactly.

**When to Use:** Upstream is authoritative (e.g., regulatory, industry standard). Pragmatic trade-off.

**Warning:** Loses local control. Use only when necessary.

---

## When to Use

✅ **Use Bounded Context Discovery when:**
- Multiple teams work on same system
- Terminology conflicts arise frequently
- Team restructuring signals vocabulary churn
- Legacy monolith requires decomposition
- Domain complexity overwhelms single vocabulary

⚠️ **Exercise Caution when:**
- Team is small (<5 people, single context sufficient)
- Domain is simple and well-understood
- Organizational politics weaponize boundaries
- Context boundaries used to avoid communication

❌ **Do Not Use when:**
- Simple CRUD app with no domain complexity
- Prototyping phase (boundaries emerge later)
- Single team with shared understanding
- Forced decomposition for architectural fashion

---

## Integration with Doctrine Stack

### Related Approaches
- **[Language-First Architecture](language-first-architecture.md)** - Strategic framework
- **[Living Glossary Practice](living-glossary-practice.md)** - Maintenance workflow

### Related Directives
- **[Directive 018: Traceable Decisions](../directives/018_traceable_decisions.md)** - Document context boundaries in ADRs

### Related Tactics
- **[Context Boundary Inference](../tactics/context-boundary-inference.tactic.md)** - Step-by-step procedure
- **[Terminology Extraction and Mapping](../tactics/terminology-extraction-mapping.tactic.md)** - Data collection

---

## Success Criteria

**Context boundaries are well-defined when:**
- ✅ Each context has explicit ownership (team/role)
- ✅ Ubiquitous language documented per context
- ✅ Translation rules defined at boundaries
- ✅ No shared mutable state across contexts
- ✅ Teams understand their context relationships

**Validation Questions:**
1. Can each team define their key terms without external help?
2. Where definitions differ, do we have translation rules?
3. Are context relationships documented in a context map?
4. Do code modules align with context boundaries?
5. Can we change one context without breaking others?

---

## Failure Modes and Mitigations

### Failure Mode 1: Over-Decomposition
**Symptom:** Too many tiny contexts, excessive translation overhead  
**Cause:** Premature boundary creation, architectural fashion  
**Mitigation:** Start with fewer contexts, split only when cognitive load or team structure demands it

### Failure Mode 2: False Boundaries
**Symptom:** Boundaries that cut across natural process flows  
**Cause:** Organizational politics, technical convenience  
**Mitigation:** Validate with event storming, check if business workflows respect boundaries

### Failure Mode 3: Ignored Boundaries
**Symptom:** Boundaries defined but not enforced, vocabulary drift persists  
**Cause:** Lack of tooling, no ownership, insufficient training  
**Mitigation:** Implement glossary enforcement, assign owners, measure compliance

### Failure Mode 4: Rigid Boundaries
**Symptom:** Boundaries prevent necessary collaboration  
**Cause:** Overly strict enforcement, misunderstanding of purpose  
**Mitigation:** Boundaries manage complexity, not prevent communication. Allow translation, not isolation.

---

## Agent Relevance

**Primary Agents:**
- **Architect Alphonso:** Strategic context identification, mapping patterns
- **Analyst Annie:** Requirements analysis per context
- **Manager Mike:** Team alignment with contexts

**Supporting Agents:**
- **Bootstrap Bill:** Initial context setup
- **Lexical Larry:** Terminology consistency within contexts
- **Code Reviewer Cindy:** Boundary violation detection

---

## References

### Research Sources
- **Experiment Materials:** `docs/architecture/experiments/ubiquitous-language/`
- **Primer:** `02-bounded-contexts-linguistic-governance.md`
- **Concept Map:** `concept-map.md` (Section 4: DDD Core, Section 5: Conway's Law)

### Theoretical Foundation
- **Domain-Driven Design:** Eric Evans (2003), Vaughn Vernon (2013)
- **Conway's Law:** Melvin Conway (1968)
- **Team Topologies:** Matthew Skelton, Manuel Pais (2019)
- **Event Storming:** Alberto Brandolini (2013)

### Related Documentation
- **[DDD Core Concepts Reference](../docs/ddd-core-concepts-reference.md)** - Terminology
- **Conway's Law Patterns** - See organizational glossary in `.contextive/contexts/organizational.yml`

---

## Version History

- **1.0.0** (2026-02-10): Initial version extracted from ubiquitous language experiment research

---

**Curation Status:** ✅ Claire Approved (Doctrine Stack Compliant)
