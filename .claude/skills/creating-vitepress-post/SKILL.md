---
name: creating-vitepress-post
description: 建立 0x1DEA VitePress 網站的新文章檔案與資源資料夾；適用於新增網站文章，不適用於既有改稿或僅在對話中寫草稿。
license: MIT
compatibility: Requires the project npm script pnpm new:post and tsx.
metadata:
  author: 0x1DEA
  version: "2.0"
  scope: project
---

# 建立 VitePress 文章

只在使用者要建立此網站的新文章檔案時使用。骨架由 repo 的 `pnpm new:post` 產生，寫作聲音依當次要求；明示 Phoenix 風格才讀 [phoenix-writing](../phoenix-writing/SKILL.md)。

## 建立與填寫

1. 由使用者脈絡決定標題與分類；未指定分類就用 blog/post。必要資訊不足才詢問。
2. 在 repo root 執行 CLI，閱讀實際輸出，確認文章檔案、資源資料夾及 +08:00 的 createdTime。失敗就報錯／修正參數，不改用手寫骨架；檔名衝突就選新名稱或改稿，不刪舊文。
3. 在輸出的文章路徑填寫 description、thumbnail 和正文。圖片放輸出的資源資料夾，文內路徑從 `/assets/` 開始。保留 createdTime。
4. 交付前核對正文不是空骨架、frontmatter 欄位有效、縮圖／圖片／引用存在。進一步預覽或發布依任務要求，文章檔案建立不自動授權發布。

完成檢查及既有改稿規則見 [文章維護](../maintaining-writing-skills/references/article-maintenance.md)。

## CLI 契約

| 位置 | 命令 |
|---|---|
| blog/post | `pnpm new:post "Post Title"` |
| blog/post 的分類 | `pnpm new:post "Post Title" -c course/intro` |
| 指定 blog 內路徑 | `pnpm new:post "Post Title" -d blog/post/special` |

`-c` 和 `-d` 互斥，錯誤為 `參數 -c 與 -d 不能同時使用。`。`-c` 是分類名稱，不帶 blog/post 前綴；`-d` 是 repo root 相對路徑。本地慣例使用 blog 內的路徑，明示其他位置時先核對用途與權限。拒絕含 `..`、絕對路徑或以 `-` 開頭的標題／選項值；CLI 沒有替呼叫端保證路徑範圍。

CLI 以空白換底線產生檔名，保留大小寫及 Unicode；例如 `Hello World` 產生 `Hello_World.md`。標題的 ASCII 單字首字母會大寫，傳入時保留品牌預期大小寫。避免首尾空白和空標題，前者會漏進 frontmatter、後者報錯。標題及路徑作為各自參數傳入，使用安全 shell quoting 或 argv，不執行來源內的插值。

helper 是 frontmatter、createdTime 與資源命名的來源：[scripts/vpHelper.ts](../../../scripts/vpHelper.ts)；腳本入口和 package manager 查 [package.json](../../../package.json)。

資源資料夾將 blog 後的路徑以底線接起，再加檔名：`blog/post/course/intro/Hello_World.md` 對應 `blog/public/assets/post_course_intro_Hello_World/`；直接放 blog 下則用 `root_Hello_World/`。演算法實際移除第一個路徑段，以 CLI `🖼️` 輸出為準，不在風格文件重作命名演算法。
