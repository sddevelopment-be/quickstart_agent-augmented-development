# Curator Work Directory

This directory contains work products from Curator Claire, the Structural & Tonal Consistency Specialist.

---

## Current Active Audit: Doctrine Dependency Direction Violations

**Date:** 2026-02-11  
**Status:** ✅ Complete, awaiting review  
**Requester:** @stijn-dejongh

### Quick Links

| Document | Purpose | Audience |
|----------|---------|----------|
| [AUDIT_SUMMARY.txt](AUDIT_SUMMARY.txt) | Visual summary (terminal-friendly) | Quick reference |
| [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) | 2-minute overview | Stakeholders |
| [REMEDIATION_CHECKLIST.md](REMEDIATION_CHECKLIST.md) | Step-by-step fixes | Implementers |
| [INDEX.md](INDEX.md) | Complete deliverables guide | All roles |

### Full Documentation

- **Main Report:** [2026-02-11-doctrine-dependency-violations-report.md](2026-02-11-doctrine-dependency-violations-report.md)
- **Work Log:** [worklog-2026-02-11-doctrine-dependency-audit.md](worklog-2026-02-11-doctrine-dependency-audit.md)
- **Validation Script:** [validate-dependencies.sh](validate-dependencies.sh)

### The Question

> "For Claire: I noticed a doctrine artifact pointing to an ADR (which are local). That is violating our dependency direction constraints, is it not?"

### The Answer

✅ **YES** - Multiple violations confirmed:
- **114 total violations** detected
- **6 critical** (direct dependencies breaking portability)
- **16 moderate** (context references, boilerplate)
- **91 informational** (intentional template patterns)

### What's Next

1. **Review:** @stijn-dejongh reviews [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)
2. **Decide:** Approve Framework Decision proposal and prioritize phases
3. **Implement:** Follow [REMEDIATION_CHECKLIST.md](REMEDIATION_CHECKLIST.md)
4. **Validate:** Run `bash validate-dependencies.sh` after fixes

---

## Previous Work

### 2026-02-10: Boy Scout Rule Fixes
- [2026-02-10-boy-scout-fixes-worklog.md](2026-02-10-boy-scout-fixes-worklog.md)
- [2026-02-10-task-validation-fixes-report.md](2026-02-10-task-validation-fixes-report.md)
- [boy-scout-fixes-deliverables-summary.md](boy-scout-fixes-deliverables-summary.md)

### 2026-02-07: Tactics Consistency Review
- [2026-02-07-tactics-consistency-review.md](2026-02-07-tactics-consistency-review.md)

### GLOSSARY Integration Work
- [GLOSSARY-integrated-v2.md](GLOSSARY-integrated-v2.md) (Final version)
- [integration-report.md](integration-report.md)
- [validation-report.txt](validation-report.txt)
- Python tools: `integrate_glossary.py`, `parse_candidates.py`, `validate_glossary.py`

---

## Directory Structure

```
work/curator/
├── README.md                          (This file)
│
├── [Audit: Dependency Direction - 2026-02-11]
│   ├── AUDIT_SUMMARY.txt              (Visual summary)
│   ├── EXECUTIVE_SUMMARY.md           (Quick reference)
│   ├── INDEX.md                       (Complete guide)
│   ├── REMEDIATION_CHECKLIST.md       (Implementation steps)
│   ├── 2026-02-11-doctrine-dependency-violations-report.md
│   ├── worklog-2026-02-11-doctrine-dependency-audit.md
│   └── validate-dependencies.sh       (Validation tool)
│
├── [Previous Work]
│   ├── 2026-02-10-boy-scout-fixes-worklog.md
│   ├── 2026-02-10-task-validation-fixes-report.md
│   ├── 2026-02-07-tactics-consistency-review.md
│   └── [GLOSSARY integration artifacts]
│
└── [Tools & Utilities]
    ├── integrate_glossary.py
    ├── parse_candidates.py
    ├── validate_glossary.py
    └── validate-dependencies.sh
```

---

## How to Use This Directory

### If you're a **Stakeholder**:
1. Read: [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)
2. Decide: Review questions and approve/reject proposals
3. Delegate: Assign implementation to appropriate team member

### If you're an **Implementer**:
1. Read: [INDEX.md](INDEX.md) for orientation
2. Follow: [REMEDIATION_CHECKLIST.md](REMEDIATION_CHECKLIST.md) step-by-step
3. Validate: Run `bash validate-dependencies.sh` after each change
4. Reference: Full report for detailed context on specific violations

### If you're an **Auditor**:
1. Review: [worklog-2026-02-11-doctrine-dependency-audit.md](worklog-2026-02-11-doctrine-dependency-audit.md)
2. Verify: Primer compliance section
3. Check: Trade-offs and decisions sections

---

## Curator Role

**Agent:** Curator Claire  
**Specialization:** Structural & Tonal Consistency  
**Primary Focus:** Alignment audits (voice, tone, structure, metadata, style)  
**Success Criteria:** Consistent, linkable artifacts with minimized divergence

**Profile:** See [doctrine/agents/curator.agent.md](../../doctrine/agents/curator.agent.md)

---

## Contact

For questions about this audit, reference the deliverables above or contact @stijn-dejongh

---

*Last Updated: 2026-02-11*
