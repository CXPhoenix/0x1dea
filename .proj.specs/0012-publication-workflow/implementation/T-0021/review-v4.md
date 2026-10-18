# Source-v4 independent review

Packet: /private/tmp/T21-source-v4-review. base=HEAD=merge-base=64b31a2c38959ef5490892fa2a001bb0bf2f8ca0. files_sha256=80c432fde08d1cbde543636bf5b242a746ffcfbc457e35c03b317f5fe6f7103f. All 2966 entries verified independently.

## Standards — t21_standards

New P0/P1/P2=0/0/1; smells=0. STD-V4-01/P2: coverage.md:3 referred to focused12 as current while the v4 checkpoint at line31 remained pending and the packet contained only v3 focused12. Final evidence must identify the actual v4 run and preserve the earlier checkpoint distinctions. The complete v4 focused run subsequently completed 12 tests in43.149s, exit0, outside the captured source packet; final metadata supplement must resolve the inconsistent label.

Historical STD-V2-01/P2 remains accepted and truthfully documented: two earlier review regressions were batched rather than individual original TDD cycles; original logs remain. This does not assert a product defect or sequential compliance. Subsequent C3 corrections followed one-test red/minimal-green. Original trailing spaces in raw logs are preserved evidence, not a finding.

## Spec — t21_spec

P0/P1/P2=0/0/0. Prior C3 durable identity P1 closed after complete state-machine tracing. First inventory, known POST and first visible unknown-outcome readback save a pending positive ID before later reads. Known pending/confirmed identities reload and compare; missing results never trigger another POST. Ref/capability drift, RemoteError, duplicate or mismatched list/direct returns do not erase saved identity. Confirmed state follows exact direct check plus before/after source/capability/run verification. Every save file-fsyncs, atomically replaces, directory-fsyncs.
C1 exact binding, C2 credential separation and C4 inherited rulesets/non-bypass/capability invalidation remain satisfied. No additional C1-C4/PC01-07/K1-K3 defects found. Closure evidence unchanged.

## Security — t21_security

HIGH/MEDIUM=0/0; exploit candidates at confidence>=0.8=0. No candidate required separate false-positive review. Durable identity save/reload and existing owner-only journal boundary add no secret disclosure, privilege expansion or untrusted state-writer path. Same-UID malicious writers lack a demonstrated in-model permission path; point-in-time races remain declared with no merge authority.

All reviewers were read-only. This source packet did not contain the eventual complete-v4 execution results. Actual GitHub app rights/effective rules/bypass/Actions/check writes, P13, remote merge races, dependency scanning/DoS/rate-limits/low-impact hardening/cross-ticket chain analysis remain unverified or excluded.
