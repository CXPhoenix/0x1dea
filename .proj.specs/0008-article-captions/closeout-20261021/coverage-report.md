# T-0008 current acceptance coverage

Current execution: 2026-10-21T15:34:43.595335+00:00. This additive closeout supersedes the missing-evidence disposition only; earlier coverage, failures, approvals and immutable oracles remain historical. Source: staging f503f00a4891a519eb12b54e6bfc8f0db267c55f, installed Node 24.13.0/pnpm 10.28.0. No new behavior or test interface is introduced.

| Criteria | Observed coverage | Evidence |
|---|---|---|
| C1–C6/C9 | Existing 25 renderer/guide cases, exact fixture provenance, three opt-in knowledge figures/six refs and original eight image alt/src pairs preserved. New temporary fixture has two figures/two tables plus an ordinary unnumbered table. | stage-unit.log.txt; fixture.md; source-pins.json; Existing coverage-report.md |
| C7 | Static built HTML and actual served page: article 3 figures/6 refs, table captions first child. 1280/390 (plus 360) light/dark: 17.5px captions, min contrast 10.94, no clipping/overflow; native Tab/Enter figure/table targets; SPA probe survives with no duplicate IDs. Screenshots now portable. | ssr-matrix.json; browser-metrics.json; keyboard-spa-actions.json; focus-fig-first-proof.png; focus-tbl-first-table.png |
| C8 | Current product checks and historical-aware Python runner/native guard executed with unchanged frozen tests. Temporary fixture and dependency links removed before native verification; no article rewrite or install. Original 85/86 failure is retained as its own historical result. | checks.json; python.log.txt; preservation.json; T-0008-deployment-check.json |

Evidence basenames resolve under `.proj.specs/_reports/ui-closeout-20261021/evidence/` unless marked Existing. Check and independent-review records are scoped to this closeout; original red/green counts are not recast as fresh execution. No line-coverage percentage is claimed. Actual public deployments and local compiled fixtures are labeled separately.

Landing receipt: [landing.json](landing.json). Current acceptance: [approval.md](approval.md). Independent reports: [review](review/). Shared readme: [evidence readme](../../_reports/ui-closeout-20261021/README.md).

Final unchanged Python runner: 273 cases across groups [95, 154, 10, 14], exit 0 at 2026-10-21T16:18:15.382119+00:00. The tested local candidate and additive archive boundary are explicit in shared test-context.md and python-receipt.json. Final native passed. Delivery-context PC01 has not yet run and is scheduled after commit; its subsequent execution record is separate from this pre-commit archive.
