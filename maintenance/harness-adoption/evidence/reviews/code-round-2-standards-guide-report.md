> Publication projection: machine paths in this historical report were replaced with logical aliases. Original report bytes and hashes remain in the private full bundle/local packet. This does not expand or backdate the original review. See maintenance/harness-adoption/evidence/publication-projection.json.

# Standards guide-only addendum

Recorded at: 2026-10-04T11:40:15Z (clock tool UTC).
Scope: only the role-model prose correction in `docs/guide.md`, compared with four frozen actual role files. No implementation re-execution or scope expansion.
Base packet SHA256: `e84119fb6d4478e51c7ef1bbed54987cfc93299b44165dcb5a66a38dc7b7ca34`.
Addendum packet: `{WORKSPACE}/review-resumed/code-round-2-guide-addendum`.
Addendum manifest SHA256: `8c2db57b874beceecac71436c8b419f659434e67892de5038043456cd54568b4`.
Corrected guide SHA256: `ffe9127a0875942bdee4b2f12c2bcf028a76263aa3e6f9c22ccf4a676f93340a`.

## Standards

**新增模型敘述 P2 已解除；剩餘 P0／P1／P2：0／0／0。本軸仍可通過；最嚴重未解問題：無。**

前次 Standards 未察覺指南把兩個 runtime 的角色都描述為繼承 session 模型。本次直接核對 `docs/guide.md:59–63`：Claude reviewer 明列 `claude-opus-5-5`，Claude researcher 使用 `inherit`，Codex roles 未設定 model override；與四份實際設定相符。

五個檔案的 manifest SHA 全部吻合。四份角色設定與 base packet 逐位元組相同；指南差異僅限上述模型說明。沒有角色、模型、權限或全域設定修改。此低影響文字修正以直接核對為充分驗證，未執行鏡像實作測試。

本次只覆核指南修正；原第二份完整 Standards 報告的覆蓋、證據與限制持續適用。第一份與第二份原始快照／報告未改動。live checkout drift 與合併 closeout 由 parent 完成；唯一寫入為本報告，candidate／snapshots 保持唯讀。

## Role-file provenance

| Frozen file | SHA256 |
| --- | --- |
| `.claude/agents/harness-reviewer.md` | `0c42560fd1e2f4ea10665f294682da4074c6895c71f38a2546804f6cfaa2d224` |
| `.claude/agents/harness-researcher.md` | `44802eb27c6a2e67627c9ff8d6f2e698005a575e116d7faf2a516b3759758963` |
| `.codex/agents/harness-reviewer.toml` | `283aef8876fb3f6d2722eddaaf35a7d50d13230cc5e987ce29823ee5285af2d4` |
| `.codex/agents/harness-researcher.toml` | `060090fb8724cb5316259721d8404716e4d8d46ea14cbf44c237cc5f901fdcca` |
