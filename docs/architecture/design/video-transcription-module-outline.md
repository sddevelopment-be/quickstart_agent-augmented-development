# Video Transcription Pipeline - Module Outline

**Version:** 1.0.0  
**Date:** 2025-11-25  
**Status:** Design Proposal  
**Related Documents:**
- [Architectural Analysis](../synthesis/video-transcription-pipeline-analysis.md)
- [ADR-015: Video Transcription Pipeline Integration](../adrs/ADR-015-video-transcription-pipeline-integration.md)
- [Ideation Document](../../ideation/2025-11-25-video-transcription-documentation-pipeline.md)

---

## Purpose

This document outlines the module structure for the video transcription pipeline, defining file organization, component boundaries, and integration points with the existing agent-augmented development framework.

---

## Module Structure

### Directory Layout

```
video-transcription-pipeline/
│
├── README.md                          # Module overview, quickstart, architecture summary
│
├── agents/                            # Agent profile definitions
│   ├── recorder.agent.md              # Recorder agent: video ingestion, metadata extraction
│   ├── transcriber.agent.md           # Transcriber agent: speech-to-text conversion
│   ├── analyzer.agent.md              # Analyzer agent: content structuring, extraction
│   ├── writer-transcription.agent.md  # Writer specialization for transcription outputs
│   └── reviewer-routing.md            # Review agent routing logic (Architect vs. Curator)
│
├── directives/                        # Pipeline-specific directives
│   ├── 016_video_transcription_workflow.md   # Core pipeline workflow and standards
│   ├── 017_privacy_and_data_handling.md      # Privacy policies, content classification
│   └── manifest.json                  # Directive manifest with metadata
│
├── templates/                         # Task and artifact templates
│   ├── task-video-ingestion.yaml     # Recorder agent task template
│   ├── task-transcription.yaml       # Transcriber agent task template
│   ├── task-analysis.yaml            # Analyzer agent task template
│   ├── task-generation.yaml          # Writer agent task template
│   ├── task-review.yaml              # Reviewer agent task template
│   ├── metadata-video.json           # Video metadata schema
│   ├── structured-outline.md         # Structured content outline format
│   └── traceability-block.md         # Standard traceability markdown block
│
├── config/                            # Configuration files
│   ├── transcription-services.yaml   # Service configuration (Whisper, AssemblyAI, etc.)
│   ├── quality-thresholds.yaml       # Confidence thresholds, validation rules
│   ├── privacy-policy.yaml           # Content sensitivity classification and handling
│   └── storage-paths.yaml            # File storage locations and retention policies
│
├── scripts/                           # Automation scripts
│   ├── ingest-video.sh               # Manual video ingestion helper
│   ├── setup-whisper.sh              # Whisper installation and configuration
│   ├── run-pipeline.sh               # End-to-end pipeline orchestration
│   ├── validate-output.sh            # Quality validation checks
│   └── cleanup-retention.sh          # Automated retention policy enforcement
│
├── docs/                              # Pipeline-specific documentation
│   ├── user-guide/
│   │   ├── quickstart.md             # Getting started guide
│   │   ├── recording-best-practices.md  # How to record for best transcription
│   │   └── troubleshooting.md        # Common issues and solutions
│   ├── architecture/
│   │   ├── agent-interaction-flow.md # Detailed agent handoff sequences
│   │   └── service-selection-guide.md # When to use Whisper vs. API services
│   └── examples/
│       ├── example-task-ingestion.yaml
│       ├── example-transcript-raw.txt
│       ├── example-structured-outline.md
│       └── example-generated-adr.md
│
└── tests/                             # Test fixtures and validation
    ├── fixtures/
    │   ├── sample-meeting-5min.mp4   # Short test video
    │   ├── sample-transcript.txt     # Expected transcript output
    │   └── sample-metadata.json      # Expected metadata
    └── validation/
        ├── validate-transcription.py # Transcription accuracy checker
        └── validate-analysis.py      # Analysis quality checker
```

---

## Integration with Existing Framework

### File Locations in Repository

The module components integrate with the existing repository structure:

```
repository-root/
│
├── .github/
│   └── agents/
│       ├── recorder.agent.md          # ← Add from module
│       ├── transcriber.agent.md       # ← Add from module
│       ├── analyzer.agent.md          # ← Add from module (or extend existing)
│       └── directives/
│           ├── 016_video_transcription_workflow.md  # ← Add from module
│           └── 017_privacy_and_data_handling.md     # ← Add from module
│
├── work/                              # Existing: task coordination
│   ├── inbox/                         # Pipeline tasks start here
│   ├── active/                        # Agents pick up tasks
│   └── completed/                     # Finished pipelines
│
├── recordings/                        # ← NEW: Source video storage
│   ├── 2025-11-25-arch-meeting.mp4
│   └── metadata/
│       └── 2025-11-25-arch-meeting.json
│
├── transcripts/                       # ← NEW: Transcript storage
│   ├── raw/                           # Raw timestamped transcripts
│   │   └── 2025-11-25-arch-meeting.txt
│   └── processed/                     # Structured outlines
│       └── 2025-11-25-arch-meeting-structured.md
│
├── docs/
│   ├── architecture/
│   │   ├── adrs/
│   │   │   └── ADR-015-*.md          # ← Generated from pipeline
│   │   └── patterns/
│   │       └── *.md                   # ← Generated from pipeline
│   ├── ideation/
│   │   └── *.md                       # ← Generated from brainstorming sessions
│   └── user-guide/
│       └── *.md                        # ← Generated from demo videos
│
└── config/                            # ← NEW: Pipeline configuration
    └── video-transcription/
        ├── transcription-services.yaml
        ├── quality-thresholds.yaml
        ├── privacy-policy.yaml
        └── storage-paths.yaml
```

### Configuration Strategy

**Approach:** Configurations live in `config/video-transcription/` to avoid cluttering root directory.

**Rationale:** 
- Keeps pipeline-specific settings isolated
- Allows per-environment overrides (dev/staging/production)
- Aligns with existing config patterns in repository

---

## Component Descriptions

### 1. Agent Profiles

#### `agents/recorder.agent.md`
- **Purpose:** Video ingestion specialist
- **Responsibilities:** Upload handling, metadata extraction, unique ID generation, initial task creation
- **Directives Loaded:** 003, 008, 012
- **Input:** Raw video file + manual metadata (title, participants)
- **Output:** Registered video asset + task YAML for Transcriber

#### `agents/transcriber.agent.md`
- **Purpose:** Speech-to-text conversion specialist
- **Responsibilities:** Service interface (Whisper/API), timestamp generation, speaker diarization, quality validation
- **Directives Loaded:** 001, 009, 011, 012, 016
- **Input:** Video file path + transcription config
- **Output:** Raw transcript with timestamps + quality report

#### `agents/analyzer.agent.md`
- **Purpose:** Content structuring and extraction specialist
- **Responsibilities:** Segmentation, topic extraction, decision identification, content type classification
- **Directives Loaded:** 004, 009, 012, 016
- **Input:** Raw transcript + context (topic, participants)
- **Output:** Structured outline + content type + entity extractions

**Note:** This may extend an existing `analyzer.agent.md` if one exists, adding video-specific capabilities as a specialization.

#### `agents/writer-transcription.agent.md`
- **Purpose:** Documentation generation specialist (transcription focus)
- **Responsibilities:** Template application, timestamp reference insertion, cross-linking, formatting
- **Directives Loaded:** 004, 008, 012, 013, 016
- **Input:** Structured outline + content type
- **Output:** Draft documentation artifacts (ADRs, notes, tutorials)

**Note:** This is a specialization of a general Writer agent, focusing on video-sourced content.

#### `agents/reviewer-routing.md`
- **Purpose:** Review routing logic (not a full agent, but routing rules)
- **Responsibilities:** Determine appropriate reviewer based on content type (Architect for ADRs, Curator for consistency)
- **Used By:** Coordinator agent or Writer agent for next-agent assignment

---

### 2. Directives

#### `directives/016_video_transcription_workflow.md`
- **Purpose:** Define standard workflow for video → documentation pipeline
- **Contents:**
  - Pipeline stages and responsibilities
  - Agent handoff protocols
  - Quality gates (confidence thresholds)
  - Artifact naming conventions
  - Traceability requirements
  - Error escalation rules

#### `directives/017_privacy_and_data_handling.md`
- **Purpose:** Privacy policies and data handling rules
- **Contents:**
  - Content sensitivity classification (public/internal/confidential/sensitive)
  - Service selection rules (local vs. API)
  - Access control requirements
  - Retention policies (videos, transcripts, docs)
  - Anonymization guidelines
  - Compliance considerations

---

### 3. Templates

#### Task Templates
Each stage has a YAML task template defining:
- Task ID format
- Agent assignment
- Input/output artifact paths
- Description format
- Metadata fields
- Handoff notes structure

**Example: `templates/task-transcription.yaml`**
```yaml
# Template for transcription task
id: YYYY-MM-DDTHHMM-transcribe-<topic-slug>
agent: transcriber
status: new
title: "Transcribe <topic> recording"
artifacts:
  input:
    - recordings/<video-id>.mp4
    - recordings/metadata/<video-id>.json
  output:
    - transcripts/raw/<video-id>.txt
    - transcripts/raw/<video-id>-quality-report.json
description: |
  Process <topic> recording through transcription service.
  Expected duration: <duration> minutes. Target confidence: >90%.
guidelines:
  - 016_video_transcription_workflow
  - 017_privacy_and_data_handling
next_agent: analyzer
metadata:
  video_duration_seconds: <duration>
  participant_count: <count>
  recording_date: "YYYY-MM-DD"
  topic: "<topic>"
  sensitivity: "<public|internal|confidential|sensitive>"
```

#### Artifact Templates

**`templates/structured-outline.md`**: Format for Analyzer output
- Section structure (Topics / Decisions / Action Items / Technical Terms)
- Timestamp reference syntax
- Entity extraction format (JSON-in-markdown or YAML frontmatter)

**`templates/traceability-block.md`**: Standard block for all generated docs
```markdown
<!-- Source Traceability -->
**Source:** [<Title> - YYYY-MM-DD](../../recordings/<video-id>.mp4)  
**Transcript:** [Full transcript](../../transcripts/processed/<video-id>-structured.md)  
**Processing Date:** YYYY-MM-DD  
**Pipeline Version:** 1.0.0

**Key Discussion Segments:**
- [<Segment 1 description>](../../recordings/<video-id>.mp4#t=<timestamp>)
- [<Segment 2 description>](../../recordings/<video-id>.mp4#t=<timestamp>)
```

---

### 4. Configuration Files

#### `config/transcription-services.yaml`
Defines available transcription services and selection logic:
```yaml
services:
  whisper:
    type: local
    model: base  # Options: tiny, base, small, medium, large
    language: auto
    device: cpu  # Options: cpu, cuda
    path: /usr/local/bin/whisper
  
  assemblyai:
    type: api
    api_key_env: ASSEMBLYAI_API_KEY
    endpoint: https://api.assemblyai.com/v2/transcript
    features:
      speaker_labels: true
      auto_highlights: true
      content_safety: false
    language: en

default_service: whisper

# Service selection based on content sensitivity
sensitivity_mapping:
  public: assemblyai
  internal: whisper
  confidential: whisper
  sensitive: whisper
```

#### `config/quality-thresholds.yaml`
Defines quality gates and validation rules:
```yaml
transcription:
  min_confidence: 0.85           # Below this: reject or flag for manual review
  flag_below: 0.90               # Below this: warn reviewer
  review_required_below: 0.85    # Below this: mandatory human review

analysis:
  min_decision_confidence: 0.80
  require_human_review:
    - architecture_decisions      # Always require Architect review
    - security_policies
    - compliance_topics

generation:
  template_match_threshold: 0.90
  require_architect_review:
    - ADR
    - pattern_document
  require_curator_review:
    - glossary_update
    - meeting_notes
```

#### `config/privacy-policy.yaml`
Maps content sensitivity to handling requirements:
```yaml
content_classification:
  public:
    transcription_service: any
    storage: cloud_or_local
    retention_days: permanent
    access: public
  
  internal:
    transcription_service: any
    storage: local_preferred
    retention_days: 365
    access: team
  
  confidential:
    transcription_service: local_only
    storage: encrypted_local
    retention_days: 180
    access: restricted
  
  sensitive:
    transcription_service: local_only
    storage: encrypted_local
    retention_days: per_compliance_policy
    access: security_team_only

anonymization:
  enabled: false
  apply_to: [confidential, sensitive]
  method: speaker_labels  # Options: speaker_labels, role_based, aggregate
```

#### `config/storage-paths.yaml`
Defines storage locations and retention:
```yaml
paths:
  recordings: recordings/
  recordings_metadata: recordings/metadata/
  transcripts_raw: transcripts/raw/
  transcripts_processed: transcripts/processed/
  docs_adrs: docs/architecture/adrs/
  docs_patterns: docs/architecture/patterns/
  docs_ideation: docs/ideation/
  docs_meetings: work/meetings/

retention:
  recordings_default_days: 90
  transcripts_raw_days: 180
  transcripts_processed: permanent
  published_docs: permanent

cleanup:
  enabled: true
  run_schedule: "0 2 * * 0"  # Weekly on Sunday at 2 AM
  dry_run: true              # Set to false to actually delete files
```

---

### 5. Scripts

#### `scripts/ingest-video.sh`
**Purpose:** Manual video ingestion helper for users  
**Usage:** `./ingest-video.sh <video-file> <title> <topic> <participants> <sensitivity>`  
**Actions:**
- Copy video to `recordings/`
- Generate unique ID (timestamp-based)
- Extract metadata (duration, format)
- Create metadata JSON file
- Create initial task YAML in `work/inbox/`
- Output task ID for tracking

#### `scripts/setup-whisper.sh`
**Purpose:** Install and configure Whisper transcription service  
**Usage:** `./setup-whisper.sh [model]`  
**Actions:**
- Check for Python 3.8+
- Install Whisper via pip or from source
- Download specified model (default: base)
- Test transcription with sample audio
- Output configuration for `transcription-services.yaml`

#### `scripts/run-pipeline.sh`
**Purpose:** End-to-end pipeline orchestration (for testing or manual runs)  
**Usage:** `./run-pipeline.sh <task-id>`  
**Actions:**
- Validate task exists in `work/inbox/`
- Execute Recorder → Transcriber → Analyzer → Writer → Reviewer sequence
- Log progress and errors
- Report final status (success / needs review / failed)

#### `scripts/validate-output.sh`
**Purpose:** Quality validation for generated artifacts  
**Usage:** `./validate-output.sh <doc-path>`  
**Actions:**
- Check traceability block exists
- Validate timestamp links are well-formed
- Check cross-references resolve
- Verify template structure (ADR, meeting notes, etc.)
- Report validation results

#### `scripts/cleanup-retention.sh`
**Purpose:** Enforce retention policies (delete old videos/transcripts)  
**Usage:** `./cleanup-retention.sh [--dry-run]`  
**Actions:**
- Read retention policies from `storage-paths.yaml`
- Identify videos older than retention period
- Delete (or report for dry-run) expired videos and raw transcripts
- Preserve processed transcripts and published docs
- Log deletions for audit trail

---

### 6. Documentation

#### User Guide

**`docs/user-guide/quickstart.md`**
- How to record a meeting for transcription
- How to submit a video for processing
- How to monitor pipeline progress
- How to review and approve generated docs

**`docs/user-guide/recording-best-practices.md`**
- Audio quality tips (microphones, room acoustics)
- Speaking practices for better transcription (enunciation, avoid crosstalk)
- Metadata preparation (what to document before recording)
- Privacy considerations (what not to record)

**`docs/user-guide/troubleshooting.md`**
- Low transcription confidence (audio quality issues, accents, jargon)
- Missing metadata (how to provide manually)
- Incorrect content type classification (how to override)
- Service failures (Whisper errors, API timeouts)

#### Architecture Documentation

**`docs/architecture/agent-interaction-flow.md`**
- Detailed sequence diagrams for each pipeline stage
- Error handling and escalation paths
- Parallel processing opportunities (future enhancement)
- Metrics and monitoring integration

**`docs/architecture/service-selection-guide.md`**
- When to use Whisper vs. API services
- Cost-benefit analysis
- Privacy trade-offs
- Performance comparisons (speed, accuracy)

#### Examples

Provide complete example artifacts for each pipeline stage:
- `examples/example-task-ingestion.yaml`: Recorder output
- `examples/example-transcript-raw.txt`: Transcriber output (with timestamps)
- `examples/example-structured-outline.md`: Analyzer output
- `examples/example-generated-adr.md`: Writer output (ADR with traceability)

---

### 7. Tests and Validation

#### Test Fixtures

**`tests/fixtures/sample-meeting-5min.mp4`**
- Short sample video for testing (architecture discussion)
- Duration: 5 minutes
- Participants: 3 speakers
- Contains: 1 decision, 2 action items, 3 technical terms

**Expected Outputs:**
- `sample-transcript.txt`: Known-good transcript for validation
- `sample-metadata.json`: Expected metadata extraction
- `sample-structured-outline.md`: Expected analysis output

#### Validation Scripts

**`tests/validation/validate-transcription.py`**
- Compares generated transcript to fixture transcript
- Calculates word error rate (WER)
- Reports confidence score alignment
- Checks timestamp format

**`tests/validation/validate-analysis.py`**
- Checks that all decisions from fixture are extracted
- Validates action item detection
- Verifies technical term cross-referencing
- Confirms content type classification

---

## Deployment Checklist

### Prerequisites
- [ ] Python 3.8+ installed
- [ ] Whisper dependencies installed (via `setup-whisper.sh`)
- [ ] Repository access (write permissions to `recordings/`, `transcripts/`, `docs/`)
- [ ] (Optional) AssemblyAI API key for non-sensitive content

### Installation Steps
1. [ ] Clone/pull repository with video transcription module
2. [ ] Run `scripts/setup-whisper.sh base` to install Whisper
3. [ ] Configure `config/transcription-services.yaml` (set API keys if using API services)
4. [ ] Configure `config/privacy-policy.yaml` (adjust sensitivity mappings to team policy)
5. [ ] Configure `config/storage-paths.yaml` (set retention policies)
6. [ ] Test with sample video: `scripts/ingest-video.sh tests/fixtures/sample-meeting-5min.mp4 ...`
7. [ ] Run pipeline: `scripts/run-pipeline.sh <task-id>`
8. [ ] Validate output: `scripts/validate-output.sh docs/architecture/adrs/ADR-XXX-*.md`
9. [ ] Review user guide: `docs/user-guide/quickstart.md`
10. [ ] Train team on workflow

### Validation
- [ ] Sample video transcribes successfully (≥85% confidence)
- [ ] Structured outline generated with expected sections
- [ ] ADR draft generated with traceability block
- [ ] Timestamp links are functional
- [ ] Retention cleanup script runs without errors (dry-run mode)

---

## Maintenance and Evolution

### Version Management
- Module version follows semantic versioning (MAJOR.MINOR.PATCH)
- Breaking changes (e.g., new agent required, config schema change) → MAJOR
- New features (e.g., additional transcription service) → MINOR
- Bug fixes, documentation improvements → PATCH

### Future Enhancements
- Real-time transcription (live meeting support)
- Multi-language support (auto-translation)
- Visual content extraction (diagrams from screen shares)
- Sentiment analysis (detect consensus, uncertainty)
- Automatic slide extraction from presentation videos
- Voice signature identification (auto-map speakers across meetings)

### Deprecation Policy
- If a component (e.g., transcription service integration) is deprecated, provide 2-version migration path
- Update directives to mark deprecated practices
- Provide migration scripts where applicable

---

## Related Documents

- **Architectural Analysis:** [Video Transcription Pipeline Analysis](../synthesis/video-transcription-pipeline-analysis.md)
- **ADR:** [ADR-015: Video Transcription Pipeline Integration](../adrs/ADR-015-video-transcription-pipeline-integration.md)
- **Ideation:** [Video Transcription Documentation Pipeline](../../ideation/2025-11-25-video-transcription-documentation-pipeline.md)
- **Diagram:** [Video Transcription Workflow PlantUML](../diagrams/transcript_usage.puml)

---

**Document Status:** Design proposal - ready for team review  
**Next Steps:** Review module structure, approve ADR-015, begin Phase 1 implementation (PoC)
