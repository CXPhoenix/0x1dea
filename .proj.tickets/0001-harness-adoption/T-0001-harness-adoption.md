---
id: T-0001
title: Adopt Harness and relocate the existing website root
epic: 0001-harness-adoption
status: review
blocked_by: []
---

## Context

The owner approved the Charter, one-ticket order/full test table and later the entire docs-to-blog site move plus two exact alias-input exceptions. Round 2 has zero P0 across four independent axes. Work uses branch tickets/T-0001/harness-adoption in an independent baseline clone; original sources remain read-only.

## Deliverable

35 complete physical skills per runtime with three canonical products, single local tracker, immutable six-capability/four-archive imports, bilingual audit and portable complete regression/rollback evidence. All 55 site files move byte-identically; six explicit adapters change only directory literals.

## Acceptance criteria

HA-01 through HA-10 and all 113 historical plus 23 adoption trace rows; spec and matrix are at ../../.proj.specs/0001-harness-adoption/. Required checks cannot be waived, reused historical answers are prohibited, and new regressions fail acceptance.

## Approved test plan

The ten-seam mandatory table in spec.en.md is the executable approved plan, with new explicit -d legacy versus blog cases and alias rejection fixtures. Approvals: ../../maintenance/harness-adoption/APPROVALS.md. Implement packages, then tracker/history, then full regression and recovery.

## Review findings carried by this ticket

P1: explicit old -d argv must not be projected. Corrected in the candidate matrix; actual CLI fixture must verify it. P2: E9 is timeline guided reading, not a docs migration fixture; corrected without modifying any input/rubric.

## 給使用者（zh-TW）

整個網站改放 blog，文章、圖片與網址維持；工程文件留在 docs。建立可重建的實體技能包與單一工作票，保留舊證據並完成全套自動測試及回復演練。本機驗收完成後，使用者於 2026-10-04T11:53:10Z 授權 commit 與非強制 push staging 供檢查；本紀錄仍待實際 landing。沒有 main merge、另行部署或 Cloudflare 修改授權。

## Coverage report

Full approved execution is recorded in [coverage-report](../../.proj.specs/0001-harness-adoption/coverage-report.md) and [portable receipts](../../maintenance/harness-adoption/evidence/README.md). Independent [code review](../../.proj.specs/0001-harness-adoption/review/code-T-0001.md) and [security review](../../.proj.specs/0001-harness-adoption/review/security-T-0001.md) cleared their declared scope. Final Standards/Spec P0/P1/P2: 0/0/0; security HIGH/MEDIUM candidates: 0. Stop at review; never set done without an authorized actual landing.
