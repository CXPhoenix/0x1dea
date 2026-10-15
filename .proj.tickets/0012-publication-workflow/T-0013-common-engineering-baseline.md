---
id: T-0013
title: Establish the common engineering baseline and M0 inventory
epic: 0012-publication-workflow
status: done
landing_evidence: .proj.specs/0012-publication-workflow/implementation/T-0013-landing/landing.json
blocked_by: []
---

## Context

Approved epic 0012; owner confirmed all six slices, their blocking edges and the existing
24-row test allocation on 2026-10-11 (Asia/Taipei). English spec blob:
`a3f0c03754c389d40ca9fb97d8bb7c1ae992651b`. Reuse the reviewed spec/traceability and approved
test plan; do not alter historical assertions or published/candidate content implicitly.



## Deliverable
 A complete reviewed two-tree inventory and an engineering-only main
baseline, integrated back into staging while retaining every unapproved article/revision,
asset, metadata and URL. Reviewers can verify the exact main diff and candidate preservation
without implementing the same engineering fix twice. This is the necessary prefactoring
and migration slice, with observable validator and tree results.

## Acceptance criteria


- Account for every delta with full commits, modes/blob hashes, ownership/shared patches,
  historical/current management classification and trusted target-role policy.
- Obtain owner approval of M0 before using it as policy; legacy contaminated candidates are
  recorded as requiring reviewed migration, never mislabeled clean.
- Exclude all unapproved publication content from main; preserve staging candidates and
  historical assertions with only explicit reviewed successors for current behavior.
- Adopt the approved main-first/operational-branch ADR clarification without changing old
  ADR-0006 evidence or done meaning; record real prerequisite and main/staging landing states.

## Requirement and test mapping
 AC-01/02/03 and AC-10 tracker boundary; P01/P02/P03, relevant P23 cases.

## Approved test plan

Allocated rows: P01, P02, P03, P23. Shared rows cover only the slice-specific boundary, not duplicate tests.
Use public Git/CLI/native seams under the approved plan; remote/surface evidence remains
separately authorized and unavailable checks are never reported as passed.

## Delivery boundary

One canonical ticket branch. Main-first delivery and actual authorized staging ancestry
are required before done; PR-ready is insufficient. This instruction authorizes tracker
publication and starting T-0013 implementation only. No merge or deployment-setting changes.
No real article publication, credential installation or live automation activation is implied.

## 給使用者（zh-TW）

盤點並建立共同工程基底，main 排除候選，staging 保留文章與修訂；歷史契約不改寫。

## Comments

Owner-approved breakdown/test allocation; implementation evidence will be appended here.

### 2026-10-11 implementation checkpoint

Implementation branch: `tickets/T-0013/common-engineering-baseline`, isolated checkout
`/private/tmp/0x1dea-T0013`, based on actual main
`eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a`. Pinned staging:
`c6efa7ded4731cbe251bdbc6fea5615e7e7b11b7`.

Read-only inventory CLI implemented through eight red/green cycles; six candidate units
and 50 owned paths, 363 deltas and complete main/staging trees recorded as an untrusted
proposal. PR20/21 are OPEN, not landed. See
[checkpoint](../../.proj.specs/0012-publication-workflow/implementation/T-0013/README.md),
[concrete M0](../../.proj.specs/0012-publication-workflow/implementation/T-0013/M0-review.md)
and [coverage](../../.proj.specs/0012-publication-workflow/implementation/T-0013/coverage.md).

Historical suites pass (66 + 16 unchanged cases); eight new CLI cases and 54 Vitest tests
pass, local build/structure/materialization pass. Direct adoption validation remains failed
on the new CLI source, as required until an exact current successor is reviewed. T13 remains
processing; concrete M0 approval, baseline/current successor, integration and real authorized
landing evidence are still required. No merge, deployment change, commit, push or PR.

Independent checkpoint review: Standards' README-language P2 resolved; Standards and Spec
remaining P0/P1/P2 = 0/0/0 each. Security found no qualifying HIGH/MEDIUM candidates. This is
not whole-ticket acceptance; see
[code review](../../.proj.specs/0012-publication-workflow/review/code-T-0013-inventory.md) and
[security review](../../.proj.specs/0012-publication-workflow/review/security-T-0013.md).

### 2026-10-14 approved M0 continuation

Concrete M0 approved by owner; remote pins unchanged, prerequisite PR20/21 still OPEN.
Common main/staging engineering projections implemented with one shared exact current
validator and unchanged hash-pinned historical main/staging validators. Native main suites:
66 harness + 34 publication + 54 Vitest; staging: 95 harness + 34 publication + 87 Vitest.
Both builds/lint/structure/materializer and current adoption checks pass. Only the existing
validator entrypoint changes in either target tree; candidate paths and published bytes remain
unchanged. No merge or deployment settings modified. Status review, never done until actual
authorized landing. Review/coverage evidence: ../../.proj.specs/0012-publication-workflow/implementation/T-0013-current/.

Independent Standards/Spec remaining P0/P1/P2 = 0/0/0 each; security found no qualifying
HIGH/MEDIUM candidates. CLI documentation followup confirmed by both code reviewers.
See [current code review](../../.proj.specs/0012-publication-workflow/review/code-T-0013-current.md)
and [current security review](../../.proj.specs/0012-publication-workflow/review/security-T-0013-current.md).
Actual landing remains pending; downstream statuses/dependencies are unchanged.

### 2026-10-14 authorized main PR delivery

Owner authorized commit, non-force ticket-branch push and main PR only, with no merge or
deployment-setting changes. Fresh remote refs match approved M0; PR20/21 remain OPEN.
No candidate article/revision or historical contract change admitted. Status remains review;
main/staging actual landing and prerequisites remain distinct, uncompleted gates.

### 2026-10-15 actual dual-target acceptance

Owner-confirmed and independently read-back PR22/main001b26f and PR23/staging0357835 are
MERGED; actual main is an ancestor of actual staging. Both complete source identities equal
approved M0 plus exact shared engineering successor, with all50 candidate identities intact.
Main66+34+54 and staging95+34+87 actual landing tests pass; build/lint/native adoption/
structure/materializer pass. Existing historical assertions/verifiers, writing packages,
receipts and candidate/published content are unchanged. PR20/21 remain OPEN and are not
recorded landed or used to close historical tickets. The ticket's blocked_by is empty.
All T13 ACs met; this local tracker closeout references actual authorized target commits, not
a proposal or open PR. Landing receipt and coverage: ../../.proj.specs/0012-publication-workflow/implementation/T-0013-landing/.
No new merge, target push or deployment-setting change.

### Engineering delivery follow-through

Owner authorized this closeout plus separate T14/T15 main PRs. This parent includes
the independently reviewed four-file current/historical verification successor,
needed so the closed tracker coexists with unchanged #22 assertions and future maps.
It does not change the actual T13 landing commits or invent new target landing evidence.
Review lineage: epic review/code-T-0013-current-successor.md and security counterpart.
