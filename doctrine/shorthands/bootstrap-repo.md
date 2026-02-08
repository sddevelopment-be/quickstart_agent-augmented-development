# Shorthand: bootstrap-repo

**Alias:** `/bootstrap-repo`  
**Category:** Repository Setup  
**Agent:** Bootstrap Bill  
**Complexity:** Medium  
**Version:** 1.0.0  
**Created:** 2026-02-08

---

## Purpose

Quick command to bootstrap Bootstrap Bill and perform repository bootstrap & scaffolding.

---

## Usage

```
/bootstrap-repo
```

Or with parameters:
```
/bootstrap-repo VISION="Multi-agent orchestration framework"
```

---

## Process

1. Clear context
2. Bootstrap as Bootstrap Bill
3. Perform repository bootstrap:
   - Create directory structure
   - Generate configuration files
   - Set up initial documentation
   - Configure tooling

---

## Required Inputs

- **Vision Summary:** One paragraph describing repository purpose

---

## Output

- Directory structure (`work/`, `docs/`, `specifications/`, etc.)
- Configuration files (`.doctrine-config/config.yaml`)
- Initial README and documentation
- Tooling setup (linters, formatters, validators)

---

## Related

- **Tactic:** `doctrine/tactics/repository-initialization.tactic.md`
- **Template:** `doctrine/templates/prompts/BOOTSTRAP_REPO.prompt.md`
- **Agent Profile:** `doctrine/agents/bootstrap-bill.agent.md`
- **Directive 003:** Repository Quick Reference
- **ADR-004:** Work Directory Structure

---

**Status:** ✅ Active  
**Maintained by:** Bootstrap Bill  
**Last Updated:** 2026-02-08
