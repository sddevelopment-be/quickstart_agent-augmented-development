# Agents Quickstart

This folder contains the shared instructions for all agents in this repository.

The idea:

- **Generic guidelines live here** (`.github/agents/*.md`).
- **Repo-specific rules live in** `docs/` (`VISION.md`, `specific_guidelines.md`).
- **Specialist agents live in** `.github/agents/*.agent.md`.

Agents should always combine both: generic + repo-specific.

---

## 1. Files in this folder

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

- `*.agent.md`  
  Predefined roles (planner, researcher, implementer, …).  
  Each file documents:
  - the purpose of the specialist
  - typical inputs and outputs
  - when to hand over to another agent

---

## 2. Customizing this template

When you create a new repository from this template:

1. Update `docs/VISION.md` to describe what this repo is trying to achieve.
2. Update `docs/specific_guidelines.md` with any hard rules or constraints.
3. Review the specialists in `.github/agents/*.agent.md`:
   - Delete ones you will not use.
   - Rename or adjust their responsibilities.
4. Optionally, add your own specialist files for your domain.

---

## 3. How agents should combine these documents

When you configure an agent, instruct it to:

1. Read `docs/VISION.md`.
2. Read `docs/specific_guidelines.md`.
3. Read `.github/agents/general_guidelines.md`.
4. Read `.github/agents/operational_guidelines.md`.
5. Read its own specialist definition defined in `.github/agents/*.agent.md`.
6. If resuming work, follow `.github/agents/rehydrate.md`.
7. If starting new work, follow `.github/agents/bootstrap.md`.

This keeps behaviour consistent while letting each repo define its own purpose.
