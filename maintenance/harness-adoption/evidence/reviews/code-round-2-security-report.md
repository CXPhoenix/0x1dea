> Publication projection: machine paths in this historical report were replaced with logical aliases. Original report bytes and hashes remain in the private full bundle/local packet. This does not expand or backdate the original review. See maintenance/harness-adoption/evidence/publication-projection.json.

# T-0001 安全複審：round 2

recorded_at_utc: 2026-10-04T11:38:49.509635+00:00

## 結果與範圍

獨立候選 reviewer 完成受影響安全複審：**0 個 HIGH／MEDIUM、信心 ≥0.8 的候選**。無候選需要 independent false-positive pass。本結論僅適用於以下凍結變更，不表示整個專案安全。

- Snapshot：`review-resumed/code-round-2`；manifest SHA-256：`e84119fb6d4478e51c7ef1bbed54987cfc93299b44165dcb5a66a38dc7b7ca34`；1597 個 entries、1488 個 regular files。
- Candidate：`{CANDIDATE}`；branch：`tickets/T-0001/harness-adoption`。
- Base、HEAD、merge-base：`ee7fecfff72f47abc735d26ac7e9a943de04ebbf`。Committed／staged 為空；pending tracked 與相關 untracked WIP 是審查範圍。
- 方法：沿用首輪已完整讀取且本輪 manifest 未變的專案 `security-review/SKILL.md`、完整 upstream methodology、AGENTS／runtime／review／spec；追蹤攻擊者控制到可觀察影響。Source、log 與 embedded examples 均當資料，不當執行指示。

逐一檢查兩輪 manifest 差異、新版 verifier 與測試 diff、README／guide／ignore 規則、candidate-delta／provenance、coverage／traceability／ticket、四份翻譯變更及新 bilingual checker。Generator、runtime packages、角色設定、產品來源與 adapters 的 manifest entries 未變，延續首輪直接閱讀結果；沒有重跑或宣稱全面重新審查這些程式。

## 證據與疑慮處置

| 檢查項目／疑慮 | 處置與依據 |
| --- | --- |
| README 內容進入 shell | 排除。`scripts/verify-harness-adoption.py:158–165` 只以固定 regex 收集 script 名稱並比對 JSON keys，不執行 README 或 package scripts。 |
| 新增路徑從 staged inventory 繞過 | 本輪修正補足 inventory。`:151–155` 用固定 argv、NUL 分隔取得 index＋untracked，再比對 baseline／moves／allowlist；沒有把檔名當 command。 |
| 非 pass／混合 receipt 形成假 pass chain | 本輪增加拒絕。`:200–207` 限制 row status，pass row 的每份 receipt 必須為 pass；`:171–179` 仍核對 exit、regular log 路徑與 SHA。可編輯本機聲明不等於 owner 授權；未找到通往未授權 landing 或外部寫入的具體流程。 |
| Evidence log 可見性造成憑證外洩 | `.gitignore:61` 例外限於 `maintenance/harness-adoption/evidence/**/*.log`。本輪唯讀核對全部 **91 份凍結 log** 的 SHA，全部符合 manifest；保守掃描 private-key、Bearer、已知 API-key 格式、JWT、credential assignment 特徵，0 命中，未輸出敏感值。這不是完整 secret scanner，也不是未來新增 log 的安全保證。 |
| Guide／翻譯提示導致權限跨越 | Guide 維持 canonical 三產品來源、framework pins、明確 landing 授權及 local account／trust 邊界；四份翻譯補回技術 inline code。沒有具體攻擊者輸入通往未授權操作的流程。 |
| 新 bilingual harness 執行文件內容 | `maintenance/harness-adoption/evidence/harness/check-bilingual-resumed.py:6–25` 做文字／hash／結構比對；Git 使用固定 baseline 與 argv。未執行讀到的 Markdown。 |
| TOCTOU、未簽章 receipts、regex parser 或未來 log hardening | 未找到可實際跨越不同權限邊界的攻擊流程；不以理論競態、可編輯本機資料或缺少防禦措施提出 HIGH／MEDIUM。 |

首輪的 source／manifest → materializer → 固定 owned runtime directories，以及 tracker／evidence → 本機驗證結果，是本輪鏈分析的信任邊界。新驗證規則只收緊失敗判斷；log 納入 evidence 不會改變網站 build root。沒有找到上述修正可與首輪排除項串連成可觀察的未授權檔案寫入、程式執行、憑證洩漏或外部發布。此受影響鏈分析不替代 epic close-out 的跨票 chain analysis。

## 執行與限制

本 reviewer 僅執行唯讀 file／manifest diff、搜尋、雜湊與有限 log 特徵檢查，並寫入本報告；未執行 implementation、harness、tests 或 exploit reproduction，未連網、安裝、修改 candidate／original repos、讀取 session files 或發布外部內容。

直接閱讀本輪保存的 `review-fixes-final-tracker.log`（26 tests／OK）、`review-fixes-final-main.log`（pass／113 rows）、`review-fixes-log-visibility-green.log`；這些是封包內既有執行證據，不是本 reviewer 新執行結果。91 份 raw logs 是本輪首次 hash／signature 檢查，不追溯宣稱首輪已讀取；其他 logs 未逐行人工審查。

排除 dependency vulnerability scanning、DoS／resource exhaustion、rate limiting、LOW hardening、production／Cloudflare 部署安全及完整跨票鏈分析。匯入框架與保留產品的完整安全性未重新逐檔評估；既有 CLI 路徑行為不是本輪新漏洞。有限 signature scan 未涵蓋所有可能 secret／PII 格式、編碼或上下文。無剩餘 reviewer blocker。
