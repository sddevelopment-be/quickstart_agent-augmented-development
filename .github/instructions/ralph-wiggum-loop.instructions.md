# ralph-wiggum-loop

The Ralph Wiggum Loop is a self-observation pattern for agents to detect and correct issues mid-execution.

## Capabilities

- self-observation
- meta-cognition
- quality-assurance
- operational-pattern

## Instructions

The Ralph Wiggum Loop enables agents to pause during execution, observe their own state, recognize warning signs (drift, confusion, gold-plating), and self-correct before completing tasks. Named after the "I'm in danger!" meme, this pattern represents meta-awareness where agents recognize problematic patterns in their own behavior.

**When to Apply:**
- Long-running tasks (>30 minutes)
- Multi-step workflows (5+ operations)
- Before cross-agent handoffs
- After major context changes
- When uncertainty markers (⚠️) accumulate

**Implementation:**
1. Pause execution at trigger points
2. Switch to `/meta-mode` for self-observation
3. Run systematic checklist (8 warning signs)
4. Make decision: Continue ✅ / Adjust Course ⚠️ / Stop & Escalate ❗️
5. Document checkpoint in work log

**Related Documentation:**
- Approach: `.github/agents/approaches/ralph-wiggum-loop.md`
- Directive: `.github/agents/directives/024_self_observation_protocol.md`
- CLI Tool: `ops/scripts/ralph-wiggum-loop.py`
- Research: `work/reports/research/ralph-wiggum-loop-background.md`

**CLI Usage:**
```bash
# Run manual checkpoint
python ops/scripts/ralph-wiggum-loop.py check --task-id 2026-01-31T1200-task

# Watch mode with automatic checkpoints
python ops/scripts/ralph-wiggum-loop.py watch --task-id 2026-01-31T1200-task --interval 15

# Generate report
python ops/scripts/ralph-wiggum-loop.py report --task-id 2026-01-31T1200-task
```

## Example Prompts

- "Run a Ralph Wiggum loop checkpoint on my current task"
- "I need to observe my execution state for warning signs"
- "Check if I'm drifting from the original goal"
- "Am I in danger? (self-observation check)"

## Metadata

- **Status:** Proposed (validated by research)
- **Research Confidence:** High ✅✅
- **Academic Foundation:** MAPE-K loop, meta-cognition, BDI architecture
- **Novel Contribution:** Directive-driven checklist for LLM agents
- **Version:** 1.0.0
- **Date:** 2026-01-31
