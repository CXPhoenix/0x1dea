---
language: zh-TW
authority: spec.en.md
synced_from: spec.en.md
synced_from_sha: 5a4fc7ac37ba85990abf41e293397ab572c1cf72
source_path: openspec/specs/post-display-views/spec.md
source_commit: ee7fecfff72f47abc735d26ac7e9a943de04ebbf
historical_harness_review: not-recorded-under-harness
---
# post-display-views 規格稽核翻譯

> 英文原文是歷史權威；本頁是全文稽核翻譯。歷史 Harness review、TDD 與 landing 未記錄，不在此次重建。 Harness 歷史狀態為 `not recorded under harness`；`historical review not recreated`。下文保留歷史 docs 路徑；目前採用的 blog 路徑投影另見 adoption 規格。

## 目的

固定三個全域註冊 Vue 文章顯示元件的公開介面：`PostCard`（16:9 縮圖直向卡片）、`PostBlock`（緊湊橫向區塊）、`PostList`（`/posts` 總覽頁，包裝前兩者，提供搜尋欄、時間／分類排序軸切換、升冪／降冪切換、卡片／區塊檢視切換，以及分類群組與 `categoryRootPath` 連結）。也記錄刻意較寬的元件本地 `Post` 介面：接受三種 `createdTime` 形狀，部分欄位為 optional；並固定主題註冊的四個全域元件 `PostCard`、`PostBlock`、`PostList`、`NewPost`。日後修改任一顯示契約，必須針對此 capability 提出差異規格。

## 需求

### Requirement: PostCard 與 PostBlock 必須接受 Post 與 optional showCategory

`PostCard` 與 `PostBlock` 都必須宣告 `post: Post`（必要）與 `showCategory?: boolean`（預設 `true`）。這裡的 `Post` 是各 `.vue` 中的**元件本地** `Post` 介面，比 `docs/shared/posts.data.ts` loader 的較窄 `Post` 寬；後者記錄於 `post-content-model`。`PostCard`／`PostBlock` 本地欄位為：必要 `title: string`、`url: string`，optional `description?: string`、`thumbnail?: string`、`category?: string`，以及必要三種形狀 union `createdTime: { seconds: number; nanoseconds: number } | string | Date`。注意：`PostCard` 與 `PostBlock` 不宣告 `categoryRootPath` 或 `categoryFromPath`，因為不使用這些欄位。`PostList` 另有下文規定的本地 `Post`，必須有 `categoryRootPath: string`，因分類群組顯示會讀取它。loader 文章符合所有本地形狀；較寬宣告讓元件也可使用其他來源的文章。

兩元件必須呈現相同文章資訊（標題、說明、分類、格式化日期、縮圖），但版型不同：`PostCard` 是有 16:9 縮圖的直向卡片，`PostBlock` 是沒有縮圖的橫向區塊。兩者都必須將整個文章表面呈現為導覽 anchor `<a href="post.url">`。

`showCategory` 為 `false` 時，即使 `post.category` 非空也不得顯示分類標籤。`post.thumbnail` 空白或 falsy 時，`PostCard` 必須完全省略縮圖容器，不顯示損壞圖片占位。`post.description` 空白或 falsy 時，兩元件都必須省略說明段落。

#### Scenario: 預設 showCategory 顯示分類標籤

- **WHEN** 以 `post.category = "資安教學"` 顯示 `<PostCard :post="post" />`
- **THEN** 輸出包含具有分類標籤 class、文字為 `"資安教學"` 的元素

#### Scenario: showCategory=false 隱藏分類標籤

- **WHEN** 以 `post.category = "資安教學"` 顯示 `<PostBlock :post="post" :show-category="false" />`
- **THEN** 輸出不包含分類標籤元素

#### Scenario: 缺少縮圖時 PostCard 省略縮圖容器

- **WHEN** 以 `post.thumbnail = ""` 顯示 `<PostCard :post="post" />`
- **THEN** DOM 不包含 `.thumbnail-wrapper`
- **AND** DOM 不包含損壞的 `<img>`

---
### Requirement: PostCard 與 PostBlock 必須將三種 createdTime 輸入格式化為 zh-TW

兩元件必須接受三種 `createdTime`，並用 `Date#toLocaleDateString('zh-TW', { year: 'numeric', month: 'long', day: 'numeric' })` 格式化：

1. 原生 `Date` 實例。
2. 可被 `new Date(...)` 解析的字串。
3. `{ seconds: number; nanoseconds: number }`（Firebase Timestamp 形狀），以 `seconds * 1000` 計算毫秒。

底層時間有效時，對任一形狀都不得拋出錯誤或顯示 `Invalid Date`。

#### Scenario: 接受 ISO-8601 字串

- **WHEN** 顯示 `<PostCard :post="{ ...post, createdTime: '2026-02-27T00:47:45+08:00' }" />`
- **THEN** 日期元素包含對應日期以 `toLocaleDateString('zh-TW', ...)` 格式化的字串

#### Scenario: 接受 Firebase 形式的時間物件

- **WHEN** 顯示 `<PostBlock :post="{ ...post, createdTime: { seconds: 1772124465, nanoseconds: 0 } }" />`；`1772124465` 秒等於 `2026-02-26T16:47:45Z`，與上一個 ISO 情境同一時刻
- **THEN** 日期元素包含該日期以 `toLocaleDateString('zh-TW', ...)` 格式化的字串

##### 範例：輸入形狀

| 輸入 | 解析時刻 UTC | 格式 |
| --- | --- | --- |
| `new Date('2026-02-27T00:47:45+08:00')` | `2026-02-26T16:47:45Z` | zh-TW 長日期字串 |
| `'2026-02-27T00:47:45+08:00'` | `2026-02-26T16:47:45Z` | zh-TW 長日期字串 |
| `{ seconds: 1772124465, nanoseconds: 0 }` | `2026-02-26T16:47:45Z` | zh-TW 長日期字串 |

---
### Requirement: PostList 必須接受 posts 陣列並提供搜尋、排序與檢視控制

`PostList` 必須宣告唯一且必要的 prop `posts: Post[]`。`PostList.vue` 的本地 `Post` 與 `PostCard`／`PostBlock` 相似，但額外將 **`categoryRootPath: string` 定為必要欄位**，讓分類群組建立標題 anchor。完整欄位為必要 `title: string`、`url: string`、`categoryRootPath: string`；optional `description?: string`、`thumbnail?: string`、`category?: string`；以及必要三形狀 union `createdTime: { seconds; nanoseconds } | string | Date`。

陣列非空時，元件必須顯示四個控制：

1. 綁定內部 `searchQuery` 的搜尋欄，字串預設為空。
2. 將 `viewMode` 在 `'card'`／`'block'` 間切換的按鈕，預設 `'block'`。
3. 將 `sortBy` 在 `'time'`／`'category'` 間切換的按鈕，預設 `'time'`。
4. 將 `sortOrder` 在 `'asc'`／`'desc'` 間切換的按鈕，預設 `'desc'`。

`PostList` 不得為狀態改變發出 events；四個控制都操作內部 reactive 狀態。

空狀態與控制列都必須依 `processedPosts.length`（搜尋篩選後的陣列）判定，而不是輸入 prop `posts`。`processedPosts.length === 0` 時：

- `PostList` 必須顯示空狀態，可見文字以 `沒有任何文章，努力產生中！` 開頭，接著 `<br />` 及顏文字 `((└(:3」┌)┘))`。
- `PostList` 不得顯示控制列。

因此，即使 `posts` 非空，只要搜尋沒有符合項目，控制列也會隱藏；使用者要重新掛載或重新整理才可取回搜尋欄。這是原始碼實際行為；下游程式不得假設搜尋進行中控制列會持續存在。

#### Scenario: 初次顯示的預設狀態

- **WHEN** 掛載 `<PostList :posts="[postA, postB]" />`
- **THEN** 搜尋欄為空
- **AND** 以 `block` 檢視顯示文章
- **AND** 依 `createdTime` 降冪，由新到舊

#### Scenario: 切換檢視會替換顯示元件

- **WHEN** 從預設狀態按一次檢視按鈕
- **THEN** 使用 `PostCard` 取代 `PostBlock` 重新顯示文章

#### Scenario: 空文章陣列顯示空狀態並隱藏控制

- **WHEN** 掛載 `<PostList :posts="[]" />`
- **THEN** 不顯示控制列
- **AND** 輸出文字以 `沒有任何文章，努力產生中！` 開頭

#### Scenario: 無搜尋結果也隱藏控制列

- **GIVEN** `<PostList :posts="[postA, postB]" />` 的兩篇標題均不包含 `"無此關鍵字"`，`sortBy` 為預設 `'time'`
- **WHEN** 使用者在搜尋欄輸入 `"無此關鍵字"`
- **THEN** `processedPosts.length` 變為 `0`，沒有標題符合
- **AND** 控制列消失，無法從顯示介面看見或清除搜尋欄
- **AND** 出現空狀態
- **AND** 唯一取回控制列的方法是重新掛載（例如重新整理或切換路由）；元件內沒有復原操作

---
### Requirement: PostList 時間模式搜尋標題，分類模式搜尋標題或分類

`sortBy === 'time'` 時，只比對 `post.title`，對 trim 後的查詢做不分大小寫的子字串比對。`sortBy === 'category'` 時，比對 `post.title` 或 `post.category || '綜合'`，任一欄位符合即保留，亦不分大小寫。空查詢或只有空白的查詢必須符合每篇文章。

#### Scenario: 時間模式只搜尋標題

- **WHEN** `sortBy === 'time'` 時輸入 `"safety"`
- **THEN** 只顯示 `title` 包含 `"safety"` 的文章，不分大小寫
- **AND** 只有 `category` 符合的文章被排除

#### Scenario: 分類模式搜尋標題或分類

- **WHEN** `sortBy === 'category'` 時輸入 `"資安"`
- **THEN** `category: "資安教學"` 的文章即使標題不含 `"資安"` 仍顯示

##### 範例：不同模式的篩選

| `sortBy` | 查詢 | 標題 | 分類 | 顯示 |
| --- | --- | --- | --- | --- |
| `'time'` | `"safe"` | `"What is Safe"` | `"資安教學"` | 是 |
| `'time'` | `"資安"` | `"What is Safe"` | `"資安教學"` | 否 |
| `'category'` | `"資安"` | `"What is Safe"` | `"資安教學"` | 是 |
| `'time'` | `""` | 任意 | 任意 | 是 |

---
### Requirement: PostList 以數值時間及分類字典序排序，同分類固定由新到舊

`sortBy === 'time'` 時，必須依 `createdTime` 的數值差排序，支援與 PostCard／PostBlock 相同三種形狀；`sortOrder` 切換會反轉結果。

`sortBy === 'category'` 時，必須以 `String#localeCompare` 排序 `post.category || '綜合'`。同分類文章的次要排序必須固定依 `createdTime` 降冪，新文章在前，不受 `sortOrder` 影響。不同分類則必須遵守 `sortOrder`。

#### Scenario: 時間降冪顯示最新文章在前

- **WHEN** `sortBy === 'time'`、`sortOrder === 'desc'`，文章 `createdTime` 為 2026-03-01、2026-02-15、2026-01-20
- **THEN** 顯示順序為 2026-03-01、2026-02-15、2026-01-20

#### Scenario: 分類模式以最新時間打破同分類排序

- **WHEN** `sortBy === 'category'`，同為 `category: "資安教學"` 的文章 `createdTime` 為 2026-03-01 與 2026-01-15
- **THEN** 不論 `sortOrder`，該分類內 2026-03-01 均先於 2026-01-15

##### 範例：分類模式順序

| 輸入文章（分類、時間） | `sortOrder` | 輸出順序（分類內按時間） |
| --- | --- | --- |
| `("研究方法教學", 2026-03-01)`、`("資安教學", 2026-02-27)`、`("資安教學", 2026-01-15)` | `'asc'` | 研究方法教學 → 資安教學(2026-02-27) → 資安教學(2026-01-15) |
| 同上 | `'desc'` | 資安教學(2026-02-27) → 資安教學(2026-01-15) → 研究方法教學 |

---
### Requirement: PostList 分類模式必須按分類標題分組，標題連到 categoryRootPath

`sortBy === 'category'` 時，`PostList` 必須為每個分類顯示標題，顯示分類名稱，anchor 連到 `group.categoryRootPath`：排序處理時**第一篇**建立該群組的文章之 `categoryRootPath`。標題下文章必須以 `showCategory="false"` 顯示，因標題已命名分類。`sortBy === 'time'` 時，則以平面清單與 `showCategory="true"` 顯示。

群組必須按排序後 `processedPosts` 的**首次遇見順序**顯示。原始碼用 `processedPosts.forEach` 建立 `Map<string, Group>`，`Map` 保留插入順序。實作不得另行排序群組項目，例如 `Array.from(groups.entries()).sort(...)`。跨分類順序完全由比較函式對 `processedPosts` 的結果及 `sortOrder` 決定。

#### Scenario: 分類標題連到分類根路徑

- **WHEN** `sortBy === 'category'`，群組文章共有 `categoryRootPath: "/post/course/cybersec"`
- **THEN** 標題以 `<a href="/post/course/cybersec">` 包住分類名稱

#### Scenario: 分組文章隱藏內嵌分類標籤

- **WHEN** 文章顯示於分類標題下
- **THEN** `PostCard`／`PostBlock` 不顯示分類標籤

#### Scenario: 平面檢視顯示內嵌分類標籤

- **WHEN** `sortBy === 'time'`
- **THEN** 每個 `PostCard`／`PostBlock` 都顯示 `post.category` 標籤，前提是分類非空

---
### Requirement: 主題必須全域註冊 PostCard、PostBlock、PostList 與 NewPost

`docs/.vitepress/theme/index.ts` 必須在主題 `enhanceApp` 中全域註冊 `PostCard`、`PostBlock`、`PostList` 與 `NewPost` 四個 Vue 元件，讓 Markdown 頁面不必逐頁匯入，就能使用 `<PostCard />`、`<PostBlock />`、`<PostList />`、`<NewPost />`。

#### Scenario: Markdown 不明確匯入即可使用 PostList

- **WHEN** Markdown（例如 `docs/posts.md`）顯示 `<PostList :posts="posts" />`
- **THEN** 無須宣告 `import PostList from ...` 即成功顯示

#### Scenario: Markdown 不明確匯入即可使用 NewPost

- **WHEN** `docs/index.md` 顯示 `<NewPost class="mt-8" :count="5" :showCategory="true" />`
- **THEN** 無須宣告 `import NewPost from ...` 即成功顯示
