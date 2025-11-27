# Documentation Template Library

**Version:** 1.0.0  
**Last Updated:** 2025-11-27  
**Purpose:** Centralized repository of reusable documentation templates for agent-augmented development

---

## Overview

This library provides standardized templates for documentation artifacts produced by autonomous agents and human collaborators. Using these templates ensures consistency, reduces token overhead, and improves interoperability across the multi-agent framework.

**Core Principles:**
- **Consistency:** All templates follow the same structural patterns
- **Modularity:** Templates are composable and can be combined
- **Clarity:** Clear guidance on when and how to use each template
- **Efficiency:** Reduce token consumption by referencing templates instead of including full structures

---

## Template Categories

### 1. Architecture Templates

**Location:** `docs/templates/architecture/`

| Template | Purpose | When to Use |
|----------|---------|-------------|
| **adr.md** | Architecture Decision Records | Document significant architectural decisions |
| **design_vision.md** | High-level design vision | Define long-term architectural direction |
| **technical_design.md** | Detailed technical specifications | Specify implementation details |
| **functional_requirements.md** | Functional requirements | Capture user needs and system behaviors |
| **roadmap.md** | Architecture roadmap | Plan evolutionary architecture changes |

**Usage Example:**
```bash
cp docs/templates/architecture/adr.md docs/architecture/decisions/ADR-015-template-library.md
# Edit the new file with specific decision details
```

### 2. Agent Task Templates

**Location:** `docs/templates/agent-tasks/`

| Template | Purpose | When to Use |
|----------|---------|-------------|
| **task-base.yaml** | Minimal task descriptor | Create simple task assignments |
| **task-context.yaml** | Extended task context | Add detailed guidance for complex tasks |
| **task-descriptor.yaml** | Complete task template | Reference for all available fields |
| **task-result.yaml** | Task completion structure | Document task outcomes |
| **task-error.yaml** | Error reporting structure | Report task failures |
| **task-examples.yaml** | Working examples | Copy and adapt for new tasks |
| **worklog.md** | Agent work log | Document agent execution and reasoning |
| **assessment.md** | Assessment reports | Evaluate artifacts, systems, or processes |
| **report.md** | General reporting | Create analysis, synthesis, or status reports |

**Usage Example:**
```bash
# Create a new task
cp docs/templates/agent-tasks/task-base.yaml work/collaboration/inbox/2025-11-27T1430-new-feature.yaml

# Document task completion
cp docs/templates/agent-tasks/worklog.md work/reports/logs/curator/2025-11-27T1430-feature-completion.md
```

**See:** [task-templates-README.md](./agent-tasks/task-templates-README.md) for detailed task template documentation.

### 3. Lexical Templates

**Location:** `docs/templates/LEX/`

| Template | Purpose | When to Use |
|----------|---------|-------------|
| **LEX_STYLE_RULES.md** | Style consistency rules | Define lexical standards |
| **LEX_DELTAS.md** | Style change tracking | Document style evolution |
| **LEX_REPORT.md** | Lexical analysis report | Report on terminology consistency |

**Usage Example:**
```bash
cp docs/templates/LEX/LEX_REPORT.md work/reports/logs/lexical/2025-11-27-terminology-audit.md
```

### 4. Project Templates

**Location:** `docs/templates/project/`

| Template | Purpose | When to Use |
|----------|---------|-------------|
| **VISION.md** | Project vision statement | Define project goals and direction |
| **CHANGELOG.md** | Change log structure | Track version history |
| **specific_guidelines.md** | Project-specific rules | Document custom guidelines |

**Usage Example:**
```bash
cp docs/templates/project/VISION.md docs/VISION.md
```

### 5. Structure Templates

**Location:** `docs/templates/structure/`

| Template | Purpose | When to Use |
|----------|---------|-------------|
| **REPO_MAP.md** | Repository structure map | Document directory organization |
| **SURFACES.md** | Interaction surfaces | Define system interfaces |
| **WORKFLOWS.md** | Process workflows | Document operational procedures |
| **CONTEXT_LINKS.md** | Context reference index | Link to key documentation |
| **repo-outline.yaml** | Machine-readable repo structure | Enable automated navigation |

**Usage Example:**
```bash
cp docs/templates/structure/WORKFLOWS.md docs/WORKFLOWS.md
```

### 6. Automation Templates

**Location:** `docs/templates/automation/`

| Template | Purpose | When to Use |
|----------|---------|-------------|
| **NEW_SPECIALIST.agent.md** | Agent profile template | Define new agent specialization |
| **PERSONA.md** | Agent persona definition | Describe agent personality and behavior |
| **framework-audit-report-template.md** | Framework audit report | Assess framework compliance |
| **framework-upgrade-plan-template.md** | Upgrade planning | Plan framework upgrades |
| **framework-manifest-template.yml** | Framework manifest | Define framework configuration |

**Usage Example:**
```bash
cp docs/templates/automation/NEW_SPECIALIST.agent.md .github/agents/optimizer.agent.md
```

---

## Template Usage Patterns

### Pattern 1: Simple Task Creation

**Scenario:** Create a straightforward task for an agent

**Steps:**
1. Copy `task-base.yaml` to `work/collaboration/inbox/`
2. Update required fields (id, agent, status, artifacts)
3. Commit and push

**Example:**
```bash
cp docs/templates/agent-tasks/task-base.yaml \
   work/collaboration/inbox/2025-11-27T1500-refactor-module.yaml
```

### Pattern 2: Work Log Documentation

**Scenario:** Document agent execution for framework improvement

**Steps:**
1. Copy `worklog.md` to `work/reports/logs/<agent-name>/`
2. Fill in all required sections
3. Include token metrics and primer checklist
4. Commit alongside task completion

**Example:**
```bash
cp docs/templates/agent-tasks/worklog.md \
   work/reports/logs/curator/2025-11-27T1500-refactor-validation.md
```

### Pattern 3: Assessment Report

**Scenario:** Evaluate artifact quality or system compliance

**Steps:**
1. Copy `assessment.md` to appropriate location
2. Define assessment scope and criteria
3. Document findings with severity indicators
4. Provide actionable recommendations

**Example:**
```bash
cp docs/templates/agent-tasks/assessment.md \
   work/reports/logs/curator/2025-11-27-security-assessment.md
```

### Pattern 4: Architecture Decision Record

**Scenario:** Document significant architectural decision

**Steps:**
1. Copy `adr.md` to `docs/architecture/decisions/`
2. Number sequentially (ADR-NNN)
3. Fill in context, decision, rationale, consequences
4. Link to related ADRs and requirements

**Example:**
```bash
cp docs/templates/architecture/adr.md \
   docs/architecture/decisions/ADR-016-caching-strategy.md
```

### Pattern 5: New Agent Profile

**Scenario:** Create a new specialized agent

**Steps:**
1. Copy `NEW_SPECIALIST.agent.md` to `.github/agents/`
2. Define specialization and capabilities
3. Set collaboration contract and mode defaults
4. Link to relevant directives

**Example:**
```bash
cp docs/templates/automation/NEW_SPECIALIST.agent.md \
   .github/agents/performance-optimizer.agent.md
```

---

## Template Customization Guidelines

### When to Extend Templates

**Extend templates when:**
- Adding project-specific sections
- Incorporating domain-specific requirements
- Enhancing with additional metadata

**Keep extensions minimal:**
- Add sections at the end (before metadata)
- Maintain existing section structure
- Document extensions in template comments

### When to Create New Templates

**Create new templates when:**
- Existing templates don't fit the use case
- A new artifact type emerges from repeated patterns
- Multiple agents need the same structure

**Template creation checklist:**
1. Check existing templates first
2. Document purpose and usage
3. Include required/optional sections clearly
4. Add example usage
5. Update this README
6. Reference in relevant directives

### Template Versioning

**Version control:**
- Templates are versioned with the repository
- Major structural changes require version bump
- Update Directive 006 (Version Governance) for breaking changes

**Deprecation:**
- Mark deprecated templates with **[DEPRECATED]** in filename
- Provide migration path in template header
- Maintain for 2 release cycles before removal

---

## Integration with Agent Framework

### Directive References

Templates are referenced in several directives:

- **Directive 008 (Artifact Templates):** Template location registry
- **Directive 014 (Work Log Creation):** Work log structure and requirements
- **Directive 018 (Traceable Decisions):** ADR usage patterns
- **Directive 004 (Documentation & Context Files):** Canonical document references

### Agent Profile Integration

Agents reference templates in their profiles:

**Example:**
```markdown
## Output Artifacts

When completing tasks, use templates from `docs/templates/`:
- Work logs: `agent-tasks/worklog.md`
- Assessments: `agent-tasks/assessment.md`
- ADRs: `architecture/adr.md`
```

### Task Orchestration

Templates support the file-based orchestration system:

1. **Task Creation:** Use `task-base.yaml` or `task-descriptor.yaml`
2. **Task Execution:** Reference templates in task context
3. **Task Completion:** Use `task-result.yaml` structure
4. **Work Logging:** Use `worklog.md` for documentation

---

## Sample Outputs

### Sample 1: Work Log

**Location:** `work/reports/logs/curator/2025-11-24T0522-poc3-final-validation-worklog.md`

**Key Features:**
- Complete context and approach documentation
- Detailed execution steps with findings
- Token metrics and primer checklist
- Lessons learned for framework improvement

**Use as reference:** This work log demonstrates best practices for documenting multi-agent chain completion.

### Sample 2: Assessment Report

**Location:** `work/reports/logs/curator/2025-11-24T0522-poc3-final-validation-report.md`

**Key Features:**
- Comprehensive four-pillar validation framework
- Detailed findings with severity indicators
- Evidence-based recommendations
- Production readiness evaluation

**Use as reference:** Demonstrates thorough assessment methodology and reporting.

### Sample 3: Benchmark Report

**Location:** `work/reports/benchmarks/orchestrator-performance-report.md`

**Key Features:**
- Executive summary with NFR compliance
- Detailed metrics with statistical analysis
- Trend analysis across scenarios
- Clear pass/fail indicators

**Use as reference:** Shows structured performance reporting.

### Sample 4: Architecture Decision Record

**Location:** `docs/architecture/decisions/ADR-009-orchestration-metrics.md`

**Key Features:**
- Clear context and decision statement
- Comprehensive rationale with trade-offs
- Envisioned consequences (positive and negative)
- Considered alternatives with rejection rationale

**Use as reference:** Exemplifies thorough architectural decision documentation.

### Sample 5: Synthesis Report

**Location:** `docs/architecture/synthesis/worklog-improvement-analysis.md`

**Key Features:**
- Cross-document pattern analysis
- Synthesized insights from multiple sources
- Actionable recommendations
- Integration with existing framework

**Use as reference:** Demonstrates multi-source synthesis approach.

---

## Template Maintenance

### Ownership

- **Primary Owner:** Curator Agent (structural consistency)
- **Reviewers:** Architect (architecture templates), Writer-Editor (clarity)
- **Approver:** Manager Agent (governance)

### Update Process

1. **Proposal:** Submit issue with template change rationale
2. **Review:** Curator validates structural consistency
3. **Approval:** Manager approves governance alignment
4. **Implementation:** Update template and this README
5. **Migration:** Update Directive 008 references
6. **Communication:** Notify in CHANGELOG.md

### Quality Standards

Templates MUST:
- Include clear purpose statement
- Define required vs optional sections
- Provide usage examples
- Use consistent markdown structure
- Include metadata section

Templates SHOULD:
- Include inline guidance (in comments or italics)
- Reference related templates
- Link to relevant directives
- Provide sample outputs

---

## Troubleshooting

### Common Issues

**Issue:** Template doesn't fit my use case  
**Solution:** Check if extending an existing template works; if not, propose a new template

**Issue:** Unsure which template to use  
**Solution:** Consult Template Categories section above; ask in issue comments

**Issue:** Template structure conflicts with directive  
**Solution:** Directive takes precedence; update template and report inconsistency

**Issue:** Template is outdated  
**Solution:** Submit issue with specific concerns; Curator will review and update

### Getting Help

- **Documentation Issues:** Tag @curator-claire in issues
- **Template Questions:** Comment on related tasks
- **New Template Proposals:** Use issue template (when available)
- **Urgent Concerns:** Tag @manager in task comments

---

## Metrics & Token Efficiency

### Template Benefits

**Token Reduction:**
- Reference template path (10-20 tokens) vs including full structure (500-1000 tokens)
- Estimated 80-95% reduction in instruction token overhead

**Consistency Gains:**
- Standardized structure reduces validation overhead
- Cross-document linking becomes reliable
- Agent handoffs are smoother

**Maintenance Efficiency:**
- Central updates propagate to all uses
- Version control simplifies change tracking
- Pattern evolution is documented

### Usage Metrics

Track template usage in work logs:
- Template referenced: `docs/templates/agent-tasks/worklog.md`
- Tokens saved: ~800 tokens
- Time saved: ~2-3 minutes per task

---

## Version History

### v1.0.0 (2025-11-27)
- Initial template library creation
- Core templates: ADR, work log, assessment, report
- Comprehensive README with usage patterns
- Integration with Directive 008

---

## Related Documentation

- **Directive 008:** [Artifact Templates](../../.github/agents/directives/008_artifact_templates.md)
- **Directive 014:** [Work Log Creation](../../.github/agents/directives/014_worklog_creation.md)
- **Directive 018:** [Traceable Decisions](../../.github/agents/directives/018_traceable_decisions.md)
- **AGENTS.md:** [Agent Specification](../../AGENTS.md)
- **GLOSSARY.md:** [Term Definitions](../../.github/agents/GLOSSARY.md)

---

## Contributing

To contribute new templates or improvements:

1. Review existing templates for patterns
2. Follow Template Customization Guidelines
3. Submit issue with proposal
4. Wait for Curator review
5. Implement approved changes
6. Update this README
7. Update relevant directives

**Template Quality Checklist:**
- [ ] Clear purpose statement
- [ ] Required/optional sections marked
- [ ] Usage example provided
- [ ] Sample output referenced
- [ ] Consistent with existing templates
- [ ] Documented in this README
- [ ] Referenced in Directive 008

---

**Maintained by:** Curator Claire  
**Contact:** Via task comments or GitHub issues  
**License:** Same as repository
