# vitepress-post-scaffolding Specification

## Purpose

TBD - created by archiving change 'add-skills-for-scripts-dir'. Update Purpose after archive.

## Requirements

### Requirement: Agents SHALL invoke the helper script for new posts

When a user requests creation of a new article file on the 0x1DEA VitePress site, the agent SHALL invoke `pnpm new:post "<title>" [-c <category> | -d <path>]`. Existing article edits and conversation-only drafts SHALL NOT trigger scaffolding. The agent SHALL preserve existing createdTime when editing a post. A helper failure SHALL be surfaced instead of bypassed by hand-writing a new article file.

#### Scenario: User asks to add a post under a category

- **WHEN** the user says "新增一篇 course/intro 的文章 'Hello World'"
- **THEN** the agent runs `pnpm new:post "Hello World" -c course/intro`
- **AND** uses the emitted article and assets paths

#### Scenario: User specifies an arbitrary directory

- **WHEN** the user says "Create a post in docs/post/special/"
- **THEN** the agent runs `pnpm new:post "<title>" -d docs/post/special`

#### Scenario: User requests a post in the default directory

- **WHEN** the user says "Add a blog post titled 'Quick Note'" to this site
- **THEN** the agent runs `pnpm new:post "Quick Note"` with no flags
- **AND** the resulting markdown lands in `docs/post/Quick_Note.md`

#### Scenario: Conversation draft and existing post

- **WHEN** the user requests a draft in conversation or revision of an existing post
- **THEN** the agent does not call the scaffolding CLI


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
### Requirement: The skill SHALL document the -c / -d exclusivity

The skill content SHALL state that the `-c` and `-d` flags MUST NOT be combined. The skill SHALL surface the exact runtime error string `參數 -c 與 -d 不能同時使用。` so agents recognize the failure mode.

#### Scenario: Reader looks up flag rules

- **WHEN** an agent reads the SKILL.md Quick Reference table
- **THEN** the agent sees `-c` and `-d` listed as mutually exclusive
- **AND** the agent sees the verbatim error string the script emits when both are passed

#### Scenario: Agent rejects a malformed request

- **WHEN** the user asks for `pnpm new:post "X" -c course -d docs/post/other`
- **THEN** the agent declines and explains the flags conflict
- **AND** the agent proposes either `-c course` or `-d docs/post/other`, not both


<!-- @trace
source: add-skills-for-scripts-dir
updated: 2026-04-27
code:
  - .agents/skills/creating-vitepress-post
  - skills/creating-vitepress-post/SKILL.md
-->

---
### Requirement: The skill SHALL describe the assets folder naming rule

The skill SHALL describe that for a post saved at `docs/post/<segments>/<file>.md`, the matching assets folder is `docs/public/assets/<segments_joined_with_underscore>_<safe_filename>/`, with `root_<safe_filename>` as the special case for posts directly under `docs/`. The skill SHALL also document that `safe_filename` is the post name with whitespace replaced by underscores.

#### Scenario: Agent needs to add an image to a freshly scaffolded post

- **WHEN** an agent must place an image into a post created by the script
- **THEN** the skill tells it the exact assets folder name to use
- **AND** the markdown reference path begins with `/assets/`

##### Example: assets folder naming for representative inputs

| Post path | Resulting assets folder |
| --------- | ----------------------- |
| `docs/post/hello_world.md` | `docs/public/assets/post_hello_world/` |
| `docs/post/course/intro/hello_world.md` | `docs/public/assets/post_course_intro_hello_world/` |
| `docs/intro.md` (directly under `docs/`) | `docs/public/assets/root_intro/` |


<!-- @trace
source: add-skills-for-scripts-dir
updated: 2026-04-27
code:
  - .agents/skills/creating-vitepress-post
  - skills/creating-vitepress-post/SKILL.md
-->

---
### Requirement: The skill frontmatter SHALL satisfy the Anthropic Agent Skill specification

The skill frontmatter SHALL retain portable Agent Skills name and description fields usable by Codex and existing compatible hosts. The name SHALL be `creating-vitepress-post`, and the concise description SHALL identify new website article creation rather than generic writing or all docs/post mentions. Existing license, compatibility and metadata SHALL be retained where accurate. The historical requirement title SHALL remain for delta compatibility and SHALL NOT make Claude-specific tools an execution dependency.

#### Scenario: Tooling validates frontmatter

- **WHEN** the skill validator parses the frontmatter
- **THEN** it finds a valid name and a concise description within 1024 characters

#### Scenario: Description focuses on invocation boundary

- **WHEN** an agent chooses the skill
- **THEN** website file creation matches while prose-only drafting and existing post editing are excluded


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
### Requirement: The skill SHALL be reachable from Claude Code, Codex, and Gemini CLI

The skill content SHALL live at a single canonical path `skills/creating-vitepress-post/SKILL.md` at the project root. The agent-specific scan paths `.claude/skills/creating-vitepress-post`, `.gemini/skills/creating-vitepress-post`, and `.agents/skills/creating-vitepress-post` SHALL each resolve to that canonical path via a relative symlink, so all three agents read identical content.

#### Scenario: Each agent path resolves to the canonical SKILL.md

- **WHEN** an operator runs `ls -laL .claude/skills/creating-vitepress-post/SKILL.md .gemini/skills/creating-vitepress-post/SKILL.md .agents/skills/creating-vitepress-post/SKILL.md`
- **THEN** all three rows reference the same underlying file
- **AND** `diff` between any two pairs returns no differences

<!-- @trace
source: add-skills-for-scripts-dir
updated: 2026-04-27
code:
  - .agents/skills/creating-vitepress-post
  - skills/creating-vitepress-post/SKILL.md
-->