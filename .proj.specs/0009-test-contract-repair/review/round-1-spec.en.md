# Deterministic verification and exact current-source acceptance

## Problem Statement

Historical verifier tests overlay mutable checkout files on pinned Git epochs.
Later valid product work therefore breaks their accepted fixtures and masks the
intended rejection diagnostics. The live preservation contract lacks successors
for later components, captions and writing material. The article migration case
confuses a frozen conversion with subsequent author edits. Python tests have no
complete documented entrypoint, and tracker JSON disagrees with its documented
Blocked view. Old execution receipts cannot establish that the current checkout
passes.

## Solution

Keep historical proof immutable, test historical accepted inputs against the
current verifier, and accept the exact owner-approved current source increment
through a bounded successor. Run both Python suites and Vitest through documented
commands. Preserve current article bytes and report unresolved dependencies
separately from the todo-only Blocked view. No historical authorization is inferred.

## User Stories

1. As a maintainer, I want historical fixtures independent of live editorial and
   product changes so regressions exercise their intended cases.
2. As an auditor, I want exact current source acceptance and retained historical
   proof so passing checks cannot hide unapproved inputs or tampering.
3. As a contributor, I want a complete test command and accurate ticket views so
   missing tests or incomplete landing evidence remain visible.

## Implementation Decisions

The approved unit is one ticket, T-0009, with no dependency edge. Requirement
convergence, ticket granularity and the six-row test table were explicitly
confirmed by the owner on 2026-10-11. Existing CLI and renderer seams are reused.

Historical component fixtures read accepted product bytes from
69ff85f5fe1baddb54102070a436dff9ac1c5b73; article-revision fixtures read accepted
revision bytes from f93237b1ed538484f24ed103ef00c7e5ee2e1828. They execute the
current verifier implementation. Missing objects fail the test rather than skip
or substitute checkout bytes. Existing negative assertions retain the offending
path or provenance condition. Fixture construction never alters the source checkout.

The original article baseline JSON remains byte-identical. A portable historical
entry fixture is reconstructed from f3eee3db6c9056b1bfd308756e2790c46513b174 plus
the separately documented task-entry shorter figure-1 caption. Its SHA-256 must be
9ee10b2b8afe41d6d201df259ed95c58e869bd5592bbaa4995d603f5823f265e, the existing
independent oracle. Freeze its migrated counterpart as test data, record both
identities and provenance, and retain the inverse-conversion assertion and source
links at the public Markdown renderer. Test the live article separately for three
figures, six references, eight original alt/src pairs, unchanged frontmatter and
source-note citations. Do not restore older prose or require source links to stay
inside captions after an editorial move. The live article remains byte-identical
to captured HEAD 6e4eb804bcbda8504935be49fd6537d6327d5303.

One new exact successor record has a reviewed digest and two sections. The product
section is the complete protected-source delta between predecessor
f93237b1ed538484f24ed103ef00c7e5ee2e1828 and captured source
6e4eb804bcbda8504935be49fd6537d6327d5303, excluding only existing management
ownership rules. Both commits must exist, be ancestors of actual HEAD, and have
the declared ancestor relationship. Validate the exact complete path set,
before/after modes and hashes against Git objects and the previously accepted
current projection. The repair section enumerates only the reviewed README,
package test scripts, article test and new frozen data/package initializers.
Reject duplicate, missing or extra entries, changed record bytes and unsupported
file types. The exact lists are frozen in the accompanying scope artifact and
reviewed guard code; expected values never refresh during verification.

The successor requires the existing staging, component and revision provenance.
Its absence retains prior fail-closed behavior and still supports pristine older
epoch fixtures. After it is validated, check every protected current byte/type
and reject unknown sources independently of Git ignore rules. Keep all original
epoch/provenance records unchanged. Validate historical package semantics against
the historical projection, while the separate current guard enforces the exact
new package scripts. Reviewed guard, test-runner and guard-test code is explicitly
enumerated code, not circularly self-authenticated hash data. No directory-wide
source allowance or CLI bypass is added. Future product changes still need review.

Add package initializers so direct root unittest discovery reaches both existing
suites. A standard-library runner discovers the two named suites, executes both,
prints their actual counts and returns nonzero for any failing/import-error suite
or either zero-test suite. Its optional tests-root argument supports disposable
CLI fixtures; the production default is the project test root. Aggregate package
commands retain test:unit, add test:python and test, and propagate failures. Use
the installed Python, Node and pnpm without dependency or lockfile changes.

Tracker JSON adds unresolved_dependencies for every ticket with non-done blockers;
blocked filters that map to todo tickets. Existing frontier and paused semantics,
dependency validation and done authorization/landing checks remain unchanged.
The view change does not remove edges or authorize closing tickets. Record the
missing T-0005 landing receipt and retain review unless authentic authorization
and actual staging containment can both be established. This reconciles the
view with the existing tracker document and ADR-0002; it does not redefine done.

Move only the observed ignored Finder metadata file to an ignored local backup
after recording its size/hash, verify backup bytes, and retain a local receipt.
Do not exempt metadata from the source guard or delete unrelated files. Append
new version-qualified validation notes to affected reports without rewriting
old execution results. Remove volatile branch/landing assertions from current
context documentation in favor of verified Git and receipt lookups.

## Acceptance Criteria

- V1: Existing historical acceptance and tamper tests pass against the current
  verifier after later checkout changes. Immutable inputs match their records;
  missing pins fail; negative cases still identify their intended offending input.
- V2: The historical article fixtures preserve the independently pinned original
  SHA and renderer/source-link/inverse-conversion assertions. The current article
  separately renders three figures, six references and eight unchanged alt/src
  pairs, retains frontmatter and source-note citation links, and its bytes equal
  captured HEAD. Original baseline JSON is unchanged.
- V3: The current public CLI passes the exact reviewed successor and repair
  delta. Record/delta/pin/history tampering, missing/non-ancestor objects, changed
  bytes/modes, missing/linked sources and extra/ignored source paths reject with
  nonzero results. Original manifests and old authorization records are unchanged.
- V4: Direct root discovery reaches both suites. test:python runs each with a
  positive count; test runs Vitest and Python. Failure, import error or a zero-test
  suite returns nonzero; no existing test is removed or skipped to pass.
- V5: blocked contains only todo tickets with non-done dependencies;
  unresolved_dependencies also exposes those edges for processing/review tickets.
  Frontier, pending, cycle/missing-id and invalid-landing counterexamples retain
  their existing behavior. Missing T-0005 landing evidence is explicitly retained.
- V6: No existing ticket becomes done without authentic authorization and actual
  staging containment. If either is missing, review and the missing-evidence
  reason remain. Historical local/remote observations are not deployment proof.
- V7: The single Finder metadata file has a matching-hash local backup and receipt;
  its original scanned path is absent. No other file is removed or exempted.
- V8: Fresh complete Vitest/Python, lint, VitePress build, structure, materializer
  and public-verifier results reference the final repair state. A coverage table
  and independent Standards/Spec/security reports record their actual scope and
  any limits. Existing historical pass/fail results remain identifiable as such.

## Testing Decisions

Use the approved six-row plan unchanged in seam and scope. One actual failing
behavior, minimum fix, then the next; existing reproduced failures are legitimate
red evidence, not new retrospective TDD. Fixtures execute real Git, Python CLI and
VitePress Markdown interfaces. Test-runner failure fixtures are disposable minimal
test modules, not mocks of internal collaborators. Check positive controls before
negative probes so an unrelated early failure cannot masquerade as coverage.

The existing non-browser Git/subprocess harness covers this tooling repair per
ADR-0006. Run the full aggregate suite once after affected green runs and execute
all required local tooling. Build verifies compatibility; no website behavior is
changed and no new browser acceptance claim is made.

## Out of Scope

Commit/push/PR/merge/deployment, external-index changes, installations, global
settings/credentials, article rewriting, new browser features, a general approval
registry, automatic expectation refresh, weakened guards, and fabricated past
approval or landing evidence.

## Further Notes

The owner's authorization is present-day reconciliation of this captured state,
not a claim that the earlier T-0007/T-0008 work met every historical gate. Rollback
reverts the repair's guard/data/test/command changes together and restores the
backed-up Finder file only if that path is absent. It restores prior failures
rather than changing product bytes or old manifests. Ticket remains review after
local delivery; landing is not authorized by this task.
