# Trusted staging synchronization adapter

T-0016 implements the approved P10-P12 local/adapter boundary on top of the existing
`staging-sync.py` contract. No active workflow, deployment setting, credential or
repository rule is changed. P13 real remote exercise and activation remain blocked.

## Supported interface and trust

`python3 scripts/staging-sync-remote.py schema` describes `run` and `validate`.
`run` without `--allow-remote-write` is inert and exits 2 with a blocked JSON record.
The controller must be the actual trusted main checkout with the expected engineering
policy digest. An external owner-reviewed activation receipt plus its separate digest,
complete reviewed registry, installed `gh`, explicit `PUBLICATION_WRITER_TOKEN`, and an
external shared state directory are required for authorized writes. The run CLI consumes
the writer credential before Git preparation and supplies it only to the JSON transport. Never take authority,
policy paths, credential choices or executable callbacks from article/API text.

The activation receipt binds repository, actual exercise run id, verified token scope,
latest-base protections, dispatch and candidate isolation, workflow path/hash, and the
exact original implementation branch seed/PR. There is deliberately no sample receipt
with fabricated successful remote checks. Local synthetic receipts are test data only.
After the initial implementation has actually landed, its exact closed merged main PR
is the sole allowed bootstrap exception on the permanent branch. It must match the
approved PR number/seed and be an observed main ancestor. Later feature or conflict
repairs require new tickets; routine operations do not reopen T-0016 as development.

## Operation and recovery

- Re-read actual main/staging/owned-branch refs. Use the event only as a wake-up hint.
  Refresh the reviewed registry against complete current Git objects, preserving every
  candidate identity and historical check. New unclassified paths or candidate changes
  require explicit reviewed source/registry/affected approval updates. A newer policy
  needs a fresh trusted main job; queued jobs coalesce by checking latest main.
- Local preparation has no source writes. Its complete result must equal an independent
  Git merge. No-op creates no branch or PR. Conflicts/check failures retain exact paths;
  drift restarts preparation with at most three retries after the initial attempt.
- Persist repository/target/branch/main/staging/policy/tree operation identity before
  mutation. Upload only verified Git objects; verify returned blob/tree/commit identities
  and read back the commit. Advance only `tickets/T-0016/main-to-staging-sync`, non-force.
- Check branch ownership and all PR pages. At most one owned open staging PR may exist.
  Closed matching operations, unrelated branch/PR identities, ref drift or uncertain
  results stop. Read back ambiguous writes before another action; an unobserved outcome
  is blocked rather than blindly creating a duplicate PR.
- Explicitly dispatch the trusted validation workflow from branch `main`, with pinned
  inputs. Require the actual run's exact main SHA, workflow identity, operation/head,
  completed state and success conclusion. Dispatch acknowledgment is insufficient.
  Polling is bounded; failed/missing/denied/stale/duplicate runs never grant readiness.
- Candidate validation uses trusted main code against candidate data. The fixed staging
  native entrypoint never imports candidate scripts. The actual VitePress build reuses
  the deny-default macOS boundary with clean environment and `CF_PAGES_BRANCH=staging`;
  outside read/write/network probes must be denied. Writer/API tokens are refused in
  the validator and never passed to the build subprocess. No unrestricted fallback.

`ready` is pinned PR readiness, never automatic merge, actual landing or publication.
The operation record remains outside source trees. Shared `writer_lock` serializes
participating local writers; deployed participating sync/preview/publication jobs must
use the same `publication-writers-${{ github.repository }}` concurrency group with
`cancel-in-progress: false`. A local lock cannot lock manual GitHub actors. Latest-base
protected checks or an equivalently verified queue are a separate activation gate.

## Inactive templates and unverified surface

`maintenance/publication-workflow/automation/*.yml.inactive` are reference artifacts,
not GitHub workflow configuration. The validation workflow has read-only permissions
and no writer secret; it is outside the writer concurrency group to avoid dispatch
waiting on its own lock. Both use a pinned checkout action and no installation step.
The designated runner needs existing Node24.13.0, dependencies, macOS isolation and
externally provisioned registry/runtime/authority files. Missing prerequisites block.

Do not move these templates to `.github/workflows`, provision tokens, change repository
rules or activate automation from this implementation. A separately authorized
owner-designated disposable repository must exercise permissions, actual dispatch/run
binding, latest-base/head race protection and non-force/owned-PR readback (P13). Actual
workflow paths also need an explicit reviewed finite engineering-policy successor;
the current policy intentionally rejects blanket `.github` additions.

## Primary API references

Reviewed for the adapter boundary, not evidence of a live remote exercise:
[workflow dispatch](https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event),
[Git refs](https://docs.github.com/en/rest/git/refs),
[workflow runs](https://docs.github.com/en/rest/actions/workflow-runs),
[pinned checkout release](https://github.com/actions/checkout/commit/11bd71901bbe5b1630ceea73d27597364c9af683).
The REST dispatch ref is a branch/tag, so the adapter dispatches `main` and independently
requires the observed run SHA to equal the expected pin. It never treats the API's
acknowledgment/run URL alone as successful validation.
