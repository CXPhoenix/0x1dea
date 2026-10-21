# UI ticket closeout — 2026-10-21

Current acceptance for T-0003, T-0004, T-0006, T-0007 and T-0008. Their implementations already landed on staging. This packet adds missing portable evidence; it never changes frozen specs, historical approvals, test assertions, M0, old receipts, product code or article/candidate content.

## Source and surfaces

- Source pins: evidence/source-pins.json. Local six-environment VitePress builds use staging f503f00a4891a519eb12b54e6bfc8f0db267c55f, installed Node 24.13.0/pnpm 10.28.0, no installation and no copied local env files. Only a named temporary fixture and dependency symlinks were added to disposable QA clones; both were removed before native verification.
- Actual public Production: Cloudflare 31cc7a4d, main 0e69006, explicit false, successful; home/article omit notice in served SSR and hydrated DOM. Actual preview: 67b8c227, staging 87ff977, explicit true, both show it. Deployment-specific build settings were read from the authenticated dashboard through cua_repl, selecting only public fields into cloudflare-observation.json. This is a contemporaneous observation receipt, not a downloaded raw dashboard export. No account/settings/credential changes occurred.
- Original exact deployments: GitHub check responses bind f93237b/1cde5ce9, f3eee3d/96271a1a, 6e4eb80/05b1fabd; each independent preview was fetched in a real browser, saved as SSR and DOM, with eight images loaded. Current branch aliases and historical immutable deployments are distinguished. Metadata-only latest heads are skipped by Cloudflare and not claimed deployed.
- Local browser: Chromium 150 agent-browser 0.29.1, 1280/360/390 light/dark, actual built pages, DOM/layout/contrast/keyboard/hash/SPA. Print uses the same Chromium page through native CDP because the CLI PDF command exposes no paper settings. A4/scale 1/backgrounds on/browser headers-footers off; summary pages 1–3 visually inspected. Full fixture PDF is retained; later decorative figure/table print layout is outside S7 summary scope.

## Reproduction and limits

The existing approved renderer/build/browser seams were reused. Evidence scripts preserve actual temporary paths and command invocations as execution records, not a new installed test runner. SSR artifacts use .html.txt to keep raw scripts inert when opened. Screenshots alone do not prove keyboard/SSR; corresponding JSON/action records do.

The first two QA-fixture attempts used an invalid caption form and absent favicon; their failed build logs remain separate. They changed no product source. One semantic CLI locator and one URL wait pattern failed; the native keyboard/SPA run then succeeded using observed hrefs and a pathname condition. Those attempts are preserved and never counted as passing cases. Canonical summary equality normalizes layout-only whitespace; all authored text/link order is compared. Native text Range selection excludes decorative SVG-mask prompts; this does not claim an OS clipboard read.

Original TDD, the earlier 85/86 article-preservation observation, and original missing-artifact audits remain version-qualified. Current results do not rewrite their dates or turn a narrative into recovered raw history. No percentage line coverage, original push timestamp, P13 readiness, automatic publication readiness, candidate article publication or external index update is claimed.

## Evidence navigation

- Each epic's closeout-20261021/coverage-report.md maps every criterion to this packet and retained original proof.
- evidence/checks.json and python.log.txt identify checks actually executed; native.json records the reviewed current CLI state.
- evidence/preservation.json binds all 112 blog entries, 50 candidate paths and 13 protected historical hashes.
- review/ contains independent captured-scope code/security results; per-epic copies retain each ticket's responsibility.
- ../ui-closeout-20261021.html is the offline Traditional Chinese evidence report.

## Additional current validation context

The full runner uses an explicitly unpublished local candidate after a real pre-closeout T6/T7 add/add refusal; see test-context.md and evidence/candidate-test-context.json. The QA main parent and all historical tests are preserved. This is not remote readiness. Omitted dependency env and default-sandbox loopback refusals remain separate attempt records. Final regression/native results are recorded after execution, not inferred from the single-case pass.

Final unchanged Python runner: 273 cases across groups [95, 154, 10, 14], exit 0 at 2026-10-21T16:18:15.382119+00:00. The tested local candidate and additive archive boundary are explicit in shared test-context.md and python-receipt.json. Final native passed. Delivery-context PC01 has not yet run and is scheduled after commit; its subsequent execution record is separate from this pre-commit archive.
