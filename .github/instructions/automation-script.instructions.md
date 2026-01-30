# automation-script

Prompt for DevOps Danny to generate an automation script based on requirements or direct prompt

## Capabilities

- automation
- complexity-medium
- automation
- scripting
- devops

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

## Example Prompts

- "Generate a script for PURPOSE"
- "Create CI/CD workflow for this task"
- "Help me generate an automation script based on requirements or direct prompt"

## Metadata

- **Agent**: devops-danny
- **Category**: automation
- **Complexity**: medium

