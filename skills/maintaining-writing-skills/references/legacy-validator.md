# 舊規格與相容入口

舊 validator 保留在 [legacy-validator](../legacy-validator/validate_article.py)。只在使用者要求舊 EAL+ 規格或需要核對既有驗證結果時執行：

```sh
python3 skills/maintaining-writing-skills/legacy-validator/validate_article.py <article.md>
```

從 repo root 執行；也可用解析後的絕對路徑。它使用本地 Python 標準庫，不呼叫模型 API。新風格的普通自檢不執行此工具。

scripts/validate_article.py 的舊路徑透過 phoenix-writing/scripts symlink 保留。輸出 JSON 的 pass 只表示舊規格的 error/warning 是否為零；其中密度與語法啟發式可能不符合新文類，不能當新風格品質指標。Tier 3 hints 是本地提示，不是已執行 LLM 評測。

原始 SKILL、AGENTS、CLAUDE 和 references 保存在 [歷史目錄](../../../maintenance/writing-skills/legacy/phoenix-writing/SKILL.md)。phoenix-writing/reference 相容指向此目錄的 reference，引用歷史規則時標示版本；當前正文只讀新 references。Mac 原資料夾備份與復原步驟見 [搬移紀錄](../../../maintenance/writing-skills/MIGRATION.md)。
