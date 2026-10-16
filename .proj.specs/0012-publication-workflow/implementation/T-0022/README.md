# T-0022：人工 PR 歷史接續

預設行為維持原契約：已同步便回報 no-op；尚有差異時，沒有 automation ownership 的 PR 會阻擋後續流程。

新增的外部核准只允許一筆精確人工合併紀錄。紀錄必須綁定 repository、固定分支、PR 編號、base／head／merge／tree、作者身分與型態，以及另一份獨立核准 receipt。輸入及 receipt 都需要獨立 SHA-256，禁止從候選內容或 PR body 自行推定授權。遠端 API 重新讀回 PR、commit tree 與祖先關係後，才把這一筆標為 manual，從衝突盤點中排除。

這份核准不會賦予人工分支 automation ownership，也不會略過其他 PR。既有精確 bootstrap 與已驗證 owned branch 復原條件仍各自適用；不會 force push、重開已關閉操作、修改舊 PR body 或改寫歷史 receipt。

實際操作入口可額外接收 `--manual-history` 與 `--manual-history-sha256`。此修正只交付本機 Git／公開 controller／重播 API 契約；沒有操作正式 GitHub PR、merge、自動化或部署。T-0016 保持 review，P13 待實際演練。
