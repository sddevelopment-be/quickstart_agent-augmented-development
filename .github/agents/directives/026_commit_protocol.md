<!-- The following information is to be interpreted literally -->

# 026 Commit Protocol

> **Purpose:** Standardized commit message format and workflow for agent-augmented development sessions

## 1. Commit Message Format

### Structure

```
<agent-slug>: task/epic description - specifics
```

### Agent Slug Selection

| Context | Agent Slug | Usage |
|---------|-----------|-------|
| General work | `general-purpose` | Refactoring, bug fixes, general improvements |
| Specialized role | Specialist name | Use specialist agent name when adopting specific role |

### Specialist Agent Slugs

- `architect` - Architectural decisions, ADRs, system design
- `backend-dev` - Backend services, APIs, integration work
- `bootstrap-bill` - Repository scaffolding, initialization
- `build-automation` - CI/CD, automation scripts, workflows
- `curator` - Directory structure, metadata, consistency
- `diagrammer` - Diagrams, visual documentation
- `framework-guardian` - Framework upgrades, dependency management
- `frontend` - UI components, frontend architecture
- `lexical` - Language style, tone analysis
- `manager` - Coordination, orchestration, planning
- `project-planner` - Project structure, roadmaps
- `researcher` - Research, investigation, analysis
- `scribe` - Documentation, technical writing
- `synthesizer` - Multi-source integration, synthesis
- `translator` - Translation, localization
- `writer-editor` - Content revision, editing

## 2. Commit Frequency

**Principle:** Small, atomic commits that preserve traceability.

**Trigger Points:**
- After creating a new file
- After completing a logical edit to existing file(s)
- Before switching contexts or roles
- After completing a discrete task step

**Anti-patterns:**
- ❌ Batching multiple unrelated changes
- ❌ Committing broken/incomplete state
- ❌ Vague messages ("fix stuff", "updates")

## 3. Examples

### Good Commits

```bash
general-purpose: refactor validation logic - extract helper functions
architect: document API decision - add ADR-023 for REST vs GraphQL
curator: normalize directory structure - align metadata in approaches/
scribe: update README - add installation section
bootstrap-bill: scaffold test directory - create pytest fixtures
build-automation: add CI validation - configure GitHub Actions workflow
```

### Poor Commits (Avoid)

```bash
# Too vague
general-purpose: updates

# Too broad (multiple unrelated changes)
architect: refactor everything - various improvements

# Missing specifics
curator: fix files
```

## 4. Workflow Integration

### Standard Flow

1. **Make change** (create/edit files)
2. **Commit immediately** with descriptive message
3. **Push at logical completion points** (feature complete, milestone reached)

### Trunk-Based Development

- Branch: Short-lived (<24 hours)
- Commits: Frequent, small, atomic
- Push: After logical groupings (3-5 related commits)
- Merge: Fast-forward when possible

## 5. Session Overrides

During specific sessions, project leads may authorize:

- **Push by exception** - Agent permitted to push directly
- **Modified format** - Alternative commit message structure
- **Batch commits** - Group related changes (document reason)

Always document session-specific rules in session notes or work logs.

## 6. Related Directives

- **020**: Locality of Change - Minimal scope principle
- **018**: Traceable Decisions - Decision documentation
- **019**: File-Based Collaboration - Multi-agent coordination

---

**Version:** 1.0.0  
**Status:** Active  
**Last Updated:** 2026-02-07
