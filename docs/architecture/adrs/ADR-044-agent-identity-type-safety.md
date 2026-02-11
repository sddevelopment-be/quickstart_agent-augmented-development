# ADR-044: Agent Identity Type Safety

**Status:** ✅ Implemented (superseded by ADR-046 for location)  
**Date:** 2026-02-09  
**Implemented:** 2026-02-11  
**Superseded by:** ADR-046 (`AgentIdentity` moved to `src/domain/doctrine/types.py`)  
**Deciders:** Architect Alphonso  
**Related:** ADR-042 (Shared Task Domain Model), ADR-043 (Status Enumeration), ADR-046 (Domain Refactoring)

> **Note:** This ADR proposed `src/common/types.py`. The `AgentIdentity` type was subsequently moved to `src/domain/doctrine/types.py` per ADR-046 to align with doctrine domain.

---

## Context

### Problem

Agent identifiers are represented as strings throughout the codebase with no type safety or validation:

**Framework Orchestration:**
```python
# src/framework/orchestration/agent_base.py
class AgentBase(ABC):
    def __init__(self, agent_name: str, ...):
        self.agent_name = agent_name  # No validation

# Task assignment
task["agent"] = "python-pedro"  # Could be typo: "python_pedro"
```

**Dashboard Configuration:**
```python
# src/llm_service/config/schemas.py
class AgentConfig(BaseModel):
    # Agent name as string key in config
    preferred_tool: str
```

**Task Files:**
```yaml
# work/collaboration/inbox/task.yaml
agent: "python-pedro"  # No validation that agent exists
```

### Risks of Current State

1. **Typos Not Caught** - "python-pedro" vs "python_pedro" vs "pythonpedro"
2. **No Validation** - Can assign tasks to non-existent agents
3. **No IDE Support** - No autocomplete for agent names
4. **Late Failure** - Invalid agent names discovered at task execution time
5. **Inconsistency** - Different naming conventions across modules
6. **Maintenance** - Adding new agent requires manual updates everywhere

### Analysis Findings

From Python Pedro's src/ duplication analysis (2026-02-09):

**Severity:** MEDIUM (promoted to HIGH per requirements)

| Module | Agent Representation | Type Safety | Validation |
|--------|---------------------|-------------|------------|
| Framework | string in agent_name | ❌ None | Runtime discovery |
| Dashboard | string keys in config | ❌ None | Config loading |
| Tasks | YAML string field | ❌ None | Assignment time |

**Known Agent Names:**
- architect (Alphonso)
- backend-dev (Benny)
- python-pedro
- frontend (Freddy)
- devops-danny
- planning-petra
- manager-mike
- curator (Claire)
- writer-editor (Eddy)
- scribe (Sally)
- researcher (Ralph)
- ... ~20 total agents

**Risk Example:**
```python
# Typo in task assignment - fails at runtime
task["agent"] = "pythonpedro"  # Should be "python-pedro"

# Task sits unassigned because agent name doesn't match
# Error only discovered when checking inbox status
```

### Requirements

Per architectural review: "intervene NOW, avoid tech debt accumulation"

1. Type-safe agent identifier representation
2. Compile-time validation of agent names (mypy)
3. IDE autocomplete for valid agent names
4. Centralized registry of valid agents
5. Backward compatible with existing YAML files
6. Extensible for new agents

---

## Decision

We will add **AgentIdentity** type definition to `src/common/types.py` that provides type-safe agent identifiers with validation support.

### Implementation

**Extend:** `src/common/types.py`

```python
"""
Shared type definitions (continued from ADR-043)
"""

from typing import Literal, get_args
from enum import Enum


# Option 1: Literal Type (Recommended for Type Checking)
AgentIdentity = Literal[
    "architect",           # Architect Alphonso
    "backend-dev",         # Backend Benny  
    "python-pedro",        # Python Pedro
    "frontend",            # Frontend Freddy
    "devops-danny",        # DevOps Danny
    "planning-petra",      # Planning Petra
    "manager-mike",        # Manager Mike
    "curator",             # Curator Claire
    "writer-editor",       # Writer-Editor Eddy
    "scribe",              # Scribe Sally
    "researcher",          # Researcher Ralph
    "diagrammer",          # Diagrammer Diana
    "lexical",             # Lexical Larry
    "synthesizer",         # Synthesizer Sam
    "translator",          # Translator Tanya
    "bootstrap-bill",      # Bootstrap Bill
    "framework-guardian",  # Framework Guardian
    "java-jenny",          # Java Jenny
    "analyst-annie",       # Analyst Annie
    "code-reviewer",       # Code Reviewer Cindy
]


# Option 2: Enum (Alternative - More Features)
class Agent(str, Enum):
    """
    Valid agent identifiers in the system.
    
    Inherits from str to maintain YAML serialization compatibility.
    """
    
    ARCHITECT = "architect"
    BACKEND_DEV = "backend-dev"
    PYTHON_PEDRO = "python-pedro"
    FRONTEND = "frontend"
    DEVOPS_DANNY = "devops-danny"
    PLANNING_PETRA = "planning-petra"
    MANAGER_MIKE = "manager-mike"
    CURATOR = "curator"
    WRITER_EDITOR = "writer-editor"
    SCRIBE = "scribe"
    RESEARCHER = "researcher"
    DIAGRAMMER = "diagrammer"
    LEXICAL = "lexical"
    SYNTHESIZER = "synthesizer"
    TRANSLATOR = "translator"
    BOOTSTRAP_BILL = "bootstrap-bill"
    FRAMEWORK_GUARDIAN = "framework-guardian"
    JAVA_JENNY = "java-jenny"
    ANALYST_ANNIE = "analyst-annie"
    CODE_REVIEWER = "code-reviewer"
    
    @classmethod
    def is_valid(cls, agent_name: str) -> bool:
        """Check if agent name is valid."""
        return agent_name in cls._value2member_map_
    
    @classmethod
    def all_agents(cls) -> list[str]:
        """Get list of all valid agent names."""
        return [agent.value for agent in cls]


# Helper function for validation
def validate_agent(agent_name: str) -> bool:
    """
    Validate that agent name is recognized.
    
    Args:
        agent_name: Agent identifier to validate
        
    Returns:
        True if agent is valid, False otherwise
    """
    # Using Literal approach
    valid_agents = get_args(AgentIdentity)
    return agent_name in valid_agents
    
    # Or using Enum approach
    # return Agent.is_valid(agent_name)


def get_all_agents() -> list[str]:
    """
    Get list of all valid agent identifiers.
    
    Returns:
        List of agent name strings
    """
    return list(get_args(AgentIdentity))
```

### Design Decision: Literal vs Enum

**Recommendation:** Use **Literal** type for type checking, **optional Enum** for runtime features.

**Rationale:**

**Literal Advantages:**
- ✅ Better mypy integration
- ✅ Simpler syntax for type hints
- ✅ No runtime overhead
- ✅ Natural for type checking use cases

**Enum Advantages:**
- ✅ Helper methods (is_valid, all_agents)
- ✅ Namespace (Agent.PYTHON_PEDRO)
- ✅ Discoverable in IDE
- ✅ Iteration support

**Hybrid Approach:** Define both, use Literal for type hints, Enum for runtime validation.

### Migration Plan

**Phase 1: Define Types** (1 hour)
1. Add AgentIdentity and Agent to `src/common/types.py`
2. Add helper functions (validate_agent, get_all_agents)
3. Write tests:
   - Test all agent names valid
   - Test validation function
   - Test enum serialization
   - Test type checking with mypy

**Phase 2: Update Framework** (2 hours)
1. Update `src/framework/orchestration/agent_base.py`:
   ```python
   from src.common.types import AgentIdentity, validate_agent
   
   class AgentBase(ABC):
       def __init__(self, agent_name: AgentIdentity, ...):
           if not validate_agent(agent_name):
               raise ValueError(f"Unknown agent: {agent_name}")
           self.agent_name = agent_name
   ```
2. Update `src/framework/orchestration/agent_orchestrator.py`:
   ```python
   from src.common.types import AgentIdentity
   
   def assign_task(task: dict, agent: AgentIdentity) -> None:
       # Type checker validates agent
       task["agent"] = agent
   ```
3. Run framework tests

**Phase 3: Update Dashboard** (2 hours)
1. Update `src/llm_service/config/schemas.py`:
   ```python
   from src.common.types import AgentIdentity
   
   class AgentConfig(BaseModel):
       # Use validator to ensure agent name is valid
       agent_name: AgentIdentity
       preferred_tool: str
   ```
2. Update task linker to validate agent names
3. Run dashboard tests

**Phase 4: Add Task Validation** (1 hour)
1. Update `src/common/task_schema.py`:
   ```python
   from .types import validate_agent
   
   def read_task(path: Path) -> Dict[str, Any]:
       task = yaml.safe_load(...)
       
       # Validate agent if present
       if "agent" in task and not validate_agent(task["agent"]):
           logger.warning(f"Unknown agent '{task['agent']}' in {path}")
       
       return task
   ```
2. Optional: Add strict mode to reject invalid agents
3. Test with existing task files

**Phase 5: Documentation** (1 hour)
1. Update agent profile documentation
2. Add agent registry to README
3. Document how to add new agents
4. Update contribution guidelines

---

## Consequences

### Positive

1. ✅ **Type Safety** - mypy catches invalid agent names at compile time
2. ✅ **IDE Support** - Autocomplete for agent identifiers
3. ✅ **Early Validation** - Invalid agents caught before task execution
4. ✅ **Discoverability** - All valid agents in one place
5. ✅ **Refactoring Safety** - Renaming agent updates all type hints
6. ✅ **Documentation** - Agent registry serves as reference
7. ✅ **No Runtime Cost** - Literal types are compile-time only

### Negative

1. ⚠️ **Maintenance** - New agents must be added to types.py
2. ⚠️ **Verbosity** - Explicit type hints required (but good practice)
3. ⚠️ **Migration Effort** - Add type hints across codebase (7 hours)

### Neutral

1. 📊 **Backward Compatible** - Existing YAML files work unchanged
2. 📊 **Optional** - Can gradually adopt type hints
3. 📊 **Extensible** - Easy to add new agents to registry

---

## Alternatives Considered

### Alternative 1: Keep Strings ❌ REJECTED

**Rationale:** No type safety, violates "intervene NOW" requirement

### Alternative 2: Enum Only ❌ REJECTED

**Rationale:** Inferior mypy support compared to Literal

### Alternative 3: Dynamic Registry ❌ REJECTED

```python
# Load agents from configuration at runtime
VALID_AGENTS = set(load_agent_config().keys())
```

**Pros:** Automatically discovers agents  
**Cons:** No compile-time type checking, complex initialization

**Verdict:** REJECTED - Type safety is primary goal

### Alternative 4: Dataclass ❌ REJECTED

```python
@dataclass
class AgentIdentity:
    name: str
    display_name: str
    role: str
```

**Pros:** Rich metadata  
**Cons:** Over-engineering for identifier, high migration cost

**Verdict:** REJECTED - Simple string type is sufficient

---

## Implementation Status

- [ ] Add AgentIdentity to src/common/types.py
- [ ] Write validation tests
- [ ] Update framework/orchestration/ type hints
- [ ] Update llm_service/config/ type hints  
- [ ] Add task validation
- [ ] Update documentation
- [ ] Full test suite passing

**Assigned To:** Python Pedro  
**Estimated:** 7 hours  
**Priority:** MEDIUM (promoted to HIGH per requirements)

---

## Examples

### Before (String-Based)

```python
# Framework - No validation
class MyAgent(AgentBase):
    def __init__(self):
        super().__init__("my-agent", ...)  # Typo not caught

# Task assignment - No validation
task["agent"] = "pythonpedro"  # Typo not caught

# Dashboard config - No validation
config = {"pythonpedro": {"preferred_tool": "python"}}
```

**Problems:**
- Typos not caught until runtime
- No IDE autocomplete
- Invalid agents accepted

### After (Type-Safe)

```python
from src.common.types import AgentIdentity, validate_agent

# Framework - Type checked
class MyAgent(AgentBase):
    def __init__(self):
        # mypy error if "my-agent" not in AgentIdentity
        super().__init__("python-pedro", ...)

# Task assignment - Type checked
def assign_task(agent: AgentIdentity):
    task["agent"] = agent  # IDE autocomplete available

# Dashboard config - Validated
class AgentConfig(BaseModel):
    agent_name: AgentIdentity  # Pydantic validates

# Runtime validation
if validate_agent("python-pedro"):
    # Agent is valid
    pass
```

**Benefits:**
- Typos caught at compile time
- IDE autocomplete for agent names
- Early validation before execution

---

## Agent Registry

Current agents (as of 2026-02-09):

| Agent ID | Display Name | Primary Role |
|----------|--------------|--------------|
| architect | Architect Alphonso | Architecture & ADRs |
| backend-dev | Backend Benny | Backend development |
| python-pedro | Python Pedro | Python specialist |
| frontend | Frontend Freddy | UI/UX development |
| devops-danny | DevOps Danny | CI/CD & automation |
| planning-petra | Planning Petra | Planning & coordination |
| manager-mike | Manager Mike | Team coordination |
| curator | Curator Claire | Documentation curation |
| writer-editor | Writer-Editor Eddy | Content editing |
| scribe | Scribe Sally | Specification writing |
| researcher | Researcher Ralph | Research & analysis |
| diagrammer | Diagrammer Diana | Diagram generation |
| lexical | Lexical Larry | Style analysis |
| synthesizer | Synthesizer Sam | Multi-source synthesis |
| translator | Translator Tanya | Language translation |
| bootstrap-bill | Bootstrap Bill | Repository initialization |
| framework-guardian | Framework Guardian | Testing & quality |
| java-jenny | Java Jenny | Java development |
| analyst-annie | Analyst Annie | Requirements analysis |
| code-reviewer | Code Reviewer Cindy | Code review |

**Adding New Agents:**
1. Add to AgentIdentity Literal in src/common/types.py
2. Add to Agent enum (if using)
3. Create agent profile in doctrine/agents/
4. Update agent registry documentation

---

## References

- Python Pedro Analysis: `work/reports/analysis/2026-02-09-src-concept-duplication-inventory.md`
- Architectural Review: `work/reports/architecture/2026-02-09-src-consolidation-review.md`
- Related ADR-042: Shared Task Domain Model
- Related ADR-043: Status Enumeration Standard
- Python Literal Types: https://docs.python.org/3/library/typing.html#typing.Literal

---

**Decision:** ACCEPTED ✅  
**Date:** 2026-02-09  
**Architect:** Alphonso
