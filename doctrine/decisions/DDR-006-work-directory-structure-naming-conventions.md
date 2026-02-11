# DDR-006: Work Directory Structure and Naming Conventions

**Status:** Active  
**Date:** 2026-02-11  
**Supersedes:** Repository-specific directory implementations (elevated from ADR-004)

---

## Context

File-based orchestration systems require consistent directory structures to enable:

- Task organization by lifecycle state
- Clear agent ownership boundaries
- Simple discovery and polling mechanisms
- Support for both automated and manual workflows
- Scalability to multiple agents and numerous tasks

Without standardized structure, universal problems emerge:
- Agents don't know where to find assigned tasks
- Task discovery requires scanning entire repository
- Ownership becomes ambiguous
- Manual intervention is error-prone
- Tooling and automation become fragile

The framework needs a directory layout that:
- Is self-documenting and intuitive
- Supports efficient polling by agents
- Enables atomic filesystem operations
- Works naturally with version control
- Allows for future extensibility

## Decision

**We establish a hierarchical work directory structure organized by lifecycle state and agent ownership as the framework's standard layout.**

### Root Structure

```
work/
  inbox/              # New tasks awaiting assignment
  assigned/           # Tasks assigned to specific agents
    <agent-name>/     # One subdirectory per agent
  done/               # Completed tasks with results
  archive/            # Long-term task retention
  logs/               # Agent execution logs (optional)
  collaboration/      # Cross-agent coordination artifacts (optional)
```

### Agent Subdirectories

Under `work/assigned/`, create one directory per agent:

```
work/assigned/
  structural/
  lexical/
  curator/
  architect/
  <agent-name>/       # Extensible for new agents
```

### Collaboration Artifacts (Optional)

Repositories may implement cross-agent coordination files:

```
work/collaboration/
  AGENT_STATUS.md     # Current state of all agents
  HANDOFFS.md         # Agent-to-agent transition log
  WORKFLOW_LOG.md     # System-wide orchestration events
```

### Naming Conventions

**Task files:**

Format: `YYYY-MM-DDTHHMM-<agent>-<slug>.<ext>`

Examples:
- `2026-02-11T1430-structural-repomap.yaml`
- `2026-02-11T1445-lexical-voice-analysis.json`
- `2026-02-11T1500-curator-glossary-sync.yaml`

**Rules:**
- Timestamp in ISO 8601 format (YYYY-MM-DDTHHMM) for chronological sorting
- Agent name matches directory under `work/assigned/`
- Slug is lowercase, hyphen-separated, descriptive
- Extension indicates format (`.yaml`, `.json`, etc.)

**Archive organization:**

```
work/archive/
  2026-02/            # Monthly grouping
    task-123.yaml
    task-456.yaml
  2026-03/
    ...
```

## Rationale

### Hierarchical Structure Benefits

**State separation:**
- `inbox/`, `assigned/`, `done/` directories make lifecycle immediately visible
- Natural filtering: `ls work/inbox/` shows only unassigned tasks
- Clear boundaries prevent state confusion

**Agent separation:**
- Each agent has dedicated subdirectory
- No mixing of tasks across agents
- Simple polling: agent watches single directory

**Atomic operations:**
- Moving file between directories is atomic (POSIX guarantee)
- State transitions are reliable
- No partial state updates

**Clear ownership:**
- Directory name = agent name
- Task location = ownership signal
- No ambiguity about responsibility

### Collaboration Directory Rationale

**Why separate from tasks?**
- Cross-cutting artifacts not tied to single agent
- Central visibility into system state
- Prevents task directory clutter
- Enables system-wide monitoring

### Naming Convention Rationale

**Why timestamp prefix?**
- Natural chronological sorting via `ls`
- Unique identifiers (unlikely collision with agent+slug)
- Human-readable at a glance
- Searchable and filterable

**Why include agent in filename?**
- Quick identification without reading file
- Searchable across entire work tree
- Consistent with directory structure

**Why monthly archive subdirectories?**
- Prevents single directory with thousands of files (filesystem performance)
- Natural retention boundary (delete dirs >12 months)
- Efficient operations on manageable file counts

### Framework-Level Pattern

This structure applies universally because:
- All file-based systems need state organization
- All frameworks benefit from clear ownership
- All repositories can create directories
- All systems need archive strategies

## Consequences

### Positive

- ✅ **Discoverability:** Clear where to find tasks in any state
- ✅ **Ownership:** Agent name in directory path = explicit ownership
- ✅ **Polling efficiency:** Agents watch single directory, not entire tree
- ✅ **Atomic operations:** File moves between directories are reliable
- ✅ **Extensibility:** Adding agent requires only directory creation
- ✅ **Intuitive:** Structure is self-documenting
- ✅ **Scalability:** Handles hundreds of tasks without performance issues
- ✅ **Version control friendly:** Empty directories tracked via `.gitkeep` files

### Negative (Accepted Trade-offs)

- ⚠️ **Setup overhead:** Each new agent requires directory creation (mitigated by initialization scripts)
- ⚠️ **Directory count:** Many subdirectories may feel cluttered initially (accepted for clarity)
- ⚠️ **Naming discipline:** Requires consistent task naming (enforced by validation)
- ⚠️ **Archive growth:** Monthly subdirectories require periodic cleanup (automation recommended)

## Implementation

Repositories adopting this framework should:

### Initial Setup

Create directory structure:

```bash
#!/bin/bash
# Initialize work directory structure

# Create lifecycle directories
mkdir -p work/inbox
mkdir -p work/assigned
mkdir -p work/done
mkdir -p work/archive
mkdir -p work/logs
mkdir -p work/collaboration

# Add .gitkeep to track empty directories
find work -type d -exec touch {}/.gitkeep \;

# Create README
cat > work/README.md <<'EOF'
# Work Directory

File-based orchestration for multi-agent coordination.

See framework documentation (DDR-004, DDR-006) for details.
EOF
```

### Adding New Agent

```bash
# Create agent directory
agent_name="new-agent"
mkdir -p "work/assigned/$agent_name"
touch "work/assigned/$agent_name/.gitkeep"

# Optional: Update agent status tracker
echo "## $agent_name" >> work/collaboration/AGENT_STATUS.md
echo "- Status: Active" >> work/collaboration/AGENT_STATUS.md
```

### Task Naming Validation

Repositories should validate task filenames:

```bash
#!/bin/bash
# Validate task file naming convention

pattern='^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{4}-[a-z-]+-[a-z0-9-]+\.(yaml|json)$'

for task in work/inbox/*.* work/assigned/*/*.* work/done/*.*; do
  filename=$(basename "$task")
  if ! echo "$filename" | grep -qE "$pattern"; then
    echo "⚠️ Invalid task filename: $filename"
    echo "   Expected: YYYY-MM-DDTHHMM-<agent>-<slug>.<ext>"
  fi
done
```

### Directory Structure Validation

Repositories should validate structure integrity:

```bash
#!/bin/bash
# Validate work directory structure

required_dirs=(
  "work/inbox"
  "work/assigned"
  "work/done"
  "work/archive"
)

for dir in "${required_dirs[@]}"; do
  if [ ! -d "$dir" ]; then
    echo "❗️ Missing required directory: $dir"
    exit 1
  fi
done

echo "✅ Work directory structure valid"
```

### Archive Management

Implement periodic cleanup:

```bash
#!/bin/bash
# Archive tasks older than retention period

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

### Collaboration Artifacts (Optional)

Repositories may track agent status:

**AGENT_STATUS.md:**

```markdown
# Agent Status Dashboard

_Last updated: 2026-02-11T15:00:00Z_

## structural
- **Status**: Idle
- **Last task**: 2026-02-11T1430-structural-repomap
- **Last seen**: 2026-02-11T14:45:00Z

## lexical
- **Status**: In Progress
- **Current task**: 2026-02-11T1445-lexical-voice-analysis
- **Started**: 2026-02-11T14:45:00Z

...
```

**HANDOFFS.md:**

```markdown
# Agent Handoff Log

## 2026-02-11 14:45 - Structural → Lexical

**Artifacts:** docs/REPO_MAP.md, docs/SURFACES.md  
**Reason:** Voice/style pass required  
**Task ID:** 2026-02-11T1445-lexical-voice-analysis  
**Status:** Assigned

...
```

**WORKFLOW_LOG.md:**

```markdown
# Workflow Orchestration Log

## 2026-02-11

**14:30** - Task created: `2026-02-11T1430-structural-repomap`  
**14:31** - Coordinator assigned to structural agent  
**14:45** - Structural completed, created follow-up  
**14:46** - Lexical started task  

...
```

## Related

- **Doctrine:** DDR-004 (File-Based Coordination) - coordination mechanism
- **Doctrine:** DDR-005 (Task Lifecycle) - state management protocol
- **Doctrine:** DDR-007 (Coordinator Pattern) - orchestration using this structure
- **Approach:** Hierarchical organization pattern (framework principles)
- **Implementation:** See repository-specific ADRs for automation scripts
