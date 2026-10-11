# PR #17 驗證修正結果

本機修正分支 `tickets/T-0010/main-verification-repair` 的測試與獨立審查已通過。遠端 main 仍是使用者手動 merge 的 `88b9c53`；本次沒有 commit、push、PR、merge 或 deploy。Ticket 保持 `review`。

## 原因與修正

1. lint fixture 從目前 checkout 複製 config，卻套用歷史 lint epoch 的固定 hash，導致成功控制組先出錯。現在從固定 `724ddad` Git 物件取輸入，再執行目前 verifier；原 hash 與負向案例保留。
2. adoption verifier 只理解較早的 adoption／lint 邊界，沒有 PR #17 的精確 successor。現在固定 pre-release main、release、merge，核對完整 45 個變更路徑及 34 個產品身分，先驗證目前檔案，再驗證歷史 predecessor。

獨立 Spec 審查另抓到既有來源被新增路徑規則排除的 P1；公開 CLI 重現五筆誤接受後修正，現在所有既有 release entries 都受保護，只有四個經審查的修正程式為明列信任根。原始歷史證據、文章、圖片、package／lockfile 皆未更新 hash。1,719 個既有檔案中只修改 verifier 與 lint fixture，其餘 1,717 個維持原始 bytes。

## 驗證

| 項目 | 結果 |
|---|---|
| Vitest | 54／54 |
| harness Python | 65／65，無 skip |
| publication Python | 16／16，無 skip |
| lint、build、structure、materializer、公開 adoption verifier | 全部 exit 0 |
| 獨立 Standards／Spec | 各 P0=0、P1=0、P2=0 |
| 獨立安全審查 | HIGH=0、MEDIUM=0，門檻 confidence >=0.8 |

公開 CLI 的 12 個新增測試方法涵蓋精確發布、歷史與 scope 變造、缺少／symlink／mode／父路徑、必要修正程式、額外 tracked／untracked／ignored 來源、錯誤 ancestry／缺少物件、replace／graft，以及既有 publication／materializer／管理來源不可變更。

main 的 `test:unit` 只執行 Vitest，沒有 tracked `.github` workflow；因此 Vitest 成功從未代表 Python 與 preservation gate 通過。這次明確執行兩套 Python 與 verifier。原 PR 的失敗紀錄保留，不改寫成成功。

詳細資料：[根因](diagnosis.md)、[coverage](coverage-report.md)、[最終程式碼審查](review/code-T-0010.md)、[安全審查](review/security-T-0010.md)、[原始審查 P1](review/code-T-0010-initial.md)。這些證據只涵蓋本機 Git／CLI 與網站 build 相容性；沒有驗證 hosted CI 或 production 部署。
