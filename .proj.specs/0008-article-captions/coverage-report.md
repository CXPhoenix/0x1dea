# Coverage report — local implementation

Owner-approved seams and ticket: approval.md and test-plan.md. No percentage instrumentation is configured; report executed cases and observed surfaces rather than inventing a coverage percentage.

| Seam | Tests | Measured coverage | Criterion | Uncovered, and why |
|---|---|---|---|---|
| VitePress Markdown renderer → HTML/error | 23 behavioral cases before article/guide cases | Passed: figures/tables, independent/reset counters, forward/reordered/inserted refs, literal contexts, captions/links/safety, malformed inputs, static IDs and namespace reuse | C1–C5 | Dynamic Vue IDs and cross-article references excluded by spec |
| Task-entry source → migrated source/HTML | 1 case | Passed: all eight alt/src pairs, three figures, six references, source links; inverse conversion SHA-256 equals original task-entry bytes | C6 | Assets unmodified; no table invented in article |
| Author guide → public Markdown renderer | 1 case | Passed: copyable guide sample covers figures/memes/tables/refs/source note | C9 | None within defined author forms |
| Served article and temporary table fixture → browser | Eight layout cases plus native keyboard and client navigation checks | Passed at 1280/390px light/dark, font 17.5px, contrast 10.94:1/12.81:1, no clipping/overflow; correct hash and no duplicate figures after SPA navigation | C7 | Local browser only; no staging/production claim |
| Existing product commands | 86 tests; full lint; VitePress build | All passed (full suite 86, lint zero errors, build successful). A subsequent type/lint-only edit passed affected 25 tests and full lint; final build after those edits and fixture cleanup also passed | C8 | Structure/materializer rejected the same pre-existing metadata drift; historical adoption verifier rejects authorized current product deltas as well; see below |

## Red → green evidence

The author approved the table before the first test. Each behavioral slice was written before its implementation: figures, tables/reset, reference insertion/reorder, diagnostic cases, literal contexts, rich/safe captions, static collisions, article migration and guide compilation. Observed failures included missing feature module, absent table captions/reference links, duplicate and invalid-reference diagnostics not throwing, unrendered emphasis, unreported anchor collisions, zero migrated figures and missing guide. Each was followed by a passing affected run. Initial test-loader URL rewriting required the repository's existing NodeURL alias; a Shiki span selector was narrowed to the authored title-bearing span. Those harness corrections are not counted as product behavior coverage.

## Baseline limitations (observed before implementation)

- `python3 scripts/verify-project.py`: FAIL, `.claude/skills/.DS_Store` bundled cache.
- `python3 scripts/materialize-writing-skills.py --check`: FAIL, extra `.DS_Store` in canonical maintaining-writing-skills and phoenix-writing trees.
- `python3 scripts/verify-harness-adoption.py`: FAIL, changed current reconciliation source `blog/.vitepress/theme/index.ts` (prior product work).

No metadata, historical guard, lockfile or installed dependency was changed to bypass these failures. Local-only delivery; landing not performed.

## Final check results

Structure and materializer still reject the same task-entry `.DS_Store` files. Final adoption verification now first rejects `blog/.vitepress/config.mts`, an authorized new product delta, whereas task-entry verification first rejected prior `theme/index.ts` work. Both are immutable-history mismatches; this is recorded rather than relabeled as a pass. No historical verifier was modified. The final VitePress build passed in 13.76s after temporary fixture removal. Independent Standards/Spec review found zero actionable issues; security review found zero concrete HIGH/MEDIUM candidates.
