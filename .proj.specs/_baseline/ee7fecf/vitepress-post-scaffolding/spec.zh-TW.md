---
language: zh-TW
authority: spec.en.md
synced_from: spec.en.md
synced_from_sha: fad7d445581ce01ae28f67db546ae115ee7a0f4a
source_path: openspec/specs/vitepress-post-scaffolding/spec.md
source_commit: ee7fecfff72f47abc735d26ac7e9a943de04ebbf
historical_harness_review: not-recorded-under-harness
---
# vitepress-post-scaffolding 規格稽核翻譯

> 英文原文是歷史權威；本頁是全文稽核翻譯。歷史 Harness review、TDD 與 landing 未記錄，不在此次重建。 Harness 歷史狀態為 `not recorded under harness`；`historical review not recreated`。下文保留歷史 docs 路徑、agent symlink 契約與原 @trace；目前 blog／實體 runtime 的局部取代另見 adoption 規格。

## 目的

待補：由封存變更 `add-skills-for-scripts-dir` 建立。原規格要求封存後更新 Purpose；本次唯讀歷史匯入保留這項未完成狀態。

## 需求

### Requirement: Agent 必須為新文章呼叫 helper script

使用者要求在 0x1DEA VitePress 網站建立新文章檔案時，agent 必須呼叫 `pnpm new:post "<title>" [-c <category> | -d <path>]`。既有文章修改及只在對話中的草稿不得觸發骨架產生。編輯既有文章時必須保留 createdTime。helper 失敗必須呈報，不得繞過失敗而手寫新文章檔案。

#### Scenario: 使用者要求在分類下新增文章

- **WHEN** 使用者說「新增一篇 course/intro 的文章 'Hello World'」
- **THEN** agent 執行 `pnpm new:post "Hello World" -c course/intro`
- **AND** 使用輸出的文章與資源路徑

#### Scenario: 使用者指定任意目錄

- **WHEN** 使用者說「Create a post in docs/post/special/」（在 docs/post/special/ 建立文章）
- **THEN** agent 執行 `pnpm new:post "<title>" -d docs/post/special`

#### Scenario: 使用者要求預設目錄中的文章

- **WHEN** 使用者對本站說「Add a blog post titled 'Quick Note'」（新增標題為 Quick Note 的文章）
- **THEN** agent 執行不帶 flags 的 `pnpm new:post "Quick Note"`
- **AND** Markdown 產生於 `docs/post/Quick_Note.md`

#### Scenario: 對話草稿與既有文章

- **WHEN** 使用者要求對話草稿或修訂既有文章
- **THEN** agent 不呼叫骨架 CLI

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
### Requirement: 技能必須記載 -c／-d 互斥

技能必須明確說明 `-c` 與 `-d` 不得合用，並提供精確的 runtime 錯誤字串 `參數 -c 與 -d 不能同時使用。`，讓 agent 辨識此失敗形式。

#### Scenario: 讀者查詢 flag 規則

- **WHEN** agent 閱讀 SKILL.md Quick Reference 表
- **THEN** 看見 `-c` 與 `-d` 列為互斥
- **AND** 看見兩者同時傳入時腳本輸出的原樣錯誤字串

#### Scenario: Agent 拒絕格式錯誤的要求

- **WHEN** 使用者要求 `pnpm new:post "X" -c course -d docs/post/other`
- **THEN** agent 拒絕並解釋 flags 衝突
- **AND** 提議 `-c course` 或 `-d docs/post/other` 擇一，不同時使用

<!-- @trace
source: add-skills-for-scripts-dir
updated: 2026-04-27
code:
  - .agents/skills/creating-vitepress-post
  - skills/creating-vitepress-post/SKILL.md
-->

---
### Requirement: 技能必須說明資源資料夾命名

技能必須說明：文章在 `docs/post/<segments>/<file>.md` 時，對應資源資料夾為 `docs/public/assets/<segments_joined_with_underscore>_<safe_filename>/`；直接位於 `docs/` 的文章，特殊形式為 `root_<safe_filename>`。亦必須說明 `safe_filename` 是將文章名稱空白換成底線的結果。

#### Scenario: Agent 要為剛產生骨架的文章加圖片

- **WHEN** agent 必須在腳本建立的文章中放入圖片
- **THEN** 技能提供應使用的精確資源資料夾名稱
- **AND** Markdown 引用路徑以 `/assets/` 開頭

##### 範例：代表性輸入的資源命名

| 文章路徑 | 資源資料夾 |
| --- | --- |
| `docs/post/hello_world.md` | `docs/public/assets/post_hello_world/` |
| `docs/post/course/intro/hello_world.md` | `docs/public/assets/post_course_intro_hello_world/` |
| `docs/intro.md`（直接位於 `docs/`） | `docs/public/assets/root_intro/` |

<!-- @trace
source: add-skills-for-scripts-dir
updated: 2026-04-27
code:
  - .agents/skills/creating-vitepress-post
  - skills/creating-vitepress-post/SKILL.md
-->

---
### Requirement: 技能 frontmatter 必須符合 Anthropic Agent Skill 規格

frontmatter 必須保留 Codex 及現有相容 host 可使用的可攜 Agent Skills name 與 description。name 必須為 `creating-vitepress-post`；精簡 description 必須指出新增網站文章，而不是一般寫作或任何提到 docs/post 的要求。現有 license、compatibility、metadata 在準確的範圍內必須保留。歷史需求標題必須保留以維持差異相容性，不得因此將 Claude 專屬工具變成執行依賴。

#### Scenario: 工具驗證 frontmatter

- **WHEN** 技能 validator 解析 frontmatter
- **THEN** 找到有效 name，以及 1024 字元內的精簡 description

#### Scenario: Description 聚焦呼叫邊界

- **WHEN** agent 選擇技能
- **THEN** 網站檔案建立符合觸發條件，而純文字草稿及既有文章編輯不符合

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
### Requirement: Claude Code、Codex 與 Gemini CLI 都必須可找到技能

內容必須位於專案根下單一 canonical 路徑 `skills/creating-vitepress-post/SKILL.md`。各 agent 掃描路徑 `.claude/skills/creating-vitepress-post`、`.gemini/skills/creating-vitepress-post`、`.agents/skills/creating-vitepress-post` 必須透過相對 symlink 解析到該 canonical 路徑，讓三種 agent 讀到相同內容。

#### Scenario: 每個 agent 路徑解析到 canonical SKILL.md

- **WHEN** 操作者執行 `ls -laL .claude/skills/creating-vitepress-post/SKILL.md .gemini/skills/creating-vitepress-post/SKILL.md .agents/skills/creating-vitepress-post/SKILL.md`
- **THEN** 三列都指向相同底層檔案
- **AND** 任兩組之間的 `diff` 都沒有差異

<!-- @trace
source: add-skills-for-scripts-dir
updated: 2026-04-27
code:
  - .agents/skills/creating-vitepress-post
  - skills/creating-vitepress-post/SKILL.md
-->
