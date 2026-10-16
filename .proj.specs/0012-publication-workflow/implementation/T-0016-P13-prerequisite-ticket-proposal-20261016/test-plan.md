# Proposed prerequisite test plan — owner approval pending

All 23 rows below are **NOT WRITTEN / NOT RUN**. These are proposed allocation units, each containing the named subcases, not a claim of 23 executable tests. Reuse existing behavioral regressions instead of duplicating them; each future ticket adds one seam/test/minimal implementation at a time under project TDD. Negative cases assert no forbidden side effect. No test code is written in this proposal.

Surfaces: **G** disposable real local Git/CLI; **N** current public native policy/preparation validator; **J** public local job preflight/input interface; **R** public reporter/controller API adapter with replayed API envelopes and local Git. R proves request/refusal contracts, not GitHub enforcement. Existing source-bound capability fixtures are explicitly local-only. No lab, live check, branch rule or Actions execution is tested here.

| ID | Proposed stimulus and observable pass/fail | AC | Surface | P13 follow-up |
|---|---|---|---|---|
| PA-01 | With no workflow grant retain default .github refusal; original v1 snapshots and existing historical fixture outcomes are unchanged | A1/K1 | G/N | a |
| PA-02 | Exact independently approved repo/main/role/path/mode/hash workflow is accepted by native policy AND preparation; readback matches bytes | A1/A2/A3 | G/N | a/c |
| PA-03 | One at a time: unknown workflow/other .github, wildcard, traversal, duplicate, link, submodule, wrong repo/role/mode/hash is refused at each public entry | A2 | G/N | a/c |
| PA-04 | Candidate-provided admission, swapped approval/digest/source and approval inferred from map are refused; no workflow executes during preparation | A1/A2/K1 | G/N | a/e |
| PA-05 | Main/staging exact projections and export/readback agree with independent grant; control-role/main/policy drift invalidates old preparation | A3 | G/N | h |
| PA-06 | Target-specific candidate/article/history/alias bytes and historical oracle outcomes remain unchanged, including unchanged existing historical fixture suite | A3/K1 | G/N | e/l |
| PB-01 | Missing/wrong Python/Node/pnpm/deps/isolation stops by named prerequisite, without install/fallback or any Git/remote write | B1/K3 | G/J | a/e |
| PB-02 | Fresh separate writer/validator input dirs, full refs and independently delivered registry/runtime digests recompute identical operation/source pins | B1/B2 | G/J | a/e |
| PB-03 | Tampered config/digest/source/state identity or each B2 snapshot root/UID/mode/type/link-count/containment/opened-identity/read-stability predicate is refused before consumption; use actual filesystem cases plus explicitly labeled owner/race observation fixtures | B2/B3 | G/J | a/e/i |
| PB-04 | Credential sentinels absent from preparation/build/validator artifacts and logs; validator refuses write credentials and retains three deny-default probe expectations | B2 | G/J/R | b/e |
| PB-05 | Fresh jobs reuse one per-repo durable operation journal; accepted-unknown retry reads back; missing/foreign state refuses; shared non-cancelling writer group and distinct validator group cannot deadlock in contract simulation; host lock never claims manual/global exclusion | B3 | G/J/R | i/j |
| PB-06 | Shallow/missing refs, wrong role/source/config and invented permission/dispatch/exercise fields refuse; local fixture results never become live capability evidence | B1/B2/B3/K3 | G/J | a/h |
| PC-01 | Exact completed-success trusted run yields only configured check/status request on candidate head; independently reread repo/op/main/stage/head/tree/policy/workflow/run/event/reporter and returned check identity agree | C1 | G/R | b/c |
| PC-02 | Ack-only, missing, timeout, denied, failed, cancelled, skipped, neutral, duplicate, wrong/ambiguous binding each yield no success and blocked readiness | C1/C3 | G/R | c/d/i |
| PC-03 | Separate expected reporter/credential is required; wrong source/actor, build or writer credential and insufficient permission cause refusal without secret leakage or extra granted privilege | C2 | G/J/R | b/e |
| PC-04 | Advance candidate H1→H2 around report/decision; H1 readiness expires, old result is not reused, no merge is attempted | C3/C4 | G/R | f |
| PC-05 | Advance target S1→S2 or change configured check/source/protection; old readiness expires; missing strict non-bypass capability or local-only evidence refuses live readiness | C3/C4 | G/R | g/l |
| PC-06 | Advance main, policy or admitted workflow while candidate head remains constant; previous binding/readiness expires and requires new independent validation | C3/C4 | G/N/R | h |
| PC-07 | Before/after report/readback drift and unknown write outcome keep readiness blocked pending exact readback; later external ref advance does not inherit readiness or a lock/merge guarantee | C3/C4 | G/R | f/g/h/i/l |
| PD-01 | Existing already-synced no-op precedes ownership handling; new ready operation with unmarked manual PR and no admission still refuses | D1 | G/R | i/k |
| PD-02 | Exact externally approved manual merged historical delivery is explicitly classified manual and excluded only from conflicting enumeration; new matching owned operation can create/reuse once | D1/D2 | G/R | i/k |
| PD-03 | Mutate repo/branch/PR/base/head/merge/tree/actor/type/approval/ancestry individually; unmerged/reopened/duplicate/ambiguous entries also refuse, without editing receipts/PR body | D2 | G/R | a/i/k |
| PD-04 | Unrelated open/closed PR, spoofed owner marker, unverified/mismatched deleted/recreated branch and closed matching owned operation retain refusal/no-reopen; exact verified owned missing-branch recovery stays non-force as parent D4 permits; manual admission cannot grant ownership; no duplicate/force/fallback branch/historical mutation | D3/K1 | G/R | i/k |

Allocation: A6 + B6 + C7 + D4 = 23. Every A/B/C/D acceptance criterion maps to at least one row. K1 preservation is a shared regression gate on every repair, even though PA-06 owns the focused successor case. K2 is checked at later delivery/closure with actual evidence, not an artificial product test.

## Existing regressions and later evidence

After any separately authorized implementation, run the product/project tests required by that ticket's scope, including publication/current/remote and preserved historical suites, verify-project, native adoption verifier and generated package check. Run unit/lint/build and real isolated candidate build when touched behavior requires them; report CLI/native and browser surfaces separately. Do not turn an existing expected denial into a blanket pass. Historical main/staging suite counts are not promised future totals.

Each future coverage table lists every allocated row/subcase, red/green evidence, pass/fail/not-run, exact source/environment and review/landing links. New regressions uncovered during implementation require an explicit table amendment and owner approval before writing them. No original P01–P24 row is renamed, reduced or marked passed by this plan.

The original P13-a..l remote matrix remains NOT RUN. In particular actual token denial/dispatch/check author, enforced isolated build, strict head/base protection, manual/nonparticipating races, branch lifecycle and actual landing readback still require a separately authorized GitHub lab. Passing all 23 local rows does not close T-0016 or authorize activation.
