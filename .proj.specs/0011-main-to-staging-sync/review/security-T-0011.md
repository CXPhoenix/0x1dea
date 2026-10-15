# T-0011 Security Review

新增 HIGH：0；新增 MEDIUM：0。未發現 confidence ≥ 0.8 且具體可利用的新增安全漏洞；沒有候選需要另行執行獨立誤判過濾。

## 審查範圍

- Reviewer：獨立 sync_security，唯讀。
- Worktree：`/Users/phoenix/.codex/worktrees/main-to-staging-sync/0x1DEA`
- Branch：`tickets/T-0011/main-to-staging-sync`
- Base、merge-base、HEAD：`4005ee45f2f3267a8b53ce24fa97af7b49cfb144`
- Pending merge parent：`eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a`
- Frozen packet：`/private/tmp/0x1dea-sync-code-review`
- Manifest SHA256：`b27c3993ad4550a73899b8e2095165bff2a73306adeecf25ab25d4a281b583ac`

已核對 packet 的 207 個檔案，大小與 SHA256 全部符合 manifest。Committed diff 為空；審查對象包含 staged merge diff、未追蹤的 T-0011 規格與證據。Unstaged diff 與 unmerged index 均為空。

已閱讀專案 AGENTS、runtime、安全審查規範、完整 upstream methodology 與 T-0011 spec。重點涵蓋三個既有來源修改，以及匯入的 main verifier helper、release tests 與相關 guard 上下文。兩個 main 來源另以 pinned main Git object 比對，確認逐位元組相同。

## 排除的疑慮與證據

| 疑慮 | 要求與證據 | 判定、影響與不確定性 |
|---|---|---|
| Dispatcher 失敗後轉用較寬鬆契約 | `scripts/verify-harness-adoption.py:16–41`：四個確切 reconciliation records 優先；main scope 包含 HEAD 存在性查找；選定 guard 後沒有捕捉驗證失敗並重試其他 guard。 | 未發現新增 fallback bypass。選擇訊號本身不授權來源，後續仍執行 guard 的固定來源與歷史檢查。屬程式碼推論，未另建攻擊 fixture。 |
| `origin/staging` 查找放寬 landing 判定 | `scripts/verify-harness-adoption.py:100–116`：仍要求 receipt、approval、有效 commit 與 ancestry；只有本機 ref 查找回傳 1 才選 remote ref。查找錯誤或本機 ancestry 錯誤直接拒絕。`tests/harness_adoption/test_tracker.py:146–196` 保留相對應負向案例。 | 未發現新增授權繞過。可任意改寫本機 Git metadata 的攻擊者原本即可改寫本機 staging ref；此修改未建立新的權限邊界。Remote-tracking ref 也不構成即時 GitHub 授權證明，程式碼未宣稱如此。 |
| CODE allowlist 擴大造成任意來源通行 | `scripts/harness_reconciliation.py:29` 只新增兩個確切路徑；`:189–214` 仍要求 reviewed-code regular files，其他來源繼續受固定 identity 與 inventory 約束。 | 未新增 prefix exemption。Reviewed verifier 程式碼本身仍是信任根；可任意改寫該信任根者不在此自我驗證機制可防護的範圍，不能據此宣稱 verifier 能抵禦自身遭替換。 |
| 新增 subprocess／動態載入導致注入 | Dispatcher 與 ref 查找使用固定 argv，沒有 shell；`--root` 是既有明確 CLI 輸入。Guard import 名稱與檔名固定，未由文章、receipt 或網路資料決定。 | 未找到不受信任輸入流向 shell 或任意 module 名稱的路徑，也沒有新增可觀察的權限提升或外洩效果。 |

## 證據與限制

本次執行的檢查是 packet 完整性與 pinned main 來源身分比對。測試結果引用 captured evidence；未重新執行測試，也未修改來源或 Git metadata。測試成功不等同安全性證明。

此審查限於同步修改，未涵蓋 dependency scanning、DoS／rate limiting、低嚴重度強化、整個專案的既有漏洞或跨票 chain analysis。Main 匯入的歷史二進位證據未重新逐像素檢視；本次瀏覽器圖片亦不作新的安全性驗證主張。S5 的 commit、push 與 PR 外部讀回尚待父代理執行，沒有將其計為已完成。父代理在儲存報告前確認完整快照沒有漂移。
