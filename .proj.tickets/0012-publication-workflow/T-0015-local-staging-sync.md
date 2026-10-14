---
id: T-0015
title: Prepare a verified main-to-staging synchronization locally
epic: 0012-publication-workflow
status: todo
blocked_by: [T-0013]
---

## Context

Approved epic 0012; owner confirmed all six slices, their blocking edges and the existing
24-row test allocation on 2026-10-11 (Asia/Taipei). English spec blob:
`a3f0c03754c389d40ca9fb97d8bb7c1ae992651b`. Reuse the reviewed spec/traceability and approved
test plan; do not alter historical assertions or published/candidate content implicitly.



## Deliverable
 Given current main/staging and trusted candidate inventory, produce an
independently computed, validated sync result and receipt, or an exact no-op/conflict/failure
report, without changing source/target refs. A maintainer can inspect the result before any
GitHub integration exists.

## Acceptance criteria


- Read current pins, compute the independent merge and validate the trusted staging role.
- Already-contained main is no-op; any conflict/check/ref drift blocks the result.
- Compare all pending candidate modes/blobs/metadata with the pinned registry, including
  conflict-free edits to different paragraphs of one published article; changed candidates
  need explicit source/registry/affected author-approval updates before retry.
- Expose supported operation/help/schema and a pinned result consumed by later automation;
  do not create a remote branch, PR or merge.

## Requirement and test mapping
 AC-05 and local AC-06 drift; P09, local ref-drift subset of P10.

## Approved test plan

Allocated rows: P09, P10. Shared rows cover only the slice-specific boundary, not duplicate tests.
Use public Git/CLI/native seams under the approved plan; remote/surface evidence remains
separately authorized and unavailable checks are never reported as passed.

## Delivery boundary

One canonical ticket branch. Main-first delivery and actual authorized staging ancestry
are required before done; PR-ready is insufficient. This instruction authorizes tracker
publication and starting T-0013 implementation only. No merge or deployment-setting changes.
No real article publication, credential installation or live automation activation is implied.

## 給使用者（zh-TW）

在本機計算與驗證 main→staging 同步，遇衝突、候選變動或漂移停止，不改遠端。

## Comments

Owner-approved breakdown/test allocation; implementation evidence will be appended here.
