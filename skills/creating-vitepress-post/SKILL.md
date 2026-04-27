---
name: creating-vitepress-post
description: "Use when the user wants to create a new article on the 0x1DEA VitePress site (e.g. \"新增文章\", \"新文章\", \"寫一篇\", \"建立文章\", \"create post\", \"add blog post\", \"write article\", \"scaffold article\"). Always invoke `pnpm new:post` for these — never hand-author the markdown file. Triggers on mentions of docs/post, \"VitePress post\", or pnpm new:post."
license: MIT
compatibility: Requires the project npm script `pnpm new:post` (defined in package.json) and `tsx`.
metadata:
  author: 0x1DEA
  version: "1.0"
  scope: project
---

# Creating a VitePress Post

## Overview

This project ships a helper at `scripts/vpHelper.ts`, exposed through the npm script `pnpm new:post`. It scaffolds a new VitePress article with project-standard frontmatter AND its matching public-assets folder. Always use this script — never hand-author the markdown file with a generic write tool. The script is the single source of truth for:

- the frontmatter contract (`title`, `description`, `createdTime`, `thumbnail`)
- the UTC+8 ISO-8601 `createdTime` timestamp (e.g. `2026-04-27T20:15:42+08:00`)
- the assets folder name derived from the post path
- conflict detection (the script refuses to overwrite an existing file)

## When to Use

Triggers — invoke this skill if the user says any of:

- 中文：「新增文章」、「新文章」、「建立文章」、「寫一篇」、「補一篇」、「我想寫一篇關於 X 的文章」
- 英文："create post", "add blog post", "write article", "scaffold article", "new VitePress post"
- 引用了 `docs/post`、`pnpm new:post`、或 0x1DEA 的文章命名規則

When NOT to use:

- Editing or rewriting an EXISTING `.md` file under `docs/post/` → use Read/Edit on that file
- Creating a non-post page (landing page, custom Vue page, sidebar config) → those live elsewhere in `docs/`
- Generating a draft outline that the user does not yet want as a real file → keep it inline in the conversation

## Quick Reference

> Each invocation creates BOTH the `.md` file AND its matching `docs/public/assets/...` folder. Do not create the assets folder yourself.

| Goal | Command |
|------|---------|
| Post in the default folder `docs/post/` | `pnpm new:post "Post Title"` |
| Post under a category `docs/post/<category>/` | `pnpm new:post "Post Title" -c <category>` |
| Post in an arbitrary directory | `pnpm new:post "Post Title" -d <relative/path>` |

**Flag rules:**

- `-c` and `-d` are **mutually exclusive**. Passing both throws `參數 -c 與 -d 不能同時使用。` (from `scripts/vpHelper.ts:47/60`).
- `-c <category>` takes a **bare category name** (e.g. `course/intro`) — do NOT prefix it with `docs/` or `docs/post/`. The script appends it under `docs/post/`. Anti-example: `-c docs/post/intro` produces `docs/post/docs/post/intro/...md`.
- `-d <path>` takes a **project-root-relative path** (e.g. `docs/post/special` or `docs/drafts`). Anti-example: `-d intro` resolves under the current working directory and lands the post outside `docs/`. Always prefix with `docs/...` unless you really mean to write elsewhere.
- The script does NOT validate that `-c` / `-d` keep the post inside `docs/`. Callers are responsible for sane paths. Reject titles or values that begin with `-` (the parser will misread them as flags) and reject `-d` values containing `..` segments.

## Constraints

- **Title vs filename.** The CLI argument is the *human-readable* title.
  - Title goes into the frontmatter `title:` and the H1, with the **first letter of each ASCII word upper-cased; all other letters preserved as-is** (regex `\b\w/g`). So `"my new post"` → `My New Post`, but `"vitepress TIPS"` → `Vitepress TIPS` (acronyms are not lowered). Pass brand names with intended casing (`VitePress`, not `vitepress`).
  - The title is **NOT trimmed**, so leading/trailing spaces leak into `title:`. The filename is trimmed and has whitespace replaced by `_` (`my_new_post.md`).
  - **CJK / unicode titles** (e.g. `"你好世界"`) pass through unchanged because the case regex is ASCII-only. Filename keeps the unicode characters; some tools may dislike non-ASCII filenames — prefer ASCII titles when possible.
  - **Empty title** errors out with `錯誤: 請輸入文章名稱 (post_name)。`. Always supply a title.
- **Default directory** is `docs/post`.
- **Conflict detection.** If the target `.md` file already exists, the script aborts with a yellow warning and exits 1. Pick a new title or delete the existing file first.
- **Assets folder** is created automatically; do not pre-create it.

## Step-by-Step

1. **Decide the directory.** If the user mentions a category (e.g. "course/intro"), use `-c course/intro`. For paths outside `docs/post/`, use `-d <relative-path>`. If unclear, ask.
2. **Run the script.**
   ```bash
   pnpm new:post "Post Title" -c <category>
   ```
3. **Read the output.** The script prints three lines:
   - `📄 文章: <abs path to .md>`
   - `🖼️  資源: <abs path to assets folder>`
   - `📅 時間: <UTC+8 ISO-8601 timestamp>`
4. **Drop images** into the assets folder shown in step 3. The image reference path **MUST** start with a leading `/`:

   ```md
   DO:    ![alt](/assets/post_course_intro_hello_world/diagram.png)
   DON'T: ![alt](./assets/...)              # breaks: relative to .md file
   DON'T: ![alt](docs/public/assets/...)    # breaks: never include docs/public/ prefix
   ```

   `docs/public/` is the VitePress public root, so `/assets/...` is the correct absolute reference at build time.
5. **Edit the markdown** to fill `description:` and `thumbnail:` (both start empty) and write the body. Do **not** rewrite `createdTime:` once it's set — downstream RSS / sort order / archive flows depend on it being immutable.

## Generated File Layout

For `pnpm new:post "Hello World" -c course/intro` from the project root:

```
docs/post/course/intro/hello_world.md                 ← the article
docs/public/assets/post_course_intro_hello_world/     ← matching assets folder
```

The markdown body starts as:

```markdown
---
title: Hello World
description:
createdTime: 2026-04-27T20:15:42+08:00
thumbnail:
---

# Hello World
```

### Assets folder naming rule

For a post at `docs/post/<segments>/<file>.md`, the assets folder is `docs/public/assets/<segments_joined_with_underscore>_<safe_filename>/`. Special case: a post **directly under `docs/`** (no intermediate folder, e.g. `docs/<file>.md`) resolves to `docs/public/assets/root_<safe_filename>/`.

| Post path | Resulting assets folder |
| --------- | ----------------------- |
| `docs/post/hello_world.md` | `docs/public/assets/post_hello_world/` |
| `docs/post/course/intro/hello_world.md` | `docs/public/assets/post_course_intro_hello_world/` |
| `docs/intro.md` | `docs/public/assets/root_intro/` |

**Implementation note** (`getAssetFolderName` at `scripts/vpHelper.ts:99`): the algorithm always strips the **first** path segment of the post's location relative to project root — *not literally `docs/`*. For posts under the standard `docs/...` tree this happens to match. Using `-d` with a non-`docs/` path (e.g. `-d notes/foo`) produces an asset folder name that drops `notes/` rather than preserving it. **Trust the script's `🖼️` output line over deriving the name yourself.**

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Hand-creating the `.md` file with a write tool to "save time" | Use `pnpm new:post`. The frontmatter contract, UTC+8 timestamp, and assets folder name are only guaranteed when the script runs. |
| Passing both `-c` and `-d` | Mutually exclusive — pick one. The script throws `參數 -c 與 -d 不能同時使用。` |
| Using `npm run new:post` or `npx tsx scripts/vpHelper.ts new post ...` directly | Project pins `pnpm@10.28.0` (`packageManager` field). Always invoke as `pnpm new:post`. |
| Putting images next to the markdown (e.g. inside `docs/post/...`) | Images go in `docs/public/assets/<asset-folder-name>/` and are referenced via `/assets/...` because `docs/public/` is VitePress's public root. |
| Re-running the script for an existing post | The script aborts with `警告: 檔案 "<name>.md" 已經存在` and exits 1. Choose a different title or delete the old file first. |
| Treating the title as the filename | The title is title-cased (first letter of each ASCII word upper-cased; rest preserved). The filename replaces whitespace with `_`. Don't pass `"my_new_post"` when the user wrote `"My New Post"` — let the script derive both. |
| Prefixing `-c` with `docs/` or `docs/post/` | `-c` takes a bare category (e.g. `course/intro`). `-c docs/post/intro` produces a duplicated `docs/post/docs/post/intro/` path. |
| Forgetting to fill `description:` and `thumbnail:` | The script writes them empty intentionally. They must be filled before the post is considered complete. |

## Reference Implementation

Source: `scripts/vpHelper.ts`. The skill describes contracts only; do not duplicate the implementation.

| Function | Location | Contract |
|----------|----------|----------|
| `parseArgs` | `scripts/vpHelper.ts:28` | CLI parser. Enforces `-c`/`-d` exclusivity. Default dir = `docs/post`. |
| `getFormattedDate` | `scripts/vpHelper.ts:85` | Returns ISO-8601 string offset to UTC+8 (`...+08:00`, never `Z`). |
| `getAssetFolderName` | `scripts/vpHelper.ts:99` | Drops the first path segment (assumed to be `docs/`), joins remainder with `_`, appends `_<safe_filename>`. Returns `root_<safe_filename>` when the post sits directly under that first segment. |
| `main` | `scripts/vpHelper.ts:123` | Validates command (`new post`), checks file conflict, writes markdown with frontmatter template, creates assets dir, prints three status lines. |

## Verification After Use

After running the script, confirm:

1. The three status lines printed (`📄`, `🖼️`, `📅`).
2. The `.md` file exists at the path shown.
3. The assets folder exists at the path shown.
4. The frontmatter `createdTime` ends with `+08:00`.

Before declaring the post finished, also confirm:

5. `description:` is filled (not blank).
6. `thumbnail:` is filled (not blank) — point it at a path under the assets folder.
7. The body has been written beyond the auto-generated `# <Title>` heading.

If any check fails, do not proceed to publish — investigate the cause first.
