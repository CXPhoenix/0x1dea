# T-0005 coverage report

| Seam | Tests | Coverage | AC | Limit |
|---|---|---|---|---|
| Public verifier CLI in disposable clones | 9 reconciliation tests with drift/path/ignored/source/type/provenance/ancestry/rollback subcases | exact baseline and reviewed overlay plus real nonzero rejection diagnostics | R1–R5 | no source-line coverage claim |
| Existing complete Python suites | 62 harness, 16 publication | retained original materializer/tracker/publication rejection assertions | R1,R2,R4,R6 | local Git objects; no remote |
| Product runtime/tools | 59 Vitest, lint, false/main build, materializer, structure | same installed toolchain, no product bytes changed for reconciliation | R5,R6 | real Production release remains separate |
| Original and corrected source boundaries | immutable manifests + corrected product hashes | original failure retained, no auto-refresh | R1,R2,R4 | historical missing approvals labeled present-day reconciliation |

Evidence is under evidence/ in this epic. Code/security review and final CLI receipt follow. No landing; ticket remains review when local gates complete.
