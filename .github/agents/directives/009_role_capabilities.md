# The following information is to be interpreted literally

# 009 Role Capabilities Directive

Purpose: Define allowed operational verbs per specialist to reduce overlap and prevent scope creep.

Canonical Verbs:
- Audit: Curator, Lexical, Manager
- Synthesize: Synthesizer, Architect (high-level), Researcher (source integration)
- Generate Diagrams: Diagrammer
- Refine Text: Editor, Lexical (micro style)
- Translate: Translator
- Plan: Planning, Manager (routing only), Bootstrap (mapping only)
- Automate: DevOps (build/pipeline), Backend (service scaffolds)

Conflict Prevention:
- If two agents share a verb (e.g., Architect & Synthesizer on synthesis), clarify target output scope before execution.
- Manager should never perform content synthesis; only coordinate transitions.

Escalation Rules:
- When encountering ambiguous responsibilities: reference Context Notes (002) then flag with ⚠️ if unresolved.

Extension:
- New roles must declare verbs and map them to existing categories; avoid introducing redundant synonyms.

