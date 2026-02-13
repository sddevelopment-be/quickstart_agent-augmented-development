# Architecture Decision Records

## ADR-048: Run Container Concept

**status**: `Accepted`
**date**: 2026-02-13
**decision-makers**: Architect Alphonso, Human-in-Charge
**consulted**: Process Architects, Planning Petra

### Context

The current task orchestration model (ADR-008, ADR-003) treats tasks as
independent units. Each task is a YAML file that moves through a lifecycle
(`new → assigned → in_progress → done`). Tasks can chain via `next_agent`,
but there is no concept of a *group* of related tasks executed as a
coherent unit.

This creates several problems as agent workflows grow more complex:

1. **No grouping:** A single iteration cycle may spawn 5-10 tasks across
   multiple agents. There is no way to view, cancel, or reason about them
   as a unit.

2. **No aggregate state:** "Is the architecture review done?" requires
   manually checking each constituent task. There is no derived status.

3. **No telemetry rollup:** Cost and duration are tracked per-task but
   cannot be aggregated to answer "How much did this iteration cost?"

4. **No reproducibility anchor:** Without a container linking the tasks,
   prompt, and context that composed a work unit, replaying or auditing
   a past iteration requires manual reconstruction.

The Local Agent Control Plane prestudy introduces "Run" as a first-class
concept to address these gaps.

### Decision

Introduce **Run** as a first-class grouping entity that contains one or
more tasks within a coherent unit of work.

**Data model:**

```yaml
# runs/<run-id>/run.yaml
id: RUN-20260213-001
created_at: 2026-02-13T10:00:00Z
status: running            # pending | running | completed | cancelled | error
phase: architecture        # semantic label (optional)
agent_role: architect-alphonso  # initiating agent (optional)
tasks:
  - task_id: 2026-02-13T1000-arch-review
  - task_id: 2026-02-13T1015-adr-draft
summary: "Architecture review and ADR creation for control plane"
```

**Key design decisions:**

1. **YAML-based, file-stored.** Runs follow the same file-based pattern
   as tasks (ADR-008). Stored in `runs/` directory (not inside
   `work/collaboration/` to avoid coupling).

2. **Reference, not containment.** Runs reference task IDs. Tasks remain
   in `work/collaboration/` and follow their existing lifecycle. A run
   does not "own" its tasks — it groups them.

3. **Derived status.** Run status is computed from constituent tasks:
   - All tasks pending → run is `pending`
   - Any task in_progress → run is `running`
   - All tasks done → run is `completed`
   - Any task error (and none in_progress) → run is `error`
   - Explicit cancellation → run is `cancelled`

4. **Optional.** Runs are not required. Tasks can exist without a parent
   run. This preserves backward compatibility with all existing workflows.

5. **Telemetry aggregation point.** JSONL events (ADR-047) carry `run_id`.
   The Query Service aggregates cost, duration, and event counts per run.

### Rationale

**Why a separate entity (not a task field)?**

- Adding a `run_id` field to existing task YAML would require migrating
  all existing tasks. A separate entity avoids this.
- Run metadata (phase, summary, agent_role) does not belong on individual
  tasks — it describes the *group*, not the *unit*.
- Separate storage allows run lifecycle to be managed independently of
  task lifecycle.

**Why reference-based (not containment)?**

- Tasks have an established lifecycle (ADR-003, ADR-008) with their own
  directory structure. Moving tasks into run directories would break all
  existing scripts, the dashboard file watcher, and the orchestrator.
- Reference-based grouping means a task could theoretically belong to
  multiple runs (e.g., a shared setup task) — though this is not a
  primary use case.

**Why derived status (not explicit)?**

- Explicit run status creates a synchronization problem: who updates the
  run when a task completes? The orchestrator? The agent? The dashboard?
- Derived status eliminates this — the Query Service computes run state
  from task states on each read. Single source of truth.
- For cancellation, the Coordination Service sets run status to
  `cancelled` explicitly and sends cancel signals to constituent tasks.

**Why optional?**

- The framework must remain usable for simple, single-task workflows.
- Forcing run creation for every task adds friction without value for
  small operations.
- The Run concept becomes valuable at 3+ tasks per work unit.

### Envisioned Consequences

**Positive:**

- **Ergonomics:** Users can view, cancel, and audit entire work units
  as a single entity. Dashboard shows run-level progress bars.
- **Repeatability:** Run YAML captures the grouping, phase, and context
  of a work unit. Combined with JSONL telemetry, full replay is possible.
- **Maintainability:** Telemetry aggregation is clean — group by `run_id`
  instead of manual task correlation.
- **Modifiability:** New features (run templates, run scheduling, run
  comparison) have a natural anchor point.

**Negative:**

- **Maintainability:** One more YAML schema to maintain and validate.
  Mitigated by keeping the schema minimal.
- **Ergonomics:** Contributors must learn when to create runs vs. bare
  tasks. Mitigated by making runs optional and documenting guidelines.
- **Agility:** Derived status computation adds a query-time cost.
  Mitigated by caching in the Query Service.

### Considered Alternatives

**Alternative 1: Add `run_id` field to task YAML**
- Simpler — no new entity. But requires task schema migration, pollutes
  task files with grouping concerns, and has no place for run-level
  metadata.
- Rejected: Schema migration cost and conceptual mixing outweigh simplicity
  gain.

**Alternative 2: Use Git branches as run containers**
- Each run maps to a Git branch. Tasks are commits on that branch.
- Rejected: Conflates version control with execution orchestration. Branch
  explosion, merge complexity, and inability to have concurrent runs on
  the same branch.

**Alternative 3: Use work log entries as implicit runs**
- Work logs (Directive 014) already group work narratively.
- Rejected: Work logs are prose documents, not structured data. Cannot
  be queried, aggregated, or used for cancellation.

**Alternative 4: No grouping — keep tasks independent**
- Status quo. Users mentally group tasks.
- Rejected: Does not scale. 10+ tasks per iteration with no grouping
  makes monitoring and auditing impractical.

### Related Documents

- **ADR-047:** CQRS Pattern for Local Agent Control Plane (companion)
- **ADR-008:** File-Based Async Coordination (foundation)
- **ADR-003:** Task Lifecycle and State Management (task model)
- **Technical design:** `docs/architecture/design/local-agent-control-plane-architecture.md`
- **Implementation mapping:** `docs/architecture/design/control-plane-implementation-mapping.md`

---

**Status:** Accepted (2026-02-13)
**Approved By:** Human-in-Charge, Architect Alphonso
