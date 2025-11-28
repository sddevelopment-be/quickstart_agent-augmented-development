# Repository Surfaces

_Version: 1.0.0_  
_Generated: 2025-11-23T22:36:42Z_  
_Agent: Bootstrap Bill_  
_Task: 2025-11-23T2157-bootstrap-bill-repomap-update_

## Overview

This document catalogs the public interfaces, entry points, and interaction surfaces of the quickstart_agent-augmented-development repository. It serves as a reference for agents, automation, and human contributors to understand how to interact with the system.

## Table of Contents

1. [Agent Entry Points](#agent-entry-points)
2. [Task Submission Surfaces](#task-submission-surfaces)
3. [Orchestration Interfaces](#orchestration-interfaces)
4. [Validation Surfaces](#validation-surfaces)
5. [Documentation Surfaces](#documentation-surfaces)
6. [CI/CD Integration Points](#cicd-integration-points)
7. [Configuration Surfaces](#configuration-surfaces)
8. [Agent Communication Protocols](#agent-communication-protocols)

---

## Agent Entry Points

### Agent Initialization

**Primary Surface:** `AGENTS.md` (root)

```markdown
Location: /AGENTS.md
Purpose: Agent Specification Document - initialization protocol
Format: Markdown with embedded directives
Usage: Read first before any agent operation
```

**Context Layers (Load Order):**

1. **Bootstrap Protocol**: `AGENTS.md` Section 1
2. **General Guidelines**: `.github/agents/guidelines/general_guidelines.md`
3. **Operational Guidelines**: `.github/agents/guidelines/operational_guidelines.md`
4. **Project Vision**: `docs/VISION.md`
5. **Project Specific**: `docs/specific_guidelines.md`
6. **Command Aliases**: `.github/agents/aliases.md`

**Validation Command:**
```bash
/validate-alignment
```

### Agent Directives (Externalized Modules)

**Location:** `.github/agents/directives/`

| Code | File | Surface Type | Load Pattern |
|------|------|--------------|--------------|
| 001 | `001_cli_shell_tooling.md` | Tool usage | `/require-directive 001` |
| 002 | `002_context_notes.md` | Context rules | `/require-directive 002` |
| 003 | `003_repository_quick_reference.md` | Structure ref | `/require-directive 003` |
| 004 | `004_documentation_context_files.md` | Doc patterns | `/require-directive 004` |
| 005 | `005_agent_profiles.md` | Role catalog | `/require-directive 005` |
| 006 | `006_version_governance.md` | Versioning | `/require-directive 006` |
| 007 | `007_agent_declaration.md` | Authority | `/require-directive 007` |
| 008 | `008_artifact_templates.md` | Templates | `/require-directive 008` |
| 009 | `009_role_capabilities.md` | Capabilities | `/require-directive 009` |
| 010 | `010_mode_protocol.md` | Mode switching | `/require-directive 010` |
| 011 | `011_risk_escalation.md` | Risk handling | `/require-directive 011` |
| 012 | `012_operating_procedures.md` | Common ops | `/require-directive 012` |
| 013 | `013_tooling_setup.md` | Tool setup | `/require-directive 013` |
| 014 | `014_worklog_creation.md` | Work logs | `/require-directive 014` |
| 015 | `015_store_prompts.md` | Prompt storage | `/require-directive 015` |

**Manifest:** `.github/agents/directives/manifest.json`

---

## Task Submission Surfaces

### Task Creation Interface

**Primary Surface:** `work/inbox/`

**File Format:** YAML (ISO 8601 timestamp + slug)

```yaml
# Naming Convention: YYYY-MM-DDTHHMM-<agent>-<slug>.yaml
# Example: 2025-11-23T1500-architect-design-api.yaml

id: "2025-11-23T1500-architect-design-api"
agent: "architect"
status: "new"
title: "Design REST API for user management"
artefacts:
  - docs/architecture/design/user-api.md
  - docs/architecture/diagrams/user-api-sequence.puml
context:
  repo: "sddevelopment-be/quickstart_agent-augmented-development"
  branch: "main"
  notes:
    - "Focus on RESTful principles"
    - "Consider authentication patterns"
priority: "normal"
mode: "/analysis-mode"
created_at: "2025-11-23T15:00:00Z"
created_by: "stijn"
```

**Template Location:** `docs/templates/agent-tasks/task-descriptor.yaml`

**Validation:**
```bash
python validation/validate-task-schema.py work/collaboration/inbox/task-file.yaml
```

### Task Status Surface

**Location:** `work/assigned/<agent>/`, `work/done/`

**Status Values:**
- `new`: In inbox, awaiting assignment
- `assigned`: In agent queue
- `in_progress`: Agent actively working
- `done`: Completed, moved to work/done/
- `error`: Failed, requires intervention

**Status Transitions (Agent Responsibility):**

```yaml
# When picking up task
status: "in_progress"
started_at: "2025-11-23T15:05:00Z"

# When completing task
status: "done"
result:
  summary: "Completed API design"
  artefacts:
    - docs/architecture/design/user-api.md
  completed_at: "2025-11-23T15:30:00Z"

# When failing
status: "error"
error:
  message: "Missing required context"
  details: "Need authentication requirements"
  failed_at: "2025-11-23T15:10:00Z"
```

---

## Orchestration Interfaces

### Agent Orchestrator

**Primary Surface:** `ops/scripts/orchestration/agent_orchestrator.py`

**Invocation:**
```bash
# Manual execution
python ops/scripts/orchestration/agent_orchestrator.py

# Via GitHub Actions
# Trigger: .github/workflows/orchestration.yml
```

**Functions:**
- Assigns tasks from inbox to agent queues
- Monitors task lifecycle
- Creates follow-up tasks from handoffs
- Updates collaboration artifacts
- Generates system health metrics

**Configuration:** Internal constants (no external config file)

### Agent Base Interface

**Primary Surface:** `ops/scripts/orchestration/agent_base.py`

**Abstract Methods (Must Implement):**

```python
class AgentBase:
    def process_task(self, task_file: str) -> bool:
        """Process a single task file. Return True on success."""
        pass
    
    def get_agent_name(self) -> str:
        """Return agent identifier matching queue name."""
        pass
```

**Usage Pattern:**
```python
from work.scripts.agent_base import AgentBase

class MyAgent(AgentBase):
    def get_agent_name(self) -> str:
        return "my-agent"
    
    def process_task(self, task_file: str) -> bool:
        # Implementation
        return True

if __name__ == "__main__":
    agent = MyAgent()
    agent.run()  # Poll assigned/my-agent/ directory
```

**Reference:** `ops/scripts/orchestration/example_agent.py`

### Handoff Interface

**Location:** Task YAML `result` block

**Pattern:**

```yaml
result:
  summary: "Completed architecture design"
  artefacts:
    - docs/architecture/design/user-api.md
  next_agent: "backend-dev"
  next_task_title: "Implement user API endpoints"
  next_artefacts:
    - src/api/users.py
    - tests/api/test_users.py
  next_task_notes:
    - "Follow design from docs/architecture/design/user-api.md"
    - "Use FastAPI framework"
  completed_at: "2025-11-23T15:30:00Z"
```

**Orchestrator Behavior:**
- Creates new task in `work/inbox/`
- Sets status to `new`
- Links via `context.parent_task_id`

---

## Validation Surfaces

### Task Schema Validation

**Surface:** `validation/validate-task-schema.py`

**Usage:**
```bash
# Validate single task
python validation/validate-task-schema.py work/collaboration/inbox/task.yaml

# Exit codes:
#   0 = Valid
#   1 = Invalid schema
```

**Schema Rules:**
- Required fields: `id`, `agent`, `status`, `artefacts`
- Timestamp format: ISO 8601
- Status enum: `new`, `assigned`, `in_progress`, `done`, `error`
- Agent name: lowercase, hyphen-separated

### Task Naming Validation

**Surface:** `validation/validate-task-naming.sh`

**Usage:**
```bash
bash validation/validate-task-naming.sh work/collaboration/inbox/task-file.yaml

# Validates: YYYY-MM-DDTHHMM-<agent>-<slug>.yaml
```

### Work Structure Validation

**Surface:** `validation/validate-work-structure.sh`

**Usage:**
```bash
bash validation/validate-work-structure.sh

# Checks:
# - All agent directories exist
# - Collaboration artifacts present
# - No orphaned tasks
```

### Repository Validation

**Surface:** `validation/validate_repo.sh`

**Usage:**
```bash
bash validation/validate_repo.sh

# Validates:
# - Directory structure
# - Required files present
# - Symlinks valid
```

---

## Documentation Surfaces

### HOW_TO_USE Guides

**Location:** `docs/HOW_TO_USE/`

| Guide | Surface | Audience |
|-------|---------|----------|
| `QUICKSTART.md` | Getting started | New users |
| `multi-agent-orchestration.md` | Orchestration system | Agent developers |
| `creating-agents.md` | Agent development | Agent developers |
| `copilot-tooling-setup.md` | CLI tools | Contributors |
| `ci-orchestration.md` | CI/CD integration | DevOps |
| `testing-orchestration.md` | Testing patterns | QA/Developers |
| `ISSUE_TEMPLATES_GUIDE.md` | Issue templates | Contributors |

### Architecture Decision Records

**Location:** `docs/architecture/adrs/`

**Format:** Markdown with MADR template

**Index:** `docs/architecture/adrs/README.md`

**Key ADRs:**
- ADR-001: Modular agent directive system
- ADR-002: Portability enhancement (OpenCode)
- ADR-003: Task lifecycle state management
- ADR-004: Work directory structure
- ADR-005: Coordinator agent pattern
- ADR-006: Three-layer governance model
- ADR-007: Repository restructuring
- ADR-008: File-based async coordination
- ADR-009: Orchestration metrics standard

### Task Templates

**Location:** `docs/templates/agent-tasks/`

**Available Templates:**

| Template | Purpose |
|----------|---------|
| `task-base.yaml` | Base task structure |
| `task-context.yaml` | Context block examples |
| `task-descriptor.yaml` | Complete descriptor |
| `task-error.yaml` | Error handling |
| `task-examples.yaml` | Example tasks |
| `task-result.yaml` | Result block examples |
| `task-timestamps.yaml` | Timestamp patterns |

**Usage:**
```bash
cp docs/templates/agent-tasks/task-descriptor.yaml work/inbox/2025-11-23T1600-my-task.yaml
# Edit and customize
```

---

## CI/CD Integration Points

### GitHub Actions Workflows

**Location:** `.github/workflows/`

#### Orchestration Workflow

**Surface:** `.github/workflows/orchestration.yml`

**Trigger:**
- Cron schedule (configurable)
- Manual workflow_dispatch
- Repository dispatch events

**Actions:**
1. Checkout repository
2. Install Python dependencies
3. Run `ops/scripts/orchestration/agent_orchestrator.py`
4. Commit state changes
5. Push updates

#### Validation Workflow

**Surface:** `.github/workflows/validation.yml`

**Trigger:**
- Push to main
- Pull request

**Actions:**
1. Validate task schemas
2. Validate work structure
3. Validate repository structure
4. Report results

#### Copilot Setup Workflow

**Surface:** `.github/workflows/copilot-setup.yml`

**Trigger:** Manual workflow_dispatch

**Actions:**
1. Install ripgrep (rg)
2. Install fd
3. Install ast-grep
4. Install jq
5. Install yq
6. Install fzf

**Usage:**
```bash
# Via GitHub UI: Actions → Copilot Setup → Run workflow
# Or via CLI:
gh workflow run copilot-setup.yml
```

#### Diagram Rendering Workflow

**Surface:** `.github/workflows/diagram-rendering.yml`

**Trigger:** Push with `.puml` file changes

**Actions:**
1. Detect PlantUML files
2. Generate PNG diagrams
3. Commit rendered images

---

## Configuration Surfaces

### OpenCode Configuration

**Surface:** `opencode-config.json`

**Purpose:** Cross-platform agent portability

**Structure:**
```json
{
  "agents": [
    {
      "name": "agent-name",
      "path": ".github/agents/agent-name.agent.md",
      "capabilities": ["capability1", "capability2"]
    }
  ],
  "directives": [
    {
      "code": "001",
      "path": ".github/agents/directives/001_cli_shell_tooling.md"
    }
  ]
}
```

**Validation:**
```bash
python ops/scripts/opencode-spec-validator.py opencode-config.json
```

**Conversion:**
```bash
python ops/scripts/convert-agents-to-opencode.py
```

### GitHub Labels

**Surface:** `.github/labels.yml`

**Purpose:** Issue/PR label definitions

**Format:**
```yaml
- name: "orchestration"
  color: "0366d6"
  description: "Multi-agent orchestration"
```

### Python Dependencies

**Surface:** `requirements.txt`

**Format:**
```
PyYAML>=6.0
pytest>=7.0
jsonschema>=4.0
```

**Installation:**
```bash
pip install -r requirements.txt
```

---

## Agent Communication Protocols

### Collaboration Artifacts

**Location:** `work/collaboration/`

#### Agent Status Dashboard

**Surface:** `work/collaboration/AGENT_STATUS.md`

**Format:** Markdown table

**Maintained By:** Agent Orchestrator

**Structure:**
```markdown
| Agent | Status | Last Active | Pending Tasks | In Progress |
|-------|--------|-------------|---------------|-------------|
| architect | idle | 2025-11-23T15:00:00Z | 0 | 0 |
```

#### Handoff Log

**Surface:** `work/collaboration/HANDOFFS.md`

**Format:** Markdown log

**Entry Pattern:**
```markdown
## 2025-11-23T15:30:00Z: architect → backend-dev

**Task:** design-user-api
**Artifacts:** docs/architecture/design/user-api.md
**Next Task:** implement-user-api
```

#### Workflow Log

**Surface:** `work/collaboration/WORKFLOW_LOG.md`

**Format:** Timestamped event log

**Event Types:**
- Task assignment
- Status transitions
- Handoff creation
- Error occurrences
- System health metrics

### Work Logs

**Location:** `work/logs/<agent>/`

**Format:** Markdown with frontmatter

**Template:** `.github/agents/directives/014_worklog_creation.md`

**Structure:**
```markdown
---
task_id: "2025-11-23T1500-architect-design-api"
agent: "architect"
started_at: "2025-11-23T15:05:00Z"
completed_at: "2025-11-23T15:30:00Z"
token_count: 12500
context_size: "45KB"
---

# Work Log: Design User API

## Objective
...

## Approach
...

## Results
...

## Challenges
...
```

---

## Summary

### Entry Point Checklist for Agents

1. ✅ Read `AGENTS.md` for initialization
2. ✅ Load context layers (guidelines, vision, specific)
3. ✅ Run `/validate-alignment`
4. ✅ Poll `work/assigned/<agent-name>/` for tasks
5. ✅ Validate task YAML before processing
6. ✅ Update task status to `in_progress`
7. ✅ Create artifacts
8. ✅ Add `result` block with completion metadata
9. ✅ Update status to `done`
10. ✅ Move task to `work/done/`
11. ✅ Create work log in `work/logs/<agent>/`
12. ✅ (Optional) Create handoff in `result.next_agent`

### Key Integration Points

| Surface | Type | Protocol |
|---------|------|----------|
| `work/inbox/` | Task input | YAML file creation |
| `work/assigned/<agent>/` | Task queue | YAML file polling |
| `work/done/` | Task output | YAML file archival |
| `work/collaboration/` | Coordination | Markdown artifacts |
| `work/logs/<agent>/` | Logging | Markdown work logs |
| GitHub Actions | Automation | Workflow triggers |
| Python scripts | Validation | CLI invocation |

---

## Related Artifacts

- **REPO_MAP.md**: Complete repository structure
- **WORKFLOWS.md**: Detailed workflow patterns
- **DEPENDENCIES.md**: Dependency inventory

---

_Generated by Bootstrap Bill (Task: 2025-11-23T2157-bootstrap-bill-repomap-update)_  
_For updates, assign new task to `bootstrap-bill` agent_  
_Surface changes: Track via Git history on this file_
