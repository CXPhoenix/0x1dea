# Discord verification source alignment

## Problem Statement
The owner-approved Discord domain verification record is published on main and synchronized to staging. The current native Harness guard rejects its exact new path because its source inventory still describes the immutable M0 tree plus engineering-only successors. Accept this published record without weakening any historical contract.

## Solution
Add a finite, trusted current-source successor for the single published Discord record. Activate its requirement only when the candidate target history contains the pinned actual main publication commit. Keep the original M0 baselines, hash-pinned legacy verifiers, five frozen #22/#32 test modules and their assertions, historical receipts and runner context selection unchanged. Only live current-context fixture adapters may change data preparation as explicitly limited below.

## User Stories
1. As the site owner, I want both current targets to pass the source guard with the approved Discord record.
2. As a maintainer, I want missing, modified, linked or unexpected sources to remain rejected and historical validation to retain its previous meaning.

## Implementation Decisions
- Reuse the native adoption CLI, baseline prepare/verify CLI and trusted current-source reconciliation seam. No new CLI flags or caller-selectable trust mode.
- Pin the actual main publication merge `0e690064985d9d734849e1ec44a8c0f8d84fb2a3`; this commit is already an ancestor of staging `87ff977bb11c42b810dfedc34c519052f62fbaa7`.
- The reviewed current control supplies the only allowed record: `blog/public/.well-known/discord`, regular Git mode `100644`, exactly 43 bytes, no trailing newline, SHA-256 `d28142c7a5a13b28d22abaa933cedc2027ce9abbabb2f09c55b989084caa5019`.
- Require that identity on any candidate whose HEAD contains the publication commit. A target prior to that commit keeps the original expected inventory; adding the record to a pre-publication tree is rejected.
- Inspect actual candidate ancestry through the existing trusted Git wrapper. Missing publication history or Git errors fail closed. Do not infer activation from file existence, a candidate policy edit, an environment override or a caller-supplied role.
- Retain exact path-set equality. No directory, suffix, management-tree or well-known-tree exemptions. All symlink parents, a symlink record, executable bits, changed bytes, missing record and extra files remain rejected.
- Preserve the current engineering policy schema and all M0 pins/digests. Update only exact mutable current engineering identities and the finite new spec/ticket/test/evidence entries needed for this repair. Do not add blog content to the engineering common map or rewrite old policy snapshots.
- Live current-context fixture adapters may materialize the one pinned record before invoking an original assertion when they deliberately advance a fixture HEAD into post-publication history. This is fixture data setup only: no change to the five frozen test modules, their assertions, the original historical fixture trees or the runner. No failure-dependent retry, alternate expected result or success substitution is allowed. Current landed-closeout and remote-validation wrappers that construct their fixtures inside inherited test methods need the same before-verification materialization boundary, without editing those frozen method bodies.
- Retain the native CLI's existing role/tracker/landing verification and `publishable: false`. Passing this guard grants no automation, credential, merge or deployment authority.

## Acceptance Criteria
- AC1: Native adoption validation succeeds on separately materialized current main and staging trees containing the exact published record, returns the correct role and preserves `publishable: false`.
- AC2: For post-publication targets, changed bytes (including an added newline), deletion, executable mode, a symlink record and linked parent directories are rejected before a success report.
- AC3: Any additional file under .well-known, another public path, or an unlisted management path is rejected. Editing a candidate's engineering map cannot authorize a changed record or a new public path.
- AC4: Historical prepare projections remain based on the same M0 commits with no new public record; historical target identity checks and cross-role refusal retain their original result. Adding the record to a pre-publication tree is rejected. An unavailable/unresolvable publication pin and any ancestry-query error are refused; only the normal Git non-ancestor result denotes a pre-publication target.
- AC5: The runner and all five frozen test modules are byte-for-byte unchanged; their original #22 and #32 contexts execute successfully. Existing current counterpart suites execute against the reviewed current source. Their live fixture adapters may only materialize the pinned published record at the defined setup boundary before original assertions run; no original assertion, expected result, frozen method body or runner context is changed, and no failure-dependent fallback or test-source substitution occurs.
- AC6: Actual candidate and published blog identities, writing packages, old receipts, M0 inventory and historical verifier pins remain unchanged. Actual current main/staging checks pass with exact policy entries after review. All unexecuted or blocked surfaces are reported explicitly.

## Testing Decisions
Only public native CLI and real disposable Git seams; no tests of private helper internals. Proposed rows D01-D06 are in test-plan.md and require owner approval before new tests or implementation. Reuse existing frozen suites unchanged, extend coverage in a new live test module, and run one failing behavior then its minimal fix per cycle. Expected record bytes and digest come from the owner's literal value and independently pinned published commit, not the implementation's own output.

## Out of Scope
General static-file admission, automatic future ownership records, Discord account interaction, article publication, P13, T-0023 lab reporting, workflow activation, dependency installation, credential/rule changes and deployment configuration changes. No remote commit/push/merge for this repair is inferred from an earlier single-record publication authorization; complete a reviewable local result first.

## Further Notes
This is a new bounded repair. The remote tracker currently ends at T-0022, but prior local work reserved T-0023 for lab reporting; do not reuse that id. Propose one new globally allocated ticket at the approval gate, rechecking all available reservations before allocation. Existing source checkout and unrelated WIP remain untouched.
