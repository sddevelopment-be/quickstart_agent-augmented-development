#!/usr/bin/env python3
"""
Unit tests for agent hierarchy validation script.

Reference: tests/validate_agent_hierarchy.py
DDR: DDR-011 (Agent Specialization Hierarchy)
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pytest

# Add tests/ to path to import the validator module
tests_path = Path(__file__).parent.parent
sys.path.insert(0, str(tests_path))

from validate_agent_hierarchy import (
    calculate_context_hash,
    detect_circular_dependencies,
    detect_priority_conflicts,
    discover_agents,
    load_agent_profile,
    validate_parent_references,
    validate_schema,
)


# --- Fixtures ---


@pytest.fixture
def sample_agent_profile() -> dict[str, Any]:
    """Valid agent profile with all required fields."""
    return {
        "name": "python-pedro",
        "specializes_from": "backend-dev",
        "routing_priority": 75,
        "max_concurrent_tasks": 5,
        "specialization_context": {
            "language": ["python"],
            "frameworks": ["pytest", "pydantic"],
            "file_patterns": ["*.py", "requirements.txt"],
        },
    }


@pytest.fixture
def tmp_doctrine_dir(tmp_path: Path) -> Path:
    """Create temporary doctrine/agents directory structure."""
    doctrine_dir = tmp_path / "doctrine" / "agents"
    doctrine_dir.mkdir(parents=True, exist_ok=True)
    return doctrine_dir


@pytest.fixture
def tmp_custom_agents_dir(tmp_path: Path) -> Path:
    """Create temporary .doctrine-config/custom-agents directory structure."""
    custom_dir = tmp_path / ".doctrine-config" / "custom-agents"
    custom_dir.mkdir(parents=True, exist_ok=True)
    return custom_dir


def create_agent_file(
    directory: Path, name: str, profile: dict[str, Any]
) -> Path:
    """Helper to create agent markdown file with YAML frontmatter."""
    import yaml

    # Ensure description is present (required by domain layer AgentParser)
    if "description" not in profile:
        profile = {**profile, "description": f"Test agent {name}"}

    file_path = directory / f"{name}.agent.md"
    frontmatter_yaml = yaml.dump(profile, default_flow_style=False)
    content = (
        f"---\n{frontmatter_yaml}---\n\n"
        f"# Agent Profile: {name}\n\n"
        f"## 2. Purpose\n\nTest agent for validation.\n"
    )

    file_path.write_text(content, encoding="utf-8")
    return file_path


# --- Test Cases ---


class TestLoadAgentProfile:
    """Tests for load_agent_profile function."""

    def test_load_valid_agent_profile(self, tmp_path: Path) -> None:
        """
        GIVEN a valid agent markdown file with YAML frontmatter
        WHEN load_agent_profile is called
        THEN it should return the parsed frontmatter dict
        """
        # Arrange
        profile_data = {
            "name": "test-agent",
            "routing_priority": 60,
        }
        agent_file = create_agent_file(tmp_path, "test-agent", profile_data)

        # Assumption
        assert agent_file.exists()

        # Act
        result = load_agent_profile(agent_file)

        # Assert
        assert result is not None
        assert result["name"] == "test-agent"
        assert result["routing_priority"] == 60

    def test_load_profile_missing_frontmatter(self, tmp_path: Path) -> None:
        """
        GIVEN a markdown file without YAML frontmatter markers
        WHEN load_agent_profile is called
        THEN it should return None
        """
        # Arrange
        agent_file = tmp_path / "invalid.agent.md"
        agent_file.write_text("# Agent without frontmatter\n\nContent here.", encoding="utf-8")

        # Assumption
        assert agent_file.exists()

        # Act
        result = load_agent_profile(agent_file)

        # Assert
        assert result is None

    def test_load_profile_incomplete_frontmatter(self, tmp_path: Path) -> None:
        """
        GIVEN a markdown file with incomplete frontmatter (only one --- marker)
        WHEN load_agent_profile is called
        THEN it should return None
        """
        # Arrange
        agent_file = tmp_path / "incomplete.agent.md"
        agent_file.write_text("---\nname: incomplete\n\nNo closing marker.", encoding="utf-8")

        # Assumption
        assert agent_file.exists()

        # Act
        result = load_agent_profile(agent_file)

        # Assert
        assert result is None

    def test_load_profile_invalid_yaml(self, tmp_path: Path) -> None:
        """
        GIVEN a markdown file with malformed YAML in frontmatter
        WHEN load_agent_profile is called
        THEN it should return None
        """
        # Arrange
        agent_file = tmp_path / "invalid-yaml.agent.md"
        agent_file.write_text("---\nname: [\ninvalid yaml\n---\n", encoding="utf-8")

        # Assumption
        assert agent_file.exists()

        # Act
        result = load_agent_profile(agent_file)

        # Assert
        assert result is None


class TestDiscoverAgents:
    """Tests for discover_agents function."""

    def test_discover_framework_agents(
        self, tmp_path: Path, tmp_doctrine_dir: Path
    ) -> None:
        """
        GIVEN framework agents in doctrine/agents/
        WHEN discover_agents is called
        THEN it should load all framework agents
        """
        # Arrange
        create_agent_file(tmp_doctrine_dir, "agent-one", {"name": "agent-one"})
        create_agent_file(tmp_doctrine_dir, "agent-two", {"name": "agent-two"})

        # Assumption
        assert len(list(tmp_doctrine_dir.glob("*.agent.md"))) == 2

        # Act
        agents = discover_agents(tmp_path)

        # Assert
        assert len(agents) == 2
        assert "agent-one" in agents
        assert "agent-two" in agents
        assert agents["agent-one"]["_source"] == "framework"
        assert agents["agent-two"]["_source"] == "framework"

    def test_discover_custom_agents(
        self, tmp_path: Path, tmp_custom_agents_dir: Path
    ) -> None:
        """
        GIVEN custom agents in .doctrine-config/custom-agents/
        WHEN discover_agents is called
        THEN it should load all custom agents
        """
        # Arrange
        create_agent_file(tmp_custom_agents_dir, "custom-one", {"name": "custom-one"})

        # Assumption
        assert len(list(tmp_custom_agents_dir.glob("*.agent.md"))) == 1

        # Act
        agents = discover_agents(tmp_path)

        # Assert
        assert len(agents) == 1
        assert "custom-one" in agents
        assert agents["custom-one"]["_source"] == "local"

    def test_custom_agent_overrides_framework(
        self, tmp_path: Path, tmp_doctrine_dir: Path, tmp_custom_agents_dir: Path
    ) -> None:
        """
        GIVEN same-named agent in both framework and custom directories
        WHEN discover_agents is called
        THEN custom agent should override framework agent
        """
        # Arrange
        create_agent_file(
            tmp_doctrine_dir, "shared-agent", {"name": "shared-agent"}
        )
        create_agent_file(
            tmp_custom_agents_dir, "shared-agent", {"name": "shared-agent"}
        )

        # Assumption
        assert (tmp_doctrine_dir / "shared-agent.agent.md").exists()
        assert (tmp_custom_agents_dir / "shared-agent.agent.md").exists()

        # Act
        agents = discover_agents(tmp_path)

        # Assert
        assert len(agents) == 1
        assert agents["shared-agent"]["_source"] == "local"

    def test_discover_no_agents_directory(self, tmp_path: Path) -> None:
        """
        GIVEN no doctrine/agents/ directory exists
        WHEN discover_agents is called
        THEN it should return empty dict
        """
        # Arrange - tmp_path has no doctrine/agents/

        # Assumption
        assert not (tmp_path / "doctrine" / "agents").exists()

        # Act
        agents = discover_agents(tmp_path)

        # Assert
        assert len(agents) == 0


class TestCircularDependencies:
    """Tests for detect_circular_dependencies function."""

    def test_detect_simple_circular_dependency(self) -> None:
        """
        GIVEN agent A specializes B, B specializes A
        WHEN detect_circular_dependencies is called
        THEN it should detect the circular dependency
        """
        # Arrange
        agents = {
            "agent-a": {"name": "agent-a", "specializes_from": "agent-b"},
            "agent-b": {"name": "agent-b", "specializes_from": "agent-a"},
        }

        # Assumption
        assert "agent-a" in agents
        assert "agent-b" in agents

        # Act
        errors = detect_circular_dependencies(agents)

        # Assert
        assert len(errors) > 0
        assert any("Circular dependency" in err for err in errors)

    def test_detect_deep_circular_dependency(self) -> None:
        """
        GIVEN agent A→B→C→A chain
        WHEN detect_circular_dependencies is called
        THEN it should detect the circular dependency
        """
        # Arrange
        agents = {
            "agent-a": {"name": "agent-a", "specializes_from": "agent-b"},
            "agent-b": {"name": "agent-b", "specializes_from": "agent-c"},
            "agent-c": {"name": "agent-c", "specializes_from": "agent-a"},
        }

        # Assumption
        assert len(agents) == 3

        # Act
        errors = detect_circular_dependencies(agents)

        # Assert
        assert len(errors) > 0
        assert any("Circular dependency" in err for err in errors)

    def test_no_circular_when_valid(self) -> None:
        """
        GIVEN valid specialization chain (Pedro→Benny, no cycle)
        WHEN detect_circular_dependencies is called
        THEN it should return no errors
        """
        # Arrange
        agents = {
            "benny": {"name": "benny"},
            "pedro": {"name": "pedro", "specializes_from": "benny"},
        }

        # Assumption
        assert agents["pedro"]["specializes_from"] == "benny"
        assert "specializes_from" not in agents["benny"]

        # Act
        errors = detect_circular_dependencies(agents)

        # Assert
        assert len(errors) == 0


class TestParentReferences:
    """Tests for validate_parent_references function."""

    def test_missing_parent_detected(self) -> None:
        """
        GIVEN agent references nonexistent parent in specializes_from
        WHEN validate_parent_references is called
        THEN it should report an error
        """
        # Arrange
        agents = {
            "child": {"name": "child", "specializes_from": "nonexistent-parent"},
        }

        # Assumption
        assert "nonexistent-parent" not in agents

        # Act
        errors = validate_parent_references(agents)

        # Assert
        assert len(errors) == 1
        assert "nonexistent-parent" in errors[0]
        assert "not found" in errors[0]

    def test_valid_parent_reference(self) -> None:
        """
        GIVEN agent references existing parent
        WHEN validate_parent_references is called
        THEN it should return no errors
        """
        # Arrange
        agents = {
            "parent": {"name": "parent"},
            "child": {"name": "child", "specializes_from": "parent"},
        }

        # Assumption
        assert agents["child"]["specializes_from"] in agents

        # Act
        errors = validate_parent_references(agents)

        # Assert
        assert len(errors) == 0

    def test_agent_with_no_parent(self) -> None:
        """
        GIVEN agent with no specializes_from field
        WHEN validate_parent_references is called
        THEN it should return no errors (root agent)
        """
        # Arrange
        agents = {
            "root": {"name": "root"},
        }

        # Assumption
        assert "specializes_from" not in agents["root"]

        # Act
        errors = validate_parent_references(agents)

        # Assert
        assert len(errors) == 0


class TestPriorityConflicts:
    """Tests for detect_priority_conflicts function."""

    def test_priority_conflict_detected(self) -> None:
        """
        GIVEN two agents with same priority and overlapping context
        WHEN detect_priority_conflicts is called
        THEN it should report a conflict warning
        """
        # Arrange
        agents = {
            "agent-a": {
                "name": "agent-a",
                "routing_priority": 75,
                "specialization_context": {"language": ["python"]},
            },
            "agent-b": {
                "name": "agent-b",
                "routing_priority": 75,
                "specialization_context": {"language": ["python"]},
            },
        }

        # Assumption
        assert agents["agent-a"]["routing_priority"] == agents["agent-b"]["routing_priority"]

        # Act
        errors = detect_priority_conflicts(agents)

        # Assert
        assert len(errors) > 0
        assert any("Priority conflict" in err for err in errors)

    def test_no_conflict_different_priorities(self) -> None:
        """
        GIVEN two agents with same context but different priorities
        WHEN detect_priority_conflicts is called
        THEN it should return no errors
        """
        # Arrange
        agents = {
            "agent-a": {
                "name": "agent-a",
                "routing_priority": 75,
                "specialization_context": {"language": ["python"]},
            },
            "agent-b": {
                "name": "agent-b",
                "routing_priority": 65,
                "specialization_context": {"language": ["python"]},
            },
        }

        # Assumption
        assert agents["agent-a"]["routing_priority"] != agents["agent-b"]["routing_priority"]

        # Act
        errors = detect_priority_conflicts(agents)

        # Assert
        assert len(errors) == 0

    def test_no_conflict_different_contexts(self) -> None:
        """
        GIVEN two agents with same priority but different contexts
        WHEN detect_priority_conflicts is called
        THEN it should return no errors
        """
        # Arrange
        agents = {
            "agent-a": {
                "name": "agent-a",
                "routing_priority": 75,
                "specialization_context": {"language": ["python"]},
            },
            "agent-b": {
                "name": "agent-b",
                "routing_priority": 75,
                "specialization_context": {"language": ["javascript"]},
            },
        }

        # Assumption
        assert agents["agent-a"]["specialization_context"] != agents["agent-b"]["specialization_context"]

        # Act
        errors = detect_priority_conflicts(agents)

        # Assert
        assert len(errors) == 0


class TestSchemaValidation:
    """Tests for validate_schema function."""

    def test_routing_priority_bounds_low(self) -> None:
        """
        GIVEN agent with routing_priority < 0
        WHEN validate_schema is called
        THEN it should report an error
        """
        # Arrange
        agents = {
            "agent": {"name": "agent", "routing_priority": -1},
        }

        # Assumption
        assert agents["agent"]["routing_priority"] < 0

        # Act
        errors = validate_schema(agents)

        # Assert
        assert len(errors) > 0
        assert any("routing_priority must be 0-100" in err for err in errors)

    def test_routing_priority_bounds_high(self) -> None:
        """
        GIVEN agent with routing_priority > 100
        WHEN validate_schema is called
        THEN it should report an error
        """
        # Arrange
        agents = {
            "agent": {"name": "agent", "routing_priority": 101},
        }

        # Assumption
        assert agents["agent"]["routing_priority"] > 100

        # Act
        errors = validate_schema(agents)

        # Assert
        assert len(errors) > 0
        assert any("routing_priority must be 0-100" in err for err in errors)

    def test_routing_priority_valid(self) -> None:
        """
        GIVEN agent with routing_priority in valid range (0-100)
        WHEN validate_schema is called
        THEN it should return no errors
        """
        # Arrange
        agents = {
            "agent": {"name": "agent", "routing_priority": 50},
        }

        # Assumption
        assert 0 <= agents["agent"]["routing_priority"] <= 100

        # Act
        errors = validate_schema(agents)

        # Assert
        assert len(errors) == 0

    def test_max_concurrent_tasks_positive(self) -> None:
        """
        GIVEN agent with max_concurrent_tasks <= 0
        WHEN validate_schema is called
        THEN it should report an error
        """
        # Arrange
        agents = {
            "agent-zero": {"name": "agent-zero", "max_concurrent_tasks": 0},
            "agent-negative": {"name": "agent-negative", "max_concurrent_tasks": -5},
        }

        # Assumption
        assert agents["agent-zero"]["max_concurrent_tasks"] <= 0
        assert agents["agent-negative"]["max_concurrent_tasks"] < 0

        # Act
        errors = validate_schema(agents)

        # Assert
        assert len(errors) == 2
        assert all("max_concurrent_tasks must be positive" in err for err in errors)

    def test_max_concurrent_tasks_valid(self) -> None:
        """
        GIVEN agent with positive max_concurrent_tasks
        WHEN validate_schema is called
        THEN it should return no errors
        """
        # Arrange
        agents = {
            "agent": {"name": "agent", "max_concurrent_tasks": 5},
        }

        # Assumption
        assert agents["agent"]["max_concurrent_tasks"] > 0

        # Act
        errors = validate_schema(agents)

        # Assert
        assert len(errors) == 0

    def test_valid_specialization_context_schema(self) -> None:
        """
        GIVEN agent with valid specialization_context with all fields
        WHEN validate_schema is called
        THEN it should return no errors
        """
        # Arrange
        agents = {
            "agent": {
                "name": "agent",
                "specialization_context": {
                    "language": ["python"],
                    "frameworks": ["pytest", "pydantic"],
                    "file_patterns": ["*.py"],
                    "domain_keywords": ["testing", "validation"],
                    "writing_style": ["concise"],
                    "complexity_preference": ["simple"],
                },
            },
        }

        # Assumption
        assert "specialization_context" in agents["agent"]

        # Act
        errors = validate_schema(agents)

        # Assert
        assert len(errors) == 0

    def test_invalid_context_key(self) -> None:
        """
        GIVEN agent with unknown key in specialization_context
        WHEN validate_schema is called
        THEN it should report an error
        """
        # Arrange
        agents = {
            "agent": {
                "name": "agent",
                "specialization_context": {
                    "language": ["python"],
                    "invalid_key": ["value"],
                    "another_bad_key": ["data"],
                },
            },
        }

        # Assumption
        assert "invalid_key" in agents["agent"]["specialization_context"]
        assert "another_bad_key" in agents["agent"]["specialization_context"]

        # Act
        errors = validate_schema(agents)

        # Assert
        assert len(errors) > 0
        assert any("invalid specialization_context keys" in err for err in errors)
        assert any("invalid_key" in err for err in errors)

    def test_context_field_not_list(self) -> None:
        """
        GIVEN agent with specialization_context field that is not a list
        WHEN validate_schema is called
        THEN it should report an error
        """
        # Arrange
        agents = {
            "agent": {
                "name": "agent",
                "specialization_context": {
                    "language": "python",  # Should be list
                },
            },
        }

        # Assumption
        assert not isinstance(agents["agent"]["specialization_context"]["language"], list)

        # Act
        errors = validate_schema(agents)

        # Assert
        assert len(errors) > 0
        assert any("must be a list" in err for err in errors)


class TestContextHashing:
    """Tests for calculate_context_hash function."""

    def test_context_hash_consistent(self) -> None:
        """
        GIVEN two identical specialization contexts
        WHEN calculate_context_hash is called
        THEN it should produce the same hash
        """
        # Arrange
        context1 = {"language": ["python"], "frameworks": ["pytest"]}
        context2 = {"language": ["python"], "frameworks": ["pytest"]}

        # Assumption
        assert context1 == context2

        # Act
        hash1 = calculate_context_hash(context1)
        hash2 = calculate_context_hash(context2)

        # Assert
        assert hash1 == hash2

    def test_context_hash_order_independent(self) -> None:
        """
        GIVEN two contexts with same values in different order
        WHEN calculate_context_hash is called
        THEN it should produce the same hash (order-independent)
        """
        # Arrange
        context1 = {"language": ["python", "go"]}
        context2 = {"language": ["go", "python"]}

        # Assumption
        assert set(context1["language"]) == set(context2["language"])

        # Act
        hash1 = calculate_context_hash(context1)
        hash2 = calculate_context_hash(context2)

        # Assert
        assert hash1 == hash2

    def test_context_hash_generalist(self) -> None:
        """
        GIVEN empty or None specialization context
        WHEN calculate_context_hash is called
        THEN it should return 'generalist'
        """
        # Arrange
        empty_context: dict[str, Any] = {}
        none_fields_context = {"language": None}

        # Assumption
        assert not empty_context

        # Act
        hash_empty = calculate_context_hash(empty_context)
        hash_none = calculate_context_hash(none_fields_context)

        # Assert
        assert hash_empty == "generalist"
        # None fields are ignored, so should also be generalist
        assert hash_none == "generalist"


class TestSpecialistRouting:
    """Tests for routing logic based on specialization_context."""

    def test_specialist_routes_to_pedro(self) -> None:
        """
        GIVEN Python files matching Pedro's specialization_context
        WHEN evaluating routing priority
        THEN Pedro should be matched (not Benny)
        """
        # Arrange - Pedro specializes in Python
        pedro = {
            "name": "python-pedro",
            "routing_priority": 75,
            "specialization_context": {
                "language": ["python"],
                "file_patterns": ["*.py", "requirements.txt"],
            },
        }

        benny = {
            "name": "backend-dev",
            "routing_priority": 50,
            "specialization_context": {
                "domain_keywords": ["backend", "api", "database"],
            },
        }

        # Assumption - Pedro has higher priority and matching context
        assert pedro["routing_priority"] > benny["routing_priority"]

        # Act - Check if file patterns match
        pedro_patterns = pedro["specialization_context"]["file_patterns"]
        test_file = "test_script.py"

        # Assert
        assert any(test_file.endswith(pattern.lstrip("*")) for pattern in pedro_patterns)

    def test_generalist_fallback(self) -> None:
        """
        GIVEN agent with no specialization_context
        WHEN validate_schema is called
        THEN it should only generate a warning (generalist is valid)
        """
        # Arrange
        agents = {
            "generalist": {
                "name": "generalist",
                "routing_priority": 30,
                # No specialization_context
            },
        }

        # Assumption
        assert "specialization_context" not in agents["generalist"]

        # Act
        errors = validate_schema(agents)

        # Assert - No errors, only warnings (handled in main() function)
        assert len(errors) == 0
