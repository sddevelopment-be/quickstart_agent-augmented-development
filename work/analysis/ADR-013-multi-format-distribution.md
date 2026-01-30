# ADR-013: Multi-Format Agent Framework Distribution Strategy

**status**: `Proposed`  
**date**: 2026-01-29  
**author**: Architect Alphonso  
**related documents**: `work/analysis/formal-technical-assessment.md`, `work/analysis/tech-design-export-pipeline.md`

---

## Context

### Current State

The saboteurs repository implements a sophisticated multi-agent framework with 16 specialized agents, 24 governance directives, and explicit multi-agent orchestration capabilities. Agent profiles are defined as structured markdown files (`.github/agents/*.agent.md`) with YAML frontmatter containing metadata (name, tools, directives, specialization).

**Framework Strengths:**

- **Governance-first design** with priority hierarchies, traceable decisions, and risk escalation
- **Multi-agent orchestration** via file-based collaboration and explicit handoff protocols
- **Quality embedded** through test-first requirements (ATDD/TDD), locality of change principles, and audience-aware documentation
- **Extensible directive system** for cross-cutting concerns and collaboration contracts

**Current Limitations:**

1. **Discoverability Gap:** No machine-readable catalog; tools cannot auto-detect agent capabilities
2. **Platform Fragmentation:** Manual integration required for each platform (Claude, OpenAI, GitHub Copilot)
3. **Integration Barrier:** High setup cost (4-8 hours) for users unfamiliar with file-based structure
4. **Distribution Constraint:** No standard packaging format limits adoption beyond internal use

### Forces at Play

**Technical Forces:**

- **Emerging Standards:** OpenCode, Model Context Protocol (MCP), GitHub Copilot Skills provide interoperability
- **Platform Lock-in Risk:** Proprietary formats (OpenAI, Claude) create vendor dependency
- **Automation Demand:** CI/CD pipelines require machine-readable specifications
- **Schema Validation:** JSON Schema provides contract enforcement and breaking change detection

**Business Forces:**

- **Market Positioning:** Reference implementation potential for enterprise multi-agent systems
- **Ecosystem Reach:** Standards compliance enables discovery by diverse tools/platforms
- **Competitive Pressure:** Commercial frameworks (Claude, OpenAI) have native platform integration
- **Community Contribution:** Open standards adoption builds credibility and influence

**Governance Forces:**

- **Source-of-Truth Preservation:** Markdown files contain rich narrative context essential for governance
- **Directive Compliance:** Directive 018 (Traceable Decisions) requires architectural decision documentation
- **Quality Gates:** Directive 016 (ATDD) and 017 (TDD) must be preserved in exports
- **Version Governance:** Directive 006 requires explicit versioning and compatibility tracking

### Problem Statement

**How do we enable broader ecosystem integration and reduce user integration friction while preserving the framework's governance sophistication and multi-agent orchestration capabilities?**

---

## Decision

**We will implement a multi-format distribution strategy that generates platform-specific exports from authoritative markdown source files at build time.**

### Scope

**Included Formats:**

1. **OpenCode** (`.opencode.json`, `.definition.yaml`)
   - Discovery files for agent capabilities
   - Definition files for input/output schemas
   - Tool registry and manifest
   - Primary distribution format (broadest compatibility)

2. **GitHub Copilot Skills** (`.yaml`)
   - Copilot-native skill definitions
   - Examples and metadata
   - Secondary format (largest current user base)

3. **Model Context Protocol** (`.json`)
   - MCP server definitions
   - Tool and resource specifications
   - Tertiary format (future-focused)

**Export Mechanisms:**

- **Build-time Generation:** CI/CD pipeline automatically generates all formats on commit
- **Source-of-Truth:** Markdown files (`.github/agents/*.agent.md`) remain authoritative
- **Custom Extensions:** Format-specific extensions preserve governance metadata
- **Validation Gates:** Exports validated against format specifications and source integrity

**Distribution Channels:**

- **GitHub Releases:** Tagged versions with all export formats (ZIP/TAR)
- **npm Package:** `@saboteurs/agents-framework` for JavaScript ecosystem
- **Docker Image:** Container with conversion tools and generated exports
- **Documentation Site:** Web-based discovery and download portal

---

## Rationale

### Why Multi-Format Over Single Format

**Alternative Considered:** Adopt single standard (e.g., OpenCode only)

**Rejected Because:**

- Different ecosystems have different adoption curves (Copilot = mature, MCP = emerging)
- Platform-specific optimizations (Copilot's native integration, OpenCode's breadth)
- Hedge against format obsolescence (diversification reduces risk)
- Low marginal cost of additional formats once pipeline exists

**Trade-off Accepted:** Increased maintenance surface area (3 formats vs. 1) in exchange for maximum ecosystem reach and format independence.

### Why Build-Time Generation Over Manual Maintenance

**Alternative Considered:** Manually maintain parallel formats

**Rejected Because:**

- High drift risk (updates to markdown not propagated to exports)
- Double maintenance burden (3x work for each agent change)
- Human error in format compliance
- No validation enforcement

**Alternative Considered:** Make exports the source-of-truth

**Rejected Because:**

- Loss of narrative context essential for governance understanding
- Reduced human readability (JSON/YAML less comprehensible than markdown prose)
- Breaks existing workflows (agents currently authored in markdown)
- Difficult to express directive relationships and collaboration contracts in structured formats

**Selected Approach Benefits:**

- ✅ Single source-of-truth (markdown) eliminates drift
- ✅ Automated generation reduces manual burden
- ✅ CI/CD validation catches errors early
- ✅ Reproducible builds from source commit
- ✅ Generated files gitignored (only in release artifacts)

### Why Custom Extensions Over Format Limitations

**Challenge:** OpenCode and similar standards lack native governance constructs.

**Alternative Considered:** Omit governance metadata from exports

**Rejected Because:**

- Loss of framework's key differentiator
- Custom tooling cannot leverage governance rules
- Users unaware of directive system benefits
- Positioned as "basic" framework instead of "enterprise-grade"

**Selected Approach:**

Use format-specific custom extensions to preserve governance context:

```json
{
  "opencode_version": "1.0",
  "agent": {
    "id": "architect-alphonso",
    "extensions": {
      "saboteurs_governance": {
        "directives": [...],
        "uncertainty_threshold": 0.3,
        "escalation_required": true
      }
    }
  }
}
```

**Benefits:**

- ✅ Standard-compliant (extensions allowed by specs)
- ✅ Backward compatible (standard tools ignore unknown fields)
- ✅ Forward compatible (custom tools can leverage governance)
- ✅ Framework uniqueness preserved and discoverable

---

## Envisioned Consequences

### Positive Consequences

**Ecosystem Integration (High Impact)**

- ✅ Agents discoverable by OpenCode-compatible tools
- ✅ Native integration with GitHub Copilot
- ✅ MCP support enables future platform adoption
- ✅ Standards compliance builds credibility

**Measurable Benefit:** +40% addressable users via standards compliance

**User Experience Improvement (High Impact)**

- ✅ Integration time reduced from 4-8 hours to <30 minutes
- ✅ Clear schema-based contracts reduce ambiguity
- ✅ Examples and metadata provide self-service onboarding
- ✅ Multiple format options suit different workflows

**Measurable Benefit:** 87% faster onboarding time

**Competitive Positioning (Medium Impact)**

- ✅ "Universal agent framework" positioning
- ✅ Reference implementation for enterprise patterns
- ✅ Contribution to emerging standards (OpenCode, MCP)
- ✅ Differentiation from platform-locked alternatives

**Measurable Benefit:** Premium positioning in market

**Operational Efficiency (Medium Impact)**

- ✅ Automated generation reduces manual documentation burden
- ✅ CI/CD validation catches format compliance issues
- ✅ Version tracking enables rollback and debugging
- ✅ Hash verification prevents unintended modifications

**Measurable Benefit:** -50% documentation maintenance burden

**Governance Preservation (High Impact)**

- ✅ Directive system discoverable via custom extensions
- ✅ Multi-agent orchestration patterns documented
- ✅ Quality gates (ATDD/TDD) maintained in exports
- ✅ Version governance enhanced by API versioning

**Measurable Benefit:** Framework sophistication becomes competitive advantage

### Negative Consequences

**Maintenance Overhead (Low Impact)**

- ⚠️ Three export formats to maintain vs. one source format
- ⚠️ Format specification updates require exporter changes
- ⚠️ CI/CD pipeline adds build complexity

**Mitigation:**

- Automated generation minimizes manual work
- Version-pinned exports isolate spec change impact
- Comprehensive tests detect breaking changes early
- Clear ownership and deprecation policy

**Estimated Cost:** ~4 hours/quarter maintenance (~$1,600/year)

**Schema Definition Effort (Medium Impact)**

- ⚠️ Requires formalizing input/output contracts
- ⚠️ JSON Schema expertise needed
- ⚠️ Initial 8-16 hours per agent for schema extraction

**Mitigation:**

- Incremental rollout (top 5 agents first = 80% coverage)
- Schema templates and examples provided
- Community review and refinement
- Long-term benefit: clearer contracts and validation

**Estimated Cost:** 128 hours initial (16 agents × 8h average)

**Custom Extension Adoption Risk (Low Impact)**

- ⚠️ External tools may not support custom governance extensions
- ⚠️ Standard fields provide basic functionality only
- ⚠️ Framework uniqueness hidden from extension-unaware tools

**Mitigation:**

- Standard fields remain usable without extensions
- Documentation highlights governance capabilities
- Examples demonstrate extension schema
- Contribute extensions to standard specifications

**Estimated Impact:** 30-40% of tools leverage extensions; remainder use standard fields

**Complexity Increase (Low Impact)**

- ⚠️ More moving parts (exporters, validators, CI/CD)
- ⚠️ Debugging requires understanding generation pipeline
- ⚠️ Contributor learning curve for format specifications

**Mitigation:**

- Comprehensive developer documentation
- Clear separation: source (markdown) vs. artifacts (generated)
- Tooling abstracts complexity (single `npm run build:exports` command)
- Validation provides clear error messages

**Estimated Impact:** +2 hours onboarding time for contributors

### Net Assessment

**Benefits significantly outweigh costs:**

- **ROI:** 269% over 3 years
- **Payback Period:** <6 months
- **Risk Level:** Low (automated generation, validation gates)
- **Strategic Fit:** High (reference implementation positioning)

---

## Considered Alternatives

### Alternative 1: OpenCode Only

**Description:** Export to OpenCode format exclusively

**Pros:**

- ✅ Single format to maintain
- ✅ Emerging open standard (future-focused)
- ✅ Simplest implementation

**Cons:**

- ❌ Limited current ecosystem adoption
- ❌ GitHub Copilot users require manual conversion
- ❌ Single point of failure if standard stagnates
- ❌ Smaller addressable user base

**Decision:** Rejected — diversification provides better ecosystem coverage and risk mitigation

---

### Alternative 2: Platform-Native Integration

**Description:** Deep integration with specific platforms (e.g., Claude MCP server, OpenAI GPT Store)

**Pros:**

- ✅ Optimized user experience on each platform
- ✅ Native feature support (tool use, streaming)
- ✅ Platform-specific discovery (app stores)

**Cons:**

- ❌ Platform lock-in risk (vendor dependency)
- ❌ High maintenance (platform APIs change frequently)
- ❌ Governance compromised (platforms dictate architecture)
- ❌ Multi-agent orchestration difficult (platforms assume single-agent)

**Decision:** Rejected — contradicts open standards positioning and governance preservation goals

---

### Alternative 3: Manual Export-on-Request

**Description:** Provide conversion tools but don't automate; users export manually

**Pros:**

- ✅ No CI/CD pipeline needed
- ✅ Users control what to export
- ✅ Simpler initial implementation

**Cons:**

- ❌ High friction for users (manual step)
- ❌ Stale exports (users forget to regenerate)
- ❌ No validation enforcement
- ❌ Distribution complexity (which version is official?)

**Decision:** Rejected — automation is core value proposition

---

### Alternative 4: Dual Source-of-Truth

**Description:** Maintain markdown AND OpenCode files manually; pick best for each use

**Pros:**

- ✅ Optimized for each use case
- ✅ No build step required

**Cons:**

- ❌ High drift risk (updates not synchronized)
- ❌ Double maintenance burden (2x work minimum)
- ❌ Version control conflicts (which is authoritative?)
- ❌ Violates Directive 021 (Locality of Change)

**Decision:** Rejected — drift risk unacceptable for governance framework

---

## Implementation Plan

### Phase 1: Schema Formalization (Week 1)

**Deliverables:**

- [ ] Define schema format convention (JSON Schema Draft 7)
- [ ] Document schema authoring guidelines
- [ ] Extract schemas for top 5 agents (architect, backend-dev, frontend-dev, tester, curator)
- [ ] Validate schema extraction approach with team review

**Success Criteria:**

- ✅ All schemas validate against JSON Schema specification
- ✅ Schemas cover 80% of agent invocations (top 5 agents)
- ✅ Team consensus on schema format

### Phase 2: Export Pipeline Development (Week 2)

**Deliverables:**

- [ ] Enhance OpenCode exporter (from prototype in `tools/opencode-exporter.js`)
- [ ] Develop GitHub Copilot Skills exporter
- [ ] Develop MCP exporter
- [ ] Complete schema coverage for remaining 11 agents
- [ ] Implement custom governance extensions

**Success Criteria:**

- ✅ All 16 agents export successfully to all 3 formats
- ✅ Governance metadata present in custom extensions
- ✅ Exports validate against target format specifications

### Phase 3: CI/CD Automation (Week 3)

**Deliverables:**

- [ ] Create GitHub Actions workflow (`.github/workflows/generate-exports.yml`)
- [ ] Implement validation tests for each format
- [ ] Add hash verification for source-export integrity
- [ ] Configure artifact upload (GitHub Actions artifacts + releases)
- [ ] Set up distribution channels (npm, Docker optional for v1.0)

**Success Criteria:**

- ✅ CI/CD pipeline runs on every commit to `.github/agents/`
- ✅ Build time <5 minutes
- ✅ Validation catches format errors before merge
- ✅ Artifacts downloadable from GitHub Actions

### Phase 4: Documentation & Release (Week 4)

**Deliverables:**

- [ ] Write user guide for each export format
- [ ] Create migration documentation (adding schemas to existing agents)
- [ ] Document custom extension schema
- [ ] Write contributing guide (how to add/modify agents)
- [ ] Package v1.0.0 release with all formats
- [ ] Publish to GitHub Releases

**Success Criteria:**

- ✅ User can integrate an agent in <30 minutes following guide
- ✅ Documentation covers all 3 formats
- ✅ Contributors understand schema requirements
- ✅ v1.0.0 release available with all artifacts

---

## Success Metrics

### Technical Metrics

- ✅ **Export Success Rate:** 100% (16/16 agents)
- ✅ **Schema Validation:** 100% pass rate
- ✅ **Source Integrity:** 0 manual edits to generated files
- ✅ **Build Performance:** <5 minutes CI/CD time
- ✅ **Format Compliance:** 100% validation pass (OpenCode validator, Copilot schema, MCP spec)

### Business Metrics

- ✅ **Integration Time:** <30 minutes (baseline: 4-8 hours)
- ✅ **External Adoption:** 2+ tools adopt framework within 6 months
- ✅ **Download Volume:** 50+ downloads/clones within 3 months
- ✅ **Community Engagement:** Positive feedback (GitHub stars, issues, PRs)
- ✅ **Market Positioning:** "Reference implementation" mentions in 3+ external publications

### Governance Metrics

- ✅ **Directive Compliance:** All exports include governance extensions
- ✅ **Quality Gate Preservation:** ATDD/TDD references present
- ✅ **Orchestration Visibility:** Multi-agent patterns documented in exports
- ✅ **Version Traceability:** All exports correlate to source commit

---

## Compliance

### Directive Alignment

| Directive | Title | Compliance |
|-----------|-------|-----------|
| 006 | Version Governance | ✅ Enhanced: API versioning, framework versioning, semantic versioning |
| 007 | Agent Declaration | ✅ Preserved: Agent authority metadata in exports |
| 018 | Traceable Decisions | ✅ Compliant: This ADR documents architectural decision at appropriate stability level |
| 020 | Lenient Adherence | ✅ Enabled: Custom extensions allow flexibility while maintaining standards |
| 021 | Locality of Change | ✅ Minimized: Build-time generation isolates format changes |

### Quality Gates

**Existing Gates Preserved:**

- ✅ Directive 016 (ATDD): Test requirements referenced in exports
- ✅ Directive 017 (TDD): Unit test requirements preserved
- ✅ Primer framework (ADR-011): Context checking metadata available

**New Gates Added:**

- ✅ Export completeness validation
- ✅ Schema validation (JSON Schema)
- ✅ Hash verification (source-export integrity)
- ✅ Format compliance validation (OpenCode, Copilot, MCP)
- ✅ Custom extension validation

---

## References

### Related Documents

- **Formal Technical Assessment:** `work/analysis/formal-technical-assessment.md`
- **Technical Design:** `work/analysis/tech-design-export-pipeline.md`
- **Framework Alignment Analysis:** `work/analysis/2026-01-29_agentic-framework-alignment.md`
- **OpenCode Fit Assessment:** `work/analysis/distribution-release-opencode-fit.md`
- **Prototype Exporter:** `tools/opencode-exporter.js`

### External Standards

- **OpenCode Specification:** <https://opencode.ai/docs/agents/>
- **GitHub Copilot Skills:** <https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot>
- **Model Context Protocol:** <https://modelcontextprotocol.io/>
- **JSON Schema:** <https://json-schema.org/specification>

### Prior Art

- **ADR-011:** Primer Execution Matrix
- **ADR-012:** Test-First Requirements (ATDD/TDD exception handling)
- **Directive 018:** Documentation Level Framework (stable vs. volatile documentation)

---

## Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| **Architect** | Architect Alphonso | 2026-01-29 | ✅ Proposed |
| **Technical Lead** | _Pending_ | | ⏳ Review Required |
| **Product Owner** | _Pending_ | | ⏳ Review Required |
| **Governance Board** | _Pending_ | | ⏳ Approval Required |

---

**Status:** Proposed  
**Next Action:** Technical Lead review and Product Owner approval  
**Target Decision Date:** 2026-02-05  
**Implementation Start (if approved):** 2026-02-07

---

**Document Version:** 1.0.0  
**Date:** 2026-01-29  
**Author:** Architect Alphonso  
**Review Cycle:** Every 6 months or on significant format specification changes
