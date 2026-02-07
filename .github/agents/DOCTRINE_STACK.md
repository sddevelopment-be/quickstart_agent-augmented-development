# Doctrine Stack: Agentic Development Framework

**Version:** 1.0.0  
**Last Updated:** 2026-02-07  
**Purpose:** Conceptual reference for the layered instruction system governing agent behavior

---

## What a Doctrine Stack Is

A **doctrine stack** is a layered system of documents that governs how LLM agents operate within a development environment. Its purpose is to externalize judgment, preference, and execution discipline so that agents do not have to infer intent from prompts, conversations, or implicit context.

The doctrine stack makes agent behavior **predictable, inspectable, and repeatable**.

Rather than treating an agent as a conversational partner, the doctrine stack treats it as an **executor operating under doctrine**: a clearly articulated set of rules, mental models, and procedures.

---

## The Five Layers

A doctrine stack separates concerns deliberately. Each layer has a distinct role—overlap is a design smell.

### 1. Guidelines

**Location:** `.github/agents/guidelines/*.md`  
**Purpose:** Enduring values, preferences, and guardrails  
**Role:** Define *how work should feel* and *what to optimize for or avoid*

**Examples:**
- `general_guidelines.md` — Broad operational principles, collaboration ethos
- `operational_guidelines.md` — Tone, honesty, reasoning discipline
- `bootstrap.md` — Initialization protocol

**Characteristics:**
- Highest precedence (after bootstrap protocol)
- Rarely change
- Shape all downstream decisions
- Provide "north star" for agent behavior

### 2. Approaches

**Location:** `.github/agents/approaches/*.md`  
**Purpose:** Conceptual models and philosophies for reasoning  
**Role:** Explain *how problems are generally framed and explored*

**Examples:**
- `trunk-based-development.md` — Branching strategy philosophy
- `decision-first-development.md` — Decision capture workflow
- `locality-of-change.md` — Premature optimization avoidance

**Characteristics:**
- Justify *why* certain tactics or directives exist
- Provide mental models for systemic reasoning
- Guide problem framing, not execution
- Support strategic alignment

### 3. Directives

**Location:** `.github/agents/directives/XXX_name.md`  
**Purpose:** Explicit instructions or constraints  
**Role:** Select *what must be done or not done in a specific situation*

**Examples:**
- `011_risk_escalation.md` — When and how to escalate issues
- `018_traceable_decisions.md` — Decision documentation requirements
- `026_commit_protocol.md` — Commit message format and workflow

**Characteristics:**
- Numbered (001-026+) for load-on-demand efficiency
- Prescriptive, not descriptive
- Select tactics, constrain approaches
- Enforce compliance boundaries

### 4. Templates

**Location:** `docs/templates/`  
**Purpose:** Structural output contracts  
**Role:** Define *what shape results must take*

**Examples:**
- `architecture/adr.md` — Architecture Decision Record structure
- `tactic.md` — Tactic document structure
- `agent-tasks/*.yaml` — Task descriptor schemas

**Characteristics:**
- Cross-cutting (serve humans and agents)
- Define required sections, not content
- Enable consistent artifact structure
- Reduce cognitive load during creation

### 5. Tactics

**Location:** `.github/agents/tactics/*.tactic.md`  
**Purpose:** Procedural execution guides  
**Role:** Define *how a specific task is carried out, step by step*

**Examples:**
- `stopping-conditions.tactic.md` — Define exit criteria for tasks
- `premortem-risk-identification.tactic.md` — Project failure mode discovery
- `adversarial-testing.tactic.md` — Stress-test proposals and designs
- `safe-to-fail-experiment-design.tactic.md` — Structured exploration under uncertainty
- `ATDD_adversarial-acceptance.tactic.md` — Adversarial acceptance test creation

**Characteristics:**
- Procedural (sequence of actions, not advice)
- Context-bounded (state preconditions, exclusions)
- Linear by default (minimal branching)
- Non-creative (minimize interpretation)
- Verifiable (concrete outputs, exit criteria)
- Failure-aware (explicit failure modes documented)

**Discovery mechanism:**
- **Primary:** Directives explicitly invoke tactics at workflow steps
- **Secondary:** Agents discover via `.github/agents/tactics/README.md` and propose to Human
- See [Discovering Available Tactics](#discovering-available-tactics) below

---

## How Layers Interact

The layers form a stack with clear precedence and composition rules:

```
┌─────────────────────────────────────────────┐
│ Guidelines (values, preferences)            │ ← Highest precedence
├─────────────────────────────────────────────┤
│ Approaches (mental models, philosophies)    │
├─────────────────────────────────────────────┤
│ Directives (explicit instructions)          │
├─────────────────────────────────────────────┤
│ Tactics (procedural execution)              │
├─────────────────────────────────────────────┤
│ Templates (output structure)                │ ← Lowest precedence
└─────────────────────────────────────────────┘
```

**Precedence Rules:**
1. Guidelines override all other layers
2. Directives override Tactics and Templates
3. Tactics and Templates operate at equal precedence (non-conflicting domains)
4. Approaches provide rationale but don't override directives

**Composition Pattern:**
- **Directives** select which **Tactics** to run
- **Approaches** justify why a **Tactic** exists
- **Guidelines** constrain how **Tactics** are applied
- **Templates** shape what **Tactics** produce

**Example Flow:**
1. Guideline: "Prefer small commits" (operational guideline)
2. Approach: "Trunk-based development" (branching philosophy)
3. Directive: "Use incremental code review for PRs" (011_risk_escalation.md)
4. Tactic: Execute `code-review.tactic.md` (step-by-step procedure)
5. Template: Format review output per `review-summary.md` template

---

## Why a Doctrine Stack Matters

### Problems Without a Doctrine Stack

Agents tend to:
- Over-interpret vague intent
- Drift in style and decision-making
- Optimize for fluency over correctness
- Re-solve the same judgment problems repeatedly
- Introduce inconsistent reasoning patterns

### Benefits of a Doctrine Stack

The doctrine stack:
- **Reduces ambiguity** — Externalized judgment eliminates guesswork
- **Centralizes judgment** — Decisions made once, applied consistently
- **Constrains execution** — Clear boundaries prevent scope creep
- **Enables safe repetition** — Predictable behavior across sessions
- **Improves traceability** — Explicit references document reasoning

**Key Insight:** It shifts the value of agentic work away from "prompt cleverness" toward **explicit system design**.

---

## Design Principles

A well-formed doctrine stack:

1. **Written for reuse, not conversation**  
   Documents are designed for repeated execution, not one-off explanations.

2. **Treats agent behavior as infrastructure**  
   Agents are executors operating under clear protocols, not creative collaborators.

3. **Separates judgment from execution**  
   Guidelines/Approaches/Directives contain judgment; Tactics/Templates execute.

4. **Assumes stateless or resettable agents**  
   No reliance on conversation memory or session continuity.

5. **Prefers boring clarity over expressive cleverness**  
   Predictability and precision over eloquence.

6. **Documents for agents, not about agents**  
   This is operational infrastructure, not meta-documentation.

---

## When to Add or Modify Each Layer

### Add a Guideline When:
- Establishing foundational values that affect all work
- Defining tone, integrity, or collaboration boundaries
- Creating guardrails that must never be violated
- **Frequency:** Rare (1-2 per year maximum)

### Add an Approach When:
- Introducing a conceptual model that shapes multiple tactics
- Justifying a family of related directives
- Documenting a philosophy that guides problem framing
- **Frequency:** Occasional (quarterly for mature frameworks)

### Add a Directive When:
- Encoding a rule that selects specific actions
- Establishing compliance requirements
- Defining escalation triggers or risk thresholds
- **Frequency:** Regular (as new patterns emerge)

### Add a Tactic When:
- Codifying a repeated task with known pitfalls
- Eliminating inconsistency in execution
- Making failure modes visible and preventable
- **Frequency:** Regular (as high-value procedures stabilize)

### Add a Template When:
- Standardizing artifact structure across agents
- Reducing cognitive load during artifact creation
- Ensuring required sections are included
- **Frequency:** Occasional (as new artifact types emerge)

---

## Relationship to AGENTS.md Context Stack

The doctrine stack layers map to AGENTS.md Section 2 (Context Stack Overview):

| AGENTS.md Layer              | Doctrine Stack Layer | Priority   |
|------------------------------|----------------------|------------|
| Bootstrap Protocol           | (initialization)     | Root       |
| General Guidelines           | Guidelines           | Highest    |
| Operational Guidelines       | Guidelines           | High       |
| Project Vision Reference     | Approaches           | Medium     |
| Project Specific Guidelines  | Directives           | Medium     |
| Tactics Reference            | Tactics              | Medium-Low |
| Command Aliases Reference    | (shortcuts)          | Low        |

**See also:** [AGENTS.md Section 2](../../AGENTS.md#2-context-stack-overview) for initialization sequence.

---

## Related Documentation

- **[AGENTS.md](../../AGENTS.md)** — Agent Specification Document (ASD)
- **[GLOSSARY.md](./GLOSSARY.md)** — Terminology reference (Doctrine Stack, Tactic definitions)
- **[directives/004_documentation_context_files.md](./directives/004_documentation_context_files.md)** — Canonical file locations
- **[tactics/README.md](./tactics/README.md)** — Tactics catalog and usage guide

---

## Maintenance

**Owner:** Curator Claire  
**Review Cycle:** Annual or when 5+ new layers/patterns emerge  
**Change Protocol:** Proposals via `work/collaboration/inbox/` task files  
**Version Governance:** Follow Directive 006 (Version Governance)

**Version History:**

| Version | Date       | Changes                     |
|---------|------------|-----------------------------|
| 1.0.0   | 2026-02-07 | Initial doctrine stack spec |

---

**The doctrine stack is not documentation *about* agents.**  
**It is documentation *for* agents.**
