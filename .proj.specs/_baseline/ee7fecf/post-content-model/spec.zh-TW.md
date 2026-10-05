---
language: zh-TW
authority: spec.en.md
synced_from: spec.en.md
synced_from_sha: 9f925a4a6c7963cdd675037749048f619a5a98c5
source_path: openspec/specs/post-content-model/spec.md
source_commit: ee7fecfff72f47abc735d26ac7e9a943de04ebbf
historical_harness_review: not-recorded-under-harness
---
# post-content-model 規格稽核翻譯

> 英文原文是歷史權威；本頁是全文稽核翻譯。歷史 Harness review、TDD 與 landing 未記錄，不在此次重建。 Harness 歷史狀態為 `not recorded under harness`；`historical review not recreated`。下文保留歷史 docs 路徑；目前採用的 blog 路徑投影另見 adoption 規格。

## 目的

固定 0x1DEA VitePress 網站的 canonical 文章資料模型：`docs/shared/posts.data.ts` 產生的 TypeScript `Post` 介面、以 `createContentLoader('post/**/*.md')` 為基礎的探索流程、文章及 `isIndex` 分類入口頁的 frontmatter 慣例、三層分類解析順序（frontmatter → 同目錄 `index.md` → URL 路徑），以及各欄位的預設值規則。規則刻意區分 `||` 與 `??`：保留明確指定的空字串 `description`，卻不保留空字串 `title`。日後修改 loader、文章 frontmatter 格式或分類繼承模型，必須針對此 capability 提出差異規格。

## 需求

### Requirement: Post 介面必須定義八個必要欄位

`docs/shared/posts.data.ts` 匯出的 `Post` 必須正好宣告下列八個欄位，且全部為必要欄位：

- `title: string`
- `url: string`
- `description: string`
- `createdTime: Date`
- `thumbnail: string`
- `category: string`
- `categoryFromPath: string`
- `categoryRootPath: string`

loader 使用端必須能匯入 `Post` 型別，並確信 loader 回傳的每篇文章都具有所有列出的欄位，沒有 optional 欄位。

loader 的 `Post` 是 VitePress 資料流程產生的 canonical、較窄資料形狀。`docs/.vitepress/theme/components/` 的顯示元件 `PostCard`、`PostBlock`、`PostList` 在本地重新宣告結構上**較寬**的 `Post`：`description`、`thumbnail`、`category` 為 optional，`createdTime` 可為 `Date | string | { seconds: number; nanoseconds: number }`。較寬形狀是顯示元件的契約，記錄於 `post-display-views`。loader 產生的文章同時符合兩者；較寬的本地形狀讓元件也能接受其他來源的文章。

#### Scenario: 匯入型別包含每個記載欄位

- **WHEN** Vue 元件匯入 `import type { Post } from '../../shared/posts.data'`
- **THEN** 型別提供 `title`、`url`、`description`、`createdTime`、`thumbnail`、`category`、`categoryFromPath`、`categoryRootPath`
- **AND** 八個欄位都不是 optional

#### Scenario: 載入文章的每個欄位都有值

- **WHEN** loader 產生代表 `docs/post/**/*.md` 任一文章的陣列元素
- **THEN** 八個欄位各具有宣告型別的值
- **AND** 沒有欄位為 `undefined` 或 `null`

---
### Requirement: Loader 必須使用 createContentLoader 探索文章並排除 index 頁

`docs/shared/posts.data.ts` 必須呼叫 `createContentLoader('post/**/*.md', { includeSrc: true, render: false, excerpt: false })` 探索文章。frontmatter 的 `isIndex` 為 truthy 時，必須排除該檔案；省略 `isIndex` 或設為 falsy 時，必須納入。

#### Scenario: 納入 docs/post/ 的一般文章

- **WHEN** loader 處理 `docs/post/<...>.md`，其 frontmatter 未設定 `isIndex`，或設為 `false`
- **THEN** 檔案以 `Post` 元素出現在回傳陣列

#### Scenario: 排除分類 index 頁

- **WHEN** loader 處理 `docs/post/<segments>/index.md`，frontmatter 設定 `isIndex: true`
- **THEN** 檔案不出現在回傳陣列

##### 範例：納入與排除

| 檔案路徑 | frontmatter `isIndex` | 納入輸出 |
| --- | --- | --- |
| `docs/post/course/cybersec/what-is-safety.md` | 省略 | 是 |
| `docs/post/course/cybersec/index.md` | `true` | 否 |
| `docs/post/course/rm/why-we-need-rm.md` | 省略 | 是 |
| `docs/post/course/rm/index.md` | `true` | 否 |

---
### Requirement: Loader 必須依三層優先順序解析 category

每篇納入的文章，loader 必須依下列順序設定 `category`，在第一個得到值的層級停止：

1. 文章自身 truthy 的 `frontmatter.category`。原始碼使用 `||`，所以空字串 `category` 會進入第二層。
2. 否則使用**同一目錄** `index.md` frontmatter 記錄的分類。查詢是以 `categoryRootPath` 為 key 的 map 做**精確 key 查詢**；loader 不往父目錄找。`docs/post/a/b/c/foo.md` 的 `categoryRootPath` 為 `/post/a/b/c`，只繼承 `docs/post/a/b/c/index.md`，不繼承 `docs/post/a/b/index.md`。查詢以 `??` 組合，只在 `undefined` 時取後備值，因此記錄的值即使是空字串也會回傳。
3. 否則使用 `getCategoryFromUrl(url)`：移除 `/post/` 前綴及副檔名，再以 `/` 串接最後一段以外的路徑。移除後少於兩段（頂層文章）時，回傳字面後備值 `'綜合'`。

#### Scenario: 明確指定的 frontmatter 分類優先

- **WHEN** `docs/post/course/cybersec/foo.md` frontmatter 宣告 `category: "Custom"`
- **AND** `docs/post/course/cybersec/index.md` 宣告 `category: "資安教學"`
- **THEN** 載入文章的 `category` 為 `"Custom"`

#### Scenario: 從同目錄 index 頁繼承分類

- **WHEN** `docs/post/course/cybersec/foo.md` 未宣告 `category`
- **AND** `docs/post/course/cybersec/index.md` 宣告 `isIndex: true` 與 `category: "資安教學"`
- **THEN** 載入文章的 `category` 為 `"資安教學"`

#### Scenario: 較深文章不繼承父目錄 index 分類

- **WHEN** 文章位於 `docs/post/course/cybersec/sub/foo.md`，未宣告 `category`
- **AND** `docs/post/course/cybersec/index.md` 宣告 `isIndex: true` 與 `category: "資安教學"`
- **AND** 沒有 `docs/post/course/cybersec/sub/index.md`
- **THEN** 載入的 `category` 為第三層 URL 推導字串 `"course/cybersec/sub"`，不是 `"資安教學"`

#### Scenario: 無同目錄 index 時由 URL 推導分類

- **WHEN** 文章位於 `docs/post/tech/js/intro.md`
- **AND** 沒有宣告分類的 `docs/post/tech/js/index.md`
- **AND** 文章本身也未宣告分類
- **THEN** 載入的 `category` 為 `"tech/js"`

#### Scenario: 頂層文章後備值為綜合

- **WHEN** 文章直接位於 `docs/post/single.md`
- **AND** 未宣告分類
- **AND** 同目錄 `index.md` 沒有提供分類
- **THEN** 載入的 `category` 為 `"綜合"`

---
### Requirement: Loader 必須一律從 URL 填入 categoryFromPath 與 categoryRootPath

對每篇納入的文章，loader 必須設定 `categoryFromPath` 為 `getCategoryFromUrl(post.url)`，`categoryRootPath` 為 `getCategoryRootPath(post.url)`，獨立於 `category` 解析順序。兩欄必須反映 URL 結構，不受 frontmatter 覆寫 `category` 影響。

#### Scenario: categoryFromPath 忽略 frontmatter 覆寫

- **WHEN** `docs/post/course/cybersec/foo.md` 宣告 `category: "Custom"`
- **THEN** `category === "Custom"`
- **AND** `categoryFromPath === "course/cybersec"`
- **AND** `categoryRootPath === "/post/course/cybersec"`，即移除檔名段的文章 URL。對 URL 以 `/` 結尾的 index 頁，移除尾端空段後得到與同目錄文章相同的 key，因此同目錄繼承查詢能成立。

##### 範例：URL 推導欄位

| 文章 URL | `categoryFromPath` | `categoryRootPath` |
| --- | --- | --- |
| `/post/course/cybersec/what-is-safety` | `course/cybersec` | `/post/course/cybersec` |
| `/post/course/rm/why-we-need-rm` | `course/rm` | `/post/course/rm` |
| `/post/single` | `綜合` | `/post` |

> **注意**：頂層文章的 `categoryFromPath === '綜合'` 是與第三層後備值相同的**字面字串**，不是「沒有路徑分類」的特殊標記。頂層文章的這兩種分類結果都是 `'綜合'`，因為無路徑階層時 `getCategoryFromUrl` 就回傳此字串。

---
### Requirement: Loader 必須為缺漏 frontmatter 套用欄位後備值

對每篇納入的文章，對應 frontmatter 缺漏或空白時必須套用以下規則：

| 欄位 | JS 運算子 | 空字串 `""` | YAML `null`／`~` | 後備值 |
| --- | --- | --- | --- | --- |
| `title` | **`\|\|`** | 使用後備值，`""` 為 falsy | 使用後備值，null 為 falsy | `'無標題'` |
| `description` | **`??`** | **保留**，`""` 非 nullish | 使用後備值，null 是 nullish | `'閱讀更多...'` |
| `createdTime` | 三元 `frontmatter.createdTime ? ... : ...` | 使用後備值，`""` 為 falsy | 使用後備值，null 為 falsy | loader 執行當下的合成 `Date.now() - idx * 86_400_000` 毫秒，每個文章陣列位置相差一天 |
| `thumbnail` | **`\|\|`** | 使用後備值 | 使用後備值 | `https://picsum.photos/seed/${idx + 1}/400/300` |

`||`（title、thumbnail、第一層 category）與 `??`（description、第二層 category）的差別是刻意設計：只有 `description` 保留明確宣告的空字串。差別不延伸到 `null`；上表所有欄位在 null 時都使用後備值，因為 `||` 與 `??` 對 null／undefined 都會取另一側。作者與工具不得假設空 `title` 或空 `thumbnail` 會保留，兩者都會直接被後備值取代。YAML 使用 `description: null` 或 `description: ~` 時，必須預期得到 `'閱讀更多...'`，而不是字面字串 `null`。

合成 `createdTime` 必須每個陣列位置正好減少一天，讓缺少明確時間的文章仍可排序。索引 `idx` 的值為 loader 執行當下捕捉的 `Date.now() - idx * 86_400_000` 毫秒。

#### Scenario: 文章缺少 description、thumbnail 與 createdTime

- **WHEN** frontmatter 只宣告 `title`，且文章在 transform 階段位於索引 `idx`
- **THEN** `description === '閱讀更多...'`
- **AND** `thumbnail` 符合 regex `^https://picsum\.photos/seed/\d+/400/300$`
- **AND** `createdTime` 是 `Date` 實例，值等於 loader 執行時捕捉的 `Date.now() - idx * 86_400_000` 毫秒；`idx === 0` 等於執行時刻，`idx === N` 則早 `N` 天

#### Scenario: 明確將 description 設為空字串

- **WHEN** frontmatter 宣告 `description: ""`
- **THEN** 載入的 `description` 為空字串 `""`
- **AND** 不套用後備值 `'閱讀更多...'`

#### Scenario: 明確將 description 設為 YAML null

- **WHEN** frontmatter 宣告 `description: ~`，或等效的 `description: null`
- **THEN** 載入的 `description` 為 `'閱讀更多...'`；`?? ` 對 `null` 與 `undefined` 相同，都會使用後備值

---
### Requirement: Post frontmatter 的 createdTime 必須使用含 +08:00 偏移的 ISO-8601

文章 frontmatter 宣告 `createdTime` 時，值必須為 ISO-8601 日期時間字串，包含 `+08:00` UTC 偏移。loader 必須直接傳給 `new Date(...)`。作者與工具不得為新文章使用其他時區偏移、未指定時區的日期時間，或以 `Z` 結尾的 UTC 字串。

#### Scenario: 作者以 +08:00 時間撰寫新文章

- **WHEN** frontmatter 宣告 `createdTime: 2026-02-27T00:47:45+08:00`
- **THEN** loader 將 `createdTime` 設為代表 `2026-02-26T16:47:45Z` 的 `Date`，即同一時刻的 UTC 表示

##### 範例：接受與拒絕的 frontmatter 時間

| 值 | 狀態 | 理由 |
| --- | --- | --- |
| `2026-02-27T00:47:45+08:00` | 接受 | ISO-8601，明確 +08:00 偏移 |
| `2026-03-01T18:33:16+08:00` | 接受 | ISO-8601，明確 +08:00 偏移 |
| `2026-02-27T00:47:45Z` | 拒絕 | UTC 時區違反台灣本地慣例 |
| `2026-02-27T00:47:45` | 拒絕 | 未指定時區，偏移不明 |
| `2026/02/27 00:47:45` | 拒絕 | 非 ISO-8601 |

---
### Requirement: Index 頁必須宣告 isIndex 並提供可繼承分類

`docs/post/<segments>/index.md` 的每個分類入口頁都必須在 frontmatter 宣告 `isIndex: true` 與 `category` 字串，供同目錄文章繼承。index 頁不得出現在 loader 輸出。`docs/post/<segments>/` 下自身未宣告 `category` 的文章，必須繼承 index 的 `category`。

#### Scenario: Index 頁提供分類給同目錄文章

- **WHEN** `docs/post/course/cybersec/index.md` 宣告 `isIndex: true` 與 `category: "資安教學"`
- **AND** `docs/post/course/cybersec/what-is-safety.md` 未宣告 `category`
- **THEN** 載入的 `what-is-safety` 文章具有 `category: "資安教學"`
- **AND** index 頁不出現在 loader 輸出

#### Scenario: 沒有 isIndex 的 index 頁會被視為一般文章

- **WHEN** `index.md` 宣告 `category`，卻省略 `isIndex`
- **THEN** loader 將它視為一般文章，納入輸出，且其分類不會被同目錄文章繼承
