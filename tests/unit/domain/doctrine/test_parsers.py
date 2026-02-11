"""
Test suite for doctrine parsers.

Tests all parser implementations (DirectiveParser, AgentParser, TacticParser, ApproachParser)
using TDD approach: tests written FIRST, then implementation.

Test Coverage Requirements (per ADR-045 Task 2):
- Valid file parsing (happy path)
- Invalid file handling (error cases)
- Missing fields (validation)
- Malformed YAML/Markdown
- File not found errors
- Source hash verification

Related ADRs
------------
- ADR-045: Doctrine Concept Domain Model

Directives Applied
------------------
- Directive 016: ATDD - Acceptance tests define success criteria
- Directive 017: TDD - Unit tests written first, RED-GREEN-REFACTOR
"""

import pytest
from pathlib import Path
from datetime import date

from src.domain.doctrine.parsers import (
    DirectiveParser,
    AgentParser,
    TacticParser,
    ApproachParser,
)
from src.domain.doctrine.models import Directive, Agent, Tactic, Approach
from src.domain.doctrine.exceptions import (
    ParseError,
    ValidationError,
    InvalidDirectiveId,
    MissingRequiredField,
)


# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def fixtures_dir() -> Path:
    """Return path to test fixtures directory."""
    # Path from tests/unit/domain/doctrine/test_parsers.py to tests/fixtures/doctrine/
    return Path(__file__).parent.parent.parent.parent / "fixtures" / "doctrine"


@pytest.fixture
def valid_directive_file(fixtures_dir: Path) -> Path:
    """Return path to valid directive fixture."""
    return fixtures_dir / "directives" / "017_test_driven_development.md"


@pytest.fixture
def valid_agent_file(fixtures_dir: Path) -> Path:
    """Return path to valid agent fixture."""
    return fixtures_dir / "agents" / "test-agent.agent.md"


@pytest.fixture
def valid_tactic_file(fixtures_dir: Path) -> Path:
    """Return path to valid tactic fixture."""
    return fixtures_dir / "tactics" / "red-green-refactor.tactic.md"


@pytest.fixture
def valid_approach_file(fixtures_dir: Path) -> Path:
    """Return path to valid approach fixture."""
    return fixtures_dir / "approaches" / "test-first-development.md"


@pytest.fixture
def invalid_no_frontmatter_file(fixtures_dir: Path) -> Path:
    """Return path to invalid directive (no frontmatter)."""
    return fixtures_dir / "directives" / "invalid_no_frontmatter.md"


@pytest.fixture
def invalid_yaml_syntax_file(fixtures_dir: Path) -> Path:
    """Return path to invalid directive (malformed YAML)."""
    return fixtures_dir / "directives" / "invalid_yaml_syntax.md"


@pytest.fixture
def invalid_missing_fields_file(fixtures_dir: Path) -> Path:
    """Return path to invalid agent (missing required fields)."""
    return fixtures_dir / "agents" / "invalid-missing-fields.agent.md"


# ============================================================================
# DirectiveParser Tests
# ============================================================================


class TestDirectiveParser:
    """Test suite for DirectiveParser (TDD approach)."""

    def test_parse_valid_directive_returns_directive_object(
        self, valid_directive_file: Path
    ):
        """Parser should parse valid directive file into Directive domain object."""
        parser = DirectiveParser()
        directive = parser.parse(valid_directive_file)

        # Verify it's a Directive instance
        assert isinstance(directive, Directive)

    def test_parse_valid_directive_extracts_id_from_filename(
        self, valid_directive_file: Path
    ):
        """Parser should extract directive ID from filename (e.g., '017')."""
        parser = DirectiveParser()
        directive = parser.parse(valid_directive_file)

        assert directive.id == "017"
        assert directive.number == 17

    def test_parse_valid_directive_extracts_title_from_content(
        self, valid_directive_file: Path
    ):
        """Parser should extract title from markdown heading."""
        parser = DirectiveParser()
        directive = parser.parse(valid_directive_file)

        assert "Test Driven Development" in directive.title

    def test_parse_valid_directive_extracts_category_from_frontmatter(
        self, valid_directive_file: Path
    ):
        """Parser should extract category from YAML frontmatter."""
        parser = DirectiveParser()
        directive = parser.parse(valid_directive_file)

        assert directive.category == "testing"

    def test_parse_valid_directive_extracts_scope(self, valid_directive_file: Path):
        """Parser should extract scope from frontmatter."""
        parser = DirectiveParser()
        directive = parser.parse(valid_directive_file)

        assert directive.scope == "all-agents"

    def test_parse_valid_directive_extracts_enforcement(
        self, valid_directive_file: Path
    ):
        """Parser should extract enforcement level from frontmatter."""
        parser = DirectiveParser()
        directive = parser.parse(valid_directive_file)

        assert directive.enforcement == "mandatory"

    def test_parse_valid_directive_extracts_description_section(
        self, valid_directive_file: Path
    ):
        """Parser should extract description from ## Description section."""
        parser = DirectiveParser()
        directive = parser.parse(valid_directive_file)

        assert "TDD" in directive.description or "Test Driven" in directive.description
        assert len(directive.description) > 0

    def test_parse_valid_directive_extracts_rationale_section(
        self, valid_directive_file: Path
    ):
        """Parser should extract rationale from ## Rationale section."""
        parser = DirectiveParser()
        directive = parser.parse(valid_directive_file)

        assert len(directive.rationale) > 0
        assert "reduce" in directive.rationale.lower() or "bug" in directive.rationale.lower()

    def test_parse_valid_directive_extracts_examples(self, valid_directive_file: Path):
        """Parser should extract examples from ## Examples section."""
        parser = DirectiveParser()
        directive = parser.parse(valid_directive_file)

        assert isinstance(directive.examples, tuple)
        assert len(directive.examples) > 0

    def test_parse_valid_directive_extracts_tags_from_frontmatter(
        self, valid_directive_file: Path
    ):
        """Parser should extract tags as frozenset from frontmatter."""
        parser = DirectiveParser()
        directive = parser.parse(valid_directive_file)

        assert isinstance(directive.tags, frozenset)
        assert "testing" in directive.tags or "tdd" in directive.tags

    def test_parse_valid_directive_calculates_source_hash(
        self, valid_directive_file: Path
    ):
        """Parser should calculate SHA-256 hash of source file."""
        parser = DirectiveParser()
        directive = parser.parse(valid_directive_file)

        # SHA-256 hash is 64 character hex string
        assert len(directive.source_hash) == 64
        assert all(c in "0123456789abcdef" for c in directive.source_hash)

    def test_parse_valid_directive_sets_source_file_path(
        self, valid_directive_file: Path
    ):
        """Parser should set source_file to original file path."""
        parser = DirectiveParser()
        directive = parser.parse(valid_directive_file)

        assert directive.source_file == valid_directive_file

    def test_parse_valid_directive_sets_version_from_frontmatter(
        self, valid_directive_file: Path
    ):
        """Parser should extract version from frontmatter."""
        parser = DirectiveParser()
        directive = parser.parse(valid_directive_file)

        assert directive.version == "1.0"

    def test_parse_valid_directive_sets_status_from_frontmatter(
        self, valid_directive_file: Path
    ):
        """Parser should extract status from frontmatter."""
        parser = DirectiveParser()
        directive = parser.parse(valid_directive_file)

        assert directive.status == "active"

    def test_parse_missing_file_raises_parse_error(self, tmp_path: Path):
        """Parser should raise ParseError when file does not exist."""
        parser = DirectiveParser()
        nonexistent_file = tmp_path / "nonexistent.md"

        with pytest.raises(ParseError) as exc_info:
            parser.parse(nonexistent_file)

        assert "not found" in str(exc_info.value).lower() or "does not exist" in str(
            exc_info.value
        ).lower()

    def test_parse_invalid_yaml_raises_parse_error(
        self, invalid_yaml_syntax_file: Path
    ):
        """Parser should raise ParseError for malformed YAML."""
        parser = DirectiveParser()

        with pytest.raises(ParseError) as exc_info:
            parser.parse(invalid_yaml_syntax_file)

        assert "yaml" in str(exc_info.value).lower() or "syntax" in str(
            exc_info.value
        ).lower()

    def test_parse_missing_frontmatter_uses_defaults(
        self, invalid_no_frontmatter_file: Path
    ):
        """Parser should handle missing frontmatter gracefully with defaults."""
        parser = DirectiveParser()

        # This might raise ValidationError or use defaults depending on implementation
        # Either is acceptable - testing the behavior
        try:
            directive = parser.parse(invalid_no_frontmatter_file)
            # If it succeeds, should have default values
            assert directive.category in ["uncategorized", "general", ""]
        except ValidationError:
            # Also acceptable to fail validation
            pass

    def test_parse_invalid_directive_id_raises_validation_error(self, tmp_path: Path):
        """Parser should raise ValidationError for invalid directive ID in filename."""
        parser = DirectiveParser()
        
        # Create file with invalid directive ID
        invalid_file = tmp_path / "abc_invalid_id.md"
        invalid_file.write_text("""---
category: test
scope: all-agents
enforcement: mandatory
---

# Directive ABC: Invalid
""")

        with pytest.raises((ValidationError, InvalidDirectiveId)):
            parser.parse(invalid_file)

    def test_parse_directive_immutability(self, valid_directive_file: Path):
        """Parsed Directive should be immutable (frozen dataclass)."""
        parser = DirectiveParser()
        directive = parser.parse(valid_directive_file)

        # Attempting to modify should raise error
        with pytest.raises((AttributeError, TypeError)):
            directive.title = "Modified"  # type: ignore


# ============================================================================
# AgentParser Tests
# ============================================================================


class TestAgentParser:
    """Test suite for AgentParser (TDD approach)."""

    def test_parse_valid_agent_returns_agent_object(self, valid_agent_file: Path):
        """Parser should parse valid agent file into Agent domain object."""
        parser = AgentParser()
        agent = parser.parse(valid_agent_file)

        assert isinstance(agent, Agent)

    def test_parse_valid_agent_extracts_id_from_frontmatter(
        self, valid_agent_file: Path
    ):
        """Parser should extract agent ID from frontmatter 'name' field."""
        parser = AgentParser()
        agent = parser.parse(valid_agent_file)

        assert agent.id == "test-agent"

    def test_parse_valid_agent_extracts_name_from_heading(self, valid_agent_file: Path):
        """Parser should extract agent name from markdown heading."""
        parser = AgentParser()
        agent = parser.parse(valid_agent_file)

        assert "Test Agent" in agent.name

    def test_parse_valid_agent_extracts_specialization(self, valid_agent_file: Path):
        """Parser should extract specialization from ## Purpose section."""
        parser = AgentParser()
        agent = parser.parse(valid_agent_file)

        assert len(agent.specialization) > 0

    def test_parse_valid_agent_extracts_capabilities_as_frozenset(
        self, valid_agent_file: Path
    ):
        """Parser should extract capabilities as frozenset."""
        parser = AgentParser()
        agent = parser.parse(valid_agent_file)

        assert isinstance(agent.capabilities, frozenset)
        assert len(agent.capabilities) > 0

    def test_parse_valid_agent_extracts_required_directives(
        self, valid_agent_file: Path
    ):
        """Parser should extract required directive IDs."""
        parser = AgentParser()
        agent = parser.parse(valid_agent_file)

        assert isinstance(agent.required_directives, frozenset)
        assert "016" in agent.required_directives or "017" in agent.required_directives

    def test_parse_valid_agent_extracts_primers(self, valid_agent_file: Path):
        """Parser should extract execution primers."""
        parser = AgentParser()
        agent = parser.parse(valid_agent_file)

        assert isinstance(agent.primers, frozenset)
        assert "ATDD" in agent.primers or "TDD" in agent.primers

    def test_parse_valid_agent_calculates_source_hash(self, valid_agent_file: Path):
        """Parser should calculate SHA-256 hash of source file."""
        parser = AgentParser()
        agent = parser.parse(valid_agent_file)

        assert len(agent.source_hash) == 64
        assert all(c in "0123456789abcdef" for c in agent.source_hash)

    def test_parse_valid_agent_sets_source_file_path(self, valid_agent_file: Path):
        """Parser should set source_file to original file path."""
        parser = AgentParser()
        agent = parser.parse(valid_agent_file)

        assert agent.source_file == valid_agent_file

    def test_parse_missing_agent_file_raises_parse_error(self, tmp_path: Path):
        """Parser should raise ParseError when file does not exist."""
        parser = AgentParser()
        nonexistent_file = tmp_path / "nonexistent.agent.md"

        with pytest.raises(ParseError):
            parser.parse(nonexistent_file)

    def test_parse_invalid_agent_missing_required_fields_raises_validation_error(
        self, invalid_missing_fields_file: Path
    ):
        """Parser should raise ValidationError for missing required fields."""
        parser = AgentParser()

        with pytest.raises((ValidationError, MissingRequiredField)):
            parser.parse(invalid_missing_fields_file)

    def test_parse_agent_immutability(self, valid_agent_file: Path):
        """Parsed Agent should be immutable (frozen dataclass)."""
        parser = AgentParser()
        agent = parser.parse(valid_agent_file)

        with pytest.raises((AttributeError, TypeError)):
            agent.name = "Modified"  # type: ignore


# ============================================================================
# TacticParser Tests
# ============================================================================


class TestTacticParser:
    """Test suite for TacticParser (TDD approach)."""

    def test_parse_valid_tactic_returns_tactic_object(self, valid_tactic_file: Path):
        """Parser should parse valid tactic file into Tactic domain object."""
        parser = TacticParser()
        tactic = parser.parse(valid_tactic_file)

        assert isinstance(tactic, Tactic)

    def test_parse_valid_tactic_extracts_id_from_filename(
        self, valid_tactic_file: Path
    ):
        """Parser should extract tactic ID from filename."""
        parser = TacticParser()
        tactic = parser.parse(valid_tactic_file)

        assert tactic.id == "red-green-refactor"

    def test_parse_valid_tactic_extracts_title(self, valid_tactic_file: Path):
        """Parser should extract title from markdown heading."""
        parser = TacticParser()
        tactic = parser.parse(valid_tactic_file)

        assert "RED-GREEN-REFACTOR" in tactic.title or "Cycle" in tactic.title

    def test_parse_valid_tactic_extracts_description(self, valid_tactic_file: Path):
        """Parser should extract description from ## Intent section."""
        parser = TacticParser()
        tactic = parser.parse(valid_tactic_file)

        assert len(tactic.description) > 0

    def test_parse_valid_tactic_extracts_steps_as_tuple(self, valid_tactic_file: Path):
        """Parser should extract execution steps as tuple."""
        parser = TacticParser()
        tactic = parser.parse(valid_tactic_file)

        assert isinstance(tactic.steps, tuple)
        assert len(tactic.steps) >= 3  # RED, GREEN, REFACTOR

    def test_parse_valid_tactic_extracts_prerequisites(self, valid_tactic_file: Path):
        """Parser should extract prerequisites as frozenset."""
        parser = TacticParser()
        tactic = parser.parse(valid_tactic_file)

        assert isinstance(tactic.prerequisites, frozenset)

    def test_parse_valid_tactic_extracts_outcomes(self, valid_tactic_file: Path):
        """Parser should extract expected outcomes as frozenset."""
        parser = TacticParser()
        tactic = parser.parse(valid_tactic_file)

        assert isinstance(tactic.outcomes, frozenset)
        assert len(tactic.outcomes) > 0

    def test_parse_valid_tactic_calculates_source_hash(self, valid_tactic_file: Path):
        """Parser should calculate SHA-256 hash of source file."""
        parser = TacticParser()
        tactic = parser.parse(valid_tactic_file)

        assert len(tactic.source_hash) == 64

    def test_parse_missing_tactic_file_raises_parse_error(self, tmp_path: Path):
        """Parser should raise ParseError when file does not exist."""
        parser = TacticParser()

        with pytest.raises(ParseError):
            parser.parse(tmp_path / "nonexistent.tactic.md")


# ============================================================================
# ApproachParser Tests
# ============================================================================


class TestApproachParser:
    """Test suite for ApproachParser (TDD approach)."""

    def test_parse_valid_approach_returns_approach_object(
        self, valid_approach_file: Path
    ):
        """Parser should parse valid approach file into Approach domain object."""
        parser = ApproachParser()
        approach = parser.parse(valid_approach_file)

        assert isinstance(approach, Approach)

    def test_parse_valid_approach_extracts_id_from_filename(
        self, valid_approach_file: Path
    ):
        """Parser should extract approach ID from filename."""
        parser = ApproachParser()
        approach = parser.parse(valid_approach_file)

        assert approach.id == "test-first-development"

    def test_parse_valid_approach_extracts_title(self, valid_approach_file: Path):
        """Parser should extract title from markdown heading."""
        parser = ApproachParser()
        approach = parser.parse(valid_approach_file)

        assert "Test-First" in approach.title or "Development" in approach.title

    def test_parse_valid_approach_extracts_purpose(self, valid_approach_file: Path):
        """Parser should extract purpose from ## Purpose section."""
        parser = ApproachParser()
        approach = parser.parse(valid_approach_file)

        assert len(approach.purpose) > 0

    def test_parse_valid_approach_extracts_principles_as_tuple(
        self, valid_approach_file: Path
    ):
        """Parser should extract principles as tuple."""
        parser = ApproachParser()
        approach = parser.parse(valid_approach_file)

        assert isinstance(approach.principles, tuple)
        assert len(approach.principles) > 0

    def test_parse_valid_approach_extracts_when_to_use(
        self, valid_approach_file: Path
    ):
        """Parser should extract 'when to use' scenarios."""
        parser = ApproachParser()
        approach = parser.parse(valid_approach_file)

        assert isinstance(approach.when_to_use, tuple)
        assert len(approach.when_to_use) > 0

    def test_parse_valid_approach_extracts_when_to_avoid(
        self, valid_approach_file: Path
    ):
        """Parser should extract 'when to avoid' scenarios."""
        parser = ApproachParser()
        approach = parser.parse(valid_approach_file)

        assert isinstance(approach.when_to_avoid, tuple)
        assert len(approach.when_to_avoid) > 0

    def test_parse_valid_approach_extracts_related_directives(
        self, valid_approach_file: Path
    ):
        """Parser should extract related directive IDs."""
        parser = ApproachParser()
        approach = parser.parse(valid_approach_file)

        assert isinstance(approach.related_directives, frozenset)

    def test_parse_valid_approach_calculates_source_hash(
        self, valid_approach_file: Path
    ):
        """Parser should calculate SHA-256 hash of source file."""
        parser = ApproachParser()
        approach = parser.parse(valid_approach_file)

        assert len(approach.source_hash) == 64

    def test_parse_missing_approach_file_raises_parse_error(self, tmp_path: Path):
        """Parser should raise ParseError when file does not exist."""
        parser = ApproachParser()

        with pytest.raises(ParseError):
            parser.parse(tmp_path / "nonexistent.md")
