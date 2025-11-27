<!-- The following information is to be interpreted literally -->

# 018 Documentation Level Framework Directive

**Purpose:** Guide agents in choosing appropriate documentation detail levels to minimize drift and maintenance burden.

**Applies to:** Creating or updating documentation, reports, READMEs, and work logs.

**Reference:** See `agents/approaches/traceable-decisions-detailed-guide.md` for comprehensive decision traceability patterns.

---

## Core Principle

> **Document decisions and intent at the level they're made.**  
> **Let code and file structure document implementation details.**

Documentation should match the **stability
** of what it describes. High-specificity documentation of volatile details creates high drift risk and maintenance burden.

---

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

---

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

---

## Practical Application

### Example: Directory Structure Documentation

**❌ Too Specific (High Drift Risk):**

```markdown
ops/scripts/planning/
├── README.md # This file
├── create-issues.sh # Main API: 400 lines
├── helper.py # Helper: 150 lines
├── utils.sh # Utilities: 75 lines
├── github-helpers/ # 2 files
│ ├── create-issue.sh # GitHub issue creation
│ └── helpers.sh # Helper functions
└── issue-definitions/ # 13 YAML files
├── architecture-epic.yml # Architecture epic
├── architecture-issues.yml # 3 architecture issues
├── build-cicd-epic.yml # Build epic
[... 9 more files listed ...]
```

**✅ Appropriate Level (Low Drift Risk):**

```markdown
ops/scripts/planning/
├── create-issues.sh # Main API (Tier 1)
├── github-helpers/ # Tracker abstraction (Tier 3)
└── issue-definitions/ # YAML definitions (Tier 2)

Key entry point: create-issues.sh
Issue definitions: issue-definitions/*.yml

> Note: See directory for complete file listing.
> File system is the source of truth.
```

---

## Integration with Other Directives

**When writing documentation or reports:**

- Follow this framework for detail level decisions
- Reference `traceable-decisions-detailed-guide.md` for architectural decision documentation
- Apply Directive 014 (Work Log Creation) for execution documentation
- Apply Directive 015 (Store Prompts) for prompt analysis

**When creating ADRs:**

- Focus on decisions and rationale (stable)
- Link to code for implementation (volatile)
- Document "why" not "what" (code shows "what")

---

## Quick Decision Matrix

**Ask yourself:** "How often will this information change?"

- **Rarely (> 6 months):** ✅ Document it
- **Sometimes (1-6 months):** ⚠️ Document at high level, reference details
- **Often (< 1 month):** ❌ Don't document, let code/structure show it

**Ask yourself:** "Can someone discover this easily another way?"

- **No, requires context/history:** ✅ Document it
- **Yes, from code/structure:** ❌ Reference it, don't duplicate

---

## Examples from Repository

### ✅ Good Documentation

- `docs/architecture/adrs/ADR-*.md` - Design decisions with rationale
- `agents/approaches/*.md` - Patterns and architectural approaches
- `ops/scripts/planning/README.md` - Architecture and usage (not file inventory)

### ⚠️ Could Improve

- Detailed file trees with per-file comments (high drift)
- Complete enumerations of current features (changes frequently)
- Line-by-line code explanations (code is source of truth)

---

**Summary:** Document the **stable intent** behind your work, not the **volatile details
**. Let code, file structure, and discovery tools document the specifics.

_Directive 018 - Documentation Level Framework_  
_Last Updated: 2025-11-27_

