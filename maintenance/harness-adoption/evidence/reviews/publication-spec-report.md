> Publication projection: machine paths in this historical report were replaced with logical aliases. Original report bytes and hashes remain in the private full bundle/local packet. This does not expand or backdate the original review. See maintenance/harness-adoption/evidence/publication-projection.json.

# Publication affected Spec implementation review

Spec 軸：**P0 0／P1 0／P2 0**；本次發布差異未發現新增規格缺口。此前三項 P1 與指南 P2 的已解決判定維持。

已直接核對 `snapshot/scripts/verify-harness-adoption.py:306–331`、`snapshot/tests/harness_adoption/test_publication.py` 與 staged-path 測試：固定 baseline 的祖先檢查接受原點及後代，拒絕無關／不存在的 baseline；其餘 370 entries／55 moves／641 framework pins／113 trace guards 保留。新測試僅加入精確允許檔名，沒有擴大產品檔例外或刪除斷言。實際 Git graph／staged fixture red→green、50 Python tests、11 unit、build、main、runtime 與 project logs 支持修正。

2026-10-04T11:53:10Z 的明示使用者授權已記錄於 APPROVALS／AGENTS／workflow，限已審查內容的 commit 與 staging 非強制 push；英文凍結規格未改。ticket 仍為 review，尚未製造 landing／done 證據。

唯讀重算 1,548 個凍結檔、189 個投影公開檔及 110 份回執的 log SHA，全部吻合。私有 bundle SHA 與原 evidence manifest 鏈吻合；160 個原始／省略項目與 bundle 匹配，三個省略 diff 共 147,277,061 bytes 的尺寸與 SHA 正確。其餘差異僅為宣告路徑別名、公開 log hash／來源鏈與歷史報告投影聲明；32 個後續發布來源的執行值亦吻合。ESLint exit 0 安裝提示唯一被明示重分類 blocked，原 runner status 保留；CI exit 2 缺既有依賴仍為 blocked，未當成 lint pass。

301 個公開 evidence 索引吻合；942 個網站／canonical／runtime／歷史及核心檔保持 bytes；寫作答案與分數未重寫，113 列仍 28 pass／85 not-run。

審查限制：未執行實作、產品、模型、Git 寫入或網路；不證明遠端 push／owner inspection／production deployment 已完成。ESLint 未成功執行；既有依賴與原 checkout hook 未修復。77 build 輸出沿用已審查證明；沒有重跑寫作／UI／rollback。其他軸報告只作位元投影比對，未以其結論作本軸依據。此為已授權發布的 affected implementation review，非第三輪 spec adversarial review。

## Provenance

```json
{
  "recorded_at_utc": "2026-10-04T12:16:56.732145+00:00",
  "reviewer_task": "/root/code_spec_final",
  "packet": "review-resumed/publication-complete",
  "manifest_sha256": "47d58597530b0eced772b74c00aba06630e1e137e2c7ebf16e37144144e51124",
  "base_head_mergebase": "ee7fecfff72f47abc735d26ac7e9a943de04ebbf",
  "private_bundle_sha256": "edf74f9816a6d39b714ec34283ba450ceabf6ca31c38fafc68a8d4036885c176",
  "read_scope": [
    "affected verifier and real Git graph/staged fixture tests",
    "authorization, ticket and coverage changes",
    "publication projection/export and drift harness sources (read only)",
    "publication raw receipts/logs and complete manifest/hash indexes",
    "private tar members read in memory without extraction; omitted diff size/hash checked",
    "five historical reviewer reports compared by bytes to alias transform plus exact disclaimer; no other-axis conclusions used"
  ],
  "hash_evidence": {
    "frozen_regular": 1548,
    "projection_public_files": 189,
    "receipt_log_pairs": 110,
    "private_bundle_source_or_omitted_matches": 160,
    "late_source_records": 32,
    "public_evidence_index": 301,
    "unchanged_core_files": 942
  },
  "implementation_execution": false,
  "candidate_writes": false,
  "network": false,
  "counts": {
    "P0": 0,
    "P1": 0,
    "P2": 0
  },
  "remaining_limits": [
    "ESLint blocked by existing missing dependency",
    "remote landing/inspection/deployment not verified by this review"
  ],
  "disposition": "affected Spec review clear; retain publication evidence and execution limits"
}
```
