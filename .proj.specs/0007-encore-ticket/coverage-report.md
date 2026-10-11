# Local coverage report

| Seam | Tests / observations | Measured coverage | Acceptance criterion | Uncovered / limitation |
|---|---|---|---|---|
| Public component mount | 2 Vitest cases: exact native-link recommendation; two independent instances, literal text, omitted description | 2/2 passing; percentage not instrumented | E1 | Invalid/untrusted URLs are outside trusted-author contract |
| VitePress build → actual article SSR | Real build; parsed recommendation anchor/title/description/action, separate following heading, no unresolved component tag | One actual consumer; passed | E2 | No second production consumer added |
| Served built article → browser | 1280px/390px × light/dark: no overflow; native link tree, visible Tab focus and Enter navigation verified | Actual built surface, not prototype | E3/E4 | See browser-evidence.md; local built site only, no deployment |
| Task-entry → final article | Byte equality against task-entry article after exactly one literal paragraph substitution | Exact comparison passed; existing caption retained | E5 | No preservation verifier pass claimed |
| Unit/build | Full Vitest suite, production VitePress build | 61/61 tests; build passed | E6 | No line-coverage percentage measured |
| Lint | After owner-authorized frozen-lockfile dependency restoration, standard pnpm lint executed with the declared UnoCSS plugin and ESLint | Full command passed, exit 0 | E6 | Earlier targeted check and missing-plugin failure are historical observations |
| Structure/materializer | Both commands executed | Blocked by existing .DS_Store metadata in skill trees | E6 partial | These unrelated files remain untouched |
| Preservation verifier | Task-entry rejected existing article caption; final run rejects changed theme/index.ts registration | Baseline failure observed | E5/E6 | Both outputs observed separately; guard stops on the first error, so the new-file inventory rejection is additionally established from static control flow; immutable records untouched |

## TDD observations

The first public-component test failed before EncoreTicket existed (import resolution), then passed after native-link rendering. An initial test assertion incorrectly counted the root anchor as a nested anchor; corrected the test to one anchor and no interactive descendants before continuing. The optional-description case then failed because the minimal template emitted an empty paragraph and passed after conditional description rendering. The actual built article check failed before registration/paragraph replacement and passed after integration. No production behavior was changed to accommodate an incorrect assertion.

## Source preservation

Task-entry snapshot is retained locally in the local frozen review-v1 packet. Final article equals that snapshot with exactly the single original recommendation paragraph replaced by the EncoreTicket invocation. No frontmatter or image change is part of this task. Review reports and final inventory supplement this comparison; existing historical guards remain authoritative for their frozen epochs and are not relaxed.

## Tool restoration before landing

The owner explicitly authorized restoring missing tools and running the normal pre-commit hook. `pnpm install --frozen-lockfile` restored ESLint 9.39.2 and @unocss/eslint-plugin 66.6.0 from the existing lockfile; package.json and pnpm-lock.yaml remained unchanged. Full lint, 61/61 unit tests and VitePress build passed again after restoration. The hook uses an existing cached lint-staged 16.4.0 executable made available temporarily in node_modules/.bin; no hook bypass or package declaration change is involved. Structure/materializer and preservation limitations above remain.
