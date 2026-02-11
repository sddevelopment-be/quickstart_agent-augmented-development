# Repository-Specific Style Guides

This directory contains style guides and naming conventions specific to this repository.

## Purpose

Document repository-specific coding standards, naming conventions, and style preferences that override or extend the generic doctrine guidelines.

## Contents

### Naming Conventions

- **python-naming-conventions.md** - Python-specific naming rules for this repository
  - Domain vs. framework class naming
  - Variable naming for domain terms
  - Glossary term usage in code
  - Module docstring standards

## Hierarchy

Style guidance follows this precedence (highest to lowest):

1. **`.doctrine-config/styleguides/`** - Repository-specific (THIS DIRECTORY)
   - Overrides and extensions for this project
   - Language-specific conventions
   - Team agreements and preferences

2. **`doctrine/docs/styleguides/`** - Generic doctrine guidelines
   - Universal DDD naming principles
   - Language-agnostic best practices
   - Cross-project standards

3. **`docs/styleguides/`** - Public-facing documentation standards
   - User documentation style
   - API documentation conventions
   - General technical writing

## When to Use Each

### Use `.doctrine-config/styleguides/` for:
- Python/Java/language-specific rules for *this repository*
- Repository-specific glossary enforcement
- Team-specific naming preferences
- Overrides to generic doctrine rules

### Use `doctrine/docs/styleguides/` for:
- Universal DDD principles (e.g., domain-driven-naming.md)
- Language-agnostic patterns
- Reusable across projects

### Use `docs/styleguides/` for:
- Public API documentation
- User-facing content
- General technical writing not specific to doctrine

## Relationship to Glossaries

Style guides in this directory should reference:
- `.contextive/contexts/*.yml` - Domain glossaries for this repository
- `doctrine/GLOSSARY.md` - Generic doctrine terminology

## Creating New Style Guides

When adding language-specific conventions:

```markdown
# {Language} Naming Conventions
**Version:** 1.0.0  
**Status:** Active  
**Purpose:** {Language}-specific naming conventions for this repository  
**Source:** Extracted from {analysis/team decision}

## Related Generic Guidelines
- [Domain-Driven Naming](../../doctrine/docs/styleguides/domain-driven-naming.md)

## Language-Specific Extensions
...
```

## Enforcement

Style guides here are enforced via:
- Code review (see `.doctrine-config/templates/pr-comment-templates.md`)
- Linting tools (configured per language)
- CI/CD checks (where applicable)
- Periodic audits by Curator Claire

## Maintenance

- **Review:** Quarterly or when language conventions evolve
- **Updates:** Any developer can propose changes via PR
- **Approval:** Requires review from relevant language specialist + Curator Claire
- **Owner:** Curator Claire, language-specific specialists (Python Pedro, etc.)

## Related Documentation

**Tactics:**
- `.doctrine-config/tactics/terminology-validation-checklist.tactic.md` - How to apply naming rules in code review

**Templates:**
- `.doctrine-config/templates/pr-comment-templates.md` - Comment templates for style violations

**Generic Guidelines:**
- `doctrine/docs/styleguides/domain-driven-naming.md` - Universal naming principles
- `doctrine/approaches/living-glossary-practice.md` - Glossary governance

**Glossaries:**
- `.contextive/contexts/orchestration.yml` - Orchestration terms
- `.contextive/contexts/task-domain.yml` - Task-specific vocabulary
- `.contextive/contexts/portfolio-domain.yml` - Portfolio management terms

---

**Last Updated:** 2026-02-10  
**Status:** Active  
**Maintainer:** Curator Claire
