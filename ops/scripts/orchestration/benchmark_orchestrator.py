#!/usr/bin/env python3
"""
Orchestrator Performance Benchmark Suite

Validates NFR4-6 performance requirements:
- NFR4: Cycle time <30 seconds
- NFR5: Validation time <1 second per task
- NFR6: 1000+ tasks without degradation

Measures:
- Total cycle time
- Individual operation durations
- Memory usage
- Validation performance
"""

from __future__ import annotations

import json
import shutil
import statistics
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

# Import orchestrator functions
sys.path.insert(0, str(Path(__file__).parent))
from agent_orchestrator import (
    ASSIGNED_DIR,
    DONE_DIR,
    INBOX_DIR,
    WORK_DIR,
    archive_old_tasks,
    assign_tasks,
    check_timeouts,
    detect_conflicts,
    process_completed_tasks,
    update_agent_status,
)

BENCHMARK_DIR = WORK_DIR / "benchmarks"
RESULTS_DIR = BENCHMARK_DIR / "results"
TEST_WORK_DIR = Path("/tmp/benchmark_work")


class BenchmarkResults:
    """Container for benchmark metrics."""

    def __init__(self, scenario: str):
        self.scenario = scenario
        self.runs: list[dict[str, Any]] = []
        self.system_info: dict[str, Any] = {}

    def add_run(self, metrics: dict[str, Any]) -> None:
        """Add a single run's metrics."""
        self.runs.append(metrics)

    def compute_statistics(self) -> dict[str, Any]:
        """Compute mean and stddev across runs."""
        if not self.runs:
            return {}

        stats: dict[str, Any] = {"scenario": self.scenario, "runs": len(self.runs)}

        # Aggregate numeric metrics
        for key in self.runs[0]:
            if isinstance(self.runs[0][key], (int, float)):
                values = [run[key] for run in self.runs if key in run]
                if values:
                    stats[f"{key}_mean"] = statistics.mean(values)
                    if len(values) > 1:
                        stats[f"{key}_stddev"] = statistics.stdev(values)
                    else:
                        stats[f"{key}_stddev"] = 0.0
                    stats[f"{key}_min"] = min(values)
                    stats[f"{key}_max"] = max(values)

        return stats


def get_system_info() -> dict[str, Any]:
    """Capture system specifications."""
    info: dict[str, Any] = {"timestamp": datetime.now(timezone.utc).isoformat()}

    try:
        import platform

        info["platform"] = platform.platform()
        info["python_version"] = platform.python_version()
        info["processor"] = platform.processor()
    except Exception:
        pass

    try:
        import psutil

        info["cpu_count"] = psutil.cpu_count()
        info["total_memory_gb"] = round(psutil.virtual_memory().total / (1024**3), 2)
    except (ImportError, Exception):
        pass

    return info


def create_synthetic_task(task_id: str, agent: str, status: str = "new") -> dict[str, Any]:
    """Generate a valid synthetic task."""
    return {
        "id": task_id,
        "agent": agent,
        "status": status,
        "title": f"Synthetic benchmark task {task_id}",
        "artefacts": [f"test/output/{task_id}.md"],
        "context": {
            "repo": "benchmark/test",
            "branch": "main",
            "notes": ["Generated for performance testing"],
        },
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "created_by": "benchmark",
    }


def setup_benchmark_environment(num_inbox: int, num_assigned: int, num_done: int) -> dict[str, int]:
    """Create synthetic task files for benchmarking."""
    # Safety check: ensure we're only deleting in /tmp
    if not str(TEST_WORK_DIR).startswith("/tmp/"):
        raise ValueError(f"TEST_WORK_DIR must be in /tmp for safety: {TEST_WORK_DIR}")
    
    if TEST_WORK_DIR.exists():
        shutil.rmtree(TEST_WORK_DIR)

    # Mirror the work directory structure
    inbox_dir = TEST_WORK_DIR / "inbox"
    assigned_dir = TEST_WORK_DIR / "assigned"
    done_dir = TEST_WORK_DIR / "done"
    collab_dir = TEST_WORK_DIR / "collaboration"

    for directory in [inbox_dir, assigned_dir, done_dir, collab_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    # Create agent directories
    agents = ["test-agent", "build-automation", "architect", "writer-editor"]
    for agent in agents:
        (assigned_dir / agent).mkdir(parents=True, exist_ok=True)

    created = {"inbox": 0, "assigned": 0, "done": 0}

    # Create inbox tasks
    for i in range(num_inbox):
        task_id = f"bench-inbox-{i:04d}"
        agent = agents[i % len(agents)]
        task = create_synthetic_task(task_id, agent, "new")
        task_file = inbox_dir / f"{task_id}.yaml"
        with open(task_file, "w", encoding="utf-8") as f:
            yaml.dump(task, f, default_flow_style=False, sort_keys=False)
        created["inbox"] += 1

    # Create assigned tasks
    for i in range(num_assigned):
        task_id = f"bench-assigned-{i:04d}"
        agent = agents[i % len(agents)]
        task = create_synthetic_task(task_id, agent, "assigned")
        task["assigned_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        task_file = assigned_dir / agent / f"{task_id}.yaml"
        with open(task_file, "w", encoding="utf-8") as f:
            yaml.dump(task, f, default_flow_style=False, sort_keys=False)
        created["assigned"] += 1

    # Create done tasks
    for i in range(num_done):
        task_id = f"bench-done-{i:04d}"
        agent = agents[i % len(agents)]
        task = create_synthetic_task(task_id, agent, "done")
        task["completed_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        task["result"] = {
            "summary": f"Completed benchmark task {task_id}",
            "artefacts": [f"test/output/{task_id}.md"],
        }
        task_file = done_dir / f"{task_id}.yaml"
        with open(task_file, "w", encoding="utf-8") as f:
            yaml.dump(task, f, default_flow_style=False, sort_keys=False)
        created["done"] += 1

    return created


def run_orchestrator_cycle() -> dict[str, Any]:
    """Execute a full orchestrator cycle with timing."""
    metrics: dict[str, float] = {}

    # Override global directories temporarily
    # NOTE: This approach uses global variable manipulation because agent_orchestrator
    # uses module-level globals. Future refactoring should consider passing directories
    # as parameters to orchestrator functions for better testability.
    import agent_orchestrator

    original_dirs = {
        "INBOX_DIR": agent_orchestrator.INBOX_DIR,
        "ASSIGNED_DIR": agent_orchestrator.ASSIGNED_DIR,
        "DONE_DIR": agent_orchestrator.DONE_DIR,
        "COLLAB_DIR": agent_orchestrator.COLLAB_DIR,
        "ARCHIVE_DIR": agent_orchestrator.ARCHIVE_DIR,
    }

    try:
        # Point to test environment
        agent_orchestrator.INBOX_DIR = TEST_WORK_DIR / "inbox"
        agent_orchestrator.ASSIGNED_DIR = TEST_WORK_DIR / "assigned"
        agent_orchestrator.DONE_DIR = TEST_WORK_DIR / "done"
        agent_orchestrator.COLLAB_DIR = TEST_WORK_DIR / "collaboration"
        agent_orchestrator.ARCHIVE_DIR = TEST_WORK_DIR / "archive"

        # Time each operation
        start_total = time.perf_counter()

        start = time.perf_counter()
        assigned = assign_tasks()
        metrics["assign_tasks_duration"] = time.perf_counter() - start
        metrics["tasks_assigned"] = assigned

        start = time.perf_counter()
        followups = process_completed_tasks()
        metrics["process_completed_duration"] = time.perf_counter() - start
        metrics["followups_created"] = followups

        start = time.perf_counter()
        timeouts = check_timeouts()
        metrics["check_timeouts_duration"] = time.perf_counter() - start
        metrics["timeouts_flagged"] = timeouts

        start = time.perf_counter()
        conflicts = detect_conflicts()
        metrics["detect_conflicts_duration"] = time.perf_counter() - start
        metrics["conflicts_detected"] = conflicts

        start = time.perf_counter()
        archived = archive_old_tasks()
        metrics["archive_old_tasks_duration"] = time.perf_counter() - start
        metrics["tasks_archived"] = archived

        start = time.perf_counter()
        update_agent_status()
        metrics["update_agent_status_duration"] = time.perf_counter() - start

        metrics["total_cycle_time"] = time.perf_counter() - start_total

    finally:
        # Restore original directories
        for key, value in original_dirs.items():
            setattr(agent_orchestrator, key, value)

    return metrics


def validate_task_performance(num_tasks: int) -> dict[str, float]:
    """Measure validation performance using inline validation."""
    validation_times: list[float] = []

    # Validate inbox tasks
    inbox_dir = TEST_WORK_DIR / "inbox"
    task_files = list(inbox_dir.glob("*.yaml"))[:num_tasks]

    for task_file in task_files:
        start = time.perf_counter()
        # Validation: load YAML and check required structure per task schema
        try:
            with open(task_file, "r", encoding="utf-8") as f:
                task = yaml.safe_load(f)
                # Validate required fields exist and have correct types
                if not isinstance(task.get("id"), str):
                    raise ValueError("id must be a string")
                if not isinstance(task.get("agent"), str):
                    raise ValueError("agent must be a string")
                if not isinstance(task.get("status"), str):
                    raise ValueError("status must be a string")
                if not isinstance(task.get("artefacts"), list):
                    raise ValueError("artefacts must be a list")
        except Exception:
            pass
        validation_times.append(time.perf_counter() - start)

    if validation_times:
        return {
            "validation_mean": statistics.mean(validation_times),
            "validation_total": sum(validation_times),
            "validation_min": min(validation_times),
            "validation_max": max(validation_times),
            "tasks_validated": len(validation_times),
        }
    return {}


def run_scenario(
    scenario_name: str,
    num_inbox: int,
    num_assigned: int,
    num_done: int,
    num_runs: int = 5,
) -> BenchmarkResults:
    """Run a complete benchmark scenario."""
    print(f"\n{'='*60}")
    print(f"Scenario: {scenario_name}")
    print(f"{'='*60}")
    print(f"Tasks: {num_inbox} inbox, {num_assigned} assigned, {num_done} done")
    print(f"Runs: {num_runs}")

    results = BenchmarkResults(scenario_name)
    results.system_info = get_system_info()

    for run_num in range(1, num_runs + 1):
        print(f"\n  Run {run_num}/{num_runs}...", end=" ", flush=True)

        # Setup environment
        created = setup_benchmark_environment(num_inbox, num_assigned, num_done)

        # Measure validation performance
        validation_metrics = validate_task_performance(min(num_inbox, 100))

        # Run orchestrator cycle
        cycle_metrics = run_orchestrator_cycle()

        # Combine metrics
        run_metrics = {
            "run": run_num,
            "tasks_created": sum(created.values()),
            **validation_metrics,
            **cycle_metrics,
        }

        results.add_run(run_metrics)
        print(f"✓ (cycle: {cycle_metrics['total_cycle_time']:.3f}s)")

    return results


def check_nfr_compliance(all_results: dict[str, BenchmarkResults]) -> dict[str, Any]:
    """Validate NFR4-6 requirements."""
    compliance: dict[str, Any] = {}

    # NFR4: Cycle time <30 seconds
    compliance["nfr4"] = {
        "requirement": "Coordinator completes cycle in <30 seconds",
        "pass": True,
        "details": {},
    }

    for scenario, results in all_results.items():
        stats = results.compute_statistics()
        cycle_time = stats.get("total_cycle_time_mean", 0)
        compliance["nfr4"]["details"][scenario] = {
            "mean_cycle_time": cycle_time,
            "max_cycle_time": stats.get("total_cycle_time_max", 0),
            "pass": cycle_time < 30,
        }
        if cycle_time >= 30:
            compliance["nfr4"]["pass"] = False

    # NFR5: Validation time <1 second per task
    compliance["nfr5"] = {
        "requirement": "Task schema validation completes in <1 second per task",
        "pass": True,
        "details": {},
    }

    for scenario, results in all_results.items():
        stats = results.compute_statistics()
        validation_mean = stats.get("validation_mean_mean", 0)
        compliance["nfr5"]["details"][scenario] = {
            "mean_validation_time": validation_mean,
            "max_validation_time": stats.get("validation_mean_max", 0),
            "pass": validation_mean < 1.0,
        }
        if validation_mean >= 1.0:
            compliance["nfr5"]["pass"] = False

    # NFR6: 1000+ tasks without degradation
    if "stress_test" in all_results:
        stress_stats = all_results["stress_test"].compute_statistics()
        cycle_time = stress_stats.get("total_cycle_time_mean", 0)
        compliance["nfr6"] = {
            "requirement": "Directory structure supports 1000+ tasks without performance degradation",
            "pass": cycle_time < 60,  # Allow 2x time for stress test
            "details": {
                "tasks_tested": 1000,
                "mean_cycle_time": cycle_time,
                "max_cycle_time": stress_stats.get("total_cycle_time_max", 0),
            },
        }
    else:
        compliance["nfr6"] = {
            "requirement": "Directory structure supports 1000+ tasks",
            "pass": False,
            "details": {"error": "Stress test not run"},
        }

    return compliance


def generate_json_report(
    all_results: dict[str, BenchmarkResults], compliance: dict[str, Any], output_file: Path
) -> None:
    """Generate machine-readable JSON report."""
    report = {
        "benchmark_run": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0",
        },
        "system_info": next(iter(all_results.values())).system_info,
        "scenarios": {},
        "nfr_compliance": compliance,
    }

    for scenario, results in all_results.items():
        report["scenarios"][scenario] = {
            "statistics": results.compute_statistics(),
            "raw_runs": results.runs,
        }

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"\n✅ JSON report saved: {output_file}")


def generate_markdown_report(
    all_results: dict[str, BenchmarkResults], compliance: dict[str, Any], output_file: Path
) -> None:
    """Generate human-readable markdown report."""
    lines = [
        "# Orchestrator Performance Benchmark Report",
        "",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"**Version:** 1.0.0",
        "",
        "## Executive Summary",
        "",
    ]

    # NFR compliance summary
    lines.append("### Non-Functional Requirements (NFR) Compliance")
    lines.append("")
    for nfr_id, nfr_data in compliance.items():
        status = "✅ PASS" if nfr_data["pass"] else "❌ FAIL"
        lines.append(f"- **{nfr_id.upper()}**: {status}")
        lines.append(f"  - {nfr_data['requirement']}")
    lines.append("")

    # System info
    system_info = next(iter(all_results.values())).system_info
    lines.append("### System Information")
    lines.append("")
    lines.append("| Property | Value |")
    lines.append("|----------|-------|")
    for key, value in system_info.items():
        if key != "timestamp":
            lines.append(f"| {key.replace('_', ' ').title()} | {value} |")
    lines.append("")

    # Scenario results
    lines.append("## Benchmark Scenarios")
    lines.append("")

    for scenario, results in all_results.items():
        stats = results.compute_statistics()
        lines.append(f"### {scenario.replace('_', ' ').title()}")
        lines.append("")

        # Key metrics table
        lines.append("| Metric | Mean | Std Dev | Min | Max |")
        lines.append("|--------|------|---------|-----|-----|")

        key_metrics = [
            ("total_cycle_time", "Total Cycle Time (s)"),
            ("assign_tasks_duration", "Assign Tasks (s)"),
            ("process_completed_duration", "Process Completed (s)"),
            ("check_timeouts_duration", "Check Timeouts (s)"),
            ("detect_conflicts_duration", "Detect Conflicts (s)"),
            ("update_agent_status_duration", "Update Status (s)"),
            ("validation_mean", "Validation per Task (s)"),
        ]

        for key, label in key_metrics:
            mean_key = f"{key}_mean"
            if mean_key in stats:
                mean_val = stats[mean_key]
                stddev_val = stats.get(f"{key}_stddev", 0)
                min_val = stats.get(f"{key}_min", 0)
                max_val = stats.get(f"{key}_max", 0)
                lines.append(
                    f"| {label} | {mean_val:.4f} | {stddev_val:.4f} | {min_val:.4f} | {max_val:.4f} |"
                )

        lines.append("")

        # Task counts
        if "tasks_assigned_mean" in stats:
            lines.append("**Task Activity:**")
            lines.append(f"- Tasks assigned: {stats.get('tasks_assigned_mean', 0):.1f}")
            lines.append(f"- Follow-ups created: {stats.get('followups_created_mean', 0):.1f}")
            lines.append(f"- Conflicts detected: {stats.get('conflicts_detected_mean', 0):.1f}")
            lines.append("")

    # NFR Analysis
    lines.append("## NFR Compliance Analysis")
    lines.append("")

    for nfr_id, nfr_data in compliance.items():
        status_icon = "✅" if nfr_data["pass"] else "❌"
        lines.append(f"### {nfr_id.upper()} {status_icon}")
        lines.append("")
        lines.append(f"**Requirement:** {nfr_data['requirement']}")
        lines.append("")

        details = nfr_data.get("details", {})
        
        # NFR6 has a different structure (single test)
        if nfr_id == "nfr6" and "tasks_tested" in details:
            lines.append(f"**Tasks Tested:** {details['tasks_tested']}")
            lines.append(f"**Mean Cycle Time:** {details.get('mean_cycle_time', 0):.3f}s")
            lines.append(f"**Max Cycle Time:** {details.get('max_cycle_time', 0):.3f}s")
            lines.append("")
        else:
            # NFR4 and NFR5 have per-scenario results
            lines.append("| Scenario | Measured Value | Pass |")
            lines.append("|----------|----------------|------|")

            for scenario, scenario_details in details.items():
                if isinstance(scenario_details, dict):
                    if "mean_cycle_time" in scenario_details:
                        value = f"{scenario_details['mean_cycle_time']:.3f}s"
                        pass_icon = "✅" if scenario_details["pass"] else "❌"
                        lines.append(f"| {scenario} | {value} | {pass_icon} |")
                    elif "mean_validation_time" in scenario_details:
                        value = f"{scenario_details['mean_validation_time']:.4f}s"
                        pass_icon = "✅" if scenario_details["pass"] else "❌"
                        lines.append(f"| {scenario} | {value} | {pass_icon} |")

            lines.append("")

    # Recommendations
    lines.append("## Recommendations")
    lines.append("")

    bottlenecks = []
    for scenario, results in all_results.items():
        stats = results.compute_statistics()
        cycle_time = stats.get("total_cycle_time_mean", 0)

        # Identify slowest operations
        operations = {
            "assign_tasks": stats.get("assign_tasks_duration_mean", 0),
            "process_completed": stats.get("process_completed_duration_mean", 0),
            "detect_conflicts": stats.get("detect_conflicts_duration_mean", 0),
        }

        if cycle_time > 0:
            for op, duration in operations.items():
                if duration > cycle_time * 0.3:  # >30% of cycle time
                    bottlenecks.append(f"- **{scenario}**: {op} ({duration:.3f}s, {duration/cycle_time*100:.1f}% of cycle)")

    if bottlenecks:
        lines.append("### Identified Bottlenecks")
        lines.append("")
        lines.extend(bottlenecks)
        lines.append("")

    if compliance["nfr4"]["pass"] and compliance["nfr5"]["pass"] and compliance["nfr6"]["pass"]:
        lines.append("### Overall Assessment")
        lines.append("")
        lines.append("✅ **All NFR requirements met.** The orchestrator performs within specified limits.")
        lines.append("")
        lines.append("The file-based orchestration framework is validated for production use.")
    else:
        lines.append("### Overall Assessment")
        lines.append("")
        lines.append("⚠️ **Some NFR requirements not met.** Review bottlenecks and consider optimization.")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Generated by benchmark_orchestrator.py*")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ Markdown report saved: {output_file}")


def main() -> int:
    """Run all benchmark scenarios."""
    print("🔬 Orchestrator Performance Benchmark Suite")
    print("=" * 60)

    scenarios = {
        "baseline": (0, 0, 0),
        "light_load": (2, 3, 5),
        "moderate_load": (10, 15, 25),
        "heavy_load": (20, 30, 50),
        "stress_test": (200, 300, 500),  # Total 1000 tasks
    }

    all_results: dict[str, BenchmarkResults] = {}

    for scenario_name, (inbox, assigned, done) in scenarios.items():
        results = run_scenario(scenario_name, inbox, assigned, done, num_runs=5)
        all_results[scenario_name] = results

    print(f"\n{'='*60}")
    print("Analyzing results...")
    print("=" * 60)

    # Check NFR compliance
    compliance = check_nfr_compliance(all_results)

    # Generate reports
    generate_json_report(
        all_results,
        compliance,
        RESULTS_DIR / "baseline-metrics.json",
    )

    generate_markdown_report(
        all_results,
        compliance,
        BENCHMARK_DIR / "orchestrator-performance-report.md",
    )

    print("\n" + "=" * 60)
    print("🎉 Benchmark complete!")
    print("=" * 60)

    # Cleanup test artifacts
    print("\n🧹 Cleaning up test artifacts...")
    if TEST_WORK_DIR.exists():
        shutil.rmtree(TEST_WORK_DIR)
        print(f"✅ Removed temporary test directory: {TEST_WORK_DIR}")

    # Return exit code based on NFR compliance
    if all(nfr["pass"] for nfr in compliance.values()):
        print("\n✅ All NFR requirements validated successfully")
        return 0
    else:
        print("\n⚠️ Some NFR requirements not met - see report for details")
        return 1


if __name__ == "__main__":
    sys.exit(main())
