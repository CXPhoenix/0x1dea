---
synced_from: spec.en.md
synced_from_sha: eb08794ad8eb4f66ce66085d568efe50c79ab107
---
# Discord 驗證檔的來源清單修補

## 問題與目標
Discord 驗證檔已發布到 main 並同步至 staging，但現行 Harness 清單仍以舊 M0 與工程變更為準，因此拒絕這個新路徑。修補目標是讓現行檢查精確接受這一筆已核准來源，並保留既有歷史驗證契約。

## 修補範圍
- 沿用原生 adoption CLI 與 baseline prepare／verify，不新增可由呼叫端選擇的信任模式。
- 只有待驗目標的 HEAD 包含實際發布 commit `0e690064985d9d734849e1ec44a8c0f8d84fb2a3` 時，才要求驗證檔。staging `87ff977bb11c42b810dfedc34c519052f62fbaa7` 已包含此 commit。
- 唯一允許的新增來源為 `blog/public/.well-known/discord`：一般檔案、Git mode `100644`、精確 43 bytes、沒有結尾換行，內容為 `dh=4acc59d1f525794606c4c966b3b879591973fd02`，SHA-256 為 `d28142c7a5a13b28d22abaa933cedc2027ce9abbabb2f09c55b989084caa5019`。
- 發布前的目標維持原本清單；若在發布前樹加入此檔案，仍須拒絕。正常非祖先結果與 Git 查詢錯誤分開處理；publication pin 不可用或查詢失敗時一律拒絕。
- 不排除整個 `.well-known/`、`public/` 或管理資料夾。精確來源集合、角色判定、tracker、落地檢查及 `publishable: false` 全部保留。
- M0、舊 policy 快照、歷史 verifier、五份凍結測試、原斷言、舊收據與 runner 保持原樣。只更新現行工程檔案及必要管理紀錄的精確身分，不把 blog 內容放入 engineering common map。
- 現行測試 adapter 若刻意把 fixture 推進至發布後歷史，可在原斷言執行前準備這筆精確資料；若要建立 Git commit，必須在擷取 tree 前完成。只更新命名 refs、HEAD 仍在舊歷史的 fixture，不得補入新檔案。不修改 frozen 方法、預期結果或 runner，也不依失敗結果改用其他驗證環境。

## 驗收條件
1. 現行 main／staging 的原生檢查接受精確檔案，回報正確角色及 `publishable: false`。
2. 檔案缺漏、內容或換行變動、任一執行位元、symlink 或連結父資料夾均拒絕，不能產生成功報告。
3. 額外的 well-known／public／管理檔案仍拒絕；待驗來源不能修改自己的 policy 來核准任意內容。
4. 歷史 prepare 產物保留原 M0 commit 與原清單，不要求 Discord 檔案；正常非祖先、pin 不可用與查詢錯誤各有對應驗證。
5. 五份 frozen modules 與 runner 逐 byte 不變，原 #22／#32 環境及現行測試都成功；現行 fixture 只補必要資料，不替換斷言或成功結果。
6. 所有既有候選、已發布文章、別名、寫作套件、M0、歷史 pins 與收據保留；獨立審查後兩個實際目標的現行檢查成功，未執行的項目明確標示。

## 測試與流程
使用公開原生 CLI、真實暫存 Git 與獨立身分比對，依 test-plan.md 的 D01–D06 驗證。新增測試與實作前須先由擁有者核准。每次只做一個 red → green 週期，不修改既有歷史測試來消除失敗。

四軸規格審查已完成兩輪，第二輪 P0／P1／P2 均為零；尚未實作或新增測試。建議一張獨立修補票，不依賴 T-0016 或 T-0023，也不關閉或重用這兩張票。已知 T-0023 曾被本機 lab reporter 保留，配置新 id 前必須查核。

## 不包含的工作
不建立通用靜態檔案准入，不自動接受未來紀錄，不操作 Discord 帳號、不發布文章、不推進 P13 或 T-0023、不啟用 workflow、不安裝套件、不調整憑證、rules 或部署設定。先完成可審閱的本機修補；本修補的遠端交付另依當時有效授權辦理。
