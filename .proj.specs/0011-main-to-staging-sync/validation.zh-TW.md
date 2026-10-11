# T-0011 本機驗證

最終完整測試為 87 個 Vitest（8 個檔案）、95 個 Harness 與 16 個 article publication 測試，全部成功且沒有 skip。完整 Python 執行前後五個相關來源的 SHA-256 相同；最終 public verifier 使用同一版來源並回傳 exit 0。lint、結構檢查、materializer --check 與隔離的 staging build 也都回傳 exit 0。

實際完整回歸找出額外原因：在本票分支建立的 disposable clone 有 origin/staging，卻沒有本機 staging。原本 landing evidence 檢查因此拒絕完整的 receipt、approval 與 commit object。回歸先重現失敗，再確認只有本機 ref 不存在才使用遠端對應 ref；本機 ref 損壞或 ancestry 錯誤不會改試另一個 ref。相關失敗、修正與最終執行紀錄全部保留。

六個衝突已解完；對 staging 的 1988 個原有追蹤項目中，1985 個保持相同，只有規格列出的三個整合來源修改。111 個 blog 項目、五篇候選文章、資源、用電文章審閱提示與 listing 均保持相同。main 的 123 個新增項目全數保留，main release helper 與其 13 個測試保持原始位元組；歷史 hash、fixture、manifest、receipt 與 package/lockfile 未改寫。

瀏覽器驗證使用本機隔離的 CF_PAGES_BRANCH=staging build：listing 顯示一張正確卡片與日期、描述，Enter 可進入用電文章並看到 staging 審閱提示。桌面 1440×900、行動視窗 390×844 的亮色與暗色模式均沒有文件橫向溢出。行動裝置 clientWidth 為 375，原生截圖為 375×812；兩者與視窗設定分別記錄，不混稱相同尺寸。VitePress 實際目的地含既有 .html 副檔名。

build 的第一次 Corepack 查找及第二次連結 cache 寫入都在 sandbox 內遭拒，沒有安裝套件或寫入外部目錄。改用已安裝的 cached pnpm 與 disposable cache 後成功；四個隔離探測均符合預期。既有 FontAwesome 樣式表 404 已註記，網站來源保持相同。

獨立規格第二輪四軸皆無發現；獨立 Standards 與 Spec 審查的 P0／P1／P2 均為 0，安全審查 HIGH／MEDIUM 均為 0，完整結果另存 review/。這些結果涵蓋本機 CLI、測試、build 與瀏覽器表面，不表示遠端 CI、部署或正式站已驗證。票券維持 review，PR 必須開到 staging 並保持未 merge；實際交付狀態由交付後 Git/GitHub 回讀確認。

詳見 [coverage-report.md](coverage-report.md)、[implementation-notes.md](implementation-notes.md) 與 evidence/ 的原始紀錄。
