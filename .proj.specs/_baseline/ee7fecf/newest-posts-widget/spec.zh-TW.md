---
language: zh-TW
authority: spec.en.md
synced_from: spec.en.md
synced_from_sha: 24328022e6b605d323551458e08bdb1435bc21a4
source_path: openspec/specs/newest-posts-widget/spec.md
source_commit: ee7fecfff72f47abc735d26ac7e9a943de04ebbf
historical_harness_review: not-recorded-under-harness
---
# newest-posts-widget 規格稽核翻譯

> 英文原文是歷史權威；本頁是全文稽核翻譯。歷史 Harness review、TDD 與 landing 未記錄，不在此次重建。 Harness 歷史狀態為 `not recorded under harness`；`historical review not recreated`。下文保留歷史 docs 路徑；目前採用的 blog 路徑投影另見 adoption 規格。

## 目的

固定 `<NewPost />` 元件的契約：它是可嵌入首頁或任何 Markdown 頁面的「最新文章」清單，供需要精選文章來源的頁面使用。範圍包含 `count`（預設 `-1`，顯示全部）、`showCategory`（預設 `false`）、嚴格的 `filter → sort → slice` 執行順序，以及 `usePostSort`／`usePostFilter` composable 契約。兩個 composable 分別匯出型別為 `(a: Post, b: Post) => number` 與 `(post: Post) => boolean` 的 `InjectionKey` symbol：`sortPostsKey` 與 `filterPostsKey`。使用頁面可透過 Vue `provide()` 覆寫其中一項或兩項，不必修改元件。日後修改 props、處理順序或覆寫契約，必須針對此 capability 提出差異規格。

## 需求

### Requirement: NewPost 必須接受 count 與 showCategory props，並提供文件所載預設值

`docs/.vitepress/theme/components/NewPost.vue` 的 `NewPost` 必須宣告兩個 props：

- `count?: number`，預設 `-1`。`-1` 代表「顯示通過篩選與排序的所有文章」。任何非負整數 `N` 必須透過 `slice(0, N)` 將顯示數量限制為最多 `N` 篇。作者不得傳入其他負整數（例如 `-2`、`-100`）。非 `-1` 的負數會進入原始碼的 `slice(0, props.count)`，套用 JavaScript 負索引 `slice` 語意，刪除末尾 `|count|` 篇；這項行為未記載、容易造成意外，必須視為契約之外。工具不得傳入非整數（例如 `1.5`、`NaN`）；非整數行為未定義。
- `showCategory?: boolean`，預設 `false`。為 `true` 時，每個顯示出的子 `PostBlock` 都必須顯示分類標籤。

每篇通過處理的文章必須只以 `PostBlock` 呈現，不使用 `PostCard` 或檢視切換。元件不得提供其他公開 props、slots 或 events。

#### Scenario: 預設 count 顯示全部文章

- **WHEN** 顯示 `<NewPost />`
- **THEN** 顯示所有通過篩選的文章，不套用 slice 數量限制
- **AND** 不顯示分類標籤，因為 showCategory 預設為 `false`

#### Scenario: 明確指定 count 限制顯示數量

- **WHEN** 對 10 篇文章顯示 `<NewPost :count="3" />`
- **THEN** 最多顯示三個 `PostBlock`

#### Scenario: showCategory 傳給子元件

- **WHEN** 顯示 `<NewPost :count="5" :showCategory="true" />`
- **THEN** 每個子 `PostBlock` 顯示自己的 `post.category` 標籤

##### 範例：count 語意

| `count` prop | 來源數量 | 顯示數量 | 說明 |
| --- | --- | --- | --- |
| `-1`（預設） | 10 | 10 | 特殊值，完全跳過 slice。 |
| `0` | 10 | 0 | 空的 slice。 |
| `3` | 10 | 3 | 一般數量限制。 |
| `100` | 10 | 10 | 限制大於來源數量，JS `slice` 回傳全部。 |
| `5` | 0 | 0 | 來源為空，限制無實際作用。 |
| `-2` | 10 | **8**（契約之外） | JS `slice(0, -2)` 刪除末尾兩篇，容易造成意外；作者不得使用。 |

---
### Requirement: NewPost 必須依 filter、sort、slice 的固定順序處理

`NewPost` 的 `newestPosts` computed 必須嚴格依下列順序轉換匯入的 `posts`：

1. 透過 `[...posts]` 淺拷貝，確保不修改匯入陣列。
2. 套用 `usePostFilter()` 回傳的 predicate。篩選必須先於排序，讓比較函式不會收到被排除的文章。
3. 套用 `usePostSort()` 回傳的比較函式。
4. 若 `count !== -1`，套用 `slice(0, count)`；否則直接回傳排序後陣列。

元件不得調換階段，也不得修改來源 `posts` 陣列。

#### Scenario: 篩選先於排序

- **WHEN** 篩選排除 category 為 `"draft"` 的文章
- **AND** 排序依 `createdTime` 由新到舊
- **THEN** 顯示清單只有非草稿文章，依時間由新到舊排列

#### Scenario: count 為 -1 時跳過 slice

- **WHEN** `count === -1`，篩選與排序後陣列長度為 7
- **THEN** 顯示陣列長度為 7，不套用 slice

#### Scenario: 不修改來源 posts 陣列

- **WHEN** 對 10 篇來源文章顯示 `<NewPost :count="3" />`
- **THEN** 顯示後匯入的 `posts` 陣列仍有 10 個元素
- **AND** 原始元素順序保持不變

---
### Requirement: usePostSort 必須匯出 sortPostsKey，預設依 createdTime 由新到舊

`docs/.vitepress/theme/composables/usePostSort.ts` 必須匯出：

- 型別別名 `PostSortFn = (a: Post, b: Post) => number`。
- 名稱為 `sortPostsKey`、由 `Symbol` 建立的 `InjectionKey<PostSortFn>`。
- `usePostSort(): PostSortFn`，回傳 `inject(sortPostsKey, defaultSort)`。

預設比較函式 `defaultSort` 必須實作 `createdTime` 降冪排序：

```ts
(a, b) => new Date(b.createdTime).getTime() - new Date(a.createdTime).getTime()
```

因 JSON 序列化可能把 Date 轉成字串，預設比較函式必須支援 `Date` 實例或 ISO-8601 字串形式的 `createdTime`。

#### Scenario: 未提供 provider 時預設由新到舊

- **WHEN** 父元件未提供 `sortPostsKey`
- **AND** 文章的 `createdTime` 是 2026-03-01、2026-02-15、2026-01-20
- **THEN** `usePostSort()` 回傳的比較函式將文章排為 2026-03-01、2026-02-15、2026-01-20

#### Scenario: 自訂 provider 取代預設值

- **WHEN** 父元件呼叫 `provide(sortPostsKey, (a, b) => a.title.localeCompare(b.title))`
- **THEN** `usePostSort()` 回傳提供的比較函式
- **AND** 文章依標題字母順序排列

---
### Requirement: usePostFilter 必須匯出 filterPostsKey，預設接受全部文章

`docs/.vitepress/theme/composables/usePostFilter.ts` 必須匯出：

- 型別別名 `PostFilterFn = (post: Post) => boolean`。
- 名稱為 `filterPostsKey`、由 `Symbol` 建立的 `InjectionKey<PostFilterFn>`。
- `usePostFilter(): PostFilterFn`，回傳 `inject(filterPostsKey, defaultFilter)`。

預設 predicate `defaultFilter` 必須是 `() => true`，接受每篇文章。

#### Scenario: 未提供 provider 時接受全部

- **WHEN** 父元件未提供 `filterPostsKey`
- **THEN** `usePostFilter()` 回傳對每篇輸入文章都回傳 `true` 的 predicate

#### Scenario: 自訂 provider 取代預設值

- **WHEN** 父元件呼叫 `provide(filterPostsKey, post => post.category === "ctf")`
- **THEN** `usePostFilter()` 回傳提供的 predicate
- **AND** `NewPost` 篩選階段只保留 `category` 為 `"ctf"` 的文章

---
### Requirement: 使用頁面必須能透過 provide 分別覆寫排序與篩選

頁面與父元件必須能匯入 `usePostSort`／`usePostFilter` 的對應 `InjectionKey` symbol，再呼叫 `provide(...)`，覆寫排序、篩選、兩者或兩者皆不覆寫。若只提供一個 key，另一個必須維持預設行為。只要 provider 位於同一元件子樹，任何使用 `<NewPost />` 的後代，不論巢狀深度，都必須符合注入契約。

#### Scenario: 頁面只提供排序

- **GIVEN** Markdown 頁面的 `<script setup>` 呼叫 `provide(sortPostsKey, ascendingByCreatedTime)`
- **AND** 頁面未提供 `filterPostsKey`
- **WHEN** 頁面內顯示 `<NewPost :count="5" />`
- **THEN** 文章由舊到新排列
- **AND** 所有文章通過預設「接受全部」篩選

#### Scenario: 頁面只提供篩選

- **GIVEN** Markdown 頁面呼叫 `provide(filterPostsKey, post => post.category.startsWith("course"))`
- **AND** 頁面未提供 `sortPostsKey`
- **WHEN** 頁面內顯示 `<NewPost :count="5" />`
- **THEN** 只保留 category 以 `"course"` 開頭的文章
- **AND** 保留文章依預設排序由新到舊

#### Scenario: 頁面同時提供排序與篩選

- **GIVEN** Markdown 頁面同時呼叫 `provide(filterPostsKey, ...)` 與 `provide(sortPostsKey, ...)`
- **WHEN** 頁面內顯示 `<NewPost :count="3" />`
- **THEN** 使用提供的 predicate 篩選
- **AND** 使用提供的比較函式排序
- **AND** slice 將最終數量限制為最多三篇

#### Scenario: 頁面不提供排序或篩選

- **GIVEN** Markdown 頁面未對任一 key 呼叫 `provide()`
- **WHEN** 頁面內顯示 `<NewPost :count="5" />`
- **THEN** 所有文章通過預設篩選
- **AND** 依 `createdTime` 由新到舊排序
- **AND** 最多顯示五篇

##### 範例：provider 組合

| 頁面 provider | 篩選行為 | 排序行為 |
| --- | --- | --- |
| 無 | 接受全部 | `createdTime` 降冪 |
| 只有 `sortPostsKey` | 接受全部 | 提供的比較函式 |
| 只有 `filterPostsKey` | 提供的 predicate | `createdTime` 降冪 |
| 兩者 | 提供的 predicate | 提供的比較函式 |
