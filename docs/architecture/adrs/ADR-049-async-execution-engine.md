# Architecture Decision Records

## ADR-049: Async Execution Engine with Cancellation

**status**: `Accepted`
**date**: 2026-02-13
**decision-makers**: Architect Alphonso, Human-in-Charge
**consulted**: Backend Benny, DevOps Danny

### Context

The current LLM execution path is synchronous:

```
RoutingEngine.execute()
  → adapter.execute()
    → SubprocessWrapper (subprocess.run())
      → blocks until completion or timeout
```

This creates three limitations:

1. **No parallelism:** Only one tool invocation can run at a time per
   process. Multi-agent work requires multiple terminal sessions.

2. **No cancellation:** Once `subprocess.run()` starts, the only
   intervention is the timeout. There is no graceful shutdown signal.
   Users must manually `kill` processes.

3. **No event streaming:** The synchronous call blocks the event loop.
   Progress events cannot be emitted until execution completes.

The Local Agent Control Plane (ADR-047) requires async dispatch with
parallel execution and cancellation support to fulfill its design goals.

### Decision

Replace the synchronous execution path with an **asyncio-based execution
engine** that provides:

1. **Async subprocess execution** via `asyncio.create_subprocess_exec()`
   as a replacement for `subprocess.run()`.

2. **Semaphore-based concurrency** — configurable maximum parallel tasks
   (default: 4). Prevents resource exhaustion.

3. **Signal-based cancellation** with escalation:
   - `SIGINT` (10s grace period) → `SIGTERM` (5s) → `SIGKILL` (immediate)
   - Configurable timeouts per step.

4. **ExecutionHandle** — returned by the Distributor, provides:
   - `cancel()` — initiate signal escalation
   - `is_running` — check execution state
   - `wait()` — await completion
   - `output_stream` — async iterator for stdout/stderr lines

5. **Backward-compatible adapter interface:**
   - Existing `ToolAdapter.execute()` (sync) continues to work.
   - New optional `ToolAdapter.async_execute()` for native async adapters.
   - Sync adapters are automatically wrapped via `asyncio.to_thread()`.

### Rationale

**Why asyncio (not threading or multiprocessing)?**

- Subprocess I/O is the bottleneck, not CPU. asyncio excels at I/O-bound
  concurrency with minimal overhead.
- asyncio integrates naturally with the event loop needed for WebSocket
  event emission (Flask-SocketIO).
- Single event loop avoids GIL issues and shared-state complexity.
- `asyncio.create_subprocess_exec()` provides direct signal control
  (`send_signal()`, `terminate()`, `kill()`).

**Why semaphore-based (not queue-based)?**

- Semaphore provides simple, in-process concurrency limiting without
  infrastructure.
- Queue-based dispatch (Redis, asyncio.Queue) is a Distributor strategy
  concern (ADR-047), orthogonal to the execution engine.
- Semaphore is compatible with any distributor — Direct, Queue, or
  Workflow.

**Why signal escalation (not just SIGKILL)?**

- LLM CLI tools may need to flush output, save partial results, or close
  API connections gracefully.
- `SIGINT` allows tools to handle Ctrl+C-like shutdown.
- `SIGTERM` is the standard process termination signal.
- `SIGKILL` is the last resort for unresponsive processes.

**Why optional async_execute() (not mandatory)?**

- Existing adapters (ClaudeCodeAdapter, GenericYAMLAdapter) are sync.
  Requiring async rewrites would block adoption.
- `asyncio.to_thread()` wrapping provides async behavior with zero
  adapter code changes.
- Native async adapters (future SDK adapters) can override for better
  performance.

### Envisioned Consequences

**Positive:**

- **Agility:** Multiple agent tasks run concurrently, reducing wall-clock
  time for multi-task iterations.
- **Ergonomics:** Users can cancel runaway operations from the dashboard
  or CLI without resorting to `kill -9`.
- **Repeatability:** Event streaming enables real-time progress tracking
  and JSONL event emission during execution.
- **Maintainability:** Clean async interface makes it straightforward to
  add new adapters and distributors.

**Negative:**

- **Maintainability:** Async code is harder to debug than sync code.
  Stack traces span coroutine boundaries. Mitigated by structured logging
  and careful error propagation.
- **Agility:** Initial migration effort to wrap existing sync adapters.
  Mitigated by `asyncio.to_thread()` compatibility layer.
- **Ergonomics:** Signal handling behavior varies across platforms
  (Windows does not support SIGTERM). Mitigated by platform detection
  and fallback to `terminate()`.

### Considered Alternatives

**Alternative 1: Thread pool executor**
- Use `concurrent.futures.ThreadPoolExecutor` for parallelism.
- Rejected: Threads lack native signal control for child processes.
  Cancellation requires process group management. asyncio provides
  cleaner subprocess control.

**Alternative 2: Multiprocessing**
- Spawn worker processes for each task.
- Rejected: Heavyweight for I/O-bound work. IPC overhead. Shared state
  complexity for event emission.

**Alternative 3: External task runner (Celery, Dramatiq)**
- Use established task queue for async execution.
- Rejected: Requires broker infrastructure (Redis/RabbitMQ). Contradicts
  local-first, no-infrastructure philosophy (ADR-008).

**Alternative 4: Keep synchronous, use multiple processes**
- Users run multiple `llm-service exec` commands in parallel.
- Rejected: No unified telemetry, no shared concurrency control, no
  dashboard integration. Status quo limitation.

### Related Documents

- **ADR-047:** CQRS Pattern (parent architecture)
- **ADR-025:** LLM Service Layer (execution model origin)
- **ADR-029:** Adapter Interface Design (ToolAdapter ABC)
- **Technical design:** `docs/architecture/design/local-agent-control-plane-architecture.md`

---

**Status:** Accepted (2026-02-13)
**Approved By:** Human-in-Charge, Architect Alphonso
**Next Action:** Spike implementation for validation
