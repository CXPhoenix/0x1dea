# Ticket acceptance and actual landing audit, 2026-10-11

This is a current readback, not a rewrite of historical outcomes. Sources are the pinned main eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a, staging c6efa7ded4731cbe251bdbc6fea5615e7e7b11b7 and original Git objects. Four review tickets remain review; evidence cleanup does not waive acceptance. Existing T-0005 is imported to main only to resolve T3/T4 dependency and its already-done landing receipt. T6/T7 are not reclassified.

| Ticket / criteria | Acceptance evidence | Actual landing | Current disposition |
|---|---|---|---|
| T-0001 HA01-10 | 0001 coverage-report, code/security reports; maintenance/harness-adoption/evidence contains full approved ten-seam results; 307 manifest entries and 111 receipt/log hash bindings rechecked | Adoption1ed1348 +privacy64799e6 are staging ancestors; original direct staging push authority APPROVALS.md:20-30 | done; new landing.json/landing-approval.md. No original push stdout/time recovered |
| T-0002 AP01-09 +cleanup | AP CLI16, native catalogs and scoped isolated candidate pass; 39 JSON/log bindings verified. cleanup lint22files0warning, harness53/Vitest14/CLI16/build and independent review pass | PR14 merge8987806 into staging; PR15e457 into main, both ancestors. Original draft PR authority does not imply merge authority | review: cleanup interactive search/sort/category/filter/view browser input timed out; Vue/build cannot replace it |
| T-0003 S1-8 | Source/tests/reviews present; components.json12/12 after hashes match PR16. Old prototype source-freeze is only1/8 current and not final oracle | PR16 merge69ff85f5 into staging is ancestor | review: required raw SSR/build matrix, 1280/360 light/dark metrics, keyboard/a11y/copy/hydration/navigation and S7printPDF/text/background evidence not in portable packet |
| T-0004 N1-7 | N1/N2/N5/N6 source/tests present; N7 retrospective explicit. Components match reviewed PR16 source | PR16 merge69ff85f5 into staging is ancestor | review: missing raw env matrix/browser evidence; N4 actual Production served home/article notice absence remains unverified |
| T-0008 C1-9 | C1-6/C9 source/tests/guide and reviews exist; browser-matrix.json8 layouts has17.5pxfont,10.94/12.81contrast,nooverflow/clipping,targetsexist. Plugin/guide/article match6e4eb80; reconstructed fixture provenance/inverse exact |6e4eb804bcbda8504935be49fd6537d6327d5303 is staging ancestor; current owner audit authority does not invent past push authority | review: C7 keyboardfocus/Enter hash, SPA probe/no duplicate and builtSSR raw evidence missing; screenshot basenames have no resolvable packet path |
| T-0010 M1-5 +L1-4 | delivery logs54Vitest/66harness/16publication;8commands exit0;four browser modes+keyboard;mobile DOM supplement closes initialP1; final code/security zero residual | PR18eeda main, then PR19c6 staging integration | done; primary main vs configured staging landing explicitly distinguished |
| T-0011 S1-5 | Existing coverage/review/evidence full87Vitest/95harness/16publication, actual merge scope and owner done message | PR19c6 staging, tree equals reviewed01b5d69; all111blog entries unchanged | retain done; local closeout records included unchanged, plus current delivery note |

## Criterion and artifact locations

T1: .proj.specs/0001-harness-adoption/spec.en.md:71-86 mandatory table; coverage-report.md; review/code-T-0001.md:5-9; review/security-T-0001.md:5-18; maintenance/harness-adoption/evidence/final-manifest.json and receipt JSON/logs. Historical113 rows remain28fresh/85inherited not-run; no full-scenario or extra ESLint gate is invented.

T2: .proj.specs/0002-article-publication/spec.en.md; evidence/cli-tests.txt; codex-discovery-escalated.json; claude-discovery.json; isolation-sentinel-followup.json; isolated-output-verification.json; lint-cleanup.md:78-84; review/code-T-0002-lint-cleanup.md:34-36. T11 browser.json covers category card/Enter/light-dark/mobile only, not the missing interactions.

T3/T4: .proj.specs/0003-article-summary/coverage-report.md:13 and 0004-shared-preview-notice/coverage-report.md:13 reference repository evidence/ and output/playwright/, both missing. maintenance/component-delivery only contains scope/TDD/source-freeze, not raw execution/browser/print artifacts. TDD.md:6-8 log references likewise do not resolve. T4 spec.en.md:33 and test-plan.md:10 require actual Production resolved=false and served absence independently from a local environment simulation.

T8: .proj.specs/0008-article-captions/browser-evidence.md:10-13 has narrative keyboard/SPA/SSR; :17 external screenshot basenames. evidence/browser-matrix.json contains layout data, not these missing interactions. tests/fixtures/article-caption-provenance.json:3-9 labels later reconstruction honestly.

T10: delivery/harness.txt:69-71, unit.txt:15-16, publication.txt:19-21; listing-followup/evidence/browser.json and mobile-viewport-supplement.json:19-35,53-67; review/code-final.md:13-15. T11 later changes to wrapper/tracker are tested under T11, not backdated as T10 runs.

## Recovery of retained-review tickets

Recover original raw artifacts with identifiable source/version and hashes, or explicitly rerun now against pinned current source. Do not relabel narrative as raw evidence or copy a different ticket's narrower browser pass. T2 needs actual search/sort/filter/view interaction. T3 needs SSR/env/browser/print evidence. T4 needs env/consumer evidence and actual Production acceptance. T8 needs keyboard/hash/SPA/SSR records. Until then leave review, even though source landed.

## Evidence limits

All current ancestor checks bind to observed staging, not proof of a historical push time. GitHub CI is not claimed: inspected old PR status-check arrays were empty. No production deployment, live Cloudflare setting, external index or new workflow change is verified. Historical browser/build/OS isolation counts are scoped to their original executions. New HTML reports receive static offline/CSP/structure inspection only; prior browser file URL policy blocked rendered report inspection and no workaround is used.

## Portable source identity archive

The current audit read the original staging management evidence named above. Exact copies of components.json, component-delivery scope/TDD/prototype freeze and later caption fixture provenance are saved under ticket-closeout/source-archive/ with their original repo-relative paths. These copies preserve source identity evidence on main without adding staging reconciliation runtime files or product fixtures. References in old imported specs remain historical; missing raw runtime artifacts are explicitly not recovered by this archive.
