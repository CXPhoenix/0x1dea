# Local validation and coverage

This evidence covers the dedicated main-based electricity candidate, not staging or production deployment. Existing approved AP/component/caption test seams are reused; no new seam or broad test rewrite was introduced. The first imported Vitest run had 53 passes and one current-editorial hash mismatch. The production expectation now pins the authorized release bytes and removes only the two draft frontmatter fields from the current-article expectation. Frozen historical fixtures and oracle are byte-identical.

| Surface/seam | Observed result | Coverage and limit |
|---|---|---|
| Full Vitest | 54/54 passed | Existing main tests plus summary, EncoreTicket and caption renderer/real article tests |
| Publication CLI tests | 16/16 passed | Existing synthetic disposable Git provenance/prepare/verify/output rejection suite |
| Historical Python harness | 53 executed; 52 passed, 1 error | Immutable lint-successor source hash rejects new caption config; retained as blocker |
| pnpm lint | exit 0 | Existing first-party scope and zero-warning threshold |
| verify-project.py | passed | Offline structure only |
| writing materializer --check | passed | No writing-skill changes |
| verify-harness-adoption.py | failed | config.mts source hash mismatch; no changed historical manifests or bypass |
| OS-enforced sentinel | passed | Inside read succeeds; outside read/write and local network connection denied; outside sentinel unchanged |
| Candidate VitePress build | exit 0 | Production environment; same sandbox allows only candidate and existing reviewed system/toolchain reads, disposable writes, no network |
| Browser | passed on local built output | 1280px light/dark and 390px light/dark; no horizontal overflow; three figures, six references, eight images all loaded; no preview notice; keyboard Enter navigates to figure; recommendation navigates to the existing safety article |
| Unselected content exclusion | exact source inventory plus supplementary full-output scan | Five excluded article routes, source paragraphs and exclusive asset bytes/hashes; final committed candidate must be rechecked |
| Independent reviews | Standards 0, Spec implementation 0, qualifying security candidates 0 | Release blocker remains; source review cannot replace final Git/build/deployment checks |

The initial sandbox build correctly rejected a Vite temp write through a toolchain-directory symlink. The candidate now owns its node_modules directory and local .vite-temp while package entries link to the installed read-only toolchain. No host security setting or dependency version changed. Python sentinel startup emitted xcrun cache-write denials but completed all four assertions and exit 0.

The owner authorized only this article's PR. It remains draft while the historical verification blocker is unresolved; no main merge or deployment was performed.

`git diff --cached --check` still reports three empty blockquote lines with inherited trailing spaces in the selected article (lines 171, 173, 177). They are byte-identical to the approved staging body and intentionally retained rather than silently reformatted. Evidence-log trailing blank lines were removed.
