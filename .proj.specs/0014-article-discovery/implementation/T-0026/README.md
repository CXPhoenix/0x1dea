# T-0026 本機實作與證據

本頁保留 A 完成時的本機檢查點；後續已 commit，且使用者追加授權 B～D 與單一 PR。最新進度見 [epic 首頁](../../README.md)及批次收尾紀錄。下列「尚未 commit／B～D 尚未實作／沒有 PR 授權」均為當時範圍，非現況。兩份新 log 後來為保留測試候選樹改名為 .txt，原始位元組與 A commit 歷史保留。

使用者於 2026-10-24 核准提案 A 及 A01～A06 測試表。實作位於 `/private/tmp/0x1dea-T0026`，分支為 `tickets/T-0026/local-notes-current-guard`，基底是本機 main `8b2cffab8ed1a8a2c50ece18b6fe5b578f186668`。HEAD 仍停在基底，修改尚未 commit。原 staging 工作目錄 `/Users/phoenix/dev/online-notes/0x1DEA` 的已追蹤來源位元組未變，只在原處保存新增的 epic／tracker 紀錄。

## 交付行為

current guard 先驗證完整的 `.proj.writing/<article-key>/`，再將合法且直接位於工作區內的 PROJECT.md、GLOSSARY.md、相容用 CONTEXT.md 檔名自實際工程來源集合排除。根目錄／工作區為連結、非法形狀、額外或巢狀項目、非一般檔案、任何執行權限，以及 HEAD／index／受信任清單的來源碰撞，都會拒絕。空的實體資料夾及合法 Unicode／空白 key 可以使用；筆記文字不能設定其他排除範圍。

Git 忽略慣例為 `/.proj.writing/`，不會取消既有追蹤，也不是筆記分類器。trusted control 與 candidate 都維持精確的 ignore 身分；其他來源名稱、模式、雜湊、角色、歷史、政策綁定及凍結歷史脈絡保留原檢查。

功能只修改 `.gitignore`、`scripts/publication_current.py`、精確 current source inventory，並新增 native CLI 測試。已審查規格／研究、正式票及本證據，均以明列檔名及精確身分納入。A 不建立 article-discovery skill、runtime 套件或作者工作區；B～D 尚未實作。原則仍是「先自由聊、按需整理」。

## 既有 merge 回歸與 additive successor

第一次完整回歸後，未修改的 sealed-input／head-reporting 測試暴露出 A 的真實退步：直接替換 helper 原 SHA 那一行，會與 staging 既有、不同的 helper 身分在 Git merge 時衝突。同一個原測試在未修改 main 基底通過，因此沒有把問題當成基底失敗，也沒有修改原斷言或輸入。

修正保留各目標已知的舊 SHA，於既有欄位前加上 `successor_sha256`。只有固定 current helper 路徑、兩個已知舊 pin、100644 模式及精確三欄格式可以使用。guard 在原有精確來源檢查之前，將此表示法轉為 active hash；其他路徑仍須遵守兩欄契約。同一個 head-reporting 測試因此轉綠，新增負向回歸也確認未知舊 pin、畸形／錯誤 active hash、錯誤模式、額外欄位及其他路徑濫用會被拒絕。

[回歸紀錄](head-policy-regression.json)保留原失敗、未修改基底及修正後執行結果。[來源範圍](source-scope.json)綁定功能審查擷取版本。之後的收尾紀錄只更新各自有限來源身分，不修改 helper／測試位元組。

## 驗證與保存檔案

- [覆蓋報告](coverage-report.md)：核准列、實際範圍與尚未涵蓋的作者 runtime 行為。
- [TDD 紀錄](tdd-red-green.json)：實際 red／green 摘要及外部原始 log 雜湊。
- [獨立 native 同時保存證據](coexistence-native.json)：main、staging 在三個筆記同時存在時的保存前／建立後／更新後報告，以及非筆記來源身分比較。
- [功能修補檔](functional.patch)：ignore、helper 與新測試，不含會隨證據更新的精確 inventory；已在隔離實作檢查可反向套用。
- [命令與結果](execution-results.json)：實際命令、結束狀態、測試分項與初次失敗處置。

乾淨 main 起始版本先完成 portable、materializer 與 native current 檢查（main 3193 項來源）。最後完整 Python runner 通過 260 項（66＋170＋10＋14），Vitest 通過 54 項。沿用既有 Node 24.13.0、pnpm 10.28.0 與本機相依套件，沒有安裝。正式獨立審查後，另以 native CLI 確認收尾紀錄的精確 inventory。

main 套件沒有 `pnpm test` 別名；該命令結束碼為 1，沒有執行測試，也沒有修改 package 製造別名。實際既有入口是 `pnpm test:unit` 與 `python3 -B scripts/run-current-python-tests.py`。後者保留歷史 #22／#32 脈絡，依既有文件設定 `PUBLICATION_TEST_DEPENDENCIES=/private/tmp/0x1dea-T0026/node_modules`。暫存 Unix socket 與本機 mock server 需要測試執行權限調整；同一批測試未略過、未改採替代成功結果。

沒有對 ticket 執行 commit、push、PR、merge、deploy、外部索引更新、帳號／trust／credential 或全域技能修改。證據涵蓋 native CLI 與本機測試，不代表 B～D 的 host 執行、真實遠端發布、browser 驗收或整個 epic 完成。T-0026 在另行授權 landing 前維持 review。

## 重建精確來源紀錄

功能修補檔以所列本機 main 為基底。`policy-admissions.json` 明列複製已審查 epic／研究／tracker／證據、套用修補檔後，須新增或更新的 A 相關 common entry。這是有限清單，不是資料夾探索或 runtime 豁免。只對所列、已審查的一般檔案重算 mode 與 SHA-256。固定 current helper entry 保留原 main SHA，先加入已審查的 active `successor_sha256`；其他既有 entry 與所有非 common 政策欄位維持原樣。政策本身由既有 trusted raw-policy 檢查綁定，不放入自己的 common map。任何後續 landing 前，都須再次驗證重建後來源集合。
