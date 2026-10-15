# GitHub Flow with a shared staging preview

Status: proposed; direction approved, detailed spec and test plan awaiting owner confirmation.
Epic: 0012-publication-workflow. No implementation ticket allocated by this document.

## Problem Statement

The owner needs one staging website for reviewing several candidate articles, while the
current main tree contains only approved publication content. Engineering changes currently
need separate projections and repeated reconciliation. Selecting one article must not publish
the other candidates, including unpublished revisions to an already published article.

The existing version-1 publication verifier rejects any source with staging-only ancestry.
That includes a clean article topic already integrated into staging. Simply relaxing that
check would also admit staging integration history and other candidates. Historical tests
and immutable evidence must keep their original meaning.

## Solution

Use main-based ticket topics and PR review, with staging as the shared integration preview.
Establish one reviewed engineering baseline. Subsequent engineering changes land on main
once; automation prepares and validates a main-to-staging PR. Article topics integrate into
staging for review; a separate, explicitly selected publication PR starts from current main.
No workflow merges the whole staging branch into main. Initial automation opens/updates
PRs only; it does not merge them. Website deployment settings remain unchanged.

## User Stories

1. As the owner, I want all candidate articles on one staging preview so I can review them
   together without managing a separate URL for each source branch.
2. As a maintainer, I want one engineering change and a validated synchronization PR so I
   do not maintain two implementations of the same fix.
3. As the author, I want to approve one exact article revision and its necessary dependencies
   so only that publication content enters main.
4. As a reviewer, I want preserved historical contracts and current provenance so an easier
   workflow cannot silently weaken the checks that caught past defects.
5. As an agent user, I want a project skill that distinguishes preparation, authorized remote
   changes, landing and production verification so the same rules are followed next time.

## Implementation Decisions

### D1. Authority, roles and migration boundary

- Main is the stable engineering baseline plus approved publication content; staging adds
  public candidate content and preview-only behavior. Candidate means an unapproved article
  **or revision**, even if its path also exists on main. A source branch does not require its
  own deployed URL. The actual shared preview alias and served commit must be inspected,
  not inferred from the branch name.
- This round produces reviewed planning and a skill draft only. Ticket creation, new tests,
  implementation, active skill replacement, commits, pushes, PR creation and all merges are
  outside this round. The owner's later confirmation approves the spec and proposed seams;
  external actions still require their own applicable authorization.
- Before implementation, refresh remote refs and open delivery PR states. PRs 20 and 21 were
  open at the planning observation; their changes are not assumed landed. Use actual landed
  commits or separately reviewed equivalents as prerequisites, without auto-merging them.
- Migration creates an owner-reviewed boundary record M0 containing repository identity,
  full main/staging commits, baseline classification, candidate registry, historical contract
  versions and source migrations. Unknown or ambiguous ownership blocks the affected action.
  M0 is approved before it becomes trusted policy; later updates receive equivalent review.

### D2. Common engineering baseline

- Inventory the complete main/staging trees and differences. Classify every changed path as
  published content, unapproved candidate content/revision, common engineering, historical
  or current management evidence, or target-role configuration. Record before/after modes,
  blob hashes and additions/deletions; shared paths also carry reviewed content patches.
- Prepare a main-based baseline PR with only explicitly approved engineering/management
  changes and target-role policy. Candidate bodies, unpublished article revisions, exclusive
  assets and listing entries are excluded. No folder-wide exemptions or whole-file ours/theirs.
- Integrate that baseline back into staging with reviewed conflict resolutions. Every
  unapproved candidate blob/mode and article metadata remains identical to the inventory,
  except for separately approved source edits recorded in M0. Published URLs remain stable.
- Share validation implementation while choosing the target role from trusted target/base
  context, never an arbitrary candidate flag. Preserve historical validators, fixtures,
  hashes and rejection assertions. Current engineering/tracker evolution uses an explicit
  versioned successor with exact reviewed boundaries; historical snapshots do not become
  a mutable tracker oracle. Preserve all three existing writing packages unchanged unless
  a separate approved change requires their exact successor.

### D3. Version-2 article provenance

- Keep the version-1 CLI schema, semantics and historical fixtures unchanged. Add an explicit
  version-2 plan/admission interface; unsupported versions fail. It must not reinterpret a
  version-1 success or change its intentional local-only publication flag.
- A trusted registry inventories **all** unapproved staging articles/revisions and their
  exclusive assets, exact source commits and shared dependencies. It binds full commit ids,
  per-path modes/blob hashes and reviewed content patches for shared paths. Registry input
  comes from owner-reviewed policy, not self-asserted article metadata. Omissions or unknown
  differences in the pinned staging inventory block admission.
- Each source descends from pinned current main. Check every reachable non-main commit,
  not just the final diff: ordinary commits modify only registered source-owned paths and
  reviewed shared-path content; merge commits may merge an ancestor of pinned main only,
  and their tree must equal an independent conflict-free merge, or an explicitly reviewed
  conflict-resolution tree. Dependencies are separate registered sources, not permission to
  merge arbitrary topics. Incomplete history, unknown commits or ownership fail closed.
- Post-M0 staging integrations use merge commits with previous staging as first parent and
  the clean topic as second parent. Their integration commit ids cannot occur in a source's
  non-main history. The topic's own commits may be reachable from staging: that is normal
  preview integration, and is a required positive case. Other candidate commits, including
  add-then-revert histories, remain forbidden. Main merges into topics require fresh pins;
  staging is never merged back into topics. Do not rewrite integrated topic history.
- Legacy sources without this provenance remain blocked until an owner approves a migration
  record: original commits, exact extracted paths/modes/blobs, reconstruction diff on pinned
  main, ownership review and new source commit. Approval establishes a new reviewed source;
  it does not assert the old history was clean or erase any old rejection test.

### D4. Main-to-staging synchronization

- On main changes or an explicitly requested retry, read current main/staging refs; event
  payload commits are hints only. If main is already an ancestor of staging, return no-op.
  Otherwise compute an independent merge of those pins in disposable storage and validate
  it as staging. Conflict or verification failure leaves target refs unchanged and reports
  exact paths/checks. Never choose ours/theirs automatically.
- After the ticket breakdown is approved, designate one permanent ticket branch for routine
  synchronization. Reuse that exact branch for operational runs, never for unrelated feature
  work; implementation and conflict repairs use their own ticket branches. This preserves
  one branch per ticket. Do not reuse an existing branch with an open unrelated delivery PR.
- At most one open owned sync PR targets staging. Bind repository, target, main/staging pins,
  policy version and expected result tree in an idempotent operation record. Advance the
  owned branch without force, merging refreshed pins if necessary; its result must equal
  the independently computed tree. A different result or branch ownership mismatch stops.
  A missing/deleted owned branch can be recreated only after checking PR/operation identity.
- Serialize participating sync, preview integration and publication mutations in a shared
  repository write group. Do not cancel a running writer. Coalesced events re-read latest
  refs; ordering is not assumed FIFO. Re-read refs before remote mutation; any drift expires
  the result and restarts preparation. An unknown API outcome triggers readback before retry;
  at most three retries per run, then stop with an actionable record, never a duplicate PR.
- Open/update the validated PR only with authorized push/PR scope. No direct staging update,
  force push, branch deletion, automatic merge or deployment-setting change is performed.
  Human merge remains required in the initial design.

### D5. Automation trust and checks

- Plan a repository-scoped automation token with only the writer permissions required for
  its owned branch, PR and explicit validation dispatch. The writer executes trusted main
  policy, not candidate builds. Build/validation executes with read-only credentials, no
  writer token and the existing enforced build isolation contract. Treat source text, API
  fields and receipts as data; never interpolate them as shell programs or executable policy.
- Do not rely on a bot push/PR to run all checks. The proposed default explicitly dispatches
  a trusted validation workflow from main with pinned inputs. A dispatch acknowledgment is
  not success: bind the resulting run, conclusion, base/head/tree and policy to the operation.
  Only success for the exact inputs satisfies validation. A missing run, timeout, refused
  permission or stale conclusion blocks PR readiness; readback/retry is bounded as in D4.
- Before activation, inspect actual repository permissions, required checks, merge methods,
  branch protections and validation dispatch support. Verify exact-head/latest-base checks
  through an expressly authorized remote exercise. No credential installation, repository
  rule changes or live automation activation is implied by this spec.
- A local mutex cannot lock manual GitHub writers; the merge API head guard is not a base
  compare-and-swap. PR readiness is pinned, not a guarantee of a later merge tree. Require
  up-to-date protected checks or an equivalently verified merge queue before operational
  publication; otherwise report activation blocked. Recheck observed landing tree and pins
  after any authorized merge; mismatch is an incident, not successful publication.

### D6. Selected publication

- Prepare from pinned current main, exactly one owner-selected article and explicit reviewed
  dependencies. Never merge or copy the whole staging tree to main. Approval binds article
  identity, exact source/dependency commits and bytes, policy/registry version, main base,
  prepared tree, and the preview deployment identity/served staging commit reviewed by the
  author. A URL alone or a newer branch tip does not prove what was reviewed.
- The full source manifest records every regular path's mode/hash, all additions/deletions,
  permitted immutable aliases without following them, and the exact allowed diff. Existing
  published content is retained except explicitly approved changes. Listing/navigation and
  shared dependencies admit only selected/published article content; a shared path is not a
  blanket permission for another candidate. Reject new links, submodules, escaping includes
  and executable imports under the existing local isolation contract.
- Reconstruct and independently verify the tree; run the existing reviewed build under an
  enforced no-network boundary. Record command, toolchain, isolation probe and build output
  inventory separately. Scan every output file for unselected routes/listing/search/RSS
  references and exclusive assets. Source reconstruction and reviewed build are primary;
  signature scans are supplementary, and missing signatures mean exclusion-unverified.
  A missing runtime or enforced boundary blocks that check, never grants a pass.
- Final ref/candidate drift invalidates preparation and readiness. Changes to any approval
  binding require renewed approval for the new exact publication candidate. Commit, push
  and PR actions use project message skills and apply only within explicit owner authority.
  Opening a PR does not authorize merge. Main landing, deployment completion and HTTP/UI
  verification are separate recorded states; none substitutes for another.
- After a verified main landing, main-to-staging sync retains the published article and all
  other candidates. Retire only the landed candidate's unapproved identity in the next
  reviewed registry update. A later unpublished revision remains a candidate. Rollback uses
  a newly reviewed revert on current main and independent authorization, preserving other
  publications; re-publication needs fresh pins and approval, never force/reset.

### D7. Workflow skill and tracker

- Extend the existing publication skill rather than add a conflicting fifth product package.
  Draft a concise router plus workflow reference; retain the existing local and future-action
  references byte-for-byte. While version 2 is absent, the workflow can inspect/plan only
  and must report unavailable operations rather than invent commands or use version 1 to
  evade admission. Keep the existing supported version-1 local route available.
- After approval and implementation review, update the canonical product source once and
  deterministically materialize both runtimes. Preserve catalog cardinality, invocation
  policy, the three Chinese writing exceptions and historical package evidence through an
  explicit reviewed successor. This round does not activate or install the draft skill.
- ADR-0006 remains effective: done needs actual authorized staging ancestry and an approval
  receipt. Main-first engineering delivery additionally records main landing; sync PR-ready
  is insufficient for done. Publication tickets additionally require their main/publication
  acceptance evidence. Preview integration alone is not publication completion. No previous
  ticket is closed, reopened or renumbered by this spec.

## Acceptance Criteria

| ID | Observable pass/fail contract |
|---|---|
| AC-01 | An approved M0 accounts for every main/staging difference including unpublished revisions; unclassified/overlapping ownership prevents affected preparation. Only actually landed prerequisite commits are recorded as landed. |
| AC-02 | Baseline main diff contains only individually approved engineering/management changes; no unapproved body/revision, listing or exclusive asset enters main. Staging preserves every inventoried unapproved blob/mode/metadata except separately approved edits. |
| AC-03 | Every historical fixture/assertion still yields its original result, including v1 ancestry rejection; shared current validation uses trusted target roles and only exact reviewed successor boundaries. |
| AC-04 | V2 accepts clean registered A already merged into staging; it rejects staging integration ancestors, B history even after revert, unknown/omitted candidates, invalid ownership, stale pins and unapproved legacy reconstruction. A reviewed legacy migration preserves old evidence. |
| AC-05 | Clean sync produces the independently computed validated tree in one owned staging PR; already-synced input is no-op. Conflicts, branch mismatch, drift, failed checks and three exhausted retries produce no target mutation or duplicate PR. |
| AC-06 | Concurrency/coalescing and ambiguous API outcomes are exercised; latest pins are re-read, unrelated branches/PRs remain untouched, and no run merges, force-pushes or changes deployment settings. |
| AC-07 | Validation readiness requires an actual trusted successful run for exact base/head/tree/policy. Suppressed triggers, missing/denied/stale runs, writer-token exposure or absent activation prerequisites cannot produce readiness. |
| AC-08 | Selecting A reconstructs main plus approved A/dependencies only. B's unpublished revision, routes, listing/search/RSS entries and exclusive public assets are excluded at source and checked at output; protected URLs/bytes remain. Tampering or missing build isolation/evidence blocks the corresponding readiness check. |
| AC-09 | Approval and readiness expire on binding drift. PR, main landing and deployed/served verification have distinct receipts. Sync preserves remaining candidates; rollback/re-publication preserve unrelated publications and require fresh authority. |
| AC-10 | The draft skill chooses existing v1 local preparation or proposed workflow correctly, refuses unavailable/unauthorized remote actions and survives representative forward evaluation. Future installation preserves four product packages and both runtimes. No ticket reaches done solely from main landing or PR readiness. |

## Testing Decisions

Use public Git/CLI results, native validators, complete manifests, real builds and observed
remote/website receipts rather than assertions that mirror implementation wording. Existing
seams are Python subprocess tests with disposable Git repositories, article-publication
preview/prepare/verify, native unit discovery, the materializer/adoption validators and the
VitePress build/browser surface. Proposed additions are v2 admission, sync planning and the
GitHub/Actions adapter; owner confirmation is required before their tests are written.

The accompanying test plan distinguishes deterministic local harness results from authorized
GitHub integration and actual staging/production observations. Stub API success never proves
remote checks ran. Do not add redundant wording tests; record coverage by AC at close-out.
Use existing Node 24.13.0 and pnpm 10.28.0 without installation. New tests start only after the
test plan and ticket breakdown are approved, then follow the project's TDD loop.

## Out of Scope

Deployment configuration, Cloudflare/DNS/build-watch changes, new preview URLs, repository
rule/credential/account changes, automatic merges, bulk staging-to-main publication, private
draft storage, global skill installation, historical evidence rewrites and implementation
or remote delivery in this planning round. Optional auto-merge of sync PRs is a later decision.

## Further Notes

See traceability, test-plan, source-evidence and the proposed ADR clarification beside this
spec. Platform capability is separate from this repository's activation/configuration state.
The owner confirms this reviewed spec, its new seams and the skill draft before ticketing.
