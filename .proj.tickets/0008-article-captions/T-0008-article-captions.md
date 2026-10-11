---
id: T-0008
title: Automatic article figure and table captions with stable references
epic: 0008-article-captions
status: review
blocked_by: []
---

## Context

The owner approved the direction, one ticket and test plan on 2026-10-11. Four independent spec axes passed round 2 with zero findings. Existing Markdown-renderer and browser seams are available.

## Deliverable

Build-time opt-in image/table captions, separate per-document counters and stable body references. Convert only three knowledge figures and six body/source-note references in the electricity/privacy article. Preserve original alt, memes, banner, frontmatter and current article WIP. Include author examples and actual local verification.

## Acceptance criteria

- [x] C1–C2: numbered semantic figures/tables; ordinary media excluded; original alt and separate counters.
- [x] C3: stable forward/backward references, insertion/reorder updates and document reset.
- [x] C4–C5: literal contexts, safe captions/source links, invalid-input/anchor diagnostics.
- [x] C6: bounded article conversion with original eight image alt/src pairs and six references.
- [x] C7: SSR plus actual responsive/light/dark/keyboard/client-navigation verification.
- [x] C8: existing checks executed and limitations accurately reported.
- [x] C9: copyable verified author guide.

## 給使用者（zh-TW）

圖片與表格只寫一次 caption，網站自動編號；正文用固定名稱引用，插圖或換序時一起更新。先套用到用電文章的三張知識圖，保留所有 alt、meme、橫幅與既有內文。表格功能另以範例驗證，不新增文章內容。

## Comments

Spec/traceability/approved test table and two review rounds: .proj.specs/0008-article-captions/. Local work only; no commit/push/deploy/install or historical guard changes. Keep status review after local delivery until authorized landing actually occurs.

Local implementation and C1–C9 verification complete. See coverage-report.md, browser-evidence.md and review/code-T-0008.md / review/security-T-0008.md in the epic. 25 new tests, 86 full-suite tests, full lint and final VitePress build passed. Structure/materializer baseline metadata failures and final immutable-history adoption rejection are disclosed, not bypassed. No commit/push/landing performed; status remains review.
