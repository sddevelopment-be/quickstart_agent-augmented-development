# Directive 038: Ensure Conceptual Alignment

**Version:** 1.0.0  
**Date:** 2026-02-10  
**Status:** Active  
**Source:** Feedback on ubiquitous language integration (comment 2786125072)

---

## Purpose

Ensure agents understand terminology used by humans before proceeding with task execution. Prevent misunderstandings by explicitly confirming conceptual alignment.

---

## Core Principle

**Never assume understanding.** When a human uses domain terminology, agents must explicitly confirm their interpretation before proceeding. Shared vocabulary doesn't guarantee shared meaning.

---

## Requirements

### For All Agents

When receiving a task assignment containing domain terminology:

1. **Identify Domain Terms**
   - Which terms are domain-specific (not general programming concepts)?
   - Which terms might have multiple meanings?
   - Which terms are unfamiliar or ambiguous?

2. **State Understanding**
   - Explicitly say what you understand each term to mean
   - Reference glossary definitions if available
   - Acknowledge bounded context scope

3. **Confirm Before Proceeding**
   - Wait for confirmation of correct understanding
   - Ask clarifying questions if uncertain
   - Don't proceed with assumptions

---

## Standard Confirmation Pattern

When receiving task: "Create an ACL layer for the Order domain"

**Agent Response (REQUIRED):**

```
✅ Conceptual Alignment Check:

Understanding of key terms:

**ACL (Anti-Corruption Layer):**
Translation layer that protects downstream context from upstream changes. 
In this case, will translate between upstream Order model and our local domain model.

**Order domain:**
Interpreting as [Sales Context Order] - customer's intent to purchase.
NOT [Fulfillment Context Order] - warehouse picking instruction.

**Bounded Context:**
This ACL will sit at the boundary between Sales and [Target Context].
Will maintain linguistic independence per DDD patterns.

Is this interpretation correct? Should I proceed?
```

---

## Application by Role

### All Agents (Mandatory Before Task Execution)

**When task contains these term types:**

1. **Domain-Driven Design terms:**
   - Bounded Context, Aggregate, Entity, Value Object
   - Anti-Corruption Layer, Published Language, Shared Kernel
   - Ubiquitous Language, Context Map

2. **Business domain terms:**
   - Customer, Order, Product, Account
   - (ANY term specific to business domain)

3. **Architecture patterns:**
   - Microservice, Event Sourcing, CQRS
   - (Patterns with multiple valid interpretations)

4. **Ambiguous pronouns:**
   - "the system", "the service", "the database"
   - "that component", "those classes"

**Required Action:** State understanding explicitly, wait for confirmation.

---

## Confirmation Template

```markdown
✅ Conceptual Alignment Check:

**Task Understood As:** [Restate task in own words]

**Key Terms Interpreted:**

**[Term 1]:**
- **My Understanding:** [Definition]
- **Source:** [Glossary/ADR/Conversation]
- **Context:** [Which bounded context]

**[Term 2]:**
- **My Understanding:** [Definition]
- **Assumptions:** [Any assumptions made]

**[Term 3]:**
- **Ambiguity:** [Multiple possible meanings]
- **Question:** [Clarification needed]

**Planned Approach:** [High-level approach based on understanding]

**Confirmation Required:** Is this interpretation correct? Should I proceed?
```

---

## Examples

### Example 1: Good Alignment

**User:** "Add an Order entity to the Sales context"

**Agent:**
```
✅ Conceptual Alignment Check:

**Task:** Create new Order entity in Sales bounded context

**Order entity:**
- Sales context's view of customer purchase intent
- Contains: customer reference, line items, totals, status
- NOT the Fulfillment context's Order (which is a picking instruction)

**Entity (DDD):**
- Has distinct identity (OrderID)
- Persists over time
- Part of an Aggregate (likely Order Aggregate)

**Sales context:**
- Bounded context owning customer-facing purchase flow
- Uses ubiquitous language: Customer, Quote, Order, Contract

Proceeding to create Order entity with:
- Unique ID
- Audit fields (created, modified)
- Business methods (not anemic)
- Ubiquitous language names

Confirm this interpretation?
```

---

### Example 2: Requesting Clarification

**User:** "The service needs to call the other service"

**Agent:**
```
⚠️ Conceptual Alignment - Clarification Needed:

Ambiguous terms detected:

**"The service":**
- Which service specifically? (Name/context?)
- Sales Service? Fulfillment Service? Payment Service?

**"The other service":**
- Which downstream service should be called?
- What context boundary are we crossing?
- Is an ACL needed?

**Additional context needed:**
1. Service names and bounded contexts
2. Integration pattern (sync/async, API/events)
3. Translation requirements at boundary

Cannot proceed without clarification. Please specify service names and contexts.
```

---

### Example 3: Multiple Interpretations

**User:** "Update the Customer model"

**Agent:**
```
⚠️ Conceptual Alignment - Multiple Interpretations Possible:

"Customer" could mean:

**Option A: Sales Context Customer**
- Person who purchases products
- Contains: contact info, purchase history, credit limit

**Option B: Support Context Customer**
- Person with support tickets
- Contains: ticket history, SLA level, contact preferences

**Option C: Shared Kernel Customer**
- Minimal shared concept
- Contains: only ID and name (shared across contexts)

**"Update" could mean:**
- Add new fields to existing model
- Change behavior/methods
- Refactor structure
- Migrate data

Which interpretation is correct? 
Please specify: context + nature of update.
```

---

## When to Apply

**ALWAYS apply when:**
- Task contains domain-specific terminology
- Working in Domain-Driven Design context
- Cross-context integration work
- Ambiguous or overloaded terms present
- First time working with this domain/context

**Especially critical when:**
- Terms have multiple meanings in codebase (Order, Account, User)
- Bounded contexts not well documented
- New to project/domain
- High-stakes changes (production systems, critical paths)

---

## Violation Consequences

**What happens without conceptual alignment:**

1. **Wrong Implementation:**
   - Agent builds Order entity in wrong context
   - Creates coupling where boundary should exist
   - Uses wrong ubiquitous language

2. **Lost Time:**
   - Work must be redone
   - Pull request rejected
   - Technical debt introduced

3. **Confusion Compounds:**
   - Wrong terminology propagates
   - Future agents inherit mistakes
   - Glossary becomes inaccurate

4. **Trust Erosion:**
   - Human loses confidence in agent
   - More micromanagement required
   - Autonomy reduced

---

## Success Criteria

**Conceptual alignment is working when:**
- ✅ Agents state understanding before proceeding
- ✅ Humans confirm or correct interpretations
- ✅ Misunderstandings caught early (before implementation)
- ✅ Task execution uses correct terminology
- ✅ Pull requests reference correct bounded contexts
- ✅ Code reviews mention fewer terminology issues

---

## Integration with Other Directives

**[Directive 037: Context-Aware Design](037_context_aware_design.md):**
- Context-Aware Design: Know which context you're in
- Conceptual Alignment: Confirm your understanding of context terms

**[Directive 007: Agent Declaration](007_agent_declaration.md):**
- Agents must acknowledge understanding of operating environment
- Conceptual Alignment extends this to task-specific terminology

**[Directive 018: Traceable Decisions](018_traceable_decisions.md):**
- Document conceptual alignment in ADRs
- "We interpreted 'Order' as Sales Context Order because..."

---

## Related Documentation

**Approaches:**
- [Living Glossary Practice](../approaches/living-glossary-practice.md) - Reference for term definitions
- [Language-First Architecture](../approaches/language-first-architecture.md) - Why terminology matters

**References:**
- [DDD Core Concepts Reference](../docs/ddd-core-concepts-reference.md) - Standard DDD terms
- Contextive Glossaries - `.contextive/contexts/` for project-specific terms

---

## Version History

- **1.0.0** (2026-02-10): Initial directive created per feedback (comment 2786125072)

---

**Curation Status:** ✅ Created per feedback, mandatory for all agents before task execution
