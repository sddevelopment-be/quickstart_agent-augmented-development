<!-- The following information is to be interpreted literally -->
# 006 Version Governance Directive

**Purpose:** Track and manage versions of context layers and governance documents to ensure agents operate against stable, known versions.

**Core Concept:** See [Version Governance](../GLOSSARY.md#version-governance) and [Context Layer](../GLOSSARY.md#context-layer) in the glossary.

| Layer                 | Current Version | Responsibility  | Filename                                      |
|-----------------------|-----------------|-----------------|-----------------------------------------------|
| Bootstrap Template    | v1.0.0          | team leadership | `agents/guidelines/bootstrap.md`              |
| Rehydrate Context     | v1.0.0          | team leadership | `agents/guidelines/rehydrate.md`              |
| Strategic Context     | v1.0.0          | team leadership | `agents/guidelines/general_guidelines.md`     |
| Operational Reference | v1.2.0          | team leadership | `agents/guidelines/operational_guidelines.md` |
| Command Aliases       | v1.1.0          | team leadership | `agents/aliases.md`                           |
| Strategic Context     | v1.0.0          | team leadership | `docs/vision.md`                              |
| Specific Guidelines   | v1.0.0          | team leadership | `docs/specific_guidelines.md`                 |

Rules:

- Do NOT auto‑modify or overwrite versioned governance files.
- Changes must be explicit and confirmed.
- On detected version delta: pause, request confirmation, then re-run `/validate-alignment`.

**Related Terms:** [Alignment](../GLOSSARY.md#alignment), [Validation](../GLOSSARY.md#validation), [Bootstrap](../GLOSSARY.md#bootstrap), [Rehydration](../GLOSSARY.md#rehydration)

