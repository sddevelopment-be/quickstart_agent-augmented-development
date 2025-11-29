# Agent-Enhanced Test Validation for Coaches and Engineers

**Audience:** Technical coaches, process architects, software engineers  
**Purpose:** How to check whether your tests read like documentation, using a lightweight dual-helper workflow.  
**Pilot signal:** Tests alone gave a **92% accurate** system description; gaps were mostly about “why” and “ops.”

## Why This Matters (You Already Know the Tech)
- Tests are often the freshest specification, but “high coverage” ≠ “high clarity.”  
- Onboarding speed, review friction, and regression risk all hinge on how well tests convey intent.  
- The question we ask: **Can a new teammate describe the system by reading only the tests?**

## The Dual-Helper Pattern
1) **Researcher Ralph (tests-only):** Reads the scoped tests and writes the system story—no docs, no prior context.  
2) **Architect Alphonso (full context):** Compares Ralph’s story to code + ADRs, scores accuracy, and lists missing context.  
3) **Close the gaps:** Add intent notes or one or two scenarios where the tests fall short (usually rationale, ops, or security).

## What We Learned in the Pilot
- **Behavioral clarity:** 92% accuracy on workflows, edge cases, and data from tests alone.  
- **Blind spots:** Design rationale (file-based, single orchestrator), ops (cron cadence, agent lifecycle), trust boundaries, performance envelope.  
- **Low-effort fixes:** ADR links in docstrings for intent-heavy areas, a “how it runs” scenario, and a lightweight perf/security probe.

## How to Run It (Lean and Repeatable)
- **Scope:** 50–100 tests in one module; don’t start with the whole repo.  
- **Enforce constraints:** Ralph gets tests only. Alphonso must read ADRs/design notes to spot missing “why.”  
- **Score simply:** High/Medium/Low for behavioral vs. architectural vs. operational clarity, each with one-line evidence.  
- **Ship the deltas:** Publish both docs; they stand alone and guide the smallest useful fixes.

## Payoffs for Teams
- Faster onboarding: tests + gap list orient newcomers in under an hour.  
- Safer changes: reveals where intent is invisible—the common source of regressions.  
- Better tests, minimal churn: tiny notes and a couple of scenarios close most gaps.

## Tradeoffs and Boundaries
- ~1 hour per run—reserve for milestones or refactors.  
- Scoring has judgment—anchor ratings with evidence lines.  
- Outputs age—rerun after significant test changes.

## Quick Example
In the pilot, orchestration tests (tasks as YAML moving `inbox → assigned → done`) let Ralph reconstruct assignment, handoffs, timeouts, conflict detection, and archiving. Alphonso filled in the “why”: single-orchestrator by design, cron-driven, Git permissions as the trust boundary. Aim for that balance—tests tell the “what,” light notes cover the “why/ops.”
