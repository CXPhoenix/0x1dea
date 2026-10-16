# 首頁預覽說明

文案直接在 `blog/index.md` 編輯，不必改部署環境：

```vue
<PreviewNotice
  title="六篇 staging 試稿預覽"
  text="這六篇供 staging 預覽與審稿，尚未發佈到正式站。"
/>
```

元件使用純文字 props，不解析 HTML／Markdown。頭尾空白裁掉，內嵌換行保留；省略或空欄位不顯示，兩者皆空時不顯示整個說明。僅文案時可存取名稱為「預覽說明」。

## 唯一環境開關

`VITE_SITE_NOTICE_ENABLED` 只有精確 `true` 會啟用。明確 `false`、空字串、空白或任何其他值皆停用；未提供時，僅 Cloudflare 自動提供的 `CF_PAGES_BRANCH=staging` 啟用，其餘分支及本機預設隱藏。此開關是公開的建置字串，不可放秘密。

| Cloudflare Pages environment | 設定 |
| --- | --- |
| Preview | `VITE_SITE_NOTICE_ENABLED=true` |
| Production | 不設定，或明確 `VITE_SITE_NOTICE_ENABLED=false` |

`CF_PAGES_BRANCH` 不需自行新增。若只要 staging 分支顯示，可省略 Preview 的開關，使用分支判斷；Preview 明確 true 會涵蓋該環境的其他 preview 分支。Production 的非 staging 分支預設隱藏；明確 false 優先於分支標記。

[Vite 環境變數](https://vite.dev/guide/env-and-mode)在建置時替換，[Cloudflare 官方建置設定](https://developers.cloudflare.com/pages/configuration/build-configuration/)列出分支標記。變更環境需重啟 dev server／重新 build。兩種部署都使用 production mode。環境設定與文案變更需要新的建置才會反映在部署。

## 本機位置與啟動

VitePress 網站 root 仍是 `blog/`；`vite.envDir` 明確指向 repo 根目錄，`.env.example` 及 `.env` 都放根目錄。Git 忽略 `.env`、模式與 local 變體，允許 `.env.example` 追蹤。

若 `.env` 尚不存在，可複製 `.env.example` 並將開關改為 `true`。既有 `.env` 請只整合這個公開開關，保留其他設定；不要覆寫原檔或提交秘密。

已有依賴的工作樹可執行：

```sh
pnpm docs:dev --host 127.0.0.1 --port 4176 --strictPort
```

本機 `.env` 的 true 也會影響同一工作樹的 build。正式站預設測試使用沒有本機 `.env` 的乾淨副本，或以 `VITE_SITE_NOTICE_ENABLED=false` 明確覆寫。僅 loopback 預覽；server 關閉後 URL 不能瀏覽。
