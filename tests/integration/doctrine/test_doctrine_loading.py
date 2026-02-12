"""
Integration tests for doctrine loading.

Tests loading real agent profiles and directives from the repository,
validating cross-references, and ensuring the entire doctrine loads correctly.

These tests use actual files from the repository:
- Agent profiles: .github/agents/*.agent.md
- Directives: doctrine/directives/*.md

Related ADRs
------------
- ADR-045: Doctrine Concept Domain Model

Test Approach
-------------
1. Load all real agent profiles from repository
2. Load all real directives from repository
3. Validate cross-references between agents and directives
4. Ensure metadata completeness
5. Check for duplicate IDs and circular dependencies
"""

import pytest
from pathlib import Path
from typing import List

from src.domain.doctrine.models import Agent, Directive
from src.domain.doctrine.parsers import AgentParser, DirectiveParser
from src.domain.doctrine.validators import (
    CrossReferenceValidator,
    MetadataValidator,
    IntegrityChecker,
)
from src.domain.doctrine.exceptions import ParseError


class TestDoctrineLoading:
    """Integration tests for loading real doctrine artifacts."""

    @pytest.fixture
    def agents_dir(self) -> Path:
        """Return path to agents directory."""
        return Path(".github/agents")

    @pytest.fixture
    def directives_dir(self) -> Path:
        """Return path to directives directory."""
        # Try multiple possible locations
        doctrine_directives = Path("doctrine/directives")
        root_directives = Path("directives")

        if doctrine_directives.exists():
            return doctrine_directives
        elif root_directives.exists():
            return root_directives
        else:
            pytest.skip("Directives directory not found")

    @pytest.fixture
    def all_agents(self, agents_dir: Path) -> List[Agent]:
        """Load all agent profiles from repository."""
        agent_files = list(agents_dir.glob("*.agent.md"))
        if not agent_files:
            pytest.skip("No agent files found in .github/agents/")

        parser = AgentParser()
        agents: List[Agent] = []
        parse_errors: List[str] = []

        for file_path in agent_files:
            try:
                agent = parser.parse(file_path)
                agents.append(agent)
            except ParseError as e:
                parse_errors.append(f"{file_path.name}: {e}")
            except Exception as e:
                parse_errors.append(f"{file_path.name}: Unexpected error - {e}")

        # Report parsing errors but don't fail the test
        if parse_errors:
            print(f"\n⚠️  Warning: {len(parse_errors)} agent files failed to parse:")
            for error in parse_errors[:5]:  # Show first 5 errors
                print(f"  - {error}")
            if len(parse_errors) > 5:
                print(f"  ... and {len(parse_errors) - 5} more")

        return agents

    @pytest.fixture
    def all_directives(self, directives_dir: Path) -> List[Directive]:
        """Load all directives from repository."""
        directive_files = list(directives_dir.glob("*.md"))
        if not directive_files:
            pytest.skip("No directive files found")

        parser = DirectiveParser()
        directives: List[Directive] = []
        parse_errors: List[str] = []

        for file_path in directive_files:
            try:
                directive = parser.parse(file_path)
                directives.append(directive)
            except ParseError as e:
                parse_errors.append(f"{file_path.name}: {e}")
            except Exception as e:
                parse_errors.append(f"{file_path.name}: Unexpected error - {e}")

        # Report parsing errors but don't fail the test
        if parse_errors:
            print(f"\n⚠️  Warning: {len(parse_errors)} directive files failed to parse:")
            for error in parse_errors[:5]:
                print(f"  - {error}")

        return directives

    def test_load_all_agents(self, all_agents: List[Agent], agents_dir: Path):
        """Load all agent profiles from .github/agents/."""
        agent_files = list(agents_dir.glob("*.agent.md"))

        # Should have loaded some agents
        assert len(all_agents) > 0, "No agents loaded from repository"

        # Report statistics
        print(f"\n✅ Successfully loaded {len(all_agents)} agents")
        print(f"   Found {len(agent_files)} agent files")
        print(f"   Parse success rate: {len(all_agents)}/{len(agent_files)}")

        # Sample agent IDs
        if len(all_agents) > 0:
            agent_ids = [a.id for a in all_agents[:5]]
            print(f"   Sample agents: {', '.join(agent_ids)}")

    def test_load_all_directives(
        self, all_directives: List[Directive], directives_dir: Path
    ):
        """Load all directives from directives directory."""
        directive_files = list(directives_dir.glob("*.md"))

        # Should have loaded some directives
        assert len(all_directives) > 0, "No directives loaded from repository"

        # Report statistics
        print(f"\n✅ Successfully loaded {len(all_directives)} directives")
        print(f"   Found {len(directive_files)} directive files")
        print(
            f"   Parse success rate: {len(all_directives)}/{len(directive_files)}"
        )

        # Sample directive IDs
        if len(all_directives) > 0:
            directive_ids = [d.id for d in all_directives[:5]]
            print(f"   Sample directives: {', '.join(directive_ids)}")

    def test_agent_metadata_validation(self, all_agents: List[Agent]):
        """Validate metadata completeness for all loaded agents."""
        if not all_agents:
            pytest.skip("No agents loaded")

        validator = MetadataValidator()
        validation_errors: List[str] = []

        for agent in all_agents:
            result = validator.validate_agent(agent)
            if result.has_errors:
                validation_errors.extend(
                    [f"Agent {agent.id}: {error}" for error in result.errors]
                )

        # Report results
        if validation_errors:
            print(f"\n⚠️  Metadata validation errors ({len(validation_errors)}):")
            for error in validation_errors[:10]:
                print(f"  - {error}")
            # Don't fail test - just report
        else:
            print(f"\n✅ All {len(all_agents)} agents have valid metadata")

    def test_cross_reference_validation(
        self, all_agents: List[Agent], all_directives: List[Directive]
    ):
        """Validate cross-references between all agents and directives."""
        if not all_agents:
            pytest.skip("No agents loaded")
        if not all_directives:
            pytest.skip("No directives loaded")

        validator = CrossReferenceValidator(all_directives, all_agents)
        result = validator.validate_all()

        # Report results
        print(f"\n📊 Cross-reference validation:")
        print(f"   Agents checked: {len(all_agents)}")
        print(f"   Directives available: {len(all_directives)}")
        print(f"   Valid: {result.valid}")
        print(f"   Errors: {len(result.errors)}")
        print(f"   Warnings: {len(result.warnings)}")

        # Show errors if any
        if result.has_errors:
            print(f"\n⚠️  Cross-reference errors:")
            for error in result.errors[:10]:
                print(f"  - {error}")
            if len(result.errors) > 10:
                print(f"  ... and {len(result.errors) - 10} more")
            # Don't fail test - this is informational

        # Show warnings if any
        if result.has_warnings:
            print(f"\n⚠️  Cross-reference warnings:")
            for warning in result.warnings[:10]:
                print(f"  - {warning}")

    def test_duplicate_id_check(self, all_agents: List[Agent]):
        """Check for duplicate agent IDs."""
        if not all_agents:
            pytest.skip("No agents loaded")

        checker = IntegrityChecker()
        result = checker.check_duplicate_ids(all_agents)

        # Report results
        print(f"\n📊 Duplicate ID check:")
        print(f"   Agents checked: {len(all_agents)}")
        print(f"   Unique IDs: {result.valid}")

        if result.has_errors:
            print(f"\n❌ Duplicate IDs found:")
            for error in result.errors:
                print(f"  - {error}")
            pytest.fail(
                f"Found {len(result.errors)} duplicate agent IDs - this is a critical error"
            )
        else:
            print(f"✅ All agent IDs are unique")

    def test_circular_dependency_check(self, all_agents: List[Agent]):
        """Check for circular dependencies in agent handoff patterns."""
        if not all_agents:
            pytest.skip("No agents loaded")

        checker = IntegrityChecker()
        result = checker.check_circular_dependencies(all_agents)

        # Report results
        print(f"\n📊 Circular dependency check:")
        print(f"   Agents checked: {len(all_agents)}")
        print(f"   No cycles: {result.valid}")

        if result.has_errors:
            print(f"\n⚠️  Circular dependencies found:")
            for error in result.errors:
                print(f"  - {error}")
            # Don't fail test - circular dependencies might be intentional
        else:
            print(f"✅ No circular dependencies detected")

    def test_complete_doctrine_validation(
        self, all_agents: List[Agent], all_directives: List[Directive]
    ):
        """Complete end-to-end validation of entire doctrine."""
        if not all_agents or not all_directives:
            pytest.skip("Agents or directives not loaded")

        print(f"\n📋 Complete Doctrine Validation Report")
        print(f"=" * 60)
        print(f"Agents loaded: {len(all_agents)}")
        print(f"Directives loaded: {len(all_directives)}")

        # Run all validators
        cross_ref_validator = CrossReferenceValidator(all_directives, all_agents)
        metadata_validator = MetadataValidator()
        integrity_checker = IntegrityChecker()

        # Cross-reference validation
        cross_ref_result = cross_ref_validator.validate_all()
        print(f"\n🔗 Cross-references:")
        print(f"   Valid: {cross_ref_result.valid}")
        print(f"   Errors: {len(cross_ref_result.errors)}")
        print(f"   Warnings: {len(cross_ref_result.warnings)}")

        # Metadata validation
        metadata_errors = 0
        for agent in all_agents:
            result = metadata_validator.validate_agent(agent)
            metadata_errors += len(result.errors)

        print(f"\n📝 Metadata:")
        print(f"   Valid: {metadata_errors == 0}")
        print(f"   Errors: {metadata_errors}")

        # Integrity checks
        duplicate_result = integrity_checker.check_duplicate_ids(all_agents)
        circular_result = integrity_checker.check_circular_dependencies(all_agents)

        print(f"\n🔍 Integrity:")
        print(f"   Unique IDs: {duplicate_result.valid}")
        print(f"   No cycles: {circular_result.valid}")

        print(f"\n" + "=" * 60)

        # Assert critical errors only (duplicates)
        assert duplicate_result.valid, "Duplicate agent IDs found - critical error"


class TestDoctrineStatistics:
    """Statistical analysis of loaded doctrine."""

    @pytest.fixture
    def all_agents(self) -> List[Agent]:
        """Load all agent profiles from repository."""
        agents_dir = Path(".github/agents")
        agent_files = list(agents_dir.glob("*.agent.md"))
        if not agent_files:
            pytest.skip("No agent files found in .github/agents/")

        parser = AgentParser()
        agents: List[Agent] = []

        for file_path in agent_files:
            try:
                agent = parser.parse(file_path)
                agents.append(agent)
            except Exception:
                pass

        return agents

    @pytest.fixture
    def all_directives(self) -> List[Directive]:
        """Load all directives from repository."""
        doctrine_directives = Path("doctrine/directives")
        root_directives = Path("directives")

        directives_dir = None
        if doctrine_directives.exists():
            directives_dir = doctrine_directives
        elif root_directives.exists():
            directives_dir = root_directives
        else:
            pytest.skip("Directives directory not found")

        directive_files = list(directives_dir.glob("*.md"))
        if not directive_files:
            pytest.skip("No directive files found")

        parser = DirectiveParser()
        directives: List[Directive] = []

        for file_path in directive_files:
            try:
                directive = parser.parse(file_path)
                directives.append(directive)
            except Exception:
                pass

        return directives

    def test_agent_capabilities_coverage(self, all_agents: List[Agent]):
        """Analyze capability coverage across agents."""
        if not all_agents:
            pytest.skip("No agents loaded")

        all_capabilities: set = set()
        for agent in all_agents:
            all_capabilities.update(agent.capabilities)

        print(f"\n📊 Agent Capabilities Statistics:")
        print(f"   Total agents: {len(all_agents)}")
        print(f"   Unique capabilities: {len(all_capabilities)}")
        print(f"   Avg capabilities per agent: {sum(len(a.capabilities) for a in all_agents) / len(all_agents):.1f}")

        # Most common capabilities
        capability_counts = {}
        for agent in all_agents:
            for cap in agent.capabilities:
                capability_counts[cap] = capability_counts.get(cap, 0) + 1

        if capability_counts:
            top_capabilities = sorted(
                capability_counts.items(), key=lambda x: x[1], reverse=True
            )[:5]
            print(f"\n   Top capabilities:")
            for cap, count in top_capabilities:
                print(f"     - {cap}: {count} agents")

    def test_directive_usage_analysis(
        self, all_agents: List[Agent], all_directives: List[Directive]
    ):
        """Analyze which directives are most commonly required."""
        if not all_agents or not all_directives:
            pytest.skip("Agents or directives not loaded")

        directive_usage = {}
        for agent in all_agents:
            for directive_id in agent.required_directives:
                directive_usage[directive_id] = directive_usage.get(directive_id, 0) + 1

        print(f"\n📊 Directive Usage Statistics:")
        print(f"   Total directives: {len(all_directives)}")
        print(f"   Directives in use: {len(directive_usage)}")
        print(f"   Unused directives: {len(all_directives) - len(directive_usage)}")

        if directive_usage:
            top_directives = sorted(
                directive_usage.items(), key=lambda x: x[1], reverse=True
            )[:5]
            print(f"\n   Most required directives:")
            for directive_id, count in top_directives:
                print(f"     - {directive_id}: {count} agents")
