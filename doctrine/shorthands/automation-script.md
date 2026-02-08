# Shorthand: automation-script

**Alias:** `/automation-script`  
**Category:** Automation  
**Agent:** DevOps Danny (Build Automation)  
**Complexity:** Medium  
**Version:** 1.0.0  
**Created:** 2026-02-08

---

## Purpose

Quick command to bootstrap DevOps Danny and generate an automation script based on requirements or direct prompt.

---

## Usage

```
/automation-script
```

Or with parameters:
```
/automation-script PURPOSE="Validate all markdown links" \
  LANGUAGE="bash" \
  INPUTS="Directory path"
```

---

## Process

1. Clear context
2. Bootstrap as DevOps Danny
3. Generate automation script with:
   - Proper error handling
   - Clear output/logging
   - Idempotency where applicable
   - Documentation/usage

---

## Required Inputs

- **Script Purpose:** One sentence description
- **Target Environment:** bash, python, node, etc.
- **Required Inputs:** Parameters, environment variables, files

---

## Optional Inputs

- **Output Format:** JSON, text, exit codes
- **Error Handling:** Fail fast, retry, graceful degradation
- **Dependencies:** Required tools, packages
- **Constraints:** Performance, portability

---

## Output

- **Script file:** Executable with proper shebang
- **Usage documentation:** Command-line interface
- **Error handling:** Clear error messages
- **Exit codes:** Standard conventions (0=success, 1=error)

---

## Example

```
/automation-script

Script Purpose: Validate all internal markdown links in docs/
Language: bash
Inputs: Directory path (default: docs/)
Output: List of broken links with file:line references
Dependencies: grep, find
```

**Output:** `tools/scripts/validate-markdown-links.sh`

---

## Related

- **Template:** `doctrine/templates/prompts/AUTOMATION_SCRIPT.prompt.md`
- **Agent Profile:** `doctrine/agents/build-automation.agent.md`

---

**Status:** ✅ Active  
**Maintained by:** DevOps Danny  
**Last Updated:** 2026-02-08
