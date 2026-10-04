## MODIFIED Requirements

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

### Requirement: The skill frontmatter SHALL satisfy the Anthropic Agent Skill specification

The skill frontmatter SHALL retain portable Agent Skills name and description fields usable by Codex and existing compatible hosts. The name SHALL be `creating-vitepress-post`, and the concise description SHALL identify new website article creation rather than generic writing or all docs/post mentions. Existing license, compatibility and metadata SHALL be retained where accurate. The historical requirement title SHALL remain for delta compatibility and SHALL NOT make Claude-specific tools an execution dependency.

#### Scenario: Tooling validates frontmatter

- **WHEN** the skill validator parses the frontmatter
- **THEN** it finds a valid name and a concise description within 1024 characters

#### Scenario: Description focuses on invocation boundary

- **WHEN** an agent chooses the skill
- **THEN** website file creation matches while prose-only drafting and existing post editing are excluded
