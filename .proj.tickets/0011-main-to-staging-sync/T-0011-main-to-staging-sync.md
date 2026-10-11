---
id: T-0011
title: Synchronize merged main into staging without changing candidates
epic: 0011-main-to-staging-sync
status: review
blocked_by: []
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
- [ ] S5: non-force ticket push and unmerged staging PR; no target update.

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
