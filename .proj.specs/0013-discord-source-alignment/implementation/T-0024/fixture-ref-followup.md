# Approved staging-ref execution checkpoint

Owner approved staging-ref alignment on2026-10-21. The exact proposed patch is implemented in both isolated overlays. Independent Standards/Spec reviews have zero new findings and security HIGH/MEDIUM=0/0 for this source-v4 change. All13 protected historical files remain exact.

Focused rerun: three existing workflow cases pass (main-ref drift, exact admitted workflow native readback for both projections, complete baseline preservation). The reused head-reporting case now reaches a later boundary and fails staging-sync registry validation: blog/public/.well-known/discord would be an engineering delta. The fixture main tree/parent remains prepublication while actual staging contains the record. This is a setup mismatch; the production no-blog-engineering rule must remain enforced.

First focused invocation also lacked PUBLICATION_TEST_DEPENDENCIES; that environment error is retained separately and not attributed to product code. Corrected environment execution confirms the actual secondary setup error. No full runner has been rerun for v4 because focused verification is still failing. Earlier source-v3 complete runs remain immutable failures with both historical contexts passing.

A concrete pending proposal updates only the live fixture main checkout to SOURCE refs/heads/main and the head-reporting synthetic parent to w.main; original assertions remain identical. Independent contract preflight found it preserves negative and historical cases, with no executed success claim. Source proposal/review: /private/tmp/0x1dea-discord-main-fixture-proposal-20261021/. Owner approval is pending; no main-fixture source edits applied. AC5 remains incomplete; no remote delivery.
