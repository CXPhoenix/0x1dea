---
id: T-0020
title: Prepare reproducible isolated writer and validator job inputs
epic: 0012-publication-workflow
status: todo
blocked_by: []
---

## Context

Owner approved the reviewed four-slice proposal, dependencies and 23-row local prerequisite allocation with the reply ‘同意’ on 2026-10-16 (Asia/Taipei). This ticket is former draft B. The approved [requirements supplement](../../.proj.specs/0012-publication-workflow/implementation/T-0016-P13-prerequisite-ticket-proposal-20261016/requirements.en.md), [traceability](../../.proj.specs/0012-publication-workflow/implementation/T-0016-P13-prerequisite-ticket-proposal-20261016/traceability.md), [test plan](../../.proj.specs/0012-publication-workflow/implementation/T-0016-P13-prerequisite-ticket-proposal-20261016/test-plan.md) and [registration approval](../../.proj.specs/0012-publication-workflow/implementation/T-0016-P13-prerequisite-ticket-proposal-20261016/registration/approval.md) govern this ticket; original frozen epic requirements and P13 remain intact.

Inactive job examples assume installed runtime, external full configuration and reusable state. They do not yet supply a checked per-job preparation path. Temporary host locks do not serialize all jobs or manual actors.

## Deliverable

A maintainer can run a local public preflight/input-preparation flow for fresh separate writer and validator jobs, recover one durable operation journal, and obtain the same pinned operation. Missing runtime/isolation/full refs/config/state stops with a named cause. This is a reproducible local contract, not provisioning or live Actions proof.

## Acceptance criteria

- [ ] Meet B1: exact existing runtime/deps/isolation/full-history checks before writes; no install or weaker fallback.
- [ ] Meet B2: independently source-bound external inputs/digests, separate fresh jobs and credentials, explicit per-job snapshot root/UID/mode/type/link-count/open/read predicates, tamper refusals and deny-default probes; label filesystem-observation fixture limits.
- [ ] Meet B3: durable per-repository state, bounded unknown-outcome recovery, shared non-cancelling writer group, separate validator group and no global/manual lock claim.
- [ ] Meet K1–K3 and PB-01–06; approved coverage, standards/spec/security review and separately authorized actual engineering landings before done. No fake capability receipt or lab setup.

## Approved test plan

Allocated rows: PB-01, PB-02, PB-03, PB-04, PB-05, PB-06. All are approved plan rows, **NOT WRITTEN / NOT RUN**. Reuse existing behavioral regressions; distinguish public local Git/native/API-adapter and filesystem-observation fixtures from actual GitHub capability evidence. Follow one seam/test/minimal implementation per TDD cycle only after separate implementation authorization. Coverage must enumerate the listed subcases. No original P01–P24 row is renamed or marked passed by this ticket.

## Delivery boundary

Current authorization publishes tracker records only. Status is todo; do not claim work or start implementation until separately authorized. Future implementation uses this permanent ticket id on its own ticket branch. Preserve published-only main, all staging candidates/assets, target-specific historical validators/receipts/oracles/aliases and exact current successors. No active workflow, lab, installation, credential/account/rule/runner/deployment changes, merge or automation activation is granted. Done requires approved coverage/reviews and separately authorized actual engineering landings on main and staging; actual remote P13 remains a separate gate, with T-0016 review.

## 給使用者（zh-TW）

把 runner 所需環境、外部設定與狀態接續做成可重現、缺項便停止的本機流程；這張票不安裝環境或建立 lab。測試分配 6 列，無其他新票阻擋。


## Registration record — 2026-10-16

Recorded by project to-tickets after owner approval and a fresh global id scan of local tracker trees and actual origin/main/origin/staging. No implementation, executable tests, lab, remote mutation, commit or push accompanies this registration. See the registration approval and mapping for immutable review identities and exact scope.
