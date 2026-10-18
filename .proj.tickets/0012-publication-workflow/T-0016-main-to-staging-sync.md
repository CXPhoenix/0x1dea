---
id: T-0016
title: Turn main changes into one trusted staging synchronization PR
epic: 0012-publication-workflow
status: review
blocked_by: [T-0015, T-0021, T-0022]
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

## Current local implementation — 2026-10-16

Owner confirmed PR21 merged and authorized conditional T12/T14/T15 closure plus T16 work. Actual main5e6c889c/staging61292484 and unchanged candidate/history bytes were verified; exact dual-target receipts permit the three local done states. Their original records are retained.

T16 local controller/adapter/CLI and inactive templates are implemented on the canonical main-based ticket branch. Approved P10–P12 run at public local seams with real disposable Git/native/enforced builds and fake GitHub; P13 is not passed. Complete main192/staging221 Python, main54/staging87 unit and zero-warning lint succeed. Independent source review resolved the bootstrap P1, shared-builder P2 and token preparation boundary; final metadata review is linked below.

Evidence: implementation/T-0016/coverage.md, final/execution.json, tdd-evidence.json; review/code-T-0016.md and security-T-0016.md. Status is review: actual separately authorized disposable GitHub exercise, later reviewed main/staging landing and activation gates remain unmet. No live workflow/repository-rule/deployment modification, token installation or merge occurred. Local metadata and code are uncommitted/unpushed; this does not claim remote tracker delivery or ticket done.

## Authorized main PR delivery — 2026-10-16

After the successful local implementation/reviews, the owner authorized commit, non-force push and one implementation PR to main for T12/T14/T15 closure plus this ticket's approved engineering/management scope. The new authorization supersedes only the earlier local-only delivery checkpoint; no historical evidence is rewritten. See implementation/T-0016-main-delivery-20261016/.

T16 remains review; P13 is unverified and activation blocked. No merge, live automation, deployment-setting or repository-rule/credential change. Actual T16 main/staging landings and the separately authorized disposable remote exercise are still required before done.


## Approved P13 prerequisite registration — 2026-10-16

Owner replied ‘同意’ to the reviewed four-ticket proposal and 23-row allocation. Registered T-0019 (A), T-0020 (B), T-0021 (C; blocked by T-0019/T-0020), and T-0022 (D). This ticket retains T-0015 and adds T-0021/T-0022 as unresolved direct blockers; A/B are transitive. No repair depends on T-0016 done. T-0017/T-0018 edges are unchanged.

Actual main8b31956f/staging05fc16c3 include the T-0016 local implementation via merged PR27/28; this does not satisfy P13. The new records authorize tracker publication only. Status remains review; the original P13 remote exercise is NOT RUN, all 23 prerequisite plan rows are NOT WRITTEN / NOT RUN, and lab/credentials/rules/automation/deployment changes remain unauthorized. No new implementation or commit/push accompanies this registration. The approved supplement, review closure and registration evidence are under implementation/T-0016-P13-prerequisite-ticket-proposal-20261016/.

## Authorized private-lab P13 A1 continuation — 2026-10-18

After actual PR34/35 engineering landing and conditional T21 closeout, the owner resumed the previously authorized private lab scope. One independently reviewed, read-only, two-minute bootstrap workflow ran on actual hosted macos-15, run39103693455 at e7d6a96. It completed failure/blocked: default Nodev22.23.2, no pnpm in PATH, three required external selections absent. This is not proof that every alternate toolcache is absent or that sandbox availability proves isolation.

The own probe workflow is disabled after evidence capture. No candidate/controller/PR/merge/race exercise or activation receipt follows the missing prerequisites. Original P13 a-l acceptance is not passed; see implementation/T-0016-P13-bootstrap-20261018/{README.md,coverage.md,evidence/}. Status remains review, with prerequisite provisioning/roles/enforcement unverified. Production refs, automation and deployment settings are unchanged. Old NOT RUN/unauthorized checkpoints above remain historical and are superseded only by the explicit private-lab authority for this bounded A1 batch.
