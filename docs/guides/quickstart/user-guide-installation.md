# Framework Installation Guide

**Step-by-step guide for first-time framework installation**

This guide walks you through installing the Quickstart Agent-Augmented Development Framework for the first time. If you're upgrading an existing installation, see the [Upgrade Guide](USER_GUIDE_upgrade.md) instead.

## Table of Contents

- [Before You Begin](#before-you-begin)
- [System Requirements](#system-requirements)
- [Installation Overview](#installation-overview)
- [Step-by-Step Installation](#step-by-step-installation)
- [What Gets Installed](#what-gets-installed)
- [Verification](#verification)
- [Installation Scenarios](#installation-scenarios)
- [What NOT to Do](#what-not-to-do)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

## Before You Begin

### What You're Installing

The framework provides:

- **AI agent profiles** that define specialized roles (DevOps, Architecture, Documentation, etc.)
- **Work templates** for tasks, analysis, and planning
- **Document templates** for ADRs, APIs, and technical documentation
- **Validation tools** for quality assurance
- **Coordination protocols** for multi-agent workflows

Think of it as a structured workspace where AI assistants know their roles, follow consistent patterns, and produce predictable outputs.

### Who Should Install This?

You should install the framework if you:

- Want structured AI-augmented development workflows
- Need consistent documentation and decision tracking
- Work with multiple AI assistants and need coordination
- Want templates for common development activities
- Value reproducibility and auditability in AI-assisted work

### What You Need to Know

This guide assumes you:

- Can use a command line terminal
- Understand basic file paths and directory navigation
- Have access to the target repository
- Can run shell scripts

Don't worry—we'll explain each step clearly. If you get stuck, the [Troubleshooting](#troubleshooting) section has your back.

## System Requirements

### Operating System

**Supported:**
- Linux (any modern distribution)
- macOS (10.15 Catalina or newer)
- Windows with WSL (Windows Subsystem for Linux)

**Not supported:**
- Native Windows Command Prompt or PowerShell

> **Windows users:** Install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) first, then follow this guide from within WSL.

### Shell Requirements

You need a POSIX-compliant shell:

- bash (most common)
- sh (minimal but sufficient)
- zsh (works great)
- dash (also works)

**Check your shell:**
```bash
echo $SHELL
# Output examples:
# /bin/bash  ✅
# /bin/zsh   ✅
# /bin/sh    ✅
```

### Required Utilities

The installation script uses standard Unix utilities that are almost certainly already installed:

| Utility | Purpose | Check with |
|---------|---------|------------|
| `find` | Locate files | `which find` |
| `cp` | Copy files | `which cp` |
| `sha256sum` or `shasum` | Checksums | `which sha256sum` |
| `date` | Timestamps | `which date` |
| `cat`, `echo`, `sed` | Text processing | Built-in |

**Verify utilities:**
```bash
# Linux
command -v find && command -v cp && command -v sha256sum && echo "✅ All utilities present"

# macOS
command -v find && command -v cp && command -v shasum && echo "✅ All utilities present"
```

If any are missing (unlikely), install them via your package manager:

```bash
# Debian/Ubuntu
sudo apt-get install coreutils findutils

# macOS
# Should all be pre-installed
```

### Disk Space

You'll need approximately:

- **10-15 MB** for the framework files
- **5 MB** for the extracted release artifact (temporary)
- **Additional space** as you create work items and documentation

Total: ~20 MB for a fresh installation.

### Permissions

You must have:

- **Read access** to the release artifact
- **Write access** to the target directory
- **Execute permission** for shell scripts

```bash
# Check target directory permissions
ls -ld /path/to/your/repo

# Expected output should show you as owner or have write permissions:
# drwxr-xr-x  10 youruser  yourgroup  320 Jan 31 10:00 /path/to/your/repo
#  ↑ The 'w' means writable
```

## Installation Overview

Here's what you'll do:

1. **Download** the release artifact (.zip file)
2. **Extract** the archive
3. **Run** the installation script
4. **Verify** the installation succeeded
5. **Explore** what was installed

**Time required:** 5-10 minutes

**Can I undo this?** Yes. The framework tracks what it installs and never overwrites existing files. You can remove installed files if needed.

## Step-by-Step Installation

### Step 1: Download the Release

Get the latest release from GitHub:

**Option A: Using wget**
```bash
wget https://github.com/sddevelopment-be/quickstart_agent-augmented-development/releases/download/v1.0.0/quickstart-framework-1.0.0.zip
```

**Option B: Using curl**
```bash
curl -L -O https://github.com/sddevelopment-be/quickstart_agent-augmented-development/releases/download/v1.0.0/quickstart-framework-1.0.0.zip
```

**Option C: Browser download**
1. Visit https://github.com/sddevelopment-be/quickstart_agent-augmented-development/releases
2. Find the latest release
3. Download `quickstart-framework-X.Y.Z.zip`
4. Note where your browser saved it

> **Note:** Replace `v1.0.0` and `1.0.0` with the actual latest version number.

**Verify the download:**
```bash
ls -lh quickstart-framework-*.zip

# You should see something like:
# -rw-r--r--  1 youruser  yourgroup   3.2M Jan 31 10:00 quickstart-framework-1.0.0.zip
```

### Step 2: Verify Integrity (Optional but Recommended)

Every release includes checksums for verification:

```bash
# Download the checksums file
wget https://github.com/sddevelopment-be/quickstart_agent-augmented-development/releases/download/v1.0.0/checksums.txt

# Verify the artifact (Linux)
sha256sum -c checksums.txt

# Verify the artifact (macOS)
shasum -a 256 -c checksums.txt

# Expected output:
# quickstart-framework-1.0.0.zip: OK
```

If verification fails, re-download the artifact. Don't proceed with a corrupted file.

### Step 3: Extract the Archive

```bash
# Extract the zip file
unzip quickstart-framework-1.0.0.zip

# Navigate into the extracted directory
cd quickstart-framework-1.0.0

# Verify contents
ls -la
```

**You should see:**
```
drwxr-xr-x   framework_core/    # Framework files to install
drwxr-xr-x   scripts/           # Installation scripts
drwxr-xr-x   META/              # Release metadata
```

### Step 4: Preview the Installation (Dry Run)

Before actually installing, see what would happen:

```bash
./scripts/framework_install.sh --dry-run . /path/to/your/repo
```

Replace `/path/to/your/repo` with your actual target directory. Use `.` if installing into the current directory.

**What you'll see:**
```
ℹ Running in DRY RUN mode - no changes will be made
ℹ Validating release artifact structure...
✓ Release artifact structure is valid
ℹ Target directory: /path/to/your/repo
ℹ Scanning framework files...
ℹ Analysis complete

Would install 287 files:
  .github/agents/devops-danny.agent.md
  .github/agents/editor-eddy.agent.md
  .github/agents/architect-anna.agent.md
  ... (and 284 more)

No files would be skipped (none already exist)

✓ Dry run completed successfully!
```

**Review the output carefully:**
- Look at which files would be installed
- Verify target directory is correct
- Confirm nothing unexpected appears

> **Tip:** If you see files you don't want, you may need a different [distribution profile](USER_GUIDE_distribution.md#distribution-profiles).

### Step 5: Run the Installation

Once you're satisfied with the dry run, install for real:

```bash
./scripts/framework_install.sh . /path/to/your/repo
```

**What you'll see:**
```
ℹ Validating release artifact structure...
✓ Release artifact structure is valid
ℹ Target directory: /path/to/your/repo
ℹ Installing framework files...

Copying files:
  ✓ .github/agents/devops-danny.agent.md
  ✓ .github/agents/editor-eddy.agent.md
  ✓ .github/agents/architect-anna.agent.md
  ... (progress continues)

ℹ Creating framework metadata...
✓ Created .framework_meta.yml

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Framework Installation Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Results:
  NEW:      287 files
  SKIPPED:  0 files (already exist)

✓ Installation completed successfully!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Installation time:** 10-30 seconds depending on your system.

### Step 6: Verify the Installation

Confirm everything installed correctly:

```bash
# Navigate to your repo (if not already there)
cd /path/to/your/repo

# Check for metadata file
cat .framework_meta.yml
```

**Expected output:**
```yaml
framework_version: 1.0.0
installed_at: 2026-01-31T10:15:30Z
source_release: quickstart-framework-1.0.0
installer_version: 1.0.0
```

**Check installed structure:**
```bash
# List installed directories
ls -la .github/agents docs/templates work/templates framework validation

# Count installed files
find .github/agents -type f | wc -l
# Should show ~20-30 files in agents directory
```

**Test a template:**
```bash
# Copy a task template
cp work/templates/TASK_TEMPLATE.md work/my-first-task.md

# View it
cat work/my-first-task.md
```

If you see the template content, everything's working! 🎉

## What Gets Installed

After installation, your repository has new directories and files:

### Directory Structure

```
your-repository/
├── .github/
│   └── agents/                    # 🆕 Agent profiles and directives
│       ├── devops-danny.agent.md
│       ├── editor-eddy.agent.md
│       ├── architect-anna.agent.md
│       ├── researcher-rachel.agent.md
│       ├── tester-tim.agent.md
│       ├── framework-guardian.agent.md
│       ├── directives/            # Reusable directive documents
│       ├── guidelines/            # Operational guidelines
│       └── aliases.md             # Command shortcuts
│
├── docs/
│   ├── templates/                 # 🆕 Document templates
│   │   ├── ADR_TEMPLATE.md
│   │   ├── API_DOCUMENTATION_TEMPLATE.md
│   │   ├── TECHNICAL_DESIGN_TEMPLATE.md
│   │   └── ...
│   └── architecture/              # 🆕 Architecture documentation
│       ├── adrs/                  # Architectural Decision Records
│       └── design/                # Technical design documents
│
├── work/
│   ├── templates/                 # 🆕 Work item templates
│   │   ├── TASK_TEMPLATE.md
│   │   ├── ANALYSIS_TEMPLATE.md
│   │   ├── INVESTIGATION_TEMPLATE.md
│   │   └── ...
│   ├── collaboration/             # 🆕 (empty, for your work)
│   ├── reports/                   # 🆕 (empty, for your work)
│   └── logs/                      # 🆕 (empty, for your work)
│
├── framework/                     # 🆕 Python framework modules
│   ├── __init__.py
│   ├── core.py
│   ├── validation.py
│   └── ...
│
├── validation/                    # 🆕 Validation scripts
│   ├── validate_structure.py
│   ├── test_integration.py
│   └── ...
│
├── AGENTS.md                      # 🆕 Agent coordination protocol
├── README.md                      # 🆕 Framework documentation
├── pyproject.toml                 # 🆕 Python configuration
├── requirements.txt               # 🆕 Python dependencies
│
└── .framework_meta.yml            # 🆕 Installation metadata
```

### File Count by Directory

| Directory | Typical Count | Purpose |
|-----------|---------------|---------|
| `.github/agents/` | ~30 files | Agent profiles and directives |
| `docs/templates/` | ~15 files | Document templates |
| `docs/architecture/` | ~20 files | ADRs and design docs |
| `work/templates/` | ~10 files | Work item templates |
| `framework/` | ~20 files | Python modules |
| `validation/` | ~30 files | Test and validation scripts |
| Root files | ~5 files | Core documentation |

**Total:** Approximately 287 files (~12 MB)

### What's NOT Installed

The framework **intentionally excludes** certain directories from installation:

- **work/collaboration/**, **work/reports/**, **work/logs/** - Created empty for you to use
- **local/** - Reserved for your project-specific overrides (never touched by framework)
- **.git/** - Your git history remains untouched
- **IDE files** (.vscode, .idea) - Your editor config is yours
- **Your existing code** - The framework lives alongside your code, not in it

## Verification

### Quick Verification

```bash
# Check metadata file
[ -f .framework_meta.yml ] && echo "✅ Metadata exists" || echo "❌ Metadata missing"

# Check agent profiles
[ -d .github/agents ] && echo "✅ Agents directory exists" || echo "❌ Agents missing"

# Check templates
[ -d work/templates ] && echo "✅ Templates exist" || echo "❌ Templates missing"

# Count files
echo "Installed $(find .github/agents -type f | wc -l) agent files"
```

### Detailed Verification

```bash
# Verify directory structure
for dir in .github/agents docs/templates work/templates framework validation; do
    if [ -d "$dir" ]; then
        count=$(find "$dir" -type f | wc -l)
        echo "✅ $dir ($count files)"
    else
        echo "❌ $dir missing"
    fi
done

# Verify key files
for file in AGENTS.md README.md .framework_meta.yml; do
    if [ -f "$file" ]; then
        size=$(du -h "$file" | cut -f1)
        echo "✅ $file ($size)"
    else
        echo "❌ $file missing"
    fi
done
```

### Functional Verification

Test that templates are usable:

```bash
# Test task template
cp work/templates/TASK_TEMPLATE.md /tmp/test_task.md && \
    echo "✅ Task template works" || \
    echo "❌ Task template failed"

# Test ADR template
cp docs/templates/ADR_TEMPLATE.md /tmp/test_adr.md && \
    echo "✅ ADR template works" || \
    echo "❌ ADR template failed"

# Clean up tests
rm /tmp/test_task.md /tmp/test_adr.md
```

## Installation Scenarios

### Scenario 1: Fresh Repository

**Situation:** You have a new or nearly empty repository.

**Process:**
```bash
# Create repository if needed
mkdir my-new-project
cd my-new-project
git init

# Install framework
./path/to/quickstart-framework-1.0.0/scripts/framework_install.sh \
    /path/to/quickstart-framework-1.0.0 .

# Result: Clean installation, all 287 files installed
```

**Expected:**
- NEW: 287 files
- SKIPPED: 0 files

**Perfect for:** Starting a new project with the framework from day one.

### Scenario 2: Existing Project

**Situation:** You have an active project and want to add the framework.

**Process:**
```bash
cd /path/to/existing-project

# Preview what will happen
./path/to/quickstart-framework-1.0.0/scripts/framework_install.sh \
    --dry-run /path/to/quickstart-framework-1.0.0 .

# Review output, then install
./path/to/quickstart-framework-1.0.0/scripts/framework_install.sh \
    /path/to/quickstart-framework-1.0.0 .
```

**Expected:**
- NEW: 287 files (or fewer if some already exist)
- SKIPPED: Any files you already have (e.g., README.md, .github/)

**Behavior:** The installer never overwrites existing files. If you already have a `README.md`, it stays untouched.

**Perfect for:** Adopting the framework in an existing project.

### Scenario 3: Monorepo with Multiple Projects

**Situation:** You have a monorepo and want to install the framework once at the root.

**Process:**
```bash
cd /path/to/monorepo-root

# Install at root level
./path/to/quickstart-framework-1.0.0/scripts/framework_install.sh \
    /path/to/quickstart-framework-1.0.0 .

# Projects can share the framework:
# monorepo/
#   .github/agents/      ← Shared across all projects
#   work/templates/      ← Shared templates
#   projects/
#     project-a/
#       local/           ← Project-specific overrides
#     project-b/
#       local/           ← Project-specific overrides
```

**Perfect for:** Organizations with multiple related projects.

### Scenario 4: Team Template Repository

**Situation:** You're creating a template repository for your team to clone.

**Process:**
```bash
# Create template repo
mkdir team-project-template
cd team-project-template
git init

# Install framework
./path/to/quickstart-framework-1.0.0/scripts/framework_install.sh \
    /path/to/quickstart-framework-1.0.0 .

# Add team-specific customizations
mkdir -p local/agents
cp .github/agents/devops-danny.agent.md local/agents/devops-danny-team.agent.md
# Edit local/agents/devops-danny-team.agent.md with team specifics

# Commit and push
git add .
git commit -m "Initial framework setup"
git push
```

**Team members then:**
```bash
git clone <your-template-repo>
cd my-new-project
# Framework is already there!
```

**Perfect for:** Standardizing framework adoption across a team.

### Scenario 5: Partial Installation (Minimal Profile)

**Situation:** You only want agent profiles and templates, not the full framework.

**Process:**
You need the minimal distribution profile. See [Distribution Guide](USER_GUIDE_distribution.md#distribution-profiles) for how to obtain it.

```bash
# Download minimal profile
wget <url-to-minimal-profile>/quickstart-framework-1.0.0-minimal.zip

# Extract and install
unzip quickstart-framework-1.0.0-minimal.zip
cd quickstart-framework-1.0.0-minimal
./scripts/framework_install.sh . /path/to/repo

# Result: Only essential files installed
```

**Perfect for:** Lightweight adoption or constrained environments.

## What NOT to Do

### ❌ Don't Run Install Twice on the Same Repository

**Problem:** Running the installer again on an already-installed repository.

**What happens:** Nothing bad—the installer skips existing files. But you waste time.

**Instead:** Use the [upgrade script](USER_GUIDE_upgrade.md) for updating existing installations.

```bash
# ❌ Wrong
./scripts/framework_install.sh . .  # Already installed

# ✅ Right
./scripts/framework_upgrade.sh . .  # Use upgrade script
```

### ❌ Don't Modify Framework Files Directly

**Problem:** Editing files in `.github/agents/`, `docs/templates/`, etc.

**What happens:** Future upgrades will detect conflicts and you'll have to merge manually.

**Instead:** Put customizations in `local/`:

```bash
# ❌ Wrong
vim .github/agents/devops-danny.agent.md  # Direct modification

# ✅ Right
mkdir -p local/agents
cp .github/agents/devops-danny.agent.md local/agents/devops-danny-custom.agent.md
vim local/agents/devops-danny-custom.agent.md
# Files in local/ are never touched by upgrades
```

### ❌ Don't Delete .framework_meta.yml

**Problem:** Removing the metadata file that tracks your installation.

**What happens:** Future upgrades won't recognize the installation and might behave incorrectly.

**Instead:** Leave it alone. It's small and important.

### ❌ Don't Install into the Framework Repository Itself

**Problem:** Running the installer inside the framework's own source directory.

**What happens:** Confusion and potential circular dependencies.

**Instead:** Always install into a separate project repository:

```bash
# ❌ Wrong
cd quickstart_agent-augmented-development
./ops/release/framework_install.sh . .

# ✅ Right
cd quickstart_agent-augmented-development
./ops/release/framework_install.sh . /path/to/other/project
```

### ❌ Don't Ignore Dry Run Warnings

**Problem:** Skipping the `--dry-run` check before installing.

**What happens:** You might install into the wrong directory or discover issues too late.

**Instead:** Always dry run first:

```bash
# ✅ Always do this first
./scripts/framework_install.sh --dry-run . /path/to/repo
# Review output carefully
./scripts/framework_install.sh . /path/to/repo
```

### ❌ Don't Install Without Backups (for Production Repos)

**Problem:** Installing into a production repository without backing up first.

**What happens:** While the installer never overwrites files, it's good practice to have backups.

**Instead:**

```bash
# ✅ For important repositories
cd /path/to/important-repo
git status  # Ensure clean state
git commit -am "Prepare for framework installation"
git tag pre-framework-install
# Now install
./scripts/framework_install.sh /path/to/release .
```

## Troubleshooting

### Issue: "No such file or directory"

**Symptom:**
```bash
$ ./scripts/framework_install.sh . /path/to/repo
bash: ./scripts/framework_install.sh: No such file or directory
```

**Cause:** You're not in the extracted release directory.

**Solution:**
```bash
# Check where you are
pwd

# Navigate to release directory
cd /path/to/quickstart-framework-1.0.0

# Try again
./scripts/framework_install.sh . /path/to/repo
```

### Issue: "Permission denied"

**Symptom:**
```bash
$ ./scripts/framework_install.sh . .
bash: ./scripts/framework_install.sh: Permission denied
```

**Cause:** Script not executable.

**Solution:**
```bash
# Make script executable
chmod +x scripts/framework_install.sh

# Try again
./scripts/framework_install.sh . .
```

### Issue: "Target directory does not exist"

**Symptom:**
```
✗ Target directory does not exist: /path/to/repo
```

**Cause:** Target directory doesn't exist or path is wrong.

**Solution:**
```bash
# Check if directory exists
ls -ld /path/to/repo

# Create it if needed
mkdir -p /path/to/repo

# Or fix the path
./scripts/framework_install.sh . /correct/path
```

### Issue: "Invalid release artifact structure"

**Symptom:**
```
✗ Invalid release artifact structure. Missing directories:
   - framework_core/
   - scripts/
```

**Cause:** You're running the script from the wrong location or the archive is corrupt.

**Solution:**
```bash
# Re-extract the archive
unzip -o quickstart-framework-1.0.0.zip

# Navigate into it
cd quickstart-framework-1.0.0

# Verify structure
ls -la
# Should show: framework_core/, scripts/, META/

# Try again
./scripts/framework_install.sh . /path/to/repo
```

### Issue: "Framework appears to be already installed"

**Symptom:**
```
⚠ Warning: Framework appears to be already installed
   Found: .framework_meta.yml
   Use framework_upgrade.sh to upgrade existing installation
```

**Cause:** Framework is already installed in the target directory.

**Solution:**

If you want to upgrade:
```bash
./scripts/framework_upgrade.sh . /path/to/repo
```

If you want to reinstall from scratch:
```bash
# Remove metadata file
rm /path/to/repo/.framework_meta.yml

# Run install again
./scripts/framework_install.sh . /path/to/repo
```

### Issue: Files Already Exist

**Symptom:**
```
Results:
  NEW:      280 files
  SKIPPED:  7 files (already exist)
```

**Cause:** Some framework files already exist in your repository.

**This is normal!** The installer never overwrites existing files.

**To see what was skipped:**
```bash
# Run with verbose flag
./scripts/framework_install.sh --verbose . /path/to/repo | grep SKIPPED
```

**If you want to overwrite specific files:**
```bash
# Remove the specific file first
rm /path/to/repo/README.md

# Re-run install
./scripts/framework_install.sh . /path/to/repo
```

### Issue: No Space Left on Device

**Symptom:**
```
cp: cannot create regular file '.github/agents/devops-danny.agent.md': No space left on device
```

**Cause:** Target filesystem is full.

**Solution:**
```bash
# Check disk space
df -h /path/to/repo

# Free up space or use a different location
./scripts/framework_install.sh . /other/path/with/space
```

### Issue: SHA256 Utility Not Found

**Symptom:**
```
✗ Neither sha256sum nor shasum found. Cannot verify checksums.
```

**Cause:** Checksum utilities missing (rare).

**Solution:**
```bash
# Linux
sudo apt-get install coreutils

# macOS
# Should be pre-installed; if not, install via Homebrew:
brew install coreutils
```

## Next Steps

### Explore What You've Got

```bash
# Browse agent profiles
ls -la .github/agents/

# Read a profile
cat .github/agents/devops-danny.agent.md | less

# Look at templates
ls -la work/templates/
ls -la docs/templates/
```

### Create Your First Task

```bash
# Copy task template
cp work/templates/TASK_TEMPLATE.md work/collaboration/my-first-task.md

# Edit it
vim work/collaboration/my-first-task.md

# Work with an AI agent referencing the profile
# In your AI assistant: "Act as Editor Eddy and help me with my-first-task.md"
```

### Read the Documentation

- **[Getting Started](quickstart/GETTING_STARTED.md)** - Quick introduction
- **[Distribution Guide](USER_GUIDE_distribution.md)** - What's in the framework
- **[Upgrade Guide](USER_GUIDE_upgrade.md)** - How to upgrade later
- **[AGENTS.md](../AGENTS.md)** - Full agent coordination protocol

### Customize Your Installation

Create project-specific overrides:

```bash
# Create local override directory
mkdir -p local/agents

# Copy and customize an agent profile
cp .github/agents/devops-danny.agent.md local/agents/devops-danny-custom.agent.md

# Edit with your team's specific practices
vim local/agents/devops-danny-custom.agent.md
```

The `local/` directory is never touched by framework upgrades, so your customizations are safe.

### Set Up Version Control

If your repository uses Git:

```bash
# Review what was installed
git status

# Stage framework files
git add .github/ docs/ work/ framework/ validation/ AGENTS.md .framework_meta.yml

# Commit
git commit -m "Install Quickstart Framework v1.0.0"

# Consider adding work/collaboration/ to .gitignore
echo "work/collaboration/" >> .gitignore
echo "work/logs/" >> .gitignore
git add .gitignore
git commit -m "Ignore work collaboration artifacts"
```

### Join the Community

- **Star the repository** on GitHub
- **Report issues** if you find bugs
- **Share feedback** on what works (or doesn't)
- **Contribute improvements** back to the framework

## Related Documentation

- **[Upgrade Guide](USER_GUIDE_upgrade.md)** - Upgrading existing installations
- **[Distribution Guide](USER_GUIDE_distribution.md)** - Understanding what's distributed
- **[Getting Started](quickstart/GETTING_STARTED.md)** - Quick start guide
- **[Technical Installation Doc](HOW_TO_USE/framework_install.md)** - Technical details
- **[ADR-013](architecture/adrs/ADR-013-zip-distribution.md)** - Distribution architecture
- **[ADR-014](architecture/adrs/ADR-014-framework-guardian-agent.md)** - Framework Guardian

## Support

Need help?

1. Check this guide's [Troubleshooting](#troubleshooting) section
2. Review the installation script help: `./scripts/framework_install.sh --help`
3. Read the [technical documentation](HOW_TO_USE/framework_install.md)
4. Search [existing issues](https://github.com/sddevelopment-be/quickstart_agent-augmented-development/issues)
5. Create a new issue with:
   - Operating system and shell version
   - Command you ran
   - Complete error output
   - Result of `ls -la` in the release directory

---

**Last Updated:** 2026-01-31  
**Document Version:** 1.0.0  
**Framework Version:** 1.0.0+

