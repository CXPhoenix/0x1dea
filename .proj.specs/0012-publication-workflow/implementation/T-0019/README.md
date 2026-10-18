# T-0019：workflow 有限准入

這張票讓核准的 workflow 經過共同工程 policy、prepare 與原生驗證；本機投影只複製檔案，不執行 workflow，也不代表可以發布或啟用正式自動化。

未提供核准紀錄時維持預設拒絕。提供紀錄後，control 實際存在的 `.github` 檔案必須恰好等於核准集合；其他 workflow、CODEOWNERS、symlink、submodule 或不同模式／內容都會拒絕。

核准紀錄放在 control 與候選目錄之外，由可信呼叫端獨立提供預期 SHA-256、repository 與完整 main commit。紀錄欄位為 `version: 1`、`repository`、`main`、`policies`（main／staging 各自核准的 policy SHA-256）、`roles: [main, staging]`、非空白 `approval` 及 `workflows` 精確路徑對應表；每個 workflow 只有 `mode` 與 `sha256`。不接受額外欄位、重複 JSON key 或萬用字元。

prepare、verify 與原生驗證提供同一組四個參數：`--workflow-admission`、`--workflow-admission-sha256`、`--trusted-repository`、`--trusted-main`。四個都須由可信管道提供，不能從候選檔案讀出後自行採信。紀錄中的每個 workflow 也須存在於指定 main 的 Git tree，且其模式與內容一致。

投影會保留核對結案紀錄所需的可信 main／staging refs，另以本機 `refs/publication/workflow-main` 綁定投影來源。main ref 或 policy 改變後，舊紀錄會失效。這些本機 refs 不構成 GitHub 權限或遠端保護證據。

目前未在正式專案放入任何 active workflow。P13 與實際落地仍待各自的驗證／核准；本票的測試與審查進度見 coverage.md。
