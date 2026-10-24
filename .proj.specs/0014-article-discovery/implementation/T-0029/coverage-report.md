# T-0029 覆蓋報告

沿用核准 D01～D08 及共用 X01。Codex 原生公開準備／交付 13 組，加上跨票 4 組，共 17 組、22 輪；獨立行為 reviewer 已判讀，沒有剩餘 P0／P1／P2。Claude OAuth 過期，行為未驗證。完整批次結果及正式審查見最終批次紀錄。

| Seam | Tests | Measured coverage | Acceptance criterion | Uncovered, and why |
|---|---|---|---|---|
| D01 建立／改稿 CLI | D01-artifacts＋獨立讀回 | 原 CLI 成功建立合成文章及資產；只改指定舊文句子，建立時間與圖片參照未變；未建筆記 | AC-07/16 | pnpm 啟動器受暫存 socket 限制，以 node --import tsx 執行同一原 CLI 成功；不代表實際作者文章／網站驗收 |
| D02 交付分工 | D02-routes 三輪 | 沿用既有建立、維護、預覽及選定準備 owner；重用已有本機權限，沒有衍生遠端授權 | AC-07/13 | 不宣稱已預覽、發布或 rollback |
| D03 事實 | facts／unavailable／variants | 具體段落核對數字、引文、版本、日期、因果及普遍保證；不可得來源具名留缺口 | AC-13 | 合成 fixture 查驗；不冒稱 live 產品已查證 |
| D04 外部素材 | materials：Q1／I1／C1 | 各素材列來源、已知使用條件或精確缺口；引註不等於許可 | AC-13 | 不作法律結論或取得權利 |
| D05 第三人範圍 | unknown／settled | 未知只問必要的公開範圍；已有匿名轉述決定直接沿用 | AC-13 | 不推論當事人同意 |
| D06 閱讀支援 | media／supported | 圖表、表格、音訊、影片對應具體說明或缺口；已充分解釋及裝飾素材不加問題 | AC-13 | 編輯檢視，不是渲染網站或完整無障礙測試 |
| D07 條件啟動 | feeling／before／rich before | 心情抒發、無觸發類別不加問卷；缺口辨識不宣稱發布就緒 | AC-13 | before 兩案原本即有良好結果，明列回歸，不捏造 red |
| D08 雙套件與保留 | draft／listen＋materializer/current／批次檢查 | 直接起稿、只聽不改寫及不保存均保留；條件參照在兩套件完整 | AC-14–16 | 套件靜態成功不等於 Claude 執行成功 |
| X01 跨票 | start 三輪→fresh-public；conflict；custom-blocker | 自由聊→起稿→稍後保存首詞→新 session 改文類；保留指定立場、暫定建議。詞彙衝突或 custom guard 不阻止獨立正文 | AC-01–17 對應子集 | 共用 fixture 最終快照不是保存當輪狀態；JSON 分列實際 t3 讀回與最終快照 |

[native-results.json](native-results.json)保存輸入、回應、相關動作與合成檔案讀回。原始 trace 在本機以 SHA-256 綁定；不提交無關私有環境資料。X01 的原生 web_search 確實執行 AWS 查詢，但事件未提供完整搜尋／頁面回傳，不能據此宣稱完整來源查驗。custom 主目標保存前 exit0，保存後 exit1 精確列出自訂筆記；原筆記與 policy 未改，正文仍交付。其餘來源案例均標明 fixture／本機範圍。

D 的條件整合承接 B／C 已觀測 red，不把本來成功的自由表達或公開準備輸出改稱失敗。沒有新增作者筆記後端、預設清單、文風分數或發布就緒旗標。核准測試表與永久相依不變。

## 批次收尾補件

完整組合 Python 287 項及 Vitest 54 項已實際成功；正式 Standards／Spec／Security 來源審查無剩餘發現。前文的 processing／等待批次關卡為先行檢查點，已由[批次紀錄](../batch/README.md)與 ticket review 狀態取代。Claude 行為未驗證與其他範圍限制仍有效；尚未 landing。
