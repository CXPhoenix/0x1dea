# T-0007 安全審查

範圍：本次新增的 EncoreTicket、靜態全域註冊及文章使用處。Base／merge-base／HEAD 均為 `f93237b1ed538484f24ed103ef00c7e5ee2e1828`，分支 `tickets/T-0007/encore-ticket`。Committed 與 staged 為空；已審閱 pending 差異、untracked 元件全文及相關規格。

獨立唯讀候選 reviewer 未發現符合 HIGH／MEDIUM、信心至少 0.8 的可利用新增漏洞，因此沒有需要另外進行誤判篩選的候選項目。

- 作者標題與說明使用 Vue interpolation，沒有 `v-html`、HTML 解析或動態執行入口。
- `href` 繫結到原生 anchor。規格限定可信任文章作者提供；本次文章為固定站內路徑，沒有新增遠端輸入來源。
- 靜態 import 與註冊未新增網路請求、權限操作或認證邊界。

排除候選：「未限制 URL scheme」在本次可信任作者來源的邊界內，屬作者原有能力；沒有可追溯的遠端攻擊者控制路徑，因此不列為 URL 注入漏洞。若日後接入不可信任遠端資料，需要重新定義並審查該邊界。

本次為程式碼靜態安全審查，未執行漏洞利用，不代表全專案安全。依技能範圍未做相依套件掃描、DoS、rate limiting 或低嚴重度強化建議。未提交、發布或寫入外部系統。
