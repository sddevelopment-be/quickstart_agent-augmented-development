# Glossary Batch Comparison: Directives vs Approaches

**Date:** 2026-02-10  
**Agent:** Lexical Larry  
**Purpose:** Compare terminology extraction across Batch 1 (directives) and Batch 2 (approaches)

---

## Overview Statistics

| Metric | Batch 1 (Directives) | Batch 2 (Approaches) | Total |
|--------|----------------------|----------------------|-------|
| **Files processed** | 32 | 41 | 73 |
| **Terms extracted** | 99 | 129 | 228 |
| **High-confidence** | 74 (75%) | 89 (69%) | 163 (71%) |
| **Medium-confidence** | 21 (21%) | 32 (25%) | 53 (23%) |
| **Low-confidence** | 4 (4%) | 8 (6%) | 12 (5%) |
| **Average terms/file** | 3.1 | 4.8 | 3.8 |

---

## Thematic Comparison

### Batch 1: Directives (Operational/Tactical)

**Focus:** How to execute tasks, operational constraints, agent behaviors

**Dominant themes:**
- Context management & token discipline
- Workflow mechanics & state transitions
- Agent collaboration protocols
- Tool usage & fallback strategies
- Error handling & escalation

**Example terms:**
- External Memory
- Token Discipline
- Bypass Check
- Remediation Technique
- Fallback Strategy

### Batch 2: Approaches (Conceptual/Strategic)

**Focus:** Why practices matter, mental models, design philosophy

**Dominant themes:**
- Mental models & philosophical concepts
- Failure modes & anti-patterns (explicit)
- Feasibility shifts & agentic enablement
- Traceability & linking patterns
- Self-observation & meta-awareness

**Example terms:**
- Language-First Architecture
- Feasibility Shift
- Organic Emergence
- Ralph Wiggum Loop
- Living Glossary

---

## Overlapping Terms (~12 terms)

Terms appearing in both batches with similar definitions:

1. **Bounded Context** - DDD concept (approaches deeper, directives operational)
2. **ADR / Traceable Decisions** - Referenced in both, approaches philosophize
3. **Glossary Ownership** - Living Glossary practice vs directive enforcement
4. **Context Layer** - Batch 1 technical, Batch 2 architectural
5. **Work Directory** - Batch 1 structure, Batch 2 orchestration model
6. **Task Lifecycle** - Batch 1 states, Batch 2 philosophical framing
7. **Handoff Protocol** - Batch 1 mechanics, Batch 2 patterns
8. **Decision Marker** - Batch 1 format, Batch 2 workflow integration
9. **Test-Driven** - Batch 1 directive, Batch 2 methodological approach
10. **Acceptance Test** - Batch 1 requirement, Batch 2 SDD integration
11. **Enforcement Tier** - Living Glossary concept in both
12. **Human in Charge** - Governance model (Batch 2 originating)

**Recommendation:** Consolidate these with preference for strategic framing from Batch 2, add operational notes from Batch 1.

---

## Unique Contributions

### Batch 1 Unique Strengths

**Procedural clarity:**
- Specific agent behaviors (e.g., Bypass Check, LOCAL_ENV.md)
- Tool-specific guidance (rg, fd, ast-grep fallbacks)
- Error handling mechanics (flaky terminal behavior)

**Agent execution context:**
- Context note types (CONTEXT, DECISION, EXECUTION)
- External memory usage patterns
- Offloading techniques for token management

### Batch 2 Unique Strengths

**Conceptual depth:**
- Philosophical frameworks (Language-First, Organic Emergence)
- Failure mode taxonomy (Gold Plating, Momentum Bias, Dictionary DDD)
- Meta-patterns (Feasibility Shift, Agentic Enablement)

**Strategic guidance:**
- Mental models for decision-making
- Anti-patterns with explicit mitigations
- Self-observation patterns for agents

---

## Integration Strategy

### Phase 1: High-Confidence Core (163 terms)
- Merge Batch 1 + Batch 2 high-confidence terms
- Resolve 12 overlaps by consolidating definitions
- Create primary glossary entries with cross-references

### Phase 2: Medium-Confidence Review (53 terms)
- Pilot integration with [DRAFT] status
- Gather feedback from usage
- Promote to canonical after 3 months validation

### Phase 3: Low-Confidence Monitoring (12 terms)
- Track in separate "Emerging Terminology" section
- Revisit quarterly as usage patterns stabilize
- Promote when confidence increases

### Phase 4: Cross-Referencing
- Link glossary entries to source files (approaches, directives)
- Add bidirectional references (term ↔ ADR, term ↔ approach)
- Create concept maps for term clusters

---

## Term Clusters (Cross-Batch)

### Cluster 1: DDD & Language
- **From Batch 1:** Context Layer, Bounded Context (operational)
- **From Batch 2:** Language-First Architecture, Living Glossary, Semantic Conflict, Ubiquitous Language
- **Integration:** Create DDD concepts section with strategic + operational views

### Cluster 2: Orchestration & Coordination
- **From Batch 1:** Work Directory, Task State, External Memory
- **From Batch 2:** File-Based Orchestration, Task Lifecycle, Handoff Pattern
- **Integration:** Orchestration section covering philosophy → mechanics

### Cluster 3: Decision & Traceability
- **From Batch 1:** Decision Marker (format), Context Notes
- **From Batch 2:** Decision-First Development, Traceability Chain, Bidirectional Linking
- **Integration:** Decision Documentation section covering workflow → artifacts

### Cluster 4: Testing & Quality
- **From Batch 1:** Acceptance Test (directive requirement)
- **From Batch 2:** Test-First Bug Fixing, Reverse Speccing, Test-as-Documentation
- **Integration:** Testing Philosophy section covering principles → practices

### Cluster 5: Self-Observation & Meta
- **From Batch 1:** Meta-Mode (directive)
- **From Batch 2:** Ralph Wiggum Loop, Meta-Awareness, Self-Observation Checkpoint
- **Integration:** Agent Meta-Cognition section (novel to agent-augmented development)

---

## Quality Observations

### Complementary Nature
- Batch 1 provides **"how"** (execution mechanics)
- Batch 2 provides **"why"** (philosophical rationale)
- Together create complete understanding (philosophy → practice)

### Consistency
- Terminology usage is consistent across batches
- No contradictory definitions found
- Cross-references naturally align

### Gaps Identified
- **Tactical procedures** (Batch 3 - tactics expected to fill)
- **Domain-specific terms** (Batch 4 - specifications will address)
- **Architectural decisions** (Batch 5 - ADRs will provide rationale)

---

## Recommendations

### For Glossary Maintainers

1. **Prioritize Strategic Framing**
   - When consolidating overlaps, prefer Batch 2 strategic definitions
   - Add Batch 1 operational notes as supplementary context

2. **Create Hierarchical Structure**
   - Top-level: Mental models & principles
   - Mid-level: Methodologies & patterns
   - Low-level: Operational mechanics

3. **Enable Multiple Entry Points**
   - Strategic readers: Start with Batch 2 concepts
   - Operational readers: Start with Batch 1 procedures
   - Cross-reference between levels

4. **Maintain Living Document**
   - Update quarterly as terminology evolves
   - Add new terms from Batches 3-5
   - Deprecate obsolete terms with migration notes

### For Documentation Writers

1. **Use Strategic Terms for Approaches**
   - Reference Batch 2 mental models in approach documents
   - Explain philosophical rationale using glossary terms

2. **Use Operational Terms for Directives**
   - Reference Batch 1 mechanics in directive documents
   - Provide step-by-step guidance using glossary terms

3. **Bridge Philosophy → Practice**
   - Link strategic concepts to operational mechanics
   - Show how mental models translate to concrete actions

---

## Next Steps

- [x] Complete Batch 1 extraction (directives)
- [x] Complete Batch 2 extraction (approaches)
- [ ] Consolidate overlapping terms (12 terms)
- [ ] Integrate high-confidence terms into doctrine/GLOSSARY.md
- [ ] Begin Batch 3 extraction (tactics/)
- [ ] Create concept maps for term clusters
- [ ] Establish glossary maintenance rhythm

---

**Status:** Analysis complete  
**Deliverables Ready:**
- batch1-directives-candidates.yaml (99 terms)
- batch2-approaches-candidates.yaml (129 terms)
- batch1-batch2-comparison.md (this document)

**Agent:** Lexical Larry  
**Date:** 2026-02-10  
**Confidence:** High—systematic extraction, consistent methodology, clear complementary relationship
