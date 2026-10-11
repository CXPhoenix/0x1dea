# T-0012 coverage report

Current native CLI verification only. Product Vitest/build/lint and browser evidence referenced by the six-ticket audit are historical, not rerun by this metadata/Python follow-up. Both clones provide a real local `staging` ref at c6efa7ded4731cbe251bdbc6fea5615e7e7b11b7; no claim is made that a shallow main-only clone supplies this landing-validation prerequisite automatically.

| Approved seam | Actual evidence | Result | AC |
|---|---|---|---|
| Public main verifier, exact original/done T1 identities | red.txt → green.txt; targeted-green.txt (4 tests); every original assertion unchanged | PASS | C2 |
| Receipt/Git negative boundaries | receipt-red.txt → receipt-green.txt; four targeted methods cover bytes, modes, links, false/missing/wrong ticket/target/commit, nonancestor, different valid ancestor and unrelated approval; T2 tamper | PASS | C2 |
| Main full harness | harness-final-main.txt: 70 tests, 0 skips after fixture correction; harness-main.txt retained prior run | PASS | C3 |
| Staging full harness | harness-final-staging.txt: 99 tests, 0 skips after fixture correction; harness-staging.txt retained prior run | PASS | C3 |
| Publication Python suite, both sources | publication-main.txt, publication-staging.txt: 16 each, 0 skips | PASS | C3 |
| Native verifier, both final sources | verifier-delivery-main.json, verifier-delivery-staging.json: exit 0 after fixture correction | PASS | C3 |
| Structure and materializer, both sources | structure-delivery-main/staging.json, materializer-delivery-main/staging.json: exit 0 | PASS | C3 |
| Historical identities and scope | artifact-audit.json: 307 manifest entries, 111 receipt bindings, 12 PR16 component identities; scope-audit.json: main 73/staging 111 unchanged blog files, original pins/assertions unchanged | PASS | C1,C3 |
| Two new HTML reports | html-static.json: static parse/resources/CSP checks only; no rendered offline browser evidence | LIMITED; does not substitute missing historical browser evidence | C1 |
| Independent review and target-specific remote delivery | review/code-final.md, review/security-final.md: residual zero; paginated PR head/base/state readback after delivery | Gate recorded in final reports and PR descriptions | C4 |

Retained status gaps: T-0002 interactive browser flows; T-0003 raw SSR/browser/print artifacts; T-0004 raw SSR/browser and actual Production N4 proof; T-0008 resolvable screenshots and raw keyboard/SPA/SSR proof. These remain review. T-0012 remains review until actual landing. No test was written to fabricate those absent observations.

SOURCE currently on staging: branch-reproduction-red/green.txt records the additional C3 fixture regression and correction. git branch -f applies only to the already-detached disposable fixture; this is not force push.
