# Tactic: Team Interaction Mapping

**Version:** 1.0.0  
**Date:** 2026-02-10  
**Status:** Active  
**Invoked By:** [Bounded Context Linguistic Discovery](../approaches/bounded-context-linguistic-discovery.md)

---

## Purpose

Map organizational communication patterns to identify vocabulary clusters and predict semantic boundaries using Conway's Law principles.

---

## Prerequisites

- [ ] Access to organizational structure documentation
- [ ] Ability to observe or survey team communication patterns
- [ ] Understanding of Conway's Law and its relationship to semantic boundaries

---

## Procedure

### Step 1: Map Teams and Communication Channels

**Objective:** Document how teams interact

**Actions:**
1. **List all teams:**
   - Development teams
   - Product teams
   - Operations teams
   - Support teams

2. **Document communication frequency:**
   - Daily: Stand-ups, pair programming, shared Slack channels
   - Weekly: Planning meetings, reviews
   - Monthly: Cross-team syncs, all-hands
   - Rarely: Occasional handoffs

3. **Identify shared artifacts:**
   - Which teams contribute to same repositories?
   - Which teams share documentation?
   - Which teams attend same meetings?

**Output:** Team interaction matrix

**Time Estimate:** 1-2 hours

---

### Step 2: Identify Vocabulary Clusters

**Objective:** Determine which teams share terminology

**Actions:**
1. **Survey teams:** Ask each team to list their core domain terms (10-20 key concepts)

2. **Compare vocabulary:**
   - Which terms are used consistently across teams?
   - Where do definitions diverge?
   - What translation happens at handoffs?

3. **Map vocabulary to teams:**
   - Team A owns terms: {Customer, Order, Quote}
   - Team B owns terms: {Shipment, Warehouse, Inventory}
   - Shared terms with conflicts: {Order - different meanings}

**Output:** Vocabulary ownership map

**Time Estimate:** 2-3 hours

---

### Step 3: Overlay Boundaries

**Objective:** Align vocabulary boundaries with team boundaries

**Actions:**
1. **Check alignment:**
   - Do semantic boundaries match team boundaries?
   - Where is there mismatch?

2. **Hypothesis formation:**
   - Teams that communicate infrequently develop different vocabularies
   - Where vocabulary diverges, context boundaries likely exist

3. **Validation:**
   - Ask teams to define same term independently
   - If definitions differ significantly, boundary exists

**Output:** Proposed context boundaries aligned with communication patterns

**Time Estimate:** 1-2 hours

---

## Success Criteria

**Mapping is successful when:**
- ✅ All team communication channels documented
- ✅ Vocabulary clusters identified and mapped to teams
- ✅ Boundaries proposed where vocabulary diverges
- ✅ Hypothesis validated with team feedback

---

## Common Issues and Solutions

**Issue 1: Teams can't articulate their vocabulary**
**Solution:** Extract from codebase, documentation, meeting notes

**Issue 2: Vocabulary conflicts but teams claim alignment**
**Solution:** Ask for definitions in writing, compare objectively

**Issue 3: Conway's Law violation (structure doesn't match semantics)**
**Solution:** Document mismatch as risk, consider reorganization

---

## Related Documentation

**Approaches:**
- [Bounded Context Linguistic Discovery](../approaches/bounded-context-linguistic-discovery.md) - Strategic framework

**Tactics:**
- [Context Boundary Inference](context-boundary-inference.tactic.md) - Comprehensive boundary detection

**Reference:**
- Conway's Law Patterns - See `.contextive/contexts/organizational.yml`

---

## Version History

- **1.0.0** (2026-02-10): Initial extraction from bounded-context-linguistic-discovery approach

---

**Curation Status:** ✅ Extracted per feedback (comment 2785993401)
