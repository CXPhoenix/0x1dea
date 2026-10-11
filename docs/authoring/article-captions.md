# 圖片、表格 caption 與自動引用

只有明確標記的圖片、表格會編號。每篇文章分別從「圖 1」「表 1」開始；meme、橫幅及一般表格維持原本寫法。

## 可直接使用的範例

這段範例可以整段放入文章。`@fig:ems` 顯示為可點擊的「圖 1」，`@tbl:power` 顯示為「表 1」。引用可放在圖表之前，也可放在圖表之後。

```md
從 @fig:ems 可以看到加熱與保溫階段；數值整理在 @tbl:power。

::: figure ems
![電鍋先以 600 W 加熱，再以 50 W 保溫。](/assets/post_course_security-awareness_electricity-privacy/simulated-ems.svg "模擬總功率；教學設定，非住戶實測。來源見 [[1]](#ref-1)。")
:::

![貓說只是來吃宵夜。](/assets/post_course_security-awareness_electricity-privacy/p-cat-event.png)

::: table power 設備功率比較（教學設定）
| 狀態 | 功率 |
| --- | ---: |
| 加熱 | 600 W |
| 保溫 | 50 W |
:::

一般表格不需要編號時，直接寫：

| 項目 | 說明 |
| --- | --- |
| 資料來源 | 教學設定 |

<small>製圖說明：@fig:ems 是模擬資料。</small>

<a id="ref-1"></a>

[1] 本文教學設定，非住戶實測。
```

## 圖片怎麼寫

`::: figure ems` 中的 `ems` 是固定名稱，不是號碼。名稱以小寫英文字母開頭，後面可以接小寫英文字母、數字與連字號，例如 `simulated-ems`。不要在換序時改名。

`![...]` 裡仍是圖片的 `alt`，供替代文字使用；圖片網址後的引號內是 caption。兩者可以不同，caption 不必另外寫在圖片下方，也不要手打「圖 1」。Caption 可使用強調與 Markdown 來源連結。雙引號需要出現在文字中時，可以寫成 `&quot;`。

每個 figure 區塊只放一張獨立的 Markdown 圖片；不要放其他段落、巢狀區塊或原始 `<img>`。區塊最後用獨立一行的 `:::` 關閉。

## 表格與正文引用

`::: table power 表題` 的 `power` 是固定名稱，後面的文字是 caption，只寫一次。區塊內放一張 Markdown 表格，網站會在表格上方產生原生 `<caption>`。

正文使用 `@fig:名稱` 或 `@tbl:名稱`。網站依當篇文章的順序產生號碼和連結；插入、刪除或移動區塊後，caption 與所有引用會一起更新。圖片和表格各自計號。

程式碼區塊、行內程式碼、圖片 alt/title、既有連結的文字與 HTML 屬性不會轉成引用。一般文字中需要原樣顯示標記時，在 `@` 前加反斜線，例如 `\@fig:ems`。Caption 裡的引用標記也保持文字。

## 錯誤與限制

以下情況會讓 Markdown 轉換／建置失敗，訊息會以 `[article-captions]` 開頭，指出相關名稱或區塊：

- 引用不存在：`Unknown reference @fig:missing`。
- 同類型名稱重複：`Duplicate figure ems`；figure 與 table 可共用名稱，因為各自有獨立 namespace。
- 名稱格式不符：`Invalid block: ::: figure Bad`。
- 圖片沒有 title caption：`Missing caption in figure ems`。
- 缺少結尾、內容不是單張圖片／單張表格，或使用巢狀編號區塊。
- 與文章既有的靜態 HTML／標題 ID 撞名：`Reserved anchor collision: fig-ems`。

`fig-` 與 `tbl-` 開頭的 ID 保留給自動圖表；不要在其他 HTML、標題或 Vue 元件使用。動態 Vue ID 不在靜態碰撞檢查範圍內。引用目前只限同一篇文章。

Caption 的 HTML 與 Vue 插值會顯示為文字，不執行；一般 Markdown 連結仍使用既有的 URL 安全檢查。這套功能不會判斷圖片內容或替你撰寫圖說，也不會自動替既有文章加上編號。
