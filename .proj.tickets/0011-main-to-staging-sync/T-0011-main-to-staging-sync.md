---
id: T-0011
title: Synchronize merged main into staging without changing candidates
epic: 0011-main-to-staging-sync
status: done
blocked_by: []
landing_evidence: .proj.specs/0011-main-to-staging-sync/landing.json
---

## Context
Owner explicitly authorized a separate synchronization branch, resolution of the six diagnosed conflicts, retained candidates/history, passing tests/review, commit/push and an unmerged PR to staging. Spec passed four independent axes in two rounds; test seams reuse prior approvals.

## Deliverable
A reviewed synchronization merge preserving staging source identities and both exact verifier contracts, delivered as an unmerged PR to staging.

## Acceptance criteria
- [x] S1: pinned merge ancestry and exact candidate/source preservation.
- [x] S2: both strict CLI contracts and all existing counterexamples pass.
- [x] S3: immutable historical oracles, main helper/tests and tracker semantics preserved.
- [x] S4: complete fresh checks, browser and independent reviews pass.
- [x] S5: non-force ticket push and unmerged staging PR; no target update.

## 給使用者（zh-TW）
把已 merge 的 main 合回 staging，修正六個衝突，保留候選文章、審閱提示與歷史驗證。測試與獨立審查完成後，只 push 本票分支並開 PR 到 staging，先不 merge。

## Comments
See the matching spec, traceability, approval and test-plan documents. Do not mark done before actual staging landing.

## Verification evidence
- [Coverage report](../../.proj.specs/0011-main-to-staging-sync/coverage-report.md): 87 Vitest, 95 harness and 16 publication tests pass with no skips; final Python sources unchanged.
- [Local validation](../../.proj.specs/0011-main-to-staging-sync/validation.zh-TW.md): tooling, isolated build, browser and exact identity audit.
- [Scope audit](../../.proj.specs/0011-main-to-staging-sync/evidence/scope-audit.json): all 111 blog entries and five candidates preserved, 123 main additions exact.
- S4 complete: independent Standards and Spec each P0/P1/P2=0; security HIGH/MEDIUM=0. See [code review](../../.proj.specs/0011-main-to-staging-sync/review/code-T-0011.md) and [security review](../../.proj.specs/0011-main-to-staging-sync/review/security-T-0011.md).
- S5 awaits the authorized commit/push/PR readback; it is not represented as completed before execution. Ticket remains review until actual staging landing.

## Actual owner landing and closeout

The preceding review/delivery notes are historical snapshots. PR #19 was delivered open with no auto-merge and then merged by the owner at 2026-10-11T12:58:17Z. The owner subsequently requested T-0011 done. Actual staging merge commit is c6efa7ded4731cbe251bdbc6fea5615e7e7b11b7; main eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a is its ancestor, and its tree equals reviewed 01b5d69bc1a006ef04d8c475b4e7df38712c9ca0.

[Landing receipt](../../.proj.specs/0011-main-to-staging-sync/landing.json), [owner approval](../../.proj.specs/0011-main-to-staging-sync/landing-approval.md), [chain analysis](../../.proj.specs/0011-main-to-staging-sync/review/chain-analysis.md), [retrospective](../../.proj.specs/0011-main-to-staging-sync/retrospective.md) and [evidence report](../../.proj.specs/0011-main-to-staging-sync/reports/t0011-closeout.html). Closeout metadata is local and uncommitted until separately delivered; this status does not claim those new files are already on GitHub.
