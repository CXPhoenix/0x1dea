# Round 1 補充證據：契約衝突

Reviewer：`/root/ad_contracts`。同一輪、同一提示、同一 spec，唯讀補充。

補充證據不改變原結論：**P0：0、P1：0、P2：0**，未新增契約衝突 finding。

已核對新增 23 份快照的長度與 SHA-256，全部一致；原 40 份快照及 frozen prompt hash 也維持不變。本次補齊：

- 文章交付契約：`skills/managing-article-publication/references/local.md:16–23,42–48,91–92` 要求完整 pins、來源分支及明確發布授權，與規格 spec.en.md:58,90 保留既有交付責任相容。
- current guard／policy：`scripts/publication_current.py:97–146,279–309` 採精確來源 inventory 與 identity。規格 spec.en.md:96,118 已明示有限、經審查的 successor 更新並保留歷史，未要求放寬為目錄級豁免。guard 會納入 ignored 檔案（:227–248）；規格也未承諾含未納管筆記的工作目錄必須直接通過此檢查，故目前不構成不可相容要求。
- Claude 原始三技能：`.claude/skills/grilling/SKILL.md:28`、domain-modeling/SKILL.md:40–74、grill-with-docs/SKILL.md:4–7 未推翻規格 spec.en.md:31,57,84 的明示文章分流與舊規則替換。
- 既有寫作案例：所附案例的作者限制、受保護內容及禁止未授權副作用要求，與規格 AC-01、04、07、13、16 相容。

仍保留一項證據範圍限制：補充 manifest 實際只有 E1～E8 的 16 份 input／rubric，未含 E9，因此不宣稱已核對 E9。此次也未執行 guard 或真實 runtime，不構成執行驗證。
