# T-0004 current acceptance coverage

Current execution: 2026-10-21T15:34:43.595335+00:00. This additive closeout supersedes the missing-evidence disposition only; earlier coverage, failures, approvals and immutable oracles remain historical. Source: staging f503f00a4891a519eb12b54e6bfc8f0db267c55f, installed Node 24.13.0/pnpm 10.28.0. No new behavior or test interface is introduced.

| Criteria | Observed coverage | Evidence |
|---|---|---|
| N1/N2 | Existing 22 flag/props cases plus article integration; literal hostile title/text rendered as text; blank instance suppressed. Exact supplied flag semantics retained. | stage-unit.log.txt; browser-metrics.json; fixture.md |
| N3 | Six clean build environments × actual home/article SSR and hydrated DOM: true/staging, absent/staging, true/main show; false/main, absent/main, absent/absent hide. Diagnostic true/main remains valid. | build-matrix.json; ssr-matrix.json; browser-metrics.json |
| N4 | Read-only actual Production deployment 31cc7a4d binds main 0e69006 and explicit false; success. Public home/article actual response and DOM omit preview notice. Preview 67b8c227 binds staging 87ff977, explicit true; both consumers show notices. Latest Git metadata-only heads are skipped, not claimed deployed. | cloudflare-observation.json; production-home-served-ssr.html.txt; production-article-served-ssr.html.txt; production-home-dom.json; production-article-dom.json; preview-home-dom.json; preview-article-dom.json |
| N5/N6 | 360px light/dark no overflow; ≥4.5 text contrast; native links preserved; no executable prop markup or hydration mismatch. Public example tracked and local env paths ignored. Clean QA clones copied no local env files. | browser-metrics.json; local-browser-actions.json; env-boundary.json |
| N7 | Original homepage f981af27 and PR16 consumer landing remain historical; this is a current rerun/acceptance, not backdated proof. | Existing retrospective.md and approval.md; landing.json; approval.md |

Evidence basenames resolve under `.proj.specs/_reports/ui-closeout-20261021/evidence/` unless marked Existing. Check and independent-review records are scoped to this closeout; original red/green counts are not recast as fresh execution. No line-coverage percentage is claimed. Actual public deployments and local compiled fixtures are labeled separately.

Landing receipt: [landing.json](landing.json). Current acceptance: [approval.md](approval.md). Independent reports: [review](review/). Shared readme: [evidence readme](../../_reports/ui-closeout-20261021/README.md).

Final unchanged Python runner: 273 cases across groups [95, 154, 10, 14], exit 0 at 2026-10-21T16:18:15.382119+00:00. The tested local candidate and additive archive boundary are explicit in shared test-context.md and python-receipt.json. Final native passed. Delivery-context PC01 has not yet run and is scheduled after commit; its subsequent execution record is separate from this pre-commit archive.
