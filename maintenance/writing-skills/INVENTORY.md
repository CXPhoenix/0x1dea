# 寫作／維護盤點與 Claude 殘留分類

## 已處理的有效指引

| 初始位置 | 原用途與問題 | 本次處理 |
|---|---|---|
| Mac phoenix-writing/SKILL.md | 風格與固定序列、圖表格式、研究與 validator 混在一起；語言不可覆寫、密度配額 | repo 的風格核心＋按需參考；保留作者聲音，分離操作與舊檢查 |
| Mac phoenix-writing/CLAUDE.md、AGENTS.md | 自稱 Claude plugin，指向 custom_skills 的父層 Spectra；編輯規則重述風格 | repo 技能內維護指標；原文存 .md.txt 歷史檔 |
| repo skills/creating-vitepress-post | 各種寫作與 docs/post 字樣都觸發 CLI，操作及 implementation 細節過多 | 只建立網站新文章；對話草稿與改稿不觸發；以源碼核對命名、保留衝突與 +08:00 契約 |
| repo CLAUDE.md／AGENTS.md | Claude 與 Codex 的生成區塊重複；Codex 找不到 .agents 下的 Spectra 技能入口 | CLAUDE 共通指向 AGENTS；Codex 由維護技能的 Spectra 參考按分支取 CLI instructions |
| repo README | 只有網站使用說明，沒有作者風格／操作邊界 | 只增技能入口與遷移說明；其他段落不變 |

## 保留且分類的殘留

- **相容與歷史名稱**：.claude 目錄、CLAUDE.md 與 archived 原始文含 Claude。這些是入口或來源識別，不是模型選擇規定。
- **供應商生成內容**：.claude/skills/spectra-* 原檔仍含 AskUserQuestion、Task/Skill、Glob 與 slash syntax；.github 和 .gemini 也有生成副本。本次不全面改造這些供應商生成工作流。Codex 寫作／維護的有效操作走 [spectra-codex](../../skills/maintaining-writing-skills/references/spectra-codex.md)，實際工具行為、CLI schema、授權與完成條件已改寫，不是替換模型字串。
- **Claude 宿主 hook**：.claude/hooks/check-staged-files.sh 輸出 PreToolUse／hookSpecificOutput JSON，.claude/settings.json 是宿主設定。保留原狀；未搬成 Codex 安全機制，也未修改全域安全設定或憑證。本任務不 commit；後續 commit 可在 Codex 用 Git 檢視選取檔案，不能宣稱此 hook 會自動執行。
- **Spectra 設定範例**：.spectra.yaml 的 claude_effort／claude_slash_commands 目前是註解範例，並非本次 Sol high/fast 的設定來源，保留以免更動供應商設定範圍。
- **舊風格原文**：歷史 SKILL／reference／validator 保留舊固定配方、密度與格式。未偽稱已換成新規則；普通風格不載入，明示舊規格才讀。
- **外部個人技能**：gcce-writer 的語言參考、humane-prose-audit 的 EAL+ 描述、skill-mirror 的示例和原個人 repo 的 openspec trace 均未改。相容入口可解析，外部 EAL+ 密度語意仍屬舊版；需要同步語意時另開授權範圍。

檔名層級的實際搜尋結果在 [residual-inventory.json](residual-inventory.json)。分類不是宣稱 repo 已完全移除 Claude，也不是宣稱所有 Spectra 生成技能都完成 GPT 改寫。無關文章、程式、CSS 和私有原稿未修改。
