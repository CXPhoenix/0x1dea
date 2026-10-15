# Evidence-backed tracker closeout follow-up

## Problem Statement
The owner requests an evidence audit of T-0001, T-0002, T-0003, T-0004, T-0008 and T-0010, recording done only after acceptance and actual authorized staging landing. T-0011 closeout must be included in two unmerged PRs. The main release guard currently rejects the otherwise valid T-0001 status transition because the original ticket is a protected release entry.

## Solution
Record a per-criterion evidence audit and truthful remaining gaps. Close only T-0001 and T-0010, retaining the already substantiated T-0011 done record. Keep T-0002/T-0003/T-0004/T-0008 at review. Add one exact T-0001 ticket successor identity to the current release guard, retaining its original identity for historical fixtures. All original ticket prose and historical reports remain unchanged; current audit documents explain later events.

## User Stories
1. As the owner, I can distinguish implemented/landed work from fully evidenced acceptance.
2. As the owner, I can review the same closeout facts on main and staging without publishing a candidate article.

## Implementation Decisions
- Reuse the existing main verification repair and staging synchronization tickets and their one-per-ticket branches; no new ticket or deployment flow is introduced. Each existing branch receives the target-specific closeout projection based on its current remote target. Both PRs remain unmerged.
- The sole new preservation exception is the exact original T-0001 regular 100644 ticket with only status review changed to done and a fixed landing_evidence field. Permit either the pinned original release identity or this independently captured exact successor. No other byte, path, mode or link exception is allowed; no blanket management-file exemption replaces the original protected inventory.
- Existing tracker validation still independently requires an authorized, landed T-0001 receipt, a regular approval receipt and a real commit ancestral to staging. Exact ticket bytes alone cannot pass a missing or invalid receipt. The receipt records the original adoption commit and current observed staging ancestry; current approval must never be backdated as original agent merge authority.
- T-0002 stays byte-identical at review. Other requested review tickets gain only additive present-day evidence notes and keep their original acceptance scope. Missing raw browser/print/SSR artifacts remain missing; later summary prose does not substitute for them.
- T-0010 records PR18 main landing and PR19 staging integration; T-0011 retains the existing owner merge and closeout record. Main imports necessary management evidence and the already-done T-0005 dependency receipt for T-0003/T-0004 without importing any blog candidate or staging reconciliation source. Main and staging keep their own verifier dispatchers.

## Acceptance Criteria
C1: All six requested tickets have a per-criterion result, resolvable evidence paths, exact landing commits and explicit limitations; done is set only for T-0001/T-0010, plus the existing T-0011 closeout. T-0002/T-0003/T-0004/T-0008 remain review.
C2: The public verifier accepts both the historical original T-0001 ticket and the exact approved done successor with valid receipts. It rejects arbitrary text/status/receipt-path changes, wrong mode, missing/link paths, missing or false receipt, wrong ticket/target, nonexistent commit and non-ancestor landing. Every prior historical/source/publication assertion remains enabled.
C3: Fresh verifier, structure, materializer and full Python harness/publication suites pass on both actual target-specific final source trees, with zero Python skips. Compare all blog paths and historical preservation manifests against each pinned target: zero differences. Fresh Vitest/lint/build need not repeat for management and Python-only changes; prior product evidence stays explicitly historical.
C4: Independent Standards/Spec and affected security review clear the captured change. Both non-force pushed PRs target the requested branches and remain open with auto-merge disabled. Their code delta is confined to the shared main-release guard and its public-CLI tests; remaining delta is management evidence. No publication, deploy, external index or workflow configuration changes occur.

## Testing Decisions
Reuse the owner-approved disposable-Git public preservation CLI and tracker/landing seams from T-0010. One exact successor acceptance regression precedes implementation, then counterexamples at the same public interface. Keep all existing test assertions and immutable release pins. Record real red/green results. Repository validators and independent target trees verify delivery scope.

## Out of Scope
Completing missing browser/production verification for the retained review tickets, article changes, changing Git/Cloudflare workflow, installations, broad validator exceptions, remote branch merges or force push.
