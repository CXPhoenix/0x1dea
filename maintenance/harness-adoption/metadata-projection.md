# Public metadata privacy projection

On 2026-10-04 the owner approved the two LOW metadata minimization changes and a normal commit/non-force push to staging. This follow-up is limited to public evidence documents for T-0001; it changes no website, skill, historical execution result or access setting. The full independent security report and the original-to-label map remain private and are not repository artifacts.

## Stable evidence labels

Labels are descriptive constants, not hashes or encodings of the original identifiers. The same receipt uses the same label in every public copy.

| Label | Retained evidence meaning |
| --- | --- |
| approval-harness-scope-01 | Owner approval of Charter, adoption scope and test matrix at 2026-10-04T07:24:41Z |
| approval-site-move-01 | Owner reply approving the site move and two alias exceptions at 2026-10-04T10:30:04Z |
| approval-site-move-question-01 | Assistant question referenced by that site-move approval |
| approval-staging-publication-01 | Owner authorization to commit and non-force push staging at 2026-10-04T11:53:10Z |
| evidence-cf-build-settings-01 | Private screenshot supporting the attributed Cloudflare build-settings attestation |
| approval-metadata-privacy-01 | Owner authorization for this metadata fix and non-force staging publication on 2026-10-04 |

## Public projection boundary

The current public copies of APPROVALS.md, deployment-handoff.md, spec.en.md, spec.zh-TW.md and review/round-2-inputs/spec.en.md replace four message identifiers and one screenshot identifier. They retain timestamps, brief quoted approvals, participant roles and substantive statements. The Chinese audit copy has a recomputed English Git-blob synchronization pin.

The captured round-2 spec copy is now explicitly a privacy projection of the historical input. The original review was not rerun or backdated; original bytes, evidence hashes and review results retain their historical meaning. The private map preserves the source-to-label correspondence. No original identifier, derived identifier fingerprint, private map or new authorization message identifier is added to this public record.

This is a forward correction. Original identifiers remain reachable in earlier public Git commits, including 1ed1348e3e7cc00bed2e073fce07fa1325335d3d. A new commit does not revoke those copies. No history rewriting or force push is performed or authorized.

## Validation coverage

The owner-approved source/evidence and translation seams were reused for this documentation-only follow-up. No raw identifier was committed as a test fixture.

| Check | Actual result |
| --- | --- |
| Private current-tree identifier scan and exact evidence-payload projection | Red on the old tree; green after all five documents were projected; private map excluded |
| English/Chinese synchronization | Updated Git-blob pin and all seven translation checks passed |
| Python harness tests | 50 passed |
| Project structure | Passed; 35 physical skills per runtime |
| Writing materializer --check | Passed; 169 generated files checked |
| Adoption/source/history/trace verifier | Passed; 55 website moves, 370 baseline entries and 113 trace rows preserved |
| Existing unit suite | 11 passed using existing Node 24.13.0 and pnpm 10.28.0, without installation |
| VitePress build | Passed under UTC; eight expected HTML routes, no management HTML; 30 available local HTML/JS/CSS/hashmap bodies match the previous fixed preview |
| ESLint | Blocked by the existing missing @unocss/eslint-plugin; CI-mode exit 2, not a pass |

The private execution receipts and affected-review reports stay outside the repository. This record makes no whole-repository security guarantee and does not infer later landing or deployment success from local validation.
