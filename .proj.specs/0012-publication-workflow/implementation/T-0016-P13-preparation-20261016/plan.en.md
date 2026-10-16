# T-0016 P13 Remote Exercise Preparation Plan

> For Codex/Claude: follow the active project runtime and an executing-plans workflow only after the owner grants the named lab authority. This proposal is NOT permission to execute.

**Goal:** Verify actual GitHub dispatch/permission/readiness/merge-protection boundaries in an isolated authorized repository while retaining production candidates and historical validation contracts.

**Architecture:** Import full reviewed history into a separate lab, prepare independently approved finite policy/runtime/check prerequisites, and prove capabilities before issuing a temporary lab-only activation receipt. Run the gated controller only after observed evidence exists; record success/negative/race outcomes separately from production activation.

**Tech Stack:** Existing Python3.11+, Git/gh, Node24.13.0/pnpm10.28.0, enforced macOS build isolation, GitHub REST/Actions and actual supported branch protections. No installation or infrastructure change is authorized by this document.

## Files and source evidence

Current immutable production baseline: main8b31956f47075a831cfd0339339f616af96b3dae, stage05fc16c30f978bbafab4b8cc89f24f8657ab3045. Re-read before any later exercise; do not reuse old readiness after drift. Frozen approved spec D4/D5, AC03/05/06/07/09 and P13 remain source of requirements. Do not edit them as part of this plan.

Read: scripts/publication_current.py(policy/prepare), scripts/staging-sync-remote.py(schema/run/validate), scripts/publication_remote.py(run_sync/GitHubAdapter), scripts/publication_remote_git.py, existing inactive templates and current tests. Preserve original validators/oracles. This proposal creates only its own documentation/evidence and finite management map entries in an isolated checkout; no implementation or production setting changes.

## Task 1 — Owner selects lab and authority

Review README.md, authorization.md and test-matrix.md. Resolve exact owner/name/visibility, creation/import rights, protected-check support, safe runner/runtime/config delivery, actor/token provisioning route, budgets/run/time limits, permitted synthetic lab target advances/merge probes and cleanup. No token values in chat. No account/org/global trust/billing changes assumed. If not all execution authority exists, stop at a prepared plan.

## Task 2 — Resolve engineering gates BEFORE remote controller exercise

1. Current policy() AND prepare() reject every .github/ path unconditionally. An exact map entry alone is insufficient. A separately approved finite successor and red/green preservation tests must precede a live validation workflow in the same tested source. Never blanket-exempt .github or alter historical snapshots.
2. Current inactive templates assume external config and installed runtime but have no provisioning step. Define reproducible writer/validator inputs and separate digests; verify actual paths/pins on each runner. Preserve deny-default probes and shared cross-job scheduling; RUNNER_TEMP flock only locks that host/path.
3. Dispatch run head_sha is main, and validator contents:read cannot publish PR-head required checks. Define/review a separate trusted reporter plus strict target freshness or equivalent queue and non-bypass actors; do not silently grant writer/validator status write or merge bypass. Prove source-main/policy drift expiry too; strict target-base protection does not lock another ref.
4. Existing manual branch history is another activation gate. Read-only API observes closed merged main PR27 (head4d6e58c) and staging PR28 (headf76eff4), both without an operation marker. _owned_pulls() may exclude only the exact approved main bootstrap PR; its remaining ownership guard rejects unmarked manual staging PR28 when a new preparation is ready. The currently already-synced main/staging pair may return no-op earlier; do not call that an observed ownership failure. This is a confirmed conditional code-path blocker once earlier activation gates are met, not an executed controller result. Reproduce it in the lab; any finite historical continuation exception/repair requires separate approval/tests/review and exact immutable PR/head/tree/actor evidence. Never edit the old PR body/receipt to manufacture ownership, blanket-ignore closed PRs, change the permanent branch unilaterally or call a manual merge an owned automation run.
5. Feature/policy/reporter/runtime changes require approved new engineering tickets/test allocation/reviews under the repository permanent-id rule; no code is changed by this operational proposal. Land approved prerequisites through their own authorized flow, recapture fresh actual source pins, then return to P13.

## Task 3 — Bootstrap authorized lab only

Create/select only the exact approved repository. Do not use blanket mirror-push or add production webhooks/Cloudflare/Pages. Import reviewed complete history, named main/staging refs and any existing candidate fixtures; preserve literal alias bytes. Fixture-only control/candidate revisions are registered and owner-approved. A lab GitHub PR number must come from the lab API; historical production PR27/28 documents are not bootstrap API proof.

Install only separately authorized lab validation/probe definitions, leaving push-driven writer automation disabled unless separately expressly required for a bounded concurrency case. Preconfigure permitted lab protections and expected reporter/check identity. If private plan lacks the required feature, stop; do not switch visibility or remove the guard. Capture all configuration before/after. Use a genuine lab implementation PR/seed when exercising that exception, or a branch-absent case as specified by the code. No fake ownership marker.

## Task 4 — Independent capability probes, no gated writer yet

Probe actual limited credential operations, explicit trusted-main dispatch, exact run correlation, real native/build isolation and head/latest-target-base refusal. These bootstrap probes run under A1 lab-specific authority; they are not a forged activation receipt. Keep observed run IDs, hashes and denial/no-mutation readbacks. If a capability is absent, retain a failed/blocked row and stop the dependent flow.

Official dispatch permission is Actions write and accepts branch/tag ref; the current adapter uses main then checks the actual run main SHA. Its pinned API version is 2022-11-28; record actual response under that version rather than assuming a newer documentation response shape. An acknowledgment/run URL is never a successful validation. [Workflow API](https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event).

## Task 5 — Owner-approved temporary lab receipt, then one bounded controller run

After real independent probes prove every prerequisite, owner reviews an external lab-only receipt and its independently delivered SHA. It must bind actual repository, verified booleans to real receipts, positive exercise_run_id, workflow path/hash, actual lab branch_seed/bootstrap_pr. Do not create sample true flags now, reuse fixture IDs or store authority inside candidate/control. Record that the capability probe id is distinct from the later controller run id.

With fresh trusted main and reviewed policy/registry/runtime, use schema/help and exact run arguments already documented in docs/staging-sync-remote.md. Explicit remote flag, installed gh, scoped token and external shared state remain required. Verify at most one owned staging PR and exact journal/operation/head/tree/parents/run/refs. Never point the controller or token at production for this lab exercise.

## Task 6 — Execute matrix and bounded race probes

Run P13-a through l with the named actor/protection context. Store redacted raw readbacks and SHA-bound artifacts outside candidate/control; write coverage outcomes per subcase. No real manual actor is locked by local flock. A merge API head guard is not base compare-and-swap; stale target base must be refused by actual required up-to-date checks/queue. Do not claim operation-ready guarantees a later landing. Unexpected acceptance, duplicate/unowned mutation, credential exposure, missing run/capability or bounded timeout stops the exercise and requires triage/review, not a broader token or skip.

## Task 7 — Close lab evidence, keep production disabled

After separately authorized synthetic lab landing, compare actual parents/tree/pins/candidate/history to recomputation. Preserve any failure before cleanup. Revoke temporary credentials/disable lab jobs/close named PRs only within the granted cleanup scope; retain repository/evidence unless deletion explicitly separately approved. Produce coverage and independent standards/spec/security evidence review. A passing lab does not verify production account/rules/runner or authorize production activation. T16 stays review in this request; later completion/activation requires explicit owner acceptance, resolved prerequisites and separately authorized production decisions.

## Present execution status

All P13 matrix rows NOT RUN. No lab repository or credentials provisioned. Production workflow count0; no activation. Current request completed only landing audit plus proposal; no commit/push/remote mutation. Safe local readbacks: git rev-parse/show/diff; python3 scripts/verify-harness-adoption.py; python3 scripts/verify-project.py; python3 scripts/materialize-writing-skills.py --check. Evidence folder records actual immutable target commits, not simulated P13.
