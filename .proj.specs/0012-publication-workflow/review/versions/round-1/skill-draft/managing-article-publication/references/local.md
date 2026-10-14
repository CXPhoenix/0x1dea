# Local preview and prepare contract

Use the repository's [CLI](../../../scripts/article-publication.py) and its `--help`.
Run from the repository root; choose fresh output storage outside the source repo.
Commands use installed Python/Git and have no network/installation step:

```sh
python3 scripts/article-publication.py preview --plan /absolute/plan.json --output /absolute/new-preview
python3 scripts/article-publication.py prepare --plan /absolute/plan.json --output /absolute/new-candidate
python3 scripts/article-publication.py verify --plan /absolute/plan.json --output /absolute/new-candidate
python3 scripts/article-publication.py verify --plan /absolute/plan.json --output /absolute/new-candidate --build-output /absolute/dist
```

## Plan

Strict version 1 JSON has exactly `version`, `repository`, `main`, `staging`,
`articles`, `dependencies`, `selected`. `repository` is absolute. `main` and `staging`
have exactly `ref`, `sha`. Each article/dependency has exactly `id`, `ref`, `sha`,
`paths`. SHAs are full lowercase 40-character commit ids matching current local refs.
Ids are unique; each paths array is nonempty, exact, unique and equals that source's
complete diff from pinned main, including deletions. No glob or directory allowlists.
`selected` contains known article ids: at least one for preview, exactly one for prepare.
List known unselected article heads too; verification checks the complete plan's pins.

A synthetic example (replace every SHA using the inspected refs):

```json
{
  "version": 1,
  "repository": "/absolute/repository",
  "main": {"ref": "main", "sha": "0000000000000000000000000000000000000000"},
  "staging": {"ref": "staging", "sha": "0000000000000000000000000000000000000000"},
  "articles": [
    {"id": "article-a", "ref": "post/article-a", "sha": "1111111111111111111111111111111111111111", "paths": ["blog/post/article-a.md"]},
    {"id": "article-b", "ref": "post/article-b", "sha": "2222222222222222222222222222222222222222", "paths": ["blog/post/article-b.md"]}
  ],
  "dependencies": [],
  "selected": ["article-a"]
}
```

Selected and dependency heads must descend from pinned main and exclude staging-only
ancestry and other article heads. Content reverted after an unwanted merge remains
contaminated. Hotfix main changes require a new plan and refreshed independent heads.
Shared images/configuration are explicit exact-path dependencies or owned article changes;
review executable configuration separately before any build. Complete article enumeration
and correct ownership remain the operator's responsibility: the CLI cannot infer intent
or establish historical provenance for undeclared/cherry-picked content from bytes alone.

## Candidate and receipt

Candidate tree reconstruction uses committed Git blobs only; dirty source files are
preserved, never silently included. Git object writes go to disposable storage. Multiple
changes to one text file use Git three-way merge-file; unresolved conflicts stop before
output installation. No source commits/branches/merges are created. The receipt records
pins, complete Git tree SHA, SHA-256 file inventory, changed paths and article inventory.

The current main contains three management-only baseline aliases. Their exact paths,
mode and literal bytes remain in the Git source manifest/tree; the regular-file export
omits them and lists `omitted_baseline_aliases`. They are never followed. New/changed
links and submodules are rejected. `candidate/` is a build projection, not a full checkout.

Verify recomputes the entire receipt and candidate projection from pinned sources.
Changed refs, file modes/bytes, extra files, symlinks or receipt edits fail. Receipts are
local evidence, not signed attestations. Recheck immediately before later authorized use.
No concurrent writer may change the source refs or candidate during a check.

## Build and output limits

The CLI does not execute builds. Use the existing reviewed VitePress build command only
inside an available OS-enforced boundary: candidate/toolchain read access, disposable
writes and no network. Probe capability with synthetic external-file sentinels first.
No sandbox installation, persistent permission or host security-setting changes.
An unavailable boundary means `build-isolation blocked`; complete preparation and
other checks. New executable Markdown/imports are refused; fenced teaching examples
remain data. Includes/snippets with ambiguous or escaping paths are refused before build.
These static checks are conservative, not a parser-complete sandbox substitute.

`verify --build-output` scans an existing regular-file output tree and binds its inventory
to the verification response; it does not prove how/when that build was produced or that
OS isolation was used. Record separate actual build command, pins/tree, toolchain and
isolation receipt before claiming build verification. Baseline main content is allowed.
The scan detects new unselected `.html` routes, exclusive asset bytes/hashes and normalized
prose paragraphs of at least 80 characters absent from allowed sources. It covers all
output files, including index/search/RSS/assets. Missing identifiable signatures produces
`exclusion-unverified`. A pass is only supplementary detection: rewrites, transformations,
short fragments, custom routing and escaped/encoded output can evade signatures. The
primary assurance is reconstructed source tree plus exact allowed diff, followed by a
reviewed, isolated build. Neither source nor output checks prove confidentiality.

In phase 1 every successful response remains `publishable: false`; publication authority
comes only from a later explicit user instruction for an exact reviewed candidate.
