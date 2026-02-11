# Assessment Reports

This directory contains completed assessment reports and summaries for architectural, linguistic, and strategic evaluations.

## Purpose

Permanent storage for finalized assessment reports that inform architectural decisions and strategic planning.

## Contents

### Conceptual Alignment Assessments

- **conceptual-alignment-assessment-summary.md** - Executive summary of the 2026-02-10 linguistic health assessment, including quick start guide and priority issues.

For detailed reports, see:
- `docs/architecture/assessments/strategic-linguistic-assessment-2026-02-10.md`
- `docs/architecture/assessments/strategic-linguistic-assessment-EXECUTIVE-SUMMARY.md`

### Related Work Products

For in-progress work and analysis artifacts, see:
- `work/` - Working directory for agent outputs
- `work/reports/` - Draft reports and analysis outputs
- `work/logs/` - Agent work logs and process documentation

## Structure Guidelines

Assessment reports in this directory should:

1. **Be finalized and reviewed** - No drafts or work-in-progress
2. **Include metadata** - Date, status, authors, reviewers
3. **Link to ADRs** - Reference architectural decisions made based on findings
4. **Be discoverable** - Follow naming convention: `{topic}-assessment-{date}.md` or `{topic}-assessment-summary.md`

## Naming Convention

- **Full reports:** `{topic}-assessment-{YYYY-MM-DD}.md`
- **Summaries:** `{topic}-assessment-summary.md`
- **Executive summaries:** `{topic}-assessment-EXECUTIVE-SUMMARY.md`

## Related Documentation

- **ADRs:** `docs/architecture/adrs/` - Decisions based on assessment findings
- **Approaches:** `doctrine/approaches/` - Methods used for assessments
- **Work logs:** `work/logs/architect/` - Process documentation for assessments

## Maintenance

- **Review:** Quarterly - ensure reports remain relevant and linked to current ADRs
- **Archival:** Move superseded assessments to `docs/architecture/archive/` with clear supersession notes
- **Owner:** Architect Alphonso, Curator Claire

---

**Last Updated:** 2026-02-10  
**Status:** Active
