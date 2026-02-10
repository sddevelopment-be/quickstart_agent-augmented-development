# Glossary Integration Plan: Batches 1-4 Complete

**Date:** 2026-02-10  
**Agent:** Lexical Larry  
**Purpose:** Consolidate and curate terminology from all four extraction batches  
**Status:** Ready for curation phase

---

## Executive Summary

Completed extraction of **475 candidate terms** across four systematic batches covering the complete doctrine framework. Ready for deduplication, consolidation, and living glossary integration.

### Extraction Results

| Batch | Source | Terms | High % | Focus |
|-------|--------|-------|--------|-------|
| **1** | Directives (32) | 99 | 75% | Rules, constraints, policies |
| **2** | Approaches (18) | 129 | 69% | Mental models, philosophies |
| **3** | Tactics (2) | 127 | 75% | Procedural workflows |
| **4** | Agents (21) | 120 | 100% | Roles, collaboration, handoffs |
| **TOTAL** | **73 files** | **475** | **79%** | **Complete doctrine stack** |

### Quality Metrics

- **Average Confidence:** 79% high-confidence
- **Source Coverage:** 100% of doctrine framework
- **Documentation:** 4 comprehensive summaries + 1 integration plan
- **Readiness:** All batches validated and committed

---

## Batch Overview

### Batch 1: Directives (99 terms, 75% high-confidence)

**Source:** 32 directive files in `doctrine/directives/`

**Key Categories:**
- Framework operations (bootstrap, tooling, versioning)
- Development practices (ATDD, TDD, bug-fixing)
- Context management (token discipline, external memory)
- Quality gates (test coverage, Boy Scout Rule)
- Documentation standards (ADRs, traceable decisions)

**Strengths:**
- Clear rule-based definitions
- Explicit enforcement mechanisms
- Well-established patterns

**Integration Needs:**
- Link to tactics that implement directives
- Cross-reference with agents who enforce directives
- Consolidate overlapping quality concepts

---

### Batch 2: Approaches (129 terms, 69% high-confidence)

**Source:** 18 approach files in `doctrine/approaches/`

**Key Categories:**
- DDD concepts (Ubiquitous Language, Bounded Context, Context Map)
- Glossary practices (Living Glossary, Terminology Extraction)
- Development philosophies (Language-First Architecture, Spec-Driven Development)
- Governance models (Human in Charge, Enforcement Tiers)

**Strengths:**
- Rich conceptual definitions
- Clear rationale and trade-offs
- Strategic framing

**Integration Needs:**
- Distinguish DDD core terms from framework-specific usage
- Merge Living Glossary Practice terms with Batch 3 tactics
- Reconcile terminology variants across approaches

---

### Batch 3: Tactics (127 terms, 75% high-confidence)

**Source:** 2 tactic files in `doctrine/tactics/`

**Key Categories:**
- Workflow procedures (6-Phase Spec-Driven Implementation, Phase Checkpoint Protocol)
- Glossary maintenance (extraction, triage, quarterly reviews)
- Quality processes (staleness audit, coverage assessment)

**Strengths:**
- Actionable step-by-step definitions
- Clear procedural guidance
- Time estimates and checklists

**Integration Needs:**
- Merge with Batch 2 (Living Glossary Practice approach)
- Link to Batch 4 agents who execute tactics
- Consolidate workflow terminology

---

### Batch 4: Agents (120 terms, 100% high-confidence)

**Source:** 21 agent profile files in `doctrine/agents/`

**Key Categories:**
- Agent roles (21 agents with specializations)
- Collaboration protocols (handoff, phase authority)
- Output artifacts (REPO_MAP, LEX_REPORT, AGENT_STATUS, etc.)
- Quality gates (self-review, coverage, type checking)
- Specialized capabilities (drift detection, voice fidelity)

**Strengths:**
- 100% high-confidence (clearest definitions)
- Complete WHO coverage (all agents documented)
- Rich collaboration boundary definitions

**Integration Needs:**
- Decide agent role entry strategy (individual vs. consolidated table)
- Link artifacts to producing agents
- Consolidate overlapping quality concepts across agents

---

## Integration Strategy

### Phase 1: Deduplication (Week 1)

**Goal:** Identify and merge overlapping terms across batches

#### 1.1 Known Overlaps

**High-Frequency Terms (appear in multiple batches):**

| Term | Batch 1 | Batch 2 | Batch 3 | Batch 4 | Integration Strategy |
|------|---------|---------|---------|---------|---------------------|
| **Specification** | ✓ (Directive 034) | ✓ (Spec-Driven Dev) | ✓ (Phase 1 output) | ✓ (Analyst Annie) | Merge: Canonical definition with phase-specific details |
| **ADR** | ✓ (Directive 018) | - | - | ✓ (Architect Alphonso) | Merge: Core definition + architect context |
| **ATDD** | ✓ (Directive 016) | - | - | ✓ (Dev agents) | Merge: Directive + agent application |
| **TDD** | ✓ (Directive 017) | - | - | ✓ (Dev agents) | Merge: Directive + agent application |
| **Living Glossary** | - | ✓ (Approach) | ✓ (Tactic) | - | Merge: Philosophy + procedures |
| **Bounded Context** | - | ✓ (DDD Core) | ✓ (Context discovery) | - | Merge: Theory + practical application |
| **Phase Checkpoint Protocol** | ✓ (Directive 034 ref) | - | ✓ (Tactic) | ✓ (Agent handoffs) | Merge: Procedure + agent execution |
| **Boy Scout Rule** | ✓ (Directive 036) | - | - | ✓ (Coding agents) | Merge: Rule + agent enforcement |
| **Work Log** | ✓ (Directive 014) | - | - | ✓ (All agents) | Merge: Standard + agent-specific usage |

**Deduplication Process:**
1. Create master term list with source batch tags
2. Group by semantic similarity (exact matches, synonyms, variants)
3. Select canonical definition (highest confidence + clearest context)
4. Enhance with batch-specific details as "Usage in [context]" sections
5. Preserve all related_terms from all sources

**Output:** `deduplication-report.md` with merge decisions

---

### Phase 2: Categorization (Week 1-2)

**Goal:** Organize terms into semantic domains for glossary navigation

#### 2.1 Proposed Category Structure

**1. Core Framework Concepts**
- Agent roles and capabilities (Batch 4)
- Directive types and enforcement (Batch 1)
- Approach philosophies (Batch 2)
- Tactic procedures (Batch 3)
- Doctrine Stack layers (Batch 4 - Curator context)

**2. Domain-Driven Design (DDD)**
- Ubiquitous Language (Batch 2)
- Bounded Context (Batch 2, 3)
- Context Map (Batch 2)
- Linguistic patterns (Batch 2)
- Aggregate, Entity, Value Object (Batch 2)

**3. Development Practices**
- ATDD, TDD (Batch 1, 4)
- Spec-Driven Development (Batch 1, 2, 3, 4)
- Boy Scout Rule (Batch 1, 4)
- Bug Fixing Techniques (Batch 1, 4)
- RED-GREEN-REFACTOR (Batch 4)

**4. Collaboration & Orchestration**
- Hand-off Protocol (Batch 4)
- Phase Authority (Batch 4)
- Agent Assignment (Batch 4)
- File-Based Orchestration (Batch 1, 4)
- Manager Mike artifacts (Batch 4)

**5. Quality & Testing**
- Coverage Threshold (Batch 4)
- Self-Review Protocol (Batch 4)
- Review Dimensions (Batch 4)
- Test Pyramid (Batch 1)
- Acceptance Criteria (Batch 1, 4)

**6. Artifacts & Outputs**
- Specification (Batch 1, 2, 3, 4)
- ADR (Batch 1, 4)
- Work Log (Batch 1, 4)
- REPO_MAP, SURFACES, WORKFLOWS (Batch 4)
- LEX_REPORT, AGENT_STATUS, Review Report (Batch 4)

**7. Glossary Practice**
- Living Glossary (Batch 2, 3)
- Terminology Extraction (Batch 2, 3)
- Maintenance Rhythm (Batch 2, 3)
- Enforcement Tiers (Batch 2)
- Ownership Model (Batch 2)

**8. Framework Maintenance**
- Drift Detection (Batch 4)
- Framework Integrity (Batch 4)
- Core/Local Boundary (Batch 4)
- Manifest (Batch 4)
- Upgrade Plan (Batch 4)

**9. Content Quality**
- Voice Fidelity (Batch 4)
- Tonal Integrity (Batch 4)
- Authorial Voice (Batch 4)
- Style Compliance (Batch 4)
- Medium Detection (Batch 4)

**10. Repository & Workspace**
- workspace_root, doc_root, spec_root, output_root (Batch 4)
- Topology Mapping (Batch 4)
- Repository Scaffolding (Batch 4)
- Doctrine Configuration (Batch 4)

**11. Technology-Specific**
- Python: pytest, mypy, ruff, black, Type Hints (Batch 4)
- Java: Maven, JVM Ecosystem (Batch 4)
- Frontend: UI Architecture, Component Patterns (Batch 4)
- Backend: Service Design, API Contract (Batch 4)

**Output:** `category-assignments.yaml` mapping terms to categories

---

### Phase 3: Ownership Assignment (Week 2)

**Goal:** Designate context owners per Living Glossary Practice

#### 3.1 Ownership by Category

| Category | Owner Agent | Rationale |
|----------|-------------|-----------|
| **Core Framework** | Framework Guardian | Meta-framework responsibility |
| **DDD Concepts** | Architect Alphonso | Strategic architecture authority |
| **Development Practices** | Python Pedro / Java Jenny | Language specialists enforce practices |
| **Collaboration** | Manager Mike | Orchestration authority |
| **Quality & Testing** | Reviewer | Quality assurance specialist |
| **Artifacts** | Producing agent | Each artifact owned by creator |
| **Glossary Practice** | Curator Claire | Maintains glossary as artifact |
| **Framework Maintenance** | Framework Guardian | Framework integrity authority |
| **Content Quality** | Lexical Larry / Curator Claire | Joint style/structure authority |
| **Repository** | Bootstrap Bill | Repository scaffolding authority |
| **Tech-Specific** | Language specialist | Python Pedro, Java Jenny, etc. |

#### 3.2 Cross-Context Terms

**Terms requiring joint ownership:**
- **Specification:** Analyst Annie (author) + Architect Alphonso (approver) + Planning Petra (planner)
- **Phase Checkpoint Protocol:** All agents participating in Spec-Driven Development
- **Living Glossary:** Curator Claire (maintainer) + All agents (contributors)

**Decision Protocol:**
- Single owner for canonical definition
- Consulted owners for context-specific usage
- Escalation path for conflicts

**Output:** `ownership-assignments.yaml` with owner + consulted fields

---

### Phase 4: Enforcement Calibration (Week 2)

**Goal:** Promote critical terms from advisory to higher tiers

#### 4.1 Enforcement Tier Criteria

**Hard Failure (Rare - must-not-violate):**
- Editing distribution files directly (Source vs Distribution)
- Skipping Bootstrap Protocol
- Operating outside Phase Authority
- Violating Core/Local Boundary

**Acknowledgment Required (Warnings):**
- Using deprecated terms
- Cross-context term usage (different meanings)
- Skipping Boy Scout Rule
- Missing test coverage threshold

**Advisory (Default - suggestions):**
- Style preferences
- Naming conventions
- Documentation structure
- New terminology

#### 4.2 Promotion Candidates

**Recommend Hard Failure:**
1. **Source vs Distribution** - Critical architecture rule
2. **Bootstrap Protocol** - Mandatory initialization
3. **Phase Authority violation** - Prevents rework
4. **Core/Local Boundary** - Prevents silent overwrites

**Recommend Acknowledgment Required:**
1. **Boy Scout Rule** - Quality gate
2. **Coverage Threshold** - Quality gate
3. **Phase Checkpoint Protocol** - Workflow gate
4. **Hand-off Protocol** - Collaboration gate
5. **ATDD/TDD requirement** - Development gate

**Output:** `enforcement-calibration.yaml` with tier promotions + rationale

---

### Phase 5: Cross-Reference Validation (Week 3)

**Goal:** Ensure bidirectional links between related terms

#### 5.1 Relationship Types

**1. Hierarchical (Parent-Child):**
- Spec-Driven Development → Phase 1, Phase 2, Phase 3, Phase 4, Phase 5, Phase 6
- Living Glossary Practice → Terminology Extraction, Glossary Maintenance Workflow
- Review → Structural Review, Editorial Review, Technical Review, Standards Compliance

**2. Sequential (Workflow):**
- Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6
- Candidate → Canonical → Deprecated → Superseded (Glossary lifecycle)
- Analysis → Architecture → Planning → Implementation → Review

**3. Agent-Artifact (Producer-Product):**
- Analyst Annie → Specification, Validation Script
- Architect Alphonso → ADR, System Decomposition
- Bootstrap Bill → REPO_MAP, SURFACES, WORKFLOWS
- Lexical Larry → LEX_REPORT, LEX_DELTAS, LEX_TONE_MAP

**4. Directive-Tactic (Invokes):**
- Directive 034 → Phase Checkpoint Protocol, 6-Phase Spec-Driven Implementation Flow
- Directive 016 → ATDD workflows
- Directive 017 → TDD cycles
- Living Glossary Practice → Terminology Extraction, Glossary Maintenance Workflow

**5. Agent-Directive (Applies):**
- Python Pedro → Directive 016 (ATDD), Directive 017 (TDD), Directive 036 (Boy Scout)
- Framework Guardian → Directive 025 (Framework Guardian), Directive 021 (Locality of Change)
- All agents → Directive 014 (Work Log), Directive 007 (Agent Declaration)

#### 5.2 Validation Process

1. Extract all related_terms fields from 475 entries
2. Check bidirectional links (if A → B, then B → A)
3. Identify missing reverse links
4. Add missing cross-references
5. Verify link targets exist in glossary

**Output:** `cross-reference-validation-report.md` + corrected YAML

---

### Phase 6: Template Integration (Week 3)

**Goal:** Verify artifact terms have corresponding templates

#### 6.1 Artifact-Template Mapping

**Required Mappings:**

| Artifact Term | Template Location | Owner Agent |
|--------------|-------------------|-------------|
| Specification | templates/specifications/ | Analyst Annie |
| ADR | templates/architecture/ADR-template.md | Architect Alphonso |
| Work Log | templates/work-log-template.md | All agents |
| REPO_MAP | (Generated by Bootstrap Bill) | Bootstrap Bill |
| AGENT_STATUS | templates/orchestration/AGENT_STATUS.md | Manager Mike |
| Review Report | templates/qa/review-report-template.md | Reviewer |
| LEX_REPORT | templates/lexical/LEX_REPORT.md | Lexical Larry |
| Audit Report | templates/GUARDIAN_AUDIT_REPORT.md | Framework Guardian |
| Upgrade Plan | templates/GUARDIAN_UPGRADE_PLAN.md | Framework Guardian |

**Validation:**
1. Check each artifact term has template field
2. Verify template path exists
3. Document generation logic for dynamic artifacts
4. Link to example outputs

**Output:** `artifact-template-map.yaml`

---

### Phase 7: Contextive Integration (Week 4)

**Goal:** Prepare glossary for IDE integration via Contextive plugin

#### 7.1 Contextive Format Requirements

**Target Format:** `.contextive/contexts/[domain].yml`

**Required Fields (per term):**
```yaml
contexts:
  - name: "Domain Name"
    terms:
      - term: "Term Name"
        definition: "Clear, concise definition (1-2 sentences)"
```

**Optional Fields:**
- `aliases: []` - Alternative names
- `examples: []` - Usage examples
- `related: []` - Cross-references

#### 7.2 Domain Splits for IDE

**Proposed Contextive Contexts:**

1. **doctrine-core.yml** - Framework fundamentals (Directive, Approach, Tactic, Agent)
2. **ddd.yml** - DDD concepts (Ubiquitous Language, Bounded Context, Context Map)
3. **development.yml** - Dev practices (ATDD, TDD, Boy Scout Rule, RED-GREEN-REFACTOR)
4. **agents.yml** - Agent roles and capabilities
5. **orchestration.yml** - Collaboration patterns (Hand-off Protocol, Phase Authority)
6. **quality.yml** - Quality gates and testing
7. **artifacts.yml** - Output products and templates
8. **glossary-practice.yml** - Living Glossary terminology

**Rationale:** Context-specific term loading reduces IDE noise, shows relevant terms for current work

#### 7.3 Transformation Process

1. Group terms by target context
2. Simplify definitions (remove YAML metadata)
3. Add code-adjacent examples where applicable
4. Generate 8 Contextive YAML files
5. Test with Contextive VSCode plugin

**Output:** `.contextive/contexts/*.yml` (8 files)

---

### Phase 8: Documentation & Rollout (Week 4)

**Goal:** Prepare glossary for team adoption

#### 8.1 Documentation Artifacts

**1. Master Glossary (doctrine/GLOSSARY.md)**
- Curated, consolidated entries from all batches
- Organized by category with TOC
- Bidirectional cross-references
- Owner and enforcement tier visible

**2. Glossary Usage Guide (docs/guides/using-glossary.md)**
- How to search and navigate
- IDE integration setup (Contextive)
- Contributing new terms
- Term lifecycle (candidate → canonical → deprecated)

**3. Maintenance Runbook (docs/processes/glossary-maintenance.md)**
- Weekly triage process
- Quarterly health check
- Annual governance retrospective
- Metrics and dashboards

**4. Change Log (doctrine/GLOSSARY_CHANGELOG.md)**
- Version history
- Batch integration milestones
- Major term additions/deprecations
- Ownership changes

#### 8.2 Rollout Plan

**Week 1-2: Soft Launch (Internal)**
- Share with agent maintainers
- Collect feedback on categorization
- Validate ownership assignments
- Test Contextive integration

**Week 3-4: Team Onboarding**
- Announce glossary availability
- Conduct IDE plugin training
- Demonstrate navigation and search
- Establish contribution process

**Week 5+: Continuous Maintenance**
- Weekly triage (30 min)
- Monthly metrics review
- Quarterly health check (2 hours)
- Annual governance retrospective

---

## Consolidation Priorities

### Must-Do (Blocking)

1. ✅ **Batch 4 extraction complete** - 120 terms validated
2. ⏳ **Deduplication** - Merge overlapping terms across batches
3. ⏳ **Categorization** - Organize 475 terms into 11 semantic domains
4. ⏳ **Ownership assignment** - Designate owners per Living Glossary Practice
5. ⏳ **Cross-reference validation** - Ensure bidirectional links
6. ⏳ **Master glossary creation** - Single source of truth in doctrine/GLOSSARY.md

### Should-Do (High Value)

7. ⏳ **Enforcement calibration** - Promote critical terms from advisory
8. ⏳ **Template integration** - Link artifacts to templates
9. ⏳ **Contextive integration** - Prepare for IDE plugin
10. ⏳ **Usage guide** - Documentation for team adoption

### Nice-to-Have (Future Enhancement)

11. Glossary dashboard (term count, staleness metrics)
12. PR-level validation (terminology checks in CI)
13. Automated term extraction from new docs
14. Glossary-spec alignment validation

---

## Success Metrics

### Coverage Metrics
- ✅ **Doctrine framework coverage:** 100% (73/73 files processed)
- ⏳ **Deduplication rate:** Target <10% overlap after merge
- ⏳ **Category coverage:** All terms assigned to categories
- ⏳ **Ownership coverage:** 100% of terms have owners

### Quality Metrics
- ✅ **Average confidence:** 79% high (exceeds 75% target)
- ✅ **Definition clarity:** All terms have context-grounded definitions
- ⏳ **Cross-reference completeness:** Target 100% bidirectional
- ⏳ **Template linkage:** Target 100% for artifact terms

### Adoption Metrics
- ⏳ **IDE integration:** Contextive plugin configured
- ⏳ **Team awareness:** Usage guide published
- ⏳ **Contribution rate:** Target >5 updates/quarter
- ⏳ **Maintenance cadence:** Weekly triage established

### Sentiment Metrics
- ⏳ **Agent maintainer feedback:** "Glossary is helpful" (Target >75%)
- ⏳ **Suppression patterns:** <10% PRs override checks
- ⏳ **Search usage:** Glossary referenced in PRs/issues

---

## Risk Mitigation

### Risk 1: Deduplication Complexity
**Symptom:** 475 terms with potential overlaps create merge conflicts
**Mitigation:** 
- Systematic comparison using term similarity scoring
- Canonical definition selection criteria (highest confidence + clearest context)
- Preserve all source contexts as "Usage in [domain]" sections
- Document merge decisions for traceability

### Risk 2: Maintenance Burden
**Symptom:** 475-term glossary becomes stale without continuous care
**Mitigation:**
- Mandatory ownership per category (Living Glossary Practice)
- Automated weekly triage process (30 min)
- Quarterly health checks (2 hours)
- Metrics dashboard for staleness detection

### Risk 3: Over-Engineering
**Symptom:** Glossary becomes compliance regime instead of shared understanding
**Mitigation:**
- Default all terms to advisory enforcement tier
- Only promote to acknowledgment/hard-failure with explicit justification
- Human-in-charge governance (not human-in-the-loop)
- Regular retrospectives to adjust enforcement

### Risk 4: Adoption Resistance
**Symptom:** Team ignores glossary, continues ad-hoc terminology
**Mitigation:**
- IDE integration reduces friction (Contextive plugin)
- Usage guide makes navigation easy
- Lightweight contribution process
- Celebrate glossary usage in PRs

### Risk 5: Tool-Specific Lock-In
**Symptom:** Glossary format tightly coupled to Contextive
**Mitigation:**
- Maintain doctrine/GLOSSARY.md as canonical source (tool-agnostic)
- .contextive/ is distribution artifact (like .github/ for Copilot)
- Export pipeline generates tool-specific formats
- Can regenerate for different IDE plugins

---

## Timeline

### Week 1: Deduplication & Categorization
- Days 1-2: Deduplication analysis and merge decisions
- Days 3-4: Category structure finalization
- Day 5: Category assignments and validation

### Week 2: Ownership & Enforcement
- Days 1-2: Ownership assignments per Living Glossary Practice
- Days 3-4: Enforcement tier calibration
- Day 5: Validation and conflict resolution

### Week 3: Validation & Integration
- Days 1-2: Cross-reference validation and correction
- Days 3-4: Artifact-template mapping
- Day 5: Contextive format generation

### Week 4: Documentation & Rollout
- Days 1-2: Master glossary creation (doctrine/GLOSSARY.md)
- Days 3-4: Usage guide and maintenance runbook
- Day 5: Soft launch and feedback collection

### Week 5+: Continuous Maintenance
- Weekly triage (30 min)
- Monthly metrics review
- Quarterly health check (2 hours)

**Total Effort:** 4 weeks curation + ongoing maintenance

---

## Deliverables

### Immediate (Post-Batch-4)
- ✅ batch4-agents-candidates.yaml (120 terms)
- ✅ batch4-agents-extraction-summary.md
- ✅ batch1-4-complete-integration-plan.md (this document)

### Curation Phase (Weeks 1-4)
- ⏳ deduplication-report.md (merge decisions)
- ⏳ category-assignments.yaml (term categorization)
- ⏳ ownership-assignments.yaml (owner designations)
- ⏳ enforcement-calibration.yaml (tier promotions)
- ⏳ cross-reference-validation-report.md (bidirectional links)
- ⏳ artifact-template-map.yaml (template linkage)
- ⏳ .contextive/contexts/*.yml (8 IDE integration files)
- ⏳ doctrine/GLOSSARY.md (master glossary)
- ⏳ docs/guides/using-glossary.md (usage guide)
- ⏳ docs/processes/glossary-maintenance.md (runbook)
- ⏳ doctrine/GLOSSARY_CHANGELOG.md (version history)

### Ongoing (Week 5+)
- Weekly triage reports
- Monthly metrics dashboards
- Quarterly health check reports
- Annual governance retrospectives

---

## Conclusion

**Extraction Complete:** All four batches finished with 475 candidate terms covering the complete doctrine framework.

**Next Phase:** Curation and consolidation following Living Glossary Practice approach.

**Success Criteria:**
- ✅ Complete coverage (73/73 files, 100%)
- ✅ High quality (79% high-confidence average)
- ✅ Clear relationships (related terms mapped)
- ✅ Integration plan documented

**Ready to proceed:** Deduplication → Categorization → Ownership → Integration → Rollout

---

**Plan Status:** ✅ COMPLETE  
**Extraction Status:** ✅ COMPLETE (4/4 batches)  
**Curation Status:** ⏳ READY TO BEGIN  
**Target Completion:** 4 weeks (Weeks 1-4)

---

_Created by: Lexical Larry_  
_Date: 2026-02-10_  
_Total Terms: 475 (99+129+127+120)_  
_Average Confidence: 79% high_  
_Source Files: 73 (32 directives + 18 approaches + 2 tactics + 21 agents)_
