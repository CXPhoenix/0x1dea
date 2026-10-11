---
id: T-0010
title: Restore main verification after the selected electricity release
epic: 0010-main-verification-repair
status: done
landing_evidence: .proj.specs/0010-main-verification-repair/landing.json
blocked_by: []
---

## Context
Owner-merged PR #17 exposes the mutable historical lint fixture and missing exact main release successor. Preserve historical contracts. The owner previously approved one ticket, no dependencies and the existing six-row test table, then explicitly requested this local follow-up. See the epic approval and reused test-plan records. T-0009 is already done; global allocation reserves T-0010 using staging's maximum, not main's older tracker.

## Deliverable
Current main's CLI and Python harness pass while old hash contracts remain unchanged and unauthorized source changes continue to fail closed. Local repair only; status cannot become done without separate landing authority.

## Acceptance criteria
M1–M5 in the epic spec and traceability table. Carry spec-review P1: reject Git replacement/graft history overlays and read original objects; include a CLI negative case.

## 給使用者（zh-TW）
修正 PR #17 後的 adoption verifier 與 Python harness，保留歷史 hash、文章與原測試契約。沿用單票、無依賴及原測試 seam，完成測試與獨立審查。這次只做本機修正，不更動遠端。

## Verification

Full 54 Vitest + 65 harness Python + 16 publication Python pass, zero Python skips. Lint/build/structure/materializer/current public verifier exit 0. See ../../.proj.specs/0010-main-verification-repair/coverage-report.md and diagnosis.md. Independent implementation review is the next gate; local verification is not landing evidence.

Initial independent Spec review found a protected-existing-source gap. Public CLI regression reproduced it; all existing release entries now remain immutable except reviewed CODE. Final 65-method harness and public verifier reruns pass. Final review remains the last local gate; see review/code-T-0010-initial.md for the retained finding.

## Final independent review

Final 43-file packet: Standards P0/P1/P2=0/0/0; Spec P0/P1/P2=0/0/0, original P1 closed; security HIGH/MEDIUM=0/0 at confidence >=0.8. Reports: ../../.proj.specs/0010-main-verification-repair/review/code-T-0010.md and security-T-0010.md. This comment and final reports were appended after the reviewed snapshot; implementation sources did not change. Local gates passed; status stays review because no landing is authorized or performed.

## Owner-requested listing follow-up

The owner explicitly requests the omitted security-awareness listing correction, illustrated by the existing cybersec series listing. Reopen local implementation within this same single no-dependency ticket. The additive listing-followup/spec.en.md and traceability.md supersede only the original one-index no-edit exclusion; earlier reports describe their earlier snapshots. No remote action is requested. Acceptance L1-L4 supplements M1-M5 with that explicit index identity exception.

## Listing follow-up local verification

L1-L4 implementation completed locally. Exact shared category index restored; 54 Vitest, 66 harness and 16 publication tests pass, Python skips 0; all named checks and sandbox build pass. Actual browser covers desktop/mobile and light/dark with Tab/Enter navigation. Preserved 1716 of 1719 merged entries; only the single index and two original tracked verifier/harness repair files differ. See listing-followup/coverage-report.md and evidence. Fresh combined independent review is next. No commit, push, PR, merge or deployment performed.

## Listing follow-up final independent review

Fresh combined 83-file implementation packet: Standards0/0/0; Spec final unresolved0/0/0; security HIGH/MEDIUM0/0. Initial Spec P1 concerned screenshot/viewport evidence; retained and closed by direct live DOM recheck in both mobile modes. No implementation code changed after capture. See listing-followup/review/code-initial.md, code-final.md, security-final.md and validation.zh-TW.md. Coverage clarification and final evidence/reports were appended after review. Local gates complete; status stays review because no landing was requested or performed.

## Explicit delivery authorization

The owner now explicitly authorizes commit, non-force branch push and a PR to main for this T-0010 verifier/harness and listing repair, excluding all other candidates and prohibiting merge. This supersedes earlier local-only delivery limits, not the preserved historical validation scope. Fresh pre-commit checks:54 Vitest+66 harness+16 publication; all named commands and sandbox build exit0, Python skips0. See delivery/authorization.md, validation.md and scope-audit.json. All reviewed implementation hashes remain unchanged. Status stays review until actual authorized landing.

## Present-day closeout follow-up

Owner-authorized evidence audit marks T-0001/T-0010 done and retains T-0002/T-0003/T-0004/T-0008 review. T-0012 separately tracks the unmerged exact T1 receipt/identity guard integration and round-1 Red-team P1 counterexamples; this ticket is done only for the original M1-M5/L1-L4 scope already landed. See ticket-closeout/spec.en.md, traceability.md, review/round-1.md and audit.md. Earlier local-only/no-landing prose describes its historical time, not the current receipt.
