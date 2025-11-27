<!-- The following information is to be interpreted literally -->
# 014 Work Log Creation Directive

**Purpose:** Define standards for creating work logs that document agent execution for agentic framework tuning and continuous improvement.

**Core Concept:** See [Work Log](../GLOSSARY.md#work-log) in the glossary for foundational definition.

## 1. When to Create a Work Log

Agents MUST create a work log when:
- Completing a task from the file-based [orchestration](../GLOSSARY.md#orchestration) system (`work/collaboration/assigned/`)
- Performing multi-step coordination with other agents
- Encountering novel or ambiguous situations requiring creative problem-solving
- Implementing new patterns or approaches not previously documented
- Requested explicitly by human stakeholders

Agents MAY create work logs for:
- Complex refactoring or structural changes
- Tasks requiring significant research or exploration
- Experimental approaches that may inform future agent design

## 2. Work Log Location

All work logs MUST be stored in:
```
work/reports/logs/<agent-name>/YYYY-MM-DDTHHMM-<description>.md
```

**Naming Convention:**
- `<agent-name>`: Agent subdirectory (lowercase, hyphenated)
- `YYYY-MM-DD`: Date in ISO 8601 format
- `THHMM`: Time in 24-hour format
- `<description>`: Short description (lowercase, hyphenated, max 50 chars)

**Example:** `work/reports/logs/curator/2025-11-23T0811-orchestration-guide.md`

## 3. Work Log Structure

Work logs MUST include the following sections:

### Required Sections

```markdown
# Work Log: <Brief Title>

**Agent:** <agent-name>
**Task ID:** <task-id> (if applicable)
**Date:** YYYY-MM-DDTHH:MM:SSZ
**Status:** completed | in-progress | blocked

## Context

Brief description of what prompted this work:
- Task assignment details
- Problem statement
- Initial conditions

## Approach

Detailed explanation of the approach taken:
- Decision-making rationale
- Alternative approaches considered
- Why this approach was selected

## Guidelines & Directives Used

Explicit list of which context layers and directives informed the work:
- General Guidelines: <yes/no>
- Operational Guidelines: <yes/no>
- Specific Directives: <list codes, e.g., 001, 004, 008>
- Agent Profile: <agent-name>
- Reasoning Mode: </analysis-mode | /creative-mode | /meta-mode>

## Execution Steps

Chronological log of actions taken:
1. Step 1 description
2. Step 2 description
3. ...

Include:
- Key decisions made at each step
- Tools or commands used
- Challenges encountered and resolutions

## Artifacts Created

List of all files created or modified:
- `path/to/artifact1.md` - Description
- `path/to/artifact2.yaml` - Description

## Outcomes

Results of the work:
- Success metrics met
- Deliverables completed
- Handoffs initiated (if applicable)

## Lessons Learned

Reflections for framework improvement:
- What worked well
- What could be improved
- Patterns that emerged
- Recommendations for future tasks

## Metadata

- **Duration:** <time-spent>
- **Token Count:** 
  - Input tokens: <tokens-loaded-from-context>
  - Output tokens: <tokens-generated-in-artifacts>
  - Total tokens: <input + output>
- **Context Size:** <files-loaded-with-estimates>
- **Handoff To:** <next-agent> (if applicable)
- **Related Tasks:** <task-ids> (if applicable)
- **Primer Checklist:** List which primers (Context Check, Progressive Refinement, Trade-Off Navigation, Transparency, Reflection) were executed, skipped, or not applicable with justification. Reference ADR-011.
```

### Optional Sections

- **Challenges & Blockers:** Detailed issues encountered
- **Research Notes:** Investigation findings
- **Collaboration Notes:** Cross-agent coordination details
- **Technical Details:** Implementation specifics
- **References:** External resources consulted

## 4. Work Log Content Guidelines

### Tone & Style
- Technical but accessible
- Concise yet comprehensive
- First-person perspective ("I did X because Y")
- Chronological narrative flow

### Required Detail Level
- **Context:** Sufficient for another agent to understand the starting point
- **Approach:** Enough detail to reproduce the reasoning process
- **Execution:** Specific commands, file paths, and decision points
- **Lessons:** Actionable insights, not generic observations

### Transparency Standards
- State assumptions explicitly
- Mark uncertainties with ⚠️
- Indicate where guidance was unclear
- Note deviations from standard procedures with rationale

## 5. Work Log vs Task Result

**Task Result** (in task YAML):
- Brief summary (1-2 sentences)
- Artifact list
- Handoff details
- Completion timestamp

**Work Log** (in markdown):
- Detailed narrative
- Reasoning process
- Step-by-step execution
- Framework improvement insights

Both are required for orchestrated tasks; they serve different purposes.

## 6. Usage for Framework Tuning

Work logs enable:
- **Pattern Recognition:** Identify common agent behaviors and workflows
- **Directive Refinement:** Detect gaps or ambiguities in current directives
- **Agent Profile Tuning:** Improve specialization boundaries and capabilities
- **Quality Assurance:** Compare intended vs actual agent behavior
- **Training Data:** Generate examples for agent onboarding and testing

Human reviewers should:
- Read work logs to understand agent reasoning
- Compare approach against stated directives
- Identify areas where additional guidance would help
- Extract successful patterns for documentation

## 7. Validation

Work logs MUST:
- Include all required sections
- Follow naming convention
- Reference specific directives used
- Provide actionable lessons learned
- Include token count metrics (input, output, total)
- Include context size analysis (files loaded with estimates)
- Be committed to Git alongside task completion

Work logs SHOULD:
- Be written immediately after task completion
- Include timestamps for major decision points
- Cross-reference related artifacts
- Note any directive conflicts or ambiguities

## 8. Example Work Log

See: `work/logs/2025-11-23T0811-curator-orchestration-guide.md` (reference implementation)

## 9. Integration with Task Lifecycle

When completing an orchestrated task:

1. Update task YAML with `result` block (brief summary)
2. Create detailed work log in `work/logs/`
3. Move task to `work/done/<agent-slug>/`
   - **Important:** Tasks must be moved to the agent-specific subdirectory under `work/done/`, not directly to `work/done/` root
   - Example: A curator task goes to `work/done/curator/`, not `work/done/`
4. Create handoff task (if applicable)
5. Commit all changes together

The work log is part of task completion, not an optional add-on.

## 10. Access & Maintenance

- **Write Access:** All agents can create work logs for their own tasks
- **Read Access:** All agents and humans should review logs for learning
- **Archival:** Work logs remain in `work/logs/` indefinitely (no automatic archival)
- **Indexing:** Consider creating `work/logs/INDEX.md` for easy navigation (optional)

## 11. Non-Compliance

If an agent completes an orchestrated task without creating a work log:
- Human reviewers should request one retroactively
- Manager agent may create a follow-up task for log generation
- Repeated omissions indicate need for agent profile refinement

Work log creation is not optional for orchestrated tasks—it's a core requirement for framework evolution.

