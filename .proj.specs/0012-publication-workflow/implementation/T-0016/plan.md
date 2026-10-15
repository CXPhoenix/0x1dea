# T-0016 implementation plan

Goal: finish evidenced T12/T14/T15 closeout, then implement the approved P10-P12 trusted writer adapter without activating production automation. Existing reviewed epic0012 and owner-approved 24-row allocation are the design and seam authority; no new requirement interview or duplicate approval is needed.

Architecture: reuse local staging-sync prepare/verify as the source-of-truth seam. A trusted Python orchestrator serializes participating operations, owns only the permanent sync branch/PR, rereads remote pins, and requires observed exact-input trusted validation. Ship inactive workflow templates outside .github; actual remote exercise P13 and activation remain blocked without separate disposable-repository authority. No deployment configuration or repository-rule changes.

Tech: Python standard library, disposable real Git, fake GitHub transport for P10-P12, existing Node/VitePress and enforced build harness.

1. Record primary PR20/21/25/26 actual landings and complete blob/mode preservation, acceptance table and receipt identities. Add one native CLI positive test (red), implement exact closeout metadata, then receipt mutation negative tests at the same approved seam. Update live fixture target context only; preserve historical assertions/oracles.
2. P10: one fake-adapter public runner test for repeat event/owned-PR identity (red), implement deterministic operation identity and branch/PR readback, then no-op/ownership/closed-PR variants one at a time.
3. P11: test accepted-but-lost response (red), implement readback-before-retry; test concurrency/drift/403/timeouts and bounded three retries with shared repository lock. Never mutate target refs or force push.
4. P12: test acknowledgement-only (red), implement exact successful trusted run binding. Add stale/failed/missing/wrong-policy and untrusted shell/token tests at the same interface.
5. Add supported CLI/schema and inactive main-event/dispatch workflow templates with shared writer concurrency, read-only validation boundary, no writer token in build job. Explicit remote receipt/permission/protection gate must prevent activation without P13.
6. Run focused/full native Python, product unit/lint/build as affected; independent Standards/Spec/security reviews; actual native CLI exercise. Retain P13 as unverified, not skipped-success. No commit/push/PR/merge is inferred from this implementation request.

Files: scripts/publication_remote.py; scripts/staging-sync-remote.py; tests/article_publication/test_remote_sync.py; tests/article_publication/test_landed_closeout.py; finite current successor/runner fixture context; docs/staging-sync-remote.md; maintenance/publication-workflow/automation/*.yml (inactive only); exact engineering map; ticket/landing/coverage/review artifacts under the configured tracker.
