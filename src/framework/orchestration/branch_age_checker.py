#!/usr/bin/env python3
"""
Branch Age Checker

Purpose: Detect and warn about long-lived feature branches.
         Enforces trunk-based development discipline (ADR-019).

Usage:
    python ops/orchestration/branch_age_checker.py [BRANCH_NAME]
    
Options:
    BRANCH_NAME          Branch to check (default: current branch)
    --all                Check all branches except main
    --format FORMAT      Output format: text or json (default: text)
    --warning HOURS      Age threshold for warnings (default: 8)
    --error HOURS        Age threshold for errors (default: 24)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


class BranchAgeChecker:
    """Check branch age to enforce trunk-based development discipline."""

    def __init__(
        self,
        warning_threshold_hours: int = 8,
        error_threshold_hours: int = 24,
    ):
        """
        Initialize branch age checker.

        Args:
            warning_threshold_hours: Age threshold for warnings
            error_threshold_hours: Age threshold for errors
        """
        self.warning_threshold = warning_threshold_hours
        self.error_threshold = error_threshold_hours

    def get_current_branch(self) -> str | None:
        """
        Get current Git branch name.

        Returns:
            Branch name or None if detached HEAD
        """
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                check=True,
            )
            branch = result.stdout.strip()
            return branch if branch else None
        except subprocess.CalledProcessError:
            return None

    def get_branch_age_hours(self, branch: str) -> float | None:
        """
        Calculate branch age in hours from first commit not in main.

        Args:
            branch: Branch name

        Returns:
            Age in hours, or None if branch doesn't exist or is main
        """
        if branch == "main":
            return None

        try:
            # Get first commit on branch not in main
            result = subprocess.run(
                ["git", "log", "--format=%ct", f"main..{branch}"],
                capture_output=True,
                text=True,
                check=True,
            )
            commits = result.stdout.strip().split("\n")
            if not commits or not commits[0]:
                # No unique commits, branch is same as main
                return None

            # Get oldest commit timestamp (last in list)
            oldest_timestamp = int(commits[-1])
            now = datetime.now(timezone.utc).timestamp()
            age_seconds = now - oldest_timestamp
            return age_seconds / 3600

        except (subprocess.CalledProcessError, ValueError, IndexError):
            return None

    def get_all_branches(self) -> list[str]:
        """
        Get all local branches except main.

        Returns:
            List of branch names
        """
        try:
            result = subprocess.run(
                ["git", "branch", "--format=%(refname:short)"],
                capture_output=True,
                text=True,
                check=True,
            )
            branches = result.stdout.strip().split("\n")
            return [b for b in branches if b and b != "main"]
        except subprocess.CalledProcessError:
            return []

    def check_branch(self, branch: str) -> dict | None:
        """
        Check a single branch for age violations.

        Args:
            branch: Branch name

        Returns:
            Dict with branch info if violations found, None otherwise
        """
        age_hours = self.get_branch_age_hours(branch)
        if age_hours is None:
            return None

        status = "ok"
        severity = "info"

        if age_hours >= self.error_threshold:
            status = "error"
            severity = "error"
        elif age_hours >= self.warning_threshold:
            status = "warning"
            severity = "warning"

        return {
            "branch": branch,
            "age_hours": round(age_hours, 1),
            "status": status,
            "severity": severity,
            "warning_threshold": self.warning_threshold,
            "error_threshold": self.error_threshold,
        }

    def check_all_branches(self) -> list[dict]:
        """
        Check all branches for age violations.

        Returns:
            List of dicts with branch info
        """
        results = []
        for branch in self.get_all_branches():
            result = self.check_branch(branch)
            if result:
                results.append(result)
        return results

    def format_text_single(self, result: dict) -> str:
        """
        Format single branch check as text.

        Args:
            result: Branch check result dict

        Returns:
            Formatted text report
        """
        lines = []
        lines.append(f"Branch Age Check: {result['branch']}")
        lines.append("=" * 70)

        age_str = f"{result['age_hours']:.1f} hours"

        if result["status"] == "error":
            lines.append(f"❌ ERROR: Branch is {age_str} old")
            lines.append(
                f"   Threshold: {result['error_threshold']}h (maximum)"
            )
            lines.append("")
            lines.append("Action Required:")
            lines.append("  - Merge to trunk immediately, OR")
            lines.append("  - Abandon branch if work is outdated")
            lines.append("")
            lines.append("See ADR-019 for trunk-based development policy.")

        elif result["status"] == "warning":
            lines.append(f"⚠️  WARNING: Branch is {age_str} old")
            lines.append(
                f"   Threshold: {result['warning_threshold']}h (warning)"
            )
            lines.append("")
            lines.append("Recommendation:")
            lines.append("  - Plan to merge within next few hours")
            lines.append(
                f"  - Must merge before {result['error_threshold']}h"
            )

        else:
            lines.append(f"✅ OK: Branch is {age_str} old")
            lines.append(
                f"   Threshold: {result['warning_threshold']}h (warning), "
                f"{result['error_threshold']}h (maximum)"
            )

        return "\n".join(lines)

    def format_text_all(self, results: list[dict]) -> str:
        """
        Format all branch checks as text.

        Args:
            results: List of branch check result dicts

        Returns:
            Formatted text report
        """
        lines = []
        lines.append("Branch Age Report")
        lines.append("=" * 70)
        lines.append(
            f"Thresholds: {results[0]['warning_threshold']}h (warning), "
            f"{results[0]['error_threshold']}h (maximum)"
        )
        lines.append("")

        if not results:
            lines.append("✅ No branches to check.")
            return "\n".join(lines)

        errors = [r for r in results if r["status"] == "error"]
        warnings = [r for r in results if r["status"] == "warning"]
        ok = [r for r in results if r["status"] == "ok"]

        if errors:
            lines.append(f"❌ {len(errors)} branch(es) exceed maximum age:")
            for result in sorted(errors, key=lambda r: r["age_hours"], reverse=True):
                lines.append(
                    f"   {result['branch']:40} {result['age_hours']:>6.1f}h"
                )
            lines.append("")

        if warnings:
            lines.append(f"⚠️  {len(warnings)} branch(es) exceed warning threshold:")
            for result in sorted(
                warnings, key=lambda r: r["age_hours"], reverse=True
            ):
                lines.append(
                    f"   {result['branch']:40} {result['age_hours']:>6.1f}h"
                )
            lines.append("")

        if ok:
            lines.append(f"✅ {len(ok)} branch(es) within acceptable age:")
            for result in sorted(ok, key=lambda r: r["age_hours"], reverse=True):
                lines.append(
                    f"   {result['branch']:40} {result['age_hours']:>6.1f}h"
                )
            lines.append("")

        if errors:
            lines.append("=" * 70)
            lines.append("Action Required:")
            lines.append("  - Merge or abandon branches exceeding maximum age")
            lines.append("  - See ADR-019 for trunk-based development policy")

        return "\n".join(lines)

    def format_json(self, results: dict | list[dict]) -> str:
        """
        Format branch check(s) as JSON.

        Args:
            results: Single result dict or list of result dicts

        Returns:
            JSON string
        """
        if isinstance(results, dict):
            # Single branch
            return json.dumps(results, indent=2)
        else:
            # Multiple branches
            errors = [r for r in results if r["status"] == "error"]
            warnings = [r for r in results if r["status"] == "warning"]

            report = {
                "total_branches": len(results),
                "errors": len(errors),
                "warnings": len(warnings),
                "has_violations": len(errors) > 0,
                "branches": results,
            }
            return json.dumps(report, indent=2)


def main() -> int:
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description="Check branch age to enforce trunk-based development",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "branch",
        nargs="?",
        help="Branch name to check (default: current branch)",
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Check all branches except main",
    )

    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    parser.add_argument(
        "--warning",
        type=int,
        default=8,
        help="Age threshold for warnings in hours (default: 8)",
    )

    parser.add_argument(
        "--error",
        type=int,
        default=24,
        help="Age threshold for errors in hours (default: 24)",
    )

    args = parser.parse_args()

    checker = BranchAgeChecker(
        warning_threshold_hours=args.warning,
        error_threshold_hours=args.error,
    )

    if args.all:
        # Check all branches
        results = checker.check_all_branches()
        if args.format == "json":
            print(checker.format_json(results))
        else:
            print(checker.format_text_all(results))

        # Exit with error if any branch exceeds maximum
        has_errors = any(r["status"] == "error" for r in results)
        return 1 if has_errors else 0

    else:
        # Check single branch
        branch = args.branch or checker.get_current_branch()
        if not branch:
            print("Error: Not on a branch (detached HEAD)")
            return 1

        if branch == "main":
            print("Branch 'main' is the trunk and has no age limit.")
            return 0

        result = checker.check_branch(branch)
        if not result:
            print(f"Branch '{branch}' has no unique commits (same as main)")
            return 0

        if args.format == "json":
            print(checker.format_json(result))
        else:
            print(checker.format_text_single(result))

        # Exit with error if branch exceeds maximum
        return 1 if result["status"] == "error" else 0


if __name__ == "__main__":
    sys.exit(main())
