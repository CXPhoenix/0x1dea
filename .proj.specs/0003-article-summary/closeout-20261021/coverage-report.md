# T-0003 current acceptance coverage

Current execution: 2026-10-21T15:34:43.595335+00:00. This additive closeout supersedes the missing-evidence disposition only; earlier coverage, failures, approvals and immutable oracles remain historical. Source: staging f503f00a4891a519eb12b54e6bfc8f0db267c55f, installed Node 24.13.0/pnpm 10.28.0. No new behavior or test interface is introduced.

| Criteria | Observed coverage | Evidence |
|---|---|---|
| S1/S2/S3 | Existing 12 component tests and compiled fixture; equal normalized canonical takeaways, fallback, rich Markdown, native containers, following sentinel; prior compiler comparison retained. | stage-unit.log.txt; fixture.md; true-staging-__closeout_acceptance.html.txt; summary-checks.json |
| S4 | Authored summaries are in static SSR; initial and SPA browser have no hydration/unresolved warnings. | ssr-matrix.json; local-browser-actions.json; keyboard-spa-actions.json |
| S5/S6 | 1280/360/390 light/dark: desktop cards share one row, mobile has three rows; zero page overflow; minimum summary text contrast 10.59; native Tab focus, selection excludes decorative prompt, canonical summaries add no controls. | browser-metrics.json; summary-checks.json; summary-keyboard-selection.json; focus-summary.png |
| S7 | Actual Chromium A4 portrait/scale 1, browser headers/footers off/backgrounds on. Print contrast 18.88; required note/cards/terminal and richer content readable on rendered pages 1–3, white backgrounds, no clipping. Full 9-page fixture PDF retained; figures/tables later pages are outside summary print acceptance. | print-settings.json; print-metrics.json; summary-A4.pdf; summary-A4.txt; print-page-1.png; print-page-2.png; print-page-3.png |
| S8 | All 112 staging blog entries and 13 protected history hashes preserved; no parser or product code change. | source-pins.json; preservation.json |

Evidence basenames resolve under `.proj.specs/_reports/ui-closeout-20261021/evidence/` unless marked Existing. Check and independent-review records are scoped to this closeout; original red/green counts are not recast as fresh execution. No line-coverage percentage is claimed. Actual public deployments and local compiled fixtures are labeled separately.

Landing receipt: [landing.json](landing.json). Current acceptance: [approval.md](approval.md). Independent reports: [review](review/). Shared readme: [evidence readme](../../_reports/ui-closeout-20261021/README.md).

Final unchanged Python runner: 273 cases across groups [95, 154, 10, 14], exit 0 at 2026-10-21T16:18:15.382119+00:00. The tested local candidate and additive archive boundary are explicit in shared test-context.md and python-receipt.json. Final native passed. Delivery-context PC01 has not yet run and is scheduled after commit; its subsequent execution record is separate from this pre-commit archive.
