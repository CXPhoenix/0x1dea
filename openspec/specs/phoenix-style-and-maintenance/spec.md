# phoenix-style-and-maintenance Specification

## Purpose

TBD - created by archiving change 'migrate-writing-skills-to-codex'. Update Purpose after archive.

## Requirements

### Requirement: Phoenix style boundaries

The Phoenix skill SHALL activate for an explicit Phoenix voice request or continuation of an established Phoenix-styled artifact. It SHALL separate voice from artifact workflow, preserve evidence and author position, and follow explicit language, length, humor and format requests over defaults.

#### Scenario: Appropriate style request

- **WHEN** the user requests a Phoenix-style explanation of caching for beginners
- **THEN** the agent explains mechanism through concrete reader concerns and a bounded analogy without mandatory chapter or image quotas

#### Scenario: Inappropriate and conflicting requests

- **WHEN** the user requests code-only repair or formal minutes without asking for Phoenix voice
- **THEN** the skill does not impose that voice
- **AND** an explicit English, no-humor, 80-word Phoenix request retains those constraints


<!-- @trace
source: migrate-writing-skills-to-codex
updated: 2026-10-04
code:
  - maintenance/writing-skills/skills-mcp-manifest.json
  - maintenance/writing-skills/SOURCES.md
  - skills/phoenix-writing/reference
  - maintenance/writing-skills/legacy/phoenix-writing/reference/templates.md
  - maintenance/writing-skills/VALIDATION.md
  - skills/maintaining-writing-skills/legacy-validator/validate_article.py
  - skills/phoenix-writing/references/tw-vocabulary.md
  - skills/maintaining-writing-skills/references/skill-maintenance.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/concept-escalation-example.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/tw-vocabulary.md
  - skills/phoenix-writing/AGENTS.md
  - skills/phoenix-writing/references/style-examples.md
  - maintenance/writing-skills/legacy/phoenix-writing/AGENTS.md.txt
  - maintenance/writing-skills/MIGRATION.md
  - skills/maintaining-writing-skills/legacy-validator/rules/__init__.py
  - maintenance/writing-skills/residual-inventory.json
  - maintenance/writing-skills/legacy/phoenix-writing/reference/kaomoji-catalog.md
  - skills/maintaining-writing-skills/legacy-validator/rules/tier1_format.py
  - maintenance/writing-skills/legacy/phoenix-writing/reference/humor-patterns.md
  - skills/phoenix-writing/scripts
  - skills/maintaining-writing-skills/legacy-validator/rules/tier3_llm_hints.py
  - maintenance/writing-skills/legacy/phoenix-writing/reference/visual-guide.md
  - skills/maintaining-writing-skills/references/article-maintenance.md
  - skills/maintaining-writing-skills/legacy-validator/config.json
  - skills/maintaining-writing-skills/legacy-validator/rules/tier2_heuristic.py
  - maintenance/writing-skills/legacy/phoenix-writing/CLAUDE.md.txt
  - AGENTS.md
  - skills/creating-vitepress-post/SKILL.md
  - skills/maintaining-writing-skills/SKILL.md
  - maintenance/writing-skills/original-manifest.json
  - .agents/skills/phoenix-writing
  - maintenance/writing-skills/legacy/phoenix-writing/SKILL.md
  - CLAUDE.md
  - skills/maintaining-writing-skills/references/writing-process.md
  - skills/phoenix-writing/SKILL.md
  - skills/maintaining-writing-skills/references/spectra-codex.md
  - .agents/skills/maintaining-writing-skills
  - skills/maintaining-writing-skills/legacy-validator/rules/_common.py
  - maintenance/writing-skills/legacy/phoenix-writing/reference/dialogue-voices.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/domain-infosec.md
  - README.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/editorial-rules.md
  - skills/maintaining-writing-skills/references/legacy-validator.md
  - maintenance/writing-skills/INVENTORY.md
  - skills/phoenix-writing/CLAUDE.md
tests:
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s1_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/p1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/v1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t3_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/k1_sparse.md
  - skills/maintaining-writing-skills/legacy-validator/tests/test_tier2_tier3.py
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/f1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/f1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t2_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e1_with_warning.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e1_no_warning.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s3_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t3_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e2e_full.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/w1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/o1_hint.md
  - maintenance/writing-skills/tests/samples.json
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/v1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s2_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/m1_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/test_tier1.py
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/c1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/p1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t1_hint.md
  - maintenance/writing-skills/tests/cases.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t2_clean.md
-->

---
### Requirement: Canonical source and recoverable migration

The active skill SHALL reside in repo skills with resolving agent entry symlinks. The Mac original SHALL have a recoverable backup before replacement by a compatibility symlink. Legacy reference and validator callers SHALL retain resolving paths with documented historical semantics.

#### Scenario: Mac and repo entrypoints

- **WHEN** an agent opens the repo or existing global Phoenix entrypoint after migration
- **THEN** all active SKILL.md paths resolve to the canonical repo file
- **AND** original files are recoverable from a hash-verified backup


<!-- @trace
source: migrate-writing-skills-to-codex
updated: 2026-10-04
code:
  - maintenance/writing-skills/skills-mcp-manifest.json
  - maintenance/writing-skills/SOURCES.md
  - skills/phoenix-writing/reference
  - maintenance/writing-skills/legacy/phoenix-writing/reference/templates.md
  - maintenance/writing-skills/VALIDATION.md
  - skills/maintaining-writing-skills/legacy-validator/validate_article.py
  - skills/phoenix-writing/references/tw-vocabulary.md
  - skills/maintaining-writing-skills/references/skill-maintenance.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/concept-escalation-example.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/tw-vocabulary.md
  - skills/phoenix-writing/AGENTS.md
  - skills/phoenix-writing/references/style-examples.md
  - maintenance/writing-skills/legacy/phoenix-writing/AGENTS.md.txt
  - maintenance/writing-skills/MIGRATION.md
  - skills/maintaining-writing-skills/legacy-validator/rules/__init__.py
  - maintenance/writing-skills/residual-inventory.json
  - maintenance/writing-skills/legacy/phoenix-writing/reference/kaomoji-catalog.md
  - skills/maintaining-writing-skills/legacy-validator/rules/tier1_format.py
  - maintenance/writing-skills/legacy/phoenix-writing/reference/humor-patterns.md
  - skills/phoenix-writing/scripts
  - skills/maintaining-writing-skills/legacy-validator/rules/tier3_llm_hints.py
  - maintenance/writing-skills/legacy/phoenix-writing/reference/visual-guide.md
  - skills/maintaining-writing-skills/references/article-maintenance.md
  - skills/maintaining-writing-skills/legacy-validator/config.json
  - skills/maintaining-writing-skills/legacy-validator/rules/tier2_heuristic.py
  - maintenance/writing-skills/legacy/phoenix-writing/CLAUDE.md.txt
  - AGENTS.md
  - skills/creating-vitepress-post/SKILL.md
  - skills/maintaining-writing-skills/SKILL.md
  - maintenance/writing-skills/original-manifest.json
  - .agents/skills/phoenix-writing
  - maintenance/writing-skills/legacy/phoenix-writing/SKILL.md
  - CLAUDE.md
  - skills/maintaining-writing-skills/references/writing-process.md
  - skills/phoenix-writing/SKILL.md
  - skills/maintaining-writing-skills/references/spectra-codex.md
  - .agents/skills/maintaining-writing-skills
  - skills/maintaining-writing-skills/legacy-validator/rules/_common.py
  - maintenance/writing-skills/legacy/phoenix-writing/reference/dialogue-voices.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/domain-infosec.md
  - README.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/editorial-rules.md
  - skills/maintaining-writing-skills/references/legacy-validator.md
  - maintenance/writing-skills/INVENTORY.md
  - skills/phoenix-writing/CLAUDE.md
tests:
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s1_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/p1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/v1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t3_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/k1_sparse.md
  - skills/maintaining-writing-skills/legacy-validator/tests/test_tier2_tier3.py
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/f1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/f1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t2_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e1_with_warning.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e1_no_warning.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s3_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t3_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e2e_full.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/w1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/o1_hint.md
  - maintenance/writing-skills/tests/samples.json
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/v1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s2_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/m1_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/test_tier1.py
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/c1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/p1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t1_hint.md
  - maintenance/writing-skills/tests/cases.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t2_clean.md
-->

---
### Requirement: Source-backed Codex maintenance

Writing maintenance instructions SHALL use available host tools and actual CLI contracts, maintain source provenance, distinguish OpenAI principles from repo choices, and record executed validation separately from unexecuted model evaluations.

#### Scenario: Reviewing migration evidence

- **WHEN** a maintainer reviews this migration
- **THEN** evidence identifies the Astra article, quill-n-grill and writing-for-agents with necessary references and preserves their limitations
- **AND** GPT-6.1-sol high plus fast is described as a task choice rather than an Astra recommendation

<!-- @trace
source: migrate-writing-skills-to-codex
updated: 2026-10-04
code:
  - maintenance/writing-skills/skills-mcp-manifest.json
  - maintenance/writing-skills/SOURCES.md
  - skills/phoenix-writing/reference
  - maintenance/writing-skills/legacy/phoenix-writing/reference/templates.md
  - maintenance/writing-skills/VALIDATION.md
  - skills/maintaining-writing-skills/legacy-validator/validate_article.py
  - skills/phoenix-writing/references/tw-vocabulary.md
  - skills/maintaining-writing-skills/references/skill-maintenance.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/concept-escalation-example.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/tw-vocabulary.md
  - skills/phoenix-writing/AGENTS.md
  - skills/phoenix-writing/references/style-examples.md
  - maintenance/writing-skills/legacy/phoenix-writing/AGENTS.md.txt
  - maintenance/writing-skills/MIGRATION.md
  - skills/maintaining-writing-skills/legacy-validator/rules/__init__.py
  - maintenance/writing-skills/residual-inventory.json
  - maintenance/writing-skills/legacy/phoenix-writing/reference/kaomoji-catalog.md
  - skills/maintaining-writing-skills/legacy-validator/rules/tier1_format.py
  - maintenance/writing-skills/legacy/phoenix-writing/reference/humor-patterns.md
  - skills/phoenix-writing/scripts
  - skills/maintaining-writing-skills/legacy-validator/rules/tier3_llm_hints.py
  - maintenance/writing-skills/legacy/phoenix-writing/reference/visual-guide.md
  - skills/maintaining-writing-skills/references/article-maintenance.md
  - skills/maintaining-writing-skills/legacy-validator/config.json
  - skills/maintaining-writing-skills/legacy-validator/rules/tier2_heuristic.py
  - maintenance/writing-skills/legacy/phoenix-writing/CLAUDE.md.txt
  - AGENTS.md
  - skills/creating-vitepress-post/SKILL.md
  - skills/maintaining-writing-skills/SKILL.md
  - maintenance/writing-skills/original-manifest.json
  - .agents/skills/phoenix-writing
  - maintenance/writing-skills/legacy/phoenix-writing/SKILL.md
  - CLAUDE.md
  - skills/maintaining-writing-skills/references/writing-process.md
  - skills/phoenix-writing/SKILL.md
  - skills/maintaining-writing-skills/references/spectra-codex.md
  - .agents/skills/maintaining-writing-skills
  - skills/maintaining-writing-skills/legacy-validator/rules/_common.py
  - maintenance/writing-skills/legacy/phoenix-writing/reference/dialogue-voices.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/domain-infosec.md
  - README.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/editorial-rules.md
  - skills/maintaining-writing-skills/references/legacy-validator.md
  - maintenance/writing-skills/INVENTORY.md
  - skills/phoenix-writing/CLAUDE.md
tests:
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s1_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/p1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/v1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t3_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/k1_sparse.md
  - skills/maintaining-writing-skills/legacy-validator/tests/test_tier2_tier3.py
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/f1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/f1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t2_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e1_with_warning.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e1_no_warning.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s3_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t3_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e2e_full.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/w1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/o1_hint.md
  - maintenance/writing-skills/tests/samples.json
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/v1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s2_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/m1_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/test_tier1.py
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/c1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/p1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t1_hint.md
  - maintenance/writing-skills/tests/cases.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t2_clean.md
-->

---
### Requirement: Figure prose and guided-reading boundary

Phoenix prose SHALL explain a figure or table's mechanism, evidence and limits within the argument. It SHALL NOT replace that argument with commands to move the reader's gaze. Explicit requests for procedural figure-reading instruction SHALL permit accurate stepwise guidance. Neither mode SHALL require a question opener or prohibit reader dialogue.

#### Scenario: Figure integrated into prose

- **WHEN** a user asks for prose explaining a single-cache timeline with data updated at 10:00 and invalidation at 10:05
- **THEN** the prose explains the interval of potential stale reads and the single-cache scope without directing gaze movement
- **AND** it preserves uncertainty and does not claim multi-service coordination

#### Scenario: Explicit guided-reading lesson

- **WHEN** a user explicitly asks for two steps teaching how to read that timeline
- **THEN** the output provides two accurate reading steps and the requested caption
- **AND** guidance serves the requested lesson without inventing figure data

#### Scenario: Preserving failed evaluation history

- **WHEN** parent QA rejects an earlier output for gaze-direction prose and a mismatched opener rubric
- **THEN** original inputs, outputs and judgments remain unchanged, with a separate parent-QA correction
- **AND** a frozen revised skill is evaluated only on the affected positive and boundary cases by fresh writers and an independent judge

<!-- @trace
source: integrate-figures-in-prose
updated: 2026-10-04
code:
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/results.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E1/rubric.json
  - README.md
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/cases/E7/input.json
  - skills/maintaining-writing-skills/legacy-validator/rules/tier3_llm_hints.py
  - skills/maintaining-writing-skills/legacy-validator/rules/tier1_format.py
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/execution-provenance.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E6/output-v2.json
  - skills/maintaining-writing-skills/references/spectra-codex.md
  - maintenance/writing-skills/behavior-eval-20261004/cases/E4/rubric.json
  - skills/maintaining-writing-skills/legacy-validator/config.json
  - skills/maintaining-writing-skills/references/skill-maintenance.md
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/mechanical-checks-final.json
  - maintenance/writing-skills/legacy/phoenix-writing/AGENTS.md.txt
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/REPORT.md
  - maintenance/writing-skills/behavior-eval-20261004/cases/E8/input.json
  - skills/phoenix-writing/reference
  - maintenance/writing-skills/behavior-eval-20261004/cases/E5/judgment-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E5/input.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E7/output-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/check_figures.py
  - maintenance/writing-skills/behavior-eval-20261004/cases/E4/input.json
  - maintenance/writing-skills/legacy/phoenix-writing/CLAUDE.md.txt
  - maintenance/writing-skills/legacy/phoenix-writing/reference/templates.md
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/instruction-snapshot.json
  - maintenance/writing-skills/legacy/phoenix-writing/reference/visual-guide.md
  - maintenance/writing-skills/behavior-eval-20261004/cases/E5/rubric.json
  - skills/phoenix-writing/CLAUDE.md
  - maintenance/writing-skills/behavior-eval-20261004/REPORT.md
  - skills/phoenix-writing/scripts
  - skills/maintaining-writing-skills/legacy-validator/rules/tier2_heuristic.py
  - maintenance/writing-skills/behavior-eval-20261004/cases/E2/judgment-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/cases/E9/judgment-v21.json
  - maintenance/writing-skills/behavior-eval-20261004/instruction-snapshot.json
  - skills/phoenix-writing/AGENTS.md
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/cases/E7/rubric.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E6/rubric.json
  - skills/maintaining-writing-skills/SKILL.md
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/freeze-v22.json
  - AGENTS.md
  - maintenance/writing-skills/behavior-eval-20261004/results-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E2/rubric.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E6/input.json
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/cases/E7/output-v22.json
  - maintenance/writing-skills/legacy/phoenix-writing/reference/tw-vocabulary.md
  - maintenance/writing-skills/behavior-eval-20261004/cases/E3/rubric.json
  - maintenance/writing-skills/behavior-eval-20261004/check_mechanical.py
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/freeze.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E3/output-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/execution-provenance.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E8/rubric.json
  - maintenance/writing-skills/SOURCES.md
  - maintenance/writing-skills/behavior-eval-20261004/cases/E5/output-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/design.json
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/design.json
  - maintenance/writing-skills/original-manifest.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E3/input.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E8/judgment-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/cases/E9/output-v21.json
  - skills/maintaining-writing-skills/legacy-validator/rules/__init__.py
  - maintenance/writing-skills/behavior-eval-20261004/freeze.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E6/judgment-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/cases/E9/rubric.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E1/judgment-v2.json
  - skills/maintaining-writing-skills/legacy-validator/rules/_common.py
  - .agents/skills/phoenix-writing
  - skills/phoenix-writing/SKILL.md
  - maintenance/writing-skills/behavior-eval-20261004/cases/E4/output-v2.json
  - maintenance/writing-skills/skills-mcp-manifest.json
  - skills/creating-vitepress-post/SKILL.md
  - .agents/skills/maintaining-writing-skills
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/cases/E9/input.json
  - maintenance/writing-skills/legacy/phoenix-writing/reference/editorial-rules.md
  - maintenance/writing-skills/behavior-eval-20261004/cases/E2/input.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E1/output-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E3/judgment-v2.json
  - maintenance/writing-skills/INVENTORY.md
  - CLAUDE.md
  - skills/maintaining-writing-skills/references/legacy-validator.md
  - skills/maintaining-writing-skills/references/writing-process.md
  - skills/phoenix-writing/references/style-examples.md
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/cases/E7/output-v21.json
  - maintenance/writing-skills/legacy/phoenix-writing/reference/concept-escalation-example.md
  - maintenance/writing-skills/MIGRATION.md
  - maintenance/writing-skills/behavior-eval-20261004/cases/E2/output-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E7/rubric.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E7/judgment-v2.json
  - skills/maintaining-writing-skills/references/article-maintenance.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/humor-patterns.md
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/instruction-snapshot-v22.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E8/output-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/parent-qa-correction.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E1/input.json
  - maintenance/writing-skills/behavior-eval-20261004/REPORT.original-v2.md
  - maintenance/writing-skills/behavior-eval-20261004/mechanical-checks-v2.json
  - maintenance/writing-skills/legacy/phoenix-writing/reference/dialogue-voices.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/domain-infosec.md
  - maintenance/writing-skills/legacy/phoenix-writing/SKILL.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/kaomoji-catalog.md
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/mechanical-checks-v21.json
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/cases/E7/judgment-v21.json
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/cases/E7/judgment-v22.json
  - maintenance/writing-skills/residual-inventory.json
  - skills/phoenix-writing/references/tw-vocabulary.md
  - maintenance/writing-skills/behavior-eval-20261004/cases/E4/judgment-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E7/input.json
  - maintenance/writing-skills/VALIDATION.md
  - skills/maintaining-writing-skills/legacy-validator/validate_article.py
tests:
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/c1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/v1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s3_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/k1_sparse.md
  - skills/maintaining-writing-skills/legacy-validator/tests/test_tier1.py
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/p1_violation.md
  - maintenance/writing-skills/tests/samples.json
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/m1_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e2e_full.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t3_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e1_with_warning.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t2_violation.md
  - maintenance/writing-skills/tests/cases.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/o1_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s1_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/v1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t1_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t2_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e1_no_warning.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/w1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t3_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/f1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/p1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/f1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/test_tier2_tier3.py
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s2_hint.md
-->