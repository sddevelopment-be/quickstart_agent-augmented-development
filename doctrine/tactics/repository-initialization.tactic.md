# Tactic: Repository Initialization

**Invoked by:**
- [Directive 003 (Repository Quick Reference)](../directives/003_repository_quick_reference.md)
- Shorthand: [`/bootstrap-repo`](../shorthands/bootstrap-repo.md)

---

## Intent

Bootstrap a new repository with standard directory structure, configuration files, and initial documentation per SDD framework.

**Apply when:**
- Creating new repository from template or scratch
- Migrating existing project to SDD framework
- Setting up derivative repository from parent

---

## Execution Steps

### 1. Create Directory Structure
```
├── doctrine/             # Portable framework (git subtree)
├── docs/                 # Canonical documentation
├── specifications/       # Optional functional specs
├── src/                  # Production code
├── tests/                # All test code
├── tools/                # Development utilities
├── fixtures/             # Test data
└── work/                 # Operational artifacts
    ├── collaboration/    # Task orchestration
    ├── reports/          # Work logs, reflections
    └── notes/            # Exploratory scratch
```

### 2. Generate Configuration Files
- [ ] `.doctrine-config/config.yaml` (repository settings)
- [ ] `.gitignore` (standard exclusions)
- [ ] `README.md` (project overview)
- [ ] `.github/workflows/` (CI/CD if applicable)

### 3. Initialize Documentation
- [ ] `docs/README.md` (documentation index)
- [ ] `docs/architecture/adrs/README.md` (ADR index)
- [ ] `CHANGELOG.md` (version history)

### 4. Configure Tooling
- [ ] Package manager files (package.json, requirements.txt, etc.)
- [ ] Linter/formatter config
- [ ] Test runner config

### 5. First Commit
- [ ] Stage all files
- [ ] Commit with message: "Initial repository structure"
- [ ] Tag as `v0.1.0` if appropriate

---

## Outputs
- Complete directory structure
- Configuration files
- Initial documentation
- First commit

---

**Status:** ✅ Active
