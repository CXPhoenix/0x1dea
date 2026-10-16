---
id: T-0022
title: Continue after one explicitly approved manual PR delivery without claiming ownership
epic: 0012-publication-workflow
status: todo
blocked_by: []
---

## Context

Owner approved the reviewed four-slice proposal, dependencies and 23-row local prerequisite allocation with the reply ‘同意’ on 2026-10-16 (Asia/Taipei). This ticket is former draft D. The approved [requirements supplement](../../.proj.specs/0012-publication-workflow/implementation/T-0016-P13-prerequisite-ticket-proposal-20261016/requirements.en.md), [traceability](../../.proj.specs/0012-publication-workflow/implementation/T-0016-P13-prerequisite-ticket-proposal-20261016/traceability.md), [test plan](../../.proj.specs/0012-publication-workflow/implementation/T-0016-P13-prerequisite-ticket-proposal-20261016/test-plan.md) and [registration approval](../../.proj.specs/0012-publication-workflow/implementation/T-0016-P13-prerequisite-ticket-proposal-20261016/registration/approval.md) govern this ticket; original frozen epic requirements and P13 remain intact.

Production PR27/28 were manual merges without operation markers. The uniquely admitted main-bootstrap exception does not admit the manual staging PR. After preparation becomes ready, the remaining ownership guard refuses that history; synchronized refs may return no-op earlier, so no live controller failure is claimed.

## Deliverable

The public recovery flow can continue past one independently approved exact manual merged delivery, records it as manual historical evidence, and creates/reuses only a newly owned matching operation. Missing approval or unrelated/mutated history still refuses. The permanent runtime branch and old records stay unchanged.

## Acceptance criteria

- [ ] Meet D1: no-op order/default ready refusal preserved; continuation approval binds every listed immutable delivery identity and ancestry.
- [ ] Meet D2: skip only that exact historical conflict, retain manual classification and original records; every listed mutation/unmerged/reopened/ambiguous case refuses.
- [ ] Meet D3: unrelated open/closed PR, fake ownership, unverified/mismatched deleted/recreated branch and closed matching owned operation remain fail-closed; preserve exact parent D4 non-force owned-branch recovery without treating manual history as owned; no duplicate/reopen/force/fallback branch.
- [ ] Meet K1–K3 and PD-01–04; approved coverage, standards/spec/security review and separately authorized actual engineering landings before done. No production PR edit or remote lab operation.

## Approved test plan

Allocated rows: PD-01, PD-02, PD-03, PD-04. All are approved plan rows, **NOT WRITTEN / NOT RUN**. Reuse existing behavioral regressions; distinguish public local Git/native/API-adapter and filesystem-observation fixtures from actual GitHub capability evidence. Follow one seam/test/minimal implementation per TDD cycle only after separate implementation authorization. Coverage must enumerate the listed subcases. No original P01–P24 row is renamed or marked passed by this ticket.

## Delivery boundary

Current authorization publishes tracker records only. Status is todo; do not claim work or start implementation until separately authorized. Future implementation uses this permanent ticket id on its own ticket branch. Preserve published-only main, all staging candidates/assets, target-specific historical validators/receipts/oracles/aliases and exact current successors. No active workflow, lab, installation, credential/account/rule/runner/deployment changes, merge or automation activation is granted. Done requires approved coverage/reviews and separately authorized actual engineering landings on main and staging; actual remote P13 remains a separate gate, with T-0016 review.

## 給使用者（zh-TW）

用明確核准的精確紀錄接續先前手動 PR，保留其手動性質；不替舊 PR 補造自動化擁有權。測試分配 4 列，無其他新票阻擋。


## Registration record — 2026-10-16

Recorded by project to-tickets after owner approval and a fresh global id scan of local tracker trees and actual origin/main/origin/staging. No implementation, executable tests, lab, remote mutation, commit or push accompanies this registration. See the registration approval and mapping for immutable review identities and exact scope.
