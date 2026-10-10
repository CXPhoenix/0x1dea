# Bounded historical and current-product reconciliation

## Problem Statement

The required preservation verifier still compares current product files with the lint-cleanup epoch. The clean, published staging baseline fails before tracker checks, and new approved components cannot be accepted by the old product inventory. Changing a checksum would erase historical proof and leave other boundaries unresolved.

## Solution

Preserve immutable adoption/publication/lint evidence. Verify their original, pinned Git epoch, then independently verify the exact known staging baseline plus specifically reviewed T-0003/T-0004 sources. Unknown paths, byte/type drift and historical tampering continue to fail. This is a local verifier increment, not a product rollback or release.

## User Stories

1. As an auditor, I want historical epochs checked against their original Git objects so later approved changes do not rewrite old evidence.
2. As a maintainer, I want the known staging baseline and approved component changes accepted so required history/tracker checks can run.
3. As a reviewer, I want unknown paths, changed bytes, invalid provenance and linked inputs rejected so reconciliation cannot silently become a general exemption.

## Implementation Decisions

The old manifests, frozen source hashes and original failure evidence remain unchanged. The last lint epoch is pinned to commit 724ddad73f8411a33c77c68d75f95b41d3af2988; reconciled staging is 32cd6a9d4ead636ddc4e5020fceb35ad9645cc7f. Both must exist and be ancestors of actual HEAD; no network/ref lookup.

A new immutable, pinned reconciliation record enumerates the historical product delta between those Git objects, with path, before/after type and hash, source commit, and an explicit present-day reconciliation receipt. This does not manufacture historical Harness approval. A separate exact component delta enumerates only reviewed paths with before/after hashes and T-0003/T-0004 provenance. Binary banner is an accepted input, not a claim that it was generated or audited by this verifier. The manifest's expected digest and exact approved component path set are part of reviewed verifier code; no arbitrary directory allowlist, editable self-approval or mutable-HEAD pin.

Data flow: validate provenance and frozen record; verify current protected product inventory against known staging Git tree plus exact component delta; build an in-memory historical projection from immutable lint Git objects; run unchanged historical preservation semantics against that projection; continue framework, tracker, translation and trace checks against current management. Existing explicit management prefixes remain as-is; new evidence is stored under existing management boundaries or outside the checkout, not allowed by broad evidence/output prefixes. The verifier does not modify files/index/refs or create commits.

Historical projection applies only after the separate current guard passes and cannot be invoked via a CLI bypass. Current existing source paths retain known staging bytes/types unless named in the reviewed delta. Missing/deleted/linked protected sources and extra unapproved product/test/docs paths fail. Generated/management ownership boundaries retain their existing checks. Guard source and its new tests are reviewed code, not purportedly self-authenticated by a circular hash.

Rollback removes the new successor and verifier integration together, restoring old fail-closed behavior; do not restore old product config or modify original epoch manifests. A stale successor rejects changed approved product bytes and requires new review rather than auto-refresh.

## Acceptance Criteria

- R1: Original adoption/publication/lint manifests retain exact historical bytes; their expected source hashes match the pinned historical Git epoch. Original clean-32cd failure receipt remains.
- R2: The clean pinned staging baseline and exact approved component product delta pass preservation, while tracker/framework/translation/trace checks still run on current management. No generic current-directory acceptance.
- R3: Extra product paths, changed config/theme/summary/banner bytes, missing source, symlink/type changes and stale component hashes fail closed through the public CLI, including untracked files.
- R4: Wrong/missing/non-ancestor pins, changed historical manifest or new provenance record, unapproved paths and before/after hashes fail; original tamper tests remain meaningful.
- R5: Read-only CLI behavior, no network/global settings/installation/publication changes, honest historical reconciliation receipt and rollback steps are documented. Old product behavior and PreviewNotice contract remain unchanged.
- R6: Full existing Python harness tests, existing product unit suite, lint/build/materializer/structural checks and actual current CLI are recorded; independent standards/spec/security review resolves in-scope findings before authorized landing. Status stays review without landing.

## Testing Decisions

Reuse the existing Python unittest verifier seam and public verifier CLI, which were already established for adoption/lint tamper tests. The user's approved correction explicitly requires real rejection red→green cases at this existing boundary; no new testing runtime or new product/browser seam. One test per actual failed guard then minimum change. Synthetic disposable clones derive real existing Git objects, never fake an approval or mutate the user's source. A clean-32cd positive case and the approved component case complement rejection cases; a unit helper result alone does not prove CLI integration. Existing product suites run once after verifier changes. Localhost recovery is separately verified with HTTP and actual Mac Chrome; no component recreation.

## Out of Scope

Framework rewrite, new general policy engine, replacing old checks, new product behavior, dependency/tool installation, historical approval backfill, blanket allowlists/waivers, commit/push/deploy/Notion, Library uploads.

## Further Notes

Owner owner receipt retained locally approved one bounded correction ticket, no technical blockers. Parent explicitly authorized the existing test seam and exact historical/component scope. External index #19 does not change repo authority. Any genuinely new security/product scope decision requires escalation, not implicit expansion.
