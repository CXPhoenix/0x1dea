# T-0029 先行來源與行為檢查

來源擷取 review-D：base＝HEAD＝merge-base fb9413f1252edafae28a9f4f08b8c1da5024dc20，共 15 檔。Standards 與 Spec 獨立唯讀判讀均為零缺陷。這是先行檢查點，不取代全組合正式審查。

Codex 原生 D 共 13 組、16 輪，跨票 X01 共 4 組、6 輪。獨立行為 reviewer 確認建立／改稿的實際 CLI、既有授權沿用、四類具體公開檢查、表達性不加清單、只聽／直接起稿、不保存，以及 fresh resume／owner 衝突／custom guard 不阻塞獨立正文。補跑版本、日期、引文、因果／一般保證後亦確認無剩餘 P0／P1／P2。

D07 與 rich 公開前測本來已有好結果，保留為回歸，不偽造 red。X01 共用 fixture 的最終快照與 t3 保存當輪讀回分列；實際 web_search 事件不等於取得完整來源回傳。Claude OAuth 過期，行為未驗證。

完整 Python 第一次執行暴露兩個真實整合問題：新證據 .log 被 Git 忽略而未進測試候選樹，以及 live head-reporting fixture 對新版套件清冊仍取 staging 舊身分。修正將兩個新 .log 原封改名 .txt；live fixture 僅對兩個精確清冊採用獨立 main tree 預期值，保留其餘 staging protected checks／全部 assertions。獨立 Standards 與 Spec 診斷確認符合凍結邊界；兩個原失敗案例重跑均成功。沒有改歷史模組或把失敗案例搬往歷史以取得綠燈。完整重跑結果另列最終批次紀錄。
