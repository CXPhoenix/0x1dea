# Phoenix 實際行為測試（2026-10-04）

以下保留首輪 v2.0 的判讀：兩位 judge 曾將八例判為 pass，七例 10/10、E7 9/10。父 QA 後續否決 E7 的讀圖操作導語及不合理的問句開場 rubric；不能把首輪結果當成最終 QA。31 項機械檢查只證明格式與快照。首輪核心 SHA-256 為 `86cffc593f0184985a2595032edc26b4a8e86eb05a642f76f61841c7f7860d11`。

最新圖文結果：E7 v2.2 與 E9 操作教學邊界 v2.1 分別由新 judge 判為 10/10、pass；中間 v2.1 E7 9/10、hard fail 完整保留。詳見 [圖文修正與針對性重測](figure-followup/REPORT.md)。原八例 JSON 未改；原報告保存於 [REPORT.original-v2.md](REPORT.original-v2.md)。其他七例未重跑。

最新完整同版回歸：已依使用者授權將 E1–E9 全部用同一份凍結 v2.2 重跑，九例首次輸出均10/10、pass；未改技能、未重試。完整 input/output／judge／前後基準與62項驗證見 [v2.2九案例回歸](full-regression-v22/REPORT.md)。下方首輪與圖文歷史仍保留，不混算版本。

## 首輪方法與實際配置

- 8 個 writer，每人一例，`fork_turns: none`；不能讀 rubric、他人輸出、live 技能或評審意見。先看候選技能名稱／描述，適用才讀正文及按需參考。封閉案例材料，不瀏覽外部來源或改文章。
- 2 個新 judge，各評四例，只給輸入、rubric、凍結指令與實際輸出；不能讀其他 judge 或主 agent 的評判。每例五項各 0–2 分；通過需無硬性失敗、每項至少 1 分且總分至少 8/10。硬性失敗含違反明示格式、改受保護事實／立場、捏造證據／經驗、未授權副作用或錯誤機制。
- 原生 collaboration.spawn_agent 接受 `model: gpt-6.1-sol`、`reasoning_effort: high`。子 writer／judge 工具沒有可指定的 fast 控制；父已回報主 work create 提交 service_tier fast 且 started，兩者分開記錄，不以子工具限制推定主 work。配置記錄見 [execution-provenance.json](execution-provenance.json)。
- 每例只有一次 completion；writer 與 judge 使用同一指定模型。這是本次八個輸出的獨立判讀，不是跨模型、統計勝率或與 v1 的實驗比較。原 11 例自評另行保留，不混算。
- `invoked_skill`／`files_read` 為 writer 自述；未取得獨立工具軌跡，不能據此證明實際載入或所有副作用。可見交付、保護文字與本次 repo Git 狀態另行核對。

## 逐例結果

| 案例 | 可見要求 | 獨立判讀 |
|---|---|---|
| [E1](cases/E1/judgment-v2.json) | 初學者付款冪等性、同鍵條件與服務界限 | 10/10，pass |
| [E2](cases/E2/judgment-v2.json) | 僅改兩句、frontmatter／引文／立場逐字保留 | 10/10，pass |
| [E3](cases/E3/judgment-v2.json) | 英文 ≤80 words、無幽默／提問 | 10/10，pass |
| [E4](cases/E4/judgment-v2.json) | 正式簽呈三行、數量／日期／提案狀態精確 | 10/10，pass |
| [E5](cases/E5/judgment-v2.json) | 純 Python 語法修正、不套作者風格 | 10/10，pass |
| [E6](cases/E6/judgment-v2.json) | 修訂保留先不採用與單機十次證據範圍 | 10/10，pass |
| [E7](cases/E7/judgment-v2.json) | 已有圖的正文與圖說、時間差及圖的界限 | 首輪 9/10、pass；父 QA fail |
| [E8](cases/E8/judgment-v2.json) | 熟練／初學兩種篇幅，不套固定章節模板 | 10/10，pass |

每個 cases 目錄保留原 input、預存 rubric、完整 output 與逐項 judgment，引用實際輸出說明評分理由。[results-v2.json](results-v2.json) 可供程式讀取。

首輪 E7 的提問開場扣分已被父 QA 更正：Phoenix 不要求固定問句開頭。真正問題是「先盯著」「沿著時間線往右看」「再把視線拉回」等導語取代自然正文，不符合使用者偏好。後續另存修正 rubric、自然圖文正例、明示操作教學邊界，及一次未標假設的實際重測失敗；沒有覆寫原判讀，最新結果見上方連結。

## 可重驗的證據與範圍

[freeze.json](freeze.json) 是測試開始時的七份指令 hash；[instruction-snapshot.json](instruction-snapshot.json) 保存其 UTF-8 原文。副本以 JSON 保存，避免證據文件再成為有效 agent 指令。原執行路徑在 freeze 中保留；可攜副本不依賴其絕對路徑。

[check_mechanical.py](check_mechanical.py) 預設僅讀取與輸出檢查結果（`--write-report` 才重新保存結果），可重新確認快照 hash、Han 字數（U+4E00–U+9FFF）、英文 whitespace words、保護文字、格式及指定程式修復；[mechanical-checks-v2.json](mechanical-checks-v2.json) 是實際 31 項結果。它不判定作者風格或機制語意，後兩者由保存的獨立 judgment 判讀。測試後七份 live 指令 hash 與凍結版仍一致。

僅新增測試證據與驗收紀錄，未改原文章、程式、CSS、全域入口、憑證或安全設定；未安裝工具、commit、push 或 deploy。新文 CLI、舊 validator、搬移與 symlink 驗證仍在上一階段 [VALIDATION.md](../VALIDATION.md)。

## 公開提交投影

以上為執行當時的歷史紀錄。公開提交前只將本機路徑 metadata 改為相對路徑，原始輸出正文、input、rubric、評分與指令快照不變；原始 bytes 與完整 50 檔備份清單保留於 Mac。公開清單排除私有草稿名稱。[公開處理規則與 hash 對照](../PUBLICATION.md)說明可重跑檢查的範圍。commit／push 狀態以上游 Git 紀錄為準，前文「未 commit／push」指當時驗收。
