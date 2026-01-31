# Task: Documentation Content Migration Planning (Batch 2 Prep)

**Task ID**: `2026-01-31T1030-docsite-content-planning`  
**Assignee**: Writer-Editor Agent (Writer Wendy)  
**Priority**: MEDIUM (Batch 2)  
**Estimated Effort**: 4-6 hours planning now; 20-25 hours Batch 2 execution  
**Depends On**: Architect Alphonso (docs-site foundation - ✅ COMPLETE)  
**Related**: `work/planning/docsite-batch-1-implementation-plan.md`, `work/planning/documentation-website-roadmap.md`

---

## Objective

Plan the migration of 19 existing HOW_TO_USE guides to the new documentation site, and outline the comprehensive Getting Started guide for Batch 2 execution.

---

## Context

The documentation site foundation is complete:
- ✅ Hugo site operational at `docs-site/`
- ✅ Section structure defined (Getting Started, Guides, Architecture, Reference, Contributing)
- ✅ Placeholder pages created
- ✅ Build and deployment process being automated (Build Buddy task)

**Your task**: Plan the content migration for Batch 2 (3 weeks, starts after Batch 1 deployment).

---

## Deliverables (Planning Phase)

### 1. Content Audit

**File**: `work/analysis/docsite-content-audit.md`

**Content**:
- Review all 19 files in `docs/HOW_TO_USE/`
- Assess content quality, clarity, completeness (rate 1-5 scale)
- Identify gaps and improvement opportunities
- Rank migration priority by user value (high/medium/low)
- Note estimated effort per guide (hours)

**Audit Template per Guide**:
```markdown
### [Guide Name]
- **File**: `docs/HOW_TO_USE/[filename].md`
- **Quality**: [1-5] (clarity, completeness, accuracy)
- **Priority**: [High/Medium/Low]
- **Improvements Needed**: [List gaps, outdated info, missing examples]
- **Effort**: [Hours to migrate + enhance]
```

---

### 2. Migration Strategy

**File**: `work/planning/docsite-content-migration-strategy.md`

**Content**:
- **Guide-by-guide plan**: Migration sequence (prioritized by value)
- **Front matter standardization**: Template for all guides
- **Internal link updates**: Strategy for updating cross-references
- **Content enhancements**: Where to add examples, diagrams, callouts
- **Quality checklist**: Validation criteria for migrated content
- **Timeline**: Week-by-week breakdown for Batch 2

**Example Front Matter Template**:
```yaml
---
title: "Guide Title"
description: "Brief description for SEO"
weight: 10
tags: ["tag1", "tag2"]
date: 2026-01-31
---
```

---

### 3. Getting Started Guide Outline

**File**: `work/planning/getting-started-guide-outline.md`

**Content**:
- **User journey mapping**: New user → first task → next steps
- **Content structure**: 
  - Quickstart (5 min): Absolute minimum
  - Installation: Detailed setup instructions
  - Core Concepts: Framework fundamentals
  - Tutorials: 5-6 hands-on tutorials
- **Tutorial topics**: First task, multi-agent, custom agent, CI/CD, advanced
- **Callout strategy**: Tips, warnings, examples placement
- **Code example requirements**: What examples to include

---

## Success Criteria (Planning Phase)

- ✅ Content audit identifies quality/gaps for all 19 guides
- ✅ Migration plan prioritizes guides by user value
- ✅ Front matter template defined and approved
- ✅ Getting Started guide structure approved by stakeholders
- ✅ Timeline confirmed for Batch 2 execution (3 weeks)

---

## Batch 2 Execution Tasks (Future)

After planning approved, Batch 2 work includes:

1. **Week 1-2**: Migrate 19 guides
   - Add front matter
   - Update internal links
   - Enhance with examples/diagrams
   - Test code samples

2. **Week 2**: Write Getting Started guide
   - Quickstart section
   - Installation instructions
   - Core concepts explanation

3. **Week 2-3**: Create tutorial series
   - 5-6 hands-on tutorials
   - Step-by-step instructions
   - Validate with test users

4. **Week 3**: Polish and configure search
   - Hugo search configuration
   - Test search relevance
   - Refine navigation menus

5. **Week 3**: Establish content style guide
   - Writing standards
   - Example conventions
   - Review checklist

---

## Reference Materials

- **Current guides**: `docs/HOW_TO_USE/*.md` (19 files)
- **Target location**: `docs-site/content/guides/`
- **Roadmap**: `work/planning/documentation-website-roadmap.md` (Batch 2 details)
- **Site architecture**: `docs-site/ARCHITECTURE.md`

**19 Guides to Migrate**:
1. QUICKSTART.md
2. ci-orchestration.md
3. ci-validation-guide.md
4. claude-deployment-guide.md
5. context-optimization-guide.md
6. copilot-tooling-setup.md
7. creating-agents.md
8. framework_install.md
9. github_workflows.md
10. ISSUE_TEMPLATES_GUIDE.md
11. mcp-server-setup.md
12. multi-agent-orchestration.md
13. mutation_testing.md
14. prompt-optimization-quick-reference.md
15. prompt-validation-guide.md
16. python-setup.md
17. release_and_upgrade.md
18. testing-orchestration.md
19. README.md (HOW_TO_USE index)

---

## Questions or Issues?

**Review**:
- `docs-site/ARCHITECTURE.md`: Content organization strategy
- `work/planning/documentation-website-roadmap.md`: Batch 2 scope
- `work/planning/docsite-batch-1-implementation-plan.md`: Overall context

**Ask**:
- Architect Alphonso for IA questions
- Users/stakeholders for content priorities

---

**Created**: 2026-01-31  
**Status**: 🟡 Ready to Start (Planning Phase)  
**Next Steps**: Content audit → Migration strategy → Getting Started outline
