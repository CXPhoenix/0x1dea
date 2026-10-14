---
id: T-0016
title: Turn main changes into one trusted staging synchronization PR
epic: 0012-publication-workflow
status: todo
blocked_by: [T-0015]
---

## Context

Approved epic 0012; owner confirmed all six slices, their blocking edges and the existing
24-row test allocation on 2026-10-11 (Asia/Taipei). English spec blob:
`a3f0c03754c389d40ca9fb97d8bb7c1ae992651b`. Reuse the reviewed spec/traceability and approved
test plan; do not alter historical assertions or published/candidate content implicitly.



## Deliverable
 A main event or explicit retry consumes local sync preparation, obtains
actual exact-input trusted validation and opens/updates at most one owned staging PR. Failure,
drift, conflict or uncertain API responses cannot silently write a target or duplicate a PR.

## Acceptance criteria


- Implement shared writer serialization and remote operation identity/readback used by
  synchronization and later selected-publication operations. Bound retries to three per run.
- Retain the approved permanent ticket-owned sync branch, update non-force and prove its
  result equals the independent merge; leave unrelated branches/PRs untouched.
- Approved canonical branch: tickets/T-0016/main-to-staging-sync. Initial implementation
  lands/reviews first; then the retained branch serves routine sync operations for this same
  permanent id. New features/conflict repairs use new ticket branches. No future operation
  reopens or repurposes the implementation ticket as new development.
- Explicit trusted validation dispatch requires an observed successful base/head/tree/policy
  run; no assumption that bot push/PR triggers all checks. Candidate builds receive no writer
  credentials or executable policy from article/API text.
- Verify actual permissions/dispatch/latest-base protections in a separately authorized
  disposable remote exercise before activation. Missing authority/capability stays blocked;
  no credential/repository-rule change, live activation or auto-merge is implied.

## Requirement and test mapping
 AC-03 target trust, AC-05/06/07 and remote AC-09 guards; P10–P13.

## Approved test plan

Allocated rows: P10, P11, P12, P13. Shared rows cover only the slice-specific boundary, not duplicate tests.
Use public Git/CLI/native seams under the approved plan; remote/surface evidence remains
separately authorized and unavailable checks are never reported as passed.

## Delivery boundary

One canonical ticket branch. Main-first delivery and actual authorized staging ancestry
are required before done; PR-ready is insufficient. This instruction authorizes tracker
publication and starting T-0013 implementation only. No merge or deployment-setting changes.
No real article publication, credential installation or live automation activation is implied.

## 給使用者（zh-TW）

串接可信檢查、自動同步 PR 與並行控制；沿用永久票分支，不自動 merge。

## Comments

Owner-approved breakdown/test allocation; implementation evidence will be appended here.
