# Harness adoption specification

> Round 2 candidate. G1/G4 were approved at 2026-10-04T07:24:41Z. The owner approved the entire website root move and the two enumerated alias-input exceptions at 2026-10-04T10:30:04Z. Implementation remains gated on this round's zero P0 result; audit translation follows it. No landing or external-write approval is implied.

## Problem Statement

0x1DEA needs the user's local harness workflow while preserving the working site's public behavior, historical Spectra evidence and validated Phoenix writing. Standard Harness management Markdown under docs would be compiled by the current VitePress docs root. The owner selected a complete website root move to blog, leaving docs for management. Two pre-existing canonical compatibility symlinks need explicit input provenance without creating linked runtime packages.

## Solution

Adopt the pinned template into an independent checkout, move the complete site tree at unchanged internal paths, preserve immutable history, and expose one local epic/ticket tracker with reproducible physical runtime packages. Project only approved metadata, local-link depth, management routing and website-directory literals; never change style rules or general product behavior.

## User Stories

1. As the owner, I want one local tracker with truthful dependencies, approvals and evidence.
2. As a contributor, I want skills discovered in a fresh native runtime without a global Phoenix installation.
3. As an auditor, I want preserved source bytes and bilingual traceability that distinguish inheritance, narrow supersession and missing evidence.
4. As a maintainer, I want unchanged site URLs and content plus complete regression and rollback evidence for the management and directory adoption.

## Source, recovery and actual authorization

Product: ee7fecfff72f47abc735d26ac7e9a943de04ebbf (staging/origin-staging baseline). Template: 917e6025da0901a79dda016e1ce5bd89b6e6e19f; original 718-file snapshot digest b7782890459cf3c546395ac5546f22dc074f13d4166688751a9c1e08d4216bf5. Both original repos were rechecked clean at resumption.

The old task-owned checkout's Git metadata and latest draft became macOS dataless; normal and precise escalated reads stalled. It remains untouched. A new independent no-hardlinks clone, implementation-resumed, is pinned to the same baseline. This revised spec reconstructs the readable frozen round-1 input, all recorded round-1 findings and the new approved exceptions; it is not presented as a byte-restored copy of the inaccessible intermediate draft. Frozen review/prompt.md, 113 baseline rows and the matrix were copied from readable original artifacts; the prompt remains verbatim.

Initial G1/G4 receipt: user Sentinel_07d4ae9a14e4819181b0aed2f6c183a9, 2026-10-04T07:24:41Z, reply "同意" to Charter/scope, one adoption ticket/order and full test matrix. Scope receipt: user Sentinel_eb826c38100881919fd654dee5b7d247 replying to assistant Sentinel_bbd52dfc79f0819191e9787b1704d80c, 2026-10-04T10:30:04Z: "cf pages 我改好了 / 其他都同意". The referenced question explicitly named entire docs-to-blog site migration and exactly two compatible canonical link source exceptions. These adjudicate the previous product-byte scope and alias-input conflicts; no vote replaces this owner decision.

## Acceptance Criteria

- **HA-01:** Work SHALL use the pinned independent clone and exact vendored template source/license/provenance; original staging/template SHALL remain unchanged. Unexpected baseline changes SHALL stop affected work. The original product LICENSE SHALL remain byte-identical; root template license/notices and every imported skill's applicable license/upstream snapshot SHALL be preserved without claiming an unverified license grant or new tuning result.
- **HA-02:** All six capabilities, their 32 requirements and 81 scenarios, and four original archives SHALL be indexed with original path/anchor/Git blob/SHA. Original openspec, .spectra.yaml and historical writing artifacts SHALL retain bytes and failures. Missing historical Harness review/TDD/landing SHALL be "not recorded under harness", never manufactured.
- **HA-03:** Executable work SHALL use only .proj.specs and .proj.tickets as configured local authority. Inactive Spectra agent instructions/commands SHALL be retained as non-discoverable text evidence. No Notion write or new release/deployment CI is included; Notion is an index managed by the parent.
- **HA-04:** Exactly phoenix-writing, maintaining-writing-skills and creating-vitepress-post SHALL have one canonical editing source and deterministic complete physical Codex/Claude packages. No symlink at any depth in either runtime tree. Inputs SHALL be tracked regular canonical files plus explicitly enumerated regular alias backing files and approved new management references. Unknown inputs, unknown links, missing/extra files, escapes, nested backing symlinks, changed alias literals/targets and output drift SHALL fail before partial replacement.
- **HA-05:** Codex SHALL have agents/openai.yaml and no Claude-only frontmatter; Claude SHALL have no Codex metadata. Manual/implicit policy SHALL match by skill; product writing stays discoverable/implicit. Each tree SHALL have the initialized template's 32 framework skills plus three product skills, complete required assets, licensing and native role configurations. Fresh native Codex discovery SHALL observe the actual candidate, with no global product installation. Markdown references in SKILL, AGENTS and references SHALL resolve after the additional runtime depth.
- **HA-06:** Shared management retains owner gates, existing-product Charter and separate landing authorization. It SHALL NOT claim a walking-skeleton exemption. Only the three named canonical writing trees and their generated runtime counterparts/references retain validated Taiwan Traditional Chinese v2.2 prose. New AGENTS/CLAUDE/docs/agents/ADR/framework management remains English. Names, scope, version, source and reasons SHALL be explicit. The three core Phoenix v2.2 files retain exact original hashes; old seven-file freeze remains historical evidence while newly allowed routing/path changes get a new freeze and fresh E1–E9 evaluation.
- **HA-07:** New spec.en.md SHALL be authority. Imported six English baselines SHALL retain original English bytes. Their zh-TW audit translations SHALL carry matching Git blob synced_from_sha and a "historical review not recreated" notice. The adoption audit translation follows zero-P0 review. Each trace row SHALL link real source, AC, allocated ticket and actual evidence or unverified status. Stale translations, dangling sources/AC/tickets and falsely passed evidence SHALL fail.
- **HA-08:** Ticket IDs SHALL be global, sequential and permanent, allocated by scanning every ticket epic. Only todo/processing/review/done/pending are stored; blocked is derived. Duplicate IDs, missing/self dependencies, cycles, incomplete pending reason/evidence/date/revisit metadata and done without actual authorized landing evidence SHALL fail. One adoption tracer-bullet ticket covers packages → tracker/history → complete regression/rollback and ends in review, not done. Landing target remains staging only with later authorization; source CF production main is unchanged.
- **HA-09:** The site SHALL move docs/<relative-path> to blog/<relative-path> for all 55 tracked site files with unchanged bytes, including .vitepress/public/shared/post and root pages. Only the explicit six non-site product files below may change directory literals. Original public URLs, internal post paths, articles/frontmatter/createdTime, images, data shape, filter/sort/slice behavior, particle behavior, dependency versions and lockfile SHALL remain unchanged. Actual candidate unit/build/CLI/UI/writing checks SHALL use recorded equivalent conditions; every mandatory unexecuted check remains not-run/blocked, never passed. Added, removed and modified product paths SHALL be guarded, not just old-path hashes.
- **HA-10:** Disposable recovery SHALL restore the original docs tree and old skill entries and rerun baseline unit/CLI/build/hash checks without touching either original repo. No commit, push, PR, merge, deployment, CF edit, installation, permission/credential change or global skill edit is authorized.

## Exact approved product path exception

Every regular baseline file under docs moves to blog with the same suffix and SHA. No site file content edit is permitted by this move; internal loader post/**/*.md, public URLs, nav/sidebar and all five cross-file imports remain unchanged. Six outside files are permitted directory-literal edits only:

1. package.json: exactly the three docs:dev/docs:build/docs:preview command root arguments docs → blog. Versions/dependencies/packageManager/new:post/test scripts remain unchanged.
2. scripts/vpHelper.ts: DEFAULT_DIR docs/post → blog/post and ASSETS_ROOT docs/public/assets → blog/public/assets; corresponding comments may name the new root. No parser, timestamp, filename, cwd, asset-prefix algorithm, error or duplicate behavior change.
3. tests/vpHelper.vitest.ts: directory constants/fixtures and labels reflect blog; all original assertions/11 product tests remain. Add meaningful migration assertions separately, without weakening expectations. Existing lower-case vphelper import and other unrelated defects are classified as baseline; no opportunistic fix.
4. tsconfig.json: the two docs include paths become blog paths, with all compiler settings unchanged.
5. skills/creating-vitepress-post/SKILL.md: site root/default/category/custom/root/assets examples and contract directory literals reflect blog. Repo links, author voice, safety/invocation rules and other semantics remain. It also receives the already-approved runtime projection when generated.
6. README.md: local site paths/examples/image-path prefix reflect blog; append the agreed management entry. Existing unrelated missing screenshot reference is disclosed, not silently repaired.

New site behavior must not be inferred from this exception. Explicit -d docs/... still means that explicit repo-relative directory: the helper does not auto-alias it to blog. Such legacy explicit input is now outside the build source and must be reported accurately by skills; the approved convention becomes blog. Default, -c and asset physical roots intentionally change; asset folder names post_x/root_x and public /assets/x URLs do not. No srcDir/base/cleanUrls/rewrites/outDir override is introduced.

The immutable baseline-files.json enumerates every 370 tracked entry and its type/hash. A candidate-delta manifest SHALL enumerate all 55 path projections, six exact product exceptions, management adapters and retired/generated entries; unknown modification, added product file or missing moved file fails. Immutable history remains at its original path with original bytes. Core style freeze names: skills/phoenix-writing/SKILL.md, references/style-examples.md, references/tw-vocabulary.md, with hashes from the original v2.2 freeze.

## Exact approved alias-input policy

Canonical aliases remain literal symlinks; the generator never follows them to enumerate inputs. Only these two mappings are permitted:

| Canonical alias | Required literal target | Regular backing tree | Physical runtime subpath |
| --- | --- | --- | --- |
| skills/phoenix-writing/reference | ../../maintenance/writing-skills/legacy/phoenix-writing/reference | maintenance/writing-skills/legacy/phoenix-writing/reference | phoenix-writing/reference |
| skills/phoenix-writing/scripts | ../maintaining-writing-skills/legacy-validator | skills/maintaining-writing-skills/legacy-validator | phoenix-writing/scripts |

Alias literal SHA-256 values are respectively 1cb52202e5157351dd1044476eba8d864757f30ddb410fcf1c2c333b0a6b4ae0 and 95f3504e0b766934407433d11c85aa44c2b0356dfef5bc57a498411224c95b45. A tracked, explicit per-file backing allowlist SHALL pin every regular backing file hash; no glob trust, resolve-only containment or arbitrary alias expansion. Check lstat on all path components; reject nested symlinks, unknown files, target change, escape, unknown source or missing file. Stage all outputs, validate, then replace only the three owned package targets; rollback on partial install failure. --check writes only temporary output and compares recomputed expected bytes, including metadata, links, manifest/source policy; it is not a manifest-only check. Two generations with unchanged inputs produce identical hashes; unrelated framework packages remain unchanged.

Canonical aliases preserve legacy callers and original bytes. Runtime packages contain copies of the enumerated regular backing files at alias subpaths, with link targets projected by canonical logical path/approved backing mapping. Repo reference depth is recomputed: canonical SKILL ../../scripts/vpHelper.ts → runtime ../../../scripts/vpHelper.ts, and reference-file repo links similarly gain one depth; sibling product links point to the same runtime's physical sibling package. Anchors/URLs/code blocks/CLI semantics remain. Unknown link syntax is a reported failure, not silently skipped.

## Mandatory test matrix and truthful verdicts

Approved full plan matrix is retained. Commands use Python 3.11+ and existing NVM Node24.13.0/pnpm10.28.0 in candidate cwd; network disabled for package-manager resolution, no installation. Owned dependency copies, lock SHA, cwd, runtime version, command/argv, exit/start/end/log/evidence hashes SHALL be recorded. Each result is pass/existing-failure/new-regression/blocked/not-run. Exit zero alone is not behavioral proof, and baseline historical integrity is not fresh runtime performance.

| Seam | Required execution and boundaries | AC |
| --- | --- | --- |
| source/product/history | original clean/SHA; whole tracked delta; 55 exact moves; six literal-only adapters; added/removed/tamper negatives; six immutable imports, four archives, historical failures | HA-01/02/09 |
| template structure/licensing | pinned original verify-project.py unchanged, 32+3 names each runtime, metadata/manual policy, roles/notice/license/upstream hashes; template22tests on owned pinned copy | HA-01/05/06 |
| materializer | real temp trees: exact2 aliases, nested/backing links/escape/target drift/unknown/missing/extra/foreign metadata; all-depth no links; link projection; check drift; two-generation hashes; partial rollback | HA-04/05 |
| tracker/translation/trace | globally allocated IDs, all five statuses/derived blockers, duplicate/missing/self/cycle/pending negatives, done-without-landing negative, stale blob translation, dangling source/AC/ticket negative | HA-02/03/07/08 |
| native discovery | fresh native Codex candidate context, actual 35-package catalog and required skill locations, no long-session catalog or filesystem-only substitute | HA-05 |
| writing | original mechanical31/30/62 checks on unchanged historical evidence, then nine fresh independent writer contexts and three fresh judges for disjoint groups using frozen case input/rubric and new runtime freeze | HA-05/06/09 |
| CLI | actual subprocess in isolated temporary repo cwd: default/category/custom/root, Unicode/spaces, +08:00, paths, duplicates preserve bytes, c/d conflict, missing title; baseline docs versus candidate blog projections and explicit old-d semantics | HA-09 |
| unit/build/routes/assets | candidate actual 11 unit tests and actual pnpm docs:build; same lock/dependency snapshot; exact eight HTML baseline routes; no management HTML; 32 public source assets SHA/public URL and data parity | HA-09 |
| UI | baseline/candidate equivalent localhost rendered surfaces: home latest, list/card/filter/sort/category, existing empty-result controls behavior, sidebar/nav/images/console/network, keyboard, 390mobile, dark/light/particles within stated coverage | HA-09 |
| recovery/closeout | owned disposable exact baseline restore, unit/CLI/build/hash rerun; original clean/SHA unchanged, code/security findings triaged; ticket review and coverage table with all actual results | HA-10 |

## Frozen writing cases and isolation

Inputs/rubrics are the nine full-regression-v22/cases/E1–E9 files from the baseline, SHA-pinned in writing-case-manifest.json before any new writer. Preserve original text/rubrics and case scores as historical evidence; The pinned nine inputs currently contain no docs-path strings; do not fabricate a moved-path case or add unrelated writer instructions. Original input/rubric bytes are preserved. Any future separately approved path-bearing case records its projection outside historical fixtures. Original case-manifest references and corrections remain accessible.

Writers get only their input, needed candidate physical skills and approved docs-to-blog annotation, not rubrics, old outputs/judgments or root verdicts. One fresh isolated context per case, nine actual responses, including near-miss/no-style/no-scaffold boundary cases. Three independent judges each get three nonoverlapping inputs/rubrics and the new corresponding outputs only, not old scores/output or root verdicts. No self-judgment or reuse. Report real model/runtime/execution IDs/attempts and content hashes. Require every rubric dimension score 2 (10/10 per case), all stated hard rules and zero invocation/safety violations; any difference is retained with its substantive classification and case remains failed until a legitimately recorded retry/new freeze. No interjudge-agreement or cross-model/statistical improvement claim.

## Explicit inheritance and supersession

All 113 historical rows retain original source text/hash. Codex/Claude link-entry/same-file clauses are superseded by physical projection only for vitepress-post-scaffolding-014/015 and phoenix-style-and-maintenance-004/005, including original legacy aliases via the two approved input mappings. Gemini's existing canonical link remains. All rows mentioning docs as a product physical path gain an enumerated docs-to-blog location projection in candidate-traceability.json; URLs and substantive behavior remain unchanged. CLI default/assets physical root and creation conventions are intentionally superseded at that path boundary, with original metadata/errors/naming/time behavior inherited. Management Spectra routing is superseded only at active entrypoints by the single local tracker; historical references remain read-only. No blanket "all remaining unchanged" contradicts these listed owner-approved boundaries.

## Cloudflare snapshot and scope boundary

The owner independently changed CF. Parent native pixel attestation of Library libfile_d33cc20e295c81918b60e1d41867b001: command npx vitepress build blog, output blog/.vitepress/dist, include blog/*, root blank, production main, automatic deploy Enabled; build-system Version3 is not Node version. Node/pnpm/excludes/preview and actual successful deployment remain unverified. Root dependency watch recommendations package.json/pnpm-lock.yaml/tsconfig.json are a handoff, not permission to edit CF. Until production main has blog, a future automatic build may fail; no push/merge/deploy is authorized to remedy that transition.

## Out of Scope

Feature/UI redesign, unrelated bug fixes, article/style rewrites, public URL changes, timestamps/images/data semantics, package/lock/version changes, srcDir-only alternative, release/deploy CI, prompt tuning, fake historical review, Notion/global skill/permission/credential changes, installation, commit/push/PR/merge/deploy/CF edits.

## Review and delivery gates

Frozen prompt is replayed verbatim for round 2 against this captured spec/matrix and new approval receipts. Four independent axes: completeness, verifiability, conflicts, red team. Two-round ceiling; remaining P0 means split/restart, not a third round or weakened checks. Zero P0 is necessary before implementation, not proof of completion. After it, allocate the one approved ticket, execute red→green verifiers/materializer and all checks, complete code/security review and deliver portable evidence at local review. Missing native/behavioral/rollback results prevent closing the ticket.

## Round-2 nonblocking corrections

Captured review inputs are preserved under review/round-2-inputs. Explicit -d argv in historical scenarios 003/008 is never projected; new blog convention is separately exercised. The E9 label was corrected without changing case inputs/rubrics. Any new regression fails acceptance; baseline-only failures cannot waive it. Missing mandatory checks keep the ticket unclosed.
