# ADR-004: Work Directory Structure and Conventions

**status**: `Accepted`  
**date**: 2025-11-20

### Context

The file-based orchestration system requires a consistent directory structure to:

- Organize tasks by lifecycle state
- Provide clear agent ownership
- Enable simple discovery and polling
- Support both automated and manual workflows
- Scale to multiple agents and hundreds of tasks

Without standardized structure:

- Agents wouldn't know where to look for their tasks
- Task discovery would require scanning entire repository
- Ownership would be ambiguous
- Manual intervention would be error-prone
- Tooling and automation would be fragile

We need a directory layout that:

- Is self-documenting and intuitive
- Supports efficient polling by agents
- Enables atomic operations
- Works with Git naturally
- Allows for future extensibility

The structure must accommodate current agents (structural, lexical, curator, diagrammer, planning, architect, translator, build-automation) and future specialized agents.

### Decision

**We will use a hierarchical `work/` directory structure organized by lifecycle state and agent ownership.**

**Root structure:**

```
work/
  inbox/              # New tasks awaiting assignment
  assigned/           # Tasks assigned to specific agents
    <agent-name>/     # One subdirectory per agent
  done/               # Completed tasks with results
  archive/            # Long-term task retention
  logs/               # Agent execution logs (optional)
  collaboration/      # Cross-agent coordination artifacts
  scripts/            # Utility scripts for orchestration
```

**Agent subdirectories under `assigned/`:**

```
work/assigned/
  structural/         # Structural analysis agent tasks
  lexical/            # Lexical/voice analysis agent tasks
  curator/            # Curation and consistency agent tasks
  diagrammer/         # Diagram generation agent tasks
  planning/           # Planning agent tasks
  coordinator/        # Meta-orchestration tasks
  architect/          # Architecture documentation tasks
  translator/         # Translation agent tasks
  build-automation/   # Build and CI automation tasks
  <future-agent>/     # Extensible for new agents
```

**Collaboration artifacts:**

```
work/collaboration/
  AGENT_STATUS.md     # Current state of all agents
  HANDOFFS.md         # Agent-to-agent transition log
  WORKFLOW_LOG.md     # System-wide orchestration events
  DEPENDENCIES.md     # Cross-task dependency tracking (optional)
```

**Naming conventions:**

- **Task files**: `YYYY-MM-DDTHHMM-<agent>-<slug>.yaml`
  - Example: `2025-11-20T1430-structural-repomap.yaml`
  - ISO 8601 timestamp prefix for natural chronological sorting
  - Agent name for quick identification
  - Slug for human readability
- **Log files**: `YYYY-MM-DD-<agent>-<task-id>.log` (optional)
- **Archive directories**: `YYYY-MM/` for monthly grouping

### Rationale

**Why hierarchical structure?**

- **Separation by state**: `inbox/`, `assigned/`, `done/` make task lifecycle immediately visible
- **Separation by agent**: Each agent has its own subdirectory, prevents mixing
- **Atomic operations**: Moving file between directories is atomic
- **Simple polling**: Agent watches single directory (`work/assigned/<agent>/`)
- **Clear ownership**: Directory name = agent name

**Why separate collaboration directory?**

- **Cross-cutting artifacts**: Status, handoffs, and logs are not tied to single agent
- **Central visibility**: One place to check system-wide state
- **No task clutter**: Keeps task directories focused on tasks only

**Why timestamp-prefixed naming?**

- **Natural sorting**: `ls` shows tasks in chronological order
- **Unique IDs**: Timestamp + agent + slug is unique enough for most cases
- **Human-readable**: Easy to identify task at a glance
- **No collision**: Unlikely two tasks created at exact same second with same slug

**Why archive subdirectories by month?**

- **Manageable size**: Prevents single directory with thousands of files
- **Natural retention**: Easy to implement retention policy (e.g., delete dirs >12 months)
- **Efficient operations**: Fewer files per directory = faster filesystem operations

**Trade-offs accepted:**

- **Directory proliferation**: Many subdirectories (one per agent) (acceptable: clear structure worth the extra directories)
- **Timestamp collisions**: Possible but rare (mitigated by including agent name and slug)
- **Deep nesting**: Three levels deep (`work/assigned/<agent>/`) (acceptable: standard Unix practice)
- **Manual directory creation**: New agents require creating their directory (acceptable: one-time setup, documented in agent profile template)

**Alternatives considered:**

1. **Flat structure** (all tasks in `work/tasks/`)
   - Rejected: Loses state and ownership information, requires reading all files to find relevant tasks
2. **Status field only** (no directory structure)
   - Rejected: Loses atomic operations, requires scanning all files
3. **Agent-first structure** (`work/<agent>/inbox/`, `work/<agent>/done/`)
   - Rejected: Cross-agent visibility is harder, Coordinator can't see all pending work easily
4. **Database-backed** (directory structure mirrors DB tables)
   - Rejected: Loses simplicity, Git-native benefits

### Envisioned Consequences

**Positive:**

- ✅ **Discoverability**: Clear where to find tasks in any state
- ✅ **Ownership**: Agent name in directory path = explicit ownership
- ✅ **Polling efficiency**: Agents watch single directory, not entire tree
- ✅ **Atomic operations**: File moves between directories are atomic
- ✅ **Extensibility**: Adding new agent requires only creating a directory
- ✅ **Intuitive**: Structure is self-documenting
- ✅ **Scalability**: Handles hundreds of tasks without performance issues
- ✅ **Git-friendly**: `.gitkeep` files ensure empty directories are tracked

**Negative:**

- ⚠️ **Setup overhead**: Each new agent requires directory creation
- ⚠️ **Directory count**: Many subdirectories may feel cluttered initially
- ⚠️ **Naming discipline**: Requires consistent task naming convention
- ⚠️ **Archive growth**: Monthly subdirectories require periodic cleanup

**Risks:**

- **Missing directories**: Agent tries to write to non-existent directory → Agent profile template includes directory setup instructions
- **Inconsistent naming**: Tasks named incorrectly → Validation script enforces naming convention
- **Filesystem limits**: Thousands of tasks in single directory → Archive policy keeps active directories lean
- **Permissions**: Directory permissions incorrect → Document required permissions, CI setup validates

**Dependencies:**

- Requires `.gitkeep` files in empty directories to track structure in Git
- Requires README.md in `work/` explaining structure and conventions
- Requires validation script to check directory structure integrity
- Requires agent profile template to include directory setup

### Directory Setup

**Initial repository setup:**

```bash
#!/bin/bash
# ops/scripts/planning/init-work-structure.sh

# Create lifecycle directories
mkdir -p work/inbox
mkdir -p work/done
mkdir -p work/archive
mkdir -p work/logs
mkdir -p work/collaboration
mkdir -p ops/scripts

# Create agent directories
mkdir -p work/assigned/structural
mkdir -p work/assigned/lexical
mkdir -p work/assigned/curator
mkdir -p work/assigned/diagrammer
mkdir -p work/assigned/planning
mkdir -p work/assigned/coordinator
mkdir -p work/assigned/architect
mkdir -p work/assigned/translator
mkdir -p work/assigned/build-automation

# Add .gitkeep to track empty directories
find work -type d -exec touch {}/.gitkeep \;

# Create initial collaboration artifacts
touch work/collaboration/AGENT_STATUS.md
touch work/collaboration/HANDOFFS.md
touch work/collaboration/WORKFLOW_LOG.md

# Create README
cat > work/README.md <<'EOF'
# Work Directory - Multi-Agent Orchestration

This directory contains the file-based orchestration system for coordinating
multiple specialized agents.

See docs/architecture/design/async_multiagent_orchestration.md for details.
EOF
```

**Adding a new agent:**

```bash
# Create agent directory
mkdir -p work/assigned/new-agent
touch work/assigned/new-agent/.gitkeep

# Update AGENT_STATUS.md
echo "## new-agent" >> work/collaboration/AGENT_STATUS.md
echo "- Status: Active" >> work/collaboration/AGENT_STATUS.md
echo "- Last seen: N/A" >> work/collaboration/AGENT_STATUS.md
```

### File Naming Conventions

**Task files:**

Format: `YYYY-MM-DDTHHMM-<agent>-<slug>.yaml`

Examples:
- `2025-11-20T1430-structural-repomap.yaml`
- `2025-11-20T1445-lexical-voice-analysis.yaml`
- `2025-11-20T1500-curator-glossary-sync.yaml`

**Rules:**
- Timestamp in ISO 8601 format (YYYY-MM-DDTHHMM)
- Agent name matches directory under `work/assigned/`
- Slug is lowercase, hyphen-separated, descriptive
- Extension is `.yaml` (not `.yml`)

**Log files (optional):**

Format: `YYYY-MM-DD-<agent>-<task-id>.log`

Examples:
- `2025-11-20-structural-2025-11-20T1430-structural-repomap.log`

**Rules:**
- Date prefix for natural sorting
- Agent name for filtering
- Task ID for correlation with task file

### Collaboration Artifacts

**AGENT_STATUS.md:**

Tracks current state of all agents for coordination and monitoring.

```markdown
# Agent Status Dashboard

_Last updated: 2025-11-20T15:00:00Z_

## structural
- **Status**: Idle
- **Last task**: 2025-11-20T1430-structural-repomap
- **Last seen**: 2025-11-20T14:45:00Z
- **Tasks completed today**: 3

## lexical
- **Status**: In Progress
- **Current task**: 2025-11-20T1445-lexical-voice-analysis
- **Started**: 2025-11-20T14:45:00Z
- **Tasks completed today**: 1

...
```

**HANDOFFS.md:**

Logs agent-to-agent transitions for traceability.

```markdown
# Agent Handoff Log

## 2025-11-20 14:45 - Structural → Lexical

**Artefacts:** docs/REPO_MAP.md, docs/SURFACES.md  
**Reason:** Voice/style pass required after structural generation  
**Task ID:** 2025-11-20T1445-lexical-voice-analysis  
**Status:** Assigned

## 2025-11-20 15:00 - Lexical → Curator

**Artefacts:** docs/LEX_REPORT.md, docs/LEX_DELTAS.md  
**Reason:** Consistency validation needed  
**Task ID:** 2025-11-20T1500-curator-validation  
**Status:** In Progress

...
```

**WORKFLOW_LOG.md:**

System-wide orchestration events.

```markdown
# Workflow Orchestration Log

## 2025-11-20

**14:30** - Task created: `2025-11-20T1430-structural-repomap`  
**14:31** - Coordinator assigned task to structural agent  
**14:45** - Structural agent completed task  
**14:45** - Coordinator created follow-up task: `2025-11-20T1445-lexical-voice-analysis`  
**14:46** - Lexical agent started task  
**14:55** - Lexical agent completed task  
**15:00** - Coordinator detected no pending tasks  

...
```

### Validation Rules

**Directory structure validation:**

```bash
#!/bin/bash
# validation/validate-work-structure.sh

# Check required directories exist
required_dirs=(
  "work/inbox"
  "work/assigned"
  "work/done"
  "work/archive"
  "work/collaboration"
)

for dir in "${required_dirs[@]}"; do
  if [ ! -d "$dir" ]; then
    echo "❗️ Missing required directory: $dir"
    exit 1
  fi
done

# Check each agent has a directory
for profile in .github/agents/*.agent.md; do
  agent_name=$(basename "$profile" .agent.md)
  if [ ! -d "work/assigned/$agent_name" ]; then
    echo "⚠️ Agent '$agent_name' missing directory under work/assigned/"
  fi
done

echo "✅ Work directory structure valid"
```

**Task file naming validation:**

```bash
#!/bin/bash
# validation/validate-task-naming.sh

# Check all task files follow naming convention
for task in work/inbox/*.yaml work/assigned/*/*.yaml work/done/*.yaml; do
  filename=$(basename "$task")
  if ! echo "$filename" | grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{4}-[a-z-]+-[a-z0-9-]+\.yaml$'; then
    echo "⚠️ Invalid task filename: $filename"
  fi
done

echo "✅ Task naming validation complete"
```

### Archive Management

**Periodic cleanup script:**

```bash
#!/bin/bash
# ops/scripts/planning/archive-done-tasks.sh

# Archive tasks older than 30 days
retention_days=30
cutoff_date=$(date -d "$retention_days days ago" +%Y-%m-%d)

for task in work/done/*.yaml; do
  task_date=$(basename "$task" | cut -d'T' -f1)
  if [[ "$task_date" < "$cutoff_date" ]]; then
    year_month=$(echo "$task_date" | cut -d'-' -f1,2)
    mkdir -p "work/archive/$year_month"
    mv "$task" "work/archive/$year_month/"
    echo "Archived: $(basename $task)"
  fi
done
```

**Compression script:**

```bash
#!/bin/bash
# ops/scripts/planning/compress-archive.sh

# Compress archive directories older than 3 months
cutoff_date=$(date -d "3 months ago" +%Y-%m)

for archive_dir in work/archive/*/; do
  year_month=$(basename "$archive_dir")
  if [[ "$year_month" < "$cutoff_date" ]]; then
    tar -czf "work/archive/${year_month}.tar.gz" -C "work/archive" "$year_month"
    rm -rf "$archive_dir"
    echo "Compressed: $year_month"
  fi
done
```

### Considered Alternatives

**1. Single Flat Directory**

- **Approach**: All tasks in `work/tasks/`, status only in YAML
- **Pros**: Simpler directory structure
- **Cons**: Loses atomic state transitions, requires scanning all files, no clear ownership
- **Reason rejected**: Loses key benefits of directory-based state

**2. Agent-First Hierarchy**

- **Approach**: `work/<agent>/inbox/`, `work/<agent>/assigned/`, `work/<agent>/done/`
- **Pros**: Agent isolation, clear per-agent view
- **Cons**: Coordinator can't easily see all pending work, cross-agent visibility harder
- **Reason rejected**: Makes coordination more complex

**3. Status Directories**

- **Approach**: `work/new/`, `work/assigned/`, `work/in_progress/`, `work/done/`, `work/error/`
- **Pros**: Status immediately visible, simpler than hierarchical
- **Cons**: Loses agent ownership, assigned and in_progress mixing, no per-agent polling
- **Reason rejected**: Ownership ambiguity, harder for agents to find their tasks

**4. Database-Backed with Filesystem Cache**

- **Approach**: SQLite database as source of truth, directories as cache
- **Pros**: ACID transactions, complex queries
- **Cons**: Adds complexity, binary format not Git-native, cache invalidation issues
- **Reason rejected**: Over-engineered, loses simplicity

---

**Related ADRs:**

- [ADR-002: File-Based Asynchronous Agent Coordination](ADR-008-file-based-async-coordination.md)
- [ADR-003: Task Lifecycle and State Management](ADR-003-task-lifecycle-state-management.md)
- [ADR-005: Coordinator Agent Pattern](ADR-005-coordinator-agent-pattern.md)

**References:**

- [Async Multi-Agent Orchestration Architecture](../design/async_multiagent_orchestration.md)
- Issue #8: Asynchronous Multi-Agent Orchestration (File-Driven Model)
