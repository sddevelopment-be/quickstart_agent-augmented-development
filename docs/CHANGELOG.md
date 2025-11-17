# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

> Scope / plan for upcoming release

### Added

- Modular agent directive system with 12 core directives (001-012)
- Comprehensive agent profiles for specialized roles (architect, curator, developer, writer, etc.)
- Directive manifest with metadata, dependencies, and safety flags
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
- Audience documentation for automation agents

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