# Automatic article captions and references

Version: 2. Owner confirmed the direction on 2026-10-11. Local delivery only.

## Problem Statement

Authors currently maintain image captions and every figure number manually. Meme images must remain unnumbered. Tables need the same authoring support without conflating image alternative text with a caption.

## Solution

Opt-in Markdown blocks produce semantic captions and per-article numbers at build time. Stable names resolve body references, including references before definitions. Apply this first to the three existing knowledge images in the electricity/privacy article; preserve its five other images, including the banner, and all image alt text.

## User Stories

1. As an author, I write a caption once and let the website number the figure or table.
2. As an author, I reference a stable name so moving or inserting a figure updates every reference.
3. As a reader, I can follow a numbered reference to its target and retain image alternative text.

## Implementation Decisions

- Extend the existing VitePress Markdown configuration; no new dependency or client-side counter. Produce complete SSR HTML, usable before hydration and after client navigation.
- Syntax: a `::: figure <id>` block contains exactly one standalone Markdown image with a nonempty quoted title. The image title is the caption; its alt remains independent. A `::: table <id> <caption>` block contains exactly one Markdown table. Each block closes with a standalone `:::`. IDs match `[a-z][a-z0-9-]*`. Numbered blocks may not nest; malformed opted-in blocks fail rendering.
- Only opted-in blocks count. Figure and table counters are separate, start at 1 for each Markdown document and follow document order. Ordinary images, raw HTML images and ordinary tables keep existing behavior. Other articles require no migration.
- Emit `<figure id="fig-<id>">` with `<figcaption>` below its image; emit an actual `<caption>` as the first child of the table, with `id="tbl-<id>"` on the table. Use labels `圖 N：` and `表 N：`. Caption content supports plain text, emphasis and ordinary Markdown links, including the article's existing source citations. Escape caption HTML and Vue interpolation rather than executing them; preserve normal link URL validation.
- Body references `@fig:<id>` and `@tbl:<id>` become native same-page links with the correct `圖 N`/`表 N` text, including forward references and references inside the existing inline `<small>` source note. Recognize IDs using the same ASCII grammar and consume no adjacent Chinese text. Do not transform code spans, fenced code, escaped markers, image alt/title, HTML attributes or existing link labels/destinations. Captions do not resolve reference markers. Duplicate IDs within a kind, unknown references, kind mismatches, missing captions, missing closing fences, invalid IDs/bodies and reserved-anchor collisions fail with a diagnostic containing the affected ID or block/reference text. Reusing an ID across figure/table kinds is valid because anchors are namespaced. The `fig-` and `tbl-` ID namespaces are reserved for this feature: reject collisions with static IDs in raw HTML or generated heading tokens. Dynamic IDs from author Vue code are out of scope; authors must not use reserved namespaces there.
- Keep citation links and source statements intact. Convert all hardcoded figure numbers in the target article, including its source note, to stable references. Preserve frontmatter bytes/times, assets, original alt strings and task-entry unrelated prose. The current article has no table; demonstrate table behavior through fixtures, not invented article content.
- Use scoped theme styles with readable captions, responsive images/tables and visible keyboard focus. No article-only inline sizing is required for the converted knowledge images. Document author syntax and validation diagnostics.

## Acceptance Criteria

- C1: Two opted-in figures render `圖 1` and `圖 2` with independent original alt/caption text and semantic figure markup; an intervening meme/raw image gets no caption or number.
- C2: Two opted-in tables render native captions `表 1` and `表 2`; an ordinary table remains unnumbered, and figure order does not affect table numbering.
- C3: Forward/backward references link to the correct namespaced targets, resolve in `<small>` text, and change correctly when definitions are reordered or inserted. Rendering another document with the same renderer restarts both counters.
- C4: Code, escaped markers, image alt/title, HTML attributes and existing link text/destinations remain literal; adjacent Chinese and punctuation remain intact. Caption links/emphasis remain usable; HTML/Vue-like caption text is literal and unsafe URL schemes do not become executable links.
- C5: Every invalid case listed above throws a diagnostic; valid normal Markdown outside these opt-in blocks still renders.
- C6: The electricity article renders exactly three numbered knowledge figures and six figure-reference links, with all eight original image alt/src pairs preserved, no literal authored `圖 N` references left and unchanged frontmatter/assets/unrelated prose. Existing source citations remain links.
- C7: The served article and table fixture work at 1280px and 390px, light/dark: caption computed font size at least 14px, text contrast at least 4.5:1 in each theme, no clipped caption text or page overflow, native reference links keyboard-focusable with a visible focus outline and activation updates the hash to the target. SSR contains captions/references; client navigation does not duplicate or lose them.
- C8: Existing unit/lint/build and project structure/materializer/adoption commands are executed using installed tools. Distinguish unrelated or historical preservation failures from regressions. No commit/push/deploy, dependency installation or historical guard modification.

- C9: The author guide includes copyable examples for a figure with independent alt/title, a meme, a captioned and ordinary table, forward/body references, source links, per-document numbering and diagnostics for invalid input. Guide examples compile through the same public renderer seam.

## Testing Decisions

Use the existing VitePress Markdown-renderer seam for compiled behavior and diagnostics, a source-preservation comparison against a task-entry snapshot, and the served site in a real browser for UI/navigation. Tests check output and observable errors, not plugin internals. Owner approval of the single-ticket test table is required before writing tests.

## Out of Scope

Bulk article migration, generated prose/image understanding, automatic classification of memes, cross-article references, lists of figures/tables, raw HTML figure/table conversion, nested numbered blocks and changes to writing-skill packages. Publication and landing require separate authorization.
