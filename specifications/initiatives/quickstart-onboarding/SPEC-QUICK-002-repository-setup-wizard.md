---
id: SPEC-QUICK-002
title: Repository Setup Wizard
status: draft
version: 1.0.0
author: Analyst Annie
created: 2026-02-10
updated: 2026-02-10
initiative: Quickstart & Onboarding
priority: high
type: functional
tags: [wizard, interactive, onboarding, guided-setup]
---

# SPEC-QUICK-002: Repository Setup Wizard

## Executive Summary

Define an interactive setup wizard that guides users through repository initialization with explanations, previews, and validation. Provides intelligent defaults while allowing customization. Optionally integrates with agent system for assisted setup.

**Goal:** Enable non-expert users to create high-quality repository setups through guided interaction, reducing setup time and errors.

---

## Problem Statement

### Current State

**Challenges with Script-Only Approach:**
- Users don't understand what's being created or why
- No preview of changes before execution
- Limited ability to customize during setup
- No guidance on best practices
- Difficult to recover from mistakes

**User Feedback:**
- "I ran the script but don't know what it did"
- "How do I customize the setup for my needs?"
- "Can I see what will be created before it happens?"
- "What should I put in the vision document?"

### Desired State

**Interactive Wizard Experience:**
- Step-by-step guided flow with explanations
- Preview of what will be created at each step
- Intelligent defaults with customization options
- Inline help and examples
- Validation with clear error messages
- Rollback capability if setup fails
- Integration with getting-started guide agent

**Benefits:**
- Lower learning curve for new users
- Higher quality setups (better vision, glossary)
- Reduced support burden
- Increased confidence during setup
- Optional agent assistance for complex decisions

---

## Requirements

### Functional Requirements

#### FR-1: Welcome and Overview
**Priority:** MUST

The wizard MUST start with welcome screen explaining the process.

**Content:**
- What will be created (directory structure, documents, configs)
- Estimated time (10-15 minutes)
- Prerequisites check (git installed, empty/new repo)
- Option to run automated mode instead
- Option to invoke getting-started guide agent

**Acceptance Criteria:**
- ✅ Clear welcome message displayed
- ✅ Prerequisites validated before proceeding
- ✅ User can exit wizard at any time (Ctrl+C)

---

#### FR-2: Project Information Collection
**Priority:** MUST

The wizard MUST collect key project information.

**Prompts:**
1. **Project Name:**
   - Default: Current directory name
   - Validation: No special characters, 50 char limit
   
2. **Project Type:**
   - Options: Software Development, Documentation, Research, Other
   - Determines template variations
   
3. **Primary Programming Language(s):**
   - Options: Python, JavaScript, Java, Go, TypeScript, Multiple, N/A
   - Used for src/ structure if applicable
   
4. **Team Size:**
   - Options: Solo, Small (2-5), Medium (6-15), Large (16+)
   - Affects collaboration examples created

**Acceptance Criteria:**
- ✅ All prompts have sensible defaults
- ✅ Validation prevents invalid inputs
- ✅ User can navigate back to previous prompts
- ✅ Collected info used to customize setup

---

#### FR-3: Vision Document Creation
**Priority:** MUST

The wizard MUST guide creation of vision document.

**Wizard Steps:**
1. **Explain Importance:**
   - Why vision matters
   - How it guides decisions
   - Link to template

2. **Collect Information:**
   - Problem statement (1-2 sentences)
   - Target users/audience (who is this for?)
   - Key objectives (3-5 bullet points)
   - Success criteria (measurable outcomes)

3. **Preview Generated Document:**
   - Show formatted vision.md
   - Highlight what can be edited later

4. **Confirm or Edit:**
   - Accept as-is
   - Edit inline (basic text editor)
   - Defer to manual editing later

**Optional Enhancement:**
- "Invoke Writer-Editor agent to improve vision?" (if agent system available)

**Acceptance Criteria:**
- ✅ Explanation shown before prompts
- ✅ Prompts have helpful examples
- ✅ Preview shows actual document content
- ✅ User can regenerate with different inputs
- ✅ Vision document created in docs/vision.md

---

#### FR-4: Glossary Setup
**Priority:** MUST

The wizard MUST guide glossary infrastructure setup.

**Wizard Steps:**
1. **Explain Glossary System:**
   - What glossaries are and why they matter
   - Contextive IDE integration benefits
   - Show example glossary entry

2. **Base Glossaries:**
   - Inform: Standard glossaries will be created (doctrine, ddd, organizational, software-design)
   - No user action needed

3. **Project-Specific Glossary:**
   - Prompt: "Do you want to add initial project terms?" (Yes/No)
   - If Yes: Collect 3-10 key domain terms with definitions
   - Provide examples and inline help

4. **Preview Glossary Structure:**
   - Show directory tree
   - Show sample glossary file content

**Optional Enhancement:**
- "Invoke Lexical Larry to analyze README and suggest terms?" (if agent system available)

**Acceptance Criteria:**
- ✅ Base glossaries created automatically
- ✅ Project glossary template created
- ✅ User can optionally add initial terms
- ✅ Contextive config references all glossaries
- ✅ README explains how to add more terms

---

#### FR-5: Directory Structure Configuration
**Priority:** SHOULD

The wizard SHOULD allow customization of directory structure.

**Default Structure:**
- .contextive/, .doctrine-config/, docs/, specifications/, work/
- Optional: src/ (if software project)

**Customization Options:**
- Include src/ directory? (Yes/No - based on project type)
- Additional top-level directories? (tests/, scripts/, tools/, etc.)
- Custom work/ subdirectories?

**Acceptance Criteria:**
- ✅ Default structure sufficient for most users
- ✅ Advanced users can customize
- ✅ Preview shows full directory tree
- ✅ Invalid structures rejected (e.g., conflicting names)

---

#### FR-6: Collaboration Setup
**Priority:** SHOULD

The wizard SHOULD offer to create collaboration examples.

**Options:**
1. **Create Example Tasks:** (Yes/No)
   - Example task YAML files in work/collaboration/examples/
   - Demonstrates multi-agent patterns
   
2. **Create First Initiative:** (Yes/No)
   - Minimal initiative in specifications/initiatives/
   - Shows spec-driven workflow
   
3. **Add README Files:** (Yes/Always/No)
   - README in key directories explaining purpose

**Acceptance Criteria:**
- ✅ User can opt-in to examples
- ✅ Examples reference actual directives
- ✅ README files explain collaboration patterns

---

#### FR-7: Preview and Confirmation
**Priority:** MUST

The wizard MUST show comprehensive preview before execution.

**Preview Content:**
1. **Directory Structure:** Full tree of what will be created
2. **Files List:** All files with sizes
3. **Key Documents:** Snippet of vision.md, config files
4. **Summary:** What was configured, what uses defaults

**Confirmation Options:**
- **Proceed:** Execute initialization
- **Edit:** Go back and modify inputs
- **Export Config:** Save configuration to file for later
- **Cancel:** Exit without changes

**Acceptance Criteria:**
- ✅ Preview shows exactly what will be created
- ✅ User can review before committing
- ✅ Clear confirmation prompt
- ✅ Cancellation at preview is safe (no changes)

---

#### FR-8: Execution with Progress
**Priority:** MUST

The wizard MUST show progress during execution.

**Progress Indicators:**
- Step-by-step messages: "Creating directory structure..."
- Progress bar or percentage (if determinable)
- Success/failure indication per step
- Elapsed time

**Error Handling:**
- Clear error messages if step fails
- Option to continue or rollback
- Log file created with detailed error info

**Acceptance Criteria:**
- ✅ User sees what's happening in real-time
- ✅ Progress is accurate (not fake loading)
- ✅ Errors provide actionable guidance
- ✅ Execution completes in <30 seconds

---

#### FR-9: Post-Setup Summary and Next Steps
**Priority:** MUST

The wizard MUST provide summary and guidance after completion.

**Summary Content:**
1. **What Was Created:**
   - Directory count
   - File count
   - Key documents list

2. **Validation Results:**
   - ✅ All checks passed
   - ⚠️ Optional items skipped
   - ❌ Issues found (if any)

3. **Next Steps:**
   - Review docs/vision.md
   - Add project-specific glossary terms
   - Create first specification
   - Run getting-started guide agent
   - Link to documentation

4. **Quick Commands:**
   - How to run dashboard
   - How to validate setup
   - How to invoke agents

**Acceptance Criteria:**
- ✅ Summary is comprehensive but concise
- ✅ Next steps are actionable
- ✅ Links to relevant documentation
- ✅ Success message is encouraging

---

### Non-Functional Requirements

#### NFR-1: Usability
- Wizard completes in <15 minutes (typical user)
- Clear, jargon-free language in prompts
- Inline help available for complex concepts
- Can pause and resume (save state to file)

#### NFR-2: Accessibility
- Works in terminal (no GUI required)
- Color coding with fallback for no-color terminals
- Keyboard navigation only (no mouse needed)
- Screen reader compatible prompts

#### NFR-3: Performance
- Instant response to user input (<100ms)
- Preview generation <1 second
- Execution completes <30 seconds
- No external network calls during execution

#### NFR-4: Reliability
- Idempotent (running twice is safe)
- Atomic operations (rollback on failure)
- State saved if process interrupted
- Comprehensive error messages

---

## Implementation Design

### Technology Choices

#### Option 1: Bash Script with Dialog/Whiptail
**Pros:**
- Native to Unix systems
- No dependencies
- Fast execution
- Simple maintenance

**Cons:**
- Limited UI capabilities
- Windows compatibility issues
- Hard to test automatically

---

#### Option 2: Python with Rich/Textual
**Pros:**
- Rich UI capabilities (colors, progress bars, tables)
- Cross-platform (Windows, macOS, Linux)
- Easy to test
- Can integrate with agent system

**Cons:**
- Requires Python runtime
- Slightly larger codebase

**Recommendation:** Python with Rich library (better UX, testability, extensibility)

---

### Script Structure (Python + Rich)

```python
#!/usr/bin/env python3
"""
setup-wizard.py - Interactive Repository Setup Wizard
"""

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.tree import Tree
import yaml
import os

console = Console()

def main():
    # 1. Welcome and prerequisites
    show_welcome()
    check_prerequisites()
    
    # 2. Collect project information
    project_info = collect_project_info()
    
    # 3. Guide vision document creation
    vision = create_vision_document(project_info)
    
    # 4. Setup glossary infrastructure
    glossary_config = setup_glossaries(project_info)
    
    # 5. Configure directory structure
    structure = configure_directories(project_info)
    
    # 6. Optional collaboration setup
    collab = setup_collaboration()
    
    # 7. Preview everything
    if not preview_and_confirm(project_info, vision, glossary_config, structure):
        console.print("[yellow]Setup cancelled.[/yellow]")
        return
    
    # 8. Execute with progress
    execute_setup(project_info, vision, glossary_config, structure, collab)
    
    # 9. Show summary and next steps
    show_summary()

if __name__ == "__main__":
    main()
```

---

### Agent Integration Points

#### Getting-Started Guide Agent

**Invocation:** Optional at welcome screen or post-setup

**Capabilities:**
- Explain setup wizard process
- Answer questions about framework
- Guide through complex decisions
- Suggest best practices

**Integration:**
```python
if agent_system_available():
    if Confirm.ask("Would you like agent assistance during setup?"):
        agent = invoke_agent("getting-started-guide")
        agent.explain_wizard()
```

---

#### Writer-Editor Agent

**Invocation:** Optional during vision document creation

**Capabilities:**
- Improve vision document clarity
- Suggest better phrasing
- Ensure completeness
- Check for jargon

**Integration:**
```python
if Confirm.ask("Invoke Writer-Editor to improve vision?"):
    improved_vision = invoke_agent("writer-editor", vision_draft)
    console.print(diff(vision_draft, improved_vision))
    if Confirm.ask("Accept improvements?"):
        vision = improved_vision
```

---

#### Lexical Larry

**Invocation:** Optional during glossary setup

**Capabilities:**
- Analyze README or docs for domain terms
- Suggest glossary entries
- Validate term definitions
- Check for term conflicts

**Integration:**
```python
if Confirm.ask("Analyze existing docs for glossary terms?"):
    suggested_terms = invoke_agent("lexical-larry", docs_path)
    console.print_table(suggested_terms)
    selected = multi_select(suggested_terms)
    glossary.add_terms(selected)
```

---

## User Experience Flow

### Wizard Session Example

```
┌──────────────────────────────────────────────────┐
│ 🚀 SDD Agentic Framework Setup Wizard           │
│                                                   │
│ This wizard will help you initialize a          │
│ framework-ready repository with:                 │
│   ✓ Directory structure                         │
│   ✓ Vision document                             │
│   ✓ Glossary infrastructure                     │
│   ✓ Collaboration examples                      │
│                                                   │
│ Estimated time: 10-15 minutes                    │
└──────────────────────────────────────────────────┘

Checking prerequisites...
✓ Git installed (version 2.43.0)
✓ Directory is empty
✓ Python 3.11+ available

Ready to proceed!

═══════════════════════════════════════════════════

Step 1/7: Project Information

Project name [my-repository]: awesome-project
Project type (software/docs/research/other) [software]: 
Primary language (python/javascript/java/go/multiple/none) [python]: 
Team size (solo/small/medium/large) [small]: 

═══════════════════════════════════════════════════

Step 2/7: Vision Document

A vision document guides all project decisions. It should answer:
• What problem does this solve?
• Who is it for?
• What does success look like?

Let's create yours...

Problem statement (1-2 sentences): 
> Internal developer tools lack consistency. We need a 
> unified CLI framework to standardize our tooling.

Target users (who is this for?):
> Engineering teams building internal CLIs

Key objectives (comma-separated):
> Consistency, Ease of use, Extensibility

Success criteria:
> 5+ teams adopt framework within 6 months

Preview:

┌─ docs/vision.md ─────────────────────────────────┐
│ # Vision: awesome-project                        │
│                                                   │
│ ## Problem                                       │
│ Internal developer tools lack consistency...     │
│                                                   │
│ ## Target Users                                  │
│ Engineering teams building internal CLIs         │
│ ...                                              │
└──────────────────────────────────────────────────┘

Accept this vision? (yes/edit/regenerate) [yes]: 

═══════════════════════════════════════════════════

Step 3/7: Glossary Setup

Glossaries help maintain consistent terminology.

Standard glossaries will be created:
  • doctrine.yml (framework concepts)
  • ddd.yml (domain-driven design)
  • organizational.yml (team patterns)
  • software-design.yml (architecture)

Add project-specific terms now? [y/n]: y

Term 1: CLI Framework
Definition: Command-line interface abstraction layer

Term 2: Tool
Definition: Individual command-line utility built on the framework

Add more terms? [y/n]: n

═══════════════════════════════════════════════════

Step 4/7: Directory Structure

Creating framework directories:
  .contextive/contexts/
  .doctrine-config/
  docs/architecture/adrs/
  specifications/initiatives/
  work/collaboration/
  src/

Include additional directories? (tests,scripts,tools) [tests,scripts]: 

═══════════════════════════════════════════════════

Step 5/7: Collaboration Setup

Create example collaboration workflows? [y/n]: y
  ✓ Multi-agent task example
  ✓ Specification-driven workflow
  ✓ Review and iteration pattern

═══════════════════════════════════════════════════

Step 6/7: Preview

Here's what will be created:

Directory Structure:
awesome-project/
├── .contextive/
│   └── contexts/ (5 files)
├── .doctrine-config/
│   └── config.yaml
├── docs/
│   ├── vision.md
│   └── architecture/adrs/
├── specifications/initiatives/
├── work/
│   ├── collaboration/
│   │   ├── assigned/
│   │   ├── pending/
│   │   └── examples/ (3 files)
│   ├── planning/
│   └── reports/
├── src/
├── tests/
└── scripts/

Total: 12 directories, 11 files, ~45 KB

Key Files:
  • docs/vision.md (632 bytes)
  • .contextive/contexts/project.yml (2 terms)
  • .doctrine-config/config.yaml (sensible defaults)

Proceed with setup? (yes/edit/export/cancel) [yes]: 

═══════════════════════════════════════════════════

Step 7/7: Executing Setup

Creating directories... ████████████████████ 100%
Generating documents... ████████████████████ 100%
Setting up glossaries... ████████████████████ 100%
Creating examples... ████████████████████ 100%
Validating setup... ████████████████████ 100%

✓ Setup complete! (8.3 seconds)

═══════════════════════════════════════════════════

🎉 Success!

Your repository is now initialized with:
  ✓ 12 directories created
  ✓ 11 files generated
  ✓ Vision document: docs/vision.md
  ✓ 5 glossaries configured
  ✓ 3 collaboration examples
  
Validation: All checks passed ✓

Next Steps:
  1. Review and refine docs/vision.md
  2. Add more project-specific glossary terms
  3. Create your first specification
  4. Run: ./scripts/getting-started-guide.sh
  
Quick Commands:
  • Validate setup: ./scripts/validate-setup.sh
  • Start dashboard: npm run dashboard
  • Invoke Bootstrap Bill: @bill setup-ci-cd
  
Documentation: See docs/README.md

Happy building! 🚀
```

---

## Testing Strategy

### Unit Tests

**Component Testing:**
- ✅ Each wizard step in isolation
- ✅ Input validation logic
- ✅ Preview generation
- ✅ Configuration file generation
- ✅ Error handling per step

**Location:** `tests/unit/test_setup_wizard.py`

---

### Integration Tests

**End-to-End Flows:**
- ✅ Complete wizard run (automated inputs)
- ✅ User cancels at various points
- ✅ Invalid inputs rejected gracefully
- ✅ Preview matches actual execution
- ✅ Agent integration (if available)

**Location:** `tests/integration/test_wizard_flow.py`

---

### Usability Testing

**Manual Testing:**
- ✅ First-time user can complete wizard without help
- ✅ Error messages are clear and actionable
- ✅ Preview is accurate and helpful
- ✅ Completion time <15 minutes
- ✅ User satisfaction survey >80%

---

## Dependencies

**Upstream (Required):**
- ✅ SPEC-QUICK-001: Repository Initialization Sequence (provides core logic)
- ✅ Python 3.11+ runtime
- ✅ Rich library for terminal UI
- ✅ Doctrine templates available

**Optional (Enhanced Experience):**
- Agent system for getting-started guide
- Writer-Editor agent for vision improvement
- Lexical Larry for glossary suggestions

**Downstream (Enables):**
- Getting-started guide agent implementation
- Dashboard integration (setup tracking)
- Documentation improvements

---

## Success Criteria

**Wizard is successful when:**
- ✅ 80% completion rate (users don't abandon mid-wizard)
- ✅ 90% of completed setups validate successfully
- ✅ Average completion time <15 minutes
- ✅ User satisfaction >80% ("easy to use")
- ✅ <5% of users request support after wizard
- ✅ Vision documents are non-trivial (not just defaults)

---

## Future Enhancements

### Phase 2 (Post-Launch):
1. **Web UI Version:**
   - Browser-based wizard
   - Richer previews with syntax highlighting
   - Save and resume across sessions

2. **Template Marketplace:**
   - Pre-configured templates for common project types
   - Community-contributed templates
   - One-click template selection

3. **AI-Powered Suggestions:**
   - LLM analyzes project type and suggests configurations
   - Auto-generates vision from brief description
   - Predicts useful glossary terms

4. **Team Collaboration:**
   - Multi-user setup (async collection of inputs)
   - Approval workflow for vision/glossary
   - Export/import configurations across teams

---

## Related Documentation

**Specifications:**
- SPEC-QUICK-001: Repository Initialization Sequence (core logic)

**Directives:**
- Directive 038: Ensure Conceptual Alignment (glossary prompts)
- Directive 037: Context-Aware Design (explains bounded contexts)

**Agent Profiles:**
- Getting-Started Guide Agent (assistance)
- Bootstrap Bill (execution)
- Writer-Editor (vision improvement)
- Lexical Larry (glossary suggestions)

**Templates:**
- `doctrine/templates/architecture/design_vision.md`
- `doctrine/templates/documentation/`

---

## Version History

- **1.0.0** (2026-02-10): Initial specification created by Analyst Annie

---

**Specification Status:** ✅ Ready for Review
**Next Steps:**
1. Review by Architect Alphonso
2. UX review by Manager Mike
3. Implementation planning by Planning Petra
4. Development by Bootstrap Bill + Python Pedro
