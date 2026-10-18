# Draft C: Report trusted validation on the exact PR head and expire stale readiness

**Proposal only:** no permanent ticket id or tracker status. Parent: T-0016 / P13 prerequisite supplement. **Blocked by:** A and B. Not blocked by D: use an independently owned fresh-operation fixture.

## Context

A trusted-main dispatch run is not a check on the candidate PR head. The read-only validator cannot publish it. Head-only merge guards do not protect target-base freshness or source-main/policy drift.

## Deliverable

A separate local trusted reporting adapter binds a completed successful run to the exact candidate head and configured check identity; local readiness refuses missing capability or stale head/base/main/policy/workflow. Integrate A's synthetic admission and B's source-bound job inputs with public adapter/Git fixtures. The ticket establishes observable requests/refusals, not live branch protection or permission proof.

## Acceptance criteria

- [ ] Meet C1: exact independently read run/source/head/report binding, successful check readback, all non-success/ambiguous cases refuse.
- [ ] Meet C2: separate reporter identity/credential without expanding writer/build/merge/admin privileges or exposing credentials.
- [ ] Meet C3: before/after ref/report readback, unknown-result recovery and distinct head/staging/main/policy/workflow drift invalidation.
- [ ] Meet C4: independently observed strict/check-source/non-bypass capability is required for live readiness, local fixtures cannot satisfy it; no point-in-time observation is called a merge lock, base CAS or later-main guarantee.
- [ ] Meet K1–K3 and PC-01–07; approved coverage, standards/spec/security review and separately authorized actual engineering landings before done. Actual enforcement remains P13; no rule/queue/workflow activation or merge here.

## 給使用者（zh-TW）

讓可信驗證對應到指定 PR head，來源或目標更新就撤銷舊判定；遠端保護是否真正生效，仍由 P13 驗證。測試分配 7 列，須等 A、B 完成。
