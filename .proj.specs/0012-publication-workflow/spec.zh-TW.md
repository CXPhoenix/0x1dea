---
synced_from: spec.en.md
synced_from_sha: a3f0c03754c389d40ca9fb97d8bb7c1ae992651b
---

# GitHub Flow 與共用 staging 預覽

狀態：提案；方向已核准，詳細規格與測試計畫等待作者確認。
Epic：0012-publication-workflow。本文件不配置實作 ticket。

## 問題陳述

作者需要在同一個 staging 網站檢閱多篇候選文章，同時讓 main 的目前 tree 只包含核准發布的內容。
目前工程變更需要分別投影、重複整理。選擇一篇發布時，不能順帶發布其他候選，包含已發布文章尚未核准的修訂。

現有 v1 publication verifier 會拒絕含有任何 staging-only ancestor 的來源，連已整合進 staging
的乾淨文章 topic 也會被拒絕。直接放寬檢查，又可能允許 staging 整合歷史或其他候選混入。
歷史測試與不可變證據必須保留原有意義。

## 解決方式

採用從 main 建立的 ticket topics 與 PR 審查，staging 作為共用整合預覽。
先建立經審查的共同工程基底。後續工程變更只在 main 落地一次，再由自動化準備、驗證 main→staging 同步 PR。
文章 topic 先整合 staging 審稿；指定文章發布時，另外從 current main 準備選文 PR。
任何流程都不整支合併 staging 到 main。初版自動化只開／更新 PR，不 merge。網站部署設定維持現況。

## 使用者故事

1. 身為作者，我希望所有候選集中在同一 staging 預覽，能一起審稿，不必管理各來源分支的個別網址。
2. 身為維護者，我希望工程修正只實作一次，再取得已驗證的同步 PR，不必維護兩份相同修正。
3. 身為作者，我希望核准一個精確文章版本及必要依賴，只有這些發布內容能進 main。
4. 身為審查者，我希望保留歷史契約與目前來源證據，便利流程不能悄悄削弱曾抓到問題的檢查。
5. 身為 agent 使用者，我希望專案 skill 分清準備、已授權遠端操作、落地與正式網站驗證，之後能沿用同一套規則。

## 實作決策

### D1. 授權、角色與遷移邊界

- Main 是穩定工程基底加上核准發布內容；staging 另外包含公開候選與僅供預覽的行為。
  候選包含未核准的文章及**修訂版本**，即使該路徑已存在 main。來源分支不要求個別部署網址。
  必須實際查驗共用預覽 alias 與服務中的 commit，不能從分支名稱推定。
- 本輪只產出已審查的規劃及 skill 草案，不包含開票、新測試、實作、替換啟用中的 skill、commit、push、開 PR 或任何 merge。
  作者之後的確認核准 spec 與提議的 seams；外部操作仍須具備各自適用的授權。
- 實作前重新取得遠端 refs 與未結束 PR 的狀態。規劃時 PR #20、#21 仍為 OPEN，不能假設已落地。
  前置條件採用實際落地的 commits，或另外審查過的等效變更，不自動 merge 既有 PR。
- 遷移建立作者審查的 M0 邊界紀錄，包含 repository 身分、完整 main/staging commits、基底分類、候選 registry、歷史契約版本與來源遷移。
  Ownership 未知或不明時阻擋受影響操作。M0 核准後才能作為可信政策，後續更新接受同等審查。

### D2. 共同工程基底

- 盤點完整 main/staging trees 與差異。每個變更路徑分類為已發布內容、未核准文章／修訂、共同工程、歷史或目前管理證據、目標角色設定。
  記錄前後 modes、blob hashes 與新增／刪除；共用路徑也要有審查過的內容 patch。
- 從 main 準備基底 PR，只包含逐項核准的工程／管理變更與目標角色政策。
  不帶入候選正文、未發布修訂、專屬 assets 或 listing 項目。不以整個資料夾放行，也不整檔選 ours/theirs。
- 將基底整合回 staging，衝突解法必須審查。每個未核准候選的 blob、mode 與文章 metadata
  均須符合盤點，只有另行核准、記入 M0 的來源修改例外。既有正式網址維持不變。
- 共用驗證實作，目標角色由可信 target/base context 決定，不能由候選任意切換旗標。
  保留歷史 validators、fixtures、hashes 與拒絕斷言。現行工程／tracker 的演進採用明確版本化、精確審查的 successor 邊界；
  不把歷史快照改成會隨目前 tracker 變動的 oracle。保留既有三個寫作套件，除非另有核准變更要求其精確 successor。

### D3. V2 文章來源證據

- V1 CLI schema、語意及歷史 fixtures 維持不變。另增明確的 v2 plan/admission 介面，拒絕不支援的版本。
  不重新解釋 v1 成功結果，也不更改它刻意保留的 local-only publication flag。
  Skill 執行前必須提供支援的操作入口、version/help 與 schema 文件；找不到介面就阻擋，不猜指令。
- 可信 registry 盤點 staging **全部**未核准文章／修訂、專屬 assets、精確來源 commits 與共用依賴。
  綁定完整 commit ids、逐路徑 modes/blob hashes，以及共用路徑審查過的內容 patches。
  Registry 來自作者審查的政策，不接受文章 metadata 自行宣告。
  固定版本的 staging 盤點若有漏列或未知差異，阻擋准入。
- 每個來源都必須以固定的 current main 為祖先。檢查所有可達、尚未在 main 的 commits，不只看最終 diff。
  一般 commit 只能修改登錄的來源 ownership 路徑與已審查共用內容；merge commit 只允許合入固定 main 的祖先，
  tree 必須等於獨立計算的無衝突 merge，或明確審查的衝突解決 tree。
  依賴是獨立登錄的來源，不代表能任意 merge topics。歷史不完整、未知 commits 或 ownership 均拒絕。
- M0 後的 staging 整合採 merge commit，first parent 為原 staging、second parent 為乾淨 topic。
  這些 integration commit ids 不得出現在來源的 non-main 歷史。
  Topic 自身的 commits 可以由 staging 到達，這是正常預覽整合，必須有驗證成功的正例。
  其他候選 commits，包括先加入再 revert 的歷史，仍禁止。
  Main 合回 topic 後必須更新 pins；不能把 staging 合回 topic，也不改寫已整合 topic 的歷史。
- 缺少這些來源證據的舊來源維持阻擋，直到作者核准遷移紀錄：原 commits、精確取出的 paths/modes/blobs、
  在固定 main 上重建的 diff、ownership 審查與新來源 commit。
  核准建立的是新審查來源，不表示舊歷史乾淨，也不刪除舊拒絕測試。

### D4. Main→staging 同步

- Main 變動或明確要求重試時，讀取目前 main/staging refs；事件 payload 的 commit 只是提示。
  Main 已是 staging 祖先則 no-op。否則在一次性儲存空間獨立計算兩個 pins 的 merge，依 staging 角色驗證。
  衝突或驗證失敗保留目標 refs，回報精確路徑／檢查，不自動選 ours/theirs。
  將結果中所有未核准候選的 mode/blob/metadata 與固定 registry 比對，包含已發布路徑上的候選修訂。
  即使 Git 無衝突、結果等於獨立 merge tree，只要候選改變就阻擋 readiness。
  必須先明確更新來源與審查 registry、重新取得受影響作者核准，再使用新 pins 準備。
- Ticket breakdown 核准後，指定一個永久 ticket branch 供日常同步，重複操作沿用同一分支，不拿來做無關功能。
  自動化實作與衝突修復各用自己的 ticket branches，維持一票一分支。
  不重用仍有無關交付 PR 的既有分支。
- 最多一個由本流程管理、目標為 staging 的 open sync PR。
  冪等操作紀錄綁定 repository、target、main/staging pins、policy version 與預期結果 tree。
  分支只能 non-force 前進，必要時合入更新的 pins；結果必須等於獨立計算的 tree。
  結果不同或分支 ownership 不符就停止。分支不存在／被刪除時，先查核 PR／operation 身分才能重建。
- 參與的 sync、preview integration 與 publication 寫入操作共用 repository write group 串行執行，不取消正在寫入的工作。
  合併處理事件時重新取得最新 refs，不假設 FIFO。遠端操作前再次讀 refs，漂移就使結果失效並重新準備。
  API 結果不明時先 readback 再重試；每次 run 最多重試三次，耗盡就停止並留下可處理紀錄，不能重複開 PR。
- 只有具備 push/PR 授權才開／更新已驗證 PR。不直接更新 staging、不 force push、不刪分支、不自動 merge、不改部署設定。
  初版仍由人決定 merge。

### D5. 自動化信任與檢查

- 規劃 repository 範圍的自動化 token，只給寫入自身分支、PR 與明確 validation dispatch 所需權限。
  Writer 執行可信 main 政策，不執行候選 build。Build/validation 使用唯讀 credentials，不能取得 writer token，並沿用強制 build isolation 契約。
  來源文字、API 欄位與 receipts 都是資料，不組成 shell 程式或可執行政策。
- 不仰賴 bot push／PR 自動跑完所有 checks。提案預設從 main 明確 dispatch 可信驗證 workflow，傳入固定 inputs。
  Dispatch 被接受不表示成功；實際 run、結論、base/head/tree 與 policy 都必須綁定同一 operation。
  只有精確 inputs 的成功結果才能完成驗證。Run 缺少、逾時、權限拒絕或結論過期都阻擋 PR readiness，readback／重試上限沿用 D4。
- 啟用前查核實際 repository 權限、required checks、merge methods、branch protections 與 dispatch 能力。
  另經明確授權的遠端演練，驗證 exact-head/latest-base checks。
  本規格不隱含安裝 credentials、更改 repository rules 或啟用 live automation 的授權。
- 本機 mutex 無法鎖定人工 GitHub 寫入；merge API 的 head guard 不等於 base compare-and-swap。
  PR readiness 綁定固定版本，不能保證之後的 merge tree。
  正式運作前必須有保持最新 base 的 protected checks，或經等效驗證的 merge queue，否則 activation blocked。
  任何已授權 merge 發生後，重新核對實際 landing tree 與 pins；不符屬於 incident，不能宣稱發布成功。

### D6. 指定文章發布

- 從固定的 current main、作者指定的**恰好一篇**文章及明確審查依賴準備。
  不整支 merge 或複製 staging tree 到 main。核准綁定文章身分、精確來源／依賴 commits 與 bytes、
  policy/registry version、main base、prepared tree，以及作者審閱的 preview deployment identity／served staging commit。
  只有網址或較新的 branch tip 不能證明審閱版本。
- 完整 source manifest 記錄每個 regular path 的 mode/hash、全部新增／刪除、允許且不跟隨的不可變 aliases，以及精確 allowed diff。
  既有正式內容保留，除非有明確核准變更。Listing/navigation 與共用依賴只能包含已發布／已選文章內容；
  允許某個共用路徑不代表能帶入其他候選。依本機 isolation 契約拒絕新 links、submodules、越界 includes 與 executable imports。
- 重建、獨立驗證 tree，在強制無網路邊界執行既有已審查 build。
  分別記錄 command、toolchain、isolation probe 與 build output inventory。
  掃描全部 output 檔案，檢查未選候選的 routes、listing/search/RSS references 與專屬 assets。
  來源重建與審查 build 是主要證據；特徵掃描只是補充，無可辨識特徵則為 `exclusion-unverified`。
  已發布的 baseline routes/listings/assets 仍允許保留；排除範圍是相對固定 main、由未選候選新增的內容，包含修訂。
  V2 PR-ready 要求 source/admission/approval 全部成功、實際隔離 build 成功，而且 output scan 成功、沒有偵測排除項目或 `exclusion-unverified`。
  任何必要檢查失敗、blocked、缺少或 `exclusion-unverified` 都阻擋 PR-ready；單靠補充掃描成功不足以授予 readiness。
  這個保守 v2 關卡可能阻擋無可辨識特徵的短修訂，沒有隱含人工覆寫。
  缺少 runtime 或強制 isolation 時，該檢查維持 blocked，不算成功。
- 最終 refs／candidate 漂移使準備與 readiness 失效。任何核准綁定改變，都必須對新的精確發布候選重新核准。
  Commit、push、PR 使用專案 message skills，限明確作者授權。開 PR 不代表允許 merge。
  Main 落地、部署完成與 HTTP/UI 驗證分別記錄，不能互相替代。
- 驗證 main 落地後，同步回 staging，保留已發布文章及所有其他候選。
  只在下一版已審查 registry 中移除已落地版本的「未核准」身分；之後的新修訂仍是候選。
  Rollback 在 current main 上準備新審查 revert，另行授權、保留其他已發布內容。
  重新發布需要 fresh pins 與核准，不 force/reset。

### D7. Workflow skill 與 tracker

- 延伸既有 publication skill，不新增互相衝突的第五個 product package。
  草案包含精簡 router 與 workflow reference；既有 local/future-action references 逐位元組保留。
  V2 尚不存在時，新 workflow 只能 inspect/plan，回報能力缺少，不編造指令或用 v1 規避准入。
  原有受支援的 v1 本機路徑仍可使用。
- 核准並完成實作審查後，canonical product source 修改一次，再確定性產生兩個 runtimes。
  透過明確審查 successor 保留 catalog 數量、invocation policy、三個中文寫作例外與歷史套件證據。
  本輪不啟用、不安裝 skill 草案。
- ADR-0006 持續有效：done 必須有實際授權 staging 祖先與 approval receipt。
  Main-first 工程交付另記 main 落地，sync PR-ready 不足以 done。
  Publication tickets 另外要求其 main／發布驗收證據；僅整合預覽不算發布完成。
  本規格不關閉、重開或重新編號任何舊票。

## 驗收條件

| ID | 可判定的成功／失敗契約 |
|---|---|
| AC-01 | 核准 M0 涵蓋每項 main/staging 差異，包含未發布修訂；未分類／ownership 重疊阻擋受影響準備。只有實際落地的前置 commits 才記為 landed。 |
| AC-02 | 基底 main diff 只含逐項核准工程／管理變更；未核准正文／修訂、listing、專屬 asset 不進 main。Staging 保留全部盤點的未核准 blob/mode/metadata，另行核准修改除外。 |
| AC-03 | 每個歷史 fixture/assertion 維持原有結果，包含 v1 ancestry 拒絕；共用現行驗證採可信 target roles 與精確審查 successor 邊界。 |
| AC-04 | V2 接受已 merge staging 的已登錄乾淨 A；拒絕 staging integration ancestors、先加入再 revert 的 B 歷史、未知／漏列候選、無效 ownership、過期 pins、未核准舊來源重建。經審查的舊來源遷移保留舊證據。 |
| AC-05 | 乾淨同步在唯一 owned staging PR 中產生獨立計算且驗證的 tree；已同步為 no-op。衝突、候選 blob/mode/metadata 變更（即使無衝突）、branch 不符、漂移、檢查失敗及三次重試耗盡，都不能產生 readiness、目標修改或重複 PR。 |
| AC-06 | 演練並行、事件合併與 API 結果不明；重新讀最新 pins、保留無關 branches/PRs，任何 run 都不 merge、force push 或修改部署設定。 |
| AC-07 | Validation readiness 必須有精確 base/head/tree/policy 的實際可信成功 run。被抑制的 trigger、缺少／拒絕／過期 run、writer token 暴露或 activation 前置條件不足，都不能產生 readiness。 |
| AC-08 | 選 A 只重建 main 加核准 A／依賴。B 的既有正式內容／routes/listings/assets 仍允許，只排除 B 未核准新增／修訂輸出。PR-ready 要求全部 source/admission/approval/build/output checks 成功；失敗、blocked、缺少或 exclusion-unverified 都阻擋。單靠 scan 成功不足。 |
| AC-09 | 核准與 readiness 遇綁定漂移即失效。同一既有 staging alias 必須呈現所有登錄候選頁面／修訂、正確 listing/navigation 及固定版本內容，否則網站驗證 blocked。PR、main 落地與部署／服務驗證分別有 receipts。同步保留其餘候選；rollback／重新發布保留其他正式內容並另取授權。 |
| AC-10 | 草案 skill 正確選擇 v1 本機準備或新 workflow，拒絕缺少能力／未授權遠端操作，完成代表情境推演。未來安裝保留四個 product packages 與兩個 runtimes。不能只因 main 落地或 PR-ready 就把 ticket 標 done。 |

## 測試決策

使用公開 Git/CLI 結果、native validators、完整 manifests、實際 builds 與觀察到的遠端／網站 receipts，
不以重述實作措辭的斷言當作行為驗證。沿用 seams：一次性 Git repositories 的 Python subprocess tests、
article-publication preview/prepare/verify、native unit discovery、materializer/adoption validators、VitePress build/browser。
新增提案是 v2 admission、sync planning 與 GitHub/Actions adapter，寫測試前需作者確認。

附帶測試計畫分開本機確定性 harness、已授權 GitHub integration、實際 staging/production 觀察。
Stub API 成功不代表遠端 checks 有執行。不新增重複措辭測試；結案依 AC 回報 coverage。
使用既有 Node 24.13.0 與 pnpm 10.28.0，不安裝。
測試計畫與 ticket breakdown 核准後才新增測試，依專案 TDD 逐一循環。

## 不在範圍內

部署設定、Cloudflare/DNS/build-watch 調整、新預覽網址、repository rules／credentials／帳號變更、自動 merge、
整批 staging→main 發布、私密草稿儲存、global skill 安裝、歷史證據改寫，以及本輪規劃中的實作或遠端交付。
是否自動 merge sync PR 留待之後決定。

## 補充說明

同目錄附 traceability、test-plan、source-evidence 與 ADR clarification 提案。
平台具備的能力與本 repository 實際啟用／設定狀態不同。
作者先確認已審查 spec、新 seams 與 skill 草案，再開票。
