# Proposed test plan — approval pending

No new test or product implementation has been written. The original native CLI was run on a fresh latest-main clone and failed solely with `current reconciliation source inventory mismatch: blog/public/.well-known/discord`.

| Row | Seam | Test intent | Scope | Acceptance criterion | Boundary conditions |
|---|---|---|---|---|---|
| D01 | native adoption / baseline verify CLI + real Git | accept exact approved record on actual main and staging projections | new live regression, first red | AC1 | correct trusted role, 43-byte body, publishable false |
| D02 | native CLI candidate mutation | refuse missing/modified/newline/executable/symlink record and linked parent | focused public negative cases | AC2 | explicit refusal, no success JSON, include every execute bit |
| D03 | native CLI + candidate policy mutation | refuse extra well-known/public/management sources and attempted self-approval | focused public negative cases | AC3 | exact path-set equality preserved |
| D04 | existing prepare/native CLI + before/after publication Git histories | old projections retain exact inventory; pre-publication addition and unavailable pin/query errors refused | new public regression + existing contracts | AC4 | normal non-ancestor distinguished from query error; no caller role/trust override |
| D05 | existing full current Python runner + Git hashes | run unchanged live suites and original fixed #22/#32 contracts | no edits to runner/frozen modules; live adapters may supply pinned record before assertions | AC5 | fail closed on changed/missing historical modules; no fallback |
| D06 | independent Git mode/blob/byte comparison + actual native commands | preserve all unrelated blog/candidate/history/M0 assets and validate both actual target trees | read-only acceptance checks | AC6 | no install, no external authority inferred |

## Proposed ticket breakdown
One independent repair ticket: accept the exact published Discord source identity in the current Harness guard while retaining historical contracts. No dependency on T-0016 or T-0023; neither ticket is closed or repurposed. Recheck global ids before allocating, retaining the known local T-0023 reservation.

## Implementation sequence
1. After approval, allocate one ticket/branch under tracker conventions and mark processing.
2. Add only D01 at `tests/article_publication/test_published_static_successor.py`; observe native failure before product edits.
3. Keep the five frozen modules and runner untouched. Adjust only live current fixture data preparation in `tests/article_publication/test_current_history_context.py` (and a finite live test helper if needed) so every deliberately advanced post-publication fixture supplies the exact pinned record before original assertions; include inherited landed-closeout/remote-validation constructions, without changing their frozen method bodies or expected results.
4. Change `scripts/publication_current.py` with one finite ancestry-gated exact identity addition. Update only exact current identities in `maintenance/publication-workflow/engineering-v1.json` so the native guard can inspect the new source and evidence; keep every historical entry/pin unchanged.
5. Run D01 green, then D02-D04 one behavior at a time, retaining red/green vs already-green regression evidence truthfully.
6. Run D05/D06 and structure/materializer/diff checks. Use existing dependencies only if required by the full runner; no installation. Use actual main/staging named refs in disposable fixtures.
7. Capture stable review packet; run independent Standards, Spec and security reviews, resolve findings, then refresh affected checks.
8. Produce measured coverage table and a local reviewable result. Any later remote delivery must match current owner authorization and use project message skills.
