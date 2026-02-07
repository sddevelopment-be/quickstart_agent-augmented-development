# Tactic: Execution.FreshContextIteration

**Related tactics:**
- `stopping-conditions.tactic.md` — defines iteration completion criteria
- `analysis-extract-before-interpret.tactic.md` — used within iterations for unbiased extraction

**Complements:**
- Directive 024 (Self-Observation Protocol) — complementary pattern for detecting drift within single executions

---

## Intent
Execute a task deterministically by repeatedly running a single, well-scoped instruction in a fresh context and aggregating results externally.

Use this tactic to eliminate context carry-over bias, ensure reproducibility, and aggregate results in a controlled manner.

---

## Preconditions

**Required inputs:**
- A clearly defined task exists
- A fixed specification or instruction set is available
- External storage for results is available
- Number of iterations is predetermined

**Assumed context:**
- Each iteration can be executed independently
- Results can be persisted and aggregated externally
- Fresh context (no memory between runs) is achievable

**Exclusions (when NOT to use):**
- When tasks require learning or adaptation across iterations
- When context carry-over is explicitly desired
- When external aggregation is impractical or unavailable

---

## Execution Steps

1. Define the task to be executed once per iteration.
2. Define the fixed specification and output format.
3. Execute the task in a **fresh context** with no prior memory.
4. Persist the result externally (file, database, API).
5. Repeat steps 3–4 a predefined number of times.
6. Aggregate results outside the execution loop.
7. Review aggregated results.
8. Stop.

---

## Checks / Exit Criteria
- Each iteration used a fresh context (no memory of previous iterations).
- Results are persisted independently.
- Aggregation is deterministic and external to iterations.
- All iterations completed successfully or failures are documented.

---

## Failure Modes
- Allowing context carry-over between iterations (defeats the purpose).
- Modifying the task or specification mid-loop.
- Performing interpretation inside the loop instead of during aggregation.
- Failing to validate that context is actually fresh.

---

## Outputs
- Set of individual task results (one per iteration)
- Aggregated result artifact
- Iteration metadata (count, timestamps, failures)

---

## Notes on Use

This tactic is particularly useful for:
- **Consistency validation** — running the same task multiple times to detect variance
- **Bias reduction** — preventing prior results from influencing subsequent runs
- **Parallel execution** — iterations are independent and can run concurrently

**Example use cases:**
- Running code generation tasks multiple times to assess consistency
- Extracting structured data from unstructured sources repeatedly
- Validating determinism of agent outputs

**Key distinction from Ralph Wiggum Loop:**
- **Ralph Wiggum Loop** (Directive 024) — self-observation *within* a single execution to detect drift
- **Fresh Context Iteration** — *multiple* executions with no shared context

---
