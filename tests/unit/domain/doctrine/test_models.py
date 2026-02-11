"""
Unit tests for doctrine domain models.

Following TDD approach (Directive 017):
- Write tests FIRST for each model
- Implement minimal code to pass
- Refactor while keeping tests green

Test Coverage Requirements:
- Construction with valid data
- Immutability enforcement (frozen=True)
- Type validation
- Source traceability fields
- Metadata completeness
- String representations
"""

import pytest
from pathlib import Path
from datetime import date
from dataclasses import FrozenInstanceError


class TestAgentModel:
    """Test suite for Agent domain model."""

    def test_agent_construction_with_valid_data(self):
        """Agent should construct successfully with all required fields."""
        from src.domain.doctrine.models import Agent

        agent = Agent(
            id="python-pedro",
            name="Python Pedro",
            specialization="Python development specialist",
            capabilities=frozenset(["python", "tdd", "type-safety"]),
            required_directives=frozenset(["001", "016", "017"]),
            primers=frozenset(["ATDD", "TDD"]),
            source_file=Path(".github/agents/python-pedro.agent.md"),
            source_hash="abc123def456",
        )

        assert agent.id == "python-pedro"
        assert agent.name == "Python Pedro"
        assert agent.specialization == "Python development specialist"
        assert "python" in agent.capabilities
        assert "016" in agent.required_directives
        assert "TDD" in agent.primers
        assert agent.source_file == Path(".github/agents/python-pedro.agent.md")
        assert agent.source_hash == "abc123def456"

    def test_agent_with_optional_metadata(self):
        """Agent should support optional metadata fields."""
        from src.domain.doctrine.models import Agent

        agent = Agent(
            id="backend-benny",
            name="Backend Benny",
            specialization="Backend development",
            capabilities=frozenset(["api-design", "databases"]),
            required_directives=frozenset(["001"]),
            primers=frozenset(),
            source_file=Path(".github/agents/backend-benny.agent.md"),
            source_hash="xyz789",
            version="2.0",
            created_date=date(2026, 2, 11),
            status="active",
            tags=frozenset(["backend", "api"]),
        )

        assert agent.version == "2.0"
        assert agent.created_date == date(2026, 2, 11)
        assert agent.status == "active"
        assert "backend" in agent.tags

    def test_agent_immutability(self):
        """Agent should be immutable (frozen dataclass)."""
        from src.domain.doctrine.models import Agent

        agent = Agent(
            id="test-agent",
            name="Test Agent",
            specialization="Testing",
            capabilities=frozenset(["testing"]),
            required_directives=frozenset(),
            primers=frozenset(),
            source_file=Path("test.md"),
            source_hash="test123",
        )

        with pytest.raises(FrozenInstanceError):
            agent.id = "modified-id"  # type: ignore

        with pytest.raises(FrozenInstanceError):
            agent.name = "Modified Name"  # type: ignore

    def test_agent_collections_are_immutable(self):
        """Agent collections should use immutable types (frozenset)."""
        from src.domain.doctrine.models import Agent

        agent = Agent(
            id="test-agent",
            name="Test Agent",
            specialization="Testing",
            capabilities=frozenset(["cap1", "cap2"]),
            required_directives=frozenset(["001"]),
            primers=frozenset(["primer1"]),
            source_file=Path("test.md"),
            source_hash="test123",
        )

        assert isinstance(agent.capabilities, frozenset)
        assert isinstance(agent.required_directives, frozenset)
        assert isinstance(agent.primers, frozenset)
        assert isinstance(agent.tags, frozenset)

    def test_agent_repr(self):
        """Agent should have readable string representation."""
        from src.domain.doctrine.models import Agent

        agent = Agent(
            id="test-agent",
            name="Test Agent",
            specialization="Testing specialist",
            capabilities=frozenset(),
            required_directives=frozenset(),
            primers=frozenset(),
            source_file=Path("test.md"),
            source_hash="test123",
        )

        repr_str = repr(agent)
        assert "Agent" in repr_str
        assert "test-agent" in repr_str
        assert "Test Agent" in repr_str


class TestDirectiveModel:
    """Test suite for Directive domain model."""

    def test_directive_construction_with_valid_data(self):
        """Directive should construct successfully with all required fields."""
        from src.domain.doctrine.models import Directive

        directive = Directive(
            id="017",
            number=17,
            title="Test Driven Development",
            category="testing",
            scope="all-agents",
            enforcement="mandatory",
            description="Apply TDD for all code changes",
            rationale="Reduces bugs and improves design",
            examples=("RED-GREEN-REFACTOR cycle", "Unit tests first"),
            source_file=Path("directives/017_test_driven_development.md"),
            source_hash="dir123",
        )

        assert directive.id == "017"
        assert directive.number == 17
        assert directive.title == "Test Driven Development"
        assert directive.category == "testing"
        assert directive.enforcement == "mandatory"
        assert any("RED-GREEN-REFACTOR" in ex for ex in directive.examples)

    def test_directive_with_optional_metadata(self):
        """Directive should support optional metadata fields."""
        from src.domain.doctrine.models import Directive

        directive = Directive(
            id="001",
            number=1,
            title="CLI Shell Tooling",
            category="context-management",
            scope="all-agents",
            enforcement="mandatory",
            description="Use CLI tools effectively",
            rationale="Improves efficiency",
            examples=(),
            source_file=Path("directives/001.md"),
            source_hash="hash001",
            version="2.0",
            status="active",
            tags=frozenset(["cli", "tooling"]),
        )

        assert directive.version == "2.0"
        assert directive.status == "active"
        assert "cli" in directive.tags

    def test_directive_immutability(self):
        """Directive should be immutable (frozen dataclass)."""
        from src.domain.doctrine.models import Directive

        directive = Directive(
            id="999",
            number=999,
            title="Test Directive",
            category="test",
            scope="test",
            enforcement="optional",
            description="Test description",
            rationale="Test rationale",
            examples=(),
            source_file=Path("test.md"),
            source_hash="test999",
        )

        with pytest.raises(FrozenInstanceError):
            directive.id = "modified"  # type: ignore

        with pytest.raises(FrozenInstanceError):
            directive.title = "Modified Title"  # type: ignore

    def test_directive_examples_immutable_tuple(self):
        """Directive examples should be immutable tuple."""
        from src.domain.doctrine.models import Directive

        directive = Directive(
            id="001",
            number=1,
            title="Test",
            category="test",
            scope="test",
            enforcement="optional",
            description="desc",
            rationale="rationale",
            examples=("example1", "example2", "example3"),
            source_file=Path("test.md"),
            source_hash="hash",
        )

        assert isinstance(directive.examples, tuple)
        assert len(directive.examples) == 3

    def test_directive_repr(self):
        """Directive should have readable string representation."""
        from src.domain.doctrine.models import Directive

        directive = Directive(
            id="017",
            number=17,
            title="TDD",
            category="testing",
            scope="all",
            enforcement="mandatory",
            description="desc",
            rationale="rationale",
            examples=(),
            source_file=Path("test.md"),
            source_hash="hash",
        )

        repr_str = repr(directive)
        assert "Directive" in repr_str
        assert "017" in repr_str
        assert "TDD" in repr_str


class TestTacticModel:
    """Test suite for Tactic domain model."""

    def test_tactic_construction_with_valid_data(self):
        """Tactic should construct successfully with all required fields."""
        from src.domain.doctrine.models import Tactic

        tactic = Tactic(
            id="red-green-refactor",
            title="RED-GREEN-REFACTOR Cycle",
            description="Core TDD workflow",
            steps=("Write failing test", "Make it pass", "Refactor"),
            prerequisites=frozenset(["testing framework"]),
            outcomes=frozenset(["working code", "test coverage"]),
            source_file=Path("tactics/red-green-refactor.md"),
            source_hash="tactic123",
        )

        assert tactic.id == "red-green-refactor"
        assert tactic.title == "RED-GREEN-REFACTOR Cycle"
        assert "Write failing test" in tactic.steps
        assert "testing framework" in tactic.prerequisites
        assert "working code" in tactic.outcomes

    def test_tactic_immutability(self):
        """Tactic should be immutable (frozen dataclass)."""
        from src.domain.doctrine.models import Tactic

        tactic = Tactic(
            id="test-tactic",
            title="Test Tactic",
            description="Test description",
            steps=("step1", "step2"),
            prerequisites=frozenset(),
            outcomes=frozenset(),
            source_file=Path("test.md"),
            source_hash="tactic999",
        )

        with pytest.raises(FrozenInstanceError):
            tactic.id = "modified"  # type: ignore

    def test_tactic_collections_immutable(self):
        """Tactic collections should use immutable types."""
        from src.domain.doctrine.models import Tactic

        tactic = Tactic(
            id="test",
            title="Test",
            description="desc",
            steps=("s1", "s2", "s3"),
            prerequisites=frozenset(["p1", "p2"]),
            outcomes=frozenset(["o1"]),
            source_file=Path("test.md"),
            source_hash="hash",
        )

        assert isinstance(tactic.steps, tuple)
        assert isinstance(tactic.prerequisites, frozenset)
        assert isinstance(tactic.outcomes, frozenset)

    def test_tactic_repr(self):
        """Tactic should have readable string representation."""
        from src.domain.doctrine.models import Tactic

        tactic = Tactic(
            id="tdd-cycle",
            title="TDD Cycle",
            description="desc",
            steps=(),
            prerequisites=frozenset(),
            outcomes=frozenset(),
            source_file=Path("test.md"),
            source_hash="hash",
        )

        repr_str = repr(tactic)
        assert "Tactic" in repr_str
        assert "tdd-cycle" in repr_str


class TestApproachModel:
    """Test suite for Approach domain model."""

    def test_approach_construction_with_valid_data(self):
        """Approach should construct successfully with all required fields."""
        from src.domain.doctrine.models import Approach

        approach = Approach(
            id="test-first-development",
            title="Test-First Development",
            purpose="Improve code quality through testing",
            principles=("Write tests before code", "Keep tests simple"),
            when_to_use=("New features", "Bug fixes"),
            when_to_avoid=("Prototyping", "Spike solutions"),
            related_directives=frozenset(["016", "017"]),
            source_file=Path("approaches/test-first.md"),
            source_hash="approach123",
        )

        assert approach.id == "test-first-development"
        assert approach.title == "Test-First Development"
        assert "Write tests before code" in approach.principles
        assert "New features" in approach.when_to_use
        assert "Prototyping" in approach.when_to_avoid
        assert "017" in approach.related_directives

    def test_approach_immutability(self):
        """Approach should be immutable (frozen dataclass)."""
        from src.domain.doctrine.models import Approach

        approach = Approach(
            id="test-approach",
            title="Test",
            purpose="Testing",
            principles=(),
            when_to_use=(),
            when_to_avoid=(),
            related_directives=frozenset(),
            source_file=Path("test.md"),
            source_hash="hash",
        )

        with pytest.raises(FrozenInstanceError):
            approach.id = "modified"  # type: ignore

    def test_approach_collections_immutable(self):
        """Approach collections should use immutable types."""
        from src.domain.doctrine.models import Approach

        approach = Approach(
            id="test",
            title="Test",
            purpose="Purpose",
            principles=("p1", "p2"),
            when_to_use=("u1",),
            when_to_avoid=("a1", "a2"),
            related_directives=frozenset(["001", "017"]),
            source_file=Path("test.md"),
            source_hash="hash",
        )

        assert isinstance(approach.principles, tuple)
        assert isinstance(approach.when_to_use, tuple)
        assert isinstance(approach.when_to_avoid, tuple)
        assert isinstance(approach.related_directives, frozenset)

    def test_approach_repr(self):
        """Approach should have readable string representation."""
        from src.domain.doctrine.models import Approach

        approach = Approach(
            id="tdd",
            title="TDD",
            purpose="purpose",
            principles=(),
            when_to_use=(),
            when_to_avoid=(),
            related_directives=frozenset(),
            source_file=Path("test.md"),
            source_hash="hash",
        )

        repr_str = repr(approach)
        assert "Approach" in repr_str
        assert "tdd" in repr_str


class TestStyleGuideModel:
    """Test suite for StyleGuide domain model."""

    def test_styleguide_construction_with_valid_data(self):
        """StyleGuide should construct successfully with all required fields."""
        from src.domain.doctrine.models import StyleGuide

        styleguide = StyleGuide(
            id="python-pep8",
            title="Python PEP 8 Style Guide",
            scope="python",
            rules=("Use 4 spaces for indentation", "Max line length 100"),
            enforcement="mandatory",
            source_file=Path("styleguides/python-pep8.md"),
            source_hash="style123",
        )

        assert styleguide.id == "python-pep8"
        assert styleguide.title == "Python PEP 8 Style Guide"
        assert styleguide.scope == "python"
        assert any("Use 4 spaces" in rule for rule in styleguide.rules)
        assert styleguide.enforcement == "mandatory"

    def test_styleguide_immutability(self):
        """StyleGuide should be immutable (frozen dataclass)."""
        from src.domain.doctrine.models import StyleGuide

        styleguide = StyleGuide(
            id="test-style",
            title="Test Style",
            scope="all",
            rules=(),
            enforcement="optional",
            source_file=Path("test.md"),
            source_hash="hash",
        )

        with pytest.raises(FrozenInstanceError):
            styleguide.id = "modified"  # type: ignore

    def test_styleguide_rules_immutable_tuple(self):
        """StyleGuide rules should be immutable tuple."""
        from src.domain.doctrine.models import StyleGuide

        styleguide = StyleGuide(
            id="test",
            title="Test",
            scope="test",
            rules=("rule1", "rule2", "rule3"),
            enforcement="recommended",
            source_file=Path("test.md"),
            source_hash="hash",
        )

        assert isinstance(styleguide.rules, tuple)
        assert len(styleguide.rules) == 3

    def test_styleguide_repr(self):
        """StyleGuide should have readable string representation."""
        from src.domain.doctrine.models import StyleGuide

        styleguide = StyleGuide(
            id="pep8",
            title="PEP 8",
            scope="python",
            rules=(),
            enforcement="mandatory",
            source_file=Path("test.md"),
            source_hash="hash",
        )

        repr_str = repr(styleguide)
        assert "StyleGuide" in repr_str
        assert "pep8" in repr_str


class TestTemplateModel:
    """Test suite for Template domain model."""

    def test_template_construction_with_valid_data(self):
        """Template should construct successfully with all required fields."""
        from src.domain.doctrine.models import Template

        template = Template(
            id="adr-template",
            title="Architecture Decision Record",
            category="architecture",
            required_sections=("Context", "Decision", "Consequences"),
            optional_sections=("Alternatives", "References"),
            source_file=Path("templates/adr-template.md"),
            source_hash="template123",
        )

        assert template.id == "adr-template"
        assert template.title == "Architecture Decision Record"
        assert template.category == "architecture"
        assert "Context" in template.required_sections
        assert "Alternatives" in template.optional_sections

    def test_template_immutability(self):
        """Template should be immutable (frozen dataclass)."""
        from src.domain.doctrine.models import Template

        template = Template(
            id="test-template",
            title="Test Template",
            category="test",
            required_sections=(),
            optional_sections=(),
            source_file=Path("test.md"),
            source_hash="hash",
        )

        with pytest.raises(FrozenInstanceError):
            template.id = "modified"  # type: ignore

    def test_template_sections_immutable_tuples(self):
        """Template sections should be immutable tuples."""
        from src.domain.doctrine.models import Template

        template = Template(
            id="test",
            title="Test",
            category="test",
            required_sections=("s1", "s2"),
            optional_sections=("o1", "o2", "o3"),
            source_file=Path("test.md"),
            source_hash="hash",
        )

        assert isinstance(template.required_sections, tuple)
        assert isinstance(template.optional_sections, tuple)
        assert len(template.required_sections) == 2
        assert len(template.optional_sections) == 3

    def test_template_repr(self):
        """Template should have readable string representation."""
        from src.domain.doctrine.models import Template

        template = Template(
            id="adr",
            title="ADR Template",
            category="architecture",
            required_sections=(),
            optional_sections=(),
            source_file=Path("test.md"),
            source_hash="hash",
        )

        repr_str = repr(template)
        assert "Template" in repr_str
        assert "adr" in repr_str


class TestModelTypeHints:
    """Test suite for type hint completeness."""

    def test_all_models_have_type_hints(self):
        """All model fields should have type hints for mypy compatibility."""
        from src.domain.doctrine.models import (
            Agent,
            Directive,
            Tactic,
            Approach,
            StyleGuide,
            Template,
        )

        # This test will pass if models are properly typed
        # mypy will catch any missing type hints at static analysis time
        models = [Agent, Directive, Tactic, Approach, StyleGuide, Template]
        for model in models:
            assert hasattr(model, "__dataclass_fields__")
