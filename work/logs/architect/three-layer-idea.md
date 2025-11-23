## 1. The Three Layers (as you framed them)

### 1) **Guardrails / Context**

> “What is always true and non-negotiable?”

* High-level rules, values, constraints, and environment.
* Examples:

    * No flattery or hype.
    * Preserve author’s integrity and voice.
    * Be honest about uncertainty.
    * Use markdown, keep things scannable.
* Lives in:

    * `context/operational-reference.md`
    * `context/strategic-context.md`
    * `AGENTS.md` (global rules)
* **All agents inherit this. No opt-out.**

---

### 2) **Guidelines / Approaches**

> “How do we generally perform this kind of work?”

* Composed from multiple directives.
* Task-type / domain / medium specific:

    * “Lexical pass on existing text”
    * “Architectural note for other devs”
    * “Longform reflective essay”
    * “Pattern entry for the library”
* Explain *approach* and *shape of output*, not micro-rules.
* Lives in something like:

    * `docs/guidelines/guideline_lexical-pass.md`
    * `docs/guidelines/guideline_architecture-note.md`
    * `docs/guidelines/guideline_linkedin-post.md`

Agents typically attach 1–2 guidelines they “follow by default”.

---

### 3) **Directives (Sharp Micro Patterns)**

> “What precise micro-rules apply here?”

* Small, atomic mini-specs.
* Examples:

    * `minimal-diffs`
    * `preserve-voice`
    * `no-best-practices`
    * `examples-before-abstract`
    * `no-reflow-without-need`
* Often reused across guidelines and agents.
* Live in:

    * `docs/directives/directive_<name>.md`

Agents or tasks can request:

> “Apply guideline X and directives A, B, C”

---

## 2. How Agents Use These Layers

You basically get:

* **Guardrails / Context** → *global contract*
* **Guidelines** → *default operating mode per agent*
* **Directives** → *task-level sharpening*

### In an agent profile (example: Lexical agent)

```markdown
## Context & Guardrails
This agent always adheres to:
- `context/operational-reference.md`
- `context/strategic-context.md`
- Global AGENTS.md contract

These are non-negotiable.

## Default Guidelines
By default, this agent applies:
- `guideline_lexical-pass`

## Directives
The `guideline_lexical-pass` includes these directives:
- `minimal-diffs`
- `preserve-voice`
- `no-best-practices`
- `examples-before-abstract`

Tasks may optionally add or override directives via:
- task YAML: `directives: [...]`
- an explicit instruction in the prompt, if allowed by guardrails.
```

---

## 3. How Tasks Plug Into This

In your async orchestration, a task can be precise without being verbose:

```yaml
id: 2025-11-21T1015-lexical-readme
agent: lexical
status: new
title: "Lexical pass on README"
artefacts:
  - README.md
guidelines:
  - lexical-pass
directives:
  - minimal-diffs
  - preserve-voice
  - examples-before-abstract
```

The Lexical agent then:

1. Loads **context / guardrails** (always).
2. Applies `guideline_lexical-pass`.
3. Tightens behavior further with the listed `directives`.

If nothing is specified, it falls back to its default guideline set.

---

## 4. Suggested Repository Layout

Something like:

```text
context/
  operational-reference.md
  strategic-context.md
  command-aliases.md
  system-bootstrap.md

docs/
  guidelines/
    00_index.md
    guideline_lexical-pass.md
    guideline_architecture-note.md
    guideline_pattern-entry.md
  directives/
    00_index.md
    directive_minimal-diffs.md
    directive_preserve-voice.md
    directive_no-best-practices.md
    directive_examples-before-abstract.md
```

Agent profiles can then reference these by name, not by copy-pasted prose.

---

## 5. How this helps your specialist agents

Given your experience (“they behave better when prompts are structured and specific”):

* **Guardrails** remove “who am I, how do I behave?” uncertainty.
* **Guidelines** remove “what shape of work is expected?” uncertainty.
* **Directives** remove “how sharp should I be on this axis?” uncertainty.

And because directives are small and composable, you can adjust behavior *by composition* instead of rewriting prompts.