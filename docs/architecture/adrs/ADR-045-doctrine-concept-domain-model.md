# ADR-045: Doctrine Concept Domain Model

**status**: Accepted  
**date**: 2026-02-11  
**supersedes**: None  
**related**: ADR-046 (Module Refactoring), SPEC-TERM-001 (Terminology Alignment)

## Context

The quickstart agent-augmented development framework uses doctrine artifacts (directives, approaches, tactics, styleguides, templates, agent profiles) to govern agent behavior. Currently, these exist only as markdown files without runtime representations.

**Problems with current state:**
1. No programmatic introspection of doctrine stack
2. Cannot validate agent compliance automatically
3. No type-safe access to agent capabilities or directive requirements  
4. UI dashboard cannot display doctrine configuration
5. Vendor tool distribution requires manual file manipulation
6. Cannot query "which agents implement Directive 018?" or "what tactics apply to this context?"

**Strategic drivers:**
- **SPEC-DIST-001**: Vendor tool distribution requires structured domain model
- **SPEC-DASH-008**: Dashboard UI needs to inspect and display doctrine configuration
- **Language-first architecture**: Terminology alignment benefits from domain object modeling
- **Type safety**: Python type hints improve maintainability

## Decision

**We will create Python dataclasses representing core doctrine concepts as domain objects.**

**Core domain model:**

```python
@dataclass(frozen=True)
class AgentProfile:
    """Represents an agent's identity, specialization, and capabilities."""
    name: str
    slug: str  # filesystem-safe identifier
    role: AgentRole  # enum: strategic, operational, quality, coordination
    specialization: str
    capabilities: list[str]
    approaches_used: list[str]  # references to Approach slugs
    directives_followed: list[int]  # Directive numbers
    source_file: Path
    metadata: dict[str, Any]

@dataclass(frozen=True)
class Directive:
    """Represents an explicit instruction or constraint."""
    number: int
    title: str
    slug: str
    status: DirectiveStatus  # enum: active, deprecated, proposed
    enforcement: EnforcementTier  # enum: mandatory, recommended, advisory
    content: str
    related_tactics: list[str]  # Tactic slugs
    source_file: Path
    
@dataclass(frozen=True)
class Tactic:
    """Represents a procedural execution guide."""
    slug: str
    title: str
    steps: list[TacticStep]
    prerequisites: list[str]
    outcomes: list[str]
    source_file: Path

@dataclass(frozen=True)
class Approach:
    """Represents a mental model or philosophy."""
    slug: str
    title: str
    purpose: str
    principles: list[str]
    when_to_use: list[str]
    when_to_avoid: list[str]
    related_directives: list[int]
    source_file: Path

@dataclass(frozen=True)
class StyleGuide:
    """Represents code or documentation standards."""
    slug: str
    scope: StyleGuideScope  # enum: python, java, markdown, all
    rules: list[StyleRule]
    enforcement: EnforcementTier
    source_file: Path

@dataclass(frozen=True)
class Template:
    """Represents output structure contracts."""
    slug: str
    category: TemplateCategory  # enum: architecture, task, specification
    required_sections: list[str]
    optional_sections: list[str]
    source_file: Path
```

**Operational concepts:**

```python
@dataclass
class Batch:
    """Grouped tasks for coordinated execution."""
    id: str
    name: str
    tasks: list[TaskDescriptor]
    assigned_agent: Optional[str]
    status: BatchStatus
    created_at: datetime
    
@dataclass
class Iteration:
    """Planning cycle with phases."""
    id: str
    cycle_number: int
    start_date: datetime
    end_date: datetime
    phases: list[IterationPhase]
    batches: list[Batch]
    status: IterationStatus

@dataclass
class Cycle:
    """Recurring process with rhythm."""
    id: str
    rhythm: CycleRhythm  # enum: daily, weekly, monthly, quarterly
    phases: list[str]
    current_iteration: Optional[Iteration]
```

**Domain objects will:**
- Use `@dataclass(frozen=True)` for immutability
- Reference other concepts by slug/id (not direct references)
- Include `source_file: Path` for traceability
- Provide `from_file()` and `to_dict()` methods
- Validate at construction time

## Rationale

**Why dataclasses over alternatives:**

1. **Dataclasses vs. TypedDict**
   - Dataclasses provide runtime validation
   - Better IDE support and autocomplete
   - Can include methods (`from_file()`, `validate()`)
   - Trade-off: Slightly more boilerplate

2. **Dataclasses vs. Pydantic**
   - No external dependency (lightweight)
   - Sufficient for our needs (we control all inputs)
   - Pydantic adds 5MB + complexity
   - Trade-off: Less powerful validation

3. **Frozen vs. Mutable**
   - Immutable domain objects prevent accidental modification
   - Clearer boundaries between read and write operations
   - Aligns with functional programming principles
   - Trade-off: Updates require creating new instances

4. **Source file traceability**
   - Every domain object knows its markdown source
   - Enables bidirectional navigation (code ↔ files)
   - Supports "show me the source" UI features
   - Essential for debugging and verification

**Benefits:**

1. **Type Safety**: `mypy --strict` catches errors at development time
2. **Introspection**: Query capabilities programmatically (`agent.capabilities`, `directive.enforcement`)
3. **UI Integration**: Dashboard can render doctrine configuration without parsing markdown
4. **Vendor Export**: Transform to OpenCode/Cursor/Cody formats via ACL adapters
5. **Validation**: Detect broken references, missing files, invalid states
6. **Testing**: Create test fixtures easily (`AgentProfile(name="test-agent", ...)`)

**Implementation constraints:**

- Domain objects live in `src/domain/doctrine/` (not `doctrine/` framework)
- No circular dependencies with framework markdown
- Parsers in `src/framework/context/loaders/`
- Validation in `src/framework/context/validators/`

## Envisioned Consequences

### Positive

**Agility (+)**
- Faster feature development with type-safe domain model
- Easier to add new doctrine concepts (just add dataclass)
- UI dashboards can be built without custom parsing logic

**Maintainability (+)**
- Type hints reduce cognitive load
- IDE autocomplete improves developer experience  
- Validation catches errors early (broken references, missing files)

**Modularity (+)**
- Clean separation: markdown (framework) vs. runtime (domain)
- ACL adapters enable vendor tool distribution
- Domain objects can evolve independently of markdown format

**Extensibility (+)**
- Easy to add new attributes (`agent.priority`, `directive.examples`)
- Support new vendor formats by adding adapters
- Can add computed properties (`agent.is_operational`)

**Reusability (+)**
- Domain objects usable across CLI, dashboard, exporters
- Test fixtures reduce test code duplication
- Shared validation logic

**Security (=)**
- Neutral: Domain objects don't change security posture
- Validation can detect malicious inputs (but we control all sources)

**Evolvability (+)**
- Clear migration path: parse markdown → domain objects → persist if needed
- Can add caching layer without changing callers
- Future: Could generate markdown from domain objects (round-trip)

### Negative

**Complexity (+)**
- Additional abstraction layer (markdown → domain objects)
- Parsers add ~500 LOC
- Learning curve for new contributors

**Performance (-)**
- Parsing overhead at startup (~50ms for full doctrine stack)
- Mitigated by: lazy loading, caching
- Not a concern for CLI/dashboard use cases

**Maintenance Cost (+)**
- Must keep dataclasses in sync with markdown format
- Changes require updating parsers and validators
- Mitigated by: comprehensive tests, schema validation

## Considered Alternatives

### Alternative 1: Keep markdown-only, parse on-demand
**Rejected because:**
- No type safety or IDE support
- UI would require custom parsing in JavaScript/React
- Cannot validate references between artifacts
- Vendor export would be brittle string manipulation

### Alternative 2: Use Pydantic for validation
**Rejected because:**
- Adds external dependency (5MB, additional attack surface)
- Overkill for controlled inputs (we own all markdown files)
- Standard dataclasses sufficient for our needs
- Can revisit if validation needs grow

### Alternative 3: Generate code from YAML schemas
**Rejected because:**
- Additional build step complexity
- Harder to customize behavior (methods, computed properties)
- Python dataclasses are readable and maintainable as-is
- YAML schemas would need maintenance too

### Alternative 4: Store in database (SQLite, PostgreSQL)
**Rejected because:**
- Markdown-first principle: files are source of truth
- Database adds deployment complexity
- Git-based workflow would break
- Filesystem is database for doctrine artifacts

## Implementation Notes

**Phase 1: Core dataclasses** (Week 1, 16h)
- Define all dataclass structures in `src/domain/doctrine/models.py`
- Add enums (`AgentRole`, `DirectiveStatus`, `EnforcementTier`)
- Write unit tests for dataclass creation and validation

**Phase 2: Parsers** (Week 2, 20h)
- Implement `AgentProfileLoader`, `DirectiveLoader`, etc.
- Parse frontmatter (YAML) and markdown content
- Handle errors gracefully (missing files, malformed YAML)

**Phase 3: Validation** (Week 3, 16h)
- Validate cross-references (`agent.directives_followed` exist)
- Check file paths resolve correctly
- Detect circular dependencies

**Phase 4: Integration** (Week 4-5, 40h)
- Refactor existing code to use domain objects
- Update CLI commands (`kitty show agents`)
- Add domain objects to dashboard API

**Phase 5: ACL adapters** (Week 6, 20h)
- Implement `OpenCodeAdapter`, `CursorAdapter`
- Transform domain objects to vendor formats
- Test export/import round-trips

**Phase 6: Polish** (Week 7, 8h)
- Performance optimization (caching)
- Documentation and examples
- Migration guide for contributors

## References

- **Architectural Analysis**: `work/reports/architecture/architectural-analysis-doctrine-code-representations.md`
- **Related ADR**: ADR-046 (Module Refactoring)
- **Initiative**: SPEC-TERM-001 (Terminology Alignment Refactoring)
- **Approach**: Language-First Architecture (`doctrine/approaches/language-first-architecture.md`)
- **Directive**: 018 (Traceable Decisions)

## Approval

**Proposed**: 2026-02-11  
**Accepted**: 2026-02-11  
**Approvers**: @stijn-dejongh (Architect Alphonso analysis approved)
