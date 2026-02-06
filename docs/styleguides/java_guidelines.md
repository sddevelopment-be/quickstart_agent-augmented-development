---
packaged: true
audiences: [software_engineer, tech_coach, process_architect]
note: Java language conventions and testing expectations.
---

# Java Guidelines

Purpose: Provide a lightweight, repo-agnostic Java guide that emphasizes readability, testing discipline, and long-term maintainability.

## 1. Naming Conventions

| Element    | Convention                                 | Example                                           |
|------------|--------------------------------------------|---------------------------------------------------|
| Classes    | `PascalCase`                               | `TaskManager`, `UserRepository`                   |
| Interfaces | `PascalCase`, often adjectives             | `Runnable`, `Serializable`, `TaskProcessor`       |
| Methods    | `camelCase`, verb-based                    | `getTasks()`, `markCompleted()`, `processQueue()` |
| Variables  | `camelCase`                                | `taskList`, `maxRetries`                          |
| Constants  | `UPPER_SNAKE_CASE`                         | `MAX_CONNECTIONS`, `DEFAULT_TIMEOUT`              |
| Packages   | `lowercase.separated`                      | `com.example.tasks`, `org.patterns.domain`        |
| Enums      | `PascalCase` (type), `UPPER_CASE` (values) | `Status.PENDING`, `Status.COMPLETED`              |

## 2. Formatting and Style

- Prefer consistent formatting via a shared formatter (e.g., Spotless + a repo formatter config).
- Avoid wildcard imports unless a formatter requires them.
- Use explicit braces for control flow (`if`, `for`, `while`) to prevent accidental logic bugs.
- Favor small, focused methods; keep public APIs documented with Javadoc.

## 3. Testing Standards

- Follow the testing styleguides in `docs/styleguides/GENERIC_TESTING.md` and `docs/styleguides/FORMALIZED_CONSTRAINT_TESTING.md`.
- Use JUnit 5 with AssertJ (or equivalent) for readable assertions.
- Prefer contract-focused tests over internal-implementation tests.
- Ensure tests cover negative paths and edge cases, not just the happy path.

## 4. Idioms and Best Practices

### 4.1 Null Handling

- Prefer `Optional` for return values over raw `null`.
- For defaults, use `Optional.ofNullable(x).orElse(default)` rather than nested ternaries.

### 4.2 Exception Assertions

- Assert on the specific exception type the code documents.
- Avoid catching or asserting generic `Exception` unless the API contract requires it.

### 4.3 File I/O

- Always specify character encoding explicitly (UTF-8).
- Use try-with-resources for all stream/file handling.

## 5. Project Structure (Maven Defaults)

```
src/
  main/java/        # Application code
  main/resources/   # Config and resources
  test/java/        # Test code
  test/resources/   # Test fixtures
target/             # Build output (gitignored)
```

## 6. Tooling Expectations

- Maven or Gradle as build tool.
- Formatter + linter integrated into CI if the project uses Java.
- Document the project’s Java version and toolchain in `README.md` or build config.

## 7. Common Pitfalls to Avoid

- Relying on system default encodings.
- Overusing inheritance instead of composition.
- Tight coupling between modules (prefer clear boundaries and interfaces).
- Tests that only validate happy paths.
