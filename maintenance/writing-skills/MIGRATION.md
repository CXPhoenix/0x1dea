# 搬移與相容紀錄

初始 repo：repo 根目錄 0x1DEA（使用者輸入 0x1dea 在此 Mac 解析到同一位置）。初始 Git dirty 狀態：乾淨。

## 位置

- 新有效來源：repo skills/phoenix-writing。
- repo Codex 與 Claude 入口：.agents/skills/phoenix-writing、.claude/skills/phoenix-writing，預期指向 ../../skills/phoenix-writing。
- Mac 原實體：~/.agents/custom_skills/phoenix-writing，切換後保存為 ~/.agents/skill-backups/phoenix-writing-pre-codex-20261004（不在有效技能掃描根目錄），原位設 symlink 到新 repo 來源。
- 原 Codex 入口 ~/.codex/skills/phoenix-writing 與 Gemini 入口保留原 symlink，經 Mac 原位解析到新來源。
- phoenix-writing/scripts 相容指向 maintaining-writing-skills/legacy-validator；reference 相容指向 maintenance/writing-skills/legacy/phoenix-writing/reference。這是舊規格相容路徑，普通寫作不載入。

## 原始備份

完整原資料夾（包括本地 temp-reference，如有）先備份到 本機 migration-evidence/original-phoenix-writing，Mac 備份保留原狀。repo 的歷史檔案只保留技能指引、reference 與 validator，沒有引入私有原稿或全域設定。公開 hash 清單只列 43 個指引、reference 與 validator 檔案；本機完整清單及備份保留全部 50 個原檔，私有草稿的名稱與 hash 不公開。

## 復原

先確認 repo 的當前修改是否要保留。把 Mac 原位的新 symlink 改名保存，再把 ~/.agents/skill-backups/phoenix-writing-pre-codex-20261004 移回 ~/.agents/custom_skills/phoenix-writing。原 Codex/Gemini symlink 可直接解析回原技能。repo 變更由 Git diff 個別檢視和回復，避免覆蓋同時修改；不執行強制 reset 或永久刪檔。

## 已發現的相依

其他個人技能以名稱引用 Phoenix（例如 gcce-writer 與 humane-prose-audit）；沒有改它們。台灣用語 reference 子路徑與 validator 入口保留可解析。外部稽核對舊 EAL+ 密度指標的描述是歷史相依，新核心不承諾這項配額；需要外部技能改版時另開範圍。

## 驗收

實際切換狀態、入口解析、來源與案例結果寫在 [驗收報告](VALIDATION.md)。上述位置表是遷移契約；以驗收報告的實際執行狀態為準。
