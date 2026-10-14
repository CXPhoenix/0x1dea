# T-0013 continuation coverage — 2026-10-14

Owner approved the concrete M0; original M0 input/inventory bytes remain unchanged. Remote
main/staging pins remain eeda8e48… / c6efa7de…; PR20/21 remain OPEN, not landed. All checks
below ran against local main/staging projections with HEAD and target refs at the exact M0
commits. Neither target advances. There is no Git merge, deployment change or remote write.

| Approved row | Actual native seam/evidence | Result | Limits |
|---|---|---|---|
| P01 | Existing 8 inventory CLI cases; approved full M0, sidecar authority and exact successor map | Unknown/overlapping/unpinned data rejected; owner approval recorded | No new article source migration/admission; legacy candidates remain legacy |
| P02 | 10 current CLI cases; prepare both pinned Git trees plus one explicit common patch; full source verification | Published main article retained; no new candidate route/body/asset imported; all 50 candidate paths retained; only existing entrypoint replaced; all new common paths enumerated | Independent local engineering projections, not integration commit or remote landing |
| P03 | Main 66 harness/34 publication tests; staging 95 harness/34 publication tests; current adoption both roles | Existing assertions unchanged; historical original verifiers retained byte-for-byte and loaded from hash-pinned Git objects. Current target role comes from executing trusted control checkout; cross-role candidate, policy waiver, candidate/history overlay, literal alias drift rejected | Trusted control code/policy must be reviewed. Executing unreviewed candidate tools is outside contract; downstream consumers must bind target/base fields. No CI activation |
| P23 | Missing landing and generic M0-ancestor receipt cases, live tracker validation | T13 cannot become done without real main/staging commits containing the engineering successor and actual authorized target ancestry | No authorized real landing; T13 remains review, downstream tickets remain todo/blocked |

## Actual commands and outputs

- `python3 scripts/run-python-tests.py`: main 66 harness + 34 publication; staging 95 harness +
  34 publication. Actual discovery counters, zero failures/errors in adjacent python logs.
- `pnpm test:unit`: main 54/54 (6 files); staging 87/87 (8 files).
- `pnpm docs:build`, `pnpm lint`: both pass, raw outputs adjacent.
- `python3 scripts/verify-harness-adoption.py`: both current roles pass. The prior unknown
  CLI rejection is resolved by exact successor validation, without broad exemptions.
- `python3 scripts/verify-project.py`, `python3 scripts/materialize-writing-skills.py --check`:
  both pass (main 176 generated/55 source files; stage 178/56). Existing three writing
  packages are unchanged for their respective target role.
- Existing Node 24.13.0/pnpm 10.28.0 dependencies reused temporarily, link removed after
  checks. No installation. Local builds are regression checks, not isolated publication
  build/scan or actual HTTP/browser/production proof.

## TDD and defects found

Public tests first exposed missing prepare/verify seams, missing native successor routing,
missing done/real-engineering-landing guards, unknown controller-topic handling, broad policy
overlays, normalized alias bypass and missing projection target refs. Each implementation
followed its observed failure. Already-covered negative byte/policy cases were added as
regression checks without inventing a failure. Existing fixture assertions were not changed.
The compatibility wrapper's missing exported constants was diagnosed by actual harness
errors; restoring the constants made the original tracker and full suites pass. Detached
projection clones originally lost target refs in nested clones; preserving the pinned refs
fixed old landing fixtures without weakening their assertions.

All unchanged source, route, article metadata and asset identities are checked against pinned
M0 trees; explicit common successors have mode/SHA-256 records. The earlier reviewed-delta.proposed.json is a pre-evidence checkpoint, not the final
map. The final finite successor is maintenance/publication-workflow/engineering-v1.json;
source-delta.json captures the final engineering source identities without a self-hash cycle. New current policy never refreshes itself from
candidate/live hashes; authoring the finite proposed boundary is separate from validation.

Independent Standards and Spec review: zero unresolved P0/P1/P2; security review: no qualifying
HIGH/MEDIUM candidates. The CLI documentation-only followup was confirmed by both code axes.
Final report-only additions are explicitly outside the original source capture; all reviewed
behavioral source hashes remain unchanged. Final exact verification is recorded separately.
