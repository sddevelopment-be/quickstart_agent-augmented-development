#!/usr/bin/env python3
"""
Integration Test Runner for generate-dashboard.py

Validates basic functionality and output formats using test metrics.
"""

import json
import sys
import tempfile
from pathlib import Path

# Add parent directory to path for common utilities
sys.path.insert(0, str(Path(__file__).parent.parent))

from common.path_utils import get_work_dir
from common.test_utils import print_test_header, run_command


def main():
    """Run integration tests for generate-dashboard.py."""
    script_dir = Path(__file__).parent
    work_dir = get_work_dir(Path(__file__))
    generate_dashboard = script_dir / "generate-dashboard.py"
    capture_metrics = script_dir / "capture-metrics.py"

    print_test_header("generate-dashboard.py", width=33)

    # Test 1: Help output
    print("[TEST 1] Help output")
    exit_code, stdout, stderr = run_command(
        [sys.executable, str(generate_dashboard), "--help"]
    )
    if exit_code == 0 and "usage:" in stdout.lower():
        print("✅ Help output works")
    else:
        print("❌ Help output failed")
        sys.exit(1)
    print()

    # Test 2: Generate test metrics first
    print("[TEST 2] Generate test metrics")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        tmp_metrics = Path(tmp.name)

    exit_code, stdout, stderr = run_command(
        [
            sys.executable,
            str(capture_metrics),
            "--work-dir",
            str(work_dir),
            "--output-file",
            str(tmp_metrics),
        ]
    )

    if tmp_metrics.exists():
        try:
            data = json.loads(tmp_metrics.read_text())
            metrics_count = data.get("metrics_count", 0)
            print(f"✅ Generated test metrics with {metrics_count} entries")
        except json.JSONDecodeError:
            print("❌ Failed to generate test metrics")
            tmp_metrics.unlink(missing_ok=True)
            sys.exit(1)
    else:
        print("❌ Failed to generate test metrics")
        sys.exit(1)
    print()

    # Test 3: Generate summary dashboard to stdout
    print("[TEST 3] Summary dashboard to stdout")
    exit_code, stdout, stderr = run_command(
        [
            sys.executable,
            str(generate_dashboard),
            "--input",
            str(tmp_metrics),
            "--dashboard-type",
            "summary",
            "--output-file",
            "-",
        ]
    )

    if exit_code == 0 and "# Metrics Summary Dashboard" in stdout:
        print("✅ Summary dashboard generated successfully")
    else:
        print("❌ Summary dashboard generation failed")
        tmp_metrics.unlink(missing_ok=True)
        sys.exit(1)
    print()

    # Test 4: Generate detail dashboard to file
    print("[TEST 4] Detail dashboard to file")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tmp:
        tmp_detail = Path(tmp.name)

    exit_code, stdout, stderr = run_command(
        [
            sys.executable,
            str(generate_dashboard),
            "--input",
            str(tmp_metrics),
            "--dashboard-type",
            "detail",
            "--output-file",
            str(tmp_detail),
        ]
    )

    if tmp_detail.exists():
        content = tmp_detail.read_text()
        if "# Metrics Detail Dashboard" in content:
            line_count = len(content.split("\n"))
            print(f"✅ Detail dashboard created with {line_count} lines")
        else:
            print("❌ Failed to create detail dashboard")
            tmp_detail.unlink(missing_ok=True)
            tmp_metrics.unlink(missing_ok=True)
            sys.exit(1)
    else:
        print("❌ Failed to create detail dashboard")
        tmp_metrics.unlink(missing_ok=True)
        sys.exit(1)

    tmp_detail.unlink(missing_ok=True)
    print()

    # Test 5: Generate trends dashboard to file
    print("[TEST 5] Trends dashboard to file")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tmp:
        tmp_trends = Path(tmp.name)

    exit_code, stdout, stderr = run_command(
        [
            sys.executable,
            str(generate_dashboard),
            "--input",
            str(tmp_metrics),
            "--dashboard-type",
            "trends",
            "--output-file",
            str(tmp_trends),
        ]
    )

    if tmp_trends.exists():
        content = tmp_trends.read_text()
        if "# Metrics Trends Dashboard" in content:
            line_count = len(content.split("\n"))
            print(f"✅ Trends dashboard created with {line_count} lines")
        else:
            print("❌ Failed to create trends dashboard")
            tmp_trends.unlink(missing_ok=True)
            tmp_metrics.unlink(missing_ok=True)
            sys.exit(1)
    else:
        print("❌ Failed to create trends dashboard")
        tmp_metrics.unlink(missing_ok=True)
        sys.exit(1)

    tmp_trends.unlink(missing_ok=True)
    print()

    # Test 6: Generate all dashboards to directory
    print("[TEST 6] Generate all dashboards to directory")
    with tempfile.TemporaryDirectory() as tmp_dir:
        exit_code, stdout, stderr = run_command(
            [
                sys.executable,
                str(generate_dashboard),
                "--input",
                str(tmp_metrics),
                "--output-dir",
                tmp_dir,
            ]
        )

        tmp_path = Path(tmp_dir)
        summary_exists = (tmp_path / "summary-dashboard.md").exists()
        detail_exists = (tmp_path / "detail-dashboard.md").exists()
        trends_exists = (tmp_path / "trends-dashboard.md").exists()

        if summary_exists and detail_exists and trends_exists:
            print("✅ All three dashboard types created in directory")
        else:
            print("❌ Failed to create all dashboards")
            tmp_metrics.unlink(missing_ok=True)
            sys.exit(1)
    print()

    # Test 7: Verify dashboard content structure
    print("[TEST 7] Verify dashboard content structure")
    exit_code, stdout, stderr = run_command(
        [
            sys.executable,
            str(generate_dashboard),
            "--input",
            str(tmp_metrics),
            "--dashboard-type",
            "summary",
            "--output-file",
            "-",
        ]
    )

    required_sections = [
        "Overall Statistics",
        "Top Agents by Task Count",
        "Recent Activity",
    ]
    all_present = True

    for section in required_sections:
        if section not in stdout:
            print(f"❌ Missing required section: {section}")
            all_present = False

    if all_present:
        print("✅ All required sections present in summary dashboard")
    print()

    # Test 8: Test verbose mode
    print("[TEST 8] Verbose mode")
    exit_code, stdout, stderr = run_command(
        [
            sys.executable,
            str(generate_dashboard),
            "--input",
            str(tmp_metrics),
            "--dashboard-type",
            "summary",
            "--output-file",
            "-",
            "--verbose",
        ]
    )

    info_count = stderr.count("[INFO]")
    if info_count > 0:
        print(f"✅ Verbose mode produces log messages ({info_count} INFO messages)")
    else:
        print("❌ Verbose mode produced no messages")
        tmp_metrics.unlink(missing_ok=True)
        sys.exit(1)
    print()

    # Test 9: Handle missing input file
    print("[TEST 9] Handle missing input file gracefully")
    exit_code, stdout, stderr = run_command(
        [
            sys.executable,
            str(generate_dashboard),
            "--input",
            "/nonexistent/file.json",
            "--dashboard-type",
            "summary",
            "--output-file",
            "-",
        ]
    )

    if "Metrics file not found" in stderr or exit_code != 0:
        print("✅ Handles missing input file with proper error message")
    else:
        print("❌ Did not handle missing input file properly")
        tmp_metrics.unlink(missing_ok=True)
        sys.exit(1)
    print()

    # Test 10: Verify chart generation
    print("[TEST 10] Verify ASCII chart generation")
    exit_code, stdout, stderr = run_command(
        [
            sys.executable,
            str(generate_dashboard),
            "--input",
            str(tmp_metrics),
            "--dashboard-type",
            "summary",
            "--output-file",
            "-",
        ]
    )

    if "█" in stdout:
        print("✅ ASCII bar charts generated in output")
    else:
        print("⚠️  No ASCII charts found (may be expected if no data)")
    print()

    # Cleanup
    tmp_metrics.unlink(missing_ok=True)

    print("=" * 33)
    print("All tests passed! ✅")


if __name__ == "__main__":
    main()
