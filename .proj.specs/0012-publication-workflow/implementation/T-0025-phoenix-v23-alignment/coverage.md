# T-0025 coverage report

| Row | Existing seam | Measured coverage | Acceptance criterion | Uncovered / why |
|---|---|---|---|---|
| W01 | P02/P22; public CLI and unchanged materializer | One positive test, both main/staging engineering projections, all ten pinned files and both materializer checks | Exact source, mode, deterministic packages | Not a new style-quality evaluation |
| W02/W03 | P03; public verifier | Three negative methods: all ten byte changes with policy repinning; missing entry/file, symlink, owner/group/other execute bits; unlisted reference; restored state succeeds | Finite writing successor, protected remainder | No new role or remote surface |
| W04 | P03; historical/current runner | 13 protected hashes retained; complete unchanged runner 248 cases, groups [66, 158, 10, 14], exit 0; raw receipt/log retained | Historical validators, frozen tests, runner, M0 unchanged | Do not infer a full-suite pass from focused tests |
| W05 | P02; Git/filesystem | Main's 74 blog entries unchanged; original 112 website entries, 50 candidate paths and 736 backup descendants unchanged | No article publication or backup mutation | Future post-landing readback remains pending |
| W06 | P22; actual physical packages | Canonical and both runtime packages at exact v2.3; context pointers resolve; invocation policy retained | Package discovery and source provenance | No fresh host reload/cross-model behavior claim |

Core independent code/security reviews are in review/code-T-0025.md and review/security-T-0025.md. Focused result: four tests, exit 0, 66.605 seconds. Initial red is preserved. A macOS temporary alias made the first materializer invocation fail; the new test now resolves its own temporary path without changing assertions or materializer behavior. Current structure/materializer/native and full regression results are recorded only after execution. This is local verification, not article publication, P13 or automation readiness.

Full execution uses the never-published aligned QA context in qa-context.json. The initial actual-ref run is preserved as failed (one PC01 policy merge conflict); original assertions, fixtures and runner remain unchanged. QA main website tree equals actual main; QA stage website tree and 50 candidates equal actual stage. Independent Standards/Spec/security reviewers verified this context.

Full execution finished 2026-10-21T17:30:02.088188+00:00. This archive was added after that run; final native/structure/materializer cover the completed archive. Program/test source and all ten writing identities remain equal to the tested snapshot. Actual main landing and post-commit PC01 are not yet observed.
