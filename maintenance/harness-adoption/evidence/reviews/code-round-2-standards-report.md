> Publication projection: machine paths in this historical report were replaced with logical aliases. Original report bytes and hashes remain in the private full bundle/local packet. This does not expand or backdate the original review. See maintenance/harness-adoption/evidence/publication-projection.json.

# Standards affected re-review

Recorded at: 2026-10-04T11:38:05Z (clock tool UTC).
Reviewer: independent read-only Standards implementation reviewer; parent writes candidate closeout.
Snapshot: `{WORKSPACE}/review-resumed/code-round-2`.
Manifest SHA256: `e84119fb6d4478e51c7ef1bbed54987cfc93299b44165dcb5a66a38dc7b7ca34`.
Base / HEAD / merge-base: `ee7fecfff72f47abc735d26ac7e9a943de04ebbf`.
Branch: `tickets/T-0001/harness-adoption`; committed/staged diff empty; pending tracked and untracked implementation reviewed.

## Standards

**剩餘 P0／P1／P2：0／0／0；本軸可通過。最嚴重未解問題：無。**

原 P1「README 命令回歸」已解除：`README.md:60、106–108` 恢復 package.json 的 `docs:*`，符合 `AGENTS.md:132–133`。`scripts/verify-harness-adoption.py:158` 的通用 package-script guard 與真正包含有效／不存在命令的 fixture 有 red／green 收據。

原 P1「生成套件維護指引衝突」已解除：`docs/guide.md:69–87` 區分 32 個獨立框架 skills 與三個 canonical 產品來源，禁止直接編輯生成包，依序執行 write／check／project verifier，符合 `AGENTS.md:149–152` 與 runtime contract。

直接閱讀受影響 verifier、tracker tests、guide、README、窄範圍 log unignore、四份翻譯修改與 tracker／coverage／trace 差異。新增 trace 拒絕 nonpass／混合收據與 staged unknown-product Git fixture，未發現新增標準違反。Heuristic smells：0 項；未重列工具已強制的檢查。

指定 manifest SHA 相符；1597 entries／1488 regular files 全部 snapshot SHA 無漂移。89 份收據的 log 全部存在且 SHA 相符；共 91 份 raw logs。直接核對受影響 red／green、26 tests OK、final main／post-translation main、materializer／project、log visibility 與七份雙語結構檢查的實際內容。第一次快照缺 log 的限制僅在本次解除，沒有追溯宣稱前次已讀。

641 framework pins 與其 manifest SHA 相符；未逐檔語意審查 immutable framework／370 baseline／77 build assets，仍依 pin／既有證據。九位 writers、UI、rollback 未受影響，不重新執行或宣稱本次重測。翻譯新增技術標記未改英文／條件；完整人工翻譯語意驗證未在本軸執行。ticket processing 是待 parent 收齊 review 的正確狀態；未授權 landing。

此報告只適用凍結快照；live checkout drift 由 parent 最終確認。未執行實作、測試或修改 candidate；唯一寫入為本報告。第一份快照與報告保持不變。本次是實作修正審查，不是第三輪 spec adversarial review。
