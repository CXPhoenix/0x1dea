# Proposed test plan — owner confirmation required

Status: not approved. No new implementation tests have been written or executed.
The table approves test intent and seams, not remote access, installation or publication.
One TDD cycle at a time after the approved breakdown; implementation file layout is deferred.

Seams: **E** existing disposable Git/CLI/native validators; **N** new v2/sync interface;
**A** new GitHub/Actions adapter; **R** expressly authorized real remote exercise;
**W** actual website HTTP/browser; **S** draft skill behavioral evaluation.
An R/W check unavailable without authority or surface evidence is blocked, never a local pass.

| ID | Seam | Setup / action | Pass/fail evidence | AC |
|---|---|---|---|---|
| P01 | E,N | Full two-tree inventory with A/B, unpublished revision at an existing path, open prerequisite PR, unknown path and overlapping ownership | Complete modes/hashes/classification; unknown/overlap blocks; open PR not treated landed | 01,04 |
| P02 | E,N | Prepare reviewed engineering baseline, then integrate while A/B stay pending; inspect whole trees | Main diff exact allowlist and approved patches; every candidate blob/time/image/mode preserved; protected URLs unchanged | 02 |
| P03 | E,N | Run unchanged historical fixture suites and new target-role/successor cases; attempt candidate-selected permissive role and broad management exemption | Old expected results retained; only trusted exact successors accepted; role spoof and broad waiver fail | 03 |
| P04 | E,N | A/B start on pinned main; merge A then B into staging using explicit integration commits; try v1 then v2 | V1 retains original rejection; v2 accepts registered clean A, candidate exact main+A/dependencies | 03,04 |
| P05 | E,N | Merge staging into A; independently add B then revert B in A; include another article ancestor | Each source rejected even if final tree contains only A | 04 |
| P06 | E,N | Refresh main, source main-merge, explicit dependency and conflict-resolution variants; truncate history or introduce unknown merge | Valid reviewed main refresh works with new pins; stale/unknown/incomplete/unreviewed merge fails | 04 |
| P07 | E,N | Omit B or B asset/revision; overlap ownership; put B text in a permitted shared index patch | Inventory/ownership mismatch fails; shared path permission cannot admit undeclared B content | 01,04,08 |
| P08 | E,N | Legacy mixed source; reconstruction with/without exact original/new pin and owner migration approval | Unapproved reconstruction blocked; approved provenance accepts only reviewed bytes; old fixture unchanged | 03,04 |
| P09 | E,N | Clean merge, already-synced graph, conflict/check failure, and main/B-candidate edits to different paragraphs of one published article | Valid tree equals independent merge; no-op creates no PR; even conflict-free changes to registered candidate modes/blobs/metadata block readiness and preserve targets | 05 |
| P10 | N,A | Repeat same event, coalesce main events, advance stage during validation; wrong owned branch and closed/open PR variants | Latest pins read; one owned open PR maximum; stale result reruns; no force/unrelated mutation | 05,06 |
| P11 | N,A | Concurrent preview/publication/sync writers and manual drift; simulate accepted-but-lost API response, 403, timeout | Participating writers serialized; readback before retry; at most three retries; no duplicate or target mutation | 05,06 |
| P12 | A | Suppressed push check, dispatch acknowledgment only, stale/failed/missing run; candidate shell payload/policy edit/token access | Exact trusted run required; no readiness for these failures; no shell execution or writer-token exposure | 03,07 |
| P13 | R | Separately authorize test-repository exercise of token scope, dispatch/run identity and protected latest-base checks; race base/head | Actual remote receipts prove conditions, or activation blocked; no main/staging merge in production | 07,09 |
| P14 | E,N | Select A; B is both a new article and an unpublished change to an existing article; include exact dependency | Whole candidate manifest equals main plus only approved A/dependency changes; B body/assets absent, published state retained | 02,08 |
| P15 | E,N | Pair valid baseline B published routes/listings/assets with B revision additions; include unauthorized listing, custom route, search/RSS data and exclusive public assets | Baseline B output allowed; unapproved additions fail source or supplemental output checks; homepage-only inspection insufficient | 08 |
| P16 | E,N | Tamper receipt/blob/mode, add symlink/submodule, escaping include or executable import; fail enforced isolation sentinel | Verify/build readiness fails; no external read/write/network; source checkout and dirty files preserved | 07,08 |
| P17 | E,N | Reviewed isolated real VitePress build; absent runtime/isolation, missing output signatures, forged inventory | Separate actual build and scan receipts; failed/missing/blocked/exclusion-unverified required result blocks PR-ready; scan alone insufficient; no installation | 08 |
| P18 | E,N,A | Approve exact served preview and candidate; advance source/dependency/main/policy/head/tree; model head-only merge guard and observed tree mismatch | Binding changes expire approval/readiness; latest base enforced before activation; observed mismatch incident, no landing success claim | 09 |
| P19 | W | At one existing staging alias, open A/B candidate pages, the candidate revision at a published path, listing and navigation; later inspect authorized production | Actual HTTP/browser evidence matches pinned rendered revisions and served SHA; missing candidate/listing/wrong revision fails; unavailable website blocks; branch tip/local build cannot substitute | 09 |
| P20 | E,N | Land A in fixture graph, sync staging with B; introduce new A revision; reviewed revert/re-publication with unrelated published C | Only landed A identity retired; B/new A remain; revert/re-publication use current pins and preserve C | 09 |
| P21 | S | Independently exercise draft skill on local preview, A-only PR request, sync conflict and missing-v2/interface workflow | Correct scope and mode; preserved local path; inventory-only fallback stated; unavailable/unauthorized actions stop without fabricated commands or receipts | 10 |
| P22 | E,S | Validate draft; compare retained references; after authorized implementation materialize both runtimes and inspect discovery | Draft frontmatter/references valid; old references identical; future four-package catalog and invocation policy preserved | 03,10 |
| P23 | E,N | Main-only landing, sync PR-ready, actual stage ancestor+approval, article preview-only states | Done refused until actual authorized staging ancestry and all ticket ACs; additional publication/main receipts as specified | 10 |
| P24 | E,S | Diff/status audit of this planning round and future dry-run refusal cases | Only new epic planning/draft artifacts; no tickets, deployment/active skills/config, implementation, commits or remote writes | 06,10 |

## Approval and later close-out

Owner confirmation must cover N/A seams, the R activation gate, evidence-limited W checks,
and the proposed sync operation branch lifecycle. No live test repository creation or
credentials are authorized here. R can use an owner-designated existing disposable repository
after explicit authority; credentials are never copied into fixtures.

This round may execute P21 and the **draft-only** portion of P22/P24 as authoring validation,
which is not product TDD or evidence that v2/automation exists. All other rows are future
implementation acceptance. At ticket closure report each applicable row with command/run,
pins, observed result and surface; skipped/blocked is not covered. Keep historical failures
as regression fixtures rather than editing their expected outcomes to make the new flow pass.
