# Multi-Format Agent Distribution: Architecture Documentation

**Date:** 2026-01-29  
**Status:** Proposed  
**Architect:** Architect Alphonso

---

## Executive Summary

This directory contains formal architectural documentation for the **Multi-Format Agent Framework Distribution Strategy**, which enables the saboteurs agent framework to export to OpenCode, GitHub Copilot Skills, and Model Context Protocol (MCP) formats while preserving its sophisticated governance and multi-agent orchestration capabilities.

**Key Decision:** Build-time generation of platform-specific exports from authoritative markdown source files.

**Strategic Value:**

- +40% addressable users via standards compliance
- 87% faster integration time (<30 minutes vs. 4-8 hours)
- 269% ROI over 3 years
- Reference implementation positioning

**Risk Level:** Low (automated generation, comprehensive validation)

---

## Document Structure

### 1. Formal Technical Assessment

**File:** `formal-technical-assessment.md`  
**Size:** 25 KB (708 lines)

**Purpose:** Comprehensive technical and business analysis of the multi-format distribution initiative.

**Contents:**

- System context and problem statement
- Architecture implications (source-of-truth preservation, governance mapping, orchestration)
- Technical feasibility analysis (export pipeline, schema extraction, CI/CD)
- Governance impact assessment (directive compliance, quality gates)
- Traceability considerations (decision hierarchy, version management)
- Risk analysis (technical, governance, adoption risks)
- Cost-benefit analysis (ROI: 269%, payback <6 months)
- Competitive landscape (market positioning, differentiation)
- Recommendations (proceed with v1.0 implementation)

**Key Findings:**

- ✅ Technically feasible (prototype exists, low complexity)
- ✅ Governance preserved via custom extensions
- ✅ Source-of-truth model prevents drift
- ✅ Strong business case (high ROI, competitive advantage)

---

### 2. Architecture Decision Record

**File:** `ADR-013-multi-format-distribution.md`  
**Size:** 19 KB (564 lines)  
**Status:** Proposed

**Purpose:** Formal decision record following established ADR template (docs/templates/architecture/adr.md).

**Contents:**

- **Context:** Current limitations, forces at play, problem statement
- **Decision:** Multi-format distribution with build-time generation
- **Rationale:** Why multi-format, why build-time, why custom extensions
- **Envisioned Consequences:**
  - Positive: Ecosystem integration (+40% reach), UX improvement (87% faster), competitive positioning
  - Negative: Maintenance overhead (~$1,600/year), schema definition effort (128h initial)
- **Considered Alternatives:** OpenCode-only, platform-native, manual export, dual source-of-truth (all rejected with rationale)
- **Implementation Plan:** 4-phase rollout (schema, pipeline, CI/CD, docs)
- **Success Metrics:** Technical (100% export rate), business (50+ downloads), governance (directive preservation)
- **Compliance:** Directive alignment (006, 007, 018, 020, 021)

**Decision Statement:**

> We will implement a multi-format distribution strategy that generates platform-specific exports (OpenCode, GitHub Copilot Skills, MCP) from authoritative markdown source files at build time.

---

### 3. Technical Design Document

**File:** `tech-design-export-pipeline.md`  
**Size:** 43 KB (1,535 lines)

**Purpose:** Detailed technical design following established template (docs/templates/architecture/technical_design.md).

**Contents:**

- **Overview:** Three-stage pipeline (Parse → Transform → Validate)
- **System Architecture:** Component diagram (PlantUML)
- **Component Design:**
  - Parser: Extract YAML frontmatter + narrative content → Intermediate Representation (IR)
  - OpenCode Generator: IR → discovery.json + definition.yaml with governance extensions
  - Copilot Generator: IR → skill.yaml
  - MCP Generator: IR → server.json
  - Validator: Schema validation + format compliance + hash verification
  - Manifest Generator: Catalog files (manifest.json, tools.json)
- **Data Flow Diagram:** End-to-end pipeline visualization (PlantUML)
- **CI/CD Integration:** GitHub Actions workflow with quality gates
- **Interface Specifications:** JSON schemas for IR, OpenCode, Copilot, MCP
- **Quality Gates:** Unit tests (90%+ coverage), integration tests, validation tests, acceptance tests
- **Deployment Process:** Pre-release checklist, release workflow, distribution channels

**Diagrams:**

1. **Export Pipeline Architecture** (PlantUML component diagram)
2. **Data Flow Diagram** (PlantUML data flow)
3. **CI/CD Integration Workflow** (PlantUML activity diagram)

**Key Technical Decisions:**

- Intermediate Representation (IR) enables format-independent transforms
- Custom extensions preserve governance metadata in standard-compliant way
- Hash verification ensures source-export integrity
- Modular design allows adding new formats without modifying existing exporters

---

## Supporting Analysis

### 4. Framework Alignment Analysis

**File:** `2026-01-29_agentic-framework-alignment.md`  
**Size:** 25 KB

**Summary:** Detailed comparison of saboteurs framework with commercial agentic frameworks (Claude, OpenAI, GitHub Copilot) and standards (OpenCode, MCP). Identifies framework strengths (governance, orchestration) and gaps (discoverability, schemas).

**Key Findings:**

- Framework **exceeds** commercial offerings in governance and multi-agent capabilities
- 70/100 OpenCode alignment score (high compatibility)
- Missing: Machine-readable catalog, input/output schemas, platform-specific formats

---

### 5. Distribution Fit Assessment

**File:** `distribution-release-opencode-fit.md`  
**Size:** 21 KB

**Summary:** OpenCode integration viability assessment with detailed fit matrix (4.1/5 score), implementation roadmap, risk analysis, and cost-benefit breakdown.

**Key Findings:**

- OpenCode highly compatible with existing structure (YAML frontmatter, tools arrays)
- Custom extensions can preserve governance without violating standard
- 1.5 weeks implementation effort (~$6,200 initial cost)
- 269% ROI over 3 years

---

## Implementation Summary

### Timeline

**Total Duration:** 4 weeks (60 hours development + testing)

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| **Week 1: Schema Formalization** | 8h | Schema conventions, top 5 agents |
| **Week 2: Export Pipeline** | 24h | OpenCode, Copilot, MCP exporters + all 16 agents |
| **Week 3: CI/CD Integration** | 8h | GitHub Actions workflow, validation, artifacts |
| **Week 4: Documentation & Release** | 8h | User guides, v1.0.0 packaging |
| **Testing (Concurrent)** | 12h | Unit, integration, acceptance tests |

**Target Release:** v1.0.0 on 2026-02-28

### Resource Requirements

- **Developer:** 60 hours (pipeline, exporters, tests)
- **DevOps:** 8 hours (CI/CD setup)
- **QA:** 12 hours (testing, validation)
- **Technical Writer:** 8 hours (documentation)
- **Total:** ~88 hours (~2.2 weeks FTE)

### Success Criteria

**Technical:**

- ✅ 100% agent export success rate (16/16)
- ✅ 100% schema validation pass
- ✅ Zero manual edits to generated files
- ✅ CI/CD build time <5 minutes

**Business:**

- ✅ Integration time <30 minutes (vs. 4-8 hours baseline)
- ✅ 2+ external tools adopt framework within 6 months
- ✅ 50+ downloads/clones within 3 months
- ✅ Positive community feedback (GitHub stars, issues, PRs)

---

## Dependencies

### Prerequisites

1. **ADR-013 Approval** — Decision record must be accepted before implementation
2. **Resource Allocation** — 88 hours across 4 roles over 4 weeks
3. **JSON Schema Expertise** — Can be acquired during schema formalization phase
4. **External Specs** — OpenCode 1.0, GitHub Copilot Skills, MCP specs (all publicly available)

### Related Directives

| Directive | Impact |
|-----------|--------|
| 006 - Version Governance | ✅ Enhanced by API versioning system |
| 007 - Agent Declaration | ✅ Authority preserved in exports |
| 018 - Traceable Decisions | ✅ ADR documents architectural decision at appropriate level |
| 020 - Lenient Adherence | ✅ Custom extensions enable flexibility |
| 021 - Locality of Change | ✅ Build-time generation minimizes coupling |

### Related ADRs

- **ADR-011:** Primer Execution Matrix (referenced for governance traceability)
- **ADR-012:** Test-First Requirements (ATDD/TDD preserved in exports)

---

## Next Steps

### Immediate Actions (Pending Approval)

1. **Technical Lead Review** — Review formal technical assessment and ADR-013
2. **Product Owner Approval** — Validate business case and strategic fit
3. **Governance Board Decision** — Approve/reject/defer ADR-013

**Target Decision Date:** 2026-02-05

### Post-Approval Actions

1. **Kickoff Meeting** — Align team on timeline and deliverables
2. **Resource Allocation** — Assign developer, DevOps, QA, technical writer
3. **Phase 1 Start** — Begin schema formalization (2026-02-07)
4. **Weekly Checkpoints** — Monitor progress, resolve blockers

---

## Risk Mitigation

### Low-Risk Items

| Risk | Mitigation |
|------|------------|
| Format specs change | Version-pinned exports; update scripts when needed |
| Generated files drift | CI/CD automation; hash verification; read-only dist/ |
| Export validation fails | Comprehensive test suite; format validators; pre-commit hooks |

### Medium-Risk Items

| Risk | Mitigation |
|------|------------|
| Schema extraction complex | Incremental rollout; top 5 agents first; community review |
| External tools don't support extensions | Standard fields remain usable; documentation highlights capabilities |

**Overall Risk Level:** ⚠️ **LOW** — Automated approach, validation gates, proven patterns

---

## Quality Assurance

### Documentation Standards

All documents follow:

- **Directive 018:** Documentation Level Framework (stable vs. volatile)
- **Markdown Linting:** Consistent formatting and structure
- **Cross-Referencing:** Clear document relationships and dependencies
- **Versioning:** Semantic versioning (MAJOR.MINOR.PATCH)

### Review Process

- ✅ Architect review (Alphonso) — Complete
- ⏳ Technical Lead review — Pending
- ⏳ Product Owner review — Pending
- ⏳ Governance Board approval — Pending

---

## References

### Internal Documents

- `.github/agents/*.agent.md` — Agent profile source files
- `.github/agents/directives/` — Governance directive system
- `docs/templates/architecture/adr.md` — ADR template
- `docs/templates/architecture/technical_design.md` — Technical design template
- `tools/opencode-exporter.js` — Prototype exporter (working implementation)

### External Standards

- **OpenCode Specification:** <https://opencode.ai/docs/specification/1.0/>
- **GitHub Copilot Skills:** <https://docs.github.com/copilot/customizing-copilot>
- **Model Context Protocol:** <https://modelcontextprotocol.io/specification>
- **JSON Schema Draft 7:** <https://json-schema.org/draft-07/schema>

### Prior Art

- **LangChain Agents:** Multi-agent orchestration patterns
- **AutoGPT Framework:** Agent capability declarations
- **Semantic Kernel:** Skills-based agent definitions

---

## Appendices

### Appendix A: Document Metrics

| Document | Size | Lines | Diagrams | Schemas |
|----------|------|-------|----------|---------|
| Formal Technical Assessment | 25 KB | 708 | 0 | 0 |
| ADR-013 | 19 KB | 564 | 0 | 0 |
| Technical Design | 43 KB | 1,535 | 3 PlantUML | 2 JSON Schema |
| **Total** | **87 KB** | **2,807** | **3** | **2** |

### Appendix B: Compliance Matrix

| Requirement | Document | Section | Status |
|-------------|----------|---------|--------|
| System Context | FTA | Section 1 | ✅ Complete |
| Architecture Implications | FTA | Section 2 | ✅ Complete |
| Technical Feasibility | FTA | Section 3 | ✅ Complete |
| Governance Impact | FTA | Section 4 | ✅ Complete |
| Traceability | FTA | Section 5 | ✅ Complete |
| ADR Context | ADR-013 | Context | ✅ Complete |
| ADR Decision | ADR-013 | Decision | ✅ Complete |
| ADR Rationale | ADR-013 | Rationale | ✅ Complete |
| ADR Consequences | ADR-013 | Consequences | ✅ Complete |
| ADR Alternatives | ADR-013 | Alternatives | ✅ Complete |
| System Design | Tech Design | Design | ✅ Complete |
| Component Design | Tech Design | Components | ✅ Complete |
| Data Flow | Tech Design | Diagrams | ✅ Complete |
| Interface Specs | Tech Design | Interfaces | ✅ Complete |
| Quality Gates | Tech Design | Testing | ✅ Complete |
| Deployment | Tech Design | Deployment | ✅ Complete |

### Appendix C: Glossary

- **ADR:** Architecture Decision Record — Formal decision documentation
- **API Version:** Input/output contract version (separate from agent version)
- **Custom Extensions:** Format-specific metadata fields preserving framework capabilities
- **Governance Framework:** Directive system defining collaboration, quality, orchestration
- **Intermediate Representation (IR):** Format-independent agent metadata structure
- **MCP:** Model Context Protocol — Open standard for agent-to-tool communication
- **Multi-Agent Orchestration:** Explicit coordination patterns for multiple agents
- **OpenCode:** Open standard for agent interoperability via discovery files
- **Source-of-Truth:** Authoritative data representation (markdown files)
- **Build-Time Generation:** Automated export creation during CI/CD (never manual)

---

**Document Version:** 1.0.0  
**Date:** 2026-01-29  
**Status:** Documentation Complete — Awaiting ADR-013 Approval  
**Next Review:** Post-implementation (2026-03-29)
