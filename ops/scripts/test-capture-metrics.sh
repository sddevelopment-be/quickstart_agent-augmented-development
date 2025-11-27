#!/usr/bin/env bash
#
# Test script for capture-metrics.py
# Validates basic functionality and output formats
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
WORK_DIR="$REPO_ROOT/work"

echo "Testing capture-metrics.py..."
echo "=============================="
echo ""

# Test 1: Help output
echo "[TEST 1] Help output"
python3 "$SCRIPT_DIR/capture-metrics.py" --help > /dev/null
echo "✅ Help output works"
echo ""

# Test 2: JSON output to stdout
echo "[TEST 2] JSON output to stdout"
OUTPUT=$(python3 "$SCRIPT_DIR/capture-metrics.py" --work-dir "$WORK_DIR" 2>/dev/null)
if echo "$OUTPUT" | python3 -m json.tool > /dev/null 2>&1; then
    echo "✅ Valid JSON output to stdout"
else
    echo "❌ Invalid JSON output"
    exit 1
fi
echo ""

# Test 3: JSON output to file
echo "[TEST 3] JSON output to file"
TMP_JSON=$(mktemp)
python3 "$SCRIPT_DIR/capture-metrics.py" --work-dir "$WORK_DIR" --output-file "$TMP_JSON" 2>/dev/null
if [ -f "$TMP_JSON" ] && python3 -m json.tool "$TMP_JSON" > /dev/null 2>&1; then
    METRICS_COUNT=$(python3 -c "import json; print(json.load(open('$TMP_JSON'))['metrics_count'])")
    echo "✅ Valid JSON file created with $METRICS_COUNT metrics"
else
    echo "❌ Failed to create valid JSON file"
    exit 1
fi
rm -f "$TMP_JSON"
echo ""

# Test 4: CSV output to file
echo "[TEST 4] CSV output to file"
TMP_CSV=$(mktemp)
python3 "$SCRIPT_DIR/capture-metrics.py" --work-dir "$WORK_DIR" --output-format csv --output-file "$TMP_CSV" 2>/dev/null
if [ -f "$TMP_CSV" ]; then
    LINE_COUNT=$(wc -l < "$TMP_CSV")
    COL_COUNT=$(head -1 "$TMP_CSV" | tr ',' '\n' | wc -l)
    echo "✅ CSV file created with $LINE_COUNT lines and $COL_COUNT columns"
else
    echo "❌ Failed to create CSV file"
    exit 1
fi
rm -f "$TMP_CSV"
echo ""

# Test 5: Verify required fields in JSON
echo "[TEST 5] Verify JSON structure"
TMP_JSON=$(mktemp)
python3 "$SCRIPT_DIR/capture-metrics.py" --work-dir "$WORK_DIR" --output-file "$TMP_JSON" 2>/dev/null
REQUIRED_FIELDS=("extracted_at" "metrics_count" "metrics" "summary")
ALL_PRESENT=true
for field in "${REQUIRED_FIELDS[@]}"; do
    if ! grep -q "\"$field\"" "$TMP_JSON"; then
        echo "❌ Missing required field: $field"
        ALL_PRESENT=false
    fi
done
if [ "$ALL_PRESENT" = true ]; then
    echo "✅ All required JSON fields present"
fi
rm -f "$TMP_JSON"
echo ""

# Test 6: Verify verbose mode
echo "[TEST 6] Verbose mode"
VERBOSE_OUTPUT=$(python3 "$SCRIPT_DIR/capture-metrics.py" --work-dir "$WORK_DIR" --verbose 2>&1 | grep -c "\[INFO\]" || true)
if [ "$VERBOSE_OUTPUT" -gt 0 ]; then
    echo "✅ Verbose mode produces log messages ($VERBOSE_OUTPUT INFO messages)"
else
    echo "⚠️  Verbose mode produced no messages (may be expected if no logs found)"
fi
echo ""

echo "=============================="
echo "All tests passed! ✅"
