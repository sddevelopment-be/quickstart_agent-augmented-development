#!/usr/bin/env python3
"""
List agent specialization hierarchy and routing metadata.

Helper script for Manager Mike (and other orchestrating agents) to query
the agent hierarchy when applying the SELECT_APPROPRIATE_AGENT tactic.

Uses the domain layer (src/domain/doctrine/) for agent loading and parsing.

Usage:
    python tools/scripts/list_agent_hierarchy.py              # Show full hierarchy tree
    python tools/scripts/list_agent_hierarchy.py --json        # Machine-readable output
    python tools/scripts/list_agent_hierarchy.py --context python  # Filter by context keyword

Reference: DDR-011 (Agent Specialization Hierarchy)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Add paths so domain layer is importable
_repo_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_repo_root))
sys.path.insert(0, str(_repo_root / "src"))

from domain.doctrine.agent_loader import AgentProfileLoader
from domain.doctrine.models import Agent


def build_hierarchy(agents: dict[str, Agent]) -> dict[str, list[str]]:
    """Build parent -> children mapping."""
    children: dict[str, list[str]] = {}
    for agent in agents.values():
        if agent.specializes_from and agent.specializes_from in agents:
            children.setdefault(agent.specializes_from, []).append(agent.id)
    return children


def find_roots(agents: dict[str, Agent]) -> list[str]:
    """Find agents that have children but no parent (hierarchy roots)."""
    children_map = build_hierarchy(agents)
    parents_with_children = set(children_map.keys())
    agents_with_parents = {
        a.id for a in agents.values() if a.specializes_from in agents
    }
    return sorted(parents_with_children - agents_with_parents)


def print_tree(
    agents: dict[str, Agent],
    children_map: dict[str, list[str]],
    name: str,
    prefix: str = "",
    is_last: bool = True,
) -> None:
    """Print hierarchy tree for a given root agent."""
    agent = agents[name]
    connector = "└── " if is_last else "├── " if prefix else ""

    priority = agent.routing_priority if agent.routing_priority is not None else "—"
    max_tasks = agent.max_concurrent_tasks if agent.max_concurrent_tasks is not None else "—"
    source_tag = " [local]" if ".doctrine-config" in str(agent.source_file) else ""

    context_parts = []
    ctx = agent.specialization_context
    if ctx:
        if "language" in ctx:
            context_parts.append(", ".join(ctx["language"]))
        if "frameworks" in ctx:
            context_parts.append(", ".join(ctx["frameworks"][:3]))
    context_str = f" ({'; '.join(context_parts)})" if context_parts else ""

    print(
        f"{prefix}{connector}{name}{source_tag}  "
        f"[priority={priority}, max_tasks={max_tasks}]{context_str}"
    )

    kids = sorted(children_map.get(name, []))
    new_prefix = prefix + ("    " if is_last else "│   ") if prefix else "    "
    for i, child in enumerate(kids):
        print_tree(agents, children_map, child, new_prefix, i == len(kids) - 1)


def filter_by_context(agents: dict[str, Agent], keyword: str) -> dict[str, Agent]:
    """Filter agents whose specialization_context matches keyword."""
    keyword_lower = keyword.lower()
    matches: dict[str, Agent] = {}

    for agent in agents.values():
        ctx = agent.specialization_context
        if not ctx:
            continue
        for values in ctx.values():
            if isinstance(values, list) and any(
                keyword_lower in str(v).lower() for v in values
            ):
                matches[agent.id] = agent
                break

    return matches


def output_json(agents: dict[str, Agent]) -> None:
    """Output hierarchy as JSON for machine consumption."""
    children_map = build_hierarchy(agents)
    result = []
    for agent in sorted(agents.values(), key=lambda a: a.id):
        entry = {
            "name": agent.id,
            "source": "local" if ".doctrine-config" in str(agent.source_file) else "framework",
            "specializes_from": agent.specializes_from,
            "routing_priority": agent.routing_priority,
            "max_concurrent_tasks": agent.max_concurrent_tasks,
            "children": sorted(children_map.get(agent.id, [])),
        }
        if agent.specialization_context:
            entry["specialization_context"] = agent.specialization_context
        result.append(entry)

    print(json.dumps(result, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="List agent specialization hierarchy (DDR-011)"
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument(
        "--context",
        type=str,
        default=None,
        help="Filter agents by specialization context keyword (e.g., python, flask)",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root (default: auto-detect)",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve() if args.repo_root else _repo_root

    loader = AgentProfileLoader(repo_root=repo_root)
    agents = loader.load_all_profiles(include_local=True)

    if not agents:
        print("No agents found.", file=sys.stderr)
        return 1

    # Filter by context keyword if requested
    if args.context:
        matches = filter_by_context(agents, args.context)
        if args.json:
            output_json(matches)
        elif matches:
            print(f"Agents matching context '{args.context}':\n")
            for agent in sorted(matches.values(), key=lambda a: a.id):
                priority = agent.routing_priority if agent.routing_priority is not None else "—"
                parent = agent.specializes_from or "—"
                print(f"  {agent.id} [priority={priority}, parent={parent}]")
        else:
            print(f"No agents match context '{args.context}'.")
        return 0

    # Full output
    if args.json:
        output_json(agents)
        return 0

    children_map = build_hierarchy(agents)
    roots = find_roots(agents)
    standalone = sorted(
        a.id
        for a in agents.values()
        if a.id not in children_map and not a.specializes_from
    )

    framework_count = sum(
        1 for a in agents.values() if ".doctrine-config" not in str(a.source_file)
    )
    local_count = len(agents) - framework_count

    print("Agent Specialization Hierarchy")
    print("==============================")
    print(f"Total: {len(agents)} agents ({framework_count} framework, {local_count} local)")
    print()

    if roots:
        print("Hierarchy Trees:")
        print()
        for root in roots:
            print_tree(agents, children_map, root, "", True)
            print()

    if standalone:
        print(f"Standalone Agents ({len(standalone)}):")
        for name in standalone:
            agent = agents[name]
            priority = agent.routing_priority if agent.routing_priority is not None else "—"
            print(f"  {name} [priority={priority}]")

    return 0


if __name__ == "__main__":
    sys.exit(main())
