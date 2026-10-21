---
id: T-0006
title: Accept exact electricity article revision and verify staging preview
epic: 0006-article-electricity-revision
status: done
landing_evidence: .proj.specs/0006-article-electricity-revision/closeout-20261021/landing.json
blocked_by: []
---

## Context
Owner-approved revised article and two images need an exact successor. Existing merged components are dependencies already present in staging.

## Deliverable
One bounded end-to-end revision: required CLI accepts exact approved sources, rejects tampering, and authorized staging preview shows the new article.

## Acceptance criteria
- [x] A1/A2: exact overlay accepted; source drift and unknown inputs rejected.
- [x] A3: immutable history and pinned provenance preserved.
- [x] A4: full required checks and independent review pass.
- [x] A5: actual staging landing and exact-SHA preview verified.

## 給使用者（zh-TW）
只讓新版文章與兩張梗圖通過精確檢查，保留舊紀錄與防竄改規則；通過測試和審查後推 staging，驗證本次公開預覽。

## Comments
Owner explicitly authorized this bounded guard modification and staging push. Existing public CLI seam and single ticket follow the reviewed proposal. No blockers: prerequisite component commits are already merged on staging; their older tracker review state is not fabricated as done. No main or external-index changes.

External index: [0X1DEA #20](https://app.notion.com/p/3f684910704181c98429ed0bed3afced), maintained by parent; local permanent ID is T-0006.

Actual pre-publication checks and review: [coverage report](../../.proj.specs/0006-article-electricity-revision/coverage-report.md); A5 awaits actual remote/deployment evidence.


## Current closeout — 2026-10-21

The owner requested closure after actual staging landing. Current A1–A5 acceptance and retained limits are in [closeout-20261021/coverage-report.md](../../.proj.specs/0006-article-electricity-revision/closeout-20261021/coverage-report.md); [actual landing](../../.proj.specs/0006-article-electricity-revision/closeout-20261021/landing.json). This dated entry supersedes the earlier review/no-landing or missing-current-evidence comments only. It does not backdate gates, remove historical failures, publish candidate articles or claim the latest metadata-only Git head was deployed.
