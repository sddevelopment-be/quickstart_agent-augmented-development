# Repository-Specific Tactics

This directory contains tactics (operational procedures) specific to this repository's workflow and practices.

## Purpose

Document actionable, step-by-step procedures for common development activities specific to this project. Tactics are focused on "how to do X" rather than "why we do X."

## Contents

### Code Quality

- **terminology-validation-checklist.tactic.md** - Quick reference for terminology validation during code review
  - Decision trees for naming issues
  - Comment templates by severity
  - Context-specific guidance
  - Escalation procedures

## Tactic Format

All tactics follow this structure:

```markdown
# Tactic: {Tactic Name}
**Version:** {version}  
**Status:** Active | Deprecated | Experimental  
**Purpose:** {Brief description}  
**Context:** {When to apply}  
**Enforcement:** {Advisory | Required | Conditional}

## When to Apply
{Conditions and triggers}

## Steps
{Numbered procedure}

## Expected Outcomes
{Success criteria}

## Escalation
{What to do if tactic doesn't work}

## Related Resources
{Links to approaches, guidelines, templates}
```

## Hierarchy

Tactics follow this precedence:

1. **`.doctrine-config/tactics/`** - Repository-specific (THIS DIRECTORY)
   - Project-specific workflows
   - Tool-specific procedures
   - Team agreements

2. **`doctrine/tactics/`** - Generic doctrine tactics
   - Universal operational procedures
   - Reusable across projects
   - Language-agnostic methods

3. **`.github/agents/tactics/`** - Agent-specific tactics (if exists)
   - Agent collaboration protocols
   - Handoff procedures
   - Task coordination

## When to Create a Tactic

Create a repository-specific tactic when:
- Procedure is unique to this repository's structure
- Workflow involves repository-specific tools or conventions
- Team has agreed on a specific approach
- Generic doctrine tactic needs repository-specific adaptation

## Creating New Tactics

1. **Start with template:**
```markdown
# Tactic: {Name}
**Version:** 1.0.0  
**Status:** Experimental  
**Purpose:** {What problem does this solve}  
**Context:** {When to apply}

## When to Apply
{Specific conditions}

## Prerequisites
{Required knowledge, tools, access}

## Steps
1. {First step with clear action}
2. {Second step}
   - Sub-step if needed
3. {Etc.}

## Expected Outcomes
- [ ] {Observable result 1}
- [ ] {Observable result 2}

## Troubleshooting
| Problem | Solution |
|---------|----------|
| {Issue} | {Fix} |

## Related Resources
- {Links to relevant docs}
```

2. **Test with team:** Use for 2-4 weeks, gather feedback
3. **Refine:** Update based on real-world usage
4. **Promote to Active:** Once proven effective

## Relationship to Other Documentation

**Tactics answer "How?"**
- Step-by-step procedures
- Checklists and templates
- Decision trees

**Approaches answer "What/Why?"**
- `doctrine/approaches/` - Strategic patterns and practices
- Conceptual understanding

**Guidelines answer "Should/Must"**
- `doctrine/guidelines/` - Rules and constraints
- Mandatory behaviors

**Templates provide structure:**
- `.doctrine-config/templates/` - Reusable formats
- Fill-in-the-blank documents

## Maintenance

- **Review:** Quarterly or after major process changes
- **Updates:** Any developer can propose changes via PR
- **Deprecation:** Mark as "Deprecated" with superseding tactic reference
- **Owner:** Curator Claire, domain specialists

## Enforcement Levels

| Status | Meaning | Action |
|--------|---------|--------|
| **Required** | Must be followed | Blocking in code review |
| **Advisory** | Recommended | Suggestion in code review |
| **Conditional** | Required if condition met | Context-dependent |
| **Experimental** | Trial period | Optional, feedback requested |

## Success Metrics

Track effectiveness:
- **Adoption rate:** % of PRs following tactic
- **Time saved:** Reduction in repeated questions
- **Error reduction:** Fewer issues caught in review
- **Feedback:** Developer satisfaction scores

## Related Documentation

**Generic Tactics:**
- `doctrine/tactics/` - Universal procedures
- `doctrine/tactics/README.md` - Tactic catalog

**Templates:**
- `.doctrine-config/templates/pr-comment-templates.md` - Comment templates used by tactics
- `.doctrine-config/templates/` - Other reusable formats

**Approaches:**
- `doctrine/approaches/living-glossary-practice.md` - Governance for terminology
- `doctrine/approaches/language-first-architecture.md` - Philosophy behind naming tactics

**Guidelines:**
- `.doctrine-config/repository-guidelines.md` - Repository-specific rules
- `doctrine/guidelines/` - Generic constraints

---

**Last Updated:** 2026-02-10  
**Status:** Active  
**Maintainer:** Curator Claire

---

*"A tactic without a clear outcome is just busywork."*
