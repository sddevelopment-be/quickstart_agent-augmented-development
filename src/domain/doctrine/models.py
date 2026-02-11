"""
Doctrine domain models.

Immutable dataclasses representing core doctrine concepts: agents, directives,
tactics, approaches, styleguides, and templates.

All models are frozen (immutable) and use immutable collection types (tuple, frozenset)
to prevent accidental modification. Type hints are provided for all fields to enable
static type checking with mypy.

Related ADRs
------------
- ADR-045: Doctrine Concept Domain Model
- ADR-046: Domain Module Refactoring

Design Principles
-----------------
1. Immutability: All dataclasses use @dataclass(frozen=True)
2. Type Safety: Complete type hints, mypy strict mode compatible
3. Source Traceability: Every model tracks its source file and hash
4. No Business Logic: Models are pure data structures
5. No External Dependencies: Keep models pure Python

Examples
--------
>>> from pathlib import Path
>>> from datetime import date
>>>
>>> agent = Agent(
...     id="python-pedro",
...     name="Python Pedro",
...     specialization="Python development specialist",
...     capabilities=frozenset(["python", "tdd", "type-safety"]),
...     required_directives=frozenset(["001", "016", "017"]),
...     primers=frozenset(["ATDD", "TDD"]),
...     source_file=Path(".github/agents/python-pedro.agent.md"),
...     source_hash="abc123def456",
... )
>>> assert agent.id == "python-pedro"
>>> assert "tdd" in agent.capabilities

>>> directive = Directive(
...     id="017",
...     number=17,
...     title="Test Driven Development",
...     category="testing",
...     scope="all-agents",
...     enforcement="mandatory",
...     description="Apply TDD for all code changes",
...     rationale="Reduces bugs and improves design",
...     examples=("RED-GREEN-REFACTOR cycle", "Unit tests first"),
...     source_file=Path("directives/017_test_driven_development.md"),
...     source_hash="dir123",
... )
>>> assert directive.number == 17
>>> assert "mandatory" == directive.enforcement
"""

from dataclasses import dataclass, field
from pathlib import Path
from datetime import date


@dataclass(frozen=True)
class Agent:
    """
    Agent profile domain model.

    Represents an AI agent with capabilities, constraints, and execution patterns.
    Immutable domain object with source traceability.

    Attributes
    ----------
    id : str
        Unique identifier for the agent (e.g., "python-pedro", "backend-benny")
    name : str
        Human-readable name (e.g., "Python Pedro", "Backend Benny")
    specialization : str
        Agent's area of expertise and focus
    capabilities : frozenset[str]
        Immutable set of agent capabilities (e.g., {"python", "tdd", "api-design"})
    required_directives : frozenset[str]
        Directive IDs this agent must follow (e.g., {"001", "016", "017"})
    primers : frozenset[str]
        Execution primers for this agent (e.g., {"ATDD", "TDD"})
    source_file : Path
        Path to source markdown file for traceability
    source_hash : str
        SHA-256 hash of source file for change detection
    version : str
        Version identifier, default "1.0"
    created_date : date | None
        Date agent profile was created
    status : str
        Profile status: "active", "deprecated", "experimental"
    tags : frozenset[str]
        Additional categorization tags

    Examples
    --------
    >>> agent = Agent(
    ...     id="backend-benny",
    ...     name="Backend Benny",
    ...     specialization="Backend development",
    ...     capabilities=frozenset(["api-design", "databases"]),
    ...     required_directives=frozenset(["001", "016"]),
    ...     primers=frozenset(["API-First"]),
    ...     source_file=Path(".github/agents/backend-benny.agent.md"),
    ...     source_hash="xyz789",
    ... )
    >>> assert "api-design" in agent.capabilities
    """

    id: str
    name: str
    specialization: str
    capabilities: frozenset[str]
    required_directives: frozenset[str]
    primers: frozenset[str]
    source_file: Path
    source_hash: str
    version: str = "1.0"
    created_date: date | None = None
    status: str = "active"
    tags: frozenset[str] = field(default_factory=frozenset)

    def __repr__(self) -> str:
        """Return readable string representation."""
        return f"Agent(id={self.id!r}, name={self.name!r}, specialization={self.specialization!r})"


@dataclass(frozen=True)
class Directive:
    """
    Directive domain model.

    Represents a mandatory framework rule or policy that governs agent behavior.

    Attributes
    ----------
    id : str
        Directive identifier (e.g., "001", "016", "017")
    number : int
        Numeric directive number for ordering
    title : str
        Directive title (e.g., "Test Driven Development")
    category : str
        Category grouping (e.g., "testing", "context-management")
    scope : str
        Applicability scope (e.g., "all-agents", "specialist-only")
    enforcement : str
        Enforcement level: "mandatory", "recommended", "optional"
    description : str
        Full description of the directive
    rationale : str
        Reasoning behind the directive
    examples : tuple[str, ...]
        Immutable sequence of usage examples
    source_file : Path
        Path to source markdown file
    source_hash : str
        SHA-256 hash of source file
    version : str
        Version identifier
    status : str
        Directive status: "active", "deprecated", "proposed"
    tags : frozenset[str]
        Additional categorization tags

    Examples
    --------
    >>> directive = Directive(
    ...     id="016",
    ...     number=16,
    ...     title="Acceptance Test Driven Development",
    ...     category="testing",
    ...     scope="all-agents",
    ...     enforcement="mandatory",
    ...     description="Define acceptance tests before implementation",
    ...     rationale="Ensures requirements are testable",
    ...     examples=("Gherkin scenarios", "Integration tests"),
    ...     source_file=Path("directives/016.md"),
    ...     source_hash="hash016",
    ... )
    >>> assert directive.number == 16
    """

    id: str
    number: int
    title: str
    category: str
    scope: str
    enforcement: str
    description: str
    rationale: str
    examples: tuple[str, ...]
    source_file: Path
    source_hash: str
    version: str = "1.0"
    status: str = "active"
    tags: frozenset[str] = field(default_factory=frozenset)

    def __repr__(self) -> str:
        """Return readable string representation."""
        return f"Directive(id={self.id!r}, title={self.title!r})"


@dataclass(frozen=True)
class Tactic:
    """
    Tactic domain model.

    Represents a specific execution pattern or procedural guide.

    Attributes
    ----------
    id : str
        Tactic identifier (e.g., "red-green-refactor", "atdd-cycle")
    title : str
        Tactic title
    description : str
        Full description of the tactic
    steps : tuple[str, ...]
        Immutable sequence of execution steps
    prerequisites : frozenset[str]
        Required conditions or tools
    outcomes : frozenset[str]
        Expected results from applying this tactic
    source_file : Path
        Path to source markdown file
    source_hash : str
        SHA-256 hash of source file
    version : str
        Version identifier
    status : str
        Tactic status: "active", "deprecated", "experimental"
    tags : frozenset[str]
        Additional categorization tags

    Examples
    --------
    >>> tactic = Tactic(
    ...     id="red-green-refactor",
    ...     title="RED-GREEN-REFACTOR Cycle",
    ...     description="Core TDD workflow",
    ...     steps=("Write failing test", "Make it pass", "Refactor"),
    ...     prerequisites=frozenset(["testing framework"]),
    ...     outcomes=frozenset(["working code", "test coverage"]),
    ...     source_file=Path("tactics/red-green-refactor.md"),
    ...     source_hash="tactic123",
    ... )
    >>> assert len(tactic.steps) == 3
    """

    id: str
    title: str
    description: str
    steps: tuple[str, ...]
    prerequisites: frozenset[str]
    outcomes: frozenset[str]
    source_file: Path
    source_hash: str
    version: str = "1.0"
    status: str = "active"
    tags: frozenset[str] = field(default_factory=frozenset)

    def __repr__(self) -> str:
        """Return readable string representation."""
        return f"Tactic(id={self.id!r}, title={self.title!r})"


@dataclass(frozen=True)
class Approach:
    """
    Approach domain model.

    Represents a recommended technique or mental model for problem-solving.

    Attributes
    ----------
    id : str
        Approach identifier (e.g., "test-first-development")
    title : str
        Approach title
    purpose : str
        Primary goal or purpose of this approach
    principles : tuple[str, ...]
        Core principles underlying this approach
    when_to_use : tuple[str, ...]
        Scenarios when this approach is recommended
    when_to_avoid : tuple[str, ...]
        Scenarios when this approach should not be used
    related_directives : frozenset[str]
        Directive IDs related to this approach
    source_file : Path
        Path to source markdown file
    source_hash : str
        SHA-256 hash of source file
    version : str
        Version identifier
    status : str
        Approach status: "active", "deprecated", "experimental"
    tags : frozenset[str]
        Additional categorization tags

    Examples
    --------
    >>> approach = Approach(
    ...     id="test-first-development",
    ...     title="Test-First Development",
    ...     purpose="Improve code quality through testing",
    ...     principles=("Write tests before code", "Keep tests simple"),
    ...     when_to_use=("New features", "Bug fixes"),
    ...     when_to_avoid=("Prototyping", "Spike solutions"),
    ...     related_directives=frozenset(["016", "017"]),
    ...     source_file=Path("approaches/test-first.md"),
    ...     source_hash="approach123",
    ... )
    >>> assert "017" in approach.related_directives
    """

    id: str
    title: str
    purpose: str
    principles: tuple[str, ...]
    when_to_use: tuple[str, ...]
    when_to_avoid: tuple[str, ...]
    related_directives: frozenset[str]
    source_file: Path
    source_hash: str
    version: str = "1.0"
    status: str = "active"
    tags: frozenset[str] = field(default_factory=frozenset)

    def __repr__(self) -> str:
        """Return readable string representation."""
        return f"Approach(id={self.id!r}, title={self.title!r})"


@dataclass(frozen=True)
class StyleGuide:
    """
    StyleGuide domain model.

    Represents coding or documentation standards.

    Attributes
    ----------
    id : str
        StyleGuide identifier (e.g., "python-pep8", "markdown-style")
    title : str
        StyleGuide title
    scope : str
        Applicability scope (e.g., "python", "markdown", "all")
    rules : tuple[str, ...]
        Immutable sequence of style rules
    enforcement : str
        Enforcement level: "mandatory", "recommended", "optional"
    source_file : Path
        Path to source markdown file
    source_hash : str
        SHA-256 hash of source file
    version : str
        Version identifier
    status : str
        StyleGuide status: "active", "deprecated", "draft"
    tags : frozenset[str]
        Additional categorization tags

    Examples
    --------
    >>> styleguide = StyleGuide(
    ...     id="python-pep8",
    ...     title="Python PEP 8 Style Guide",
    ...     scope="python",
    ...     rules=("Use 4 spaces for indentation", "Max line length 100"),
    ...     enforcement="mandatory",
    ...     source_file=Path("styleguides/python-pep8.md"),
    ...     source_hash="style123",
    ... )
    >>> assert styleguide.scope == "python"
    """

    id: str
    title: str
    scope: str
    rules: tuple[str, ...]
    enforcement: str
    source_file: Path
    source_hash: str
    version: str = "1.0"
    status: str = "active"
    tags: frozenset[str] = field(default_factory=frozenset)

    def __repr__(self) -> str:
        """Return readable string representation."""
        return f"StyleGuide(id={self.id!r}, title={self.title!r})"


@dataclass(frozen=True)
class Template:
    """
    Template domain model.

    Represents reusable structure patterns for common artifacts.

    Attributes
    ----------
    id : str
        Template identifier (e.g., "adr-template", "task-descriptor")
    title : str
        Template title
    category : str
        Template category (e.g., "architecture", "task", "specification")
    required_sections : tuple[str, ...]
        Mandatory sections that must be present
    optional_sections : tuple[str, ...]
        Optional sections that may be included
    source_file : Path
        Path to source markdown file
    source_hash : str
        SHA-256 hash of source file
    version : str
        Version identifier
    status : str
        Template status: "active", "deprecated", "draft"
    tags : frozenset[str]
        Additional categorization tags

    Examples
    --------
    >>> template = Template(
    ...     id="adr-template",
    ...     title="Architecture Decision Record",
    ...     category="architecture",
    ...     required_sections=("Context", "Decision", "Consequences"),
    ...     optional_sections=("Alternatives", "References"),
    ...     source_file=Path("templates/adr-template.md"),
    ...     source_hash="template123",
    ... )
    >>> assert "Context" in template.required_sections
    """

    id: str
    title: str
    category: str
    required_sections: tuple[str, ...]
    optional_sections: tuple[str, ...]
    source_file: Path
    source_hash: str
    version: str = "1.0"
    status: str = "active"
    tags: frozenset[str] = field(default_factory=frozenset)

    def __repr__(self) -> str:
        """Return readable string representation."""
        return f"Template(id={self.id!r}, title={self.title!r})"


__all__ = [
    "Agent",
    "Directive",
    "Tactic",
    "Approach",
    "StyleGuide",
    "Template",
]
