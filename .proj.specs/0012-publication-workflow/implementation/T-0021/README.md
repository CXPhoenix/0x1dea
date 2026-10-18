# T-0021：指定 PR head 的可信回報

這次把可信 run、候選 head 與回報 check 分開核對。workflow_dispatch 的 main head 不會被拿來當作候選 head。成功寫入後，仍要從獨立讀取端確認 check 的 head、來源 app、識別碼與結論；任一來源更新或結果不明，都不能沿用舊的本機判定。

`report_from_job` 會重用 T-0020 的封存 validator inputs 與 T-0019 的外部 workflow admission；回報前後重新驗證來源。`check_reporter_from_environment` 只消費明示的 reporter credential，不借用 writer／build credential，也不擴大它們的權限。只有 reporter 的固定 Checks API request 會接觸該憑證。

已確認的 check ID 會固定保存，之後讀回不同 ID 就拒絕。non-bypass 觀察要求標準 write 角色、完整的上層 ruleset 清單與可見的 bypass 資料；缺項或自訂角色都拒絕。保護設定摘要改變，也會讓舊判定失效。

未知寫入結果會先記錄意圖，再讀回；無法確認便保持 blocked，後續執行也不能盲目重複建立 check。保護設定、actor、PR head、staging、main、policy 或 workflow 變動，都需要重新驗證。此處的鎖只協調同一主機，不保證阻擋手動或其他主機的寫入。

這是本機 API 契約。`local_ready` 是當下觀察；`live_ready` 保持 false，`live=True` 會拒絕。重播的權限或分支保護資料不能變成正式證明；實際權限、ruleset／bypass 與競態的驗證仍屬 P13。本票不啟用 workflow、不修改部署、不 merge，也不發布候選文章。

測試列與界線見 [coverage.md](coverage.md)，實作授權見 [authority.md](authority.md)。執行完整 Python 測試時，沿用既有 Node24.13.0、pnpm10.28.0 與依賴，設定 `PUBLICATION_TEST_DEPENDENCIES`，再執行 `python3 scripts/run-current-python-tests.py`；不安裝新工具。

GitHub 的 check run 有獨立的 commit head、external_id、app 與 conclusion；本機 adapter 按此 REST 契約對應。參考 [Checks API](https://docs.github.com/en/rest/checks/runs?apiVersion=2022-11-28) 與 [Workflow Runs API](https://docs.github.com/en/rest/actions/workflow-runs?apiVersion=2022-11-28)。文件確認不等於本專案已取得平台能力。

分支規則使用 [Rules API](https://docs.github.com/en/rest/repos/rules?apiVersion=2022-11-28) 明示讀取上層 rulesets；沒有可見的 bypass 清單就拒絕，不要求擴大權限。角色依 [Collaborator Permissions API](https://docs.github.com/en/rest/collaborators/collaborators?apiVersion=2022-11-28#get-repository-permissions-for-a-user) 的 role_name 區分，不能只靠舊版 permission 欄位推定沒有 bypass。

歷史測試與目前驗證會分開執行，原始測試與斷言都保留。四個固定歷史模組會在明示的 #32 版本執行，同一批 14 項斷言也會使用目前來源與實際分支位置執行；任何一組失敗都會讓整體驗證失敗。根因與界線見 [historical-context-repair.md](historical-context-repair.md)。
