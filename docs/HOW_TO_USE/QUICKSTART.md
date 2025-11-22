# Agents Quickstart

This repository is set up to host autonomous agents that can help manage, build, and maintain the codebase. This Quickstart guide explains how to use the agent framework provided here.

## Overview of the Agent Framework

### Main guardrail documents

Core ideas of this framework:
- **Generic guidelines live here:** `.github/agents/*.md`.
- **Repo-specific rules live in** `docs/` (`VISION.md`, `specific_guidelines.md`).
- **Specialist agents live in** `.github/agents/*.agent.md`.

Agents should always combine both: generic + repo-specific.

### Specialist agents

Specialist agents are defined in `.github/agents/` as `*.agent.md` files. Each file describes a specific role (e.g., planner, researcher, implementer) with its own purpose and collaboration rules. This is done to limit the scope of each agents, making them more effective, easier to manage, and less likely to forget important contextual details.

To limit the amount of information each agent has to process, agents should only load the generic guidelines, repo-specific rules, and their own specialist definition.

Specialist agents use:

- **Their own role description** from `.github/agents/*.agent.md`.
- **Specific Directives** they need to perform their tasks from `.github/agents/directives` (referenced in their definition).
- **Approaches** defined in `.github/agents/approaches/` (if applicable).
- **Specific work or output folders** defined in `docs/specific_guidelines.md` or their own definition.


---

## 1. Main Guardrail Documents

This repository includes four main guardrail documents that define how agents should behave and operate within any context:

- `general_guidelines.md`  
  How agents should generally behave (tone, safety, collaboration, etc.).

- `operational_guidelines.md`  
  How agents should work inside this repository:
  - where to read from
  - where to write
  - what to treat as authoritative

- `bootstrap.md`  
  How a new agent should start when it has no prior context.

- `rehydrate.md`  
  How an agent should recover context and resume existing work.

---

## 2. Customizing this template

When you create a new repository from this template:

1. Update `docs/VISION.md` to describe what this repo is trying to achieve. Use the template in [docs/templates/project](docs/templates/project/VISION.md) as a baseline.
2. Update `docs/specific_guidelines.md` with any hard rules or constraints. Use the template in [docs/templates/project](docs/templates/project/specific_guidelines.md) as a baseline.
3. Review the specialists in `.github/agents/*.agent.md`:
   - Delete ones you will not use.
   - Rename or adjust their responsibilities.
4. Optionally, add your own specialist files for your domain.

> **Tip:** Use the "Bootstrap Repository" issue template to guide you through this process (see next section).

> **Tip 2:** Combining the 'curator' and `manager` agents is a good way to come up with your own agent definitions. Instruct them to help you design specialist agents for your domain.

---

## 3. Using Issue Templates for Agent Tasks

This repository includes specialized issue templates that streamline agent-driven workflows:

### Bootstrap Repository Template
- **File:** `.github/ISSUE_TEMPLATE/bootstrap-repo.yml`
- **Purpose:** Configure repository vision, guidelines, and agent context
- **Assigned to:** Bootstrap Bill (`agent:bootstrap-bill` label)
- **Use when:** Setting up a new repository or updating vision and operational guidelines

The template captures:
- Repository vision and scope
- Technology stack and constraints
- Communication preferences
- Agent roles and responsibilities
- Reference materials

### Create New Agent Template

- **File:** `.github/ISSUE_TEMPLATE/create-new-agent.yml`
- **Purpose:** Request creation of a new specialized agent
- **Assigned to:** Manager Mike (`agent:manager-mike` label)
- **Use when:** Need a new specialized agent for a specific domain

The template captures:
- Agent name and purpose
- Primary focus and specialization
- Success criteria and tools needed
- Collaboration protocols
- Reference materials (stored in `docs/references/` if requested)

### Agent Ownership Labels

Issues are automatically routed using agent-specific labels defined in `.github/labels.yml`:
- `agent:bootstrap-bill` - Repository structure and scaffolding
- `agent:manager-mike` - Coordination and routing
- `agent:writer-editor` - Documentation and content
- `agent:architect` - System design
- And 11 more specialist labels...

For complete details, see [`docs/HOW_TO_USE/ISSUE_TEMPLATES_GUIDE.md`](/docs/HOW_TO_USE/ISSUE_TEMPLATES_GUIDE.md).

---

## 4. How agents should combine these documents

When you configure an agent, instruct it to:

1. Read `docs/VISION.md`.
2. Read `docs/specific_guidelines.md`.
3. Read `.github/agents/guidelines/general_guidelines.md`.
4. Read `.github/agents/guidelines/operational_guidelines.md`.
5. Read its own specialist definition defined in `.github/agents/*.agent.md`.
6. If resuming work, follow `.github/agents/guidelines/rehydrate.md`.
7. If starting new work, follow `.github/agents/guidelines/bootstrap.md`.

This keeps behaviour consistent while letting each repo define its own purpose.
