# P13 authority proposal — not a grant

The current owner request authorizes read-only production landing verification and preparation of this operational proposal only. No lab exists by virtue of this document. No token/rules/workflow/provisioning/merge/deletion action is currently authorized.

## Required explicit owner choices

| Field | Proposed scope / unresolved choice |
|---|---|
| Repository | Exact owner/name; suggested CXPhoenix/0x1dea-p13-lab, uncreated/unverified availability; private preferred, capability/plan eligibility must be checked |
| Creation/history | Create only if explicitly approved; import complete reviewed Git history and named main/staging/seed refs, plus synthetic lab fixtures only; no mirror push to production |
| Lab settings | Named manual validation/bootstrap workflows, finite reviewed policy successor, required checks/protection and approved merge method; changes only in designated lab; no production configuration |
| Actors/credentials | Owner/bootstrap administrator separate from short-lived repository-scoped writer, read-only validator and any trusted check reporter; no raw credentials in chat or receipts |
| Runner/cost | Exact isolated runner; existing reviewed runtime/dependencies or separately approved provisioning; max runs, job timeout, retention and maximum new spend agreed before execution; stop if exceeded |
| Writes | Lab-owned branch/PR and bounded synthetic target advances needed for race tests; negative probes may attempt forbidden actions only against disposable lab targets |
| Merge probes | Explicit permission for lab-only synthetic PR merges, including an attempted stale merge which must be rejected; unexpected acceptance is a failing result, preserve evidence and stop, never reset production |
| Cleanup | Revoke short-lived lab credentials, stop lab workflow, close named test PRs after receipts saved; no automatic repository deletion, billing/trust/account changes or removal of unrelated resources |

## Least-privilege roles

- Bootstrap administrator: creates/imports/configures only the authorized lab and prepares approved workflow/check-reporting policy. This is a human/admin setup capability, not a writer credential.
- Writer: repo-scoped Contents write, Pull requests write, Actions write plus necessary read inventory. No Administration or secrets management. Workflow-file mutation rights are NOT presumed: refs APIs may require Workflows write for workflow changes. Prefer administrator-prepared fixed workflow inputs; any observed extra permission need stops for separate review, not automatic scope expansion.
- Validator/build: Contents read only; no PUBLICATION_WRITER_TOKEN, GH_TOKEN or GITHUB_TOKEN in the build child; original clean environment and deny-default isolation remain enforced. Any fetch credential is removed before candidate build.
- Trusted reporter, if adopted: separately reviewed check/status publisher credential and expected source identity, never in build or writer. Current inactive validator does not supply this functionality.
- Approver/merge probe actor: expressly lab-authorized non-bypass actor for protection tests; admin bypass must not turn a rejected-merge test into a false pass. Do not give the automation writer bypass or merge authority.

Permissions are requests to verify against real endpoint responses, not observed grants. Reference: [dispatch Actions write](https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event), [PR write](https://docs.github.com/en/rest/pulls/pulls#create-a-pull-request), [refs and workflow-sensitive permissions](https://docs.github.com/en/rest/git/refs#update-a-reference).

## Non-circular authority stages

A0: current read-only verification/proposal; complete, no remote mutation.
A1: separately authorized lab bootstrap and independent capability probes. No production and no gated writer. Obtain actual run IDs/permission/rule/isolated-build/race receipts first.
A2: owner reviews those real capability receipts and approves a temporary lab-only external activation receipt/digest, plus a bounded controller exercise. Never prefill verified booleans or exercise_run_id from fixtures. Record controller exercise evidence separately from the prior bootstrap capability run.
A3: separately scoped lab cleanup/retention. Failed probes never become true by changing the record. A later finite historical branch-continuation change needs its own explicit engineering approval; this proposal never authorizes editing old PR bodies/receipts or inventing operation ownership.
A4: production activation is a future independent decision/PR after prerequisites and reviews; no authorization here, even if every lab case passes. Re-evaluate actual production permissions/rules and fresh pins at that point.

The request to keep automation disabled covers the present work. A future grant must explicitly carve out temporary lab-only validation/probe execution; it must never be inferred as production activation. Until then all proposed remote steps remain unexecuted and T16 stays review.
