# Coverage report before implementation review

Verified on tickets/T-0010/main-verification-repair, HEAD/base/merge-base 88b9c53852f527ee636bcc4b4ca5e166f6ec10fd, with the two tracked repairs and explicit new verifier/test sources. All eight recorded commands exit 0. Full Python discovery: 65 harness methods and 16 publication methods; failures=0, errors=0, skipped=0. Full Vitest: 54 tests in 6 files. Subtest failure records in earlier red runs are not counted as failed test methods.

| Seam | Tests | Measured coverage | AC | Uncovered, and why |
|---|---|---|---|---|
| Historical Python verifier input | existing lint positive and negative cases within 65 harness tests | frozen 724ddad epoch with current verifier; original failure reproduced; all old cases retained | M1 | no line/branch instrumentation; behavior measured at the existing seam |
| Current public CLI | 12 new methods plus existing 53 harness methods | accepted exact merge; changed bytes (9 inputs), scope alteration/deletion, missing/link/mode/parent, all 4 required repair sources, tracked/untracked/ignored article, nonancestor/missing Git objects, replace/graft and generated-output symlink rejection; four formerly allowed existing tool/management paths cannot change, and existing publication code cannot disappear | M2,M3,M4 | trusted reviewer-controlled verifier bytes are not self-authenticated |
| Complete release and preservation | current CLI, exact Git comparison, preservation audit | 45/45 release delta paths, 34/34 product identities; 55 site moves, 370 baseline entries, 641 framework files, 113 trace rows; all pre-existing files unchanged except the two declared repair files | M2,M4 | new management records follow existing allowances; generated output excluded |
| Website/VitePress renderer | 54 Vitest tests | full unchanged main suite including captions, summary, EncoreTicket, helper and lint tests | M4,M5 | no new browser behavior; browser/deployment not revalidated |
| Publication CLI | 16 Python methods | complete existing publication suite passes | M5 | synthetic local fixtures do not establish remote publication |
| Full command compatibility | lint, build, structure, materializer, public verifier | all exit 0; existing Node 24.13.0/pnpm 10.28.0, no install | M5 | no hosted CI or external services were run |

Commands, exact outputs and exits are in evidence/. Historical PR #17 failure records remain unchanged. The main package still runs Vitest only via test:unit; both Python suites were explicitly executed. This report precedes stage 6; independent review outcomes will be recorded separately, not inferred from green tests. Status remains review until separately authorized landing.

## Review correction and final retest

Initial Spec review found one P1: the new-path management policy also exempted existing tool sources. A public CLI method reproduced five failure records (four changes and one deletion accepted); after protecting all 1,719 release entries except the two existing CODE trust roots, the same method passed. The other two CODE roots are new files. All 1,717 other existing entries remain unchanged. The complete final Python harness was then rerun: 65 methods in 105.087s, zero failures/errors/skips. Public CLI re-run also exits 0. Red/green logs and final preservation audit are retained in evidence/. Unchanged Vitest, publication suite, lint/build/structure/materializer results remain applicable because their source/toolchain inputs did not change. Final independent review uses a new frozen packet.
