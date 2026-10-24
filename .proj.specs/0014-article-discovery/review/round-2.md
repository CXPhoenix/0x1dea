# 0014 article-discovery：第二輪獨立對抗式審查

日期：2026-10-24（Asia/Taipei）。結論：**四個面向均為 0 P0、0 P1、0 P2，規格通過 stage 3 審查關卡。**

這是規格判讀，並非 skill、current guard、網站或實際對話已驗收。第一輪原始結果與來源快照完整保留。

## 四個獨立結果

| 面向 | P0 | P1 | P2 | 報告 |
|---|---|---|---|---|
| 完整性 | 0 | 0 | 0 | [完整報告](round-2/completeness.md) |
| 可驗證性 | 0 | 0 | 0 | [完整報告](round-2/verifiability.md) |
| 契約衝突 | 0 | 0 | 0 | [完整報告](round-2/contracts.md) |
| 紅隊 | 0 | 0 | 0 | [完整報告](round-2/red-team.md) |

四位 reviewer 使用新的獨立上下文，未互讀結果；原封不動使用第一輪 frozen prompt。63 份來源中只更換 spec、traceability 與 README 三份提案版本，其餘 60 份周邊契約維持相同 bytes。沒有以多數票調整分級，未收到需要作者裁決的互斥 finding。

## 第一輪問題的規格修正

| 第一輪問題 | 本輪修正 | 對應驗收 |
|---|---|---|
| V-01／P0：公開檢查無最低結果 | D8 分四個既有類別定義觸發與具體段落／資源結果；可具名列缺口，但不得冒充已驗證或可發布。沒有觸發的類別不增加問卷 | AC-13；R32、R41–R44 |
| C-R1-01／P1：單一未指定 GLOSSARY 漏驗收 | 明列直接沿用，不再追問指定、不建立競爭副本 | AC-12；R29 |
| C-R1-02／P1：暫定升格作者確認 | 對話→保存→續寫均維持暫定、確認、未知、刻意留白；未答建議不得升格 | AC-08；R18、R40 |
| C-R1-03＋RT-01／同一類 P1：本機筆記與 guard | D5a 定義受限本機產物形狀；排除前驗名稱／物件／Git 追蹤與預期來源碰撞，並增加保存後的 guard 交集 | AC-17；R20、R45–R48 |

修訂版共 17 項 AC、48 列追溯；第一輪歷史 1 筆 P0／4 筆 P1 的原分級不被回寫。本輪結論是修正已進入規格，且獨立 reviewer 未再提出 finding，不是已實作修復。

## 本機筆記的相容方式

- 唯一預設命名空間：`.proj.writing/<article-key>/`。
- 只接受直接位於工作區的 PROJECT.md、GLOSSARY.md，以及相容用 legacy CONTEXT.md；一般、不可執行檔案，root／workspace 為實體目錄。
- 可變動內容作為本機產物，不納入工程來源 identity；排除前拒絕 HEAD／index 已追蹤或 trusted expected-inventory 碰撞。
- 額外檔名、巢狀目錄、連結、非一般物件與可執行筆記仍拒絕；命名空間外未核准來源維持拒絕，不全面放行目錄。
- 自訂位置不自動取得豁免。若阻擋 current guard，保留筆記、指明 blocker、繼續正文，不為通過而搬移／刪除或擴張放行。
- 後續須在可丟棄 current main／staging 驗證保存前、建立後、更新後都保留角色與非筆記來源身分；本輪沒有實作或執行它。

## 證據與剩餘關卡

- [凍結提示](prompt.md)：SHA-256 `3f5d674830cff8f9154503ee589378ebeb7a3ba1175953e350e70b8bebe7526d`，與第一輪完全相同。
- [第二輪 capture](versions/round-2/capture.json)／[跨輪差異](versions/round-2/round-1-to-round-2.patch)／[修正對照](round-2/revision-map.md)。
- [機器可讀結果](round-2/results.json)／[文件檢查](versions/round-2/document-validation.json)。
- 審查來源 spec SHA-256：`1dd95c9e0883a7f29d2512ad53449463fb56edd1d92310364c9a2fe73d21e7c4`；Git blob：`aa08308eb23756514ebc770e6a4719c60388d83d`。
- [繁中稽核譯文](../spec.zh-TW.md)於通過後產生並綁定上述 blob，英文仍是實作依據；譯文不是另一輪審查的證據。
- 限制：未執行 skill、materializer、native guard、fresh-host 行為或使用者驗收；未配置 ticket、未實作或變更遠端。契約報告列出未逐行稽核的額外相依檔；未把缺少執行證據當成通過。
- 下一階段是拆票與作者核准；實作前仍須核准測試計畫表。兩輪已用完，沒有第三輪。
- HTML 沿用先前已知的 file:// 預覽政策限制，未嘗試替代瀏覽器或間接路徑；只做靜態結構／內部連結檢查，視覺呈現未驗證。
