# Traceability

All rows are proposed. Existing seams are reused; new/materially changed seams need owner
confirmation with the test plan. The specification is authoritative for each contract.

| Type | Field / case | Boundary | Expected behavior | AC | Test |
|---|---|---|---|---|---|
| Migration | repository, refs, prerequisites, M0 | observed remote → trusted policy | full pins; pending PR is not landed | 01 | P01 |
| Inventory | complete path delta, modes, blobs, additions/deletions | main/staging → baseline | every difference classified; ambiguity stops | 01,02 | P01,P02 |
| Candidate | new article and revision at published path | staging → main | both remain excluded until individually approved | 02,08 | P02,P14 |
| Baseline | engineering/management and shared patches | baseline PR → main | individually approved exact changes only | 02,03 | P02,P03 |
| Preservation | URLs, article bytes, time, images | baseline → staging | all unapproved blobs/metadata unchanged except recorded approvals | 02 | P02 |
| Validation | immutable fixtures and exact successors | historical → current | original assertions retained; no folder waiver | 03 | P03 |
| Validation | target role | target/base → validator | trusted role; candidate cannot select permissive policy | 03,07 | P03,P12 |
| Admission | explicit version | CLI plan → v1/v2 | old contract unchanged; unknown version refused | 03,04 | P03,P04 |
| Admission | clean A already integrated as topic | staging reachability → v2 | accept clean owned topic, reject integration ancestry | 04 | P04,P05 |
| Admission | B added then reverted | complete graph → source | reject regardless of clean final diff | 04 | P05 |
| Admission | main refresh, dependencies, merges | graph/ownership → source | current main ancestor; only reviewed main merges/dependencies | 04 | P06 |
| Registry | all articles/revisions, assets, shared paths | inventory → admission | unknown/omitted/overlapping entries block | 01,04,08 | P01,P07 |
| Legacy | old/new source, paths/hashes, approval | contaminated history → migrated source | explicit new provenance; old rejection remains | 03,04 | P08 |
| Sync | current pins and expected tree | main event → disposable merge | compute/validate independently; ignore stale event pins | 05,06 | P09,P10 |
| Sync | ancestry no-op, conflict and failed check | merge → operation result | no-op or exact failure; target unchanged | 05 | P09 |
| Sync | ticket branch ownership, non-force updates | operation → branch/PR | one owned branch and one open PR; unrelated objects untouched | 05,06 | P10,P11 |
| Sync | coalescing, drift, concurrency | simultaneous operations → writer | serialize participants; re-read latest refs, expire stale result | 06 | P10,P11 |
| Remote | unknown outcome, timeout, retries | API → recorded operation | readback before at most three retries; no duplicate | 05,06 | P11 |
| Actions | trigger suppression, dispatch, correlation | writer → validation run | actual exact-input successful run required | 07 | P12,P13 |
| Security | token scopes, candidate text/code | untrusted source → automation | no shell injection or writer credential in build; trusted policy | 07,08 | P12,P16 |
| Activation | permissions/protection/merge method | proposal → live automation | authorized verified preconditions or blocked | 07 | P13 |
| Publication | exactly selected A and dependencies | current main → candidate | no whole staging projection or B | 08 | P14 |
| Publication | shared listing/navigation/config | shared file → main | exact approved patches; B cannot hide behind path permission | 08 | P14,P15 |
| Publication | regular files, aliases, includes | source → build projection | exact tree; no new links/submodules/escaping reads | 08 | P16 |
| Build | command/toolchain/isolation/receipt | candidate → output | actual isolated build; failures remain blocked | 08 | P16,P17 |
| Output | route/search/RSS/prose/public asset | output → exclusion claim | complete scan; signatures supplementary, missing evidence unverified | 08 | P15,P17 |
| Approval | source/base/tree/policy/deployed SHA | owner preview → PR readiness | exact binding; drift renews approval | 09 | P18 |
| Landing | head/base guards, actual tree | PR → main | readiness distinct from observed landing; mismatch incident | 07,09 | P13,P18 |
| Website | staging/production served identity | Git/build → browser/HTTP | observed deployed commit only; URL/tip alone insufficient | 09 | P19 |
| Lifecycle | selected identity, new revision, remaining B | main landing → staging/registry | preserve article/B; retire only landed revision | 09 | P20 |
| Recovery | revert and re-publication | current main → new PR | new pins/authority, preserve unrelated publications | 09 | P20 |
| Skill | mode, capability, authorization | request → agent actions | right local/workflow route; no invented remote command | 10 | P21 |
| Packaging | canonical/generated copies, policy | draft → future installation | four packages, two runtimes, unchanged old references | 03,10 | P22 |
| Tracker | main/staging receipts, approval, done | PR result → ticket | preserve ADR-0006; no premature done | 10 | P23 |
| Scope | deployment, remote mutation, activation | planning → delivery | no implementation or external mutation in this round | 06,10 | P24 |

AC references in this table use the numeric suffix of `AC-NN` in spec.en.md.
