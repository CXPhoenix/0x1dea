## Why

原 Phoenix 寫作技能將作者聲音、固定章節配方與工具操作混在一起，且全域實體與 repo 技能入口分散。重整可讓 GPT/Codex 依文類使用風格，同時維持既有 Mac 入口和歷史內容。

## What Changes

- 將 Phoenix 風格移至 repo 的 skills 單一来源，保留 Mac 相容 symlink 與可恢復備份。
- 收斂風格觸發，拆開新文 CLI、編輯維護與舊版 validator，明示用戶要求優先。
- 更新 Codex 可讀入口、Claude 相容指引與新文技能；記錄指定來源、repo 決策與驗收證據。

## Capabilities

### New Capabilities

- `phoenix-style-and-maintenance`: 作者風格邊界、維護路由、Mac 搬移相容與驗證。

### Modified Capabilities

- `vitepress-post-scaffolding`: 精準區分建立網站文章與對話草稿，將 frontmatter 契約改為可供 GPT/Codex 使用的格式。

## Impact

- `skills/phoenix-writing/SKILL.md`、`skills/creating-vitepress-post/SKILL.md`、`skills/maintaining-writing-skills/SKILL.md`。
- `AGENTS.md`、`CLAUDE.md`、`README.md` 與 `.agents/skills`、`.claude/skills` 的技能入口。
- `maintenance/writing-skills` 保存來源追溯、歷史資料與驗收；Mac 原技能位置透過相容 symlink 回到 repo。
