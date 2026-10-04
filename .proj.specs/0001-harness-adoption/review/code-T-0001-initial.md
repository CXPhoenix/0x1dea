# Initial independent implementation reviews

Recorded after native reviewer reports at 2026-10-04; report recording is not backdated. Packet: code-round-1-complete, manifest SHA 6d7df364972af2eae3d274c90528f44a9f9b7d3cddaf1a90582f5b9019f2df35. Base/HEAD/merge-base: ee7fecfff72f47abc735d26ac7e9a943de04ebbf. Scope: pending tracked and untracked WIP; committed/staged empty. Reviewers were fork-none read-only native collaboration tasks, inherited session model with no override. Source reports are conversation tool outcomes; this file preserves their findings and limits.

## Standards

Reviewer `/root/code_standards_final`: P1 ×2, P0/P2 ×0; heuristic smells0.

1. README.md:60,106–108 uses pnpm blog:dev/build/preview, absent from package.json:6–8. Violates AGENTS.md:132–133 actual product commands. Restore docs:* names while keeping physical blog paths.
2. docs/guide.md:44–47 tells contributors to directly edit runtime skills and only run verify-project. This conflicts with AGENTS.md:149–152/runtime.md:142–148 canonical-only editing and materialize/check for the three writing packages. Guide is not within immutable641pins. Worst standards issue: generated editing instruction can create drift and overwrite contributor edits.

Read generator/verifier/both harness-adoption test files/trackedWIP/product writing and management contracts. Frozen1374regular hashes/641frameworkpins match; did not rerun tests or manually semantically rereview immutable framework/370source/77build. Original snapshot omitted70receipt log files due *.log ignore, so original report could not inspect their contents. Parent supplied a separate72-log frozen supplement afterward (manifest6ec2c0ece0ccd24d395dfdf0a54352f30ec248388359efb7c514b35cea08649f); this does not retroactively claim first reviewers inspected it.

## Spec

Reviewer `/root/code_spec_final`: P1 ×3, P0/P2 ×0.

1. Same README script-name regression, contrary to HA-09/spec.en.md:45,50.
2. verify-harness-adoption.py:180–184 accepts row pass with a blocked/not-run receipt because check_evidence:151–159 accepts those and only validates successful receipt logs. HA-07 requires falsely passed evidence to fail. Add blocked/not-run and mixed-success negatives.
3. verify-harness-adoption.py:299–302 searches only untracked added files; an index-staged blog/extra.md bypasses that and is absent from baseline. HA-09 requires all added product paths guarded. Include cached new paths and a staged-addition fixture.

Directly read389-linegenerator/323-lineverifier/tests/nineevidenceharness/product6diffs/runtime/roles/ADRs. Recomputed1374packetregular/641framework/169generated/302nonexceptionbaseline (including55moves) with zero hash mismatch. Did not execute implementation; initial raw-log omission limited behavioral review. Original native failure/writing provenance/historical unverified scenarios were accurately disclosed. Truthful final report/ticket gate inprogress was not counted as an implementation defect. Worst Spec issues: false successful evidence and staged-product additions.

These are implementation reviews, not a third spec adversarial round. The parent accepted actionable overlapping findings for correction; there was no conflicting reviewer decision requiring owner adjudication. The first packet remains immutable. A new packet will include fixes and all raw logs for affected re-review.
