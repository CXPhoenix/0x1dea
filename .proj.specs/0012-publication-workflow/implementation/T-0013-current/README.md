# T-0013：共同工程基底實作

2026-10-14 已核准具體 M0，完成本機共同工程基底與精確 current successor；測試與獨立審查已完成。
原本的 M0、歷史測試及 validator 保留。[完整覆蓋與限制](coverage.md)記錄實際驗證結果。

main 保留已發布文章；staging 的六個候選單位、50 個文章／資源路徑與既有修訂都保留。
兩份驗證樹使用相同的新工程檔案，只有既有 validator entrypoint 被替換為轉接層。
兩個原始版本都封存並以固定 Git commit／SHA-256 載入，不執行候選程式碼。

實作分支：`tickets/T-0013/common-engineering-baseline`，獨立 checkout：
`/private/tmp/0x1dea-T0013`。使用方式與信任邊界見 `docs/publication-baseline.md`。

這是本機工程驗證，不是 main／staging merge、文章發布或部署證據。T-0013 維持 review；
真正落地前不標為 done，後五票仍依原阻擋關係等待。未修改部署設定，也未執行 merge。

[程式碼審查](../../review/code-T-0013-current.md)與[安全審查](../../review/security-T-0013-current.md)均無未解 finding。
`source.patch` 保存本次工程來源；精確完整邊界以 implementation checkout 的
`maintenance/publication-workflow/engineering-v1.json` 為準。先前 reviewed-delta 是測試前 checkpoint，
不是包含審查後紀錄的最終 map。

[最後本機驗證](final-verification.json)記錄兩份 target 的 native CLI 結果及逐候選身分檢查。
加入此紀錄後重新捕捉有限 successor，並再次完成相同驗證；該次輸出留在本機工作目錄，
避免證據檔案包含自身 hash。
