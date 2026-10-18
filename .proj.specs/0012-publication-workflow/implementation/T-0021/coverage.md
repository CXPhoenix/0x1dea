# T-0021 approved coverage report

Source-v5 checkpoint: reporting code is identical to reviewed source-v4. PC01-07 focused12/12 pass (43.149s); runner guards2/2 pass including12 contract mutations; current-context14/14 and original frozen-#32-context14/14 pass (200.897s/201.068s), with real isolated builds. Complete main236/236 and retained-stage265/265 executions of this fixed source PASS (all four contexts), with two real isolated builds per target. Website checks54/87 unit, lint/build, project structure and materialized packages passed on unchanged website/package bytes.

Surface: public report_validation/report_from_job/check_reporter_from_environment; real full-history Git; replayed read-only/reporting REST envelopes; real finite workflow admission and sealed job/runtime/sandbox inputs. These are local source/API/CLI/build observations, never actual Actions/check/permission/rules enforcement or P13 proof.

| Row | Public behavioral coverage and observations | Result / limits |
|---|---|---|
| PC-01 | Exact completed trusted-main workflow_dispatch run bound independently to repo/op/main/stage/head/tree/policy/workflow/id/attempt/title; one configured success check request targets candidate head, separate list/direct readback binds check id/app/conclusion; full A/B source integration | Focused pass; replayed REST, not live check capability |
| PC-02 | Queued/in_progress, failure/cancelled/skipped/neutral/timed_out, missing, duplicate, wrong main/event/attempt/repo/head-repo/workflow/title, denied and malformed operation id/tree/policy/main/stage/version; no success mutation | Focused pass; canonical independent expected binding is frozen in memory |
| PC-03 | Separate reporter role/app; wrong writer/validator/app and401/403 refuse. Explicit reporter credential is consumed before source jobs, reaches only filtered gh JSON environment; no token in command/body/results. Read-only candidate validation rejects reporter credential before candidate execution; real sealed validator inputs and external finite grant feed public reporting entry | Focused pass; actual effective permissions remain unverified. Token/transport process observations are synthetic sentinels |
| PC-04 | H1→H2 before write, during accepted write and after readback invalidates H1; before-write drift sends no success, all refuse readiness and request fresh validation; no merge request | Focused pass; point-in-time observation only |
| PC-05 | Staging advance, missing strict up-to-date, wrong configured name/app, admin bypass allowance, wrong/admin actor, protection/source drift before/after; complete parent ruleset inventory/detail and visible empty active bypass lists, exact standard write role, unknown/custom/hidden/denied identities refuse; candidate-provided verified flag and all local live=True requests cannot satisfy live readiness | Focused pass; classic protection, inherited rulesets and actor-role observations are replayed contract prerequisites, not live platform proof |
| PC-06 | Main advance including mid-observation, policy/workflow byte changes at fixed candidate head; named refusal and new independent preparation; actual A/B grant tamper refuses before API action | Focused pass; no later-main guarantee |
| PC-07 | Durable journal records intent before success write; accepted-unknown result is independently read before retry. Hidden outcome stays blocked across fresh calls without duplicate; exact later readback recovers. Report app/head/external-id/status/conclusion/id mutations and duplicate run inventory refuse; confirmed check id is pinned and replacement or journal tampering refuses; capability configuration fingerprint changes invalidate a prior result; old success rechecks refs; no merge/global lock/base CAS claim | Focused pass; one-host lock and durable per-binding journal are not distributed/manual exclusion |

## Existing regression and preservation

The exact #22 T13 contract remains at001b26f8e931e0cf1e62373c5aa088a1b5ed09eb. Four unmodified fixed-history modules run explicitly at approved #32 source64b31a2c38959ef5490892fa2a001bb0bf2f8ca0, and all14 original assertions also run against current source/actual histories in independent fixture namespaces. Contract byte guards reject any missing/linked/changed original before discovery. There is no failure-selected fallback; any context failure fails the overall command. See historical-context-repair.md and raw evidence.

Current and prospective stage article trees are unchanged: published main73 paths, retained stage111 paths including50 candidate paths. All557 pre-existing maintenance paths other than the evolving exact engineering policy remain identical; M0, frozen test files, original receipts/oracles/aliases and deployment sources remain unchanged. Final current native/readback and source manifest checks must accompany complete execution records.

## Historical development and review

| Source | Recorded result | Disposition |
|---|---|---|
| v1 | Spec2P1; Standards/security0; earlier focused9pass; full attempts interrupted | Check identity and missing local non-bypass observations fixed; interrupted logs not passes |
| v2 | Spec1P1 same-call ID; Standards1P2 batching; security0; focused11pass; full attempts interrupted | Same-call identity fixed; batching deviation accepted and preserved, not rewritten as sequential TDD |
| v3 | Spec1P1 durable retry identity; new Standards/security0; focused12pass; full attempts interrupted | First known ID now saved before subsequent observations and survives retries |
| v4 | Spec0; security0; Standards1P2 coverage version label; focused12pass; both complete full runs6fail | Correct native refusal exposed fixed-history/current metadata conflation; explicit contexts and current negative counterparts repair it |
| v5 | Source Standards/Spec/security0; context14+14/guard2pass | Complete fixed-source main236/staging265 pass; exact tested snapshot and limits are in execution.json |

STD-V2-01 remains an accepted historical P2: two review regressions were batched rather than individual original TDD cycles. No retrospective sequential claim is made. Later corrections used one failing test, minimal change, green. STD-V4-01 is resolved by explicit source labels and the actual v4 focused log. All original failure/interruption records remain.

Measured coverage is the named behavioral cases and original assertion sets above, not an invented line/branch percentage. local_ready is point-in-time only; live_ready/publishable remain false and live=True refuses. Actual platform rights, effective rules/bypass and remote races remain P13. T-0016 stays review. T-0021 cannot be done before separately authorized actual engineering landings.

## Complete execution and final-record boundary

| Test tree | Harness/current | Publication/current | Original #22 | Original #32 | Total / exit |
|---|---:|---:|---:|---:|---:|
| Prospective main | 66 | 146 | 10 | 14 | 236 / 0 |
| Retained-stage | 95 | 146 | 10 | 14 | 265 / 0 |

Raw complete logs, actual isolation receipts and full tested-source manifest are retained in evidence/. Tested snapshot SHA-256: 7c5352346dc6954c13c749b31cd8fd71ce0bfe6595d4b92743cac30f2087c7a0. These totals count executions in explicit contexts, not unique assertions or a coverage percentage. Both contexts are required and failures propagate.

After these commands only records, T-0021 review metadata and exact policy hashes are finalized; implementation/test bytes are unchanged. Fresh post-record native self-validation and trusted cross-role readback verify the finalized metadata/policy. No full-regression claim is made for an unexecuted later source tree. Final metadata review is recorded separately in final-review.md.

T-0019/T-0020/T-0022 are locally done from actual approved dual-target implementation landings and complete historical source evidence. T-0021 is review, not done: its actual engineering landings remain pending. T-0016 stays review and P13 NOT RUN. No commit/push/PR/merge/activation/deployment action accompanies this local completion.
