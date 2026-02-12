"""
Unit tests for doctrine validators.

Tests validation logic for cross-references, metadata completeness, circular
dependencies, and duplicate IDs. All tests follow TDD approach: tests written
first, then implementation.

Related ADRs
------------
- ADR-045: Doctrine Concept Domain Model

Test Coverage Requirements
---------------------------
- Cross-reference validation (valid and broken references)
- Metadata validation (complete and incomplete data)
- Circular dependency detection
- Duplicate ID detection
- Integration with domain models
"""

from pathlib import Path

from src.domain.doctrine.models import Agent, Directive
from src.domain.doctrine.validators import (
    CrossReferenceValidator,
    IntegrityChecker,
    MetadataValidator,
    ValidationResult,
)


class TestValidationResult:
    """Test ValidationResult data structure."""

    def test_validation_result_construction(self):
        """ValidationResult can be constructed with errors and warnings."""
        result = ValidationResult(
            valid=False,
            errors=["Error 1", "Error 2"],
            warnings=["Warning 1"],
        )

        assert result.valid is False
        assert len(result.errors) == 2
        assert len(result.warnings) == 1

    def test_validation_result_has_errors_property(self):
        """has_errors returns True when errors exist."""
        result = ValidationResult(valid=False, errors=["Error"], warnings=[])
        assert result.has_errors is True

        result_no_errors = ValidationResult(valid=True, errors=[], warnings=[])
        assert result_no_errors.has_errors is False

    def test_validation_result_has_warnings_property(self):
        """has_warnings returns True when warnings exist."""
        result = ValidationResult(valid=True, errors=[], warnings=["Warning"])
        assert result.has_warnings is True

        result_no_warnings = ValidationResult(valid=True, errors=[], warnings=[])
        assert result_no_warnings.has_warnings is False


class TestCrossReferenceValidator:
    """Test cross-reference validation between agents and directives."""

    def test_validator_initialization(self):
        """CrossReferenceValidator can be initialized with directives and agents."""
        directives = [
            Directive(
                id="001",
                number=1,
                title="CLI & Shell Tooling",
                category="tooling",
                scope="all-agents",
                enforcement="mandatory",
                description="Use CLI tools effectively",
                rationale="Improves efficiency",
                examples=("pytest", "ruff"),
                source_file=Path("directives/001.md"),
                source_hash="hash001",
            )
        ]
        agents = [
            Agent(
                id="python-pedro",
                name="Python Pedro",
                specialization="Python development",
                capabilities=frozenset(["python", "tdd"]),
                required_directives=frozenset(["001"]),
                primers=frozenset(["TDD"]),
                source_file=Path("agents/python-pedro.md"),
                source_hash="hash_pedro",
            )
        ]

        validator = CrossReferenceValidator(directives, agents)

        assert len(validator.directives) == 1
        assert len(validator.agents) == 1

    def test_validate_agent_directives_with_valid_references(self):
        """Validate agent with all valid directive references passes."""
        directives = [
            Directive(
                id="001",
                number=1,
                title="Test Directive",
                category="testing",
                scope="all-agents",
                enforcement="mandatory",
                description="Test description",
                rationale="Test rationale",
                examples=("example1",),
                source_file=Path("directives/001.md"),
                source_hash="hash001",
            ),
            Directive(
                id="016",
                number=16,
                title="ATDD",
                category="testing",
                scope="all-agents",
                enforcement="mandatory",
                description="ATDD description",
                rationale="ATDD rationale",
                examples=("example1",),
                source_file=Path("directives/016.md"),
                source_hash="hash016",
            ),
        ]

        agent = Agent(
            id="python-pedro",
            name="Python Pedro",
            specialization="Python development",
            capabilities=frozenset(["python"]),
            required_directives=frozenset(["001", "016"]),
            primers=frozenset(["TDD"]),
            source_file=Path("agents/python-pedro.md"),
            source_hash="hash_pedro",
        )

        validator = CrossReferenceValidator(directives, [agent])
        result = validator.validate_agent_directives(agent)

        assert result.valid is True
        assert len(result.errors) == 0
        assert len(result.warnings) == 0

    def test_validate_agent_directives_with_missing_directive(self):
        """Validate agent with missing directive reference fails."""
        directives = [
            Directive(
                id="001",
                number=1,
                title="Test Directive",
                category="testing",
                scope="all-agents",
                enforcement="mandatory",
                description="Test description",
                rationale="Test rationale",
                examples=("example1",),
                source_file=Path("directives/001.md"),
                source_hash="hash001",
            )
        ]

        agent = Agent(
            id="python-pedro",
            name="Python Pedro",
            specialization="Python development",
            capabilities=frozenset(["python"]),
            required_directives=frozenset(["001", "999"]),  # 999 doesn't exist
            primers=frozenset(["TDD"]),
            source_file=Path("agents/python-pedro.md"),
            source_hash="hash_pedro",
        )

        validator = CrossReferenceValidator(directives, [agent])
        result = validator.validate_agent_directives(agent)

        assert result.valid is False
        assert len(result.errors) == 1
        assert "999" in result.errors[0]
        assert "python-pedro" in result.errors[0]

    def test_validate_agent_directives_with_deprecated_directive_warning(self):
        """Validate agent using deprecated directive generates warning."""
        directives = [
            Directive(
                id="001",
                number=1,
                title="Deprecated Directive",
                category="testing",
                scope="all-agents",
                enforcement="mandatory",
                description="Test description",
                rationale="Test rationale",
                examples=("example1",),
                source_file=Path("directives/001.md"),
                source_hash="hash001",
                status="deprecated",  # Deprecated directive
            )
        ]

        agent = Agent(
            id="python-pedro",
            name="Python Pedro",
            specialization="Python development",
            capabilities=frozenset(["python"]),
            required_directives=frozenset(["001"]),
            primers=frozenset(["TDD"]),
            source_file=Path("agents/python-pedro.md"),
            source_hash="hash_pedro",
        )

        validator = CrossReferenceValidator(directives, [agent])
        result = validator.validate_agent_directives(agent)

        assert result.valid is True  # Still valid, just a warning
        assert len(result.errors) == 0
        assert len(result.warnings) == 1
        assert "deprecated" in result.warnings[0].lower()
        assert "001" in result.warnings[0]

    def test_validate_all_agents(self):
        """Validate all agents accumulates errors and warnings."""
        directives = [
            Directive(
                id="001",
                number=1,
                title="Test Directive",
                category="testing",
                scope="all-agents",
                enforcement="mandatory",
                description="Test description",
                rationale="Test rationale",
                examples=("example1",),
                source_file=Path("directives/001.md"),
                source_hash="hash001",
            )
        ]

        agent1 = Agent(
            id="agent1",
            name="Agent 1",
            specialization="Testing",
            capabilities=frozenset(["test"]),
            required_directives=frozenset(["001"]),  # Valid
            primers=frozenset([]),
            source_file=Path("agents/agent1.md"),
            source_hash="hash1",
        )

        agent2 = Agent(
            id="agent2",
            name="Agent 2",
            specialization="Testing",
            capabilities=frozenset(["test"]),
            required_directives=frozenset(["999"]),  # Invalid
            primers=frozenset([]),
            source_file=Path("agents/agent2.md"),
            source_hash="hash2",
        )

        validator = CrossReferenceValidator(directives, [agent1, agent2])
        result = validator.validate_all()

        assert result.valid is False
        assert len(result.errors) == 1
        assert "agent2" in result.errors[0]
        assert "999" in result.errors[0]

    def test_validate_all_with_no_errors(self):
        """Validate all agents with valid references passes."""
        directives = [
            Directive(
                id="001",
                number=1,
                title="Test Directive",
                category="testing",
                scope="all-agents",
                enforcement="mandatory",
                description="Test description",
                rationale="Test rationale",
                examples=("example1",),
                source_file=Path("directives/001.md"),
                source_hash="hash001",
            )
        ]

        agent1 = Agent(
            id="agent1",
            name="Agent 1",
            specialization="Testing",
            capabilities=frozenset(["test"]),
            required_directives=frozenset(["001"]),
            primers=frozenset([]),
            source_file=Path("agents/agent1.md"),
            source_hash="hash1",
        )

        agent2 = Agent(
            id="agent2",
            name="Agent 2",
            specialization="Testing",
            capabilities=frozenset(["test"]),
            required_directives=frozenset(["001"]),
            primers=frozenset([]),
            source_file=Path("agents/agent2.md"),
            source_hash="hash2",
        )

        validator = CrossReferenceValidator(directives, [agent1, agent2])
        result = validator.validate_all()

        assert result.valid is True
        assert len(result.errors) == 0


class TestMetadataValidator:
    """Test metadata completeness validation."""

    def test_validate_agent_with_complete_metadata(self):
        """Validate agent with all required fields passes."""
        agent = Agent(
            id="python-pedro",
            name="Python Pedro",
            specialization="Python development specialist",
            capabilities=frozenset(["python", "tdd"]),
            required_directives=frozenset(["001"]),
            primers=frozenset(["TDD"]),
            source_file=Path("agents/python-pedro.md"),
            source_hash="hash_pedro",
            version="1.0",
            status="active",
        )

        validator = MetadataValidator()
        result = validator.validate_agent(agent)

        assert result.valid is True
        assert len(result.errors) == 0

    def test_validate_agent_with_missing_id(self):
        """Validate agent with missing ID fails."""
        agent = Agent(
            id="",  # Empty ID
            name="Python Pedro",
            specialization="Python development specialist",
            capabilities=frozenset(["python", "tdd"]),
            required_directives=frozenset(["001"]),
            primers=frozenset(["TDD"]),
            source_file=Path("agents/python-pedro.md"),
            source_hash="hash_pedro",
        )

        validator = MetadataValidator()
        result = validator.validate_agent(agent)

        assert result.valid is False
        assert any("ID" in error for error in result.errors)

    def test_validate_agent_with_missing_name(self):
        """Validate agent with missing name fails."""
        agent = Agent(
            id="python-pedro",
            name="",  # Empty name
            specialization="Python development specialist",
            capabilities=frozenset(["python", "tdd"]),
            required_directives=frozenset(["001"]),
            primers=frozenset(["TDD"]),
            source_file=Path("agents/python-pedro.md"),
            source_hash="hash_pedro",
        )

        validator = MetadataValidator()
        result = validator.validate_agent(agent)

        assert result.valid is False
        assert any("name" in error.lower() for error in result.errors)

    def test_validate_agent_with_missing_specialization(self):
        """Validate agent with missing specialization fails."""
        agent = Agent(
            id="python-pedro",
            name="Python Pedro",
            specialization="",  # Empty specialization
            capabilities=frozenset(["python", "tdd"]),
            required_directives=frozenset(["001"]),
            primers=frozenset(["TDD"]),
            source_file=Path("agents/python-pedro.md"),
            source_hash="hash_pedro",
        )

        validator = MetadataValidator()
        result = validator.validate_agent(agent)

        assert result.valid is False
        assert any("specialization" in error.lower() for error in result.errors)

    def test_validate_agent_with_invalid_status(self):
        """Validate agent with invalid status fails."""
        agent = Agent(
            id="python-pedro",
            name="Python Pedro",
            specialization="Python development",
            capabilities=frozenset(["python"]),
            required_directives=frozenset(["001"]),
            primers=frozenset(["TDD"]),
            source_file=Path("agents/python-pedro.md"),
            source_hash="hash_pedro",
            status="invalid_status",  # Invalid status
        )

        validator = MetadataValidator()
        result = validator.validate_agent(agent)

        assert result.valid is False
        assert any("status" in error.lower() for error in result.errors)

    def test_validate_agent_with_invalid_version_generates_warning(self):
        """Validate agent with invalid version generates warning."""
        agent = Agent(
            id="python-pedro",
            name="Python Pedro",
            specialization="Python development",
            capabilities=frozenset(["python"]),
            required_directives=frozenset(["001"]),
            primers=frozenset(["TDD"]),
            source_file=Path("agents/python-pedro.md"),
            source_hash="hash_pedro",
            version="invalid",  # Invalid version format
        )

        validator = MetadataValidator()
        result = validator.validate_agent(agent)

        assert result.valid is True  # Warnings don't make it invalid
        assert len(result.warnings) == 1
        assert "version" in result.warnings[0].lower()


class TestIntegrityChecker:
    """Test overall doctrine integrity checks."""

    def test_check_duplicate_ids_with_unique_ids(self):
        """Check duplicate IDs with all unique IDs passes."""
        agents = [
            Agent(
                id="agent1",
                name="Agent 1",
                specialization="Testing",
                capabilities=frozenset(["test"]),
                required_directives=frozenset([]),
                primers=frozenset([]),
                source_file=Path("agents/agent1.md"),
                source_hash="hash1",
            ),
            Agent(
                id="agent2",
                name="Agent 2",
                specialization="Testing",
                capabilities=frozenset(["test"]),
                required_directives=frozenset([]),
                primers=frozenset([]),
                source_file=Path("agents/agent2.md"),
                source_hash="hash2",
            ),
        ]

        checker = IntegrityChecker()
        result = checker.check_duplicate_ids(agents)

        assert result.valid is True
        assert len(result.errors) == 0

    def test_check_duplicate_ids_with_duplicates(self):
        """Check duplicate IDs with duplicate agent IDs fails."""
        agents = [
            Agent(
                id="agent1",
                name="Agent 1",
                specialization="Testing",
                capabilities=frozenset(["test"]),
                required_directives=frozenset([]),
                primers=frozenset([]),
                source_file=Path("agents/agent1.md"),
                source_hash="hash1",
            ),
            Agent(
                id="agent1",  # Duplicate ID
                name="Agent 1 Copy",
                specialization="Testing",
                capabilities=frozenset(["test"]),
                required_directives=frozenset([]),
                primers=frozenset([]),
                source_file=Path("agents/agent1_copy.md"),
                source_hash="hash1_copy",
            ),
        ]

        checker = IntegrityChecker()
        result = checker.check_duplicate_ids(agents)

        assert result.valid is False
        assert len(result.errors) == 1
        assert "agent1" in result.errors[0].lower()
        assert "duplicate" in result.errors[0].lower()

    def test_check_circular_dependencies_with_no_cycles(self):
        """Check circular dependencies with no cycles passes."""
        # Agent graph: A → B → C (no cycles)
        agents = [
            Agent(
                id="agent_a",
                name="Agent A",
                specialization="Testing",
                capabilities=frozenset(["test"]),
                required_directives=frozenset([]),
                primers=frozenset([]),
                source_file=Path("agents/agent_a.md"),
                source_hash="hash_a",
                handoff_patterns=(
                    # HandoffPattern will be used by parser, but for testing we can use dict
                ),
            ),
            Agent(
                id="agent_b",
                name="Agent B",
                specialization="Testing",
                capabilities=frozenset(["test"]),
                required_directives=frozenset([]),
                primers=frozenset([]),
                source_file=Path("agents/agent_b.md"),
                source_hash="hash_b",
            ),
            Agent(
                id="agent_c",
                name="Agent C",
                specialization="Testing",
                capabilities=frozenset(["test"]),
                required_directives=frozenset([]),
                primers=frozenset([]),
                source_file=Path("agents/agent_c.md"),
                source_hash="hash_c",
            ),
        ]

        checker = IntegrityChecker()
        # Since we're testing circular dependencies via handoff patterns,
        # we'll need to build the graph from handoff_patterns
        result = checker.check_circular_dependencies(agents)

        assert result.valid is True
        assert len(result.errors) == 0

    def test_check_circular_dependencies_with_cycle(self):
        """Check circular dependencies with cycle fails."""
        from src.domain.doctrine.models import HandoffPattern

        # Agent graph: A → B → C → A (cycle)
        agents = [
            Agent(
                id="agent_a",
                name="Agent A",
                specialization="Testing",
                capabilities=frozenset(["test"]),
                required_directives=frozenset([]),
                primers=frozenset([]),
                source_file=Path("agents/agent_a.md"),
                source_hash="hash_a",
                handoff_patterns=(
                    HandoffPattern(
                        source_agent="agent_a",
                        target_agent="agent_b",
                        direction="to",
                        context="Handoff to B",
                    ),
                ),
            ),
            Agent(
                id="agent_b",
                name="Agent B",
                specialization="Testing",
                capabilities=frozenset(["test"]),
                required_directives=frozenset([]),
                primers=frozenset([]),
                source_file=Path("agents/agent_b.md"),
                source_hash="hash_b",
                handoff_patterns=(
                    HandoffPattern(
                        source_agent="agent_b",
                        target_agent="agent_c",
                        direction="to",
                        context="Handoff to C",
                    ),
                ),
            ),
            Agent(
                id="agent_c",
                name="Agent C",
                specialization="Testing",
                capabilities=frozenset(["test"]),
                required_directives=frozenset([]),
                primers=frozenset([]),
                source_file=Path("agents/agent_c.md"),
                source_hash="hash_c",
                handoff_patterns=(
                    HandoffPattern(
                        source_agent="agent_c",
                        target_agent="agent_a",  # Back to A - creates cycle
                        direction="to",
                        context="Handoff to A",
                    ),
                ),
            ),
        ]

        checker = IntegrityChecker()
        result = checker.check_circular_dependencies(agents)

        assert result.valid is False
        assert len(result.errors) > 0
        assert any("circular" in error.lower() for error in result.errors)


class TestValidationIntegration:
    """Integration tests for combined validation."""

    def test_complete_validation_pipeline(self):
        """Test complete validation workflow with all validators."""
        # Setup test data
        directives = [
            Directive(
                id="001",
                number=1,
                title="Test Directive",
                category="testing",
                scope="all-agents",
                enforcement="mandatory",
                description="Test description",
                rationale="Test rationale",
                examples=("example1",),
                source_file=Path("directives/001.md"),
                source_hash="hash001",
            )
        ]

        agents = [
            Agent(
                id="agent1",
                name="Agent 1",
                specialization="Testing agent",
                capabilities=frozenset(["test"]),
                required_directives=frozenset(["001"]),
                primers=frozenset([]),
                source_file=Path("agents/agent1.md"),
                source_hash="hash1",
            )
        ]

        # Run all validators
        cross_ref_validator = CrossReferenceValidator(directives, agents)
        metadata_validator = MetadataValidator()
        integrity_checker = IntegrityChecker()

        cross_ref_result = cross_ref_validator.validate_all()
        metadata_result = metadata_validator.validate_agent(agents[0])
        duplicate_result = integrity_checker.check_duplicate_ids(agents)
        circular_result = integrity_checker.check_circular_dependencies(agents)

        # All should pass
        assert cross_ref_result.valid is True
        assert metadata_result.valid is True
        assert duplicate_result.valid is True
        assert circular_result.valid is True
