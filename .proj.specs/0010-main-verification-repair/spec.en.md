# Main verification repair

## Problem Statement
After owner-merged PR #17, the preservation CLI rejects the legitimate electricity article release and one Python harness positive control reads current source into an immutable lint-era fixture. Existing historical contracts must remain unchanged.

## Solution
Validate the already merged release as one exact successor to its main predecessor, and run historical tests using pinned epoch input with the current verifier. Keep historical and current validation separate; both must pass.

## User Stories
1. As the owner, I want the main verification commands to accept the exact merged article release while detecting additional or changed product input.
2. As a maintainer, I want historical positive and tampering controls to test their original contract after later product changes.

## Implementation Decisions
- Preserve all article, image, dependency, framework and historical evidence bytes. Do not import the staging reconciliation chain or its other five candidates.
- Pin predecessor e457143e8be2f7d54f69bc3e9b80230375be49de, release 604f8733ca47d67fc277ec127a9da743cefbc22e, and owner merge 88b9c53852f527ee636bcc4b4ca5e166f6ec10fd. The release and merge must be actual HEAD ancestors; the predecessor must be a release ancestor. Missing objects fail closed.
- Use the existing release scope, pinned by its immutable Git blob and SHA-256, as the exact 34-path product delta oracle. Validate the complete release delta: those 34 paths plus the exact 11 existing release evidence paths. Validate before/after identities from Git objects and compare current protected inputs to the merged release, including type and executable mode.
- The reviewed verifier and harness repair code are explicit trust roots; require each repair source to exist as a regular file. Management additions retain existing management rules. Pin existing historical boundary/provenance files and existing release evidence to Git bytes even where management rules normally allow changes.
- Run old preservation checks against validated predecessor bytes only after validating the exact live successor. Do not refresh old expected hashes, infer approval from current bytes, or introduce a skip flag or generic update mechanism.
- Reject missing, linked, changed-mode and changed-byte protected input, unknown tracked/untracked input and ignored source under blog, docs and tests. Generated VitePress dist/cache/.temp and Python __pycache__ directories are outside source inventory; linked generated directories fail.
- The existing lint positive control materializes its accepted epoch from commit 724ddad73f8411a33c77c68d75f95b41d3af2988. Its negative cases and hash expectations remain intact and no skip is introduced.

## Acceptance Criteria
- M1: The existing lint historical positive control and its tampering cases pass with current verifier code and frozen epoch input. Missing pinned input must error, not skip.
- M2: The public preservation CLI accepts the merged main plus only reviewed repair code/management additions, and still executes baseline/framework/lint/translation/trace/tracker checks.
- M3: The same CLI rejects changed article/config or historical evidence, a forged release scope, missing/linked/mode-changed protected source, missing repair code, nonancestor/missing pinned objects, and extra tracked/untracked/ignored source. Each negative test begins with an accepted positive control and identifies the intended rejection.
- M4: The complete 45-path release diff and its 34 product identities are validated against pinned Git objects. All pre-existing historical boundary files, article fixtures, current article/assets and package/lockfile remain byte-identical to the merged main.
- M5: Full Vitest, both Python suites, lint, build, structure, materializer and public verifier pass on this repair checkout. Record actual commands, exits, test counts and skipped cases. Independent standards, spec and security reviews have no unresolved blocking findings.

## Testing Decisions
Reuse the owner's approved Python verifier CLI/disposable Git fixtures, current preservation CLI and complete-command seams. Extend tests one red-green slice at a time. Use literal pinned Git epochs and existing release evidence as independent oracles, never live-derived expected hashes. Keep all existing negative tests. Scope is local Git/CLI behavior and website build compatibility; no deployment or browser behavior is changed.

## Out of Scope
Article edits, other candidate publication, staging chain import, test runner redesign, dependency installation, commits, pushes, new PRs, merges, deployment and external index updates.

## Further Notes
This is a single no-dependency follow-up to the owner's approved test-contract repair intent, after T-0009 was marked done. Global ticket allocation uses staging's maximum T-0009 even though main has older tracker content. Prior release gate and failing logs remain historical evidence, not rewritten to claim they passed. Landing status stays review until separately authorized landing.
