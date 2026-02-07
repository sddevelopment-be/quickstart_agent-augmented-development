# Agent Schema Documentation

**Purpose:** Define and document input/output schemas for agent profiles in the multi-format export pipeline.

**Audience:** Contributors, Agent Authors, Developers

---

## Quick Start

### 1. Creating a New Agent Schema

1. Read [`schema-conventions.md`](./schema-conventions.md) (10-15 minutes)
2. Use [`agent-schema-template.json`](./agent-schema-template.json) as starting point
3. Follow [`migration-checklist.md`](./migration-checklist.md) for step-by-step guidance

**Time Estimate:** 60-120 minutes for full schema migration

---

## Documents in This Directory

### [`schema-conventions.md`](./schema-conventions.md) ⭐ Start Here

**What:** Comprehensive conventions for defining agent schemas  
**When:** Read first before creating any schemas  
**Key Sections:**

- 5 key decisions (location, extraction, format, validation, compatibility)
- Decision tree: Frontmatter vs separate files
- Schema structure templates
- FAQ with 10 common questions
- Examples (simple, complex, shared types)

**Size:** 990 lines (~25KB)  
**Read Time:** 20-30 minutes

---

### [`agent-schema-template.json`](./agent-schema-template.json)

**What:** Ready-to-use JSON Schema template  
**When:** Use as starting point for new schemas  
**Features:**

- Reusable type definitions (Task, Artifact, Status, Mode, Metrics)
- Input/output schema templates
- Inline documentation
- 4 complete usage examples
- Customization checklist

**Size:** 425 lines (~14KB)  
**Usage:**

```bash
# Copy template to create new schema
cp docs/schemas/agent-schema-template.json docs/schemas/my-agent.input.schema.json
```

---

### [`migration-checklist.md`](./migration-checklist.md)

**What:** Step-by-step guide for adding schemas to existing agents  
**When:** Migrating existing agent profiles  
**Structure:**

- Pre-migration (4 steps, ~40 min): Understand conventions, analyze agent
- Migration (6 steps, ~60 min): Create schemas, validate
- Post-migration (2 steps, ~10 min): Commit, review
- Common pitfalls with solutions

**Size:** 700 lines (~16KB)  
**Time Estimate:** 60-120 minutes per agent

---

## Schema Conventions Summary

### Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Location** | Mixed (frontmatter + files) | Simple in frontmatter, complex in separate files |
| **Extraction** | Semi-automated | Human authors, parser validates |
| **Format** | JSON Schema Draft 7 | Industry standard, mature ecosystem |
| **Validation** | Layered (build + runtime) | Fail-fast at CI, safety net at runtime |
| **Compatibility** | Progressive enhancement | Optional → encouraged → required |

### Frontmatter vs Separate File

**Use Frontmatter when:**

- Schema has ≤5 properties at root level
- No deeply nested structures (≤2 levels)
- Properties are simple types
- Schema is stable and unlikely to be reused

**Use Separate File when:**

- Schema has >5 properties at root level
- Complex nested structures (>2 levels deep)
- Contains reusable type definitions
- Shared across multiple agents

---

## Example Schemas

### Simple Schema (Frontmatter)

```yaml
---
name: formatter-felix
inputs:
  type: object
  properties:
    file_paths:
      type: array
      items:
        type: string
    style_guide:
      type: string
      enum: ["google", "airbnb", "standard"]
      default: "standard"
  required: [file_paths]
---
```

### Complex Schema (Separate File)

```yaml
---
name: reviewer-rachel
inputs: "file://schemas/reviewer-rachel.input.schema.json"
outputs: "file://schemas/reviewer-rachel.output.schema.json"
---
```

See full examples in [`schema-conventions.md`](./schema-conventions.md#examples).

---

## Validation Commands

```bash
# Validate single agent schema
npm run validate:schema -- agents/my-agent.agent.md

# Validate all agent schemas
npm run validate:schemas

# Test schema with sample data
npm run schema:test -- docs/schemas/my-agent.input.schema.json tests/fixtures/my-input.json
```

---

## Pattern Coverage

Conventions cover **~85%** of common agent patterns:

✅ Task definitions (task_id, description, priority)  
✅ Mode selection (enum)  
✅ Context files (array of paths)  
✅ Dependencies (array of task IDs)  
✅ Standard outputs (task_id, status, artifacts)  
✅ Artifact structure (path, type, format, hash, size)  
✅ Metrics (duration, coverage, quality)  
✅ Warnings/errors (array of objects)  
✅ Enum-driven parameters  
✅ String/numeric constraints  
✅ Nested objects with $ref  
✅ Reusable type definitions

**Uncovered patterns** (~15%): Documented in FAQ with guidance.

---

## Common Pitfalls

1. **Missing Descriptions:** Every property should have a description
2. **Inconsistent Naming:** Always use `snake_case`
3. **Over-Specification:** Mark only essentials as required
4. **Missing Constraints:** Define enums, patterns, ranges when known
5. **Deep Nesting Without $ref:** Extract nested types into definitions
6. **Schema-Narrative Drift:** Update both schema and narrative together

See [`migration-checklist.md`](./migration-checklist.md#common-pitfalls-and-solutions) for solutions.

---

## Resources

### Internal Documentation

- **IR Structure:** `docs/technical/ir-structure.md`
- **Export Pipeline Design:** `work/analysis/tech-design-export-pipeline.md`
- **Multi-Format Strategy:** `work/analysis/ADR-013-multi-format-distribution.md`
- **Work Log:** `work/reports/logs/architect/2026-01-29-task-1.3-schema-conventions.md`

### External References

- **JSON Schema Draft 7:** <https://json-schema.org/draft-07/schema>
- **JSON Schema Understanding:** <https://json-schema.org/understanding-json-schema/>
- **JSON Schema Best Practices:** <https://json-schema.org/understanding-json-schema/reference/generic.html>

---

## FAQ Quick Reference

**Q: What if my agent has no inputs?**  
A: Define minimal schema or omit it. Document why no inputs needed.

**Q: Can I use JSON Schema Draft 2020-12?**  
A: No, use Draft 7 for consistency and tooling support.

**Q: How do I version schemas?**  
A: Include version in `$id` field. Maintain old versions for breaking changes.

**Q: Can agents share schemas?**  
A: Yes, store shared schemas in `docs/schemas/common/`.

**Q: What if narrative conflicts with schema?**  
A: Schema is authoritative. Update narrative to match or vice versa.

See full FAQ in [`schema-conventions.md`](./schema-conventions.md#faq).

---

## Status and Roadmap

**Current Status:** ✅ Conventions defined, ready for adoption

**Adoption Phases:**

1. **Phase 1 (Current):** Schemas optional, encouraged for new agents
2. **Phase 2 (3 months):** Schemas expected, migration guide available
3. **Phase 3 (6+ months):** Schemas required, CI enforces presence

**Next Steps:**

- Task 1.4: Create 5 schemas using conventions (Backend Benny)
- Task 2.4: Complete 12 schemas for remaining agents
- Refine conventions based on practical usage
- Implement automated schema suggestions

---

## Getting Help

**Questions about conventions?**  
→ See FAQ in [`schema-conventions.md`](./schema-conventions.md#faq)

**Stuck during migration?**  
→ Check [`migration-checklist.md`](./migration-checklist.md) common pitfalls section

**Need schema review?**  
→ Tag @architect-alphonso or @backend-benny in PR

**Found a gap in conventions?**  
→ Document in issue, propose update to conventions

---

**Document Status:** ✅ Complete  
**Version:** 1.0.0  
**Date:** 2026-01-29  
**Author:** Architect Alphonso  
**Related Task:** mfd-task-1.3-schema-conventions
