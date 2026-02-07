---
packaged: true
audiences: [automation_agent, software_engineer, process_architect]
note: Automation-focused templates and guidance.
---

# Automation Templates

Purpose: Templates for automation workflows, scripts, and CI/CD helpers.

What belongs: Automation prompt/templates, configuration examples.  
What doesn’t: Live automation configs for specific environments (store those under `ops/` or `work/` as appropriate).

## Available Templates

- **`doctrine-config-template.yaml`** — Doctrine framework configuration template
  - Configures path variables (workspace_root, doc_root, spec_root, output_root)
  - Sets repository metadata
  - Enables tool integrations (GitHub Copilot, Claude, Cursor)
  - Bootstrap Bill creates this as `.doctrine/config.yaml` during repo setup

- **`NEW_SPECIALIST.agent.md`** — Agent profile template for creating new specialists

- **`TEMPLATE-LOCAL_ENV.md`** — Local environment documentation template

- **`framework-audit-report-template.md`** — Framework Guardian audit report template

- **`framework-upgrade-plan-template.md`** — Framework upgrade plan template

- **`framework-manifest-template.yml`** — Framework version manifest
