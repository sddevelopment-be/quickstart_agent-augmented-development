# Doctrine Framework: Extension Surfaces

_Version: 1.0.0_  
_Last Updated: 2026-02-13_  
_Agent: Bootstrap Bill_  
_Purpose: Extension points and integration interfaces for the doctrine framework_

---

## Overview

This document describes **how to extend, customize, and integrate** the Doctrine Framework into your own repositories and workflows. It catalogs the **extension points, integration interfaces, and customization patterns** that enable safe, maintainable adaptations without breaking core governance.

### Key Principles

1. **Additive, Not Overriding** - Local extensions augment doctrine, never replace core guidelines
2. **Clear Precedence** - Framework guidelines > Local extensions > User requests
3. **Backward Compatible** - Extensions don't break existing agents or workflows
4. **Portable** - Customizations remain portable when updating doctrine via git subtree

---

## Table of Contents

1. [Extension Points](#extension-points)
2. [Customization Patterns](#customization-patterns)
3. [Integration Surfaces](#integration-surfaces)
4. [Artifact Formats](#artifact-formats)
5. [Validation Interfaces](#validation-interfaces)
6. [Distribution Methods](#distribution-methods)
7. [Tool Integration](#tool-integration)

---

## Extension Points

### 1. Local Guidelines Extension

**Location:** `.doctrine-config/specific_guidelines.md`

**Purpose:** Add repository-specific constraints and conventions without overriding core principles

**Structure:**

```markdown
# Project-Specific Guidelines

_Version: 1.0.0_  
_Repository: your-repo-name_  
_Last Updated: YYYY-MM-DD_

## Repository-Specific Constraints

### Code Style
- Python: Black formatting, 100-character line limit
- TypeScript: Prettier, semicolons required

### Naming Conventions
- Classes: PascalCase
- Functions: snake_case
- Constants: SCREAMING_SNAKE_CASE

### Commit Messages
- Format: `<type>(<scope>): <description>`
- Types: feat, fix, docs, style, refactor, test, chore

## Project-Specific Conventions

### File Organization
- Tests mirror src/ structure
- Integration tests in tests/integration/
- Fixtures in fixtures/<category>/

### Documentation
- All public APIs require docstrings
- Complex algorithms require inline comments
- ADRs required for architectural decisions >1 week effort
```

**Constraints:**
- ❌ **Cannot override** `doctrine/guidelines/general_guidelines.md`
- ❌ **Cannot override** `doctrine/guidelines/operational_guidelines.md`
- ✅ **Can extend** with repository-specific rules
- ✅ **Can reference** doctrine directives and tactics

**Load Order:**
1. `doctrine/guidelines/general_guidelines.md` (HIGHEST)
2. `doctrine/guidelines/operational_guidelines.md` (HIGH)
3. `.doctrine-config/specific_guidelines.md` (MEDIUM)
4. User requests (LOWEST)

### 2. Custom Agent Profiles

**Location:** `.doctrine-config/agents/`

**Purpose:** Create repository-specific agents or customize existing profiles

**Pattern:**

```bash
# Copy existing agent
cp doctrine/agents/architect.agent.md .doctrine-config/agents/

# Customize for your domain
vi .doctrine-config/agents/architect.agent.md

# Agents load local profile if exists, otherwise use doctrine default
```

**Customization Example:**

```markdown
# Agent Profile: Domain Architect

## 1. Context Sources (Extended)
- Global Principles: doctrine/guidelines/
- Directives: doctrine/directives/ (007, 014, 018, 020, 036)
- Local Guidelines: .doctrine-config/specific_guidelines.md
- **Domain Models:** .doctrine-config/approaches/domain-driven-design.md

## 3. Specialization (Domain-Specific)
- **Primary focus:** Microservices architecture, event-driven systems
- **Secondary awareness:** Kubernetes, distributed tracing
- **Avoid:** Frontend implementation, database schema design (delegate to backend-dev)
- **Success means:** Clear service boundaries, documented event contracts, ADRs for integration decisions

## 6. Initialization Declaration
✅ SDD Agent "Domain Architect" initialized.
**Context layers:** Operational ✓, Strategic ✓, Command ✓, Bootstrap ✓, AGENTS ✓, Domain ✓.
**Purpose acknowledged:** Design microservices architecture with event-driven patterns.
```

**Naming Convention:**
- Use descriptive names reflecting specialization
- Avoid conflicts with doctrine agent names
- Follow `kebab-case-name.agent.md` pattern

### 3. Custom Directives

**Location:** `.doctrine-config/directives/`

**Purpose:** Add organization-specific instructions without modifying doctrine

**Numbering Scheme:**
- **001-099:** Reserved for doctrine framework
- **100-199:** Available for local directives
- **200-299:** Available for organization-wide directives
- **300+:** Available for experimental directives

**Example: Local Directive 100**

```markdown
# Directive 100: Security Scanning Protocol

**Version:** 1.0.0  
**Applicability:** All code changes  
**Precedence:** High (after Directive 036 Boy Scout Rule)

## Purpose

Enforce security scanning before committing code changes.

## Instructions

### Pre-Commit Security Checks

1. **Static Analysis:**
   ```bash
   bandit -r src/ -ll  # Python security issues
   safety check         # Vulnerable dependencies
   ```

2. **Secret Detection:**
   ```bash
   trufflehog --regex --entropy=False src/
   ```

3. **License Compliance:**
   ```bash
   pip-licenses --format=markdown --with-urls
   ```

### Failure Handling

If any check fails:
1. Fix issues immediately
2. Document any false positives
3. Re-run checks
4. Do not commit until all pass

## Related Tactics

- `input-validation-checklist.tactic.md` (doctrine)
- `code-review-checklist.tactic.md` (doctrine)

## Invoked By

- Pre-commit hook (automated)
- Directive 036 (Boy Scout Rule) - explicit security check
```

**Load Pattern:**

```markdown
/require-directive 100  # Security Scanning Protocol
```

### 4. Custom Tactics

**Location:** `.doctrine-config/tactics/`

**Purpose:** Add domain-specific or organization-specific procedures

**Example: Organization Tactic**

```markdown
# Tactic: GDPR Compliance Checklist

**Version:** 1.0.0  
**Category:** Compliance  
**Invoked By:** Directive 100 (Security Scanning), custom-directive-101 (Privacy Review)

## Preconditions

- Feature involves personal data (PII)
- Feature deployed in EU or serves EU users
- Feature modifies data storage or processing

## Exclusions

- Features with no PII
- Internal tools not accessible to end-users
- Anonymous analytics only

## Procedure

### Step 1: Identify Personal Data

- [ ] List all PII fields (name, email, IP address, etc.)
- [ ] Document data sources (user input, logs, third-party APIs)
- [ ] Classify sensitivity (low, medium, high)

### Step 2: Assess Legal Basis

- [ ] Identify lawful basis (consent, contract, legitimate interest)
- [ ] Document purpose limitation
- [ ] Define data retention period

### Step 3: Implement Technical Controls

- [ ] Encryption at rest (AES-256)
- [ ] Encryption in transit (TLS 1.3)
- [ ] Access controls (RBAC, audit logging)
- [ ] Data anonymization/pseudonymization where possible

### Step 4: User Rights Implementation

- [ ] Right to access (export data)
- [ ] Right to rectification (update data)
- [ ] Right to erasure ("delete my account")
- [ ] Right to data portability (download in standard format)

### Step 5: Documentation

- [ ] Update privacy policy
- [ ] Document data processing activities (ROPA)
- [ ] Create data flow diagram
- [ ] Record consent mechanisms

## Success Criteria

- All checklist items completed
- Legal review approved
- Technical implementation validated
- Documentation updated

## Failure Modes

- **Missing PII identification:** Conduct data audit with DPO
- **Insufficient technical controls:** Escalate to security team
- **Unclear legal basis:** Consult legal counsel before proceeding
```

**Naming Convention:**
- Descriptive names reflecting domain/organization
- Follow `kebab-case-title.tactic.md` pattern
- Prefix with category (e.g., `GDPR-`, `SOC2-`, `HIPAA-`)

### 5. Custom Approaches

**Location:** `.doctrine-config/approaches/`

**Purpose:** Add mental models and philosophies specific to your domain

**Example:**

```markdown
# Approach: Domain-Driven Design

**Version:** 1.0.0  
**Context:** Microservices architecture  
**Related Directives:** 018 (Traceable Decisions)

## Core Concepts

### Bounded Contexts

A bounded context is a semantic contextual boundary within which a particular model is defined and applicable.

**Principles:**
- Each service owns its domain model
- Explicit context mapping between services
- Shared kernel for common concepts only

### Ubiquitous Language

**Definition:** A common language shared by domain experts and developers, used in code, documentation, and conversations.

**Practice:**
- Class names match business terminology
- Method names reflect business operations
- Tests describe business scenarios (Given/When/Then)

### Aggregates

**Definition:** A cluster of domain objects treated as a single unit for data consistency.

**Rules:**
- One aggregate root per aggregate
- Transactions don't span aggregates
- References between aggregates use IDs, not objects

## Application to This Repository

- Use DDD for microservices (backend-dev, architect agents)
- Document bounded contexts in ADRs (Directive 018)
- Model aggregates in `src/domain/models/`
- Tests use ubiquitous language (Directive 016 ATDD)

## Related Tactics

- `ATDD_critical-user-path.tactic.md` - Use business scenarios
- `premortem-risk-identification.tactic.md` - Identify aggregate boundaries

## Related Directives

- 018 (Traceable Decisions) - Document bounded context decisions
- 034 (Specification-Driven Development) - Capture ubiquitous language
```

---

## Customization Patterns

### Pattern 1: Extend Existing Agent

**Scenario:** Architect agent needs domain-specific knowledge

**Steps:**

1. Copy agent profile:
   ```bash
   cp doctrine/agents/architect.agent.md .doctrine-config/agents/
   ```

2. Add local approaches:
   ```markdown
   ## 1. Context Sources (Extended)
   - **Domain Models:** .doctrine-config/approaches/domain-driven-design.md
   ```

3. Add local directives:
   ```markdown
   ## 3. Specialization
   - **Primary focus:** Domain modeling, bounded contexts, event-driven architecture
   - **Required directives:** 007, 014, 018, 100 (Security Scanning)
   ```

4. Preserve collaboration contract:
   ```markdown
   ## 4. Collaboration Contract
   - Never override General or Operational guidelines ← Keep this
   - Stay within defined specialization ← Keep this
   - Ask clarifying questions when uncertainty >30% ← Keep this
   ```

### Pattern 2: Add Organization Directive

**Scenario:** Organization requires SOC2 compliance checks

**Steps:**

1. Create directive:
   ```bash
   mkdir -p .doctrine-config/directives
   vi .doctrine-config/directives/101_soc2_compliance.md
   ```

2. Define applicability:
   ```markdown
   **Applicability:** All production code changes  
   **Invoked By:** Pre-merge CI/CD pipeline
   ```

3. Invoke custom tactic:
   ```markdown
   ## Procedure
   
   At step 3 of code review:
   - Invoke: `.doctrine-config/tactics/SOC2-access-control-review.tactic.md`
   ```

4. Update agent profiles:
   ```markdown
   # In .doctrine-config/agents/backend-dev.agent.md
   
   ## 3. Specialization
   - **Required directives:** 007, 014, 017, 101 (SOC2 Compliance)
   ```

### Pattern 3: Add Domain-Specific Tactic

**Scenario:** Team needs ML model validation checklist

**Steps:**

1. Create tactic:
   ```bash
   mkdir -p .doctrine-config/tactics
   vi .doctrine-config/tactics/ML-model-validation.tactic.md
   ```

2. Follow tactic template:
   ```markdown
   # Tactic: ML Model Validation
   
   ## Preconditions
   - Model trained on representative data
   - Training/validation/test split completed
   
   ## Procedure
   ### Step 1: Data Quality
   - [ ] Check for data leakage
   - [ ] Verify class balance
   
   ### Step 2: Model Metrics
   - [ ] Accuracy > 90%
   - [ ] Precision/Recall balanced
   
   ### Step 3: Bias Analysis
   - [ ] Test for demographic parity
   - [ ] Check for proxy discrimination
   ```

3. Invoke from directive:
   ```markdown
   # In .doctrine-config/directives/102_ml_deployment.md
   
   At deployment stage:
   - Invoke: `.doctrine-config/tactics/ML-model-validation.tactic.md`
   ```

---

## Integration Surfaces

### Domain Model API

**Location:** `src/domain/` (if using ADR-045 implementation)

**Purpose:** Programmatic access to doctrine artifacts

**Python Interface:**

```python
from src.domain.parsers import AgentParser, DirectiveParser, TacticParser
from src.domain.validators import AgentValidator, DirectiveValidator

# Parse agent profile
parser = AgentParser(doctrine_root="doctrine/")
agent = parser.parse_file("doctrine/agents/architect.agent.md")

print(agent.name)           # "Architect"
print(agent.specialization) # "Architecture design and documentation"
print(agent.directives)     # ["007", "014", "018"]

# Parse directive
parser = DirectiveParser(doctrine_root="doctrine/")
directive = parser.parse_file("doctrine/directives/014_worklog_creation.md")

print(directive.code)       # "014"
print(directive.title)      # "Work Log Creation"
print(directive.related_tactics) # ["stopping-conditions"]

# Validate agent cross-references
validator = AgentValidator(doctrine_root="doctrine/")
errors = validator.validate_agent("architect")

if errors:
    for error in errors:
        print(f"Error: {error.message} at {error.location}")
```

**Extension:**

```python
# Add custom parsers for local extensions
from src.domain.parsers import DirectiveParser

class LocalDirectiveParser(DirectiveParser):
    def __init__(self):
        super().__init__(doctrine_root="doctrine/", local_root=".doctrine-config/")
    
    def parse_all_directives(self):
        """Parse both doctrine and local directives."""
        doctrine_directives = self.parse_directory("doctrine/directives/")
        local_directives = self.parse_directory(".doctrine-config/directives/")
        return doctrine_directives + local_directives
```

### Task Orchestration API

**Location:** `work/scripts/agent_base.py`

**Purpose:** Integrate doctrine-aware agents into orchestration

**Python Interface:**

```python
from work.scripts.agent_base import AgentBase
import yaml

class DoctrineAwareAgent(AgentBase):
    def __init__(self):
        super().__init__()
        self.load_doctrine()
    
    def load_doctrine(self):
        """Load doctrine context from agent profile."""
        profile_path = f"doctrine/agents/{self.get_agent_name()}.agent.md"
        # Parse profile to extract required directives
        # Load directives from doctrine/directives/
        # Load tactics from doctrine/tactics/
        pass
    
    def get_agent_name(self) -> str:
        return "doctrine-aware-agent"
    
    def process_task(self, task_file: str) -> bool:
        with open(task_file, 'r') as f:
            task = yaml.safe_load(f)
        
        # 1. Validate task against doctrine
        self.validate_task_context(task)
        
        # 2. Load required directives for task
        self.load_required_directives(task)
        
        # 3. Execute work following doctrine
        result = self.execute_with_doctrine(task)
        
        # 4. Create work log (Directive 014)
        self.create_work_log(task, result)
        
        return result
```

### Export API

**Location:** `tools/exporters/`

**Purpose:** Export doctrine artifacts to different formats

**Copilot Format:**

```python
# tools/exporters/copilot/export_to_copilot.py

def export_agent_to_copilot(agent_path: str) -> dict:
    """
    Export agent profile to GitHub Copilot format.
    
    Args:
        agent_path: Path to agent markdown file
        
    Returns:
        dict: Copilot skill JSON
    """
    parser = AgentParser()
    agent = parser.parse_file(agent_path)
    
    return {
        "name": agent.name,
        "description": agent.specialization,
        "instructions": [
            {
                "type": "directive",
                "code": directive,
                "path": f"doctrine/directives/{directive}_*.md"
            }
            for directive in agent.directives
        ],
        "context_files": [
            "doctrine/guidelines/general_guidelines.md",
            "doctrine/guidelines/operational_guidelines.md",
            agent_path
        ]
    }
```

**Claude Format:**

```python
# tools/exporters/claude/export_to_claude.py

def export_agent_to_claude(agent_path: str) -> dict:
    """
    Export agent profile to Claude Desktop custom skill format.
    
    Args:
        agent_path: Path to agent markdown file
        
    Returns:
        dict: Claude skill JSON
    """
    parser = AgentParser()
    agent = parser.parse_file(agent_path)
    
    return {
        "name": agent.name,
        "description": agent.specialization,
        "system_prompt": build_system_prompt(agent),
        "context": {
            "guidelines": [
                "doctrine/guidelines/general_guidelines.md",
                "doctrine/guidelines/operational_guidelines.md"
            ],
            "directives": [
                f"doctrine/directives/{d}_*.md" for d in agent.directives
            ],
            "profile": agent_path
        }
    }
```

**OpenCode Format:**

```python
# tools/exporters/opencode/export_to_opencode.py

def export_to_opencode(doctrine_root: str = "doctrine/") -> dict:
    """
    Export entire doctrine to OpenCode format.
    
    Args:
        doctrine_root: Path to doctrine directory
        
    Returns:
        dict: OpenCode configuration JSON
    """
    return {
        "version": "1.0.0",
        "agents": [
            export_agent(agent_path)
            for agent_path in glob.glob(f"{doctrine_root}/agents/*.agent.md")
        ],
        "directives": [
            export_directive(directive_path)
            for directive_path in glob.glob(f"{doctrine_root}/directives/*.md")
        ],
        "tactics": [
            export_tactic(tactic_path)
            for tactic_path in glob.glob(f"{doctrine_root}/tactics/*.tactic.md")
        ]
    }
```

---

## Artifact Formats

### Agent Profile Format

**File Extension:** `.agent.md`

**Required Sections:**

```markdown
# Agent Profile: <Agent Name>

## 1. Context Sources
- List of doctrine layers and directives

## 2. Purpose
- Single-sentence purpose statement

## 3. Specialization
- Primary focus
- Secondary awareness
- Avoid list
- Success criteria

## 4. Collaboration Contract
- Guidelines (never override)
- Specialization boundaries
- Collaboration rules

## 5. Mode Defaults
- /analysis-mode, /creative-mode, /meta-mode

## 6. Initialization Declaration
- ✅ Readiness announcement template
```

**Frontmatter (Optional):**

```yaml
---
agent: "agent-name"
version: "1.0.0"
specialization: "One-line description"
required_directives: ["007", "014", "018"]
related_agents: ["architect", "backend-dev"]
---
```

### Directive Format

**File Extension:** `.md`

**Naming:** `NNN_kebab-case-title.md`

**Required Sections:**

```markdown
# Directive NNN: Title

**Version:** X.Y.Z  
**Applicability:** Context where directive applies  
**Precedence:** High | Medium | Low

## Purpose

What problem this directive solves.

## Instructions

Step-by-step what agents must do.

## Related Tactics

- `tactic-name.tactic.md` - When to invoke

## Related Directives

- NNN: Related directive
```

### Tactic Format

**File Extension:** `.tactic.md`

**Naming:** `kebab-case-title.tactic.md`

**Required Sections:**

```markdown
# Tactic: Title

**Version:** X.Y.Z  
**Category:** Category name  
**Invoked By:** Directive NNN

## Preconditions

- Condition 1
- Condition 2

## Exclusions

- When NOT to use this tactic

## Procedure

### Step 1: Title
- [ ] Checklist item 1
- [ ] Checklist item 2

### Step 2: Title
- [ ] Checklist item 1

## Success Criteria

- Measurable outcome 1
- Measurable outcome 2

## Failure Modes

- **Failure scenario:** Recovery action
```

---

## Validation Interfaces

### Schema Validation

**JSON Schemas:** `src/framework/schemas/`

**Agent Profile Schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["name", "specialization", "directives"],
  "properties": {
    "name": {"type": "string"},
    "specialization": {"type": "string"},
    "directives": {
      "type": "array",
      "items": {"type": "string", "pattern": "^[0-9]{3}$"}
    },
    "modes": {
      "type": "array",
      "items": {"enum": ["analysis", "creative", "meta"]}
    }
  }
}
```

**Directive Schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["code", "title", "version", "applicability"],
  "properties": {
    "code": {"type": "string", "pattern": "^[0-9]{3}$"},
    "title": {"type": "string"},
    "version": {"type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"},
    "applicability": {"type": "string"},
    "related_tactics": {
      "type": "array",
      "items": {"type": "string"}
    }
  }
}
```

### Cross-Reference Validation

**Python Validators:** `src/domain/validators/`

**Agent Validator:**

```python
from src.domain.validators import AgentValidator

validator = AgentValidator(
    doctrine_root="doctrine/",
    local_root=".doctrine-config/"  # Optional
)

errors = validator.validate_all_agents()

# Returns list of validation errors:
# - Missing directives
# - Circular references
# - Invalid directive codes
# - Broken tactic links
```

**Directive Validator:**

```python
from src.domain.validators import DirectiveValidator

validator = DirectiveValidator(
    doctrine_root="doctrine/",
    local_root=".doctrine-config/"
)

errors = validator.validate_all_directives()

# Returns list of validation errors:
# - Missing related tactics
# - Circular directive dependencies
# - Invalid tactic references
```

---

## Distribution Methods

### Git Subtree

**Add Doctrine:**

```bash
git subtree add --prefix=doctrine \
  https://github.com/sddevelopment-be/quickstart_agent-augmented-development.git \
  main --squash
```

**Update Doctrine:**

```bash
git subtree pull --prefix=doctrine \
  https://github.com/sddevelopment-be/quickstart_agent-augmented-development.git \
  main --squash
```

**Contribute Back:**

```bash
git subtree push --prefix=doctrine \
  https://github.com/sddevelopment-be/quickstart_agent-augmented-development.git \
  feature-branch
```

### Git Submodule (Alternative)

**Add Doctrine:**

```bash
git submodule add \
  https://github.com/sddevelopment-be/quickstart_agent-augmented-development.git \
  doctrine
```

**Update Doctrine:**

```bash
cd doctrine
git pull origin main
cd ..
git add doctrine
git commit -m "chore: update doctrine to latest"
```

### Package Distribution (Future)

**Python Package (Planned):**

```bash
pip install sdd-doctrine
```

**NPM Package (Planned):**

```bash
npm install @sdd/doctrine
```

---

## Tool Integration

### GitHub Copilot

**Export:**

```bash
python tools/exporters/copilot/export_to_copilot.py
```

**Result:** `.github/copilot/agents/<agent-name>.json`

**Usage in Copilot:**

```markdown
@agent-name please design the API for user management
```

### Claude Desktop

**Export:**

```bash
python tools/exporters/claude/export_to_claude.py
```

**Result:** `.claude/agents/<agent-name>.json`

**Usage in Claude:**

```markdown
Use the architect skill to design the API
```

### VSCode Extension (Planned)

**Features:**
- Doctrine explorer (tree view of agents/directives/tactics)
- Directive quick-load (auto-complete for `/require-directive`)
- Agent initialization wizard
- Task YAML templates
- Work log templates

### JetBrains Plugin (Planned)

**Features:**
- Doctrine navigator panel
- Live directive validation
- Agent profile editor
- Tactic execution guides

---

## Summary

### Extension Checklist

- ✅ Create `.doctrine-config/` directory
- ✅ Add `specific_guidelines.md` for repository constraints
- ✅ Copy and customize agent profiles if needed
- ✅ Create custom directives (100+ numbering)
- ✅ Create custom tactics for domain procedures
- ✅ Add custom approaches for mental models
- ✅ Validate with domain model API
- ✅ Export to tool formats (Copilot, Claude, OpenCode)

### Do's and Don'ts

**Do:**
- ✅ Extend with local customizations
- ✅ Add domain-specific directives/tactics
- ✅ Customize agent specializations
- ✅ Use numbering ranges for locals (100+)
- ✅ Follow tactic/directive templates
- ✅ Validate cross-references

**Don't:**
- ❌ Override `general_guidelines.md`
- ❌ Override `operational_guidelines.md`
- ❌ Modify doctrine files directly (use `.doctrine-config/`)
- ❌ Use directive codes 001-099 for locals
- ❌ Break precedence hierarchy
- ❌ Ignore validation errors

---

## Related Artifacts

- **[REPO_MAP.md](REPO_MAP.md)** - Doctrine framework structure
- **[DOCTRINE_STACK.md](DOCTRINE_STACK.md)** - Five-layer governance model
- **[tactics/README.md](tactics/README.md)** - Tactics catalog
- **[../SURFACES.md](../SURFACES.md)** - Parent repository surfaces
- **[../VISION.md](../VISION.md)** - Framework vision and philosophy

---

_Generated by Bootstrap Bill_  
_For extension questions: Submit issue to upstream repository_  
_For local customizations: Use `.doctrine-config/` directory_  
_Last Updated: 2026-02-13_
