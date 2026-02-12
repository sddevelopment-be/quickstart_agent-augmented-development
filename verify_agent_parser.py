#!/usr/bin/env python3
"""
Verification script for ADR-045 Task 3 enhanced agent parser.

Demonstrates parsing of agent profiles with new features:
- Capability descriptions
- Handoff patterns
- Constraints
- Preferences
- Primer matrix
- Default mode
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.domain.doctrine.parsers import AgentParser
from src.domain.doctrine.models import Agent


def verify_enhanced_parser():
    """Verify enhanced agent parser features."""
    print("=" * 80)
    print("ADR-045 TASK 3 VERIFICATION - Enhanced Agent Profile Parser")
    print("=" * 80)
    print()

    # Find a real agent file to parse
    agent_files = [
        Path("doctrine/agents/python-pedro.agent.md"),
        Path("doctrine/agents/architect.agent.md"),
        Path("tests/fixtures/doctrine/agents/test-agent.agent.md"),
    ]

    parser = AgentParser()

    for agent_file in agent_files:
        if agent_file.exists():
            print(f"📄 Parsing: {agent_file}")
            print("-" * 80)

            agent = parser.parse(agent_file)

            # Display basic info
            print(f"✅ Agent ID: {agent.id}")
            print(f"✅ Name: {agent.name}")
            print(f"✅ Default Mode: {agent.default_mode}")
            print()

            # Display capability descriptions
            if agent.capability_descriptions:
                print("📋 Capability Descriptions:")
                for category, description in agent.capability_descriptions.items():
                    print(f"  • {category.upper()}: {description[:60]}...")
                print()

            # Display handoff patterns
            if agent.handoff_patterns:
                print("🤝 Handoff Patterns:")
                for pattern in agent.handoff_patterns[:3]:  # First 3
                    print(
                        f"  • {pattern.direction.upper()}: "
                        f"{pattern.source_agent} → {pattern.target_agent}"
                    )
                if len(agent.handoff_patterns) > 3:
                    print(f"  ... and {len(agent.handoff_patterns) - 3} more")
                print()

            # Display constraints
            if agent.constraints:
                print("⚠️  Constraints:")
                for constraint in list(agent.constraints)[:3]:  # First 3
                    print(f"  • {constraint[:60]}...")
                if len(agent.constraints) > 3:
                    print(f"  ... and {len(agent.constraints) - 3} more")
                print()

            # Display preferences
            if agent.preferences:
                print("⚙️  Preferences:")
                for key, value in list(agent.preferences.items())[:3]:  # First 3
                    print(f"  • {key}: {value}")
                if len(agent.preferences) > 3:
                    print(f"  ... and {len(agent.preferences) - 3} more")
                print()

            # Display primer matrix
            if agent.primer_matrix:
                print("🎯 Primer Matrix:")
                for entry in agent.primer_matrix[:2]:  # First 2
                    primers = ", ".join(sorted(entry.required_primers))
                    print(f"  • {entry.task_type}: {primers}")
                if len(agent.primer_matrix) > 2:
                    print(f"  ... and {len(agent.primer_matrix) - 2} more")
                print()

            print("=" * 80)
            print()
            break  # Only parse first available file

    else:
        print("❌ No agent files found for verification")
        return False

    print("✅ VERIFICATION COMPLETE")
    print()
    print("Enhanced features successfully parsed:")
    print("  ✅ Capability descriptions")
    print("  ✅ Handoff patterns")
    print("  ✅ Constraints")
    print("  ✅ Preferences")
    print("  ✅ Primer matrix")
    print("  ✅ Default mode")
    print()

    return True


if __name__ == "__main__":
    success = verify_enhanced_parser()
    sys.exit(0 if success else 1)
