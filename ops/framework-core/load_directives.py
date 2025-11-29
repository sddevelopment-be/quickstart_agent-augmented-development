#!/usr/bin/env python3
"""
Directive Loader

Purpose: On-demand inclusion of externalized directive markdown blocks.
Replaces load_directives.sh with improved type safety and testability.

Usage:
    python3 load_directives.py 001 006
    python3 load_directives.py --list
"""

import argparse
import sys
from pathlib import Path


class DirectiveLoader:
    """Loads directive markdown files by code."""

    def __init__(self, directives_dir: Path):
        """
        Initialize directive loader.

        Args:
            directives_dir: Path to directory containing directive files
        """
        self.directives_dir = Path(directives_dir)

    def list_directives(self) -> list[dict[str, str]]:
        """
        List all available directives.

        Returns:
            List of dicts with 'code' and 'filename' keys
        """
        directives = []
        for file_path in sorted(self.directives_dir.glob("*_*.md")):
            code = self._extract_code(file_path.name)
            if code:
                directives.append({"code": code, "filename": file_path.name})
        return directives

    def load_directives(self, codes: list[str]) -> str:
        """
        Load one or more directives by code.

        Args:
            codes: List of directive codes to load

        Returns:
            Concatenated directive content with markers
        """
        output = []
        for code in codes:
            file_path = self._find_directive_file(code)
            if file_path is None:
                print(f"[WARN] No directive found for code {code}", file=sys.stderr)
                continue

            content = file_path.read_text(encoding="utf-8")
            formatted = self._format_directive(code, content)
            output.append(formatted)

        return "".join(output)

    def _find_directive_file(self, code: str) -> Path | None:
        """
        Find directive file by code.

        Args:
            code: Directive code (e.g., "001", "014")

        Returns:
            Path to directive file, or None if not found
        """
        # Look for files matching pattern: {code}_*.md
        matches = list(self.directives_dir.glob(f"{code}_*.md"))
        if matches:
            return matches[0]
        return None

    def _extract_code(self, filename: str) -> str | None:
        """
        Extract directive code from filename.

        Args:
            filename: Name of directive file (e.g., "001_cli_shell_tooling.md")

        Returns:
            Directive code or None if invalid format
        """
        if "_" not in filename:
            return None
        code = filename.split("_")[0]
        return code if code.isdigit() else None

    def _format_directive(self, code: str, content: str) -> str:
        """
        Format directive content with markers.

        Args:
            code: Directive code
            content: Directive markdown content

        Returns:
            Formatted content with begin/end markers
        """
        return f"\n<!-- Directive {code} Begin -->\n{content}\n<!-- Directive {code} End -->\n"


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description="Load directive markdown files by code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  load_directives.py 001 006
  load_directives.py --list
        """,
    )

    parser.add_argument(
        "--list", action="store_true", help="List all available directives"
    )

    parser.add_argument(
        "codes",
        nargs="*",
        help="Directive codes to load (e.g., 001 006 014)",
    )

    parser.add_argument(
        "--directives-dir",
        type=Path,
        help="Path to directives directory (default: .github/agents/directives)",
    )

    args = parser.parse_args()

    # Determine directives directory
    if args.directives_dir:
        directives_dir = args.directives_dir
    else:
        # Default: assume script is in ops/framework-core, go up to repo root
        script_dir = Path(__file__).parent
        repo_root = script_dir.parent.parent
        directives_dir = repo_root / ".github" / "agents" / "directives"

    if not directives_dir.exists():
        print(
            f"[ERROR] Directives directory not found: {directives_dir}", file=sys.stderr
        )
        sys.exit(1)

    loader = DirectiveLoader(directives_dir)

    if args.list:
        # List mode
        print("Available directives (code : filename)")
        for directive in loader.list_directives():
            print(f"  {directive['code']} : {directive['filename']}")
        sys.exit(0)

    if not args.codes:
        parser.print_help()
        sys.exit(1)

    # Load directives
    content = loader.load_directives(args.codes)
    print(content, end="")


if __name__ == "__main__":
    main()
