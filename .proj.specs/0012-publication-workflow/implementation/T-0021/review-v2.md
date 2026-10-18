# Source-v2 independent review checkpoint

Packet: /private/tmp/T21-source-v2-review; base=HEAD=64b31a2c38959ef5490892fa2a001bb0bf2f8ca0; files_sha256=184de6a66d9c2e91c890028e2ad04752a5f9ace3a2810af4d736ccfb698c4175. All 2953 entries matched.

| Axis / independent reviewer | Result | Resolution |
|---|---|---|
| Standards / t21_standards | P0/P1/P2=0/0/1; smells=0 | STD-V2-01: original two review regressions were batched; retain truthful process deviation below |
| Spec / t21_spec | P0/P1/P2=0/1/0 | Original two P1 fixed; remaining same-call ID drift now reproduced/fixed in v3 |
| Security finder / t21_security | HIGH/MEDIUM=0/0; exploit candidates>=0.8=0 | Source only; no independent false-positive stage needed without candidates |

Spec P1 at scripts/publication_reporting.py:230-253: pending/no prior journal leaves check_id=None, allowing first checks ID81 then second checks ID82 with matching payload/app to become ready. C3/PC-07 requires fixing first observed identity. Source-v3 adds one test method with existing, pending and known-POST variants: all three reproduce red, then a minimal pin of first inventory/acknowledged POST ID makes all green. No extra seam or plan row.

Security noted the same identity substitution did not establish an attacker able to control the trusted app, so it was not an exploitable HIGH/MEDIUM candidate; this does not overrule the Spec contract defect.
Full-v2 runs were interrupted before source edits. Partial logs and receipt remain under attempts/, not passes.

## STD-V2-01 disposition

Accepted and documented process deviation: the original two v1 review findings were reproduced and fixed as a batch, contrary to workflow Stage5's one seam/test/minimal-implementation cycle. The raw red/green logs are preserved. No claim is made that those original corrections followed individual TDD cycles; retrospective runs cannot change that history. The product defects still require the real focused/full regressions and independent source review. Subsequent same-call ID correction follows one test red, minimal implementation, green. The historical P2 is retained rather than rewritten to zero; no product exception, plan expansion or weakening is introduced.
