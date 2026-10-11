# Test and preservation contract repair — proposal

> Resolution on 2026-10-11: the owner approved this single/no-dependency proposal
> and its original six-row table. Required spec/reviews completed and T-0009 was
> published. This document preserves the earlier proposal; current authority and
> implementation evidence live in `../../0009-test-contract-repair/approval.md`
> and `../../../.proj.tickets/0009-test-contract-repair/T-0009-test-contract-repair.md`.

## Destination

Make the installed local verification commands exercise all existing suites, keep
historical fixtures deterministic, and distinguish current source acceptance from
historical proof and ticket readiness. Preserve the current article and immutable
records. The owner requested fixes on 2026-10-11 after the diagnosis below.

This is a stage-1 proposal, not an approved spec, published ticket, or test plan.
No implementation or new tests have been written. The next available epic and
ticket numbers are 0009 and T-0009; recheck allocation before publishing.

## Notes

Captured HEAD: `6e4eb804bcbda8504935be49fd6537d6327d5303`.
Captured branch: `tickets/T-0008/article-captions`; task-entry worktree was clean.

Local observations from 2026-10-11:

| Surface | Executed check | Result |
|---|---|---|
| Vitest | `pnpm test:unit` | 85 passed, one article-preservation case failed |
| Python harness | `python3 -B -m unittest discover -s tests/harness_adoption -v` | 69 test methods; 14 failure records across six methods, including subtests |
| Python publication | `python3 -B -m unittest discover -s tests/article_publication -v` | 16 passed |
| Root Python discovery | `python3 -B -m unittest discover -s tests -v` | zero tests, exit 5 on installed Python 3.14.3 |
| Existing tooling | lint, verify-project, materializer check | passed |
| Current public verifier | `python3 -B scripts/verify-harness-adoption.py` | rejected current config source |
| Differential fixture probe | four existing failing reconciliation methods with source frozen at f93237b | all four passed; source checkout unchanged |

The Python fixture checks out a fixed historical commit but copies overlay and
revision inputs from the current checkout. This contaminates accepted fixtures and
causes unrelated early errors to mask negative cases. A previous correction of the
same class is recorded in the reconciliation epic's TDD record.

The current article's two shortened captions disagree with its migration fixture.
Even inverse conversion using the original figure blocks produces a different
source SHA, so changing only those two expectations is insufficient. The existing
coverage report is a historical claim, not evidence for the captured final HEAD.

The current preservation boundary has seven content mismatches and nine unknown
paths. The unknown paths include new product sources and one ignored Finder
metadata file. The verifier stops at its first mismatch. This is separate from the
fixture defect: freezing a test does not authorize changed live sources.

All eight local tickets remain review. T-0003 and T-0004 depend on T-0005; local
Git history contains the related staging merge, but the ticket lacks a completed
landing record. The documented Blocked view selects todo tickets, whereas the
implementation currently returns unresolved dependencies for every status.

## Proposed decisions

1. Use one bounded repair epic and one complete tracer-bullet ticket, with no
   implementation blocker edge to T-0005: this repair exists to resolve the
   verification and presentation problems, and does not depend on relabeling an
   older ticket done. Proposed slug: `test-contract-repair`.
2. Load historical accepted fixtures from explicit immutable Git objects matching
   their existing provenance records. Current guard implementation remains the
   implementation under test. Never derive an expected hash from mutable live
   bytes or weaken a negative assertion to accept an unrelated early error.
3. Separate the historical article-conversion proof from checks of the current
   article's semantic figures, references, original image alt/src, and citations.
   Preserve the captured article bytes. Record the later editorial successor
   explicitly; preserve the original baseline and old execution evidence.
4. Add a bounded, reviewed exact successor for the known later product changes
   and the necessary repair delta. Keep historical manifests unchanged; validate
   pins, ancestry, exact paths, predecessor hashes, current hashes and file types.
   Unknown or ignored sources and tampering still reject. No runtime refresh of
   expectations, mutable-HEAD pin, or whole-directory exemption.
5. Keep the Finder metadata bytes in a local ignored backup with a hash receipt
   before removing that single file from the scanned docs tree. Do not broaden
   the source allowlist or delete unrelated files.
6. Provide a documented local command that runs both Python suites and fails on
   any failure, import error, or zero-test suite. Provide an aggregate command for
   Vitest and Python. Preserve the existing Vitest command and installed toolchain.
7. Keep unresolved dependency edges independently visible. Make the Blocked view
   follow its documented todo-only selection; processing/review tickets remain
   in flight. Preserve cycle/missing-id/pending/landing validation. Close an older
   ticket only if actual staging containment and an authentic owner authorization
   receipt are both available; otherwise explicitly retain review and the missing
   evidence. Do not infer authorization from a commit or merge alone.
8. Append current validation and supersession notes to affected reports. Update
   current-state documentation where needed, preserving historical results and
   labeling their captured scope. Complete independent spec, code and security
   review and real local CLI verification before claiming the repair passes.

### Alternatives considered

- **Bounded exact successor (recommended):** preserves the current contract and
  repairs the captured state with a small reviewed increment. Future product
  changes still require an explicit accepted successor.
- **General approval registry:** could support arbitrary future epics, but changes
  the policy model and requires broader security and migration decisions.
- **Separate repair epics:** could isolate each defect, but would defer verification
  of the complete passing command and produce intermediate unresolved gates.

### Proposed ticket

**T-0009: Restore deterministic complete verification and accurate gate reporting.**
Blocked by: none. Deliverable: one reproducible local verification path that covers
both language runtimes, accepts the exact reviewed current source successor, rejects
counterexamples, and reports dependency state without fabricated landing evidence.
Implementation branch: `tickets/T-0009/test-contract-repair`.

### Test plan proposed for owner approval

| Seam | Test intent | Scope | Acceptance group | Boundary conditions |
|---|---|---|---|---|
| Existing Python verifier CLI in disposable Git clones | historical accepted inputs stay valid after later source changes; negative cases reach the intended offending path | component/revision fixtures and public CLI | deterministic fixtures | changed live article/theme, missing object, wrong pin, byte/mode/link/missing source, unknown and ignored paths |
| Existing VitePress renderer and article source checks | current article preserves semantic figures/references/citations; historical conversion uses frozen input | existing article-caption suite | article and evidence consistency | three figures, six references, eight alt/src pairs, source links, independent historical hash; current prose remains byte-identical |
| Existing current public preservation CLI | accept only the exact reviewed successor without altering old manifests | captured product and repair delta | current source acceptance | before/after hash, record digest, ancestry, extra/ignored source, linked source and changed historical manifest; preserved Finder metadata receipt |
| Local test command subprocess | run both Python suites and aggregate with Vitest; propagate failure and reject zero discovery | existing runtimes, no dependency installation | complete test entrypoint | success, failing suite, import failure, zero tests; no test logic copied into the runner |
| Existing tracker/public CLI JSON | documented views agree with status and dependency rules | todo/processing/review/done/pending and unresolved edges | accurate gate reporting | unresolved dependencies remain visible, true blocked todo, invalid landing receipt, missing id and cycle |
| Existing complete project commands | final integrated state is verified and reports reference the executed state | full Vitest and both Python suites, lint, build, structure, materializer and current verifier | integrated acceptance | run on the repair checkout; no silent skips, historical passes reused as current, or external deployment claim |

## Decisions so far

The user authorized proceeding with corrections and explicitly invoked the project
`to-tickets` skill on 2026-10-11. Its concrete output is the
[single-ticket draft](ticket-proposal.md). The diagnosis and existing public seams
are already known. This proposal makes no claim that the new ticket breakdown,
successor scope or test table has been approved.

## Not yet specified

- Owner confirmation of the proposed scope, one-ticket breakdown and test table.
- Explicit invocation of the project's manual-only requirement/spec skills,
  followed by the prescribed four-axis spec review (at most two rounds).
  `to-tickets` has already been explicitly invoked; do not ask for it again.
- Exact successor record and final repair source list, to be fixed in the reviewed
  spec; no self-approval or broad exemption is proposed.
- Whether authentic additional landing authorization for T-0005 can be recovered.
  Missing evidence does not block implementing accurate views or deterministic tests.

## Out of scope

Commit, push, PR, merge, deployment, external-index updates, dependency installation,
global skill/trust/credential changes, article rewriting, retrospective fabrication
of approvals, and a general replacement for the existing policy system.

## Evidence pointers

- Existing fixture: `tests/harness_adoption/test_reconciliation.py`.
- Existing article case: `tests/articleCaptions.vitest.ts` and
  `tests/fixtures/article-caption-baseline.json`.
- Public guard: `scripts/harness_reconciliation.py` and
  `scripts/verify-harness-adoption.py`.
- Existing contract: `.proj.specs/0005-harness-reconciliation/spec.en.md` and `TDD.md`.
- Tracker contract: `docs/agents/issue-tracker.md` and ADR-0002 / ADR-0006.
- Latest article evidence: `.proj.specs/0008-article-captions/coverage-report.md`.
- Diagnostic logs remain local in the temporary directory; they are not portable
  approval receipts or publication artifacts.
