# Batch 4: Agent Profile Terminology Extraction Summary

**Date:** 2026-02-10  
**Agent:** Lexical Larry  
**Source:** `doctrine/agents/` (21 agent profiles)  
**Output:** `batch4-agents-candidates.yaml`

---

## Executive Summary

**Final extraction batch** (4 of 4) focusing on agent roles, collaboration patterns, and handoff protocols. Extracted **120 high-confidence terms** defining WHO does WHAT in the doctrine ecosystem.

### Key Metrics

- **Agents Processed:** 21/21 (100%)
- **Terms Extracted:** 120
- **Confidence Distribution:** 100% high-confidence
- **New Terms:** ~95 (agent names, roles, phase authority, handoff patterns)
- **Enhanced Terms:** ~25 (existing terms with agent-specific context)

### Quality Assessment

✅ **Strengths:**
- Complete coverage of all agent profiles
- High confidence across all terms (agent roles clearly defined)
- Strong focus on collaboration boundaries and handoff protocols
- Clear mapping of Spec-Driven Development phase authority
- Comprehensive output artifact definitions

⚠️ **Considerations:**
- Some overlap with existing glossary terms (ADR, Specification, TDD) - enhanced with agent context
- Agent-specific terminology may need consolidation during curation
- Review dimensions could be further detailed

---

## Extraction Overview

### Source Coverage

**21 Agent Profiles Analyzed:**

| Agent | Role | Primary Focus |
|-------|------|---------------|
| Analyst Annie | Requirements Specialist | Testable specifications, data validation |
| Architect Alphonso | Architecture Specialist | System decomposition, ADRs, trade-offs |
| Backend Benny | Backend Developer | Service design, API contracts, persistence |
| Bootstrap Bill | Repository Scaffolding | Topology mapping, structural artifacts |
| DevOps Danny | Build Automation | CI/CD pipelines, reproducible builds |
| Code Reviewer Cindy | Review Specialist | Code quality, standards compliance |
| Curator Claire | Curation Specialist | Structural consistency, doctrine stack |
| Diagram Daisy | Diagramming Specialist | Diagram-as-code, semantic fidelity |
| Framework Guardian | Framework Maintenance | Drift detection, upgrade management |
| Frontend Freddy | Frontend Specialist | UI architecture, component patterns |
| Java Jenny | Java Developer | Java quality, Maven, testing |
| Lexical Larry | Style Analyst | Tone fidelity, style compliance |
| Manager Mike | Coordinator | Task routing, workflow orchestration |
| Planning Petra | Planning Specialist | Milestone definition, batch planning |
| Python Pedro | Python Developer | Type safety, pytest, coverage |
| Researcher Ralph | Research Specialist | Literature synthesis, source grounding |
| Reviewer | Quality Assurance | Multi-dimensional reviews |
| Scribe Sally | Documentation Specialist | Meeting notes, neutral summaries |
| Synthesizer Sam | Integration Specialist | Multi-agent synthesis |
| Translator Tanya | Translation Specialist | Voice fidelity, tone preservation |
| Editor Eddy | Writer-Editor | Editorial refinement, voice alignment |

---

## Terminology Categories

### 1. Agent Role Names (21 terms)

**Definition Pattern:** "[Agent Name]" = [Role] agent focused on [primary capability] with [key deliverable]

**Examples:**
- **Analyst Annie:** Requirements specialist producing testable specifications
- **Architect Alphonso:** Architecture specialist creating ADRs and trade-off analysis
- **Python Pedro:** Python developer applying ATDD + TDD with type safety

**Usage Context:** Agent assignment, handoff protocols, authority designation

---

### 2. Collaboration Protocols (10 terms)

**Key Concepts:**
- **Hand-off Protocol:** Structured agent-to-agent work transfer
- **Phase Authority:** PRIMARY/CONSULT/NO designation per Spec-Driven Development phase
- **Phase 1-6:** Explicit phase definitions with authority assignments

**Spec-Driven Development Flow:**
```
Phase 1 (Analysis)      → Analyst Annie (PRIMARY)
Phase 2 (Architecture)  → Architect Alphonso (PRIMARY)
Phase 3 (Planning)      → Planning Petra (PRIMARY)
Phase 4 (Accept Tests)  → Assigned agent
Phase 5 (Implementation)→ Assigned agent
Phase 6 (Review)        → Reviewer, Architect, Analyst
```

**Critical Pattern:** Clean boundaries prevent agents from operating outside authority, ensuring phase transitions and preventing rework.

---

### 3. Output Artifacts (22 terms)

**Structural Artifacts (Bootstrap Bill):**
- **REPO_MAP:** Repository topology documentation
- **SURFACES:** Integration points and API documentation
- **WORKFLOWS:** Build, test, deployment workflow documentation

**Coordination Artifacts (Manager Mike):**
- **AGENT_STATUS:** Current agent assignments and progress
- **WORKFLOW_LOG:** Chronological multi-agent execution log
- **HANDOFFS:** Work products ready for next agent

**Planning Artifacts (Planning Petra):**
- **PLAN_OVERVIEW:** Goals, themes, focus areas
- **NEXT_BATCH:** Concrete ready-to-run tasks (1-2 weeks)

**Quality Artifacts (Reviewer, Framework Guardian):**
- **Review Report:** Multi-dimensional quality findings
- **Audit Report:** Framework integrity vs. manifest
- **Upgrade Plan:** Conflict resolution with minimal patches

**Style Artifacts (Lexical Larry):**
- **LEX_REPORT:** Per-file style compliance checklist
- **LEX_DELTAS:** Minimal suggested edits grouped by rule
- **LEX_TONE_MAP:** Medium detection with confidence scores

**Curation Artifacts (Curator Claire):**
- **Discrepancy Report:** Detected inconsistencies
- **Corrective Action Set:** Minimal alignment proposals

---

### 4. Quality Gates & Procedures (12 terms)

**Development Quality Gates:**
- **Self-Review Protocol:** Systematic pre-completion checklist
- **Coverage Threshold:** ≥80% required (with ADR exceptions)
- **Type Checking:** mypy clean (Python), no type errors
- **RED-GREEN-REFACTOR:** TDD cycle discipline

**Review Dimensions (Multi-dimensional QA):**
- **Structural Review:** Organization, flow, template compliance
- **Editorial Review:** Clarity, readability, terminology consistency
- **Technical Review:** Accuracy, examples, code correctness
- **Standards Compliance Review:** Style guides, directives, ADRs

**Testing Concepts:**
- **Acceptance Criteria:** Explicit testable conditions
- **Executable Test:** Automated validation of requirements
- **Representative Data:** Real-world samples for validation

---

### 5. Specialized Capabilities (9 terms)

**Framework Maintenance (Framework Guardian):**
- **Drift Detection:** Divergence identification via checksums
- **Conflict Classification:** Auto-merge vs. manual review categorization
- **Core/Local Boundary:** Framework vs. customization separation

**Style & Translation:**
- **Medium Detection:** Pattern/Podcast/LinkedIn/Essay identification
- **Voice Fidelity:** Authorial tone/rhythm preservation measure
- **Tone Preservation:** Maintaining emotional register during transformation

**Visualization:**
- **Diagram-as-Code:** Text-based diagram formats (Mermaid, PlantUML)
- **Semantic Fidelity:** Conceptual accuracy in visual representation

**Repository Analysis:**
- **Topology Mapping:** Structure scanning and navigation documentation

---

### 6. Workspace Organization (4 terms)

**Path Variables (Doctrine Configuration):**

| Variable | Default | Purpose | Used As |
|----------|---------|---------|---------|
| `workspace_root` | `work` | Task orchestration workspace | `${WORKSPACE_ROOT}` |
| `doc_root` | `docs` | Documentation root | `${DOC_ROOT}` |
| `spec_root` | `specifications` | Specification files | `${SPEC_ROOT}` |
| `output_root` | `output` | Generated artifacts | `${OUTPUT_ROOT}` |

**Configuration:** Defined in `.doctrine/config.yaml`, generated by Bootstrap Bill during repository initialization.

---

### 7. Doctrine Stack Concepts (4 terms)

**Architecture Principles (Curator Claire's domain):**

- **Source vs Distribution:** `doctrine/` (canonical source) vs. `.github/`, `.claude/`, `.opencode/` (generated)
- **Export Pipeline:** Automated transformation from source to tool-specific formats
- **Tool-Specific Distribution:** Format-adapted content for dev tools
- **Layer Boundary:** Separation preventing content type mixing (Guidelines/Approaches/Directives/Tactics/Templates)

**Critical Rule:** Always edit source (`doctrine/`), never distribution files. Re-run export pipeline after changes.

---

### 8. Integration Patterns (8 terms)

**Orchestration:**
- **Agent Assignment:** Task routing to appropriate specialized agent
- **YAML Task File:** Structured task definition for file-based orchestration

**Planning:**
- **Batch Planning:** Time-boxed units (not date promises)
- **Task Breakdown:** Spec → executable tasks with dependencies
- **Dependency Mapping:** Prerequisite relationship documentation
- **Milestone Definition:** Goals with decision gates and re-planning triggers

**Quality:**
- **Finding Summary:** Executive summary of review critical issues
- **Validation Checklist:** Review completeness verification

---

### 9. Technology-Specific Terms

**Python Development (Python Pedro):**
- **Type Hints:** Python 3.9+ type annotations
- **pytest:** Testing framework with fixtures and parametrization
- **mypy:** Static type checker
- **ruff:** Fast linter (replaces flake8, isort, pydocstyle)
- **black:** Code formatter (PEP 8 compliance)

**Frontend Development (Frontend Freddy):**
- **UI Architecture:** Component hierarchies, state boundaries, data flow
- **Component Patterns:** Reusable UI designs
- **State Boundaries:** State ownership and flow divisions
- **Design System:** Reusable components, patterns, guidelines

**Backend Development (Backend Benny):**
- **Service Design:** Boundaries, contracts, failure modes
- **Persistence Strategy:** Data storage and retrieval decisions
- **Performance Budget:** Explicit constraints on response time/resources
- **Integration Surface:** APIs, protocols, external interaction contracts

**Build Automation (DevOps Danny):**
- **Build Graph:** Dependency DAG for execution order
- **Reproducible Build:** Identical artifacts from same inputs

---

### 10. Collaboration Boundaries

**Role Definition:**
- **Specialization Boundary:** Explicit limits on agent capabilities (focus/awareness/avoid/success)
- **Escalation:** Surfacing to humans when uncertainty >30%

**Voice Preservation:**
- **Tonal Integrity:** Consistent voice across documents
- **Authorial Voice:** Distinctive style to preserve (calm, slightly amusing, patient)
- **Tone Preservation:** Active maintenance during transformation

**Change Management:**
- **Minimal Patch:** Smallest change resolving issue (Directive 021)
- **Corrective Action Set:** Minimal curator proposals preserving voice
- **Local Customization:** Repository-specific modifications to preserve

---

## Key Patterns Identified

### 1. Spec-Driven Development Phase Authority

**Structured Workflow with Clean Boundaries:**

Each phase has explicit PRIMARY authority preventing agents from operating outside their domain:

```
Annie (Analysis) → Alphonso (Architecture) → Petra (Planning) → Implementation Agent → Review Agents
```

**Hand-off Protocol Requirements:**
- What artifacts are ready
- Validation criteria passed
- Which agent receives next
- Phase checkpoint confirmation

**Prevents:** Scope creep, rework, role confusion, responsibility gaps

---

### 2. Multi-Agent Orchestration

**File-Based Coordination (Manager Mike):**

Three coordination artifacts maintain workflow visibility:
- **AGENT_STATUS.md:** Current assignments and progress
- **WORKFLOW_LOG.md:** Chronological execution history
- **HANDOFFS.md:** Ready work products awaiting next agent

**YAML Task Files:** Structured definitions moved through `assigned/` → `done/` directories

**Enables:** Conflict-free, traceable workflows with at-a-glance visibility

---

### 3. Quality Through Self-Review

**Development Agents Apply:**
1. Test-First (ATDD + TDD) before implementation
2. Self-Review Protocol before completion
3. Boy Scout Rule (leave better than found)
4. Work Log documentation (Directive 014)

**Quality Gates:**
- ≥80% test coverage
- Type checking clean
- Linting clean
- Acceptance criteria met
- ADR compliance verified

**Prevents:** Quality degradation, technical debt accumulation, untested code

---

### 4. Framework Integrity Without Overwrites

**Framework Guardian Principles:**
- **Audit-only:** Never modifies files directly
- **Drift Detection:** Checksum-based divergence identification
- **Conflict Classification:** Explicit categorization (auto-merge/preserve/breaking)
- **Core/Local Boundary:** Clear separation preserving customizations

**Output:** Audit reports and upgrade plans requiring human approval

**Prevents:** Silent overwrites, customization loss, upgrade conflicts

---

### 5. Voice Preservation Through Minimal Edits

**Content Agents (Lexical, Editor, Translator, Curator):**
- Preserve authorial voice and rhythm
- Minimal diffs (patch-ready)
- Before/after snippets for non-trivial changes
- Rule-grounded rationales

**Lexical Larry Evaluation Grid:**
- Tone: calm/clear/sincere
- Rhythm: sentence variety, short paragraphs
- Markdown: semantic structure
- Anti-fluff: no hype, no flattery

**Prevents:** Stylistic flattening, voice loss, unnecessary rewrites

---

### 6. Doctrine Stack Awareness

**Curator Claire's Deep Knowledge:**

5-Layer Stack with boundary enforcement:
1. **Guidelines:** Values, preferences (highest precedence)
2. **Approaches:** Mental models, philosophies
3. **Directives:** Instructions, constraints
4. **Tactics:** Procedural execution
5. **Templates:** Output structures (lowest precedence)

**Critical Distinction:**
- **Source:** `doctrine/` (edit here)
- **Distribution:** `.github/`, `.claude/`, `.opencode/` (generated)

**Export Pipeline:** Transforms source to tool-specific formats

**Prevents:** Layer boundary violations, source/distribution confusion, manual edits to generated files

---

## Confidence Analysis

### High Confidence (100% - 120 terms)

**Why 100% high confidence:**
1. **Clear source context:** Agent profiles explicitly define roles, capabilities, boundaries
2. **Consistent patterns:** Standard profile structure across all 21 agents
3. **Explicit definitions:** Specialization sections detail focus/awareness/avoid/success
4. **Well-documented protocols:** Hand-off protocols and phase authority clearly specified
5. **Concrete artifacts:** Output artifacts with defined locations and formats

**Agent Role Names:** All 21 agents have explicit role definitions with examples
**Collaboration Protocols:** Phase authority tables explicitly define PRIMARY/CONSULT/NO
**Output Artifacts:** Clear templates and directory paths specified
**Quality Gates:** Concrete thresholds (≥80% coverage, mypy clean, etc.)

**No medium or low confidence terms:** All extracted terms have clear definitions grounded in agent profile context.

---

## Relationship to Previous Batches

### Batch 1 (Directives) - 99 terms
**Overlap:** Directives referenced by agents (ATDD, TDD, Boy Scout Rule, Spec-Driven Development)
**New Context:** Agent-specific application of directives (who applies when)

### Batch 2 (Approaches) - 129 terms
**Overlap:** Approaches like Language-First Architecture, Spec-Driven Development
**New Context:** Which agents embody which approaches

### Batch 3 (Tactics) - 127 terms
**Overlap:** Phase Checkpoint Protocol, 6-Phase Spec-Driven Implementation Flow
**New Context:** Which agents execute which tactics

### Batch 4 (Agents) - 120 terms
**Unique Focus:** 
- Agent role names and identities (21 new terms)
- Collaboration boundaries and handoff protocols (mostly new)
- Agent-specific output artifacts (AGENT_STATUS, LEX_REPORT, etc.)
- Phase authority assignments (new granularity)
- Specialized capabilities per agent

**Integration Value:** Completes WHO-WHAT-HOW-WHY stack:
- **WHO:** Agents (Batch 4)
- **WHAT:** Directives (Batch 1)
- **HOW:** Tactics (Batch 3)
- **WHY:** Approaches (Batch 2)

---

## Curation Recommendations

### 1. Agent Role Name Consolidation

**Issue:** 21 agent role terms may be verbose for glossary
**Recommendation:** 
- Create single "Agent Roles" glossary entry with table
- Link to individual agent profile files for full details
- Or keep individual entries for discoverability (searchability)

**Decision needed:** Breadth vs. depth trade-off

---

### 2. Phase Authority Integration

**Issue:** Phase 1-6 terms are tightly coupled to Spec-Driven Development
**Recommendation:**
- Group under "Spec-Driven Development Phases" parent term
- Cross-reference to Directive 034 and 6-Phase tactic
- Ensure Phase Checkpoint Protocol is linked

---

### 3. Output Artifact Organization

**Issue:** 22 artifact terms may benefit from categorization
**Recommendation:**
- Group by agent owner (Bootstrap artifacts, Coordination artifacts, etc.)
- Or by purpose (Structural, Planning, Quality, Style, etc.)
- Maintain cross-references between artifacts (AGENT_STATUS ↔ WORKFLOW_LOG ↔ HANDOFFS)

---

### 4. Technology-Specific Term Depth

**Issue:** Python-specific terms (pytest, mypy, ruff, black) may be too implementation-focused
**Recommendation:**
- Keep if Python is primary language in target repos
- Or generalize to "Testing Framework", "Type Checker", "Linter", "Formatter"
- Decision depends on glossary audience (Python devs vs. multi-language teams)

---

### 5. Doctrine Stack Terminology

**Issue:** "Source vs Distribution" and "Export Pipeline" are meta-framework concepts
**Recommendation:**
- Mark as "Framework Meta" or "Doctrine Architecture" category
- Ensure Curator Claire profile is referenced
- Link to distribution architecture ADRs

---

### 6. Review Dimensions Expansion

**Issue:** Four review dimensions could have more detailed definitions
**Recommendation:**
- Expand with concrete checklists from Reviewer agent profile
- Add examples of findings for each dimension
- Link to Review Report template

---

### 7. Collaboration Pattern Terms

**Issue:** "Hand-off Protocol", "Specialization Boundary", "Escalation" are general patterns
**Recommendation:**
- Ensure these connect to Collaboration Contract sections
- Cross-reference between agent profiles showing handoff examples
- Document escalation thresholds (>30% uncertainty rule)

---

## Integration with Living Glossary Practice

### Candidate Status

All 120 terms marked as `status: candidate` ready for curation workflow.

### Enforcement Tier

All terms marked as `enforcement_tier: advisory` (default for initial extraction).

**Curation Phase Should:**
- Promote critical terms to "acknowledgment_required" (e.g., Phase Authority, Core/Local Boundary)
- Consider "hard_failure" for must-not-violate patterns (e.g., editing distribution files directly)

### Ownership Assignment

**Recommended Owners by Category:**
- **Agent Roles:** Framework Guardian (meta-framework)
- **Collaboration Protocols:** Manager Mike (orchestration)
- **Spec-Driven Development:** Analyst Annie + Architect Alphonso + Planning Petra (joint)
- **Quality Gates:** Reviewer (quality assurance)
- **Doctrine Stack:** Curator Claire (architecture)
- **Tech-Specific:** Python Pedro (Python), Java Jenny (Java), etc.

---

## Next Steps

### Immediate (Post-Batch-4)

1. ✅ **Complete extraction:** 120 terms extracted, validated
2. ✅ **Update statistics:** Metadata, confidence distribution
3. ⏳ **Create integration plan:** Batch 1-4 consolidation strategy
4. ⏳ **Commit artifacts:** All YAML and summary files

### Curation Phase (Next)

1. **Deduplication:** Compare 475 total terms (99+129+127+120) across batches
2. **Consolidation:** Merge overlapping definitions with enhanced context
3. **Categorization:** Organize by domain (DDD, Testing, Architecture, Agents, etc.)
4. **Ownership Assignment:** Per bounded context or role
5. **Enforcement Calibration:** Promote critical terms from advisory
6. **Cross-Reference Validation:** Ensure related_terms links are bidirectional
7. **Template Integration:** Verify all artifact terms have templates
8. **IDE Integration:** Prepare for Contextive plugin deployment

---

## Success Criteria Met

✅ **Coverage:** 21/21 agent profiles processed (100%)
✅ **Confidence:** 120/120 high-confidence terms (100%)
✅ **Focus:** Role-specific terminology, collaboration, handoff patterns
✅ **Documentation:** Clear definitions with source citations
✅ **Relationships:** Related terms mapped for navigation
✅ **Integration:** Completes WHO-WHAT-HOW-WHY doctrine stack

**Ready for curation phase.**

---

## File Outputs

- `batch4-agents-candidates.yaml` - 120 candidate glossary entries
- `batch4-agents-extraction-log.md` - Detailed extraction process log
- `batch4-agents-extraction-summary.md` - This comprehensive summary

**Next:** `batch1-4-complete-integration-plan.md` - Consolidation strategy across all four batches

---

**Extraction Status:** ✅ COMPLETE  
**Quality:** ✅ HIGH (100% high-confidence)  
**Ready for:** Curation Phase  
**Batch:** 4 of 4 (FINAL extraction before curation)

---

_Extracted by: Lexical Larry_  
_Date: 2026-02-10_  
_Total Agent Profiles Analyzed: 21_  
_Total Terms Extracted: 120_  
_Confidence Distribution: 120 high, 0 medium, 0 low_
