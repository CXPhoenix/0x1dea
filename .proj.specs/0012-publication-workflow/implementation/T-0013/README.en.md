# T-0013: M0 inventory implementation checkpoint

Status: partial implementation; owner review of concrete M0 is pending. No baseline PR,
trusted current successor, integration, landing or ticket completion is claimed.

## Public interface

`python3 scripts/publication-baseline.py --help`

`python3 scripts/publication-baseline.py inventory --repo . --classification .proj.specs/0012-publication-workflow/implementation/T-0013/M0-classification.proposed.json`

The CLI prints JSON only after complete validation. Schema version 1 here denotes the
**inventory classification format**, not the article publication plan v1 or future v2.
It is read-only and does not prepare a publication tree, merge, deploy or admit a candidate.
It reads pinned Git trees, not the dirty working tree or a served website. JSON observations
are input evidence, not authenticated GitHub receipts. No input can declare itself trusted.

Classification keys are exactly the changed paths. Each has `category`, `owner`, and optional
boolean `shared`. Categories are published, candidate, engineering, historical-management,
current-management and target-role. Shared changes carry exact full-index patches. Every
candidate path has one owner, including unchanged owned assets; candidate deletions retain
the published main state and record staging absence. All current source candidates are
explicitly `legacy-requires-migration`; this tool never labels them clean. Prerequisite
observations bind a PR, state, target, full head and optional merge commit; landed requires
both a MERGED observation and local merge ancestry. Observation authentication remains
outside this proposal-only interface.

No category or path is an exemption from a validator. Noncandidate main actions remain
pending exact review. Candidate main actions retain published state (including absence of
new candidates), while staging actions preserve the pinned state exactly.

## Concrete review material

- [M0 classification input](M0-classification.proposed.json)
- [Full trees, hashes, modes, differences and shared patches](M0-inventory.proposed.json)
- [Owner-readable M0 review](M0-review.md)
- [Coverage and verification](coverage.md)

The concrete M0 is not approved merely because the abstract spec/test plan was approved.
The spec D1 says: "M0 is approved before it becomes trusted policy". Continue the engineering
baseline/successor implementation only after the concrete boundary is approved; any later
exact successor update receives equivalent review. There is no broad management waiver.

## Remaining T-0013 work

Implement and review the exact main engineering projection, shared current validation with
trusted target/base role selection and versioned exact successors; validate independent
staging integration without losing candidates. Obtain applicable delivery authorization and
actual main/staging landing receipts. P02, current-successor P03 and landing P23 remain open.
T-0014 through T-0018 remain dependent on done upstream tickets.
