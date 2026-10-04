# Codex 的 Spectra 操作

repo 已安裝 Spectra，規格在 openspec/specs，任務在 openspec/changes。既有 .claude/skills、.github/skills、.gemini/skills 的生成檔保存供應商歷史。本參考把寫作／技能維護涉及的操作轉成 Codex 可執行路徑；生成檔中的 Claude 工具名不作工具依賴。

## 選擇分支

- 需求需要釐清：只讀相關規格與來源，提出會影響結果的缺口。已清楚的實作指令可直接建立可驗收變更。
- 提案：用 spectra new change <name> --agent codex，再依 spectra instructions <artifact> --change <name> --json 的 schema 建立 proposal、所需 design、delta specs、tasks。用 spectra new artifact 的 --stdin 寫入。只要求提案時，完成驗證後停在提案；已授權實作時继續 apply，避免額外批准循環。
- 接續／需求變更：先看 spectra list --json 與 spectra list --parked --json，讀指定 change 的 status 和相關 artifacts。原有續作授權足夠時 unpark；不明確才詢問。將需求改動寫回 artifacts，再執行 apply。
- 實作：用 spectra status 與 spectra instructions apply 取得 contextFiles、tasks 和 preflight，讀 .spectra.yaml 的偏好。依任务實现並驗證；spectra task done 用 CLI 返回的 task id，檔案 checkbox 是進度來源。tdd/audit instructions 按實際修改風險與 repo 偏好適用；文件變更核對行為與结構，不新增模仿文字的測試。
- 查詢：spectra show/search 或直接讀相關 spec；純查詢不修改文件。
- 歸檔：確認任務實際完成、delta specs 行為正確，再執行 spectra validate、spectra analyze。已授權完成本次工作可用 spectra archive <name> --yes 同步規格並歸檔；未完成的任務保留未勾選並報告，不能用 mark-tasks-complete 或 no-validate 掩蓋。
- commit：只有明示授權才執行；以 Git 狀態及 change 的 touched/task 紀錄選取相關檔案，不使用 git add . 混入其他修改。

命令失敗先報真正錯誤，CLI 不在時停止依賴它的操作；不安裝工具或手造 CLI 成功結果。命令參數以當前 --help 為準。

## 宿主工具對應

「Read/Edit/Write」是讀改檔行為，用 Codex 的檔案／shell／patch 工具；「Glob/Grep」用 rg --files 與 rg；「AskUserQuestion」表示需要資訊時的提問，用當前可用的提問工具或文字，不假設工具名稱存在。「Task/Skill」需要核對宿主是否有相應能力，純粹本地同步規格可交給已安裝 CLI，不為名稱模仿缺少的工具。

需求、權限與副作用邊界來自當次使用者授權。舊指引中的 Plan mode、Claude 計畫目錄或模型 effort 不決定 Codex 的執行模式；不用讀全域 session、憑證或私密設定來取得計畫。
