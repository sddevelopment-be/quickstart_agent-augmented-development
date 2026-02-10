# Glossary Candidates Directory

## Purpose
Storage for candidate glossary entries extracted from various sources (directives, approaches, tactics, code) before elevation to canonical GLOSSARY.md.

## Structure
- `batch1-directives-candidates.yaml` - Terms extracted from doctrine/directives/ (001-038)
- `batch2-approaches-candidates.yaml` - Terms from doctrine/approaches/ (future)
- `batch3-tactics-candidates.yaml` - Terms from doctrine/tactics/ (future)

## Workflow
1. **Extract** - Agent performs terminology extraction per Living Glossary Practice
2. **Review** - Curator Claire validates consistency with existing glossary
3. **Approve** - Domain experts confirm definitions and usage
4. **Elevate** - High-confidence candidates added to GLOSSARY.md with canonical status

## Status
- **candidate** - Proposed, under review
- **approved** - Validated, ready for elevation
- **rejected** - Not domain-specific or redundant
- **deferred** - Needs further clarification

## Related Documentation
- `doctrine/approaches/living-glossary-practice.md` - Glossary maintenance approach
- `doctrine/tactics/terminology-extraction-mapping.tactic.md` - Extraction methodology
- `doctrine/GLOSSARY.md` - Canonical glossary
