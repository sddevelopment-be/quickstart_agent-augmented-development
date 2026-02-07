# Step 7: Log Work

## When to Use

After completing any task (successful or failed).

## Log Location

Create execution logs in:

```
`${WORKSPACE_ROOT}/reports/logs/<your-agent-name>/YYYY-MM-DDTHHMM-<description>.md
```

## Log Contents

Document:

- Task processing decisions
- Work performed
- Reasoning and trade-offs
- Any issues encountered
- Directive and approach references used

## Example

```markdown
# Work Log: Refactor Directive 019

**Agent:** curator
**Task ID:** 2025-11-26T0614-curator-refactor-directive-019-minimal
**Date:** 2025-11-26T06:30:00Z
**Status:** completed

## Context

Refactored verbose Directive 019 into minimal directive with approach references.

## Approach

Extracted step-by-step content into .github/agents/approaches/file_based_collaboration/
with one file per logical step, allowing agents to load only task-relevant information.

## Guidelines & Directives Used

- Directive 012: Common Operating Procedures
- Directive 014: Work Log Creation
- Approach: Locality of Change

## Execution Steps

1. Created approach directory structure
2. Extracted 7 logical steps into separate files
3. Created README.md overview with step index
4. Rewrote directive as minimal reference
5. Validated structure with existing approaches

## Outcome

Token efficiency improved - agents now load ~200 tokens vs ~2000 tokens.
Maintains full guidance while respecting context window constraints.
```

## Best Practices

- Be concise but complete
- Include relevant metrics (token counts, processing time)
- Reference directives and approaches used
- Document any deviations from standard process

## Related

See Directive 014 (Work Log Creation) for complete standards.
