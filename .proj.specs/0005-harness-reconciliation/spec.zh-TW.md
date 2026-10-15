---
synced_from: spec.en.md
synced_from_sha: 43a784963f7e8700f11a7e2af5c0f068dfd74acf
---

# 歷史與目前產品的有界保存後繼

## 問題

required verifier 仍將目前產品 bytes 與 lint 清理 epoch 比對。乾淨 staging 已失敗，已批准元件也不在舊 inventory。只換 checksum 會覆寫舊證據，且無法解決其他邊界。

## 解法與使用者需求

保留 adoption／publication／lint 不可變證據，驗證原本 pinned Git epoch；另驗證精確已知 staging 與經審閱 T-0003／T-0004 來源。未知路徑、bytes／型別漂移及歷史篡改繼續拒絕。稽核者可以查歷史來源，維護者可以讓目前合法產品通過，reviewer 可以確認新合約不是一般豁免。這是本機 verifier 修正，不是產品回復或發布。

## 實作決策

舊 manifests、source hashes 與原失敗證據不變。lint epoch 固定724ddad73f8411a33c77c68d75f95b41d3af2988；staging固定32cd6a9d4ead636ddc4e5020fceb35ad9645cc7f。兩個 objects 必須存在且為實際 HEAD 祖先，不查網路或浮動 refs。

新 pinned record 列出歷史兩個 objects 的精確產品差異、before／after 型別與 hash、來源 commit 及現在 reconciliation 收據。缺少當年 Harness approval 不補造。元件 delta 另外列出已審閱路徑／hash／票號；banner 是先前接受的 input，不宣稱本 verifier 產生或稽核圖片。最終 corrected packet manifest SHA-256 固定8d29af326616c8811cc4b9526417d7a0b1864e33564acee335723175cfdfd1dc；舊 source-freeze 僅是 provenance。可攜 excerpt 保留 reviewed hashes，不能由 runtime checkout 自動刷新期待值。record digest 與精確元件 path set 由受審閱的 code 固定，不用目錄 allowlist、mutable HEAD 或可自我批准的記錄。

資料流先驗證 provenance，再驗證目前 source inventory；通過後才從不可變 lint objects 建立 memory projection，執行原歷史保存語義。runtime／tracker／翻譯／trace 仍驗證目前管理資料。保留既有明示管理 prefixes；新 evidence 放既有管理界線或 checkout 外，不放寬 evidence／output。CLI 不修改檔案、index、refs 或建立 commits；不提供 bypass。guard code 與測試由 review 驗證，不用循環 hash 自稱可信。

現有來源維持已知 staging 型別／bytes，除非精確 reviewed delta 指名。未知、缺少、刪除、linked、stale 來源皆拒絕；ignored 的新 Markdown 也不能漏列。compilable blog inventory 不受 Git ignore 影響，只有明示的 generated dist／cache／temp 不算 source。generated／management ownership 仍保持既有檢查。

rollback 一起移除新 successor 與 verifier integration，回到舊 fail-closed 行為；不改回舊產品 config、不修改原 manifests。後繼變 stale 必須新 review，不能自動 rebaseline。

## 驗收標準

- R1：舊 adoption／publication／lint manifests 保持 bytes，來源 hashes 符合 pinned epoch，原乾淨32cd失敗收據保留。
- R2：乾淨 staging 與精確元件 delta 通過保存檢查，tracker／framework／翻譯／trace仍檢查目前管理資料；不接受泛用候選目錄。
- R3：額外／ignored路徑、config／theme／summary／banner篡改、缺檔、symlink／type與stale hash 在公開CLI fail-closed，包含 untracked files。
- R4：錯誤／缺少／非祖先 pin、篡改舊 manifest或新 record、未批准path與before／afterhash皆拒絕，原反例仍有意義。
- R5：唯讀、無網路／global setting／安裝／發布變更，記錄真實現在 reconciliation與rollback；產品及Notice契約不變。
- R6：完整Python harness、產品unit、lint／build／materializer／structure與真正CLI有結果；獨立standards／spec／security解決票內findings。無landing則保持review。

## 測試與範圍

沿用既有Python unittest與公開verifier CLI seam，使用者已批准真實拒絕red→green，不加runtime或新的產品／browser seam。合成disposable clones取既有Git objects，不偽造批准、不改原來源；乾淨及精確元件正向案例搭配拒絕案例，helper單獨通過不算CLI證明。原產品suite在verifier改動後驗證。localhost恢復另有HTTP與Mac Chrome證據，不重做元件。

排除框架重寫／一般policy engine／取代舊check／新產品功能／套件安裝／舊批准回填／blanket allowlist或waiver／commit／push／deploy／Notion／Library上傳。使用者owner receipt retained locally批准一張無技術阻擋的有界修正票，父明示歷史及元件範圍與既有測試流程。外部#19不是repo authority；新的產品或安全範圍決策須另外確認。
