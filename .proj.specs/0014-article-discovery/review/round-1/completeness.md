# Round 1：完整性

Reviewer：`/root/ad_completeness`；獨立上下文、唯讀。父執行緒保存以下回傳結果，未更動其分級。

完成 round 1 Completeness（完整性）審查：**P0：0、P1：2、P2：0**。兩項發現都是正文需求尚未完整落到驗收條件；可於 ticket 內補齊，不構成目前的 P0 障礙。

審查使用 capture.json 指定的 frozen .txt 副本。40 份副本的大小與 SHA-256 均符合 manifest；四份新增檔案的完整 patch 均與副本相符。提供的 base／HEAD 同為 `6fcb277a9841dfad21d91f79005d39924acd92d2`，staged／unstaged patch 均為空。全程唯讀。

## C-R1-01｜P1｜單獨存在、未另外指定的 GLOSSARY.md 缺少明確驗收落點

- 原始位置：`.proj.specs/0014-article-discovery/spec.en.md:81`、`:114`；`.proj.specs/0014-article-discovery/traceability.md:37`、`:38`。
- 需求組合：既有寫作工作區 × 唯一存在且未另外指定的 GLOSSARY.md × 返回／讀取／更新詞彙。
- 相關 AC／row：AC-12、R29、R30。
- 預期要求：D7 明定沒有指定權威時，沿用唯一既有的文章 GLOSSARY.md 或 legacy CONTEXT.md。
- 證據：AC-12 明列的是「single legacy article CONTEXT.md or designated glossary」。R29 只列 legacy CONTEXT.md；R30 列指定權威、兩檔競爭及無效／遺失指定，沒有納入「唯一、未指定的 GLOSSARY.md」。
- 具體反例：工作區已有 PROJECT.md 與唯一 GLOSSARY.md。作者要求延續寫稿，agent 卻要求作者重新指定詞彙權威。這違反 D7 的直接沿用規則，但現有 AC-12／R29／R30 的明列案例可能仍全部通過。
- 影響：漏掉正常返回情境，讓本來無須決策的詞彙權威問題增加一次追問。
- 最小修正：將 AC-12 明列為「單一、未指定的文章 GLOSSARY.md 或 legacy CONTEXT.md，以及有效指定的 glossary」，並補入 R29／R30 的相應組合。沿用既定規則即可，不需要再向作者確認政策。
- 不確定性：實作者可能把 AC-12 的 glossary 寬鬆解讀為涵蓋所有既有 glossary；但其 designated 限定與矩陣列舉並未明確涵蓋此情境。這是驗收覆蓋缺口，並非正文完全沒有規則。

## C-R1-02｜P1｜暫定建議與作者確認的區別未形成明確驗收條件

- 原始位置：`.proj.specs/0014-article-discovery/spec.en.md:45`、`:66`、`:110`；`.proj.specs/0014-article-discovery/traceability.md:26`。
- 需求組合：暫定建議／agent 推論 × 決策狀態與確認來源 × 對話整理、保存與跨次沿用。
- 相關 AC／row：AC-04、AC-08、R18；目前沒有直接對應此狀態區別的 row。
- 預期要求：D3 明定暫定建議須保持暫定，推論不能記成作者確認；D5 要保存相關的 confirmed／tentative settings。
- 證據：AC-08 驗收相關脈絡的保存、沿用與 readback；R18 同樣要求保存相關 brief/context。兩者沒有明列確認狀態必須忠實保留。AC-04 保護用詞、立場與協助限制，也沒有直接驗收「不得捏造作者已確認」。
- 具體反例：agent 提出「這篇可以暫時寫給初學者」，作者尚未回應便要求先寫一段。保存時，agent 將它記為「作者已確認：受眾為初學者」，且 readback 與報告完全一致。檔案保存成功並不足以驗出這項 D3 違規。
- 影響：返回寫作時，推論可能被當成已定選擇，造成錯誤沿用、限制作者方向，或衍生不必要的重新確認。
- 最小修正：在 AC-08 或 AC-04 增列：保存與重用時保留 confirmed／tentative／unknown 等相關狀態，不得將建議、推論或未答覆事項升格為作者確認；補一列對話→保存→返回的追溯組合。
- 不確定性：「相關脈絡」可以被解讀為包含正確狀態，但目前沒有明示的 pass/fail 落點。正文足以指導實作，因此列 P1。

## 覆蓋表

| 檢查範圍 | 對應範圍 | 完整性結論 |
|---|---|---|
| 入口及直接起稿／修訂繞過 | D1；AC-01；R01–R02 | 有覆蓋 |
| 自由聊、抒發、listen-only、未知目的與受眾 | D2–D3；AC-02–05；R03–R12 | 有覆蓋；不要求固定表單或完整訪談 |
| 返回、改方向、重複摘要與協助強度 | D2–D3；AC-03–05、08 | 有沿用與停止追問規則；確認狀態缺口見 C-R1-02 |
| 純文章、混合工具需求、skill 本身的工程流程 | D4；AC-06–07；R13–R16 | 有覆蓋；工程需求不阻擋無關 prose |
| 無術語、首個術語、未解決詞義、自訂用法與比喻 | D6；AC-09–11；R21–R28 | 有覆蓋 |
| 保存關閉／啟用、artifact-only、明示 scaffold | D5–D6；AC-08–09；R17–R23 | 有覆蓋 |
| legacy CONTEXT、單一 GLOSSARY、兩檔與指定失效 | D7；AC-12；R29–R30 | 單一未指定 GLOSSARY 的驗收缺口見 C-R1-01 |
| 工程 root context、來源內指令、路徑與寫入權限 | D4、D6–D7；AC-10–12；R25、R28–R30 | 有覆蓋 |
| 工作區、穩定 key、碰撞、公開／ignored、readback 失敗 | D5；Further Notes；AC-08；R17–R20 | 有覆蓋；沒有把忽略規則當成保密保證 |
| 公開準備與既有交付授權 | D8；AC-07、13；R16、R31–R32 | 有覆蓋 |
| 第五套件、有限政策更新、歷史保存與 native-host 證據 | D9；AC-14–16；R33–R39 | 有覆蓋；scenario families 明確不是已核准測試或執行結果 |

未發現完成本面向所必需而未提供的證據。本報告只判斷凍結規格的完整性；沒有執行新 skill、runtime 行為測試或使用性驗收，也不裁定其他審查面向。
