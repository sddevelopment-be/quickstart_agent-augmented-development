# Issue Templates Guide

**Audience:** Maintainers and project managers choosing the right template for incoming work (see `docs/audience/line_manager.md` and `docs/audience/ai_power_user.md`).

## Overview

This repository provides specialized GitHub issue templates that integrate seamlessly with our multi-agent workflow system. These templates streamline common agent-driven tasks and ensure proper routing and execution.

## Available Issue Templates

### 1. Bootstrap Repository (`bootstrap-repo.yml`)

**Purpose:** Configure repository vision, guidelines, and agent context

**Assigned to:** Bootstrap Bill (`agent:bootstrap-bill`)

**When to use:**

- Setting up a new repository based on this template
- Defining or updating repository vision and scope
- Establishing operational guidelines and constraints
- Configuring agent communication preferences

**What it does:**

- Captures your repository's vision, scope, and desired outcomes
- Documents technology stack and operational constraints
- Defines communication preferences for agents
- Specifies agent roles and responsibilities
- References existing materials and documentation

**Workflow:**

1. Create an issue using the "Bootstrap Repository" template
2. Fill in vision, scope, and preferences
3. Issue is automatically labeled with `agent:bootstrap-bill`
4. Bootstrap Bill reads the issue and generates:
    - Updated `docs/VISION.md`
    - Updated `docs/specific_guidelines.md`
    - Scaffolding artifacts in `work/` (REPO_MAP, SURFACES, etc.)
    - Recommendations for agent configuration

### 2. Create New Agent (`create-new-agent.yml`)

**Purpose:** Request creation of a new specialized agent

**Assigned to:** Manager Mike (`agent:manager-mike`)

**When to use:**

- Need a specialized agent for a specific domain
- Want to extend the agent ecosystem
- Require custom agent behavior or focus area

**What it does:**

- Defines the new agent's purpose and specialization
- Specifies focus areas, tools, and success criteria
- Documents collaboration protocols
- References template materials and examples

**Workflow:**

1. Create an issue using the "Create New Agent" template
2. Define agent name, purpose, and specialization
3. Issue is automatically labeled with `agent:manager-mike`
4. Manager Mike coordinates:
    - Creates new agent file in `.github/agents/[agent-name].agent.md`
    - Uses `docs/templates/automation/NEW_SPECIALIST.agent.md` as baseline
    - Synthesizes reference materials into `docs/references/` if requested
    - Updates coordination artifacts (AGENT_STATUS, HANDOFFS)
    - May delegate to other specialists (Writer/Editor for documentation)

## Agent Ownership Labels

Issues are automatically tagged with agent-specific labels to route work:

| Label                    | Agent              | Responsibility                       |
|--------------------------|--------------------|--------------------------------------|
| `agent:bootstrap-bill`   | Bootstrap Bill     | Repository structure and scaffolding |
| `agent:manager-mike`     | Manager Mike       | Coordination and routing             |
| `agent:writer-editor`    | Writer/Editor      | Documentation and content            |
| `agent:architect`        | Architect          | System design                        |
| `agent:backend-dev`      | Backend Developer  | Server-side implementation           |
| `agent:frontend-dev`     | Frontend Developer | UI implementation                    |
| `agent:researcher`       | Researcher         | Exploration and analysis             |
| `agent:diagrammer`       | Diagrammer         | Visual documentation                 |
| `agent:scribe`           | Scribe             | Meeting notes                        |
| `agent:curator`          | Curator            | Content organization                 |
| `agent:synthesizer`      | Synthesizer        | Information consolidation            |
| `agent:lexical`          | Lexical Agent      | Terminology and naming               |
| `agent:translator`       | Translator         | Language conversion                  |
| `agent:project-planner`  | Project Planner    | Planning and roadmaps                |
| `agent:build-automation` | Build Automation   | CI/CD and tooling                    |

## How It Fits Together

### 1. Issue Creation

- User creates issue from template
- Template pre-populates with structured fields
- Automatic labels route to appropriate agent

### 2. Agent Detection

- Agents monitor issues with their ownership label
- GitHub's agent panel surfaces relevant issues
- Human can also manually assign via @mention or assignment

### 3. Agent Execution

- Agent reads issue body (structured YAML fields)
- Follows operating procedure from agent definition
- Generates artifacts in `work/` or `output/`
- Updates issue with progress and results

### 4. Artifact Flow

```
Issue → Agent → Artifacts → Review → Integration

Example (Bootstrap):
Issue (bootstrap-repo.yml)
  ↓
Bootstrap Bill reads and processes
  ↓
Generates:
  - docs/VISION.md
  - docs/specific_guidelines.md
  - work/scaffolding/REPO_MAP.md
  ↓
Human reviews and approves
  ↓
Artifacts merged into repository
```

```
Example (New Agent):
Issue (create-new-agent.yml)
  ↓
Manager Mike coordinates
  ↓
Creates:
  - .github/agents/[name].agent.md
  - docs/references/[domain].md (optional)
  - work/coordination/AGENT_STATUS.md (updated)
  ↓
May delegate to Writer/Editor for polish
  ↓
Human reviews and approves
  ↓
New agent ready for use
```

## Best Practices

### For Bootstrap Issues

- Be specific about your vision and constraints
- Include links to reference materials
- Define clear success criteria
- Specify communication preferences early

### For Agent Creation Issues

- Focus agent scope tightly (single responsibility)
- Define clear boundaries (what NOT to do)
- Include reference materials or examples
- Specify collaboration points with other agents

### General

- One template per logical task
- Use additional task/feature templates for complex work
- Review agent output before integration
- Update templates based on learnings

## Integration with Existing Workflow

These issue templates complement the existing hierarchy:

- **Epic** → Strategic initiatives (multi-agent, multi-phase)
- **Feature** → Capabilities (may involve multiple agents)
- **Task** → Discrete work (single agent, clear completion)
- **Bootstrap/Agent Creation** → Infrastructure setup (agent-driven)

Templates work together:

1. Bootstrap repository (foundation)
2. Create specialized agents (capabilities)
3. Use epics/features/tasks (execution)

## Reference

- Templates: `.github/ISSUE_TEMPLATE/`
- Agent definitions: `.github/agents/*.agent.md`
- Agent template: `docs/templates/automation/NEW_SPECIALIST.agent.md`
- Labels: `.github/labels.yml`
- Quickstart: `.github/agents/QUICKSTART.md`

## Troubleshooting

**Agent doesn't respond to issue:**

- Verify correct label is applied (`agent:[name]`)
- Check agent definition exists in `.github/agents/`
- Try mentioning in issue comments
- Use GitHub's agent panel for manual assignment

**Wrong agent picked up the issue:**

- Remove incorrect label
- Add correct `agent:[name]` label
- Comment with instructions if needed

**Need custom template:**

- Copy existing template as baseline
- Follow GitHub issue form schema
- Add appropriate agent label
- Document in this guide
