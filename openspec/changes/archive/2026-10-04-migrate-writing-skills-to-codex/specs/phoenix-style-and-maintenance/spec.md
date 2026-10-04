## ADDED Requirements

### Requirement: Phoenix style boundaries

The Phoenix skill SHALL activate for an explicit Phoenix voice request or continuation of an established Phoenix-styled artifact. It SHALL separate voice from artifact workflow, preserve evidence and author position, and follow explicit language, length, humor and format requests over defaults.

#### Scenario: Appropriate style request

- **WHEN** the user requests a Phoenix-style explanation of caching for beginners
- **THEN** the agent explains mechanism through concrete reader concerns and a bounded analogy without mandatory chapter or image quotas

#### Scenario: Inappropriate and conflicting requests

- **WHEN** the user requests code-only repair or formal minutes without asking for Phoenix voice
- **THEN** the skill does not impose that voice
- **AND** an explicit English, no-humor, 80-word Phoenix request retains those constraints

### Requirement: Canonical source and recoverable migration

The active skill SHALL reside in repo skills with resolving agent entry symlinks. The Mac original SHALL have a recoverable backup before replacement by a compatibility symlink. Legacy reference and validator callers SHALL retain resolving paths with documented historical semantics.

#### Scenario: Mac and repo entrypoints

- **WHEN** an agent opens the repo or existing global Phoenix entrypoint after migration
- **THEN** all active SKILL.md paths resolve to the canonical repo file
- **AND** original files are recoverable from a hash-verified backup

### Requirement: Source-backed Codex maintenance

Writing maintenance instructions SHALL use available host tools and actual CLI contracts, maintain source provenance, distinguish OpenAI principles from repo choices, and record executed validation separately from unexecuted model evaluations.

#### Scenario: Reviewing migration evidence

- **WHEN** a maintainer reviews this migration
- **THEN** evidence identifies the Astra article, quill-n-grill and writing-for-agents with necessary references and preserves their limitations
- **AND** GPT-6.1-sol high plus fast is described as a task choice rather than an Astra recommendation
