---
name: "AUTOMATION SCRIPT"
description: "Prompt for DevOps Danny to generate an automation script based on requirements or direct prompt"
version: "1.0.0"
type: "prompt-template"
agent: "devops-danny"
category: "automation"
tags: ["automation", "scripting", "devops", "ci-cd", "tooling"]
---

# AUTOMATION SCRIPT

Prompt for DevOps Danny to generate an automation script based on requirements or direct prompt

## Instructions

Clear context. Bootstrap as DevOps Danny. When ready: 

Generate automation script.

## Inputs:

- Script Purpose (sentence): \<PURPOSE>
- Requirements Source (path or none): \<REQ_SOURCE>
- Environment Assumptions (bullets): \<ENV>
- Target Platform (local|ci|multi): \<PLATFORM>
- Languages/Tools (comma): \<TOOLS>
- Idempotency Required? (yes/no): \<IDEMPOTENT>
- Security Constraints (bullets): \<SECURITY>
- Observability (logs|metrics|none): \<OBS>
- Invocation Method (manual|scheduled|hook): \<INVOCATION>
- Output Artifacts (paths/formats): \<OUTPUTS>

## Task:

1. If \<REQ_SOURCE> provided: extract structured requirements list.
2. Design script phases (init, validate, execute, report, cleanup).
3. Generate script (prefer POSIX shell or repo language) with inline comments.
4. Provide runbook: prerequisites, invocation examples, failure modes, rollback steps.
5. Suggest CI integration snippet (GitHub Actions YAML) if \<PLATFORM> includes ci.
6. Add observability hooks per \<OBS>.
7. Ensure idempotency if \<IDEMPOTENT>=yes (state checks, guard clauses).
8. Output to `work/automation/\<slug>-script.sh` (or `.py` based on \<TOOLS>).

## Output:

- Script content
- Runbook markdown
- Optional CI snippet

## Constraints:

- No destructive operations without explicit pre-check & confirmation comment.
- Validate tool availability (fallback instructions if absent).
- Avoid hard-coded secrets; reference env vars.

Ask clarifying questions if \<PURPOSE> unclear or conflicting requirements detected.

## Workflow

1. Output to `work/automation/\<slug>-script.sh` (or `.py` based on \<TOOLS>).

## Inputs

- **PURPOSE** (required) - sentence
- **REQ_SOURCE** (required) - path or none
- **ENV** (required) - bullets
- **PLATFORM** (required) - local|ci|multi
- **TOOLS** (required) - comma
- **IDEMPOTENT** (required) - yes/no
- **SECURITY** (required) - bullets
- **OBS** (required) - logs|metrics|none
- **INVOCATION** (required) - manual|scheduled|hook
- **OUTPUTS** (required) - paths/formats

## Outputs

- Optional CI snippet

