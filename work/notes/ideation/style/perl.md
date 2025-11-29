+++
title = "Perl Primer"
subtitle = "There's More Than One Way To Do It (TIMTOWTDI)"
aliases = ["perl-primer", "programming-languages/perl"]
author = "Stijn Dejongh"
outputs = ['html', 'rss', 'json']
date = "2025-11-10T04:00:00+00:00"
tags = ["programming", "perl", "primer", "reference", "intermediate"]
summary = """
Perl values expressiveness and pragmatism over rigid orthodoxy. Born as a text-processing powerhouse, it evolved into a full-spectrum language where regular expressions are first-class citizens and "There's More Than One Way To Do It" is a core principle. Perl rewards those who master its idioms with terse, powerful solutions—though readability requires discipline.
"""
image = "primers/perl_logo"
+++

## 1. Language Philosophy

> "There's More Than One Way To Do It" — *The Perl Motto*

Perl values expressiveness and pragmatism over rigid orthodoxy. Larry Wall designed it to feel natural—borrowing from shell scripting, C, awk, and sed while adding its own distinctive personality. The language celebrates linguistic flexibility, treating programming as a form of expression where style and context matter as much as correctness.

- **TIMTOWTDI (There's More Than One Way To Do It).** Perl trusts programmers to choose the approach that fits their problem best, whether that's procedural, object-oriented, or functional. This flexibility is a feature, not a bug.
- **Text processing DNA.** Regular expressions are woven into the syntax, making pattern matching and text manipulation feel native rather than bolted on. If your domain involves logs, templates, or unstructured data, Perl speaks your language.
- **Practical extraction and reporting.** The name itself—Practical Extraction and Report Language—signals Perl's roots in getting real work done: parsing files, generating reports, automating systems administration tasks.
- **Contextual evaluation.** Variables change behaviour based on context (scalar vs. list), and operators adapt their meaning based on what's around them. This makes Perl dense and powerful but requires careful attention to avoid surprises.
- **"Make easy things easy and hard things possible."** Perl won't force ceremony on simple tasks, but it provides the power and flexibility to tackle complex problems when needed.

Treat Perl as a Swiss Army knife for text processing, system automation, and rapid prototyping. It shines brightest when you need to wrangle data, automate workflows, or build tools that need to adapt to messy real-world inputs.

## 2. Syntax and Naming Conventions

Perl's syntax is famously dense and sigil-heavy. Variables wear prefixes that signal their type, and the language leans on punctuation to compress meaning. Community conventions keep code navigable despite this flexibility.

| Element              | Convention                     | Example                                    |
|----------------------|--------------------------------|--------------------------------------------|
| Scalar variables     | `$snake_case`                  | `$pending_count`, `$task_title`            |
| Array variables      | `@snake_case`                  | `@tasks`, `@completed_items`               |
| Hash variables       | `%snake_case`                  | `%task_by_id`, `%user_preferences`         |
| Subroutines          | `snake_case`                   | `mark_complete()`, `filter_overdue()`      |
| Package/Module names | `CamelCase::Hierarchy`         | `TaskManager`, `TaskManager::Repository`   |
| Constants            | `ALL_CAPS` or `CamelCase`      | `MAX_TASKS`, `DefaultPriority`             |
| Private subroutines  | `_leading_underscore`          | `_validate_state()`, `_load_config()`      |
| Filehandles          | `UPPERCASE` (legacy)           | `TASK_FILE`, `LOG`                         |

**Sigils matter:** `$task` is a scalar, `@task` is an array, `%task` is a hash. The same base name can represent different data structures—context determines which you mean.

Style enforcement tools like [Perl::Tidy](https://metacpan.org/pod/Perl::Tidy) format code consistently, while [Perl::Critic](https://metacpan.org/pod/Perl::Critic) catches common antipatterns. Use `strict` and `warnings` pragmas in every script to catch errors early:

```perl
use strict;
use warnings;
use v5.30;  # Enable modern Perl features
```

Modern Perl (5.10+) adds features like `say`, postfix dereferencing, and signatures. Enable them explicitly with `use feature` or a version declaration.

## 3. Version and Dependency Management

Perl ships with most Unix-like systems, but system Perl should stay untouched. Modern workflows use version managers and isolated dependency management to keep projects reproducible.

| Tool        | Role                                          | Why teams use it                                  |
|-------------|-----------------------------------------------|---------------------------------------------------|
| `perlbrew`  | Install and switch between Perl versions      | Keeps multiple Perl runtimes side by side         |
| `plenv`     | Alternative version manager (pyenv-style)     | Lightweight, shell-based version switching        |
| `cpanm`     | Fast, modern CPAN client                      | Install modules without configuration ceremony    |
| `Carton`    | Dependency manager with lockfile support      | Pins exact versions for reproducible builds       |
| `local::lib`| Isolate module installations to local dir     | Alternative to system-wide installations          |

Typical workflow:

```bash
# Install perlbrew
curl -L https://install.perlbrew.pl | bash
perlbrew init

# Install and switch to modern Perl
perlbrew install perl-5.38.0
perlbrew switch perl-5.38.0

# Install cpanm
perlbrew install-cpanm

# Set up project dependencies with Carton
cpanm Carton
carton install  # Reads cpanfile, writes cpanfile.snapshot
```

The `cpanfile` format specifies dependencies:

```perl
requires 'Moose', '>= 2.2200';
requires 'DateTime', '== 1.59';
requires 'JSON::MaybeXS';

on 'test' => sub {
    requires 'Test::More', '>= 1.302';
    requires 'Test::Exception';
};
```

`cpanfile.snapshot` locks exact versions for reproducibility. Legacy projects may use `Makefile.PL` or `Build.PL` with traditional CPAN tooling—expect to encounter both patterns.

## 4. Build and Packaging Tooling

Perl's packaging ecosystem evolved organically, so you'll encounter multiple build systems depending on project age. Modern projects lean toward `Dist::Zilla` or `Minilla` for streamlined releases, while legacy code uses `ExtUtils::MakeMaker` or `Module::Build`.

| Tool                   | Role                                  | Notes                                              |
|------------------------|---------------------------------------|----------------------------------------------------|
| `ExtUtils::MakeMaker`  | Classic build system (Makefile.PL)    | Still ubiquitous, works everywhere                 |
| `Module::Build`        | Pure-Perl alternative (Build.PL)      | Cleaner than MakeMaker, less configuration needed  |
| `Dist::Zilla`          | Author-time distribution builder      | Powerful plugin system, steep learning curve       |
| `Minilla`              | Lightweight alternative to Dist::Zilla| Sensible defaults, git-aware, less ceremony        |
| `CPAN`/`cpanm`         | Module installer/client               | Frontend for fetching and installing modules       |

Reference layout (traditional):

```
project/
├── lib/
│   └── TaskManager.pm
│   └── TaskManager/
│       ├── Task.pm
│       └── Repository.pm
├── t/
│   ├── 00-load.t
│   ├── 01-task.t
│   └── 02-repository.t
├── bin/
│   └── todo
├── Makefile.PL         # or Build.PL
├── cpanfile
├── cpanfile.snapshot
├── MANIFEST
└── README.md
```

Standard workflow:

```bash
# Classic MakeMaker
perl Makefile.PL
make
make test
make install

# Or with Module::Build
perl Build.PL
./Build
./Build test
./Build install

# Modern approach with Carton
carton install
carton exec prove -l t/
```

CPAN publishing is typically done via PAUSE (Perl Authors Upload Server) using `cpan-upload` or via `Dist::Zilla dzil release`.

## 5. Testing Frameworks

Perl has a mature testing culture rooted in the TAP (Test Anything Protocol) standard. The `prove` harness runs tests, and Test::More provides the canonical testing vocabulary. Modern projects may use Test2, the next-generation framework.

- **Testing mindset:** Write tests close to the Perl tradition of "test everything, often." The CPAN ecosystem prizes comprehensive test coverage, and contributors expect test files to accompany every module.

| Tool              | Purpose                               | Why it matters                                     |
|-------------------|---------------------------------------|----------------------------------------------------|
| `Test::More`      | Classic testing framework (TAP)       | De facto standard; simple, widely understood       |
| `Test2::Suite`    | Modern test framework                 | Richer diagnostics, better composability           |
| `Test::Exception` | Test exception throwing               | Verify error conditions cleanly                    |
| `Test::Deep`      | Deep data structure comparison        | Essential for complex hash/array validation        |
| `Devel::Cover`    | Code coverage analysis                | Measure test coverage percentage                   |
| `prove`           | TAP harness (ships with Perl)         | Runs `.t` files, aggregates results                |

Canonical `Test::More` example:

```perl
# t/01-task.t
use strict;
use warnings;
use Test::More tests => 5;
use TaskManager::Task;

my $task = TaskManager::Task->new(
    title => 'Write documentation',
    state => 'todo',
);

ok($task, 'Task object created');
is($task->title, 'Write documentation', 'Title set correctly');
is($task->state, 'todo', 'Initial state is todo');

$task->start;
is($task->state, 'in_progress', 'State transitions to in_progress');

$task->complete;
is($task->state, 'done', 'State transitions to done');
```

Run tests with `prove`:

```bash
prove -l t/              # Run all tests in t/
prove -v t/01-task.t     # Verbose output for one test
prove -lr t/             # Recursive, with lib in @INC
```

Coverage reporting:

```bash
cover -test              # Run tests and generate coverage report
cover -report html       # Create HTML coverage report
```

Modern Perl shops integrate testing into CI pipelines and expect every module to ship with comprehensive `.t` files.

## 6. Programming Idioms

Perl is a multi-paradigm language by design. Object-oriented code organizes long-lived systems, functional approaches keep data transformations clean, and imperative scripts handle automation and orchestration. The same project will mix all three styles.

### 6.1 Object-Oriented Idioms

Perl's native object system is minimal—bless a reference into a package and you have an object. Modern OO in Perl means using [Moose](https://metacpan.org/pod/Moose) or [Moo](https://metacpan.org/pod/Moo) for classes with proper attributes, type constraints, and method modifiers.

- Use **Moose** for full-featured OO with type checking, roles, and meta-programming.
- Use **Moo** for lightweight OO with minimal overhead and faster startup.
- Favor composition via roles (`with 'Role::Name'`) over inheritance.

```perl
package TaskManager::Task;
use Moose;
use DateTime;

has 'title' => (
    is       => 'ro',
    isa      => 'Str',
    required => 1,
);

has 'state' => (
    is      => 'rw',
    isa     => 'Str',
    default => 'todo',
);

has 'created_at' => (
    is      => 'ro',
    isa     => 'DateTime',
    default => sub { DateTime->now },
);

has 'due_at' => (
    is        => 'rw',
    isa       => 'Maybe[DateTime]',
    predicate => 'has_due_date',
);

has 'tags' => (
    is      => 'ro',
    isa     => 'ArrayRef[Str]',
    default => sub { [] },
);

sub start {
    my $self = shift;
    $self->state('in_progress') if $self->state eq 'todo';
}

sub complete {
    my $self = shift;
    $self->state('done') if $self->state eq 'in_progress';
}

sub is_overdue {
    my $self = shift;
    return 0 unless $self->has_due_date;
    return DateTime->compare($self->due_at, DateTime->now) < 0;
}

__PACKAGE__->meta->make_immutable;
1;
```

Moose provides `has` for attribute declaration, automatic accessors, type constraints (`isa`), and builders. The `__PACKAGE__->meta->make_immutable` line optimizes the class at compile time.

### 6.2 Functional Programming Idioms

Perl supports functional programming through first-class functions, closures, and higher-order functions. `map`, `grep`, and `reduce` (from `List::Util`) are the workhorses for transforming data without mutation.

- Prefer `map` and `grep` over explicit loops for transformations and filtering.
- Use anonymous subroutines (`sub { ... }`) for callbacks and closures.
- Lean on `List::Util` (`reduce`, `any`, `all`, `first`) for common patterns.

```perl
package TaskManager::Stats;
use strict;
use warnings;
use List::Util qw(reduce any all first);

sub completion_rate {
    my (@tasks) = @_;
    return 0 unless @tasks;
    
    my $done_count = grep { $_->state eq 'done' } @tasks;
    return $done_count / @tasks;
}

sub overdue_tasks {
    my (@tasks) = @_;
    return grep { $_->is_overdue } @tasks;
}

sub tasks_by_tag {
    my ($tag, @tasks) = @_;
    return grep { any { $_ eq $tag } @{$_->tags} } @tasks;
}

sub urgent_task {
    my (@tasks) = @_;
    return first { $_->has_due_date && $_->is_overdue } @tasks;
}

# Using reduce for aggregation
sub total_tasks_by_state {
    my (@tasks) = @_;
    return reduce {
        $a->{$b->state}++;
        $a;
    } {}, @tasks;
}

1;
```

Functional style keeps business logic pure and easy to test. Combine with closures for partial application:

```perl
sub tag_filter {
    my ($tag) = @_;
    return sub {
        my ($task) = @_;
        return any { $_ eq $tag } @{$task->tags};
    };
}

my $urgent = tag_filter('urgent');
my @urgent_tasks = grep { $urgent->($_) } @tasks;
```

### 6.3 Imperative Programming Idioms

Imperative Perl handles orchestration: file I/O, system administration, CLI tools, and integration scripts. Explicit control flow and side effects make failure points visible.

- Use `open` with three-argument form for safety: `open my $fh, '<', $filename`.
- Leverage `autodie` pragma to convert system call failures into exceptions.
- Store file handles in lexical variables, not barewords.

```perl
package TaskManager::Repository;
use strict;
use warnings;
use autodie;
use JSON::MaybeXS;
use Path::Tiny;

sub load_tasks {
    my ($class, $filepath) = @_;
    
    return [] unless -e $filepath;
    
    my $json = path($filepath)->slurp_utf8;
    my $data = decode_json($json);
    
    return [
        map { TaskManager::Task->new(%$_) } @$data
    ];
}

sub save_tasks {
    my ($class, $filepath, @tasks) = @_;
    
    my @data = map {
        {
            title      => $_->title,
            state      => $_->state,
            created_at => $_->created_at->iso8601,
            due_at     => $_->has_due_date ? $_->due_at->iso8601 : undef,
            tags       => $_->tags,
        }
    } @tasks;
    
    my $json = encode_json(\@data);
    path($filepath)->spew_utf8($json);
}

sub complete_first_task {
    my ($class, $filepath) = @_;
    
    my $tasks = $class->load_tasks($filepath);
    return unless @$tasks;
    
    $tasks->[0]->complete;
    $class->save_tasks($filepath, @$tasks);
}

1;
```

For CLI applications, use [Getopt::Long](https://metacpan.org/pod/Getopt::Long) (core) or modern alternatives like [Getopt::Long::Descriptive](https://metacpan.org/pod/Getopt::Long::Descriptive) or [App::Cmd](https://metacpan.org/pod/App::Cmd):

```perl
#!/usr/bin/env perl
use strict;
use warnings;
use Getopt::Long;
use TaskManager::Repository;

my $task_file = 'tasks.json';
my $action    = 'list';

GetOptions(
    'file=s'   => \$task_file,
    'action=s' => \$action,
) or die "Usage: $0 [--file FILE] [--action list|add|complete]\n";

if ($action eq 'complete') {
    TaskManager::Repository->complete_first_task($task_file);
    say "First task marked as done.";
} elsif ($action eq 'list') {
    my $tasks = TaskManager::Repository->load_tasks($task_file);
    say $_->title for @$tasks;
}
```

### 6.4 Idiom Integration

Structure Perl systems in layers to keep concerns separated:

1. **Domain core (OO + Functional).** Use Moose/Moo for entities with identity and lifecycle. Keep business logic in pure functions (FP) that transform data without side effects.
2. **Application services (OO).** Thin service classes coordinate persistence, external APIs, and stateful operations. Use dependency injection (pass objects to constructors) to keep tests simple.
3. **Orchestration (Imperative).** CLI scripts, cron jobs, and integration adapters handle I/O, configuration, and error recovery. Call domain logic from these layers but don't mix concerns.

This separation keeps logic testable, side effects visible, and architecture approachable for maintainers.

## 7. Workspace Bootstrap

Establish a stable local environment before writing code so every developer can reproduce the same setup.

1. **Install prerequisites.** Ensure you have build tools (`gcc`, `make`), version control (`git`), and system libraries needed by common CPAN modules (SSL, zlib, database drivers). On Ubuntu: `sudo apt install build-essential libssl-dev zlib1g-dev`. On macOS: `xcode-select --install`.
2. **Provision Perl runtime.** Use `perlbrew` (or `plenv`) to install a modern Perl version (e.g., `perlbrew install perl-5.38.0 && perlbrew switch perl-5.38.0`). This keeps system Perl untouched.
3. **Install cpanm.** Run `perlbrew install-cpanm` to get a fast, zero-config CPAN client. This replaces the legacy `cpan` shell.
4. **Set up Carton.** Install globally: `cpanm Carton`. Create a `cpanfile` in your project root listing dependencies. Run `carton install` to generate `cpanfile.snapshot` and populate `local/` with exact module versions.
5. **Lay out automation.** Create a `Makefile` (or shell scripts) with targets like `test`, `cover`, `tidy`, and `critic` that wrap `carton exec prove`, coverage reports, and linting. Keep CI and local dev aligned.
6. **Wire quality gates.** Install `Perl::Tidy` and `Perl::Critic` via `cpanm`. Add a `.perltidyrc` and `.perlcriticrc` to enforce style. Run `perlcritic -5 lib/` to find policy violations. Consider git pre-commit hooks to auto-format and lint.
7. **Scaffold the TODO app.** Organize modules under `lib/`, tests under `t/`, and scripts under `bin/` or `script/`. Store sample data (`tasks.json`) in `examples/` so new developers can exercise the system immediately.

## 8. Quickstart Setup (Unix)

> Minimal, repeatable steps for macOS, Ubuntu, and most Linux distributions.

1. **System dependencies.**
    - Ubuntu:
      ```bash
      sudo apt update
      sudo apt install -y build-essential curl git libssl-dev zlib1g-dev \
          libexpat-dev libdb-dev
      ```
    - macOS (Homebrew):
      ```bash
      xcode-select --install
      brew install curl git openssl
      ```

2. **Install perlbrew.**
   ```bash
   curl -L https://install.perlbrew.pl | bash
   echo 'source ~/perl5/perlbrew/etc/bashrc' >> ~/.bashrc  # or ~/.zshrc
   source ~/.bashrc
   ```

3. **Install a modern Perl.**
   ```bash
   perlbrew install perl-5.38.0
   perlbrew switch perl-5.38.0
   perlbrew install-cpanm
   ```

4. **Verify installation.**
   ```bash
   perl -v              # Should show 5.38.0
   which cpanm          # Should be in perlbrew path
   ```

5. **Install Carton.**
   ```bash
   cpanm Carton
   ```

6. **Create a project scaffold.**
   ```bash
   mkdir todo-app && cd todo-app
   mkdir -p lib/TaskManager t bin examples
   
   # Create cpanfile
   cat > cpanfile <<'EOF'
   requires 'Moose', '>= 2.2200';
   requires 'DateTime';
   requires 'JSON::MaybeXS';
   requires 'Path::Tiny';
   requires 'List::Util';
   
   on 'test' => sub {
       requires 'Test::More', '>= 1.302';
       requires 'Test::Exception';
   };
   EOF
   
   carton install
   ```

7. **Install quality tools.**
   ```bash
   cpanm Perl::Tidy Perl::Critic Devel::Cover
   ```

8. **Verify tooling.**
   ```bash
   carton exec perl -v
   carton exec prove --version
   perltidy --version
   perlcritic --version
   ```

9. **Optional: IDE setup.** Install Perl plugins for VS Code (Perl, Perl Navigator) or use vim/emacs with LSP support (`Perl::LanguageServer`). Configure to use the perlbrew Perl and respect `local/` for module paths.

10. **Convenience aliases (optional).**
    ```bash
    alias prove-local="carton exec prove -lr t/"
    alias tidy="perltidy -b -bext='/' lib/**/*.pm t/*.t"
    alias critic="perlcritic --stern lib/"
    alias cover="cover -test -report html"
    ```

## 9. First-Time Verification Checklist

Run these commands once the project scaffold is in place to ensure everything works end-to-end:

| Check               | Command                                       | Expected                                  |
|---------------------|-----------------------------------------------|-------------------------------------------|
| Perl runtime        | `perl -v`                                     | 5.38.x (from perlbrew)                    |
| Module installer    | `cpanm --version`                             | Displays version                          |
| Carton              | `carton -v`                                   | Displays Carton version                   |
| Dependency install  | `carton install`                              | Resolves and installs all deps            |
| Tests               | `carton exec prove -l t/`                     | All tests pass (TAP output)               |
| Code coverage       | `cover -test`                                 | Generates coverage report                 |
| Tidy check          | `perltidy --check-only lib/**/*.pm`           | No changes needed or lists files          |
| Critic check        | `perlcritic --stern lib/`                     | No violations (or actionable warnings)    |
| Smoke test script   | `carton exec perl bin/todo --help`            | Usage info displayed                      |

**Troubleshooting notes**

- If `perlbrew` commands aren't found, verify the init script is sourced in your shell rc file (`.bashrc`, `.zshrc`).
- For missing XS modules (SSL, DB_File), install the corresponding system development packages (`libssl-dev`, etc.) and reinstall the module via `cpanm --reinstall`.
- When `prove` can't find modules, ensure you're using `carton exec` or add `-I local/lib/perl5` to `@INC`.
- If Perl::Critic complains about policies you don't care about, add exclusions to `.perlcriticrc` or lower severity with `--gentle`.

## 10. Appendix

### Core References

- [Perl documentation](https://perldoc.perl.org/) — official language reference and standard library docs.
- [Modern Perl](http://modernperlbooks.com/books/modern_perl_2016/) — free book covering contemporary Perl practices.
- [MetaCPAN](https://metacpan.org/) — search and browse CPAN modules with documentation and examples.
- Tooling: [perlbrew](https://perlbrew.pl/), [cpanm](https://metacpan.org/pod/App::cpanminus), [Carton](https://metacpan.org/pod/Carton), [Moose](https://metacpan.org/pod/Moose), [Test::More](https://metacpan.org/pod/Test::More).

### Practice Accelerators

- Read `perldoc perlstyle` and `perldoc perlmod` to internalize community idioms and module structure.
- Run `perlcritic --verbose 8 lib/YourModule.pm` to see detailed explanations for every policy violation—it's a teaching tool as much as a linter.
- Rebuild the TODO app layers from scratch (Moose classes, pure functions, CLI harness) whenever you join a new codebase. Twenty focused minutes reinforces patterns better than reading docs.
- Keep a `scratch/` directory for quick one-liners and experiments. Perl's REPL (`perl -de1` or `reply` via CPAN) is useful for testing snippets interactively.

### Recovery Moves

- **Module won't install:** Check for missing system libraries (SSL, zlib, database headers). Install `build-essential` and relevant `-dev` packages, then retry.
- **Carton lock mismatch:** Delete `cpanfile.snapshot` and `local/`, then rerun `carton install` to rebuild from scratch.
- **Test failures on fresh checkout:** Ensure `carton install` ran successfully and you're using `carton exec` to run tests with the correct module versions.
- **Perlbrew environment issues:** Run `perlbrew list` to confirm which Perl is active, and `perlbrew switch` to change it. Check that PATH includes `~/perl5/perlbrew/bin`.
- **Sigil confusion:** Remember: `$scalar`, `@array`, `%hash`. If you see `$array[0]`, that's a scalar from an array. If you see `$hash{key}`, that's a scalar from a hash. Context is everything.

### Common Pitfalls

- **Forgetting `use strict; use warnings;`** — Always enable these at the top of every script and module. They catch typos, undeclared variables, and other common errors.
- **Bareword filehandles** — Avoid `open FILE, '<', $path`. Use lexical handles: `open my $fh, '<', $path or die`.
- **Not using three-arg open** — `open my $fh, $filename` is dangerous (mode is embedded in filename). Use `open my $fh, '<', $filename`.
- **Mutable default arguments** — `sub add_tag { my ($task, $tags) = @_; $tags ||= []; }` creates a shared default. Use `$tags //= []` or assign inside the sub.
- **Ignoring context** — `my $count = @array;` assigns the array length (scalar context). `my @copy = @array;` copies elements (list context). Operators behave differently depending on context.
- **Overusing punctuation variables** — `$_`, `@_`, `$!`, `$/` are powerful but cryptic. Use them in small scopes; prefer named variables for clarity.

### Modern Perl Features

Perl continues to evolve. Enable recent features with version declarations:

```perl
use v5.36;  # Enables signatures, say, state, unicode_strings, fc, etc.

sub greet($name) {     # Signatures (5.20+, stable in 5.36)
    say "Hello, $name";
}

state $counter = 0;    # Persistent lexical variable
```

Consider these modules for modern codebases:

- **Moose/Moo** — OO with proper attributes and type constraints.
- **Try::Tiny** — Clean exception handling (`try`/`catch`/`finally`).
- **JSON::MaybeXS** — Fast JSON parsing (falls back to pure Perl if XS unavailable).
- **Path::Tiny** — Clean file operations (`path($file)->slurp_utf8`).
- **List::Util** and **List::MoreUtils** — Rich set of list manipulation functions.

### Further Learning

- [Perl Weekly](http://perlweekly.com/) — Curated newsletter of Perl news, articles, and modules.
- [PerlMonks](https://www.perlmonks.org/) — Q&A community for Perl programmers.
- [Perl Maven](https://perlmaven.com/) — Tutorials and screencasts on Perl topics.
- [Task::Kensho](https://metacpan.org/pod/Task::Kensho) — Curated list of recommended CPAN modules by category (web, testing, databases, etc.).
