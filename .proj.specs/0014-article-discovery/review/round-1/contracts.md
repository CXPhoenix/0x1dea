# Round 1：契約衝突

Reviewer：`/root/ad_contracts`；獨立上下文、唯讀。父執行緒保存以下回傳結果，未更動其分級。

Round 1 Contract conflict 審查完成：**P0：0、P1：0、P2：0**。在供應的凍結證據內，未找到必須同時遵守卻無法相容的契約。這不代表 runtime 行為或使用體驗已通過驗證。

審查基準為 staging，base＝HEAD＝`6fcb277a9841dfad21d91f79005d39924acd92d2`；staged／unstaged patch 均為空，四個未追蹤範圍檔案另有完整 addition patch。已核對 capture.json 所列 40 份快照的長度與 SHA-256，全部一致。全程唯讀。

以下 S 代表原始路徑 `.proj.specs/0014-article-discovery/spec.en.md`；行號均對應 frozen .txt 的原始內容。

| 覆蓋項目 | 雙方契約證據 | AC／row | 結果 |
|---|---|---|---|
| 自由聊、抒發、只聽、不明目的、未指定受眾 | S:35–45；既有 `.agents/skills/grilling/SKILL.md:6–28` | AC-02～05；R03～R12 | S:31 明示不匯入完整工程訪談契約，因此工程的完整收斂與確認條件不會成為文章起稿前提。 |
| 直接起稿、反覆摘要、回訪與改方向 | S:30、:36–45；`docs/agents/codex.md:9–12` | AC-01、03、05；R02、R07、R10～R12 | 沿用既有答案及授權、僅更新受影響設定，與 Codex 避免重複核准的契約相容。 |
| 純文章、混合工程需求、skill 本身的 spec | S:50–60；`AGENTS.md:47–84`；`docs/agents/workflow.md:29–100` | AC-06、14；R13～R14、R33 | S:57 明示新增狹義 editorial exception；:55 同時保留 skill／工具修改的工程關卡。這是明示變更，非默默繞過 pipeline。 |
| 無術語、首個可重用術語、草案與已解決定義、比喻、空骨架覆寫 | S:64–77；`skills/maintaining-writing-skills/references/writing-process.md:9–11` | AC-08～11；R17～R28 | S:84 明示取代每專案必建 CONTEXT／PROJECT 的規則；作者用法、來源定義與讀者解釋各有分工，未發現須強迫消除文學多義性的殘留要求。 |
| 僅 legacy CONTEXT、僅 GLOSSARY、兩者並存、有效／無效／缺失指定 | S:79–84；`docs/agents/domain.md:3–13,43–47`；`.agents/skills/domain-modeling/SKILL.md:3,40–64` | AC-10～12、14；R25、R29～R30、R33 | 新規格明確區分工程與文章詞彙所有權；既有檔案沿用、不自動遷移，歧義只暫停詞彙寫入。工程 CONTEXT 不作文章 fallback。 |
| 保存授權、既有工作區、來源內嵌指令、路徑與碰撞、可見性及 readback 失敗 | S:64–77,143；`skills/maintaining-writing-skills/SKILL.md:20` | AC-08、11；R17～R20、R28 | 保存啟用條件、指定工作區寫入範圍、安全預設及失敗揭露可同時成立；來源文字未取得額外操作權限。 |
| 建文、修訂、分支、預覽與發布權限 | S:53–59,89–90,130；`skills/creating-vitepress-post/SKILL.md:14–21`；`skills/managing-article-publication/SKILL.md:14–33`；其 `references/future-actions.md:7–18` | AC-07、13；R15～R16、R31～R32 | 保留既有 owner、來源分支、候選 pin 與動作別授權；探索完成不構成發布或遠端操作權限。 |
| 第五個 canonical 套件、語言例外、有限更新與歷史保存 | S:94–97,117–126,144–146；`docs/adr/0005-physical-product-writing-packages.md:8–26`；`docs/adr/0007-validated-taiwan-writing-language-exception.md:8–16`；`scripts/materialize-writing-skills.py:98–146,254–276` | AC-15～16；R34～R39 | 第五個套件及必要 inventory／policy 更新已明示；三個中文例外、兩個 alias、原始工程技能與凍結證據仍受保護。靜態輸出與真實 host 驗證也已分開。 |

未列為 finding 的關鍵理由：S:57、:84、:94–96、:138 已分別明示工程／文章分流、舊寫作 CONTEXT 規則替換、套件擴充及研究提案取代。不能再把這些預期變更本身認定為契約衝突。

## 證據限制

- 未提供 `skills/managing-article-publication/references/local.md` 的凍結內容；因此僅能確認規格保留該交付契約，無法核對其全部 topic allocation、分支及 ownership 細節。
- 未提供 `scripts/verify-harness-adoption.py` 及其 current-source guard 相依內容；因此無法判定實作時所需 successor 更新的完整檔案集合。
- 未提供 Claude 對應工程技能的凍結內容，也未執行任一 runtime；本報告不宣稱兩個 runtime 的實際觸發、停問或寫檔行為已獲驗證。
