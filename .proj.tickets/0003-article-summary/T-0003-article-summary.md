---
id: T-0003
title: Native Markdown summaries with three appearances
epic: 0003-article-summary
status: review
blocked_by: [T-0005]
---


## Context

A new summary component needs one shared native-slot contract and three small appearances. Spec review, ticket breakdown and test plan are approved; implementation starts on this permanent ticket branch.

## Deliverable

An author can use ArticleSummary directly in Markdown, select note/cards/terminal, and show the same three authored takeaways on a built, accessible article page. One writer owns shared registration and component styles.

## Acceptance criteria

- [ ] S1–S3: all three appearances and fallback render the canonical list and richer Markdown without custom containers, content loss or boundary capture.
- [ ] S4–S7: actual built SSR page and hydrated browser pass navigation, mobile, light/dark, keyboard/accessibility and print checks.
- [ ] S8: no arbitrary HTML parser or unrelated article/banner changes; usage guidance and one approved consumer are demoable.
- [ ] Approved plan is followed with actual red/green and a coverage report; code/security/surface gates pass before authorized landing.

## 給使用者（zh-TW）

一張票交付 A 淡色便條、B 三張 icon 卡片、C 深色終端三行，文字由作者在 Markdown 自行提供。三種共用原生 slot，不重複文章文案。做完可以在實際頁面看三種外觀、手機直排、深色與列印效果。

## Comments

External index: 0X1DEA #17 (external index maintained privately). Parent verified creation and readback; external status is processing. Repository status and blocking edges remain authoritative.

Blocked by: T-0005 (owner-approved required preservation gate reconciliation); prior no-edge statement predates the correction; authorized implementation may start. Separate tickets for CSS, registration and tests would be horizontal slices. If later evidence justifies splitting note first and cards/terminal after, revise and obtain approval before publishing edges.

Approval: ../../.proj.specs/0003-article-summary/approval.md. No landing authorized; status cannot become done.

## Local verification evidence

See coverage-report.md under the epic, maintenance/component-delivery/TDD.md and scope.md. Local behavior verified; existing harness verifier config hash mismatch reproduced on pristine baseline. Actual deployment/landing not performed.
