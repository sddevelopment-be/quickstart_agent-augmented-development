# Shorthand: new-agent

**Alias:** `/new-agent`  
**Category:** Agent Management  
**Agent:** Manager Mike  
**Complexity:** Medium  
**Version:** 1.0.0  
**Created:** 2026-02-08

---

## Purpose

Quick command to request creation of a new specialized agent (Manager Mike runs it).

---

## Usage

```
/new-agent
```

Or with parameters:
```
/new-agent NAME="Security Auditor Sally" \
  SPECIALIZATION="Security auditing and vulnerability assessment"
```

---

## Process

1. Clear context
2. Bootstrap as Manager Mike
3. Create new agent:
   - Define agent profile
   - Specify capabilities
   - Document collaboration patterns
   - Set up tooling requirements

---

## Required Inputs

- **Agent Name:** Name and persona
- **Specialization:** Core focus area and expertise

---

## Output

- Agent profile file (`doctrine/agents/{name}.agent.md`)
- Capability documentation
- Collaboration contract
- Tooling requirements

---

## Related

- **Template:** `doctrine/templates/prompts/NEW_AGENT.prompt.md`
- **Agent Profile:** `doctrine/agents/manager.agent.md`
- **Directive 005:** Agent Profiles

---

**Status:** ✅ Active  
**Maintained by:** Manager Mike  
**Last Updated:** 2026-02-08
