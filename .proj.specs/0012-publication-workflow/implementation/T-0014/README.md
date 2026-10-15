# T-0014：指定文章 v2 實作與證據

本機隔離分支 `tickets/T-0014/v2-selected-candidate`，base/main `001b26f`、staging
`0357835`。目前 30 項 public Git/CLI 測試、54 項網站 unit、build/lint/structure/
materializer 通過。實際 VitePress 隔離 build 的外部讀取／寫入／網路探針均遭拒；
相鄰 receipt 分別記錄 build、完整 source/產物與本機 ready，核准資料為合成 fixture，
不代表實際網站預覽或作者核准。

原 v1 程式與 assertions 保留。新增 source 准入、完整 registry、shared patch、依賴、
精確 legacy 原始／重建綁定、alias 完整性及過期拒絕，不搬移實際 legacy 候選。
獨立審查提出的 alias 新增／刪除、empty candidate ancestry 與 promisor/lazy-fetch
問題皆已有公開 CLI 的修正驗證；完整 current／historical runner 與最終審查另記。

此票尚未落地，不能標記 done。沒有 commit、push、PR、merge、部署設定或實際
候選內容修改。所有 Git fixture commits 使用 plumbing，沒有使用者分支 commit。
