> Publication projection: machine paths in this historical report were replaced with logical aliases. Original report bytes and hashes remain in the private full bundle/local packet. This does not expand or backdate the original review. See maintenance/harness-adoption/evidence/publication-projection.json.

# Spec implementation guide addendum

唯一剩餘 **P2 已解決**；Spec 軸剩餘 **P0 0／P1 0／P2 0**。此前三項 P1 的已解決判定維持。

直接核對凍結 addendum 的 `snapshot/docs/guide.md:59–63` 與四份原生角色設定：指南正確說明 Codex 兩角色沒有 model override、繼承 session；Claude reviewer 明訂 `claude-opus-5-5`；Claude researcher 使用 `inherit`。這修正了前輪模型說明不準確的 P2，符合 HA-05 保留原生角色設定的契約。

五個 addendum 檔案 SHA 全數吻合。四份角色設定與 base packet 位元完全相同；指南唯一差異為該段角色模型說明。base packet 與原 P2 報告均未修改。

此次只做指南與角色設定的直接比對，未執行實作、產品或原生模型，也未修改 candidate。這是同一次 implementation review 的低影響文字補充；不需要新增實作測試，亦非第三輪 spec adversarial review。完整實作的證據與限制沿用 `code-round-2-spec-report.md`；本 addendum 不擴大其覆蓋，也不代表 landing 授權。

## Provenance

```json
{
  "recorded_at_utc": "2026-10-04T11:40:25.730577+00:00",
  "reviewer_task": "/root/code_spec_final",
  "base_packet": "review-resumed/code-round-2",
  "base_manifest_sha256": "e84119fb6d4478e51c7ef1bbed54987cfc93299b44165dcb5a66a38dc7b7ca34",
  "addendum_packet": "review-resumed/code-round-2-guide-addendum",
  "addendum_manifest_sha256": "8c2db57b874beceecac71436c8b419f659434e67892de5038043456cd54568b4",
  "guide_sha256": "ffe9127a0875942bdee4b2f12c2bcf028a76263aa3e6f9c22ccf4a676f93340a",
  "base_head_mergebase": "ee7fecfff72f47abc735d26ac7e9a943de04ebbf",
  "read_files": [
    "docs/guide.md",
    ".claude/agents/harness-reviewer.md",
    ".claude/agents/harness-researcher.md",
    ".codex/agents/harness-reviewer.toml",
    ".codex/agents/harness-researcher.toml"
  ],
  "comparison": "five frozen file hashes verified; four roles byte-identical to base; sole guide hunk inspected",
  "implementation_execution": false,
  "candidate_writes": false,
  "remaining_counts": {
    "P0": 0,
    "P1": 0,
    "P2": 0
  },
  "disposition": "prior three P1 resolved; sole remaining P2 resolved; no findings within targeted scope"
}
```
