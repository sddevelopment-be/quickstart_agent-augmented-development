# Terminology Quick Reference - Code Reviewers

**Purpose:** Quick reference for terminology validation during code review  
**Source:** work/terminology-validation-report.md  
**Updated:** 2026-02-10

---

## 🚦 Quick Decision Tree

### When Reviewing Code, Ask:

1. **Does this introduce new domain concepts?**
   - ✅ YES → Check if term exists in glossary
   - ❌ NO → Proceed

2. **Is glossary term available?**
   - ✅ YES → Use glossary term consistently
   - ❌ NO → Add to glossary candidates list

3. **Is this a generic name (Manager/Handler/Processor)?**
   - ✅ YES → Check if domain-specific name would be clearer
   - ❌ NO → Proceed

---

## ✅ Well-Established Terms (Use Consistently)

| Term | Usage | Context |
|------|-------|---------|
| **Agent** | 87 files | Identity and orchestration |
| **Task** | Pervasive | Work unit in orchestration |
| **Orchestrator** | 6 files | Coordination component |
| **TaskStatus** | 8 files | Lifecycle state enum |
| **Specification** | 10 files | Requirements document |
| **Initiative** | 5 files | High-level project grouping |
| **Feature** | 19 files | Specific capability in spec |

---

## ⚠️ Inconsistent Terms (Standardize)

| What You'll See | Prefer | Notes |
|-----------------|--------|-------|
| task_file / file_path / YAML | **task_file** | Variable naming |
| Task File | **Task File** | Documentation |
| work dir / WORK_DIR / work/ | **work_dir** | Variable naming |
| Work Directory | **Work Directory** | Documentation |
| read_task / load / load_task | **read_task** | Function name (Pythonic) |
| write_task / save / persist | **write_task** | Function name (Pythonic) |

---

## ❌ Generic Anti-Patterns (Avoid or Justify)

### RED FLAGS in Domain Code

| Pattern | Problem | Better Alternative |
|---------|---------|-------------------|
| `*Manager` | Vague responsibility | `*Renderer`, `*Service`, `*Builder` |
| `*Handler` (non-event) | Confusing context | `*Service`, `*Processor`, `*Executor` |
| `*Wrapper` | Implementation detail | `*Executor`, `*Client`, domain name |
| `*Helper` / `*Utils` | Kitchen sink | Extract to domain-specific modules |

### GREEN FLAGS for Framework Code

| Pattern | Acceptable When | Example |
|---------|----------------|---------|
| `*Handler` | Event handler (watchdog, etc.) | `TaskFileHandler(FileSystemEventHandler)` |
| `*Adapter` | Adapter pattern implementation | `ClaudeCodeAdapter(ToolAdapter)` |
| `*Wrapper` | Thin technical wrapper | `SubprocessWrapper` (debatable) |

---

## 🆕 Missing from Glossary (Candidates)

### High Priority - Document These

| Term | Files | Definition | Context |
|------|-------|------------|---------|
| **TaskStatus** | 8 | Task lifecycle enum | Task Domain |
| **FeatureStatus** | 4 | Feature implementation enum | Task Domain |
| **TaskPriority** | 3 | Priority levels enum | Task Domain |
| **TaskMode** | 1 | Agent operating modes | Task Domain |
| **AgentIdentity** | 2 | Type-safe agent ID | Task Domain |
| **Configuration** | 15 | System settings | Infrastructure |
| **Template** | 12 | Jinja2 config generator | Infrastructure |
| **Dashboard** | 14 | Web UI for task mgmt | UI Domain |
| **Telemetry** | 8 | Structured logging | Observability |

---

## 📋 Code Review Checklist

### For New Classes

- [ ] Class name uses domain language (not generic suffix)?
- [ ] If generic suffix used, is it justified (framework convention)?
- [ ] Domain concepts documented in glossary?
- [ ] ADR exists for architectural decisions?

### For New Domain Terms

- [ ] Term defined in relevant glossary?
- [ ] Definition includes source (ADR, module, spec)?
- [ ] Related terms cross-referenced?
- [ ] Enforcement tier specified?

### For Terminology Changes

- [ ] Glossary updated to reflect code?
- [ ] OR code updated to reflect glossary?
- [ ] Rationale documented if diverging?
- [ ] Migration path specified if renaming?

---

## 🎯 Context-Specific Guidance

### Orchestration Context (`src/framework/orchestration/`)

**Strong alignment** - Use as reference for other modules

✅ **Do:**
- Use "Agent", "Task", "Orchestrator" consistently
- Reference TaskStatus enum for state checks
- Document file-based coordination patterns

⚠️ **Watch:**
- "Status" vs. "State" - code uses "Status", glossary says "State"
- "TaskDescriptor" not implemented (Dict[str, Any] used instead)
- Directory naming inconsistency (WORK_DIR / work_dir / work/)

---

### Dashboard Context (`src/llm_service/dashboard/`)

**Weak alignment** - Rich domain, missing glossary

✅ **Do:**
- Use Specification, Initiative, Feature consistently
- Document portfolio management concepts
- Create bounded context glossary

⚠️ **Watch:**
- Generic class names (TaskAssignmentHandler, SpecificationCache)
- Domain vocabulary not in any glossary
- Bounded context not explicitly documented

---

### Common Types (`src/common/types.py`)

**Good alignment potential** - Strong types, need glossary

✅ **Do:**
- Use enums (TaskStatus, FeatureStatus, TaskPriority, TaskMode)
- Validate agent IDs with AgentIdentity
- Reference state machine semantics

⚠️ **Watch:**
- Enums not in glossary (should be!)
- No ADR cross-references in glossary
- Type safety decisions undocumented

---

## 🔍 Review Comments Template

### Advisory Comment (Suggestion)

```markdown
ℹ️ **Terminology:** Consider using "Portfolio View" instead of "dashboard view" 
per Portfolio Domain glossary (when created). This aligns with domain language 
in `spec_parser.py`. (Advisory)
```

### Acknowledgment Required Comment

```markdown
⚠️ **Generic Naming:** `TaskManager` uses generic "Manager" suffix without 
clear domain context. Consider:
- `TaskOrchestrator` (if coordinating multiple tasks)
- `TaskExecutor` (if executing single task)
- `TaskRepository` (if managing persistence)

Please acknowledge if keeping current name. (Acknowledgment Required)

See: work/terminology-validation-report.md, Section 2.2
```

### Question Comment

```markdown
❓ **New Domain Concept?** This introduces "WorkflowStage" concept. Should we:
1. Add to glossary (if domain term)
2. Use existing "TaskStatus" (if lifecycle state)
3. Document distinction (if different concept)

cc: @architect-alphonso @curator-claire
```

---

## 📚 Key Resources

- **Full Report:** work/terminology-validation-report.md
- **Living Glossary Practice:** doctrine/approaches/living-glossary-practice.md
- **Glossaries:** .contextive/contexts/*.yml
- **Enforcement Tiers:** Advisory → Acknowledgment → Hard Failure

---

## 🎓 Enforcement Philosophy

**Start Permissive**

1. First PR with new term: **Advisory** comment
2. Second PR with same term: **Acknowledgment Required**
3. Third PR: Escalate to architect for glossary decision

**Goal:** Education over enforcement. Build shared understanding.

---

## 💡 Pro Tips

1. **Search before naming:** Check `src/common/types.py` for existing enums
2. **Prefer specific over generic:** "TemplateRenderer" > "TemplateManager"
3. **When in doubt, ask:** cc @curator-claire or @lexical-larry
4. **Framework conventions OK:** FileSystemEventHandler → *Handler is fine
5. **Document decisions:** "We chose X over Y because..." in ADR

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-10  
**Next Review:** After glossary additions approved

---

*"Good terminology is invisible - you only notice it when it's missing."*  
— Code-reviewer Cindy
