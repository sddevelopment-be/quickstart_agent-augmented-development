"""
Doctrine domain validators.

Validators for checking cross-references, metadata completeness, circular
dependencies, and duplicate IDs in doctrine artifacts (agents, directives, etc.).

All validators are read-only and report errors/warnings without modifying domain
objects. Follows validation pattern: construct validator with data, call validate
methods, receive ValidationResult with errors/warnings.

Related ADRs
------------
- ADR-045: Doctrine Concept Domain Model

Design Principles
-----------------
1. Read-only: Never modify domain objects
2. Explicit results: Return ValidationResult with errors and warnings
3. Composable: Validators can be combined for complete validation
4. Performance: Efficient algorithms for large numbers of agents/directives
5. Type safety: Full type hints for mypy strict mode

Examples
--------
>>> from pathlib import Path
>>> from .models import Agent, Directive
>>> from .validators import CrossReferenceValidator
>>>
>>> directives = [
...     Directive(
...         id="001",
...         number=1,
...         title="Test Driven Development",
...         category="testing",
...         scope="all-agents",
...         enforcement="mandatory",
...         description="Apply TDD",
...         rationale="Improves quality",
...         examples=("RED-GREEN-REFACTOR",),
...         source_file=Path("directives/001.md"),
...         source_hash="hash001",
...     )
... ]
>>>
>>> agents = [
...     Agent(
...         id="python-pedro",
...         name="Python Pedro",
...         specialization="Python development",
...         capabilities=frozenset(["python"]),
...         required_directives=frozenset(["001"]),
...         primers=frozenset(["TDD"]),
...         source_file=Path("agents/pedro.md"),
...         source_hash="hash_pedro",
...     )
... ]
>>>
>>> validator = CrossReferenceValidator(directives, agents)
>>> result = validator.validate_all()
>>> assert result.valid is True
>>> assert len(result.errors) == 0
"""

from dataclasses import dataclass, field

from .models import Agent, Directive


@dataclass
class ValidationResult:
    """
    Result of validation check.

    Contains validation status, errors (failures), and warnings (non-critical issues).
    Immutable result object that can be inspected after validation.

    Attributes
    ----------
    valid : bool
        True if validation passed (no errors), False otherwise
    errors : List[str]
        List of error messages (validation failures)
    warnings : List[str]
        List of warning messages (non-critical issues)

    Examples
    --------
    >>> result = ValidationResult(valid=True, errors=[], warnings=["Minor issue"])
    >>> assert result.valid is True
    >>> assert result.has_warnings is True
    >>> assert result.has_errors is False
    """

    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        """Return True if validation has errors."""
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        """Return True if validation has warnings."""
        return len(self.warnings) > 0


class CrossReferenceValidator:
    """
    Validates cross-references between doctrine artifacts.

    Checks that agent required_directives reference existing directives,
    and generates warnings for deprecated directives.

    Attributes
    ----------
    directives : Dict[str, Directive]
        Dictionary of directives by ID for fast lookup
    agents : Dict[str, Agent]
        Dictionary of agents by ID for fast lookup

    Examples
    --------
    >>> validator = CrossReferenceValidator(directives, agents)
    >>> result = validator.validate_all()
    >>> if result.has_errors:
    ...     print("Validation errors:", result.errors)
    """

    def __init__(self, directives: list[Directive], agents: list[Agent]) -> None:
        """
        Initialize validator with loaded artifacts.

        Parameters
        ----------
        directives : List[Directive]
            List of all directives in the doctrine
        agents : List[Agent]
            List of all agents in the doctrine
        """
        self.directives: dict[str, Directive] = {d.id: d for d in directives}
        self.agents: dict[str, Agent] = {a.id: a for a in agents}

    def validate_agent_directives(self, agent: Agent) -> ValidationResult:
        """
        Validate that all required directives exist.

        Checks each directive ID in agent.required_directives exists in the
        directives dictionary. Generates errors for missing directives and
        warnings for deprecated directives.

        Parameters
        ----------
        agent : Agent
            Agent to validate

        Returns
        -------
        ValidationResult
            Result with errors for missing directives, warnings for deprecated
        """
        errors: list[str] = []
        warnings: list[str] = []

        for directive_id in agent.required_directives:
            if directive_id not in self.directives:
                errors.append(
                    f"Agent {agent.id} requires non-existent directive: {directive_id}"
                )
            elif self.directives[directive_id].status == "deprecated":
                warnings.append(
                    f"Agent {agent.id} requires deprecated directive: {directive_id}"
                )

        return ValidationResult(
            valid=(len(errors) == 0), errors=errors, warnings=warnings
        )

    def validate_all(self) -> ValidationResult:
        """
        Validate all cross-references.

        Validates all agents in the doctrine, accumulating errors and warnings
        from each agent validation.

        Returns
        -------
        ValidationResult
            Combined result with all errors and warnings
        """
        all_errors: list[str] = []
        all_warnings: list[str] = []

        for agent in self.agents.values():
            result = self.validate_agent_directives(agent)
            all_errors.extend(result.errors)
            all_warnings.extend(result.warnings)

        return ValidationResult(
            valid=(len(all_errors) == 0), errors=all_errors, warnings=all_warnings
        )


class MetadataValidator:
    """
    Validates metadata completeness and correctness.

    Checks that required fields are present and valid in agents and directives.
    Generates errors for missing required fields and warnings for invalid
    optional fields.

    Examples
    --------
    >>> validator = MetadataValidator()
    >>> result = validator.validate_agent(agent)
    >>> if not result.valid:
    ...     print("Metadata errors:", result.errors)
    """

    VALID_STATUSES: set[str] = {"active", "deprecated", "experimental"}

    def validate_agent(self, agent: Agent) -> ValidationResult:
        """
        Validate agent metadata.

        Checks required fields (id, name, specialization) are present and
        validates optional fields (status, version) if provided.

        Parameters
        ----------
        agent : Agent
            Agent to validate

        Returns
        -------
        ValidationResult
            Result with errors for missing required fields, warnings for
            invalid optional fields
        """
        errors: list[str] = []
        warnings: list[str] = []

        # Required fields
        if not agent.id:
            errors.append("Agent ID is required")
        if not agent.name:
            errors.append("Agent name is required")
        if not agent.specialization:
            errors.append("Agent specialization is required")

        # Status validation
        if agent.status not in self.VALID_STATUSES:
            errors.append(f"Invalid agent status: {agent.status}")

        # Version format (warning only)
        if not agent.version or not agent.version[0].isdigit():
            warnings.append(f"Agent {agent.id} has invalid version: {agent.version}")

        return ValidationResult(
            valid=(len(errors) == 0), errors=errors, warnings=warnings
        )


class IntegrityChecker:
    """
    Checks overall doctrine integrity.

    Validates that there are no duplicate IDs and no circular dependencies
    in agent handoff patterns.

    Examples
    --------
    >>> checker = IntegrityChecker()
    >>> result = checker.check_duplicate_ids(agents)
    >>> if result.has_errors:
    ...     print("Duplicate IDs found:", result.errors)
    """

    def check_duplicate_ids(self, agents: list[Agent]) -> ValidationResult:
        """
        Check for duplicate agent IDs.

        Scans all agents to ensure each ID is unique.

        Parameters
        ----------
        agents : List[Agent]
            List of agents to check

        Returns
        -------
        ValidationResult
            Result with errors for each duplicate ID found
        """
        seen_ids: set[str] = set()
        errors: list[str] = []

        for agent in agents:
            if agent.id in seen_ids:
                errors.append(f"Duplicate agent ID: {agent.id}")
            seen_ids.add(agent.id)

        return ValidationResult(valid=(len(errors) == 0), errors=errors, warnings=[])

    def check_circular_dependencies(self, agents: list[Agent]) -> ValidationResult:
        """
        Detect circular handoff dependencies.

        Builds a dependency graph from agent handoff patterns and detects
        cycles using depth-first search. A cycle means Agent A depends on B,
        B depends on C, and C depends on A (or any similar cycle).

        Parameters
        ----------
        agents : List[Agent]
            List of agents to check

        Returns
        -------
        ValidationResult
            Result with errors for each circular dependency found
        """
        # Build adjacency list from handoff patterns
        graph: dict[str, set[str]] = {}
        for agent in agents:
            graph[agent.id] = set()
            for pattern in agent.handoff_patterns:
                if pattern.direction == "to":
                    # This agent hands off to target agent
                    graph[agent.id].add(pattern.target_agent)

        # Detect cycles using DFS
        errors: list[str] = []
        visited: set[str] = set()
        rec_stack: set[str] = set()

        def has_cycle(node: str, path: list[str]) -> bool:
            """DFS helper to detect cycles."""
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            # Check all neighbors
            for neighbor in graph.get(node, set()):
                if neighbor not in visited:
                    if has_cycle(neighbor, path):
                        return True
                elif neighbor in rec_stack:
                    # Found a cycle
                    cycle_start = path.index(neighbor)
                    cycle_path = " → ".join(path[cycle_start:] + [neighbor])
                    errors.append(f"Circular dependency detected: {cycle_path}")
                    return True

            path.pop()
            rec_stack.remove(node)
            return False

        # Check for cycles starting from each unvisited node
        for agent_id in graph.keys():
            if agent_id not in visited:
                has_cycle(agent_id, [])

        return ValidationResult(valid=(len(errors) == 0), errors=errors, warnings=[])


__all__ = [
    "ValidationResult",
    "CrossReferenceValidator",
    "MetadataValidator",
    "IntegrityChecker",
]
