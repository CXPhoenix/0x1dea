# Independent skill forward evaluation

Scope: draft authoring validation, not product tests or proof of remote capabilities.
Reviewer: `workflow_skill_forward`, fresh context with only the skill/references, four raw
simulated user requests/observations and actual current CLI help. No intended answers,
spec findings or proposed fixes were provided. No commands, Git changes or remote actions
were executed. Hash-bound raw inputs are preserved in `inputs/` and inputs-manifest.json.

| Request | Observed agent behavior | Parent assessment |
|---|---|---|
| Local A/B preview, v1 clean sources | Selected actual preview then verify commands; prepare is single-article; build/isolation remained unverified; no remote action | Correct existing local route |
| A-only commit/push/PR, A/B already in staging, v1 only | Preserved exact existing authority but returned inventory/plan due missing v2/registry; no fake command, no history rewrite or B delivery | Correct capability gate |
| Sync with sidebar conflict and old validation | Kept owned branch/PR identity, stopped before push/PR update, required reviewed patch/new pins/checks; no blanket conflict strategy | Correct conflict and stale-evidence gate |
| Common baseline, existing article revision/B/assets/shared sidebar/history, PR20 open | Excluded pending article/revision/assets, split shared content review, preserved history and treated PR20 as unlanded; written plan only | Correct preservation and authority gate |

The agent exposed three usability gaps, corrected before round 2:

1. The retained v1 reference says staging-only ancestry without spelling out that it includes
   the clean topic's own commit after preview integration. The new workflow reference now
   explains the exact v1 refusal separately from v2 admission; old reference bytes stay intact.
2. An alleged v2 adapter did not provide a callable interface. The reference now directs
   read-only discovery through repository package scripts, approved implementation record
   and actual help/version/schema, and stops if not found. The spec requires publication of
   those entry points; no command is invented in the planning draft.
3. Missing-v2 baseline fallback did not say whether a workflow-verified patch was expected.
   It now explicitly means inventory and written plan/PR-description only. Independent
   engineering implementation can use its own approved process; it is not certified by
   absent workflow tooling.

The initial four simulations matched their intended authority/capability boundaries.
The clarified draft receives a focused read-only follow-up and the four-axis round-2 review.
This does not satisfy future Git/CLI, remote integration, build or website acceptance rows.

## Focused follow-up on the clarified draft

The same independent evaluator re-read only the revised skill and original raw observations.
It reported no remaining ambiguity preventing next-action selection across these four cases:
local v1 preview/verify remained executable; selected release without v2/registry remained
plan-only; sync conflict/interface absence remained blocked; missing-v2 baseline explicitly
ended at inventory and written PR-description. No commands or remote operations occurred.

This supports the draft's routing and capability/authority gates for the supplied cases only.
It is not installation, native discovery, real Git/CLI execution or product acceptance.
