---
synced_from: spec.en.md
synced_from_sha: ad38e39db5b2784e1ff18dc4346d1625c2af53df
---

# 認知推廣系列 listing 補修

使用者明確要求修正遺漏的 listing，並以既有資安教學系列的文章列為範例。本次納入尚未提交的 T-0010，只取代原規格對單一分類 index 的修改限制；原規格及審查保留為歷史紀錄。沿用單票、無依賴及已核准的 renderer／build／browser、公開 verifier CLI 測試 seam，不 commit、push、開 PR、merge 或部署。

PR #17 使用手寫 Markdown 清單；只恢復 staging `4005ee45f2f3267a8b53ce24fa97af7b49cfb144` 的同一檔案，以既有 `NewPost`、分類篩選與 `count: -1` 呈現，保留介紹，不匯入 staging 歷史或其他文章。

原 index 的 mode 為 `100644`、SHA-256 為 `7da24230dca20c0a475caef2d616b15a7f56f47443f97eb7e0f8de6963c1f174`；新檔案 mode 同為 `100644`、SHA-256 為 `5c578e76cdbd84e0d316008e341d56daaa34a0f150237a53a9111bcd58c73d3a`。先完整驗證原 34 個產品／45 個總路徑契約，再單獨核對目前 index 的固定新身分；不得將它加入可自由變更的 CODE、更新舊 scope，或從目前 bytes 推導核准。執行時不需 staging 物件。

- L1：index 精確符合固定新檔案。實際瀏覽器只有用電文章的一列 `.post-block`，呈現原 frontmatter 標題、摘要、日期 `2026年10月9日` 與 `/post/course/security-awareness/electricity-privacy.html` 連結；保留介紹，排除其他分類及五篇未發布候選。
- L2：桌面 `1440×900` 與手機 `390×844` 的明暗模式都可見標題、摘要、日期，沒有水平溢出；鍵盤聚焦後按 Enter 能開啟文章，共用元件不變。
- L3：公開 preservation CLI 接受修正後的 main；舊靜態 index、bytes／executable mode 改變、刪除及 symlink 都拒絕。每個負向控制先確認正向成功並核對預定錯誤，原歷史 hash、scope、祖先及其他來源拒絕檢查保留。
- L4：文章、時間、圖片、其他分類、package／lockfile、既有發布與歷史證據維持原 bytes；只允許此 index 及 T-0010 既有 verifier／harness 修正。完整測試與檢查成功，Python 無 skip，獨立 Standards／Spec／安全審查無未解決的阻擋問題。

沿用實際 build／browser，不新增 UI 測試框架。含可執行 Markdown 的 build 在 OS sandbox 中執行，禁止網路，限制寫入可丟棄投影與暫存輸出，並實測拒絕外部寫入及網路。只證明本機行為；publication CLI 對新增可執行 Markdown 的拒絕維持，不宣稱遠端已修復。
