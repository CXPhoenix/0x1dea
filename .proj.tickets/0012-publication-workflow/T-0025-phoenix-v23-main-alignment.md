---
id: T-0025
title: Align the exact Phoenix v2.3 shared writing baseline onto main
epic: 0012-publication-workflow
status: review
blocked_by: []
---

## Context

Owner explicitly requested main fast-forward and the existing staging Phoenix v2.3 writing baseline on main. This is the exact approved-writing-successor exception in epic D2 / AC-02; the implementation plan and retained approved public test seams are in implementation/T-0025-phoenix-v23-alignment/plan.md.

## Deliverable

Main contains the exact staging v2.3 canonical package and deterministically generated Codex/Claude copies, active input/output identities and source provenance. A finite current-verifier successor admits only these reviewed identities. No website content or preview configuration is published by this ticket.

## Acceptance criteria

- Ten transferred identities match pinned staging bf6f872 exactly; generation is deterministic and other packages/aliases retain their bytes.
- Exact current main/staging engineering projections accept the successor, while modified/missing/linked/executable/unlisted writing inputs remain rejected.
- Preserve the original public wrapper, materializer, frozen tests, runner, M0, old assertions and historical evidence.
- Main blog tree is unchanged; all 50 staging candidate paths, original workspace and existing backups are preserved.
- Capture coverage and independent code/security review; actual authorized main landing is observed separately from publication readiness.

## 給使用者（zh-TW）

將 staging 既有 Phoenix v2.3 寫作基準單獨移植到 main，同步 Codex／Claude 套件與必要的精確來源驗證。候選文章、圖片、備份及歷史驗證契約均保留，不調整作者風格。

## Comments

Owner authorization and existing epic-seam mapping: implementation/T-0025-phoenix-v23-alignment/approval.md and plan.md. Implementation is verified and independently reviewed; status remains review until actual authorized main landing.
