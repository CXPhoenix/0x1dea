# 文章摘要元件 ArticleSummary

在 Markdown 直接使用已註冊的 PascalCase 元件。Opening tag 後、closing tag 前保留空白行，內文由 VitePress 原生 Markdown 編譯。

```md
<ArticleSummary variant="note">

- 總度數會漏掉時間變化；較細的用電紀錄，可能留下作息線索。
- NILM 與在家狀態模型做的是估計，曲線不能直接證明誰做了什麼。
- 刪掉姓名仍可能保留連結線索。收哪些細節，先看分析目的。

</ArticleSummary>

這段後文在元件外面。
```

| Prop | 預設 | 行為 |
|---|---|---|
| variant | note | note 淡色便條；cards 三張 icon 卡片、手機直排；terminal 深色視窗，標題列與每個頂層 unordered-list 項目前的裝飾 $。省略／無效值回 note。 |
| title | TL;DR | 純文字標題與可及性名稱；空白回 TL;DR。Terminal 使用它作為視窗 title。 |

三種外觀使用同一份作者內容。段落、list、link、粗體／斜體、inline code、fence 與原生 info/tip/warning/details 都可保留。標準三短句以頂層三項 unordered list 表示；其他內容不會被裁切、重寫或自動生成。

Cards 的 icon 與 Terminal 的 $ 都是純裝飾，不加入複製與可及性文字。Prompt 只在直接頂層項目出現，視覺換行、巢狀清單與容器清單不重複添加。Terminal 是靜態閱讀視窗，沒有命令輸入或假的視窗控制項。所有樣式支援深／淺色、手機與白底列印。

CSS module 限定元件樣式；不新增 custom container、Markdown parser 或 v-html。作者 Markdown 沿用本站可信作者編譯流程，不是任意不受信任 HTML 的清理器。錯誤／未閉合標籤遵循原 compiler 行為，請先修正 Markdown 標記。

參考：[Vue in Markdown](https://vitepress.dev/guide/using-vue)、[Custom Containers](https://vitepress.dev/guide/markdown#custom-containers)。本次驗證使用既有 VitePress 2.0.0-alpha.16，沒有升級依賴。
