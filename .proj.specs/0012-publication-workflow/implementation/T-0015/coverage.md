# T-0015 local synchronization coverage

Approved rows: P09 and the local-ref drift subset of P10. Surface: native public CLI and disposable real Git; fixture plumbing only. No remote, PR, concurrency/API, browser or deployed surface evidence is implied.

| Row | Public behavior | Evidence | Result |
| --- | --- | --- | --- |
| P09 | Clean result equals a separately constructed expected complete file identity map; dirty index/worktree/untracked/source object database preserved | `test_clean_sync_has_independent_expected_tree_and_preserves_dirty_source` | Pass |
| P09 | Main already contained -> no-op; local_ready false | `test_already_contained_main_returns_noop_without_pr_readiness`, actual pinned main/staging reports | Pass |
| P09 | Git conflict exact paths; no result; no ours/theirs | `test_conflict_reports_exact_paths_and_never_materializes_readiness` | Pass |
| P09 | Different-paragraph conflict-free merge changes full candidate blob -> block | `test_conflict_free_different_paragraph_edit_blocks_full_candidate_blob` | Pass |
| P09 | Full metadata, mode, asset ownership, source identity, registry role/delta inventory and protected checks | Candidate metadata/mode/tampering, source-pin, strict registry, immutable history, fixed-role and explicit UI engineering cases | Pass |
| P09 | Historical literal aliases retained; unsafe links blocked; source merge driver/template not executed; output aliases rejected | Alias/custom driver/template/output-parent public cases | Pass |
| P10 local | Main, stage, candidate refs advancing expires receipt; final pins re-read after native merge event | Local pin advance and native wrapper race cases | Pass |
| P09/P10 | Supported help/schema and exact receipt re-verification | `test_schema_and_help_expose_supported_local_operations_without_role_selector`, tampering and clean verification | Pass |
| P10 remote | Coalescing, owned remote branch/PR state, remote pre-mutation refresh | T-0016 allocation | Not measured by this ticket |

Command: `python3 -m unittest discover -s tests/article_publication -p test_staging_sync.py -v`; 23 tests pass. Literal expected tree is assembled from the pinned stage fixture plus one known engineering replacement, independently of the implementation merge algorithm.

13 genuine red -> green cycles are retained: missing CLI (01-cli), no-op status (02), structured conflict paths (03), complete candidate diagnostic paths (04), missing strict ownership validation (05), source identity mismatch (06), allowed exact historical alias (07), stale verdict (08), public schema (09), omitted history check (10), redirected output (11), finite preview UI engineering (13), target ref relabeling (14). Later race, metadata/mode, receipt, custom driver/template cases were immediately green regressions; `additional-template-regression.txt` is explicitly not claimed as a red. The first package-style unittest invocation encountered discovery configuration and is not a behavior red.

Existing Node 24.13.0 / pnpm 10.28.0 reused; no installation. Unit: 54 passing; build/lint pass; structure and materializer (176 generated / 55 source) pass. Local product build is regression evidence, not isolated publication build/browser evidence. Full native runner and current adoption results are recorded separately; parent-owned historical-context/current successor repair is tracked explicitly rather than changing historical assertions.

Actual main 001b26f8e931e0cf1e62373c5aa088a1b5ed09eb and staging 035783590895a426ee395045829ebc9d50e2b9cf were inspected with a finite locally reviewed registry. All six candidates / 50 owned path bytes match the approved M0 stage snapshot. prepare and verify both return no-op, tree a3c0f92567452640a3aeb1943dd2b25ba582de55, publishable=false/local_ready=false. Registry digest is frozen in both reports; authoring the evidence does not grant a future caller self-approval.

No commits, pushes, PRs, branch/target updates or deployment settings were changed. Ticket remains review pending independent code/security review and actual future engineering delivery.

Security follow-up checkpoint: partial/promisor (including local include files), missing/corrupted blob bytes, deleted aliases and omitted fixed historical boundaries are refused. The original 13 red cycles were followed by harmless config/source-object/alias red -> green regressions; corruption required correcting the fixture read-only object mode, not weakening an assertion. Current shared native guard has 3 public cases (real closed targets, fake M0, partial config); new runner preflight has 1 case. The full current-runner checkpoint passed 66 live harness + 43 live publication + 10 immutable #22 cases before these final security follow-ups; final integrated full verification is parent-owned and must not be inferred from that earlier count. Latest actual-final registry/prepare/verify JSON uses mandatory fixed historical checks, returns no-op with all 50 candidate paths and the same actual target pins.

Final post-hardening full run:66 live harness +51 live publication +10 immutable #22=127,
exit0/failures0/errors0. Raw `python-current-final.txt` supersedes earlier119checkpoint for
latest code acceptance, without rewriting that historical result. Standards/Spec/Security
final counts0. Shared current guard protects original historicaltestbytes and validates
actual T13 landing policy/target ancestry without demanding futureticketcode in oldcommit.
No remote/native CI/deployment/HTTP authority is inferred from local_ready.
