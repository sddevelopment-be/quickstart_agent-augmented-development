# Maintenance Checklist Templates

**Version:** 1.0.0  
**Last Updated:** 2025-11-27  
**Maintained by:** Curator & Build Automation agents

---

## Purpose

This directory contains reusable checklist templates for standardizing routine maintenance tasks, tool adoption processes, and derivative repository setup. These templates ensure consistent execution of critical maintenance activities and support the long-term health of agent-augmented development workflows.

---

## Available Templates

### 1. Quarterly Tool Review (`quarterly-tool-review.md`)

**Purpose:** Systematic review of tooling infrastructure each quarter.

**When to use:**
- End of each quarter (Q1, Q2, Q3, Q4)
- After major framework updates
- When performance issues are suspected
- Before planning major upgrades

**Key sections:**
- Version update checks for CLI tools and framework components
- Security audit (tool sources, vulnerabilities, access control)
- Performance validation (tool speed, agent execution, CI/CD)
- Documentation updates (user guides, agent docs, templates)
- Roadmap planning (priorities, deprecations, features)
- Quality metrics and traceability
- Derivative repository assessment
- Action items and review completion

**Output:** Completed checklist archived to `work/reports/maintenance/YYYY-QX-tool-review.md`

---

### 2. Tool Adoption Checklist (`tool-adoption-checklist.md`)

**Purpose:** Evaluate and integrate new CLI tools or agent capabilities.

**When to use:**
- Proposing a new development tool
- Adding capability to agent profiles
- Introducing new dependency to framework
- Evaluating community-suggested tools

**Key sections:**
- Evaluation criteria (business value, technical assessment)
- Security review (source verification, supply chain, risk)
- Testing requirements (installation, functionality, edge cases)
- Documentation needs (user guides, agent docs, templates)
- Integration validation (repo structure, CI/CD, orchestration)
- Rollout steps (preparation, implementation, monitoring)
- Training and communication
- Success criteria
- Decision rationale
- Post-adoption review

**Output:** Decision record and archived checklist for future reference

---

### 3. Derivative Repository Setup (`derivative-repo-setup.md`)

**Purpose:** Guide setup of new projects using this framework.

**When to use:**
- Creating new project from this template
- Adopting framework in existing project
- Forking for specialized use case
- Setting up team or organizational derivative

**Key sections:**
- Customization assessment (project context, framework fit)
- Platform verification (repository, framework install, tools)
- Testing validation (setup, agents, CI/CD)
- Documentation updates (project-specific, agent docs, templates)
- Customization best practices (local overrides, version control)
- Team onboarding (knowledge transfer, access)
- Success criteria (functional, quality)
- Post-setup tasks (next steps, maintenance plan)
- Rollback plan
- Setup completion and sign-off
- Lessons learned

**Output:** Completed setup record archived to `work/reports/setup/YYYY-MM-DD-derivative-setup.md`

---

## Usage Instructions

### How to Use a Checklist Template

1. **Copy the template**
   ```bash
   cp ${DOC_ROOT}/templates/checklists/<template-name>.md work/reports/<category>/YYYY-MM-DD-<description>.md
   ```

2. **Fill in header information**
   - Replace all `{{placeholders}}` with actual values
   - Update date, version, reviewer/owner information
   - Set initial status

3. **Work through sections systematically**
   - Check off items as completed: `- [x] Item description`
   - Fill in requested information in blanks: `_____`
   - Add notes and details as needed
   - Mark items N/A if not applicable with justification

4. **Document findings**
   - Record all issues in action items table
   - Capture metrics and measurements
   - Note deviations from expected outcomes
   - Link to related artifacts

5. **Complete and archive**
   - Ensure all sections addressed
   - Get required sign-offs
   - Archive to designated location
   - Update related documentation

### Customization Guidelines

These templates are designed to be customized for your project's needs:

- **Add sections:** If your project has specific requirements not covered
- **Remove sections:** If certain sections don't apply (document why)
- **Adjust frequency:** Modify review schedules based on project cadence
- **Extend metrics:** Add project-specific success criteria
- **Localize:** Adapt terminology and references to your context

**Important:** Keep the core structure and intent of each template to maintain consistency across projects using this framework.

---

## Integration with Orchestration System

These checklists integrate with the file-based orchestration system:

### Creating Tasks from Checklists

Convert checklist items into agent tasks:

1. Identify items suitable for agent execution
2. Create task descriptor in `work/inbox/`
3. Reference checklist as context
4. Track completion in checklist

**Example task reference:**
```yaml
context:
  source_checklist: work/reports/maintenance/2025-Q4-tool-review.md
  checklist_section: "4. Documentation Updates"
  parent_task: quarterly-review-q4-2025
```

### Agent Coordination

Agents can:
- **Read** checklists to understand maintenance status
- **Update** checklists with completion status
- **Generate** reports referenced by checklists
- **Create** follow-up tasks based on findings

Checklists remain human-owned but agent-supported artifacts.

---

## Maintenance Workflow

### Regular Reviews

| Frequency | Checklist | Responsible | Duration |
|-----------|-----------|-------------|----------|
| Quarterly | Tool Review | Build Automation / Curator | 2-4 hours |
| As-needed | Tool Adoption | Build Automation / Team | 1-8 hours |
| Per-project | Derivative Setup | Architect / Curator | 4-8 hours |

### Continuous Improvement

After completing each checklist:

1. **Gather feedback:** What worked? What didn't?
2. **Document issues:** Track problems encountered
3. **Propose improvements:** Update templates based on learnings
4. **Version updates:** Increment template versions when significantly changed
5. **Share learnings:** Inform derivative projects of improvements

---

## Examples

### Example: Completed Quarterly Review

```markdown
# Quarterly Tool Review Checklist

**Version:** 1.0.0
**Last Updated:** 2025-09-30
**Reviewer:** Build Automation Agent
**Quarter:** Q3 2025

[... completed checklist with all items checked and documented ...]

**Review completed by:** build-automation
**Date:** 2025-09-30
**Sign-off:** @team-lead
```

Archived to: `work/reports/maintenance/2025-Q3-tool-review.md`

### Example: Tool Adoption Decision

```markdown
# Tool Adoption Checklist

**Tool Name:** uv (Python package manager)
**Proposed By:** @developer
**Date:** 2025-11-15
**Status:** Approved

[... evaluation details ...]

**Decision:** ✅ Approved with conditions
- Condition 1: Pilot in one project first
- Condition 2: Document migration from pip
- Condition 3: Review after 1 month

**Decision Date:** 2025-11-20
**Decided By:** Tech Lead + Build Automation
```

Archived with decision rationale and action items.

---

## Related Documentation

### Framework Context
- **Operational Guidelines:** `.github/agents/guidelines/operational_guidelines.md`
- **Work Directory Structure:** `work/README.md`
- **Agent Profiles:** `.github/agents/profiles/`

### Specific Guides
- **Tooling Setup:** `docs/HOW_TO_USE/copilot-tooling-setup.md`
- **Creating Agents:** `docs/HOW_TO_USE/creating-agents.md`
- **Orchestration:** `docs/HOW_TO_USE/multi-agent-orchestration.md`

### Directives
- **001:** CLI & Shell Tooling - Tool selection criteria
- **004:** Documentation & Context Files - Template usage
- **012:** Common Operating Procedures - Quality standards
- **014:** Work Log Creation - Documentation requirements

---

## Feedback and Improvements

These templates are living documents. Please contribute improvements:

1. **Report issues:** Unclear sections, missing items, errors
2. **Suggest additions:** New checklist types, additional sections
3. **Share successes:** Effective practices from your usage
4. **Document patterns:** Common customizations worth standardizing

**Feedback channels:**
- GitHub issues on this repository
- Team retrospectives
- Direct suggestions to curator agent
- Pull requests with improvements

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-11-27 | Initial creation of checklist templates | Curator Claire |

---

**Questions?** Refer to `docs/HOW_TO_USE/` guides or create an issue for support.

**Template Source:** Derived from existing repository maintenance practices and community feedback.
