#!/usr/bin/env python3
"""
Validate agent specialization hierarchy relationships and prevent configuration errors.

Checks:
- Circular dependencies (A specializes B, B specializes A)
- Parent references exist
- Priority conflicts (two agents with same priority matching same context)
- Specialization context schema validity
- Routing priority bounds (0-100)
- Max concurrent tasks is positive integer

Reference: DDR-011 (Agent Specialization Hierarchy)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml


def load_agent_profile(path: Path) -> dict[str, Any] | None:
    """
    Load agent profile from markdown file with YAML frontmatter.

    Returns frontmatter dict or None if parsing fails.
    """
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()

        # Extract YAML frontmatter between --- markers
        if not content.startswith("---"):
            return None

        parts = content.split("---", 2)
        if len(parts) < 3:
            return None

        frontmatter = yaml.safe_load(parts[1])
        return frontmatter if isinstance(frontmatter, dict) else None

    except (OSError, yaml.YAMLError):
        return None


def discover_agents(repo_root: Path) -> dict[str, dict[str, Any]]:
    """
    Discover all agent profiles from doctrine/agents/ and .doctrine-config/custom-agents/.

    Returns dict mapping agent name to profile dict.
    """
    agents: dict[str, dict[str, Any]] = {}

    # Framework agents
    framework_agents_dir = repo_root / "doctrine" / "agents"
    if framework_agents_dir.exists():
        for agent_file in framework_agents_dir.glob("*.agent.md"):
            profile = load_agent_profile(agent_file)
            if profile and "name" in profile:
                profile["_source"] = "framework"
                profile["_path"] = str(agent_file)
                agents[profile["name"]] = profile

    # Local custom agents
    local_agents_dir = repo_root / ".doctrine-config" / "custom-agents"
    if local_agents_dir.exists():
        for agent_file in local_agents_dir.glob("*.agent.md"):
            profile = load_agent_profile(agent_file)
            if profile and "name" in profile:
                profile["_source"] = "local"
                profile["_path"] = str(agent_file)
                # Local agents override framework agents
                agents[profile["name"]] = profile

    return agents


def validate_schema(agents: dict[str, dict[str, Any]]) -> list[str]:
    """Validate specialization_context schema and required fields."""
    errors: list[str] = []

    for name, profile in agents.items():
        # routing_priority validation
        priority = profile.get("routing_priority")
        if priority is not None:
            if not isinstance(priority, int):
                errors.append(
                    f"{name}: routing_priority must be an integer (got {type(priority).__name__})"
                )
            elif not (0 <= priority <= 100):
                errors.append(
                    f"{name}: routing_priority must be 0-100 (got {priority})"
                )

        # max_concurrent_tasks validation
        max_tasks = profile.get("max_concurrent_tasks")
        if max_tasks is not None:
            if not isinstance(max_tasks, int):
                errors.append(
                    f"{name}: max_concurrent_tasks must be an integer (got {type(max_tasks).__name__})"
                )
            elif max_tasks <= 0:
                errors.append(
                    f"{name}: max_concurrent_tasks must be positive (got {max_tasks})"
                )

        # specialization_context validation
        context = profile.get("specialization_context")
        if context is not None:
            if not isinstance(context, dict):
                errors.append(
                    f"{name}: specialization_context must be a mapping (got {type(context).__name__})"
                )
                continue

            # Valid keys per DDR-011
            valid_keys = {
                "language",
                "frameworks",
                "file_patterns",
                "domain_keywords",
                "writing_style",
                "complexity_preference",
            }

            invalid_keys = set(context.keys()) - valid_keys
            if invalid_keys:
                errors.append(
                    f"{name}: invalid specialization_context keys: {sorted(invalid_keys)}"
                )

            # Type validation for known keys
            for key in ["language", "frameworks", "file_patterns", "domain_keywords", "writing_style", "complexity_preference"]:
                if key in context and not isinstance(context[key], list):
                    errors.append(
                        f"{name}: specialization_context.{key} must be a list"
                    )

    return errors


def detect_circular_dependencies(agents: dict[str, dict[str, Any]]) -> list[str]:
    """Detect circular parent-child relationships in agent hierarchy."""
    errors: list[str] = []

    def has_cycle(name: str, visited: set[str], stack: list[str]) -> bool:
        if name in stack:
            cycle = " → ".join(stack[stack.index(name):] + [name])
            errors.append(f"Circular dependency detected: {cycle}")
            return True

        if name in visited:
            return False

        visited.add(name)
        stack.append(name)

        parent_name = agents[name].get("specializes_from")
        if parent_name and parent_name in agents:
            has_cycle(parent_name, visited, stack)

        stack.pop()
        return False

    visited: set[str] = set()
    for agent_name in agents:
        if agent_name not in visited:
            has_cycle(agent_name, visited, [])

    return errors


def validate_parent_references(agents: dict[str, dict[str, Any]]) -> list[str]:
    """Validate that all parent references (specializes_from) exist."""
    errors: list[str] = []

    for name, profile in agents.items():
        parent_name = profile.get("specializes_from")
        if parent_name and parent_name not in agents:
            errors.append(
                f"{name}: parent agent '{parent_name}' not found (referenced in specializes_from)"
            )

    return errors


def calculate_context_hash(context: dict[str, Any]) -> str:
    """
    Calculate simple hash of specialization context for conflict detection.

    Two agents have conflicting contexts if they match the same domains.
    """
    if not context:
        return "generalist"

    # Sort all list values for consistent comparison
    parts: list[str] = []
    for key in sorted(context.keys()):
        value = context[key]
        if isinstance(value, list):
            parts.append(f"{key}:{','.join(sorted(str(v) for v in value))}")

    return "|".join(parts) if parts else "generalist"


def detect_priority_conflicts(agents: dict[str, dict[str, Any]]) -> list[str]:
    """
    Detect agents with identical priority matching same context.

    This would cause ambiguous routing decisions.
    """
    errors: list[str] = []

    # Group agents by (context_hash, routing_priority)
    conflicts: dict[tuple[str, int], list[str]] = {}

    for name, profile in agents.items():
        priority = profile.get("routing_priority", 50)  # Default per DDR-011
        context = profile.get("specialization_context", {})
        context_hash = calculate_context_hash(context)

        key = (context_hash, priority)
        if key not in conflicts:
            conflicts[key] = []
        conflicts[key].append(name)

    # Report conflicts
    for (context_hash, priority), agent_names in conflicts.items():
        if len(agent_names) > 1 and context_hash != "generalist":
            errors.append(
                f"Priority conflict: agents {sorted(agent_names)} have same priority ({priority}) "
                f"and overlapping context"
            )

    return errors


def find_hierarchy_relationships(agents: dict[str, dict[str, Any]]) -> list[tuple[str, str]]:
    """Find all parent-child relationships in hierarchy."""
    relationships: list[tuple[str, str]] = []

    for name, profile in agents.items():
        parent_name = profile.get("specializes_from")
        if parent_name and parent_name in agents:
            relationships.append((parent_name, name))

    return relationships


def validate_hierarchy(
    agents: dict[str, dict[str, Any]], verbose: bool = False
) -> tuple[bool, dict[str, list[str]]]:
    """
    Run all validation checks on agent hierarchy.

    Returns (success, checks_dict) where checks_dict maps check_name to errors.
    """
    checks: dict[str, list[str]] = {
        "schema": validate_schema(agents),
        "circular_dependencies": detect_circular_dependencies(agents),
        "parent_references": validate_parent_references(agents),
        "priority_conflicts": detect_priority_conflicts(agents),
    }

    success = all(not errors for errors in checks.values())
    return success, checks


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate agent specialization hierarchy (DDR-011)"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed validation information",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root directory (default: auto-detect from script location)",
    )
    args = parser.parse_args()

    # Determine repository root
    if args.repo_root:
        repo_root = args.repo_root.resolve()
    else:
        # Script is at tools/validators/validate-agent-hierarchy.py
        repo_root = Path(__file__).resolve().parent.parent.parent

    print("Agent Hierarchy Validation")
    print("==========================")

    # Discover agents
    agents = discover_agents(repo_root)

    framework_count = sum(1 for a in agents.values() if a.get("_source") == "framework")
    local_count = sum(1 for a in agents.values() if a.get("_source") == "local")

    print(f"Loaded: {len(agents)} agents ({framework_count} framework + {local_count} local)")

    # Find hierarchy relationships
    relationships = find_hierarchy_relationships(agents)
    print(f"Hierarchy: {len(relationships)} parent-child relationships found")

    if args.verbose and relationships:
        print("\nRelationships:")
        for parent, child in sorted(relationships):
            print(f"  {parent} ← {child}")

    # Run validation checks
    success, checks = validate_hierarchy(agents, verbose=args.verbose)

    print("\nChecks:")

    check_labels = {
        "circular_dependencies": "No circular dependencies",
        "parent_references": "All parent references valid",
        "priority_conflicts": "No priority conflicts",
        "schema": "Schema valid for all agents",
    }

    passed = 0
    failed = 0
    warnings = 0

    for check_name, errors in checks.items():
        label = check_labels.get(check_name, check_name)
        if errors:
            print(f"  [FAIL] {label}")
            failed += 1
            if args.verbose:
                for error in errors:
                    print(f"    - {error}")
        else:
            print(f"  [PASS] {label}")
            passed += 1

    # Check for agents without specialization_context (generalists)
    generalists = [
        name for name, profile in agents.items()
        if not profile.get("specialization_context")
    ]

    if generalists:
        print(f"  [WARN] {len(generalists)} agents have no specialization_context (generalist agents)")
        warnings += 1
        if args.verbose:
            for name in sorted(generalists):
                print(f"    - {name}")

    # Summary
    print(f"\nResult: {'PASSED' if success else 'FAILED'} ({passed} checks passed, {failed} failed, {warnings} warnings)")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
