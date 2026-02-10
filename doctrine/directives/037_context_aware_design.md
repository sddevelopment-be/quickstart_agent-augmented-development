# Directive 037: Context-Aware Design

**Version:** 1.0.0  
**Date:** 2026-02-10  
**Status:** Active  
**Source:** Feedback on ubiquitous language integration (comment 2786008080)

---

## Purpose

Ensure agents and developers consider bounded context boundaries when making design decisions, preventing accidental coupling and maintaining linguistic consistency within contexts.

---

## Core Principle

**Design decisions must respect context boundaries.** Code, terminology, and abstractions should align with the bounded context they inhabit. Crossing context boundaries requires explicit translation.

---

## Requirements

### For All Agents

When making design decisions (architecture, code structure, naming, interfaces):

1. **Identify Current Context**
   - Which bounded context does this code/design inhabit?
   - What is the ubiquitous language for this context?
   - Who owns this context's vocabulary?

2. **Check Context Boundaries**
   - Does this design cross context boundaries?
   - Are translations needed at boundaries?
   - Is an Anti-Corruption Layer required?

3. **Validate Linguistic Consistency**
   - Do names use the context's ubiquitous language?
   - Are domain terms consistent with glossary?
   - Are generic names avoided (Manager, Handler, Data)?

4. **Document Context Decisions**
   - Record context membership in code/docs
   - Document boundary crossings in ADRs
   - Explain translation logic at boundaries

---

## Application by Role

### Architect Alphonso

**Primary Responsibility:** Define and maintain context boundaries

**Activities:**
- Map bounded contexts to system architecture
- Design integration patterns (ACL, Published Language, Shared Kernel)
- Create context maps showing relationships
- Document context ownership and vocabulary

**References:**
- [Bounded Context Linguistic Discovery](../approaches/bounded-context-linguistic-discovery.md)
- [Context Boundary Inference](../tactics/context-boundary-inference.tactic.md)

---

### Code Reviewer Cindy

**Primary Responsibility:** Enforce context boundaries in code

**Review Checklist:**
- ✅ Code uses context's ubiquitous language
- ✅ Cross-context dependencies have translation layers
- ✅ No direct coupling between contexts (no shared mutable state)
- ✅ Domain terms match glossary for this context
- ✅ Generic names flagged (Manager, Handler, Info)

**References:**
- [Linguistic Anti-Patterns](../docs/linguistic-anti-patterns.md)
- DDD Core Concepts - Context Mapping Patterns

---

### Analyst Annie

**Primary Responsibility:** Scope specifications to single context

**Specification Guidelines:**
- Each spec belongs to one bounded context
- Use context's ubiquitous language consistently
- Cross-reference context glossary
- Document cross-context integrations explicitly

**References:**
- [Living Glossary Practice](../approaches/living-glossary-practice.md)
- [Terminology Extraction and Mapping](../tactics/terminology-extraction-mapping.tactic.md)

---

### Backend Benny / Python Pedro

**Primary Responsibility:** Implement context boundaries in code

**Implementation Patterns:**
- Separate modules/packages per context
- Translation layers (Adapters/Mappers) at boundaries
- Context-specific domain models (no shared entities)
- Integration via events or APIs (Published Language)

**Anti-Patterns to Avoid:**
- Shared database tables across contexts
- Direct object references across contexts
- Generic "Utils" shared everywhere
- Anemic domain models (all logic in services)

**References:**
- [DDD Core Concepts Reference](../docs/ddd-core-concepts-reference.md)

---

## When to Apply

**ALWAYS apply when:**
- Creating new modules, packages, or services
- Designing interfaces between components
- Naming classes, methods, or database tables
- Reviewing pull requests
- Writing specifications or ADRs

**Critical moments:**
- System decomposition decisions
- Microservice boundary definition
- Team ownership assignment
- API contract design
- Database schema design

---

## Context Mapping Patterns Reference

### Safe Patterns (Maintain Independence)

**Anti-Corruption Layer (ACL):**
- Downstream translates upstream model
- Protects local vocabulary
- Use when: Downstream must maintain independence

**Published Language:**
- Upstream publishes stable API
- Multiple downstreams consume
- Use when: Many consumers, want stability

**Separate Ways:**
- No integration between contexts
- Use when: No business need to integrate

---

### Coupling Patterns (Use Carefully)

**Shared Kernel:**
- Small shared model between contexts
- Requires high coordination
- Use when: Truly shared concepts, close teams

**Conformist:**
- Downstream accepts upstream model
- Loses local vocabulary control
- Use when: Upstream is authoritative (e.g., regulatory)

**Customer/Supplier:**
- Downstream depends on upstream
- Upstream considers downstream needs
- Use when: Strong partnership exists

---

## Violation Signals

**Red flags indicating context boundaries ignored:**

1. **Same term, different meanings** in different parts of code
2. **Translation logic scattered** across multiple files
3. **Shared mutable state** between modules
4. **Generic names dominate** (Manager, Handler, Service, Utils)
5. **Team conflicts** over naming or design
6. **High coupling** between supposedly separate modules
7. **Integration bugs** at module boundaries

**Action:** Stop, identify implicit boundary, make explicit, add translation layer.

---

## Success Metrics

**Context-aware design is working when:**
- ✅ Each context has clear vocabulary (documented in glossary)
- ✅ Translation logic is explicit (ACL, Mappers at boundaries)
- ✅ Teams understand their context scope
- ✅ Integration bugs rare at boundaries
- ✅ Code uses domain language (not generic terms)
- ✅ Context map up-to-date and referenced

---

## Related Directives

- **[Directive 018: Traceable Decisions](018_traceable_decisions.md)** - Document context choices in ADRs
- **[Directive 034: Spec-Driven Development](034_spec_driven_development.md)** - Scope specs to contexts
- **[Directive 036: Boy Scout Rule](036_boy_scout_rule.md)** - Improve context clarity incrementally

---

## Related Documentation

**Approaches:**
- [Language-First Architecture](../approaches/language-first-architecture.md)
- [Bounded Context Linguistic Discovery](../approaches/bounded-context-linguistic-discovery.md)
- [Living Glossary Practice](../approaches/living-glossary-practice.md)

**Tactics:**
- [Context Boundary Inference](../tactics/context-boundary-inference.tactic.md)
- [Team Interaction Mapping](../tactics/team-interaction-mapping.tactic.md)

**References:**
- [DDD Core Concepts Reference](../docs/ddd-core-concepts-reference.md)
- [Linguistic Anti-Patterns](../docs/linguistic-anti-patterns.md)

---

## Version History

- **1.0.0** (2026-02-10): Initial directive created per feedback (comment 2786008080)

---

**Curation Status:** ✅ Created per feedback, ready for integration into agent profiles
