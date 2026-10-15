---
id: T-0005
title: Reconcile immutable history with exact approved product successors
epic: 0005-harness-reconciliation
status: done
blocked_by: []
landing_evidence: .proj.specs/0005-harness-reconciliation/landing.json
---

## Context

Known staging evolution and reviewed components fail a historical live-byte guard. Owner approved one bounded correction after root-cause disclosure. Four frozen spec axes cleared zero P0 in two rounds.

## Deliverable

A read-only required verifier accepts the exact known staging and approved component delta, preserves immutable historical evidence, and rejects extra/ignored paths, byte/type drift and invalid provenance through real CLI rejection tests.

## Acceptance criteria

- [x] R1/R4: immutable epoch and provenance checks retain history and reject tampering.
- [x] R2/R3: known staging and exact components pass; unknown, ignored, missing, linked or stale sources fail.
- [x] R5: no product/env behavior or publication changes; honest reconciliation and rollback documented.
- [x] R6: full required checks and independent code/security review recorded before authorized landing.

## 給使用者（zh-TW）

保留舊 manifests，新增可驗證的精確後繼合約，讓已審閱的 staging 與元件改動被辨識，未批准來源仍被擋下。不改 checksum、不放寬整個候選目錄，也不把缺少的舊流程補寫成當年已通過。

## Comments

External index: 0X1DEA #19 (external index maintained privately), parent verified readback, external processing. Repository is authority.

Blocked by: none. This single tracer bullet is owner-approved, not a framework rewrite. T-0003/T-0004 completion gates depend on resolving it. No commit/push/deploy or Library upload authorized. Approval and test-plan are under the epic.

## Authorized staging landing — 2026-10-11T07:14:47.240742+00:00

The owner explicitly requested T-0005 done, T-0009 done and push to staging.
The earlier local-only comments above describe their original scope; this new
receipt supersedes that restriction for the requested landing. Actual GitHub
staging was read back at 6c315d9fbcdf38b21a979159504937be245f77a2, containing this ticket's commit 69ff85f5fe1baddb54102070a436dff9ac1c5b73.
Status is now done; see .proj.specs/0005-harness-reconciliation/landing.json and landing-approval.md.
Other tickets retain their own statuses and dependency edges. No main or separate
deployment operation was performed. Epic close-out is recorded in review/chain-analysis.md,
retrospective.md and reports/staging-closeout.html.
