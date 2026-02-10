# DDD Core Concepts Reference

**Version:** 1.0.0  
**Date:** 2026-02-10  
**Purpose:** Quick reference for Domain-Driven Design terminology  
**Audience:** All agents working with domain-driven systems

---

## Overview

This document provides concise definitions of core Domain-Driven Design (DDD) concepts extracted from the ubiquitous language experiment research. It serves as a quick reference for agents and developers.

**Source Materials:**
- Eric Evans, *Domain-Driven Design* (2003)
- Vaughn Vernon, *Implementing Domain-Driven Design* (2013)
- Experiment research: `docs/architecture/experiments/ubiquitous-language/`

---

## Strategic Design Concepts

### Ubiquitous Language

**Definition:** Shared vocabulary between domain experts and developers, used consistently in all communication—conversations, documentation, code, and tests.

**Why it matters:** Eliminates translation errors between business and technical domains. If terminology differs between meetings and code, the model has failed.

**Key Practices:**
- Use domain terms in class/method names
- Write tests using business vocabulary
- Avoid technical jargon when domain terms exist
- Evolve language through continuous collaboration

**Anti-pattern:** Dictionary DDD—creating glossary document, never updating it, ignoring in code.

**Related:** Bounded Context, Living Documentation

---

### Bounded Context

**Definition:** Explicit boundary within which a domain model and its ubiquitous language have clear, consistent meaning. Outside that boundary, the same words may mean different things.

**Why it matters:** Prevents forced global unification of terminology. Different parts of the system can legitimately use the same words with different meanings, as long as boundaries are explicit.

**Key Characteristics:**
- Has explicit ownership (team, person, or role)
- Maintains its own ubiquitous language
- Requires translation at boundaries
- Aligns with team boundaries (Conway's Law)

**Examples:**
- **Sales Context:** "Order" = customer's intent to purchase
- **Fulfillment Context:** "Order" = warehouse picking instruction
- These are DIFFERENT concepts in different contexts

**Related:** Context Map, Translation, Anti-Corruption Layer

---

### Semantic Boundary

**Definition:** Division based on meaning (how terms are used), not technology or organizational structure.

**Why it matters:** Distinguishes linguistic boundaries from technical or team boundaries. A microservice boundary is not necessarily a semantic boundary.

**Detection Signals:**
- Same term, different meanings → hidden semantic boundary
- Different teams, different vocabulary → likely semantic boundary
- Translation logic exists → boundary should be explicit

**Related:** Bounded Context, Conway's Law

---

### Context Map

**Definition:** Visual diagram showing relationships between bounded contexts, including upstream/downstream flows and translation patterns.

**Why it matters:** Makes context relationships explicit. Documents which contexts depend on which, where translation happens, and what integration patterns are used.

**Relationship Types:**
- Upstream/Downstream
- Anti-Corruption Layer
- Published Language
- Shared Kernel
- Conformist
- Partnership

**Related:** Bounded Context, Context Mapping Patterns

---

## Context Mapping Patterns

### Anti-Corruption Layer (ACL)

**Definition:** Translation layer protecting downstream context from upstream changes. Isolates local model from external influence.

**When to use:** Downstream context needs linguistic independence from upstream.

**Implementation:**
- Adapter classes
- Mapper functions
- Translation services

**Example:**
```python
# Sales Order → Fulfillment Picking Instruction
class SalesOrderACL:
    def to_picking_instruction(self, sales_order):
        return PickingInstruction(
            warehouse_id=sales_order.ship_from_location,
            recipient=sales_order.customer.shipping_address,
            items=[self._map_item(item) for item in sales_order.items]
        )
```

**Related:** Upstream/Downstream, Bounded Context

---

### Upstream/Downstream

**Definition:** Data flow relationship where upstream context provides information, downstream context consumes it. Upstream changes can impact downstream.

**Power dynamics:** Upstream has power (can change without consulting downstream). Downstream must adapt (or protect with ACL).

**Example:**
- Sales (upstream) → Fulfillment (downstream)
- Sales defines OrderPlaced event schema
- Fulfillment must handle event (or use ACL to translate)

**Related:** Anti-Corruption Layer, Conformist

---

### Published Language

**Definition:** Stable API that upstream context exposes for multiple downstream consumers. Often uses industry-standard format (JSON Schema, OpenAPI, XML).

**When to use:** Upstream serves multiple downstream consumers. Want to decouple upstream from knowing all consumers.

**Example:**
- Sales publishes OrderPlaced event with JSON Schema
- Fulfillment, Accounting, Shipping all consume event
- Sales doesn't know (or care) who consumes

**Benefits:**
- Decouples producer from consumers
- Stable contract
- Industry-standard formats

**Costs:**
- Versioning complexity
- Schema maintenance
- Can't tailor to specific consumer needs

**Related:** Upstream/Downstream, Open Host Service

---

### Shared Kernel

**Definition:** Small, carefully controlled subset of model shared between contexts. Requires high coordination.

**When to use:** Two contexts need perfect synchronization on a small set of concepts (rare).

**Example:**
- Sales and Fulfillment share "Address" value object
- Any change to Address requires both teams' approval
- Tight coupling justified by coordination value

**Warning:** Sharing creates coupling. Keep minimal. Most contexts should translate, not share.

**Related:** Partnership, Bounded Context

---

### Conformist

**Definition:** Downstream context accepts upstream model without translation. Surrenders linguistic autonomy.

**When to use:**
- Upstream is authoritative (regulatory, industry standard)
- Cost of translation exceeds benefit
- Pragmatic trade-off

**Example:**
- Payment processor API (Stripe, PayPal)
- Regulatory reporting format
- Industry-standard data exchange

**Warning:** Loses local control. Use only when upstream is genuinely authoritative.

**Related:** Upstream/Downstream, Anti-Corruption Layer (alternative)

---

### Partnership

**Definition:** Two contexts have mutual dependency. Neither upstream nor downstream. Coordinated planning required.

**When to use:** Rare. Most relationships should be upstream/downstream.

**Example:**
- Sales and Marketing need synchronized customer data
- Both can change, but must coordinate
- Symmetric relationship

**Warning:** High coordination cost. Prefer asymmetric relationships (upstream/downstream) when possible.

**Related:** Shared Kernel

---

## Tactical Design Concepts

### Aggregate

**Definition:** Cluster of domain objects treated as a unit for data changes. Enforces business invariants. Has a root entity.

**Why it matters:** Defines consistency boundaries. What changes together, what can be eventually consistent.

**Key Rules:**
- External references only to root
- Changes go through root
- Root enforces invariants
- Can span transactions

**Example:**
```python
class Order:  # Aggregate Root
    def __init__(self, customer_id):
        self.order_id = generate_id()
        self.customer_id = customer_id
        self.line_items = []  # Part of aggregate
        self.status = "draft"
    
    def add_item(self, product, quantity):
        # Root enforces invariants
        if self.status == "submitted":
            raise Exception("Cannot modify submitted order")
        self.line_items.append(LineItem(product, quantity))
```

**Related:** Entity, Value Object, Ubiquitous Language

---

### Entity

**Definition:** Object with distinct identity that persists over time. Identity matters more than attributes.

**Example:** Customer (same customer even if name/address changes)

**Contrast with Value Object:** Value objects have no identity (two addresses with same street/city are identical).

**Related:** Aggregate, Value Object

---

### Value Object

**Definition:** Object defined entirely by its attributes. No identity. Immutable.

**Example:** Address, Money, Date Range

**Benefits:**
- Safer to share (immutable)
- Simpler to reason about
- Can be cached/reused

**Related:** Entity

---

### Domain Event

**Definition:** Business-significant state change expressed in ubiquitous language, named in past tense.

**Why it matters:** Makes implicit processes explicit. Domain experts should recognize event names as business occurrences.

**Naming Convention:** Past tense (OrderPlaced, PaymentReceived, ShipmentCompleted)

**Example:**
```python
class OrderPlaced:
    def __init__(self, order_id, customer_id, items, timestamp):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items
        self.timestamp = timestamp
```

**Anti-pattern:** Event Explosion—creating too many fine-grained events (OrderLineItemQuantityChangedBy1) that obscure business significance.

**Related:** Aggregate, Event Storming

---

## Design Practices

### Event Storming

**Definition:** Collaborative workshop technique using sticky notes to discover domain events, commands, actors, and process flows.

**Why it matters:** Creates shared understanding faster than traditional requirements gathering. Captures ubiquitous language through collaborative discovery.

**Process:**
1. Identify domain events (orange stickies)
2. Map event sequences (temporal flow)
3. Add commands (blue) and actors
4. Identify aggregates and bounded contexts
5. Draw context boundaries

**Output:** Visual model of business processes, vocabulary, and contexts.

**Related:** Domain Event, Bounded Context Discovery

---

### Responsibility-Driven Design (RDD)

**Definition:** Object-oriented approach where objects are defined by their responsibilities (knowing or doing something).

**Why it matters:** Forces team to speak domain language. If you can't name responsibilities using domain terms, the model is wrong.

**Tool:** CRC Cards (Class-Responsibility-Collaborator)

**Example:**
```
Class: Order
Responsibilities:
- Know order total
- Validate item availability
- Emit OrderPlaced event
Collaborators:
- LineItem, Customer, PaymentService
```

**Related:** Ubiquitous Language, Concept-Based Design

---

## Common Anti-Patterns

### Dictionary DDD

**Problem:** Team creates glossary document, considers DDD "done," never updates it. Glossary becomes stale instantly.

**Solution:** Living glossary integrated into workflow (see [Living Glossary Practice](../approaches/living-glossary-practice.md))

---

### Anemic Domain Model

**Problem:** Objects are data bags (getters/setters only), all logic in separate "Service" classes. Domain logic scattered, no linguistic clarity.

**Solution:** Move behavior into domain objects. Objects should DO things, not just hold data.

---

### Performative Compliance

**Problem:** People say "official" terms publicly while using different terms internally. Indicates forced unification has failed.

**Solution:** Recognize bounded contexts. Allow local vocabulary differences. Translate at boundaries.

---

## Usage Guide

### For Architects

Use this reference when:
- Designing context boundaries
- Choosing integration patterns
- Writing ADRs about domain structure
- Explaining DDD to teams

### For Developers

Use this reference when:
- Naming classes and methods
- Deciding where logic belongs
- Understanding context relationships
- Reviewing code for domain alignment

### For Agents

Use this reference when:
- Analyzing codebases (Architect Alphonso)
- Validating terminology (Lexical Larry, Code Reviewer Cindy)
- Writing specifications (Analyst Annie)
- Bootstrapping glossaries (Bootstrap Bill)

---

## Related Documentation

**Approaches:**
- [Language-First Architecture](../approaches/language-first-architecture.md)
- [Bounded Context Linguistic Discovery](../approaches/bounded-context-linguistic-discovery.md)
- [Living Glossary Practice](../approaches/living-glossary-practice.md)

**Tactics:**
- [Terminology Extraction and Mapping](../tactics/terminology-extraction-mapping.tactic.md)
- [Context Boundary Inference](../tactics/context-boundary-inference.tactic.md)

**External Resources:**
- Eric Evans, *Domain-Driven Design* (2003)
- Vaughn Vernon, *Implementing Domain-Driven Design* (2013)
- Martin Fowler, *Patterns of Enterprise Application Architecture* (2002)

---

## Version History

- **1.0.0** (2026-02-10): Initial version extracted from ubiquitous language experiment research

---

**Curation Status:** ✅ Claire Approved
