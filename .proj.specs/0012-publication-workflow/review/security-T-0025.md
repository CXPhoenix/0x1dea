# T-0025 獨立安全審查（核心範圍）

Base／HEAD／merge-base 8baa132eec03336f6776ea45b0c8e4a6889c3c74；17 份固定 pending/new 快照 hash 全符。新增 HIGH 0、MEDIUM 0，沒有 confidence ≥0.8 的候選需要獨立誤報排除。

可信程式固定十個 mode／SHA-256，與 immutable bf6f872、payload 與 policy 相符；缺項、改寫或重釘選 policy 不能自行授權。例外只限精確名稱，其他 writing 路徑仍受保護，沒有 prefix 放行。candidate 檢查全部 execute bit，沿用 regular／parent symlink 與內容比對；角色、歷史、Git 邊界及 publishable=false 保留。

寫作內容是指定來源的文字移植，沒有新執行或遠端輸入介面。本輪唯讀程式分析，沒有跑測試；完整 runner／legacy 執行及後續 reports／receipts 尚未覆蓋。未作相依套件、DoS／rate limiting 或低風險強化稽核。

## 最終證據補審

獨立安全審查核對 53 檔 mode／SHA、未變的核心程式／測試與十檔 payload，新增 HIGH 0、MEDIUM 0，沒有需另作誤報排除的候選。QA bundle 大小、hash、兩個 QA refs 與公開 prerequisites 符合，唯讀 bundle verify exit 0，沒有匯入 refs；重建指引限定獨立 clone。失敗／成功 log 分開保存且 receipt hash 符合，沒有把 QA 成功當成實際落地。常見憑證格式掃描沒有命中，這不是完整秘密偵測。實際 target landing、遠端 tree 與後續驗收仍待觀察；其他排除範圍沿用核心審查。
