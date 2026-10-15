# Proposed tracer-bullet breakdown

Status: proposed; awaiting owner approval, not published tickets.
Source: approved epic 0012 specification, English blob
`a3f0c03754c389d40ca9fb97d8bb7c1ae992651b`; see approval.md.

The ids below are tentative labels for review, not permanent allocation. A read-only scan
across all local tracker trees/available refs and the prior delivery clones found T-0012 as
the highest existing id. Live branch heads also stop at T-0012. Recheck immediately before
publishing approved tickets. Target tracker: .proj.tickets, not GitHub Issues or Notion.

## Prerequisites and delivery boundaries

Read-only remote observation on 2026-10-11:

- main: eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a.
- staging: c6efa7ded4731cbe251bdbc6fea5615e7e7b11b7.
- PR20 remains OPEN, head e6e7a04da7a1e4d9819fa6f8aaadb72a0611e20c, targeting main.
- PR21 remains OPEN, head a67b8de69f70f794a9e062e3ac50a957688ffa9a, targeting staging.

The baseline slice can begin inventory without these PRs merging. Its landing acceptance
requires refreshed prerequisite evidence: actual landed T-0012 changes or separately reviewed
equivalents, as the spec permits. Do not invent T-0012 done or impose it as the only possible
blocking edge. No existing ticket is modified by this breakdown.

Each slice delivers observable behavior through its whole applicable boundary, not a schema,
test-only or documentation-only layer. Local sync preparation is independently usable before
remote automation. Common baseline lands through explicit manual synchronization during
bootstrap, so it does not depend circularly on future automation. All actual ticket done
transitions retain authorized staging ancestry, acceptance/coverage and approval receipts.
Bootstrap retains one branch per ticket: complete the baseline main PR first, then prepare
its staging integration on that same ticket-owned branch. A staging integration result is
never subsequently offered as a main/article source; no second ticket branch is invented.

### 1. T-0013 — Establish the common engineering baseline and M0 inventory

**Blocked by:** none.

**What it delivers:** A complete reviewed two-tree inventory and an engineering-only main
baseline, integrated back into staging while retaining every unapproved article/revision,
asset, metadata and URL. Reviewers can verify the exact main diff and candidate preservation
without implementing the same engineering fix twice. This is the necessary prefactoring
and migration slice, with observable validator and tree results.

**Acceptance:**

- Account for every delta with full commits, modes/blob hashes, ownership/shared patches,
  historical/current management classification and trusted target-role policy.
- Obtain owner approval of M0 before using it as policy; legacy contaminated candidates are
  recorded as requiring reviewed migration, never mislabeled clean.
- Exclude all unapproved publication content from main; preserve staging candidates and
  historical assertions with only explicit reviewed successors for current behavior.
- Adopt the approved main-first/operational-branch ADR clarification without changing old
  ADR-0006 evidence or done meaning; record real prerequisite and main/staging landing states.

**Traceability/tests:** AC-01/02/03 and AC-10 tracker boundary; P01/P02/P03, relevant P23 cases.

### 2. T-0014 — Prepare and verify one article through the explicit v2 contract

**Blocked by:** T-0013.

**What it delivers:** From current main and the reviewed registry, the local CLI prepares a
candidate containing exactly A plus approved dependencies, even when clean A already appears
in staging. It verifies provenance, full tree and build/output evidence; B's unapproved
content is excluded while B's existing published baseline remains. No remote mutation.

**Acceptance:**

- Publish actual v2 entry points/help/schema; preserve all v1 behavior and fixtures.
- Validate complete registry/ownership and every non-main commit; reject integration ancestry,
  B add/revert history, missing candidates/history, unknown commits and stale pins.
- Accept legacy reconstruction only with explicit original/new provenance and owner approval;
  implementing this gate does not migrate every real candidate or authorize source rewriting.
- Reconstruct exact modes/blobs/diff and retain allowed aliases; reject escaping reads,
  executable imports, new links/submodules and tampering.
- Use the existing isolated build contract and separate actual build/output receipts;
  failed/missing/blocked/exclusion-unverified required evidence prevents v2 PR-ready.

**Traceability/tests:** AC-03/04/08 and local AC-09 binding; P04–P08, P14–P17.

### 3. T-0015 — Prepare a verified main-to-staging synchronization locally

**Blocked by:** T-0013.

**What it delivers:** Given current main/staging and trusted candidate inventory, produce an
independently computed, validated sync result and receipt, or an exact no-op/conflict/failure
report, without changing source/target refs. A maintainer can inspect the result before any
GitHub integration exists.

**Acceptance:**

- Read current pins, compute the independent merge and validate the trusted staging role.
- Already-contained main is no-op; any conflict/check/ref drift blocks the result.
- Compare all pending candidate modes/blobs/metadata with the pinned registry, including
  conflict-free edits to different paragraphs of one published article; changed candidates
  need explicit source/registry/affected author-approval updates before retry.
- Expose supported operation/help/schema and a pinned result consumed by later automation;
  do not create a remote branch, PR or merge.

**Traceability/tests:** AC-05 and local AC-06 drift; P09, local ref-drift subset of P10.

### 4. T-0016 — Turn main changes into one trusted staging synchronization PR

**Blocked by:** T-0015.

**What it delivers:** A main event or explicit retry consumes local sync preparation, obtains
actual exact-input trusted validation and opens/updates at most one owned staging PR. Failure,
drift, conflict or uncertain API responses cannot silently write a target or duplicate a PR.

**Acceptance:**

- Implement shared writer serialization and remote operation identity/readback used by
  synchronization and later selected-publication operations. Bound retries to three per run.
- Retain the approved permanent ticket-owned sync branch, update non-force and prove its
  result equals the independent merge; leave unrelated branches/PRs untouched.
- Proposed canonical branch: tickets/T-0016/main-to-staging-sync. Initial implementation
  lands/reviews first; then the retained branch serves routine sync operations for this same
  permanent id. New features/conflict repairs use new ticket branches. No future operation
  reopens or repurposes the implementation ticket as new development.
- Explicit trusted validation dispatch requires an observed successful base/head/tree/policy
  run; no assumption that bot push/PR triggers all checks. Candidate builds receive no writer
  credentials or executable policy from article/API text.
- Verify actual permissions/dispatch/latest-base protections in a separately authorized
  disposable remote exercise before activation. Missing authority/capability stays blocked;
  no credential/repository-rule change, live activation or auto-merge is implied.

**Traceability/tests:** AC-03 target trust, AC-05/06/07 and remote AC-09 guards; P10–P13.

### 5. T-0017 — Deliver only the approved article and record publication/recovery states

**Blocked by:** T-0014 and T-0016.

**Why both edges:** Uses v2's exact candidate and the remote writer's shared serialization,
operation identity, trusted run/protection checks and ambiguous-outcome handling. Neither
candidate preparation alone nor a synchronization PR is the complete selected-delivery path.

**What it delivers:** An exact author approval produces a reviewable A-only main PR under
applicable commit/push/PR authority, with distinct readiness, observed landing and served
evidence. Candidate B survives subsequent synchronization. Revert/re-publication plans bind
current main and preserve unrelated publications.

**Acceptance:**

- Bind approval to actual reviewed staging deployment and source/dependency/main/policy/tree;
  drift expires readiness and affected author approval.
- Observe one existing preview alias containing registered candidate pages/revisions and
  correct listing/navigation; unavailable evidence stays blocked rather than inferred.
- Verify the exact allowed main diff/build; use project message skills and only explicitly
  authorized remote actions. A PR is not merge/publication authority.
- Validate main-only delivery through disposable Git and expressly authorized test-repository
  exercise. Do not publish a real candidate or create a production PR merely to finish this
  implementation ticket; those require an exact later article request and authority.
- Observe actual authorized landing separately from production completion/HTTP/UI evidence;
  test receipts do not claim a live article was published. Verify protected latest-base and
  post-landing mismatches without trusting a head-only guard.
- Sync preserves other candidates/new revisions, retires only a landed candidate identity
  in a reviewed registry update, and prepares reviewed rollback/re-publication without reset.
  Later live production article evidence is recorded only when that operation is authorized;
  unavailable required live acceptance remains unverified, never fabricated as covered.

**Traceability/tests:** AC-08 integration and AC-09; P18/P19/P20; reuse P13–P17 at the integrated
boundary without duplicating already-proven unit assertions. P19's actual production portion
is conditional on separately authorized real publication, not a new release request here.

### 6. T-0018 — Install and demonstrate the project workflow skill in both runtimes

**Blocked by:** T-0017 (which transitively depends on the local and remote workflow slices).

**What it delivers:** The installed publication skill routes real user requests to the
reviewed baseline, local preview, sync and selected-article capabilities, with truthful
fallback when a capability/authority is missing. Both runtimes discover the same approved
four-product-package contract; a fresh agent can follow the implemented workflow.

**Acceptance:**

- Update only canonical publication skill source and materialize both runtimes, retaining
  existing references, invocation policy, catalog cardinality and three writing exceptions
  through exact reviewed successors. No generated-copy edits or global installation.
- Replace proposal notices only with actual implementation/version/interface references;
  preserve v1 routing, missing-v2 fallback and independent remote/merge/deploy authority gates.
- Demonstrate native discovery and representative agent behavior against actual interfaces,
  including candidate preservation, unavailable checks and refusal of premature ticket done.
- Preserve P24's original planning evidence and verify future dry-run refusal cases at their
  actual authorized stage, not an obsolete assertion that no approved tickets can ever exist.
- Complete the epic's integrated coverage/security-chain analysis and evidence/retrospective
  gates, keeping blocked/unverified surfaces separate from successful local verification.

**Traceability/tests:** AC-03 packaging and AC-10; P21/P22/P23 and retained/future parts of P24.

## Dependency graph and test allocation

```text
T-0013 ──→ T-0014 ───────────────┐
   └────→ T-0015 → T-0016 ──────┴→ T-0017 → T-0018
```

No new test seams are added. Shared ACs cross ticket boundaries; each ticket reports its
specific contract/coverage rather than claiming the entire AC passed early. Reused rows do
not mean duplicate tests. Proposed full allocation covers P01–P24 and AC-01–AC-10.

Owner confirmation requested: six-slice granularity, genuine blocking edges, T-0016 retained
operational branch lifecycle and this allocation of the existing 24-row test plan. Approval
publishes one file per ticket with todo/blocked_by under the configured tracker; it does not
authorize implementation, actual publication, remote merges or deployment changes by itself.
