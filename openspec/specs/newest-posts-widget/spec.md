# newest-posts-widget Specification

## Purpose

Locks down the `<NewPost />` widget — the embeddable "newest posts" list used by the homepage and any markdown page that wants a curated feed — including its `count` (default `-1` = render all) and `showCategory` (default `false`) props, the strict `filter → sort → slice` pipeline order, and the `usePostSort` / `usePostFilter` composable contract. The composables export `sortPostsKey` and `filterPostsKey` `InjectionKey` symbols (typed `(a: Post, b: Post) => number` and `(post: Post) => boolean` respectively) so any consuming page can override either or both via Vue `provide()` without modifying the widget. Future changes to the widget's props, pipeline order, or the override contract SHALL propose a delta against this capability.

## Requirements

### Requirement: NewPost SHALL accept count and showCategory props with documented defaults

The `NewPost` component at `docs/.vitepress/theme/components/NewPost.vue` SHALL declare two props:

- `count?: number` — default `-1`. The sentinel `-1` SHALL mean "render every post that survives the filter and sort pipeline." Any non-negative integer `N` SHALL clamp the rendered output to at most `N` posts via `slice(0, N)`. Authors SHALL NOT pass any other negative integer (e.g., `-2`, `-100`); negative-but-not-`-1` values fall through to the source's `slice(0, props.count)` call, which then applies JavaScript's negative-index `slice` semantics (drops the last `|count|` posts) — this is undocumented, surprising, and SHALL be treated as out of contract. Tooling SHALL NOT pass non-integer numbers (e.g., `1.5`, `NaN`); behavior with non-integer numbers is undefined.
- `showCategory?: boolean` — default `false`. When `true`, every rendered child `PostBlock` SHALL display its category tag.

The component SHALL render each surviving post as a `PostBlock` exclusively (no `PostCard`, no view-mode toggle). The component SHALL NOT expose any other public props, slots, or events.

#### Scenario: Default count renders all posts

- **WHEN** `<NewPost />` is rendered
- **THEN** every post that survives the filter is rendered (no slice clamp applied)
- **AND** no category tags are rendered (showCategory defaults to `false`)

#### Scenario: Explicit count clamps the rendered output

- **WHEN** `<NewPost :count="3" />` is rendered against a post pool of size 10
- **THEN** at most three `PostBlock` instances are rendered

#### Scenario: showCategory flag propagates to children

- **WHEN** `<NewPost :count="5" :showCategory="true" />` is rendered
- **THEN** every child `PostBlock` displays its `post.category` tag

##### Example: count semantics

| `count` prop   | Source pool size | Rendered post count | Notes                                                                              |
| -------------- | ---------------- | -------------------- | ---------------------------------------------------------------------------------- |
| `-1` (default) | 10               | 10                   | Sentinel — slice skipped entirely.                                                 |
| `0`            | 10               | 0                    | Empty slice.                                                                       |
| `3`            | 10               | 3                    | Normal clamp.                                                                      |
| `100`          | 10               | 10                   | Clamp larger than pool — JS `slice` returns whole pool.                            |
| `5`            | 0                | 0                    | Empty pool — clamp is moot.                                                        |
| `-2`           | 10               | **8** (out of contract) | JS `slice(0, -2)` drops the last 2; surprising — authors SHALL NOT use this.       |

---
### Requirement: NewPost SHALL apply the pipeline filter then sort then slice in that exact order

The `newestPosts` computed property inside `NewPost` SHALL transform the imported `posts` array using exactly this pipeline, in this order:

1. Take a shallow clone via `[...posts]` so the imported array is never mutated.
2. Apply the predicate returned by `usePostFilter()` — this SHALL run before sorting so the sort comparator never sees filtered-out posts.
3. Apply the comparator returned by `usePostSort()`.
4. If `count !== -1`, apply `slice(0, count)`. Otherwise, return the sorted array unchanged.

The component SHALL NOT reorder these phases. The component SHALL NOT mutate the source `posts` array.

#### Scenario: Filter runs before sort

- **WHEN** the filter excludes posts whose category is `"draft"`
- **AND** the sort orders by `createdTime` descending
- **THEN** the rendered list contains only non-draft posts in newest-first order

#### Scenario: Slice is skipped when count is -1

- **WHEN** `count === -1` and the filtered+sorted array has length 7
- **THEN** the rendered array has length 7 (no slice applied)

#### Scenario: Source posts array is not mutated

- **WHEN** `<NewPost :count="3" />` renders against a 10-post source array
- **THEN** the imported `posts` array still has length 10 after rendering
- **AND** the imported array's element order is unchanged

---
### Requirement: usePostSort SHALL export sortPostsKey and default to descending createdTime

The composable at `docs/.vitepress/theme/composables/usePostSort.ts` SHALL export:

- A type alias `PostSortFn = (a: Post, b: Post) => number`.
- A `Symbol`-backed `InjectionKey<PostSortFn>` named `sortPostsKey`.
- A function `usePostSort(): PostSortFn` that returns `inject(sortPostsKey, defaultSort)`.

The default comparator (`defaultSort`) SHALL implement descending order by `createdTime`:

```ts
(a, b) => new Date(b.createdTime).getTime() - new Date(a.createdTime).getTime()
```

The default comparator MUST tolerate `createdTime` values that arrive as either `Date` instances or ISO-8601 strings (because JSON serialization can flatten Date to string).

#### Scenario: No provider yields the default newest-first order

- **WHEN** no parent component provides `sortPostsKey`
- **AND** posts have `createdTime` values 2026-03-01, 2026-02-15, 2026-01-20
- **THEN** `usePostSort()` returns a comparator that, when used to sort the array, yields the order 2026-03-01, 2026-02-15, 2026-01-20

#### Scenario: Custom provider replaces the default

- **WHEN** a parent calls `provide(sortPostsKey, (a, b) => a.title.localeCompare(b.title))`
- **THEN** `usePostSort()` returns the provided comparator
- **AND** posts are sorted alphabetically by title

---
### Requirement: usePostFilter SHALL export filterPostsKey and default to accept-all

The composable at `docs/.vitepress/theme/composables/usePostFilter.ts` SHALL export:

- A type alias `PostFilterFn = (post: Post) => boolean`.
- A `Symbol`-backed `InjectionKey<PostFilterFn>` named `filterPostsKey`.
- A function `usePostFilter(): PostFilterFn` that returns `inject(filterPostsKey, defaultFilter)`.

The default predicate (`defaultFilter`) SHALL be `() => true`, accepting every post.

#### Scenario: No provider yields the accept-all predicate

- **WHEN** no parent component provides `filterPostsKey`
- **THEN** `usePostFilter()` returns a predicate that returns `true` for every input post

#### Scenario: Custom provider replaces the default

- **WHEN** a parent calls `provide(filterPostsKey, post => post.category === "ctf")`
- **THEN** `usePostFilter()` returns the provided predicate
- **AND** only posts whose `category` equals `"ctf"` survive the filter phase inside `NewPost`

---
### Requirement: Consuming pages SHALL be able to override sort and filter independently via provide

Pages and parent components SHALL be able to override sort, filter, neither, or both by calling `provide(...)` on the respective `InjectionKey` symbols imported from `usePostSort` and `usePostFilter`. When only one key is provided, the other SHALL retain its default behavior. The injection contract MUST hold for any descendant that uses `<NewPost />`, regardless of nesting depth, as long as the provider is on the same component subtree.

#### Scenario: Page provides only sort

- **GIVEN** a markdown page with a `<script setup>` block that calls `provide(sortPostsKey, ascendingByCreatedTime)`
- **AND** the page does not provide `filterPostsKey`
- **WHEN** `<NewPost :count="5" />` renders inside that page
- **THEN** posts are sorted oldest-first
- **AND** every post survives the filter (default accept-all is used)

#### Scenario: Page provides only filter

- **GIVEN** a markdown page that calls `provide(filterPostsKey, post => post.category.startsWith("course"))`
- **AND** the page does not provide `sortPostsKey`
- **WHEN** `<NewPost :count="5" />` renders inside that page
- **THEN** only posts whose category starts with `"course"` survive
- **AND** the surviving posts are sorted newest-first (default sort is used)

#### Scenario: Page provides both sort and filter

- **GIVEN** a markdown page that calls both `provide(filterPostsKey, ...)` and `provide(sortPostsKey, ...)`
- **WHEN** `<NewPost :count="3" />` renders inside that page
- **THEN** filtering uses the provided predicate
- **AND** sorting uses the provided comparator
- **AND** the slice clamps the final result to at most three posts

#### Scenario: Page provides neither sort nor filter

- **GIVEN** a markdown page with no `provide()` calls for either key
- **WHEN** `<NewPost :count="5" />` renders inside that page
- **THEN** every post survives the default filter
- **AND** posts are sorted newest-first by `createdTime`
- **AND** the rendered list contains at most five posts

##### Example: provider combinations

| Provider on page                                   | Filter behavior                                | Sort behavior                       |
| -------------------------------------------------- | ---------------------------------------------- | ----------------------------------- |
| (none)                                             | accept all                                     | descending `createdTime`            |
| `sortPostsKey` only                                | accept all                                     | provided comparator                 |
| `filterPostsKey` only                              | provided predicate                             | descending `createdTime`            |
| both                                               | provided predicate                             | provided comparator                 |
