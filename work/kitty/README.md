# The Unified Agentic Stack

**Date:** 2026-02-14  
**Status:** Proposed  
**Authors:** Architect Alphonso, Planning Petra, Manager Mike  
**Context:** Unification of Spec Kitty (SK) and Agentic Doctrine (AAD) into a single coherent framework

---

## Why Unify?

Two agent-augmented development systems evolved independently — **Spec Kitty** as a workflow
orchestrator, **Agentic Doctrine** as a behavioral governance framework. Analysis (see
[SUMMARY.md](./SUMMARY.md)) confirmed they are **complementary, not competing**: SK excels at
*what* gets done (lifecycle, missions, orchestration), while AAD excels at *how* it gets done
(governance, traceability, agent depth). Neither alone covers the full picture.

The goal is to **merge strengths, align concepts, and preserve backward compatibility** — creating
a unified stack that downstream projects can adopt incrementally through a
"build your own framework" configuration flow.

---

## The Unified Doctrine Stack

The unified stack extends Spec Kitty's existing architecture with AAD's governance depth,
organized into five conceptual layers. Each layer has clear ownership and well-defined boundaries.

```
┌─────────────────────────────────────────────────────────────────────┐
│  Layer 1 — Governance (Doctrine Extension)                         │
│  doctrine/: Guidelines · Approaches · Directives · Tactics         │
│  Constitution: Project-local governance overlay                    │
│  Precedence: General Guidelines > Operational > Constitution >     │
│              Directives > Mission guidance > Tactics/Templates     │
├─────────────────────────────────────────────────────────────────────┤
│  Layer 2 — Specification Domain (Spec Kitty Authority)             │
│  kitty-specs/: spec → plan → tasks → implement → review → accept  │
│  Missions: Domain-specific workflow profiles (software, research…) │
├─────────────────────────────────────────────────────────────────────┤
│  Layer 3 — Orchestration (Spec Kitty, extension-enabled)           │
│  WP lifecycle · Worktree isolation · Dependency scheduling         │
│  Event Bridge: Normalized events from all lifecycle transitions    │
├─────────────────────────────────────────────────────────────────────┤
│  Layer 4 — Routing (Spec Kitty, policy-informed)                   │
│  RoutingProvider API · Agent-to-model mapping · Fallback chains    │
│  DoctrinePolicyProvider: Routing hints from doctrine agent profiles│
├─────────────────────────────────────────────────────────────────────┤
│  Layer 5 — Execution                                               │
│  LLM vendor adapters · Telemetry store · Artifact capture          │
│  Budget enforcement · Cost tracking · Work log emission            │
└─────────────────────────────────────────────────────────────────────┘
```

**Visual reference:** [`proposal/spec-kitty-doctrine-layered-target-architecture.puml`](./proposal/spec-kitty-doctrine-layered-target-architecture.puml)  
**C4 diagram:** [`proposal/diagrams/unified-doctrine-stack.puml`](./proposal/diagrams/unified-doctrine-stack.puml)

---

## Constitution: The Local Governance Overlay

Both frameworks independently arrived at the same concept — a project-scoped customization layer
that tailors a general framework for a specific repository's needs:

| Aspect | Spec Kitty | Agentic Doctrine |
|--------|-----------|------------------|
| **Name** | Constitution | `.doctrine-config/` |
| **Form** | Narrative Markdown (human-first) | Structured YAML + Markdown (machine + human) |
| **Generation** | Interactive CLI questionnaire | Agent-generated during bootstrap |
| **Content** | Testing standards, code quality, branch strategy, tribal knowledge | Testing standards, code quality, model routing, custom agents, hooks |

In the unified stack, we adopt **"Constitution"** as the canonical term for this concept. It
represents the single project governance state with two complementary renderings:

- **Constitution Markdown** — Human-readable narrative (what SK generates)
- **`.doctrine-config/`** — Machine-parseable config (what AAD agents consume)

A bidirectional sync mechanism keeps both views consistent. The `spec-kitty init --doctrine`
flow generates both from the same questionnaire answers.

### Precedence Rule (Immutable)

The Doctrine instruction hierarchy is explicit and non-negotiable:

1. **Doctrine General Guidelines** — Immutable framework values
2. **Doctrine Operational Guidelines** — Immutable behavioral norms
3. **Constitution** (`.doctrine-config/`) — Project-specific customization
4. **Directives** — Explicit constraints (apply unless Constitution narrows scope)
5. **Mission guidance** — Domain-specific workflow context
6. **Tactics and Templates** — Execution patterns

Constitution **extends, narrows, and adds** project-specific rules. It **cannot contradict**
General or Operational Guidelines. This preserves framework integrity while enabling full
project customization — the same principle as SK's Constitution, now anchored in a formal
hierarchy.

---

## Missions and the "Build Your Own Framework" Flow

Spec Kitty's **Mission** system and AAD's **Approaches + Directives** serve the same need:
domain-specific behavioral adaptation. A software development mission needs different prompts,
validation rules, and artifact structures than a research or documentation mission.

The unified stack leverages both:

| Concern | Spec Kitty Missions | AAD Approaches + Directives |
|---------|--------------------|-----------------------------|
| **Domain context** | Mission profiles define prompts, rules, artifacts per domain | Approaches define mental models; Directives define constraints |
| **Activation** | `spec-kitty use-mission <name>` | `/require-directive <code>` |
| **Scope** | Per-feature or per-project | Cross-cutting (apply to all work) |

**The "build your own framework" vision:** A downstream project runs `spec-kitty init`, selects
a mission profile, optionally enables Doctrine governance, and gets a fully configured stack:

1. **Choose mission** → Sets domain context (software-dev, research, documentation)
2. **Answer Constitution questions** → Generates project governance (Constitution + `.doctrine-config/`)
3. **Select governance depth** → Opt into directives, approaches, agent profiles
4. **Start working** → Framework adapts to your choices

This maps naturally to the layered architecture: Mission configures Layer 2, Constitution
configures Layer 1, and the operator decides how much governance to enable.

---

## Agent Profiles: From Flat Keys to Rich Identities

One of AAD's clear strengths is its **rich agent profile model** — 20+ specialist profiles
with capabilities, handoff patterns, reasoning modes, and collaboration norms. Spec Kitty
currently uses flat agent config keys (`agent: claude-sonnet`) that identify a tool, not a
role.

The unified model bridges this gap:

```
SK agent config key ─→ AgentProfile lookup ─→ Rich identity
     "claude-sonnet"       doctrine/agents/       capabilities, tone,
                           architect.agent.md      directives, handoffs
```

**What AAD adds:**
- **Role specialization** — Architect, Backend Dev, Planner, Reviewer (not just "which LLM")
- **Capability declarations** — What an agent can/cannot do, in machine-readable form
- **Handoff patterns** — How agents collaborate and transfer context
- **Directive awareness** — Which governance rules each role must follow
- **Reasoning modes** — Analysis, creative, meta — with annotated transitions

**What SK provides:**
- **Tool binding** — Which LLM CLI/API to invoke for execution
- **Worktree isolation** — Each agent works in its own git worktree
- **Mission context** — Domain-specific prompts and artifact templates

The `RoutingProvider` in Layer 4 unifies these: given a task context, it selects both the
**role** (from Doctrine agent profiles) and the **tool** (from SK agent config), producing a
complete routing decision with fallback chains.

---

## The Feedback Loop: Traceability as a Learning System

A key gap in the current SK stack is **operator feedback** — the system executes work but
doesn't systematically help operators become better at using it. AAD addresses this through:

### Work Logs (Directive 014)

Structured records of what was done, what decisions were made, and what the outcomes were.
In the unified stack, these are **automatically generated** from lifecycle events:

```
Lane transition (WP moves from "doing" → "for_review")
  └── EventBridge.emit_lane_transition()
        ├── WorkLogEmitter.record()        → Structured work log entry
        ├── TelemetryStore.append()        → Cost/time/token metrics
        └── GovernancePlugin.validate()    → Compliance check result
              └── EventBridge.emit_validation_event()
```

### Prompt Documentation (Directive 015)

Captures the prompts used, their effectiveness, and improvement opportunities (SWOT analysis).
This creates an institutional memory that improves prompt quality over time.

### The Unified Event Spine

Both feedback mechanisms attach to the same **Event Bridge** — the normalized event stream
from Layer 3. Every lifecycle transition, governance check, and agent execution is an event.
Adding new feedback concerns (cost dashboards, performance benchmarks, agent skill tracking)
requires only a new EventBridge consumer — zero changes to the orchestrator.

**Practical result:** Operators and maintainers accumulate structured knowledge about:
- Which prompts work well for which tasks
- Which agents perform best on which work types
- Where governance checks catch real issues vs. false positives
- How cost and token usage trend over time

This turns the framework from a tool into a **learning system** that improves with use.

---

## Alignment Principles

These principles govern how we merge the two frameworks:

### 1. Spec Kitty Owns Workflow

Lifecycle commands, mission execution, worktree orchestration, and the spec-driven development
methodology remain Spec Kitty's authority. The unified stack does not replace or duplicate SK's
workflow engine.

### 2. Doctrine Extends Governance

The Doctrine stack (Guidelines → Approaches → Directives → Tactics → Templates) provides
behavioral governance as an **optional extension**. Projects that don't need governance run
pure Spec Kitty unchanged. Projects that enable it gain layered policy enforcement,
decision traceability, and agent profile depth.

### 3. Constitution Unifies Project Configuration

A single project governance state, rendered as both human narrative (Constitution) and machine
config (`.doctrine-config/`), replaces the dual-authority risk. The "build your own framework"
flow generates both from the same inputs.

### 4. Events Enable Everything Else

The Event Bridge is the universal integration point. Telemetry, work logs, governance checks,
dashboards, cost tracking, and future concerns all consume the same event stream. This keeps
the core orchestrator lean while enabling rich observability.

### 5. Backward Compatibility by Default

No forced migration. Existing SK projects work unchanged. Existing Doctrine projects work
unchanged. Enabling the unified stack is additive — `spec-kitty init --doctrine` adds
governance; removing it returns to pure SK.

### 6. Keep What Works, Bridge What Differs

Where concepts align (Constitution ↔ `.doctrine-config/`, WP ↔ Feature, Worktree ↔ Run
Container), we converge on a single term and model. Where concepts don't have a counterpart
(Missions in SK, Directive 014/015 in AAD), we preserve them as unique strengths and provide
bridge points for cross-system interaction.

---

## Concept Alignment Summary

| Unified Concept | Spec Kitty Origin | AAD Origin | Status |
|----------------|-------------------|------------|:------:|
| **Constitution** | Constitution (narrative) | `.doctrine-config/` (structured) | ✅ Converged |
| **Governance Stack** | — (no equivalent) | Doctrine layers (Guidelines→Templates) | ✅ Extension |
| **Mission** | Mission profiles | Approaches + Directives | 🟡 Bridge needed |
| **Agent Profile** | Flat agent config key | 20+ rich specialist profiles | 🟡 Bridge built in Layer 4 |
| **Work Package** | WP (kanban lanes) | Feature / Batch | ✅ Direct mapping |
| **Lifecycle Events** | Lane transitions | — (no event system) | ✅ Event Bridge |
| **Traceability** | — (thin) | Directives 014, 015 (work logs, prompt docs) | ✅ Extension |
| **Telemetry** | — (gap) | — (designed, not built) | 🔨 Build in Phase 1 |
| **Routing** | Model-agnostic (no routing) | RoutingProvider design | 🔨 Build in Phase 3 |
| **Quality Gates** | Merge preflight, validators | Governance hooks (pass/warn/block) | ✅ Complementary |
| **Workspace Isolation** | Git worktrees | Run Container (ADR-048) | ✅ Direct mapping |

---

## What's Next

The [EXECUTION_ROADMAP.md](./proposal/EXECUTION_ROADMAP.md) details six phases of implementation.
The immediate priorities are:

1. **Phase 1 — Telemetry & Observability** — Build the event infrastructure that both systems
   need (EventBridge, TelemetryStore, WorkLogEmitter)
2. **Phase 2 — Governance Extension** — Implement the GovernancePlugin interface, Constitution
   sync, and directive loader
3. **Upstream Collaboration** — Engage with Spec Kitty maintainers on extension points needed
   in the SK orchestrator

For navigation across all analysis, proposal, and status documents, see [INDEX.md](./INDEX.md).

---

## Document Map

| Document | Purpose |
|----------|---------|
| **This README** | Unified architecture narrative and alignment principles |
| [INDEX.md](./INDEX.md) | Complete navigation index with reading order by role |
| [SUMMARY.md](./SUMMARY.md) | Phase 0 analysis summary |
| [proposal/ARCHITECTURE_SPEC.md](./proposal/ARCHITECTURE_SPEC.md) | Technical specification (interfaces, layers, acceptance criteria) |
| [proposal/EXECUTION_ROADMAP.md](./proposal/EXECUTION_ROADMAP.md) | 6-phase implementation plan (34 work packages) |
| [proposal/COORDINATION.md](./proposal/COORDINATION.md) | Decision log, risk register, stakeholder map |
| [proposal/VISION.md](./proposal/VISION.md) | Long-term strategic vision |
| [glossary/](./glossary/) | Terminology mapping across both frameworks |
| [sddev_stack_reference/](./sddev_stack_reference/) | AAD architecture diagrams (PlantUML) |

### Architecture Diagrams (PlantUML)

| Diagram | Style | Source |
|---------|-------|--------|
| [`proposal/diagrams/unified-doctrine-stack.puml`](./proposal/diagrams/unified-doctrine-stack.puml) | C4 Container | 5-layer architecture stack |
| [`proposal/diagrams/unified-event-spine.puml`](./proposal/diagrams/unified-event-spine.puml) | Sequence | Event Bridge fan-out pattern |
| [`proposal/diagrams/phase-dependency-dag.puml`](./proposal/diagrams/phase-dependency-dag.puml) | State / DAG | Phase dependency graph with critical path |
| [`proposal/diagrams/agent-profile-bridge.puml`](./proposal/diagrams/agent-profile-bridge.puml) | C4 Component | Agent config → rich identity → routing |
| [`proposal/spec-kitty-doctrine-layered-target-architecture.puml`](./proposal/spec-kitty-doctrine-layered-target-architecture.puml) | Rectangle | Full target architecture (original) |
| [`analysis/spec-kitty-doctrine-layered-integration.puml`](./analysis/spec-kitty-doctrine-layered-integration.puml) | C4 Container | Coverage analysis integration map |
