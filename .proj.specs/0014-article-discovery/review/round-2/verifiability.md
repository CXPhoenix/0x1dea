# Round 2：可驗證性

Reviewer：`/root/ad2_verifiability`；獨立上下文、唯讀。父執行緒保存回傳結果，未更動其分級。

Verifiability 審查完成：**未發現 P0、P1 或 P2 finding**。此結論僅表示 round 2 規格的驗收條件具有可觀察判準，不代表技能行為、原生主機、CLI 或可用性已驗證通過。

審查版本為 review/versions/round-2；base／HEAD 均為 `6fcb277a9841dfad21d91f79005d39924acd92d2`，branch 為 staging。63 份 frozen source 的 SHA-256 與位元組長度均符合 capture.json；prompt SHA-256 為 `3f5d674830cff8f9154503ee589378ebeb7a3ba1175953e350e70b8bebe7526d`。staged／unstaged patch 均為空，新增內容由 supplied addition patch 與 frozen source 納入範圍，未因 Git diff 為空而排除。

| 覆蓋範圍 | 原始位置、AC／矩陣 | 可觀察判準與審查結果 |
|---|---|---|
| 入口、直接起稿、非寫作請求 | spec.en.md:29–30,122；AC-01；R01–R02 | 由請求與實際 routing／action trace 判定是否誤加 discovery 問卷。 |
| 自由聊、抒發、listen-only、未知目的與受眾、混合文類 | spec.en.md:35–44,123–124；AC-02–03；R03–R07 | 可檢查是否先交付指定協助、是否重寫／評價，以及是否將設定變成起稿前提。作者刻意留白是有效輸入狀態。 |
| 提問、反覆摘要、深入訪談、返回與改變方向 | spec.en.md:35–39,45,126；AC-05；R10–R12、R40 | 問題須具有下一步、語意或事實相依；已回答問題不得重問，開始寫作要求有明確轉換行為。可從多輪輸入差異與 transcript 判定。 |
| 作者限制、保護文字、Phoenix 觸發 | spec.en.md:44–46,125；AC-04；R08–R09 | 可對照明示約束、原文與產出，辨認虛構經驗、立場改動或未觸發的風格套用。 |
| 純文章、混合工具修改、技術需求與交付權限 | spec.en.md:50–60,109,127–128；AC-06–07；R13–R16 | 可由建立的 artifacts 與 action trace，判斷是否誤建工程文件、是否繼續不受影響的文字，以及是否超出原有交付權限。 |
| 保存開關、既有工作區、key／碰撞、保存失敗 | spec.en.md:64–68,129,164；AC-08；R17–R20、R40 | 授權脈絡、前後檔案、readback 與回報可交叉核對；暫定、已確認、未知、刻意未設定的狀態不可在保存／續寫時被提升。 |
| 無術語、第一個可重用術語、未解定義、作者用語、一般隱喻與 scaffold | spec.en.md:81–86,130–132；AC-09–11；R21–R28 | 建立門檻、作者明示例外、resolved／pending 存放位置，以及來源定義與作者用法的區分均可從請求與檔案內容核對。 |
| 單一／雙重 glossary、有效／缺失／無效指定、工程 CONTEXT 與嵌入指令 | spec.en.md:86,90–93,133；AC-11–12；R28–R30 | 可由現存檔案、指定與授權判定沿用或暫停詞彙寫入；無須先強迫解決不影響其他文字的問題。 |
| 公開前查核與可接受的未解結果 | spec.en.md:99–108,134；AC-13；R31–R32、R41–R44 | D8 表格已指定觸發、具體段落／素材、來源結果或具名缺口。泛泛提醒明確不算完成；未解結果也不能宣稱已驗證或可發布。 |
| 第五個 canonical 套件、有效文件與歷史保存 | spec.en.md:113–116,135–137,163–168；AC-14–16；R33–R39 | 可利用有效指引盤點、實體檔案／metadata／連結檢查、重複生成、故意修改產物與精確 identity audit 判定。靜態生成與 fresh-host 執行明確分開。 |
| notes／current guard、main／staging、拒絕案例與自訂位置 | spec.en.md:72–77,138,165；AC-17；R45–R48 | 有有限 namespace／檔名／物件形狀、HEAD／index／trusted-inventory 碰撞與 namespace 外額外來源的拒絕規則；正常路徑要求三次 native verification 比較相同角色與非筆記來源身分。 |
| 驗證方法與測試核准界線 | spec.en.md:142–147；traceability.md:62–68 | scenario family 未冒充已核准測試或執行結果；未來 ticket 必須列出具體輸入、預期輸出與 runtime 範圍。缺少實作測試不是本階段的驗收判準缺口。 |

對照反例後，未形成 finding：已授權保存不等於作者接受未回答的建議；公開查核列出具體缺口不等於缺口已解決；產生兩份 runtime 套件不等於兩個主機行為已通過；.gitignore 也不等於 current guard 已排除筆記。規格均明示上述區別。

未修改檔案、未讀取其他 reviewer 結果、未執行新技能或測試。就此指定面向，未遇到阻礙判斷的缺失證據；實際主機結果、具體 ticket 測試表與實作驗證仍屬後續證據。
