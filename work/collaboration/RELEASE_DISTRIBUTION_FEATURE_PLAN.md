# Release/Distribution Feature Implementation Plan

**Coordinator:** Manager Mike  
**Date:** 2025-11-24T20:00:00Z  
**Status:** Tasks Created - Awaiting Assignment

## Overview

This plan decomposes the release/distribution feature (ADR-013, ADR-014) into actionable tasks following the file-based orchestration approach. The feature enables downstream repositories to adopt and upgrade the agent-augmented development framework through zip-based releases with automated audit and upgrade assistance.

## Architecture References

- **ADR-013:** Zip-Based Framework Distribution
- **ADR-014:** Framework Guardian Agent
- **Architecture Vision:** `docs/architecture/design/distribution_of_releases_architecture.md`
- **Technical Design:** `docs/architecture/design/distribution_of_releases_technical_design.md`

## Task Breakdown

### 1. Packaging Pipeline (Critical Priority)
**Task ID:** `2025-11-24T1954-build-automation-packaging-pipeline`  
**Agent:** build-automation  
**Effort:** 1-2 days  
**Dependencies:** None (foundational)

**Deliverables:**
- `scripts/framework_package.sh` - Creates release zip with proper structure
- `META/MANIFEST.yml` - File inventory with sha256 checksums
- `.github/workflows/release-packaging.yml` - CI automation
- `docs/HOW_TO_USE/release-process.md` - Process documentation

**Critical Path:** This task blocks install/upgrade scripts and Guardian implementation.

### 2. Installation Script (High Priority)
**Task ID:** `2025-11-24T1955-build-automation-install-script`  
**Agent:** build-automation  
**Effort:** 1 day  
**Dependencies:** Task 1 (for MANIFEST.yml format)

**Deliverables:**
- `scripts/framework_install.sh` - First-time installation logic
- `scripts/tests/test_framework_install.sh` - Test suite
- `docs/HOW_TO_USE/framework-installation.md` - User guide

**Key Features:**
- Detects first-time vs. existing install
- Never overwrites existing files
- Creates `.framework_meta.yml` tracking

### 3. Upgrade Script (High Priority)
**Task ID:** `2025-11-24T1956-build-automation-upgrade-script`  
**Agent:** build-automation  
**Effort:** 1.5 days  
**Dependencies:** Tasks 1, 2 (for manifest and meta formats)

**Deliverables:**
- `scripts/framework_upgrade.sh` - Upgrade with conflict detection
- `scripts/tests/test_framework_upgrade.sh` - Test suite
- `docs/HOW_TO_USE/framework-upgrades.md` - User guide

**Key Features:**
- `--dry-run` support for previewing changes
- Writes `.framework-new` for conflicts
- Generates `upgrade-report.txt` summary
- Never touches `local/**` directories

### 4. Framework Guardian Profile (High Priority)
**Task ID:** `2025-11-24T1957-architect-framework-guardian-profile`  
**Agent:** architect  
**Effort:** 0.5-1 day  
**Dependencies:** None (can proceed in parallel)

**Deliverables:**
- `.github/agents/framework-guardian.agent.md` - Agent specification
- `docs/templates/framework/TEMPLATE_AUDIT_REPORT.md` - Audit report template
- `docs/templates/framework/TEMPLATE_FRAMEWORK_UPDATE_PLAN.md` - Upgrade plan template
- `docs/HOW_TO_USE/framework-guardian.md` - Guardian usage guide

**Key Specifications:**
- Two modes: Audit and Upgrade
- Strict guardrails (no automatic overwrites)
- Context loading order defined

### 5. Guardian Implementation (High Priority)
**Task ID:** `2025-11-24T1958-backend-dev-guardian-implementation`  
**Agent:** backend-dev  
**Effort:** 2-3 days  
**Dependencies:** Tasks 1, 3, 4 (for formats and spec)

**Deliverables:**
- `work/scripts/framework_guardian.py` - Core implementation
- `work/scripts/tests/test_framework_guardian.py` - Test suite
- `validation/FRAMEWORK_AUDIT_REPORT.md` - Example audit output
- `validation/FRAMEWORK_UPGRADE_PLAN.md` - Example upgrade plan

**Key Features:**
- CLI with `--mode audit|upgrade`
- Reads MANIFEST.yml, .framework_meta.yml, upgrade-report.txt
- Classifies conflicts and proposes resolutions
- Outputs structured Markdown reports

### 6. User Documentation (Medium Priority)
**Task ID:** `2025-11-24T1959-writer-editor-release-documentation`  
**Agent:** writer-editor  
**Effort:** 1-1.5 days  
**Dependencies:** Tasks 1, 2, 3, 4 (for understanding workflows)

**Deliverables:**
- `docs/HOW_TO_USE/framework-releases.md` - Release overview
- `docs/HOW_TO_USE/upgrading-framework.md` - Upgrade walkthrough
- `docs/HOW_TO_USE/troubleshooting-upgrades.md` - Common issues
- `META/RELEASE_NOTES_TEMPLATE.md` - Release notes template
- `META/UPGRADE_NOTES_TEMPLATE.md` - Upgrade notes template

**Focus Areas:**
- Clear step-by-step instructions
- Examples and screenshots
- Troubleshooting common scenarios

### 7. Integration Testing (High Priority)
**Task ID:** `2025-11-24T2000-build-automation-integration-testing`  
**Agent:** build-automation  
**Effort:** 1-1.5 days  
**Dependencies:** Tasks 1, 2, 3, 5 (complete workflow)

**Deliverables:**
- `scripts/tests/integration_test_release_workflow.sh` - E2E tests
- `scripts/tests/fixtures/test_project_v1/` - Test fixtures
- `scripts/tests/fixtures/test_project_v2/` - Test fixtures
- `docs/HOW_TO_USE/testing-releases.md` - Testing guide

**Test Scenarios:**
- New installation
- Upgrade with no conflicts
- Upgrade with conflicts
- Guardian audit mode
- Guardian upgrade mode

## Execution Strategy

### Phase 1: Foundation (Days 1-2)
- **Task 1:** Packaging pipeline (critical path)
- **Task 4:** Guardian profile (parallel work)

### Phase 2: Core Scripts (Days 3-4)
- **Task 2:** Install script
- **Task 3:** Upgrade script

### Phase 3: Guardian & Documentation (Days 5-7)
- **Task 5:** Guardian implementation
- **Task 6:** User documentation (can start earlier with partial info)

### Phase 4: Validation (Day 8)
- **Task 7:** Integration testing
- Final validation and adjustments

## Success Criteria

✅ **Packaging:** CI generates valid `quickstart-framework-<version>.zip` with complete MANIFEST.yml  
✅ **Installation:** New projects can install framework without errors  
✅ **Upgrades:** Conflicts detected and written as `.framework-new` files  
✅ **Guardian Audit:** Reports missing/outdated/misplaced files accurately  
✅ **Guardian Upgrade:** Proposes actionable conflict resolutions  
✅ **Documentation:** Clear end-to-end guides for adopters  
✅ **Testing:** Integration tests pass in CI pipeline  

## Estimated Timeline

- **Total Effort:** 8-11 workdays (across 4 agents)
- **Elapsed Time:** 8-10 calendar days (with parallel work)
- **Urgency:** High (required before next public release per technical design)

## Agent Workload Distribution

| Agent             | Tasks | Estimated Effort | Priority Mix        |
|-------------------|-------|------------------|---------------------|
| build-automation  | 4     | 5-6.5 days       | 1 critical, 3 high  |
| architect         | 1     | 0.5-1 day        | 1 high              |
| backend-dev       | 1     | 2-3 days         | 1 high              |
| writer-editor     | 1     | 1-1.5 days       | 1 medium            |

## Risk Assessment

**High Risk:**
- ⚠️ Packaging pipeline CI configuration complexity
- ⚠️ Cross-platform script compatibility (Windows/WSL, macOS, Linux)
- ⚠️ Checksum calculation performance on large repos

**Mitigation:**
- Thorough shellcheck validation
- Test on multiple platforms
- Optimize checksum calculation (size/timestamp filtering)

**Medium Risk:**
- ⚠️ Guardian conflict classification accuracy
- ⚠️ Template format evolution

**Mitigation:**
- Start with simple classification rules, iterate
- Version templates and maintain backward compatibility

## Next Steps

1. ✅ Tasks created in `work/inbox/`
2. ⏳ Orchestrator assigns Task 1 (packaging pipeline) to build-automation
3. ⏳ Orchestrator assigns Task 4 (Guardian profile) to architect
4. ⏳ Monitor progress and adjust sequence based on actual completion times
5. ⏳ Coordinate handoffs between agents as dependencies resolve

## Related Documentation

- File-Based Orchestration: `.github/agents/approaches/file-based-orchestration.md`
- Task Lifecycle: `ADR-003`
- Work Directory Structure: `ADR-004`
- Orchestration Metrics: `ADR-009`

---

_Plan coordinated by: Manager Mike_  
_Review status: Ready for execution_  
_Next review: After Phase 1 completion_
