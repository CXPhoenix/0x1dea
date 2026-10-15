# T-0013 coverage report — inventory checkpoint, not ticket closure

Surface: local Python CLI/disposable Git fixtures, pinned real Git trees, native validators,
Vitest and local VitePress build. No GitHub mutation, browser/HTTP, served SHA, real integration,
merge, live automation or deployment verification. No installation. Node 24.13.0 / pnpm
10.28.0 reused existing dependencies through a temporary link removed after unit/build checks.

| Approved row | Evidence | Observed result | Coverage limit |
|---|---|---|---|
| P01 | `python3 -m unittest discover -s tests/article_publication -p test_baseline_inventory.py -v`; real `publication-baseline.py inventory` | 8 public CLI cases pass; full 1831/2174-path trees, 363 exact classifications; unknown/stale/overlapping owners rejected; open prerequisites not landed; full commit pins, duplicate JSON, trust/role/category input, overlays and literal patch paths covered | Proposal only; no clean source admission or authenticated remote prerequisite receipt |
| P02 | Inventory CLI read-only fixture and candidate deletion/retention cases; concrete candidate ownership registry | Exact modes/blobs and main published revision retained in output; source checkout unchanged | Engineering baseline preparation and independent staging integration NOT implemented or verified; pending concrete M0 approval |
| P03 | Unchanged harness suite (66) and unchanged article-publication suite (16), plus 8 new inventory cases; `materialize-writing-skills.py --check` | 66 harness + 24 publication tests pass; v1 rejection assertions retained; 176 generated files match 55 sources | Shared current role/successor NOT implemented; direct current adoption check fails closed on new unapproved CLI path |
| P23 | Existing historical tracker cases, proposal prerequisite records; all six local ticket statuses audited | No ticket marked done; T13 processing, downstream todo with explicit blockers | Actual authorized main/staging landing NOT exercised or claimed; current landing successor remains open |

## Check results

- Before implementation: historical harness 66/66; article publication 16/16.
- Final local suites: harness 66/66, article publication 24/24 (including 8 new CLI tests),
  Vitest 54/54 across 6 files. Raw outputs are adjacent.
- VitePress local build: pass. This is a local regression check of the main-based site,
  not an isolated selected-article build/scan or HTTP/browser acceptance.
- Project structure: pass. Materializer: pass. Raw exit codes and output in checks.json.
- **Current adoption verifier: FAIL**, exit 1, `unknown publication source:
  scripts/publication-baseline.py`. The original guard is unchanged and still excludes new
  unapproved sources. No hash refresh, folder exemption or assertion change was introduced.
  This checkpoint is not landable; the explicit exact successor is remaining T13 work after
  concrete M0 review. Passing fixture suites does not override this failed current check.

Each inventory behavior was written as a failing public CLI test, then implemented and
rerun green before the next behavior. Cycles: complete trees/revision, exact classifications,
ownership conflicts, open prerequisite and shared patch record, pins/schema/trust refusal,
history overlays, candidate deletion, literal Git patch paths. Existing assertions were not
edited. Fixture Git commits create disposable test history only; no project delivery commit
was made.

## Scope and next gates

No existing tracked source, candidate content, three canonical writing packages, generated
runtime package, historical fixture or deployment setting was changed. New ADR-0008 records
the owner-approved design without changing ADR-0006. A successful inventory is never trusted
policy. Concrete owner M0 review, the exact successor/baseline implementation and remaining
P02/P03/P23 coverage precede delivery/closure. T14–18 remain blocked by the approved graph.
