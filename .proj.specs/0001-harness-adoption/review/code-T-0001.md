> Publication projection: machine paths in this historical report were replaced with logical aliases. Original report bytes and hashes remain in the private full bundle/local packet. This does not expand or backdate the original review. See maintenance/harness-adoption/evidence/publication-projection.json.

# T-0001 final independent code review

Recorded at 2026-10-04T11:41:24.122877+00:00, after all actual native reports. Base/HEAD/merge-base ee7fecfff72f47abc735d26ac7e9a943de04ebbf; branch tickets/T-0001/harness-adoption; committed/staged layers empty; complete pending tracked/untracked WIP reviewed. Original implementation packet and reports remain immutable.

Round-2 full packet SHA e84119fb6d4478e51c7ef1bbed54987cfc93299b44165dcb5a66a38dc7b7ca34; guide-only addendum SHA 8c2db57b874beceecac71436c8b419f659434e67892de5038043456cd54568b4. The addendum only corrects role-model prose; four role configurations were unchanged. This is implementation review, not a third spec-adversarial round.

Final Standards and Spec axes each have zero unresolved P0/P1/P2. All first-round actionable findings were fixed with real red/green checks; the later guide-model P2 was fixed and independently rechecked by both axes. Security has zero concrete HIGH/MEDIUM candidates in its declared scope. No accepted candidate required an independent false-positive pass. No landing occurred; T-0001 stops at review. Raw original reports are preserved byte-identically under maintenance/harness-adoption/evidence/reviews/. Reviewer recording times are their actual saved times, never backdated.


---

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

---

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

---

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

---

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
