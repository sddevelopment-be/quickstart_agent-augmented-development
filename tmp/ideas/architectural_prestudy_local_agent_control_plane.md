# Architectural Prestudy -- Local Agent Control Plane (Dashboard + OpenCode + Task Runner)

## Status

Draft prestudy / design outline.

## Intent

Design a local-first architecture that supports multiple agent stacks,
multiple tools/providers, and parallel execution, while providing:

-   a high-level localhost dashboard (progress, states, artifacts)
-   an interactive console (OpenCode TUI) to kick off new work
-   a task runner service that wraps heterogeneous CLI tools
-   traceable task lifecycle events and log capture
-   reproducibility and auditability without giving up interactivity

This is an observability + governance design, not "LLM automation for
its own sake".

------------------------------------------------------------------------

## Context and Problem

### Current reality

-   Work is performed locally using CLI tools in interactive mode.
-   Multiple projects and stacks run in parallel.
-   The high-level dashboard exists, but live tracing is fragmented
    across terminals.
-   Outputs and progress are hard to aggregate coherently.

### Design goal

Provide a local agent control plane that keeps a human in charge while
making agent work: - visible (what is running, where, why) - traceable
(logs + events) - comparable (per-run artifacts) - cancellable
(timeouts, stop signals)

------------------------------------------------------------------------

## High-Level Architecture

### Components

1.  Dashboard UI (Localhost Web UI)
    -   Displays run-level and task-level state.
    -   Reads telemetry and artifacts from filesystem / telemetry store.
    -   Provides links to logs and outputs.
    -   Does not run tools directly.
2.  OpenCode TUI (Interactive Console)
    -   Used for interactive work and kicking off new implementations.
    -   Can trigger new tasks through the LLM service.
    -   Can open task logs and artifacts.
3.  LLM Service / Task Runner (Local daemon)
    -   The execution layer.
    -   Provides a consistent API to start/stop tasks across tools.
    -   Emits lifecycle events and captures logs.
    -   Manages parallelism.
4.  Tool Wrappers
    -   Encapsulate provider/tool-specific invocation details.
    -   Configured via YAML (tool → command mapping + env + mode +
        timeouts).
5.  Telemetry Store
    -   Append-only JSONL trace log (primary)
    -   Optional SQLite index for fast queries (secondary)
    -   Artifacts and raw logs stored on filesystem

------------------------------------------------------------------------

## Execution Model

### Key concepts

-   Run: umbrella container for coherent work.
-   Task: single executable unit (one tool invocation).
-   Phase: process stage (research, primer, architecture, etc.).
-   Agent role: semantic worker identity.

### Two execution modes

1.  Batch (prompt-and-log)
    -   Deterministic, traceable runs.
    -   Outputs written to artifacts folder.
2.  Interactive
    -   Tool runs attached to a pseudo-TTY.
    -   Used for exploratory work.
    -   Still emits lifecycle events and captures logs.

------------------------------------------------------------------------

## Data and Storage Layout

Recommended layout:

runs/ RUN-YYYYMMDD-### telemetry.jsonl tasks/ `<task_id>`{=html}/
task.json stdout.log stderr.log artifacts/

------------------------------------------------------------------------

## Telemetry Event Schema (Minimal)

Each JSONL event:

{ "ts": "ISO_TIMESTAMP", "run_id": "RUN-...", "phase": "architecture",
"agent_role": "architecture-agent", "task_id": "task\_...", "tool":
"opencode", "mode": "batch", "event": "task_started", "status":
"running", "log_paths": { "stdout": "path/to/stdout.log", "stderr":
"path/to/stderr.log" }, "summary": "Short human-readable summary" }

Completion events include: - exit_code - duration_ms - artifacts -
error_class

------------------------------------------------------------------------

## Tool Configuration (YAML Example)

tools: opencode_batch: mode: batch cmd: \["opencode", "run", "--model",
"{model}", "--", "{prompt}"\] timeout_sec: 1800

opencode_interactive: mode: interactive cmd: \["opencode"\]

------------------------------------------------------------------------

## Concurrency Model

Recommendation: - Use asyncio + create_subprocess_exec - Apply
semaphores for max parallel tasks - Support timeouts and cancellation
(SIGINT → SIGTERM → SIGKILL)

------------------------------------------------------------------------

## Governance

-   Human in charge of checkpoints
-   Optional checkpoint_required events
-   Advisory defaults; minimal hard enforcement

------------------------------------------------------------------------

## Implementation Outline

1.  Define schemas (event JSONL + YAML tool config).
2.  Implement runner core (asyncio subprocess orchestration).
3.  Add lifecycle event logging.
4.  Capture stdout/stderr to files.
5.  Integrate dashboard with telemetry.jsonl.
6.  Integrate OpenCode via batch and interactive modes.
7.  Add cancellation and timeout handling.

------------------------------------------------------------------------

## Design Principles

-   Local-first
-   Human in charge
-   Explicit lifecycle events
-   Reproducible prompt/context capture
-   Advisory over prescriptive enforcement
