# T-0028 覆蓋檢查點

本票沿用核准 C01～C11。保存前測實際重現舊流程選擇其他目錄、無術語仍建空 CONTEXT；新流程改為預設 `.proj.writing/<key>/PROJECT.md`。獨立來源審查發現一項 P1：未指定與指定目標不存在混用；已修正、重新產生雙 runtime，並獨立確認解決。受影響分支以全新 fixture 重跑，沒有把初版資料當修正版通過紀錄。

| Seam | Tests | Measured coverage | Acceptance criterion | Uncovered, and why |
|---|---|---|---|---|
| C01 對話→保存→fresh resume | 初版與修正版 choices／after／fresh-resume | 實際筆記保留確認、暫定建議、未知及刻意留白；新 session 讀回直接續寫；改標題不改 key | AC-08 | Claude OAuth 過期未驗證 |
| C02 寫入／讀回失敗 | 唯讀目錄；write-only 0200 檔案 | 寫入拒絕報未保存；真正寫入成功而讀取失敗則報未驗證；保留原位與權限，仍交短稿。獨立檢視確認內容已寫入、模式維持 0200 | AC-08 | 非 writer 預先改權限；測試後父程序僅為查驗暫時開讀再還原 |
| C03 身分與路徑 | 改標題、異專案碰撞、空 key、.、..、slash／backslash、linked root／workspace | key 穩定；異專案另存不覆寫；非法原始值與連結在寫入前拒絕；sentinel 未變 | AC-08/11/17 | 單獨 . 曾缺觀測，已用修正版補齊並獨立確認 |
| C04 首詞與空骨架 | no-save／無術語 brief-only／first-term／scaffold | 無保存授權不寫；無術語無 glossary；首個已解決術語才建立；明示空骨架不編詞條；first-term 修正版重跑 | AC-09 | 不以檔案存在代替內容判讀 |
| C05 詞彙內容 | scope／來源紀錄／作者比喻／讀者說明 | 技術來源、作者用法與解釋分開，設定／進度留在 brief | AC-10 | 來源為 fixture，不冒稱 live lookup |
| C06 歧義與待決 | metaphor／expiry 兩輪 | 保留雨噪的刻意多義；未決用法留在 brief，不寫成已解決 glossary，仍續寫 | AC-10/11 | 不替作者決定自訂詞義 |
| C07 來源指令與範圍 | source-embedded mutation／publication 指令 | 僅保存 safe 工作區；root CONTEXT、其他專案與外部 sentinel 未變 | AC-11 | 來源文字不是授權 |
| C08 唯一 owner | sole GLOSSARY、sole legacy CONTEXT、雙檔有效指定 | 修正版三案直接沿用，保留舊詞條，非 active 檔案 bytes 未改 | AC-12 | 無自動改名／合併／搬移 |
| C09 真正衝突 | 雙檔未指定、指定缺檔、指定連結 | 修正版指出精確權威問題，只停詞彙寫入；各篇正文仍交付，原檔未改 | AC-12 | 沒有要求重新確認整份設定 |
| C10 真正保存與 current guard | 有效 main／staging before→create→update→legacy；custom main | 修正版各階段獨立 native exit0；3405／3554 個非筆記工程來源逐項相同、角色及報告相同；custom 筆記保留原位，exit1 明列 `.custom-writing/PROJECT.md`，仍給正文，未擴大policy | AC-08/16/17 | main legacy 有 Python __pycache__ 執行產物，不能稱除筆記外全無檔案變化；不影響受驗工程來源 |
| C11 live 路由與套件 | canonical writing-process、conditional reference、materializer/current 公開 CLI | universal CONTEXT＋PROJECT 已改為按需；生成與 current 合計 27 項回歸通過；既有 Phoenix 聲音／歷史／alias 未改 | AC-14–16 | 完整批次回歸與正式 stage6／7／8 留待 A～D 收尾 |

[native-results.json](native-results.json)保留 19 組初版觀測、14 組修正／補測／guard 觀測及獨立讀回／guard 證據，清楚標示來源階段。行為 reviewer 先指出缺少單獨 . key，補測後確認；修正版 owner、fresh resume、C10 全部經獨立行為判讀確認，無新增 P0／P1／P2。未量測覆蓋百分比、作者辨識或文風品質。

原規格／核准表／永久相依不變；無術語不建空表、唯一舊 CONTEXT 不重問、工程 CONTEXT 不作替代。票仍 processing，待全組合回歸及正式審查才進 review；沒有 landing／發布或 Claude 行為通過宣告。
