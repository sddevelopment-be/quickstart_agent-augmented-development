# Primers: Focused Concept Guides

**Purpose:** Short, focused primers (10-minute reads) on core concepts for the ubiquitous language experiment  
**Reading Order:** Sequential (each builds on previous)  
**Total Reading Time:** ~40 minutes

---

## Available Primers

### [Primer 01: Ubiquitous Language as Operational Practice](./01-ubiquitous-language-operational-practice.md)
**Reading Time:** ~10 minutes  
**Concepts:** Ubiquitous language, translation errors, linguistic collaboration, living documentation

**What you'll learn:**
- Why ubiquitous language matters more than tactical DDD patterns
- How to embed domain language directly in code (no translation layer)
- Common failure modes (Dictionary DDD, technical jargon wins)
- How agentic systems enable continuous linguistic monitoring

**Key Takeaway:** Language fragmentation predicts system problems. Converging on shared vocabulary between domain experts and developers eliminates translation errors.

---

### [Primer 02: Bounded Contexts as Linguistic Governance](./02-bounded-contexts-linguistic-governance.md)
**Reading Time:** ~10 minutes  
**Concepts:** Bounded contexts, semantic boundaries, context mapping, translation patterns

**What you'll learn:**
- Why global glossaries fail (cognitive load, context-dependent meaning)
- How bounded contexts legitimize local vocabulary differences
- Context mapping patterns (ACL, published language, shared kernel)
- Translation at boundaries (required, not failure)

**Key Takeaway:** Agreement is local, not global. Each bounded context owns its vocabulary. Translation at boundaries is deliberate architectural work.

---

### [Primer 03: Conway's Law and Semantic Boundaries](./03-conways-law-semantic-boundaries.md)
**Reading Time:** ~10 minutes  
**Concepts:** Conway's Law, team topologies, vocabulary structure, organizational alignment

**What you'll learn:**
- How team boundaries predict semantic boundaries (linguistic corollary)
- Why misaligned topology creates persistent language conflicts
- Team types and their vocabulary responsibilities (stream-aligned, platform, enabling)
- How to diagnose topology problems through linguistic evidence

**Key Takeaway:** Vocabulary structure mirrors communication structure. Language drift is often a symptom of organizational structure, not just lack of discipline.

---

### [Primer 04: Object-Oriented and Event-Based Modeling in DDD](./04-oo-event-modeling-ddd.md)
**Reading Time:** ~10 minutes  
**Concepts:** Responsibility-driven design, concept-based design, domain events, Event Storming

**What you'll learn:**
- How OO responsibility assignment embodies ubiquitous language (CRC cards)
- Concept-based design: purpose, operational principle, state
- Domain events as business-significant state changes (past tense naming)
- Event Storming for collaborative domain discovery
- Common failure modes (anemic models, event explosion)

**Key Takeaway:** Objects and events are linguistic anchors, not technical constructs. Responsibility-driven design and event modeling make domain concepts explicit through ubiquitous language.

---

## Reading Paths

### For Engineers
**Goal:** Understand practical application

1. Start with Primer 01 (ubiquitous language basics)
2. Read Primer 04 (OO and event modeling - hands-on design)
3. Read Primer 02 (when to split contexts)
4. Skim Primer 03 (organizational context)

**Time:** 30-35 minutes

---

### For Architects
**Goal:** Understand strategic design

1. Read all four primers sequentially
2. Review [Context Map](../concept-map.md) for relationships
3. Check [Claim Inventory](../claim-inventory.md) for testable hypotheses

**Time:** 50-65 minutes

---

### For Team Leads
**Goal:** Understand organizational implications

1. Start with Primer 03 (Conway's Law)
2. Read Primer 02 (bounded contexts)
3. Read Primer 01 (ubiquitous language)
4. Read Primer 04 (OO and event modeling) if involved in design sessions

**Time:** 30-40 minutes

---

## How to Use These Primers

### Quality Gates

Each primer includes a quality gate checklist:
- ✅ Can a tired engineer read this in ~10 minutes?
- ✅ Does it answer "how do I act differently?"
- ✅ Are failure modes explicit?
- ✅ Are limitations clear?
- ✅ Are glossary terms extractable?

### Glossary Integration

Each primer contributes seed terms to the [Terminology Map](../terminology-map.md):
- **Primer 01:** 6 terms (ubiquitous language, translation error, living documentation, etc.)
- **Primer 02:** 10 terms (bounded context, ACL, context map, semantic boundary, etc.)
- **Primer 03:** 10 terms (Conway's Law, team topologies, cognitive load, etc.)
- **Primer 04:** 10 terms (responsibility-driven design, CRC card, concept, domain event, Event Storming, etc.)

**Total:** 36 seed terms for Phase 2 glossary expansion

**Total:** 36 seed terms for Phase 2 glossary expansion

---

## Key Claims by Primer

### Primer 01 Claims
1. "A project faces serious problems when its language is fractured." (Evans)
2. Code must use domain language directly, not technical abstractions
3. If code and conversations use different terminology, the model has failed
4. Refactoring names is not optional—it's maintaining linguistic integrity

### Primer 02 Claims
1. Multiple models are necessary; attempting unification causes bugs
2. Each bounded context has its own ubiquitous language
3. Bounded context is conceptual boundary, not technical boundary
4. Translation required at boundaries, not unification

### Primer 03 Claims
1. System structure mirrors organizational communication structure (Conway)
2. Vocabulary structure mirrors communication structure (linguistic corollary)
3. Cognitive load limits vocabulary size teams can internalize
4. Stream-aligned teams naturally develop coherent domain vocabulary

### Primer 04 Claims
1. "Good names reveal intention and responsibilities" (Wirfs-Brock)
2. "Concepts are the atoms of software design" (Jackson)
3. Domain events make implicit processes explicit (Evans)
4. Event Storming creates shared understanding faster than traditional requirements (Brandolini)

---

## Connection to Experiment

These primers ground the **ubiquitous language experiment hypothesis:**

> **Language drift precedes architectural drift by 2-4 weeks. Agentic systems can detect linguistic patterns that serve as early signals for architectural interventions.**

### How Primers Support Experiment

| Primer | Experiment Support |
|--------|-------------------|
| **01: Ubiquitous Language** | Establishes why linguistic monitoring matters (translation errors compound) |
| **02: Bounded Contexts** | Defines governance structure (enforcement tiers per context relationship) |
| **03: Conway's Law** | Predicts where conflicts occur (team boundaries → semantic boundaries) |
| **04: OO & Event Modeling** | Shows how objects/events embody ubiquitous language in code |

---

## Failure Modes Documented

### Primer 01 Failure Modes
1. **Dictionary DDD** - Glossary created, never enforced
2. **Technical Jargon Wins** - Developers dominate, domain experts disengage
3. **Premature Standardization** - Locking in wrong terms creates debt
4. **Ignoring Sociolinguistic Reality** - Forced unification creates resistance

### Primer 02 Failure Modes
1. **Premature Boundaries** - Drawing contexts before understanding domain
2. **Ignoring Translation Costs** - Too many small contexts = too much translation
3. **Context = Microservice Dogma** - Conflating semantic and deployment boundaries
4. **Missing Context Maps** - Relationships stay implicit, complexity hidden

### Primer 03 Failure Modes
1. **Ignoring Conway's Law** - Ideal contexts don't align with team structure
2. **Using Law as Excuse** - "We can't change because Conway's Law"
3. **Over-Fragmenting Contexts** - Every team gets a context regardless of collaboration
4. **Vocabulary-Driven Reorgs** - Expensive solution to cheap problem

### Primer 04 Failure Modes
1. **"Perfect Object Model" Paralysis** - Spending weeks designing before coding
2. **Anemic Domain Models** - Objects as data bags, all logic in services
3. **Event Explosion** - Hundreds of fine-grained events overwhelming signal
4. **Technical Events Leak** - Infrastructure events (DatabaseUpdated) instead of domain events
5. **CRC Cards as Theater** - Creating beautiful cards, filing away, never updating

---

## Next Steps

After reading these primers:

1. **Review [Terminology Map](../terminology-map.md)** - See all 40 seed terms with definitions
2. **Check [Claim Inventory](../claim-inventory.md)** - Understand what's testable in Phase 2
3. **Read [Experiment Primer](../experiment-primer.md)** - Full experiment overview (15 min)
4. **Decide on Phase 2** - Pilot selection or archive

---

## Maintenance

**Update Trigger:** When pilot feedback contradicts primer content  
**Ownership:** Researcher Ralph (research phase), Primer Agent (synthesis phase)  
**Review Cycle:** After each experiment stage  
**Versioning:** Semantic versioning (1.0.0 = initial, 1.1.0 = refinements, 2.0.0 = major changes)

---

## References

- [Experiment Primer](../experiment-primer.md) - Comprehensive overview
- [Reading List](../reading-list.md) - Annotated sources
- [Concept Map](../concept-map.md) - Visual relationships
- [Research Findings](../research-findings-summary.md) - Executive summary

---

**Status:** ✅ Phase 1 Extended - 4 primers delivered  
**Quality Gates:** All passed  
**Next:** Phase 2 pilot selection and glossary expansion
