+++
title = "Python Primer"
subtitle = "There should be one — and preferably only one — obvious way to do it."
aliases = ["python-primer", "programming-languages/python"]
author = "Stijn Dejongh"
outputs = ['html', 'rss', 'json']
date = "2025-11-09T12:00:00+00:00"
tags = ["programming", "python", "primer", "reference", "intermediate"]
summary = """
Python prizes clarity over cleverness and treats readability as a social contract. Code should look like well-edited prose: explicit, orthogonal, and easy to explain to the next engineer. The language stays small on purpose so that libraries, not the core grammar, carry most complexity.
"""
image = "primers/python_logo"
+++

## 1. Language Philosophy

> “There should be one — and preferably only one — obvious way to do it.” — *The Zen of Python*

Python prizes clarity over cleverness and treats readability as a social contract. Code should look like well-edited prose: explicit, orthogonal, and easy to explain to the next engineer. The language stays small on purpose so that libraries, not
the core grammar, carry most complexity.

- **Human-centric design.** Features exist to keep conversations about code short—naming, indentation, and structure all reinforce collective understanding.
- **Pragmatic dynamism.** Strong introspection and runtime flexibility let you build tools quickly, but the community expects discipline when touching metaprogramming or monkey-patching.
- **Batteries included.** The standard library covers files, networking, parsing, testing, and concurrency so teams can focus on their own logic.
- **Cultural restraint.** Community norms discourage “clever” one-liners when straight code is clearer; idioms evolve from practice, not dogma.

Treat Python as a glue language with range: ideal for orchestration, data analysis, scripting, and prototyping, yet capable of long-lived services when you apply structure intentionally.

## 2. Syntax and Naming Conventions

Python syntax stays intentionally boring so that structure—not punctuation—carries the meaning. Naming is the loudest signal of intent, so teams lean on consistent cases and docstrings.

{{< bootstrap-table "bootstrap-table table-striped table-responsive " >}}
| Element             | Convention                   | Example                                |
|---------------------|------------------------------|----------------------------------------|
| Variables/functions | `snake_case`                 | `pending_tasks`, `archive_completed()` |
| Classes             | `PascalCase`                 | `TaskBoard`, `TaskRepository`          |
| Constants           | `ALL_CAPS`                   | `MAX_ACTIVE_TASKS = 10`                |
| Private members     | `_single_leading_underscore` | `_task_cache`, `_load_board()`         |
| Modules/files       | `lowercase_with_underscores` | `task_filters.py`                      |
| Docstrings          | Triple quotes, summary first | `"""Calculate completion rate."""`     |
| Type hints          | Optional but encouraged      | `def mark_done(task: Task) -> Task:`   |
{{< /bootstrap-table >}}

PEP 8 is the shared style contract. Enforce it automatically with [Black](https://black.readthedocs.io/en/stable/) for formatting and [Ruff](https://docs.astral.sh/ruff/) or `flake8` for linting. F-strings, assignment expressions, and type hints
are idiomatic when they keep code expressive without obscuring intent.

## 3. Version and Dependency Management

Isolation is non-negotiable because Python versions, native extensions, and CLI tools evolve at their own pace. The modern kit keeps system Python untouched while giving each project a repeatable environment.

{{< bootstrap-table "bootstrap-table table-striped table-responsive " >}}
| Tool        | Role                                           | Why teams use it                               |
|-------------|-----------------------------------------------|------------------------------------------------|
| `pyenv`     | Install and switch between Python runtimes    | Keeps multiple 3.x versions side by side       |
| `pipx`      | Isolated global CLI installer                 | Lets you install Poetry, Ruff, etc. safely     |
| `poetry`    | Dependency manager + virtualenv + builder     | Single command surface for add/install/publish |
| `venv`      | Standard library virtual environment module   | Lightweight fallback used under the hood       |
{{< /bootstrap-table >}}


Typical workflow:

```bash
pyenv install 3.12.3
pyenv local 3.12.3
poetry init
poetry add requests
poetry add --group dev pytest
poetry shell
```

`poetry.lock` pins exact versions for reproducibility. Legacy stacks may still rely on `pip` + `requirements.txt`, so expect to read both formats. Teams expect developers to activate the right virtualenv before running tools—automate it via direnv
or shell hooks if needed.

## 4. Build and Packaging Tooling

Python build tooling is layered: the language runtime stays small while packaging tools evolve independently. Modern projects lean on the `pyproject.toml` standard so that formatters, linters, and build tools share one config surface.

{{< bootstrap-table "bootstrap-table table-striped table-responsive " >}}
| Tool         | Role                                      | Notes                                           |
|--------------|-------------------------------------------|-------------------------------------------------|
| `poetry`     | Build + publish projects via PEP 517 flow | Recommended default; wraps env + deps + build   |
| `setuptools` | Legacy builder                            | Still common in older repos or corporate libs   |
| `build`      | PEP 517 reference builder                 | What `poetry build` calls under the hood        |
| `twine`      | Upload wheels/sdist to PyPI               | Used for manual or CI-driven publishing         |
{{< /bootstrap-table >}}

Reference layout:

```
project/
├── pyproject.toml        # build + dependency metadata
├── poetry.lock
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── core.py
│       └── adapters.py
├── tests/
│   └── test_core.py
├── README.md
└── .pre-commit-config.yaml
```

CI typically runs `poetry install`, `poetry run pytest`, and `poetry build`. Publishing is either `poetry publish` (with stored credentials) or a `twine upload dist/*` step.

## 5. Testing Frameworks

- **Testing mindset:** prefer small, behaviour-focused tests with descriptive names. Fixtures and parametrization replace heavy inheritance hierarchies. Integration tests stay close to the public interface; property-based approaches cover data-heavy
  paths.

{{< bootstrap-table "bootstrap-table table-striped table-responsive " >}}
| Tool         | Purpose                          | Why it matters                                  |
|--------------|----------------------------------|-------------------------------------------------|
| `pytest`     | De facto testing framework       | Fixtures, parametrization, rich plugin ecosystem|
| `unittest`   | Standard library xUnit           | Still used in legacy codebases                  |
| `hypothesis` | Property-based testing           | Generates inputs to challenge invariants        |
| `tox`        | Multi-environment orchestration  | Runs tests across Python versions or envs       |
{{< /bootstrap-table >}}

Canonical `pytest` example:

```python
# tests/test_stats.py
from todo_app.models import Task, TaskState
from todo_app.stats import completion_rate


def test_completion_rate_handles_empty_board():
    assert completion_rate([]) == 0.0


def test_completion_rate_counts_done_tasks():
    tasks = [
        Task(title="Draft notes", state=TaskState.DONE),
        Task(title="Record episode", state=TaskState.IN_PROGRESS),
    ]
    assert completion_rate(tasks) == 0.5
```

Commands stay explicit: `poetry run pytest`, `poetry run pytest tests/integration`, or `tox -e py312`. Coverage tooling (`coverage.py`) and mutation testing (`mutmut`) are optional add-ons when the domain justifies them.

## 6. Programming Idioms

Python embraces multiple paradigms. Object-oriented code structures long-lived domains, functional helpers keep transformations honest, and imperative orchestration glues everything together. The language makes paradigm shifts cheap, so choose the
style that keeps intent clearest for each layer.

### 6.1 Object-Oriented Idioms

Reach for OO when you need identity, lifecycle, or substitutable collaborators. Python favors composition over inheritance: keep behaviour in focused methods, lean on `@dataclass` for value objects, and expose interfaces via `abc.ABC` or
`typing.Protocol`.

- Use `dataclasses`/`attrs` for concise domain models and value semantics.
- Rely on `@property`, `__repr__`, and comparison dunder methods to keep objects debuggable.
- Prefer protocols and dependency injection over hard-coded concrete types.

```python
from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime, timezone


class TaskState(Enum):
    TODO = auto()
    IN_PROGRESS = auto()
    DONE = auto()


@dataclass
class Task:
    title: str
    state: TaskState = TaskState.TODO
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    due_at: datetime | None = None
    tags: set[str] = field(default_factory=set)
    completed_at: datetime | None = None

    def start(self) -> None:
        if self.state == TaskState.TODO:
            self.state = TaskState.IN_PROGRESS

    def complete(self) -> None:
        if self.state == TaskState.IN_PROGRESS:
            self.state = TaskState.DONE
            self.completed_at = datetime.now(timezone.utc)
```

Pair these objects with thin service classes (e.g., `TaskSyncService`, `TaskRepository`) so orchestration layers can swap implementations in tests. OO shines when you must guard invariants or coordinate multiple collaborators over time.

### 6.2 Functional Programming Idioms

Functional techniques keep business rules pure and predictable. Treat functions as values, chain them with comprehensions or iterators, and pass data through pipelines instead of mutating shared state.

- First-class functions, closures, and `functools.partial` encourage composition.
- Immutability via tuples, frozen dataclasses, or `typing.NamedTuple` keeps data trustworthy.
- `itertools`, generator expressions, and comprehensions make lazy pipelines ergonomic.

```python
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from functools import partial

from todo_app.models import Task, TaskState


def tag_overdue(current_time: datetime, task: Task) -> Task:
    if task.due_at and task.due_at < current_time and task.state != TaskState.DONE:
        return replace(task, tags=task.tags | {"overdue"})
    return task


mark_overdue = partial(tag_overdue, datetime.now(timezone.utc))

tasks = [
    Task(title="Draft outline", due_at=datetime.now(timezone.utc) - timedelta(days=1)),
    Task(title="Record episode", due_at=datetime.now(timezone.utc) + timedelta(days=2)),
]

active = (t for t in tasks if t.state != TaskState.DONE)
overdue = [mark_overdue(t) for t in active]
```

Reach for FP when modeling transformations (parsing, validation, scoring) or whenever you want trivial unit tests. Property-based testing (`hypothesis`) pairs naturally with this style.

### 6.3 Imperative Programming Idioms

Imperative code glues everything together: CLI commands, cron jobs, deployment scripts, and adapters that coordinate IO. Being explicit about steps and side effects keeps failure modes visible.

- Favor straight-line `for`/`while` control flow for orchestration.
- Use context managers (`with ...`) to scope resources such as files or network connections.
- Bubble up meaningful exceptions; define domain-specific ones when necessary.

```python
import json
from dataclasses import asdict
from pathlib import Path

from todo_app.models import Task, TaskState


def sync_tasks(path: Path) -> list[Task]:
    if not path.exists():
        return []
    data = json.loads(path.read_text())
    return [Task(**task) for task in data]


def complete_first_task(path: Path) -> None:
    tasks = sync_tasks(path)
    if not tasks:
        return
    tasks[0].state = TaskState.DONE
    path.write_text(json.dumps([asdict(task) for task in tasks], default=str, indent=2))


try:
    complete_first_task(Path("tasks.json"))
    print("Marked the first task as done.")
except json.JSONDecodeError:
    print("tasks.json is corrupt — run the repair command.")
```

Use imperative style for orchestration layers, CLI tooling (`typer`, `click`), and task runners (`invoke`, `nox`). Keep domain logic in pure functions; call them from these command surfaces so behaviour remains testable.

### 6.4 Idiom Integration

Healthy Python systems layer paradigms to keep trade-offs explicit:

1. **Domain core (FP).** Pure functions implement calculations, parsing, validation, and decisions so they remain easy to test and reason about.
2. **Application services (OO).** Small classes model stateful collaborators—repositories, gateways, schedulers—and give you seams for substitution or instrumentation.
3. **Orchestration (imperative).** Commands, CLI entry points, and adapters invoke the core, handle IO, retries, logging, and configuration.

This separation keeps logic deterministic, side effects contained, and architecture approachable for new collaborators.

## 7. Workspace Bootstrap

Stabilize the local environment before writing code so every collaborator can reproduce the same workflow.

1. **Install prerequisites.** Make sure build essentials, `git`, and SSL/zlib headers are present. On Ubuntu this is `sudo apt install build-essential curl git zlib1g-dev libssl-dev ...`; on macOS run `xcode-select --install` and
   `brew install openssl readline sqlite3 xz zlib tcl-tk git`.
2. **Provision runtimes.** Use `pyenv` to install and pin the project’s Python (e.g., `pyenv install 3.12.3 && pyenv local 3.12.3`). Install `pipx` so CLI tools (Poetry, Ruff, Black, Mypy) stay isolated from system Python.
3. **Initialize Poetry.** Run `poetry init -n`, then add dependencies (`poetry add typer rich` and `poetry add --group dev pytest black ruff mypy pre-commit`). Configure `poetry config virtualenvs.in-project true` if you want `.venv/` 
   located in the project directory (and add it to `.gitignore`).
4. **Lay out automation.** Create a `Makefile` (or `noxfile.py`) with targets like `fmt`, `lint`, `test`, and `typecheck` that shell out to `poetry run ...`. Keep orchestration declarative so CI can reuse the same commands.
5. **Wire quality gates.** Install `pre-commit` via `pipx install pre-commit`, add hooks for Ruff, Black, and Mypy, then run `pre-commit install`. CI should execute the same hooks plus `poetry run pytest`.
6. **Scaffold the TODO app (or your domain).** Organize code under `src/your_package`, tests under `tests/`, and keep CLI entry points (Typer, Click) in `src/your_package/cli.py`. Store example data/state (e.g., `tasks.json`) in `examples/` so
   onboarding developers can run through a realistic workflow.

## 8. Quickstart Setup (Unix)

> Minimal, repeatable steps for macOS, Ubuntu, and most Linux distributions.

1. **System dependencies.**
    - Ubuntu:
      ```bash
      sudo apt update
      sudo apt install -y build-essential curl git zlib1g-dev libssl-dev \
          libbz2-dev libsqlite3-dev libncurses5-dev libffi-dev liblzma-dev tk-dev
      ```  
    - macOS (Homebrew):
      ```bash
      xcode-select --install
      brew install openssl readline sqlite3 xz zlib tcl-tk git
      ```

2. **Install `pyenv`.**
   ```bash
   curl https://pyenv.run | bash
   echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.zshrc
   echo 'eval "$(pyenv init -)"' >> ~/.zshrc
   echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
   ```  
   Restart your shell, then `pyenv install 3.12.3 && pyenv global 3.12.3`.

3. **Install `pipx`.**
   ```bash
   python -m pip install --user pipx
   python -m pipx ensurepath
   ```

4. **Install Poetry.**
   ```bash
   pipx install poetry
   poetry --version
   poetry config virtualenvs.in-project true
   ```

5. **Install global tooling (optional).**
   ```bash
   pipx install pre-commit
   pipx install ruff
   pipx install black
   pipx install mypy
   ```

6. **Create a project scaffold.**
   ```bash
   mkdir todo-app && cd todo-app
   poetry init -n
   poetry env use 3.12.3
   poetry add typer rich
   poetry add --group dev pytest black ruff mypy pre-commit
   poetry shell
   ```

7. **Verify tooling.**
   ```bash
   python -V          # 3.12.x
   poetry -V
   pytest --version
   ruff --version
   ```

8. **Optional VS Code setup.** Install the Python, Pylance, Black, Ruff, and Mypy extensions, then choose the Poetry-created `.venv` via *Python: Select Interpreter*.

9. **Convenience aliases (optional).**
   ```bash
   alias fmt="poetry run ruff --fix . && poetry run black ."
   alias lint="poetry run ruff ."
   alias test="poetry run pytest"
   alias typecheck="poetry run mypy"
   ```

## 9. First-Time Verification Checklist

Run these commands once the project scaffold is in place to ensure everything works end-to-end:

{{< bootstrap-table "bootstrap-table table-striped table-responsive " >}}
| Check              | Command                                            | Expected                               |
|--------------------|----------------------------------------------------|----------------------------------------|
| Python runtime     | `python -V`                                        | `Python 3.12.x` (from project `.venv`) |
| Poetry version     | `poetry -V`                                        | Displays installed release             |
| Dependency install | `poetry install`                                   | Resolves and installs app + dev deps   |
| Tests              | `poetry run pytest`                                | All tests green; failure output if not |
| Formatter          | `poetry run black --check .`                       | “All done!” or files listed for fix    |
| Linter             | `poetry run ruff .`                                | No diagnostics or actionable warnings  |
| Type checker       | `poetry run mypy`                                  | “Success: no issues found”             |
| Pre-commit         | `pre-commit install && pre-commit run --all-files` | Hooks run cleanly                      |
| CLI smoke test     | `poetry run python -m your_package.cli --help`     | Help text rendered                     |
{{< /bootstrap-table >}}

**Troubleshooting notes**

- If `pyenv` shims are not picked up, confirm the PATH exports live in your shell rc file and reopen the terminal.
- For SSL or bz2 import errors, install the missing system libraries (`libssl-dev`, `libbz2-dev`, etc.) and rebuild the Python version via `pyenv uninstall && pyenv install`.
- When hooks modify files, rerun `git status` to ensure changes are staged before committing.

## 10. Appendix

### Core References

- [Python documentation](https://docs.python.org/3/) — canonical manual for language, stdlib, and tooling.
- [The Zen of Python](https://peps.python.org/pep-0020/) and [PEP 8](https://peps.python.org/pep-0008/) — tone setters for clarity and style.
- Tooling specs: [Pyenv](https://github.com/pyenv/pyenv), [Poetry](https://python-poetry.org/docs/), [Pipx](https://pipx.pypa.io/stable/), [Ruff](https://docs.astral.sh/ruff/), [Pytest](https://docs.pytest.org/),
  and [Hypothesis](https://hypothesis.readthedocs.io/).

### Practice Accelerators

- Run `import this` in the REPL weekly to keep the philosophy fresh.
- Use `black --diff .` and `ruff --explain <code>` to understand the reasoning behind formatting or linting nudges.
- Rebuild the TODO app layers from scratch (datamodel, stats functions, CLI) whenever you join a new team—twenty focused minutes reinforces idioms better than reading another blog post.
- Keep a `scripts/experiments/` directory for short notebooks or throwaway spikes; it reduces pressure to over-engineer early drafts.

### Recovery Moves

- **Environment drift:** if commands suddenly hit the wrong Python, re-run `pyenv local <version>` and `poetry env info` to confirm you are inside `.venv`. Consider `direnv` to automate activation.
- **System package gaps:** SSL, bz2, or sqlite import errors usually mean missing OS libraries—install the relevant `lib*-dev` packages (or Homebrew formulas) and reinstall the Python version via `pyenv`.
- **Mutable defaults:** avoid `def add_task(task, labels=set())`; default to `None` and instantiate inside the function.
- **Corrupt task data:** keep a `poetry run python -m todo_app repair tasks.json` helper (or similar) so the team can fix JSON state without guesswork.

### Editor and Tooling Profiles

- **VS Code:** enable Python, Pylance, Ruff, Black, and Mypy extensions; set `"python.defaultInterpreterPath": ".venv/bin/python"` and wire format-on-save to Black.
- **JetBrains (PyCharm / IDEA):** add the Poetry interpreter, enable “on save” actions for Black/Ruff, and configure file watchers for `mypy` if you want instant feedback.
- **Terminal aliases:** the quickstart’s `fmt`, `lint`, `test`, and `typecheck` keep CLIs symmetrical across IDEs; add `sync` for `poetry run todo sync` if your workflow depends on remote boards.
