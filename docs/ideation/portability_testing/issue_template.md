# ✅ 4. GitHub Issue Template: “Portability Analysis Request”

Place under:
`.github/ISSUE_TEMPLATE/portability_analysis.yml`

````yaml
name: "Portability Analysis Request"
description: Run a full cross-model portability analysis for a real agent task.
title: "[Portability] <task name>"
labels: ["portability", "analysis"]

body:

  - type: input
    id: task_id
    attributes:
      label: Task ID
      description: Unique identifier for the portability test (e.g. portability-repomap)
      placeholder: portability-repomap
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: Description of Real Task
      description: What useful task should be executed across models?
      placeholder: e.g., Update REPO_MAP.md based on new directory structure

  - type: textarea
    id: expected_outcome
    attributes:
      label: Expected Outcome
      placeholder: Describe what consistent behaviour should look like

  - type: textarea
    id: relevant_agents
    attributes:
      label: Relevant Agents
      description: Which agents are involved?
      placeholder: structural, lexical, planning, etc.

  - type: textarea
    id: directives
    attributes:
      label: Required Directives
      description: List the directives used in this task
      placeholder: minimal-diffs, preserve-voice, examples-before-abstract

  - type: textarea
    id: guidelines
    attributes:
      label: Relevant Guidelines
      placeholder: structural-baseline, lexical-pass

  - type: textarea
    id: artefacts
    attributes:
      label: Artefacts to Compare
      placeholder: docs/REPO_MAP.md, docs/LEX_REPORT.md

  - type: markdown
    attributes:
      value: |
        ## Instructions
        After submitting this issue, run:
        - The task via GitHub Copilot (verbose mode)
        - The task via Codex (CLI or JetBrains)
        - The task via ChatGPT (GPT-4.1 / 4o / 4o-mini)
        - The task via Claude Sonnet 4.5
        Save logs in:
        ```
        validation/portability_logs/<task>/<model>/<timestamp>/
        ```

  - type: textarea
    id: additional_notes
    attributes:
      label: Additional Notes
      placeholder: Anything else?
````
