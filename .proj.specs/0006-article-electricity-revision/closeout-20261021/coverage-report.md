# T-0006 current acceptance coverage

Current execution: 2026-10-21T15:34:43.595335+00:00. This additive closeout supersedes the missing-evidence disposition only; earlier coverage, failures, approvals and immutable oracles remain historical. Source: staging f503f00a4891a519eb12b54e6bfc8f0db267c55f, installed Node 24.13.0/pnpm 10.28.0. No new behavior or test interface is introduced.

| Criteria | Observed coverage | Evidence |
|---|---|---|
| A1/A2/A3 | Existing exact article successor/negative controls and immutable historical tests retained; current native guard rejects tampering and full regression is rerun separately. | Existing coverage-report.md; preservation.json; native.json; python.log.txt |
| A4 | Current 87 unit tests/lint/six VitePress builds, structure/materializer/native/Python and independent closeout review. Old failures remain historical. | stage-unit.log.txt; stage-lint.log.txt; build-matrix.json; checks.json; review/ |
| A5 | Exact original staging commit f93237b is an ancestor; GitHub Cloudflare check success identifies immutable deployment 1cde5ce9. Actual browser and served SSR at that deployment load all eight images, including both new memes. Later authorized article revisions are distinct successors. | T-0006-deployment-check.json; T-0006-exact-preview-dom.json; T-0006-exact-preview.html.txt; landing.json |

Evidence basenames resolve under `.proj.specs/_reports/ui-closeout-20261021/evidence/` unless marked Existing. Check and independent-review records are scoped to this closeout; original red/green counts are not recast as fresh execution. No line-coverage percentage is claimed. Actual public deployments and local compiled fixtures are labeled separately.

Landing receipt: [landing.json](landing.json). Current acceptance: [approval.md](approval.md). Independent reports: [review](review/). Shared readme: [evidence readme](../../_reports/ui-closeout-20261021/README.md).

Final unchanged Python runner: 273 cases across groups [95, 154, 10, 14], exit 0 at 2026-10-21T16:18:15.382119+00:00. The tested local candidate and additive archive boundary are explicit in shared test-context.md and python-receipt.json. Final native passed. Delivery-context PC01 has not yet run and is scheduled after commit; its subsequent execution record is separate from this pre-commit archive.
