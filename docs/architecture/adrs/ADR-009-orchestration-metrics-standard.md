# ADR-009: Orchestration Metrics and Quality Standards

**status**: `Accepted`  
**date**: 2025-11-23  
**supersedes**: None  
**related**: ADR-008 (File-Based Async Coordination)

## Context

After completing POC1 (Curator) and POC2 (Diagrammer) for the file-based orchestration framework, we discovered several quality and measurement gaps that limit our ability to:

1. **Benchmark performance**: Without standardized metrics capture, we cannot compare agent efficiency or identify bottlenecks
2. **Validate artifact quality**: Missing per-artifact integrity markers reduce validation granularity
3. **Maintain accessibility**: Diagrams lack alt-text descriptions, reducing inclusivity
4. **Scale work logs**: No tiering guidance leads to inconsistent verbosity (440 lines for POC1 vs concise POC2)
5. **Verify rendering**: Diagram syntax correctness remains unvalidated until human review

### Evidence from POC Executions

**POC1 (Curator) - 2025-11-23T07:22**
- **Duration**: ~18 minutes (estimated from timestamps)
- **Deliverables**: 1 user guide (multi-agent-orchestration.md)
- **Work log size**: 440 lines
- **Strengths**: Rich audit trail, clear handoff mechanism
- **Weaknesses**: Log verbosity excessive for single deliverable, no structured metrics

**POC2 (Diagrammer) - 2025-11-23T12:00**
- **Duration**: ~22 minutes for 5 artifacts
- **Deliverables**: 4 new PlantUML diagrams + 1 reused state machine + README
- **Work log size**: Concise with structured sections
- **Strengths**: Multi-artifact efficiency, mode differentiation (/creative-mode)
- **Weaknesses**: No rendering verification, missing accessibility metadata, inconsistent metrics format

### Architectural Concerns

The orchestration framework must support:
- Continuous improvement through measurable performance data
- Quality assurance through granular validation
- Inclusive documentation through accessibility standards
- Efficient communication through tiered logging
- Pre-commit verification through automated checks

Without standardized practices, these concerns remain unmet, limiting production readiness for multi-agent chains (POC3 and beyond).

## Decision

**We will establish mandatory metrics capture and quality standards for all orchestrated agent tasks.**

Specifically:

### 1. Structured Metrics Capture

All agents completing orchestrated tasks MUST include a `metrics` block in task results:

```yaml
result:
  summary: "Brief description of work completed"
  artefacts:
    - "path/to/artifact.md"
  metrics:
    duration_minutes: 22
    token_count:
      input: 15000
      output: 8500
      total: 23500
    context_files_loaded: 12
    artifacts_created: 5
    artifacts_modified: 2
    per_artifact_timing:
      - name: "task-lifecycle-state-machine.puml"
        action: "reused"
        duration_seconds: 30
      - name: "workflow-sequential-flow.puml"
        action: "created"
        duration_seconds: 180
  completed_at: "2025-11-23T12:22:00Z"
```

**Required Fields:**
- `duration_minutes`: Total task execution time
- `token_count`: Input, output, and total token usage
- `context_files_loaded`: Number of files read for context
- `artifacts_created`: Count of new files
- `artifacts_modified`: Count of edited files

**Optional Fields:**
- `per_artifact_timing`: Detailed breakdown for multi-artifact tasks
- `mode_transitions`: Log of reasoning mode switches
- `handoff_latency_seconds`: Time between task completion and next task creation

### 2. Per-Artifact Integrity Markers

Work logs MUST include explicit validation markers for each artifact:

```markdown
## Artifacts Created

- ✅ `docs/architecture/diagrams/workflow-sequential-flow.puml` - Validated: Syntax correct, semantic fidelity confirmed
- ✅ `docs/architecture/diagrams/workflow-parallel-flow.puml` - Validated: Cross-referenced with design doc
- ⚠️ `docs/architecture/diagrams/metrics-dashboard.puml` - Partial: Syntax correct, awaiting user feedback on layout
```

**Validation Levels:**
- ✅ Full validation: Artifact meets all quality criteria
- ⚠️ Partial validation: Artifact created but has known limitations
- ❗️ Validation failed: Artifact has errors requiring correction

### 3. Tiered Work Logging

Work logs SHALL follow a two-tier structure:

**Core Tier (Required):**
- Context (3-5 sentences)
- Approach (key decisions only)
- Execution Steps (numbered list, 5-10 items)
- Artifacts Created (list with validation markers)
- Outcomes (success metrics)
- Metadata (duration, tokens, handoff)

**Extended Tier (Optional):**
- Challenges & Blockers (detailed issues)
- Research Notes (investigation findings)
- Collaboration Notes (cross-agent details)
- Technical Details (implementation specifics)

**Guidance:**
- Single-deliverable tasks: Core tier sufficient
- Multi-artifact tasks (>3 artifacts): Core tier + selective Extended sections
- Complex multi-agent chains: Core tier + full Extended tier for handoff artifacts

**Target Size:**
- Core tier: 100-200 lines
- Extended tier: Additional 100-300 lines as needed

### 4. Accessibility Requirements

All visual artifacts (diagrams, charts, graphs) MUST have accompanying textual descriptions.

**Implementation:**
- Create `docs/architecture/diagrams/DESCRIPTIONS.md` as central registry
- Each diagram entry includes:
  - File path
  - Alt-text summary (1-2 sentences)
  - Detailed description (accessibility-focused)
  - Last updated timestamp

**Example:**
```markdown
### workflow-sequential-flow.puml

**Alt-text:** "Sequence diagram showing three-agent linear workflow: Architect creates ADR, Writer-Editor polishes content, Curator validates consistency."

**Description:** This PlantUML sequence diagram illustrates a sequential workflow pattern where tasks flow linearly between three specialized agents. The Architect agent initiates by creating an architecture decision record (ADR), which is then handed off to the Writer-Editor agent for clarity improvements. Finally, the Curator agent performs structural validation. Each handoff is represented by an arrow with labeled task metadata, and completion states are marked with checkmarks.

**Updated:** 2025-11-23T12:15:00Z
```

### 5. Diagram Rendering Verification

Visual artifacts MUST be validated for syntax correctness before task completion.

**Options:**
1. **CI Integration** (preferred): Add PlantUML rendering check to GitHub Actions
2. **Local Script**: `work/scripts/render-diagrams.sh` for pre-commit validation
3. **Manual Verification**: Agent renders locally and confirms in work log

**Minimum Standard:**
- Agent MUST attempt rendering or include ⚠️ marker noting unverified syntax
- Syntax errors MUST be corrected before marking artifact as ✅ validated

## Rationale

### Why Structured Metrics?

**Problem:** Ad-hoc metrics (POC1: estimated timing; POC2: informal notes) prevent:
- Performance benchmarking across agents
- Bottleneck identification in multi-agent chains
- Token efficiency optimization
- Comparative analysis of approach effectiveness

**Solution:** Standardized metrics block enables:
- Data-driven framework tuning
- Agent performance profiling
- Predictable resource planning
- Evidence-based process improvements

**Trade-off:** Slight overhead to capture metrics (~30 seconds per task) justified by long-term optimization value.

### Why Per-Artifact Validation?

**Problem:** POC2 used single overall success marker, obscuring which artifacts were fully validated vs. assumed correct.

**Solution:** Explicit per-artifact markers surface:
- Validation confidence levels
- Incomplete work requiring follow-up
- Handoff risk areas for next agent

**Trade-off:** More verbose artifact lists, but critical for multi-artifact quality assurance.

### Why Tiered Logging?

**Problem:** POC1 produced 440-line log for single deliverable (excessive); POC2 was concise but lacked deep rationale for complex decisions. No guidance led to inconsistency.

**Solution:** Core/Extended tiers balance:
- **Auditability**: Core tier ensures minimum traceability
- **Efficiency**: Simple tasks avoid unnecessary verbosity
- **Depth**: Complex tasks can expand with Extended tier
- **Consistency**: Clear guidelines reduce variance

**Trade-off:** Agents must decide tier appropriateness, but guidelines minimize ambiguity.

### Why Accessibility Standards?

**Problem:** POC2 diagrams lack alt-text, limiting:
- Screen reader usability
- Non-visual understanding
- Search/discovery capability
- Compliance with accessibility standards

**Solution:** Centralized descriptions registry ensures:
- Consistent accessibility metadata
- Discoverability via single file
- Maintenance simplicity
- Git-tracked evolution

**Trade-off:** Additional work per diagram (~5 minutes), but mandatory for inclusive documentation.

### Why Rendering Verification?

**Problem:** Diagram syntax errors discovered only during manual review or CI failure, delaying feedback loop.

**Solution:** Pre-commit or agent-time rendering catches:
- Syntax errors immediately
- Layout issues before merge
- Semantic drift from intent

**Trade-off:** Requires PlantUML tooling or CI setup, but prevents downstream failures.

## Envisioned Consequences

### Positive

✅ **Measurable Performance**: Standardized metrics enable benchmarking and optimization  
✅ **Quality Assurance**: Per-artifact validation increases confidence in deliverables  
✅ **Efficient Communication**: Tiered logging balances audit depth with token efficiency  
✅ **Inclusive Documentation**: Accessibility standards ensure broad usability  
✅ **Early Error Detection**: Rendering verification catches issues before merge  
✅ **Framework Tuning**: Rich data supports directive refinement and agent profiling  
✅ **Predictability**: Consistent practices reduce variance and surprises  

### Negative

⚠️ **Additional Overhead**: Metrics capture and accessibility work add ~5-10% to task duration  
⚠️ **Learning Curve**: Agents must understand tiering and validation standards  
⚠️ **Tooling Dependency**: Rendering verification requires PlantUML setup  
⚠️ **Enforcement Challenge**: Requires reviewer diligence to ensure compliance  

### Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Metrics gaming**: Agents optimize for metrics vs. quality | Distorted priorities | Pair metrics with qualitative review; emphasize outcome over numbers |
| **Verbosity creep**: Extended tier overused | Token waste | Reinforce Core tier sufficiency in guidelines; review logs for patterns |
| **Accessibility neglect**: Descriptions become stale | Outdated metadata | Curator audits include DESCRIPTIONS.md freshness check |
| **Rendering false negatives**: Syntax correct but semantic drift | Misleading validation | Require semantic fidelity note in per-artifact marker |

## Implementation Roadmap

### Phase 1: Foundation (Pre-POC3)
- ✅ ADR-009 drafted and accepted
- [ ] Update Directive 014 with tiered logging standards
- [ ] Create `docs/architecture/diagrams/DESCRIPTIONS.md` template
- [ ] Add metrics block to task result template (`docs/templates/agent-tasks/task-result.yaml`)
- [ ] Document per-artifact validation marker format in Directive 014

### Phase 2: Validation (POC3 Execution)
- [ ] Architect task: Include metrics block in result
- [ ] Diagrammer task: Add accessibility descriptions for new/modified diagrams
- [ ] All agents: Use tiered logging (Core tier minimum)
- [ ] All agents: Include per-artifact validation markers
- [ ] Measure compliance rate and overhead impact

### Phase 3: Refinement (Post-POC3)
- [ ] Analyze POC3 metrics data for insights
- [ ] Adjust tiering guidelines based on observed patterns
- [ ] Add rendering verification script (`work/scripts/render-diagrams.sh`)
- [ ] Integrate PlantUML check into CI pipeline (optional)
- [ ] Update agent profiles with metrics/validation expectations

## Validation Criteria

This ADR succeeds if POC3 demonstrates:

1. **Metrics Completeness**: All agents provide structured metrics block (100% compliance)
2. **Artifact Validation**: Every artifact has explicit ✅/⚠️/❗️ marker (100% coverage)
3. **Log Efficiency**: Core tier logs average 100-200 lines; Extended tier used only for complex tasks
4. **Accessibility Coverage**: All diagrams have entries in DESCRIPTIONS.md with alt-text
5. **Quality Improvement**: Per-artifact validation catches ≥1 issue before final merge

## Related ADRs

- **ADR-008**: File-Based Asynchronous Agent Coordination (foundation for orchestration)
- **ADR-003**: Task Lifecycle and State Management (defines task result structure)
- **ADR-004**: Work Directory Structure (establishes work log location conventions)

## References

- **POC1 Assessment**: `work/logs/architect/2025-11-23T1125-orchestration-poc-dual-assessment.md` (Section 3-4)
- **POC2 Assessment**: `work/logs/architect/2025-11-23T1125-orchestration-poc-dual-assessment.md` (Section 4)
- **Post-PR Review**: `work/logs/architect/2025-11-23T1730-post-pr-review-orchestration-assessment.md` (Section 5.3, 7)
- **Directive 014**: `.github/agents/directives/014_worklog_creation.md` (work log standards)
- **Task Templates**: `docs/templates/agent-tasks/` (task descriptor formats)
- **Accessibility Guidelines**: WCAG 2.1 Level AA (informative reference)

---

**Maintained by:** Architect Alphonso  
**Next Review:** Post-POC3 (estimated 2025-11-24)  
**Version:** 1.0.0
