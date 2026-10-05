# post-content-model Specification

## Purpose

Locks down the canonical post data model used by the 0x1DEA VitePress site: the `Post` TypeScript interface emitted by `docs/shared/posts.data.ts`, the `createContentLoader('post/**/*.md')`-based discovery pipeline, the frontmatter conventions for posts and `isIndex` category landing pages, the three-tier category resolution chain (frontmatter → same-directory `index.md` → URL-derived path), and the field-by-field fallback rules (including the deliberate `||` vs `??` asymmetry that preserves an explicit empty-string `description` but not an explicit empty-string `title`). Future changes that touch the loader, the post frontmatter format, or the category inheritance model SHALL propose a delta against this capability.

## Requirements

### Requirement: Post interface SHALL define eight required fields

The `Post` interface exported from `docs/shared/posts.data.ts` SHALL declare exactly the following eight fields, all required:

- `title: string`
- `url: string`
- `description: string`
- `createdTime: Date`
- `thumbnail: string`
- `category: string`
- `categoryFromPath: string`
- `categoryRootPath: string`

Consumers of the loader SHALL be able to import the `Post` type and rely on every listed field being present (non-optional) on every post returned by the loader.

The loader's `Post` is the canonical, narrowed shape produced by the VitePress data pipeline. Display components under `docs/.vitepress/theme/components/` (`PostCard`, `PostBlock`, `PostList`) redeclare a structurally **wider** `Post` interface locally — they mark `description`, `thumbnail`, and `category` as optional and accept `createdTime` as a union of `Date | string | { seconds: number; nanoseconds: number }`. That wider shape is the contract for the components and is captured in the `post-display-views` capability. Posts flowing from this loader satisfy both shapes; the wider local shape exists so the components remain usable for posts originating from other sources.

#### Scenario: Type import covers every documented field

- **WHEN** a Vue component imports `import type { Post } from '../../shared/posts.data'`
- **THEN** the imported type exposes `title`, `url`, `description`, `createdTime`, `thumbnail`, `category`, `categoryFromPath`, and `categoryRootPath`
- **AND** none of those eight fields is marked optional

#### Scenario: A loaded post has every field populated

- **WHEN** the loader emits an array element representing any post under `docs/post/**/*.md`
- **THEN** every one of the eight fields holds a value of the declared type
- **AND** no field is `undefined` or `null`

---
### Requirement: Loader SHALL discover posts via createContentLoader and exclude index pages

The loader at `docs/shared/posts.data.ts` SHALL discover posts by calling `createContentLoader('post/**/*.md', { includeSrc: true, render: false, excerpt: false })`. Files whose frontmatter contains a truthy `isIndex` field SHALL be excluded from the returned array. Files whose frontmatter omits `isIndex` (or sets it to a falsy value) SHALL be included.

#### Scenario: Regular post under docs/post/ is included

- **WHEN** the loader processes a file at `docs/post/<...>.md` whose frontmatter does not set `isIndex` (or sets it to `false`)
- **THEN** the file appears as a `Post` element in the returned array

#### Scenario: Category index page is excluded

- **WHEN** the loader processes a file at `docs/post/<segments>/index.md` whose frontmatter sets `isIndex: true`
- **THEN** the file does not appear in the returned array

##### Example: representative inclusion / exclusion

| File path                                          | Frontmatter `isIndex` | Included in loader output |
| -------------------------------------------------- | --------------------- | ------------------------- |
| `docs/post/course/cybersec/what-is-safety.md`      | (omitted)             | yes                       |
| `docs/post/course/cybersec/index.md`               | `true`                | no                        |
| `docs/post/course/rm/why-we-need-rm.md`            | (omitted)             | yes                       |
| `docs/post/course/rm/index.md`                     | `true`                | no                        |

---
### Requirement: Loader SHALL resolve category through a three-tier priority chain

For every included post, the loader SHALL set the `category` field by walking this priority chain in order, stopping at the first tier that yields a value:

1. `frontmatter.category` declared on the post itself, if it is truthy. (The source uses `||`, so an empty-string `category` falls through to tier 2.)
2. Otherwise, the category recorded in the **same-directory** `index.md` page's frontmatter. The match is an **exact-key lookup** in a map keyed by `categoryRootPath` — the loader does NOT walk up parent directories. A post at `docs/post/a/b/c/foo.md` (whose `categoryRootPath` is `/post/a/b/c`) inherits only from `docs/post/a/b/c/index.md`; it does NOT inherit from `docs/post/a/b/index.md`. The recorded value is returned even if it is an empty string, because the lookup is composed via `??` (coalescing only on `undefined`).
3. Otherwise, the output of `getCategoryFromUrl(url)`, which strips the `/post/` prefix and the file extension, then joins all path segments except the last with `/`. When the URL has fewer than two segments after stripping (top-level posts), this function returns the literal fallback `'綜合'`.

#### Scenario: Explicit frontmatter category wins

- **WHEN** a post under `docs/post/course/cybersec/foo.md` declares `category: "Custom"` in its frontmatter
- **AND** `docs/post/course/cybersec/index.md` declares `category: "資安教學"`
- **THEN** the loaded post's `category` is `"Custom"`

#### Scenario: Category inherited from same-directory index page

- **WHEN** a post under `docs/post/course/cybersec/foo.md` does not declare `category`
- **AND** `docs/post/course/cybersec/index.md` declares `isIndex: true` and `category: "資安教學"`
- **THEN** the loaded post's `category` is `"資安教學"`

#### Scenario: Deeper post does NOT inherit from a parent-directory index page

- **WHEN** a post lives at `docs/post/course/cybersec/sub/foo.md` and does not declare `category`
- **AND** `docs/post/course/cybersec/index.md` declares `isIndex: true` and `category: "資安教學"`
- **AND** there is no `docs/post/course/cybersec/sub/index.md`
- **THEN** the loaded post's `category` is the URL-derived string `"course/cybersec/sub"` (tier 3), NOT `"資安教學"`

#### Scenario: Category derived from URL when no same-directory index exists

- **WHEN** a post lives at `docs/post/tech/js/intro.md`
- **AND** there is no `docs/post/tech/js/index.md` declaring a category
- **AND** the post itself does not declare a category
- **THEN** the loaded post's `category` is `"tech/js"`

#### Scenario: Fallback to 綜合 for top-level posts

- **WHEN** a post lives directly at `docs/post/single.md`
- **AND** the post does not declare a category
- **AND** no same-directory `index.md` provides one
- **THEN** the loaded post's `category` is `"綜合"`

---
### Requirement: Loader SHALL always populate categoryFromPath and categoryRootPath from the URL

Independently of the `category` resolution chain, the loader SHALL set `categoryFromPath` to the result of `getCategoryFromUrl(post.url)` and `categoryRootPath` to the result of `getCategoryRootPath(post.url)` for every included post. These two fields MUST reflect the URL structure regardless of any frontmatter override applied to `category`.

#### Scenario: categoryFromPath ignores frontmatter override

- **WHEN** a post at `docs/post/course/cybersec/foo.md` declares `category: "Custom"` in its frontmatter
- **THEN** `category === "Custom"`
- **AND** `categoryFromPath === "course/cybersec"`
- **AND** `categoryRootPath === "/post/course/cybersec"` (the post URL with its filename segment removed; for index pages whose URL ends with `/`, the trailing-empty segment is dropped, producing the same key as sibling posts — this is what makes the same-directory inheritance lookup work)

##### Example: URL-derived fields for representative posts

| Post URL                                       | `categoryFromPath` | `categoryRootPath`        |
| ---------------------------------------------- | ------------------ | ------------------------- |
| `/post/course/cybersec/what-is-safety`         | `course/cybersec`  | `/post/course/cybersec`   |
| `/post/course/rm/why-we-need-rm`               | `course/rm`        | `/post/course/rm`         |
| `/post/single`                                 | `綜合`             | `/post`                   |

> **Note**: `categoryFromPath === '綜合'` for top-level posts is a *literal-string collision* with the tier-3 fallback, not a sentinel meaning "no path-derived category". Both fields produce `'綜合'` for top-level posts because `getCategoryFromUrl` returns that exact string when no path hierarchy exists.

---
### Requirement: Loader SHALL apply field fallbacks for missing frontmatter

For every included post, the loader SHALL apply the following fallbacks when the corresponding frontmatter field is missing or empty:

| Field         | JS Operator | Behavior on empty string `""`           | Behavior on YAML `null` / `~`           | Fallback                                                                                    |
| ------------- | ----------- | --------------------------------------- | --------------------------------------- | ------------------------------------------------------------------------------------------- |
| `title`       | **`\|\|`**   | falls through to fallback (`""` falsy)  | falls through (null is falsy)           | `'無標題'`                                                                                   |
| `description` | **`??`**    | **preserved** (`""` is non-nullish)     | falls through (null IS nullish)         | `'閱讀更多...'`                                                                              |
| `createdTime` | ternary `frontmatter.createdTime ? ... : ...` | falls through (`""` falsy)              | falls through (null falsy)              | Synthetic `Date.now() - idx * 86_400_000` ms (1 day per post-array-position, captured at loader-execution time) |
| `thumbnail`   | **`\|\|`**   | falls through to fallback               | falls through                           | `https://picsum.photos/seed/${idx + 1}/400/300`                                              |

The asymmetry between `||` (title, thumbnail, category-tier-1) and `??` (description, category-tier-2) is deliberate: only `description` preserves an explicit empty-string declaration. The asymmetry does NOT extend to `null`: every column above falls through on null, because both `||` and `??` short-circuit on null/undefined. Authors and tooling SHALL NOT rely on empty `title` or empty `thumbnail` propagating to the output — both are silently replaced by the fallback. Authors writing `description: null` or `description: ~` in YAML SHALL expect the `'閱讀更多...'` fallback, NOT the literal string `null`.

The synthetic `createdTime` fallback MUST decrement by exactly one calendar day per array position so that posts without explicit timestamps remain orderable. The synthetic value for array index `idx` is `Date.now() - idx * 86_400_000` ms, captured at the moment the loader runs.

#### Scenario: Post missing description, thumbnail, and createdTime

- **WHEN** a post declares only `title` in its frontmatter and ends up at array index `idx` in the transform pass
- **THEN** `description === '閱讀更多...'`
- **AND** `thumbnail` matches the regex `^https://picsum\.photos/seed/\d+/400/300$`
- **AND** `createdTime` is a `Date` instance whose value equals `Date.now() - idx * 86_400_000` ms captured at loader-execution time (so a post at `idx === 0` has a timestamp equal to the loader-execution moment, and a post at `idx === N` is `N` days older)

#### Scenario: Post explicitly sets description to an empty string

- **WHEN** a post declares `description: ""` in its frontmatter
- **THEN** the loaded post's `description` is the empty string `""`
- **AND** the fallback `'閱讀更多...'` is NOT applied

#### Scenario: Post explicitly sets description to YAML null

- **WHEN** a post declares `description: ~` (or equivalently `description: null`) in its frontmatter
- **THEN** the loaded post's `description` is `'閱讀更多...'` (the fallback IS applied, because `?? ` short-circuits on `null` exactly like on `undefined`)

---
### Requirement: Post frontmatter SHALL use ISO-8601 with +08:00 offset for createdTime

When a post declares `createdTime` in its frontmatter, the value SHALL be an ISO-8601 datetime string with the `+08:00` UTC offset. The loader SHALL pass that string directly to `new Date(...)`. Authors and tooling SHALL NOT use any other timezone offset, naive datetimes, or `Z`-suffixed UTC strings for new posts.

#### Scenario: Author writes a new post with a +08:00 timestamp

- **WHEN** the post frontmatter declares `createdTime: 2026-02-27T00:47:45+08:00`
- **THEN** the loader sets `createdTime` to a `Date` representing `2026-02-26T16:47:45Z` (the same instant in UTC)

##### Example: accepted vs. rejected frontmatter timestamps

| Frontmatter value                          | Status   | Reason                                       |
| ------------------------------------------ | -------- | -------------------------------------------- |
| `2026-02-27T00:47:45+08:00`                | accepted | ISO-8601 with explicit +08:00 offset         |
| `2026-03-01T18:33:16+08:00`                | accepted | ISO-8601 with explicit +08:00 offset         |
| `2026-02-27T00:47:45Z`                     | rejected | Wrong timezone (UTC); breaks Taiwan-local convention |
| `2026-02-27T00:47:45`                      | rejected | Naive datetime; ambiguous offset             |
| `2026/02/27 00:47:45`                      | rejected | Not ISO-8601                                 |

---
### Requirement: Index pages SHALL declare isIndex and provide an inheritable category

Every category landing page at `docs/post/<segments>/index.md` SHALL declare `isIndex: true` in its frontmatter, and SHALL declare a `category` string used as the inheritable category name for sibling posts. Index pages MUST NOT appear in the loader output. Posts under `docs/post/<segments>/` whose own frontmatter omits `category` SHALL inherit the index page's `category`.

#### Scenario: Index page provides category to siblings

- **WHEN** `docs/post/course/cybersec/index.md` declares `isIndex: true` and `category: "資安教學"`
- **AND** `docs/post/course/cybersec/what-is-safety.md` does not declare a `category`
- **THEN** the loaded `what-is-safety` post has `category: "資安教學"`
- **AND** the index page itself is absent from the loader output

#### Scenario: Index page without isIndex would be treated as a regular post

- **WHEN** an `index.md` file declares `category` but omits `isIndex`
- **THEN** the loader treats it as a regular post (it appears in the output and its category is NOT inherited by siblings)
