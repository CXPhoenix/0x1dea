---
id: T-0021
title: Report trusted validation on the exact PR head and expire stale readiness
epic: 0012-publication-workflow
status: review
blocked_by: [T-0019, T-0020]
---

## Context

Owner approved the reviewed four-slice proposal, dependencies and 23-row local prerequisite allocation with the reply ‘同意’ on 2026-10-16 (Asia/Taipei). This ticket is former draft C. The approved [requirements supplement](../../.proj.specs/0012-publication-workflow/implementation/T-0016-P13-prerequisite-ticket-proposal-20261016/requirements.en.md), [traceability](../../.proj.specs/0012-publication-workflow/implementation/T-0016-P13-prerequisite-ticket-proposal-20261016/traceability.md), [test plan](../../.proj.specs/0012-publication-workflow/implementation/T-0016-P13-prerequisite-ticket-proposal-20261016/test-plan.md) and [registration approval](../../.proj.specs/0012-publication-workflow/implementation/T-0016-P13-prerequisite-ticket-proposal-20261016/registration/approval.md) govern this ticket; original frozen epic requirements and P13 remain intact.

A trusted-main dispatch run is not a check on the candidate PR head. The read-only validator cannot publish it. Head-only merge guards do not protect target-base freshness or source-main/policy drift.

## Deliverable

A separate local trusted reporting adapter binds a completed successful run to the exact candidate head and configured check identity; local readiness refuses missing capability or stale head/base/main/policy/workflow. Integrate T-0019's synthetic admission and T-0020's source-bound job inputs with public adapter/Git fixtures. The ticket establishes observable requests/refusals, not live branch protection or permission proof.

## Acceptance criteria

- [x] Meet C1: exact independently read run/source/head/report binding, successful check readback, all non-success/ambiguous cases refuse.
- [x] Meet C2: separate reporter identity/credential without expanding writer/build/merge/admin privileges or exposing credentials.
- [x] Meet C3: before/after ref/report readback, unknown-result recovery and distinct head/staging/main/policy/workflow drift invalidation.
- [x] Meet C4: independently observed strict/check-source/non-bypass capability is required for live readiness, local fixtures cannot satisfy it; no point-in-time observation is called a merge lock, base CAS or later-main guarantee.
- [ ] Meet K1–K3 and PC-01–07; approved coverage, standards/spec/security review and separately authorized actual engineering landings before done. Actual enforcement remains P13; no rule/queue/workflow activation or merge here.

## Approved test plan — original registration checkpoint

Allocated rows: PC-01, PC-02, PC-03, PC-04, PC-05, PC-06, PC-07. All are approved plan rows, **NOT WRITTEN / NOT RUN**. Reuse existing behavioral regressions; distinguish public local Git/native/API-adapter and filesystem-observation fixtures from actual GitHub capability evidence. Follow one seam/test/minimal implementation per TDD cycle only after separate implementation authorization. Coverage must enumerate the listed subcases. No original P01–P24 row is renamed or marked passed by this ticket.

## Delivery boundary — original registration checkpoint

Current authorization publishes tracker records only. Status is todo; do not claim work or start implementation until separately authorized. Future implementation uses this permanent ticket id on its own ticket branch. Preserve published-only main, all staging candidates/assets, target-specific historical validators/receipts/oracles/aliases and exact current successors. No active workflow, lab, installation, credential/account/rule/runner/deployment changes, merge or automation activation is granted. Done requires approved coverage/reviews and separately authorized actual engineering landings on main and staging; actual remote P13 remains a separate gate, with T-0016 review.

## 給使用者（zh-TW）

讓可信驗證對應到指定 PR head，來源或目標更新就撤銷舊判定；遠端保護是否真正生效，仍由 P13 驗證。測試分配 7 列，須等 A、B 完成。


## Registration record — 2026-10-16

Recorded by project to-tickets after owner approval and a fresh global id scan of local tracker trees and actual origin/main/origin/staging. No implementation, executable tests, lab, remote mutation, commit or push accompanies this registration. See the registration approval and mapping for immutable review identities and exact scope.

## Implementation authority — 2026-10-18

The owner explicitly requested completing the conditional prerequisite closeouts and implementing T-0021 through tests and independent review under the approved PC-01–07 table. This supersedes the historical registration-only delivery checkpoint. T-0019/T-0020 now have actual approved dual-target landing evidence. No material seam or test-plan change is made. No production merge, activation or deployment-setting change is granted; actual P13 remains separate and T-0016 stays review.

## Local implementation completion — 2026-10-18

Status review. Approved PC01-07 local behavior is implemented; focused12 and complete prospective-main236/retained-stage265 pass, including all current negatives, unchanged #22/#32 historical contracts and actual deny-default builds. Source Standards/Spec/security reviews have no unresolved implementation findings. Historical STD-V2-01 batching deviation remains recorded rather than rewritten as sequential TDD; the later coverage label inconsistency is corrected. Coverage/execution/reviews are in ../../.proj.specs/0012-publication-workflow/implementation/T-0021/.

C1-C4 checkmarks describe the approved local contract only. Replayed API envelopes are not real platform capability evidence. The original registration NOT WRITTEN/NOT RUN/todo paragraphs above are historical and superseded by the explicit implementation authority and this checkpoint. The remaining combined acceptance item still requires separately authorized actual engineering landings on main and staging before done. T-0016 remains review; P13 NOT RUN. No production merge, automation activation or deployment change.
