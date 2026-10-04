---
language: zh-TW
authority: spec.en.md
synced_from: spec.en.md
synced_from_sha: 8114acb27db2c27b159667e97a398dd2e49f5b68
source_path: .proj.specs/0001-harness-adoption/spec.en.md
historical_harness_review: not-recreated
---
# Harness 採用規格稽核翻譯

> 英文 spec.en.md 是權威；本頁依完成零 P0 審查後的英文版本全文翻譯，不重建歷史 Harness review（`historical review not recreated`）。英文來源的第二輪候選說明如下：G1／G4 於 2026-10-04T07:24:41Z 獲批准；擁有者於 2026-10-04T10:30:04Z 批准網站根目錄整體搬移及列明的兩個 alias 輸入例外。實作仍以本輪零 P0 結果為 gate，稽核翻譯在其後進行。不推導 landing 或外部寫入授權。

## 問題

0x1DEA 需要採用使用者的本地 harness 流程，同時保留網站公開行為、歷史 Spectra 證據及通過驗證的 Phoenix 寫作。標準 Harness 管理 Markdown 放在 docs 下，會被目前以 docs 為根的 VitePress 編譯。擁有者選擇將完整網站根搬至 blog，docs 留給管理文件。兩個既有 canonical 相容 symlink 需要明確輸入來源，同時不得建立含連結的 runtime 套件。

## 解法

在獨立 checkout 採用固定模板，保留內部相對路徑搬移整棵網站，保留不可變歷史，提供單一本地 epic／ticket tracker 與可重現的實體 runtime 套件。只投影已批准的 metadata、本地連結深度、管理路由與網站目錄字面值；不改寫風格規則或一般產品行為。

## 使用者故事

1. 擁有者需要單一本地 tracker，依賴、批准與證據都必須如實。
2. 貢獻者需要在新的原生 runtime 發現技能，不依賴全域 Phoenix 安裝。
3. 稽核者需要保留來源位元組，並以雙語追溯區分繼承、精準局部取代及缺漏證據。
4. 維護者需要網站 URL 與內容不變，並有管理及目錄採用的完整回歸與復原證據。

## 來源、復原與實際授權

產品：`ee7fecfff72f47abc735d26ac7e9a943de04ebbf`，staging／origin-staging 基準。模板：`917e6025da0901a79dda016e1ce5bd89b6e6e19f`；原始 718 檔快照 digest 為 `b7782890459cf3c546395ac5546f22dc074f13d4166688751a9c1e08d4216bf5`。恢復工作時已重新核對兩個原 repo 都乾淨。

舊 task checkout 的 Git metadata 及最新草稿成為 macOS dataless；一般讀取與精準升權讀取都停滯，保留原樣不動。新的獨立、無 hardlink clone `implementation-resumed` 固定於相同基準。修訂規格由可讀的凍結第一輪輸入、全部已記錄第一輪 findings，以及新批准例外重建；不聲稱它是無法存取的中間草稿之逐位元組復原。凍結 `review/prompt.md`、113 列 baseline 與矩陣由可讀原始 artifact 複製；prompt 保持原文。

初始 G1／G4 回執：使用者 `Sentinel_07d4ae9a14e4819181b0aed2f6c183a9`，`2026-10-04T07:24:41Z`，對 Charter／範圍、單一 adoption ticket／順序及完整測試矩陣回覆「同意」。範圍回執：使用者 `Sentinel_eb826c38100881919fd654dee5b7d247` 回覆助理 `Sentinel_bbd52dfc79f0819191e9787b1704d80c`，`2026-10-04T10:30:04Z`：「cf pages 我改好了 / 其他都同意」。被引用的問題明確列出整體 docs→blog 網站搬移，以及正好兩個相容 canonical 連結來源例外。此批准裁定先前的產品位元組範圍與 alias 輸入衝突；投票不能取代擁有者決策。

## 驗收條件

- **HA-01:** 必須使用固定的獨立 clone，以及精確 vendored 模板來源、license 與來源脈絡；原始 staging／模板必須保持不變。意外基準變更必須停止受影響工作。產品原 LICENSE 必須逐位元組不變；模板根 license／notices，以及每個匯入技能適用的 license／upstream 快照都必須保留，不聲稱未驗證的授權或新的 tuning 結果。
- **HA-02:** 全部六個 capabilities、32 個 requirements、81 個 scenarios 及四個原始 archives 都必須以原路徑、anchor、Git blob、SHA 建立索引。原 openspec、.spectra.yaml 與歷史寫作 artifact 必須保留位元組及失敗。缺少的歷史 Harness review／TDD／landing 必須標示「not recorded under harness」，不得補造。
- **HA-03:** 可執行工作只能以設定的 .proj.specs 與 .proj.tickets 作為本地權威。停用的 Spectra agent 指引／命令必須保留為不會被發現的文字證據。範圍不包含 Notion 寫入或新的 release／deployment CI；Notion 是父任務管理的索引。
- **HA-04:** 正好 phoenix-writing、maintaining-writing-skills、creating-vitepress-post 三者必須各有單一 canonical 編輯來源，以及確定性、完整的實體 Codex／Claude 套件。兩個 runtime 樹的任何深度都不得有 symlink。輸入只能是已追蹤的 regular canonical 檔案、明確逐檔列出的 regular alias backing 檔案，以及批准的新管理參考。未知輸入、未知連結、缺少／多出檔案、越界、backing 巢狀 symlink、alias 字面值／target 改變或輸出漂移，都必須在部分取代之前失敗。
- **HA-05:** Codex 必須有 agents/openai.yaml，且不得有 Claude 專屬 frontmatter；Claude 不得有 Codex metadata。各技能的 manual／implicit 政策必須相符，產品寫作保持可發現／可隱式觸發。每棵樹必須包含初始化模板的 32 個框架技能加三個產品技能，以及完整必要 assets、license、原生角色設定。新的原生 Codex discovery 必須觀察實際候選，不依賴全域產品安裝。SKILL、AGENTS 與 references 的 Markdown 引用，在 runtime 多一層後仍必須可解析。
- **HA-06:** 共用管理保留擁有者 gates、既有產品 Charter 與獨立 landing 授權，不得聲稱 walking-skeleton 豁免。只有上述三個 canonical 寫作樹及生成 runtime 對應內容／參考，保留已驗證的台灣繁體中文 v2.2 正文。新 AGENTS／CLAUDE／docs/agents／ADR／框架管理維持英文。名稱、範圍、版本、來源與理由必須明列。Phoenix v2.2 三個核心檔案維持原始精確雜湊；舊七檔 freeze 保留為歷史證據，新批准的路由／路徑改變另建新 freeze 與新 E1–E9 評估。
- **HA-07:** 新 spec.en.md 必須是權威。六份匯入英文 baseline 必須保留原英文位元組。zh-TW 稽核翻譯必須有相符的 Git blob synced_from_sha 與「historical review not recreated」說明。adoption 稽核翻譯在零 P0 審查後進行。每列 trace 必須連到真實來源、AC、已分配 ticket、實際證據或未驗證狀態。過期翻譯、懸空來源／AC／ticket 及假冒通過的證據都必須失敗。
- **HA-08:** Ticket ID 必須全域、連續且永久，透過掃描每個 ticket epic 分配。儲存狀態只有 todo／processing／review／done／pending；blocked 由條件推導。重複 ID、缺少／自我依賴、循環、pending 的原因／證據／日期／重訪 metadata 不完整，以及沒有實際授權 landing 證據的 done，都必須失敗。單一 adoption tracer-bullet ticket 涵蓋套件 → tracker／歷史 → 完整回歸／復原，結束為 review，不是 done。landing 目標仍是 staging，需之後另授權；來源 CF production main 不變。
- **HA-09:** 全部 55 個已追蹤網站檔案必須由 docs/<relative-path> 搬至 blog/<relative-path>，位元組不變，包含 .vitepress／public／shared／post 及根頁。只有下文精確六個網站外產品檔案可以修改目錄字面值。原公開 URL、內部文章路徑、文章／frontmatter／createdTime、圖片、資料形狀、filter／sort／slice 行為、粒子行為、dependency 版本及 lockfile 必須不變。實際候選 unit／build／CLI／UI／writing 檢查必須用已記錄的等價條件；每項未執行的必要檢查維持 not-run／blocked，不得稱通過。必須防護新增、移除與修改產品路徑，而非只檢查舊路徑雜湊。
- **HA-10:** 可丟棄環境中的復原必須還原原 docs 樹及舊技能入口，重跑 baseline unit／CLI／build／hash，不碰兩個原 repo。沒有授權 commit、push、PR、merge、deployment、CF 編輯、安裝、權限／憑證改變或全域技能修改。

## 精確批准的產品路徑例外

docs 下每個 regular baseline 檔案搬到 blog，相同 suffix、相同 SHA。此搬移不允許編輯任何網站檔案內容；內部 loader `post/**/*.md`、公開 URL、nav／sidebar 及全部五個跨檔匯入保持不變。網站外只有六個檔案可修改目錄字面值：

1. package.json：正好 docs:dev／docs:build／docs:preview 三個命令的根目錄參數 docs→blog。版本、dependencies、packageManager、new:post／test scripts 不變。
2. scripts/vpHelper.ts：DEFAULT_DIR docs/post→blog/post；ASSETS_ROOT docs/public/assets→blog/public/assets；對應註解可用新根名稱。不得改 parser、時間、檔名、cwd、asset-prefix 演算法、錯誤或重複處理行為。
3. tests/vpHelper.vitest.ts：目錄常數／fixtures／標籤反映 blog；全部原斷言與 11 個產品測試保留。另加有意義的搬移斷言，不削弱期待。既有小寫 vphelper 匯入及其他無關缺陷分類為 baseline，不順便修復。
4. tsconfig.json：兩個 docs include 改為 blog，其餘編譯器設定不變。
5. skills/creating-vitepress-post/SKILL.md：網站根、預設、分類、自訂、根目錄與 assets 範例及契約的目錄字面值改為 blog。Repo 連結、作者聲音、安全／觸發規則及其他語意保留；生成時亦套用已批准 runtime 投影。
6. README.md：本地網站路徑、範例、圖片路徑前綴反映 blog，附上同意的管理入口。既有無關的缺少截圖引用必須揭露，不私下修復。

不得從此例外推導新網站行為。明確 `-d docs/...` 仍代表該明確 repo 相對目錄，helper 不會自動將它 alias 到 blog。此舊明確輸入現在位於 build source 之外，技能必須準確回報；批准的慣例改為 blog。預設、`-c` 與 assets 實體根刻意改變；資料夾名稱 post_x／root_x 與公開 `/assets/x` URL 不變。不加入 srcDir／base／cleanUrls／rewrites／outDir 覆寫。

不可變 baseline-files.json 列出全部 370 個 tracked entries 的型態／雜湊。candidate-delta manifest 必須列出全部 55 個路徑投影、六個精確產品例外、管理 adapter，以及退休／生成 entries；未知修改、新增產品檔案或缺少搬移檔案都失敗。不可變歷史留在原路徑、保留原位元組。核心風格 freeze 檔案：skills/phoenix-writing/SKILL.md、references/style-examples.md、references/tw-vocabulary.md，雜湊來自原 v2.2 freeze。

## 精確批准的 alias 輸入政策

Canonical aliases 保留字面 symlink；產生器永不沿它們列舉輸入。只允許下列兩個映射：

| Canonical alias | 必要字面 target | Regular backing 樹 | 實體 runtime 子路徑 |
| --- | --- | --- | --- |
| skills/phoenix-writing/reference | ../../maintenance/writing-skills/legacy/phoenix-writing/reference | maintenance/writing-skills/legacy/phoenix-writing/reference | phoenix-writing/reference |
| skills/phoenix-writing/scripts | ../maintaining-writing-skills/legacy-validator | skills/maintaining-writing-skills/legacy-validator | phoenix-writing/scripts |

兩個 alias 字面 SHA-256 分別為 `1cb52202e5157351dd1044476eba8d864757f30ddb410fcf1c2c333b0a6b4ae0` 與 `95f3504e0b766934407433d11c85aa44c2b0356dfef5bc57a498411224c95b45`。必須以已追蹤、明確逐檔 backing allowlist 固定每個 regular backing 檔案雜湊；不信任 glob，不只依賴 resolve 後的包含關係，也不任意擴展 alias。對每個路徑組件做 lstat；拒絕巢狀 symlink、未知檔案、target 改變、越界、未知來源或缺檔。先 staging 全部輸出、驗證，再只取代三個擁有的套件目標；部分安裝失敗必須 rollback。--check 只寫 temporary 輸出，重新計算並比較預期位元組，包括 metadata、連結、manifest／source policy，不只是比較 manifest。輸入不變的兩次生成必須有相同雜湊；無關框架套件保持不變。

Canonical aliases 保留舊呼叫者及原位元組。Runtime 在 alias 子路徑包含逐檔列出的 regular backing 複本，連結依 canonical 邏輯路徑／批准 backing 映射投影。重新計算 repo 引用深度：canonical SKILL 的 ../../scripts/vpHelper.ts→runtime ../../../scripts/vpHelper.ts；reference 的 repo 連結亦多一層；同層產品連結指向相同 runtime 的實體 sibling 套件。Anchors、URL、code blocks 與 CLI 語意保持。未知連結語法必須呈報失敗，不可靜默略過。

## 必要測試矩陣與如實判定

保留已批准完整計畫矩陣。候選 cwd 使用 Python 3.11+ 與既有 NVM Node24.13.0／pnpm10.28.0；package manager 解析停用網路，不安裝。必須記錄擁有的依賴複本、lock SHA、cwd、runtime 版本、命令／argv、exit、起訖時間、log／證據雜湊。每項結果為 pass／existing-failure／new-regression／blocked／not-run。Exit zero 本身不是行為證明，baseline 歷史完整性也不是新的 runtime 表現。

| Seam | 必要執行與邊界 | AC |
| --- | --- | --- |
| 來源／產品／歷史 | 原始乾淨／SHA；完整 tracked delta；55 個精確搬移；六個只改字面值的 adapters；新增／刪除／竄改負向案例；六份不可變匯入、四個 archives、歷史失敗 | HA-01/02/09 |
| 模板結構／license | 固定原 verify-project.py 不變；各 runtime 32+3 名稱、metadata／manual policy、roles／notice／license／upstream 雜湊；在擁有的固定複本跑模板 22 tests | HA-01/05/06 |
| materializer | 真實 temp 樹：精確兩 aliases、巢狀／backing links、越界、target 漂移、未知／缺少／多出／foreign metadata；全部深度無 link；連結投影；check 漂移；兩次生成雜湊；部分 rollback | HA-04/05 |
| tracker／翻譯／trace | 全域 ID；五狀態與推導 blockers；重複／缺少／自我／循環／pending 負向案例；無 landing 的 done 負向案例；過期 blob 翻譯、懸空來源／AC／ticket 負向案例 | HA-02/03/07/08 |
| native discovery | 新的原生 Codex 候選 context，實際 35 套件 catalog 與必要技能位置；不得用長 session catalog 或只看 filesystem 取代 | HA-05 |
| writing | 未變的歷史證據跑原 mechanical 31／30／62；之後九個新的獨立 writer contexts、三個新 judges，各處理互斥分組，使用凍結 input／rubric 與新 runtime freeze | HA-05/06/09 |
| CLI | 隔離 temporary repo cwd 的實際 subprocess：預設／分類／自訂／根、Unicode／空白、+08:00、路徑、重複保留原位元組、c／d 衝突、缺少標題；baseline docs 對候選 blog 投影，以及明確舊 -d 語意 | HA-09 |
| unit／build／routes／assets | 候選實際 11 unit 與 pnpm docs:build；相同 lock／dependency 快照；精確八個 baseline HTML routes；無管理 HTML；32 個 public 原資源 SHA／公開 URL 與資料一致性 | HA-09 |
| UI | baseline／候選的等價 localhost 顯示：首頁最新文章、list／card／filter／sort／category、既有空結果控制行為、sidebar／nav／images／console／network、keyboard、390mobile、dark／light／particles，依聲明的覆蓋範圍 | HA-09 |
| recovery／closeout | 擁有的可丟棄環境精確還原 baseline，重跑 unit／CLI／build／hash；原 repo 乾淨／SHA 不變；code／security findings 分類處理；ticket review 與全部實際結果的 coverage 表 | HA-10 |

## 凍結寫作案例與隔離

Input／rubric 是 baseline 的九個 full-regression-v22/cases/E1–E9 檔案，在任何新 writer 前於 writing-case-manifest.json 固定 SHA。原文字、rubric 及案例分數保留為歷史證據。固定的九個 inputs 目前都沒有 docs 路徑字串；不得虛構路徑搬移案例或增加無關 writer 指令。原 input／rubric 位元組保留。未來若另獲批准的案例含路徑，必須在歷史 fixtures 之外記錄投影。原 case-manifest 引用與修正仍可存取。

Writer 只收到自己 input、需要的候選實體技能及已批准 docs→blog 註記，不收到 rubric、舊 output／judgment 或 root verdict。每例一個新的隔離 context，九個實際回覆，含 near-miss／不套風格／不產骨架邊界。三個獨立 judges 各只收到三個互不重疊 inputs／rubrics 及相對應新 outputs，不收到舊分數／output 或 root verdict。不得自評或重用。回報實際 model／runtime／execution IDs／attempts 與內容雜湊。每個 rubric 維度必須得 2，每例 10/10，符合全部 hard rules 且零 invocation／安全違規。所有差異保留並實質分類，案例維持失敗，直到有合法記錄的 retry／新 freeze。不得聲稱 judge 間一致性、跨模型或統計改善。

## 明確繼承與局部取代

全部 113 歷史列保留原來源文字／雜湊。Codex／Claude 連結入口／同一檔案條款，只針對 vitepress-post-scaffolding-014/015 與 phoenix-style-and-maintenance-004/005 被實體投影取代，含經兩個批准輸入映射保留的原 legacy aliases。Gemini 既有 canonical 連結保留。凡 docs 作為產品實體路徑的列，必須於 candidate-traceability.json 逐列列出 docs→blog 位置投影；URL 與實質行為不變。CLI 預設／assets 實體根與建立慣例在此路徑邊界刻意取代，繼承原 metadata／errors／命名／時間行為。管理 Spectra 路由只在有效入口由單一本地 tracker 取代；歷史參考保持唯讀。不得用一概「其餘全部不變」抵觸這些列明、獲擁有者批准的邊界。

## Cloudflare 快照與範圍邊界

擁有者自行修改 CF。父任務對 Library `libfile_d33cc20e295c81918b60e1d41867b001` 的原生像素見證：命令 npx vitepress build blog、output blog/.vitepress/dist、include blog/*、root 空白、production main、自動 deploy Enabled；build-system Version3 不是 Node 版本。Node／pnpm／excludes／preview 與實際成功 deployment 仍未驗證。根依賴監看建議 package.json／pnpm-lock.yaml／tsconfig.json 是交接資訊，不是修改 CF 授權。production main 尚未有 blog 前，未來自動 build 可能失敗；未授權為此過渡而 push／merge／deploy。

## 不在範圍內

Feature／UI 重設計、無關 bug 修復、文章／風格重寫、公開 URL 改變、時間／圖片／資料語意改變、package／lock／version 改變、只用 srcDir 的替代方案、release／deploy CI、prompt tuning、虛構歷史 review、Notion／全域技能／權限／憑證改變、安裝、commit／push／PR／merge／deploy／CF 編輯。

## 審查與交付 gates

針對捕捉的 spec／matrix 與新批准回執，第二輪原樣重播凍結 prompt。四個獨立軸為 completeness、verifiability、conflicts、red team。最多兩輪；若仍有 P0，必須拆分／重啟，不能第三輪或削弱檢查。零 P0 是實作前必要條件，不是完成證明。之後分配單一已批准 ticket，執行 red→green verifiers／materializer 與全部檢查，完成 code／security review，提供可攜證據供本地 review。缺少 native／行為／rollback 結果，不能關閉 ticket。

## 第二輪非阻斷修正

捕捉的 review inputs 保存在 review/round-2-inputs。歷史 scenarios 003／008 的明確 -d argv 絕不投影，新 blog 慣例另行執行。E9 標籤修正不修改 input／rubric。任何新回歸都不符合驗收，只有 baseline 失敗不能豁免新回歸。缺少必要檢查，ticket 保持未關閉。
