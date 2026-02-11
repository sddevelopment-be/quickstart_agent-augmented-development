#!/bin/bash
# Integration test for error reporting system
# Tests the complete workflow from error generation to artifact creation

set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd -- "$SCRIPT_DIR/.." && pwd)
cd "$REPO_ROOT"

echo "🧪 Testing Agent-Friendly Error Reporting System"
echo "================================================"
echo ""

# Create test output directory
TEST_OUTPUT="$(mktemp -d)"
trap "rm -rf $TEST_OUTPUT" EXIT

echo "📁 Test directory: $TEST_OUTPUT"
echo ""

# Test 1: Generate sample error output
echo "Test 1: Creating sample validation errors..."
cat > "$TEST_OUTPUT/sample_errors.txt" << 'EOF'
❌ work/collaboration/done/task1.yaml: invalid status 'foo', expected one of ['done', 'error', 'assigned']
❌ work/collaboration/done/task2.yaml:5: missing required field: agent
⚠️ work/collaboration/done/task3.yaml: ISO8601 timestamp should end with Z
❗️ Missing required directory: work/reports
EOF

echo "✅ Sample errors created"
echo ""

# Test 2: Run error summary generator
echo "Test 2: Running error summary generator..."
python3 tools/scripts/generate-error-summary.py \
  --workflow "Test Workflow" \
  --job "test-job" \
  --validator "test-validator" \
  --input "$TEST_OUTPUT/sample_errors.txt" \
  --output-json "$TEST_OUTPUT/errors.json" \
  --output-markdown "$TEST_OUTPUT/errors.md" \
  > "$TEST_OUTPUT/stdout.txt" 2>&1

if [ $? -eq 0 ]; then
  echo "✅ Error summary generator completed"
else
  echo "❌ Error summary generator failed"
  cat "$TEST_OUTPUT/stdout.txt"
  exit 1
fi
echo ""

# Test 3: Validate JSON output
echo "Test 3: Validating JSON output..."
if [ ! -f "$TEST_OUTPUT/errors.json" ]; then
  echo "❌ JSON file not created"
  exit 1
fi

# Check JSON is valid
if ! python3 -m json.tool "$TEST_OUTPUT/errors.json" > /dev/null 2>&1; then
  echo "❌ Invalid JSON format"
  cat "$TEST_OUTPUT/errors.json"
  exit 1
fi

# Check required fields
WORKFLOW=$(python3 -c "import json; print(json.load(open('$TEST_OUTPUT/errors.json'))['workflow'])")
if [ "$WORKFLOW" != "Test Workflow" ]; then
  echo "❌ Workflow name mismatch"
  exit 1
fi

ERROR_COUNT=$(python3 -c "import json; print(json.load(open('$TEST_OUTPUT/errors.json'))['summary']['total_errors'])")
if [ "$ERROR_COUNT" -lt 1 ]; then
  echo "❌ No errors captured"
  exit 1
fi

echo "✅ JSON output valid"
echo "  - Workflow: $WORKFLOW"
echo "  - Errors: $ERROR_COUNT"
echo ""

# Test 4: Validate Markdown output
echo "Test 4: Validating Markdown output..."
if [ ! -f "$TEST_OUTPUT/errors.md" ]; then
  echo "❌ Markdown file not created"
  exit 1
fi

# Check for required sections
if ! grep -q "# 🔍 Error Summary" "$TEST_OUTPUT/errors.md"; then
  echo "❌ Missing header in Markdown"
  exit 1
fi

if ! grep -q "Issues by Validator" "$TEST_OUTPUT/errors.md"; then
  echo "❌ Missing validator section in Markdown"
  exit 1
fi

echo "✅ Markdown output valid"
echo ""

# Test 5: Display sample outputs
echo "Test 5: Sample outputs..."
echo ""
echo "--- JSON Sample (first 20 lines) ---"
head -20 "$TEST_OUTPUT/errors.json"
echo ""
echo "--- Markdown Sample (first 30 lines) ---"
head -30 "$TEST_OUTPUT/errors.md"
echo ""

# Test 6: Test shell wrapper
echo "Test 6: Testing shell wrapper..."
bash tools/scripts/generate-error-summary.sh \
  --workflow "Shell Test" \
  --job "shell-job" \
  --validator "shell-validator" \
  --input "$TEST_OUTPUT/sample_errors.txt" \
  --output-json "$TEST_OUTPUT/shell_errors.json" \
  --output-markdown "$TEST_OUTPUT/shell_errors.md" \
  > "$TEST_OUTPUT/shell_stdout.txt" 2>&1

if [ $? -eq 0 ]; then
  echo "✅ Shell wrapper completed"
else
  echo "❌ Shell wrapper failed"
  cat "$TEST_OUTPUT/shell_stdout.txt"
  exit 1
fi
echo ""

# Test 7: Verify shell wrapper outputs
echo "Test 7: Validating shell wrapper outputs..."
if [ ! -f "$TEST_OUTPUT/shell_errors.json" ]; then
  echo "❌ Shell wrapper did not create JSON"
  exit 1
fi

if [ ! -f "$TEST_OUTPUT/shell_errors.md" ]; then
  echo "❌ Shell wrapper did not create Markdown"
  exit 1
fi

echo "✅ Shell wrapper outputs valid"
echo ""

# Summary
echo "================================================"
echo "✅ All error reporting tests passed!"
echo ""
echo "Artifacts created in: $TEST_OUTPUT"
echo "  - errors.json (Python script)"
echo "  - errors.md (Python script)"
echo "  - shell_errors.json (Shell wrapper)"
echo "  - shell_errors.md (Shell wrapper)"
echo ""
echo "🎉 Error reporting system is ready for use!"
