> Publication projection: machine paths in this historical report were replaced with logical aliases. Original report bytes and hashes remain in the private full bundle/local packet. This does not expand or backdate the original review. See maintenance/harness-adoption/evidence/publication-projection.json.

# Publication affected Standards review

Recorded at: 2026-10-04T12:15:11Z (clock tool UTC).
Frozen packet: `{WORKSPACE}/review-resumed/publication-complete`.
Manifest SHA256: `47d58597530b0eced772b74c00aba06630e1e137e2c7ebf16e37144144e51124`.
Base / HEAD / merge-base: `ee7fecfff72f47abc735d26ac7e9a943de04ebbf`; branch `tickets/T-0001/harness-adoption`.
Scope: publication changes since cleared code-round-2 plus guide addendum; read-only candidate/snapshots, no implementation/test/network execution. Only this outside-candidate report is written.

## Standards

**P0／P1／P2：0／0／1。Heuristic smells：0。最嚴重未解問題為下列文件 P2；沒有阻擋發布的實作標準問題。**

**P2 — 已授權發布仍要求再次授權。** `maintenance/harness-adoption/LOCAL-REVIEW.md:21` 寫「done 需要後續另行授權並實際 landing」，與同檔 :3、`APPROVALS.md:18–29` 的現已授權 commit／非強制推送，以及 `docs/agents/workflow.md:190–195` 的 T-0001 publication adapter 衝突。影響：後續接手者可能重複索取已取得的授權。建議改成「done 需依既有授權完成實際 landing 並核對 remote SHA」；不需改 frozen spec 或角色設定。

直接讀新 ancestry guard、全部 test_publication、tracker 的單一擴充、authority 文件與 public projection。固定 baseline manifest 驗證仍在；main 改用真實 Git ancestor check，接受 baseline／descendant、拒絕 unrelated／missing。新 test filename 僅精準加入 allowlist；existing assertions 未移除。原 README／canonical-only／角色模型修正保留。

直接核對 ancestry 與 staged allowlist 的 behavior red／green logs，以及 50 Python tests OK、11 unit、build、main／runtime／project 的收據。ESLint 是 blocked：exit0 只到安裝提示，CI exit2 缺既有 @unocss/eslint-plugin；沒有宣稱 lint 成功或以移除規則修正。

1657 entries／1548 regular snapshot SHA 無漂移；110 published receipts 的 log SHA 全部相符，301-file evidence index 相符。私有 bundle 182955019 bytes，SHA `edf74f9816a6d39b714ec34283ba450ceabf6ca31c38fafc68a8d4036885c176`，其原 evidence index SHA 相符。逐一對回 157 prepublication＋32 新 raw source：ledger 私有／公開 SHA、路徑投影、原 outcome／時間／status（明示 lint blocked 分類除外）與非 JSON 內容均符合；三個 omitted diffs 大小／SHA 相符。公開複本明示為 projection，沒有偽稱 raw identity。

1060 份 source／runtime／case／history bytes 與前包相同；641 framework pins 相符。未重新語意審查 immutable framework／370 baseline／77 build assets，未重跑 writers／UI／rollback。此報告只覆蓋凍結快照與私有投影來源；實際 remote landing 尚未發生，live drift 與 P2 closeout 文句由 parent 處理。本次為 publication implementation review，不是第三輪 spec adversarial review。

## Targeted P2 closeout

Recorded at: 2026-10-04T12:18:29Z (clock tool UTC).
Before SHA256: `4816c466188e02efc9730105f18c340c6159f5d60e1bcc7293c0d9b33004c658`.
After SHA256: `755e802b72ffe1303af9c5206d065d769392798e6d9cf7bd078043784078fc07`.

唯讀核對 `LOCAL-REVIEW.md:21` 已改成「done 需依既有授權完成實際 landing 並核對 remote SHA」。凍結 before 與 candidate after SHA 均符合 `publication-p2-closeout.json`；兩份全文差異恰為此單一替換。原 P2 已解除，**最終 P0／P1／P2＝0／0／0；Standards 可通過，最嚴重未解問題：無。** 未重跑整包或實作；前述證據範圍與限制持續適用。
