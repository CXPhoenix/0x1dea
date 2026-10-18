# T-0019：保留歷史 CLI 的三檔驗證契約

這是既有 T-0019 的 A1／A3、PA-06 與 K1 修補，沿用原分支及測試分配。歷史斷言、oracle、不可變 receipt、M0 歸屬與候選內容均保留。已授權的 main PR #29～#31 都已合併；追加修補 PR 仍需新的明確 merge 授權。staging 同步須先等修補實際落地 main，再核對同一批 commit。T-0019、T-0016 維持 review；P13 尚未執行，正式自動化與部署設定未變動。英文說明見 [README.en.md](README.en.md)。

## 原因與修正

#29 在分流歷史契約之前匯入 `publication_workflows`。舊 CLI fixture 依契約只疊入三個檔案，沒有這個新模組，因此在原本的正反向檢查執行前就發生 `ModuleNotFoundError`。main 的即時測試沒有 staging 保留的原 reconciliation 模組，所以先前僅測 main 時漏掉此問題。保留檔案清單見 preservation 紀錄。原 staging 完整測試產生 35 筆同原因的失敗紀錄；發布測試及原樣的 PR #22 測試成功。原歷史測試未修改。

修正後，只有可信 CONTROL 具備目前版本的 policy 時，才註冊 workflow CLI 參數與相依模組。完整參數解析仍先於目標 Git 查詢；目標契約沿用原 policy／祖先關係判準，目前版本目標搭配不完整 CONTROL 會明確拒絕。沒有在驗證失敗後切換契約。新增的 PA-06 公開 CLI 回歸重現原三檔 fixture，並確認舊入口拒絕新參數、目前版本的 help／未知參數提早結束時不查詢目標 Git。

第一版修補恢復了歷史正向案例，卻把 Git 查詢移到完整參數解析之前。安全審查提出尚未確認的 remote-helper 疑點；PATH 探針只證明查詢順序改變，未證明可利用的攻擊。該版本已替換，兩次未完成的長跑明確中止（exit143），留在 attempts，不列為最終成功證據。最終版本保留原解析順序，移除新增的觸發面。

## 隔離 repository 的 Git 物件問題

相同最終程式碼曾在 staging 巢狀 fixture 遇到 Git exit128。最小重現取得 `ignoring alternate object stores, nesting too deep`：暫存環境累積六層共用 repository，造成四筆發布失敗及十筆原樣 fixture 失敗；95 項 Harness 已成功。處理方式只補齊隔離預演自己的物件庫，經 fsck 確認後移除 alternates。前後 HEAD、tree、main／staging refs 與乾淨狀態完全相同，未修改產品、測試、runner 斷言或歷史 commit。原先失敗的 PA-02／PA-06 已成功，隨後完整重跑原套件。環境失敗與物件身分紀錄另行保留，不視為產品修正。

## 驗證範圍與證據

最終 main Python 209 項、保留候選的 staging 預演 Python 238 項均完整成功，分開留存原始結果。staging 使用隔離合成投影，尚未落地遠端，也不是 Actions／P13 證據。原始 red、最終結果及實際 deny-default build receipt 均保留。先前尚未提交 merge 的 native 拒絕屬祖先關係與前置設定診斷，不列為成功。

最終版本另跑 main unit 54 項、staging unit 87 項、兩邊 lint 與 VitePress build，結果均成功；完整 Python 流程也執行實際隔離 build。此修補僅涉及 Python 與管理紀錄，沒有宣稱瀏覽器驗證。
