# T-0016：#28 落地核對與 P13 演練準備

這是一份本機提案，不是啟用授權。本輪只讀正式 repository 與本機 Git／驗證器；沒有建立測試 repository、安裝憑證、啟用 workflow、調整 rules／部署設定、執行 P13 或 commit／push。

## 已確認的落地

| 項目 | 目前實際證據 |
|---|---|
| main | `8b31956f47075a831cfd0339339f616af96b3dae`，PR #27；tree 與已審 `4d6e58c` 相同 |
| staging | `05fc16c30f978bbafab4b8cc89f24f8657ab3045`，PR #28；tree 與已審 `f76eff4` 相同；main 為祖先 |
| 共同工程 | main 的 874 個 common 身分全部與 staging 相同；staging 多出的 22 個 common 路徑都是本輪同步與審查管理證據，並非其他候選文章 |
| 候選／文章 | staging 的 111 個 blog 路徑及 50 個候選路徑，逐檔 mode／blob 與 #28 前一致；main 仍是 73 個 blog 路徑 |
| 歷史契約 | main 的 372 個歷史路徑與其原 main baseline 一致；staging 的 376 個與其原 staging baseline 一致。兩端原有四份 staging 專屬 receipts 與兩份不同 manifest 保留，沒有強行合一 |
| 現行驗證 | 在上述實際 commit 的乾淨 detached checkout，兩端 native／結構／materializer 均成功；T-0012／T-0014／T-0015 為 done，T-0016 兩端仍為 review |
| 未啟用現況 | 正式 repo 的 Actions workflow 數量為 0；main 已套用規則為 deletion／non-fast-forward／pull-request，未列 required-status-checks；staging 的 applied rules 回應為空。這不是所有外部／組織政策的完整否定證明 |

完整 Python 與產品測試沿用已審且相同 tree 的 #27／#28 紀錄，不宣稱本輪重新執行。原始讀回、驗證輸出與 SHA-256 見 evidence/。Git／本機證據不等於 CI、HTTP 或部署證據。

## P13 要驗證什麼

確認真實 GitHub 權限、可信 dispatch／run 綁定、單一 owned PR、非 force 更新，以及 head／base 漂移時確實拒絕舊結果。成功標準必須同時包含正向與拒絕案例；不能只看「API 回傳成功」或一張綠色畫面。詳見 [P13 分項驗證表](test-matrix.md)。

## 所需測試 repository

建議由你指定一個專用、可拋棄的私有 repository，例如 **`CXPhoenix/0x1dea-p13-lab`**；這只是建議名稱，尚未建立，也未確認名稱可用。

- 與正式 `CXPhoenix/0x1dea` 明確分開，不連結 Cloudflare／Pages／正式網域，也不自動推回 upstream。
- 保留必要完整 Git 歷史與精確來源 refs，再使用 lab 的 main／staging／永久票分支及合成工程變更。不可淺複製或只搬最後一棵 tree，否則舊驗證器無法證明契約。
- private repo 必須實際支援所需 branch protection／ruleset 與 required checks；目前尚未查驗帳號方案。若能力不足，停下改選支援的 repository／方案；不得默默改公開或省略保護。[GitHub 保護分支條件](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- 需要已配置的乾淨 macOS runner、Node 24.13.0、pnpm 10.28.0、完整 dependencies，以及可信外部 registry／runtime／state。現有範本沒有安裝或產生這些檔案的步驟；不能假設 `macos-15` 已具備所有條件。不得把個人工作用電腦直接當作執行不受信任候選的長駐 runner。

## 開始前的四項工程缺口

1. **有限 workflow successor。** 目前 `publication_current.policy()` 與 `prepare()` 都直接拒絕 `.github/` 路徑，並非只要把精確 hash 加進現有 map 就能執行。需先另經專案流程核准有限 successor 與測試；不能刪掉歷史保護或改成整個目錄豁免。
2. **可重現的 runner／外部設定交付。** writer 與 validator 必須各自取得符合該次 pins 的完整 checkout、外部 registry／runtime 檔及分開交付的 SHA；writer state 需跨參與作業共用。`RUNNER_TEMP` 的本機 lock 不能當作跨機器／人工操作的鎖。
3. **真正的 head／latest-base merge guard。** 現有 validation workflow 綁定 main 的 run，且只有 read 權限，沒有另把成功結果發佈成 PR head 的 required check。須先審查可信 reporter／strict required checks 或等價 merge queue 的方案。只比對 merge API 的 head SHA，無法證明 base 沒改。[GitHub strict checks 說明](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

4. **人工 #28 與 owned PR 的接續。** 唯讀 API 確認 #27／#28 均已 closed＋merged，且沒有 `0x1DEA-operation` marker。現有 `_owned_pulls()` 最多排除精確的已核准 main bootstrap PR（預期 #27）；當未來有新的同步準備結果為 ready 時，其後的 owner 檢查仍會拒絕人工 staging PR #28；目前 main 已被 staging 包含，可能先回 no-op，並非本輪觀察到 controller 失敗。這是依目前 API 資料與程式碼可確認的條件式 blocker，並非已執行 controller／P13 的結果。演練必須重現它，再另行核准最小且精確的歷史接續處理；不能改寫舊 PR body／receipt、捏造 marker，或忽略所有 closed PR。原始盤點見 evidence/canonical-pr-lifecycle.json。

需要程式、policy、runner 或 check reporter 變更時，先另行核准修正票／測試／審查；不得夾在本輪文件或 P13 執行中直接修改。這些缺口未完成，P13 可停在「前置條件不足」，不能填假 receipt 讓 controller 開始寫入。

## 演練順序

1. **核准範圍。** 指定 lab 完整名稱、是否建立、runner、費用／run 上限、lab-only 設定與測試 merge 權限；正式 repo 不在寫入範圍。
2. **準備 lab。** 依審查過的有限 successor 配置 lab 的驗證 workflow／保護，複製完整必要歷史，讀回 refs／rules／workflow hash；使用真實 lab bootstrap PR，不能拿正式 #27 的號碼充當 lab PR。
3. **先做獨立 capability probes。** 以 lab 憑證確認允許／拒絕權限、dispatch 的實際 run、可信 build 隔離，以及 head/base 漂移的拒絕結果。此時不執行 gated writer，避免「先聲稱 P13 成功才能開始 P13」的循環。
4. **證據夠才跑 controller。** 由擁有者審查實際 probes，另在控制端之外產生 lab 專用 receipt 與 digest；各 verified 欄位只能引用實際成功證據。再授權一次有界的 lab writer smoke，核對單一 PR、operation／head／tree／policy／run 與 refs。
5. **跑拒絕與競態案例。** 權限不足、錯誤／缺漏／失敗／重複／過時 run、head/base/main 漂移、既有無關 PR、未知結果讀回及共用 writer 排程，均依表留下原始證據。測試目標 base 改變時，不得只依賴本機 mutex；實際伺服器必須拒絕過期 merge。
6. **收整。** 保存去除敏感值的 run／PR／refs／rules 前後讀回與覆蓋表，撤銷 lab 短期憑證並停止 lab workflow。關閉測試 PR／撤銷憑證等清理也須列入 lab 授權；預設保留稽核 repository，不自動刪除。

完整工程操作與停止條件見 [plan.en.md](plan.en.md)。P13 成功也不會自動授權正式啟用；正式 repository 的 token、rules、workflow 與部署仍需要另外核准。

## 之後需要你的授權

目前已授權的是核對與整理。要實際開始，至少要明確確認：**lab 的 owner/name 與可見性、是否可建立／匯入歷史、可啟用哪些 lab workflow／保護、runner 與用量上限、短期憑證交付方式、可否進行 lab 合成 PR 的正向／預期失敗 merge 測試，以及清理範圍。** 請勿在對話中貼 token；憑證由安全的設定管道提供。

詳細角色與權限列於 [authorization.md](authorization.md)。在取得這份有限授權、補齊前置工程及完成真實證據前，T-0016 維持 review，P13 未驗證，正式自動化停用。

本提案已完成獨立 Standards／Spec／安全審查；均無未解問題，範圍與限制見 [review.md](review.md)。本輪文件與精確管理 map 只留在隔離的本機提案 checkout，尚未 commit／push；正式 main／staging 與部署設定未變。
