# T-0026 覆蓋報告

使用者已核准 A01～A06，並正式配置 T-0026～T-0029。A 的本機實作與最後功能回歸已完成，未量測程式碼覆蓋百分比。實作位於 `/private/tmp/0x1dea-T0026`；原 staging 已追蹤內容未變。僅 A 已實作，B～D 維持 todo。

## 覆蓋報告表

| Seam | Tests | Measured coverage | Acceptance criterion | Uncovered, and why |
|---|---|---|---|---|
| Native current CLI：筆記生命週期 | A01：不存在／空範圍、三種合法檔名、建立／更新／移除，以及雙角色非筆記身分獨立比較 | 最後完整回歸通過；24 次 native 呼叫。另以 main、staging 驗證三筆記同時存在的保存前／建立後／更新後流程 | AC-17／R20,R45 | 不建立真正作者工作區；保存／返回的技能互動屬 C |
| Native CLI：範圍形狀 | A02：檔案／連結根目錄與工作區、巢狀資料夾、額外檔名、反斜線 key；A01 含合法 Unicode／空白 key | 16 次 native 呼叫依預期接受或拒絕，涵蓋兩種角色 | AC-17／R46 | 無法用實體路徑表示的空字串／點／分隔符輸入，於 C03 的寫入動作邊界驗證 |
| Native CLI：不安全筆記物件 | A03 兩個方法：三種檔名各測連結／失效連結／FIFO／socket／三種執行權限，涵蓋雙角色，另有 group-bit TDD 案例 | 42 個物件變體及 2 次 group-bit 呼叫通過；外部 sentinel 未變 | AC-17／R46 | 初次 socket 建立被 sandbox 拒絕；同案例及最後完整回歸取得暫存測試執行權限後執行，沒有略過或替代成功 |
| Native CLI：來源歸屬 | A04 三個方法：只在 index、HEAD 已追蹤但 index 移除、trusted inventory 已列入 | 雙角色共 12 次基準／拒絕呼叫通過 | AC-16/17／R47 | Git plumbing 僅操作暫存案例；原專案 index 與 HEAD 未變 |
| Native CLI：完整範圍及外部來源 | A05：合法筆記混入非法物件、範圍外未核准來源；筆記不能選擇其他排除路徑 | 雙角色共 8 次基準／拒絕呼叫通過 | AC-17／R46 | 自訂保存位置的作者互動屬 C10 |
| 既有來源與公開 CLI 保留 | A06 四個方法：ignore 不取消追蹤；精確 ignore pin 的竄改／缺失／連結／各執行權限；獨立 trusted control 拒絕 candidate hash／權限變動；有限 additive guard-pin 變體 | 39 次基準／拒絕呼叫通過。ignore 及 successor 變體涵蓋雙角色；獨立 control 的 candidate-ignore 案例使用有效 main。未修改的 head-reporting merge 回歸及兩個歷史脈絡均通過 | AC-16/17／R38,R47 | 不宣稱 article-discovery host、真實遠端發布或整個 epic 已驗收 |

新模組共 12 個方法通過，記錄 143 次 native CLI 呼叫的預期接受／拒絕結果；這些是實際次數，不是覆蓋百分比。[命令紀錄](execution-results.json)保留分項與原始 trace 雜湊；[同時保存證據](coexistence-native.json)保留雙角色實際前／建立後／更新後報告與獨立來源身分比較，凍結功能版本分別為 main 3377、staging 3526 項來源。

## 完整回歸

未修改的 current Python runner 結束碼為 0：live Harness 66＋live article-publication 170＋原 #22 的 10＋原 #32 的 14＝**260 項通過，零失敗／錯誤／略過**。見[完整 log](full-current-python.txt)。最後執行沿用既有文件的相依環境設定，耗時 1192.154 秒。Vitest 54 項全數通過。portable、materializer --check、lint 與 native working-main 也已通過；實際命令與結果保留於 execution-results.json。

`pnpm test` 因 main 沒有此別名而以 1 結束，沒有執行測試；package scripts 未變。實際入口是 `pnpm test:unit` 與 `PUBLICATION_TEST_DEPENDENCIES=/private/tmp/0x1dea-T0026/node_modules PYTHONDONTWRITEBYTECODE=1 python3 -B scripts/run-current-python-tests.py`。這是命令調整紀錄，不把失敗別名報成成功。沿用既有 Node 24.13.0／pnpm 10.28.0 相依套件，沒有安裝。

## Red／green 與失敗處置

實際 red → green 包含：一般筆記原先被拒絕、反斜線 key 原先被接受、group 可執行筆記原先被接受、index 所屬筆記原先被接受，以及缺少忽略規則。[TDD 紀錄](tdd-red-green.json)保留摘要與原始 log 雜湊。

[第一次完整 log](first-full-current-python.txt)保留缺少相依環境設定的失敗；已依既有測試前置條件修正。之後原 head-reporting 測試暴露 A 的真實 helper-policy merge 衝突；同一原測試在未修改 main 通過，未更改其斷言／輸入。固定路徑的 additive successor 修正後，同測試、新增有限 pin 負向案例及最後完整 runner 均通過。見[回歸紀錄](head-policy-regression.json)。沒有豁免歷史失敗或修改舊測試使其轉綠。

## 保留檢查、審查與最後 metadata 關卡

[保留稽核](preservation.json)：57 個受保護 canonical／歷史檔案雜湊一致；兩個 checkout 的 blog／寫作／工程 CONTEXT／凍結 runner 與斷言路徑均無已追蹤差異；原 index 為空；規格／追溯矩陣／凍結提示身分未變。[建票稽核](ticket-allocation.json)：四個全域永久票號無重複，相依與全部 36 列核准測試表逐列一致。

本表先於正式 stage-6 Standards／Spec 及 stage-7 安全收尾。前期來源審查未發現功能問題；正式結果在 coverage／metadata 一致性確認後連至 T-0026。使用者導覽曾誤用英文，已依語言規範修正兩份 README 與本報告，保留原始 machine-readable 紀錄。[功能擷取版本](source-scope.json)對應受測核心；其後收尾紀錄另按精確檔名更新身分。最後 current metadata 以獨立 native CLI 關卡確認；執行 receipt 保留於來源樹外，避免來源與報告身分循環。

A 在另行授權 landing 前維持 review，尚非 done。native CLI／本機測試不表示 browser、Codex／Claude discovery host、真實遠端發布、作者工作流程或整個 epic 已通過。沒有真正的 .proj.writing 工作區，也未對 ticket 執行 commit、push、PR、merge、deploy、外部索引更新、安裝、帳號／trust／credential 或全域技能修改。維持「先自由聊、按需整理」，A 不新增作者問卷。
