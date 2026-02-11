# ADR-046: Domain Module Refactoring (src/common → src/domain)

**status**: Accepted  
**date**: 2026-02-11  
**supersedes**: None  
**related**: ADR-045 (Domain Model), ADR-042 (Shared Task Domain Model)

## Context

The `src/common/` directory currently contains a mix of domain concepts, utilities, and type definitions without clear boundaries:

```
src/common/
├── __init__.py
├── agent_loader.py      # Agent profile loading
├── task_schema.py       # Task validation schemas
└── types.py             # TaskStatus, FeatureStatus, AgentIdentity
```

**Problems:**

1. **Unclear purpose**: "common" doesn't describe what's inside
2. **Mixed concerns**: Domain objects (Agent, Task) mixed with utilities
3. **Poor discoverability**: Hard to find where concepts live
4. **Conceptual drift**: As identified in conceptual alignment assessment
5. **No bounded contexts**: Everything in one flat directory
6. **Import ambiguity**: `from common.types import TaskStatus` - which domain?

**Related work:**
- **Conceptual Alignment Assessment** (2026-02-10) identified "task polysemy" - term "task" used across 3 contexts
- **ADR-042** proposed shared task domain model but didn't address module structure
- **ADR-045** defines doctrine concept domain model needing a home

## Decision

**We will refactor `src/common/` into `src/domain/` with bounded context modules:**

```
src/domain/
├── __init__.py
├── collaboration/           # Agent orchestration domain
│   ├── __init__.py
│   ├── agent.py            # AgentProfile, AgentIdentity
│   ├── task.py             # Task, TaskDescriptor, TaskStatus
│   ├── batch.py            # Batch, BatchStatus
│   ├── iteration.py        # Iteration, IterationPhase
│   └── orchestrator.py     # Orchestration concepts
│
├── doctrine/               # Doctrine artifact domain
│   ├── __init__.py
│   ├── models.py           # Directive, Approach, Tactic, StyleGuide
│   ├── agent_profile.py    # AgentProfile domain representation
│   └── loaders.py          # Parsers (may move to framework later)
│
├── specifications/         # Specification domain
│   ├── __init__.py
│   ├── specification.py    # Specification, Feature
│   ├── initiative.py       # Initiative, Epic
│   └── portfolio.py        # Portfolio view concepts
│
└── common/                 # Truly shared utilities ONLY
    ├── __init__.py
    ├── validation.py       # Generic validators
    └── parsing.py          # Generic parsers
```

**Migration strategy:**

1. **Create new structure** (`src/domain/`)
2. **Move files** to appropriate bounded contexts
3. **Update imports** across codebase
4. **Run tests** to validate
5. **Update documentation** (import paths, architecture diagrams)
6. **Remove old** `src/common/` directory

**Import path changes:**

```python
# Before
from src.common.types import TaskStatus, AgentIdentity
from src.common.agent_loader import load_agent_profile

# After
from src.domain.collaboration import TaskStatus, AgentIdentity
from src.domain.doctrine import AgentProfile
```

**Bounded context definitions:**

- **collaboration**: Agent orchestration, task management, batch execution
- **doctrine**: Doctrine artifact representations (directives, approaches, tactics)
- **specifications**: Feature specifications, initiatives, portfolio management
- **common**: Generic utilities with no domain semantics (validation, parsing)

## Rationale

**Why domain over common:**

1. **Clarity**: "domain" signals business concepts, not utilities
2. **DDD alignment**: Domain-Driven Design uses "domain" terminology
3. **Mental model**: Aligns with language-first architecture approach
4. **Industry standard**: Most codebases use `domain/` or `models/`

**Why bounded contexts:**

1. **Conceptual alignment**: Addresses "task polysemy" identified in assessment
2. **Locality of change**: Changes to collaboration don't affect specifications
3. **Import clarity**: `from domain.collaboration import Task` vs. `from common import Task`
4. **Team autonomy**: Different teams can own different contexts
5. **Future-proof**: Easy to extract contexts into separate packages

**Why keep common/**:**

1. **Avoid premature abstraction**: Generic utilities don't belong in domain
2. **Dependency direction**: `domain/` can depend on `common/`, not vice versa
3. **Clear signal**: If it's in `common/`, it's generic and reusable
4. **Migration path**: Move items to `common/` when patterns emerge

**Why collaboration instead of orchestration:**

1. **Human-centric**: Agents collaborate with humans
2. **Broader scope**: Includes coordination, delegation, handoffs (not just task execution)
3. **Matches glossary**: "Collaboration" is defined in new task-domain.yml
4. **Terminology alignment**: Reflects conceptual alignment assessment findings

## Envisioned Consequences

### Positive

**Maintainability (+++)**
- Clear module boundaries reduce cognitive load
- Easier to find where concepts live
- Changes isolated to specific domains
- New contributors onboard faster

**Modularity (+++)**
- Clean separation between domain concerns
- Can extract bounded contexts to separate packages
- Easier to test in isolation
- Reduced coupling between domains

**Agility (+)**
- Add new domain concepts without affecting others
- Refactor one domain without breaking others
- Parallel development by multiple teams

**Evolvability (++)**
- Clear migration path for future changes
- Can add new bounded contexts easily
- Domain concepts can evolve independently

**Reusability (+)**
- True shared utilities in `common/` are obviously reusable
- Domain objects can be shared across features
- Less duplication through clear boundaries

### Negative

**Complexity (+)**
- More directories to navigate
- Must decide which domain for new concepts
- Import paths are longer

**Migration Cost (--)**
- All imports must be updated (~150 files affected)
- Risk of breaking changes if not careful
- Requires comprehensive test coverage
- Estimated 16 hours for full migration

**Learning Curve (+)**
- New contributors must understand bounded contexts
- Team must agree on domain boundaries
- Requires documentation and onboarding updates

## Considered Alternatives

### Alternative 1: Keep src/common/, add subdirectories
```
src/common/
├── collaboration/
├── doctrine/
└── specifications/
```

**Rejected because:**
- "common" still signals "shared utilities" not "domain"
- Doesn't address conceptual alignment issues
- Less clear intention
- Import paths still ambiguous (`from common.collaboration`)

### Alternative 2: Single src/models/ directory
```
src/models/
├── agent.py
├── task.py
├── directive.py
```

**Rejected because:**
- Flat structure doesn't scale
- No bounded contexts
- Hard to navigate as concepts grow
- Doesn't address "task polysemy"

### Alternative 3: Separate packages (src/collaboration/, src/doctrine/)
```
src/
├── collaboration/
├── doctrine/
└── specifications/
```

**Rejected because:**
- Too granular for current codebase size
- Harder to share common utilities
- More boilerplate (`__init__.py`, `setup.py`)
- Can migrate to this later if needed

### Alternative 4: Keep src/common/, rename to src/domain later
**Rejected because:**
- "Do it later" rarely happens
- Migration is manageable now (~16 hours)
- Conceptual alignment issue persists
- Best to fix before more code depends on it

## Implementation Notes

**Phase 1: Create new structure** (2 hours)
- Create `src/domain/` directory
- Create bounded context subdirectories
- Add `__init__.py` files with proper exports
- Copy files to new locations (don't delete old yet)

**Phase 2: Update imports** (8 hours)
- Use automated refactoring tools (PyCharm, `rope`)
- Update all `from src.common` imports
- Run `mypy` and `pylint` to catch missed imports
- Fix any circular dependencies

**Phase 3: Run tests** (2 hours)
- Run full test suite
- Fix any broken tests
- Verify no import errors

**Phase 4: Update documentation** (2 hours)
- Update architecture diagrams
- Update import examples in README
- Update developer onboarding docs
- Add bounded context definitions

**Phase 5: Remove old** (1 hour)
- Delete `src/common/` directory
- Remove from `.gitignore` if needed
- Update CI/CD if paths are hardcoded

**Phase 6: Validation** (1 hour)
- Run all linters, tests, type checkers
- Verify dashboard still works
- Check CLI commands
- Manual smoke test

**Total effort:** 16 hours

**Rollback plan:**
1. Revert commit
2. Re-run tests to confirm working state
3. If needed, can keep both `src/common/` and `src/domain/` temporarily with deprecation warnings

## Migration Checklist

- [ ] Create `src/domain/` structure
- [ ] Create bounded context subdirectories
- [ ] Move `agent_loader.py` → `src/domain/doctrine/agent_profile.py`
- [ ] Move `types.py` → Split between `collaboration/` and `specifications/`
- [ ] Move `task_schema.py` → `src/domain/collaboration/task.py`
- [ ] Update imports in `src/framework/`
- [ ] Update imports in `tests/`
- [ ] Update imports in `tools/`
- [ ] Run test suite
- [ ] Update documentation
- [ ] Remove `src/common/`

## References

- **Conceptual Alignment Assessment**: `work/conceptual-alignment-assessment-synthesis.md` (Task polysemy issue)
- **Architectural Analysis**: `work/reports/architecture/architectural-analysis-doctrine-code-representations.md`
- **Related ADR**: ADR-045 (Doctrine Concept Domain Model)
- **Related ADR**: ADR-042 (Shared Task Domain Model)
- **Directive**: 018 (Traceable Decisions)
- **Directive**: 021 (Locality of Change)

## Approval

**Proposed**: 2026-02-11  
**Accepted**: 2026-02-11  
**Approvers**: @stijn-dejongh (mentioned in problem statement)

## Notes

This refactoring addresses the "side note" from @stijn-dejongh:
> "Side note: the current 'src/common' should probably be renamed to 'src/domain' and classes distributed to domain-specific modules (e.g. 'collaboration', 'doctrine', 'specifications')"

The refactoring will be coordinated with:
- Terminology Alignment Refactoring Initiative (SPEC-TERM-001)
- Glossary updates (task-domain.yml, portfolio-domain.yml)
- Language-first architecture approach
