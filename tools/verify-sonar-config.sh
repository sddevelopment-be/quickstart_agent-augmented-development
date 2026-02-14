#!/bin/bash
# verify-sonar-config.sh
# Verify SonarQube configuration for coverage integration
# Usage: bash tools/verify-sonar-config.sh

set -e

echo "🔍 Verifying SonarQube Coverage Integration Configuration"
echo "=========================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

# Check if sonar-project.properties exists
echo -e "\n📄 Checking sonar-project.properties..."
if [[ -f "sonar-project.properties" ]]; then
    echo -e "${GREEN}✓${NC} sonar-project.properties exists"
else
    echo -e "${RED}✗${NC} sonar-project.properties not found"
    ((ERRORS++))
    exit 1
fi

# Check required properties
echo -e "\n🔧 Checking required SonarQube properties..."

check_property() {
    local prop=$1
    local description=$2
    
    if grep -q "^${prop}=" sonar-project.properties; then
        local value
        value=$(grep "^${prop}=" sonar-project.properties | cut -d'=' -f2-)
        echo -e "${GREEN}✓${NC} ${description}: ${value}"
    else
        echo -e "${RED}✗${NC} ${description} not configured"
        ((ERRORS++))
    fi
}

check_property "sonar.projectKey" "Project Key"
check_property "sonar.organization" "Organization"
check_property "sonar.sources" "Source Directories"
check_property "sonar.tests" "Test Directories"
check_property "sonar.python.coverage.reportPaths" "Coverage Report Path"

# Check if coverage report path is correct
echo -e "\n📊 Checking coverage report configuration..."
COVERAGE_PATH=$(grep "^sonar.python.coverage.reportPaths=" sonar-project.properties | cut -d'=' -f2- | tr -d ' \r\n')
if [[ "${COVERAGE_PATH}" = "coverage.xml" ]]; then
    echo -e "${GREEN}✓${NC} Coverage path correctly set to coverage.xml"
else
    echo -e "${YELLOW}⚠${NC} Coverage path is '${COVERAGE_PATH}', expected 'coverage.xml'"
    ((WARNINGS++))
fi

# Check workflow configuration
echo -e "\n🔄 Checking GitHub workflow configuration..."
WORKFLOW_FILE=".github/workflows/validation-enhanced.yml"

if [[ -f "${WORKFLOW_FILE}" ]]; then
    echo -e "${GREEN}✓${NC} Workflow file exists"
    
    # Check if sonarqube job has dependency on unit-tests
    if grep -A 3 "sonarqube:" "${WORKFLOW_FILE}" | grep -q "needs: unit-tests"; then
        echo -e "${GREEN}✓${NC} SonarQube job depends on unit-tests"
    else
        echo -e "${RED}✗${NC} SonarQube job missing 'needs: unit-tests' dependency"
        ((ERRORS++))
    fi
    
    # Check if coverage artifacts are downloaded
    if grep -A 20 "sonarqube:" "${WORKFLOW_FILE}" | grep -q "download-artifact"; then
        echo -e "${GREEN}✓${NC} SonarQube job downloads artifacts"
        
        # Check artifact name
        if grep -A 20 "sonarqube:" "${WORKFLOW_FILE}" | grep -A 2 "download-artifact" | grep -q "name: coverage-reports"; then
            echo -e "${GREEN}✓${NC} Correct artifact name: coverage-reports"
        else
            echo -e "${RED}✗${NC} Artifact name mismatch or not specified"
            ((ERRORS++))
        fi
    else
        echo -e "${RED}✗${NC} SonarQube job does not download coverage artifacts"
        ((ERRORS++))
    fi
    
    # Check if unit-tests job uploads coverage artifacts
    if grep -A 100 "unit-tests:" "${WORKFLOW_FILE}" | grep -B 5 "coverage-reports" | grep -q "upload-artifact"; then
        echo -e "${GREEN}✓${NC} Unit-tests job uploads coverage artifacts"
    else
        echo -e "${YELLOW}⚠${NC} Cannot confirm unit-tests uploads coverage artifacts"
        ((WARNINGS++))
    fi
else
    echo -e "${RED}✗${NC} Workflow file not found: ${WORKFLOW_FILE}"
    ((ERRORS++))
fi

# Check if source directories exist
echo -e "\n📁 Checking source directories..."
SOURCES=$(grep "^sonar.sources=" sonar-project.properties | cut -d'=' -f2- | tr -d '\r\n')
IFS=',' read -ra SOURCE_DIRS <<< "${SOURCES}"

for dir in "${SOURCE_DIRS[@]}"; do
    # Trim whitespace
    dir=$(echo "${dir}" | xargs)
    if [[ -d "${dir}" ]]; then
        echo -e "${GREEN}✓${NC} Source directory exists: ${dir}"
    else
        echo -e "${RED}✗${NC} Source directory not found: ${dir}"
        ((ERRORS++))
    fi
done

# Check if test directory exists
TESTS=$(grep "^sonar.tests=" sonar-project.properties | cut -d'=' -f2- | tr -d '\r\n' | xargs)
if [[ -d "${TESTS}" ]]; then
    echo -e "${GREEN}✓${NC} Test directory exists: ${TESTS}"
else
    echo -e "${RED}✗${NC} Test directory not found: ${TESTS}"
    ((ERRORS++))
fi

# Summary
echo -e "\n=========================================================="
echo "📋 Verification Summary"
echo "=========================================================="

if [[ ${ERRORS} -eq 0 ]] && [[ ${WARNINGS} -eq 0 ]]; then
    echo -e "${GREEN}✅ All checks passed!${NC}"
    echo "   SonarQube coverage integration is properly configured."
    exit 0
elif [[ ${ERRORS} -eq 0 ]]; then
    echo -e "${YELLOW}⚠ Configuration OK with warnings${NC}"
    echo "   Errors: ${ERRORS}"
    echo "   Warnings: ${WARNINGS}"
    exit 0
else
    echo -e "${RED}❌ Configuration has errors${NC}"
    echo "   Errors: ${ERRORS}"
    echo "   Warnings: ${WARNINGS}"
    echo ""
    echo "Please fix the errors above before running the workflow."
    exit 1
fi
