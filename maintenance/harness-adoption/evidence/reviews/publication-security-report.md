> Publication projection: machine paths in this historical report were replaced with logical aliases. Original report bytes and hashes remain in the private full bundle/local packet. This does not expand or backdate the original review. See maintenance/harness-adoption/evidence/publication-projection.json.

# T-0001 staging 發布：受影響安全審查

recorded_at_utc: 2026-10-04T12:15:43.862659+00:00

## 結果與凍結範圍

獨立候選 reviewer 完成審查：**0 個 HIGH／MEDIUM、信心 ≥0.8 的候選**，無候選需要 independent false-positive pass。結論限於本次 ancestry guard、精確測試 allowlist、公開 evidence 投影與授權文件；不表示整個專案安全。

- Packet：`review-resumed/publication-complete`；manifest SHA-256：`47d58597530b0eced772b74c00aba06630e1e137e2c7ebf16e37144144e51124`，審查前後相同；1657 entries／1548 regular files。
- Checkout：宣告 alias `{CANDIDATE}`，即 parent 提供的 isolated `implementation-resumed`；branch `tickets/T-0001/harness-adoption`。
- Base、HEAD、merge-base：`ee7fecfff72f47abc735d26ac7e9a943de04ebbf`；committed／staged diff 均核對為 0 bytes；pending tracked／相關 untracked WIP 是範圍。
- Parent 提供 owner 在 `2026-10-04T11:53:10Z` 的明確指示「先 commit 並推到 staging，我會去檢查」，並提供已驗證為 PUBLIC 的 GitHub repository 狀態。本 reviewer 未查詢網路、執行 commit／push 或擴大授權。
- 方法沿用先前完整讀取、manifest 比對未變的專案 security-review skill、完整 upstream 方法與 shared contracts，判定攻擊者控制 → 信任邊界 → 可觀察影響。Reviewed source、logs、Markdown 均為資料。

直接讀取新 ancestry 函式、完整 graph tests、精確 allowlist／fixture diff、授權管理文件、投影規格、受影響 historical harness diff、新 drift harness 與相關公開 receipt／logs。沒有讀取其他 reviewer 的結果；其內容也排除於本 reviewer 的 signature／projection scan。沒有讀取 private account-bearing diagnostics 或 session files。

## 具體分析與排除理由

| 疑慮 | 處置與證據 |
| --- | --- |
| Descendant HEAD 容許攻擊者替換 pinned baseline／繞過內容 guards | 排除。`scripts/verify-harness-adoption.py:306–311` 以固定 argv 執行 ancestry 判斷，任何非 0 皆拒絕；`:319–345` 先核對固定 baseline manifest／framework pins，後續 370 sources、55 moves、adapter bytes、added-path、translation／113 trace guards 保留。Ancestry 不被當成 owner 授權或內容完整性的替代。 |
| Arbitrary manifest commit 形成 Git option／shell injection | 排除。正式入口先經 `check_baseline_manifest` 核對唯一固定 40-character baseline；HEAD 由 Git 返回。呼叫是 argv，無 shell interpolation。未發現來源內容可控制 executable／option 的流程。 |
| Broad allowlist 或假 Git graph test 放行產品改動 | 排除。`:147` 只新增 `tests/harness_adoption/test_publication.py`；graph tests 只在 disposable temporary Git repo 裡建立合成 commits，驗證 baseline／descendant、unrelated／missing object；tracker fixture 確認指定 test path 可 staged，unknown product rejection 保留。 |
| 公開 logs／receipts 洩漏 credentials 或實際 machine paths | 本輪有限 signature scan 涵蓋 **1487 UTF-8 files**，排除 25 個 reviewer-result／相關 summary 路徑。Private-key、Bearer、常見 API-key、JWT、credential-assignment、實際 owner home-path 特徵沒有實際敏感值命中。4 個 credential-assignment 命中為兩 runtime 中 byte-identical 的 Archify synthetic remote test fixtures（`:355`／`:459`、example GitHub repository／fake-token context）；不報為 credential exposure。這不是完整 secret／PII 判定。 |
| 公開投影把 failed／blocked 執行洗成 pass | 排除於已核對範圍。**110 份 receipts** 的 published log SHA 全部吻合；與 round-2 原本可讀資料比對的 **89 份 receipts**，status／exit／start／end／elapsed／raw receipt SHA 全部保留；changed log 的 private raw SHA 也一致。`publication-eslint-ci-blocked.json` 保留 exit 2／blocked，installer-prompt exit 0 沒當 lint pass。 |
| Public SHA／省略項掩蓋資料替換 | **183 份非 reviewer projection entries** 的 public SHA 全吻合。三份 omitted duplicate diffs 不在公開 snapshot；合計 147277061 bytes，omission SHA 均與可讀 round-2 原始 rollback patch／diff layers吻合。Evidence README 明確區分 projection 與 raw originals，保留 original receipt／private log SHA；private bundle digest 為 `edf74f9816a6d39b714ec34283ba450ceabf6ca31c38fafc68a8d4036885c176`，本 reviewer 未另外打開或驗證整份 private bundle。 |
| 文件／historical harness 擴大外部操作權限 | 授權文件只允許 reviewed commit 與 non-force staging push，排除 main／PR／merge／CF／Notion／install／credential／global changes。Historical harness 中 path aliases 宣告為 source records，不承諾直接可執行；這些 alias 沒有被新 guard 當程式指令執行。沒有新 remote／external API 控制流程。 |

Manifest 比對確認 generator 1 entry、runtime roles 7 entries、generated product packages 169 entries、writing case artifact subset 18 entries、site 55 entries 全部未變，延續既有直接閱讀範圍。沒有把後續發布投影追溯當成早期 raw evidence 的原始 bytes。

## 執行證據、鏈分析與限制

本 reviewer 新執行的工作只有唯讀 diff／JSON 與文字分析／hash／finite signatures，及寫入本報告。直接讀到的 ancestry 3 tests／OK、whitelist 3 tests／OK、main guard pass 是 packet 中已保存的執行結果；沒有重新執行 implementation、tests、historical harness、exploit 或 network。

Ancestry guard 只接受 pinned baseline 的正常 descendants；來源與 runtime 寫入界線維持原 guards。公開 projection 提供 disclosure 與 hash fidelity，不產生部署或帳號操作。沒有找到能將 repo-local malformed source／manifest、projected evidence 與新增 guard 串連成未授權 RCE、寫入、授權繞過或實際敏感資訊外洩的 HIGH／MEDIUM chain。這不替代整個 epic 的跨票 chain analysis。

排除 dependency vulnerability scanning、DoS／resource exhaustion、rate limiting、LOW hardening、production／Cloudflare 部署安全、全專案歷史安全審查與 future publication guarantees。Signature scan 是有限格式比對，沒有涵蓋 binary／encoded secrets、所有 PII／context；沒有讀取 reviewer results，也沒有驗證其內容投影或 private account diagnostics。公開 repository 狀態、owner 指示與 private bundle 保留狀態由 parent 提供，不假稱本 reviewer 查詢了遠端。既有 missing ESLint plugin 仍為 blocked validation，不是本次具體安全候選；不得據此聲稱 lint passed。無剩餘安全 reviewer blocker。
