# Domain-Driven Naming Guidelines
**Version:** 1.0.0  
**Status:** Canonical  
**Purpose:** Universal naming principles for domain-driven design  
**Audience:** All teams, language-agnostic

---

## Core Principle

**Names should reveal domain intent, not implementation details.**

Good names answer:
- **What** is this in the domain?
- **Why** does it exist?

Bad names answer:
- **How** is it implemented?
- **What** design pattern was used?

---

## The Specificity Ladder

From generic (avoid) to specific (prefer):

```
❌ GENERIC SUFFIXES (Implementation Focus)
   Manager, Handler, Processor, Wrapper, Helper, Utility
   Problem: What does it manage/handle/process?

⚠️ TECHNICAL PATTERNS (Infrastructure OK, Domain Risky)
   Service, Repository, Factory, Builder, Strategy
   Problem: Pattern is visible, domain concept is hidden

✅ DOMAIN VERBS (Preferred)
   Renderer, Validator, Parser, Executor, Router, Calculator
   Benefit: Reveals specific responsibility

✅✅ UBIQUITOUS LANGUAGE (Best)
   OrderPricer, InvoiceGenerator, ShipmentTracker
   Benefit: Maps directly to domain expert vocabulary
```

---

## Anti-Pattern: Generic Suffixes

### Manager

**Problem:** "Manager" can mean anything. It's a code smell.

❌ **Bad examples:**
- `TemplateManager` - Does it load? render? cache? validate?
- `UserManager` - Does it authenticate? authorize? CRUD?
- `ConfigurationManager` - Does it parse? validate? merge?

✅ **Better alternatives:**
```
TemplateManager → TemplateRenderer (if rendering templates)
                → TemplateCache (if caching)
                → TemplateValidator (if validating)

UserManager → UserAuthenticator (if checking credentials)
           → UserRepository (if CRUD operations)
           → UserAuthorizer (if permission checks)

ConfigurationManager → ConfigurationLoader (if loading from files)
                     → ConfigurationMerger (if combining sources)
                     → ConfigurationValidator (if checking rules)
```

**Exception:** Framework code implementing established patterns (e.g., `ConnectionPoolManager` from library interfaces).

---

### Handler

**Problem:** "Handler" implies event-driven architecture. Confusing when used for regular method calls.

❌ **Bad examples:**
- `TaskAssignmentHandler` - Not handling events, just assigning tasks
- `RequestHandler` - Every web endpoint "handles" requests
- `DataHandler` - What kind of data? What action?

✅ **Better alternatives:**
```
TaskAssignmentHandler → TaskAssignmentService (if orchestrating)
                      → TaskAssigner (if primary responsibility)

RequestHandler → OrderProcessor (if processing orders)
              → InvoiceGenerator (if generating invoices)

DataHandler → DataTransformer (if transforming)
           → DataValidator (if validating)
```

**Exception:** Legitimate event handlers (e.g., `FileSystemEventHandler`, `SignalHandler`).

---

### Processor

**Problem:** Too generic. Every component "processes" something.

❌ **Bad examples:**
- `DataProcessor` - What data? What processing?
- `TaskProcessor` - Does it create? execute? validate?
- `MessageProcessor` - Does it parse? route? transform?

✅ **Better alternatives:**
```
DataProcessor → DataNormalizer (if normalizing)
             → DataEnricher (if adding fields)
             → DataAggregator (if combining)

TaskProcessor → TaskExecutor (if running tasks)
             → TaskValidator (if checking validity)

MessageProcessor → MessageRouter (if routing)
                → MessageTransformer (if transforming)
```

---

### Helper / Utility

**Problem:** Kitchen sink. Becomes dumping ground for unrelated functions.

❌ **Bad examples:**
- `StringHelper` - What string operations?
- `DateUtils` - Parse? format? calculate?
- `FileHelper` - Read? write? validate?

✅ **Better alternatives:**
```
StringHelper → StringValidator (if validating)
            → StringFormatter (if formatting)
            → StringNormalizer (if normalizing)

DateUtils → DateParser (if parsing)
         → DateFormatter (if formatting)
         → DateCalculator (if calculating ranges/durations)

FileHelper → FileReader / FileWriter (if I/O)
          → FilenameValidator (if validating paths)
```

**Better yet:** Move to domain-specific modules, not shared utilities.

---

## Pattern: Use Domain Verbs

**Prefer verbs that reveal specific actions:**

| Generic | Specific Verb | Domain Context |
|---------|--------------|----------------|
| Manager | Renderer | Templates, views, UI |
| Manager | Calculator | Prices, totals, scores |
| Manager | Tracker | Status, history, audit |
| Handler | Validator | Input, schemas, rules |
| Handler | Transformer | Data formats, shapes |
| Handler | Router | Requests, messages, events |
| Processor | Parser | Text, files, protocols |
| Processor | Enricher | Data, entities, contexts |
| Processor | Aggregator | Collections, reports, stats |

---

## Pattern: Use Ubiquitous Language

**Best practice:** Use terms that domain experts use.

✅ **Examples from different domains:**

**E-commerce:**
- `OrderPricer` (not `PriceCalculator`)
- `InventoryReserver` (not `InventoryManager`)
- `ShipmentTracker` (not `TrackingService`)

**Healthcare:**
- `PatientRegistrar` (not `PatientManager`)
- `AppointmentScheduler` (not `AppointmentService`)
- `PrescriptionValidator` (not `PrescriptionChecker`)

**Finance:**
- `TransactionReconciler` (not `TransactionProcessor`)
- `RiskAssessor` (not `RiskCalculator`)
- `PortfolioRebalancer` (not `PortfolioManager`)

**Benefit:** Domain experts can read code and understand it. New developers learn domain vocabulary through code.

---

## When Generic Names Are Acceptable

### 1. Framework/Infrastructure Code

When implementing library interfaces or framework patterns:
```
✅ FileSystemEventHandler(EventHandler)  # Library interface
✅ BaseOrchestrator(ABC)                 # Framework pattern
✅ DatabaseConnectionManager              # Infrastructure concern
```

### 2. Well-Established Technical Patterns

When pattern name IS the ubiquitous language:
```
✅ UserRepository    # Repository pattern is well-known
✅ OrderFactory      # Factory pattern is intentional
✅ CommandBus        # Bus is the domain concept
```

### 3. Adapter/Bridge Patterns

When explicitly implementing design pattern for integration:
```
✅ LegacySystemAdapter    # Adapter pattern
✅ ThirdPartyClientWrapper # Wrapper pattern
```

**Rule:** If using generic name in domain code, **require justification** in PR description or ADR.

---

## Naming Checklist

Before accepting a name, ask:

- [ ] **Does it reveal domain intent?** (not just technical role)
- [ ] **Would a domain expert recognize this term?** (ubiquitous language)
- [ ] **Is it specific enough?** (not generic Manager/Handler/Processor)
- [ ] **Does it describe the "what" and "why"?** (not the "how")
- [ ] **If generic, is there clear justification?** (framework, pattern, infrastructure)

---

## Enforcement Strategy

**Level 1 (Advisory):** Suggest better alternatives, author decides  
**Level 2 (Acknowledgment):** Author must respond with rationale  
**Level 3 (Blocker):** Escalate to architect for bounded context review

**When to enforce:**
- New domain code (higher standards)
- Public APIs (impacts many developers)
- Core domain (highest clarity needed)

**When to be lenient:**
- Legacy code (refactor opportunistically)
- Framework code (established conventions)
- Infrastructure (technical focus appropriate)

---

## Related Practices

**Living Glossary:**
- Maintain glossary of domain terms: `.contextive/contexts/*.yml`
- Review glossary quarterly
- Reference terms in docstrings

**Bounded Contexts:**
- Same term may have different meanings in different contexts
- Use context-specific glossaries
- Document translation layers (Anti-Corruption Layer)

**Language-First Architecture:**
- Start with domain language, not code patterns
- Involve domain experts in naming
- Treat terminology conflicts as architecture signals

---

## Resources

**Books:**
- Domain-Driven Design (Eric Evans) - Ubiquitous Language
- Implementing Domain-Driven Design (Vaughn Vernon) - Bounded Contexts
- Clean Code (Robert Martin) - Meaningful Names

**Approaches:**
- `doctrine/approaches/language-first-architecture.md`
- `doctrine/approaches/living-glossary-practice.md`

**Repository Guidelines:**
- `.doctrine-config/styleguides/python-naming-conventions.md` (Python-specific)
- `.doctrine-config/styleguides/java-naming-conventions.md` (Java-specific)
- `.doctrine-config/tactics/terminology-validation-checklist.tactic.md`

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-10  
**Next Review:** 2026-05-10 (quarterly)  
**Maintainer:** Architect Alphonso, Curator Claire

---

*"The vocabulary of the domain model is the backbone of a common language." - Eric Evans*
