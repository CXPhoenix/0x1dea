# vitepress-post-scaffolding Specification

## Purpose

TBD - created by archiving change 'add-skills-for-scripts-dir'. Update Purpose after archive.

## Requirements

### Requirement: Agents SHALL invoke the helper script for new posts

When a user requests a new article on the 0x1DEA VitePress site, the agent SHALL invoke `pnpm new:post "<title>" [-c <category> | -d <path>]` rather than hand-authoring the markdown file with a generic write tool. The agent SHALL NOT bypass the helper script even when the desired output appears trivial, because the script enforces frontmatter fields, the UTC+8 ISO-8601 `createdTime` timestamp, the title-case rule, and the matching assets folder.

#### Scenario: User asks to add a post under a category

- **WHEN** the user says "新增一篇 course/intro 的文章 'Hello World'"
- **THEN** the agent runs `pnpm new:post "Hello World" -c course/intro`
- **AND** the agent does not call any direct file-write tool to create the markdown file

#### Scenario: User specifies an arbitrary directory

- **WHEN** the user says "Create a post in docs/post/special/"
- **THEN** the agent runs `pnpm new:post "<title>" -d docs/post/special`

#### Scenario: User requests a post in the default directory

- **WHEN** the user says "Add a blog post titled 'Quick Note'"
- **THEN** the agent runs `pnpm new:post "Quick Note"` with no flags
- **AND** the resulting markdown lands in `docs/post/quick_note.md`


<!-- @trace
source: add-skills-for-scripts-dir
updated: 2026-04-27
code:
  - .agents/skills/creating-vitepress-post
  - skills/creating-vitepress-post/SKILL.md
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

The `SKILL.md` frontmatter SHALL declare `name` (letters, numbers, hyphens only), and a third-person `description` that begins with "Use when" and lists triggering conditions without summarizing internal workflow. The total frontmatter character count MUST NOT exceed 1024 characters. The skill name SHALL be `creating-vitepress-post`.

#### Scenario: Tooling validates frontmatter length

- **WHEN** a verification step runs `head -n 20 skills/creating-vitepress-post/SKILL.md | wc -c`
- **THEN** the byte count is at most 1024

#### Scenario: Description focuses on triggers, not workflow

- **WHEN** a reviewer reads the description field
- **THEN** the description names trigger phrases in Traditional Chinese and English
- **AND** the description does not enumerate the steps the agent must perform after triggering


<!-- @trace
source: add-skills-for-scripts-dir
updated: 2026-04-27
code:
  - .agents/skills/creating-vitepress-post
  - skills/creating-vitepress-post/SKILL.md
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