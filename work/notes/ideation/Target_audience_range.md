# Extend usability to target audiences

Most underserved personas based on the mapped set (README, AGENTS, VISION, key docs, HOW_TO_USE, architecture overview/vision, ADRs 001–010):

- Line manager: Regularly flagged as potential miss—docs focus on mechanics, not outcomes. Needs ROI, risk, and success-metric summaries.
- AI power user: Often “low/medium” fit—guides assume repo contributor/CI access; little practical “prompting” guidance.
- Non‑tech educator: Rarely addressed—no pedagogy framing or low-friction walkthroughs.
- Automation agent: Covered in several places but usually “medium” because content is human-facing; could use tighter, task-ready checklists.

Targeted improvements:

1. Line manager (highest gap)
    - Add 1-page executive summaries with “why it matters / risks / effort” for VISION, SURFACES, WORKFLOWS, DEPENDENCIES, CI guide, and ADR bundles (e.g., docs/CHANGELOG.md, docs/WORKFLOWS.md, docs/SURFACES.md, ADR rollups).
    - Insert “Leadership Snapshot” boxes with business value, risk mitigations, and 3–5 KPIs (throughput, handoff success, rework rate).
    - Provide a short “How to sponsor” section in docs/HOW_TO_USE/README.md and ISSUE_TEMPLATES_GUIDE.md (what they approve, what to watch).
2. AI power user
    - Create a “Power User Quickstart” in docs/HOW_TO_USE/ with concrete prompt patterns, do/don’t, and minimal Git/CI assumptions.
    - Add a “Practical prompts” appendix to QUICKSTART.md and link from README.
3. Non‑tech educator
    - Add a short “Non-technical tour” to README or docs/HOW_TO_USE/README.md with plain-language goals, examples, and a glossary pointer.
    - Provide 1–2 annotated examples of agent tasks in classroom-like scenarios (could live under docs/HOW_TO_USE/examples/ or docs/audience/ cross-link).
4. Automation agent (tighten execution fit)
    - Add an agent-facing checklist appendix to AGENTS.md or docs/HOW_TO_USE/QUICKSTART.md (exact load order, allowed write paths, required logs).
    - Link each agent-facing doc to the relevant directive codes so agents can load minimal context quickly.
