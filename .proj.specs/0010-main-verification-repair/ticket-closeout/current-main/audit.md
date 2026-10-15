# Acceptance and actual landing audit after PR #26

Pinned original #20: e6e7a04da7a1e4d9819fa6f8aaadb72a0611e20c; current main: 87740186f2a1b57f8c1df89f36647cbe3663f428; staging: 035783590895a426ee395045829ebc9d50e2b9cf. `confirmed` is limited to the cited acceptance scope; `unverifiable` means evidence is insufficient, not a confirmed product defect. Original reports/raw logs remain historical. Current interpretation supersedes the October 11 audit only where explicitly stated below.

## Disposition

| Ticket | Status in this PR | Reason / actual landing |
|---|---|---|
| T-0001 | done | HA evidence and actual authorized staging ancestry; original adoption 1ed1348e3e7cc00bed2e073fce07fa1325335d3d, privacy successor 64799e6df56cc1fab6673ce387f78794938619cb |
| T-0002 | done (corrected) | AP-01–09 and all six cleanup rows evidenced; PR14 staging merge 8987806a3c34653a236ca0c683a46bcc9632c27d, also present on main through PR15. Extra browser timeout was never a required gate |
| T-0003 | review | Actual source landed via PR16 69ff85f5fe1baddb54102070a436dff9ac1c5b73; required built/browser/print raw absent |
| T-0004 | review | PR16 staging source landed; env/hydration/production evidence incomplete. PreviewNotice is absent from current main; that absence is not N4 Production evidence |
| T-0008 | review | Caption source 6e4eb804bcbda8504935be49fd6537d6327d5303 is a staging ancestor, shared renderer already on main; complete C7 keyboard/SPA/built-SSR raw absent |
| T-0010 | done | Original M1–M5/L1–L4 landed via PR18 eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a and PR19 c6efa7ded4731cbe251bdbc6fea5615e7e7b11b7; new guard work is T12 |
| T-0011 | retain done | Owner reported done and PR19 merged; actual tree equals tested 01b5d69bc1a006ef04d8c475b4e7df38712c9ca0. Missing original non-force invocation stdout remains a precision limit |
| T-0005 | retain done, dependency import | Existing reconciliation receipt required by imported T3/T4 records; no new status transition |
| T-0012 | review | Current metadata/current-verifier integration is not yet landed; no backdating into T10 |

## T-0002: corrected gate interpretation

Evidence root `.proj.specs/0002-article-publication/`; source CLI `scripts/article-publication.py`, original tests `tests/article_publication/test_cli.py`.

| AC | Result | Evidence / limit |
|---|---|---|
| AP-01 | confirmed | evidence/cli-tests-followup.txt:12, demo-result.json: A+B preview, independent A-only candidate tree, source preservation |
| AP-02 | confirmed | Same raw and test_cli.py:85,212: reverted ancestry/staging-only history |
| AP-03 | confirmed | test_cli.py:93,118,223,253: strict schema/dependency ownership/symlink/exclusive assets |
| AP-04 | confirmed | test_cli.py:126,204: main/article/dependency/output drift and receipt tampering |
| AP-05 | confirmed | test_cli.py:106: conflicts rejected, refs retained |
| AP-06 | confirmed | test_cli.py:170,240: malicious article/no remote action; separately authorized installation was not a CLI action |
| AP-07 | confirmed | isolation-sentinel-followup.json, sentinel-output-followup.json, isolated-build-followup.txt, isolated-output-verification.json: scoped synthetic macOS build/sentinels; publishable:false |
| AP-08 | confirmed | codex-discovery-escalated.json, claude-discovery.json, materializer/harness raw; fourth product package only |
| AP-09 | confirmed | managing-article-publication/references/future-actions.md:7,22,31: future action rules, not actual publication/rollback |

The six lint-cleanup.md:33–40 gates are first-party lint zero warnings; exact compatible dependency versions; immutable preservation boundaries; article/assets/CSS source/tree plus built route/content equivalence; existing product regressions; independent review and correct draft PR. The inventories lint-cleanup-validation.json, lint-cleanup-clean-validation.json and prior follow-up records bind the raw executions. The independent follow-up checked 27 referenced log hashes. Browser timeout at lint-cleanup.md:78–84,97 is retained as an extra uncompleted check, not inserted into these approved gates.

Implementation 8890d5250e22ec4ee0e0493c1e72bab89d16489b → cleanup 724ddad73f8411a33c77c68d75f95b41d3af2988 → reviewed head c503a6852affcafce927d8248c35e5fba9c0d1b3 → owner-performed PR14 merge 8987806a3c34653a236ca0c683a46bcc9632c27d. All are actual staging ancestors. Three publication package trees, CLI/schema are byte-identical in original #20/current main/staging. Original authority: lint-cleanup.md:3–6 and public-evidence.md:54–57; conditional closeout authority: ../approval.md plus latest owner request. Exact current receipt/approval are local to this folder. Prior prose saying review remains as historical checkpoint text, followed by the dated/current ticket closeout.

## T-0003: each original S criterion

Root `.proj.specs/0003-article-summary/`; original tests `tests/articleSummary.vitest.ts`.

| AC | Result | Evidence / gap |
|---|---|---|
| S1 | unverifiable overall | :14,28,48 unit confirms content/fallback/static title; missing built browser decoration/wrap/copy/accessible-text raw |
| S2 | unverifiable overall | :14,75 slot/pinned renderer covered; test-plan.md:6 three compiled pages missing |
| S3 | unverifiable overall | :68,75 parser covered; dual-instance/compiler comparison/nested computed-style raw missing |
| S4 | unverifiable | :56 renderToString is not built HTML plus initial/client navigation |
| S5 | unverifiable | 360/1280 long URL/code/stack/overflow raw missing |
| S6 | unverifiable | light/dark contrast/focus/accessibility/copy raw missing |
| S7 | unverifiable | specified A4/PDF/text/background/contrast/clipping evidence missing |
| S8 | confirmed for source scope | native slot, no new parser; accepted component/consumer/docs integration. Main selected source came via 604f8733ca47d67fc277ec127a9da743cefbc22e |

coverage-report.md:6–9,13 references repository evidence/ and output/playwright/ absent in all three pinned sources. Later 12-test/T15 unit raw cannot replace real surface acceptance. The original ArticleSummary source-freeze hash f6ce99… differs from actual landed 7a51dd…; actual PR16/#20/main/staging component bytes match. The old freeze is a prototype snapshot, not a present hash oracle. These are evidence gaps, not assertions that the component is broken.

## T-0004: each original N criterion

Root `.proj.specs/0004-shared-preview-notice/`; source is present on staging only.

| AC | Result | Evidence / gap |
|---|---|---|
| N1 | unverifiable overall | historical 32 component+1 consumer tests; missing dual-consumer built artifacts |
| N2 | unverifiable overall | unit/renderToString truth table; hydration matrix raw absent |
| N3 | unverifiable | five clean env combinations × homepage/article generated HTML/DOM absent |
| N4 | unverifiable | spec.en.md:33 actual Production resolved=false plus served absence evidence absent; local/main absence cannot replace it |
| N5 | unverifiable overall | unit literal text/role/name; 360px/contrast/keyboard/SSR-DOM/navigation raw absent |
| N6 | confirmed | staging .env.example:1–6, .gitignore:9–13, config:51–53; no new env parser |
| N7 | confirmed | retrospective.md:3–9 distinguishes later recovery and missing original TDD/deploy evidence |

coverage-report.md raw links do not resolve. PreviewNotice exact landed SHA begins 63f60f… on staging; main/#20 has no such component. No deployment setting is changed or acceptance invented.

## T-0008: each original C criterion

Root `.proj.specs/0008-article-captions/`; tests `tests/articleCaptions.vitest.ts`.

| AC | Result | Evidence / gap |
|---|---|---|
| C1 | confirmed | :18 public caption renderer |
| C2 | confirmed | :30 native/ordinary table/counter reset |
| C3 | confirmed | :43,72 insert/reorder/namespaces |
| C4 | confirmed | :78,98 literal context/safe caption |
| C5 | confirmed | :54,113,123 diagnostics/anchors |
| C6 | confirmed, current reproducible scope | :128,152 oracle/entry/fixtures byte-identical across pins; provenance.json labels later reconstruction |
| C7 | unverifiable overall | browser-matrix.json has eight font/contrast/overflow/target observations; missing keyboard activation/hash, SPA and built SSR raw |
| C8 | confirmed for later version | T15 main-refresh-20261015/unit.txt 26 caption /54 full tests, build/lint raw; not evidence of original 86-test execution |
| C9 | confirmed | :168 guide examples through public renderer |

browser-evidence.md:10–13 is prose for keyboard/SPA/SSR, :17 references external screenshot basenames. T10/T11 narrower listing/notice browser checks do not establish full C7. Preserve review and request original identified artifacts or an explicitly authorized rerun later.

## Limits and recovery

No new browser/production acceptance was run to manufacture old closeout. Git ancestry proves current reachable landing, not original push invocation/time. Original logs retain their exact execution versions; old failed red/attempt logs are never presented as green. GitHub arrays with no checks are not CI passes. The new current native/Python checks are recorded separately. Recover original raw artifacts with source/version/hashes, or approve targeted reruns for T3/T4/T8. This PR does not complete those missing tasks.

## T-0001: original HA acceptance

A = `.proj.specs/0001-harness-adoption/`; E = `maintenance/harness-adoption/evidence/`. Original adopted product scope, not a new adoption run.

| AC | Result | Evidence |
|---|---|---|
| HA01 | confirmed | E/original-sources-dependencies-snapshot-digest-final.log:1,6682: source pins/718 snapshot/737 template entries; original LICENSE and three core Phoenix files independently hash-matched |
| HA02 | confirmed | Same raw; A/coverage-report.md:9,12: original requirements/history retained, no claim history originally used Harness |
| HA03 | confirmed | A/coverage-report.md:12; original openspec/.spectra bytes/type preserved, new tracker independently authoritative |
| HA04 | confirmed | E/materializer-code-review-proof.log:1, review-fixes-final-tracker.log:29:169 generated/52 sources, physical packages and alias negatives; two runtimes each35skills, no links |
| HA05 | confirmed | E/native-catalog-proof.json:1: fresh discovery35 projectskills/errors empty; A/coverage-report.md:24 separately records failed native exec |
| HA06 | confirmed | A/coverage-report.md:13,14,38; E/fresh-writing-mechanical-final.log:23 and three writing-judge JSON support E1–E9, no skeleton exemption |
| HA07 | confirmed | E/review-fixes-bilingual-final.log:2: seven pairs/32requirements/81scenarios/230clauses/9traces; earlier bilingual-full-structure-provenance.log failure remains a failure |
| HA08 | confirmed, original invocation limited | Original spec:39, APPROVALS.md:20–30, A/landing.json:6,10: original direct staging authority and actual adoption/privacy ancestry; original push stdout/time unavailable |
| HA09 | confirmed | 55 docs→blog entries independently equal mode/type/blob; E/build-routes-assets-data-parity.log:2,129, browser-ui-equivalence-proof-final.log:2 and CLI raw |
| HA10 | confirmed | E/rollback-actual-adopt-restore.log:1875, rollback-restored-unit.log:11, rollback-restored-cli.log:2, rollback-restored-build.log:8: actual disposable restoration and reruns |

Independent immutable-object audit recalculated 307 manifest entries and 111 receipt→log bindings without mismatch. Public evidence is a declared projection, not byte identity with the private raw bundle. T1 exact successor is only review→done plus fixed landing_evidence. Original ticket/landing/approval SHA bindings are retained. The spec:73 requires timestamp/command/exit/hash for tests, not original git-push stdout; absence of the latter is retained as a limit, not an invented new AC. Baseline ESLint blocked and 85 inherited not-rerun assertions remain historical, not relabeled green by done.

## T-0010: original repair and listing acceptance

M = `.proj.specs/0010-main-verification-repair/`. T12 current guard work is excluded from these original pass claims.

| AC | Result | Evidence |
|---|---|---|
| M1 | confirmed | M/spec.en.md:23, coverage/raw baseline and negatives: fixed724dd positive control, missing objects fail, no skip |
| M2 | confirmed | M/delivery/validation.md:7,20; five actual eeda source hashes equal reviewed sources |
| M3 | confirmed | Original coverage/CLI negatives for bytes/type/link/missing/history/scope/ignored sources; positive retained |
| M4 | confirmed | M/delivery/scope-audit.json; PR17→18 had1719entries,1716identical, only index/verifier/tracker-test changed; only selected blog index |
| M5 | confirmed | M/delivery/harness.txt:69 (66), publication.txt:19 (16), unit.txt:16 (54), validation.md:7 remaining checks/reviews |
| L1 | confirmed | listing-followup/spec.en.md:13 and browser raw: selected card/date/summary/href, no other candidate |
| L2 | confirmed | listing-followup/evidence/browser.json, mobile-viewport-supplement.json: desktop1440x900/mobile390x844 light/dark, keyboard destination/DOM no overflow;375x812 screenshot dimensions separately limited |
| L3 | confirmed | listing-followup/spec.en.md:15, coverage/negatives: predecessor/bytes/mode/delete/link rejected with valid positive |
| L4 | confirmed | delivery/scope-audit.json, sandbox-probe.txt, listing-followup/review/code-final.md:13: preservation/isolated build/review |

Original actual main landing eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a is ancestor of both target pins; staging integration is c6efa7ded4731cbe251bdbc6fea5615e7e7b11b7. Immutable Git retains records and source hash bindings, but not every delivery JSON has a raw-log SHA. Do not claim the complete T1-style receipt→log chain for T10.

## T-0011: previously closed staging synchronization

S = `.proj.specs/0011-main-to-staging-sync/`.

| AC | Result | Evidence |
|---|---|---|
| S1 | confirmed | S/closeout/delivery-commit.json:2,4,5; parents4005/eeda,1988existing entries only3approvedintegrationchanges,111blogentries retained,123mainadditions exact |
| S2 | confirmed | S/coverage-report.md:7, evidence/python.txt:104: dual-contract positives/negatives,95harness, nofallback |
| S3 | confirmed | evidence/python.json five source hashes equal actual reviewed01b5d69; main helper/originalassertions retained |
| S4 | confirmed | python.txt:104,125 (95+16), unit.txt:18 (87), build-isolation.json:2/browser.json local metadata/keyboard/notice/four viewport-theme combinations |
| S5 | result confirmed, invocation unverifiable | closeout/delivery-pr-open.json:2,5,11 and delivery-remote-refs.txt:1: canonical topic/OPEN→staging/noauto/targetpins; pr-19.json plus ownerdone prove later manualmerge. Original push argv/stdout absent, so absence of force flag is not independently reconstructed |

Topic01b5d69bc1a006ef04d8c475b4e7df38712c9ca0 and actual mergec6efa7ded4731cbe251bdbc6fea5615e7e7b11b7 have identical Git trees and are actual stage ancestors. They need not be main ancestors. S5 does not require saving stdout; missing invocation alone cannot prove force was used. Ownerdone/actualtree/authorizedlanding support retaining done with this precision limit. closeout/final-local-audit.json committed/pushed:false refers to later closeout metadata, not an absence of implementation landing.

## T-0005: retained dependency evidence

R = `.proj.specs/0005-harness-reconciliation/`; no new status transition.

| AC | Result | Evidence |
|---|---|---|
| R1 | confirmed | R/coverage-report.md:6,8 and immutable-source/failure records: original failures/manifests retained, no historical auto-refresh |
| R2 | confirmed | evidence/current-cli.txt:2, materializer.txt:1, structure.txt:1: knownstage/components and liveframework/tracker positive |
| R3 | confirmed | evidence/public-reconciliation.txt:1,12:9 public CLI tests inclunknown/ignored/type/bytes/missing |
| R4 | confirmed | Same pin/history/rollback cases, coverage-report.md:5,8 separates present reconstruction/original authority |
| R5 | confirmed | coverage-report.md:7 and scope/rollbackrecords: no product/deploy change by reconciliation |
| R6 | confirmed | evidence/harness-final.txt:65 (62), publication16/unit59, build/materializer/structure/reviews; landing.json:6/owner authority |

Configured landing69ff85f5fe1baddb54102070a436dff9ac1c5b73 and observed6c315d9 are stage ancestors, not main ancestors. Importing this already-done dependency record does not assert its staging-only source was imported into main. Original landing/approval bytes remain fixed. T6/T7/T9 and future ticket statuses are not changed by this audit.

## Supplementary actor evidence

Current primary GitHub readback pr-14-actor.json records mergedBy.login=CXPhoenix, is_bot=false, exact PR14 staging merge8987806a3c34653a236ca0c683a46bcc9632c27d and timestamp. This supplies the missing actor field behind the T2 owner-performed description; the initial pr-14.json alone did not supply that field. Original agent draft authority and subsequent actual merge remain separate.
