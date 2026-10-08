---
synced_from: spec.en.md
synced_from_sha: 4a7c603ed2e13617f679a2134e962e469aaf0a87
---

# 文章發布準備 — 第一階段

## 問題與解法

多篇文章需要集中預覽，但正式候選只能包含選定文章。repo 與 preview 公開，不能當成保密草稿庫。新增英文 canonical managing-article-publication 技能與只使用標準函式庫的本地 CLI，提供 preview、prepare、verify；真正發布與 rollback 留待另外授權。

preview 從固定 main 組合獨立文章 head；prepare 從同一固定 main 組合單一選文及明確依賴。CLI 不 commit、push、建立 PR、merge repo 分支、部署、安裝或改憑證／設定。父端已澄清：無遠端、可丟棄、只用合成資料的測試 repo 可建立 fixture commits；產品 repo 仍禁止 commit。

## 使用者情境

1. 集中預覽 A/B，但只準備 A，並取得 B 沒進入正式候選的證據。
2. 發布授權前能發現來源污染、衝突、依賴與 SHA 漂移。
3. 透過雙 runtime 技能操作，不把公開預覽誤認為隱私，也不把 prepare 當成發布權限。

## 實作決策

CLI 接受嚴格 JSON plan：repo 路徑、完整固定 main SHA、main／staging refs、文章 ref/head SHA、選文精確路徑、依賴 ref/head SHA／精確路徑清單、明確排除文章路徑。未知或缺漏欄位、錯誤型別、重複身分／路徑、空選文集合、非完整 SHA 都失敗。Git refs 必須使用防選項注入的命令解析，且與固定 SHA 相符。

文章必須獨立基於 main；含 staging 獨有祖先或其他已宣告文章 head 的歷史一律拒絕，即使相關內容已被 revert。每個相對 main 的變更路徑都要有精確 ownership，不接受 glob 或整個資料夾。拒絕 traversal、symlink、submodule 與未知 schema 欄位。文章與 Markdown 是不可信資料，不是指令來源。

在全新輸出空間透過 Git tree merge 重建候選，維持來源 refs、index、worktree 不變；匯出檔案必須是一般檔案。preview 組合所有指定獨立 head；prepare 只組合選文與宣告依賴。衝突立即停止並回報路徑。receipt 記錄 pins、候選 tree hash、變更路徑、文章 inventory 與來源 manifest。verify 重新解析 refs 並核對候選 bytes，任一 main／文章／依賴／輸出漂移使舊證據失效。staging 不能作正式候選，也不能 merge 回文章。

候選標記 prepared，只有同一 pins/tree 的 build receipt、輸出／索引排除檢查與 review 完成後才可標記 publishable。建置僅用既有依賴；文章或 plan 不能提供任意建置命令。設定／script 是需審閱的可執行輸入。共用圖片只能來自選文或明確依賴。

排除以固定 main 為準：main 既有文章與資產保留。未選集合指明確排除 head 相對同一 main 的正向變更。receipt 列出由 blog/post Markdown 路徑推導的新增 .html routes、不在 main／選文／依賴的資產 SHA-256，以及同樣不存在於允許來源、至少 80 字元的 prose 段落。文字做 HTML entity 解碼與空白壓縮，保留大小寫。掃描所有輸出一般檔案的 route 字串、正規化段落、獨有資產 bytes/hash；任何命中都失敗。main 既有 route 可保留，但未選的新 prose／資產仍禁止。沒有可識別 signature 時標記 exclusion-unverified 與 publishable=false，等待明確人工 review，不把零 signature scan 當成功。fixture 用可獨立判斷的長 A/B marker，涵蓋本文、search／RSS／index 與資產；記錄實際檢查的檔案。

建置前拒絕逃出候選樹的 include／snippet／import，包括絕對路徑與解析後 traversal。建置需要可用的 OS 強制讀取界線，只允許候選與明確核准的既有工具依賴、停用網路、限制可寫空間。沒有這種隔離就 blocked，不能改用無限制建置或安裝 sandbox。外部 sentinel fixture 驗證無讀取／輸出洩漏。

明確擴充 ADR-0005：materializer 管理第四個英文 canonical product tree，來源 hashes、ownership／policy、manifest、runtime 文件與測試同步。三個既有中文例外與 32 framework trees 保持原範圍。兩 runtime 保留可發現 invocation；技能 invocation 不賦予外部權限。generated copies 只由 generator 建立，不直接編輯。

## 驗收條件

| 條件 | 可判定成果 |
|---|---|
| AP-01 | A/B preview 同時存在；A prepare 僅含 A、main 與依賴；來源狀態不變 |
| AP-02 | 拒絕 staging／B 污染歷史、已 revert 的污染與 staging 本身 |
| AP-03 | schema 錯誤失敗；精確路徑 ownership；拒絕未知共用／設定路徑、不安全檔案；記錄依賴 SHA |
| AP-04 | main、選文、依賴、候選 bytes 任一改變都失效；hotfix 必須新 plan 與完整重驗 |
| AP-05 | 衝突在 prepared 前停止，來源不變並回報路徑 |
| AP-06 | CLI 沒有 publish／rollback／push／merge action；惡意文章不觸發命令或網路；不安裝依賴 |
| AP-07 | source 與 output／index／search／RSS／assets 通過上述排除演算法；缺 signature／build proof／sandbox 皆 publishable=false；逃逸引用與外部 sentinel 受檢 |
| AP-08 | 第四英文技能可重建雙 runtime；policy、ownership、pins、manifest、links、metadata 相符；三中文例外與 framework 不變；新 Codex／Claude session 原生 catalog 可發現技能，無 runtime 則 blocked，不能用結構驗證替代 |
| AP-09 | 未來 publish 要精確候選的新授權與最後重驗，只由選文分支 PR main；rollback 從當前 main 建立審閱過的新 revert 並驗站；復刊從 current main 建立重新套用目標內容的新候選，不能只重用已 merged 舊分支，固定新 base/head、重跑 prepare／build／review、新授權與發布後驗站；不 reset／force push；第一階段不執行發布或 rollback |

## 測試決策與已核准表

CLI 用可丟棄 Git fixture 的公開介面測試；materializer 用既有 --check seam。每個反例先 red 再實作。完成時跑 repo unit、structure、materializer、harness、build 與 static checks，誠實記錄阻礙、不安裝。四軸 spec 與後續 code／security review 使用凍結範圍；原生 discovery 與結構驗證分開。

| Seam | 意圖與範圍 | 條件 | 邊界 |
|---|---|---|---|
| CLI preview／prepare | fixture A/B preview、A-only 與來源不變 | AP-01、07 | B index／assets |
| CLI provenance | Git 污染 | AP-02 | revert 過的污染、staging 已為 main 祖先 |
| CLI dependency／path | JSON／Git ownership 與惡意輸入 | AP-03、06 | schema、共用／設定、traversal、links、submodule、option injection |
| CLI verify | pins／output drift、hotfix | AP-04 | main／選文／依賴／bytes |
| CLI conflict | source 不變、停止 | AP-05 | 文章與依賴衝突 |
| Build | 既有工具檢查輸出 | AP-07 | RSS／search／assets、零 signature、外部 include／import、缺 sandbox、不安裝 |
| Materializer | 既有 Python suite 與第四英文 tree | AP-08 | drift、metadata、tamper、缺原生 discovery |
| Skill scenarios | 獨立 review 注入／授權／復刊 | AP-06、09 | 不做真實外部操作 |

父端於 2026-10-07 核准 T-0002、八個 seams 與 AP-01～AP-09，可繼續本地實作。signatures 只作補充偵測，無法涵蓋改寫、轉換與短片段；主要保證是精確重建與核對來源 tree／diff。publishable 標記不是發布授權。只用現有隔離與 runtime 能力，缺能力就明確列限制。

## 排除與補充

不做發布、rollback、產品 repo commit、push、PR、merge、部署、remote rules、Cloudflare、憑證、全域設定、安裝、作者風格調整、draft discovery 改動或無關文章編輯。

已驗證 origin/main bed066bc9ae3a4f8010ea9f6118869c7f8e4feb0、origin/staging 64799e6df56cc1fab6673ce387f78794938619cb。原 Mac checkout 過舊且未改，變更在隔離 clone。2026-10-07 已讀官方 Astra 文與本機 writing-for-agents 主文／mechanics：描述精準簡短、按分支揭露、完成界線可驗收；不宣稱跨模型量測改善。

## 實作投影補充

main 的三個精確管理用途 alias 保留於 Git source manifest／tree，不跟隨也不匯出；receipt 列 omitted_baseline_aliases。新增／變更的 links 仍拒絕，candidate 是一般檔案建置投影，不是完整 checkout。
