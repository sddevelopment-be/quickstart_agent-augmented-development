# Portability Run — Cross-Model Behaviour Verification  
**Repository:** `quickstart_agent-augmented-development`  
**Purpose:** Validate that agent behaviour, directives, guidelines, and orchestration remain **consistent across models and environments**, using real tasks rather than artificial tests.

---

## 1. Scope & Philosophy

This portability run is intentionally **useful work**, not synthetic benchmarking.

The idea:

- Use **real, valuable tasks** (e.g., updating REPO_MAP, performing lexical passes, generating diagrams).
- Execute the *same task* across:
  - GitHub Copilot (verbose logging)
  - Codex (via Copilot CLI or JetBrains)
  - ChatGPT (OpenAI GPT-4.1, 4o, 4o-mini)
  - Claude Sonnet 4.5
- Collect all logs and outputs.
- Analyse where models diverge in:
  - Guardrail adherence  
  - Directive interpretation  
  - Guideline application  
  - Artefact generation  
  - YAML task handling  
  - File-based orchestration behaviour  

This produces a **real-world portability profile** across LLM runtimes and developer environments.

---

## 2. The Portability Task Set

Each portability cycle includes:

### **Task A — Structural Mapping (High-Signal Test)**  
Generates/updates:
- `docs/REPO_MAP.md`
- `docs/SURFACES.md`

**Reason:**  
Structural agents are deterministic; divergences indicate directive or guideline ambiguity.

---

### **Task B — Lexical Pass**  
Runs the lexical agent on a real repo file (e.g. `README.md` or `VISION.md`).

**Reason:**  
Tests directive-level behaviour (`preserve-voice`, `minimal-diffs`, etc.)

---

### **Task C — Diagram Generation (PlantUML)**  
Asks the diagram agent to produce a basic PlantUML mapping.

**Reason:**  
Tests formatting stability and output structure across models.

---

### **Task D — Planning Agent Decomposition**  
Requests a decomposition of a feature request into sub-tasks.

**Reason:**  
Tests hierarchy, ordering, and guideline adherence.

---

## 3. Execution Environments

Run each task on:

- **GitHub Copilot Chat** (verbose logs enabled)  
- **Copilot CLI / Codex**  
- **ChatGPT (GPT-4o, 4.1, 4o-mini)**  
- **Claude Sonnet 4.5**  
- **Optional: Local runner** using the OpenAI or Anthropic API libraries  

---

## 4. What to Save From Each Run

For each model + environment:

Create:

```

validation/portability_logs/<task>/<model>/<timestamp>/

```

Include:

- `input_context.md` — agent prompt + guidelines + directives shown to the model
- `model_output.md` — final artefacts  
- `model_deltas.diff` — diff against “reference output”
- `model_log.txt` — verbose Copilot/Codex logs where applicable
- `model_reflection.txt` (optional)  
  Ask the model:
  > “List which directives you followed, which guidelines you loaded, and any conflicts you encountered.”

---

## 5. Success Criteria

A model is “portable” if:

- It interprets named directives **consistently**
- It loads guardrails **reliably**
- It applies guidelines **predictably**
- It produces artefacts with similar **structure, sections, and ordering**
- It does not hallucinate repo structure
- It respects task YAML semantics

A portability run passes if **3/4 models** behave consistently with the reference implementation (usually **GPT-4.1 or Claude Sonnet 4.5**).

---

## 6. Improving the Framework

Any divergence should trigger:

- tightening of directives  
- clarification of guidelines  
- refinement of agent profiles  
- improved task-YAML specs  
- documented restrictions for Codex/Copilot where needed  

Each portability run incrementally strengthens the framework.

---

## 7. Notes

This file is intended to evolve alongside improvements to:

- `.github/agents/general_guidelines.md`  
- `.github/agents/*.agent.md`  
- `docs/templates/agent-tasks/`  
- `work/` orchestration design  

