---
synced_from: spec.en.md
synced_from_sha: 598d7befb48b6ab018d4d87d49f2318eeed437b5
---

# main 合回 staging

## 問題與方案

PR #18 merge 後，main 與 staging 有六個合併衝突。從 staging 4005ee45f2f3267a8b53ce24fa97af7b49cfb144 建立獨立分支，合入 main eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a，保留候選文章、預覽行為與兩套歷史驗證契約，再開 PR 到 staging，先不 merge。

## 實作決策

- 單票、無依賴；目前授權包含同步 commit、non-force push 與 staging PR。
- staging 原有 tracked 檔案的內容與 mode 完全保留，例外只有共用 verifier、reconciliation helper 與 tracker harness。用電審閱稿、五篇 local-preview 候選及資產不變；listing 兩邊已相同。
- 透過實際 merge 帶入 main 的修復 helper、release 測試與證據。原 manifests、紀錄、hash、package／lockfile 與負向預期不變。
- 任一 reconciliation provenance 紀錄存在（含連結）時，執行原 staging 契約；否則 main release scope 選擇原 main 契約；兩者皆無時保留歷史 adoption 流程。驗證失敗不得 fallback。每套 guard 仍完整檢查 pin、來源身分、mode、型別、ancestry 與額外來源。
- guard 按所選契約載入，讓舊 fixture 不需無關模組。reconciliation 僅新增兩個精確 main 修復來源作為 reviewed code，沒有前綴豁免。保留 main helper 原始內容及四個必要 regular repair sources。
- tracker 保留 staging 的 blocked／unresolved_dependencies 行為，lint fixture 保留固定 epoch 與 no-replace Git 讀取，不新增 skip。
- 兩邊 fixture 都執行目前共用 CLI，保留所有既有測試與 counterexamples。

## 驗收條件

- S1：實際 merge 保留兩個固定 parent；除三個整合來源外，staging 原有 tracked 檔案身分完全相同；候選、資產、預覽標記、文章與 listing 不變，保留 main 新增修復與證據。
- S2：staging 目前 CLI 與兩邊歷史／目前正向控制全部成功；既有 bytes、mode、link、missing、record、pin、history 與 unknown／ignored-source 負向案例仍拒絕，不新增 fallback 或通用 bypass。
- S3：舊 manifests、fixture、紀錄與所有既有測試保留；main helper／release 測試與 main 相同；tracker 保留 staging 語意與固定 lint epoch。
- S4：完整 Vitest、兩套 Python、lint、build、structure、materializer、verifier 都取得實際成功結果與 counts／skips，獨立 Standards／Spec／security 審查沒有未解決的阻擋 finding。本機 /post/course/security-awareness/ 顯示「資安認知推廣備課系列」與唯一卡片「用電紀錄裡的正常與異常：家裡哪台設備在偷偷忙？」、原 staging description／date，連至 /post/course/security-awareness/electricity-privacy；鍵盤 Enter 可到文章，標題相符且顯示「staging 修訂審閱稿」。listing 在 1440×900／390×844、light／dark 下 scrollWidth 等於 clientWidth。這些是本機證據，不代表部署。
- S5：只 non-force push ticket branch，PR base 為 staging，附加到本任務，保持未 merge 且不啟用自動 merge。交付時遠端 main／staging 仍為原 pin；變動時重新評估。實際 landing 前 ticket 保持 review。

## 測試與範圍

沿用 T-0009／T-0010 已核准的 Git／CLI、renderer、runner、tracker、完整指令與瀏覽器 seam，保存既有失敗證據，不安裝依賴。精確來源比對獨立驗證候選保留。排除文章改稿／發布、staging 合回 main、依賴更新、hash 刷新、遠端 merge／deploy、全域設定與外部索引。需要 rollback 時以經審查的 revert 處理，不 reset／force push。
