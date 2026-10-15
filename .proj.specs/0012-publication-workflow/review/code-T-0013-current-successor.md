Scope note: this T13 delivery reuses ONLY the four identical shared current/runner files from the captured T15 review; no T15 sync implementation is included. Original full review follows.

# T-0015 與共同 successor／runner 獨立審查

範圍：main-based `tickets/T-0015/local-staging-sync`；base/HEAD/merge-base 均
`001b26f`。固定54檔／13 context、Git 分層 diff/status 及 hashes 見
`../implementation/T-0015/review-capture.json` 與 review-git-context.json。T14五檔
另行審查，本報告涵蓋 T15、共同 guard／runner、有限逐檔 policy 與證據。

## Standards

P0/P1/P2=0/0/0。historical runner 在執行前比對 #22 原 test bytes；live suites
與固定歷史 module 明確分開，無失敗後換契約的 fallback。T13 固定 landed policy
仍須 target ancestry 與精確工程 identity；current common 逐檔 mode/SHA，沒有
候選／blog／歷史路徑或資料夾豁免。v1/helper/舊runner/assertions bytes未變。
新增 red／立即 green regression／舊119checkpoint／最新結果分開記錄。

## Spec

P0/P1/P2=0/0/0。完整 trees、獨立 bare merge、候選 modes/blobs/metadata 與
protected identities 均核對；不同段落無衝突變更仍拒絕；衝突保留 exact paths；
main 已包含時 no-op。多次讀 pins，漂移 stale、不保留新結果。local_ready 只覆蓋
CLI source checks，不能替代 native/build/CI/browser；遠端 adapter 屬 T16。
T13 結案綁定真實 main landing policy 與可信 controller objects；偽 M0 receipt
仍拒絕。固定 #22 原 code/tracker/assertions 測試與新 live closed cases 不混用。

三個獨立 reviewer 均唯讀，沒有執行候選程式；原固定快照提供23sync、3closed、
1runnerpreflight與產品檢查。父 agent 於審查後確認最新版完整127Python通過，
134Python的T14獨立分支也通過；不能相加當成不重複測試數量。metadata收尾另以
current native guard核對。無遠端／HTTP／production驗收。兩票維持review，不是done。
