# Primer: Object-Oriented and Event-Based Modeling in DDD

**Reading Time:** ~10 minutes  
**Version:** 1.0.0  
**Date:** 2026-02-09  
**Concept:** OO Design, Event-Based Modeling, and DDD Integration

---

## What It Is

**Object-Oriented modeling** in DDD focuses on **responsibility assignment**—which objects do what, and how they collaborate. **Event-based modeling** captures **state changes** and **business processes** through domain events. Together, they form complementary approaches to discovering and implementing ubiquitous language.

**Not:** Generic OO patterns (factories, singletons) divorced from domain  
**Not:** Event-driven architecture (message queues, microservices) as infrastructure  
**Is:** **Domain-centric design** where objects and events express business concepts using ubiquitous language

---

## Why These Approaches Matter in DDD

### The Relationship to Ubiquitous Language

DDD emphasizes **strategic design** (bounded contexts, context mapping) over **tactical patterns** (entities, aggregates). However, tactical patterns become powerful when they **embody ubiquitous language**:

| Approach | Language Contribution | Example |
|----------|----------------------|---------|
| **Responsibility-Driven Design** | Object names reveal roles and collaborations | `OrderFulfillment.allocate_inventory()` vs `OrderProcessor.process()` |
| **Concept-Based Design** | Concepts have clear purpose and operational principle | `Reservation` (purpose: hold resources temporarily, principle: expires if not confirmed) |
| **Event-Based Modeling** | Events capture business-significant state changes | `OrderPlaced`, `PaymentReceived`, `ShipmentScheduled` |

**Key Insight:** Objects and events are not technical constructs—they are **linguistic anchors** that make domain concepts explicit.

---

## Responsibility-Driven Design (RDD)

### Core Principle: Objects Have Responsibilities

**Responsibility** = knowing or doing something on behalf of the system.

**Two types:**
1. **Knowing:** Object maintains state (e.g., `Order` knows its items and total)
2. **Doing:** Object performs computation or coordinates action (e.g., `PaymentProcessor` validates payment)

---

### CRC Cards: Responsibility Discovery Technique

**CRC = Class-Responsibility-Collaborator**

A physical or digital card with three sections:

```
┌─────────────────────────────────────┐
│ Class: OrderFulfillment             │
├─────────────────────────────────────┤
│ Responsibilities:                   │
│ - Verify order is valid             │
│ - Allocate inventory                │
│ - Schedule shipment                 │
├─────────────────────────────────────┤
│ Collaborators:                      │
│ - Order                             │
│ - InventoryService                  │
│ - ShipmentScheduler                 │
└─────────────────────────────────────┘
```

**Process:**
1. Domain expert describes a business scenario
2. Team identifies actors (objects) involved
3. For each actor, list responsibilities
4. Identify collaborators (which objects work together)
5. If responsibilities feel misplaced, reassign until it "feels right"

**Value:** Forces team to speak domain language. If you can't name an object or its responsibilities using domain terms, the model is wrong.

---

### How Names Reveal Responsibilities

**Before (generic technical names):**
```python
class DataManager:
    def save(self, data):
        # What responsibility? Unclear.
        pass
```

**After (responsibility-driven names):**
```python
class OrderRepository:
    def store_pending_order(self, order):
        # Responsibility: persist orders awaiting fulfillment
        pass
```

**Test:** Can a domain expert read the class name and method name and understand what it does without seeing code?

---

## Concept-Based Design (Daniel Jackson)

### Core Principle: Concepts are Design Atoms

A **concept** is a self-contained piece of functionality with:
1. **Purpose:** Why it exists (the problem it solves)
2. **Operational Principle:** How it works (core behavior)
3. **State:** What it tracks

---

### Example: "Reservation" Concept

**Purpose:** Hold resources temporarily to prevent double-booking  
**Operational Principle:**  
- When reservation created, resource marked unavailable
- If confirmed before expiration, resource allocated permanently
- If not confirmed, reservation expires and resource becomes available again

**State:**
- `reservation_id`
- `resource` (what's reserved)
- `expires_at` (time limit)
- `status` (pending/confirmed/expired)

---

### Concepts and Ubiquitous Language

Concepts should map directly to domain vocabulary:

| Domain Term | Concept | Purpose |
|-------------|---------|---------|
| **Cart** | Shopping Cart | Allow customer to collect items before purchase |
| **Wishlist** | Item Collection | Allow customer to save items for later |
| **Subscription** | Recurring Service | Grant access as long as payment continues |
| **Coupon** | Discount Mechanism | Reduce price based on conditions |

**Anti-pattern:** Creating concepts that domain experts don't recognize:
- "DataAccessLayer" (technical, not domain)
- "ServiceManager" (vague, no clear purpose)
- "Helper" (admits unclear responsibility)

---

### Concept Specificity Balance

**Too General:**
```python
class Item:  
    # Could be anything: product, document, task, etc.
    pass
```

**Too Specific:**
```python
class BlueWidgetForCaliforniaCustomersWithPremiumSubscription:
    # Brittle: changes frequently, hard to evolve
    pass
```

**Right Level:**
```python
class Product:
    # Clear domain concept
    # Specific enough to have coherent responsibility
    # General enough to accommodate variations
    pass
```

---

## Event-Based Modeling: Domain Events

### What Are Domain Events?

**Domain Event** = Something **business-significant** that happened in the past.

**Not:** Technical events (button clicked, API called)  
**Is:** Business state changes expressed in domain language

---

### Naming Convention: Past Tense

Events are facts—they already happened:

| Good Event Names | Bad Event Names |
|-----------------|-----------------|
| `OrderPlaced` | `PlaceOrder` (command, not event) |
| `PaymentReceived` | `Payment` (ambiguous) |
| `InventoryAllocated` | `AllocateInventory` (command) |
| `CustomerRegistered` | `CustomerRegistration` (noun, not action) |

**Pattern:** `<Subject><PastTenseVerb>` (e.g., `ShipmentScheduled`, `RefundIssued`)

---

### Event Storming: Collaborative Discovery

**Event Storming** is a workshop technique for discovering domain events and process flows.

**Materials:**
- Sticky notes (orange = domain events)
- Large wall space
- Domain experts + developers

**Process:**
1. **Chaotic Exploration:** Everyone writes domain events on orange stickies ("Order Placed", "Payment Failed", etc.)
2. **Timeline:** Arrange events left-to-right in chronological order
3. **Hot Spots:** Mark conflicts, questions, or unclear areas
4. **Commands:** Add blue stickies for actions that trigger events ("Place Order" → "Order Placed")
5. **Actors:** Add yellow stickies for who/what triggers commands (Customer, System, External Service)
6. **Aggregates:** Group events around key domain objects (Order aggregate emits OrderPlaced, OrderCanceled, etc.)

**Outcome:** Shared understanding of domain process expressed in ubiquitous language.

---

### Events and Bounded Contexts

Events often **cross context boundaries**:

```
Sales Context               Fulfillment Context
    │                             │
    │ OrderPlaced event           │
    ├────────────────────────────>│
    │                             │
    │                       InventoryAllocated event
    │                             │
    │<────────────────────────────┤
    │                             │
```

**Translation at boundary:**
- Sales context emits `OrderPlaced` (includes sales-specific data: discount, sales rep)
- Fulfillment context receives `OrderReadyForFulfillment` (translated: only fulfillment-relevant data)

**Why translate?** Prevents tight coupling. Sales context changes (new discount types) don't break Fulfillment.

---

## How OO and Events Work Together

### Example: Order Fulfillment Flow

**Objects (Responsibility-Driven):**
- `Order` (knows: items, total, status)
- `OrderFulfillment` (does: orchestrate fulfillment process)
- `InventoryService` (does: allocate/deallocate inventory)
- `ShipmentScheduler` (does: schedule shipment)

**Events (State Changes):**
- `OrderPlaced` → triggers `OrderFulfillment.fulfill_order()`
- `InventoryAllocated` → internal event, advance state
- `ShipmentScheduled` → complete fulfillment, notify customer

**Code (simplified):**
```python
class OrderFulfillment:
    def handle_order_placed(self, event: OrderPlaced):
        order = self.order_repository.find(event.order_id)
        
        if not self.is_valid(order):
            self.emit(OrderRejected(order.id, reason="Invalid order"))
            return
            
        self.inventory_service.allocate(order.items)
        self.emit(InventoryAllocated(order.id))
        
        self.shipment_scheduler.schedule(order)
        self.emit(ShipmentScheduled(order.id))
```

**Notice:**
- Method names use domain language (`handle_order_placed`, not `process_event`)
- Events are business concepts (`InventoryAllocated`, not `DataUpdated`)
- Responsibilities clear (OrderFulfillment orchestrates, doesn't do everything)

---

## What These Approaches Do NOT Solve

### 1. Technical Architecture Decisions

Responsibility-driven design tells you **which objects collaborate**, not **where they run** (same process, different service, different data center).

**Example:** `OrderFulfillment` and `InventoryService` may be:
- Same class
- Different classes, same process
- Different microservices

RDD informs but doesn't dictate deployment architecture.

---

### 2. Event Infrastructure Complexity

Domain events are conceptual. **Event-driven architecture** (Kafka, RabbitMQ, event sourcing) is infrastructure.

**Risk:** Conflating the two leads to premature technical decisions.

**Start simple:** Domain events as in-memory notifications. Add infrastructure only when distribution is required.

---

### 3. Over-Engineering Early Models

Early models are always incomplete. Discovering "the perfect object model" upfront is impossible.

**Mitigation:** Use Event Storming for discovery, CRC cards for initial design, then **evolve through refactoring**.

---

## Known Failure Modes

### Failure Mode 1: "Perfect Object Model" Paralysis

**Symptom:** Team spends weeks designing object hierarchies before writing code.

**Why it fails:** Understanding emerges through implementation. Premature abstraction creates rigidity.

**Mitigation:** Start with **obvious objects** (Order, Customer, Product). Refine as understanding deepens.

---

### Failure Mode 2: Anemic Domain Models

**Symptom:** Objects are data bags (getters/setters only). All logic in "Service" classes.

```python
class Order:
    # Just data, no behavior
    def get_total(self): return self.total
    def set_total(self, total): self.total = total

class OrderService:
    # All logic here
    def calculate_order_total(self, order): ...
    def validate_order(self, order): ...
```

**Why it fails:** Domain logic scattered across services. Hard to find, hard to test, no linguistic clarity.

**Mitigation:** Push behavior into objects. `Order.calculate_total()` and `Order.validate()` encode business rules where they belong.

---

### Failure Mode 3: Event Explosion

**Symptom:** Hundreds of fine-grained events (`OrderLineItemQuantityChangedBy1`).

**Why it fails:** Noise overwhelms signal. Developers drown in events.

**Mitigation:** Events should represent **business-significant** state changes, not every mutation. Ask: "Would a domain expert care about this?"

---

### Failure Mode 4: Technical Events Leak into Domain

**Symptom:** Events named after infrastructure (`DatabaseUpdated`, `MessageReceived`).

**Why it fails:** Domain experts don't recognize these. Language fragmentation reappears.

**Mitigation:** Events must use ubiquitous language. If you can't explain an event to a domain expert, rethink it.

---

### Failure Mode 5: CRC Cards as Documentation Theater

**Symptom:** Team creates beautiful CRC cards, files them away, never updates.

**Why it fails:** Same as "Dictionary DDD"—artifacts divorced from practice.

**Mitigation:** CRC cards are **discovery tools**, not documentation artifacts. Use them in design sessions, then throw them away. Living design lives in code.

---

## Applicability in This Context (Agentic Monitoring)

### How Agents Use OO and Event Models

**Observing Objects:**
- Agent scans class names: Are they domain terms or technical jargon?
- Agent checks method names: Do they reflect responsibilities or generic actions?
- Agent measures: Anemic models (high ratio of getters/setters to behavior)?

**Observing Events:**
- Agent scans event names: Past tense? Business-significant? Ubiquitous language?
- Agent tracks event flows: Do events cross context boundaries without translation?
- Agent detects: Event explosion (too many fine-grained events)?

---

### Feedback Examples

**Object Naming Feedback:**
```
⚠️ Class "DataManager" detected in OrderContext.
Suggested: Rename to domain-specific responsibility (e.g., "OrderRepository", "OrderValidator").
Rationale: Domain experts don't recognize "DataManager" as business concept.
```

**Event Naming Feedback:**
```
⚠️ Event "ProcessOrder" detected (command, not event).
Suggested: Rename to "OrderPlaced" (past tense, business outcome).
Rationale: Events represent facts that already happened, not actions to take.
```

**Responsibility Clarity Feedback:**
```
✅ Class "OrderFulfillment" has clear responsibilities:
  - verify_order_is_valid()
  - allocate_inventory()
  - schedule_shipment()
No action needed.
```

---

## Glossary Seed Terms

From this primer, the following terms should enter the glossary:

| Term | Definition | Context |
|------|------------|---------|
| **Responsibility-Driven Design (RDD)** | OO approach where objects are defined by their responsibilities (knowing/doing) | Design Practice |
| **CRC Card** | Class-Responsibility-Collaborator card used to discover object responsibilities | Design Tool |
| **Concept** | Self-contained piece of functionality with purpose, operational principle, and state | Design Atom |
| **Purpose** | Why a concept exists (the problem it solves) | Concept Anatomy |
| **Operational Principle** | How a concept works (core behavior) | Concept Anatomy |
| **Domain Event** | Business-significant state change expressed in ubiquitous language, named in past tense | Event Modeling |
| **Event Storming** | Collaborative workshop technique for discovering domain events and process flows | Design Practice |
| **Anemic Domain Model** | Anti-pattern where objects are data bags, all logic in separate service classes | Failure Mode |
| **Event Explosion** | Anti-pattern of creating too many fine-grained events that obscure business significance | Failure Mode |
| **Aggregate** | Cluster of domain objects treated as a unit for data changes, emits domain events | DDD Tactical Pattern |

---

## Key Claims (Source-Grounded)

### Rebecca Wirfs-Brock, *Object Design* (2002)

**Claim 1:** "Good names reveal intention and responsibilities."  
- **Implication:** If you can't name an object's responsibility clearly, the design is unclear.

**Claim 2:** "Collaborations clarify design."  
- **Implication:** Understanding **how** objects work together is as important as **what** they do individually.

**Claim 3:** "Refactoring names is refactoring design."  
- **Implication:** Changing terminology isn't cosmetic—it's architectural work.

---

### Daniel Jackson, *The Essence of Software* (2021)

**Claim 4:** "Concepts are the atoms of software design."  
- **Implication:** If your concepts are fuzzy, your software will be fuzzy.

**Claim 5:** "Every concept must have a clear purpose."  
- **Implication:** Objects without clear purpose accumulate cruft and become maintenance burdens.

**Claim 6:** "Operational principle explains how a concept works."  
- **Implication:** If you can't articulate how a concept behaves, users (and developers) won't understand it.

---

### Eric Evans, *Domain-Driven Design* (2003)

**Claim 7:** "Domain events make implicit processes explicit."  
- **Implication:** Events surface business logic that would otherwise stay hidden in code.

**Claim 8:** "Aggregates enforce invariants."  
- **Implication:** Consistency boundaries (what changes together) should align with business rules.

---

### Alberto Brandolini, Event Storming (2013)

**Claim 9:** "Event Storming creates shared understanding faster than traditional requirements gathering."  
- **Implication:** Collaborative discovery beats documentation handoffs.

**Claim 10:** "Orange stickies (domain events) are the most important artifact."  
- **Implication:** Focus on **what happens** (events) before **how it's implemented** (objects/services).

---

## How to Act Differently

### Before This Primer
- Objects named generically (`Manager`, `Handler`, `Processor`)
- Responsibilities vague or scattered across services
- Events named after technical actions (`DataUpdated`, `MessageSent`)
- Design discussions dominated by technical patterns

### After This Primer
- Objects named after domain roles with clear responsibilities
- CRC cards used to discover and refine responsibilities
- Events capture business-significant state changes in domain language
- Event Storming used for collaborative domain discovery

### Concrete Actions
1. **In design sessions:** Use CRC cards to discover responsibilities. If you can't fill in the card using domain language, the model needs work.
2. **In code review:** Flag generic names (`Manager`, `Service`, `Data`). Propose domain-specific alternatives.
3. **In Event Storming:** Start with domain events (orange stickies). Let the timeline reveal process flow before discussing implementation.
4. **In refactoring:** When renaming classes/methods, check if domain experts recognize the new names. If not, iterate.
5. **In testing:** Write tests that read like domain scenarios. Event names and object responsibilities should make tests self-documenting.

---

## Connection to Other Concepts

This primer builds on and connects to:

- **Primer 01: Ubiquitous Language** - Objects and events embody ubiquitous language
- **Primer 02: Bounded Contexts** - Events often cross boundaries; objects are scoped to contexts
- **Primer 03: Conway's Law** - Team ownership of aggregates/events reflects communication patterns

---

## Quality Gate Check

✅ **Can a tired engineer read this in ~10 minutes?** Yes (~2,200 words)  
✅ **Does it answer "how do I act differently?"** Yes (concrete actions section)  
✅ **Are failure modes explicit?** Yes (5 documented)  
✅ **Are limitations clear?** Yes (what it doesn't solve)  
✅ **Are glossary terms extractable?** Yes (10 seed terms)

---

## References

- Rebecca Wirfs-Brock, *Object Design: Roles, Responsibilities, and Collaborations* (2002)
- Daniel Jackson, *The Essence of Software* (2021)
- Eric Evans, *Domain-Driven Design* (2003), Chapters 5-6 (Entities, Value Objects, Domain Events)
- Vaughn Vernon, *Implementing Domain-Driven Design* (2013), Chapter 8 (Domain Events)
- Alberto Brandolini, *Event Storming* (2013)
- DDD-Crew, Event Storming resources (https://github.com/ddd-crew/eventstorming-glossary-cheat-sheet)
- [Experiment Primer](../experiment-primer.md)
- [Reading List](../reading-list.md)

---

**Previous:** [Primer 03: Conway's Law](./03-conways-law-semantic-boundaries.md)  
**Next:** [Claim Inventory](../claim-inventory.md)
