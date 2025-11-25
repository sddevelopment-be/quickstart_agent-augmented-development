## 1. Big picture: what the release zip should contain

Think of each release as a **drop-in framework core** with:

```text
quickstart-framework-1.2.0/
  framework_core/          # all the opinionated defaults
    .github/agents/
    docs/directives/
    docs/guidelines/
    docs/templates/
    validation/
    work/README.md
    ... (other core files)
  scripts/
    framework_install.sh
    framework_upgrade.sh
  META/
    MANIFEST.yml           # list of core files + modes
    RELEASE_NOTES.md
    UPGRADE_NOTES_1.1_to_1.2.md
```

Users can be on:

* GitHub / GitLab / Bitbucket
* bare Git on a local NAS
* another VCS
* no VCS at all

All they need is:

1. Download `quickstart-framework-1.2.0.zip`
2. Unzip
3. Run a script with their project path
4. Check generated diff / conflict report

---

## 2. Core concept: **core vs local** in any project

To preserve local customizations, your framework must never require people to *edit core files directly*.

Recommend you standardize this pattern in projects:

```text
project-root/
  framework_core/     # synced from release zip; "do not edit" in principle
  local/              # project-specific overrides + custom agents
  .framework_meta.yml # version, installation info
  ...
```

Or, if you don’t want a visible `framework_core` folder, you can still **treat some paths as “managed”**:

* `.github/agents/` (core agents and guardrails)
* `docs/templates/agent-tasks/`
* `docs/directives/`
* `docs/guidelines/`
* `validation/`
* `work/README.md`

And reserve:

* `local/**`
* `local_agents/**`
* `local_guidelines/**`

for custom stuff.

Your scripts then:

* **sync only the core paths**
* never touch `local/**`
* never delete anything

---

## 3. Behaviour of the shell scripts

### `framework_install.sh` (fresh project)

Usage:

```bash
./scripts/framework_install.sh /path/to/project-root
```

It should:

1. Detect if this is a first-time install (`.framework_meta.yml` missing).
2. Copy all `framework_core` files into the project:

    * create missing directories
    * only overwrite if target file doesn’t exist
    * record installed version in `.framework_meta.yml`
3. Print a summary:

    * NEW files
    * SKIPPED files (already existed)

After this, the user tweaks:

* `docs/VISION.md`
* any local overrides in `local/**`

---

### `framework_upgrade.sh` (existing project)

Usage:

```bash
./scripts/framework_upgrade.sh /path/to/project-root --dry-run
./scripts/framework_upgrade.sh /path/to/project-root
```

It should:

1. Read `.framework_meta.yml` to know the current version.
2. For each file in `framework_core`:

    * if target file **does not exist** → copy (mark `NEW`)
    * if target file exists and is **identical** → report `UNCHANGED`
    * if target file exists and **differs** →

        * **do not overwrite directly**
        * write new version as `<name>.framework-new`
        * optionally back up old as `<name>.bak.<timestamp>`
        * log as `CONFLICT`
3. Update `.framework_meta.yml` with new framework version.
4. In `--dry-run` mode: do everything except the actual copying.

This gives the user a very clear workflow:

* run `--dry-run`, inspect report
* run full upgrade, then manually fix any `.framework-new` conflicts
* commit / snapshot changes in their own VCS

---

## 4. Minimal example shell script (POSIX-ish)

This is intentionally simple and conservative.

```bash
#!/usr/bin/env sh
# scripts/framework_upgrade.sh
# Usage: framework_upgrade.sh /path/to/project-root [--dry-run]

set -eu

FRAMEWORK_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CORE_DIR="${FRAMEWORK_ROOT}/framework_core"
PROJECT_ROOT="${1:-.}"
DRY_RUN="${2:-}"

if [ ! -d "$PROJECT_ROOT" ]; then
  echo "❌ Target project directory does not exist: $PROJECT_ROOT" >&2
  exit 1
fi

echo "▶ Framework core: $CORE_DIR"
echo "▶ Project root:   $PROJECT_ROOT"
[ "$DRY_RUN" = "--dry-run" ] && echo "▶ Mode:           DRY RUN (no files will be changed)"

# Simple helper to copy or simulate
copy_file() {
  src="$1"
  dst="$2"

  dst_dir=$(dirname "$dst")
  [ -d "$dst_dir" ] || mkdir -p "$dst_dir"

  if [ "$DRY_RUN" = "--dry-run" ]; then
    echo "  - WOULD COPY: $src -> $dst"
  else
    cp "$src" "$dst"
    echo "  - COPIED: $src -> $dst"
  fi
}

# Walk framework_core and sync files
cd "$CORE_DIR"

echo "▶ Scanning framework_core for files to sync..."

# Use find to list regular files
find . -type f | while read -r relpath; do
  src="${CORE_DIR}/${relpath}"
  dst="${PROJECT_ROOT}/${relpath#./}"

  # Skip obvious meta files if you want, e.g. local overrides
  case "$relpath" in
    ./local/*) 
      # never sync anything from framework's local/ if present
      continue
      ;;
  esac

  if [ ! -e "$dst" ]; then
    echo "NEW       $relpath"
    copy_file "$src" "$dst"
  else
    # Compare contents
    if diff -q "$src" "$dst" >/dev/null 2>&1; then
      echo "UNCHANGED $relpath"
    else
      # Conflict – do not overwrite, create .framework-new
      new_path="${dst}.framework-new"
      echo "CONFLICT  $relpath"
      if [ "$DRY_RUN" = "--dry-run" ]; then
        echo "  - WOULD WRITE NEW VERSION TO: $new_path"
      else
        cp "$src" "$new_path"
        echo "  - WROTE NEW VERSION TO: $new_path"
      fi
    fi
  fi
done

echo "▶ Done."
echo "  - NEW:      files were added where missing."
echo "  - UNCHANGED: files identical to current version."
echo "  - CONFLICT: *.framework-new files need manual merge."

# Note: you can update .framework_meta.yml here if desired.
```

You’d mirror this logic for `framework_install.sh`, but with a simpler behaviour (no conflict logic, because you assume first install).

---

## 5. Making this work across platforms

* On macOS / Linux / WSL → script above is fine.
* On Windows:

    * Recommend running in Git Bash or WSL.
    * Optionally ship a `framework_upgrade.ps1` that wraps the same logic in PowerShell.

Because the “contract” is just **“copy these files according to these rules”**, it doesn’t matter which VCS or platform they use — the semantics are the same.

---

## 6. Release pipeline for you

In your CI / local release script:

1. Clean export of framework core:

   ```bash
   mkdir -p dist/framework_core
   rsync -a \
     .github/agents \
     docs/templates \
     docs/directives \
     docs/guidelines \
     validation \
     work/README.md \
     dist/framework_core/
   ```
2. Copy `scripts/framework_install.sh` and `framework_upgrade.sh` into `dist/scripts/`.
3. Generate `META/MANIFEST.yml` and `META/RELEASE_NOTES.md`.
4. Zip `dist/`:

   ```bash
   cd dist
   zip -r ../quickstart-framework-1.2.0.zip .
   ```

That zip is now:

* Git agnostic
* Platform agnostic (modulo shell)
* Easy to host anywhere (GitHub releases, simple web server, local share)

---

## 7. What you get out of this

* People on any platform can adopt the framework with **one download + one script**.
* Local customizations live outside the core (or at least are protected by the `.framework-new` conflict rule).
* Upgrades are **transparent**: they see NEW / UNCHANGED / CONFLICT, nothing hidden.
* You can tighten and evolve the framework without breaking existing user repos.

A next step could be a small `MANIFEST.yml` example that:

* marks which paths are “core-managed”
* optionally distinguishes “copy once” vs “always sync” files so the scripts can be a bit smarter without getting complicated.
