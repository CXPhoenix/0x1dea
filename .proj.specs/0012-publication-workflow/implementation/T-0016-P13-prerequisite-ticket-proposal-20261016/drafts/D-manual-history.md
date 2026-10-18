# Draft D: Continue after one explicitly approved manual PR delivery without claiming ownership

**Proposal only:** no permanent ticket id or tracker status. Parent: T-0016 / P13 prerequisite supplement. **Blocked by:** none; demonstrate the ready path with disposable history and replayed API records.

## Context

Production PR27/28 were manual merges without operation markers. The uniquely admitted main-bootstrap exception does not admit the manual staging PR. After preparation becomes ready, the remaining ownership guard refuses that history; synchronized refs may return no-op earlier, so no live controller failure is claimed.

## Deliverable

The public recovery flow can continue past one independently approved exact manual merged delivery, records it as manual historical evidence, and creates/reuses only a newly owned matching operation. Missing approval or unrelated/mutated history still refuses. The permanent runtime branch and old records stay unchanged.

## Acceptance criteria

- [ ] Meet D1: no-op order/default ready refusal preserved; continuation approval binds every listed immutable delivery identity and ancestry.
- [ ] Meet D2: skip only that exact historical conflict, retain manual classification and original records; every listed mutation/unmerged/reopened/ambiguous case refuses.
- [ ] Meet D3: unrelated open/closed PR, fake ownership, unverified/mismatched deleted/recreated branch and closed matching owned operation remain fail-closed; preserve exact parent D4 non-force owned-branch recovery without treating manual history as owned; no duplicate/reopen/force/fallback branch.
- [ ] Meet K1–K3 and PD-01–04; approved coverage, standards/spec/security review and separately authorized actual engineering landings before done. No production PR edit or remote lab operation.

## 給使用者（zh-TW）

用明確核准的精確紀錄接續先前手動 PR，保留其手動性質；不替舊 PR 補造自動化擁有權。測試分配 4 列，無其他新票阻擋。
