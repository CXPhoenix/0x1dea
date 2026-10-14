---
id: T-0014
title: Prepare and verify one article through the explicit v2 contract
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
 From current main and the reviewed registry, the local CLI prepares a
candidate containing exactly A plus approved dependencies, even when clean A already appears
in staging. It verifies provenance, full tree and build/output evidence; B's unapproved
content is excluded while B's existing published baseline remains. No remote mutation.

## Acceptance criteria


- Publish actual v2 entry points/help/schema; preserve all v1 behavior and fixtures.
- Validate complete registry/ownership and every non-main commit; reject integration ancestry,
  B add/revert history, missing candidates/history, unknown commits and stale pins.
- Accept legacy reconstruction only with explicit original/new provenance and owner approval;
  implementing this gate does not migrate every real candidate or authorize source rewriting.
- Reconstruct exact modes/blobs/diff and retain allowed aliases; reject escaping reads,
  executable imports, new links/submodules and tampering.
- Use the existing isolated build contract and separate actual build/output receipts;
  failed/missing/blocked/exclusion-unverified required evidence prevents v2 PR-ready.

## Requirement and test mapping
 AC-03/04/08 and local AC-09 binding; P04–P08, P14–P17.

## Approved test plan

Allocated rows: P04, P05, P06, P07, P08, P14, P15, P16, P17. Shared rows cover only the slice-specific boundary, not duplicate tests.
Use public Git/CLI/native seams under the approved plan; remote/surface evidence remains
separately authorized and unavailable checks are never reported as passed.

## Delivery boundary

One canonical ticket branch. Main-first delivery and actual authorized staging ancestry
are required before done; PR-ready is insufficient. This instruction authorizes tracker
publication and starting T-0013 implementation only. No merge or deployment-setting changes.
No real article publication, credential installation or live automation activation is implied.

## 給使用者（zh-TW）

新增明確 v2 來源准入與單篇候選驗證，保留 v1；只產出本機候選，不做遠端發布。

## Comments

Owner-approved breakdown/test allocation; implementation evidence will be appended here.
