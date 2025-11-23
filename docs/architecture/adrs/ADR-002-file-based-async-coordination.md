# Architecture Decision Records

## ADR-002: File-Based Asynchronous Agent Coordination

**status**: `Proposed`  
**date**: 2025-11-20

### Context

Multi-agent systems require coordination mechanisms to distribute work, track progress, and ensure artifacts are produced consistently. Traditional approaches include:

- **Message queues** (RabbitMQ, Kafka): Require infrastructure, add operational complexity
- **RPC/API calls** (REST, gRPC): Require running services, introduce network dependencies
- **Shared databases**: Add persistence layer, schema migrations, query complexity
- **In-memory coordination**: Lost on crash, not portable, not human-inspectable

We need a coordination mechanism that:

- Works without additional infrastructure or services
- Is transparent and human-inspectable at all times
- Leaves a complete audit trail
- Integrates naturally with Git workflows
- Requires minimal setup for new agents
- Allows both automated (CI) and manual (local) execution

The development team values simplicity, transparency, and maintainability over low-latency real-time coordination. Agent tasks are measured in minutes to hours, not milliseconds, making asynchronous coordination acceptable.

### Decision

**We will coordinate multiple agents using file-based task descriptions stored in a shared `work/` directory structure.**

Specifically:

1. **Task representation**: Each task is a single YAML file with a unique identifier
2. **State transitions**: Task status changes via file movements between directories
3. **Agent assignment**: Moving a file to `work/assigned/<agent>/` assigns the task
4. **Result communication**: Agents update the YAML file with a `result:` block
5. **Workflow sequencing**: Agents specify `next_agent:` for multi-step workflows
6. **Audit trail**: All state is tracked in Git commits

No databases, no running services, no APIs—just files moving through directories.

### Rationale

**Why files?**

- **Git-native**: Every state change is a commit, providing full history and diff capability
- **Human-readable**: YAML is easy to read, write, and edit manually when needed
- **Zero infrastructure**: No services to run, maintain, or secure
- **Portable**: Works in CI, locally, or on any system with file access
- **Debuggable**: Problems are visible by reading files, no hidden state
- **Recoverable**: Roll back via git revert, no database restore needed

**Why YAML?**

- Widely supported, human-friendly syntax
- Preserves comments for annotations
- Natural representation of nested data structures
- Schema-validatable with standard tools
- No escaping issues unlike JSON strings

**Why directory-based state?**

- Filesystem provides atomic move operations (rename is atomic on POSIX)
- Directory structure makes status immediately visible (`ls work/assigned/structural/`)
- Polling is simple and reliable
- No need for status databases or tracking tables

**Trade-offs accepted:**

- **Latency**: File-based coordination is seconds-to-minutes, not milliseconds (acceptable for our use case)
- **Git overhead**: Many small commits (mitigated by periodic squashing, archive cleanup)
- **Concurrent access**: Potential race conditions on same artifact (mitigated by Coordinator serialization)

**Alternatives considered:**

1. **Message queue (RabbitMQ/SQS)**
   - Rejected: Requires infrastructure, operational overhead, not Git-native
2. **Shared database (PostgreSQL)**
   - Rejected: Schema management, migration complexity, not human-inspectable
3. **GitHub Issues/Projects**
   - Rejected: API rate limits, not suitable for high-frequency updates, requires network
4. **Event bus (Redis Streams)**
   - Rejected: Requires running service, events not versioned in Git

### Envisioned Consequences

**Positive:**

- ✅ **Simplicity**: No additional infrastructure or services to manage
- ✅ **Transparency**: Full visibility into task state at any point in time
- ✅ **Auditability**: Complete history of all tasks in Git log
- ✅ **Portability**: Works across CI systems, local environments, different LLM toolchains
- ✅ **Recoverability**: Simple rollback via git commands
- ✅ **Extensibility**: Adding a new agent requires only creating a directory and profile
- ✅ **Debuggability**: Read files to understand system state, no log aggregation needed
- ✅ **Collaboration**: Human can inspect, modify, or create tasks manually

**Negative:**

- ⚠️ **Latency**: Not suitable for real-time coordination (acceptable trade-off)
- ⚠️ **Commit noise**: Many small commits may clutter history (addressed via archive strategy)
- ⚠️ **Race conditions**: Multiple agents modifying same artifact needs serialization (Coordinator handles this)
- ⚠️ **File system limits**: Very large numbers of tasks may hit directory size limits (addressed via archive cleanup)
- ⚠️ **No transactions**: Multi-file operations are not atomic (mitigated by task design)

**Risks:**

- **Concurrent modification**: Two agents updating same file simultaneously → Use file locking via task status, Coordinator conflict detection
- **Lost tasks**: File accidentally deleted → Git history provides recovery, validation scripts detect missing files
- **Disk space growth**: Archive grows indefinitely → Periodic cleanup strategy, compression of old tasks

**Dependencies:**

- Requires all agents to follow task lifecycle protocol
- Requires Coordinator agent to manage assignments and handoffs
- Requires task YAML schema validation before execution

### Considered Alternatives

**1. GitHub Issues API**

- **Pros**: Native to GitHub, good UI, existing permissions model
- **Cons**: API rate limits, network dependency, not suitable for high-frequency updates, not fully Git-native
- **Reason rejected**: Coordination would be opaque to local development, rate limits constrain automation

**2. Shared SQLite Database**

- **Pros**: Simple, no server, ACID transactions
- **Cons**: Binary format not human-readable, merge conflicts on database file, not naturally versioned
- **Reason rejected**: Loses transparency, merge conflicts are destructive

**3. Event Sourcing with JSON Files**

- **Pros**: Append-only log, full history
- **Cons**: More complex to implement, requires event replay logic, no natural directory-based state
- **Reason rejected**: Unnecessary complexity for our use case, loses clarity of current state

**4. Pull Request Per Task**

- **Pros**: Built-in review workflow, GitHub native
- **Cons**: PR overhead for every task, notification spam, slow for simple coordination
- **Reason rejected**: Too heavy-weight for frequent agent coordination, obscures system state

---

**Related ADRs:**

- [ADR-003: Task Lifecycle and State Management](ADR-003-task-lifecycle-state-management.md)
- [ADR-004: Work Directory Structure](ADR-004-work-directory-structure.md)
- [ADR-005: Coordinator Agent Pattern](ADR-005-coordinator-agent-pattern.md)

**References:**

- [Async Multi-Agent Orchestration Architecture](async_multiagent_orchestration.md)
- Issue #8: Asynchronous Multi-Agent Orchestration (File-Driven Model)
