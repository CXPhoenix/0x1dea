# Adversarial review — round 1

Captured version: `versions/round-1/manifest.json`, 25 hash-bound files. Frozen prompt:
`prompt.md`, SHA-256 `aa59f979c01171f27e5e19c43801478299a2c49a76577d80504fbe4b9481f307`.
Base/HEAD/merge-base: `4005ee45f2f3267a8b53ce24fa97af7b49cfb144`; tracked/staged diff empty.
New-file patch and capture metadata are preserved separately. No reviewer ran product tests,
builds, remote actions or edits. These are independent design reviews, not acceptance passes.

| Axis / reviewer | P0 | P1 | P2 |
|---|---:|---:|---:|
| Completeness / workflow_completeness | 0 | 1 | 0 |
| Verifiability / workflow_verifiability | 1 | 1 | 0 |
| Contract conflict / workflow_contracts | 0 | 0 | 0 |
| Red team / workflow_redteam | 0 | 1 | 0 |
| Total | 1 | 3 | 0 |

## Findings and dispositions

All references below are to captured round-1 paths/lines. The parent accepts each finding;
there is no conflicting reviewer opinion requiring owner adjudication.

- **C01, P1, Completeness:** `spec.en.md:29,213`, `traceability.md:36`, `test-plan.md:32`.
  Correct staging SHA alone does not prove every candidate is visible at the shared alias.
  Listing may omit B or a published-path candidate revision may render old bytes. Add actual
  shared listing/navigation/pages and rendered-revision checks; unavailable website blocks.
  **Disposition:** expand AC-09, P19 and candidate/revision website traceability.
- **V01, P0, Verifiability:** `spec.en.md:169–172,212`, `test-plan.md:30`.
  `exclusion-unverified` had no decidable effect on PR-ready when exact source and build pass.
  **Disposition:** v2 PR-ready now requires all source/admission/approval/build/output checks
  to pass. Failed, missing, blocked or exclusion-unverified is blocking. Signature scan alone
  cannot grant readiness. Record conservative inability to publish undetectable short revisions
  through this gate; no implicit override. Historical v1 behavior remains unchanged.
- **V02, P1, Verifiability:** `spec.en.md:163–170,212`, `test-plan.md:27–28`.
  B's existing published route/listing/assets could be over-excluded when only its revision is
  pending. **Disposition:** exclusion is relative to pinned main; baseline published output
  remains allowed. P15 now pairs baseline acceptance with unapproved-revision rejection.
- **R01, P1, Red team:** `spec.en.md:109,120`, skill `references/workflow.md:43`, `test-plan.md:22`.
  Main and a pending revision can edit different paragraphs and merge without conflict,
  changing the registered candidate blob. **Disposition:** explicit sync comparison of all
  pending modes/blobs/metadata; any difference blocks readiness until source, registry and
  affected author approval are updated. Add conflict-free counterexample to P09 and skill.

Contract reviewer found no direct contradiction: v1 rejection remains historical, v2 is an
explicit successor, ADR-0006 done remains staging-based, one permanent sync ticket branch is
a proposed lifecycle, and four product packages retain canonical materialization. Unknown
live configuration remains a future activation gate, not an assumed success.

Before round 2 the parent checks that these narrow corrections do not override preserved
published baseline content, create automatic merge authority, weaken history or claim live
verification. The same prompt and immutable contract inputs are replayed; no third round.
