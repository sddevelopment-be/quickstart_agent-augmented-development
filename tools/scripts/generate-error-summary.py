#!/usr/bin/env python3
"""
Agent-Friendly Error Summary Generator for GitHub Actions

Aggregates validation errors from multiple sources and generates:
1. Structured JSON for programmatic access
2. Markdown summary for human/agent readability
3. GitHub Actions annotations for inline feedback

Usage:
    python generate-error-summary.py \
        --output-json errors.json \
        --output-markdown errors.md \
        --workflow "Work Directory Validation" \
        --job "validate"

Input: Reads from GITHUB_STEP_SUMMARY environment or stdin
Output: JSON artifact + Markdown summary + exit code

Design: ADR-028 compliant, test-first bug fixing for CI/CD
Context: Directive 001 (CLI & Shell Tooling), Directive 018 (Documentation Level)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Literal


@dataclass
class ErrorLocation:
    """Location information for an error."""
    file_path: str | None = None
    line_number: int | None = None
    column_number: int | None = None
    context_lines: list[str] = field(default_factory=list)


@dataclass
class ErrorSuggestion:
    """Suggested fix for an error."""
    description: str
    diff: str | None = None
    command: str | None = None


@dataclass
class ValidationError:
    """Structured validation error for agent consumption."""
    
    # Core fields
    error_id: str  # Unique identifier
    error_type: str  # validation_failure, schema_error, syntax_error, etc.
    severity: Literal["error", "warning", "info"]
    message: str  # Human-readable error message
    
    # Context
    validator: str  # Which validator produced this error
    timestamp: str  # ISO8601 with Z suffix
    
    # Location
    location: ErrorLocation | None = None
    
    # Fix suggestions
    suggestions: list[ErrorSuggestion] = field(default_factory=list)
    
    # Additional metadata
    raw_output: str | None = None  # Original error text
    documentation_url: str | None = None
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = asdict(self)
        # Convert nested dataclasses
        if self.location:
            result["location"] = asdict(self.location)
        if self.suggestions:
            result["suggestions"] = [asdict(s) for s in self.suggestions]
        return result
    
    def to_github_annotation(self) -> str:
        """Format as GitHub Actions workflow command for inline annotation."""
        level = "error" if self.severity == "error" else "warning"
        message = self.message.replace("\n", "%0A")
        
        if self.location and self.location.file_path:
            parts = [f"file={self.location.file_path}"]
            if self.location.line_number:
                parts.append(f"line={self.location.line_number}")
            if self.location.column_number:
                parts.append(f"col={self.location.column_number}")
            location_str = ",".join(parts)
            return f"::{level} {location_str}::{message}"
        else:
            return f"::{level}::{message}"
    
    def to_markdown(self) -> str:
        """Format as markdown for human/agent readability."""
        icon = "❌" if self.severity == "error" else "⚠️"
        lines = [f"{icon} **{self.error_type}**: {self.message}"]
        
        if self.location and self.location.file_path:
            loc_parts = [f"📁 `{self.location.file_path}`"]
            if self.location.line_number:
                loc_parts.append(f"Line {self.location.line_number}")
            lines.append("  - " + ", ".join(loc_parts))
        
        if self.suggestions:
            lines.append("\n  **Suggested fixes:**")
            for i, suggestion in enumerate(self.suggestions, 1):
                lines.append(f"  {i}. {suggestion.description}")
                if suggestion.command:
                    lines.append(f"     ```bash\n     {suggestion.command}\n     ```")
        
        if self.documentation_url:
            lines.append(f"\n  📚 [Documentation]({self.documentation_url})")
        
        return "\n".join(lines)


@dataclass
class ErrorSummary:
    """Complete error summary for a workflow run."""
    
    workflow: str
    job: str
    run_id: str | None = None
    run_url: str | None = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    
    errors: list[ValidationError] = field(default_factory=list)
    
    def add_error(self, error: ValidationError) -> None:
        """Add an error to the summary."""
        self.errors.append(error)
    
    def error_count(self) -> int:
        """Count of errors."""
        return sum(1 for e in self.errors if e.severity == "error")
    
    def warning_count(self) -> int:
        """Count of warnings."""
        return sum(1 for e in self.errors if e.severity == "warning")
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "workflow": self.workflow,
            "job": self.job,
            "run_id": self.run_id,
            "run_url": self.run_url,
            "timestamp": self.timestamp,
            "summary": {
                "total_errors": self.error_count(),
                "total_warnings": self.warning_count(),
                "total_issues": len(self.errors),
            },
            "errors": [e.to_dict() for e in self.errors],
        }
    
    def to_json(self, pretty: bool = True) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2 if pretty else None)
    
    def to_markdown(self) -> str:
        """Generate markdown summary."""
        lines = [
            f"# 🔍 Error Summary: {self.workflow}",
            "",
            f"**Job:** {self.job}",
            f"**Timestamp:** {self.timestamp}",
        ]
        
        if self.run_url:
            lines.append(f"**Run:** [View Full Logs]({self.run_url})")
        
        lines.append("")
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- ❌ **Errors:** {self.error_count()}")
        lines.append(f"- ⚠️ **Warnings:** {self.warning_count()}")
        lines.append(f"- 📊 **Total Issues:** {len(self.errors)}")
        lines.append("")
        
        if not self.errors:
            lines.append("✅ No issues found!")
            return "\n".join(lines)
        
        # Group by validator
        by_validator: dict[str, list[ValidationError]] = {}
        for error in self.errors:
            by_validator.setdefault(error.validator, []).append(error)
        
        lines.append("## Issues by Validator")
        lines.append("")
        
        for validator, errors_list in sorted(by_validator.items()):
            error_count = sum(1 for e in errors_list if e.severity == "error")
            warning_count = sum(1 for e in errors_list if e.severity == "warning")
            
            lines.append(f"### {validator}")
            lines.append(f"*{error_count} errors, {warning_count} warnings*")
            lines.append("")
            
            for error in errors_list:
                lines.append(error.to_markdown())
                lines.append("")
        
        lines.append("---")
        lines.append("*Generated by Agent-Friendly Error Reporter*")
        
        return "\n".join(lines)
    
    def emit_github_annotations(self) -> None:
        """Emit GitHub Actions workflow commands for inline annotations."""
        for error in self.errors:
            print(error.to_github_annotation())


class ErrorParser:
    """Parse validation output into structured errors."""
    
    @staticmethod
    def parse_validation_line(line: str, validator: str) -> ValidationError | None:
        """Parse a single validation error line."""
        # Example formats:
        # "❌ work/path/file.yaml: invalid status 'foo', expected one of ['done', 'error']"
        # "❗️ Missing required directory: work/collaboration"
        # "⚠️ Agent 'danny' missing directory under work/collaboration/assigned/"
        
        if not any(marker in line for marker in ["❌", "❗️", "⚠️", "ERROR:", "FAIL:"]):
            return None
        
        severity = "error"
        if "⚠️" in line:
            severity = "warning"
        
        # Extract file path if present
        file_path = None
        line_number = None
        parts = line.split(":")
        
        if len(parts) >= 2 and "/" in parts[0]:
            potential_path = parts[0].replace("❌", "").replace("❗️", "").replace("⚠️", "").strip()
            if Path(potential_path).exists() or "/" in potential_path:
                file_path = potential_path
                # Check for line number
                if parts[1].strip().isdigit():
                    line_number = int(parts[1].strip())
        
        # Extract message
        message = line
        for marker in ["❌", "❗️", "⚠️"]:
            message = message.replace(marker, "").strip()
        
        error_id = f"{validator}_{abs(hash(line)) % 10000:04d}"
        
        location = ErrorLocation(
            file_path=file_path,
            line_number=line_number,
        ) if file_path else None
        
        return ValidationError(
            error_id=error_id,
            error_type="validation_failure",
            severity=severity,
            message=message,
            validator=validator,
            timestamp=datetime.utcnow().isoformat() + "Z",
            location=location,
            raw_output=line,
        )
    
    @staticmethod
    def parse_python_validator_output(output: str, validator: str) -> list[ValidationError]:
        """Parse Python validator output (like validate-task-schema.py)."""
        errors = []
        
        for line in output.split("\n"):
            error = ErrorParser.parse_validation_line(line, validator)
            if error:
                errors.append(error)
        
        return errors
    
    @staticmethod
    def parse_shell_validator_output(output: str, validator: str) -> list[ValidationError]:
        """Parse shell script validator output."""
        errors = []
        
        for line in output.split("\n"):
            error = ErrorParser.parse_validation_line(line, validator)
            if error:
                errors.append(error)
        
        return errors


def add_common_suggestions(error: ValidationError) -> None:
    """Add common fix suggestions based on error type."""
    
    # Schema validation suggestions
    if "invalid status" in error.message:
        error.suggestions.append(ErrorSuggestion(
            description="Update status field to one of: done, assigned, in_progress, error",
            command=None,
        ))
    
    if "ISO8601 with Z suffix" in error.message:
        error.suggestions.append(ErrorSuggestion(
            description="Use UTC timestamp format: YYYY-MM-DDTHH:MM:SSZ",
            command=None,
        ))
    
    if "Missing required directory" in error.message:
        error.suggestions.append(ErrorSuggestion(
            description="Create missing directory",
            command=f"mkdir -p {error.message.split(':')[1].strip()}",
        ))
    
    # YAML syntax suggestions
    if "yaml" in error.error_type.lower() or "syntax" in error.error_type.lower():
        error.suggestions.append(ErrorSuggestion(
            description="Validate YAML syntax locally",
            command="yamllint .github/workflows/",
        ))
    
    # Workflow suggestions
    if "workflow" in error.validator.lower():
        error.suggestions.append(ErrorSuggestion(
            description="Test workflow locally with act",
            command="act -l",
        ))
        error.documentation_url = "https://github.com/nektos/act"


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate agent-friendly error summaries from validation output"
    )
    parser.add_argument(
        "--workflow",
        required=True,
        help="Workflow name",
    )
    parser.add_argument(
        "--job",
        required=True,
        help="Job name",
    )
    parser.add_argument(
        "--validator",
        default="unknown",
        help="Validator name (e.g., 'task-schema', 'work-structure')",
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Input file with validation output (default: stdin)",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        help="Output JSON file path",
    )
    parser.add_argument(
        "--output-markdown",
        type=Path,
        help="Output markdown file path",
    )
    parser.add_argument(
        "--emit-annotations",
        action="store_true",
        help="Emit GitHub Actions annotations",
    )
    parser.add_argument(
        "--fail-on-errors",
        action="store_true",
        help="Exit with code 1 if errors found",
    )
    
    args = parser.parse_args()
    
    # Read input
    if args.input:
        with open(args.input, "r") as f:
            input_text = f.read()
    else:
        input_text = sys.stdin.read()
    
    # Parse errors
    errors = ErrorParser.parse_python_validator_output(input_text, args.validator)
    
    # Add suggestions
    for error in errors:
        add_common_suggestions(error)
    
    # Create summary
    summary = ErrorSummary(
        workflow=args.workflow,
        job=args.job,
        run_id=os.getenv("GITHUB_RUN_ID"),
        run_url=os.getenv("GITHUB_SERVER_URL") 
            and os.getenv("GITHUB_REPOSITORY")
            and os.getenv("GITHUB_RUN_ID")
            and f"{os.getenv('GITHUB_SERVER_URL')}/{os.getenv('GITHUB_REPOSITORY')}/actions/runs/{os.getenv('GITHUB_RUN_ID')}",
    )
    
    for error in errors:
        summary.add_error(error)
    
    # Output JSON
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output_json, "w") as f:
            f.write(summary.to_json())
        print(f"✅ JSON summary written to {args.output_json}", file=sys.stderr)
    
    # Output Markdown
    if args.output_markdown:
        args.output_markdown.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output_markdown, "w") as f:
            f.write(summary.to_markdown())
        print(f"✅ Markdown summary written to {args.output_markdown}", file=sys.stderr)
    
    # Emit annotations
    if args.emit_annotations:
        summary.emit_github_annotations()
    
    # Print summary to stdout
    print("\n" + summary.to_markdown())
    
    # Exit code
    if args.fail_on_errors and summary.error_count() > 0:
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
