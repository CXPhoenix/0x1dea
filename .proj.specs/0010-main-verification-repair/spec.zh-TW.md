---
synced_from: spec.en.md
synced_from_sha: 5cae7271a544e50801bf510418f6ded0231158ac
---

# main 驗證修正

## 問題
使用者 merge PR #17 後，preservation CLI 拒絕已核准的用電文章；Python harness 的 lint 正向 fixture 則混入目前的檔案。必須保留原有歷史契約。

## 解法與使用情境
為已 merge 的文章建立精確 successor，歷史測試則以固定 epoch 輸入執行目前 verifier。維護者能確認原歷史正向與變造案例；使用者能確認正式 main 接受指定發布，同時拒絕額外產品輸入。

## 決策
保留文章、圖片、相依套件、framework 與歷史證據 bytes，不引入 staging reconciliation 或其他五篇候選。固定 predecessor `e457143e8be2f7d54f69bc3e9b80230375be49de`、release `604f8733ca47d67fc277ec127a9da743cefbc22e`、merge `88b9c53852f527ee636bcc4b4ca5e166f6ec10fd`；前者必須是 release 的祖先，後兩者必須是 HEAD 的實際祖先，缺少物件時拒絕。

以原 release scope 的固定 Git blob 與 SHA-256 為獨立依據，完整驗證 34 個產品路徑及 11 個既有發布證據路徑，從 Git 物件檢查前後身分，再核對目前檔案 bytes、型別與 executable mode。修正程式是明列且經審查的信任根，仍必須存在且為普通檔案。新增管理資料沿用既有規則，但歷史 boundary／provenance 與既有 release 證據仍須符合固定 Git bytes。

先驗證目前 successor，再以 predecessor bytes 執行舊 preservation 檢查。不更新舊預期 hash，不從目前 bytes 推導授權，不新增略過旗標或通用更新機制。拒絕缺少、symlink、mode 或 bytes 改變的產品輸入，以及未知 tracked／untracked 輸入與 blog、docs、tests 下被 ignore 的來源。VitePress dist/cache/.temp 與 Python __pycache__ 不算來源；其資料夾若為 symlink 仍拒絕。

lint fixture 固定取自 `724ddad73f8411a33c77c68d75f95b41d3af2988`，保留原負向案例與預期 hash，缺少資料時不可 skip。

## 驗收條件
- M1：目前 verifier 搭配固定 lint 輸入時，歷史正向及變造案例通過；缺少輸入時報錯。
- M2：公開 CLI 接受已 merge 的 main 加上經審查的修正程式與管理資料，並繼續執行 baseline/framework/lint/translation/trace/tracker 檢查。
- M3：公開 CLI 拒絕改動文章、config、歷史證據或 scope，以及缺少／symlink／mode 改變的來源、缺少修正程式、錯誤祖先／物件、額外 tracked／untracked／ignored 來源。每個負向案例先證明正向控制成功，再核對預定拒絕原因。
- M4：完整驗證 45 路徑差異及 34 個產品身分；所有既有歷史 boundary、文章 fixture、目前文章／圖片及 package／lockfile 與 merge 後 main 完全一致。
- M5：在修正 checkout 實際執行完整 Vitest、兩套 Python、lint、build、structure、materializer 與公開 verifier，記錄指令、exit code、測試數與 skip。獨立 Standards、Spec、安全審查沒有未解決的阻擋問題。

## 測試與範圍
沿用已核准的 Python CLI／可丟棄 Git fixture、目前 preservation CLI 及完整指令 seam，逐一 red → green；以固定 Git epoch 和原發布證據作獨立依據。只驗證本機 Git／CLI 行為與網站 build 相容性，不改瀏覽器行為，不宣稱部署。

不修改文章、不發布其他候選、不匯入 staging chain、不重設 test runner、不安裝套件、不 commit／push／開 PR／merge／deploy，也不修改外部索引。T-0009 已 done，本次沿用原單票無依賴粒度，依全域編號記錄 T-0010；舊失敗紀錄保留，未授權 landing 前維持 review。
