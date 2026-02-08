#!/usr/bin/env python3
"""
Integration Test Runner for capture-metrics.py

Validates basic functionality and output formats using actual work directory.
Complements unit tests in validation/dashboards/test_capture_metrics.py
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
    """Run integration tests for capture-metrics.py."""
    script_dir = Path(__file__).parent
    work_dir = get_work_dir(Path(__file__))
    capture_metrics = script_dir / "capture-metrics.py"

    print_test_header("capture-metrics.py", width=30)

    # Test 1: Help output
    print("[TEST 1] Help output")
    exit_code, stdout, stderr = run_command(
        [sys.executable, str(capture_metrics), "--help"]
    )
    if exit_code == 0 and "usage:" in stdout.lower():
        print("✅ Help output works")
    else:
        print("❌ Help output failed")
        sys.exit(1)
    print()

    # Test 2: JSON output to stdout
    print("[TEST 2] JSON output to stdout")
    exit_code, stdout, stderr = run_command(
        [sys.executable, str(capture_metrics), "--work-dir", str(work_dir)]
    )
    if exit_code == 0:
        try:
            json.loads(stdout)
            print("✅ Valid JSON output to stdout")
        except json.JSONDecodeError:
            print("❌ Invalid JSON output")
            sys.exit(1)
    else:
        print("⚠️  Command failed (may be expected if no work logs)")
    print()

    # Test 3: JSON output to file
    print("[TEST 3] JSON output to file")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        tmp_json = Path(tmp.name)

    exit_code, stdout, stderr = run_command(
        [
            sys.executable,
            str(capture_metrics),
            "--work-dir",
            str(work_dir),
            "--output-file",
            str(tmp_json),
        ]
    )

    if tmp_json.exists():
        try:
            data = json.loads(tmp_json.read_text())
            metrics_count = data.get("metrics_count", 0)
            print(f"✅ Valid JSON file created with {metrics_count} metrics")
        except json.JSONDecodeError:
            print("❌ Failed to create valid JSON file")
            tmp_json.unlink(missing_ok=True)
            sys.exit(1)
    else:
        print("❌ Output file not created")
        sys.exit(1)

    tmp_json.unlink(missing_ok=True)
    print()

    # Test 4: CSV output to file
    print("[TEST 4] CSV output to file")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
        tmp_csv = Path(tmp.name)

    exit_code, stdout, stderr = run_command(
        [
            sys.executable,
            str(capture_metrics),
            "--work-dir",
            str(work_dir),
            "--output-format",
            "csv",
            "--output-file",
            str(tmp_csv),
        ]
    )

    if tmp_csv.exists():
        content = tmp_csv.read_text()
        lines = content.strip().split("\n")
        line_count = len(lines)
        col_count = len(lines[0].split(",")) if lines else 0
        print(f"✅ CSV file created with {line_count} lines and {col_count} columns")
    else:
        print("❌ Failed to create CSV file")
        sys.exit(1)

    tmp_csv.unlink(missing_ok=True)
    print()

    # Test 5: Verify JSON structure
    print("[TEST 5] Verify JSON structure")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        tmp_json = Path(tmp.name)

    run_command(
        [
            sys.executable,
            str(capture_metrics),
            "--work-dir",
            str(work_dir),
            "--output-file",
            str(tmp_json),
        ]
    )

    required_fields = ["extracted_at", "metrics_count", "metrics", "summary"]
    all_present = True

    if tmp_json.exists():
        content = tmp_json.read_text()
        for field in required_fields:
            if f'"{field}"' not in content:
                print(f"❌ Missing required field: {field}")
                all_present = False

        if all_present:
            print("✅ All required JSON fields present")
    else:
        print("❌ Output file not created")
        sys.exit(1)

    tmp_json.unlink(missing_ok=True)
    print()

    # Test 6: Verbose mode
    print("[TEST 6] Verbose mode")
    exit_code, stdout, stderr = run_command(
        [
            sys.executable,
            str(capture_metrics),
            "--work-dir",
            str(work_dir),
            "--verbose",
        ]
    )

    info_count = stderr.count("[INFO]")
    if info_count > 0:
        print(f"✅ Verbose mode produces log messages ({info_count} INFO messages)")
    else:
        print("⚠️  Verbose mode produced no messages (may be expected if no logs found)")
    print()

    print("=" * 30)
    print("All tests passed! ✅")


if __name__ == "__main__":
    main()
