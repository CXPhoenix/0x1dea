---
synced_from: spec.en.md
synced_from_sha: cb920f71b3e104b06a4d78001acc89b27b2dfbe6
---

# 可重現的驗證與精確的目前來源接受邊界

## 問題與方案

歷史 verifier 測試混用固定 Git 時點與目前工作目錄，後續合法修改使成功案例失敗，也遮蔽負向案例原本要驗證的診斷。現行來源保存合約缺少後續元件、caption 與寫作素材的 successor。文章測試混淆歷史轉換與後續編修；Python 缺少完整入口，tracker 的 blocked 與文件不一致。舊執行紀錄不能證明目前狀態成功。

保留不可變的歷史證據，以目前 verifier 驗證固定歷史輸入；新增範圍精確且經審查的 successor 接受目前增量。提供 Vitest 與兩套 Python suite 的完整指令，保留目前文章所有位元組，將未完成依賴與僅限 todo 的 Blocked view 分開。不得推定歷史授權。

## 使用者需求

1. 維護者需要不受目前文章或產品修改影響的歷史 fixture。
2. 稽核者需要精確的目前來源接受邊界，保留原始證據並拒絕竄改。
3. 貢獻者需要完整測試入口與正確的票單檢視，揭露缺少測試及 landing 證據的情況。

## 實作決策

使用已核准的單票 T-0009，無依賴，沿用六列測試表與既有 CLI／renderer seam。

元件 fixture 從 69ff85f5fe1baddb54102070a436dff9ac1c5b73 讀取產品位元組；文章修訂 fixture 從 f93237b1ed538484f24ed103ef00c7e5ee2e1828 讀取。兩者均執行目前 verifier；缺少 Git object 時失敗，不跳過或改讀目前檔案。保留負向案例的目標路徑診斷，不改動來源工作目錄。

原始 article baseline JSON 不變。歷史文章入口由 f3eee3db6c9056b1bfd308756e2790c46513b174 與已記錄的較短圖 1 caption 重建，必須符合獨立 oracle SHA-256 9ee10b2b8afe41d6d201df259ed95c58e869bd5592bbaa4995d603f5823f265e。凍結遷移後資料並標明重建來源及兩者雜湊，保留公開 Markdown renderer、來源連結與反向轉換驗證。另驗證目前文章三張 figure、六個引用、八組原始 alt/src、frontmatter 與來源註記連結；目前文章位元組必須與 6e4eb804bcbda8504935be49fd6537d6327d5303 一致，不恢復舊文。

新增單一 successor record，digest 固定在經審查的 guard。product 段落涵蓋 predecessor f93237b1ed538484f24ed103ef00c7e5ee2e1828 到 captured 6e4eb804bcbda8504935be49fd6537d6327d5303 的完整受保護差異，僅排除既有管理路徑規則。兩個 commit 必須存在、都是實際 HEAD 的 ancestor，且 predecessor 是 captured 的 ancestor。精確驗證完整路徑集合、前後 mode/hash、Git object 及原接受投影。repair 段落僅列出核准的 README、package scripts、文章測試、凍結資料及 package initializer；完整清單在 source-scope.json 與 guard 程式碼。拒絕重複、缺少、額外項目、record 位元組變更及不支援的型別；執行時不得更新期望值。

successor 必須有 staging、component、revision provenance。沒有 successor 時維持先前的封閉拒絕行為及歷史 fixture 支援。接受後仍檢查全部目前來源位元組、型別及未知檔案，Git ignore 不得隱藏來源。原始 epoch/provenance record 不變。歷史 package 合約對歷史投影驗證，目前 scripts 另受精確邊界保護。guard、runner 與 guard 測試屬明確列舉的審查程式碼，不以循環自我雜湊認證；不新增目錄級允許或 CLI 繞過。

加入 Python package initializer，讓 root discovery 觸及兩套 suite。標準函式庫 runner 分別 discover 並執行 harness_adoption、article_publication，分列 testsRun 方法數與 failure/error 紀錄；subtest 紀錄不是失敗方法數。任一 suite 零測試、失敗或 import error 都回傳非零。預設使用專案 tests，可指定 tests-root 測試一次性 CLI fixture。保留 test:unit，新增 test:python 與 test，傳遞失敗結果；不安裝依賴、不改 lockfile。

tracker 新增所有狀態的 unresolved_dependencies，blocked 只取 todo；frontier、pending、依賴及 done 檢查不變。保留 T-0005 缺少 landing receipt 的原因與 review；必須有真實授權和實際 staging containment 才能 done。自動檢查只能驗證 receipt 格式、存在性及 ancestry，不能驗證人類授權真實性。

只將觀察到的單一 Finder metadata 檔移到被忽略的本機備份，先記錄大小、hash，再確認備份並保留 receipt；不豁免 metadata 或刪除其他檔案。舊報告僅附加註明版本的新結果，不改寫原紀錄。CONTEXT 的易變 branch／landing 宣告改成 Git 與 receipt 查詢來源。

## 驗收條件

- V1：歷史成功與竄改案例對目前 verifier 成功，固定輸入符合紀錄；缺少 pin 失敗，負向診斷仍指向原目標。
- V2：歷史文章符合原 SHA、renderer、來源連結與反向轉換；目前文章三圖、六引用、八組 alt/src、frontmatter、來源註記連結及所有位元組不變；baseline JSON 不變。
- V3：公開 CLI 接受精確 successor／repair；record、delta、pin、history、缺少或非 ancestor object、位元組／mode、缺少／link／未知／ignored source 皆拒絕。原 manifest 與授權紀錄不變。
- V4：root discovery 觸及兩套 suite，test:python 分別執行正數測試，test 執行 Vitest 與 Python；失敗、import error、零測試回傳非零，不刪除或跳過測試求成功。
- V5：blocked 僅含 todo 未完成依賴；processing／review 依賴在 unresolved_dependencies 可見；既有 frontier、pending、cycle、missing-id、invalid-landing 行為保留，明列 T-0005 缺證。
- V6：既有票不能在缺少真實授權或 staging containment 時 done；缺證時保留 review 與原因。done 變更須另記錄人工授權來源查核。歷史本機／remote 觀察不證明部署。
- V7：單一 Finder 檔有同 hash 備份與 receipt，原掃描路徑不存在，其他檔案不刪除或豁免。在一次性副本驗證 guard／data／tests／commands 成組 rollback、文章及歷史不變；目的路徑已存在時拒絕覆寫，只能還原到不存在的路徑。
- V8：完整 Vitest／Python、lint、VitePress build、結構、materializer、公開 verifier 結果均對應最終修正狀態；coverage 表與獨立 Standards／Spec／security 報告說明實際範圍及限制。舊結果保留歷史識別。

## 測試與範圍

沿用核准六列測試表，一個實際 red 行為、最小修正、再下一個；已重現的既有失敗可作 red 證據。使用真實 Git、Python CLI、公開 renderer；runner 使用一次性最小測試模組。先驗證成功控制，再做負向探測，避免其他提早失敗造成假覆蓋。依 ADR-0006 使用既有非瀏覽器 harness；完整 aggregate 在局部 green 後執行，並跑必要工具。build 只證明相容性，不新增瀏覽器驗收宣稱。

不包含 commit／push／PR／merge／部署、外部索引、安裝、全域設定或憑證、改寫文章、新瀏覽器功能、一般授權 registry、自動更新期望值、弱化 guard 或偽造過去授權。

目前授權是對 captured 狀態的現在式核對，不代表先前 T-0007／T-0008 滿足全部歷史關卡。rollback 成組還原修正並只在原路徑不存在時還原 Finder 備份；它恢復先前失敗，不改產品文章或舊 manifest。本機交付後票維持 review，這次未授權 landing。
