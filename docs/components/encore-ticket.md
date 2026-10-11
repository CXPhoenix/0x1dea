# 同場加映票券

`EncoreTicket` 可直接用在網站 Markdown 文章，不需要自行 import。整張票券都是連結，會在同一個分頁開啟推薦文章；外觀跟隨網站的深淺色主題，手機也會保留直排票根。

提供推薦標題、站內連結與說明文字：

```vue
<EncoreTicket
  title="什麼是安全？能吃嗎？"
  href="/post/course/cybersec/what-is-safety"
  description="如果平常怎麼運作都還不清楚，要怎麼發現哪裡出了問題呢？"
/>
```

也可以省略說明文字：

```vue
<EncoreTicket
  title="什麼是安全？能吃嗎？"
  href="/post/course/cybersec/what-is-safety"
/>
```

| Prop | 必填 | 用途 |
|---|---|---|
| `title` | 是 | 推薦文章的標題 |
| `href` | 是 | 作者提供的連結；本站文章使用以 `/post/` 開頭的路徑 |
| `description` | 否 | 推薦理由；省略時不會留下空白段落 |

標題與說明都以純文字顯示，不解析 HTML 或 Markdown。連結由文章作者提供，元件不會自動查詢文章資料，也不是不可信任網址的過濾器。
