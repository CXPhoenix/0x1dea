---
id: T-0009
title: Restore deterministic tests and exact current-source verification
epic: 0009-test-contract-repair
status: done
blocked_by: []
landing_evidence: .proj.specs/0009-test-contract-repair/landing.json
---

## Context

Owner approved one ticket, no dependencies and the original six-row test plan.
Spec and traceability passed four independent axes in two rounds, with zero
remaining findings. See .proj.specs/0009-test-contract-repair/approval.md.

## Deliverable

Historical tests remain deterministic against the current verifier, the exact
reviewed source state passes a fail-closed successor, both Python suites and
Vitest run through complete commands, and tracker views retain truthful blockers
and landing evidence. Preserve the live article and original history.

## Acceptance criteria

- [x] V1: fixed historical acceptance and diagnostic fixtures.
- [x] V2: frozen migration proof and independent live article preservation.
- [x] V3: exact successor, original provenance and rejection counterexamples.
- [x] V4: complete discovery and failure-propagating commands.
- [x] V5–V6: accurate views and unchanged landing authorization boundary.
- [x] V7: preserved Finder backup and no-clobber coupled rollback.
- [x] V8: fresh complete checks, coverage and independent reviews.

## 給使用者（zh-TW）

修正歷史 fixture 混用目前檔案、文章測試與後續編修混淆、Python 測試入口不完整及 blocked 顯示不一致。以精確 successor 核對目前來源，保留文章、歷史證據與未完成依賴。本次僅本機修正，不包含 commit、push 或部署。

## Comments

Approved spec, traceability, source scope, test plan and reviews live in the
matching epic directory. Existing owner authorization carries forward. Keep
review after local delivery; no landing authority is granted.

Final local aggregate passed: 87 Vitest + 81 harness Python + 16 publication Python.
Coverage table and executed logs exist before the refreshed final code/security
review. Original article/history/lock identities are unchanged. V8 independent review closure
is recorded in the epic; status review does not mean authorized landing.

Final independent Standards/Spec/security review is complete with no remaining
findings. Local CLI verification covers the actual tooling surface. No commit,
push, landing or deployment was performed. Existing T-0005 evidence remains
missing and its dependents retain their edges.

## Authorized staging landing — 2026-10-11T07:14:47.240742+00:00

The owner explicitly requested T-0005 done, T-0009 done and push to staging.
The earlier local-only comments above describe their original scope; this new
receipt supersedes that restriction for the requested landing. Actual GitHub
staging was read back at 6c315d9fbcdf38b21a979159504937be245f77a2, containing this ticket's commit 6c315d9fbcdf38b21a979159504937be245f77a2.
Status is now done; see .proj.specs/0009-test-contract-repair/landing.json and landing-approval.md.
Other tickets retain their own statuses and dependency edges. No main or separate
deployment operation was performed. Epic close-out is recorded in review/chain-analysis.md,
retrospective.md and reports/staging-closeout.html.
