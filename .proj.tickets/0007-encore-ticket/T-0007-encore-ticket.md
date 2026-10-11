---
id: T-0007
title: Reusable encore ticket and electricity article integration
epic: 0007-encore-ticket
status: review
blocked_by: []
---

## Context

The owner selected the D screening-ticket prototype and approved one tracer-bullet delivery and its test plan. Four-axis spec review has zero P0 after two rounds. Existing Vue, registration and article seams are already available.

## Deliverable

A reusable EncoreTicket accepts a title, href and optional description, appears at the electricity article's current recommendation, and opens the existing related article. Include a short author guide and actual browser verification.

## Acceptance criteria

- [x] E1: public props, independent instances, escaped plain text and optional description; two author examples.
- [x] E2: actual Markdown/SSR integration with intact next section.
- [x] E3/E4: D appearance in desktop/mobile and light/dark; keyboard/link semantics and actual navigation.
- [x] E5: task-entry article preserved except the exact recommendation paragraph; bounded source inventory.
- [ ] E6: product checks pass; preservation rejections accurately separated; no historical guard change or external publication.

## 給使用者（zh-TW）

將 D「加映票券」做成可在 Markdown 重複使用的元件，並只替換這篇文章的「同場加映」。保留原文案、推薦連結及你現有的圖說修改，驗證手機、深色與鍵盤操作。

## Comments

Approval and test seams: ../../.proj.specs/0007-encore-ticket/approval.md and test-plan.md. No commit, push or deployment requested. Status must remain review after local delivery until separately authorized landing.

Local UI delivery and independent code/security reviews are complete. E6 remains partial: standard full lint is unavailable due to the missing installed UnoCSS ESLint plugin; structure/materializer reject unrelated .DS_Store; baseline and authorized-delta preservation rejections are recorded separately. No historical verifier, dependency, or unrelated files were changed to bypass these limitations. See coverage-report.md and browser-evidence.md under the epic. No landing authorized or performed.

The owner subsequently authorized a scoped commit and non-force origin/staging push on 2026-10-11 after disclosure of the above limits. This supersedes earlier no-publication statements for the requested Git actions only. Existing caption WIP is excluded from the index. Status remains review while the disclosed E6 checks are unresolved; actual Git landing will be verified independently.

The owner subsequently authorized missing-tool restoration and required the normal hook. Frozen-lockfile restoration resolved full lint: pnpm lint, all 61 unit tests and VitePress build passed again, without manifest or lockfile changes. The earlier missing-plugin limitation is resolved; unrelated metadata and historical preservation limitations remain. See approval.md and coverage-report.md for the narrowed installation exception.
