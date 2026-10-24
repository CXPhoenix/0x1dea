# T-0027 覆蓋檢查點

本票沿用核准 B01～B11。Codex 原生 15 組、20 輪實際互動已完成，由獨立行為稽核逐案判讀；未發現缺陷，所有對話案例檔案差異為空。Claude 實際呼叫因 OAuth 過期而無法驗證；不更改帳號、不把套件存在報成 host 成功。完整組合回歸、正式 stage-6／7／8 及 ticket 完成判定留待 A～D 批次收尾；目前不是整個 epic 或完整雙 host 驗收。

| Seam | Tests | Measured coverage | Acceptance criterion | Uncovered, and why |
|---|---|---|---|---|
| B01 原生發現／呼叫 | B01-explicit、B01-natural，實際讀取技能與回應 | Codex 通過；舊版找不到技能的 red 已保存 | AC-01/15 | Claude OAuth 過期，行為未驗證 |
| B02 路由與檔案 | code／emotion／proof／specified draft | 四案直接回應，沒有設定訪談或額外筆記 | AC-01/08 | 不推論其他 host |
| B03 起稿 | B03 t1～t2 | 未知／刻意留白受眾仍可直接起稿 | AC-02/03/05 | 不量測文風品質 |
| B04 只聽 | B04 t1 | 僅聆聽回應，無改寫／分析／檔案 | AC-02/08 | 無 |
| B05 改方向 | B03 t3、B05-audience 延續同 session | 改文類與受眾，不重開訪談，保留指定句 | AC-03 | 無 |
| B06 聲音／保護文字 | B06 三輪 | Phoenix 明示／延續／切換其他聲音；保留原句與立場 | AC-04 | 不宣稱作者辨識或品質分數 |
| B07 事實與選擇 | B07-fact、known-source、local-record | 不可得證據留缺口；自行讀 max-age／Age 紀錄判讀 40 秒，未回問作者 | AC-05/13 | 本機 fixture，不是外部 live lookup |
| B08 深入訪談 | B08 兩輪 | 明示訪談才深入，要求開始即起稿，無心理診斷 | AC-05 | 不以問題數配額判定 |
| B09 工程／文章 | B09 mixed | 交付短稿、辨認 renderer 為工程需求，無工具修改 | AC-06 | 不宣稱 renderer 已實作 |
| B10 materializer 公開 CLI | fifth-package＋繼承既有 fixture 回歸 | 23 項通過；原四套件 fixture 21 項亦通過；二次產生穩定、第五套件竄改被拒絕；portable／quick_validate 成功 | AC-14/15 | 靜態格式不代表 Claude host 執行 |
| B11 current／歷史契約 | current counterpart 4 項；原 Phoenix 4 項在固定歷史 main／staging refs；current native | 全部通過；新增精確 successor，沒有改原 runner／斷言 | AC-16 | 全套 Python／Vitest 為最終組合關卡；此處不提前宣告 |

[native-results.json](native-results.json)保留實際輸入、回應、相關本機讀取動作與檔案差異；原始 CLI trace 留在本機並以 SHA-256 綁定，避免把無關工具或私人環境資料送入 PR。獨立稽核先指出改受眾與可取得來源尚缺觀測，補跑同一原生 session 及本機紀錄查驗後確認補足。沒有把未知項目改寫為通過。

第五套件使原 Phoenix 正向測試固定要求的 v2.3 policy／manifest 位元組不再適用。原檔與 runner 完整保留；新 runner 在執行前固定三種歷史脈絡並比對原測試 bytes，不做失敗後回退。原 Phoenix 模組在 `8b2cffab…` main 與 `6fcb277a…` staging 脈絡完整執行；current counterpart 繼承三個原負向方法，另外驗證五套件與原 Phoenix 聲音位元組。缺少歷史本機 named refs 的首跑失敗也已記錄，補齊明定 fixture refs 後四項通過。

保留「先自由聊、按需整理」；B 不暴露 C／D 尚未存在的參照。既有工程技能、文章、資產、root CONTEXT、兩個 alias 與歷史 E1～E8 未改。核准測試表未改，相依票在單一 PR landing 前不標 done。
