# Portability Test Protocol
**Purpose:** Run real multi-model agent tasks and analyse divergence.

---

# 1. Preparation

## Step 1 — Identify a real task
Pick a task that produces real value (not a synthetic test).  
Examples:
- Update REPO_MAP
- Lexical pass on README
- Planning: Create decomposition for feature X
- Diagram generation

## Step 2 — Create a task YAML
Place under:

```

work/inbox/

````

Example:

```yaml
id: portability-repomap
agent: structural
status: new
title: "Portability check — Structural agent"
artefacts:
  - docs/REPO_MAP.md
guidelines:
  - structural-baseline
directives:
  - minimal-diffs
created_by: "portability"
````

---

# 2. Execute the task across models

Run the same agent prompt + task YAML through:

### ✔ GitHub Copilot Chat (verbose mode)

### ✔ Codex (Copilot CLI or JetBrains)

### ✔ ChatGPT GPT-4.1 / 4o

### ✔ Claude Sonnet 4.5

### ✔ Optional: Local runner script

---

# 3. Collect Logs

Store each run at:

```
validation/portability_logs/<task-name>/<model>/<timestamp>/
```

Include:

* `input_context.md`
* `output.md`
* `logs.txt`
* `delta.diff`
* `reflection.md` (model-provided explanation)

---

# 4. Compare Results

Evaluate:

* Guardrail adherence
* Directive recognition
* Guideline loading
* Artefact structure consistency
* YAML interpretation
* Hallucination or omission

---

# 5. Evaluate Portability

A task is “portable” if:

* ≥ 3 models produce equivalent structure
* No model violates guardrails
* Directives influence behaviour identically
* Outputs differ only in minor wording, not structure

---

# 6. Integrate Learnings

Use divergences to improve:

* directives
* guidelines
* agent profiles
* orchestration rules
* task templates

Commit improvements to:

* `.github/agents/`
* `docs/templates/agent-tasks`
* `work/README.md`


