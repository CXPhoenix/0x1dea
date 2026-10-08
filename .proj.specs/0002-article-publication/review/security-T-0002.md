# T-0002 獨立安全 review

/root/code_security 按專案 security-review／upstream methodology 唯讀檢查相同凍結 surface 與最終測試 delta。信心 ≥ 0.8 的 HIGH／MEDIUM 候選為 0，沒有需要另做 false-positive filtering 的候選。以下為父整理，非逐字報告。

已追查 JSON／ref 到 Git 參數陣列、Git tree 到一般檔案匯出、精確 ownership／未選文章 dependency 拒絕、完整 receipt 重算與候選 inventory、baseline aliases，以及文章到執行／發布的界線。CLI 沒有建置或外部動作，成功回應都 publishable=false。

排除項目：靜態 Markdown regex 非完整 parser，且 CLI 不執行 build；signatures 可被轉換／短片段規避，但文件披露限制；未宣告／cherry-picked 內容仍需操作者完整枚舉與 ownership；並行本機 writer 的競態在此無並行 writer contract 下未形成可升格的具體 exploit。

最終測試 delta 使用合成 commit-tree 物件與第四 product fixture，沒有新 hook 或產品執行路徑。沒有執行攻擊重現；不涵蓋 dependency scanning、DOS／資源耗盡、低風險 hardening、未來發布或真實候選建置隔離。零候選不代表全站安全。

## 2026-10-08 授權 follow-up 安全 review

/root/code_security 唯讀檢查相同 follow-up 凍結 source／diff／manifest、套件與 lockfile、successor checker／tests、sandbox profile、sentinel probe 與結果。信心 ≥ 0.8 的 HIGH／MEDIUM 候選為 0，沒有需要獨立 false-positive filtering 的候選。

新增 read rule 為 literal `/`，不允許 descendants；network deny 與限定寫入保留，沒有 host 持久安全變更。Dependency 固定版本、lockfile integrity；checker 的 source hashes 為本地可審閱 preservation evidence，不是不可偽造授權或簽章。CLI 未變，publishable=false。

Reviewers 沒有重跑安裝／sandbox／build；官方 registry、ignore-scripts 及 sentinel pass 依實際執行紀錄。單一 sentinel 不證明所有檔案或 IPC／process attack paths 隔離，profile 明確允許工具鏈目錄及全域 metadata 讀取。此輪不含依賴漏洞掃描、完整 sandbox escape audit、DOS 或後續發布。最終 checker／51 harness tests 通過證據由 Spec reviewer 另行補核，初次 failure 保留。
