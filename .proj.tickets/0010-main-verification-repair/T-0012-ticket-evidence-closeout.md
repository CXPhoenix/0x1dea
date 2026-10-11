---
id: T-0012
title: Integrate evidence-backed ticket closeout with the exact main guard
epic: 0010-main-verification-repair
status: review
blocked_by: []
---

## Context
The owner requests current acceptance/landing audits and two unmerged closeout PRs. Original T1/T10 work has landed; a newly required exact T1 done/receipt successor needs its own unlanded tracking rather than silently extending an already-done ticket. Reuse the approved one-slice/no-dependency granularity and existing CLI/tracker/Git seams.

## Deliverable
Exact T1 original/done identities and pinned landing/approval receipts; six-ticket truthful audit plus T11 closeout in target-specific management projections. Preserve all candidate content and historical validation assertions.

## Acceptance criteria
C1-C4 in ticket-closeout/spec.en.md and traceability.md. Carry round1 Red-team P1: reject a different valid ancestor and unrelated regular approval. Public CLI red/green evidence resolves that risk.

## Approved test plan
Reused owner-approved verifier/real Git/tracker seams in ticket-closeout/test-plan.md. No new product interface or installation.

## 給使用者（zh-TW）
這張票只追蹤結案所需的精確 verifier 修正與證據交付。T-0001、T-0010 的原工作已落地，可依驗收紀錄結案；這次新 guard 修正仍待兩份 PR 合併，因此本票保持 review，不提前標記 done。四張缺證票維持 review，候選文章與歷史契約保留。

## Delivery boundary
Canonical branch tickets/T-0012/ticket-evidence-closeout targets main. Existing tickets/T-0011/main-to-staging-sync carries the staging projection, preserving one canonical branch per implementation ticket. Commit and non-force push/open PRs are authorized; merge/auto-merge/deploy are prohibited.

## Carried spec-review dispositions

Round2 P0=0 across all axes. The repeated stale branch-cell P1 is corrected in the test plan: T12→main, T11→staging. Completeness mappings explicitly cover T12 review status and exact receipt/approval identities under C1/C2/C4. No third adversarial round or new seam. Final implementation review must confirm both corrections; T12 cannot be done before actual landing.

## Implementation evidence

Coverage: .proj.specs/0010-main-verification-repair/ticket-closeout/coverage-report.md (repository-relative). Independent Standards/Spec report: ticket-closeout/review/code-final.md; security report: ticket-closeout/review/security-final.md. The C3 SOURCE=staging fixture P1 is reproduced and resolved in branch-reproduction-red/green.txt. These paths are relative to the epic under .proj.specs unless stated otherwise. T12 remains review pending actual landing.
