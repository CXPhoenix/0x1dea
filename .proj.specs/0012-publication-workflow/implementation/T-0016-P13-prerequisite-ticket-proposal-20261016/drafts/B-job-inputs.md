# Draft B: Prepare reproducible isolated writer and validator job inputs

**Proposal only:** no permanent ticket id or tracker status. Parent: T-0016 / P13 prerequisite supplement. **Blocked by:** none; demonstrate with the existing trusted no-workflow source, then C integrates A/B.

## Context

Inactive job examples assume installed runtime, external full configuration and reusable state. They do not yet supply a checked per-job preparation path. Temporary host locks do not serialize all jobs or manual actors.

## Deliverable

A maintainer can run a local public preflight/input-preparation flow for fresh separate writer and validator jobs, recover one durable operation journal, and obtain the same pinned operation. Missing runtime/isolation/full refs/config/state stops with a named cause. This is a reproducible local contract, not provisioning or live Actions proof.

## Acceptance criteria

- [ ] Meet B1: exact existing runtime/deps/isolation/full-history checks before writes; no install or weaker fallback.
- [ ] Meet B2: independently source-bound external inputs/digests, separate fresh jobs and credentials, explicit per-job snapshot root/UID/mode/type/link-count/open/read predicates, tamper refusals and deny-default probes; label filesystem-observation fixture limits.
- [ ] Meet B3: durable per-repository state, bounded unknown-outcome recovery, shared non-cancelling writer group, separate validator group and no global/manual lock claim.
- [ ] Meet K1–K3 and PB-01–06; approved coverage, standards/spec/security review and separately authorized actual engineering landings before done. No fake capability receipt or lab setup.

## 給使用者（zh-TW）

把 runner 所需環境、外部設定與狀態接續做成可重現、缺項便停止的本機流程；這張票不安裝環境或建立 lab。測試分配 6 列，無其他新票阻擋。
