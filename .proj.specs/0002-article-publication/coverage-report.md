# 第一階段驗收與限制

產品實作完成並留在 review；工作分支交付已授權，沒有 landing 或網站發布。實測 surface 是原生 Python/Git CLI 與既有工具檢查，不是新網站 UI。以下表格保存初次驗證狀態；最新結果在文末。

| Seam | Tests／證據 | Measured coverage | Acceptance | Uncovered／原因 |
|---|---|---|---|---|
| CLI preview／prepare | 16 個 CLI tests 的 A/B、依賴、receipt、source preservation；合成 demo tree 等於獨立 A tree | 未量測行覆蓋率；實際子程序介面驗證 | AP-01、07 source 部分 | 真實候選 build blocked |
| Provenance | staging-only、已 revert B ancestry 反例 | 未量測 | AP-02 | 未宣告／cherry-pick 內容仍需操作人員枚舉 |
| JSON／dependency／path | schema、ownership、symlink、include、dependency 夾帶、惡意文字 | 未量測 | AP-03、06 | regex 非完整 Markdown sandbox |
| Verify／hotfix | main／head／dependency／output drift；完整 receipt tamper | 未量測 | AP-04 | 真實未來 hotfix 仍須重新 pin 與 rebase |
| Conflict | dependency／article 衝突停止、source 不變 | 未量測 | AP-05 | 無真實文章 conflict 演練 |
| Build／output | 合成 index／asset 夾帶與零 signature fail closed | 未量測 | AP-07 部分 | OS isolation 不可用，無不可信候選實際 build／sentinel 隔離測試 |
| Materializer／tracker | 50 個 Python harness tests，其中 21 個 materializer tests；生成／check／framework pins | 未量測 | AP-08 結構部分 | Codex 與 Claude native catalog pass（Codex 由精確 escalation 補驗） |
| Skill／future actions | 四軸 spec、獨立 Standards／Spec／Security review | 不適用 | AP-06、09 | 沒有跨模型 invocation 行為 eval；無外部發布／rollback |

## 初次實測結果（後續結果見末節）

- CLI 合成 fixtures：16/16 pass；無遠端、合成資料、可丟棄，Git 物件由 plumbing 建立。
- Python harness suite：50/50 pass；最初三-product fixtures 引起的 6 個失敗已修正，舊失敗 log 保留。
- 既有 Vitest：11/11 pass。既有可信網站 pnpm docs:build pass（3.11 秒）。blog source bytes 相對 HEAD 沒變；此不是不可信候選建置證據。
- verify-project、materializer --check、verify-harness-adoption、AST parse、git diff --check pass。
- Claude 原生初始化 catalog 找到 managing-article-publication；工具與 session persistence 關閉，只檢查 catalog。
- Standards／Spec 最終各 P0/P1/P2=0；Security 無信心達門檻的 HIGH/MEDIUM 候選。

## 初次精確 blocked（後續補驗見附錄）

1. build-isolation：現有 /usr/bin/sandbox-exec 的最小 probe exit 71，sandbox_apply: Operation not permitted。未改安全設定、持久權限或安裝；不對不可信候選做無界線建置。
2. Codex native discovery：app-server skills/list probe 在初始化前退出，不能初始化 ~/.codex SQLite state。沒有 trust／設定修改；結構 pass 不替代 native discovery。
3. ESLint：既有 config 要求 @unocss/eslint-plugin 並提示安裝。未接受安裝，缺套件仍 MODULE_NOT_FOUND。提示流程 exit 0 不代表 lint pass。

signatures 僅補充偵測，不涵蓋改寫、轉換、短片段或自訂 route；source tree／精確允許 diff 是主要保證。receipt 永遠 publishable=false，沒有發布授權。產品沒有 commit/push/PR/merge/deploy，原 checkout 不變。

## 有界診斷後更新

[阻礙診斷](blocker-diagnosis.md) 與 evidence/bounded-blocker-diagnosis.json 保存各次精確命令結果。Codex native discovery 已在 transient 禁止網路／sessions 讀取 profile 下透過自動審核允許的 escalation 成功，兩 runtime catalog 現均通過。原先 SQLite 初始化阻礙來自 workspace sandbox。

build-isolation 仍 blocked：host transient no-network probe pass，但 read/write-limited 與 read-boundary sentinel startup 皆 exit 134，沒有隔離斷言證據。這不是 auto-review 拒絕，不能用較弱 profile 代替。ESLint 仍 blocked。沒有候選 build、安裝或產品程式修改。

## 2026-10-08 授權後最新結果

先前 blocked 記錄保留作歷史證據。使用者已授權有界診斷與隔離副本安裝；[follow-up](authorized-followup.md) 記錄範圍與新增反例。

- OS sentinel pass：內部可讀、外部讀／寫 denied、network denied。根目錄 literal `/` 是 kernel log 確认缺失的唯一新增讀取規則，不允許其子路徑。
- A-only 合成候選使用同一 OS profile build pass；原 candidate receipt verify pass；B 的 route／long prose 補充輸出檢查 supplementary-pass，publishable=false。
- CLI 16/16、Vitest 11/11、可信網站 build、結構與 materializer 通過。新增依賴增量反例後 harness 51/51 與保存 checker 通過。
- ESLint 已解除缺套件 blocked，結果為 existing-failure：未改 TS 檔案 355 errors；manifest 8 errors 與 HEAD baseline 訊息完全相同。沒有 lint 綠燈、沒有 autofix 或關閉規則。既有 ESLint 10 peer-range warnings 保留。
- 沒有 commit／push／PR／merge／部署，沒有原 repo、host 安全／trust／憑證變更。正式網站候選、未來任意內容、跨平台隔離與發布未驗證。

完整重跑結果：[初次檢查](evidence/followup-checks.json)、[修正後檢查](evidence/followup-final-checks.json)、[解決與限制](evidence/followup-resolution.json)。初次保存 checker failure 與紅測保留，未覆寫成 pass。

## 工作分支提交前驗證

使用者已授權 commit 與 non-force push 工作分支，未授權這輪 PR／merge／部署。新的完整驗證紀錄在 [pre-push-validation.json](evidence/pre-push-validation.json)。Lint 仍為 existing-failure，355 個既有 TypeScript errors 加 8 個 manifest errors，沒有宣稱全過。

公開證據的本機路徑已遮罩，log hashes 綁定公開副本；私人授權內容與 host-specific profiles 留在 repo 外。[Public evidence boundary](public-evidence.md) 說明呈現差異與可驗證範圍。
