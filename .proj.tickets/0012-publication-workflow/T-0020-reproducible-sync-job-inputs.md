---
id: T-0020
title: Prepare reproducible isolated writer and validator job inputs
epic: 0012-publication-workflow
status: done
blocked_by: []
landing_evidence: .proj.specs/0012-publication-workflow/implementation/prerequisite-closeout-20261018/T-0020-landing.json
---

## Context

Owner approved the reviewed four-slice proposal, dependencies and 23-row local prerequisite allocation with the reply ‘同意’ on 2026-10-16 (Asia/Taipei). This ticket is former draft B. The approved [requirements supplement](../../.proj.specs/0012-publication-workflow/implementation/T-0016-P13-prerequisite-ticket-proposal-20261016/requirements.en.md), [traceability](../../.proj.specs/0012-publication-workflow/implementation/T-0016-P13-prerequisite-ticket-proposal-20261016/traceability.md), [test plan](../../.proj.specs/0012-publication-workflow/implementation/T-0016-P13-prerequisite-ticket-proposal-20261016/test-plan.md) and [registration approval](../../.proj.specs/0012-publication-workflow/implementation/T-0016-P13-prerequisite-ticket-proposal-20261016/registration/approval.md) govern this ticket; original frozen epic requirements and P13 remain intact.

Inactive job examples assume installed runtime, external full configuration and reusable state. They do not yet supply a checked per-job preparation path. Temporary host locks do not serialize all jobs or manual actors.

## Deliverable

A maintainer can run a local public preflight/input-preparation flow for fresh separate writer and validator jobs, recover one durable operation journal, and obtain the same pinned operation. Missing runtime/isolation/full refs/config/state stops with a named cause. This is a reproducible local contract, not provisioning or live Actions proof.

## Acceptance criteria

- [x] Meet B1: exact existing runtime/deps/isolation/full-history checks before writes; no install or weaker fallback.
- [x] Meet B2: independently source-bound external inputs/digests, separate fresh jobs and credentials, explicit per-job snapshot root/UID/mode/type/link-count/open/read predicates, tamper refusals and deny-default probes; label filesystem-observation fixture limits.
- [x] Meet B3: durable per-repository state, bounded unknown-outcome recovery, shared non-cancelling writer group, separate validator group and no global/manual lock claim.
- [x] Meet K1–K3 and PB-01–06; approved coverage, standards/spec/security review and separately authorized actual engineering landings before done. No fake capability receipt or lab setup.

## Approved test plan

Allocated rows: PB-01, PB-02, PB-03, PB-04, PB-05, PB-06. These approved rows are now implemented; current results are recorded in the implementation coverage table. The registration commit preserves their original NOT WRITTEN / NOT RUN checkpoint. Reuse existing behavioral regressions; distinguish public local Git/native/API-adapter and filesystem-observation fixtures from actual GitHub capability evidence. Follow one seam/test/minimal implementation per TDD cycle only after separate implementation authorization. Coverage must enumerate the listed subcases. No original P01–P24 row is renamed or marked passed by this ticket.

## Delivery boundary

Current authorization covers implementation, approved tests, independent reviews and reviewable delivery on this permanent ticket branch. Earlier registration-only statements below are historical. Status remains review until actual authorized engineering landings on both targets. Preserve published-only main, all staging candidates/assets, target-specific historical validators/receipts/oracles/aliases and exact current successors. No active workflow, lab, installation, credential/account/rule/runner/deployment changes, merge or automation activation is granted. Done requires approved coverage/reviews and separately authorized actual engineering landings on main and staging; actual remote P13 remains a separate gate, with T-0016 review.

## 給使用者（zh-TW）

把 runner 所需環境、外部設定與狀態接續做成可重現、缺項便停止的本機流程；這張票不安裝環境或建立 lab。測試分配 6 列，無其他新票阻擋。


## Registration record — 2026-10-16

Recorded by project to-tickets after owner approval and a fresh global id scan of local tracker trees and actual origin/main/origin/staging. No implementation, executable tests, lab, remote mutation, commit or push accompanies this registration. See the registration approval and mapping for immutable review identities and exact scope.


## Implementation authority — 2026-10-16

Owner requested autonomous completion after approving PB-01–06. This supersedes the registration-only checkpoint for implementation/test/review and reviewable delivery. Production merge/automation/deployment changes remain excluded; bounded private P13 lab scope was separately approved. This independent branch starts at the common reviewed registration commit, without depending on unlanded T-0019 implementation.

## Local implementation checkpoint

PB-01–06 implemented and focused six-method run passed. See implementation/T-0020 coverage and authority records. Full regression and independent reviews pending; no actual landing or P13 completion is claimed. Earlier registration-only statements are historical, superseded by the implementation authority above.

## Reviewable delivery checkpoint

Local approved coverage and complete source regressions passed; independent Standards/Spec/security source reviews have no unresolved findings. See implementation/T-0020/execution.json and review/code-T-0020.md, review/security-T-0020.md. Final evidence supplement and actual main/staging landings are recorded separately; this ticket is not done and does not prove P13.

## Conditional actual dual-target closeout — 2026-10-18

All allocated local prerequisite rows and independent reviews are complete; the main engineering PR and staging PR33 actually landed. T-0019 also includes the separately authorized PR32 historical CLI correction. See .proj.specs/0012-publication-workflow/implementation/prerequisite-closeout-20261018/coverage.md, evidence/ and T-0020-landing.json for per-criterion evidence. Both target native readbacks pass; common1071 identities, all111 staging blog paths, all50 candidate paths, published-only main and immutable contracts are preserved. Earlier pending/review statements remain historical checkpoints. Status is now done for this repair only; actual remote capability/P13 is still NOT RUN and T-0016 remains review. No production merge, activation or deployment-setting change accompanies this closure.
