# 0014 article-discovery：第一輪獨立對抗式審查

日期：2026-10-24（Asia/Taipei）。結論：**尚未通過 stage 3；1 項 P0 未解決，尚不能建立實作 tickets。**

四個面向由四個獨立上下文的 harness-reviewer 唯讀審查，未互閱其他 reviewer 結果。原始快照 40 份，因 reviewer 指出本機證據缺口，於同一輪一致補充 23 份。原 spec、追溯矩陣與 prompt 均未改動。補充不是第二輪，未消耗不同版本的第二次審查。

## 各面向結果

| 面向 | P0 | P1 | P2 | 初始報告與同輪補充 |
|---|---|---|---|---|
| 完整性 | 0 | 3 | 0 | [初始](round-1/completeness.md)／[補充](round-1/supplement-completeness.md) |
| 可驗證性 | 1 | 0 | 0 | [初始](round-1/verifiability.md)／[補充](round-1/supplement-verifiability.md) |
| 契約衝突 | 0 | 0 | 0 | [初始](round-1/contracts.md)／[補充](round-1/supplement-contracts.md) |
| 紅隊 | 0 | 1 | 0 | [初始](round-1/red-team.md)／[補充](round-1/supplement-red-team.md) |

合計 1 筆 P0、4 筆 P1、0 筆 P2。C-R1-03 與 RT-01 指向同一筆記／guard 問題，因此按問題歸納為 **1 類 P0、3 類 P1**；保留兩位 reviewer 各自的原始發現，不以多數票調整分級。

## 問題與最小修正方向

| 問題 | 分級／來源 | 證據 | 最小修正方向 |
|---|---|---|---|
| 公開前檢查寫了處理，未定義最低完成結果 | P0；V-01 | spec.en.md:89、115；AC-13／R32 | 為現有類別明列觸發與最低輸出，或精確指向既有判準；不增加每篇必填問卷 |
| 單一未指定 GLOSSARY 的沿用規則未完整進入驗收 | P1；C-R1-01 | spec.en.md:81、114；traceability.md:37–38 | AC-12／矩陣明列此正常返回情境，避免重新詢問權威 |
| 暫定設定不能升格為作者確認，缺少直接驗收 | P1；C-R1-02 | spec.en.md:45、66、110；traceability.md:26 | 補對話→保存→返回的狀態忠實性案例 |
| ignored 本機筆記仍被 current source guard 盤點 | P1；C-R1-03、RT-01 | spec.en.md:68、143；scripts/publication_current.py:227–248、300–302 | 決定筆記的來源分類／驗證投影或掃描外位置，補保存與更新後的 guard 交集案例；不採 blanket waiver |

## 使用者指定重點的回答

- 過度追問：四份初始報告都認為自由聊、直接起稿、listen-only、未知設定、沿用回答及停止追問有可檢查條文。仍有兩個驗收缺口可能讓正常返回多問一次，或將暫定設定錯認為已定；公開檢查的籠統要求也可能延伸訪談。這是靜態判讀，未觀察實際模型互動。
- 工程／文章分工：契約 reviewer 認為規格已明示狹義 editorial exception，且 skill／工具修改仍保留工程關卡，不構成默默繞過。其餘面向也未提出新的分支／發布權限漏洞；但筆記與 guard 的操作相容性仍須補齊。
- GLOSSARY 按需建立：無術語不建檔、有持久保存才建檔、明示空骨架為例外、比喻不強制定義，均已有規則。
- 既有 CONTEXT 相容：單一 legacy 檔沿用，雙檔權威不明只停詞彙寫入，工程 root 不作 fallback；未發現這些正文規則彼此衝突。單一未指定 GLOSSARY 的 AC 覆蓋仍是 C-R1-01。

## 保留的判讀差異

完整性與紅隊將筆記／guard 交集列為 P1。契約 reviewer 也確認 guard 會讀 ignored files，但認為規格沒有承諾含筆記的工作目錄直接通過，因此不構成不可相容契約。這些不同面向的結論並列保留；本報告不將它升級為 P0，也不以契約面向零 finding 抵銷 P1。後續修訂應明定實際驗證 surface。

## 證據與限制

- [凍結提示](prompt.md)，SHA-256：`3f5d674830cff8f9154503ee589378ebeb7a3ba1175953e350e70b8bebe7526d`。
- [原始 capture](versions/round-1/capture.json)／[補充 capture](versions/round-1/supplement/capture.json)／[完整來源索引](source-index.json)。
- [完整性檢查紀錄](capture-verification.json)／[機器可讀 findings](round-1/findings.json)。
- spec SHA-256：`fbd2e51bd5bc94823232d46af41e61c248403a8a100649a3961e72eee0f034e9`。base＝HEAD＝`6fcb277a9841dfad21d91f79005d39924acd92d2`。
- 原 staged／unstaged patch 為空；四份未追蹤提案內容以 scope-untracked.patch 保存，不以空 Git diff 代表無審查範圍。
- 補充案例實際為 E1–E8；E9 不在 manifest，不宣稱已核對 E9。初始報告列出的其他本機來源缺口由同輪補充補齊。
- 未實作 skill、未執行真實 runtime 行為、未建立寫作筆記或執行 guard 反例。來源盤點的意外後果是靜態程式碼支持的推論，不是重現測試。
- 原始 spec／traceability 保持凍結；沒有進行第二輪、建立 ticket、commit 或遠端交付。依既有規則，修訂後第二輪須沿用同一 prompt；第二輪仍有 P0 應拆分，不能開第三輪。

## 報告呈現檢查

瀏覽器安全政策拒絕 file:// 本機預覽；未繞過限制。HTML 結構、內部錨點及來源完整性已靜態檢查，實際視覺呈現尚未驗證。見 [預覽紀錄](report-preview-status.md) 與 [靜態驗證](report-validation.json)。
