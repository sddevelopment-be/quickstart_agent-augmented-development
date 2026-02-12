"""
Test suite for enhanced AgentParser features (ADR-045 Task 3).

Tests advanced agent profile parsing: capabilities descriptions, handoff patterns,
constraints, preferences, and primer matrix.

Test Coverage (TDD Approach):
- Capabilities section (primary, secondary, avoid)
- Handoff patterns (from/to other agents)
- Constraints and preferences
- Primer matrix (Directive 010 compliance)
- Default reasoning mode
- Edge cases (missing sections, malformed data)

Related ADRs
------------
- ADR-045: Doctrine Concept Domain Model (Task 3)

Directives Applied
------------------
- Directive 016: ATDD - Acceptance tests define success criteria
- Directive 017: TDD - Unit tests written first, RED-GREEN-REFACTOR
"""

from pathlib import Path

import pytest

from src.domain.doctrine.models import HandoffPattern, PrimerEntry
from src.domain.doctrine.parsers import AgentParser

# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def agent_file_with_capabilities(tmp_path: Path) -> Path:
    """Create agent profile with structured capabilities section."""
    file_path = tmp_path / "backend-dev.agent.md"
    file_path.write_text("""---
name: backend-dev
description: Backend development specialist
version: "1.0"
status: active
---

# Agent Profile: Backend Dev (Backend Development Specialist)

## 2. Purpose

Backend development specialist focusing on API design and testing.

## 3. Specialization

- **Primary focus:** Python development, API design, testing with pytest
- **Secondary awareness:** Architecture review, code documentation, performance tuning
- **Avoid:** Frontend work, DevOps infrastructure, database administration
- **Success means:** Type-safe APIs with >90% test coverage

## 4. Collaboration Contract

Standard collaboration protocols apply.

### Collaboration Patterns

#### Handoff To
- **Backend-benny:** Service integration and deployment
- **Architect:** Major design decisions requiring ADRs
- **Build-automation:** CI/CD pipeline integration

#### Handoff From
- **Architect:** ADRs, design specifications, architectural constraints
- **Project-planner:** Requirements, user stories, acceptance criteria

#### Works With
- **Curator:** Documentation updates and API references
- **Code-reviewer:** Code quality validation

## 5. Mode Defaults

| Mode             | Description                  | Use Case          |
|------------------|------------------------------|-------------------|
| `/analysis-mode` | Code design & testing        | Default mode      |
| `/creative-mode` | Alternative implementations  | Algorithm options |
""")
    return file_path


@pytest.fixture
def agent_file_with_all_features(tmp_path: Path) -> Path:
    """Create comprehensive agent profile with all enhanced features."""
    file_path = tmp_path / "python-pedro.agent.md"
    file_path.write_text("""---
name: python-pedro
description: Python development specialist applying ATDD + TDD
version: "1.0"
status: active
tags:
  - python
  - testing
  - tdd
---

# Agent Profile: Python Pedro (Python Development Specialist)

## 2. Purpose

Deliver high-quality Python code with TDD and type safety.

## 3. Specialization

- **Primary focus:** Python 3.9+ code quality, type hints, pytest, pydantic
- **Secondary awareness:** Performance profiling, memory management, packaging
- **Avoid:** Non-Python concerns, infrastructure-as-code, frontend details
- **Success means:** Type-safe code with >80% coverage

## 4. Collaboration Contract

### Collaboration Patterns

#### Handoff To
- **Backend-dev:** Service integration, API design, deployment patterns
- **Architect:** Major design decisions, cross-cutting concerns, ADR creation
- **Build-automation:** CI/CD pipeline integration, test automation

#### Handoff From
- **Architect:** ADRs, design specifications, architectural constraints
- **Project-planner:** Requirements, user stories, acceptance criteria
- **Manager:** Task assignments, priority, coordination signals

#### Works With
- **Curator:** Documentation updates, docstring quality
- **Lexical:** Style consistency in docstrings
- **Framework-guardian:** Python framework version upgrades

### Constraints

- Must follow PEP 8 style guide
- Type hints required for all functions
- Minimum 80% test coverage

### Preferences

- Default mode: analysis-mode
- Test framework: pytest
- Linter: ruff + mypy

## 5. Mode Defaults

| Mode             | Description                  | Use Case                     |
|------------------|------------------------------|------------------------------|
| `/analysis-mode` | Code design & testing        | Test planning, refactoring   |
| `/creative-mode` | Alternative implementations  | Algorithm exploration        |
| `/meta-mode`     | Process & quality reflection | Self-review, coverage check  |

## 6. Primers

**Primer Requirement:** Follow Directive 010 (Mode Protocol) and log per Directive 014.

**Test-First Requirement:** Follow Directives 016 (ATDD) and 017 (TDD) for all code changes.

**Primer Matrix:**
- **Feature development:** ATDD → TDD → Implementation
- **Bug fixes:** Reproduce with failing test → Fix → Verify
- **Refactoring:** Preserve tests → Refactor → Verify
""")
    return file_path


@pytest.fixture
def agent_file_minimal(tmp_path: Path) -> Path:
    """Create minimal agent profile without enhanced features."""
    file_path = tmp_path / "minimal-agent.agent.md"
    file_path.write_text("""---
name: minimal-agent
description: Minimal agent for testing
---

# Agent Profile: Minimal Agent

## 2. Purpose

Basic agent profile for parser validation.
""")
    return file_path


# ============================================================================
# TestAgentParserCapabilities: Structured Capability Parsing
# ============================================================================


class TestAgentParserCapabilities:
    """Test capability descriptions extraction from ## Specialization section."""

    def test_parse_capabilities_extracts_primary_focus(
        self, agent_file_with_capabilities: Path
    ):
        """Parser should extract primary focus from specialization section."""
        parser = AgentParser()
        agent = parser.parse(agent_file_with_capabilities)

        assert hasattr(agent, "capability_descriptions")
        assert isinstance(agent.capability_descriptions, dict)
        assert "primary" in agent.capability_descriptions
        assert "Python development" in agent.capability_descriptions["primary"]
        assert "API design" in agent.capability_descriptions["primary"]

    def test_parse_capabilities_extracts_secondary_awareness(
        self, agent_file_with_capabilities: Path
    ):
        """Parser should extract secondary awareness capabilities."""
        parser = AgentParser()
        agent = parser.parse(agent_file_with_capabilities)

        assert "secondary" in agent.capability_descriptions
        assert "Architecture review" in agent.capability_descriptions["secondary"]
        assert "code documentation" in agent.capability_descriptions["secondary"]

    def test_parse_capabilities_extracts_avoid_list(
        self, agent_file_with_capabilities: Path
    ):
        """Parser should extract avoid list from specialization."""
        parser = AgentParser()
        agent = parser.parse(agent_file_with_capabilities)

        assert "avoid" in agent.capability_descriptions
        assert "Frontend work" in agent.capability_descriptions["avoid"]
        assert "DevOps" in agent.capability_descriptions["avoid"]

    def test_parse_capabilities_extracts_success_criteria(
        self, agent_file_with_capabilities: Path
    ):
        """Parser should extract success criteria from specialization."""
        parser = AgentParser()
        agent = parser.parse(agent_file_with_capabilities)

        assert "success" in agent.capability_descriptions
        assert "Type-safe" in agent.capability_descriptions["success"]
        assert "90%" in agent.capability_descriptions["success"]

    def test_parse_capabilities_handles_missing_section(self, agent_file_minimal: Path):
        """Parser should handle missing capabilities section gracefully."""
        parser = AgentParser()
        agent = parser.parse(agent_file_minimal)

        # Should not fail, just return empty capabilities
        assert agent.capability_descriptions == {}


# ============================================================================
# TestAgentParserHandoffPatterns: Collaboration Pattern Extraction
# ============================================================================


class TestAgentParserHandoffPatterns:
    """Test handoff pattern extraction from collaboration sections."""

    def test_parse_handoff_patterns_extracts_handoff_to(
        self, agent_file_with_capabilities: Path
    ):
        """Parser should extract 'Handoff To' patterns."""
        parser = AgentParser()
        agent = parser.parse(agent_file_with_capabilities)

        assert hasattr(agent, "handoff_patterns")
        assert isinstance(agent.handoff_patterns, tuple)
        assert len(agent.handoff_patterns) > 0

        # Find handoff to backend-benny
        to_patterns = [p for p in agent.handoff_patterns if p.direction == "to"]
        assert len(to_patterns) >= 1

        backend_pattern = next(
            (p for p in to_patterns if "backend-benny" in p.target_agent.lower()), None
        )
        assert backend_pattern is not None
        assert "Service integration" in backend_pattern.context

    def test_parse_handoff_patterns_extracts_handoff_from(
        self, agent_file_with_capabilities: Path
    ):
        """Parser should extract 'Handoff From' patterns."""
        parser = AgentParser()
        agent = parser.parse(agent_file_with_capabilities)

        from_patterns = [p for p in agent.handoff_patterns if p.direction == "from"]
        assert len(from_patterns) >= 1

        architect_pattern = next(
            (p for p in from_patterns if "architect" in p.source_agent.lower()), None
        )
        assert architect_pattern is not None
        assert (
            "ADRs" in architect_pattern.context or "design" in architect_pattern.context
        )

    def test_parse_handoff_patterns_extracts_works_with(
        self, agent_file_with_capabilities: Path
    ):
        """Parser should extract 'Works With' collaboration patterns."""
        parser = AgentParser()
        agent = parser.parse(agent_file_with_capabilities)

        works_with_patterns = [
            p for p in agent.handoff_patterns if p.direction == "works_with"
        ]
        assert len(works_with_patterns) >= 1

        curator_pattern = next(
            (p for p in works_with_patterns if "curator" in p.target_agent.lower()),
            None,
        )
        assert curator_pattern is not None

    def test_parse_handoff_patterns_creates_handoff_pattern_objects(
        self, agent_file_with_all_features: Path
    ):
        """Parser should create HandoffPattern domain objects."""
        parser = AgentParser()
        agent = parser.parse(agent_file_with_all_features)

        assert len(agent.handoff_patterns) > 0
        first_pattern = agent.handoff_patterns[0]

        assert isinstance(first_pattern, HandoffPattern)
        assert hasattr(first_pattern, "source_agent")
        assert hasattr(first_pattern, "target_agent")
        assert hasattr(first_pattern, "direction")
        assert hasattr(first_pattern, "context")

    def test_parse_handoff_patterns_handles_missing_section(
        self, agent_file_minimal: Path
    ):
        """Parser should handle missing handoff patterns section."""
        parser = AgentParser()
        agent = parser.parse(agent_file_minimal)

        # Should not fail, just return empty tuple
        assert agent.handoff_patterns == ()


# ============================================================================
# TestAgentParserConstraints: Constraint and Preference Extraction
# ============================================================================


class TestAgentParserConstraints:
    """Test constraint and preference extraction."""

    def test_parse_constraints_extracts_from_section(
        self, agent_file_with_all_features: Path
    ):
        """Parser should extract constraints from ### Constraints section."""
        parser = AgentParser()
        agent = parser.parse(agent_file_with_all_features)

        assert hasattr(agent, "constraints")
        assert isinstance(agent.constraints, frozenset)
        assert len(agent.constraints) > 0

        # Check specific constraints
        constraints_list = list(agent.constraints)
        assert any("PEP 8" in c for c in constraints_list)
        assert any("Type hints" in c for c in constraints_list)
        assert any("80%" in c or "coverage" in c for c in constraints_list)

    def test_parse_preferences_extracts_from_section(
        self, agent_file_with_all_features: Path
    ):
        """Parser should extract preferences from ### Preferences section."""
        parser = AgentParser()
        agent = parser.parse(agent_file_with_all_features)

        assert hasattr(agent, "preferences")
        assert isinstance(agent.preferences, dict)
        assert len(agent.preferences) > 0

        # Check specific preferences
        assert "default_mode" in agent.preferences
        assert agent.preferences["default_mode"] == "analysis-mode"
        assert "test_framework" in agent.preferences
        assert agent.preferences["test_framework"] == "pytest"

    def test_parse_constraints_handles_missing_section(self, agent_file_minimal: Path):
        """Parser should handle missing constraints section."""
        parser = AgentParser()
        agent = parser.parse(agent_file_minimal)

        assert agent.constraints == frozenset()

    def test_parse_preferences_handles_missing_section(self, agent_file_minimal: Path):
        """Parser should handle missing preferences section."""
        parser = AgentParser()
        agent = parser.parse(agent_file_minimal)

        assert agent.preferences == {}


# ============================================================================
# TestAgentParserPrimerMatrix: Primer Requirement Extraction
# ============================================================================


class TestAgentParserPrimerMatrix:
    """Test primer matrix extraction (Directive 010 compliance)."""

    def test_parse_primer_matrix_extracts_entries(
        self, agent_file_with_all_features: Path
    ):
        """Parser should extract primer matrix entries."""
        parser = AgentParser()
        agent = parser.parse(agent_file_with_all_features)

        assert hasattr(agent, "primer_matrix")
        assert isinstance(agent.primer_matrix, tuple)
        assert len(agent.primer_matrix) > 0

    def test_parse_primer_matrix_creates_primer_entry_objects(
        self, agent_file_with_all_features: Path
    ):
        """Parser should create PrimerEntry domain objects."""
        parser = AgentParser()
        agent = parser.parse(agent_file_with_all_features)

        assert len(agent.primer_matrix) > 0
        first_entry = agent.primer_matrix[0]

        assert isinstance(first_entry, PrimerEntry)
        assert hasattr(first_entry, "task_type")
        assert hasattr(first_entry, "required_primers")
        assert isinstance(first_entry.required_primers, frozenset)

    def test_parse_primer_matrix_extracts_feature_development(
        self, agent_file_with_all_features: Path
    ):
        """Parser should extract feature development primer workflow."""
        parser = AgentParser()
        agent = parser.parse(agent_file_with_all_features)

        feature_entry = next(
            (e for e in agent.primer_matrix if e.task_type == "feature_development"),
            None,
        )
        assert feature_entry is not None
        assert "ATDD" in feature_entry.required_primers
        assert "TDD" in feature_entry.required_primers

    def test_parse_primer_matrix_handles_missing_section(
        self, agent_file_minimal: Path
    ):
        """Parser should handle missing primer matrix section."""
        parser = AgentParser()
        agent = parser.parse(agent_file_minimal)

        assert agent.primer_matrix == ()


# ============================================================================
# TestAgentParserDefaultMode: Default Reasoning Mode Extraction
# ============================================================================


class TestAgentParserDefaultMode:
    """Test default reasoning mode extraction."""

    def test_parse_default_mode_from_preferences(
        self, agent_file_with_all_features: Path
    ):
        """Parser should extract default mode from preferences."""
        parser = AgentParser()
        agent = parser.parse(agent_file_with_all_features)

        assert hasattr(agent, "default_mode")
        assert agent.default_mode == "analysis-mode"

    def test_parse_default_mode_from_mode_defaults_table(
        self, agent_file_with_capabilities: Path
    ):
        """Parser should infer default mode from Mode Defaults table."""
        parser = AgentParser()
        agent = parser.parse(agent_file_with_capabilities)

        # Should extract from "Default mode" comment in table
        assert hasattr(agent, "default_mode")
        assert agent.default_mode == "analysis-mode"

    def test_parse_default_mode_uses_fallback(self, agent_file_minimal: Path):
        """Parser should use 'analysis-mode' as default when not specified."""
        parser = AgentParser()
        agent = parser.parse(agent_file_minimal)

        assert agent.default_mode == "analysis-mode"


# ============================================================================
# TestAgentParserIntegration: Full Integration Tests
# ============================================================================


class TestAgentParserIntegration:
    """Integration tests for complete agent profile parsing."""

    def test_parse_complete_profile_all_features(
        self, agent_file_with_all_features: Path
    ):
        """Parser should successfully parse complete profile with all features."""
        parser = AgentParser()
        agent = parser.parse(agent_file_with_all_features)

        # Verify all enhanced fields exist and are populated
        assert agent.capability_descriptions != {}
        assert agent.handoff_patterns != ()
        assert agent.constraints != frozenset()
        assert agent.preferences != {}
        assert agent.primer_matrix != ()
        assert agent.default_mode != ""

    def test_parse_minimal_profile_uses_defaults(self, agent_file_minimal: Path):
        """Parser should handle minimal profile with default values."""
        parser = AgentParser()
        agent = parser.parse(agent_file_minimal)

        # All enhanced fields should exist but be empty
        assert agent.capability_descriptions == {}
        assert agent.handoff_patterns == ()
        assert agent.constraints == frozenset()
        assert agent.preferences == {}
        assert agent.primer_matrix == ()
        assert agent.default_mode == "analysis-mode"

    def test_parse_agent_immutability_with_enhanced_fields(
        self, agent_file_with_all_features: Path
    ):
        """Agent objects with enhanced fields should remain immutable."""
        parser = AgentParser()
        agent = parser.parse(agent_file_with_all_features)

        # Attempting to modify should raise exception
        with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
            agent.capability_descriptions = {}

        with pytest.raises(Exception):
            agent.handoff_patterns = ()

        with pytest.raises(Exception):
            agent.constraints = frozenset()


# ============================================================================
# TestAgentParserEdgeCases: Error Handling and Edge Cases
# ============================================================================


class TestAgentParserEdgeCases:
    """Test error handling and edge cases."""

    def test_parse_malformed_capabilities_section(self, tmp_path: Path):
        """Parser should handle malformed capabilities section gracefully."""
        file_path = tmp_path / "malformed.agent.md"
        file_path.write_text("""---
name: malformed-agent
description: Test malformed sections
---

# Agent Profile: Malformed Agent

## 3. Specialization

This section has no proper formatting.
Just plain text without bullet points.
""")
        parser = AgentParser()
        agent = parser.parse(file_path)

        # Should not crash, just return empty capabilities
        assert agent.capability_descriptions == {}

    def test_parse_malformed_handoff_patterns(self, tmp_path: Path):
        """Parser should handle malformed handoff patterns gracefully."""
        file_path = tmp_path / "malformed-handoff.agent.md"
        file_path.write_text("""---
name: malformed-handoff
description: Test malformed handoff patterns
---

# Agent Profile: Malformed Handoff

## 4. Collaboration Contract

### Collaboration Patterns

Random text without proper formatting.
No bullet points or structure.
""")
        parser = AgentParser()
        agent = parser.parse(file_path)

        # Should not crash, just return empty patterns
        assert agent.handoff_patterns == ()

    def test_parse_empty_constraints_section(self, tmp_path: Path):
        """Parser should handle empty constraints section."""
        file_path = tmp_path / "empty-constraints.agent.md"
        file_path.write_text("""---
name: empty-constraints
description: Test empty constraints
---

# Agent Profile: Empty Constraints

## 4. Collaboration Contract

### Constraints

(None specified)
""")
        parser = AgentParser()
        agent = parser.parse(file_path)

        assert agent.constraints == frozenset()
