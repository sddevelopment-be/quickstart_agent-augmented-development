# Repository-Specific Templates

This directory contains reusable document templates specific to this repository's workflow.

## Purpose

Provide fill-in-the-blank templates for common development artifacts, ensuring consistency and completeness across the team.

## Contents

### Code Review

- **pr-comment-templates.md** - Standardized comment templates for code review
  - Terminology issues
  - Documentation issues
  - Generic naming anti-patterns
  - Domain concept questions
  - Style and quality feedback
  - Escalation comments

## Template Categories

### 1. Code Review Templates
- PR comment templates (terminology, style, quality)
- Review checklists
- Approval criteria

### 2. Documentation Templates (future)
- ADR template overrides (if repository-specific)
- Module docstring examples
- README structures

### 3. Issue Templates (future)
- Bug report formats
- Feature request structures
- Terminology issue reports

### 4. Agent Task Templates (future)
- Task descriptor formats
- Handoff templates
- Result documentation

## Using Templates

### In Code Review

Reference templates from PR comments:

```markdown
See template: .doctrine-config/templates/pr-comment-templates.md - "Advisory Comment"
```

### In Documentation

Copy template structure:

```markdown
# Based on template: .doctrine-config/templates/{template-name}.md
```

### In Automation

Templates can be used by:
- GitHub Actions (PR comment automation)
- Pre-commit hooks (template validation)
- IDE snippets (code generation)

## Template Format

All templates should include:

```markdown
# {Template Name}
**Version:** {version}  
**Purpose:** {What this template is for}  
**Audience:** {Who should use this}

## When to Use
{Conditions for using this template}

## Template Structure
{The actual template content}

## Example Usage
{Filled-in example}

## Customization
{Which parts to adapt, which to keep}

## Related Resources
{Links to tactics, guidelines, examples}
```

## Hierarchy

Templates follow this precedence:

1. **`.doctrine-config/templates/`** - Repository-specific (THIS DIRECTORY)
   - Project-specific formats
   - Team conventions
   - Tool integrations

2. **`doctrine/templates/`** - Generic doctrine templates
   - Universal formats
   - Reusable across projects

3. **`docs/templates/`** - Public documentation templates
   - User-facing formats
   - API documentation structures

## Creating New Templates

### 1. Identify Need
- Repeated formatting work
- Inconsistent document structures
- New process requiring standardization

### 2. Draft Template
```markdown
# Template: {Name}
**Version:** 0.1.0 (DRAFT)  
**Purpose:** {Brief description}  
**Status:** Draft

## Structure
{Template content with placeholders}

## Instructions
{How to fill in placeholders}

## Example
{Filled-in example}
```

### 3. Test with Team
- Use for 2-4 weeks
- Gather feedback
- Identify missing sections

### 4. Refine and Publish
- Update based on feedback
- Promote version to 1.0.0
- Change status to Active

### 5. Maintain
- Update when process changes
- Deprecate if superseded
- Archive outdated templates

## Customization Guidelines

### Always Customize
- {Placeholders in curly braces}
- Dates and timestamps
- Names and identifiers
- Context-specific details

### Usually Keep
- Section headings
- Required fields
- Metadata structure
- Links to guidelines

### Sometimes Adapt
- Optional sections
- Example content
- Formatting choices
- Ordering of sections

## Template Validation

Templates should be:
- **Complete:** Cover all required information
- **Clear:** Unambiguous instructions
- **Consistent:** Match project conventions
- **Tested:** Used in real scenarios
- **Maintained:** Updated when processes change

## Automation Opportunities

Templates in this directory can be:
- **Integrated with GitHub:** Issue/PR templates in `.github/`
- **Used in CI/CD:** Validate document structure
- **IDE snippets:** Code completion for common patterns
- **Git hooks:** Pre-commit template validation

## Related Documentation

**Tactics (How to use templates):**
- `.doctrine-config/tactics/terminology-validation-checklist.tactic.md` - References PR comment templates
- `doctrine/tactics/` - Generic procedures using templates

**Styleguides (What content to put in templates):**
- `.doctrine-config/styleguides/python-naming-conventions.md` - Naming patterns
- `doctrine/docs/styleguides/domain-driven-naming.md` - Generic naming rules

**Examples (Filled templates):**
- `docs/architecture/adrs/` - Completed ADRs following templates
- `work/logs/` - Work logs following logging templates
- `.contextive/contexts/` - Glossaries following YAML template

**Generic Templates:**
- `doctrine/templates/` - Universal formats
- `docs/templates/` - Public documentation templates

## Maintenance

- **Review:** Quarterly or after major process changes
- **Updates:** Any developer can propose changes via PR
- **Versioning:** Increment version on significant changes
- **Deprecation:** Mark as "Deprecated" with superseding template reference
- **Owner:** Curator Claire, process owners

## Success Metrics

Track template effectiveness:
- **Adoption rate:** % of artifacts using templates
- **Completeness:** Reduction in missing sections
- **Consistency:** Similarity scores across documents
- **Time saved:** Reduction in formatting time
- **Satisfaction:** Developer feedback scores

---

**Last Updated:** 2026-02-10  
**Status:** Active  
**Maintainer:** Curator Claire

---

*"Good templates are invisible - you only notice them when they're missing."*
