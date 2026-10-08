# Authorized lint cleanup follow-up

The owner authorized cleanup of existing lint and dependency compatibility issues,
commit and non-force push on the current ticket branch, and one combined draft PR
targeting staging. Merge, direct protected-branch push, deployment, trust/security
configuration and external tracker updates remain outside this work.

## Scope and acceptance

The complete first-party ESLint scope is `scripts/`, `tests/`, `blog/shared/`,
`blog/.vitepress/` and the root ESLint, Vitest, UnoCSS, TypeScript and package
manifests. ESLint checks its supported JS/TS/Vue/JSON/YAML sources; Python is covered
by the CLI/harness suites, structure and preservation validators. `pnpm lint` must
exit zero with no warnings. No rule disabling, new ignore rules or weaker assertions.

Published Markdown, public assets, CSS, historical evidence and imported framework
packages are immutable in this follow-up. `eslint .` is a broader diagnostic, not
the first-party check: it includes historical instructional snippets and pinned
third-party packages. Record its actual result and exclusions, never call it green.

Add a separate exact successor boundary pinned to the pre-cleanup commit
`8890d5250e22ec4ee0e0493c1e72bab89d16489b`. Keep adoption manifests and the article
publication predecessor boundary unchanged. Only enumerated first-party source
updates and the necessary manifest/lockfile change may pass. Verify dependency
versions and semantics, not only successor hashes.

## Approved verification seams

This is the existing preservation/dependency, CLI, harness, Vitest and build matrix
extended by the explicitly authorized cleanup and lint reproduction checks. No new
product behavior or publication authority is introduced.

| Seam | Red / regression check | Acceptance |
| --- | --- | --- |
| Complete first-party lint | Record file/rule diagnostics before fixes | Same full scope passes with zero warnings |
| Dependency compatibility | Installed ESLint 10 violates existing peer ranges | Exact ESLint 9.39.2; UnoCSS plugin 66.6.0 retained; no unrelated version drift |
| Preservation successor | Old exact-byte boundary rejects formatting | Exact before/after files, immutable historical manifests, reject unlisted/tampered source |
| Article/website preservation | Compare source tree and built route/content output before/after | Article/assets/CSS bytes identical; website behavior and markup preserved |
| Product regressions | Existing CLI, harness, Vitest, build/materializer/structure commands | All pass on final sources |
| Delivery | Standards, Spec and affected security/public-information independent review | Findings resolved; draft PR targets staging at exact pushed SHA |

The Notion index is maintained by the parent. This follow-up remains review, not done.

## Observed results and limits

Initial focused CLI/helper/manifest reproduction: 363 errors. Original unrestricted
ESLint 10 invocation stopped with exit 2 because no UnoCSS config existed. A
temporary default-empty config allowed diagnostic classification: 1,232 files,
182,876 errors and 48 warnings; the related first-party subset was 20 files,
517 errors and 46 warnings. The final `pnpm lint --format json` scope is 22 files
(including the new shared UnoCSS config and preservation regression tests), zero
errors/warnings and exit 0. Every final file/rule diagnostic is recorded; no new
ignores or disabled rules. The broad diagnostic remains an explicit existing failure.

The only direct dependency change is exact ESLint 9.39.2. All added/removed package
versions are reachable through the old/new ESLint dependency closure; intersecting
package metadata and unrelated direct versions are unchanged. The UnoCSS plugin
remains 66.6.0. Clean frozen installation with strict peer checking and scripts
disabled exits 0; no peer-range warning remains. Existing deprecation notices are
not hidden. Source reference: UnoCSS [ESLint integration](https://unocss.dev/integrations/eslint)
and [configuration](https://unocss.dev/guide/config-file); installed 66.6.0 source
confirms the Vite wrapper's default Wind3 preset, now shared explicitly with lint.

CLI 16, harness 53 and Vitest 14 pass on final sources. The three new Vue regression
expectations also pass on original pre-cleanup sources. Preservation adds explicit
counterexamples for arbitrary dependency/script drift, unknown successor paths,
wrong pins/hashes, source tampering and historical-boundary changes. Public-function
comparison passes eight transform fixtures (including current article frontmatter),
nine CLI argument fixtures, four asset-path fixtures and two YAML files.

Both built versions have eight identical routes; their normalized HTML is identical.
Changed asset hashes, corresponding Vue scope IDs, class-token ordering and the
generated route hash map are presentation-normalized for comparison. CSS rules are
identical after mapping corresponding component scope IDs; import sorting reorders
scoped PostBlock/PostCard rules. This is content/cascade review, not pixel identity.
Published Markdown, public assets and authored CSS bytes are unchanged.

Chrome loaded both localhost builds with matching article/date/order output, but
input dispatch timed out before sorting/search interaction. Interactive browser
verification is therefore blocked, not passed. The Vue interface tests cover search,
sorting, category route headings, view switching and timestamp rendering. No new
sandboxed candidate build is claimed; the publication CLI and harness rerun the
current safety fixtures, while prior host-specific isolation evidence remains
historical and bounded to its synthetic candidate.

## Lint cleanup final coverage

| Check / surface | Final observed result | Evidence / limit |
| --- | --- | --- |
| First-party ESLint | 22 files, 0 errors / warnings, exit 0 | lint-cleanup-green.json; broad diagnostic is a separate existing failure |
| CLI / harness / Vitest | 16 / 53 / 14 pass | lint-cleanup-validation.json; Vue regressions also pass on pre-cleanup sources |
| Build / materializer / structure / preservation | All exit 0 | Final logs and separate pinned lint successor; historical manifests unchanged |
| Fresh install / lint / Vitest / build | All exit 0 | Frozen lockfile, strict peers, official registry, installation scripts disabled |
| Website / articles | 8 routes, normalized HTML / mapped CSS blocks equal; read-only bytes unchanged | lint-cleanup-build-comparison.json; not pixel identity |
| Independent Standards / Spec | No residual findings | review/code-T-0002-lint-cleanup.md; language P2 resolved |
| Security / public information | No HIGH/MEDIUM candidates; no residual public gate finding | review/security-T-0002-lint-cleanup.md; host paths sanitized and hashes rechecked |
| Interactive browser / fresh candidate OS-isolated build | Blocked / not rerun | Chrome input timeout; earlier isolation is historical, scoped fixture evidence |

Reports and evidence paths above resolve from this epic, with log/JSON files under
`evidence/`. Commit/branch push/draft PR do not mean merge, deployment or done.
