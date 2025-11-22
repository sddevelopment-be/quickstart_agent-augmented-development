# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

> Scope / plan for upcoming release

### Added

- Modular agent directive system with 13 core directives (001-013)
- Comprehensive agent profiles for specialized roles (architect, curator, developer, writer, etc.)
- Directive manifest with enhanced metadata (directive_version, status fields)
- Validation tooling (`validation/validate_directives.sh`) for directive integrity checks
- Agent bootstrapping and rehydration protocols
- Command aliases system for efficient agent interaction
- Issue templates for epics, features, tasks, bugs, and agent creation
- Work collaboration space structure (`work/collaboration/`, `work/curator/`)
- Documentation templates for architecture (ADR, design vision, technical design, roadmap)
- Documentation templates for structure mapping (REPO_MAP, SURFACES, WORKFLOWS, CONTEXT_LINKS)
- LEX (Lexical Excellence) templates for style consistency
- OpenCode configuration mapping and validation scripts
- Portability enhancement documentation
- Audience documentation for automation agents (`docs/audience/automation_agent.md`)
- Architecture documentation directory (`docs/architecture/`)
  - ADR-001: Modular Agent Directive System
  - ADR-001: Portability Enhancement – OpenCode Specification (standardized agent configuration using OpenCode JSON for portability, validation, and CI/CD)
  - Architectural Vision document
  - Agent Specialization Patterns guide
  - Directive System Architecture technical documentation
  - Architecture README with navigation and guidelines
- Directive 013: Tooling Setup & Fallbacks (install commands, version requirements, fallback strategies)
- Redundancy rationale documentation in directive 012
- Meta-version tracking in `AGENTS.md` (core_version, directive_set_version)

### Changed

- Refactored `AGENTS.md` to lean core specification (12 sections) with external directive references
- Externalized detailed operational guidance into modular directives
- Improved token efficiency through lazy directive loading
- Enhanced agent initialization protocol with validation checkpoints
- Standardized integrity markers (✅ ⚠️ ❗️) across all agent communications

### Removed

> Deprecated features and functionalities

### Fixed

> Bug fixes and issues resolved

### Security

> Vulnerabilities addressed and security improvements