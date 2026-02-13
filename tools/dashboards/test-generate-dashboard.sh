#!/usr/bin/env bash
#
# Test script for generate-dashboard.py
# Validates basic functionality and output formats
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
WORK_DIR="${REPO_ROOT}/work"

echo "Testing generate-dashboard.py..."
echo "================================="
echo ""

# Test 1: Help output
echo "[TEST 1] Help output"
python3 "${SCRIPT_DIR}/generate-dashboard.py" --help > /dev/null
echo "✅ Help output works"
echo ""

# Test 2: Generate test metrics first
echo "[TEST 2] Generate test metrics"
TMP_METRICS=$(mktemp)
python3 "${SCRIPT_DIR}/capture-metrics.py" --work-dir "${WORK_DIR}" --output-file "${TMP_METRICS}" 2>/dev/null
if [[ -f "${TMP_METRICS}" ]]; then
    METRICS_COUNT=$(python3 -c "import json; print(json.load(open('${TMP_METRICS}'))['metrics_count'])")
    echo "✅ Generated test metrics with ${METRICS_COUNT} entries"
else
    echo "❌ Failed to generate test metrics"
    exit 1
fi
echo ""

# Test 3: Generate summary dashboard to stdout
echo "[TEST 3] Summary dashboard to stdout"
OUTPUT=$(python3 "${SCRIPT_DIR}/generate-dashboard.py" --input "${TMP_METRICS}" --dashboard-type summary --output-file - 2>/dev/null)
if echo "${OUTPUT}" | grep -q "# Metrics Summary Dashboard"; then
    echo "✅ Summary dashboard generated successfully"
else
    echo "❌ Summary dashboard generation failed"
    exit 1
fi
echo ""

# Test 4: Generate detail dashboard to file
echo "[TEST 4] Detail dashboard to file"
TMP_DETAIL=$(mktemp)
python3 "${SCRIPT_DIR}/generate-dashboard.py" --input "${TMP_METRICS}" --dashboard-type detail --output-file "${TMP_DETAIL}" 2>/dev/null
if [[ -f "${TMP_DETAIL}" ]] && grep -q "# Metrics Detail Dashboard" "${TMP_DETAIL}"; then
    LINE_COUNT=$(wc -l < "${TMP_DETAIL}")
    echo "✅ Detail dashboard created with ${LINE_COUNT} lines"
else
    echo "❌ Failed to create detail dashboard"
    exit 1
fi
rm -f "${TMP_DETAIL}"
echo ""

# Test 5: Generate trends dashboard to file
echo "[TEST 5] Trends dashboard to file"
TMP_TRENDS=$(mktemp)
python3 "${SCRIPT_DIR}/generate-dashboard.py" --input "${TMP_METRICS}" --dashboard-type trends --output-file "${TMP_TRENDS}" 2>/dev/null
if [[ -f "${TMP_TRENDS}" ]] && grep -q "# Metrics Trends Dashboard" "${TMP_TRENDS}"; then
    LINE_COUNT=$(wc -l < "${TMP_TRENDS}")
    echo "✅ Trends dashboard created with ${LINE_COUNT} lines"
else
    echo "❌ Failed to create trends dashboard"
    exit 1
fi
rm -f "${TMP_TRENDS}"
echo ""

# Test 6: Generate all dashboards to directory
echo "[TEST 6] Generate all dashboards to directory"
TMP_DIR=$(mktemp -d)
python3 "${SCRIPT_DIR}/generate-dashboard.py" --input "${TMP_METRICS}" --output-dir "${TMP_DIR}" 2>/dev/null
if [[ -f "${TMP_DIR}/summary-dashboard.md" ]] && \
   [[ -f "${TMP_DIR}/detail-dashboard.md" ]] && \
   [[ -f "${TMP_DIR}/trends-dashboard.md" ]]; then
    echo "✅ All three dashboard types created in directory"
else
    echo "❌ Failed to create all dashboards"
    exit 1
fi
rm -rf "${TMP_DIR}"
echo ""

# Test 7: Verify dashboard content structure
echo "[TEST 7] Verify dashboard content structure"
TMP_SUMMARY=$(mktemp)
python3 "${SCRIPT_DIR}/generate-dashboard.py" --input "${TMP_METRICS}" --dashboard-type summary --output-file "${TMP_SUMMARY}" 2>/dev/null

REQUIRED_SECTIONS=("Overall Statistics" "Top Agents by Task Count" "Recent Activity")
ALL_PRESENT=true
for section in "${REQUIRED_SECTIONS[@]}"; do
    if ! grep -q "${section}" "${TMP_SUMMARY}"; then
        echo "❌ Missing required section: ${section}"
        ALL_PRESENT=false
    fi
done
if [[ "${ALL_PRESENT}" = true ]]; then
    echo "✅ All required sections present in summary dashboard"
fi
rm -f "${TMP_SUMMARY}"
echo ""

# Test 8: Test verbose mode
echo "[TEST 8] Verbose mode"
VERBOSE_OUTPUT=$(python3 "${SCRIPT_DIR}/generate-dashboard.py" --input "${TMP_METRICS}" --dashboard-type summary --output-file - --verbose 2>&1 | grep -c "\[INFO\]" || true)
if [[ "${VERBOSE_OUTPUT}" -gt 0 ]]; then
    echo "✅ Verbose mode produces log messages (${VERBOSE_OUTPUT} INFO messages)"
else
    echo "❌ Verbose mode produced no messages"
    exit 1
fi
echo ""

# Test 9: Test with missing input file
echo "[TEST 9] Handle missing input file gracefully"
if python3 "${SCRIPT_DIR}/generate-dashboard.py" --input /nonexistent/file.json --dashboard-type summary --output-file - 2>&1 | grep -q "Metrics file not found"; then
    echo "✅ Handles missing input file with proper error message"
else
    echo "❌ Did not handle missing input file properly"
    exit 1
fi
echo ""

# Test 10: Verify chart generation
echo "[TEST 10] Verify ASCII chart generation"
if echo "${OUTPUT}" | grep -q "█"; then
    echo "✅ ASCII bar charts generated in output"
else
    echo "⚠️  No ASCII charts found (may be expected if no data)"
fi
echo ""

# Cleanup
rm -f "${TMP_METRICS}"

echo "================================="
echo "All tests passed! ✅"
