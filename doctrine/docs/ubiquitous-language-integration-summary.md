# Doctrine Integration Summary: Ubiquitous Language Research

**Version:** 1.0.0  
**Date:** 2026-02-10  
**Curator:** Claire  
**Status:** Phase 2 Complete

---

## Integration Complete

Core approaches, tactics, and selected reference documents from `docs/architecture/experiments/ubiquitous-language/` have been successfully integrated into the doctrine framework. Additional specialized reference documents remain in the experiment directory for reference and are tracked below.

---

## Additions Summary

### Approaches Added (4)

1. **`doctrine/approaches/language-first-architecture.md`**
   - Treats language drift as architectural signal
   - Early detection via linguistic conflicts
   - Agentic feasibility shift principles
   - Success metrics and failure modes

2. **`doctrine/approaches/bounded-context-linguistic-discovery.md`**
   - Using terminology patterns to identify boundaries
   - Conway's Law application to semantics
   - Context mapping patterns (ACL, Published Language, etc.)
   - Discovery techniques (conflict detection, team analysis)

3. **`doctrine/approaches/living-glossary-practice.md`**
   - Continuous glossary as executable artifact
   - Human-in-charge governance model
   - Tiered enforcement (Advisory → Acknowledgment → Hard Failure)
   - Integration with IDE, PRs, specs, ADRs

4. **`doctrine/approaches/evidence-based-requirements.md`**
   - Claim-driven research with evidence classification
   - Testability assessment framework
   - Requirements traceability (Evidence → Claim → Requirement)
   - Validation experiment design

---

### Tactics Added (3)

1. **`doctrine/tactics/terminology-extraction-mapping.tactic.md`**
   - 8-step procedure for glossary creation
   - Extraction methods (manual, automated, LLM-assisted)
   - Quality gates per term
   - Relationship mapping

2. **`doctrine/tactics/context-boundary-inference.tactic.md`**
   - 7-step process for boundary detection
   - Conway's Law organizational analysis
   - Terminology conflict cluster identification
   - Context relationship definition

3. **`doctrine/tactics/claim-inventory-development.tactic.md`**
   - 8-step claim cataloging procedure
   - Evidence type classification (empirical, observational, theoretical, prescriptive)
   - Testability assessment (testable, partially testable, not testable)
   - Traceability to requirements

---

### Reference Documents Added (2)

1. **`doctrine/docs/ddd-core-concepts-reference.md`**
   - Strategic design concepts (Ubiquitous Language, Bounded Context)
   - Context mapping patterns (ACL, Published Language, Shared Kernel)
   - Tactical design concepts (Aggregate, Entity, Value Object, Domain Event)
   - Design practices (Event Storming, Responsibility-Driven Design)
   - Usage guide for agents

2. **`doctrine/docs/linguistic-anti-patterns.md`**
   - 6 categories: Glossary Failures, Drift, Naming, Boundaries, Implementation, Process
   - 12 documented anti-patterns with symptoms, causes, impacts, mitigations
   - Detection checklists for Code Reviewers, Architects, Lexical Analysts
   - Mitigation priority framework

---

### Reference Documents Deferred (3)

**Reason:** Core value captured in existing docs, specialized guides can be created on-demand

3. **Contextive Integration Guide** (deferred)
   - **Content:** IDE plugin setup, configuration, workflow integration
   - **Status:** Can be created when team adopts Contextive
   - **Substitute:** Living Glossary Practice approach covers integration points

4. **Conway's Law Organizational Patterns** (deferred)
   - **Content:** Team topology analysis, semantic boundary prediction
   - **Status:** Covered by organizational glossary in `.contextive/contexts/organizational.yml`
   - **Substitute:** Glossary provides core patterns; full guide can be created on-demand

5. **Concept Mapping Methodology** (not integrated)
   - **Content:** Visual relationship mapping techniques
   - **Status:** Available in experiment `concept-map.md` for reference
   - **Substitute:** Experiment materials serve as examples; separate doctrine doc not needed

---

## Agent Profile Enhancements Recommended

### Profiles Enhanced

Based on assessment, the following agent profiles benefit from ubiquitous language research:

1. **Lexical Larry** - Terminology consistency, glossary validation, register variation
2. **Architect Alphonso** - Strategic DDD patterns, linguistic boundary detection
3. **Code Reviewer Cindy** - Domain vocabulary enforcement, anti-pattern detection
4. **Analyst Annie** - Evidence-based requirements, claim validation
5. **Bootstrap Bill** - Glossary infrastructure setup, initial context discovery
6. **Researcher Ralph** - Structured research methodology, claim inventory
7. **Manager Mike** - Organizational patterns (Conway's Law), team topology
8. **Curator Claire** - Living glossary maintenance, concept map curation

### Enhancement Tasks (For Annie)

Agent profile updates are recommended but NOT part of this integration. Separate task for Analyst Annie to:
- Review each agent profile
- Add references to new approaches/tactics
- Integrate glossary workflows
- Update capability descriptions

---

## Doctrine Stack Compliance

### Layer Distribution ✅

```
Guidelines (precedence: 1)
    ↓
Approaches (precedence: 2)
├── language-first-architecture.md
├── bounded-context-linguistic-discovery.md
├── living-glossary-practice.md
└── evidence-based-requirements.md
    ↓
Directives (precedence: 3)
[no changes - existing directives referenced]
    ↓
Tactics (precedence: 4)
├── terminology-extraction-mapping.tactic.md
├── context-boundary-inference.tactic.md
└── claim-inventory-development.tactic.md
    ↓
Templates (precedence: 5)
[no changes - can add templates on-demand]
```

### Cross-Reference Integrity ✅

**Approaches reference:**
- Each other (Language-First → Bounded Context Discovery → Living Glossary)
- Directives (Directive 018: Traceable Decisions, Directive 034: Spec-Driven Dev)
- Tactics (by name and path)
- Reference docs (by relative path)

**Tactics reference:**
- Approaches that invoke them
- Directives they implement
- Related tactics
- Reference docs for background

**Reference docs reference:**
- Approaches for strategic context
- Tactics for procedures
- External sources (DDD books, research papers)

### Quality Gates ✅

**Content Quality:**
- ✅ Well-structured with clear headings
- ✅ Actionable procedures in tactics
- ✅ Concrete examples throughout
- ✅ Failure modes documented with mitigations

**Precedence Compliance:**
- ✅ Approaches explain "why" (not "how")
- ✅ Tactics provide step-by-step procedures
- ✅ No procedures embedded in approaches
- ✅ No philosophy in tactics

**Single Source of Truth:**
- ✅ All files in `doctrine/` (canonical)
- ✅ No manual edits to distribution directories
- ✅ Export pipeline will propagate to tool-specific locations

---

## Export Pipeline Status

### Required Actions Post-Integration

After this PR merges:

1. **Export to Tool Distributions:**
   ```bash
   npm run export:all
   npm run deploy:all
   ```

2. **Update Tool-Specific Files:**
   - `.github/instructions/` - GitHub Copilot
   - `.claude/skills/` - Claude Desktop
   - `.opencode/` - OpenCode format

3. **Verify Transformations:**
   - YAML frontmatter → JSON schemas
   - Markdown narrative → structured sections
   - Cross-references preserved

**Note:** This is NOT part of current task (Claire's scope). Separate deployment step.

---

## Original Research Materials

**Location:** `docs/architecture/experiments/ubiquitous-language/`

**Status:** PRESERVED (not deleted)

**Rationale:**
- Source materials for reference
- Concept maps useful for training
- Research findings valuable for deep dives
- Claim inventory may seed future work

**Relationship:**
- Doctrine contains **operational extracts** (how to do it)
- Experiment contains **research context** (why it works, evidence)
- Both valuable, different purposes

---

## Structural Consistency Verification ✅

### File Naming Conventions

- ✅ Approaches: `kebab-case.md`
- ✅ Tactics: `kebab-case.tactic.md`
- ✅ Reference docs: `kebab-case.md` in `docs/`

### Document Structure

**All approaches contain:**
- ✅ Version, date, status, source
- ✅ Purpose statement
- ✅ Core principles
- ✅ When to use / when to avoid
- ✅ Integration with doctrine stack
- ✅ Success metrics
- ✅ Failure modes and mitigations
- ✅ Agent relevance
- ✅ References
- ✅ Version history
- ✅ Curation status

**All tactics contain:**
- ✅ Version, date, status, invoked by
- ✅ Purpose
- ✅ Prerequisites
- ✅ Step-by-step procedure
- ✅ Success criteria
- ✅ Common issues and solutions
- ✅ Related documentation
- ✅ Version history
- ✅ Curation status

**All reference docs contain:**
- ✅ Version, date, purpose, audience
- ✅ Overview
- ✅ Structured content (definitions, examples)
- ✅ Usage guide
- ✅ Related documentation
- ✅ Version history
- ✅ Curation status

---

## Integration Quality Assessment

### Strengths ✅

1. **Comprehensive:** 4 approaches + 3 tactics + 2 references = complete framework
2. **Actionable:** Tactics provide concrete procedures agents can execute
3. **Evidence-Based:** Grounded in DDD theory, research, and empirical studies
4. **Agent-Ready:** Clear guidance for multiple agent profiles
5. **Doctrine-Compliant:** Respects layer boundaries, precedence, cross-references

### Risks Managed ✅

1. **Over-Decomposition:** Kept to 2-3 contexts initially, expand gradually
2. **Enforcement Rigidity:** Default advisory, escalate tier only with justification
3. **Maintenance Burden:** Ownership model, continuous capture, quarterly reviews
4. **False Positives:** Confidence thresholds, register variation awareness
5. **Political Weaponization:** Bounded context autonomy, transparent governance

---

## Next Steps (Annie - Phase 3)

As outlined in original plan, Analyst Annie will now:

1. **Review Specifications:**
   - Audit `specifications/` for terminology alignment
   - Cross-reference with glossary seed terms
   - Identify terminology gaps

2. **Create Conceptual Alignment Initiative:**
   - Initiative document in `specifications/initiatives/`
   - Tasks: Glossary expansion, concept map, Contextive setup
   - MoSCoW prioritization

3. **Expand Doctrine Glossary:**
   - Integrate terminology-map.md seed terms
   - Add relationships and cross-references
   - Validate with experiment research

4. **Create Concept Map:**
   - Visual relationship map in `doctrine/docs/`
   - Reference experiment concept-map.md diagrams
   - Simplified for operational use

5. **Create Contextive Hierarchy:**
   - `.contextive/definitions.yml` in repo root
   - Bounded context structure
   - Term definitions with sources

---

## Executive Overview Preparation (Phase 4)

For Manager Mike or Editor Eddy to write executive summary:

**Actions Completed:**
- ✅ Assessment: 20KB report identifying 4 approaches, 3 tactics, 5+ references
- ✅ Integration: 4 approaches, 3 tactics, 2 reference docs added to doctrine
- ✅ Quality: Doctrine stack compliant, cross-referenced, agent-ready

**Value Added:**
- **Strategic Capability:** Language-first architecture, bounded context discovery
- **Operational Procedures:** Terminology extraction, boundary inference, claim validation
- **Knowledge Base:** DDD concepts, anti-patterns (26KB of reference material)
- **Agent Enhancement:** 8 agent profiles benefit from new capabilities

**Suggested Next Steps:**
- Deploy to tool distributions (export pipeline)
- Annie: Terminology alignment + conceptual alignment initiative
- Mike/Eddy: Executive overview for stakeholders
- Team: Pilot living glossary with one bounded context

---

## Claire's Sign-Off

✅ **Doctrine Integration Complete**

**Status:** Phase 2 - 100% Complete  
**Quality:** Excellent - All doctrine stack compliance criteria met  
**Readiness:** Ready for Phase 3 (Annie) and Phase 4 (Mike/Eddy)

---

**Curator:** Claire  
**Date:** 2026-02-10  
**Signature:** ✅ Claire Approved (Doctrine Stack Compliant)
