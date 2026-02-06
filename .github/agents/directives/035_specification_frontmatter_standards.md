# Directive 035: Specifications Directory Structure and Frontmatter Standards

**Status:** Active  
**Introduced:** 2026-02-06  
**Applies to:** Planning Petra, Manager Mike, Analyst Annie, Architect Alphonso  
**Related Directives:** 034 (Specification-Driven Development), 016 (ATDD), 018 (Traceable Decisions), 022 (Audience-Oriented Writing)

---

## Purpose

Establish **mandatory standards** for specification directory structure, YAML frontmatter format, and feature organization to ensure specifications integrate correctly with the dashboard portfolio view and task linking system.

This directive complements Directive 034 (Specification-Driven Development) by defining the **technical structure** that enables programmatic consumption of specifications by dashboard services.

---

## Core Principle

Every specification MUST include YAML frontmatter with a standardized structure. This frontmatter serves as:
1. **Machine-readable metadata** for portfolio tracking (ADR-037)
2. **Feature hierarchy definition** for task-to-feature linking
3. **Progress tracking foundation** for initiative rollup calculations
4. **Searchable index** for dashboard assignment features

---

## Mandatory Directory Structure

```
specifications/
├── README.md                       # Overview and guidance (see below)
├── {initiative-slug}/              # Initiative-specific subdirectories
│   ├── {feature-1-slug}.md        # Specification with YAML frontmatter
│   ├── {feature-2-slug}.md        # Each spec = one major feature/capability
│   └── {feature-3-slug}.md
└── {another-initiative-slug}/
    ├── {spec-a}.md
    └── {spec-b}.md
```

**Examples:**
```
specifications/
├── llm-dashboard/
│   ├── markdown-rendering.md
│   ├── priority-editing.md
│   ├── initiative-tracking.md
│   └── orphan-task-assignment.md
├── llm-service/
│   ├── anthropic-adapter.md
│   ├── openai-adapter.md
│   └── telemetry-collection.md
└── framework/
    ├── agent-profiles.md
    └── file-orchestration.md
```

---

## Mandatory YAML Frontmatter Schema

Every specification file MUST begin with YAML frontmatter delimited by `---`:

```yaml
---
id: "SPEC-{INITIATIVE}-{NUMBER}"          # Unique identifier (e.g., SPEC-DASH-001)
title: "Human-Readable Specification Title"
status: "draft|active|implemented|deprecated"
initiative: "Initiative Name"              # High-level grouping (e.g., "Dashboard Enhancements")
priority: "CRITICAL|HIGH|MEDIUM|LOW"
epic: "Optional Epic Name"                 # Broader theme (e.g., "Dashboard Core Features")
target_personas: ["persona-slug-1", "persona-slug-2"]  # From docs/audience/
features:                                  # REQUIRED: Array of features within this spec
  - id: "FEAT-{INITIATIVE}-{NUMBER}-{SUBNUM}"
    title: "Feature Name"
    status: "draft|in_progress|done|blocked"
  - id: "FEAT-{INITIATIVE}-{NUMBER}-{SUBNUM}"
    title: "Another Feature Name"
    status: "draft"
completion: null|0-100                     # Overall completion percentage (null if draft)
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
author: "agent-slug"                       # Author agent (e.g., "analyst-annie")
---
```

### Field Descriptions

| Field              | Type            | Required | Description                                                                 |
|--------------------|-----------------|----------|-----------------------------------------------------------------------------|
| `id`               | String          | Yes      | Unique spec ID: `SPEC-{INITIATIVE_CODE}-{NUMBER}` (e.g., `SPEC-DASH-001`)  |
| `title`            | String          | Yes      | Human-readable specification title                                          |
| `status`           | Enum            | Yes      | `draft`, `active`, `implemented`, `deprecated`                              |
| `initiative`       | String          | Yes      | High-level grouping for portfolio rollup                                    |
| `priority`         | Enum            | Yes      | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`                                         |
| `epic`             | String          | No       | Broader theme for strategic grouping                                        |
| `target_personas`  | Array[String]   | No       | Slug names from `docs/audience/` (e.g., `software-engineer`)                |
| `features`         | Array[Object]   | Yes      | Array of feature objects (see Feature Schema below)                         |
| `completion`       | Integer or null | No       | 0-100 percentage; `null` if not started                                     |
| `created`          | Date (YYYY-MM-DD) | Yes    | Creation date                                                               |
| `updated`          | Date (YYYY-MM-DD) | Yes    | Last update date                                                            |
| `author`           | String          | Yes      | Author agent slug (e.g., `analyst-annie`)                                   |

---

## Feature Schema (Within `features:` Array)

Each feature object MUST have:

```yaml
features:
  - id: "FEAT-{INITIATIVE}-{SPEC_NUM}-{FEAT_NUM}"
    title: "Feature Title"
    status: "draft|in_progress|done|blocked"
    description: "Optional one-line summary"  # Optional
```

**Feature ID Format:**
- Pattern: `FEAT-{INITIATIVE_CODE}-{SPEC_NUM}-{FEAT_NUM}`
- Example: `FEAT-DASH-001-02` = Dashboard initiative, Spec 001, Feature 02

**Feature Status Values:**
- `draft` - Not yet started
- `in_progress` - Actively being worked on
- `done` - Completed and tested
- `blocked` - Cannot proceed (dependency or blocker)

---

## Specification Lifecycle States

### Draft
```yaml
status: "draft"
completion: null
features:
  - id: "FEAT-DASH-001-01"
    status: "draft"
```
- Initial authoring phase (Analyst Annie)
- Features defined but not implemented
- May have unresolved open questions

### Active
```yaml
status: "active"
completion: 25
features:
  - id: "FEAT-DASH-001-01"
    status: "done"
  - id: "FEAT-DASH-001-02"
    status: "in_progress"
  - id: "FEAT-DASH-001-03"
    status: "draft"
```
- Implementation in progress
- At least one feature `in_progress` or `done`
- `completion` calculated from feature status

### Implemented
```yaml
status: "implemented"
completion: 100
features:
  - id: "FEAT-DASH-001-01"
    status: "done"
  - id: "FEAT-DASH-001-02"
    status: "done"
```
- All features completed and tested
- `completion: 100`
- All feature `status: "done"`
- Specification becomes historical reference

### Deprecated
```yaml
status: "deprecated"
completion: null  # or partial if abandoned mid-implementation
```
- No longer relevant (requirements changed, feature cancelled)
- Historical record preserved

---

## Task-to-Specification Linking

Tasks link to specifications via the `specification:` field in task YAML:

**Task YAML:**
```yaml
id: 2026-02-06T1150-dashboard-initiative-tracking
title: "Dashboard Initiative Tracking Implementation"
agent: python-pedro
priority: HIGH
status: assigned
specification: "specifications/llm-dashboard/initiative-tracking.md"
feature: "Feature 3: Portfolio API Endpoint"  # Optional: link to specific feature
```

**Linking Rules:**
1. `specification:` field MUST contain relative path from repository root
2. Path MUST point to existing file in `specifications/` directory
3. Optional `feature:` field links to specific feature title from frontmatter
4. Dashboard uses this to:
   - Group tasks under correct initiative/feature in portfolio
   - Calculate progress rollup (done=100%, in_progress=50%, inbox=0%)
   - Identify orphan tasks (no `specification:` field or invalid path)

---

## Agent Responsibilities

### Analyst Annie (Primary Author)
**When creating specifications:**
1. ✅ Use `docs/templates/specifications/feature-spec-template.md` as starting point
2. ✅ Add YAML frontmatter at top of file (before markdown heading)
3. ✅ Define features with unique IDs following `FEAT-{INITIATIVE}-{SPEC_NUM}-{FEAT_NUM}` pattern
4. ✅ Set `status: "draft"` and `completion: null` for new specs
5. ✅ Include at least 1 feature (specs without features won't appear in portfolio)
6. ✅ Save to correct subdirectory: `specifications/{initiative-slug}/{spec-name}.md`

**Example workflow:**
```bash
# Annie creates new spec
specifications/llm-dashboard/orphan-task-assignment.md

# With frontmatter:
---
id: "SPEC-DASH-007"
title: "Orphan Task Assignment (Feature-Level)"
status: "draft"
initiative: "Dashboard Enhancements"
priority: "MEDIUM"
features:
  - id: "FEAT-DASH-007-01"
    title: "Assignment Modal UI"
    status: "draft"
  - id: "FEAT-DASH-007-02"
    title: "Task-to-Feature Linking API"
    status: "draft"
completion: null
created: "2026-02-06"
updated: "2026-02-06"
author: "analyst-annie"
---

# Specification: Orphan Task Assignment
...
```

---

### Planning Petra (Task Creation)
**When creating tasks from specifications:**
1. ✅ Read specification frontmatter to understand feature structure
2. ✅ Create tasks with `specification:` field pointing to spec file
3. ✅ Optionally add `feature:` field matching feature title from frontmatter
4. ✅ Ensure specification path is correct (relative to repo root)
5. ✅ Use feature titles as guidance for task breakdown

**Example workflow:**
```yaml
# Petra creates task for SPEC-DASH-007 Feature 1
id: 2026-02-06T1600-orphan-assignment-modal
title: "Implement Assignment Modal UI"
agent: frontend-freddy
priority: MEDIUM
status: inbox
specification: "specifications/llm-dashboard/orphan-task-assignment.md"
feature: "Assignment Modal UI"  # Matches FEAT-DASH-007-01 title
estimated_hours: 4
```

---

### Manager Mike (Progress Tracking)
**When monitoring initiative progress:**
1. ✅ Check portfolio view in dashboard for initiative-level rollup
2. ✅ Verify specification `completion` matches actual feature progress
3. ✅ Update specification `status` when all features complete:
   - `draft` → `active` when first task starts
   - `active` → `implemented` when all features done
4. ✅ Identify orphan tasks and assign them to specifications
5. ✅ Escalate blocked features to Architect Alphonso

**Progress Calculation Logic:**
- Feature progress = (done_tasks / total_tasks) × 100
- Specification progress = average(all feature progress)
- Initiative progress = average(all spec progress in initiative)

---

## Validation Rules

### Specification File Must:
1. ✅ Have valid YAML frontmatter (parseable by PyYAML)
2. ✅ Include all required fields: `id`, `title`, `status`, `initiative`, `priority`, `features`, `created`, `updated`, `author`
3. ✅ Have at least 1 feature in `features:` array
4. ✅ Use correct ID format: `SPEC-{CODE}-{NUMBER}`
5. ✅ Have unique ID (no duplicates across all specs)
6. ✅ Be saved in correct subdirectory: `specifications/{initiative-slug}/`

### Feature Objects Must:
1. ✅ Have `id`, `title`, `status` fields (minimum)
2. ✅ Use correct ID format: `FEAT-{CODE}-{SPEC_NUM}-{FEAT_NUM}`
3. ✅ Have unique IDs within specification
4. ✅ Have valid status: `draft`, `in_progress`, `done`, `blocked`

### Task Linking Must:
1. ✅ Use `specification:` field with path relative to repo root
2. ✅ Point to existing file in `specifications/` directory
3. ✅ If `feature:` field used, match a feature title from spec frontmatter

---

## Migration Guide for Existing Specifications

If you encounter a specification **without YAML frontmatter**:

### Step 1: Identify Missing Elements
- No `---` delimiters at start of file?
- Frontmatter missing required fields?
- Features not defined in frontmatter?

### Step 2: Extract Metadata from Markdown
```markdown
# Specification: Dashboard Task Priority Editing

**Status:** Draft  
**Created:** 2026-02-06  
...
```
→ Convert to frontmatter:
```yaml
---
id: "SPEC-DASH-001"
title: "Dashboard Task Priority Editing"
status: "draft"
...
---
```

### Step 3: Define Features
Look for functional requirements or implementation sections:
```markdown
## Functional Requirements

**FR-M1:** System MUST allow users to change task priority
**FR-M2:** System MUST update YAML file
...
```
→ Group into features:
```yaml
features:
  - id: "FEAT-DASH-001-01"
    title: "Priority Dropdown UI Component"
    status: "draft"
  - id: "FEAT-DASH-001-02"
    title: "YAML Update with Comment Preservation"
    status: "draft"
```

### Step 4: Set Status Based on Implementation
- All features implemented? → `status: "implemented"`, `completion: 100`
- Some features done? → `status: "active"`, `completion: 50`
- No features started? → `status: "draft"`, `completion: null`

### Step 5: Commit with Migration Note
```bash
git commit -m "Add YAML frontmatter to {spec-name}.md

Migrated specification to Directive 035 format:
- Added frontmatter with id, status, features
- Defined {N} features based on functional requirements
- Set status: implemented (all features complete)

Dashboard portfolio will now display this specification correctly."
```

---

## Examples

### Example 1: New Specification (Draft)

**File:** `specifications/llm-dashboard/search-functionality.md`

```yaml
---
id: "SPEC-DASH-008"
title: "Dashboard Search and Filtering"
status: "draft"
initiative: "Dashboard Enhancements"
priority: "MEDIUM"
epic: "Dashboard Productivity"
target_personas: ["software-engineer", "project-manager"]
features:
  - id: "FEAT-DASH-008-01"
    title: "Global Search Bar"
    status: "draft"
    description: "Full-text search across tasks, specs, and agents"
  - id: "FEAT-DASH-008-02"
    title: "Advanced Filtering"
    status: "draft"
    description: "Multi-criteria filters with save/load presets"
  - id: "FEAT-DASH-008-03"
    title: "Search Result Highlighting"
    status: "draft"
    description: "Highlight matching terms in results"
completion: null
created: "2026-02-07"
updated: "2026-02-07"
author: "analyst-annie"
---

# Specification: Dashboard Search and Filtering
...
```

---

### Example 2: Active Implementation

**File:** `specifications/llm-dashboard/orphan-task-assignment.md`

```yaml
---
id: "SPEC-DASH-007"
title: "Orphan Task Assignment (Feature-Level)"
status: "active"
initiative: "Dashboard Enhancements"
priority: "MEDIUM"
features:
  - id: "FEAT-DASH-007-01"
    title: "Assignment Modal UI"
    status: "in_progress"
  - id: "FEAT-DASH-007-02"
    title: "Task-to-Feature Linking API"
    status: "draft"
completion: 25
created: "2026-02-06"
updated: "2026-02-06"
author: "analyst-annie"
---
```

**Linked Task:**
```yaml
id: 2026-02-06T1600-orphan-assignment-modal
specification: "specifications/llm-dashboard/orphan-task-assignment.md"
feature: "Assignment Modal UI"
status: in_progress
```

---

### Example 3: Completed Specification

**File:** `specifications/llm-dashboard/markdown-rendering.md`

```yaml
---
id: "SPEC-DASH-002"
title: "Dashboard Markdown Rendering in Task Details"
status: "implemented"
initiative: "Dashboard Enhancements"
priority: "HIGH"
features:
  - id: "FEAT-DASH-002-01"
    title: "Core Markdown Parser Integration"
    status: "done"
  - id: "FEAT-DASH-002-02"
    title: "Selective Field Rendering"
    status: "done"
  - id: "FEAT-DASH-002-03"
    title: "Security Hardening with XSS Prevention"
    status: "done"
completion: 100
created: "2026-02-06"
updated: "2026-02-06"
author: "analyst-annie"
---
```

**Linked Tasks (both done):**
```yaml
id: 2026-02-06T1148-dashboard-markdown-rendering
specification: "specifications/llm-dashboard/markdown-rendering.md"
status: done
```

---

## Dashboard Integration Points

### Portfolio View (`/api/portfolio`)
- Reads all specifications from `specifications/` directory
- Parses YAML frontmatter to extract initiatives, features, metadata
- Links tasks via `specification:` field
- Calculates progress rollup from task statuses
- Displays hierarchical view: Initiative → Specification → Feature → Tasks

### Orphan Task Assignment
- Lists all specifications with features for modal selection
- Validates specification path before assignment
- Updates task YAML with `specification:` and `feature:` fields
- Moves task from orphan section to portfolio hierarchy

### Specification Parser (`src/llm_service/dashboard/spec_parser.py`)
- Scans `specifications/` directory recursively
- Extracts frontmatter using PyYAML
- Validates required fields
- Caches parsed results (invalidates on file watcher events)
- Provides structured data to API endpoints

---

## Troubleshooting

### Issue: Specification Not Appearing in Portfolio

**Symptom:** Spec file exists but doesn't show in dashboard

**Possible Causes:**
1. ❌ Missing YAML frontmatter → Add frontmatter with `---` delimiters
2. ❌ Invalid YAML syntax → Validate with `python -c "import yaml; yaml.safe_load(open('spec.md').read().split('---')[1])"`
3. ❌ Missing required fields → Check `id`, `title`, `status`, `initiative`, `features`
4. ❌ Empty `features:` array → Add at least one feature
5. ❌ File saved outside `specifications/` → Move to correct subdirectory

---

### Issue: Tasks Not Linking to Specification

**Symptom:** Task has `specification:` field but shows as orphan

**Possible Causes:**
1. ❌ Incorrect path → Must be relative to repo root: `specifications/{dir}/{file}.md`
2. ❌ Typo in filename → Check exact spelling and extension
3. ❌ Specification file doesn't exist → Verify file presence
4. ❌ Feature name mismatch → `feature:` must exactly match title in frontmatter

**Debug:**
```bash
# Verify specification file exists
ls -la specifications/llm-dashboard/orphan-task-assignment.md

# Check task YAML
cat work/collaboration/inbox/2026-02-06T1600-task.yaml | grep specification

# Verify path matches
# Task: specification: "specifications/llm-dashboard/orphan-task-assignment.md"
# File: specifications/llm-dashboard/orphan-task-assignment.md
# ✅ Paths match!
```

---

### Issue: Feature Progress Not Calculating

**Symptom:** Features show 0% progress despite completed tasks

**Possible Causes:**
1. ❌ Task `specification:` field missing → Add to task YAML
2. ❌ Feature title mismatch → `feature:` must match frontmatter exactly
3. ❌ Task status not recognized → Must be `done`, `in_progress`, `assigned`, `inbox`
4. ❌ Progress calculator cache stale → Dashboard file watcher will refresh

---

## Related Documentation

- **Directive 034:** Specification-Driven Development (when to create specs)
- **Directive 016:** Acceptance Test-Driven Development (linking specs to tests)
- **Directive 018:** Traceable Decisions (linking specs to ADRs)
- **ADR-037:** Dashboard Initiative Tracking (portfolio view architecture)
- **Template:** `docs/templates/specifications/feature-spec-template.md`
- **README:** `specifications/README.md` (overview and guidance)

---

## Changelog

| Version | Date       | Changes                                      |
|---------|------------|----------------------------------------------|
| 1.0     | 2026-02-06 | Initial directive with frontmatter standards |

---

**End of Directive 035**
