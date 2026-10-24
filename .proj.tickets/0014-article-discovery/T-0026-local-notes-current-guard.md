---
id: T-0026
title: Keep authorized local writing notes compatible with the current source guard
epic: 0014-article-discovery
status: review
blocked_by: []
proposal_key: A
test_plan_approved: true
approval_evidence: .proj.specs/0014-article-discovery/planning/approval.md
---

## Context

Implement approved slice A of the [reviewed article-discovery specification](../../.proj.specs/0014-article-discovery/spec.en.md). The owner approved all four slices, dependency edges and test plans, and explicitly requested starting A with TDD. The product principle remains: talk freely first; organize settings only when useful. The [approval receipt](../../.proj.specs/0014-article-discovery/planning/approval.md) binds the original proposal and shared checks.

## Deliverable

On otherwise valid disposable current main and staging targets, an authorized note save/update under the finite default namespace leaves native verification successful with the same role and non-note source identities. Malformed, tracked or trusted-source collisions still refuse. The complete deliverable includes namespace classification, Git-ignore convention, narrowly reviewed current identities and native CLI evidence. It does not require or create an article-discovery skill or an actual author's workspace.

## Acceptance criteria

- Implement only D5a's finite local-output shape: real root/workspace directories, one valid key component, and immediate regular non-executable PROJECT.md, GLOSSARY.md or compatibility CONTEXT.md files. Empty real directories are valid; validate the entire namespace before exclusion.
- Refuse a namespace entry tracked in candidate HEAD, present in its Git index, or named by the trusted expected source inventory. An arbitrary ignored file or caller-selected path receives no exemption.
- Notes do not become trusted configuration, executable input, materializer input or publication input. Preserve all other source names, modes, hashes, role/history/policy checks and the original historical behavior.
- Add the default Git-ignore convention without untracking anything, creating author notes, or implying confidentiality. Review only finite live successor identities needed for this delivery; preserve frozen validators, fixtures and evidence.
- Demonstrate a full native pass → save → pass → update → pass on both valid current roles; no mock of source enumeration substitutes for this evidence.

Primary traceability: R20 (guard portion), R38, R45–R47; AC-16/17. C owns author-facing workspace lifecycle and replays this boundary through actual save/resume interactions.

## Approved test plan

The following table is copied unchanged from approved proposal A. Approval is for the plan, not evidence of execution. Shared X01–X03 apply as scoped in the [approved overview](../../.proj.specs/0014-article-discovery/planning/ticket-proposal/README.md#共用驗證與收尾). Preserve one public seam, one failing behavior and one minimal implementation per TDD cycle.

| ID | Seam | Test intent | Scope | Acceptance criterion | Boundary conditions |
|---|---|---|---|---|---|
| A01 | Native current verification CLI + independent Git fixtures | Establish a valid baseline, then create, update and remove each permitted note; compare role and non-note identity records | Both current main and staging; absent root, empty root/workspace, PROJECT, GLOSSARY and legacy CONTEXT; AD35 | AC-17; R20/R45 | Every normal phase passes; free-form and instruction-like note text cannot alter trusted behavior; no production workspace mutation |
| A02 | Native CLI namespace inspection | Reject malformed directory shapes and reachable invalid-key representations | File/symlink root or workspace, nested directory, extra filename, backslash key; AD36 | AC-17; R46 | Valid Unicode/space keys are not rejected merely for their spelling; slash nesting is invalid; nonrepresentable empty/dot keys are covered at C03's file-action boundary |
| A03 | Native CLI namespace inspection | Reject unsafe note object types and executable modes | Each permitted filename as a link, FIFO/socket or executable regular file; AD36 | AC-17; R46 | Include dangling links and links outside the fixture; protect an external sentinel; unsupported object types are named unverified, never silently passed |
| A04 | Native CLI + independently prepared HEAD/index/inventory | Reject each source-ownership collision independently | HEAD-tracked but index-removed note; index-only forced addition; trusted expected-inventory entry; AD37 | AC-16/17; R47 | Git ignore does not hide ownership; no candidate-controlled expected inventory; preserve frozen historical input contracts |
| A05 | Native CLI full source comparison | Refuse a valid-looking namespace containing one invalid object, and refuse an unrelated extra source outside it | Both roles; mixed valid/invalid notes and external source mutation; AD36 | AC-17; R46 | No partial-namespace success, early success or broad directory waiver; custom paths are not configurable exclusions |
| A06 | Existing current/historical verification interfaces + identity audit | Admit exact reviewed live successors and retain existing rejection/preservation behavior | A's affected regression cases, historical runner/assertion hashes, role/history and finite identity mutations; AD34/AD37 | AC-16/17; R38/R47 | Changed/missing source, mode/hash drift and role/history tampering still fail at their existing public seam; historical fixtures are not rewritten to pass |

## Implementation boundaries

Use branch `tickets/T-0026/local-notes-current-guard`. Follow the approved proposal's evidence requirements and existing engineering review/landing gates. No new remote Git/publication or installation authority is granted. Original proposal references A–D denote the mapping in the approval receipt, not additional global ticket ids.

## 給使用者（zh-TW）

這張票交付「筆記可以變動，但工程來源仍精確驗證」的完整行為。只接受預設資料夾內三種指定筆記檔；多一個檔案、出現連結、可執行檔，或與已追蹤／受信任來源重疊，都必須拒絕。會實際在有效的 main、staging 暫存案例各跑一次保存前、保存後與更新後驗證；不會替一般聊天建立資料夾。

拆分與測試表已核准；實際進度以本票 frontmatter 與驗證紀錄為準。

## Comments

2026-10-24: allocated from approved proposal A; initial state todo. Only A is authorized to begin implementation in the current request. B–D retain their approved plans and dependency edges; do not infer implementation or landing completion from allocation.

## Implementation evidence

2026-10-24: local TDD complete in `/private/tmp/0x1dea-T0026`, branch `tickets/T-0026/local-notes-current-guard`, HEAD/base `8b2cffab8ed1a8a2c50ece18b6fe5b578f186668`; no ticket commit or landing. The [coverage report](../../.proj.specs/0014-article-discovery/implementation/T-0026/coverage-report.md) records 12 new native test methods / 143 expected CLI outcomes, the 260-test full Python pass, 54 Vitest passes, and preserved historical artifacts. [Implementation evidence](../../.proj.specs/0014-article-discovery/implementation/T-0026/README.md) includes the patch, failure disposition and exact-source reconstruction list. Formal [Standards/Spec review](../../.proj.specs/0014-article-discovery/review/code-review-T-0026.md) and [security review](../../.proj.specs/0014-article-discovery/review/security-T-0026.md) are closure artifacts; B–D remain unimplemented. Status stays review until authorized landing.
