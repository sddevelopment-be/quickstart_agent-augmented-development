---
description: 'Prompt for Bootstrap Bill to bootstrap a cloned repository for local/project context'
agent: bootstrap-bill
category: repository-structure
complexity: medium
inputs_required: VISION, SCOPE, OUTCOMES
outputs: vision doc, guidelines, repo map, surfaces, workflows
tags: [bootstrap, repository, scaffolding, initialization, structure]
version: 2025-11-22
---

Clear context. Bootstrap as Bootstrap Bill. When ready: 

Perform repository bootstrap & scaffolding.

## Inputs:

- Vision Summary (paragraph): \<VISION>
- Scope (in/out bullets): \<SCOPE>
- Desired Outcomes (bullets): \<OUTCOMES>
- Primary Language: \<LANGUAGE>
- Tech Stack (bullets): \<STACK>
- Communication Preferences (bullets): \<COMM_PREFS>
- Operational Constraints (bullets): \<CONSTRAINTS>
- Agent Roles (bullets): \<ROLES>
- Reference Materials (paths/links): \<REFS>
- Additional Context: \<EXTRA>

## Task:

1. Validate clarity of \<VISION> and boundary firmness in \<SCOPE>.
2. Generate/update:
   - `docs/VISION.md` (structured vision doc)
   - `${LOCAL_DOCTRINE_ROOT}/specific_guidelines.md` (constraints + conventions)
   - `work/bootstrap/REPO_MAP.md` (directory roles)
   - `work/bootstrap/SURFACES.md` (interaction & integration surfaces)
   - `work/bootstrap/WORKFLOWS.md` (agent workflow examples)
3. Recommend initial agent set (list existing + suggested removals/additions).
4. Output scaffold diffs (do not overwrite silently) with creation notices.
5. Summarize next 5 refinement actions.

## Output:

- Vision doc content
- Guidelines content
- REPO_MAP, SURFACES, WORKFLOWS
- Agent recommendation list
- Next actions list

## Constraints:

- No architectural decisions beyond mapping.
- Keep each scaffold artifact concise & machine-consumable.
- Flag ambiguities (≥30% uncertainty) before finalizing.

Ask clarifying questions if \<VISION> vague or missing boundaries.

