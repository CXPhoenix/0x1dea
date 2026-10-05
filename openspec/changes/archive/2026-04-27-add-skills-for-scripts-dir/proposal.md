## Why

`scripts/vpHelper.ts`（透過 `package.json` 的 `pnpm new:post` 暴露）封裝了 0x1DEA 部落格新文章的三項契約：frontmatter 欄位（`title` / `description` / `createdTime` / `thumbnail`）、UTC+8 ISO-8601 時間戳，以及 `docs/public/assets/<segments>_<safe-filename>` 的對應資源資料夾命名規則。LLM 在沒有 skill 引導時，會傾向用 `Write` 工具直接建立 markdown，繞過上述契約，導致時區錯誤、欄位漏掉、assets 資料夾命名不一致等漂移。需要一支符合 Anthropic Agent Skill 規範的 skill 引導 Claude Code、Codex、Gemini CLI 等 agent 在自動化流程中一律使用 `pnpm new:post`。

## What Changes

- 新增 canonical skill 檔：`skills/creating-vitepress-post/SKILL.md`，遵循 Anthropic Agent Skill 規範（`name`/`description` 必填、總長度 ≤ 1024 chars、第三人稱「Use when…」描述、letters/numbers/hyphens 命名）
- 在三個 agent 標準掃描路徑分別建立 symlink 指回 canonical：`.claude/skills/creating-vitepress-post`、`.gemini/skills/creating-vitepress-post`、`.agents/skills/creating-vitepress-post`
- Skill 內容覆蓋：觸發條件（中英雙語）、CLI 三種呼叫方式、`-c`/`-d` 互斥規則、產生的檔案結構、frontmatter 契約、assets 命名演算法、5 條常見錯誤、`vpHelper.ts` 關鍵函式對照
- 為日後新增 `scripts/<other>.ts` 時建立可複製模式：每支腳本對應一支 `skills/<verb-noun>/` skill 並在三個 agent 路徑下 symlink

## Non-Goals

- 不修改 `scripts/vpHelper.ts` 的執行行為（只描述外部契約）
- 不為 `scripts/` 以外的功能撰寫 skill
- 不在使用者層級（`~/.claude/skills/` 等）建立全域 skill — 此 skill 與專案 npm script 緊耦合，跨專案無意義
- 不採用既有 `spectra-*` skills 的「在每個 agent 目錄重複實體檔案」做法 — 手寫 skill 改用 canonical + symlink 確保三家 agent 讀到完全一致內容、避免漂移
- 不為 skill 進行嚴格 RED/GREEN 子代理壓力測試 — 此屬 reference + technique 混合型 skill，依 `superpowers:writing-skills` 指引以 Inline Self-Review（placeholder / consistency / scope / ambiguity 四檢核）+ live skill load 取代

## Capabilities

### New Capabilities

- `vitepress-post-scaffolding`：規範 LLM agent 在使用者要求建立 0x1DEA 新文章時必須呼叫 `pnpm new:post`，並描述 skill 觸發條件、`-c`/`-d` 互斥約束，以及 assets 資料夾命名演算法的對外契約。

### Modified Capabilities

(none)

## Impact

- Affected specs: `vitepress-post-scaffolding`（新增）
- Affected code:
  - New: `skills/creating-vitepress-post/SKILL.md`
  - New: `.claude/skills/creating-vitepress-post`（symlink → `../../skills/creating-vitepress-post`）
  - New: `.gemini/skills/creating-vitepress-post`（symlink → `../../skills/creating-vitepress-post`）
  - New: `.agents/skills/creating-vitepress-post`（symlink → `../../skills/creating-vitepress-post`）
  - Modified: (none)
  - Removed: (none)
