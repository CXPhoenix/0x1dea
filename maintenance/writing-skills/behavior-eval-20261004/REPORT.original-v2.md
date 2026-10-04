# Phoenix 實際行為測試（2026-10-04）

八個新 writer 的實際輸出經兩個另起脈絡的 judge 獨立判讀，八例均通過預先保存的規準；七例 10/10，圖文案例 E7 為 9/10。31 項機械檢查全數通過。未在評分後更改技能，v2.0 核心 SHA-256 為 `86cffc593f0184985a2595032edc26b4a8e86eb05a642f76f61841c7f7860d11`。

## 方法與實際配置

- 8 個 writer，每人一例，`fork_turns: none`；不能讀 rubric、他人輸出、live 技能或評審意見。先看候選技能名稱／描述，適用才讀正文及按需參考。封閉案例材料，不瀏覽外部來源或改文章。
- 2 個新 judge，各評四例，只給輸入、rubric、凍結指令與實際輸出；不能讀其他 judge 或主 agent 的評判。每例五項各 0–2 分；通過需無硬性失敗、每項至少 1 分且總分至少 8/10。硬性失敗含違反明示格式、改受保護事實／立場、捏造證據／經驗、未授權副作用或錯誤機制。
- 原生 collaboration.spawn_agent 接受 `model: gpt-6.1-sol`、`reasoning_effort: high`。使用者要求 fast，但該工具沒有可指定的 fast 控制；不把 service tier 描述當成 fast 驗證。配置記錄見 [execution-provenance.json](execution-provenance.json)。
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
| [E7](cases/E7/judgment-v2.json) | 已有圖的正文與圖說、時間差及圖的界限 | 9/10，pass |
| [E8](cases/E8/judgment-v2.json) | 熟練／初學兩種篇幅，不套固定章節模板 | 10/10，pass |

每個 cases 目錄保留原 input、預存 rubric、完整 output 與逐項 judgment，引用實際輸出說明評分理由。[results-v2.json](results-v2.json) 可供程式讀取。

E7 的「由問題引出圖中時間差」項目只得 1 分：實際開頭是「你可以先盯著10:00」，直接帶看圖，未先提出讀者疑問。其他四項完整符合，無硬性失敗。這是可改善的表達選擇，不足以支持所有篇章強制提問；維持技能的文類／篇幅彈性，沒有為單一樣本加固定開場或重跑已通過案例。

## 可重驗的證據與範圍

[freeze.json](freeze.json) 是測試開始時的七份指令 hash；[instruction-snapshot.json](instruction-snapshot.json) 保存其 UTF-8 原文。副本以 JSON 保存，避免證據文件再成為有效 agent 指令。原執行路徑在 freeze 中保留；可攜副本不依賴其絕對路徑。

[check_mechanical.py](check_mechanical.py) 預設僅讀取與輸出檢查結果（`--write-report` 才重新保存結果），可重新確認快照 hash、Han 字數（U+4E00–U+9FFF）、英文 whitespace words、保護文字、格式及指定程式修復；[mechanical-checks-v2.json](mechanical-checks-v2.json) 是實際 31 項結果。它不判定作者風格或機制語意，後兩者由保存的獨立 judgment 判讀。測試後七份 live 指令 hash 與凍結版仍一致。

僅新增測試證據與驗收紀錄，未改原文章、程式、CSS、全域入口、憑證或安全設定；未安裝工具、commit、push 或 deploy。新文 CLI、舊 validator、搬移與 symlink 驗證仍在上一階段 [VALIDATION.md](../VALIDATION.md)。
