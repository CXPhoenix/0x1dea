# Proposed ticket breakdown

> Resolution on 2026-10-11: the owner approved this single/no-dependency proposal
> and its original six-row table. Required spec/reviews completed and T-0009 was
> published. This document preserves the earlier proposal; current authority and
> implementation evidence live in `../../0009-test-contract-repair/approval.md`
> and `../../../.proj.tickets/0009-test-contract-repair/T-0009-test-contract-repair.md`.

Prepared with the explicitly invoked project `to-tickets` skill on 2026-10-11.
This document is a draft for approval. It does not allocate a permanent ticket id,
set a tracker status, or authorize tests or implementation. Spec, traceability and
the prescribed zero-P0 review remain prerequisites to publishing the ticket.

## 1. Proposed T-0009 — Restore deterministic complete verification and accurate gate reporting

### Context

The current local verification path combines immutable historical expectations
with mutable checkout inputs. Later product and editorial changes break historical
fixtures and mask intended rejection diagnostics. The current exact preservation
boundary does not yet accept the later reviewed source changes. Python suites lack
a complete documented entrypoint, and the Blocked view differs from its documented
selection. Old pass reports and ticket states must be distinguished from verified
current evidence.

### Deliverable

A maintainer can run one documented aggregate test command against the repair
checkout and execute the existing full Vitest and both Python suites. Historical
accepted fixtures stay deterministic under later live-source changes. The public
preservation CLI accepts only the exact reviewed successor and continues to reject
tampering. Tracker views distinguish blocked todo tickets, in-flight tickets and
their unresolved dependencies. Current article bytes and historical proof remain
intact, and reports identify their verified source version.

### Blocked by

None. T-0005 is a subject of the dependency-state audit, not a prerequisite for
implementing this repair. Required spec review and owner approvals are workflow
gates, not fabricated ticket dependency edges.

### Proposed acceptance criteria

- [ ] V1 — Existing historical component and revision acceptance cases use
  immutable inputs matching their provenance. Changing live article/theme inputs
  does not corrupt those fixtures. Existing negative cases reject the intended
  offending source rather than an unrelated earlier fixture error.
- [ ] V2 — Historical article-conversion proof uses a frozen source independently
  of current editorial content. The current article still renders three knowledge
  figures, six reference links and its original eight image alt/src pairs, with
  source citations preserved. Its task-entry bytes remain unchanged by the repair.
- [ ] V3 — The current public verifier accepts the exact reviewed successor and
  repair delta, while original manifests remain byte-identical. Wrong or missing
  pins, invalid ancestry, record or predecessor tampering, byte/type/missing/link
  drift and extra or ignored unapproved sources continue to reject.
- [ ] V4 — One documented Python command runs both existing suites and an
  aggregate command also runs Vitest. Failures, import errors and a zero-test suite
  produce a nonzero result. Existing cases are not removed or skipped to pass.
- [ ] V5 — The Blocked view selects only todo tickets with unresolved dependencies.
  Unresolved dependency edges remain visible for processing/review tickets without
  presenting them as blocked todo. Invalid dependency graphs, pending metadata
  and landing records remain rejected.
- [ ] V6 — Existing tickets become done only with actual staging containment and
  authentic authorization evidence. A missing receipt remains explicitly recorded;
  a commit or merge alone is not treated as owner authorization.
- [ ] V7 — The single observed Finder metadata file is preserved in an ignored
  local backup with matching hash before leaving the scanned source tree. The
  repair does not broaden inventory exemptions or remove unrelated files.
- [ ] V8 — Full Vitest and both Python suites, lint, build, structure, materializer
  and the current public verifier have fresh results for the repair checkout.
  Coverage and supersession notes distinguish old observations from these runs.
  Independent code/security review covers the final change; verification of this
  tooling repair uses its actual local CLI surface.

### Test plan

Reuse the six-row proposed test table in the [repair proposal](map.md#test-plan-proposed-for-owner-approval).
The table has not yet received explicit owner approval. Implement through one
failing behavior and minimum fix at a time after the required approvals.

### 給使用者（zh-TW）

這張票把測試、保存檢查與狀態呈現修到可以一起驗證：歷史測試固定讀取
對應版本，完整跑到兩組 Python 與 Vitest 測試，保存檢查只接受精確核准的
後繼內容。保留目前文章文字與舊證據；缺少 landing 授權的票維持原狀，並
清楚呈現未解決的依賴。不是把錯誤隱藏、刪除測試或把全部票改成 done。

### Boundaries

Local implementation and verification only after workflow approval. No commit,
push, PR, merge, deployment, dependency installation, external-index update,
global configuration changes, article rewriting or retrospective approval claims.

### Why one ticket

The demoable result is the complete local verification path with accurate gate
reporting. The fixture repair, source acceptance and aggregate execution are
verified together, with existing public seams and no independent product feature
to release. Separate tickets by language, manifest or tracker would leave that
integrated result unresolved between deliveries.

## Publication gate

Confirm granularity, no-blocker decision and deliverable with the owner. Before
publishing, complete the project's spec and traceability, four-axis review with
zero P0 findings, and recheck global id allocation. The proposed number is subject
to that final allocation check. The implementation test table requires approval
before the first affected test is written.
