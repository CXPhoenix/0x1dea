---
id: T-0014
title: Prepare and verify one article through the explicit v2 contract
epic: 0012-publication-workflow
status: done
landing_evidence: .proj.specs/0012-publication-workflow/implementation/dual-landing-20261016/T-0014-landing.json
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

### 2026-10-15 local implementation acceptance

Actual T13 dual-target landing unblocks this slice. Explicit v2 schema/prepare/verify/build/ready
implements approved P04–08/P14–17. Thirty focused public Git/CLI cases and actual enforced
VitePress build pass; full current Python66+58 and immutable #22 original10 pass (134 total),
plus54 website unit/build/lint/structure/materializer. Independent Standards/Spec review
resolved twoP1 (canonical alias delta and empty other-topic ancestry) and twoP2; security
resolved independently confirmed lazy-fetch HIGH; all final unresolved counts0.
Shared current successor/runner independently reviewed with T15. Evidence and coverage:
`.proj.specs/0012-publication-workflow/implementation/T-0014/`; reviews in epic review directory.
Original v1/assertions/history remain unchanged. Six actual candidates stay legacy, with no
source migration, article content or deployment changes. Local synthetic approval/build
evidence does not prove real served preview or authorize publication/remote delivery.
Status review only: no new main/staging landing receipts; done remains prohibited.

### 2026-10-15 PR25 current-main revalidation

Owner authorized scoped PR25 update against actual main PR24 landing `c1dd3bb`, with
no merge or deployment change. Independent review confirmed and fixed MEDIUM corrupt
source-blob admission: the v2-only Git wrapper verifies blob bytes against Git OIDs;
v1/history remain unchanged. Approved P16 public seam: one new red-green regression
with baseline/A/B subtests, plus subsequent public verify rejection. Fresh full run135
(66 live harness +59 live publication +10 immutable PR22), website54/build/lint and
native/structure/materializer pass. Actual isolated build denies outside read/write/net.
Evidence: implementation/T-0014/main-refresh-20261015 in the epic spec directory;
additional code/security main-refresh reports retain separate review axes. Six actual
candidates/50 owned paths remain unchanged; synthetic preview approvals are not HTTP
or real publication evidence. Status remains review; no new landing is claimed.

## 2026-10-16 actual dual-target closeout

The owner conditionally authorized this closure after manually merging PR21. Primary GitHub readbacks and real Git ancestry establish the main landing and staging61292484 landing, whose tree equals reviewed head dbb17ad8. The current acceptance audit and exact receipt are under `.proj.specs/0012-publication-workflow/implementation/dual-landing-20261016/`. Prior review/unlanded notes above remain historical checkpoints. Done refers to this ticket's approved engineering acceptance and actual landing, not deployment, remote automation activation or publication. Candidate bytes and immutable contracts remain preserved.
