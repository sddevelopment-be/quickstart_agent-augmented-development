# Repository Surfaces

_Version: 1.0.0_  
_Last Updated: 2026-02-13_  
_Agent: Bootstrap Bill_  
_Purpose: API surfaces, integration points, and interaction contracts_

---

## Overview

This document catalogs the public interfaces, entry points, and interaction surfaces of the quickstart_agent-augmented-development repository. It serves as a reference for agents, automation systems, and human contributors to understand **how to interact** with the system.

### Document Structure

- **Agent Entry Points**: How agents initialize and load context
- **Task Submission Surfaces**: How to submit and manage tasks
- **Orchestration Interfaces**: How tasks flow through the system
- **Framework Integration**: How to use framework components
- **Validation Surfaces**: How to validate artifacts
- **Documentation Surfaces**: How to create and maintain docs
- **CI/CD Integration**: How automation systems interact
- **Configuration Surfaces**: How to configure the system

---

## Table of Contents

1. [Agent Entry Points](#agent-entry-points)
2. [Task Submission Surfaces](#task-submission-surfaces)
3. [Orchestration Interfaces](#orchestration-interfaces)
4. [Framework Integration Points](#framework-integration-points)
5. [Validation Surfaces](#validation-surfaces)
6. [Documentation Surfaces](#documentation-surfaces)
7. [CI/CD Integration Points](#cicd-integration-points)
8. [Configuration Surfaces](#configuration-surfaces)
9. [Domain Model API](#domain-model-api)
10. [CLI Interfaces](#cli-interfaces)

---

## Agent Entry Points

### Agent Initialization Surface

**Primary Surface:** `AGENTS.md` (root)

```markdown
Location: /AGENTS.md
Purpose: Agent Specification Document (ASD) - initialization protocol
Format: Markdown with embedded directives
Required Reading: MUST be read before any agent operation
```

**Initialization Sequence:**

1. **Read AGENTS.md** - Core specification (Section 1-13)
2. **Load Bootstrap Protocol** - `doctrine/guidelines/bootstrap.md`
3. **Load General Guidelines** - `doctrine/guidelines/general_guidelines.md`
4. **Load Operational Guidelines** - `doctrine/guidelines/operational_guidelines.md`
5. **Load Agent Profile** - `doctrine/agents/<agent-name>.agent.md`
6. **Load Required Directives** - Via `/require-directive NNN`
7. **Validate Alignment** - Run `/validate-alignment`
8. **Announce Readiness** - Emit ✅ symbol with context summary

**Example Initialization:**

```markdown
✅ SDD Agent "Bootstrap Bill" initialized.
**Context layers:** Operational ✓, Strategic ✓, Command ✓, Bootstrap ✓, AGENTS ✓.
**Purpose acknowledged:** Repository topology mapping and scaffolding generation.
```

### Directive Loading Surface

**Location:** `doctrine/directives/`

**Load Pattern:**

```markdown
/require-directive 001  # CLI & Shell Tooling
/require-directive 014  # Work Log Creation
/require-directive 016  # Acceptance Test-Driven Development
```

**Directive Manifest:**

| Code | File | Surface Type | Use Case |
|------|------|--------------|----------|
| 001 | `001_cli_shell_tooling.md` | Tool usage | Fast file/text enumeration |
| 002 | `002_context_notes.md` | Context rules | Resolve shorthand precedence |
| 003 | `003_repository_quick_reference.md` | Structure ref | Directory role mapping |
| 004 | `004_documentation_context_files.md` | Doc patterns | Reuse existing docs |
| 006 | `006_version_governance.md` | Versioning | Capture version tags |
| 007 | `007_agent_declaration.md` | Authority | Validate before generating |
| 014 | `014_worklog_creation.md` | Work logs | Token count, context metrics |
| 016 | `016_atdd.md` | Testing | Acceptance TDD workflow |
| 017 | `017_tdd.md` | Testing | Unit TDD workflow |
| 018 | `018_traceable_decisions.md` | Documentation | ADR protocol |
| 028 | `028_bugfixing_techniques.md` | Bug fixing | Test-first bug workflow |
| 034 | `034_specification_driven.md` | Requirements | Functional spec capture |
| 036 | `036_boy_scout_rule.md` | Maintenance | Pre-task cleanup (mandatory) |

**Manifest File:** `doctrine/directives/manifest.json`

### Tactics Discovery Surface

**Location:** `doctrine/tactics/README.md`

**Discovery Mechanism:**

1. **Primary:** Directives explicitly invoke tactics at workflow steps
2. **Secondary:** Agents discover via README and propose to human

**Tactics Index:** 50 procedural guides with applicability matrix

**Example Tactic Invocation:**

```markdown
# Directive 016 invokes ATDD_adversarial-acceptance.tactic.md
# Agent reads tactic and follows step-by-step procedure
```

**Available Tactics:**
- `stopping-conditions.tactic.md` - Define exit criteria
- `premortem-risk-identification.tactic.md` - Failure mode analysis
- `adversarial-testing.tactic.md` - Stress-test proposals
- `AMMERSE-quality-assessment.tactic.md` - Quality framework
- `safe-to-fail-experiment-design.tactic.md` - Exploration under uncertainty
- ... (50 total)

### Agent Profile Surface

**Location:** `doctrine/agents/<agent-name>.agent.md`

**Profile Structure:**

```markdown
# Agent Profile: <Agent Name>

## 1. Context Sources
- Global Principles, Directives, Bootstrap, Local Protocol

## 2. Purpose
- Clear single-sentence purpose statement

## 3. Specialization
- Primary focus, secondary awareness, avoid list, success criteria

## 4. Collaboration Contract
- Never override guidelines
- Stay within specialization
- Ask clarifying questions when uncertain
- Escalate before problems grow

## 5. Mode Defaults
- /analysis-mode, /creative-mode, /meta-mode

## 6. Initialization Declaration
- ✅ Readiness announcement template
```

**21 Available Agents:**
- `analyst-annie.agent.md` - Requirements analysis
- `architect.agent.md` - Architecture design
- `backend-dev.agent.md` - Backend implementation
- `bootstrap-bill.agent.md` - Repository mapping & scaffolding
- `code-reviewer-cindy.agent.md` - Code review
- `curator.agent.md` - Content curation
- `python-pedro.agent.md` - Python development
- ... (21 total)

---

## Task Submission Surfaces

### Task Creation Interface

**Primary Surface:** `work/inbox/`

**File Format:** YAML (ISO 8601 timestamp + agent + slug)

**Naming Convention:**
```
YYYY-MM-DDTHHMM-<agent-name>-<slug>.yaml

Examples:
- 2026-02-13T1500-architect-design-api.yaml
- 2026-02-13T1600-backend-dev-implement-endpoints.yaml
- 2026-02-13T1700-curator-update-docs.yaml
```

**Task YAML Structure:**

```yaml
id: "2026-02-13T1500-architect-design-api"
agent: "architect"
status: "new"
title: "Design REST API for user management"
artefacts:
  - "docs/architecture/design/user-api.md"
  - "docs/architecture/diagrams/user-api-sequence.puml"
context:
  repo: "sddevelopment-be/quickstart_agent-augmented-development"
  branch: "main"
  notes:
    - "Focus on RESTful principles"
    - "Consider authentication patterns"
    - "Reference ADR-012 for API standards"
priority: "normal"  # Optional: low|normal|high|critical
mode: "/analysis-mode"  # Optional: reasoning mode
created_at: "2026-02-13T15:00:00Z"
created_by: "human-username"
```

**Template Location:** `docs/templates/agent-tasks/task-descriptor.yaml`

**Validation:**
```bash
python work/scripts/validate-task-schema.py work/inbox/task.yaml
bash work/scripts/validate-task-naming.sh work/inbox/task.yaml
```

### Task Status Surface

**Location:** Task YAML `status` field

**Status Values:**
- `new` - In inbox, awaiting assignment
- `assigned` - In agent queue, not yet started
- `in_progress` - Agent actively working
- `done` - Completed, moved to work/done/
- `error` - Failed, requires human intervention

**Status Transitions:**

```yaml
# Agent picks up task
status: "in_progress"
started_at: "2026-02-13T15:05:00Z"

# Agent completes task
status: "done"
result:
  summary: "Completed API design with OpenAPI spec"
  artefacts:
    - "docs/architecture/design/user-api.md"
  metrics:
    token_count: 12500
    duration_seconds: 1500
  completed_at: "2026-02-13T15:30:00Z"

# Agent encounters error
status: "error"
error:
  message: "Missing authentication specification"
  details: "Cannot proceed without auth requirements"
  failed_at: "2026-02-13T15:10:00Z"
  retry_allowed: true
  required_action: "Add context.auth_spec field"
```

### Handoff Interface

**Location:** Task YAML `result` block

**Handoff Pattern:**

```yaml
result:
  summary: "Architecture design completed"
  artefacts:
    - "docs/architecture/design/api.md"
  
  # Single handoff
  next_agent: "backend-dev"
  next_task_title: "Implement user API endpoints"
  next_artefacts:
    - "src/api/users.py"
    - "tests/api/test_users.py"
  next_task_notes:
    - "Follow design in docs/architecture/design/api.md"
    - "Use FastAPI framework"
    - "Write tests first (Directive 017)"
  
  # OR: Multiple handoffs (parallel workflows)
  handoffs:
    - agent: "frontend"
      title: "Implement UI components"
      artefacts: ["src/ui/components.tsx"]
      notes: ["Use React + TypeScript"]
    - agent: "backend-dev"
      title: "Implement API endpoints"
      artefacts: ["src/api/endpoints.py"]
      notes: ["Use FastAPI"]
  
  completed_at: "2026-02-13T15:30:00Z"
```

**Orchestrator Behavior:**
- Creates new task in `work/inbox/`
- Sets `context.parent_task_id` to link tasks
- Assigns `created_by: "agent-orchestrator"`

---

## Orchestration Interfaces

### Agent Orchestrator API

**Primary Surface:** `work/scripts/agent_orchestrator.py`

**Invocation:**
```bash
# Manual execution
python work/scripts/agent_orchestrator.py

# Via GitHub Actions
# Trigger: .github/workflows/orchestration.yml (cron or manual)
```

**Functions:**
- Scans `work/inbox/` for new tasks
- Routes tasks to `work/assigned/<agent>/`
- Monitors task lifecycle (timeouts, errors)
- Creates follow-up tasks from handoffs
- Updates collaboration artifacts
- Generates system health metrics

**Configuration:** Internal constants (no external config file)

### Agent Base Interface

**Primary Surface:** `work/scripts/agent_base.py`

**Abstract Class Contract:**

```python
from work.scripts.agent_base import AgentBase

class MyAgent(AgentBase):
    def get_agent_name(self) -> str:
        """Return agent identifier matching queue name."""
        return "my-agent"
    
    def process_task(self, task_file: str) -> bool:
        """
        Process a single task file.
        
        Args:
            task_file: Path to YAML task file
            
        Returns:
            True on success, False on failure
            
        Required Actions:
        1. Update status to in_progress
        2. Perform work
        3. Add result block (success) or error block (failure)
        4. Move to work/done/ (success only)
        """
        pass
```

**Usage Pattern:**

```python
from work.scripts.agent_base import AgentBase
import yaml
from datetime import datetime

class MyAgent(AgentBase):
    def get_agent_name(self) -> str:
        return "my-agent"
    
    def process_task(self, task_file: str) -> bool:
        # 1. Load and update status
        with open(task_file, 'r') as f:
            task = yaml.safe_load(f)
        
        task["status"] = "in_progress"
        task["started_at"] = datetime.utcnow().isoformat() + "Z"
        
        with open(task_file, 'w') as f:
            yaml.safe_dump(task, f)
        
        # 2. Perform work
        try:
            artifacts = self.do_work(task)
            
            # 3. Add result block
            task["result"] = {
                "summary": "Work completed successfully",
                "artefacts": artifacts,
                "completed_at": datetime.utcnow().isoformat() + "Z"
            }
            task["status"] = "done"
            
            with open(task_file, 'w') as f:
                yaml.safe_dump(task, f)
            
            # 4. Move to done/
            os.rename(task_file, f"work/done/{os.path.basename(task_file)}")
            
            return True
            
        except Exception as e:
            # 5. Handle errors
            task["error"] = {
                "message": str(e),
                "failed_at": datetime.utcnow().isoformat() + "Z",
                "retry_allowed": True
            }
            task["status"] = "error"
            
            with open(task_file, 'w') as f:
                yaml.safe_dump(task, f)
            
            return False

if __name__ == "__main__":
    agent = MyAgent()
    agent.run()  # Poll work/assigned/my-agent/ directory
```

**Reference Implementation:** `work/scripts/example_agent.py`

### Collaboration Artifacts Surface

**Location:** `work/collaboration/`

#### Agent Status Dashboard

**Surface:** `work/collaboration/AGENT_STATUS.md`

**Format:** Markdown table

**Maintained By:** Agent Orchestrator

**Structure:**

```markdown
| Agent | Status | Last Active | Pending | In Progress | Completed (24h) | Error |
|-------|--------|-------------|---------|-------------|-----------------|-------|
| architect | active | 2026-02-13T15:30:00Z | 0 | 1 | 5 | 0 |
| backend-dev | idle | 2026-02-13T14:00:00Z | 2 | 0 | 3 | 0 |
| curator | active | 2026-02-13T15:25:00Z | 1 | 0 | 2 | 1 |
```

#### Handoff Log

**Surface:** `work/collaboration/HANDOFFS.md`

**Format:** Markdown log

**Entry Pattern:**

```markdown
## 2026-02-13T15:30:00Z: architect → backend-dev

**Parent Task:** 2026-02-13T1500-architect-design-api
**New Task:** 2026-02-13T1530-backend-dev-implement-api
**Artifacts:** src/api/users.py, tests/api/test_users.py
**Context:** Follow design in docs/architecture/design/api.md
```

#### Workflow Log

**Surface:** `work/collaboration/WORKFLOW_LOG.md`

**Format:** Timestamped event log

**Event Types:**

```markdown
[2026-02-13T15:00:00Z] Task created: 2026-02-13T1500-architect-design-api (by: human)
[2026-02-13T15:01:00Z] Task assigned: architect
[2026-02-13T15:05:00Z] Task started: architect
[2026-02-13T15:30:00Z] Task completed: architect (duration: 25m)
[2026-02-13T15:30:30Z] Handoff created: backend-dev
[2026-02-13T15:31:00Z] Task created: 2026-02-13T1530-backend-dev-implement-api (by: orchestrator)
```

---

## Framework Integration Points

### Framework Runtime API

**Location:** `src/framework/`

**Core Components:**

#### Task Abstraction

```python
from framework.core import Task

task = Task(
    id="task-123",
    agent="architect",
    title="Design API",
    artefacts=["docs/design/api.md"],
    context={"repo": "quickstart", "branch": "main"}
)
```

#### Agent Abstraction

```python
from framework.core import Agent

class MyAgent(Agent):
    def __init__(self):
        super().__init__(name="my-agent", capabilities=["design", "documentation"])
    
    def execute(self, task: Task) -> TaskResult:
        # Implementation
        pass
```

#### Orchestrator Abstraction

```python
from framework.orchestration import Orchestrator

orchestrator = Orchestrator()
orchestrator.route_task(task, agent)
orchestrator.monitor_lifecycle()
```

### Domain Model API (ADR-045)

**Location:** `src/domain/`

**Coverage:** 92% (195 tests)

#### Immutable Models

```python
from src.domain.models import AgentModel, DirectiveModel, ADRModel

# Load agent profile
agent = AgentModel(
    name="architect",
    specialization="Architecture design and documentation",
    modes=["analysis", "creative", "meta"],
    directives=["007", "014", "018"]
)

# Load directive
directive = DirectiveModel(
    code="014",
    title="Work Log Creation",
    applicability=["all agents"],
    related_tactics=["stopping-conditions"]
)

# Load ADR
adr = ADRModel(
    number=45,
    title="Doctrine Concept Domain Model",
    status="Accepted",
    consequences=["Type-safe doctrine access", "Validation automation"]
)
```

#### Parsers

```python
from src.domain.parsers import AgentParser, DirectiveParser, ADRParser

# Parse agent profile
parser = AgentParser()
agent = parser.parse_file("doctrine/agents/architect.agent.md")

# Parse directive
parser = DirectiveParser()
directive = parser.parse_file("doctrine/directives/014_worklog_creation.md")

# Parse ADR
parser = ADRParser()
adr = parser.parse_file("docs/architecture/adrs/ADR-045-doctrine-concept-domain-model.md")
```

#### Validators

```python
from src.domain.validators import AgentValidator, DirectiveValidator

# Validate agent cross-references
validator = AgentValidator(doctrine_root="doctrine/")
errors = validator.validate_agent("architect")

if errors:
    for error in errors:
        print(f"Validation error: {error.message} at {error.location}")

# Validate directive relationships
validator = DirectiveValidator(doctrine_root="doctrine/")
errors = validator.validate_directive("014")
```

**Benefits:**
- Type-safe programmatic access to doctrine artifacts
- Comprehensive validation and integrity checking
- Clear separation between content and structure
- Foundation for future doctrine tooling and automation

---

## Validation Surfaces

### Task Schema Validation

**Surface:** `work/scripts/validate-task-schema.py`

**Usage:**

```bash
# Validate single task
python work/scripts/validate-task-schema.py work/inbox/task.yaml

# Exit codes:
#   0 = Valid
#   1 = Invalid schema
```

**Schema Rules:**
- Required fields: `id`, `agent`, `status`, `artefacts`
- Timestamp format: ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
- Status enum: `new`, `assigned`, `in_progress`, `done`, `error`
- Agent name: lowercase, hyphen-separated
- ID format: `YYYY-MM-DDTHHMM-<agent>-<slug>`

**Validation Errors:**

```json
{
  "errors": [
    {
      "field": "id",
      "message": "Invalid ID format. Expected: YYYY-MM-DDTHHMM-<agent>-<slug>",
      "severity": "error"
    },
    {
      "field": "artefacts",
      "message": "Missing required field: artefacts",
      "severity": "error"
    }
  ]
}
```

### Task Naming Validation

**Surface:** `work/scripts/validate-task-naming.sh`

**Usage:**

```bash
bash work/scripts/validate-task-naming.sh work/inbox/task-file.yaml

# Validates: YYYY-MM-DDTHHMM-<agent>-<slug>.yaml
```

**Naming Rules:**
- Timestamp: ISO 8601 compact format (YYYY-MM-DDTHHMM)
- Agent: Lowercase, hyphen-separated (matching queue name)
- Slug: Kebab-case description (lowercase, hyphens)
- Extension: `.yaml` (not `.yml`)

### Work Structure Validation

**Surface:** `work/scripts/validate-work-structure.sh`

**Usage:**

```bash
bash work/scripts/validate-work-structure.sh

# Checks:
# - All 21 agent directories exist in work/assigned/
# - Collaboration artifacts present
# - No orphaned tasks (wrong queue)
# - Timestamp consistency
```

### Repository Validation

**Surface:** `validation/validate_repo.sh`

**Usage:**

```bash
bash validation/validate_repo.sh

# Validates:
# - Directory structure (doctrine/, docs/, work/, src/, tools/, tests/, fixtures/)
# - Required files present (AGENTS.md, README.md, etc.)
# - Symlinks valid (if any)
# - Configuration files present
```

### Error Reporting Surface (ADR-028)

**Surface:** `tools/scripts/generate-error-summary.py`

**Purpose:** Agent-friendly error aggregation and reporting

**Usage:**

```bash
# Generate error summary from validation runs
python tools/scripts/generate-error-summary.py

# Outputs:
# - errors-summary.json (machine-readable)
# - errors-summary.md (human-readable)
```

**JSON Output Format:**

```json
{
  "summary": {
    "total_errors": 15,
    "by_severity": {"critical": 2, "error": 10, "warning": 3},
    "by_category": {"schema": 5, "naming": 4, "structure": 6}
  },
  "errors": [
    {
      "file": "work/inbox/task.yaml",
      "line": 5,
      "severity": "error",
      "category": "schema",
      "message": "Missing required field: artefacts",
      "suggestion": "Add artefacts: [] field to task YAML"
    }
  ]
}
```

**Markdown Output Format:**

```markdown
# Error Summary

**Total Errors:** 15  
**Critical:** 2 | **Error:** 10 | **Warning:** 3

## Schema Errors (5)

### work/inbox/task.yaml:5
**Severity:** error  
**Message:** Missing required field: artefacts  
**Suggestion:** Add artefacts: [] field to task YAML

## Naming Errors (4)

### work/inbox/2026-02-13-task.yaml
**Severity:** error  
**Message:** Invalid timestamp format in filename  
**Suggestion:** Use format: YYYY-MM-DDTHHMM-<agent>-<slug>.yaml
```

**GitHub Actions Integration:**

```yaml
# .github/workflows/validation-enhanced.yml
- name: Generate Error Summary
  if: failure()
  run: |
    python tools/scripts/generate-error-summary.py
    cat errors-summary.md >> $GITHUB_STEP_SUMMARY
```

---

## Documentation Surfaces

### ADR Creation Surface

**Template:** `docs/templates/architecture/adr-template.md`

**Workflow:**

1. Copy template:
   ```bash
   cp docs/templates/architecture/adr-template.md \
      docs/architecture/adrs/ADR-XXX-title.md
   ```

2. Fill sections:
   - Status: Proposed | Accepted | Deprecated | Superseded
   - Context: Problem statement and constraints
   - Decision: What was decided and why
   - Consequences: Positive, negative, and neutral impacts

3. Update index:
   ```bash
   # Add entry to docs/architecture/adrs/README.md
   ```

4. Submit PR and update status after merge

**ADR Structure:**

```markdown
# ADR-XXX: Title

**Status:** Proposed  
**Date:** YYYY-MM-DD  
**Deciders:** List of decision-makers  
**Consulted:** List of stakeholders consulted  
**Informed:** List of stakeholders informed

## Context

Problem statement and constraints...

## Decision

What was decided and why...

## Consequences

### Positive
- Benefit 1
- Benefit 2

### Negative
- Trade-off 1
- Trade-off 2

### Neutral
- Side-effect 1
```

### Specification Creation Surface

**Template:** `docs/templates/specifications/feature-spec-template.md`

**Workflow (Directive 034):**

1. Copy template:
   ```bash
   cp docs/templates/specifications/feature-spec-template.md \
      specifications/features/feature-name.md
   ```

2. Define personas from `docs/audience/`

3. Write Given/When/Then acceptance criteria

4. Apply MoSCoW prioritization (MUST/SHOULD/COULD/WON'T)

5. Link to related ADRs

**Specification Structure:**

```markdown
# Feature: Feature Name

**Version:** 1.0  
**Status:** Draft | Approved | Implemented  
**Target Personas:** Developer, Architect, End User

## Overview

Brief description...

## Acceptance Criteria

### Scenario 1: Title

**Priority:** MUST

**Given** initial state  
**When** action occurs  
**Then** expected outcome

### Scenario 2: Title

**Priority:** SHOULD

**Given** initial state  
**When** action occurs  
**Then** expected outcome

## Related ADRs

- ADR-012: Testing Strategy
- ADR-018: Traceable Decisions

## Implementation Notes

Technical considerations...
```

### Work Log Creation Surface (Directive 014)

**Location:** `work/reports/logs/<agent>/`

**Format:** Markdown with YAML frontmatter

**Template Structure:**

```markdown
---
task_id: "2026-02-13T1500-architect-design-api"
agent: "architect"
started_at: "2026-02-13T15:05:00Z"
completed_at: "2026-02-13T15:30:00Z"
token_count: 12500
context_size: "45KB"
status: "success"
---

# Work Log: Design REST API

## Objective

Clear statement of what was to be accomplished...

## Approach

How the work was structured...

## Results

What was delivered:
- docs/architecture/design/user-api.md
- docs/architecture/diagrams/user-api-sequence.puml

## Challenges

Issues encountered and how they were resolved...

## Lessons Learned

Insights for future work...

## Next Steps

Recommendations for follow-up work...
```

**Required Fields:**
- `task_id` - Links to task YAML
- `agent` - Agent name
- `started_at` / `completed_at` - Timestamps
- `token_count` - Approximate tokens consumed
- `context_size` - Context window usage

---

## CI/CD Integration Points

### GitHub Actions Workflows

**Location:** `.github/workflows/`

#### Validation Workflow

**Surface:** `.github/workflows/validation-enhanced.yml`

**Trigger:** Push, Pull Request

**Steps:**
1. Code quality checks (Black, Ruff)
2. Unit tests (pytest)
3. Coverage report (pytest-cov → SonarCloud)
4. Schema validation (task YAML, JSON schemas)
5. E2E orchestration tests
6. Error summary generation

**Configuration:**

```yaml
name: Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      
      # Code quality
      - run: black --check src/ tools/ tests/
      - run: ruff check src/ tools/ tests/
      
      # Tests
      - run: python3 -m pytest --cov=src --cov-report=xml
      
      # Schema validation
      - run: |
          for task in work/inbox/*.yaml work/assigned/*/*.yaml; do
            [ -f "$task" ] && python work/scripts/validate-task-schema.py "$task"
          done
      
      # Error summary
      - if: failure()
        run: |
          python tools/scripts/generate-error-summary.py
          cat errors-summary.md >> $GITHUB_STEP_SUMMARY
```

#### Orchestration Workflow

**Surface:** `.github/workflows/orchestration.yml`

**Trigger:** Cron schedule (configurable), Manual workflow_dispatch

**Steps:**
1. Checkout repository
2. Install Python dependencies
3. Run `work/scripts/agent_orchestrator.py`
4. Commit state changes (task movements, status updates)
5. Push updates to branch

**Configuration:**

```yaml
name: Agent Orchestration

on:
  schedule:
    - cron: '*/15 * * * *'  # Every 15 minutes
  workflow_dispatch:

jobs:
  orchestrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python work/scripts/agent_orchestrator.py
      - run: |
          git config user.name "Agent Orchestrator"
          git config user.email "orchestrator@example.com"
          git add work/
          git commit -m "chore: orchestrator update" || true
          git push
```

#### Copilot Setup Workflow

**Surface:** `.github/workflows/copilot-setup.yml`

**Trigger:** Manual workflow_dispatch

**Purpose:** Install CLI tooling (rg, fd, ast-grep, jq, yq, fzf)

**Steps:**
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

**Steps:**
1. Detect modified PlantUML files
2. Generate PNG diagrams
3. Commit rendered images

---

## Configuration Surfaces

### Doctrine Configuration

**Surface:** `.doctrine-config/config.yaml`

**Created By:** Bootstrap Bill during repository setup

**Structure:**

```yaml
# Repository Metadata
repository:
  name: "quickstart_agent-augmented-development"
  description: "AI-augmented development quickstart"
  version: "1.1.0"

# Path Variables (customize for your repository)
paths:
  workspace_root: "work"          # Task orchestration workspace
  doc_root: "docs"                # Documentation root
  spec_root: "specifications"     # Specification files
  output_root: "output"           # Generated artifacts

# Tool Integrations (enable based on detected tooling)
integrations:
  github: true                    # .github/ directory detected
  claude: false                   # .claude/ directory not found
  cursor: false                   # .cursor/ directory not found
  copilot: true                   # .github/copilot/ detected

# Agent Configuration
agents:
  enabled: true
  profiles_path: "doctrine/agents"
  directives_path: "doctrine/directives"
  tactics_path: "doctrine/tactics"
```

**Path Detection Heuristics:**
- Look for existing `work/`, `docs/`, `specifications/` directories
- Check `.gitignore` for output directory patterns
- Scan for task YAML files to identify orchestration workspace
- Inspect CI configs for build output paths

### Local Doctrine Extensions

**Surface:** `.doctrine-config/specific_guidelines.md`

**Purpose:** Repository-specific guidelines that extend (but don't override) core doctrine

**Structure:**

```markdown
# Project-Specific Guidelines

_Version: 1.0.0_  
_Last Updated: YYYY-MM-DD_

## Repository-Specific Constraints

- Constraint 1
- Constraint 2

## Project Conventions

- Convention 1
- Convention 2

## Tool Preferences

- Tool 1 configuration
- Tool 2 configuration
```

**Hard Constraint:** Cannot override `doctrine/guidelines/general_guidelines.md` or `doctrine/guidelines/operational_guidelines.md`

### Python Configuration

**Surface:** `pyproject.toml`

**Key Sections:**

```toml
[project]
name = "quickstart_agent-augmented-development"
version = "1.1.0"
requires-python = ">=3.11"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--strict-markers --cov=src --cov-report=term-missing"
pythonpath = ["src", "tools", "."]

[tool.black]
line-length = 100
target-version = ["py311"]

[tool.ruff]
line-length = 100
target-version = "py311"
```

### SonarCloud Configuration

**Surface:** `sonar-project.properties`

**Key Properties:**

```properties
sonar.projectKey=sddevelopment-be_quickstart_agent-augmented-development
sonar.organization=sddevelopment-be

# Source directories
sonar.sources=src,tools
sonar.tests=tests

# Coverage reports
sonar.python.coverage.reportPaths=coverage.xml

# Exclusions
sonar.exclusions=**/node_modules/**,**/__pycache__/**,**/venv/**
```

---

## CLI Interfaces

### Task Management CLI

```bash
# Create task
cp docs/templates/agent-tasks/task-descriptor.yaml work/inbox/2026-02-13T1500-architect-design-api.yaml

# Validate task
python work/scripts/validate-task-schema.py work/inbox/2026-02-13T1500-architect-design-api.yaml

# Run orchestrator
python work/scripts/agent_orchestrator.py

# View agent status
cat work/collaboration/AGENT_STATUS.md

# View handoffs
cat work/collaboration/HANDOFFS.md
```

### Testing CLI

```bash
# Run all tests
python3 -m pytest

# Run specific test suite
python3 -m pytest tests/unit/domain/

# Run with coverage
python3 -m pytest --cov=src --cov-report=html

# Run E2E orchestration tests
python3 -m pytest work/scripts/test_orchestration_e2e.py
```

### Validation CLI

```bash
# Validate repository structure
bash validation/validate_repo.sh

# Validate work directory structure
bash work/scripts/validate-work-structure.sh

# Validate task naming
bash work/scripts/validate-task-naming.sh work/inbox/*.yaml

# Generate error summary
python tools/scripts/generate-error-summary.py
```

### Agent Profile Export CLI

```bash
# Export to Copilot format
python tools/exporters/copilot/export_to_copilot.py

# Export to Claude Desktop format
python tools/exporters/claude/export_to_claude.py

# Export to OpenCode format
python tools/exporters/opencode/export_to_opencode.py
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
11. ✅ Create work log in `work/reports/logs/<agent>/` (Directive 014)
12. ✅ (Optional) Create handoff in `result.next_agent`

### Key Integration Points

| Surface | Type | Protocol |
|---------|------|----------|
| `work/inbox/` | Task input | YAML file creation |
| `work/assigned/<agent>/` | Task queue | YAML file polling |
| `work/done/` | Task output | YAML file archival |
| `work/collaboration/` | Coordination | Markdown artifacts |
| `work/reports/logs/<agent>/` | Logging | Markdown work logs |
| GitHub Actions | Automation | Workflow triggers |
| Python scripts | Validation | CLI invocation |
| Domain models | Framework | Python API |
| Error summary | Reporting | JSON/Markdown output |

---

## Related Artifacts

- **[REPO_MAP.md](REPO_MAP.md)**: Complete repository structure and navigation
- **[VISION.md](VISION.md)**: Project vision and strategic goals
- **[docs/WORKFLOWS.md](docs/WORKFLOWS.md)**: Detailed workflow patterns
- **[DEPENDENCIES.md](DEPENDENCIES.md)**: Complete dependency inventory
- **[TESTING_STATUS.md](TESTING_STATUS.md)**: Test suite status
- **[SONARCLOUD_FIXES.md](SONARCLOUD_FIXES.md)**: Code quality status

---

_Generated by Bootstrap Bill_  
_For updates: Assign task to `bootstrap-bill` agent in `work/inbox/`_  
_Last Updated: 2026-02-13_
