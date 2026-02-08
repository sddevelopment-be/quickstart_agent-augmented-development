# Prompt Optimization Quick Reference

A one-page guide to writing efficient prompts for the agent-augmented development framework.

---

## ✅ Good Prompt Checklist

Before sending any task prompt, verify it includes:

- [ ] **Clear objective** (1-2 sentences, measurable goal)
- [ ] **Explicit deliverable list** (files to create/modify with paths)
- [ ] **Success criteria** (3-5 measurable checkboxes)
- [ ] **Constraints** (Do/Don't lists, time box)
- [ ] **Context files** (specific paths, not "load everything")
- [ ] **Directive references** (with file paths)
- [ ] **Priority/sequence** (if multiple steps)
- [ ] **Handoff instructions** (if multi-agent)

---

## ❌ Anti-Patterns to Avoid

### 1. Vague Action Verbs
**Bad:** "Assess the work"  
**Good:** "Create work log (Directive 014 Core tier) with production-readiness verdict (1 paragraph)"

### 2. Missing Deliverables
**Bad:** "Update documentation"  
**Good:** "Update: docs/HOW_TO_USE/orchestration.md (Section: Troubleshooting, add 3 new scenarios)"

### 3. Unclear Priorities
**Bad:** "Fix errors and implement features"  
**Good:** "Critical: Fix errors (20 min). High: Implement features (30 min). Medium: Update docs (15 min)."

### 4. Scope Creep Language
**Bad:** "Check all suggestions"  
**Good:** "Review critical Copilot suggestions only (4 specific items). Skip: Style/preference comments."

### 5. Missing File Paths
**Bad:** "Follow Directive 014"  
**Good:** "Follow Directive 014: .github/agents/directives/014_worklog_creation.md"

### 6. Heavy Context Loading
**Bad:** "Load repository context"  
**Good:** "Load: AGENTS.md, task YAML, Directive 014. Skip: Historical logs, examples."

### 7. No Success Criteria
**Bad:** "Create comprehensive guide"  
**Good:** "Guide: 300-500 lines, 8 sections minimum, 3 YAML examples, all code blocks validated."

### 8. Overloaded Prompts
**Bad:** Single prompt with 5+ distinct tasks  
**Good:** Split into 2-3 focused tasks with dependencies

---

## 📋 Prompt Template (Copy & Customize)

```yaml
# [Task Type]: [Brief Title]

## Objective
[Clear, measurable goal in 1-2 sentences]

## Deliverables
- [ ] File: [path/to/artifact]
      Type: [report/code/doc/diagram]
      Validation: [how to verify quality]
- [ ] Update: [existing/file]
      Section: [specific section]
      Change: [what to modify]

## Success Criteria
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]
- [ ] [Measurable criterion 3]

## Constraints
**Do:**
- [Explicit allowed action 1]
- [Explicit allowed action 2]

**Don't:**
- [Explicit prohibited action 1]
- [Explicit prohibited action 2]

**Time Box:** [duration] minutes

## Context Files (Load These)
1. [path/to/critical/file1]
2. [path/to/critical/file2]
3. [path/to/supporting/file3]

**Skip:** [categories to exclude]

## Compliance Requirements
- Directive [number]: [path/to/directive]
- ADR [number]: [path/to/adr]
- Mode: [/analysis-mode | /creative-mode | /meta-mode]

## Handoff (If Multi-Agent)
Next Agent: [agent-name]
Next Task: [title of follow-up task]
Context to Carry: [key information]
```

---

## 🎯 Examples: Before & After

### Example 1: Bug Fix Task

**❌ Before (Inefficient)**
```
Fix the validation errors. Make sure everything passes.
```
*Problems:* Vague scope, no success criteria, unclear deliverables

**✅ After (Optimized)**
```yaml
## Objective
Fix validation errors to make CI green.

## Deliverables
- [ ] Fixed: work/assigned/*/*.yaml (timestamp formats)
- [ ] Verified: All validation scripts exit code 0

## Success Criteria
- [ ] bash work/scripts/validate-work-structure.sh → exit 0
- [ ] python work/scripts/validate-task-schema.py → exit 0

## Constraints
Do: Surgical fixes only (minimal changes)
Don't: Refactor unrelated code
Time Box: 20 minutes

## Context Files
1. docs/templates/task-descriptor.yaml (schema reference)
```
*Improvement:* 40% faster (12 min vs 20 min), zero clarifications

---

### Example 2: Documentation Task

**❌ Before (Inefficient)**
```
Create a user guide for the orchestration system. Make it comprehensive.
```
*Problems:* No definition of "comprehensive", missing structure

**✅ After (Optimized)**
```yaml
## Objective
Create user-facing orchestration guide for new framework users.

## Deliverables
- [ ] File: docs/HOW_TO_USE/multi-agent-orchestration.md
      Type: User guide
      Validation: 300-500 lines, 8 sections, 3 examples

## Success Criteria
- [ ] Includes: Overview, Quick Start, Use Cases, Troubleshooting
- [ ] Contains: Minimum 3 YAML examples (simple, sequential, parallel)
- [ ] All code blocks syntax-checked
- [ ] Follows sibling guide style (QUICKSTART.md)

## Constraints
Do: Focus on practical "how-to" patterns
Don't: Duplicate technical architecture docs
Time Box: 45 minutes

## Context Files
1. work/README.md (technical overview)
2. docs/templates/task-descriptor.yaml (task schema)
3. docs/HOW_TO_USE/QUICKSTART.md (style reference)
Skip: Architecture deep-dives, historical logs
```
*Improvement:* 30% faster (31 min vs 45 min), consistent structure

---

### Example 3: Multi-Step Task

**❌ Before (Inefficient)**
```
Load context, fix validation, implement features, assess work, update status.
```
*Problems:* Overloaded, unclear priorities, no sequence

**✅ After (Optimized)**
```yaml
## Task 1: Fix Validation (20 min) - CRITICAL
Objective: Make CI green
Deliverables: Fixed task YAMLs
Success: All validation scripts pass

## Task 2: Implement Features (30 min) - HIGH
Depends On: Task 1
Objective: Address critical Copilot suggestions
Deliverables: 4 specific bug fixes
Success: No deprecation warnings, race condition fixed

## Task 3: Manager Assessment (15 min) - MEDIUM
Depends On: Tasks 1-2
Objective: Production readiness evaluation
Deliverables: Work log + status update
Success: Assessment complete, AGENT_STATUS.md updated
```
*Improvement:* 35% faster (42 min vs 65 min), clear progress tracking

---

## 📊 Token Efficiency Tips

### Context Loading Strategy
**Heavy (Avoid):** Load entire repository → 35K-48K input tokens  
**Efficient:** Load critical files only → 10K-15K input tokens (70% reduction)

**Template:**
```yaml
## Context Files (Load These)
**Critical (Always Load):**
- AGENTS.md
- [specific task directive]
- [task YAML file]

**Supporting (Load If Needed):**
- work/README.md
- [related ADR]

**Reference (Paths Only, Don't Load):**
- docs/architecture/design/
- work/logs/
```

### Output Optimization
**Verbose (Avoid):** 440-line work log for 10-minute task  
**Efficient:** Core tier (100-200 lines) for routine tasks

**Guideline:**
- Simple tasks (< 30 min): Core tier (100-200 lines)
- Complex tasks (30-120 min): Extended tier (200-500 lines)
- Novel/critical tasks: Comprehensive tier (500+ lines)

---

## 🚀 Impact Comparison

| Metric | Before Optimization | After Optimization | Improvement |
|--------|---------------------|-------------------|-------------|
| **Task Duration** | 37 min avg | 25 min avg | **32% faster** |
| **Clarifications** | 30% of prompts | <10% of prompts | **67% reduction** |
| **Rework Rate** | 15% tasks | <5% tasks | **67% reduction** |
| **Token Usage** | 40,300 avg | 28,000 avg | **30% reduction** |
| **Annual Time** | 740 hours | 500 hours | **240 hours saved** |

---

## 💡 Remember

1. **Specificity beats generality** - "Create X with Y criteria" > "Make it good"
2. **Lists beat prose** - Checkboxes > paragraphs
3. **Paths beat references** - "path/to/file" > "the directive"
4. **Constraints prevent scope creep** - "Don't refactor" > assuming restraint
5. **Time boxes prevent over-engineering** - "20 minutes" > "until perfect"

---

## 📚 Resources

- **Full Analysis:** work/reports/assessments/work-log-analysis-suboptimal-patterns.md
- **Executive Summary:** work/reports/exec_summaries/prompt-optimization-executive-summary.md
- **Directive 014:** .github/agents/directives/014_worklog_creation.md
- **Task Templates:** docs/templates/task-descriptor.yaml

---

**Version:** 1.0  
**Last Updated:** 2025-01-30  
**Maintained By:** Researcher Ralph  
**Feedback:** Create issue with label `prompt-optimization`
