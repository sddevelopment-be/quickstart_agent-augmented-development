<!-- The following information is to be interpreted literally -->

# 011 Risk & Escalation Directive

**Purpose:** Clarify standardized markers and triggers for surfacing issues early.

**Core Concepts:** See [Integrity Symbol](../GLOSSARY.md#integrity-symbol) and [Escalation](../GLOSSARY.md#escalation) in the glossary.

Markers:

- ❗️ Critical integrity breach (policy, ethical, structural contradiction)
- ⚠️ Assumption-based or low confidence reasoning
- ✅ Alignment confirmed after correction or validation

Escalation Triggers:

- Unverifiable source or citation required for decision baseline
- Divergence between Operational and Strategic guidance
- Multi-agent [artifact](../GLOSSARY.md#artifact) conflict (two agents editing same file set)
- Version mismatch in governance layers (see [Version Governance](../GLOSSARY.md#version-governance) and 006)
- Failure to execute Transparency & Error Signaling [primer](../GLOSSARY.md#primer) (see DDR-001) when a risk is discovered

Procedure:

1. Flag with marker
2. Provide one-line summary of risk
3. Offer 2–3 remediation options
4. Pause action awaiting confirmation if ❗️

Timeout Handling:

- If no response after reasonable cycles (context-specific), downgrade or archive with clear note.

Primer Integration:

- Each ❗️/⚠️ event must reference the active primer in the log or artifact (e.g., “Transparency primer invoked — ❗️ blocking conflict”).
- When `/meta-mode` reflection changes direction, log the resolution path and associated integrity marker.
