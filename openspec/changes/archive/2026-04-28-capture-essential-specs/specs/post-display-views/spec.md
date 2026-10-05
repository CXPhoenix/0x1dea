## ADDED Requirements

### Requirement: PostCard and PostBlock SHALL accept a Post and an optional showCategory prop

`PostCard` and `PostBlock` SHALL each declare two props: `post: Post` (required) and `showCategory?: boolean` (default `true`). The `Post` interface used by these props is the **component-local** `Post` declared inside each `.vue` file — structurally wider than the loader's narrower `Post` from `docs/shared/posts.data.ts` (which is captured in the `post-content-model` capability). For `PostCard` and `PostBlock` the local interface declares the following fields: `title: string` (required), `url: string` (required), `description?: string` (optional), `thumbnail?: string` (optional), `category?: string` (optional), and `createdTime: { seconds: number; nanoseconds: number } | string | Date` (required, three-shape union). Note: `PostCard` and `PostBlock` do NOT declare `categoryRootPath` or `categoryFromPath` — they have no use for them. `PostList` declares its own local `Post` (specified separately below) which DOES require `categoryRootPath: string` because its category-grouping renderer reads it. Posts emitted by the loader satisfy every local shape. The wider declaration exists so the components remain usable for posts originating from sources other than this loader.

The two components SHALL render the same post fields (title, description, category, formatted date, thumbnail) but in different layouts: `PostCard` as a vertical card with a thumbnail and 16:9 aspect ratio, and `PostBlock` as a horizontal block without a thumbnail. Both components SHALL render the post as an anchor (`<a href="post.url">`) so the entire surface is a navigation link.

When `showCategory` is `false`, neither component SHALL render the category tag, even if `post.category` is non-empty. When `post.thumbnail` is empty / falsy, `PostCard` SHALL omit the thumbnail wrapper entirely (no broken-image placeholder). When `post.description` is empty / falsy, both components SHALL omit the description paragraph.

#### Scenario: Default showCategory renders the category tag

- **WHEN** `<PostCard :post="post" />` is rendered with `post.category = "資安教學"`
- **THEN** the rendered output contains an element with the category tag class displaying `"資安教學"`

#### Scenario: showCategory=false hides the category tag

- **WHEN** `<PostBlock :post="post" :show-category="false" />` is rendered with `post.category = "資安教學"`
- **THEN** the rendered output does NOT contain the category tag element

#### Scenario: Missing thumbnail omits the thumbnail wrapper in PostCard

- **WHEN** `<PostCard :post="post" />` is rendered with `post.thumbnail = ""`
- **THEN** the rendered DOM does NOT contain a `.thumbnail-wrapper` element
- **AND** the rendered DOM does NOT contain a broken `<img>` tag

---

### Requirement: PostCard and PostBlock SHALL format createdTime in zh-TW for three input shapes

Both components SHALL accept `createdTime` as one of three shapes and format it with `Date#toLocaleDateString('zh-TW', { year: 'numeric', month: 'long', day: 'numeric' })`:

1. A native `Date` instance.
2. A string parseable by `new Date(...)`.
3. An object of shape `{ seconds: number; nanoseconds: number }` (Firebase Timestamp shape), where the millisecond value is computed as `seconds * 1000`.

The components SHALL NOT throw or render `Invalid Date` for any of those three shapes when the underlying timestamp is valid.

#### Scenario: ISO-8601 string is accepted

- **WHEN** `<PostCard :post="{ ...post, createdTime: '2026-02-27T00:47:45+08:00' }" />` is rendered
- **THEN** the rendered date element contains a string formatted by `toLocaleDateString('zh-TW', ...)` for the corresponding date

#### Scenario: Firebase-style timestamp object is accepted

- **WHEN** `<PostBlock :post="{ ...post, createdTime: { seconds: 1772124465, nanoseconds: 0 } }" />` is rendered (`1772124465` seconds = `2026-02-26T16:47:45Z`, the same instant as the ISO scenario above)
- **THEN** the rendered date element contains a string formatted by `toLocaleDateString('zh-TW', ...)` for that date

##### Example: input shape coverage

| Input shape                                           | Resolved instant (UTC)                | Formatted as                          |
| ----------------------------------------------------- | ------------------------------------- | ------------------------------------- |
| `new Date('2026-02-27T00:47:45+08:00')`               | `2026-02-26T16:47:45Z`                | zh-TW long-form date string           |
| `'2026-02-27T00:47:45+08:00'`                         | `2026-02-26T16:47:45Z`                | zh-TW long-form date string           |
| `{ seconds: 1772124465, nanoseconds: 0 }`             | `2026-02-26T16:47:45Z`                | zh-TW long-form date string           |

---

### Requirement: PostList SHALL accept a posts array and provide search, sort, and view-mode controls

`PostList` SHALL declare a single required prop `posts: Post[]`. The local `Post` interface declared inside `PostList.vue` is structurally similar to the one in `PostCard` / `PostBlock` but adds **`categoryRootPath: string` as a required field**, because the category-grouping renderer reads it to build heading anchors. The local interface declares: `title: string` (required), `url: string` (required), `categoryRootPath: string` (required), `description?: string` (optional), `thumbnail?: string` (optional), `category?: string` (optional), and `createdTime: { seconds; nanoseconds } | string | Date` (required, three-shape union).

When the array is non-empty, the component SHALL render four controls:

1. A search input bound to internal state `searchQuery` (string, default empty).
2. A view-mode toggle that flips internal state `viewMode` between `'card'` and `'block'`. Default `'block'`.
3. A sort-axis toggle that flips internal state `sortBy` between `'time'` and `'category'`. Default `'time'`.
4. A sort-order toggle that flips internal state `sortOrder` between `'asc'` and `'desc'`. Default `'desc'`.

`PostList` SHALL NOT emit any events for state changes; all four controls operate on internal reactive state.

The empty-state and the controls bar SHALL both gate on `processedPosts.length` (the filtered, post-search array), not on the input `posts` prop. When `processedPosts.length === 0`:

- `PostList` SHALL render an empty-state placeholder whose visible text begins with `沒有任何文章，努力產生中！` (followed by a `<br />` and the kaomoji `((└(:3」┌)┘))`).
- `PostList` SHALL NOT render the controls bar.

This means a non-empty `posts` prop combined with a search query that filters to zero matches will *also* hide the controls bar — the user loses access to the search input until they remount or refresh. This is the source's actual behavior; downstream code MUST NOT assume the controls bar persists while a search query is active.

#### Scenario: Default state on first render

- **WHEN** `<PostList :posts="[postA, postB]" />` is mounted
- **THEN** the search input is empty
- **AND** posts render in `block` view mode
- **AND** posts render sorted by descending `createdTime` (newest first)

#### Scenario: Toggling view-mode swaps the renderer

- **WHEN** the view-mode button is clicked once from the default state
- **THEN** posts re-render using the `PostCard` component instead of `PostBlock`

#### Scenario: Empty posts array renders empty state and hides controls

- **WHEN** `<PostList :posts="[]" />` is mounted
- **THEN** the controls bar is NOT rendered
- **AND** the rendered output's text content begins with `沒有任何文章，努力產生中！`

#### Scenario: Search query that filters to zero matches also hides the controls bar

- **GIVEN** `<PostList :posts="[postA, postB]" />` with both posts having titles that do not contain the substring `"無此關鍵字"`, and `sortBy` at its default `'time'`
- **WHEN** the user types `"無此關鍵字"` into the search input
- **THEN** `processedPosts.length` becomes `0` (no title matches the query)
- **AND** the controls bar disappears (the user can no longer see or clear the search input via the rendered UI)
- **AND** the empty-state placeholder appears
- **AND** the only way to recover the controls bar is to remount the component (e.g., page reload or route change) — the source provides no in-component recovery path

---

### Requirement: PostList search SHALL filter by title in time mode and by title or category in category mode

When `sortBy === 'time'`, the search filter SHALL match against `post.title` only (case-insensitive substring match on the trimmed query). When `sortBy === 'category'`, the search filter SHALL match against `post.title` OR `post.category || '綜合'` (case-insensitive substring match on either field). An empty or whitespace-only search query SHALL match every post.

#### Scenario: Title-only search in time mode

- **WHEN** the user types `"safety"` while `sortBy === 'time'`
- **THEN** only posts whose `title` contains `"safety"` (case-insensitive) remain visible
- **AND** posts whose only match is in `category` are filtered out

#### Scenario: Title-or-category search in category mode

- **WHEN** the user types `"資安"` while `sortBy === 'category'`
- **THEN** posts with `category: "資安教學"` remain visible even if their title does not contain `"資安"`

##### Example: filter behavior across modes

| `sortBy`     | Query    | Post title       | Post category | Visible? |
| ------------ | -------- | ---------------- | ------------- | -------- |
| `'time'`     | `"safe"` | `"What is Safe"` | `"資安教學"`  | yes      |
| `'time'`     | `"資安"` | `"What is Safe"` | `"資安教學"`  | no       |
| `'category'` | `"資安"` | `"What is Safe"` | `"資安教學"`  | yes      |
| `'time'`     | `""`     | any              | any           | yes      |

---

### Requirement: PostList SHALL sort by time numerically and by category lexicographically with a newest-first tiebreaker

When `sortBy === 'time'`, posts SHALL be ordered by the numeric difference of their `createdTime` (using the same three input shapes as PostCard / PostBlock); the `sortOrder` toggle inverts the result.

When `sortBy === 'category'`, posts SHALL be ordered by `post.category || '綜合'` using `String#localeCompare`. When two posts share the same category, the tiebreaker SHALL place the newer post first (descending `createdTime`) regardless of the current `sortOrder`. Posts with different categories SHALL respect the `sortOrder` toggle.

#### Scenario: Time-descending order matches createdTime newest-first

- **WHEN** `sortBy === 'time'`, `sortOrder === 'desc'`, and posts have `createdTime` values 2026-03-01, 2026-02-15, 2026-01-20
- **THEN** posts render in order: 2026-03-01, 2026-02-15, 2026-01-20

#### Scenario: Category mode breaks ties by newest createdTime

- **WHEN** `sortBy === 'category'` and posts share `category: "資安教學"` with `createdTime` values 2026-03-01 and 2026-01-15
- **THEN** the 2026-03-01 post renders before the 2026-01-15 post within that category, regardless of `sortOrder`

##### Example: category-mode ordering

| Input posts (category, createdTime)                                                  | `sortOrder` | Output order (by createdTime within each category) |
| ------------------------------------------------------------------------------------ | ----------- | --------------------------------------------------- |
| `("研究方法教學", 2026-03-01)`, `("資安教學", 2026-02-27)`, `("資安教學", 2026-01-15)` | `'asc'`     | 研究方法教學 → 資安教學(2026-02-27) → 資安教學(2026-01-15) |
| same                                                                                 | `'desc'`    | 資安教學(2026-02-27) → 資安教學(2026-01-15) → 研究方法教學 |

---

### Requirement: PostList in category mode SHALL render posts grouped under category headers linking to categoryRootPath

When `sortBy === 'category'`, `PostList` SHALL render a heading per category. Each heading SHALL display the category name and SHALL link via an anchor to `group.categoryRootPath` (the `categoryRootPath` of the **first post** that established that group during the sort pass). Posts grouped under a heading SHALL be rendered with `showCategory="false"` (the heading already names the category). When `sortBy === 'time'`, posts SHALL be rendered in a flat list with `showCategory="true"`.

Groups SHALL be rendered in **first-encounter order** from the sorted `processedPosts` array — the source builds the groups via `Map<string, Group>` with `processedPosts.forEach`, and `Map` preserves insertion order. Implementations MUST NOT independently sort the group entries (e.g., via `Array.from(groups.entries()).sort(...)`); the cross-category ordering is determined entirely by the comparator's effect on `processedPosts` plus the `sortOrder` toggle.

#### Scenario: Category headings link to the category root

- **WHEN** `sortBy === 'category'` and a group's posts share `categoryRootPath: "/post/course/cybersec"`
- **THEN** the category heading renders an `<a href="/post/course/cybersec">` anchor wrapping the category name

#### Scenario: Grouped posts hide their inline category tag

- **WHEN** posts render under a category heading
- **THEN** the rendered `PostCard` / `PostBlock` instances do NOT display a category tag

#### Scenario: Flat view shows category tags inline

- **WHEN** `sortBy === 'time'`
- **THEN** every rendered `PostCard` / `PostBlock` displays its `post.category` as a tag (subject to the post having a non-empty category)

---

### Requirement: PostCard, PostBlock, PostList, and NewPost SHALL be globally registered by the theme

The custom theme entry at `docs/.vitepress/theme/index.ts` SHALL register `PostCard`, `PostBlock`, `PostList`, and `NewPost` as global Vue components inside the theme's `enhanceApp` hook so that markdown pages can use them as `<PostCard />`, `<PostBlock />`, `<PostList />`, and `<NewPost />` without per-page imports.

#### Scenario: Markdown page uses PostList without an explicit import

- **WHEN** a markdown file (e.g., `docs/posts.md`) renders `<PostList :posts="posts" />`
- **THEN** the component renders successfully without the page declaring an `import PostList from ...`

#### Scenario: Markdown page uses NewPost without an explicit import

- **WHEN** `docs/index.md` renders `<NewPost class="mt-8" :count="5" :showCategory="true" />`
- **THEN** the widget renders successfully without the page declaring an `import NewPost from ...`
