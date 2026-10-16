# Supplement traceability

Parent frozen epic AC03/05/06/07/09/10 and P13 remain intact. This table elaborates the four recorded prerequisites; it does not add passing evidence to original P13 or replace its 24-row allocation. Original P13 a–l subcase definitions live in sibling preparation/test-matrix.md.

| Type / fields | Trust boundary / negative dimensions | Supplement acceptance | Owner / tests | Parent / remote follow-up |
|---|---|---|---|---|
| Admission: repository, main, role, literal path/mode/hash, approval | Trusted external approval → current policy; absent/forged/candidate-provided/digest substitution | A1/A2 | A, PA-01/02/03/04 | AC03/05/09; P13 a/c/e |
| Workflow bytes and source identities | Policy → prepare/export/readback, main ↔ staging; undeclared .github, wildcard/traversal/duplicate/link/submodule/wrong role/hash/mode, drift | A2/A3/K1 | A, PA-02/03/04/05/06 | AC03/05/07; P13 a/c/h |
| Runtime: versions/deps/isolation/history/refs | Host → job; missing runtime/capability, shallow/missing refs, installation/fallback | B1 | B, PB-01/06 | AC06/09; P13 a/e |
| Registry/runtime: root/UID/mode/type/link-count/containment/open identity/read stability/digests/repo/role/source | Independent approval → fresh writer and validator; each explicit B2 snapshot predicate, tamper/link/identity/immutability; owner/race fixture limits declared | B2 | B, PB-02/03/06 | AC03/06/09; P13 a/e/h |
| Credential / verified flags / probes | Writer/reporter/validator → candidate process; secret escape or invented observed evidence | B1/B2/B3/C2/K3 | B, PB-01/04/06; C, PC-03 | AC06/09; P13 a/b/e |
| Journal: repo/op/retry/host; scheduling group | Per-job → durable shared writer state; unknown outcome, cancel, temporary lock overclaim, validation deadlock | B3 | B, PB-05 | AC06/09; P13 i/j |
| Run: repo/op/main/stage/head/tree/policy/workflow/run/event/reporter | Trusted-main run/API → candidate-head check; wrong identity, non-success, duplicate, spoof, ack only | C1/C2 | C, PC-01/02/03 | AC06/09; P13 b/c/d |
| Head H1/H2, stage S1/S2, main/policy/workflow | Before/after API observation → point-in-time readiness; drift/unknown write/independent actors | C3/C4 | C, PC-04/05/06/07 | AC06/09; P13 f/g/h/i/l |
| Check name/source, actor, strict capability/config identity | Reporter → readiness gate; missing/bypass/changed protection, fixture vs observed evidence | C2/C4 | C, PC-03/05/07 | AC06/09; P13 b/f/g/l |
| Historical PR: repo/branch/number/base/head/merge/tree/actor/type/approval/ancestry | Manual merged history → new owned op; absent/forged/mutated/reopened/unmerged/ambiguous receipt | D1/D2 | D, PD-01/02/03 | AC06/09; P13 a/i/k |
| Branch lifecycle, unrelated PRs, old matching owned op | No-op/ready → enumeration/recovery; unverified/mismatched recreation refuses, exact parent D4 owned recovery retained; duplicate/reopen/force/body rewrite | D1/D2/D3 | D, PD-01/02/03/04 | AC06/09; P13 i/k |
| Candidate/article/assets/history/aliases/oracles | Source/target ownership and local proof → actual landing | K1/K2/K3/A3 | All owners; PA-06 and existing preservation suites in every ticket | AC03/05/07/10; P13 e/l |
| Ticket ids/status/edges; original test plan | Proposal → tracker / local → live; premature allocation/done, dependency cycle, fake remote pass | K2/K3/dependencies | Documentary graph/table checks; all local rows NOT WRITTEN/NOT RUN | P13 a–l remain NOT RUN |

## Source anchors (baseline, not implementation instructions)

- scripts/publication_current.py: policy() and prepare() independently reject `.github/`; both need the bounded successor. Exact common records alone cannot bypass either guard.
- scripts/publication_remote.py and scripts/publication_remote_git.py: trusted dispatch correlation, scoped reporter gap, no-op ordering, PR ownership/bootstrap and branch lifecycle guards.
- scripts/staging-sync-remote.py and maintenance/publication-workflow/: current external config/runtime and inactive templates. State and lock scope must not be overstated.
- sibling preparation/plan.en.md Task 2 items 1–4; authorization.md and test-matrix.md; evidence/landing-audit.json and canonical-pr-lifecycle.json. Four blockers are code-path and prerequisite findings; no remote controller failure is claimed.
- docs/agents/issue-tracker.md, review.md, runtime.md, workflow.md; CONTEXT.md and existing ADRs: local tracker, immutable historical evidence, separate capability/landing proof. Old CONTEXT ticket-state prose is historical; actual target snapshots and approved later receipts govern current status.

The captured source packet includes the actual pinned main tree, working/untracked inventory, diff, prior preparation artifacts and this supplement. Review exactly one axis against the frozen prompt and packet; do not execute candidate code or perform remote mutation.
