# Round 1 — proposal-v1

Packet: `/private/tmp/T16-P13-prerequisite-review-round1`; files manifest SHA-256 `2c1895df47a7f00c1748f260f4e50e185f632a4471716a421f171ab02260fa68`. Prompt SHA-256 `8159428349fc05f1841e42db54967d3b7cd710ea7d470e80d1c65c3a505586da`. Four independent read-only contexts checked the same 2,730 entries (2,727 regular files, three literal aliases). No candidate code or remote exercise was run.

| Axis / reviewer | P0 | P1 | P2 | Verdict |
|---|---:|---:|---:|---|
| Completeness / t13_sync_spec | 0 | 0 | 0 | Covered within this axis |
| Verifiability / p13_prerequisite_verifiability | 1 | 0 | 0 | V-01 blocks formal tickets |
| Contract conflict / t13_sync_standards | 0 | 1 | 0 | C-01 requires D correction |
| Red team / t13_sync_security | 0 | 0 | 0 | Covered within this axis |

## Findings and bounded corrections for v2

**V-01, P0:** requirements.en.md:31 B2 and test-plan.md:17 PB-03 referenced ownership/path constraints without a decidable owner/root predicate. A digest-correct root-owned input versus a job-owned input had no unique expected result. Correction: define the consumed per-job snapshot's independently approved external canonical root, effective-UID owner, directory/file permission bits, regular file/link-count/containment and checked open/read identity. Source copying may precede sealing; writable durable state is explicitly outside the read-only snapshot predicate. PB-03 varies each condition and labels owner/race observation fixtures versus actual filesystem tests. Reviewer also noted missing explicit working HEAD/merge-base metadata; v2 context records these without claiming remote exercise proof.

**C-01, P1:** requirements.en.md:53 D3, drafts/D-manual-history.md:17 and test-plan.md:31 incorrectly treated all deleted/recreated branches as refused. Parent spec D4 (spec.en.md:128), ADR-0008:23 and existing remote seam permit exact verified owned branch recovery, non-force. Correction: refuse only unverified/mismatched recreation, explicitly preserve that existing owned recovery, never derive ownership from manual history admission. PD-04 includes its positive and negative cases. No new historical exception or branch rename is introduced.

## Self-check before second round

The B clarification decides previously unnamed predicates rather than adding a new job/permission system; it applies to consumed read-only config snapshots, not writable journal storage, so it does not conflict with B3. The D correction restores parent behavior rather than weakening manual-history ownership. Rechecked A1–D3/K1–K3, the 23 row ids, unchanged allocation A6/B6/C7/D4 and acyclic edges A/B/D independent, C→A/B, proposed T16→C/D. No original spec, tracker, executable test, article or active workflow changes. Both findings remain open pending independent round 2. Round 2 uses the identical prompt and same axis assignments; only the captured proposal version changes.
