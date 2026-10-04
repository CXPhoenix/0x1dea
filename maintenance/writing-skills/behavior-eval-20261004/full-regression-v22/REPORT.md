# v2.2 九案例完整回歸

九個新 writer 各完成一例，三個另起脈絡的 judge 各判讀三例；九例首次輸出均為10/10、pass，無硬性失敗。全部使用同一份凍結 v2.2 指令，沒有混用版本或重試，測試期間未改技能。核心 SHA-256：`456ccbb6a52f6fcabad1dfa8e7dfeb072d92aa1518df2cfb8ae149856b338a73`。

## 原始要求與證據

E1–E6、E8 沿用首輪 input/rubric；E7 沿用圖文修正後、不要求問句開場的 rubric與原 input；E9 沿用操作式讀圖教學 input/rubric。18份 input/rubric hash在 [case-manifest.json](case-manifest.json)，本輪未修改。每個 cases 子目錄保留 input、rubric、output-reg22 和 judgment-reg22 的完整 JSON；baselines保存逐案對照的實際舊輸出、判讀與規準。

## 前後對照

| 案例 | 對照版本 | 對照分數 | 本輪 v2.2 | 分數差 |
|---|---|---|---|---|
| E1 | 2.0 | 10/10 | 10/10、pass | 0 |
| E2 | 2.0 | 10/10 | 10/10、pass | 0 |
| E3 | 2.0 | 10/10 | 10/10、pass | 0 |
| E4 | 2.0 | 10/10 | 10/10、pass | 0 |
| E5 | 2.0 | 10/10 | 10/10、pass | 0 |
| E6 | 2.0 | 10/10 | 10/10、pass | 0 |
| E7 | 2.2 | 10/10 | 10/10、pass | 0 |
| E8 | 2.0 | 10/10 | 10/10、pass | 0 |
| E9 | 2.1 | 10/10 | 10/10、pass | 0 |

對照取最近有效輸出：E1–E6／E8為v2.0，E7為上輪v2.2，E9為v2.1。此表標明混合歷史基準；「完整驗證版本」只指本輪九例全部在v2.2執行，不把歷史基準說成同版實驗。原E7父QA fail與v2.1獨立hard fail仍在 [圖文歷史](../figure-followup/REPORT.md)，未被新結果覆寫。

本輪沒有較低分、硬性失敗或實質回歸需補救。文字有變化但目前五項規準皆滿足；一例一次和不同judge不能量化隨機變異，也不能證明未來可靠度、模型提升或統計顯著。三位judge評不同案例，沒有同案重複評分，不能計算一致率。[results.json](results.json)保存每例版本、分數、差異及限制。

## 實際執行配置與驗證

9位writer、3位judge全為fresh fork_turns none，原生工具接受 GPT-6.1-sol／high。writer不能讀rubric、baseline或評審意見；judge不能讀baseline／主agent判斷。worker API沒有fast欄位；父回報主work create已提交service_tier fast且started，兩者分開記錄於 [execution-provenance.json](execution-provenance.json)。本子任務未另讀provider遙測。

七份指令原文與hash在 [freeze.json](freeze.json)、[instruction-snapshot.json](instruction-snapshot.json)。測試後七份live檔案仍與凍結版一致。本輪62項快照、字數、格式、保護文字、input/rubric不變及判讀JSON一致性檢查通過，見 [mechanical-checks-reg22.json](mechanical-checks-reg22.json)。[check_regression.py](check_regression.py)預設只讀，--write-report才保存新檢查結果；機械檢查不替代獨立語意／風格判讀。

初次檢查器將E5的空list誤當成未回報「不套技能」；harness沒有要求boolean型別，已修正接受空表示，保留初次結果及 [checker-correction.json](checker-correction.json)。這是驗證器表示方式修正，沒有修改writer輸出、rubric或技能。E3 files_read以檔案路徑紀錄，execution_note細分header／正文，粒度差異已由judge註記；兩者皆自述，沒有獨立instrumentation，不能推定實際讀檔副作用。

這次只追加完整回歸證據與驗收紀錄；未改正式文章、程式、CSS、管理設定、技能內容或全域入口，未安裝、commit、push、deploy。管理方式與harness成本詢問另作唯讀估算，不視為遷移授權。

## 公開提交投影

以上為執行當時的歷史紀錄。公開提交前只將本機路徑 metadata 改為相對路徑，原始輸出正文、input、rubric、評分與指令快照不變；原始 bytes 與完整 50 檔備份清單保留於 Mac。公開清單排除私有草稿名稱。[公開處理規則與 hash 對照](../../PUBLICATION.md)說明可重跑檢查的範圍。commit／push 狀態以上游 Git 紀錄為準，前文「未 commit／push」指當時驗收。
