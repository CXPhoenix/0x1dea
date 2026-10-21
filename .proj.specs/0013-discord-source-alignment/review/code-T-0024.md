# Independent change review

## Standards

# Standards review — source snapshot

範圍：review-context.json 所列 main／staging，各 16 份固定檔案快照；main base/HEAD 0e690064985d9d734849e1ec44a8c0f8d84fb2a3，staging base/HEAD 87ff977bb11c42b810dfedc34c519052f62fbaa7。各有三個 tracked WIP 與十三個 untracked，沒有已提交差異。

獨立 reviewer：discord_standards。文件化標準違反 0，smell 0；未發現需修正項目。

核准 ticket／D01–D06、T-0024 分支與 tracker 格式一致；中文 spec 的 synced_from_sha 與英文來源相符。兩份 policy 只更新現行 guard 與 live adapter 的兩筆既有身分，新增本票十三筆精確 entries；schema、M0 pins、scope 及其他既有 entries 不變，staging 專有三十三筆全數保留。Frozen 五份測試、runner、文章與歷史收據未變。Live adapter 只在原斷言前準備固定資料，真實 process 結果照原樣回傳，未見失敗後替換結果。Fowler heuristics 無值得回報的 smell；測試保留獨立 literal 與 publication pin。

限制：本輪為唯讀 Standards 軸，未執行完整測試，不宣稱仍在執行的 suites 通過，也未涵蓋後續 coverage／landing 紀錄或遠端操作。


## Spec

# Spec review — source snapshot

獨立 reviewer：discord_requirement。範圍與 hashes 見 review-context.json；兩個 checkout 的固定快照均無 drift。P0／P1／P2 = 0／0／0，未發現違反 AC1–AC6 的實作缺陷。

current guard 僅在指定 publication commit 的祖先判定成功後加入固定 record；正常非祖先沿用舊 inventory，其他 Git 錯誤拒絕。完整 path-set equality、逐檔 mode／digest、所有 execute bits 拒絕、tracker／landing 與 publishable false 均保留，沒有目錄例外。八個新測試從 native CLI／真實 Git 驗證正向、變造、額外來源、自行修改 policy、舊 M0、跨角色、缺失 pin 與查詢失敗，未直接測 private helper。

Live fixture adapter 只補必要資料並回傳原始 process 結果，不修改原斷言；五個 frozen modules 與 runner 均與兩個 base 相同。兩份 policy 的 schema／M0 pins／scope 不變，兩筆 current 身分更新、十三筆新增、三十三筆 staging-only entries 保留。

限制：本輪為靜態需求審查，不宣稱仍在執行的 full suites 通過；AC5 的完整歷史執行與 AC6 的最終本機雙目標檢查，須由父代理補齊證據。


## Final source-v6 supplement

# source-v3 fixture supplement

The parent and independent contract reviewer found an initial new-test control-role assumption. This was a test-fixture defect, not a product-role defect. A staging focused run failed with an earlier role check; the first correction exposed insufficient control Git objects in the missing-pin fixture. Both failed checkpoints and the interrupted full source-v1 runs are retained.

Final setup separates candidate/control for policy mutation; retains a complete-history main projection as the trusted controller while only the missing-pin candidate receives old Git metadata; and uses the matching main-root controller for the query-error boundary. The staging focused three-case run completed successfully in 39.655 seconds. Frozen modules, original assertions, runner, product guard and live adapter did not change in this supplement; only the new test and its exact policy identity changed.

| Independent reviewer | Axis | Final findings |
|---|---|---|
| discord_standards | Standards | Documented violations 0, smells 0; snapshot mismatch 0, source drift 0. |
| discord_requirement | Spec | P0/P1/P2 = 0/0/0; focused raw red/green confirmed; prior affected coverage conclusion superseded. |
| discord_security | Security | HIGH/MEDIUM = 0/0; no new executable product changes or false-positive candidates. |

All reviewers checked both 16-file snapshot packets and hashes. No review claims the still-running v3 full suites passed. Full results are recorded separately after actual completion. No commit, remote push, PR, merge, installation, workflow activation or deployment-setting change is part of this local supplement.

# source-v4 owner-approved fixture supplement

Owner approved current workflow fixture staging-ref alignment and full rerun. Captured scope: both target overlays,50 files each, four existing tracked WIP files; see manifest.json. The only new executable delta after v3 is test_workflow_admission.py setUp: real Git resolves SOURCE refs/heads/staging with --no-replace-objects instead of fixed d2e59426fe545116f2c2b637fc6f181dcfcdbaf5. Query failure aborts setup. Only temporary fixture refs change. All original assertions, product guard, prior live adapter, new Discord tests, frozen modules and runner remain unchanged.

Independent Standards reviewer discord_standards: documented violations0, smells0. Independent Spec reviewer discord_requirement: P0/P1/P2=0/0/0. Security reviewer discord_security: HIGH/MEDIUM=0/0, no candidate requiring independent false-positive filtering. Each reviewer verified both50-file manifest hashes and live snapshot agreement. Exact current policy identities changed only for the approved fixture/ticket and new approval record, with no removed entries or changed schema/pins.

These are read-only source reviews; focused/full reruns had not completed when reports were issued. Their actual results must be evaluated separately. No full-pass or remote-authority claim follows from source review. Prior v3 failure/current baseline evidence remains preserved.

# source-v5 approved fixture alignment supplement

Owner approved current main/staging fixture setup and full rerun. Captured scope: both58-file target packets with five existing tracked WIP files; see manifest.json. WorkflowAdmissionTests.setUp now resolves SOURCE main/staging refs through real Git with --no-replace-objects; head-reporting synthetic commit retains already-created w.main as parent. The published record and its ancestry are consistent while no staging candidate parent is introduced. Original assertions, expected results, product guard, prior live adapter, new Discord tests, frozen5 and runner are unchanged.

Independent Standards reviewer discord_standards: documented violations0, smells0. Independent Spec reviewer discord_requirement: P0/P1/P2=0/0/0, negative conditions retain distinguishable invalid inputs. Security reviewer discord_security: HIGH/MEDIUM=0/0; no candidate requires false-positive filtering. Each verified both58-file manifest hashes and live agreement. The precise current policy identities only admit approved files/metadata; no removed entries, schema or M0 pin changes.

Read-only source reviews do not claim focused/full results; tests were in progress at review. Prior failed fixture checkpoints remain retained. Passing local source checks grants no remote delivery or automation authority.

# source-v6 deterministic fixture layout supplement

The owner approved actual main/staging fixture alignment. The external real Git merge experiment identified only engineering-v1.json: current new entries including inert WORKFLOW and actual staging's33 extra entries share the closing-map insertion hunk. Fixture setup now groups every newly introduced common key before baseline keys, retaining all keys/values/schema and the baseline relative order. This occurs once, before tree capture and grant digest; it never follows a merge failure or retries product validation. The actual source policy is not reordered. Product merge-tree, registry, exact identity and original assertions run unchanged.

Independent Standards reviewer discord_standards: documented violations0, smells0. Independent Spec reviewer discord_requirement: P0/P1/P2=0/0/0, this remains authorized fixture alignment. Security reviewer discord_security: HIGH/MEDIUM=0/0; no false-positive candidates. All independently verified main/staging59-file manifest hashes and live agreement. Previous executable code/frozen5/runner/assertions unchanged; exact source policy admits the updated fixture digest and layout note only.

Source-only reviews did not execute experiments or claim focused/full pass. Separate parent evidence includes one failed layout experiment (WORKFLOW still at tail), a successful all-new-entries-first real merge-tree experiment, and actual focused/full outcomes. Full-v5 interrupted runs count as neither completed nor passing. No remote authority is inferred.
