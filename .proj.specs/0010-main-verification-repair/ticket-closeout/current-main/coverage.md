# Current-main coverage and disposition

| Criterion / seam | Current result | Evidence / limit |
|---|---|---|
| C1 six-ticket audit plus existing T11 closeout | pass for evidence truthfulness | audit.md has every original AC and actual landing. T1/T2/T10 done, T5/T11 retain done; T3/T4/T8 review; T12 review. T2 extra browser timeout was not an AP/cleanup gate. Original incomplete records stay incomplete |
| C2 native CLI exact successor | pass | cycle1/2 red→green; focused.txt 5 tests; arbitrary prose/status/path/map repins, mode/missing/link/receipt/approval rejected, exact main+staging accepted. extra-boundaries.json independently rejects a different valid stage ancestor/nonancestor/missing/link/executable receipt and restores a passing positive |
| C2 historical assertions | pass, unchanged contexts | all live assertions unchanged; original main release fixture remains accepted, fixed #22 fixture still exactly10 tests; no extra freezing or failure fallback |
| C3 main full Python | pass,164 total | main-python.txt:66 live harness+88 live publication+10 explicit historical;0failures/errors/skips. Synthetic real macOS isolated build executes, not skipped |
| C3 staging projection full Python | pass,193 total | staging-python.txt:95 live harness+88 live publication+10 explicit historical;0failures/errors/skips; local complete Git source projection, not remote staging landing |
| C3 structure/materializer/native | pass at recorded checkpoints; final source rerun required before commit | separate main/staging native JSON, structure and materializer raw;176/55 main and178/56 stage generated/source files. These are static package checks, not fresh native skill discovery |
| C3 protected source | pass | source-scope.json:main73blog/stage111blog/50candidate paths unchanged; protected history and every pre-existing main test file/legacy helper/runner unchanged |
| C4 independent review | reviewed; actor precision issue corrected | code-review.md and security-review.md; original actor P2 resolved by primary pr-14-actor.json. Final metadata checks follow these reports |
| C4 delivery | preflight branch/refs fixed; remote outcome recorded in updated PR | original canonical T12 topic, non-force push to same branch, original PR20→main only. No #21 update, target merge, auto-merge, installation or deployment-setting change |

Full suites ran the same final controller/test/runner bytes reviewed in the capture. Afterwards only additive acceptance/audit/raw-report metadata and its exact map were updated. Native verifier, structure and materializer are rerun on final main/staging projections before commit, with another native readback after commit. Verification output necessarily predates the commit that records it; no source commit SHA is invented for pending files.

The approved C3 table does not require repeating Vitest/lint/full website build for management/Python-only changes. Previous product/browser/print/deployment evidence remains historical and scoped. The new isolated build is a synthetic CLI test, not publication readiness for a real article or production acceptance. Original push invocation limits remain explicit. New red logs are public path-label projections as documented in compatibility.md; original captured raw remains outside Git.

## Final precommit checkpoint

After the final metadata capture both independent code-review axes report P0/P1/P2=0/0/0; security HIGH/MEDIUM=0/0. Native verifier, structure and materializer then passed for both exact delivery projections: main2544/staging2696 source paths, candidate paths preserved50. The report text and its exact hashes are refreshed once to record that observed checkpoint, followed by another native identity check before commit; original controller/test/runner bytes stay unchanged. Remote C4 readback follows the authorized non-force push and is recorded in the updated original PR, not invented in this precommit record.
