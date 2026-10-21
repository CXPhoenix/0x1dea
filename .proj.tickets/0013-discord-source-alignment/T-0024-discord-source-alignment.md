---
id: T-0024
title: Admit the exact published Discord source without changing historical contracts
epic: 0013-discord-source-alignment
status: review
blocked_by: []
---

## Context
The owner approved this one-ticket repair and D01-D06 on 2026-10-21. Main/staging already contain the exact Discord record; native reconciliation rejects the path outside M0. Spec and independent review are under .proj.specs/0013-discord-source-alignment/.

## Deliverable
Both current target guards accept the exact published record while tamper/unknown-source refusals and unchanged historical contracts retain their meaning.

## Acceptance criteria
- [x] AC1 / D01: exact record passes on main and staging, with correct role and publishable false.
- [x] AC2 / D02: missing/modified/newline/executable/link mutations fail.
- [x] AC3 / D03: unknown sources and candidate self-approval fail.
- [x] AC4 / D04: pre-publication inventory and ancestry failures retain fail-closed behavior.
- [x] AC5 / D05: original frozen modules and runner unchanged; original/current suites pass.
- [x] AC6 / D06: content/history identities preserved; actual current target checks pass.

## Approved test plan
D01-D06: ../../.proj.specs/0013-discord-source-alignment/test-plan.md. One public behavior and minimal implementation per red/green cycle.

## 給使用者（zh-TW）
讓現行 Harness 精確接受已發布的 Discord 驗證檔，保留原有凍結測試、歷史 assertions、runner、M0 與收據；其他額外或遭變造的來源仍須拒絕。

## Comments
Implementation starts in the isolated main-based checkout on tickets/T-0024/discord-source-alignment. Original staging checkout remains untouched. Status cannot become done without actual authorized landings and all acceptance evidence.

## Implementation checkpoint — 2026-10-21

Discord-specific behavior and preservation checks pass locally. Original #22/#32 contracts pass unchanged on both targets. Full current publication suites retain 4 failures and 1 error per role from a reproduced pre-existing T-0021 workflow fixture ref mismatch. AC5 remains incomplete; no delivery or done status. See ../../.proj.specs/0013-discord-source-alignment/implementation/T-0024/coverage.md. Narrow fixture-ref scope expansion is awaiting the owner; no approval is inferred.

## Approved fixture scope extension — 2026-10-21

The owner approved the exact additional live workflow fixture staging-ref alignment and full rerun. See fixture-ref-approval.md in the governing spec directory. This supersedes the earlier pending scope decision only; AC5 remains unchecked until actual successful checks. Historical contracts and all original assertions remain unchanged.

## Staging-ref extension checkpoint

Approved staging-ref setup is applied. Three focused workflow cases pass; head-reporting exposes its prepublication synthetic main versus actual staging record mismatch. See implementation/T-0024/fixture-ref-followup.md in the spec directory. The proposed main fixture alignment awaits separate scope approval; AC5 remains unchecked and no full-v4 success is claimed.

## Approved main fixture extension — 2026-10-21

The owner approved aligning the current main/staging fixture and completing tests. main-fixture-approval.md supplements original AC5 and fixture-ref-approval.md. Apply the captured setup-only patch; all prior pending statements are historical checkpoints. AC5 remains open until observed verification completes.

## Local acceptance — 2026-10-21

Owner-approved D01-D06 implemented and locally verified. See ../../.proj.specs/0013-discord-source-alignment/implementation/T-0024/coverage.md and the independent code/security review reports. Both current target overlays pass while original frozen contracts remain unchanged. This acceptance supersedes prior failed/pending checkpoints; both owner-approved fixture extensions and deterministic temporary JSON layout are implemented and verified. No actual repair landing has occurred; status remains review.

## Publication authority — 2026-10-21

The owner authorized commit, main publication and subsequent staging alignment while preserving historical contracts and candidates. See publication-approval.md in the governing spec directory. Earlier no-delivery statements are historical checkpoints. Status remains review until actual authorized landings and readbacks.
