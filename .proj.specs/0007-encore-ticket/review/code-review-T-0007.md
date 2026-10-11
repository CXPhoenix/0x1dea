# T-0007 變更審查

範圍為本次尚未提交的元件、全域註冊、文章推薦替換、測試、使用指南及追蹤文件。Base、merge-base 與 HEAD 均為 `f93237b1ed538484f24ed103ef00c7e5ee2e1828`；分支 `tickets/T-0007/encore-ticket`。Committed 與 staged diff 為空；pending 與 untracked 的完整內容均已擷取到本機凍結封包。原有圖說修改以 task-entry 內容作為基準，不列為本次修改。

## Standards

獨立唯讀 reviewer 結論：文件化標準違反 0 項，主觀 code smell 0 項。

元件使用明確 props、單一原生連結與 CSS module；註冊延續現有 hook。文章變更限於推薦段落，指南使用台灣繁體中文並包含有／無說明兩種用法。測試驗證公開行為，未綁定 CSS class hash。已揭露標準 lint、結構與保存檢查限制，未誤稱全數通過。

## Spec

另一獨立唯讀 reviewer 結論：P0／P1／P2 為 0／0／0。

E1 的 props、文字跳脫、省略說明與獨立實例符合規格；E2 註冊與文章文案／目的地保留；E3／E4 的結構、主題、窄版與焦點樣式符合靜態要求。Reviewer 獨立比對文章，確認除了唯一推薦段落替換，task-entry 內容完全保留。指南含兩種 props 範例。

## 證據限制

兩位 reviewer 使用同一凍結封包，未修改檔案、未重跑測試，也沒有將建置推論為瀏覽器驗收。瀏覽器結果由主代理另行完成，見 `browser-evidence.md`。E6 的完整 lint、結構／materializer 與保存檢查未通過，詳見 coverage-report.md。產品程式碼與擷取時的 hash 在交付前再次比對；證據文件的後續補寫另行列明。

後續依使用者明確授權還原缺少的工具後，完整 lint、61 個測試與 build 已通過；套件宣告、lockfile 與受審產品程式碼未變更。結構／materializer 與歷史保存檢查限制仍記錄於 coverage-report.md。
