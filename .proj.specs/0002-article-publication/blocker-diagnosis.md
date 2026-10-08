# 有界阻礙診斷與補驗

本次只診斷現有宿主能力，沒有變更產品程式。

- 所有精確 escalation 都獲自動審核允許；沒有審核拒絕，沒有繞過拒絕或更改權限設定。
- 原 workspace sandbox 內 sandbox-exec exit 71（sandbox_apply: Operation not permitted）；escalation 後 allow-default／deny-network 的 true probe exit 0。宿主支援 transient sandbox，前次失敗與外層限制有關。
- deny-default echo、完整 read/write-limited 合成 sentinel、移除寫入限制的 read-boundary probe 均 exit 134，沒有 sentinel receipt。因此檔案界線尚未驗證，也不能斷言只是寫入限制。未用弱 profile 建置、未擴建沙箱平台。
- Codex app-server 在原 sandbox 無法初始化 ~/.codex SQLite；精確 escalation 後 fresh skills/list 成功找到 repo managing-article-publication，enabled=true。probe 使用禁止網路與禁止 sessions／archived_sessions 目錄讀取的 transient profile，只有 initialize／skills/list，沒有 thread、model、session API。允許一般 runtime SQLite 初始化，未變更 trust、設定或憑證。
- 初次 escalated native probe timeout；移除未消費 stderr pipe、標出 timeout phase 後相同 probe 成功。沒有把初次 timeout 誤判為權限拒絕。
- ESLint 缺 @unocss/eslint-plugin 仍 blocked，沒有安裝。

上述診斷結束時剩兩項限制：build-isolation 與 ESLint。Codex 原生 discovery 限制已解除；Claude 原生 discovery 先前已通過。

最小後續步驟是釐清必要 runtime 讀取 allowlist，或使用已驗證的既有 transient build profile，再跑合成 sentinel。這是額外有界技術診斷，不需要變更 Mac 安全設定、trust 或憑證；本輪已停止，不自行擴張。實際候選 build 尚未執行。

## 2026-10-08 已授權補驗

使用者明確批准繼續隔離診斷、在隔離副本補齊套件及重跑測試。精確 kernel log 指出合成 echo 被拒絕 `file-read-data /`；只增加根目錄本身 literal 讀取後，sentinel 的外部讀取／寫入與網路拒絕斷言全通過。使用同一受限 profile 的 A-only 合成候選 VitePress 建置 exit 0，原始 candidate receipt 未改，完整 output scan supplementary-pass、publishable=false。沒有擴大根目錄子路徑權限或修改 host 安全設定。

官方 npm registry 的 @unocss/eslint-plugin 66.6.0 已安裝於隔離副本，停用安裝 scripts，既有套件版本未變。ESLint 現在能跑；未改 TypeScript 檔案仍有既有 355 錯誤，package.json 的 8 錯誤與 HEAD baseline 訊息相同。保留 ESLint 10 的既有 peer-range 警告，未關閉規則或做無關格式修改。

歷史保存檢查起初拒絕新增依賴；新增精確 successor hashes 與 fail-closed manifest 增量測試後通過，歷史 adoption manifests 保持不變。授權與範圍見 [authorized-followup.md](authorized-followup.md)，執行證據見 [followup-resolution.json](evidence/followup-resolution.json)。隔離建置能力已在合成候選證明；不代表未來候選、正式發布或任意宿主已驗證。
