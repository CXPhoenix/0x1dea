---
title: 元件驗收
sidebar: false
aside: false
showParticle: false
---

# 元件驗收

<ArticleSummary variant="note">

- 總度數會漏掉 **時間變化**；較細的用電紀錄，可能留下作息線索。
- NILM 與在家狀態模型做的是*估計*，曲線不能直接證明誰做了什麼。
- 刪掉姓名仍可能保留連結線索。收哪些細節，先看分析目的。閱讀 [關於本站](/about) 與 `inline-code`。

</ArticleSummary>

<ArticleSummary variant="cards">

- 總度數會漏掉 **時間變化**；較細的用電紀錄，可能留下作息線索。
- NILM 與在家狀態模型做的是*估計*，曲線不能直接證明誰做了什麼。
- 刪掉姓名仍可能保留連結線索。收哪些細節，先看分析目的。閱讀 [關於本站](/about) 與 `inline-code`。

</ArticleSummary>

<ArticleSummary variant="terminal">

- 總度數會漏掉 **時間變化**；較細的用電紀錄，可能留下作息線索。
- NILM 與在家狀態模型做的是*估計*，曲線不能直接證明誰做了什麼。
- 刪掉姓名仍可能保留連結線索。收哪些細節，先看分析目的。閱讀 [關於本站](/about) 與 `inline-code`。

</ArticleSummary>

後文 sentinel 不在摘要中。

<ArticleSummary variant="terminal" title="Markdown 邊界">

- 很長的內容會在手機換行，一個項目只有一個 prompt，不會因為文字換行再次添加 prompt。
  - 巢狀項目不是新的 prompt。
- [很長連結](https://example.com/a-long-unbroken-path-that-should-never-cause-page-horizontal-overflow-in-the-summary)
- 程式碼 `long-inline-code-abcdefghijklmnopqrstuvwxyz1234567890`

段落 **強調** 與 *斜體*。

```js
console.log('$ is code content')
```

::: info 內部容器
- 容器項目不是 prompt。
:::

</ArticleSummary>

第二個後文 sentinel。

::: info info
原生 INFO

- 容器項目不是 prompt。
:::

::: tip tip
原生 TIP
:::

::: warning warning
原生 WARNING
:::

::: details details
可展開的 DETAILS
:::

<ArticleSummary variant="bad">

fallback note

</ArticleSummary>


## Caption acceptance

::: figure first-proof
![Independent first alt](/assets/post_course_security-awareness_electricity-privacy/p-inference.png "First figure caption")
:::

See @fig:first-proof, @fig:second-proof, @tbl:first-table, @tbl:second-table.

::: table first-table First table caption
| Label | Value |
| --- | --- |
| Alpha | One |
:::

::: figure second-proof
![Independent second alt](/assets/post_course_security-awareness_electricity-privacy/p-inference.png "Second figure caption")
:::

::: table second-table Second table caption
| Label | Value |
| --- | --- |
| Beta | Two |
:::

| Ordinary | Table |
| --- | --- |
| Unnumbered | Unchanged |

[Actual article](/post/course/security-awareness/electricity-privacy)

<PreviewNotice title="Hostile <img src=x onerror=alert(1)>" text="Plain <script>alert(1)</script>
Second line" />
<PreviewNotice title="" text="" />
<EncoreTicket title="First safe recommendation" href="/about" description="Independent first" />
<EncoreTicket title="Second <script>safe</script> recommendation" href="/about" />
