> Publication projection: machine paths in this historical report were replaced with logical aliases. Original report bytes and hashes remain in the private full bundle/local packet. This does not expand or backdate the original review. See maintenance/harness-adoption/evidence/publication-projection.json.

# Spec implementation affected review

Spec 軸：**P0 0／P1 0／P2 1**。前輪三項 P1 均已修正；最嚴重剩餘項目為協作指南的模型說明不準確，屬文件問題。

- **P2 — 指南將 Claude reviewer 誤述為繼承模型。** `snapshot/docs/guide.md:59–60` 說兩宿主 reviewer／researcher 的模型預設均繼承 session；但 `snapshot/.claude/agents/harness-reviewer.md:5` 明訂 `claude-opus-5-5`。HA-05（`snapshot/.proj.specs/0001-harness-adoption/spec.en.md:34`）要求保留原生角色設定；設定本身正確，指南應精確說明 Codex 兩角色與 Claude researcher 繼承，Claude reviewer 使用其設定模型。信心高；不影響原三項 P1 的修正判定。

三項修正已直接核對：README 保留既有 `docs:*`，新增 package-script 檢查；pass trace 拒絕每種 nonpass 與 mixed 回執；新增檔檢查同時涵蓋 Git index 和未追蹤檔。反例 red→green 與 final 26 tests 的原始 logs 支持修正（`snapshot/scripts/verify-harness-adoption.py:151–207、315–324`；`snapshot/tests/harness_adoption/test_tracker.py:96–243`）。canonical-only 維護指引、狹義 log unignore 及四份翻譯的對應技術標記修正也已檢視。

唯讀重算 1,488 個凍結檔 SHA、89 份回執的 log SHA，皆吻合。已讀取原始 CLI 各 8 案、77 build 檔／32 assets 證明、370 entries 回復、3,587 writing checks、native 35 catalog 與 browser 證據；370 回復紀錄與 baseline manifest 完全一致。六份英文 imports 保留原文 bytes，翻譯結構合計 32 requirements／81 scenarios／230 conditions／9 trace blocks。28 pass／85 not-run 的保守歷史區分未變。

本輪只檢視修正影響；沒有執行實作、修改 candidate 或讀取其他 reviewer 結論。未逐檔重新建置 77 個輸出，也未重新執行產品或 model；immutable framework/source 依先前 641／370 SHA 證明。翻譯語意未獲人工認證；寫作 dispatch／時間限制維持披露。前輪缺 logs 的限制不回填，本輪新封包已納入。ticket processing、最終報告待關卡完成及未 landing 均如實保留。此為實作 affected review，非第三輪 spec adversarial review。

## Provenance

```json
{
  "recorded_at_utc": "2026-10-04T11:39:15.587321+00:00",
  "reviewer_task": "/root/code_spec_final",
  "packet": "review-resumed/code-round-2",
  "manifest_sha256": "e84119fb6d4478e51c7ef1bbed54987cfc93299b44165dcb5a66a38dc7b7ca34",
  "base_head_mergebase": "ee7fecfff72f47abc735d26ac7e9a943de04ebbf",
  "read_scope": [
    "changed verifier and tests",
    "README/guide/gitignore/ticket/coverage/trace changes",
    "four translation changes and six English sources",
    "new bilingual harness and correction receipts",
    "all 89 referenced raw logs hash checked; key behavior log contents inspected",
    "1488 frozen regular file hashes checked"
  ],
  "execution": "read-only data inspection and hashing; no implementation execution",
  "candidate_writes": false,
  "other_reviewer_conclusions_read": false,
  "counts": {
    "P0": 0,
    "P1": 0,
    "P2": 1
  },
  "prior_P1_disposition": "all three resolved",
  "disposition": "nonblocking P2 guide correction remains; affected implementation P1 fixes verified"
}
```
