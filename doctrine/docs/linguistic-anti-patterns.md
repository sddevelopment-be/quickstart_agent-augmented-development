# Linguistic Anti-Patterns Catalog

**Version:** 1.0.0  
**Date:** 2026-02-10  
**Purpose:** Catalog of common terminology misuse patterns  
**Audience:** Code reviewers, architects, lexical analysts

---

## Overview

This catalog documents recognizable patterns of terminology misuse that lead to architectural problems. Each anti-pattern includes:
- **Symptom:** How to recognize it
- **Cause:** Why it happens
- **Impact:** What problems it causes
- **Mitigation:** How to fix it

**Source:** `docs/architecture/experiments/ubiquitous-language/` research

---

## Category 1: Glossary Failures

### Dictionary DDD

**Symptom:** Glossary document exists but is never updated or referenced in code.

**Cause:** Team treats glossary as deliverable, not living artifact.

**Impact:**
- Glossary becomes stale within weeks
- Developers ignore glossary
- No enforcement mechanism
- "DDD theater" without actual practice

**Mitigation:**
- Integrate glossary into workflow (IDE plugins, PR checks)
- Assign ownership per bounded context
- Automate staleness detection
- See [Living Glossary Practice](../approaches/living-glossary-practice.md)

**Detection:**
```bash
# Check last glossary update
git log --oneline glossary.md | head -1

# If >6 months old, likely stale
```

---

### Glossary as Power Tool

**Symptom:** Glossary weaponized in organizational politics to enforce control.

**Cause:** Centralized authority, no bounded context autonomy.

**Impact:**
- Teams resist glossary adoption
- Performative compliance (say official terms, use internal terms)
- Trust erosion
- Innovation stifled

**Mitigation:**
- Bounded context authority (local glossaries)
- Default advisory enforcement
- Transparent decision history
- Escalation to leadership for conflicts

---

## Category 2: Terminology Drift

### Vocabulary Churn

**Symptom:** Rapid terminology changes, often following organizational restructuring.

**Cause:** Team reorganization, Conway's Law in action.

**Impact:**
- Code uses deprecated terms
- Documentation outdated
- Cross-team confusion
- Productivity drop

**Mitigation:**
- Expected after reorgs (3-6 month stabilization)
- Track deprecated terms explicitly
- Phased migration plan
- Don't enforce during churn period

**Detection:**
```bash
# Find deprecated term usage
rg "OldCustomer" --count
```

---

### Performative Compliance

**Symptom:** People say "official" terms publicly, use different terms internally (Slack, code comments).

**Cause:** Forced terminology unification, ignores register variation.

**Impact:**
- Official language disconnected from reality
- False sense of alignment
- Communication overhead (internal translation)

**Mitigation:**
- Recognize bounded contexts
- Allow local vocabulary differences
- Understand sociolinguistic register variation
- Don't enforce purity across contexts

**Detection:**
- Compare meeting notes with code comments
- Survey: "What terms do you actually use?"

---

## Category 3: Naming Problems

### Generic Names Correlate with High Coupling

**Symptom:** Classes/methods with generic names ("Manager", "Handler", "Data", "Info").

**Cause:** Insufficient domain understanding or lazy naming.

**Impact:**
- High coupling (measured empirically: r=0.67)
- Unclear responsibilities
- Difficult to refactor
- Maintenance burden

**Mitigation:**
- Use domain-specific names
- "Customer" not "User" (if domain uses "Customer")
- "OrderProcessor" not "DataHandler"
- Code review focus on naming

**Detection:**
```python
# Find generic names
rg "class.*Manager|class.*Handler|class.*Data|class.*Info" --count
```

**Evidence:** Bavota et al. (2015) - Empirical correlation study

---

### Translation Error (Missing Ubiquitous Language)

**Symptom:** Developers "translate" domain concepts into technical jargon mentally.

**Cause:** Code uses different terminology than domain experts.

**Impact:**
- Requirements misunderstandings
- Incorrect implementations
- Bugs introduced during maintenance
- Onboarding difficulty

**Mitigation:**
- Use ubiquitous language in code
- Name classes/methods using domain terms
- Write tests in business language
- Validate with domain experts

**Detection:**
- Show code to domain expert: "Do you recognize this?"
- If answer is "No", translation error exists

---

## Category 4: Context Boundary Problems

### Hidden Bounded Context Boundary

**Symptom:** Same term means different things in different parts of codebase.

**Cause:** Implicit context boundary not made explicit.

**Impact:**
- Accidental coupling
- Unexpected side effects
- Integration bugs
- Refactoring paralysis

**Mitigation:**
- Make boundary explicit
- Create separate models per context
- Translation layer at boundary
- Context map documentation

**Detection:**
```bash
# Find "Order" definitions
rg "class Order" --with-filename

# If multiple definitions with different fields → boundary exists
```

---

### Boundary Leak

**Symptom:** Vocabulary from one context used in another without translation.

**Cause:** Shared code, direct dependencies across contexts.

**Impact:**
- Context coupling
- Cannot evolve contexts independently
- Ripple effects from changes

**Mitigation:**
- Anti-Corruption Layer at boundary
- Published Language for integration
- Explicit translation rules

**Detection:**
```python
# Fulfillment code using Sales vocabulary
# BAD: directly using SalesOrder
from sales.models import SalesOrder

# GOOD: using FulfillmentOrder with ACL
from fulfillment.models import FulfillmentOrder
from fulfillment.acl import SalesOrderACL
```

---

## Category 5: Implementation Anti-Patterns

### Anemic Domain Model

**Symptom:** Domain objects are data bags (getters/setters only), all logic in "Service" classes.

**Cause:** Misunderstanding of OOP, procedural thinking.

**Impact:**
- Domain logic scattered
- No linguistic clarity (services don't speak domain language)
- Hard to find logic
- Difficult to test

**Mitigation:**
- Move behavior into domain objects
- Objects should DO things
- Responsibility-Driven Design
- Aggregate patterns

**Detection:**
```python
# BAD: Anemic
class Order:
    def __init__(self):
        self.items = []
        self.total = 0
    
    def get_items(self): return self.items
    def set_total(self, total): self.total = total

class OrderService:
    def calculate_total(self, order):  # Logic outside domain object
        total = sum(item.price for item in order.get_items())
        order.set_total(total)

# GOOD: Rich domain model
class Order:
    def __init__(self):
        self.items = []
    
    def add_item(self, item):
        self.items.append(item)
    
    def total(self):  # Logic inside domain object
        return sum(item.price for item in self.items)
```

---

### Event Explosion

**Symptom:** Too many fine-grained events (OrderLineItemQuantityChangedBy1) that obscure business significance.

**Cause:** Event sourcing without domain understanding.

**Impact:**
- Noise overwhelms signal
- Event handlers proliferate
- Performance degradation
- Difficult to reason about

**Mitigation:**
- Events should represent business-significant state changes
- Aggregate multiple technical changes into one domain event
- Ask: "Would domain expert care about this event?"

**Detection:**
- Count events per aggregate
- If >20 event types for one aggregate → explosion

---

## Category 6: Process Failures

### Linguistic Policing

**Symptom:** Glossary enforcement feels like compliance regime instead of collaboration.

**Cause:** Punitive defaults, centralized authority, hard failures.

**Impact:**
- Developer resentment
- Workarounds and suppressions
- Trust erosion
- Glossary abandonment

**Mitigation:**
- Default advisory enforcement
- Bounded context autonomy
- Justify hard failures in writing
- Annual retrospective on enforcement

**Detection:**
- Survey: "Is glossary helpful or annoying?"
- High suppression rate (>25% PRs override checks)

---

### False Positives / Review Fatigue

**Symptom:** Terminology checks flag normal variation, developers ignore feedback.

**Cause:** Poor context awareness, register variation misunderstood.

**Impact:**
- Trust in tooling erodes
- Real issues ignored
- Glossary abandoned

**Mitigation:**
- Confidence thresholds
- Understand sociolinguistic register
- Human review for ambiguous cases
- Continuous model tuning

**Detection:**
- False positive rate >30%
- Developers routinely suppress checks

---

## Detection Checklists

### For Code Reviewers (Cindy)

When reviewing PR, check:
- [ ] Are domain terms used consistently?
- [ ] Generic names flagged ("Manager", "Handler")?
- [ ] Cross-context vocabulary violations?
- [ ] Translation at boundaries present?
- [ ] New terminology documented in glossary?

### For Architects (Alphonso)

When reviewing architecture, check:
- [ ] Hidden context boundaries identified?
- [ ] Vocabulary ownership clear?
- [ ] Translation layers at boundaries?
- [ ] Same term, multiple meanings documented?
- [ ] Context map up to date?

### For Lexical Analysts (Larry)

When auditing repository, check:
- [ ] Glossary last updated (staleness)?
- [ ] Deprecated terms still in use (count)?
- [ ] Generic name frequency (coupling risk)?
- [ ] Terminology conflicts (same term, different meanings)?
- [ ] Register variation appropriately handled?

---

## Mitigation Priority

**High Priority (Fix Immediately):**
- Hidden bounded context boundaries (coupling risk)
- Translation errors (bug risk)
- Anemic domain models (maintenance burden)

**Medium Priority (Address in Refactoring):**
- Generic naming (technical debt)
- Boundary leaks (coupling accumulation)
- Vocabulary churn (post-reorg stabilization)

**Low Priority (Monitor):**
- Dictionary DDD (process improvement)
- Event explosion (optimization)
- False positives (tooling tuning)

---

## Related Documentation

**Approaches:**
- [Language-First Architecture](../approaches/language-first-architecture.md) - Strategic framework
- [Bounded Context Linguistic Discovery](../approaches/bounded-context-linguistic-discovery.md) - Boundary detection
- [Living Glossary Practice](../approaches/living-glossary-practice.md) - Maintenance workflow

**Reference:**
- [DDD Core Concepts Reference](ddd-core-concepts-reference.md) - Correct patterns

---

## Version History

- **1.0.0** (2026-02-10): Initial catalog from ubiquitous language experiment research

---

**Curation Status:** ✅ Claire Approved
