# Source-v3 independent review checkpoint

Packet /private/tmp/T21-source-v3-review; files_sha256=7d1143ad5883fba3a9fc2cd0e8882729c907a81c6bd6fe2e9fe515bd201a7902; base=HEAD=64b31a2c38959ef5490892fa2a001bb0bf2f8ca0. All 2960 entries matched.

Standards (t21_standards): new P0/P1/P2=0/0/0, historical STD-V2-01 P2=1 with adequate truthful disposition, unhandled=0, smells=0.
Spec (t21_spec): P0/P1/P2=0/1/0. Same-call identity comparison fixed but first known ID was only in memory. A known POST81/readback82 refusal left pending/check_id=None; a later same-binding retry could accept82. C3/PC-07 requires preserving the first known identity across failed attempts.
Security (t21_security): HIGH/MEDIUM=0/0, candidates>=0.8=0; no secret/authority/boundary defect found, live capability and full regression unverified. This is a distinct security threshold, not a rejection of the Spec contract finding.
Focused-v3 12 methods passed the narrower original cases. Full-v3 attempts were interrupted before source edits and are not passing evidence.

Source-v4 extends that single PC-07 test with a retry for each of existing/pending/known-POST variants: all three fail first, then pass after first known inventory/acknowledged/readback identity is saved immediately. Pending state can contain a positive integer ID; every later observation/retry must match it. Journal rename is followed by directory fsync. No approved test row or surface changes.
