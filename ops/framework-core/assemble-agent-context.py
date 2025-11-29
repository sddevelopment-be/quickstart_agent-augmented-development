#!/usr/bin/env python3
"""
Agent Context Assembler

Purpose: Emits a compact, ready-to-paste agent context to STDOUT.
Replaces assemble-agent-context.sh with improved maintainability.

Usage:
    python3 assemble-agent-context.py --agent backend-dev --mode minimal --directives 001 006
"""

import argparse
import subprocess
import sys
from pathlib import Path


class AgentContextAssembler:
    """Assembles agent context from various source files."""

    def __init__(self, repo_root: Path | None = None):
        """
        Initialize the assembler.

        Args:
            repo_root: Repository root path (defaults to auto-detect)
        """
        if repo_root:
            self.repo_root = Path(repo_root)
        else:
            # Auto-detect: assume script is in ops/framework-core
            self.repo_root = Path(__file__).parent.parent.parent

        self.agents_dir = self.repo_root / ".github" / "agents"
        self.runtime_sheet = self.agents_dir / "guidelines" / "runtime_sheet.md"
        self.general = self.agents_dir / "guidelines" / "general_guidelines.md"
        self.operational = self.agents_dir / "guidelines" / "operational_guidelines.md"
        self.aliases = self.agents_dir / "aliases.md"
        self.directive_loader = (
            self.repo_root / "ops" / "framework-core" / "load_directives.py"
        )

    def resolve_agent_path(self, agent: str) -> Path | None:
        """
        Resolve agent name or path to actual file.

        Args:
            agent: Agent basename (e.g., "backend-dev") or path

        Returns:
            Path to agent file, or None if not found
        """
        # If it's already a path and exists, use it
        agent_path = Path(agent)
        if agent_path.is_file():
            return agent_path

        # Try as basename in agents directory
        basename = agent.removesuffix(".agent.md")
        candidate = self.agents_dir / f"{basename}.agent.md"
        if candidate.is_file():
            return candidate

        return None

    def print_section(self, title: str, file_path: Path) -> None:
        """
        Print a section with file content.

        Args:
            title: Section title
            file_path: Path to file to include
        """
        if not file_path.is_file():
            print(f"[WARN] Skipping missing file: {file_path}", file=sys.stderr)
            return

        print(f"\n<!-- {title} -->")
        print(file_path.read_text(encoding="utf-8"))

    def load_directives(self, directive_codes: list[str]) -> str:
        """
        Load directives using the directive loader.

        Args:
            directive_codes: List of directive codes to load

        Returns:
            Loaded directive content
        """
        if not self.directive_loader.is_file():
            print(
                f"[WARN] Directive loader not found: {self.directive_loader}",
                file=sys.stderr,
            )
            return ""

        try:
            result = subprocess.run(
                [sys.executable, str(self.directive_loader)] + directive_codes,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"[WARN] Failed to load directives: {e}", file=sys.stderr)
            return ""

    def assemble(
        self,
        agent: str | None = None,
        mode: str = "minimal",
        directives: list[str] | None = None,
        include_aliases: bool = True,
    ) -> str:
        """
        Assemble agent context.

        Args:
            agent: Agent name or path
            mode: "minimal" or "full"
            directives: List of directive codes
            include_aliases: Whether to include aliases

        Returns:
            Assembled context as string
        """
        if not self.runtime_sheet.is_file():
            print(
                f"[ERROR] Missing runtime sheet at {self.runtime_sheet}",
                file=sys.stderr,
            )
            sys.exit(1)

        output = []
        output.append(f"<!-- Assembled agent context: {mode} mode -->")

        # Runtime sheet (always included)
        self._append_section(output, "Runtime Sheet", self.runtime_sheet)

        # Agent profile (if specified)
        if agent:
            agent_path = self.resolve_agent_path(agent)
            if agent_path:
                self._append_section(output, "Agent Profile", agent_path)
            else:
                print(f"[ERROR] Agent profile not found for '{agent}'", file=sys.stderr)
                sys.exit(1)

        # Aliases (if enabled)
        if include_aliases:
            self._append_section(output, "Aliases", self.aliases)

        # Directives (if any)
        if directives:
            output.append("\n<!-- Directives -->")
            directive_content = self.load_directives(directives)
            output.append(directive_content)

        # Full mode includes additional guidelines
        if mode == "full":
            self._append_section(output, "General Guidelines", self.general)
            self._append_section(output, "Operational Guidelines", self.operational)

        return "\n".join(output)

    def _append_section(self, output: list[str], title: str, file_path: Path) -> None:
        """
        Append a section to output list.

        Args:
            output: Output list to append to
            title: Section title
            file_path: Path to file to include
        """
        if not file_path.is_file():
            print(f"[WARN] Skipping missing file: {file_path}", file=sys.stderr)
            return

        output.append(f"\n<!-- {title} -->")
        output.append(file_path.read_text(encoding="utf-8"))


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description="Assemble agent context for copy-paste",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  assemble-agent-context.py --agent backend-dev --mode minimal --directives 001 006
  assemble-agent-context.py --mode full
        """,
    )

    parser.add_argument(
        "--agent",
        help="Agent name (e.g., 'backend-dev') or path to agent file",
    )

    parser.add_argument(
        "--mode",
        choices=["minimal", "full"],
        default="minimal",
        help="Context mode: minimal (default) or full",
    )

    parser.add_argument(
        "--directives",
        nargs="*",
        help="Directive codes to include (e.g., 001 006 014)",
    )

    parser.add_argument(
        "--no-aliases",
        action="store_true",
        help="Skip including aliases.md",
    )

    args = parser.parse_args()

    assembler = AgentContextAssembler()
    context = assembler.assemble(
        agent=args.agent,
        mode=args.mode,
        directives=args.directives or [],
        include_aliases=not args.no_aliases,
    )

    print(context)


if __name__ == "__main__":
    main()
