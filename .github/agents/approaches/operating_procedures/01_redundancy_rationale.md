# Redundancy Rationale for Behavioral Norms

## Purpose

Explain why behavioral norms are intentionally duplicated across agent profiles, directives, and other framework components.

## Design Decision

This directive **intentionally duplicates** behavioral norms found in individual agent profiles and other directives. This redundancy serves critical safety and operational purposes.

**Tradeoff:** We accept the ~200-300 token overhead in exchange for increased reliability and safety.

## Cognitive Priming

### Context Loading Variations
- Agents may load context in different orders or with partial directive sets
- Repetition ensures critical norms are reinforced regardless of load sequence
- Cognitive anchoring: seeing a behavioral rule multiple times increases adherence

### Example Scenario
An agent initializes with only its profile loaded, before directives are available. If the profile contains key behavioral norms (e.g., "ask clarifying questions when uncertainty >30%"), the agent can operate safely even with incomplete context.

## Defense Against Partial Context Loss

### Context Window Fragmentation
- LLM context windows can be truncated or fragmented
- If an agent profile is partially loaded or corrupted, safety-critical behaviors remain accessible
- Fallback mechanism: if specific directive is unavailable, this catch-all ensures baseline behavior

### Resilience Strategy
Multiple instances of critical behavioral rules create redundancy similar to RAID storage:
- If one "copy" is inaccessible, others provide the same guidance
- Reduces single points of failure in agent behavior

## Consistency Across Agent Specializations

### Cross-Domain Operation
- Different agents may operate in vastly different domains (code, documentation, architecture)
- Centralizing shared norms ensures uniform behavior despite role differences
- Cross-agent collaboration depends on predictable, consistent operational protocols

### Example
When Curator Claire delegates to Architect Alex, both agents follow the same core behavioral norms (clarifying questions, validation alignment, minimal diffs) even though their specializations differ dramatically.

## Validation and Audit Trail

### Single Source of Truth
- Having a central reference for behavioral norms simplifies validation
- Human reviewers can reference this directive to check agent conformity
- Automated tools can verify agent outputs against centralized behavioral standards

### Quality Assurance
Framework maintainers can:
1. Update behavioral norms in one place (Directive 012)
2. Propagate to agent profiles as needed
3. Validate consistency across all agents
4. Track behavioral compliance over time

## Recovery and Rehydration

### Session Continuity
- When agents restart or rehydrate from previous sessions, loading this directive provides quick behavioral calibration
- Acts as a "sanity check" reference point for resumed operations
- Ensures continuity of behavioral norms across session boundaries

### Cold Start Protection
New agent sessions benefit from immediate access to behavioral guidelines without requiring full context reconstruction.

## Safety-Critical Threshold Example

### The "30% Uncertainty Rule"

**Why It's Repeated:**
The line "Ask clarifying questions when uncertainty >30%." appears in:
1. Every agent's Collaboration Contract section
2. Directive 012 (Common Operating Procedures)
3. Various approach files where relevant

**Justification:**
- This specific threshold is safety-critical
- Must be visible in every agent's primary operating context
- Cannot rely on external directives that may or may not be loaded
- Prevents agents from proceeding with ambiguous tasks

## Token Cost Justification

### Cost Analysis
- Redundancy overhead: ~200-300 tokens
- Misalignment risk reduction: High
- Safety improvement: Significant

### Return on Investment
**Without redundancy:**
- Agent operates with partial context → misalignment risk
- Misalignment detected → rollback, re-execution, token waste
- Human intervention required → delay, context switching cost

**With redundancy:**
- Agent operates consistently even with partial context
- Behavioral norms accessible from multiple sources
- Reduced misalignment incidents → net token savings over time

### Calculation Example
If redundancy prevents even 1 misalignment incident per 10 tasks:
- Cost: 300 tokens × 10 tasks = 3,000 tokens
- Savings: 1 rollback/re-execution = ~5,000-10,000 tokens
- **Net benefit: 2,000-7,000 tokens saved**

## Implementation Guidelines

### What to Repeat
Safety-critical behavioral norms that:
- Prevent irreversible operations
- Ensure human collaboration (clarifying questions)
- Maintain code/documentation integrity (minimal diffs)
- Enable validation and recovery

### What NOT to Repeat
- Implementation details specific to one context
- Formatting preferences without safety impact
- Tool-specific instructions
- Temporary or experimental guidelines

### Propagation Rules
When updating redundant behavioral norms:
1. Update Directive 012 first (source of truth)
2. Propagate to agent profiles
3. Update approach files if relevant
4. Validate consistency with search: `rg "uncertainty >30%"`

## Non-Removal Clause

**CRITICAL:** Safety-critical behavioral norms MUST remain in every agent's primary context.

**Example:** The "Ask clarifying questions when uncertainty >30%." line MUST remain in every agent's Collaboration Contract section.

**Reason:** This ensures the behavioral norm is visible even if:
- Directives are not loaded
- Context window is truncated
- Agent initializes with minimal context

## Framework Evolution

### Future Considerations
As the framework evolves, monitor:
- Actual redundancy token costs
- Misalignment incident rates
- Agent behavior consistency metrics
- Context loading patterns

### Adjustment Triggers
Consider reducing redundancy if:
- Context loading becomes fully reliable
- Context window sizes increase significantly
- Misalignment rates drop below threshold (< 1%)

Consider increasing redundancy if:
- Misalignment incidents increase
- New safety-critical norms emerge
- Cross-agent collaboration expands

## Summary

Redundancy in behavioral norms is a **conscious design decision** that prioritizes:
1. **Safety**: Multiple access points for critical guidelines
2. **Reliability**: Consistent behavior across contexts
3. **Resilience**: Protection against partial context loss
4. **Collaboration**: Predictable cross-agent interaction

The token cost is justified by reduced misalignment incidents, improved safety, and enhanced framework reliability.
