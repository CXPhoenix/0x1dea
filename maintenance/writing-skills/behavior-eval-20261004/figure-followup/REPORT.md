# 圖文父 QA 修正與針對性重測

最終 Phoenix 核心為 v2.2，SHA-256 `456ccbb6a52f6fcabad1dfa8e7dfeb072d92aa1518df2cfb8ae149856b338a73`。E7 最終實際正文與操作式教學邊界 E9 各獲新獨立 judge 10/10、pass。中間一次 E7 硬性失敗完整保留；本次只測兩個受影響案例，共三份新 writer 完成輸出，未重跑其他七例。

## 歷史與實際結果

| 版本／案例 | 實際判讀 | 保留的問題或結果 |
|---|---|---|
| 原 v2.0 E7 | 原 judge 9/10、pass；父 QA fail | 移動視線的導語取代正文；原「提問開場」扣分不合技能彈性 |
| [v2.1 E7](cases/E7/judgment-v21.json) | 新 judge 9/10、fail | 「你在10:01讀到舊資料」未標假設，把可能寫成確定事件，屬硬性失敗 |
| [v2.1 E9](cases/E9/judgment-v21.json) | 新 judge 10/10、pass | 明示操作式讀圖教學，準確兩步驟與圖說；保留可能性及範圍 |
| [v2.2 E7](cases/E7/judgment-v22.json) | 再起新 judge 10/10、pass | 自然論述更新／失效落差，假設明示，證據與範圍完整 |

原 E7 的 [input](../cases/E7/input.json)、[output](../cases/E7/output-v2.json)、[judgment](../cases/E7/judgment-v2.json) 均未覆寫。[parent-qa-correction.json](parent-qa-correction.json) 保存父 QA 原因與原八例 32 份 JSON 的 hash。新 rubric 在本目錄 cases/E7；原 rubric 仍留在上層歷史案例，不能當作現行圖文要求。

## 最小變更與來源

核心自檢與 writing-process 要求圖的機制、關係、證據及限制融入論述，一般文章不用移動視線的命令串接；明示操作教學時才導引。style-examples 加一個自然融合正例和操作教學邊界，並補「可能事件」正反例；核心按需參考入口加入圖文。沒有禁止讀者對話，也沒有規定提問開場。

quill draft 的段落功能／文類、revise 的 brief／來源與 uncertainty、explain 的機制／成立條件支持本次選擇；「一般圖文不用移動視線導語」具體規則來自使用者偏好及 repo 選擇，並非偽稱 quill 原文禁令。來源映射追加在 [SOURCES](../../SOURCES.md)。

## 測試與限制

兩位新 writer 各處理 v2.1 E7、E9，第一位新 judge 評兩案；v2.1 E7 失敗後，再起新 writer／新 judge 只處理 v2.2 E7。均 fork_turns none，writer 不讀 rubric、舊輸出、評審或父 QA；judge 不讀舊判讀或主 agent 意見。E7 重測沿用原 user input，只修正技能與預存 rubric。每項 0–2 分，通過需無硬性失敗、各項至少1、總分至少8；不以問句開場評分。

v2.1 與 v2.2 的七份指令原文／hash 分別保存於 instruction-snapshot.json、instruction-snapshot-v22.json，以及兩份 freeze。v2.2 最終 live 指令 hash 與快照一致；E9 僅在 v2.1 實際執行，v2.2 沒有改其已通過的操作教學規則，故未再重跑。不把歷史案例都說成在 v2.2 重測通過。

[check_figures.py](check_figures.py) 預設只讀，核對快照、字數／格式、JSON 判讀一致性和原案例 hash；[mechanical-checks-final.json](mechanical-checks-final.json) 保存實際30項、0失敗。這不代表中間正文無語意失敗，機制／風格結果以獨立 judgment 為準。

[execution-provenance.json](execution-provenance.json)：worker 工具接受 GPT-6.1-sol／high；子 writer／judge API 沒有 fast 欄位。父已回報主 work create 提交 service_tier fast 且 started；這與 worker API 限制分開記錄，本子任務未另讀 provider 遙測。writer 的載入／讀檔紀錄仍為自述，無獨立 instrumentation。

本次是同一指定模型、每輪每例一次的質性觀察，不是跨模型、統計效果、judge 一致率或通過率估計。原資料、失敗與修正均可追溯；未改文章、程式、CSS 或全域入口，未安裝、commit／push／deploy。

## 公開提交投影

以上為執行當時的歷史紀錄。公開提交前只將本機路徑 metadata 改為相對路徑，原始輸出正文、input、rubric、評分與指令快照不變；原始 bytes 與完整 50 檔備份清單保留於 Mac。公開清單排除私有草稿名稱。[公開處理規則與 hash 對照](../../PUBLICATION.md)說明可重跑檢查的範圍。commit／push 狀態以上游 Git 紀錄為準，前文「未 commit／push」指當時驗收。
