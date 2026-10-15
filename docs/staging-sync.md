# 本機 main → staging 同步

`python3 scripts/staging-sync.py` 只計算固定 `staging` 角色的本機結果。它不會建立遠端分支、PR、merge 或修改部署設定；`local_ready` 只表示本機來源檢查符合這份固定契約。

先取得經維護者審查的完整 registry 與另外提供的 SHA-256，不能把候選自行提供的 registry 和自行算出的 digest 當成核准。執行程式與 registry 都屬於可信任的控制端；這個介面不抵禦控制端或其執行環境遭竄改。

```sh
python3 scripts/staging-sync.py schema
python3 scripts/staging-sync.py --help
python3 scripts/staging-sync.py prepare \
  --registry /absolute/reviewed-registry.json \
  --registry-sha256 REVIEWED_EXTERNAL_SHA256 \
  --output /absolute/new-result
python3 scripts/staging-sync.py verify \
  --registry /absolute/reviewed-registry.json \
  --registry-sha256 REVIEWED_EXTERNAL_SHA256 \
  --output /absolute/new-result
```

registry 的 version 固定為 `1`，target 固定為 `staging`。main／staging 的 ref 只能使用同名本機分支、`refs/heads/` 或 `refs/remotes/origin/`；每個 ref 都必須附上完整 commit SHA。`trees` 列出兩個完整 Git tree 的逐檔 mode／blob，`candidates` 列出所有候選的 id、來源 ref／SHA 和完整逐檔身分，`engineering` 逐檔列出其餘差異，`checks` 列出結果必須保留的逐檔身分。所有 `maintenance/harness-adoption/` 歷史路徑，以及既有固定 source-boundary、寫作 baseline manifests、reconciliation receipts、PR #17 scope 與歷史 verifier 副本，都必須在 checks 中；完整清單是程式中的 `PROTECTED_HISTORY`。

候選可以是既有已發布路徑的新修訂，也包含未更動但由該候選持有的資產。來源與 staging 中的候選身分必須一致。完整 blob 包含 frontmatter 與本文，不使用段落、檔名或 metadata 欄位的近似比對。

`blog/post/` 與 `blog/public/assets/` 的差異不得用工程分類豁免。`blog/.vitepress/`、`blog/shared/` 與特定 `blog/index.md` 可以逐檔列入工程分類；每個完整 tree 與確切差異仍須驗證，沒有整個資料夾免驗。三個固定歷史 alias 只允許原始 literal target，不會跟隨連結；main、staging 與結果的 alias 身分必須相同，不允許新增、刪除或改 mode。其餘 symlink 與 submodule 一律拒絕。

計算使用新的暫存 bare repository，以唯讀 alternates 取得來源 objects，採 Git 的獨立 merge tree。控制端不會讀取候選程式碼來執行 checker，也不繼承來源的自訂 shell merge driver。Git reads 關閉 lazy fetch 與所有遠端 protocol，拒絕含 include 檔的 partial／promisor 設定、shallow、grafts 與 replacement refs。完整 source blob 都必須存在，實際內容 hash 必須符合其 Git OID。來源分支、HEAD、index、dirty 檔案及來源 object database 都不寫入。成功輸出只有 `result.git` 和 `receipt.json`，需位於來源 checkout 與 Git storage 之外；不允許自訂 symlink 導向輸出路徑。

- `ready`：獨立結果符合完整來源 tree、候選完整 mode／blob 與 protected checks，local_ready 為 true。
- `no-op`：main 已是 staging 的 ancestor，local_ready 為 false，不需要 PR。
- `conflict`：回報 Git 的確切衝突路徑，不會選 ours／theirs。
- `failure`：回報具體 schema／tree／candidate／protected check 問題與可取得的路徑。
- `stale`：main、staging 或候選來源 ref 漂移，舊 receipt 不能繼續使用。

prepare 與 verify 都在讀取、計算後及回傳結果前重讀 pins。verify 會重算獨立 merge，並比對整份 receipt 與結果 tree；修改 receipt 不能重新賦予 readiness。receipt 的 registry SHA、main／staging／source pins 與 result tree 可供後續自動化綁定操作，但正式遠端寫入前仍須再次重讀遠端 refs 並做 concurrency／ownership 檢查。這些遠端流程屬於 T-0016，尚未啟用。

verify 也會依重算結果的完整清單讀取輸出 `result.git` 的每個 blob，核對 type／長度與內容的 Git OID。只保留 receipt／tree／OID，卻用另一份 loose object 遮蔽原始 blob，仍會被拒絕；來源檢查不能代替輸出內容檢查。這是當次驗證，後續寫入前仍須重新驗證，不能保證驗證後的儲存內容不再遭修改。

本機 CLI 檢查不等同產品 native guard、網站 build、瀏覽器、GitHub CI 或正式環境驗證。不同段落即使 Git 沒有衝突，只要合併後候選的完整 blob、mode 或 metadata 改變，就會停止；需先更新來源、重新審查 registry 並取得受影響作者核准，才能重試。

歷史 Python assertions 不會改成配合現行 done 狀態。`python3 scripts/run-current-python-tests.py` 執行現行 suites，再明確用 PR #22 的 Git snapshot 執行原 T-0013 的 10 項 fixtures；只固定該歷史 module，原檔被改會拒絕，新票與目前結案 tracker 仍在 live suite 驗證，沒有失敗後改跑另一份契約的 fallback。
