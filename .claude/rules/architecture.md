<!-- Source: 018_traceable_decisions.md -->
# Architecture

**Purpose:** Guide agents in capturing architectural decisions and maintaining decision traceability throughout the development lifecycle.

**Applies to:** Creating or updating documentation, reports, READMEs, and work logs.

**Reference:** See `agents/approaches/traceable-decisions-detailed-guide.md` for comprehensive decision traceability patterns.


## Core Principle


Documentation should match the **stability** of what it describes. High-specificity documentation of volatile details creates high drift risk and maintenance burden.


## Documentation Level Framework

| Detail Level                | Volatility | Document?         | Examples                                                                            |
|-----------------------------|------------|-------------------|-------------------------------------------------------------------------------------|
| **Architecture & Intent**   | Low        | ✅ Always          | "3-tier design: API → Data → Helpers"<br>"Separation enables tracker swapping"      |
| **Design Decisions**        | Low        | ✅ Always          | "Chose YAML for multiline support"<br>"File-based coordination (no infrastructure)" |
| **High-Level Structure**    | Medium     | ✅ Yes             | "Main API in root directory"<br>"Data files in issue-definitions/"                  |
| **Key Entry Points**        | Medium     | ✅ Yes             | "Main script: create-issues.sh"<br>"Config: config/settings.yml"                    |
| **Component Relationships** | Medium     | ✅ Yes             | "Service A calls Service B via REST"<br>"Frontend reads from cache layer"           |
| **File Inventory**          | High       | ⚠️ Reference only | "See directory listing"<br>"Run: ls -la for current files"                          |
| **Implementation Details**  | High       | ⚠️ Code documents | Function names, variable names, etc.                                                |
| **Per-File Comments**       | Very High  | ❌ Don't document  | "script.sh # Does X" (file does this)                                               |
| **Line Numbers**            | Very High  | ❌ Never           | "See line 42" (will change immediately)                                             |


## Guidelines for Agents

### ✅ DO Document:

1. **Why decisions were made**
    - Rationale, alternatives considered, trade-offs
    - Example: "Chose grep/awk over yq for reliability and no dependencies"

2. **Architectural intent**
    - Purpose of layers, boundaries, patterns
    - Example: "Tier 3 provides tracker abstraction for easy swapping"

3. **Key relationships**
    - How components interact, data flow
    - Example: "Engine reads YAML → parses → calls helpers → creates issues"

4. **Usage patterns**
    - How to use the system, common commands
    - Example: "Run with --dry-run to preview before creating"

5. **Stability markers**
    - What's stable vs. experimental
    - Example: "API stable. Internal parsing may change."

### ❌ DON'T Document:

1. **Facts that change frequently**
    - File counts, line counts, specific filenames
    - Bad: "Contains 13 YAML files" (will change)
    - Good: "YAML files in issue-definitions/" (location stable)

2. **Details visible in code**
    - Function signatures, variable names
    - Bad: "Function create_issue(title, body, labels)"
    - Good: "Helper functions handle GitHub API calls"

3. **Current state details**
    - Exact configuration values, current version numbers
    - Bad: "Currently v2.0.1 with 15 features"
    - Good: "See CHANGELOG.md for version history"

4. **Exhaustive enumerations**
    - Complete lists of files, all options
    - Bad: "Files: a.yml, b.yml, c.yml, d.yml..." (13 files listed)
    - Good: "Files: *-epic.yml (epics), *-issues.yml (issues)"


## Practical Application
