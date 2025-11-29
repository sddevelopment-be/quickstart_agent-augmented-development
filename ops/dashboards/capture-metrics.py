#!/usr/bin/env python3
"""
ADR-009 Metrics Capture Script

Extracts orchestration metrics from work logs and task YAML files.
Supports JSON and CSV output formats for aggregation and trend analysis.

Usage:
    python3 ops/scripts/capture-metrics.py [options]

Options:
    --work-dir PATH       Path to work directory (default: work/)
    --output-format FMT   Output format: json or csv (default: json)
    --output-file PATH    Output file path (default: stdout)
    --include-logs        Include metrics from work logs
    --include-tasks       Include metrics from task YAML files
    --verbose             Enable verbose logging

ADR-009 Metrics Extracted:
    - duration_minutes: Total task execution time
    - token_count: Input, output, and total token usage
    - context_files_loaded: Number of files read for context
    - artifacts_created: Count of new files
    - artifacts_modified: Count of edited files
    - per_artifact_timing: Detailed breakdown for multi-artifact tasks
    - handoff_count: Number of agent handoffs
"""

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print(
        "ERROR: PyYAML is required. Install with: pip install PyYAML", file=sys.stderr
    )
    sys.exit(1)


class MetricsExtractor:
    """Extracts ADR-009 metrics from work logs and task files."""

    def __init__(self, work_dir: Path, verbose: bool = False):
        self.work_dir = Path(work_dir)
        self.verbose = verbose
        self.metrics: list[dict[str, Any]] = []

    def log(self, message: str) -> None:
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            print(f"[INFO] {message}", file=sys.stderr)

    def extract_from_work_logs(self) -> None:
        """Extract metrics from markdown work logs."""
        logs_dir = self.work_dir / "reports" / "logs"
        if not logs_dir.exists():
            self.log(f"Work logs directory not found: {logs_dir}")
            return

        log_files = list(logs_dir.rglob("*.md"))
        self.log(f"Found {len(log_files)} work log files")

        for log_file in log_files:
            try:
                metrics = self._parse_work_log(log_file)
                if metrics:
                    self.metrics.append(metrics)
                    self.log(f"Extracted metrics from {log_file.name}")
            except Exception as e:
                self.log(f"Error parsing {log_file}: {e}")

    def _parse_work_log(self, log_file: Path) -> dict[str, Any] | None:
        """Parse a work log markdown file and extract metrics."""
        content = log_file.read_text(encoding="utf-8")

        # Initialize metrics dictionary
        metrics = {
            "source_type": "work_log",
            "source_file": str(log_file.relative_to(self.work_dir.parent)),
            "agent": self._extract_agent_from_path(log_file),
            "timestamp": self._extract_timestamp_from_filename(log_file.name),
        }

        # Extract task ID
        task_id_match = re.search(r"\*\*Task ID:\*\*\s*([^\s\n]+)", content)
        if task_id_match:
            metrics["task_id"] = task_id_match.group(1)

        # Extract metadata section
        metadata_section = self._extract_section(content, "Metadata")
        if metadata_section:
            # Duration
            duration_match = re.search(
                r"\*\*Duration:\*\*\s*(\d+)\s*minutes?", metadata_section
            )
            if duration_match:
                metrics["duration_minutes"] = int(duration_match.group(1))

            # Token usage
            token_match = re.search(
                r"\*\*Token Usage:\*\*\s*([0-9,]+)\s*input\s*\+\s*([0-9,]+)\s*output\s*=\s*([0-9,]+)\s*total",
                metadata_section,
            )
            if token_match:
                metrics["token_input"] = int(token_match.group(1).replace(",", ""))
                metrics["token_output"] = int(token_match.group(2).replace(",", ""))
                metrics["token_total"] = int(token_match.group(3).replace(",", ""))

            # Context files loaded
            context_match = re.search(
                r"\*\*Context Files Loaded:\*\*\s*(\d+)", metadata_section
            )
            if context_match:
                metrics["context_files_loaded"] = int(context_match.group(1))

            # Artifacts created/modified
            artifacts_created_match = re.search(
                r"\*\*Artifacts Created:\*\*\s*(\d+)", metadata_section
            )
            if artifacts_created_match:
                metrics["artifacts_created"] = int(artifacts_created_match.group(1))

            artifacts_modified_match = re.search(
                r"\*\*Artifacts Modified:\*\*\s*(\d+)", metadata_section
            )
            if artifacts_modified_match:
                metrics["artifacts_modified"] = int(artifacts_modified_match.group(1))

            # Handoff information
            handoff_match = re.search(r"- Next agent:\s*([^\n]+)", metadata_section)
            if handoff_match:
                metrics["next_agent"] = handoff_match.group(1).strip()
                metrics["handoff_count"] = 1

        # Return metrics only if we found at least some data
        if len(metrics) > 4:  # More than just the basic fields
            return metrics
        return None

    def extract_from_task_files(self) -> None:
        """Extract metrics from YAML task files."""
        # Search in done/ directory for completed tasks
        done_dir = self.work_dir / "collaboration" / "done"
        if not done_dir.exists():
            self.log(f"Done tasks directory not found: {done_dir}")
            return

        task_files = list(done_dir.rglob("*.yaml")) + list(done_dir.rglob("*.yml"))
        self.log(f"Found {len(task_files)} task files in done/")

        for task_file in task_files:
            try:
                metrics = self._parse_task_file(task_file)
                if metrics:
                    self.metrics.append(metrics)
                    self.log(f"Extracted metrics from {task_file.name}")
            except Exception as e:
                self.log(f"Error parsing {task_file}: {e}")

    def _parse_task_file(self, task_file: Path) -> dict[str, Any] | None:
        """Parse a YAML task file and extract metrics from result block."""
        try:
            with open(task_file, encoding="utf-8") as f:
                task_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            self.log(f"YAML parse error in {task_file}: {e}")
            return None

        if not task_data or not isinstance(task_data, dict):
            return None

        # Initialize metrics dictionary
        metrics = {
            "source_type": "task_file",
            "source_file": str(task_file.relative_to(self.work_dir.parent)),
            "task_id": task_data.get("id"),
            "agent": task_data.get("agent"),
            "status": task_data.get("status"),
        }

        # Extract from result block
        result = task_data.get("result", {})
        if not result:
            return None

        # Extract metrics from result.metrics
        result_metrics = result.get("metrics", {})
        if result_metrics:
            if "duration_minutes" in result_metrics:
                metrics["duration_minutes"] = result_metrics["duration_minutes"]

            # Token count
            token_count = result_metrics.get("token_count", {})
            if token_count:
                metrics["token_input"] = token_count.get("input")
                metrics["token_output"] = token_count.get("output")
                metrics["token_total"] = token_count.get("total")

            if "context_files_loaded" in result_metrics:
                metrics["context_files_loaded"] = result_metrics["context_files_loaded"]

            if "artifacts_created" in result_metrics:
                metrics["artifacts_created"] = result_metrics["artifacts_created"]

            if "artifacts_modified" in result_metrics:
                metrics["artifacts_modified"] = result_metrics["artifacts_modified"]

            # Per-artifact timing
            if "per_artifact_timing" in result_metrics:
                timing_data = result_metrics["per_artifact_timing"]
                if timing_data:
                    metrics["per_artifact_count"] = len(timing_data)
                    metrics["per_artifact_total_seconds"] = sum(
                        item.get("duration_seconds", 0) for item in timing_data
                    )

        # Extract timestamps
        if "completed_at" in result:
            metrics["completed_at"] = result["completed_at"]

        if "created_at" in task_data:
            metrics["created_at"] = task_data["created_at"]

        # Count handoffs (if next agent is specified)
        if result.get("next_agent"):
            metrics["next_agent"] = result["next_agent"]
            metrics["handoff_count"] = 1

        # Return metrics only if we found at least some data
        if len(metrics) > 5:  # More than just the basic fields
            return metrics
        return None

    def _extract_section(self, content: str, section_name: str) -> str | None:
        """Extract a markdown section by heading."""
        # Match ## Section or **Section** format
        pattern = rf"(?:^|\n)(?:##\s+{section_name}|.*\*\*{section_name}[:\s]*\*\*)(.*?)(?=\n##|\n---|\Z)"
        match = re.search(pattern, content, re.DOTALL | re.MULTILINE | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    def _extract_agent_from_path(self, file_path: Path) -> str:
        """Extract agent name from file path."""
        # Path format: work/reports/logs/<agent-name>/...
        parts = file_path.parts
        try:
            logs_idx = parts.index("logs")
            if logs_idx + 1 < len(parts):
                return parts[logs_idx + 1]
        except ValueError:
            pass
        return "unknown"

    def _extract_timestamp_from_filename(self, filename: str) -> str | None:
        """Extract ISO timestamp from filename."""
        # Format: YYYY-MM-DDTHHMM-description.md
        match = re.match(r"(\d{4}-\d{2}-\d{2}T\d{4})", filename)
        if match:
            return match.group(1)
        return None

    def get_metrics(self) -> list[dict[str, Any]]:
        """Return collected metrics."""
        return self.metrics

    def output_json(self, output_file: Path | None = None) -> None:
        """Output metrics as JSON."""
        output_data = {
            "extracted_at": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "metrics_count": len(self.metrics),
            "metrics": self.metrics,
            "summary": self._calculate_summary(),
        }

        json_str = json.dumps(output_data, indent=2, default=str)

        if output_file:
            output_file.write_text(json_str, encoding="utf-8")
            self.log(f"Metrics written to {output_file}")
        else:
            print(json_str)

    def output_csv(self, output_file: Path | None = None) -> None:
        """Output metrics as CSV."""
        if not self.metrics:
            self.log("No metrics to output")
            return

        # Determine all unique fields across all metrics
        all_fields = set()
        for metric in self.metrics:
            all_fields.update(metric.keys())

        # Sort fields for consistent column order
        fields = sorted(all_fields)

        # Write CSV
        import io

        output = io.StringIO() if not output_file else None

        if output_file:
            f = open(output_file, "w", newline="", encoding="utf-8")
        else:
            f = output

        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(self.metrics)

        if output_file:
            f.close()
            self.log(f"Metrics written to {output_file}")
        else:
            print(output.getvalue())

    def _calculate_summary(self) -> dict[str, Any]:
        """Calculate summary statistics across all metrics."""
        if not self.metrics:
            return {}

        summary = {
            "total_tasks": len(self.metrics),
            "agents": {},
            "totals": {
                "duration_minutes": 0,
                "token_total": 0,
                "artifacts_created": 0,
                "artifacts_modified": 0,
                "handoffs": 0,
            },
        }

        # Calculate totals and per-agent stats
        for metric in self.metrics:
            agent = metric.get("agent", "unknown")
            if agent not in summary["agents"]:
                summary["agents"][agent] = {
                    "count": 0,
                    "total_duration": 0,
                    "total_tokens": 0,
                }

            summary["agents"][agent]["count"] += 1

            if "duration_minutes" in metric:
                duration = metric["duration_minutes"]
                summary["totals"]["duration_minutes"] += duration
                summary["agents"][agent]["total_duration"] += duration

            if "token_total" in metric:
                tokens = metric["token_total"]
                summary["totals"]["token_total"] += tokens
                summary["agents"][agent]["total_tokens"] += tokens

            if "artifacts_created" in metric:
                summary["totals"]["artifacts_created"] += metric["artifacts_created"]

            if "artifacts_modified" in metric:
                summary["totals"]["artifacts_modified"] += metric["artifacts_modified"]

            if "handoff_count" in metric:
                summary["totals"]["handoffs"] += metric["handoff_count"]

        return summary


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Extract ADR-009 metrics from work logs and task files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=Path("work"),
        help="Path to work directory (default: work/)",
    )
    parser.add_argument(
        "--output-format",
        choices=["json", "csv"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "--output-file", type=Path, help="Output file path (default: stdout)"
    )
    parser.add_argument(
        "--include-logs",
        action="store_true",
        default=True,
        help="Include metrics from work logs (default: True)",
    )
    parser.add_argument(
        "--include-tasks",
        action="store_true",
        default=True,
        help="Include metrics from task YAML files (default: True)",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    # Validate work directory
    if not args.work_dir.exists():
        print(f"ERROR: Work directory not found: {args.work_dir}", file=sys.stderr)
        sys.exit(1)

    # Create extractor
    extractor = MetricsExtractor(args.work_dir, verbose=args.verbose)

    # Extract metrics
    if args.include_logs:
        extractor.extract_from_work_logs()

    if args.include_tasks:
        extractor.extract_from_task_files()

    # Check if any metrics were found
    metrics = extractor.get_metrics()
    if not metrics:
        print("WARNING: No metrics found", file=sys.stderr)
        if args.verbose:
            print(
                "Check that work logs and task files contain ADR-009 metrics",
                file=sys.stderr,
            )

    # Output results
    if args.output_format == "json":
        extractor.output_json(args.output_file)
    else:
        extractor.output_csv(args.output_file)


if __name__ == "__main__":
    main()
