<!-- SPECTRA:START v1.0.2 -->

# Spectra Instructions

This project uses Spectra for Spec-Driven Development(SDD). Specs live in `openspec/specs/`, change proposals in `openspec/changes/`.

## Use `$spectra-*` skills when:

- A discussion needs structure before coding → `$spectra-discuss`
- User wants to plan, propose, or design a change → `$spectra-propose`
- Tasks are ready to implement → `$spectra-apply`
- There's an in-progress change to continue → `$spectra-ingest`
- User asks about specs or how something works → `$spectra-ask`
- Implementation is done → `$spectra-archive`
- Commit only files related to a specific change → `$spectra-commit`

## Workflow

discuss? → propose → apply ⇄ ingest → archive

- `discuss` is optional — skip if requirements are clear
- Requirements change mid-work? `ingest` → resume `apply`

## Parked Changes

Changes can be parked（暫存）— temporarily moved out of `openspec/changes/`. Parked changes won't appear in `spectra list` but can be found with `spectra list --parked`. To restore: `spectra unpark <name>`. The `$spectra-apply` and `$spectra-ingest` skills handle parked changes automatically.

<!-- SPECTRA:END -->


# 寫作與維護路由

- 明示 Phoenix 聲音或延續其作品：讀 [phoenix-writing](skills/phoenix-writing/SKILL.md)。一般繁中與正式文件不因此套用該風格。
- 建立本站新文章檔案：讀 [creating-vitepress-post](skills/creating-vitepress-post/SKILL.md)。對話草稿與既有文章修訂不建立骨架。
- 修改寫作技能／agent 指引、維護文章檔案或查舊 validator：讀 [maintaining-writing-skills](skills/maintaining-writing-skills/SKILL.md)。
- 上方 Spectra 操作在 Codex 用 [Spectra 操作參考](skills/maintaining-writing-skills/references/spectra-codex.md)；舊生成檔的 Claude 工具名對應實際可用工具，先核對 CLI instructions，不讀全域 sessions。

有效技能內容在 skills；.agents/skills 與 .claude/skills 入口解析到同一來源。來源、模型選擇與歷史範圍在 [搬移來源](maintenance/writing-skills/SOURCES.md)，只在維護或追溯時讀。使用者當次要求與既有授權優先；完成本地修改與驗證不推導 commit、push 或發布權限。
