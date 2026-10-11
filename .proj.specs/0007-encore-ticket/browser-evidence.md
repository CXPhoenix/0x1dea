# 建置後文章的瀏覽器驗證

驗證表面：現有 `pnpm docs:build` 產生的實際文章，透過 `pnpm docs:preview --host 127.0.0.1 --port 4180` 與獨立 Chromium session 檢查。這不是前一階段的設計原型，也不代表部署結果。

| Viewport | 主題 | 文章／票券寬度 | 票券在文章範圍內 | 票券／文字水平溢出 |
|---|---|---|---|---|
| 1280px | 淺色 | 624px／624px | 是 | 無／無 |
| 1280px | 深色 | 624px／624px | 是 | 無／無 |
| 390px | 淺色 | 342px／342px | 是 | 無／無 |
| 390px | 深色 | 342px／342px | 是 | 無／無 |

四種狀態已擷取截圖並檢視實際版型。票根保留直排，虛線為 dashed，缺口由偽元素呈現；手機標題及說明可換行，沒有固定高度裁切。淺色背景為 rgb(246, 246, 247)，深色為 rgb(32, 33, 39)，沿用 VitePress tokens。

鍵盤：從前一節 permalink 按 Tab，焦點到達票券。淺色 outline 為 rgb(52, 81, 178) solid 3px，深色為 rgb(168, 177, 255) solid 3px；`:focus-visible` 為 true。可存取樹呈現一個包含「同場加映、延伸閱讀、推薦標題、說明、來看這一篇」的 link，沒有 ENCORE 或箭頭。沒有巢狀互動元素。

在手機深色狀態按 Enter，原分頁導覽到 `/post/course/cybersec/what-is-safety.html`，頁面標題為「安全？能吃嗎？ | 0x1DEA」。Browser error log 為空。原始 prop 仍是 `/post/course/cybersec/what-is-safety`，由現有 VitePress router 解析。

截圖保存在本次本機 visualization 輸出目錄：`encore-ticket-article-desktop.png`、`encore-ticket-article-dark.png`、`encore-ticket-article-mobile.png`、`encore-ticket-article-mobile-dark.png`。
