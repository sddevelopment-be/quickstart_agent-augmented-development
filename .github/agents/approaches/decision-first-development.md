# Decision-First Development Workflow

**Approach Type:** Documentation Pattern  
**Version:** 1.0.0  
**Last Updated:** 2025-11-25  
**Status:** Active

## Overview

This approach describes how to systematically capture architectural decisions throughout the development lifecycle, integrating decision rationale with artifacts to preserve "why" knowledge for future contributors and AI agents. It implements the traceable decision patterns established in ADR-017.

## Core Principles

### 1. Decision Visibility
Every architectural decision should be discoverable and traceable from ideation through implementation.

### 2. Flow State Respect
Decision capture timing should adapt to individual productivity rhythms—defer when deep in creation, collaborate when iterating with agents, formalize during reflection.

### 3. Bidirectional Linking
Decisions reference affected artifacts; artifacts reference governing decisions. No orphaned rationale.

### 4. Progressive Fidelity
Start with lightweight markers, evolve to synthesis documents, formalize as ADRs when patterns stabilize.

### 5. Agent Awareness
AI agents check relevant ADRs before proposing changes and include decision references in generated artifacts.

## When to Use This Approach

**Use decision-first development when:**
- Making architectural choices that will affect multiple components
- Evaluating trade-offs between alternative implementations
- Establishing conventions or patterns for the codebase
- Working with AI agents on complex features requiring context
- Onboarding new contributors who need to understand rationale

**Do NOT use this approach when:**
- Making trivial implementation details (e.g., variable naming)
- Implementing well-established patterns already documented
- Working on experimental prototypes not intended for production
- Decision rationale is obvious from the code itself

## Decision Capture Workflow

### Phase 1: Exploration (Ideation)

**Objective:** Investigate problem space and evaluate options.

**Activities:**
- Research alternative approaches
- Document trade-offs and constraints
- Capture assumptions and unknowns
- Sketch potential solutions

**Artifacts:**
- Ideation documents in `docs/ideation/<topic>/`
- Exploration notes with alternatives considered
- Proof-of-concept code (if applicable)

**Decision Markers:**
```markdown
<!-- EXPLORATION-NOTE: ADR pending -->
**Problem:** [Statement of problem being explored]
**Options:** [List of alternatives being evaluated]
**Open Questions:** [Uncertainties requiring resolution]
```

### Phase 2: Synthesis (Integration)

**Objective:** Integrate multiple exploration threads into coherent patterns.

**Activities:**
- Map related ideation documents
- Identify recurring themes
- Assess architectural compatibility
- Evaluate implementation costs

**Artifacts:**
- Synthesis documents in `docs/architecture/synthesis/`
- Pattern integration analysis
- Recommendations for formalization

**Decision Markers:**
```markdown
**Pattern Identified:** [Name of recurring pattern]
**Source Ideations:** [Links to exploration documents]
**Recommended Action:** [ADR creation, directive update, etc.]
```

### Phase 3: Formalization (ADR)

**Objective:** Document architectural decision with full rationale.

**Activities:**
- Draft ADR using standard template
- Reference source ideation and synthesis
- List affected artifacts and directives
- Define acceptance criteria

**Artifacts:**
- ADR in `docs/architecture/adrs/ADR-NNN-<title>.md`
- Updates to ADR README index
- Cross-references to related ADRs

**Decision Markers:**
```markdown
<!-- DECISION-MARKER: ADR-NNN -->
**Decision:** [Brief statement of what was decided]
**Rationale:** [Why this approach was chosen]
**Alternatives:** [Options considered and rejected]
**Consequences:** [Accepted trade-offs]
**Status:** Implemented
**Date:** YYYY-MM-DD
<!-- END-DECISION-MARKER -->
```

### Phase 4: Implementation (Code/Docs)

**Objective:** Apply decision in artifacts with clear traceability.

**Activities:**
- Add decision markers to code/documentation
- Reference ADRs in commit messages
- Update directives if behavioral changes needed
- Link artifacts to governing decisions

**Artifacts:**
- Code files with decision markers
- Documentation with ADR references
- Updated directives (if applicable)

**Commit Message Format:**
```
<type>: <subject>

Decision: [Brief decision statement]
ADR: [ADR-NNN reference]
Rationale: [One-line justification]
Context: [Link to synthesis/ideation if applicable]
```

**Inline Marker (code/docs):**
```markdown
<!-- DECISION-MARKER: ADR-NNN -->
**Decision:** [What was decided]
**Rationale:** [Why this approach]
**ADR:** [Link to ADR-NNN]
**Context:** [Link to synthesis if applicable]
<!-- END-DECISION-MARKER -->
```

## Flow State Adaptation

### Deep Creation Flow

**Characteristics:**
- Uninterrupted focus on implementation
- High cognitive load from problem-solving
- Momentum-driven progress

**Decision Capture Strategy:**
```
1. Add lightweight markers in code (<!-- TODO: DECISION -->) 
2. Defer formal documentation to session-end
3. Agents stay passive, no interruptions
4. Batch markers into decision log at break point
```

**Agent Behavior:**
- Passive background support only
- No decision-related interruptions
- Capture context for later synthesis

**Example:**
```python
# TODO: DECISION - Why async here? 
# Related to coordination pattern from ideation/2025-11-20.md
async def process_task():
    ...
```

### Agent Collaboration Flow

**Characteristics:**
- Iterative refinement with AI assistance
- Active back-and-forth on approach
- Real-time decision-making

**Decision Capture Strategy:**
```
1. Agent suggests decision markers during iteration
2. Use templates for consistent format
3. Document immediately with agent assistance
4. Reference relevant ADRs in context
```

**Agent Behavior:**
- Active co-creation with templates
- Suggest relevant ADRs to check
- Validate decision marker format
- Add decision rationale to task results

**Example Interaction:**
```
Human: "Should we use file-based or API coordination?"
Agent: "Checking ADR-008... File-based coordination is established pattern.
        Shall I add decision marker referencing ADR-008?"
Human: "Yes"
Agent: [Adds formatted decision marker with ADR-008 reference]
```

### Reflection/Synthesis Flow

**Characteristics:**
- Dedicated time for documentation
- Lower cognitive load from active coding
- Big-picture thinking mode

**Decision Capture Strategy:**
```
1. Review accumulated markers from creation sessions
2. Draft formal ADRs from patterns
3. Update synthesis documents
4. Agents summarize and suggest formalization
```

**Agent Behavior:**
- Summarize decision patterns
- Suggest when markers should become ADRs
- Draft synthesis documents from related decisions
- Validate cross-references

**Example:**
```
Agent: "Found 5 decision markers related to coordination patterns.
        Decision debt ratio: 35% (above 20% threshold).
        Recommend: Draft ADR consolidating these decisions.
        Shall I create synthesis document first?"
```

## Implementation Steps

### For Human Contributors

**Starting a Feature:**

1. Check ADR README for related decisions
2. Review relevant synthesis documents
3. Identify governing ADRs for your area
4. Note any new decisions needed

**During Development:**

1. **Deep creation:** Add TODO markers for decisions
2. **Collaboration:** Work with agent to add formal markers
3. **Commit:** Include decision references in messages
4. **Session-end:** Batch TODO markers into proper format

**Completing Work:**

1. Ensure all decision markers reference ADRs
2. Update ADR forward links if new artifacts created
3. Create synthesis doc if multiple related decisions made
4. Add decision rationale to work log

### For AI Agents

**Pre-Task Check:**

1. Load ADR README to identify relevant decisions
2. Read referenced ADRs into context
3. Note any decision patterns in task description
4. Flag if task conflicts with established ADRs

**During Execution:**

1. Reference relevant ADRs in generated artifacts
2. Add decision markers when architectural choices made
3. Validate all markers follow standard format
4. Include decision rationale in task YAML result

**Post-Task:**

1. Add decision context to work log
2. Extract patterns for potential synthesis
3. Flag decision debt if markers accumulate
4. Suggest ADR creation when appropriate

### For Agent Orchestrator

**Task Assignment:**

1. Identify ADRs relevant to task scope
2. Include ADR references in task context
3. Flag tasks requiring decision documentation

**Handoff Processing:**

1. Check decision rationale in completed tasks
2. Propagate decision context to next agent
3. Track decision debt metrics

**Health Monitoring:**

1. Calculate decision debt ratio across tasks
2. Alert when debt exceeds 20% threshold
3. Suggest synthesis review when patterns emerge

## Decision Marker Reference

### Inline Marker (Full Format)

```markdown
<!-- DECISION-MARKER: ADR-017 -->
**Decision:** Use file-based coordination for agent handoffs
**Rationale:** Git-native, transparent, no infrastructure dependencies
**Alternatives:** Message queue (rejected: operational complexity), API (rejected: network dependency)
**Consequences:** Latency measured in seconds not milliseconds (acceptable for our use case)
**Status:** Implemented
**Date:** 2025-11-20
<!-- END-DECISION-MARKER -->
```

### Inline Marker (Minimal)

```markdown
<!-- DECISION: ADR-017 - File-based coordination chosen for Git-native transparency -->
```

### Commit Message Format

```
feat: implement async task routing

Decision: File-based coordination (ADR-008)
Rationale: Git-native, transparent, no new dependencies
Context: Exploration in docs/ideation/architecture/2025-11-20-coordination-patterns.md
```

### Task YAML Schema

```yaml
task:
  id: "2025-11-25T1200-architect-coordination"
  status: "done"
  decision_rationale:
    adr: "ADR-017"
    justification: "Traceable decision patterns require explicit linking"
    alternatives_considered: ["inline comments only", "separate decision log"]
    chosen_because: "Integrated with task lifecycle, visible to agents"
```

## Discovery Patterns

### For Human Contributors

**Finding Decision Rationale:**

1. **Start with ADR README:** Canonical index of all major decisions
2. **Follow synthesis trail:** Synthesis docs link ideation → ADR
3. **Check artifact headers:** New files reference governing ADRs
4. **Search decision markers:** `rg "DECISION-MARKER"` finds embedded rationale
5. **Review work logs:** Agent logs include decision context

**Common Searches:**

```bash
# Find all decision markers
rg "DECISION-MARKER" --type md

# Find ADR references in code
rg "ADR-\d+" --type py --type js

# List decisions by topic
rg "Decision:.*coordination" docs/architecture/adrs/

# Find decisions needing formalization
rg "TODO: DECISION" --type md --type py
```

### For AI Agents

**Pre-Check Protocol:**

1. Load `docs/architecture/adrs/README.md` for decision index
2. Identify ADRs relevant to task scope (keyword match)
3. Load full text of 2-3 most relevant ADRs
4. Check for related synthesis documents
5. Flag if task conflicts with established decisions

**Context Loading Strategy:**

```yaml
# Load selectively to manage context window
priority_high:
  - ADR README (always load)
  - ADRs matching task keywords (top 3)
  
priority_medium:
  - Synthesis docs referenced by ADRs
  - Recent work logs from same agent type
  
priority_low:
  - Full ideation document history
  - Older ADRs unless specifically referenced
```

**Validation Checks:**

- Verify decision markers reference valid ADRs (no broken links)
- Check new artifacts include ADR references in headers
- Ensure commit messages include decision rationale
- Validate decision marker format compliance

## Best Practices

### Decision Capture

- **Capture early:** Don't wait until implementation complete
- **Capture often:** Small markers better than one large ADR
- **Capture context:** Include "why not" for rejected alternatives
- **Capture uncertainty:** Mark assumptions and open questions

### Marker Management

- **Start lightweight:** TODO markers during deep creation
- **Formalize iteratively:** Promote to proper markers during collaboration
- **Batch sensibly:** Group related decisions in synthesis docs
- **Promote judiciously:** Not every marker needs an ADR (20% debt ratio acceptable)

### Agent Coordination

- **Check ADRs first:** Load relevant decisions before proposing changes
- **Reference explicitly:** Link ADRs in generated artifacts
- **Validate consistently:** Run format checks on decision markers
- **Suggest patterns:** Extract recurring themes for synthesis

### Quality Standards

- **All ADRs link to source explorations** (if applicable)
- **All new artifacts reference governing ADRs** (header/frontmatter)
- **All architectural changes include decision rationale** (commit messages)
- **All agent work logs document decision-making** (context section)

## Decision Debt Tracking

### Metric Definition

**Decision Debt Ratio** = (Total markers - Promoted to ADRs) / Total markers

### Acceptable Thresholds

- **<20%** (Green): Healthy balance, some markers are implementation details
- **20-40%** (Yellow): Growing backlog, schedule synthesis review
- **>40%** (Red): Critical, requires dedicated ADR creation time

### Tracking in Work Logs

```yaml
metrics:
  decision_debt:
    markers_added: 3           # New decision markers created
    markers_promoted: 1        # Markers formalized as ADRs
    adrs_referenced: 2         # Existing ADRs linked
    debt_ratio: 0.15          # Calculated ratio
```

### Monthly Review

1. Calculate aggregate decision debt across all tasks
2. Identify agents/task types with highest debt
3. Schedule synthesis sessions for high-debt areas
4. Promote critical markers to ADRs
5. Archive resolved markers

## Integration with Agent Profiles

Each agent profile should specify:

### Decision Awareness

- **Pre-check requirements:** Which ADRs to load before starting tasks
- **Reference patterns:** How to cite ADRs in generated artifacts
- **Marker generation:** When to suggest decision markers
- **Validation:** Decision traceability checks to perform

### Example from Architect Profile

```markdown
### Decision-First Development

- Check `docs/architecture/adrs/README.md` before proposing new patterns
- Reference relevant ADRs in all architecture documents
- Add decision markers when establishing new conventions
- Draft synthesis documents from related explorations
- Suggest ADR creation when patterns stabilize (3+ related decisions)
- Track decision debt in work logs
```

## Validation

Use these checks to ensure correct implementation:

**Decision Marker Format:**
```bash
# Validate marker syntax
rg 'DECISION-MARKER: ADR-\d+' --count docs/

# Check for incomplete markers
rg 'TODO: DECISION' --count
```

**ADR Linking:**
```bash
# Verify ADR cross-references are valid
python work/scripts/validate-adr-links.py

# Check new artifacts reference ADRs
rg '^<!-- ADR' docs/ --count
```

**Decision Debt:**
```bash
# Calculate current debt ratio
python work/scripts/calculate-decision-debt.py work/logs/
```

**Quality Standards:**
- All ADRs have unique numbers
- ADR cross-references are valid (no broken links)
- New artifacts in `docs/` reference at least one ADR
- Work logs include decision rationale sections
- Task YAMLs with architectural impact include `decision_rationale` block

## Troubleshooting

### Decision Marker Overload

**Symptoms:** Too many markers, signal-to-noise ratio degrading.

**Causes:**
- Marking implementation details instead of architectural decisions
- Not promoting markers to ADRs when patterns stabilize
- Over-documenting obvious choices

**Solutions:**
1. Review markers monthly, archive implementation details
2. Promote recurring patterns to ADRs
3. Reserve markers for non-obvious decisions
4. Target <20% decision debt ratio

### Broken ADR References

**Symptoms:** Links to non-existent ADRs in decision markers.

**Causes:**
- ADR numbers changed during reorganization
- Marker references ADR not yet created
- Typos in ADR numbers

**Solutions:**
1. Run link validation script
2. Update markers to reference correct ADRs
3. Create missing ADRs if decisions are critical
4. Integrate validation into CI/pre-commit

### Low Decision Debt but Poor Discoverability

**Symptoms:** All markers promoted to ADRs, but contributors still can't find rationale.

**Causes:**
- ADRs not linked from artifacts
- Missing synthesis documents
- ADR README not maintained
- Search keywords don't match actual decisions

**Solutions:**
1. Add ADR references to artifact headers
2. Create synthesis docs linking related ADRs
3. Update ADR README with better categorization
4. Improve ADR titles and keywords

## References

- **Authoritative ADR:** [ADR-017: Traceable Decision Integration](../../../docs/architecture/adrs/ADR-017-traceable-decision-integration.md)
- **Synthesis:** [Traceable Decision Patterns Synthesis](../../../docs/architecture/synthesis/traceable-decision-patterns-synthesis.md)
- **Source Ideation:**
  - [Structured Knowledge Sharing](../../../docs/ideation/tracability/structured_knowledge_sharing.md)
  - [Personal Productivity Flow](../../../docs/ideation/tracability/personal_productivity_flow.md)
- **Directives:**
  - 004: Documentation & Context Files
  - 008: Artifact Templates
  - 018: Traceable Decisions (implementing directive)
- **Related ADRs:**
  - ADR-001: Modular Agent Directive System
  - ADR-003: Task Lifecycle and State Management
  - ADR-004: Work Directory Structure
  - ADR-008: File-Based Async Coordination
  - ADR-009: Orchestration Metrics Standard

## Change Log

| Version | Date       | Changes                                      |
|---------|------------|----------------------------------------------|
| 1.0.0   | 2025-11-25 | Initial approach documentation               |

---

_Maintained by: Curator Claire & Architect Alphonso_  
_For questions, see: `.github/agents/curator.agent.md` or `.github/agents/architect.agent.md`_
