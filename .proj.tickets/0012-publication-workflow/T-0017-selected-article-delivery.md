---
id: T-0017
title: Deliver only the approved article and record publication/recovery states
epic: 0012-publication-workflow
status: todo
blocked_by: [T-0014, T-0016]
---

## Context

Approved epic 0012; owner confirmed all six slices, their blocking edges and the existing
24-row test allocation on 2026-10-11 (Asia/Taipei). English spec blob:
`a3f0c03754c389d40ca9fb97d8bb7c1ae992651b`. Reuse the reviewed spec/traceability and approved
test plan; do not alter historical assertions or published/candidate content implicitly.



**Why both edges:** Uses v2's exact candidate and the remote writer's shared serialization,
operation identity, trusted run/protection checks and ambiguous-outcome handling. Neither
candidate preparation alone nor a synchronization PR is the complete selected-delivery path.

## Deliverable
 An exact author approval produces a reviewable A-only main PR under
applicable commit/push/PR authority, with distinct readiness, observed landing and served
evidence. Candidate B survives subsequent synchronization. Revert/re-publication plans bind
current main and preserve unrelated publications.

## Acceptance criteria


- Bind approval to actual reviewed staging deployment and source/dependency/main/policy/tree;
  drift expires readiness and affected author approval.
- Observe one existing preview alias containing registered candidate pages/revisions and
  correct listing/navigation; unavailable evidence stays blocked rather than inferred.
- Verify the exact allowed main diff/build; use project message skills and only explicitly
  authorized remote actions. A PR is not merge/publication authority.
- Validate main-only delivery through disposable Git and expressly authorized test-repository
  exercise. Do not publish a real candidate or create a production PR merely to finish this
  implementation ticket; those require an exact later article request and authority.
- Observe actual authorized landing separately from production completion/HTTP/UI evidence;
  test receipts do not claim a live article was published. Verify protected latest-base and
  post-landing mismatches without trusting a head-only guard.
- Sync preserves other candidates/new revisions, retires only a landed candidate identity
  in a reviewed registry update, and prepares reviewed rollback/re-publication without reset.
  Later live production article evidence is recorded only when that operation is authorized;
  unavailable required live acceptance remains unverified, never fabricated as covered.

## Requirement and test mapping
 AC-08 integration and AC-09; P18/P19/P20; reuse P13–P17 at the integrated
boundary without duplicating already-proven unit assertions. P19's actual production portion
is conditional on separately authorized real publication, not a new release request here.

## Approved test plan

Allocated rows: P18, P19, P20. Shared rows cover only the slice-specific boundary, not duplicate tests.
Use public Git/CLI/native seams under the approved plan; remote/surface evidence remains
separately authorized and unavailable checks are never reported as passed.

## Delivery boundary

One canonical ticket branch. Main-first delivery and actual authorized staging ancestry
are required before done; PR-ready is insufficient. This instruction authorizes tracker
publication and starting T-0013 implementation only. No merge or deployment-setting changes.
No real article publication, credential installation or live automation activation is implied.

## 給使用者（zh-TW）

串起指定文章核准與 A-only main PR，分開記錄落地、部署及網站證據，保留其餘候選。

## Comments

Owner-approved breakdown/test allocation; implementation evidence will be appended here.
