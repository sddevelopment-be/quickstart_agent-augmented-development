# Core Use Cases

---
**Document Type:** Workflow Reference  
**Version:** 1.0.0  
**Last Updated:** 2026-02-14  
**Status:** Active  
**Related Documents:**
- [VISION.md](../../../VISION.md)
- [DOCTRINE_STACK.md](../../DOCTRINE_STACK.md)
- [docs/WORKFLOWS.md](../../../docs/WORKFLOWS.md)

---

## Overview

This document describes practical use cases for the Agent-Augmented Development Framework, demonstrating how the Doctrine Stack enables structured, multi-agent workflows with clear handoffs and consistent outcomes.

Each use case follows the pattern: **Scenario → Workflow → Outcome**, showing how agents collaborate under explicit directives to deliver predictable results.

---

## 1. Repository Bootstrapping

### Scenario
New project needs agent-augmented development setup.

### Workflow
1. Fork quickstart repository
2. Bootstrap Bill initializes structure and creates REPO_MAP.md
3. Customize `.doctrine-config/config.yaml` with repository paths
4. Review and adapt agent profiles in `doctrine/agents/`
5. Start submitting tasks to `work/inbox/`

### Outcome
Production-ready agent orchestration in <1 hour.

### Key Directives
- Directive 007 (Agent Declaration)
- Directive 010 (Mode Protocol)
- Directive 001 (CLI Efficiency)

---

## 2. Multi-Agent Feature Development

### Scenario
Complex feature requires architecture → implementation → testing.

### Workflow
1. **Human** submits architecture task to `work/inbox/`
2. **Orchestrator** assigns to architect agent
3. **Architect** creates design docs, diagrams, ADR
4. **Architect** hands off to backend-dev (via `result.next_agent`)
5. **Backend-dev** implements API following ATDD (Directive 016)
6. **Backend-dev** hands off to test-agent
7. **Test-agent** creates E2E tests, validates coverage

### Outcome
Feature complete with full test coverage and decision trail.

### Key Directives
- Directive 016 (ATDD Workflow)
- Directive 017 (TDD Workflow)
- Directive 018 (ADR Protocol)
- Directive 036 (Boy Scout Rule)

---

## 3. Code Quality Improvement

### Scenario
Repository has static analysis issues, needs systematic remediation.

### Workflow
1. **DevOps agent** configures coverage integration
2. **Architect** analyzes issues, categorizes, creates remediation plan
3. **Manager** coordinates execution across issue categories
4. **All agents** create work logs (Directive 014) and prompt documentation (Directive 015)

### Outcome
Issues systematically resolved with complete audit trail and documented approach.

### Key Directives
- Directive 014 (Work Log Protocol)
- Directive 015 (Prompt Documentation)
- Directive 036 (Boy Scout Rule)

### Reference Implementation
See Sprint 1 case study in `work/reports/SPRINT1_EXECUTIVE_SUMMARY.md` for detailed metrics and approach.

---

## 4. Documentation Maintenance

### Scenario
Documentation outdated after major refactoring.

### Workflow
1. **Curator** scans changed files, identifies affected docs
2. **Curator** updates READMEs, guides, API references
3. **Curator** validates internal links, cross-references
4. **Scribe** reviews for consistency, tone, clarity
5. **Scribe** generates doc status report

### Outcome
Documentation synchronized with code, zero broken links.

### Key Directives
- Directive 004 (Documentation & Context Files)
- Directive 022 (Audience-Oriented Writing)
- Directive 036 (Boy Scout Rule)

---

## 5. Specification-Driven Development

### Scenario
New feature needs persona-driven requirements capture.

### Workflow
1. **Analyst Annie** captures requirements from stakeholders
2. **Analyst Annie** creates feature spec using template (Directive 034)
3. **Analyst Annie** defines Given/When/Then acceptance criteria
4. **Backend-dev** implements feature following spec
5. **Test-agent** validates all acceptance criteria pass
6. **Curator** marks spec as "Implemented"

### Outcome
Traceability from requirements → tests → implementation.

### Key Directives
- Directive 034 (Specification Template)
- Directive 016 (ATDD Workflow)
- Directive 018 (ADR Protocol)

---

## Common Patterns

### Handoff Protocol
All agent-to-agent handoffs follow explicit patterns:
- Document next agent in task `result.next_agent` field
- Create handoff summary in work logs
- Reference prerequisite artifacts
- Specify completion criteria

### Quality Gates
Every workflow includes mandatory quality checks:
- Test-first discipline (Directives 016, 017)
- Boy Scout Rule application (Directive 036)
- Work log creation (Directive 014)
- Decision documentation via ADRs (Directive 018)

### Escalation Triggers
Agents escalate when:
- Uncertainty > 30% (per agent collaboration contract)
- Requirements ambiguous or conflicting
- Scope extends beyond specialization
- Critical issues discovered (security, data loss risk)

---

## Anti-Patterns to Avoid

❌ **Don't:** Skip test-first discipline for "quick fixes"  
✅ **Do:** Always write tests before code (Directives 016, 017, 028)

❌ **Don't:** Allow agents to make architectural decisions autonomously  
✅ **Do:** Require human approval for all strategic changes

❌ **Don't:** Bypass work log creation to save time  
✅ **Do:** Document all work per Directive 014 for audit trail

❌ **Don't:** Ignore Boy Scout Rule for unrelated issues  
✅ **Do:** Fix broken links, typos, stale dates on every task (Directive 036)

---

## Related Documents

- **[VISION.md](../../../VISION.md)** - Strategic vision and framework goals
- **[DOCTRINE_STACK.md](../../DOCTRINE_STACK.md)** - Five-layer governance model
- **[docs/WORKFLOWS.md](../../../docs/WORKFLOWS.md)** - Detailed workflow patterns
- **[work/reports/SPRINT1_EXECUTIVE_SUMMARY.md](../../../work/reports/SPRINT1_EXECUTIVE_SUMMARY.md)** - Real-world case study

---

_Extracted from VISION.md on 2026-02-14_  
_For questions: See AGENTS.md for appropriate agent assignment_
