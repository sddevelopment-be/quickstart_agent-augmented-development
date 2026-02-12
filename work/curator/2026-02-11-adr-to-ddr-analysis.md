# ADR to DDR Elevation Analysis

**Date:** 2026-02-11  
**Curator:** Curator Claire  
**Context:** Doctrine Violation Remediation - Phase 2

## Executive Summary

Analysis of 23 ADRs referenced in doctrine violations to identify which contain framework-level decisions that should be elevated to Doctrine Decision Records (DDRs).

**Key Findings:**
- **7 ADRs recommended for DDR elevation** (framework-level decisions)
- **16 ADRs should remain as ADRs** (repository-specific decisions)
- **2 ADRs already converted** (DDR-001, DDR-002)

**Recommended DDRs:** DDR-004 through DDR-010 (7 new DDRs)

---

## Analysis Methodology

### Classification Criteria

**FRAMEWORK (should be DDR):**
- ✅ Defines universal patterns applicable to any repository using the framework
- ✅ Describes core framework concepts (agents, directives, tactics, approaches)
- ✅ Establishes fundamental coordination patterns (file-based, task lifecycle)
- ✅ Defines framework distribution/portability mechanisms

**REPOSITORY (stays as ADR):**
- ❌ Specific to this repository's tooling (CI, deployment, local architecture)
- ❌ Technology choices for this specific project (Flask, WebSocket, etc.)
- ❌ Project governance decisions (TDD mandates, trunk-based dev)
- ❌ Implementation-specific patterns for this codebase

---

## Detailed Analysis

### FRAMEWORK DECISIONS → Recommended for DDR Elevation

#### 1. ADR-001: Modular Agent Directive System → **DDR-010**

**Current Status:** `docs/architecture/adrs/ADR-001-modular-agent-directive-system.md`

**Classification:** **FRAMEWORK** ✅

**Rationale:**
- **Core framework architecture:** Defines the foundational structure of agents, directives, profiles, and context loading
- **Universal applicability:** Any repository adopting the framework needs this directive system
- **Portability mechanism:** Explicitly designed for "cross-toolchain compatibility" and "reusability across projects"
- **Framework-level concepts:** Introduces `.github/agents/`, directive manifest, bootstrap/rehydration protocols
- **Not repository-specific:** Describes the framework itself, not how this repo uses it

**Proposed DDR Title:** "Modular Agent Directive System Architecture"

**Evidence from ADR:**
> "Markdown-first: All directives in portable `.md` format, no vendor-specific syntax"
> "Cross-toolchain compatibility: Works with any LLM system supporting markdown context"
> "Reusability: Directives can be shared across projects with minimal adaptation"

**DDR Content Changes:**
- Remove implementation notes specific to this repo (file paths, version numbers)
- Generalize to "framework core" concepts
- Keep directive system architecture, manifest schema, validation patterns

---

#### 2. ADR-002: File-Based Asynchronous Agent Coordination → **DDR-004**

**Current Status:** `docs/architecture/adrs/ADR-002-portability-enhancement-opencode.md`

**Classification:** **FRAMEWORK** ✅ (Note: File name doesn't match violations report - ADR-008 is the actual file-based coordination decision)

**Note:** The violations report references "ADR-002: File-Based Async Coordination" but the actual file is ADR-002: OpenCode Portability Enhancement, which is REPOSITORY-specific. **ADR-008 is the actual file-based coordination decision.**

**Corrected Analysis:** See ADR-008 below.

**ADR-002 (OpenCode) Classification:** **REPOSITORY** ❌
- Technology choice for *this* repository
- Specific vendor format (OpenCode)
- Not a universal framework pattern

---

#### 3. ADR-003: Task Lifecycle and State Management → **DDR-005**

**Current Status:** `docs/architecture/adrs/ADR-003-task-lifecycle-state-management.md`

**Classification:** **FRAMEWORK** ✅

**Rationale:**
- **Core framework concept:** Defines the five-state task lifecycle (new → assigned → in_progress → done/error)
- **Universal coordination pattern:** Fundamental to file-based orchestration in any repository
- **State transition rules:** Framework-level protocol for task ownership and lifecycle
- **Not implementation-specific:** Defines *what* the lifecycle is, not *how* this repo implements it
- **Enables multi-agent coordination:** Universal pattern for task handoffs

**Proposed DDR Title:** "Task Lifecycle and State Management Protocol"

**Evidence from ADR:**
> "We need a task lifecycle that provides clear ownership at each stage, prevents duplicate processing, handles errors gracefully"
> "State transitions via directory structure and YAML status field"

**DDR Content Changes:**
- Keep lifecycle states and transition rules
- Keep state persistence patterns (directory structure)
- Remove repository-specific directory paths
- Generalize validation rules to framework patterns

---

#### 4. ADR-004: Work Directory Structure → **DDR-006**

**Current Status:** `docs/architecture/adrs/ADR-004-work-directory-structure.md`

**Classification:** **FRAMEWORK** ✅

**Rationale:**
- **Framework-level pattern:** Defines the canonical directory structure for file-based orchestration
- **Universal convention:** `work/inbox/`, `work/assigned/<agent>/`, `work/done/` applicable to any repository
- **Enables atomic operations:** Directory-based state transitions are framework primitive
- **Coordination foundation:** Required for agents to discover and process tasks
- **Not repository-specific:** Describes the framework's work directory convention

**Proposed DDR Title:** "Work Directory Structure and Naming Conventions"

**Evidence from ADR:**
> "We will use a hierarchical `work/` directory structure organized by lifecycle state and agent ownership"
> "Hierarchical structure... is self-documenting and intuitive"

**DDR Content Changes:**
- Keep directory hierarchy pattern and naming conventions
- Keep file naming standards (ISO 8601 timestamps, agent prefixes)
- Remove specific agent names (structural, lexical, etc.) - these are repo-specific
- Generalize collaboration artifacts pattern

---

#### 5. ADR-005: Coordinator Agent Pattern → **DDR-007**

**Current Status:** `docs/architecture/adrs/ADR-005-coordinator-agent-pattern.md`

**Classification:** **FRAMEWORK** ✅

**Rationale:**
- **Core framework concept:** Defines the meta-agent orchestration pattern
- **Universal coordination pattern:** Any file-based orchestration needs task assignment and workflow sequencing
- **Framework role definition:** Establishes coordinator responsibilities (assignment, handoff, conflict detection)
- **Not implementation-specific:** Defines the *pattern*, not Python implementation details
- **Enables multi-agent workflows:** Foundation for orchestration chains

**Proposed DDR Title:** "Coordinator Agent Orchestration Pattern"

**Evidence from ADR:**
> "We will implement a Coordinator agent as a specialized meta-agent responsible for orchestration tasks but not artifact generation"
> "Polling-based, idempotent, stateless: All state stored in files"

**DDR Content Changes:**
- Keep coordinator responsibilities and execution model
- Keep workflow sequencing and conflict detection patterns
- Remove Python code examples (implementation-specific)
- Remove GitHub Actions examples (repository-specific)
- Generalize to orchestration patterns

---

#### 6. ADR-008: File-Based Asynchronous Agent Coordination → **DDR-004**

**Current Status:** `docs/architecture/adrs/ADR-008-file-based-async-coordination.md` (Note: Appears to be ADR-009 in the repo)

**Classification:** **FRAMEWORK** ✅

**Rationale:**
- **Core framework architecture:** Defines the fundamental coordination mechanism
- **Universal applicability:** File-based coordination is the framework's defining characteristic
- **Portability principle:** "Works across CI systems, local environments, different LLM toolchains"
- **Framework primitive:** YAML tasks, directory-based state, Git-native coordination
- **Not repository-specific:** Describes framework coordination paradigm

**Proposed DDR Title:** "File-Based Asynchronous Coordination Protocol"

**Evidence from ADR:**
> "We will coordinate multiple agents using file-based task descriptions stored in a shared `work/` directory structure"
> "Git-native: Every state change is a commit, providing full history and diff capability"
> "Portable: Works in CI, locally, or on any system with file access"

**DDR Content Changes:**
- Keep coordination mechanism and YAML task schema principles
- Keep directory-based state transition pattern
- Keep Git-native rationale
- Remove repository-specific implementation details

---

#### 7. ADR-013: Zip-Based Framework Distribution → **DDR-008**

**Current Status:** `docs/architecture/adrs/ADR-013-zip-distribution.md`

**Classification:** **FRAMEWORK** ✅

**Rationale:**
- **Framework distribution mechanism:** Defines how the framework is packaged and distributed
- **Portability enabler:** "Consumers span GitHub, GitLab, on-prem Git, and file shares"
- **Core vs. local boundary:** Establishes framework upgrade patterns respecting local customization
- **Universal packaging pattern:** Applies to any framework release, not this repository's deployment
- **Not repository-specific:** Describes framework distribution, not this project's build process

**Proposed DDR Title:** "Framework Distribution and Upgrade Mechanisms"

**Evidence from ADR:**
> "Ship every framework release as `quickstart-framework-<version>.zip`"
> "Scripts never overwrite divergent files; conflicts become explicit artifacts"
> "Enables learning period for trust building"

**DDR Content Changes:**
- Keep zip structure and upgrade script patterns
- Keep core/local boundary principles
- Keep safety mechanisms (conflict detection)
- Remove repository-specific implementation scripts
- Generalize to framework release patterns

---

#### 8. ADR-017: Traceable Decision Integration → **DDR-009**

**Current Status:** `docs/architecture/adrs/ADR-017-traceable-decision-integration.md`

**Classification:** **FRAMEWORK** ✅

**Rationale:**
- **Framework-level pattern:** Defines decision marker format and linking conventions
- **Universal traceability protocol:** Applies to any repository using ADRs with agent coordination
- **Framework integration:** Extends agent directive system with decision capture requirements
- **Not repository-specific:** Describes *how* decisions are traced in agent workflows, not this repo's decisions
- **Agent coordination pattern:** Defines agent behavior for decision capture

**Proposed DDR Title:** "Traceable Decision Patterns and Agent Integration"

**Evidence from ADR:**
> "We will adopt traceable decision patterns as a mandatory practice for all agent-augmented development tasks"
> "All architectural decisions embedded in code, documentation, or task artifacts MUST use standardized markers"
> "Agents MUST: Pre-check: Load relevant ADRs; Context awareness: Reference appropriate ADRs; Marker generation"

**DDR Content Changes:**
- Keep decision marker format and linking conventions
- Keep agent directive requirements for decision capture
- Keep flow-aware capture strategy
- Remove repository-specific validation scripts
- Generalize to framework-level decision traceability

---

### REPOSITORY DECISIONS → Remain as ADRs

#### 9. ADR-002: Portability Enhancement (OpenCode)

**Classification:** **REPOSITORY** ❌

**Rationale:**
- **Technology choice:** Adoption of OpenCode specification for *this* repository
- **Vendor-specific:** OpenCode is a specific format, not a universal framework pattern
- **Repository configuration:** Describes *this* project's migration to OpenCode
- **Not framework-level:** Other repositories could use different formats

---

#### 10. ADR-009: Orchestration Metrics Standard

**Classification:** **REPOSITORY** ❌

**Rationale:**
- **Quality standards for this repo:** Defines metrics capture for *this* repository's tasks
- **Not framework requirement:** Other repositories could use different metrics formats
- **Project-specific targets:** "target: 25 minutes", "100-200 lines" are repository conventions
- **Implementation-specific:** Addresses specific POC findings (POC1, POC2) from this repo
- **Could be framework guidance:** But current form is too prescriptive for universal application

**Borderline Decision - Keep as ADR for now:**
- Could become a framework *guideline* (not decision) later
- Current metrics are repository-specific baselines
- Framework shouldn't mandate specific target values

---

#### 11. ADR-011: Primer Execution Matrix (Already DDR-001)

**Classification:** **FRAMEWORK** ✅ (Already converted)

**Status:** Already elevated to `doctrine/decisions/DDR-001-primer-execution-matrix.md`

**No action needed.**

---

#### 12. ADR-012: Test-Driven Development Mandate

**Classification:** **REPOSITORY** ❌

**Rationale:**
- **Project governance decision:** *This* repository mandates ATDD/TDD, not the framework
- **Process choice:** Other repositories could use different testing approaches
- **Not framework architecture:** Describes development practices, not framework mechanics
- **Repository-specific enforcement:** "agents approach new or modified code" in this repo

**Note:** While testing is important, the framework doesn't mandate specific testing methodologies.

---

#### 13. ADR-014: Framework Guardian Agent (Already DDR-002)

**Classification:** **FRAMEWORK** ✅ (Already converted)

**Status:** Already elevated to `doctrine/decisions/DDR-002-framework-guardian-role.md`

**No action needed.**

---

#### 14. ADR-015: Follow-Up Task Lookup Pattern

**Classification:** **REPOSITORY** ❌

**Status:** **REJECTED** ADR (not accepted)

**Rationale:**
- **Status:** Explicitly rejected as over-engineered
- **Not implemented:** Never part of framework or repository
- **No action needed:** Rejected ADRs don't become DDRs

---

#### 15. ADR-019: Trunk-Based Development

**Classification:** **REPOSITORY** ❌

**Rationale:**
- **Project governance decision:** Branching strategy for *this* repository
- **Not framework requirement:** Other repositories could use Git Flow, GitHub Flow, etc.
- **Repository-specific integration:** GitHub Actions, CI pipelines specific to this project
- **Development practice:** Not a framework architectural decision

---

#### 16. ADR-020: Multi-Tier Agentic Runtime

**Classification:** **REPOSITORY** ❌

**Rationale:**
- **Technology stack choice:** Specific vendor routing (OpenRouter, OpenCode.ai) for this project
- **Implementation architecture:** Layer 3 model execution (OpenAI, Anthropic, Ollama) is this repo's choice
- **Not framework requirement:** Framework is model-agnostic
- **Project-specific runtime:** Describes *this* repository's runtime setup

---

#### 17. ADR-023: Prompt Optimization Framework

**Classification:** **REPOSITORY** ❌

**Rationale:**
- **Project-specific analysis:** Based on "129 work logs across 15 agent types" *in this repository*
- **Repository baselines:** "37 minutes average" are this project's metrics
- **Implementation tooling:** Export pipeline, parser.js, validator.js are this repo's tools
- **Not framework-level:** Prompt optimization could be guidance, but current form is too specific

**Note:** Status is "Proposed" - not yet accepted.

---

#### 18. ADR-028: Tool-Model Compatibility Validation

**Classification:** **REPOSITORY** ❌

**Rationale:**
- **LLM Service Layer implementation:** Specific to this repository's `llm-service` component
- **Technology-specific validation:** Claude-code, Codex are this project's tool choices
- **Repository architecture:** Part of this repo's Python service layer
- **Not framework requirement:** Framework doesn't mandate LLM service architecture

---

#### 19. ADR-032: Real-Time Execution Dashboard

**Classification:** **REPOSITORY** ❌

**Rationale:**
- **Technology stack choice:** Flask + Flask-SocketIO is this repository's choice
- **Implementation feature:** Dashboard is a feature of *this* repository's llm-service
- **Not framework requirement:** Framework doesn't mandate dashboards
- **Repository-specific architecture:** WebSocket implementation, SQLite telemetry are project choices

**Note:** The ADR correctly states: "Our existing file-based orchestration approach MUST be maintained" - the dashboard *observes* the framework, but isn't part of it.

---

#### 20. ADR-043: Status Enumeration Standard

**Classification:** **REPOSITORY** ❌

**Rationale:**
- **Implementation choice:** Python enums in `src/common/types.py` are this repository's implementation
- **Technology-specific:** Python-specific enum patterns (str inheritance, Literal types)
- **Repository codebase:** Addresses specific modules in this repo (framework/, llm_service/)
- **Not framework architecture:** Framework defines *conceptual* states (ADR-003/DDR-005), but not Python implementation

**Note:** The *states themselves* (new, assigned, in_progress, done, error) are framework-level (in DDR-005), but the *Python enum implementation* is repository-specific.

---

## Recommended Actions

### Phase 1: Create New DDRs (7 total)

**Priority 1 - Core Framework Architecture (Must do first):**

1. **DDR-010: Modular Agent Directive System Architecture**
   - Source: ADR-001
   - Rationale: Foundation of framework structure
   - Effort: 3-4 hours (significant generalization needed)

2. **DDR-004: File-Based Asynchronous Coordination Protocol**
   - Source: ADR-008
   - Rationale: Core coordination mechanism
   - Effort: 2-3 hours

**Priority 2 - Task Lifecycle Patterns (Dependent on P1):**

3. **DDR-005: Task Lifecycle and State Management Protocol**
   - Source: ADR-003
   - Rationale: Fundamental task coordination pattern
   - Effort: 2-3 hours

4. **DDR-006: Work Directory Structure and Naming Conventions**
   - Source: ADR-004
   - Rationale: Required for file-based coordination
   - Effort: 2 hours

5. **DDR-007: Coordinator Agent Orchestration Pattern**
   - Source: ADR-005
   - Rationale: Meta-agent coordination pattern
   - Effort: 2-3 hours

**Priority 3 - Framework Distribution and Governance (Can be done in parallel):**

6. **DDR-008: Framework Distribution and Upgrade Mechanisms**
   - Source: ADR-013
   - Rationale: Framework portability and upgrade patterns
   - Effort: 2 hours

7. **DDR-009: Traceable Decision Patterns and Agent Integration**
   - Source: ADR-017
   - Rationale: Decision capture and linking in agent workflows
   - Effort: 2-3 hours

**Total Estimated Effort:** 15-20 hours

---

### Phase 2: Update Doctrine References

**After DDRs created:**

1. Update all doctrine files that currently reference these ADRs
2. Change references from `../../docs/architecture/adrs/ADR-XXX` to `./decisions/DDR-XXX.md`
3. Verify no broken links remain

**Files to update:** (From violations report)
- `doctrine/agents/architect.md`
- `doctrine/agents/coordinator.md`
- `doctrine/agents/curator.md`
- `doctrine/agents/developer.md`
- `doctrine/agents/lexical.md`
- `doctrine/agents/planning.md`
- `doctrine/agents/structural.md`
- `doctrine/agents/synthesizer.md`
- `doctrine/agents/writer-editor.md`
- `doctrine/core_specification.md`
- `doctrine/directives/002_context_notes.md`
- `doctrine/directives/004_documentation_context_files.md`
- `doctrine/directives/018_documentation_level_framework.md`
- `doctrine/guidelines/bootstrap.md`
- `doctrine/guidelines/general_guidelines.md`
- `doctrine/guidelines/operational_guidelines.md`
- `doctrine/tactical/file-based-orchestration.md`

**Effort:** 2-3 hours

---

### Phase 3: Maintain ADRs in Repository

**No changes needed for these ADRs - they remain in `docs/architecture/adrs/`:**

- ADR-002: OpenCode Portability Enhancement
- ADR-009: Orchestration Metrics Standard
- ADR-012: Test-Driven Development Mandate
- ADR-015: Follow-Up Task Lookup Pattern (Rejected)
- ADR-019: Trunk-Based Development
- ADR-020: Multi-Tier Agentic Runtime
- ADR-023: Prompt Optimization Framework (Proposed)
- ADR-028: Tool-Model Compatibility Validation
- ADR-032: Real-Time Execution Dashboard
- ADR-043: Status Enumeration Standard

**Add deprecation notices in original ADRs that were elevated:**

Each elevated ADR should have a notice added:

```markdown
> **⚠️ ELEVATED TO DOCTRINE**
> This ADR has been elevated to framework-level guidance.
> See: `doctrine/decisions/DDR-XXX-[title].md`
> 
> This repository-specific implementation reference is maintained for historical context.
```

---

## DDR Content Transformation Guidelines

When creating DDRs from ADRs, follow these transformation rules:

### 1. Generalize Implementation Details

**Remove:**
- Specific file paths in this repository
- Python/JavaScript code examples
- GitHub Actions workflows
- Repository-specific agent names
- This project's CI/CD configuration

**Keep:**
- Framework-level patterns and schemas
- Directory structure conventions
- YAML schema definitions
- Conceptual workflows and state machines
- Rationale and architectural principles

### 2. Elevate to Framework Language

**Transform:**
- "In this repository, we..." → "Repositories adopting this framework should..."
- "Our agents are..." → "Agents are defined as..."
- "We use Python to..." → "Implementations may use..."
- "GitHub Actions runs..." → "Automation systems should..."

### 3. Preserve Decision Context

**Keep:**
- Original decision rationale
- Alternatives considered
- Trade-offs accepted
- Consequences (positive and negative)
- Validation criteria

### 4. Add Framework-Level Metadata

**Add to each DDR:**
```yaml
---
framework_version: 1.0.0
category: [Architecture|Coordination|Distribution|Governance]
requires: [DDR-XXX, DDR-YYY]  # Dependencies on other DDRs
applies_to: [All|Coordinator|Agent|Distribution]
---
```

### 5. Structure Adjustments

**DDR Structure:**
1. Context (framework-level problem)
2. Decision (universal pattern/rule)
3. Rationale (why this benefits all adopters)
4. Implementation Guidance (how repositories should apply)
5. Validation Criteria (how to verify compliance)
6. Examples (multiple implementation approaches)
7. References (to related DDRs and framework docs)

---

## Validation Checklist

Before finalizing each DDR, verify:

- [ ] ✅ No repository-specific paths or names
- [ ] ✅ No technology-specific implementation code
- [ ] ✅ Decision applies to *any* framework adopter
- [ ] ✅ All references point to doctrine/ or framework docs
- [ ] ✅ Contains implementation guidance (not implementation)
- [ ] ✅ Includes examples from multiple perspectives
- [ ] ✅ Dependencies on other DDRs are explicit
- [ ] ✅ Original ADR has deprecation notice with DDR link
- [ ] ✅ All doctrine files referencing old ADR updated to new DDR

---

## Impact Assessment

### Benefits of Elevation

**Framework Portability:**
- Core patterns documented in doctrine for all adopters
- Clear boundary between framework and repository decisions
- Easier adoption by new repositories

**Consistency:**
- Framework-level decisions no longer mixed with repository-specific ADRs
- Doctrine violations eliminated (23 → 0)
- Clear governance hierarchy

**Maintainability:**
- Framework evolution separate from repository evolution
- DDRs can be versioned independently
- Clearer upgrade paths for adopters

### Risks and Mitigations

**Risk: Breaking existing references**
- Mitigation: Phase 2 updates all doctrine references before marking ADRs as deprecated

**Risk: Over-generalizing ADRs loses valuable context**
- Mitigation: Keep original ADRs with deprecation notices for historical reference

**Risk: Time investment (15-20 hours)**
- Mitigation: Prioritize core framework DDRs (DDR-004, DDR-010) first; others can follow

**Risk: Confusion during transition period**
- Mitigation: Add clear deprecation notices with forwarding links

---

## Open Questions

1. **Should ADR-009 (Metrics Standard) become framework guidance later?**
   - Current form is too prescriptive
   - Could be rewritten as "Framework Metrics Guidelines" (optional standards)
   - Decision: Keep as ADR for now, revisit in Q2 2026

2. **Should we version DDRs differently than ADRs?**
   - DDRs affect all framework adopters
   - Proposal: Use semantic versioning (DDR-010 v1.0.0)
   - Decision: Defer to separate versioning discussion

3. **How do we handle DDRs that supersede each other?**
   - DDR-004 (File-Based Coordination) is foundational to DDR-005 (Task Lifecycle)
   - Need clear dependency chain documentation
   - Decision: Add `requires:` metadata to each DDR

---

## Next Steps

**Immediate (This Sprint):**
1. ✅ Complete this analysis document
2. Review with Architect and Framework Guardian
3. Prioritize DDR-004 and DDR-010 (foundation)
4. Create first 2 DDRs and validate transformation approach

**Short-Term (Next 2 Sprints):**
5. Create remaining 5 DDRs (DDR-005 through DDR-009)
6. Update all 17 doctrine files with new references
7. Add deprecation notices to elevated ADRs
8. Validate no broken links

**Medium-Term (Q2 2026):**
9. Review ADR-009 for potential framework guidelines conversion
10. Establish DDR versioning strategy
11. Document DDR dependency chain
12. Create framework release notes referencing new DDRs

---

## Appendix: Summary Table

| ADR | Title | Classification | DDR | Priority | Effort |
|-----|-------|----------------|-----|----------|--------|
| ADR-001 | Modular Agent Directive System | FRAMEWORK ✅ | DDR-010 | P1 | 3-4h |
| ADR-002 | OpenCode Portability | REPOSITORY ❌ | - | - | - |
| ADR-003 | Task Lifecycle Management | FRAMEWORK ✅ | DDR-005 | P2 | 2-3h |
| ADR-004 | Work Directory Structure | FRAMEWORK ✅ | DDR-006 | P2 | 2h |
| ADR-005 | Coordinator Agent Pattern | FRAMEWORK ✅ | DDR-007 | P2 | 2-3h |
| ADR-008 | File-Based Async Coordination | FRAMEWORK ✅ | DDR-004 | P1 | 2-3h |
| ADR-009 | Orchestration Metrics | REPOSITORY ❌ | - | - | - |
| ADR-011 | Primer Execution Matrix | FRAMEWORK ✅ | DDR-001 | Done | 0h |
| ADR-012 | TDD Mandate | REPOSITORY ❌ | - | - | - |
| ADR-013 | Zip Distribution | FRAMEWORK ✅ | DDR-008 | P3 | 2h |
| ADR-014 | Framework Guardian | FRAMEWORK ✅ | DDR-002 | Done | 0h |
| ADR-015 | Follow-Up Lookup | REJECTED ❌ | - | - | - |
| ADR-017 | Traceable Decisions | FRAMEWORK ✅ | DDR-009 | P3 | 2-3h |
| ADR-019 | Trunk-Based Dev | REPOSITORY ❌ | - | - | - |
| ADR-020 | Multi-Tier Runtime | REPOSITORY ❌ | - | - | - |
| ADR-023 | Prompt Optimization | REPOSITORY ❌ | - | - | - |
| ADR-028 | Tool-Model Validation | REPOSITORY ❌ | - | - | - |
| ADR-032 | Real-Time Dashboard | REPOSITORY ❌ | - | - | - |
| ADR-043 | Status Enumeration | REPOSITORY ❌ | - | - | - |

**Total:** 7 new DDRs to create, ~15-20 hours effort

---

## Confidence Assessment

**Analysis Confidence:** 95%

**High Confidence Decisions:**
- ADR-001, ADR-003, ADR-004, ADR-005, ADR-008 are clearly framework-level (100% confident)
- ADR-011, ADR-014 already converted to DDRs (100% confident)
- ADR-012, ADR-019, ADR-028, ADR-032, ADR-043 are clearly repository-specific (100% confident)

**Medium Confidence Decisions:**
- ADR-013 (Zip Distribution): 85% confident it's framework-level - could argue it's a repository release process, but the "core vs. local boundary" pattern is framework-level
- ADR-017 (Traceable Decisions): 85% confident it's framework-level - the decision marker format is framework guidance, though the tooling is repo-specific

**Borderline Cases:**
- ADR-009 (Metrics Standard): 60% framework / 40% repository - current form is too prescriptive, but could become framework *guidance* later
- ADR-023 (Prompt Optimization): 70% repository / 30% framework - too repo-specific currently, but underlying patterns could be framework guidance

**Recommendation:** Proceed with high-confidence decisions first (DDR-004 through DDR-007 and DDR-010), then review borderline cases after transformation validates the approach.

---

## Document Metadata

**Prepared by:** Curator Claire (Structural & Tonal Consistency Specialist)  
**Analysis Date:** 2026-02-11  
**Review Status:** Awaiting Architect and Framework Guardian review  
**Version:** 1.0  
**Related Work:**
- `work/doctrine/2026-02-11-doctrine-violation-remediation-report.md` (Phase 1)
- `doctrine/decisions/DDR-001-primer-execution-matrix.md`
- `doctrine/decisions/DDR-002-framework-guardian-role.md`

**Next Reviewer:** Architect Alphonso
