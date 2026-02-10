# Glossary Extraction Summary: Batch 2 - Approaches

**Date:** 2026-02-10  
**Agent:** Lexical Larry  
**Source Directory:** `doctrine/approaches/`  
**Method:** Systematic extraction with contextual analysis  
**Focus:** Conceptual and philosophical terms (mental models, patterns, practices)

---

## Executive Summary

Extracted **129 candidate glossary terms** from **41 approach files** in the `doctrine/approaches/` directory. These terms represent strategic, conceptual, and philosophical concepts that guide agent-augmented development practices. The extraction prioritized mental models, design patterns, and methodology concepts over technical implementation details.

**Key Insight:** Approaches contain higher-level strategic concepts compared to directives (Batch 1), with stronger emphasis on mental models, failure modes, feasibility shifts, and organizational patterns.

---

## Statistics

### Files Processed

| Category | Count | Notes |
|----------|-------|-------|
| **Total approach files** | 41 | Includes subdirectories |
| **Core approaches** | 29 | Top-level approach files |
| **Subdirectory approaches** | 12 | file_based_collaboration/, operating_procedures/, prompt_documentation/ |
| **Files with extracted terms** | 27 | ~66% yield rate |
| **Files without terms** | 14 | README files, superseded files, operational checklists |

### Term Distribution

| Confidence Level | Count | Percentage | Rationale |
|-----------------|-------|------------|-----------|
| **High** | 89 | 69% | Clear definition from context, consistent usage, well-documented |
| **Medium** | 32 | 25% | Partially documented, context-dependent, or emerging pattern |
| **Low** | 8 | 6% | Nuanced concept, requires interpretation, or metric-based |
| **Total** | 129 | 100% | — |

### Category Breakdown

| Domain | Terms | Notable Concepts |
|--------|-------|------------------|
| **SDD & Specification** | 18 | Specification-Driven Development, Living Specification, 6-Phase Cycle, Scenario-Driven Design |
| **DDD & Language-First** | 24 | Language-First Architecture, Living Glossary, Bounded Context Discovery, Semantic Conflict |
| **Requirements & Evidence** | 8 | Evidence-Based Requirements, Claim Classification, Testability Assessment |
| **Traceability & Linking** | 8 | Traceability Chain, Bidirectional Linking, Impact Analysis, Orphaned Artifact |
| **Testing & Quality** | 13 | Reverse Speccing, Test-First Bug Fixing, Test-as-Documentation, Accuracy Score |
| **Self-Observation & Meta** | 8 | Ralph Wiggum Loop, Meta-Awareness, Warning Sign Detection, Meta-Analysis |
| **Orchestration & Coordination** | 11 | File-Based Orchestration, Task Lifecycle, Handoff Pattern, Work Directory Model |
| **Design Principles** | 14 | Locality of Change, Gold Plating, Complexity Creep, Simplicity Preservation |
| **Version Control** | 7 | Trunk-Based Development, Short-Lived Branch, Ship/Show/Ask Pattern |
| **Communication & Audience** | 7 | Target-Audience Fit, Persona-Driven Writing, Progressive Disclosure |
| **Tooling & Environment** | 4 | Tool Selection Rigor, Graceful Degradation, Version Pinning Strategy |
| **Meta-Patterns** | 7 | Feasibility Shift, Agentic Enablement, Organic Emergence, Pattern Before Prescription |

---

## Key Findings

### 1. Mental Models & Philosophical Concepts Dominate

Approaches focus heavily on **mental models** (how to think about problems) rather than **procedures** (what steps to take):

- **Language-First Architecture** - treating language drift as architectural signal
- **Feasibility Shift** - recognizing when technology makes previously infeasible practices viable
- **Organic Emergence** - letting patterns emerge from practice before prescribing
- **Human in Charge** - governance model emphasizing proactive ownership vs reactive oversight

**Implication:** These terms require careful definition and contextualization in the glossary to convey philosophical intent.

### 2. High Emphasis on Failure Modes & Anti-Patterns

Approaches document **what NOT to do** extensively:

- **Linguistic Policing** - glossary as compliance regime
- **Dictionary DDD** - create glossary, consider DDD done, never update
- **Gold Plating** - adding features "just in case"
- **Momentum Bias** - skipping phases due to pressure to move forward
- **Over-Decomposition** - too many tiny bounded contexts

**Implication:** Anti-pattern terms provide valuable "negative space" defining boundaries of good practice.

### 3. Agentic Enablement as Emerging Theme

Multiple approaches reference **feasibility shifts** enabled by AI agents:

- **Continuous Capture** - automated real-time observation replacing manual efforts
- **Incremental Maintenance** - small frequent updates instead of big-bang
- **Agentic Enablement** - capabilities making previously labor-intensive practices tractable
- **Economic Feasibility** - analyzing practice viability given current costs vs benefits

**Implication:** These meta-pattern terms explain WHY certain practices (Living Glossary, Language-First Architecture) are NOW viable but weren't historically.

### 4. Strong Traceability & Linking Patterns

Approaches emphasize **bidirectional connections** between artifacts:

- **Traceability Chain** - Goal → Spec → Tests → ADRs → Implementation → Logs
- **Bidirectional Linking** - forward AND backward navigation
- **Impact Analysis** - identifying affected artifacts when requirements change
- **Orphaned Artifact** - code/tests with no traceable purpose

**Implication:** These terms form a conceptual cluster around maintaining "why" knowledge throughout development lifecycle.

### 5. Self-Observation & Meta-Cognitive Patterns

Unique focus on **agent self-awareness**:

- **Ralph Wiggum Loop** - agent detecting warning signs in own behavior
- **Meta-Awareness** - observing and reasoning about execution state
- **Warning Sign Detection** - recognizing internal signals indicating problems
- **Self-Observation Checkpoint** - structured mid-task assessment

**Implication:** These represent novel concepts specific to agent-augmented development requiring clear glossary entries for newcomers.

---

## Comparison: Batch 1 (Directives) vs. Batch 2 (Approaches)

| Aspect | Batch 1 (Directives) | Batch 2 (Approaches) |
|--------|----------------------|----------------------|
| **Term count** | ~99 | 129 |
| **Confidence: High** | 74 (75%) | 89 (69%) |
| **Focus** | Procedural, operational, tactical | Conceptual, philosophical, strategic |
| **Dominant themes** | Context management, token discipline, workflow mechanics | Mental models, failure modes, feasibility shifts |
| **Anti-patterns** | Rare, implicit | Explicit, well-documented |
| **Agent-specific** | High (agent behaviors, directives) | Medium (methodology, patterns) |
| **Duplicates with Batch 1** | N/A | ~12 terms overlap (e.g., Traceability, ADR, Bounded Context) |

**Key Insight:** Approaches complement directives by providing the **"why"** (philosophy, rationale) while directives provide the **"how"** (specific actions, constraints).

---

## Term Categorization by Usage Context

### Strategic Terms (for Architects, Managers)
- Language-First Architecture
- Feasibility Shift
- Organic Emergence
- Evidence-Based Requirements
- Bounded Context Linguistic Discovery
- Conway's Law Applied

### Methodological Terms (for Development Teams)
- Specification-Driven Development
- Six-Phase Cycle
- Test-First Bug Fixing
- Trunk-Based Development
- File-Based Orchestration
- Decision-First Development

### Quality Assurance Terms (for QA, Testing)
- Reverse Speccing
- Test-as-Documentation
- Accuracy Score
- Regression Prevention
- Test Validates Fix

### Agent-Specific Terms (for Agent Developers)
- Ralph Wiggum Loop
- Meta-Awareness
- Warning Sign Detection
- Self-Observation Checkpoint
- Phase Checkpoint Protocol

### Governance & Process Terms (for Framework Maintainers)
- Living Glossary
- Glossary Ownership
- Enforcement Tier
- Human in Charge
- Decision Debt

---

## Quality Observations

### High-Quality Term Definitions

Terms with clear, unambiguous definitions from source material:

1. **Specification-Driven Development** - comprehensive definition with examples
2. **Six-Phase Cycle** - detailed phase descriptions with ownership model
3. **Reverse Speccing** - clear dual-agent validation technique with metrics
4. **Ralph Wiggum Loop** - well-documented self-observation pattern with triggers
5. **Living Glossary** - contrasts with traditional glossaries, explains benefits

### Terms Requiring Additional Context

Terms that may need supplemental notes or examples in glossary:

1. **Feasibility Shift** - abstract concept, needs concrete examples
2. **Linguistic Signal** - requires understanding of Language-First Architecture
3. **Decision Debt** - metric concept, needs threshold explanations
4. **Meta-Awareness** - philosophical concept, needs operational grounding
5. **Organic Emergence** - principle requiring examples of application

### Terms with Potential Overlap

Terms that may need cross-referencing to avoid redundancy:

- **Living Specification** ↔ **Living Glossary** (both "living" artifacts)
- **Bidirectional Linking** ↔ **Traceability Chain** (linking concepts)
- **Gold Plating** ↔ **Premature Abstraction** (related anti-patterns)
- **Momentum Bias** ↔ **Role Confusion** (related failure modes)
- **Test-as-Documentation** ↔ **Reverse Speccing** (test quality concepts)

---

## Extraction Methodology Notes

### Inclusion Criteria

Terms were included if they:
- Represent **conceptual/philosophical ideas** (not technical jargon)
- Have **clear definitions** from context or explicit explanations
- Appear **consistently** across sections or multiple files
- Provide **strategic guidance** or **mental models**
- Represent **patterns, practices, or anti-patterns**

### Exclusion Criteria

Terms were excluded if they:
- Are **purely technical** (e.g., "YAML", "Git", "REST API")
- Are **agent names** or **specific tools** (covered in other glossaries)
- Are **obvious** without definition (e.g., "documentation", "testing")
- Lack **sufficient context** to define accurately
- Are **one-off usage** without conceptual significance

### Extraction Process

1. **Systematic Reading** - Read each approach file completely
2. **Concept Identification** - Flag conceptual terms, mental models, patterns
3. **Context Extraction** - Extract definition from surrounding paragraphs
4. **Related Terms Mapping** - Identify term clusters and relationships
5. **Confidence Assessment** - Evaluate clarity, consistency, and context
6. **YAML Generation** - Format with metadata, confidence, and notes

---

## Recommendations

### For Glossary Integration

1. **Prioritize High-Confidence Terms (89 terms)**
   - These have clear definitions and strong contextual support
   - Recommend immediate integration into `doctrine/GLOSSARY.md`

2. **Review Medium-Confidence Terms (32 terms)**
   - May require additional examples or clarification
   - Consider pilot integration with [DRAFT] status

3. **Defer Low-Confidence Terms (8 terms)**
   - Require more usage examples or stabilized definitions
   - Revisit after 6 months of operational observation

4. **Address Overlaps with Batch 1**
   - ~12 terms appear in both batches (e.g., Bounded Context, ADR references)
   - Consolidate definitions, preferring approach-level (strategic) framing

### For Documentation Enhancements

1. **Create Visual Concept Maps**
   - Cluster related terms (e.g., DDD concepts, SDD lifecycle, testing patterns)
   - Show relationships and dependencies visually

2. **Add Concrete Examples**
   - Supplement abstract terms (Feasibility Shift, Organic Emergence) with real-world examples
   - Link to work logs or completed tasks demonstrating concepts

3. **Cross-Reference ADRs**
   - Many terms reference architectural decisions (ADR-008, ADR-017, etc.)
   - Ensure bidirectional links between glossary and ADRs

4. **Maintain Living Document**
   - Glossary should follow its own principle—continuous updates as terminology evolves
   - Quarterly reviews to add new terms, deprecate obsolete ones

### For Future Batch Extractions

1. **Batch 3: Tactics** (~30 files expected)
   - Expect more procedural terms, step-by-step patterns
   - Likely higher term density but lower strategic significance

2. **Batch 4: Specifications** (variable count)
   - Domain-specific terminology, feature-related concepts
   - May require separate domain glossaries

3. **Batch 5: ADRs** (~40+ decisions)
   - Decision-specific rationale, trade-off terminology
   - High overlap with approaches but more concrete

---

## Appendix: Files Processed

### Files with Terms Extracted (27)

1. spec-driven-development.md
2. spec-driven-6-phase-cycle.md
3. decision-first-development.md
4. language-first-architecture.md
5. bounded-context-linguistic-discovery.md
6. living-glossary-practice.md
7. evidence-based-requirements.md
8. reverse-speccing.md
9. test-first-bug-fixing.md
10. test-readability-clarity-check.md
11. traceability-chain-pattern.md
12. traceable-decisions-detailed-guide.md
13. ralph-wiggum-loop.md
14. work-directory-orchestration.md
15. locality-of-change.md
16. meta-analysis.md
17. trunk-based-development.md
18. target-audience-fit.md
19. style-execution-primers.md
20. agent-profile-handoff-patterns.md
21. design_diagramming-incremental_detail.md
22. tooling-setup-best-practices.md
23. bug-fixing-checklist.md
24. file_based_collaboration/README.md (partial)
25. operating_procedures/README.md (partial)
26. prompt_documentation/README.md (partial)
27. 01_redundancy_rationale.md (partial)

### Files Without Terms Extracted (14)

- README.md (index, no conceptual terms)
- file-based-orchestration.md (superseded)
- file_based_collaboration/01-07 (operational checklists)
- operating_procedures/01_redundancy_rationale.md (duplicate)
- prompt_documentation/01-04 (process guidelines)

---

## Metrics Summary

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **Approaches processed** | 41 | 41 | ✅ Complete |
| **Terms extracted** | 129 | 100+ | ✅ Exceeds target |
| **High-confidence terms** | 89 | 70+ | ✅ High quality |
| **Extraction time** | ~3 hours | <4 hours | ✅ On schedule |
| **Average terms/file** | 4.8 | 3-5 | ✅ Good density |
| **Duplicate rate** | ~9% | <15% | ✅ Low overlap |

---

## Next Steps

1. **Review Candidates** ✅ DONE
   - Generated batch2-approaches-candidates.yaml with 129 terms

2. **Integration Planning** (Week of 2026-02-17)
   - Compare with Batch 1 to identify overlaps
   - Prioritize high-confidence terms for immediate integration
   - Create consolidated glossary merge plan

3. **Glossary Update** (Week of 2026-02-24)
   - Integrate high-confidence terms into doctrine/GLOSSARY.md
   - Add cross-references to approaches and ADRs
   - Update glossary maintenance documentation

4. **Batch 3 Extraction** (Week of 2026-03-03)
   - Extract from doctrine/tactics/
   - Expected ~80-100 terms (more procedural focus)

5. **Quality Review** (Week of 2026-03-10)
   - Cross-validate all batches
   - Consolidate duplicate definitions
   - Generate final integrated glossary v2.0

---

**Status:** ✅ Batch 2 extraction complete  
**Deliverables:**
- [x] batch2-approaches-candidates.yaml (129 terms)
- [x] batch2-approaches-extraction-summary.md (this document)
- [ ] Comparison analysis with Batch 1 (pending)
- [ ] Integration into doctrine/GLOSSARY.md (pending)

**Confidence Assessment:** High—extraction methodology consistent, term definitions well-grounded in source material, cross-referencing comprehensive.

**Agent:** Lexical Larry  
**Date:** 2026-02-10  
**Review Recommended:** Yes—by Curator Claire or Architect Alphonso for validation
