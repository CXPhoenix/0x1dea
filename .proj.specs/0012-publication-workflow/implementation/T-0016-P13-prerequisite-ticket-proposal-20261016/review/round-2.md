# Round 2 — proposal-v2, final requirements round

Packet: `/private/tmp/T16-P13-prerequisite-review-round2`; files manifest SHA-256 `4d6679da51298d028c983c14b74fb23860bb4b0d4f54fa71692365b1ca6ad6b6`; context SHA-256 `e54c458ed824b4c09d43dfc652f1c0c8eef1a70127cbf9e815df31629eb4507f`. Frozen prompt SHA-256 remains `8159428349fc05f1841e42db54967d3b7cd710ea7d470e80d1c65c3a505586da`, byte-identical to round 1. Each independent reviewer checked all 2,731 captured entries, including three literal aliases. Source context now explicitly records detached working HEAD, main/staging tree pins, merge-base, untracked inventory and tracked/staged/HEAD patches.

| Assigned axis / independent reviewer | Unresolved P0 | P1 | P2 | Reported verdict |
|---|---:|---:|---:|---|
| Completeness / t13_sync_spec | 0 | 0 | 0 | Proposal may be sent to owner |
| Verifiability / p13_prerequisite_verifiability | 0 | 0 | 0 | V-01 resolved; proposal may be sent to owner |
| Contract conflict / t13_sync_standards | 0 | 0 | 0 | C-01 resolved; proposal may be sent to owner |
| Red team / t13_sync_security | 0 | 0 | 0 | Proposal may be sent to owner |

## Independent conclusions recorded by parent

**Completeness:** B2's root/UID/mode/type/link-count/containment/open/read predicates reach traceability row 4 and PB-03; D3 exact owned recovery and mismatched/unverified refusal reach lifecycle traceability and PD-04. A1–D3/K1–K3 have no missing allocated type/field/boundary. A6+B6+C7+D4 remains 23 unique rows. Edges remain acyclic with A/B/D independent, C consuming A/B and proposed T16 consuming C/D.

**Verifiability:** V-01 closed by requirements.en.md:33 and PB-03. A root-owned input while effective job UID differs now has an explicit refusal result. Actual filesystem cases and observation fixtures are distinguished. D3 positive exact recovery versus negative mismatched recovery are separately decidable. Readiness, actual landing and completion boundaries remain separate. Added HEAD/merge-base context closes the previously disclosed source-metadata limit. This is no implementation/security audit or live P13 verdict.

**Contract conflict:** C-01 closed by requirements.en.md:55, D draft, PD-04 and lifecycle traceability; exact parent D4/ADR-0008 non-force owned recovery remains intact, without deriving ownership from a manual-history grant. B2 snapshot restrictions exclude writable durable state, so B3 is not contradicted. No new conflict with parent rules, historical contract or candidate preservation was reported.

**Red team:** The revised snapshot identity restrictions do not let candidate data approve itself or broaden credentials. Manual continuation still cannot launder ownership, ignore unrelated closed PRs or overwrite mismatched refs. Finite workflow admission, independent capability evidence, credential separation, unknown-outcome refusal and head/base/main drift expiry retain their original boundaries. No new unintended trust crossing was reported.

## Scope limits

All reviewers were read-only and performed no candidate execution or remote actions. The 23 local plan rows are NOT WRITTEN / NOT RUN. Original P13 a–l remains NOT RUN; actual permissions, runner, reporter, check enforcement, races and landing evidence remain unverified. There is no unresolved reviewer disagreement and no third/fifth arbitration pass. This is the second and final requirements round. New unresolved P0 after this ceiling would require splitting/reconverging; none remains in this reviewed version.
