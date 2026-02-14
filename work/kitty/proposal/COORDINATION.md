# Integration Coordination Document
## Spec Kitty × Doctrine Governance Framework

**Version:** 1.0  
**Date:** 2026-02-14  
**Owner:** Manager Mike (Coordination)  
**Status:** Active — Awaiting Human Decision  
**Context:** [Directive 018 — Traceable Decisions](../../../doctrine/directives/018_traceable_decisions.md)

---

## 1. Mission Statement

We are building a **unified agent-augmented development platform** that combines Spec Kitty's production-grade workflow orchestration (spec lifecycle, mission-based routing, worktree isolation, quality gates) with Doctrine's layered governance framework (5-layer behavioral policy stack, agent profiles, directives, file-based collaboration protocols). The result: a platform where **Spec Kitty manages what work gets done and when**, while **Doctrine ensures how agents behave and why decisions are made**. This integration enables teams to adopt rigorous AI governance without disrupting proven workflow patterns, providing both operational velocity and behavioral accountability.

---

## 2. Strategic Positioning

### Problem Statement
Neither system solves these problems alone:

| Gap | Without Spec Kitty | Without Doctrine |
|-----|-------------------|------------------|
| **Governance rigor** | Manual agent behavior enforcement | ✅ Layered policy stack with precedence |
| **Production workflow** | ✅ Spec-driven lifecycle with quality gates | Ad-hoc task management |
| **Multi-agent coordination** | ✅ Worktree isolation + orchestrator | Status files without lifecycle semantics |
| **Behavioral traceability** | No decision provenance | ✅ Decision log + directive references |
| **Telemetry & observability** | ❌ Both systems lack production telemetry | ❌ |
| **Model routing intelligence** | ❌ Model-agnostic (vendor neutral) | ❌ No routing layer |

### Value Proposition

**For teams:** Adopt enterprise-grade agent governance without rewriting existing Spec Kitty workflows.

**For individual developers:** Get started quickly with Spec Kitty's CLI/TUI, then layer in governance rigor as complexity grows.

**For agent operators:** Gain observable, auditable agent behavior with clear precedence contracts and decision traceability.

### What Is NOT in Scope

1. **Replacing Spec Kitty's core workflow** — WP lane lifecycle, mission system, worktree semantics remain authoritative.
2. **Mandatory Doctrine adoption** — Spec Kitty must remain fully functional without Doctrine plugin enabled.
3. **Building a third framework** — This is a plugin integration, not a greenfield rewrite.
4. **Upstream fork/extraction** — Spec Kitty remains an external dependency; we contribute extensions upstream where possible.

---

## 3. Success Criteria

### Measurable Outcomes

| # | Criterion | Measurement Method | Target |
|---|-----------|-------------------|--------|
| 1 | **Dual-mode operation** | Spec Kitty runs unchanged when `doctrine-governance` plugin disabled | 100% backward compatibility |
| 2 | **Policy enforcement transparency** | All governance checks log source directive + rationale | Every check traceable to directive |
| 3 | **Zero workflow disruption** | WP lane transitions do not change schema or CLI commands | No breaking changes to `sk` CLI |
| 4 | **Agent profile fidelity** | Agent behavior in Doctrine mode matches profile specifications | 95%+ alignment score via validation suite |
| 5 | **Decision provenance** | All agent decisions logged with context references | 100% coverage for tier-1 decisions |
| 6 | **Routing provider swappability** | Model routing configured via provider interface, not hardcoded | ≥2 providers (doctrine, custom) supported |
| 7 | **Documentation coverage** | Constitution generated from Doctrine layers with precedence contract visible | Constitution includes full precedence map |

### Qualitative Success Signals

- Teams report faster onboarding with governance clarity
- Audit trails pass compliance review without manual annotation
- Upstream Spec Kitty maintainers adopt governance hooks as stable extension point
- Zero "two-masters" ambiguity reports (i.e., Constitution contradicting General/Operational Guidelines, or conflicting authority between Constitution and Directives)

---

## 4. Stakeholder Map

### Primary Stakeholders

| Stakeholder | Interest | Engagement Level | Communication Channel |
|-------------|----------|-----------------|----------------------|
| **Spec Kitty upstream maintainers** | Extension API stability, plugin model compatibility | High — requires design consultation before implementation | GitHub discussions, RFC proposals |
| **Doctrine framework users** | Preserve governance rigor, ensure directive compatibility | High — early validation of integration design | This repo's issue tracker, ADR reviews |
| **Agent operators (human users)** | Clear mental model, no dual-authority confusion | Medium — need documentation + migration guide | Docs site, example repositories |
| **This repo's contributors** | Maintain Doctrine framework integrity during integration | High — code review, validation suite updates | PR reviews, weekly coordination sync |

### Secondary Stakeholders

- **Compliance/audit teams:** Benefit from decision provenance; inform requirements but not blocking approval.
- **LLM service stack users:** Future consumers of unified telemetry/routing; inform Phase 2+ design.
- **Open-source community:** Watchers/contributors; informed via changelog and public roadmap.

---

## 5. Coordination Protocol

### Progress Tracking (Dual-Codebase)

#### In This Repository (`quickstart_agent-augmented-development`)
- **Status file:** `work/kitty/INTEGRATION_STATUS.md`
- **Cadence:** Updated after each phase milestone or blocker
- **Format:**
  ```yaml
  phase: "Phase 1 — Governance Extension Design"
  progress: 60%
  blockers:
    - "Awaiting Spec Kitty maintainer feedback on plugin hook design"
  completed:
    - "Analysis artifacts (SUMMARY.md, EXECUTIVE_SUMMARY.md, VISION.md)"
    - "Coordination document (COORDINATION.md)"
  next:
    - "Draft RFC for governance plugin interface"
  ```

#### In Spec Kitty Repository (External)
- **Mechanism:** Git subtree at `spec-kitty/governance/doctrine/` (once distribution decision finalized)
- **Tracking:** Link Spec Kitty issues/PRs back to this repo's `INTEGRATION_STATUS.md`
- **Synchronization:** Bi-directional sync on doctrine updates (Option C from analysis — subtree with periodic rebase)

### Handling Upstream Spec Kitty Changes

| Change Type | Detection Method | Response Protocol | SLA |
|-------------|-----------------|-------------------|-----|
| **Breaking change (WP schema, CLI commands)** | Spec Kitty release notes + CI integration tests | Immediate blocker flag; coordination meeting within 48h | 2 business days |
| **New feature (mission type, validator)** | GitHub watch + monthly review | Evaluate compatibility; update integration design if needed | Next sprint |
| **Bug fix (non-breaking)** | Automated dependency update (Dependabot) | Merge after CI green | 1 week |
| **Extension API added** | GitHub discussion notification | Assess adoption opportunity; propose doctrine extension | 2 weeks |

### Communication Cadence

- **Weekly (async):** Status update in `INTEGRATION_STATUS.md` by assigned coordinator
- **Bi-weekly (sync):** 30min coordination call with core contributors (this repo + Spec Kitty liaison if available)
- **Monthly:** Stakeholder report to Doctrine framework users + Spec Kitty community (via GitHub discussion)
- **Ad-hoc:** Blocker escalation within 24h via GitHub issue + direct maintainer ping

### Decision-Making Process (Per Directive 018)

#### Level 1: Operational Decisions (Implementation Details)
- **Who decides:** Implementation lead (Backend Benny, Python Pedro)
- **Documentation:** Commit messages, PR descriptions
- **Review:** Code Reviewer Cindy approval required
- **Example:** "Use YAML vs TOML for routing provider config"

#### Level 2: Tactical Decisions (Architecture Choices)
- **Who decides:** Architect Alphonso with Manager Mike coordination
- **Documentation:** ADR in `docs/architecture/decisions/`
- **Review:** Two-person approval (architecture + relevant specialist)
- **Example:** "Routing provider interface design"

#### Level 3: Strategic Decisions (Integration Direction)
- **Who decides:** Human stakeholder with recommendation from Manager Mike + Architect Alphonso
- **Documentation:** This COORDINATION.md + decision log entries below
- **Review:** Public comment period (1 week) before finalization
- **Example:** "Adopt git subtree vs npm package for Doctrine distribution"

---

## 6. Risk Register

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|------|:----------:|:------:|------------|-------|
| 1 | **Upstream Spec Kitty rejects plugin model** | Medium | High | Early RFC engagement; demonstrate value with working prototype; offer to maintain extension externally if needed | Manager Mike |
| 2 | **Two-masters governance conflict** | High | High | Explicit precedence contract in constitution (see Decision Log #4); validation suite to detect conflicts; fail-fast on ambiguity | Architect Alphonso |
| 3 | **Integration complexity stalls development** | Medium | Medium | Phased rollout (governance first, routing later); maintain dual-mode operation to isolate risk; rollback plan via feature flag | Backend Benny |
| 4 | **Doctrine updates break Spec Kitty integration** | Medium | Medium | Semantic versioning enforcement; integration test suite in both repos; pin to stable Doctrine releases for Spec Kitty distribution | Code Reviewer Cindy |
| 5 | **Adoption friction due to dual vocabulary** | High | Low | Terminology crosswalk table in docs; migration guide with before/after examples; CLI help text bridges concepts | Scribe Sam |

---

## 7. Decision Log

### Key Decisions Made

#### Decision #1: Spec Kitty as Primary Platform
- **Date:** 2026-02-14
- **Context:** Analysis showed 25% infrastructure coverage overlap; systems are complementary (workflow vs governance)
- **Rationale:** Spec Kitty has production-grade workflow orchestration; building equivalent is duplicative. Doctrine's value is governance rigor, not workflow replacement.
- **Implication:** All integration work extends Spec Kitty; Doctrine becomes optional plugin layer.
- **Reference:** `work/kitty/SUMMARY.md` (Analysis 1 & 2)

#### Decision #2: Doctrine as Optional Plugin
- **Date:** 2026-02-14
- **Context:** Spec Kitty has existing user base; forcing Doctrine adoption risks migration friction
- **Rationale:** Maximize adoption by making governance opt-in; demonstrate value before requiring behavioral change.
- **Implication:** Spec Kitty must fully function with `doctrine-governance` plugin disabled; dual-mode operation required.
- **Reference:** `work/kitty/proposal/EXECUTIVE_SUMMARY.md`

#### Decision #3: Git Subtree Distribution (Option C)
- **Date:** 2026-02-14 (provisional — pending human approval)
- **Context:** Three options evaluated: fork, full merge, external dependency
- **Rationale:** Subtree balances autonomy (Doctrine evolves independently) with integration (Spec Kitty users get stable snapshot). Avoids npm/PyPI packaging overhead in early phases.
- **Implication:** Periodic sync required; version pinning strategy needed; upstream Doctrine changes require manual rebase.
- **Reference:** `work/kitty/2026-02-14-doctrine-spec-kitty-integration-analysis.md` (Section: Recommended Integration)
- **Status:** ⚠️ **Awaiting stakeholder approval** (see Open Items #2)

#### Decision #4: Doctrine-First Precedence with Constitution as Local Override
- **Date:** 2026-02-14 (revised)
- **Context:** Risk of conflicting authority between Spec Kitty's Constitution and Doctrine's guidelines
- **Rationale:** The Doctrine instruction hierarchy (AGENTS.md) is explicit and immutable: General/Operational Guidelines are HIGHEST priority; local overrides (`.doctrine-config/`) sit at MEDIUM priority and MUST NOT contradict them. Constitution is functionally equivalent to `.doctrine-config/` (see ARCHITECTURE_SPEC Q3a), so it occupies the same level — it customizes Doctrine for a specific project but cannot override core framework values.
- **Implication:** Precedence contract: `Doctrine General Guidelines → Operational Guidelines → Constitution/.doctrine-config → Directives → Mission Guidance → Tactics/Templates`. Constitution extends, narrows, and adds project-specific rules within Doctrine bounds.
- **Reference:** `AGENTS.md` (Instruction Hierarchy — Immutable), `doctrine/guidelines/bootstrap.md` (line 57: "Local overrides MUST NOT override general_guidelines.md or operational_guidelines.md")
- **Refinement (2026-02-14):** Constitution and `.doctrine-config/` are near-identical concepts — both are project-scoped governance overlays. Treat them as two views of the same governance state (Constitution = human narrative, `.doctrine-config/` = machine config). Phase 2 must include a sync/validation mechanism.

#### Decision #6: Unified Event Spine for Cross-Cutting Concerns
- **Date:** 2026-02-14
- **Context:** Governance hooks, telemetry, work logging, and cost tracking all attach to the same lifecycle points (lane transitions, phase boundaries).
- **Rationale:** Rather than wiring each concern independently into the orchestrator, governance validations emit events through the EventBridge. A single event stream serves telemetry, work logging (Directive 014), cost tracking, and compliance metrics. New concerns require only a new consumer registration — zero additional hook points.
- **Implication:** Phase 1 telemetry library includes `WorkLogEmitter` consumer; Phase 2 governance hooks emit `ValidationEvent` through EventBridge.
- **Reference:** `work/kitty/proposal/ARCHITECTURE_SPEC.md` (Design Note: Lifecycle Hooks as Unified Event Sources)

#### Decision #5: Pluggable Routing Provider Interface
- **Date:** 2026-02-14
- **Context:** Model routing is critical missing capability; hard-coding doctrine routing logic into Spec Kitty core creates vendor lock-in
- **Rationale:** Provider interface allows swappable routing strategies (doctrine-based, custom, cost-optimized, etc.) without core rewrites.
- **Implication:** Phase 3 implementation must design `RoutingProvider` interface before building doctrine routing provider.
- **Reference:** `work/kitty/analysis/2026-02-14-evaluation-doctrine-governance-extension.md` (Section: Recommended Shape, Phase 3)

---

## 8. Open Items Requiring Human Decision

### Critical Path (Block Phase 1 Implementation)

#### Item #1: Upstream Collaboration Strategy
- **Question:** Do we engage Spec Kitty maintainers before building, or build prototype first and propose after?
- **Options:**
  - **A. Early RFC:** Draft extension interface proposal, submit to Spec Kitty discussions, wait for feedback (2-4 weeks delay)
  - **B. Prototype-first:** Build working extension in fork, demonstrate value, then propose upstream merge (faster start, riskier acceptance)
  - **C. Hybrid:** Informal maintainer outreach + parallel prototype development (balances risk and speed)
- **Recommendation:** Option C — DM Spec Kitty lead with 1-page concept, start Phase 1 design in parallel
- **Impact:** Determines whether we can use official extension points or need external adapter layer
- **Deadline:** Decision needed by 2026-02-20 to maintain Phase 1 schedule

#### Item #2: Doctrine Distribution Mechanism
- **Question:** Confirm git subtree (Option C) or explore npm/PyPI package distribution?
- **Options:**
  - **A. Git subtree:** Simple initial integration, manual sync overhead, no external dependency management
  - **B. PyPI package:** Cleaner dependency management, requires packaging infrastructure, adds version compatibility complexity
  - **C. Hybrid:** Subtree for Spec Kitty integration, separate PyPI package for standalone Doctrine users
- **Recommendation:** Option A for Phase 1-2, revisit Option C in Phase 3 once integration stable
- **Impact:** Determines synchronization workflow and version pinning strategy
- **Deadline:** Decision needed before Phase 2 kickoff (estimated 4-6 weeks from now)

### Non-Blocking (Inform Later Phases)

#### Item #3: Budget/Resource Allocation
- **Question:** What is implementation capacity for 4-phase roadmap?
- **Context:** Phase 1 (governance extension) is ~2-3 weeks solo dev work; Phase 2-4 require infrastructure build (telemetry, event emission, routing provider)
- **Options:**
  - **Light:** Focus on governance extension (Phase 1) only; defer routing/telemetry to future
  - **Moderate:** Phase 1-2 (governance + basic routing); ~6-8 weeks total
  - **Full:** All 4 phases; ~12-16 weeks with parallel workstreams
- **Impact:** Determines scope committed in initial release vs deferred to roadmap
- **Deadline:** Decision needed for public roadmap publication (estimated 2026-03-01)

#### Item #4: Success Metrics Tracking
- **Question:** Who owns validation suite and integration test maintenance?
- **Context:** Dual-mode operation requires continuous validation that both Doctrine-enabled and Doctrine-disabled modes work
- **Options:**
  - **A. This repo:** Maintain tests in `quickstart_agent-augmented-development/tests/integration/spec_kitty/`
  - **B. Spec Kitty repo:** Contribute tests upstream if plugin model accepted
  - **C. Shared:** Core tests upstream, doctrine-specific tests in this repo
- **Recommendation:** Option A initially, migrate to Option C after upstream acceptance
- **Impact:** Determines CI/CD setup and test ownership boundaries
- **Deadline:** Decision needed before Phase 1 completion (when tests get written)

---

## 9. Next Steps

### Immediate Actions (This Week)

1. **Manager Mike:** Socialize this COORDINATION.md with stakeholders; collect feedback via GitHub discussion
2. **Architect Alphonso:** Draft Phase 1 design spec (`governance-doctrine-extension-design.md`) covering:
   - Extension entrypoints
   - Config precedence contract
   - Validation hook design
3. **Scribe Sam:** Create terminology crosswalk table for docs (Spec Kitty ↔ Doctrine glossary mapping)

### Short-Term (Next 2 Weeks)

1. **Manager Mike:** Resolve Open Item #1 (upstream collaboration strategy) via Spec Kitty maintainer outreach
2. **Planning Petra:** Create Phase 1 task breakdown in `work/collaboration/inbox/`
3. **Bootstrap Bill:** Set up `work/kitty/INTEGRATION_STATUS.md` tracking file

### Medium-Term (Next 4-6 Weeks)

1. **Backend Benny:** Implement Phase 1 governance extension (pending design spec approval)
2. **Code Reviewer Cindy:** Design validation suite for dual-mode operation
3. **Manager Mike:** Resolve Open Item #2 (distribution mechanism) before Phase 2 kickoff

---

## 10. Appendices

### A. Reference Documents

| Document | Location | Purpose |
|----------|----------|---------|
| Full Analysis Summary | `work/kitty/SUMMARY.md` | Comprehensive integration feasibility analysis |
| Integration Analysis | `work/kitty/analysis/2026-02-14-doctrine-spec-kitty-integration-analysis.md` | Detailed concept mapping + options evaluation |
| Coverage Analysis | `work/kitty/analysis/2026-02-14-control-plane-spec-kitty-coverage.md` | Infrastructure gap assessment |
| Terminology Comparison | `work/kitty/analysis/spec-kitty-vs-quickstart-terminology-comparison.md` | Vocabulary alignment analysis |
| Executive Summary | `work/kitty/proposal/EXECUTIVE_SUMMARY.md` | Leadership-level decision summary |
| Vision Statement | `work/kitty/proposal/VISION.md` | Target-state architecture principles |
| Directive 018 | `doctrine/directives/018_traceable_decisions.md` | Decision documentation standards |

### B. Contact Points

- **Integration Coordination:** Manager Mike (this document's owner)
- **Architecture Decisions:** Architect Alphonso
- **Spec Kitty Upstream Liaison:** TBD (assign after Open Item #1 resolved)
- **Doctrine Framework Authority:** This repo's maintainers (collective)

### C. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-02-14 | Initial coordination document | Manager Mike |

---

**Document Status:** ✅ Active — Awaiting Human Decisions on Open Items #1-4

**Next Review Date:** 2026-02-21 (or upon resolution of Open Item #1, whichever comes first)
