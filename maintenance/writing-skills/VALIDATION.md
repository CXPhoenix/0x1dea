# 寫作技能搬移驗收

日期：2026-10-04。狀態：指定 skills-mcp 當前版本的主文與必要 references 已讀取並複核，來源阻礙已解除。核心、流程、搬移及代表性案例已完成，歸檔狀態見下方最終驗證。

## 實際執行結果

| 項目 | 結果與範圍 |
|---|---|
| 起始 Git 狀態 | 0x1DEA 乾淨；Mac custom_skills 原有 untracked writing-human-prose/，未改該目錄 |
| 搬移前檢查 | canonical Phoenix 檔案尚不存在，repo/global samefile 驗收如預期失敗 |
| 相容入口 | repo .agents、.claude、Mac 原位、全域 Codex、全域 Gemini 共 5 個 SKILL.md 都 samefile 到 skills/phoenix-writing/SKILL.md |
| 可恢復備份 | ~/.agents/skill-backups/phoenix-writing-pre-codex-20261004 的 50 個原檔 SHA-256 與 manifest 一致；另有執行 workspace 完整副本。備份放在有效技能掃描根目錄外 |
| 歷史與 validator | 保留指引、reference 和 validator byte-equivalent；歷史 AGENTS/CLAUDE 改檔名 .md.txt 避免成為有效指令 |
| 舊 validator | 在可寫隔離副本執行既有 test_tier1.py：11/11，test_tier2_tier3.py：17/17。共 28 個通過；這只驗舊工具相容，不驗新風格品質 |
| Frontmatter | 3 個有效技能以 YAML 解析驗 name、description 和長度，均符合；Phoenix 與維護技能通過本地 skill-creator quick_validate |
| quick_validate 限制 | 本地檢查器 allowed keys 未含 compatibility，對原有新文技能報此欄位不支援。保留準確的原欄位，以直接 YAML 解析補核；未修改全域 validator 或假稱三份皆通過該檢查器 |
| 新文 CLI 契約 | 使用已有 Node v24.13.0 和 repo 已有 tsx，在 workspace/scaffold-fixture 實際執行 helper；生成 Hello_World.md、同名資源資料夾與 +08:00 時戳。重複檔名退出 1 且原文未改，-c/-d 同用退出 1 且錯誤字串符合。未建立 repo 文章、未安裝工具 |
| 風格與路由 | [11 個案例與實際小樣本](tests/cases.md)：明示 Phoenix、英文無幽默 80 字上限、一般繁中、正式紀錄、純程式、既有正文草稿、假設經驗、保留立場、圖表融入正文，另加專案詞彙／任務分離與正式模板案例。均由本 agent 自行評閱；英文例為 57 words |
| Claude 殘留 | [分類盤點](INVENTORY.md) 與 residual-inventory.json，區分相容名稱、生成工作流、hook、歷史規則、外部個人技能相依；不宣稱完全移除 Claude |
| 引用與 symlink | 首輪 44 個有效／新增本地連結全部可解析；新版來源複核與歸檔後的連結數見下方最終驗證，完成有效文件的本地連結、技能入口與相容 scripts/reference 解析檢查；README 原有 CONTRIBUTING.md 缺檔不在本次新增範圍 |
| Diff 範圍 | 僅指引、技能、歷史／驗收與 Spectra artifacts；不改 docs 文章、網站程式或 CSS。git diff --check 通過。沒有 commit/push/deploy |

## 已處理的環境限制

第一次直接在 read-only repo 執行舊測試時，測試嘗試暫時改名 config.json，被 sandbox 擋下；已改在 hash-equivalent 可寫測試副本執行，28 個測試全通過，原 config 未修改。第一次隔離 CLI 測試因 PATH 找不到 node 未啟動；後續找到已有 NVM Node 並用絕對路徑成功執行，未改 shell 或全域設定。

## 來源複核與驗證限制

- 已改用使用者指定 @skills-mcp 的 load_skill/read_skill_resource；新版 quill 的 references 是 plan/draft/revise、project-context、context-handling、explain、glossary 與相關 genres 子檔。writing-for-agents 的 SKILL-MECHANICS.md 也已讀。兩份主文共 2 檔、必要 references 共 11 檔，EOF 與 SHA-256 均核對，版本和 hash 在 [source manifest](skills-mcp-manifest.json)。先前 catalog 檔名差異及失敗保留為歷史，現在不再是阻礙。
- 依新來源將 Phoenix 核心再收斂，寫作流程揭露到 writing-process.md；CONTEXT.md 限術語，PROJECT.md／既有任務文件保存需求與決策。保留正式摘要、有用回顧與段落功能，沒有複製 ChatGPT 的「下次上傳」宿主限制。未匯入研究統計或身份／偵測規避目標。
- 9 個既有樣本按最新來源逐項再評閱，仍符合聲音／明示要求／證據／文類邊界；追加專案詞彙與正式模板案例。這仍是本 agent 自檢，不是獨立或跨模型 eval。
- 最終 Spectra validate/analyze、連結檢查與歸檔結果在下方最終驗證記錄；未用 mark-tasks-complete 或 no-validate 跳過必要驗收。
- 搬移首輪未執行獨立評審；後續使用者另行授權的獨立行為測試見下方追加紀錄。未執行跨模型 eval、網站 build 或完整網站測試。本次沒有網站程式變更，不把未執行項目當成通過。

原始 hash 清單在 [original-manifest.json](original-manifest.json)，來源與 repo 選擇在 [SOURCES.md](SOURCES.md)，位置與復原在 [MIGRATION.md](MIGRATION.md)。本機完整測試 log 在 本機 migration-evidence，供此次驗收；其他 contributor 不依賴這些本機路徑。

## 最終驗證

- skills-mcp 當前 immutable version 的主文／references 共 13 檔已核對 SHA-256 與 EOF；來源缺口解除。
- 新版核心為 2,850 bytes；50 個有效／新增本地連結全部可解析，3 份 frontmatter 名稱／描述有效，5 個 Phoenix 入口仍指向同一來源。原備份 50 個檔案 hash 一致。
- 11 個文字與路由案例按新版來源自評通過；28 個舊 validator 測試、隔離 helper 的建立／衝突／互斥旗標測試結果保留，不因文檔修訂重複跑無關測試。
- Spectra validate 通過，analyze 無 Critical／Warning，4 個 concrete-example Suggestions 保留。5/5 任務實際完成。
- 已執行 spectra archive migrate-writing-skills-to-codex --yes；[歸檔任務](../../openspec/changes/archive/2026-10-04-migrate-writing-skills-to-codex/tasks.md)，同步 phoenix-style-and-maintenance 與 vitepress-post-scaffolding，CLI 報 added 3／modified 2。建立可復原 spec snapshot，未使用跳過驗證或強制完成旗標。
- git diff --check 通過；沒有文章、程式、CSS、憑證或安全設定修改，沒有 commit／push／deploy。

## 使用者授權後的獨立行為測試

2026-10-04 另以 8 個新脈絡 writer 各產生一例、2 個新脈絡 judge 各評四例；工具接受 GPT-6.1-sol／high 指定。完整輸入、預存規準、實際輸出、獨立評分、指令快照及配置限制已保存於 [行為測試報告](behavior-eval-20261004/REPORT.md)。

- 八例均通過，七例 10/10，圖文案例 9/10；沒有硬性失敗。涵蓋風格適用／純程式不適用、英文無幽默、正式模板、保留作者立場與證據、圖文融合與不同篇幅。
- 31 項 hash／長度／格式／保護文字機械檢查通過；七份指令測試後與凍結 hash 一致，Phoenix 核心仍為 v2.0，未因單一開場偏好加入強制提問規則。
- 一例一次完成、同一指定模型，未測 v1 baseline 或跨模型效果。技能載入與讀檔紀錄為 writer 自述，沒有獨立 instrumentation；fast 雖為使用者偏好，原生 worker 工具未提供其控制，未宣稱已驗證。
- 這次只追加驗收證據，沒有修改原文章、網站程式或全域入口，未安裝工具、commit／push／deploy。

## 圖文父 QA 與 v2.2 最終驗收

前節「八例均通過」是首輪 judge 歷史判讀；父 QA 否決 E7 的操作式導語及固定問句開場 rubric。原八例 32 份 JSON hash 保持不變，未覆寫歷史。

- 最小修正核心自檢、圖文風格對照及寫作流程，圖的機制／證據直接融入正文；明示操作教學才導引。按需參考加入圖文，假設情境須標示，沒有規定問句開場或禁止讀者對話。
- v2.1 E7 首次重測因「你在10:01讀到舊資料」未標假設而被新 judge 判 9/10、hard fail；v2.1 E9 操作教學邊界 10/10、pass。v2.2 僅再重跑 E7，另一新 judge 判10/10、pass。三份實際輸出與兩位新 judge 的完整證據在 [後續報告](behavior-eval-20261004/figure-followup/REPORT.md)。
- 最終核心 v2.2 SHA-256：456ccbb6a52f6fcabad1dfa8e7dfeb072d92aa1518df2cfb8ae149856b338a73。30項機械檢查通過，七份最終 live 指令 hash 與凍結版一致；其他七例未重跑。
- 父回報主 work create 已提交 service_tier fast 且 started；子 writer／judge API 沒有 fast 欄位。本子任務未獨立查看 provider 遙測。模型／effort工具指定為 GPT-6.1-sol／high，不把一次同模型質性觀察說成統計效果或跨模型 eval。

最終結構驗證：5個 Phoenix 入口同源、59個本地引用可解析、git diff --check 通過。Spectra validate 通過，analyze 無 Critical／Warning，保留2個具體例子 Suggestions（optional design 未建立，Consistency 因此略過）。4/4 任務完成，已正常 [歸檔圖文修正](../../openspec/changes/archive/2026-10-04-integrate-figures-in-prose/tasks.md)，規格 added1；未跳過驗證或強制完成任務。

## v2.2 九案例完整回歸定版

使用者批准後另起9位writer、3位獨立judge，E1–E9全部以同一份凍結v2.2執行；原 input／rubric hash 保持不變，E7採修正後不要求問句開場的規準。九例首次輸出均10/10、pass，無hard failure，無重試或技能修改；完整證據與前後版本對照在 [九案例回歸報告](behavior-eval-20261004/full-regression-v22/REPORT.md)。

- 本輪完整驗證版本為2.2，核心hash仍456ccbb6a52f6fcabad1dfa8e7dfeb072d92aa1518df2cfb8ae149856b338a73，七份live指令與凍結版一致；62項機械檢查通過。
- 最近有效歷史基準分別為v2.0（E1–E6／E8）、v2.2（E7）、v2.1（E9），逐案分數差皆0；這只是本次可觀察結果，無跨模型／統計／未來可靠度保證，三位judge評不同案例，未測一致率。
- 初次檢查器錯把E5空list要求成literal false，已按原本未限定型別的harness修正，保留初次結果；未改writer輸出或rubric。E3讀檔紀錄的精度差異保留，路由／讀檔仍僅自述。
- 所有worker工具指定為GPT-6.1-sol／high，子API無fast欄位；主work fast依父回報提交且started，非子任務provider遙測。本輪僅追加驗收，未修改正式文章、程式、CSS、管理設定或全域入口，未安裝／commit／push／deploy。

## 公開提交投影

以上為執行當時的歷史紀錄。公開提交前只將本機路徑 metadata 改為相對路徑，原始輸出正文、input、rubric、評分與指令快照不變；原始 bytes 與完整 50 檔備份清單保留於 Mac。公開清單排除私有草稿名稱。[公開處理規則與 hash 對照](PUBLICATION.md)說明可重跑檢查的範圍。commit／push 狀態以上游 Git 紀錄為準，前文「未 commit／push」指當時驗收。
