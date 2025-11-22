---
description: 'Prompt to request creation of a new specialized agent (Manager Mike runs it)'
---

Clear context. Bootstrap as Manager Mike. When ready: 

Create a NEW SPECIALIST agent definition.

Inputs:
- Agent Name: <NAME>
- Purpose: <PRIMARY_MANDATE>
- Primary Focus (bullets): <PRIMARY_FOCUS>
- Secondary Awareness (bullets, optional): <SECONDARY_AWARENESS>
- Avoid (bullets): <OUT_OF_SCOPE>
- Success Criteria (bullets): <SUCCESS_CRITERIA>
- Default Reasoning Mode: <MODE>
- Tools Required (comma list): <TOOLS>
- Operating Procedure (numbered steps): <OPERATING_PROCEDURE>
- Collaboration Protocol (bullets): <COLLABORATION_PROTOCOL>
- Reference Materials (paths/links): <REFERENCES>
- Store synthesized references? (yes/no): <STORE_FLAG>
- Additional Context: <EXTRA>

Task:
1. Validate inputs for scope tightness (flag scope creep if > 2 domains).
2. Use `docs/templates/automation/NEW_SPECIALIST.agent.md` as baseline.
3. Produce file: `agents/<slug>.agent.md` (slug: kebab-case of name).
4. Include initialization declaration section.
5. Add only directives relevant to role (choose from existing `agents/directives/`).
6. Add a brief "First 3 Tasks" bootstrap list in profile.
7. If <STORE_FLAG> = yes: create `docs/references/<slug>-refs.md` summarizing key sources.
8. Write coordination update to `work/coordination/AGENT_STATUS.md` (append).

Output:
- New agent file content (markdown)
- Optional references file content
- Diff snippet for AGENT_STATUS

Constraints:
- Do not duplicate existing agent scopes; propose refinement if overlap >30%.
- Keep purpose ≤ 2 sentences.
- Each focus bullet begins with a verb.
- Avoid hype, flattery, subjective praise.

Ask clarifying questions ONLY if critical fields are blank or ambiguous.
