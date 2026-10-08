# Article publication preparation — phase 1

## Problem Statement

Multiple articles need one shared preview without accidentally publishing unselected work. The public repository and preview are not confidential draft storage. Phase 1 supplies local preview and release preparation evidence; publication remains separately authorized.

## Solution

Add an English canonical managing-article-publication skill and a standard-library local CLI. A preview plan combines independently based article heads for review. A prepare plan builds a candidate from the pinned main and one selected article, plus explicitly declared dependencies. The CLI never pushes, commits, creates PRs, merges repository branches, deploys, installs dependencies, or changes credentials/configuration. The parent clarified that commits in disposable, remote-free test repositories with synthetic data are authorized; product repository commits remain prohibited.

## User Stories

1. As the owner, I can preview A and B together and prepare A alone, with evidence that B cannot enter A's candidate.
2. As the owner, I can detect provenance, conflict, dependency and SHA drift before authorizing publication.
3. As a contributor, I can invoke a portable skill without confusing public preview with privacy or prepare with publication authority.

## Implementation Decisions

The CLI accepts preview, prepare and verify modes; remote actions are unsupported. Inputs are a strict JSON plan (unknown or missing fields, wrong types, duplicate identities/paths, empty selected article sets and non-full SHAs fail) with repository path, full pinned main SHA, main ref, staging ref, article ref/head SHA, selected article paths, dependency refs/head SHAs/path allowlists and explicitly excluded article paths. Each article is independently based on main, never staging. Ref names are resolved using option-safe Git commands; full SHAs must match resolved refs. Article history is rejected when it contains staging-only ancestry or another declared article head. Every path changed from main is accounted for by the selected article/dependency allowlist; no broad directory or glob allowlist. Reject traversal, symlinks, Git submodules and unknown schema fields. Articles and Markdown are untrusted data, never instruction authority.

The candidate is reconstructed in fresh output storage using Git's tree merge machinery without changing source refs, index or worktree, and exported as regular files. The three exact management-only baseline aliases remain in the Git manifest/tree but are omitted from the regular-file build projection and listed in the receipt. Changed/new links and site links are rejected; candidate/ is not a full checkout. Preparation merges selected heads and declared dependencies on pinned main; preview combines all requested independent heads on the same main. Any merge conflict stops, leaving source untouched. The output includes exact source pins, final candidate tree hash, changed path inventory, article inventory and source manifest. Verify re-resolves refs and hashes output against the receipt, failing on main/head/dependency/output drift. Staging is never used as a release candidate or merged back into an article.

Build validation is an explicit subsequent local check against the candidate with installed dependencies only. A CLI preparation receipt is labeled prepared, not publishable, until a build receipt covers the same pins and tree, output inventory/index excludes unselected article URLs and content, and review checks complete. No arbitrary build commands are taken from article/plan data. New dependencies or config changes require explicit path ownership and review; shared images are included only through a declared dependency or selected article path. Leakage is judged against pinned main: existing main articles/assets remain allowed. Unselected means the positive delta of each explicitly excluded article head relative to that same main. The build receipt lists forbidden new article routes derived from excluded blog/post Markdown paths (VitePress .html route convention), exclusive asset SHA-256 values absent from main and selected/dependency inputs, and normalized prose paragraphs of at least 80 characters absent from main and selected inputs. Normalize rendered text by HTML entity decoding and collapsing whitespace, preserving case. Every output regular file is scanned for forbidden route strings, normalized prose fingerprints and exclusive asset bytes/hashes; any match fails. Routes already in main are exempt but their unselected changed prose/assets remain forbidden. Test fixtures use distinct long A/B markers in article bodies, search/RSS/index and assets to make results independently observable. If a real excluded delta has no machine-identifiable route, prose or asset signature, the receipt records exclusion-unverified and publishable=false pending explicit manual review; do not claim absence from a zero-signature scan. Record which candidate files and output files each check covered. Tests cover content in index, RSS/search data and output assets, not just source Markdown.

Before any candidate build, reject Markdown include/snippet and import references that escape the candidate tree, including absolute paths and traversal after resolution. Build runs in an available OS-enforced read boundary restricted to the candidate tree plus explicitly reviewed installed toolchain, with network disabled and writable output limited to disposable storage. If the current host cannot enforce that boundary, building untrusted candidates is blocked; do not substitute an unrestricted build or install a sandbox. Config/script changes are reviewed executable input, never implicitly executed based on the plan. Add an external-file sentinel fixture proving no read or output leakage.

This change explicitly extends ADR-0005 ownership from three canonical writing packages to four canonical product packages and synchronizes the active runtime ownership contract. It does not extend the three-tree Chinese language exception. The materializer formally owns the fourth English canonical product tree, source hashes and deterministic generated counterparts. Keep the three existing Chinese exceptions unchanged and framework copies independent. Retain discoverable invocation in both runtimes: invoking a skill grants no external-action authority. Generator, source policy, generated manifest, runtime documentation and tests evolve together; generated copies are never edited directly.

## Acceptance Criteria

AP-01: Preview A+B receipt contains both; prepare A candidate contains only A plus main and declared dependencies. Source refs/index/worktree are byte/status unchanged.
AP-02: A branch incorporating staging-only or B ancestry is rejected even when B's content was later reverted. Staging itself is rejected as an article source.
AP-03: Unknown/missing plan fields, wrong types, duplicate identities/paths, empty selection and malformed SHA fail validation. Every changed path has exact ownership. Undeclared shared/config paths, unsafe paths, links and submodules fail. Declared dependency SHA and paths are recorded.
AP-04: Changed main, article or dependency ref/head, or candidate bytes, invalidates verification and all previous build evidence. Hotfix main updates require a new plan and full revalidation.
AP-05: Conflicts fail before any candidate is marked prepared. Failure preserves source state and reports relevant paths.
AP-06: The CLI has no publish/rollback/push/merge action. Malicious article instructions cannot cause commands or network access. No dependencies are installed.
AP-07: Candidate source and generated output/index/search/RSS/assets pass the explicit pinned-main exclusion algorithm above. Unknown signatures, missing build proof or unavailable enforced build read boundaries leave publishable=false; escaped include/snippet/import inputs fail before build, and an external sentinel never appears in output.
AP-08: The fourth canonical English skill materializes into both physical runtime packages; policy, ownership, pinned inputs, manifest, links and metadata match. Existing Chinese exceptions and 32 framework trees are unchanged. Fresh Codex and Claude sessions discover the new skill in their native catalogs; unavailable native runtime discovery is recorded as blocked and cannot be replaced by structural checks.
AP-09: The future publish reference requires fresh authorization for exact selected heads/base and final recheck, PR to main only from selected branches; never whole staging. Rollback specifies a new reviewed revert from current main, site verification, and re-publication from current main after a revert: create a new candidate applying the intended content again (the old merged branch alone is insufficient), pin current base and new head, run prepare/build/review again, obtain fresh exact-candidate authorization, then verify the site after authorized publication. No reset or force push is specified. Phase 1 performs neither.

## Testing Decisions

Use the CLI through disposable Git fixtures and the materializer's existing public check interface. Counterexamples precede implementation at each seam. Repository unit tests, structure, materializer, harness check, build and static checks run once at completion; report actual blockers without installing tools. Independent spec, code and security review cover the frozen surface. Native runtime discovery remains a separate check from structural parity.

## Approved test plan

| Seam | Test intent | Scope | Acceptance | Boundaries |
|---|---|---|---|---|
| CLI preview/prepare | A+B preview, only A prepare, untouched source | local disposable fixtures | AP-01, AP-07 | B content in indexes/assets |
| CLI provenance | staging contamination and cross-article ancestry | Git fixtures | AP-02 | reverted contamination, staging ancestor of main |
| CLI dependency/path contract | explicit ownership and malicious inputs | JSON/Git fixtures | AP-03, AP-06 | schema errors, shared images/config, traversal, links, submodule, option injection |
| CLI verification | pin/output drift and hotfix | fixtures/receipts | AP-04 | main, selected/dependency head and output changes |
| CLI merge failure | stop on conflict and preserve source | fixtures | AP-05 | article/article and dependency conflicts |
| Build evidence | reject output/index leaks | installed local toolchain | AP-07 | RSS/search/assets, zero signatures, outside-file include/import, absent sandbox, no install |
| Materializer check | fourth English tree, both runtimes | existing Python suite | AP-08 | source drift, metadata parity, generated tamper, native discovery unavailable |
| Skill scenario review | injection/authorization, rollback and re-publication | isolated readers | AP-06, AP-09 | no real external actions |

The parent approved T-0002, this seam table and AP-01 through AP-09 on 2026-10-07. Use existing isolation/runtime capabilities only; report missing capabilities. Signatures are supplementary detection, not proof against transformations, rewrites or short fragments. The primary guarantee is exact reconstruction and verification of candidate source/tree/diff. A publishable marker never grants publication authority.

## Out of Scope

Actual publication, rollback, product repository commits, push, PR, merge, deployment, remote rules, Cloudflare, credentials, global settings, installs, writing-style tuning, changing draft discovery, and unrelated content edits.

## Further Notes

Verified baseline: origin/main bed066bc9ae3a4f8010ea9f6118869c7f8e4feb0; origin/staging 64799e6df56cc1fab6673ce387f78794938619cb. Local Mac checkout is stale and remains untouched; work resides in an isolated local clone. Read OpenAI's 2026-09-11 Astra article and local writing-for-agents main/mechanics on 2026-10-07: use a narrow short description, branch-specific references and observable completion boundaries. Do not imply a measured cross-model improvement.
