---
id: T-0022
title: Continue after one explicitly approved manual PR delivery without claiming ownership
epic: 0012-publication-workflow
status: done
blocked_by: []
landing_evidence: .proj.specs/0012-publication-workflow/implementation/prerequisite-closeout-20261018/T-0022-landing.json
---

## Context

Owner approved the reviewed four-slice proposal, dependencies and 23-row local prerequisite allocation with the reply ‘同意’ on 2026-10-16 (Asia/Taipei). This ticket is former draft D. The approved [requirements supplement](../../.proj.specs/0012-publication-workflow/implementation/T-0016-P13-prerequisite-ticket-proposal-20261016/requirements.en.md), [traceability](../../.proj.specs/0012-publication-workflow/implementation/T-0016-P13-prerequisite-ticket-proposal-20261016/traceability.md), [test plan](../../.proj.specs/0012-publication-workflow/implementation/T-0016-P13-prerequisite-ticket-proposal-20261016/test-plan.md) and [registration approval](../../.proj.specs/0012-publication-workflow/implementation/T-0016-P13-prerequisite-ticket-proposal-20261016/registration/approval.md) govern this ticket; original frozen epic requirements and P13 remain intact.

Production PR27/28 were manual merges without operation markers. The uniquely admitted main-bootstrap exception does not admit the manual staging PR. After preparation becomes ready, the remaining ownership guard refuses that history; synchronized refs may return no-op earlier, so no live controller failure is claimed.

## Deliverable

The public recovery flow can continue past one independently approved exact manual merged delivery, records it as manual historical evidence, and creates/reuses only a newly owned matching operation. Missing approval or unrelated/mutated history still refuses. The permanent runtime branch and old records stay unchanged.

## Acceptance criteria

- [x] Meet D1: no-op order/default ready refusal preserved; continuation approval binds every listed immutable delivery identity and ancestry.
- [x] Meet D2: skip only that exact historical conflict, retain manual classification and original records; every listed mutation/unmerged/reopened/ambiguous case refuses.
- [x] Meet D3: unrelated open/closed PR, fake ownership, unverified/mismatched deleted/recreated branch and closed matching owned operation remain fail-closed; preserve exact parent D4 non-force owned-branch recovery without treating manual history as owned; no duplicate/reopen/force/fallback branch.
- [x] Meet K1–K3 and PD-01–04; approved coverage, standards/spec/security review and separately authorized actual engineering landings before done. No production PR edit or remote lab operation.

## Approved test plan

Allocated rows: PD-01, PD-02, PD-03, PD-04. These approved rows are now implemented; current results are recorded in the implementation coverage table. The registration commit preserves their original NOT WRITTEN / NOT RUN checkpoint. Reuse existing behavioral regressions; distinguish public local Git/native/API-adapter and filesystem-observation fixtures from actual GitHub capability evidence. Follow one seam/test/minimal implementation per TDD cycle only after separate implementation authorization. Coverage must enumerate the listed subcases. No original P01–P24 row is renamed or marked passed by this ticket.

## Delivery boundary

Current authorization covers implementation, approved tests, independent reviews and reviewable delivery on this permanent ticket branch. Earlier registration-only statements below are historical. Status remains review until actual authorized engineering landings on both targets. Preserve published-only main, all staging candidates/assets, target-specific historical validators/receipts/oracles/aliases and exact current successors. No active workflow, lab, installation, credential/account/rule/runner/deployment changes, merge or automation activation is granted. Done requires approved coverage/reviews and separately authorized actual engineering landings on main and staging; actual remote P13 remains a separate gate, with T-0016 review.

## 給使用者（zh-TW）

用明確核准的精確紀錄接續先前手動 PR，保留其手動性質；不替舊 PR 補造自動化擁有權。測試分配 4 列，無其他新票阻擋。


## Registration record — 2026-10-16

Recorded by project to-tickets after owner approval and a fresh global id scan of local tracker trees and actual origin/main/origin/staging. No implementation, executable tests, lab, remote mutation, commit or push accompanies this registration. See the registration approval and mapping for immutable review identities and exact scope.

## Implementation authority and local checkpoint — 2026-10-16

Owner requested autonomous implementation after approval of PD-01–04. This supersedes the historical registration-only checkpoint. Local focused four-method and existing 22-method remote controller checks passed; full regression/reviews/authorized actual landings remain pending. No production merge/activation/deployment or remote P13 proof is claimed. See implementation/T-0022 authority and coverage.

## Reviewable delivery checkpoint

Local approved coverage and complete source regressions passed; independent Standards/Spec/security source reviews have no unresolved findings. See implementation/T-0022/execution.json and review/code-T-0022.md, review/security-T-0022.md. Final evidence supplement and actual main/staging landings are recorded separately; this ticket is not done and does not prove P13.

## Conditional actual dual-target closeout — 2026-10-18

All allocated local prerequisite rows and independent reviews are complete; the main engineering PR and staging PR33 actually landed. T-0019 also includes the separately authorized PR32 historical CLI correction. See .proj.specs/0012-publication-workflow/implementation/prerequisite-closeout-20261018/coverage.md, evidence/ and T-0022-landing.json for per-criterion evidence. Both target native readbacks pass; common1071 identities, all111 staging blog paths, all50 candidate paths, published-only main and immutable contracts are preserved. Earlier pending/review statements remain historical checkpoints. Status is now done for this repair only; actual remote capability/P13 is still NOT RUN and T-0016 remains review. No production merge, activation or deployment-setting change accompanies this closure.
