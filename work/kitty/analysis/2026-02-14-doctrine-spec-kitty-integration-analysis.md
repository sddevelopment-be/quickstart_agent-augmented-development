# Doctrine x Spec Kitty Integration Analysis

**Date:** 2026-02-14
**Author:** Architect Alphonso
**Status:** Draft -- Pending Human Review
**Traceability:** Directive 018 (Traceable Decisions), ADR-045, ADR-046
**Prior Art:** `doctrine/docs/references/comparative_studies/2026-02-05-spec-kitty-comparative-analysis.md`, `docs/architecture/design/spec-kitty-inspired-enhancements.md`

---

## Executive Summary

This document analyzes how the **Agentic Doctrine** governance framework and **Spec Kitty** workflow orchestration tool could integrate. The two systems operate at different but complementary layers of the agent-augmented development stack: Doctrine governs *how agents behave*, while Spec Kitty governs *what agents work on and in what order*. Neither system fully subsumes the other, but there are meaningful overlaps in configuration, agent identity, and project initialization that create both integration opportunities and friction points.

The recommended path forward is **Option C: Doctrine as External Dependency**, where Spec Kitty projects can optionally pull in the Doctrine governance stack via a git subtree into `.kittify/doctrine/`, with the Constitution acting as a gateway document that references Doctrine layers. This approach preserves both systems' independence, requires the fewest changes to either system, and leverages the distribution mechanism Doctrine already uses.

---

## 1. Architectural Vision Alignment

### 1.1 Core Philosophies Compared

**Spec Kitty** centers on a *workflow orchestration* model. Its fundamental unit of work is the **feature lifecycle**: specifications describe deltas from the current state, plans decompose those deltas into work packages, agents execute work packages in isolated worktrees, and lane transitions track progress. The system assumes agents are already running and provides them with context and coordination -- it does not invoke agents directly. Its governing metaphor is a **kanban board with work package routing**.

**Agentic Doctrine** centers on a *behavioral governance* model. Its fundamental concern is: given an agent operating in a repository, what should it do, how should it reason, what constraints apply, and what output shape is expected? The Doctrine Stack (Guidelines, Approaches, Directives, Tactics, Templates) externalizes judgment so agents behave predictably. Its governing metaphor is a **layered policy stack with precedence rules**.

### 1.2 Where They Naturally Complement Each Other

The two systems address orthogonal concerns that together form a more complete agent-augmented development environment:

| Concern | Spec Kitty | Doctrine | Combined |
|---------|-----------|----------|----------|
| What to work on next | Work package lanes, dependency tracking | Not addressed | SK provides work selection |
| How to behave while working | Constitution (lightweight) | Doctrine Stack (deep) | Doctrine enriches behavioral governance |
| What shape output takes | Spec/plan/task templates | Template layer | Both contribute output contracts |
| How to coordinate agents | WP lanes, frontmatter status | File-based YAML tasks in `work/collaboration/` | Overlapping but different granularity |
| How to initialize a project | `spec-kitty init` + missions | Bootstrap protocol + `.doctrine-config/` | Complementary initialization |
| How to track decisions | Not explicit (specs capture intent) | ADRs, traceable decisions (Directive 018) | Doctrine adds decision traceability |

**Key insight:** Spec Kitty tells agents *what to do*; Doctrine tells agents *how to do it well*. A project using both would have stronger coverage of the agent-augmented development lifecycle.

### 1.3 Where They Potentially Conflict or Overlap

**Agent identity and configuration.** Spec Kitty manages agents via `.kittify/config.yaml` with a simple key-based model (`claude`, `codex`, `cursor`). Doctrine defines rich agent profiles (`.agent.md` files) with capabilities, directive requirements, and collaboration contracts. If both systems are active in a project, the question of "who is the authority on what an agent is?" becomes ambiguous.

**Coordination mechanisms.** Spec Kitty tracks work via frontmatter lanes in flat task files. Doctrine tracks work via YAML task files moving through directory-based lifecycles (`assigned/ -> in_progress/ -> done/`). These are conceptually similar but structurally incompatible. Running both would create two parallel coordination systems.

**Project-level principles.** Spec Kitty's Constitution (`.kittify/memory/constitution.md`) and Doctrine's Guidelines layer both claim to be the top-level behavioral authority for agents. Without explicit precedence, agents receiving context from both could encounter contradictory instructions.

**Template ownership.** Both systems define templates for output artifacts. Spec Kitty has spec/plan/task templates; Doctrine has ADR/tactic/agent-task templates. The overlap is limited (different artifact types) but the pattern is duplicated.

---

## 2. Concept Mapping

| Doctrine Concept | Spec Kitty Equivalent | Alignment | Notes |
|---|---|---|---|
| **Doctrine Stack** (5 layers) | Constitution + Mission config | Partial | Constitution approximates Guidelines; Mission approximates Approaches + Templates. Doctrine has three additional layers (Directives, Tactics, Templates) with no SK equivalent. |
| **Agent Profiles** (`.agent.md`) | Agent keys in `config.yaml` | Weak | Doctrine profiles define capabilities, directive refs, collaboration contracts. SK has flat key-value config. The concepts are related but at different fidelity levels. |
| **Directives** (numbered constraints) | No equivalent | Gap | SK has no explicit constraint/instruction system. The Constitution provides general principles but not numbered, enforceable rules. |
| **Tactics** (procedural steps) | Workflow commands (`implement`, `review`) | Partial | Both are procedural. SK workflow phases are lifecycle-oriented (plan, implement, review); Doctrine tactics are task-oriented (code-review, premortem, stopping-conditions). Different granularity. |
| **Approaches** (mental models) | Mission philosophy | Loose | Doctrine approaches are reasoning models (trunk-based dev, locality of change). SK missions are workflow adapters (software-dev, research, documentation). Related but not interchangeable. |
| **Templates** (output contracts) | Spec/Plan/Task templates | Strong | Both define required output structure. Different artifact types, same pattern. |
| **Bootstrap Protocol** | `spec-kitty init` + constitution | Partial | Both initialize agent context at project start. Doctrine bootstrap loads the governance stack; SK init creates directory structure and templates. |
| **File-based collaboration** (`work/collaboration/`) | WP lanes + frontmatter | Moderate | Both use file-based async coordination. Doctrine uses directory-based state machines; SK uses in-file frontmatter fields. Structurally different, conceptually similar. |
| **`.doctrine-config/`** | `.kittify/` | Strong | Both are project-level config directories for local overrides and customization. |
| **Work logs** | Activity logs in WP frontmatter | Partial | Doctrine logs are per-agent markdown files. SK logs are inline in task frontmatter. Doctrine has richer logging requirements. |
| **Domain model** (ADR-045 dataclasses) | No equivalent | Gap | SK has no runtime domain model for its governance concepts. |
| **Multi-format export** (Parser, IR, Generators) | Template-based command generation | Partial | Both generate agent-specific artifacts. Doctrine exports to Claude/Copilot/OpenCode formats; SK generates slash command files per agent. Different outputs, related pattern. |
| **Bounded contexts** (ADR-046) | `missions/` separation | Weak | Doctrine has formal bounded contexts (doctrine, collaboration, specifications). SK separates by mission type but without explicit boundary contracts. |

### Alignment Summary

- **Strong alignment:** Template patterns, project config directories, config-driven agent management
- **Partial alignment:** Initialization, coordination, approaches/missions, output generation
- **Gaps in SK:** Directives (constraints), domain model, precedence system, rich agent profiles
- **Gaps in Doctrine:** Workflow lifecycle management, git worktree isolation, live dashboard, spec-as-delta philosophy

---

## 3. Integration Architecture Options

### Option A: Doctrine as a Mission Type

**Concept:** Create a `governance` mission within Spec Kitty that wraps the Doctrine Stack. The mission defines workflow phases that map to doctrine layers (e.g., "load guidelines before working", "apply directives during implementation", "use templates for output").

**How it would work:**
- `missions/governance/mission.yaml` references doctrine layers as workflow context
- Constitution becomes the entry point that loads Guidelines
- Mission phases inject relevant directives and tactics
- Agent context enrichment pulls from Doctrine agent profiles

**Trade-offs:**

| Factor | Assessment |
|--------|------------|
| Changes to SK | Medium -- new mission type, agent context enrichment |
| Changes to Doctrine | Low -- package doctrine artifacts as mission-compatible structure |
| Coupling | High -- Doctrine becomes deeply embedded in SK's mission system |
| Portability | Low -- Doctrine artifacts bound to SK's mission format |
| Independence | Lost -- Doctrine cannot operate without SK infrastructure |

**Verdict: Not recommended.** Forcing Doctrine into SK's mission model distorts its identity. Missions are workflow adapters; Doctrine is a behavioral governance layer. The abstraction mismatch would create maintenance friction and limit Doctrine's use outside Spec Kitty contexts.

### Option B: Doctrine as a Plugin/Extension System

**Concept:** `.kittify/doctrine/` as a subdirectory holding doctrine artifacts. Spec Kitty's constitution references doctrine guidelines. Slash commands load doctrine layers as additional context.

**How it would work:**
- `.kittify/doctrine/` mirrors the doctrine structure (guidelines/, directives/, etc.)
- Constitution includes: "Load and follow principles from `doctrine/guidelines/`"
- Slash command templates reference doctrine directives where relevant
- No formal SK code changes -- purely file-based integration

**Trade-offs:**

| Factor | Assessment |
|--------|------------|
| Changes to SK | Low -- no code changes, convention-based |
| Changes to Doctrine | Low -- package for `.kittify/` subdirectory |
| Coupling | Low -- file convention only |
| Portability | Medium -- Doctrine artifacts portable but placed in SK-specific location |
| Independence | Preserved -- both systems work independently |
| Discoverability | Low -- agents need to know to look in `.kittify/doctrine/` |

**Verdict: Viable but fragile.** The absence of formal integration points means agents may or may not load doctrine context consistently. There is no enforcement mechanism -- it depends on constitution text and agent compliance.

### Option C: Doctrine as External Dependency (git subtree)

**Concept:** Similar to how Doctrine currently distributes to consuming repositories via git subtree. `spec-kitty init --doctrine` (or a separate manual step) pulls the doctrine stack into `.kittify/doctrine/` or a top-level `doctrine/` directory. The Constitution references doctrine principles. Agent command templates are enriched with directive references.

**How it would work:**
- Doctrine distributed via git subtree (existing mechanism)
- Located at `doctrine/` (project root) or `.kittify/doctrine/`
- Constitution acts as a gateway: "This project follows Agentic Doctrine governance. See `doctrine/DOCTRINE_STACK.md` for the behavioral governance framework."
- SK agent command templates include: "Before implementing, load relevant directives from `doctrine/directives/`"
- `.doctrine-config/` holds project-local overrides (existing pattern)
- Both systems' config directories coexist: `.kittify/` for workflow, `.doctrine-config/` for governance

**Trade-offs:**

| Factor | Assessment |
|--------|------------|
| Changes to SK | Low -- optional `--doctrine` flag on init; enriched templates |
| Changes to Doctrine | Very low -- already distributes via git subtree |
| Coupling | Very low -- git subtree is a loose dependency |
| Portability | High -- Doctrine stays in standard structure |
| Independence | Fully preserved -- either system works alone |
| Versioning | Strong -- git subtree provides version pinning |
| Discoverability | Medium -- constitution gateway + template references |

**Verdict: Recommended.** This option leverages existing distribution mechanisms, preserves both systems' independence, and provides the cleanest separation of concerns. The constitution-as-gateway pattern is lightweight and compatible with how both systems already work.

### Option D: Bidirectional Integration

**Concept:** Doctrine repos get Spec Kitty's workflow orchestration (spec lifecycle, WP lanes, worktree isolation). Spec Kitty repos get Doctrine's governance depth (directives, rich profiles, precedence). Both `.doctrine-config/` and `.kittify/` coexist.

**How it would work:**
- Projects can adopt both independently
- Shared concepts use adapter interfaces (e.g., agent identity mapping)
- A thin integration layer translates between coordination systems
- Both systems maintain their own config but share references

**Trade-offs:**

| Factor | Assessment |
|--------|------------|
| Changes to SK | Medium -- adapter interfaces, agent identity enrichment |
| Changes to Doctrine | Medium -- SK-compatible collaboration mode, WP awareness |
| Coupling | Medium -- adapter layer creates dependency surface |
| Portability | High -- both systems work independently |
| Complexity | High -- maintaining bidirectional compatibility is ongoing work |
| Value | Highest -- users get full capabilities of both |

**Verdict: Aspirational but premature.** This is the eventual desired state, but attempting it now would spread development effort too thin. Pursue Option C first, then evolve toward Option D as both systems mature and real integration usage patterns emerge.

### Decision Matrix

| Criterion (weight) | Option A: Mission | Option B: Plugin | Option C: Subtree | Option D: Bidirectional |
|---|---|---|---|---|
| Preserves independence (high) | Poor | Good | Excellent | Good |
| Minimal changes needed (high) | Medium | Good | Excellent | Poor |
| Leverages existing mechanisms (medium) | Poor | Medium | Excellent | Medium |
| Long-term extensibility (medium) | Poor | Medium | Good | Excellent |
| Agent discoverability (medium) | Good | Poor | Medium | Good |
| **Overall** | **Not recommended** | **Viable fallback** | **Recommended** | **Future target** |

---

## 4. Changes Needed in Spec Kitty

For Option C (recommended), Spec Kitty needs minimal but specific changes:

### 4.1 Constitution Gateway Pattern (Priority: High)

The constitution template should support an optional doctrine reference block:

```markdown
## Governance Framework

This project follows Agentic Doctrine governance.
See `doctrine/DOCTRINE_STACK.md` for the behavioral governance framework.

### Precedence
1. This Constitution (project-level principles)
2. Doctrine Guidelines (enduring values)
3. Doctrine Directives (explicit constraints)
4. Mission-specific workflow guidance
5. Doctrine Tactics and Templates (execution)
```

**Rationale:** This establishes clear precedence between SK's Constitution and Doctrine's layers, resolving the authority conflict identified in Section 1.3.

### 4.2 Agent Profile Enrichment Hook (Priority: Medium)

Spec Kitty's agent config could reference Doctrine profiles for richer context:

```yaml
# .kittify/config.yaml (enhanced)
agents:
  available:
    - claude
    - codex
  doctrine_profiles:
    claude: doctrine/agents/python-pedro.agent.md
    codex: doctrine/agents/backend-dev.agent.md
```

**Rationale:** This bridges the gap between SK's simple agent keys and Doctrine's rich profiles without requiring SK to parse Doctrine's profile format. The mapping is advisory -- agents that support Doctrine will load the profile; others ignore it.

### 4.3 Command Template Enrichment (Priority: Medium)

Slash command templates generated by `spec-kitty init` could include doctrine directive references where relevant:

```markdown
<!-- .claude/commands/implement.md (enriched) -->
Before implementing, review applicable governance:
- `doctrine/directives/016_acceptance_test_driven_development.md` (test-first)
- `doctrine/directives/018_traceable_decisions.md` (document decisions)
- `doctrine/directives/026_commit_protocol.md` (commit format)
```

**Rationale:** This is the lightest-touch integration -- plain text references in generated templates. No code changes in SK required; just updated template content.

### 4.4 Init Flag for Doctrine Setup (Priority: Low)

An optional `--doctrine` flag on `spec-kitty init` could automate doctrine subtree setup:

```bash
spec-kitty init --doctrine https://github.com/org/doctrine-repo
```

**Rationale:** Convenience feature. Not required for integration -- users can set up the git subtree manually. Worth adding only after the integration pattern is validated in practice.

### 4.5 Directive Enforcement Hooks (Priority: Future)

For deeper integration (Option D territory), SK would need:
- Pre-workflow hooks that validate directive compliance
- Post-workflow hooks that check output against template requirements
- A constraint evaluation system that reads directive metadata

**Rationale:** This is aspirational. Defer until real-world usage reveals which enforcement points provide value.

---

## 5. Changes Needed in Doctrine

### 5.1 Spec Kitty Compatibility Documentation (Priority: High)

A guide in `doctrine/docs/` explaining how to use Doctrine in a Spec Kitty project:
- Where to place doctrine artifacts
- How to reference them from the Constitution
- Which directives are most relevant to SK workflows
- How agent profiles map to SK agent keys

**Rationale:** Documentation is the highest-leverage, lowest-risk change. It enables integration without any code changes.

### 5.2 Constitution-Aware Guidelines (Priority: Medium)

The bootstrap protocol (`guidelines/bootstrap.md`) should acknowledge that in SK-enabled projects, the Constitution is the top-level document, and Doctrine loads as a referenced governance layer rather than the root authority.

A conditional block in the bootstrap sequence:

```
If `.kittify/` exists alongside `doctrine/`:
  - Constitution is the project-level root document
  - Doctrine Guidelines extend Constitution principles
  - Doctrine Directives apply unless Constitution explicitly overrides
```

**Rationale:** This resolves the "two masters" problem by establishing conditional precedence. In standalone Doctrine repos, Guidelines remain the root. In SK+Doctrine repos, Constitution outranks Guidelines on project-specific matters but Doctrine provides the deeper behavioral framework.

### 5.3 Work Package Awareness in Collaboration System (Priority: Low)

The file-based collaboration system (`work/collaboration/`) could optionally read WP lane state from SK task frontmatter, enabling the collaboration dashboard to show SK work packages alongside native Doctrine tasks.

**Rationale:** Nice-to-have for teams using both systems. Defer until there is real demand. The two coordination systems can coexist without interoperating -- agents simply use whichever system applies to their current task.

### 5.4 Lane-Based Status Compatibility (Priority: Low)

Doctrine's task status lifecycle (`new -> assigned -> in_progress -> done -> archive`) and SK's lane model (`planned -> doing -> for_review -> done`) differ. An optional mapping could be defined:

| Doctrine Status | SK Lane | Notes |
|---|---|---|
| new | planned | Both represent "ready but not started" |
| assigned | planned | Doctrine has an explicit assignment step |
| in_progress | doing | Direct equivalent |
| (no equivalent) | for_review | Doctrine delegates review via separate tasks |
| done | done | Direct equivalent |
| archive | (no equivalent) | Doctrine has an archival phase |

**Rationale:** This mapping is informational, not enforced. Useful for documentation and for future adapter code.

### 5.5 Mission-Aware Doctrine Configuration (Priority: Future)

For Option D integration, `.doctrine-config/` could support mission-specific overrides:

```
.doctrine-config/
  specific_guidelines.md
  missions/
    software-dev/
      directives/  # Additional directives for software missions
    research/
      approaches/  # Research-specific approaches
```

**Rationale:** This mirrors SK's mission-based workflow customization at the Doctrine governance level. Premature now; valuable if bidirectional integration becomes a reality.

---

## 6. Recommended Plan of Action

### Phase 1: Foundation Alignment (1-2 weeks)

**Goal:** Establish shared understanding and terminology without code changes.

**Deliverables:**
1. **Terminology mapping document** -- Finalize the concept mapping table (Section 2) as a shared reference. Publish in `doctrine/docs/references/`.
2. **Constitution gateway template** -- Write a sample constitution block showing how to reference Doctrine from an SK project. Publish in `doctrine/docs/guides/`.
3. **Integration guide** -- Document the recommended directory layout for projects using both systems. Include in Doctrine's distribution docs.

**Decision required:** Where should doctrine artifacts live in an SK project -- `doctrine/` at project root (consistent with Doctrine's standard layout) or `.kittify/doctrine/` (contained within SK's config directory)?

**Trade-off analysis for this decision:**
- `doctrine/` at root: Consistent with non-SK projects, visible, standard. But `.kittify/` users expect everything project-config related to be under `.kittify/`.
- `.kittify/doctrine/`: Contained, consistent with SK conventions. But non-standard for Doctrine, requires subtree path customization.
- **Recommendation:** `doctrine/` at project root. Doctrine is a governance framework that transcends any single tool. Placing it at root signals its cross-cutting authority and keeps the git subtree path standard.

### Phase 2: Proof of Concept (2-4 weeks)

**Goal:** Validate the integration pattern with a real project.

**Deliverables:**
1. **Reference project** -- Create a sample repository that has both `.kittify/` and `doctrine/` configured. Include a Constitution that references Doctrine, and SK command templates enriched with directive references.
2. **Agent behavior validation** -- Test whether agents (Claude, Copilot) can follow both SK workflow commands and Doctrine behavioral constraints in the same session.
3. **Friction log** -- Document what breaks, what confuses agents, and what works well. Capture in a structured report.

**Success criteria:**
- An agent can receive a work package from SK, load relevant Doctrine directives, implement the work following Doctrine's TDD cycle (Directive 017), and move the WP to the review lane.
- No contradictory instructions reach the agent from the two systems simultaneously.

### Phase 3: Integration Design (4-8 weeks, after Phase 2 validation)

**Goal:** Formalize the integration pattern based on Phase 2 learnings.

**Deliverables:**
1. **ADR for integration pattern** -- Document the chosen integration architecture, alternatives considered, and rationale. Include Phase 2 findings.
2. **SK changes specification** -- If Phase 2 reveals needed code changes in SK (e.g., `--doctrine` init flag, agent profile enrichment), write a formal spec per SK's contribution process.
3. **Doctrine changes implementation** -- Implement any needed Doctrine changes (bootstrap conditional, compatibility docs).
4. **Precedence specification** -- Formal document defining the authority hierarchy when both systems are active.

### Phase 4: Implementation (timeline depends on Phase 3 scope)

**Goal:** Ship the integration to users.

**Deliverables:**
1. **Doctrine distribution update** -- Ensure git subtree works in SK project contexts.
2. **SK template updates** -- Enriched command templates referencing Doctrine (if SK maintainers agree).
3. **User documentation** -- Getting started guide for "Using Doctrine with Spec Kitty".
4. **Validation suite** -- Tests confirming the integration works as designed.

---

## 7. Risks and Mitigations

| Risk | Severity | Likelihood | Mitigation |
|---|---|---|---|
| **Two-masters problem:** Agents receive contradictory guidance from Constitution and Guidelines | High | Medium | Phase 1 precedence specification; Constitution gateway pattern with explicit override rules |
| **Context window pressure:** Loading both SK context and Doctrine governance exhausts agent token budgets | Medium | High | Doctrine's load-on-demand pattern (numbered directives, scoped tactics); only load what's relevant to current WP |
| **Coordination confusion:** Two parallel task tracking systems (WP lanes vs. collaboration tasks) | Medium | Medium | Clear guidance: use SK lanes for feature work, Doctrine collaboration for governance/maintenance tasks |
| **Maintenance burden:** Two governance systems to keep aligned | Medium | High | Phase 1 mapping document; annual alignment review; option to use either system standalone |
| **SK community resistance:** SK maintainers may not want Doctrine-specific hooks | Low | Medium | Option C requires zero SK code changes; enriched templates are community contributions, not core changes |

---

## 8. Open Questions

1. **Is there appetite from the Spec Kitty maintainer community for this integration?** This analysis assumes willingness. Phase 2 should include outreach.

2. **Should Doctrine's export pipeline generate SK-compatible command templates?** The multi-format export system (Parser, IR, Generators) could include a Spec Kitty generator. This would be a Phase 3/4 feature.

3. **How does the domain model (ADR-045) represent SK concepts?** The `src/domain/specifications/` bounded context already has `Specification` and `Feature` types. Do these align with SK's feature specs, or do they need adaptation?

4. **What is the token cost of loading both systems' context?** Empirical measurement in Phase 2 will determine whether the combined governance overhead is practical within current model context windows.

---

## 9. References

### Internal Documents
- `doctrine/DOCTRINE_STACK.md` -- Five-layer governance model
- `docs/architecture/adrs/ADR-045-doctrine-concept-domain-model.md` -- Domain model
- `docs/architecture/adrs/ADR-046-domain-module-refactoring.md` -- Bounded contexts
- `docs/architecture/design/spec-kitty-inspired-enhancements.md` -- Prior integration design
- `doctrine/docs/references/comparative_studies/2026-02-05-spec-kitty-comparative-analysis.md` -- Comparative analysis
- `doctrine/directives/034_spec_driven_development.md` -- SDD directive
- `doctrine/approaches/spec-driven-development.md` -- SDD approach

### External References
- Spec Kitty repository: `https://github.com/Priivacy-ai/spec-kitty`
- Spec Kitty mission system documentation (analyzed from source)
- Spec Kitty constitution pattern (analyzed from source)

---

**Document Status:** Draft -- Awaiting human review and Phase 1 decision on directory placement.
**Next Action:** Human review of Option C recommendation and Phase 1 deliverables.
