# Proposed single ticket and test plan

Status: owner approved the single ticket and this table on 2026-10-11; see approval.md. No tests were written before approval. Round-2 clarifications use the same seams and scope.

One tracer-bullet ticket, T-0008: automatic image/table captions and references, the electricity article consumer, author guide and local verification. No blocking edges. This includes the entire demoable path rather than separate parser/CSS/article tickets.

| Seam | Test intent | Scope | Acceptance criterion | Boundary conditions |
|---|---|---|---|---|
| Existing VitePress Markdown renderer → HTML | Figure/table semantics, independent counters, meme exclusion, original alt | Opt-in blocks plus ordinary images/tables | C1–C2 | Multiple blocks; separate/reset counters; Markdown image title used once |
| Existing VitePress Markdown renderer → HTML | References follow IDs after insertion/reorder | Forward/backward and same renderer across documents | C3 | Chinese adjacency, `<small>`, table references, namespaced anchors |
| Existing VitePress Markdown renderer → HTML/error | Preserve literal contexts and caption safety; reject invalid input | Public Markdown authoring syntax | C4–C5, C9 | Code/escapes/links/attributes/images; HTML/Vue text, unsafe URLs; duplicate/unknown/wrong-kind/id/body/title/fence/anchor-collision errors; compile author guide examples |
| Task-entry source → migrated source/build | Exact article conversion and preserved owner WIP | Actual electricity article | C6 | All 8 alt/src pairs, original frontmatter/assets/prose and source links; no invented table |
| Served site → real browser | Responsive captions and native reference navigation | Article plus temporary table fixture; 1280px/390px light/dark | C7 | SSR, font ≥14px, contrast ≥4.5:1, no clipped text, visible keyboard focus/hash activation, client navigation; temporary fixture removed afterwards |
| Existing unit/lint/build/structure/materializer/adoption commands | Compatibility and accurate validation scope | Current installed toolchain | C8 | No install/publication/historical guard edits; report unrelated failures separately |
