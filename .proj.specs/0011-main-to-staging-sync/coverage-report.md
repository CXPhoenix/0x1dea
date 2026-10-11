# T-0011 coverage report

This is an acceptance/seam report, not instrumented line coverage. Final source hashes are in evidence/python.json and scope-audit.json. No test was skipped.

| Approved seam / AC | Executed verification | Result | Evidence |
|---|---|---|---|
| Disposable Git / dual contracts / S1,S2,S3 | Full harness suite, including 13 unchanged main-release tests, staging/historical positive controls and byte/mode/link/missing/pin/history/extra/ignored negative controls | 95 tests passed; exit 0 | evidence/python.txt, python.json |
| Landing evidence ref resolution / S2,S3 | Existing tracker seam; absent local branch accepts valid origin/staging, invalid local ref or ancestry does not fall back, missing refs/approval reject | Red then green; included in 95 | evidence/landing-ref-red.json, landing-ref-green.json, invalid-ref-red.json, invalid-ref-green.json |
| Article publication / S1,S3,S4 | Complete existing publication suite | 16 tests passed; exit 0 | evidence/python.txt, python.json |
| Renderer / runner / S3,S4 | Full Vitest, unchanged JS/website inputs | 87 tests in 8 files passed; exit 0 | evidence/unit.txt, unit.json |
| Tooling / S4 | lint, structure, materializer --check, final public verifier | All exit 0 | evidence/lint.json, structure.json, materializer.json, verifier-final.json |
| Website / S4 | Isolated local staging build with installed runtime and sandbox probes | Build exit 0; all four boundary probes true | evidence/build.txt, build.json, build-isolation.json |
| Browser / S4 | One listing card, metadata, generated .html destination, Enter navigation, preview notice, desktop/mobile light and dark overflow | All assertions observed locally | evidence/browser.json, screenshot-dimensions.json and five JPG captures |
| Exact identity / S1,S3 | Full staging inventory and main-only additions | 1985/1988 existing entries exact; only 3 permitted integration sources differ; 111 blog entries exact; 123 main additions exact | evidence/scope-audit.json |
| Reviews / S4 | Four spec axes, Standards, Spec and security | Spec round 2 all zero; Standards/Spec P0/P1/P2=0, security HIGH/MEDIUM=0 | review/round-2.md, code-T-0011.md, security-T-0011.md |
| Delivery / S5 | Commit parents, non-force ticket push, unmerged PR base/head and remote readback | Pending external delivery at snapshot; checked after commit/push | Final PR and Git readback outside this pre-delivery snapshot |

The full Python run observed final-source hashes before and after execution with source_unchanged=true. Vitest and build inputs have not changed since their successful executions. There is no remote CI, deployment or production-browser claim.

## Actual closeout follow-up

The delivery row above is the original pre-delivery snapshot. PR #19 was subsequently verified open with no auto-merge, then owner-merged at c6efa7ded4731cbe251bdbc6fea5615e7e7b11b7. Owner explicitly requested done. See landing.json and closeout/ for actual open-delivery and merged readbacks. Post-closeout metadata validation uses an independent staging clone so the original local staging ref and checkouts stay untouched. No product/source implementation changed; full suites are not repeated for status-only metadata.
